"""Recipe verification engine with item state tracking.

Simulates crafting step-by-step, tracking item rarity and mod counts.
Validates preconditions, flags impossible transitions, handles loops,
and treats omen+currency as a single compound step.
"""

from dataclasses import dataclass, field
from typing import Optional


# ============================================================================
# Item State
# ============================================================================

@dataclass
class ItemState:
    """Tracked item state during recipe verification."""
    rarity: str = "normal"          # normal | magic | rare | corrupted
    prefix_count: int = 0
    suffix_count: int = 0
    max_prefixes: int = 3
    max_suffixes: int = 3
    quality: int = 0
    corrupted: bool = False
    fractured: bool = False
    identified: bool = False

    @property
    def total_mods(self) -> int:
        return self.prefix_count + self.suffix_count

    @property
    def has_open_prefix(self) -> bool:
        return self.prefix_count < self.max_prefixes

    @property
    def has_open_suffix(self) -> bool:
        return self.suffix_count < self.max_suffixes

    @property
    def has_open_slot(self) -> bool:
        return self.has_open_prefix or self.has_open_suffix

    @property
    def is_normal(self) -> bool:
        return self.rarity == "normal"

    @property
    def is_magic(self) -> bool:
        return self.rarity == "magic"

    @property
    def is_rare(self) -> bool:
        return self.rarity == "rare"

    def summary(self) -> str:
        parts = [f"{self.rarity}"]
        if self.total_mods > 0:
            parts.append(f"{self.prefix_count}p+{self.suffix_count}s")
        if self.corrupted:
            parts.append("corrupted")
        if self.fractured:
            parts.append("fractured")
        return ", ".join(parts)

    def copy(self) -> "ItemState":
        return ItemState(
            rarity=self.rarity,
            prefix_count=self.prefix_count,
            suffix_count=self.suffix_count,
            max_prefixes=self.max_prefixes,
            max_suffixes=self.max_suffixes,
            quality=self.quality,
            corrupted=self.corrupted,
            fractured=self.fractured,
            identified=self.identified,
        )


# ============================================================================
# Currency Rules — preconditions & postconditions
# ============================================================================

# Each entry: { preconditions dict, postcondition function }
# Precondition keys:
#   rarity: required rarity (str or list of str)
#   min_mods: minimum total mods
#   max_mods: maximum total mods
#   has_mods: must have at least 1 mod
#   no_mods: must have 0 mods
#   open_prefix: must have open prefix slot
#   open_suffix: must have open suffix slot
#   open_slot: must have open prefix OR suffix
#   not_corrupted: must not be corrupted (default True)
#   not_fractured: must not be fractured (default False — allowed by default)

CURRENCY_RULES = {
    "orb_of_transmutation": {
        "pre": {"rarity": "normal", "no_mods": True},
        "post": lambda s: _set_rarity(s, "magic", prefix=1, suffix=1),
    },
    "orb_of_augmentation": {
        "pre": {"rarity": "magic", "open_slot": True},
        "post": lambda s: _add_random_mod(s, 1),
    },
    "orb_of_alchemy": {
        "pre": {"rarity": "normal", "no_mods": True},
        "post": lambda s: _set_rarity(s, "rare", prefix=3, suffix=2),  # 4-6 mods typical
    },
    "chaos_orb": {
        "pre": {"rarity": "rare"},
        "post": lambda s: _reroll_all(s),
    },
    "regal_orb": {
        "pre": {"rarity": "magic"},
        "post": lambda s: _add_random_mod(_set_rarity(s, "rare"), 1),
    },
    "exalted_orb": {
        "pre": {"rarity": "rare", "open_slot": True},
        "post": lambda s: _add_random_mod(s, 1),
    },
    "orb_of_annulment": {
        "pre": {"has_mods": True},
        "post": lambda s: _remove_random_mod(s),
    },
    "divine_orb": {
        "pre": {"has_mods": True},
        "post": lambda s: s,  # rerolls values, not mods
    },
    "vaal_orb": {
        "pre": {},
        "post": lambda s: _corrupt(s),
    },
    "orb_of_chance": {
        "pre": {"rarity": "normal", "no_mods": True},
        "post": lambda s: _set_rarity(s, "magic", prefix=1, suffix=1),  # most common outcome
    },
    "orb_of_scouring": {
        "pre": {},
        "post": lambda s: _set_rarity(s, "normal", prefix=0, suffix=0),
    },
    "fracturing_orb": {
        "pre": {"rarity": "rare", "min_mods": 4},
        "post": lambda s: _fracture(s),
    },
    "essence_of_the_body": {
        "pre": {"rarity": ["normal", "magic"]},
        "post": lambda s: _set_rarity(s, "rare", prefix=max(s.prefix_count, 1), suffix=max(s.suffix_count, 1)),
    },
    "essence_of_wrath": {
        "pre": {},
        "post": lambda s: _set_rarity(s, "rare", prefix=max(s.prefix_count, 1), suffix=max(s.suffix_count, 1)),
    },
    "essence_of_abyss": {
        "pre": {"rarity": ["magic", "rare"]},  # corrupted essence — works on magic/rare
        "post": lambda s: _remove_random_mod(_add_random_mod(s, 1)),  # removes 1, adds 1
    },
    "essence_of_hysteria": {
        "pre": {"rarity": ["magic", "rare"]},  # corrupted essence
        "post": lambda s: _add_random_mod(s, 1),  # adds hysteria mod
    },
    "greater_exalted_orb": {
        "pre": {"rarity": "rare", "open_slot": True},
        "post": lambda s: _add_random_mod(s, 1),  # same as exalt but min ilvl 35
    },
    "perfect_exalted_orb": {
        "pre": {"rarity": "rare", "open_slot": True},
        "post": lambda s: _add_random_mod(s, 1),  # same as exalt but min ilvl 50
    },
    "preserved_cranium": {
        "pre": {"rarity": "rare"},  # desecration — applies to rare jewels
        "post": lambda s: _add_random_mod(s, 1),  # adds a desecrated suffix mod
    },
    "liquid_contempt": {
        "pre": {"rarity": "rare", "has_mods": True},  # removes 1, adds +1 suffix/prefix
        "post": lambda s: s,  # net zero — removes 1 mod, adds 1 crafted mod
    },
    "liquid_ferocity": {
        "pre": {"rarity": "rare", "has_mods": True},  # removes 1, adds effect mod
        "post": lambda s: s,  # net zero — removes 1 mod, adds 1 effect mod
    },
}

# Add generic essence rule (any essence follows same pattern)
ESSENCE_PRE = {"rarity": ["normal", "magic"]}
for _name in list(CURRENCY_RULES.keys()):
    pass  # already handled above

# Catalysts — apply quality, no rarity change
CATALYST_NAMES = [
    "catalyst_physical", "catalyst_fire", "catalyst_cold", "catalyst_lightning",
    "catalyst_chaos", "catalyst_life", "catalyst_mana", "catalyst_defence",
    "catalyst_attack", "catalyst_caster", "catalyst_speed", "catalyst_attribute",
    "flesh_catalyst", "neural_catalyst", "carapace_catalyst",
    "uul_netol_catalyst", "xophs_catalyst", "tuls_catalyst",
    "eshs_catalyst", "chayulas_catalyst", "reaver_catalyst",
    "sibilant_catalyst", "skittering_catalyst", "adaptive_catalyst",
]
for _cat in CATALYST_NAMES:
    CURRENCY_RULES[_cat] = {
        "pre": {"not_corrupted": True},
        "post": lambda s: _add_quality(s, 20),
    }

# Quality items (scraps, whetstones, etchers)
for _qi in ["armourer_scrap", "blacksmith_whetstone", "arcanist_etcher"]:
    CURRENCY_RULES[_qi] = {
        "pre": {"not_corrupted": True},
        "post": lambda s: _add_quality(s, 20),
    }

# Omen → currency mapping (which currency an omen pairs with)
OMEN_CURRENCY_MAP = {
    "sinistral_exaltation": "exalted_orb",
    "dextral_exaltation": "exalted_orb",
    "greater_exaltation": "exalted_orb",
    "catalysing_exaltation": "exalted_orb",
    "sinistral_annulment": "orb_of_annulment",
    "dextral_annulment": "orb_of_annulment",
    "sinistral_crystallisation": "essence",
    "dextral_crystallisation": "essence",
    "sinistral_erasure": "chaos_orb",
    "dextral_erasure": "chaos_orb",
    "sinistral_necromancy": "desecration",
    "dextral_necromancy": "desecration",
    "greater_annulment": "orb_of_annulment",
    "omen_of_chance": "orb_of_chance",
    "omen_of_the_ancients": "orb_of_chance",
    "omen_of_blessed": "divine_orb",
    "omen_of_sanctification": "vaal_orb",
    "whittling": "exalted_orb",
}

# Omen postcondition modifiers (change what the currency does)
OMEN_POST_MODIFIERS = {
    "greater_exaltation": lambda s: _add_random_mod(s, 1),  # adds 1 extra mod (total 2)
    "sinistral_exaltation": lambda s: s,  # just targets prefix — state-wise same
    "dextral_exaltation": lambda s: s,    # just targets suffix — state-wise same
    "sinistral_annulment": lambda s: s,   # targets prefix
    "dextral_annulment": lambda s: s,     # targets suffix
    "sinistral_crystallisation": lambda s: s,  # essence removes only prefixes
    "dextral_crystallisation": lambda s: s,    # essence removes only suffixes
}


# ============================================================================
# State transition helpers
# ============================================================================

def _set_rarity(s: ItemState, rarity: str, prefix: int = None, suffix: int = None) -> ItemState:
    ns = s.copy()
    ns.rarity = rarity
    ns.identified = True
    if prefix is not None:
        ns.prefix_count = min(prefix, ns.max_prefixes)
    if suffix is not None:
        ns.suffix_count = min(suffix, ns.max_suffixes)
    return ns


def _add_random_mod(s: ItemState, count: int = 1) -> ItemState:
    ns = s.copy()
    ns.identified = True
    for _ in range(count):
        if ns.has_open_prefix and ns.has_open_suffix:
            # Could go either way — assume prefix first
            ns.prefix_count += 1
        elif ns.has_open_prefix:
            ns.prefix_count += 1
        elif ns.has_open_suffix:
            ns.suffix_count += 1
        # else: full — no change
    return ns


def _remove_random_mod(s: ItemState) -> ItemState:
    ns = s.copy()
    if ns.total_mods <= 0:
        return ns
    # Remove from whichever has more, or prefix first
    if ns.prefix_count >= ns.suffix_count and ns.prefix_count > 0:
        ns.prefix_count -= 1
    elif ns.suffix_count > 0:
        ns.suffix_count -= 1
    # If all mods removed, downgrade to normal
    if ns.total_mods == 0:
        ns.rarity = "normal"
    return ns


def _reroll_all(s: ItemState) -> ItemState:
    ns = s.copy()
    ns.identified = True
    # Chaos rerolls to 4-6 mods on rare
    ns.prefix_count = 3
    ns.suffix_count = 2
    return ns


def _corrupt(s: ItemState) -> ItemState:
    ns = s.copy()
    ns.corrupted = True
    return ns


def _fracture(s: ItemState) -> ItemState:
    ns = s.copy()
    ns.fractured = True
    return ns


def _add_quality(s: ItemState, target: int) -> ItemState:
    ns = s.copy()
    ns.quality = min(target, 20)
    return ns


# ============================================================================
# Verification result types
# ============================================================================

@dataclass
class Check:
    """A single verification check."""
    test: str
    passed: bool
    severity: str = "error"   # error | warning | info

    def to_dict(self) -> dict:
        return {"test": self.test, "pass": self.passed, "severity": self.severity}


@dataclass
class StepResult:
    """Verification result for a single step."""
    step: int
    action: str
    currency: str
    omen: Optional[str] = None
    checks: list = field(default_factory=list)
    state_before: Optional[ItemState] = None
    state_after: Optional[ItemState] = None

    @property
    def all_pass(self) -> bool:
        return all(c.passed for c in self.checks if c.severity == "error")

    @property
    def has_warnings(self) -> bool:
        return any(not c.passed and c.severity == "warning" for c in self.checks)

    def to_dict(self) -> dict:
        return {
            "step": self.step,
            "action": self.action,
            "currency": self.currency,
            "omen": self.omen,
            "checks": [c.to_dict() for c in self.checks],
            "all_pass": self.all_pass,
            "state_before": self.state_before.summary() if self.state_before else None,
            "state_after": self.state_after.summary() if self.state_after else None,
        }


@dataclass
class VerificationResult:
    """Full recipe verification result."""
    overall: bool
    steps: list  # list of StepResult
    errors: list = field(default_factory=list)  # global errors

    def to_dict(self) -> dict:
        return {
            "overall": self.overall,
            "errors": self.errors,
            "steps": [s.to_dict() for s in self.steps],
        }


# ============================================================================
# Core verification engine
# ============================================================================

def verify_recipe(recipe: dict, prolog_kb: str = "") -> VerificationResult:
    """Verify a recipe by simulating state transitions step-by-step.

    Handles:
    - Omen+currency as compound step (omen is a modifier, not standalone)
    - Loop detection and goto validation
    - State-dependent precondition checking
    - Impossible transition flagging
    """
    steps = recipe.get("steps", [])
    game = recipe.get("game", "poe2")
    state = ItemState()
    results = []
    global_errors = []

    # --- Phase 1: Normalize steps (merge omen into currency step) ---
    normalized = _normalize_steps(steps)

    # --- Phase 2: Build step index for goto validation ---
    step_targets = {}  # step_num -> step data
    for ns in normalized:
        step_targets[ns["step_num"]] = ns

    # --- Phase 3: Verify each step ---
    for ns in normalized:
        step_num = ns["step_num"]
        action = ns["action"]
        currency = ns["currency"]
        omen = ns.get("omen")
        conditions = ns.get("conditions", [])
        else_goto = ns.get("else_goto")
        else_repeat = ns.get("else_repeat", False)

        sr = StepResult(
            step=step_num,
            action=action,
            currency=currency,
            omen=omen,
            state_before=state.copy(),
        )

        # 3a: Check currency exists in KB
        if prolog_kb:
            exists = f"currency({game}, {currency})" in prolog_kb
            sr.checks.append(Check(
                f"Currency '{currency}' exists in {game.upper()}",
                exists,
            ))
            if not exists:
                # Check other game
                other = "poe1" if game == "poe2" else "poe2"
                if f"currency({other}, {currency})" in prolog_kb:
                    sr.checks.append(Check(
                        f"⚠ STALE: '{currency}' exists in {other.upper()} not {game.upper()}",
                        False, "warning",
                    ))

        # 3b: Check omen validity
        if omen:
            if prolog_kb:
                omen_exists = f"omen({game}, {omen}," in prolog_kb
                sr.checks.append(Check(
                    f"Omen '{omen}' exists in {game.upper()}",
                    omen_exists,
                ))
                disabled = f"disabled(omen, {omen}" in prolog_kb
                sr.checks.append(Check(
                    f"Omen '{omen}' is not disabled",
                    not disabled,
                ))
            # Check omen-currency pairing
            # "essence" in the map means "any essence currency" (wildcard)
            # "desecration" means "any desecration currency" (preserved_cranium, etc.)
            expected_currency = OMEN_CURRENCY_MAP.get(omen)
            if expected_currency:
                if expected_currency == "essence":
                    # Wildcard: any essence-type currency is valid
                    is_essence = ("essence" in currency or currency in CURRENCY_RULES
                                  and CURRENCY_RULES.get(currency, {}).get("pre", {}).get("rarity") in (["normal", "magic"], ["normal", "magic", "rare"]))
                    if not is_essence and "essence" not in currency:
                        sr.checks.append(Check(
                            f"Omen '{omen}' pairs with any essence, not '{currency}'",
                            False,
                        ))
                elif expected_currency == "desecration":
                    # Wildcard: any desecration currency is valid
                    is_desecration = ("cran" in currency or "desecrat" in currency
                                      or currency in CURRENCY_RULES)
                    if not is_desecration:
                        sr.checks.append(Check(
                            f"Omen '{omen}' pairs with any desecration currency, not '{currency}'",
                            False,
                        ))
                elif expected_currency != currency:
                    sr.checks.append(Check(
                        f"Omen '{omen}' pairs with '{expected_currency}', not '{currency}'",
                        False,
                    ))

        # 3c: Check currency preconditions against current state
        if currency in CURRENCY_RULES:
            pre = CURRENCY_RULES[currency]["pre"]
            pre_checks = _check_preconditions(state, pre, currency, step_num, normalized)
            sr.checks.extend(pre_checks)
        elif currency not in CURRENCY_RULES and not prolog_kb:
            sr.checks.append(Check(
                f"Unknown currency '{currency}' — no precondition rules",
                False, "warning",
            ))

        # 3d: Validate else_repeat (would this step be repeatable?)
        if else_repeat:
            simulated = _apply_step(state, currency, omen)
            if currency in CURRENCY_RULES:
                repeat_pre = CURRENCY_RULES[currency]["pre"]
                repeat_checks = _check_preconditions(
                    simulated, repeat_pre, currency, step_num, normalized
                )
                for rc in repeat_checks:
                    if not rc.passed:
                        sr.checks.append(Check(
                            f"Repeat step {step_num}: after applying, precondition fails — cannot repeat",
                            False, "error",
                        ))

        # 3g: Apply state transition (only if preconditions pass)
        if sr.all_pass:
            state = _apply_step(state, currency, omen)

        sr.state_after = state.copy()
        results.append(sr)

    # --- Phase 4: Global checks ---
    # Detect unreachable loop backs
    _check_loop_reachability(normalized, results, global_errors)

    overall = all(r.all_pass for r in results) and not global_errors
    return VerificationResult(overall=overall, steps=results, errors=global_errors)


# ============================================================================
# Step normalization — merge omen into currency step
# ============================================================================

def _normalize_steps(steps: list) -> list:
    """Merge standalone omen steps into the following currency step.

    If step N is action='apply_with_omen' and step N+1 is a currency step,
    merge them into a single step with omen modifier.

    Also handles the case where the user made the omen a separate step
    before the currency it modifies.
    """
    normalized = []
    i = 0
    while i < len(steps):
        step = steps[i]
        action = step.get("action", "")
        currency = step.get("currency", "")
        omen = step.get("omen")

        # Case 1: Step has explicit omen field (already compound)
        if omen:
            normalized.append({
                "step_num": step.get("step", len(normalized) + 1),
                "action": action,
                "currency": currency,
                "omen": omen,
                "conditions": step.get("conditions", []),
                "else_goto": step.get("else_goto"),
                "else_repeat": step.get("else_repeat", False),
            })
            i += 1
            continue

        # Case 2: Standalone omen step — merge with next currency step
        if action == "apply_with_omen" and currency in OMEN_CURRENCY_MAP:
            # Find the next step that's a currency application
            if i + 1 < len(steps):
                next_step = steps[i + 1]
                next_currency = next_step.get("currency", "")
                expected = OMEN_CURRENCY_MAP.get(currency)
                if expected and next_currency == expected:
                    # Merge: omen modifies the currency step
                    normalized.append({
                        "step_num": next_step.get("step", len(normalized) + 1),
                        "action": next_step.get("action", "apply_currency"),
                        "currency": next_currency,
                        "omen": currency,  # the omen name
                        "conditions": next_step.get("conditions", []),
                        "else_goto": next_step.get("else_goto"),
                        "else_repeat": next_step.get("else_repeat", False),
                    })
                    i += 2  # skip both steps
                    continue
                else:
                    # Omen doesn't match next currency — flag it but keep separate
                    normalized.append({
                        "step_num": step.get("step", len(normalized) + 1),
                        "action": action,
                        "currency": currency,
                        "omen": None,
                        "conditions": step.get("conditions", []),
                        "else_goto": step.get("else_goto"),
                        "else_repeat": step.get("else_repeat", False),
                    })
                    i += 1
                    continue

        # Case 3: Normal step
        normalized.append({
            "step_num": step.get("step", len(normalized) + 1),
            "action": action,
            "currency": currency,
            "omen": omen,
            "conditions": step.get("conditions", []),
            "else_goto": step.get("else_goto"),
            "else_repeat": step.get("else_repeat", False),
        })
        i += 1

    return normalized


# ============================================================================
# Precondition checking
# ============================================================================

def _check_preconditions(state: ItemState, pre: dict, currency: str,
                         step_num: int, all_steps: list) -> list:
    """Check currency preconditions against current item state."""
    checks = []

    if pre.get("not_corrupted", True) and state.corrupted:
        checks.append(Check(
            f"Step {step_num}: '{currency}' requires item not corrupted",
            False,
        ))

    # Rarity check
    req_rarity = pre.get("rarity")
    if req_rarity:
        if isinstance(req_rarity, list):
            if state.rarity not in req_rarity:
                checks.append(Check(
                    f"Step {step_num}: '{currency}' requires {req_rarity}, item is {state.rarity}",
                    False,
                ))
            else:
                checks.append(Check(
                    f"Step {step_num}: '{currency}' requires {req_rarity}, item is {state.rarity}",
                    True,
                ))
        else:
            if state.rarity != req_rarity:
                checks.append(Check(
                    f"Step {step_num}: '{currency}' requires {req_rarity}, item is {state.rarity}",
                    False,
                ))
            else:
                checks.append(Check(
                    f"Step {step_num}: '{currency}' requires {req_rarity}, item is {state.rarity}",
                    True,
                ))

    # No mods check (for transmutation, alchemy, chance on normal base)
    if pre.get("no_mods"):
        if state.total_mods > 0:
            checks.append(Check(
                f"Step {step_num}: '{currency}' requires item with no mods (has {state.total_mods})",
                False,
            ))
        else:
            checks.append(Check(
                f"Step {step_num}: '{currency}' requires item with no mods",
                True,
            ))

    # Has mods check (for annulment, divine)
    if pre.get("has_mods"):
        if state.total_mods == 0:
            checks.append(Check(
                f"Step {step_num}: '{currency}' requires item with at least 1 mod",
                False,
            ))
        else:
            checks.append(Check(
                f"Step {step_num}: '{currency}' requires item with at least 1 mod",
                True,
            ))

    # Min mods check
    min_mods = pre.get("min_mods")
    if min_mods:
        if state.total_mods < min_mods:
            checks.append(Check(
                f"Step {step_num}: '{currency}' requires at least {min_mods} mods (has {state.total_mods})",
                False,
            ))
        else:
            checks.append(Check(
                f"Step {step_num}: '{currency}' requires at least {min_mods} mods",
                True,
            ))

    # Open slot checks
    if pre.get("open_slot"):
        if not state.has_open_slot:
            checks.append(Check(
                f"Step {step_num}: '{currency}' requires open prefix or suffix slot (full: {state.prefix_count}p+{state.suffix_count}s)",
                False,
            ))
        else:
            checks.append(Check(
                f"Step {step_num}: '{currency}' requires open prefix or suffix slot",
                True,
            ))

    if pre.get("open_prefix"):
        if not state.has_open_prefix:
            checks.append(Check(
                f"Step {step_num}: '{currency}' requires open prefix slot ({state.prefix_count}/{state.max_prefixes})",
                False,
            ))
        else:
            checks.append(Check(
                f"Step {step_num}: '{currency}' requires open prefix slot",
                True,
            ))

    if pre.get("open_suffix"):
        if not state.has_open_suffix:
            checks.append(Check(
                f"Step {step_num}: '{currency}' requires open suffix slot ({state.suffix_count}/{state.max_suffixes})",
                False,
            ))
        else:
            checks.append(Check(
                f"Step {step_num}: '{currency}' requires open suffix slot",
                True,
            ))

    return checks


# ============================================================================
# State transition application
# ============================================================================

def _apply_step(state: ItemState, currency: str, omen: str = None) -> ItemState:
    """Apply a currency (with optional omen) to the item state."""
    if currency in CURRENCY_RULES:
        post_fn = CURRENCY_RULES[currency]["post"]
        new_state = post_fn(state)
        # Apply omen modifier if present
        if omen and omen in OMEN_POST_MODIFIERS:
            new_state = OMEN_POST_MODIFIERS[omen](new_state)
        return new_state
    # Unknown currency — return state unchanged
    return state.copy()


# ============================================================================
# Loop reachability analysis
# ============================================================================

def _check_loop_reachability(normalized: list, results: list,
                             global_errors: list):
    """Check that goto targets are reachable from the current state.

    For each goto/else_goto, simulates the state at the goto point and
    checks whether the target step's preconditions can be satisfied.
    """
    # Build state timeline
    states = []
    state = ItemState()
    for ns in normalized:
        states.append(state.copy())
        currency = ns["currency"]
        omen = ns.get("omen")
        if currency in CURRENCY_RULES:
            state = _apply_step(state, currency, omen)

    # Check each step's goto targets
    for i, ns in enumerate(normalized):
        step_num = ns["step_num"]
        conditions = ns.get("conditions", [])
        else_goto = ns.get("else_goto")

        for cond in conditions:
            goto = cond.get("goto")
            if goto is None:
                continue
            # Find target step index
            target_idx = None
            for j, n in enumerate(normalized):
                if n["step_num"] == goto:
                    target_idx = j
                    break
            if target_idx is None:
                global_errors.append(
                    f"Step {step_num}: goto step {goto} does not exist"
                )
                continue

            # State at goto point = state after the step that jumps
            # (the condition is checked AFTER applying the current step)
            current_state = states[i].copy()
            # Apply current step to get post-state
            if ns["currency"] in CURRENCY_RULES:
                current_state = _apply_step(current_state, ns["currency"], ns.get("omen"))

            # Check target step's preconditions
            target_ns = normalized[target_idx]
            target_currency = target_ns["currency"]
            if target_currency in CURRENCY_RULES:
                target_pre = CURRENCY_RULES[target_currency]["pre"]
                checks = _check_preconditions(
                    current_state, target_pre, target_currency, goto, normalized
                )
                failed = [c for c in checks if not c.passed]
                if failed:
                    # One error per goto target (not per failed precondition)
                    global_errors.append(
                        f"Step {step_num} → goto {goto}: "
                        f"target step requires {target_pre.get('rarity', '?')} "
                        f"but item would be {current_state.rarity} "
                        f"({current_state.summary()})"
                    )

        # Check else_goto
        if else_goto:
            target_idx = None
            for j, n in enumerate(normalized):
                if n["step_num"] == else_goto:
                    target_idx = j
                    break
            if target_idx is None:
                global_errors.append(
                    f"Step {step_num}: else_goto step {else_goto} does not exist"
                )
                continue

            current_state = states[i].copy()
            if ns["currency"] in CURRENCY_RULES:
                current_state = _apply_step(current_state, ns["currency"], ns.get("omen"))

            target_ns = normalized[target_idx]
            target_currency = target_ns["currency"]
            if target_currency in CURRENCY_RULES:
                target_pre = CURRENCY_RULES[target_currency]["pre"]
                checks = _check_preconditions(
                    current_state, target_pre, target_currency, else_goto, normalized
                )
                failed = [c for c in checks if not c.passed]
                if failed:
                    global_errors.append(
                        f"Step {step_num} → else_goto {else_goto}: "
                        f"target step requires {target_pre.get('rarity', '?')} "
                        f"but item would be {current_state.rarity}"
                    )
