"""Crafting Simulator — weighted rolling engine + sequence executor.

Simulates PoE 2 crafting by rolling mods according to their weights,
enforcing exclusion groups, and tracking item state through sequences
of currency operations.

Usage:
    from simulator import CraftingSimulator
    sim = CraftingSimulator()
    item = sim.create_item("ring", ilvl=80)
    sim.apply_currency(item, "orb_of_transmutation")
    sim.apply_currency(item, "exalted_orb")
    print(item)
"""

import random
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).parent
RESOURCES = PROJECT_ROOT / "resources"
PROLOG_FILE = PROJECT_ROOT / "poe2_crafting.pl"


# ============================================================================
# Data Loading
# ============================================================================

def _load_mod_pool() -> dict[tuple[str, str], list[dict]]:
    """Load mod groups keyed by (category, slot) -> list of mod dicts."""
    pl = PROLOG_FILE.read_text()
    for consult in re.findall(r":- (?:consult|load_files)\('([^']+)'", pl):
        data_path = PROJECT_ROOT / consult
        if data_path.exists():
            pl += "\n" + data_path.read_text()

    pool: dict[tuple[str, str], list[dict]] = {}
    for m in re.finditer(
        r"mod_group\((\w+),\s*'?([^',]+)'?,\s*'([^']*)',\s*\[([^\]]*)\],\s*(\d+),\s*(\d+),\s*(\d+),\s*(\w+)\)",
        pl
    ):
        cat = m.group(1)
        group = m.group(2)
        desc = m.group(3)
        tags = [t.strip() for t in m.group(4).split(",") if t.strip()]
        weight = int(m.group(5))
        max_ilvl = int(m.group(6))
        tier_count = int(m.group(7))
        slot = m.group(8)

        # Parse roll range from description: "(#-#)" pattern
        roll_min, roll_max = _parse_roll_range(desc)

        mod = {
            "group": group,
            "description": desc,
            "tags": tags,
            "weight": weight,
            "max_ilvl": max_ilvl,
            "tier_count": tier_count,
            "slot": slot,
            "roll_min": roll_min,
            "roll_max": roll_max,
        }

        key = (cat, slot)
        pool.setdefault(key, []).append(mod)

    return pool


def _parse_roll_range(desc: str) -> tuple[int, int]:
    """Extract roll range from description like '(40-60)% increased ...'."""
    m = re.search(r'\((\d+)-(\d+)\)', desc)
    if m:
        return int(m.group(1)), int(m.group(2))
    # Single value: '+# to ...' — no range
    return 0, 0


def _normalize_stat_text(text: str) -> str:
    """Normalize a stat text pattern for fuzzy matching.

    Strips numbers, normalizes whitespace, lowercases.
    Converts '(40-60)' style ranges to '#',
    and standalone digits to '#'.
    """
    text = text.lower().strip()
    # Replace (N-M) range patterns with a generic marker
    text = re.sub(r'\(\d+-\d+\)', '#', text)
    # Replace standalone numbers with #
    text = re.sub(r'\d+', '#', text)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    return text


def _load_exclusion_groups() -> list[dict]:
    """Load exclusion groups from resource file."""
    eg_file = RESOURCES / "exclusion_groups.pl"
    if not eg_file.exists():
        return []
    content = eg_file.read_text()
    groups = []
    for m in re.finditer(
        r"exclusion_group\(poe2,\s*(\w+),\s*'([^']*)',\s*\[([^\]]*)\]\)",
        content
    ):
        raw_patterns = m.group(3)
        patterns = []
        if raw_patterns.strip():
            for p in re.finditer(r"'([^']*)'", raw_patterns):
                patterns.append(p.group(1).strip())
        groups.append({
            "id": m.group(1),
            "description": m.group(2),
            "patterns": patterns,
        })
    return groups


def _load_exclusions() -> list[dict]:
    """Load modifier exclusions from resource file."""
    me_file = RESOURCES / "modifier_exclusions.pl"
    if not me_file.exists():
        return []
    content = me_file.read_text()
    exclusions = []
    for m in re.finditer(
        r"modifier_exclusion\(poe2,\s*'([^']*)',\s*\[([^\]]*)\],\s*'([^']*)'\)",
        content
    ):
        exclude_from = [e.strip().strip("'\"") for e in m.group(2).split(",") if e.strip()]
        exclusions.append({
            "pattern": m.group(1),
            "exclude_from": exclude_from,
            "comment": m.group(3),
        })
    return exclusions


def _load_omens() -> dict[str, dict]:
    """Load omen facts from poe2_crafting.pl."""
    pl = PROLOG_FILE.read_text()
    omens: dict[str, dict] = {}
    for m in re.finditer(
        r"omen\(poe2,\s*(\w+),\s*(\w+),\s*(\w+),\s*(\w+)\)",
        pl
    ):
        name = m.group(1)
        omens[name] = {
            "name": name,
            "currency": m.group(2),
            "effect": m.group(3),
            "slot_restriction": m.group(4),
        }
    return omens


# ============================================================================
# Item State
# ============================================================================

MAX_PREFIXES = 3
MAX_SUFFIXES = 3


@dataclass
class RolledMod:
    """A single mod rolled on an item."""
    group: str           # mod group ID (e.g. 'IncreasedLife')
    description: str     # human-readable (e.g. '(70-79)% increased maximum Life')
    tags: list[str]      # mod tags (e.g. ['life'])
    slot: str            # 'prefix' or 'suffix'
    roll: int = 0        # actual rolled value (within range)
    tier: int = 0        # tier number (1 = best)

    def __str__(self):
        if self.roll:
            return f"[{self.slot[0].upper()}] {self.description} (rolled {self.roll})"
        return f"[{self.slot[0].upper()}] {self.description}"


@dataclass
class Item:
    """Represents an item being crafted."""
    category: str           # e.g. "ring", "helmet_str"
    ilvl: int               # item level
    rarity: str = "normal"  # normal, magic, rare, unique
    prefixes: list[RolledMod] = field(default_factory=list)
    suffixes: list[RolledMod] = field(default_factory=list)
    quality: int = 0
    corrupted: bool = False
    history: list[str] = field(default_factory=list)

    @property
    def all_mods(self) -> list[RolledMod]:
        return self.prefixes + self.suffixes

    @property
    def prefix_count(self) -> int:
        return len(self.prefixes)

    @property
    def suffix_count(self) -> int:
        return len(self.suffixes)

    @property
    def mod_count(self) -> int:
        return self.prefix_count + self.suffix_count

    def has_mod(self, group: str) -> bool:
        return any(m.group == group for m in self.all_mods)

    def get_mod(self, group: str) -> Optional[RolledMod]:
        for m in self.all_mods:
            if m.group == group:
                return m
        return None

    def __str__(self):
        lines = [f"[{self.rarity.upper()}] {self.category} (ilvl {self.ilvl})"]
        if self.prefixes:
            lines.append("  Prefixes:")
            for m in self.prefixes:
                lines.append(f"    {m}")
        if self.suffixes:
            lines.append("  Suffixes:")
            for m in self.suffixes:
                lines.append(f"    {m}")
        if not self.prefixes and not self.suffixes:
            lines.append("  (no mods)")
        return "\n".join(lines)


# ============================================================================
# Crafting Simulator
# ============================================================================

class CraftingSimulator:
    """Simulates PoE 2 crafting operations."""

    def __init__(self, seed: Optional[int] = None):
        self._rng = random.Random(seed)
        self._mod_pool: dict[tuple[str, str], list[dict]] = _load_mod_pool()
        self._exclusion_groups = _load_exclusion_groups()
        self._exclusions = _load_exclusions()
        self._omens = _load_omens()
        # Build exclusion group membership: group_id -> set of excluded group_ids
        self._exclusion_membership = self._build_exclusion_membership()

    def _build_exclusion_membership(self) -> dict[str, set[str]]:
        """Build a mapping from mod group ID -> set of conflicting mod group IDs.

        For each exclusion group, maps its patterns to actual mod group IDs
        using fuzzy matching on stat text descriptions.
        """
        # Build reverse index: normalized description -> list of mod group IDs
        desc_to_groups: dict[str, list[str]] = {}
        for _key, mods in self._mod_pool.items():
            for mod in mods:
                norm = _normalize_stat_text(mod["description"])
                if norm not in desc_to_groups:
                    desc_to_groups[norm] = []
                if mod["group"] not in desc_to_groups[norm]:
                    desc_to_groups[norm].append(mod["group"])

        membership: dict[str, set[str]] = {}

        for eg in self._exclusion_groups:
            # Map each pattern to mod group IDs
            eg_groups: set[str] = set()
            for pattern in eg["patterns"]:
                norm_pattern = _normalize_stat_text(pattern)
                # Try exact normalized match first
                if norm_pattern in desc_to_groups:
                    eg_groups.update(desc_to_groups[norm_pattern])
                else:
                    # Fuzzy: check if normalized pattern is substring of any description
                    for norm_desc, groups in desc_to_groups.items():
                        if (norm_pattern in norm_desc or
                                norm_desc in norm_pattern):
                            eg_groups.update(groups)

            # Map each group in this exclusion group to all OTHER groups in the group
            for gid in eg_groups:
                if gid not in membership:
                    membership[gid] = set()
                membership[gid].update(eg_groups - {gid})

        return membership

    def create_item(self, category: str, ilvl: int = 80) -> Item:
        """Create a new normal item."""
        return Item(category=category, ilvl=ilvl)

    # ------------------------------------------------------------------
    # Core Rolling
    # ------------------------------------------------------------------

    def roll_mod(
        self,
        category: str,
        slot: str,
        ilvl: int,
        exclude_groups: Optional[set[str]] = None,
        guarantee_tag: Optional[str] = None,
    ) -> Optional[RolledMod]:
        """Roll a single mod from the pool for a given category/slot.

        Args:
            category: item category (e.g. "ring")
            slot: "prefix" or "suffix"
            ilvl: item level (filters mods by max_ilvl)
            exclude_groups: set of mod group IDs already on the item (for exclusion checking)
            guarantee_tag: if set, only roll mods with this tag (for essences)

        Returns:
            RolledMod or None if no valid mods available.
        """
        pool = self._mod_pool.get((category, slot), [])
        if not pool:
            return None

        # Filter by ilvl
        candidates = [m for m in pool if m["max_ilvl"] >= ilvl]
        if not candidates:
            return None

        # Filter by guarantee tag (essences)
        if guarantee_tag:
            candidates = [m for m in candidates if guarantee_tag in m["tags"]]
            if not candidates:
                return None

        # Filter by exclusion groups
        if exclude_groups:
            excluded = self._get_excluded_groups(exclude_groups)
            # Also exclude groups already on the item (no duplicate groups)
            excluded = excluded | exclude_groups
            candidates = [m for m in candidates if m["group"] not in excluded]
            if not candidates:
                return None

        # Weighted random selection
        weights = [m["weight"] for m in candidates]
        total = sum(weights)
        if total == 0:
            return None

        chosen = self._rng.choices(candidates, weights=weights, k=1)[0]

        # Roll the value within the range
        roll = 0
        if chosen["roll_min"] and chosen["roll_max"]:
            roll = self._rng.randint(chosen["roll_min"], chosen["roll_max"])

        return RolledMod(
            group=chosen["group"],
            description=chosen["description"],
            tags=chosen["tags"],
            slot=chosen["slot"],
            roll=roll,
        )

    def _get_excluded_groups(self, existing_groups: set[str]) -> set[str]:
        """Given mod groups on the item, return all groups that would conflict.

        Uses the pre-built exclusion membership mapping to find which groups
        conflict with already-present mod groups.
        """
        excluded = set()
        for gid in existing_groups:
            if gid in self._exclusion_membership:
                excluded.update(self._exclusion_membership[gid])
        return excluded - existing_groups  # don't exclude what's already there

    # ------------------------------------------------------------------
    # Currency Operations
    # ------------------------------------------------------------------

    def apply_currency(self, item: Item, currency: str) -> bool:
        """Apply a currency orb to an item.

        Returns True if the currency was applied successfully, False if
        the preconditions aren't met.
        """
        if item.corrupted:
            item.history.append(f"FAILED: {currency} on corrupted item")
            return False

        handler = getattr(self, f"_apply_{currency}", None)
        if handler:
            return handler(item)

        # Unknown currency — log and skip
        item.history.append(f"SKIPPED: unknown currency '{currency}'")
        return False

    def apply_currency_with_omen(self, item: Item, currency: str, omen_name: str) -> bool:
        """Apply a currency orb with an omen modifier.

        The omen modifies the behavior of the currency application.
        Returns True if the currency was applied successfully.
        """
        if item.corrupted:
            item.history.append(f"FAILED: {currency}+{omen_name} on corrupted item")
            return False

        # Look up the omen
        omen = self._omens.get(omen_name)
        if not omen:
            item.history.append(f"FAILED: unknown omen '{omen_name}'")
            return False

        # Verify omen matches the currency
        if omen["currency"] != currency:
            item.history.append(
                f"FAILED: omen '{omen_name}' targets '{omen['currency']}', not '{currency}'"
            )
            return False

        effect = omen["effect"]
        slot = omen["slot_restriction"]

        # Dispatch to effect-specific handler
        handler = self._get_omen_handler(effect)
        if handler:
            return handler(item, currency, omen_name, slot)

        # Fall back to normal currency behavior with omen logged
        item.history.append(f"OMEN({omen_name}): effect '{effect}' not implemented")
        return self.apply_currency(item, currency)

    def _get_omen_handler(self, effect: str):
        """Get the handler function for an omen effect."""
        handlers = {
            "removes_only_prefixes": self._omen_removes_only_slot,
            "removes_only_suffixes": self._omen_removes_only_slot,
            "max_prefixes": self._omen_max_slot,
            "max_suffixes": self._omen_max_slot,
            "adds_only_prefixes": self._omen_adds_only_slot,
            "adds_only_suffixes": self._omen_adds_only_slot,
            "adds_two_mods": self._omen_adds_two_mods,
            "removes_two_mods": self._omen_removes_two_mods,
            "adds_same_tag_mod": self._omen_adds_same_tag_mod,
            "removes_lowest_level_mod": self._omen_removes_lowest_level_mod,
        }
        # All other effects get the placeholder handler
        placeholder_effects = {
            "wont_destroy_item", "upgrades_to_random_unique",
            "rerolls_implicit_only", "sanctifies_item", "always_changes",
            "removes_desecrated_only", "replaces_all_mods_and_corrupts",
            "enables_recombination", "consumes_quality_for_targeting",
            "guarantees_ulaman_mod", "guarantees_amanamu_mod",
            "guarantees_kurgal_mod", "reroll_desecrated_options",
        }
        if effect in placeholder_effects:
            return self._omen_placeholder
        return handlers.get(effect)

    def _omen_removes_only_slot(self, item: Item, currency: str, omen_name: str, slot: str) -> bool:
        """Omen: chaos/annul removes mods only from one slot (prefix or suffix)."""
        target_slot = "prefix" if slot == "prefix" else "suffix"

        if currency == "chaos_orb":
            if item.rarity != "rare":
                item.history.append(f"FAILED: {currency}+{omen_name} requires rare item")
                return False
            # Remove all mods from target slot, keep the other slot
            mods_to_remove = list(item.prefixes if target_slot == "prefix" else item.suffixes)
            if not mods_to_remove:
                item.history.append(f"FAILED: {currency}+{omen_name} — no {target_slot} mods to remove")
                return False
            if target_slot == "prefix":
                item.prefixes.clear()
            else:
                item.suffixes.clear()
            # Re-roll mods for the cleared slot only
            max_in_slot = MAX_PREFIXES if target_slot == "prefix" else MAX_SUFFIXES
            count = self._rng.randint(1, max_in_slot)
            for _ in range(count):
                if (target_slot == "prefix" and item.prefix_count < MAX_PREFIXES) or \
                   (target_slot == "suffix" and item.suffix_count < MAX_SUFFIXES):
                    existing_groups = {m.group for m in item.all_mods}
                    mod = self.roll_mod(item.category, target_slot, item.ilvl,
                                        exclude_groups=existing_groups)
                    if mod:
                        self._add_mod(item, mod)
            item.history.append(
                f"{currency}+{omen_name} → rerolled {target_slot}s ({item.mod_count} total)"
            )
            return True

        if currency == "orb_of_annulment":
            target_mods = list(item.prefixes if target_slot == "prefix" else item.suffixes)
            if not target_mods:
                item.history.append(f"FAILED: {currency}+{omen_name} — no {target_slot} mods")
                return False
            removed = self._rng.choice(target_mods)
            if removed.slot == "prefix":
                item.prefixes.remove(removed)
            else:
                item.suffixes.remove(removed)
            if item.mod_count == 0:
                item.rarity = "normal"
            elif item.mod_count <= 2 and item.rarity == "rare":
                item.rarity = "magic"
            item.history.append(f"{currency}+{omen_name} → removed {removed.group} ({target_slot})")
            return True

        item.history.append(f"FAILED: {currency}+{omen_name} — unsupported currency")
        return False

    def _omen_max_slot(self, item: Item, currency: str, omen_name: str, slot: str) -> bool:
        """Omen: alchemy maximizes mods in a specific slot."""
        if currency != "orb_of_alchemy":
            item.history.append(f"FAILED: {omen_name} only works with orb_of_alchemy")
            return False
        if item.rarity != "normal" or item.mod_count > 0:
            item.history.append(f"FAILED: {currency}+{omen_name} requires normal item with no mods")
            return False

        item.rarity = "rare"
        target_slot = "prefix" if slot == "prefix" else "suffix"
        other_slot = "suffix" if target_slot == "prefix" else "prefix"
        max_target = MAX_PREFIXES if target_slot == "prefix" else MAX_SUFFIXES

        # Max out the target slot
        for _ in range(max_target):
            existing_groups = {m.group for m in item.all_mods}
            mod = self.roll_mod(item.category, target_slot, item.ilvl,
                                exclude_groups=existing_groups)
            if mod:
                self._add_mod(item, mod)

        # Fill remaining with other slot (up to 6 total)
        remaining = 6 - item.mod_count
        for _ in range(remaining):
            if (other_slot == "prefix" and item.prefix_count >= MAX_PREFIXES) or \
               (other_slot == "suffix" and item.suffix_count >= MAX_SUFFIXES):
                break
            existing_groups = {m.group for m in item.all_mods}
            mod = self.roll_mod(item.category, other_slot, item.ilvl,
                                exclude_groups=existing_groups)
            if mod:
                self._add_mod(item, mod)

        item.history.append(f"{currency}+{omen_name} → {item.mod_count} mods (max {target_slot}s)")
        return True

    def _omen_adds_only_slot(self, item: Item, currency: str, omen_name: str, slot: str) -> bool:
        """Omen: regal/exalt adds mod only to specified slot."""
        target_slot = "prefix" if slot == "prefix" else "suffix"

        if currency == "regal_orb":
            if item.rarity != "magic":
                item.history.append(f"FAILED: {currency}+{omen_name} requires magic item")
                return False
            if target_slot == "prefix" and item.prefix_count >= MAX_PREFIXES:
                item.history.append(f"FAILED: {currency}+{omen_name} — {target_slot}s full")
                return False
            if target_slot == "suffix" and item.suffix_count >= MAX_SUFFIXES:
                item.history.append(f"FAILED: {currency}+{omen_name} — {target_slot}s full")
                return False

            item.rarity = "rare"
            existing_groups = {m.group for m in item.all_mods}
            mod = self.roll_mod(item.category, target_slot, item.ilvl,
                                exclude_groups=existing_groups)
            if mod:
                self._add_mod(item, mod)
                item.history.append(f"{currency}+{omen_name} → added {mod.group} ({target_slot})")
            else:
                item.history.append(f"{currency}+{omen_name} → no valid {target_slot} mod")
            return True

        if currency == "exalted_orb":
            if item.rarity != "rare":
                item.history.append(f"FAILED: {currency}+{omen_name} requires rare item")
                return False
            if target_slot == "prefix" and item.prefix_count >= MAX_PREFIXES:
                item.history.append(f"FAILED: {currency}+{omen_name} — {target_slot}s full")
                return False
            if target_slot == "suffix" and item.suffix_count >= MAX_SUFFIXES:
                item.history.append(f"FAILED: {currency}+{omen_name} — {target_slot}s full")
                return False

            existing_groups = {m.group for m in item.all_mods}
            mod = self.roll_mod(item.category, target_slot, item.ilvl,
                                exclude_groups=existing_groups)
            if mod:
                self._add_mod(item, mod)
                item.history.append(f"{currency}+{omen_name} → added {mod.group} ({target_slot})")
            else:
                item.history.append(f"{currency}+{omen_name} → no valid {target_slot} mod")
            return True

        item.history.append(f"FAILED: {currency}+{omen_name} — unsupported currency")
        return False

    def _omen_adds_two_mods(self, item: Item, currency: str, omen_name: str, slot: str) -> bool:
        """Omen: greater_exaltation adds 2 mods instead of 1."""
        if currency != "exalted_orb":
            item.history.append(f"FAILED: {omen_name} only works with exalted_orb")
            return False
        if item.rarity != "rare":
            item.history.append(f"FAILED: {currency}+{omen_name} requires rare item")
            return False
        if item.mod_count >= 6:
            item.history.append(f"FAILED: {currency}+{omen_name} — item is full")
            return False

        added = []
        for _ in range(2):
            if item.prefix_count >= MAX_PREFIXES and item.suffix_count >= MAX_SUFFIXES:
                break
            mod = self._roll_one_mod_respecting_slots(item)
            if mod:
                self._add_mod(item, mod)
                added.append(mod.group)

        if added:
            item.history.append(f"{currency}+{omen_name} → added {', '.join(added)}")
        else:
            item.history.append(f"{currency}+{omen_name} → no valid mods")
        return True

    def _omen_removes_two_mods(self, item: Item, currency: str, omen_name: str, slot: str) -> bool:
        """Omen: greater_annulment removes 2 mods instead of 1."""
        if currency != "orb_of_annulment":
            item.history.append(f"FAILED: {omen_name} only works with orb_of_annulment")
            return False
        if item.mod_count == 0:
            item.history.append(f"FAILED: {currency}+{omen_name} — no mods to remove")
            return False

        removed = []
        for _ in range(min(2, item.mod_count)):
            all_mods = item.all_mods
            if not all_mods:
                break
            mod = self._rng.choice(all_mods)
            if mod.slot == "prefix":
                item.prefixes.remove(mod)
            else:
                item.suffixes.remove(mod)
            removed.append(mod.group)

        if item.mod_count == 0:
            item.rarity = "normal"
        elif item.mod_count <= 2 and item.rarity == "rare":
            item.rarity = "magic"

        item.history.append(f"{currency}+{omen_name} → removed {', '.join(removed)}")
        return True

    def _omen_adds_same_tag_mod(self, item: Item, currency: str, omen_name: str, slot: str) -> bool:
        """Omen: homogenising exaltation/coronation adds a mod with the same tag."""
        if item.rarity not in ("rare", "magic"):
            item.history.append(f"FAILED: {currency}+{omen_name} requires magic or rare item")
            return False
        if item.mod_count == 0:
            item.history.append(f"FAILED: {currency}+{omen_name} — item has no mods to match tags")
            return False
        if item.prefix_count >= MAX_PREFIXES and item.suffix_count >= MAX_SUFFIXES:
            item.history.append(f"FAILED: {currency}+{omen_name} — item is full")
            return False

        # Collect all tags from existing mods
        all_tags: set[str] = set()
        for m in item.all_mods:
            all_tags.update(m.tags)
        if not all_tags:
            item.history.append(f"FAILED: {currency}+{omen_name} — existing mods have no tags")
            return False

        tag = self._rng.choice(sorted(all_tags))

        # For regal, upgrade rarity
        if currency == "regal_orb" and item.rarity == "magic":
            item.rarity = "rare"

        mod = self._roll_one_mod_respecting_slots(item, guarantee_tag=tag)
        if mod:
            self._add_mod(item, mod)
            item.history.append(f"{currency}+{omen_name} → added {mod.group} (tag: {tag})")
        else:
            item.history.append(f"{currency}+{omen_name} → no valid mod with tag '{tag}'")
        return True

    def _omen_removes_lowest_level_mod(self, item: Item, currency: str, omen_name: str, slot: str) -> bool:
        """Omen: whittling — chaos removes the lowest-tier mod then re-rolls."""
        if currency != "chaos_orb":
            item.history.append(f"FAILED: {omen_name} only works with chaos_orb")
            return False
        if item.rarity != "rare":
            item.history.append(f"FAILED: {currency}+{omen_name} requires rare item")
            return False

        all_mods = item.all_mods
        if not all_mods:
            item.history.append(f"FAILED: {currency}+{omen_name} — no mods")
            return False

        # Remove mod with lowest roll (proxy for lowest tier)
        lowest = min(all_mods, key=lambda m: m.roll if m.roll else 0)
        if lowest.slot == "prefix":
            item.prefixes.remove(lowest)
        else:
            item.suffixes.remove(lowest)

        if item.mod_count == 0:
            item.rarity = "normal"
        elif item.mod_count <= 2 and item.rarity == "rare":
            item.rarity = "magic"

        # Re-roll one new mod
        mod = self._roll_one_mod_respecting_slots(item)
        if mod:
            self._add_mod(item, mod)

        item.history.append(
            f"{currency}+{omen_name} → removed {lowest.group}, "
            f"added {mod.group if mod else 'nothing'} ({item.mod_count} total)"
        )
        return True

    def _omen_placeholder(self, item: Item, currency: str, omen_name: str, slot: str) -> bool:
        """Placeholder for special omens not yet fully implemented."""
        item.history.append(f"OMEN({omen_name}): effect not yet simulated, applying base {currency}")
        return self.apply_currency(item, currency)

    def _apply_orb_of_transmutation(self, item: Item) -> bool:
        """Normal item → magic with 1-2 mods."""
        if item.rarity != "normal" or item.mod_count > 0:
            item.history.append("FAILED: orb_of_transmutation requires normal item with no mods")
            return False

        item.rarity = "magic"
        # Roll 1-2 mods (1 prefix + 0-1 suffix, or 0-1 prefix + 1 suffix)
        count = self._rng.choice([1, 2])
        slots = self._pick_slots(count, item.category)
        for slot in slots:
            mod = self.roll_mod(item.category, slot, item.ilvl)
            if mod:
                self._add_mod(item, mod)
        item.history.append(f"orb_of_transmutation → {item.mod_count} mods")
        return True

    def _apply_orb_of_alchemy(self, item: Item) -> bool:
        """Normal item → rare with 4-6 mods."""
        if item.rarity != "normal" or item.mod_count > 0:
            item.history.append("FAILED: orb_of_alchemy requires normal item with no mods")
            return False

        item.rarity = "rare"
        # Roll 4-6 mods
        count = self._rng.randint(4, 6)
        self._roll_multiple_mods(item, count)
        item.history.append(f"orb_of_alchemy → {item.mod_count} mods")
        return True

    def _apply_chaos_orb(self, item: Item) -> bool:
        """Rare item → reroll all mods (4-6 new mods)."""
        if item.rarity != "rare":
            item.history.append("FAILED: chaos_orb requires rare item")
            return False

        item.prefixes.clear()
        item.suffixes.clear()
        count = self._rng.randint(4, 6)
        self._roll_multiple_mods(item, count)
        item.history.append(f"chaos_orb → {item.mod_count} mods")
        return True

    def _apply_regal_orb(self, item: Item) -> bool:
        """Magic item → rare, adds 1 mod."""
        if item.rarity != "magic":
            item.history.append("FAILED: regal_orb requires magic item")
            return False

        item.rarity = "rare"
        mod = self._roll_one_mod_respecting_slots(item)
        if mod:
            self._add_mod(item, mod)
        item.history.append(f"regal_orb → {item.mod_count} mods")
        return True

    def _apply_exalted_orb(self, item: Item) -> bool:
        """Rare item → add 1 mod (if slot available)."""
        if item.rarity != "rare":
            item.history.append("FAILED: exalted_orb requires rare item")
            return False
        if item.prefix_count >= MAX_PREFIXES and item.suffix_count >= MAX_SUFFIXES:
            item.history.append("FAILED: exalted_orb — item is full")
            return False

        mod = self._roll_one_mod_respecting_slots(item)
        if mod:
            self._add_mod(item, mod)
            item.history.append(f"exalted_orb → added {mod.group}")
        else:
            item.history.append("exalted_orb → no valid mod (exclusion/full)")
        return True

    def _apply_orb_of_augmentation(self, item: Item) -> bool:
        """Magic item → add 1 mod (if slot available)."""
        if item.rarity != "magic":
            item.history.append("FAILED: orb_of_augmentation requires magic item")
            return False
        if item.prefix_count >= MAX_PREFIXES and item.suffix_count >= MAX_SUFFIXES:
            item.history.append("FAILED: orb_of_augmentation — item is full")
            return False

        mod = self._roll_one_mod_respecting_slots(item)
        if mod:
            self._add_mod(item, mod)
            item.history.append(f"orb_of_augmentation → added {mod.group}")
        else:
            item.history.append("orb_of_augmentation → no valid mod")
        return True

    def _apply_orb_of_annulment(self, item: Item) -> bool:
        """Remove 1 random mod."""
        if item.mod_count == 0:
            item.history.append("FAILED: orb_of_annulment — no mods to remove")
            return False

        all_mods = item.all_mods
        removed = self._rng.choice(all_mods)
        if removed.slot == "prefix":
            item.prefixes.remove(removed)
        else:
            item.suffixes.remove(removed)

        # Downgrade rarity if needed
        if item.mod_count == 0:
            item.rarity = "normal"
        elif item.mod_count <= 2 and item.rarity == "rare":
            item.rarity = "magic"

        item.history.append(f"orb_of_annulment → removed {removed.group}")
        return True

    def _apply_orb_of_chance(self, item: Item) -> bool:
        """Normal item → random rarity (normal/magic/rare/unique)."""
        if item.rarity != "normal":
            item.history.append("FAILED: orb_of_chance requires normal item")
            return False

        # PoE 2 odds: mostly stays normal, small chance magic/rare, tiny unique
        roll = self._rng.random()
        if roll < 0.78:
            item.rarity = "normal"
            item.history.append("orb_of_chance → stayed normal")
        elif roll < 0.95:
            item.rarity = "magic"
            count = self._rng.choice([1, 2])
            slots = self._pick_slots(count, item.category)
            for slot in slots:
                mod = self.roll_mod(item.category, slot, item.ilvl)
                if mod:
                    self._add_mod(item, mod)
            item.history.append(f"orb_of_chance → magic ({item.mod_count} mods)")
        elif roll < 0.995:
            item.rarity = "rare"
            count = self._rng.randint(4, 6)
            self._roll_multiple_mods(item, count)
            item.history.append(f"orb_of_chance → rare ({item.mod_count} mods)")
        else:
            item.rarity = "unique"
            item.history.append("orb_of_chance → unique!")
        return True

    def _apply_essence_of_the_body(self, item: Item) -> bool:
        """Essence: guarantees a life mod, rerolls rest (magic only)."""
        return self._apply_essence(item, "life")

    def _apply_essence_of_wrath(self, item: Item) -> bool:
        """Essence: guarantees a damage mod, rerolls rest (magic only)."""
        return self._apply_essence(item, "damage")

    def _apply_essence(self, item: Item, guarantee_tag: str) -> bool:
        """Apply an essence: guarantees one mod with the tag, rerolls rest."""
        if item.rarity != "magic":
            item.history.append(f"FAILED: essence requires magic item (has {item.rarity})")
            return False

        # Clear existing mods
        item.prefixes.clear()
        item.suffixes.clear()

        # Roll guaranteed mod
        slot = self._rng.choice(["prefix", "suffix"])
        mod = self.roll_mod(item.category, slot, item.ilvl, guarantee_tag=guarantee_tag)
        if mod:
            self._add_mod(item, mod)

        # Roll 1 more mod in the other slot
        other_slot = "suffix" if slot == "prefix" else "prefix"
        mod2 = self.roll_mod(item.category, other_slot, item.ilvl)
        if mod2:
            self._add_mod(item, mod2)

        item.history.append(f"essence → guaranteed {guarantee_tag}, {item.mod_count} mods total")
        return True

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _pick_slots(self, count: int, category: str) -> list[str]:
        """Pick which slots to fill (prefix/suffix)."""
        if count == 1:
            return [self._rng.choice(["prefix", "suffix"])]
        elif count == 2:
            return ["prefix", "suffix"]
        else:
            # For 3+ mods, distribute between prefix and suffix
            prefixes = self._rng.randint(1, min(count - 1, MAX_PREFIXES))
            suffixes = min(count - prefixes, MAX_SUFFIXES)
            return ["prefix"] * prefixes + ["suffix"] * suffixes

    def _roll_one_mod_respecting_slots(
        self, item: Item, guarantee_tag: Optional[str] = None
    ) -> Optional[RolledMod]:
        """Roll one mod, choosing the slot that has room."""
        available_slots = []
        if item.prefix_count < MAX_PREFIXES:
            available_slots.append("prefix")
        if item.suffix_count < MAX_SUFFIXES:
            available_slots.append("suffix")
        if not available_slots:
            return None

        slot = self._rng.choice(available_slots)
        existing_groups = {m.group for m in item.all_mods}
        return self.roll_mod(
            item.category, slot, item.ilvl,
            exclude_groups=existing_groups,
            guarantee_tag=guarantee_tag,
        )

    def _roll_multiple_mods(self, item: Item, count: int):
        """Roll multiple mods for an item (used by alchemy, chaos)."""
        slots = self._pick_slots(count, item.category)
        for slot in slots:
            if (slot == "prefix" and item.prefix_count >= MAX_PREFIXES) or \
               (slot == "suffix" and item.suffix_count >= MAX_SUFFIXES):
                continue
            existing_groups = {m.group for m in item.all_mods}
            mod = self.roll_mod(item.category, slot, item.ilvl, exclude_groups=existing_groups)
            if mod:
                self._add_mod(item, mod)

    def _add_mod(self, item: Item, mod: RolledMod):
        """Add a mod to the item."""
        if mod.slot == "prefix":
            item.prefixes.append(mod)
        else:
            item.suffixes.append(mod)
