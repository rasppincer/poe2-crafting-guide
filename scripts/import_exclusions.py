#!/usr/bin/env python3
"""
Import exclusion_groups.json and modifier_exclusions.json from PathOfCrafting
into Prolog fact files for use in the PoE2 crafting guide.

Generates:
  - resources/exclusion_groups.pl    — mutual exclusion groups (patterns)
  - resources/modifier_exclusions.pl — per-modifier item-type exclusions

Source repo: /tmp/poe2-pathofcrafting/backend/source_data/

=== Data Structure Analysis ===

exclusion_groups.json (40 entries):
  Each entry defines a set of modifier stat_text patterns that are MUTUALLY
  EXCLUSIVE — only one mod from the group can appear on an item at a time.
  
  Fields:
    description     (str)        — human-readable name
    patterns        (list[str])  — stat_text patterns using '#' as numeric wildcard
    note            (str, opt)   — extra context
    tags            (str, opt)   — tag-based grouping (e.g. 'ailment')
    applicable_items (list[str], opt) — restricts rule to specific item types

  Semantics: If a mod's stat_text matches any pattern in a group, it conflicts
  with all other mods whose stat_text matches any OTHER pattern in the same group.
  Pattern matching uses '#' as wildcard for numeric values.

modifier_exclusions.json (3 entries):
  Each entry identifies a modifier pattern that is EXCLUDED from specific
  item base types (it simply cannot roll on those bases).

  Fields:
    comment         (str)        — explanation
    stat_text       (str)        — modifier pattern with '{}' as numeric wildcard
    exclude_from    (list[str])  — item types the mod cannot appear on

  All 3 entries exclude ES hybrid mods from boots and gloves.

=== Prolog Predicate Design ===

1. exclusion_group(+GroupId, +Description, +Patterns)
   - GroupId: integer (0-based index)
   - Description: atom
   - Patterns: list of pattern atoms with '#' as wildcard
   
2. exclusion_group_items(+GroupId, +ApplicableItems)
   - Only present when the group is restricted to specific item types
   - ApplicableItems: list of item type atoms
   
3. exclusion_group_tag(+GroupId, +Tag)
   - Only present for tag-based exclusion groups (currently only 'ailment')
   
4. modifier_excluded_from(+StatPattern, +ExcludeFrom)
   - StatPattern: atom with '{}' as numeric wildcard
   - ExcludeFrom: list of item type atoms
"""

import json
import re
import sys
from pathlib import Path

# === Paths ===
SOURCE_DIR = Path("/tmp/poe2-pathofcrafting/backend/source_data")
OUTPUT_DIR = Path(__file__).parent.parent / "resources"

EXCLUSION_GROUPS_SRC = SOURCE_DIR / "exclusion_groups.json"
MODIFIER_EXCLUSIONS_SRC = SOURCE_DIR / "modifier_exclusions.json"

EXCLUSION_GROUPS_OUT = OUTPUT_DIR / "exclusion_groups.pl"
MODIFIER_EXCLUSIONS_OUT = OUTPUT_DIR / "modifier_exclusions.pl"


def prolog_atom(s: str) -> str:
    """Convert a string to a Prolog atom, quoting if necessary."""
    # Replace single quotes within the string
    s_escaped = s.replace("'", "\\'")
    # Always quote for safety (patterns contain special chars)
    return f"'{s_escaped}'"


def prolog_list(items: list[str]) -> str:
    """Convert a list of strings to a Prolog list literal."""
    if not items:
        return "[]"
    atoms = [prolog_atom(s) for s in items]
    return "[" + ", ".join(atoms) + "]"


def generate_exclusion_groups(data: list[dict]) -> str:
    """Generate Prolog facts for exclusion groups."""
    lines = [
        "%%% Auto-generated exclusion group facts from PathOfCrafting",
        "%%% exclusion_group(+GroupId, +Description, +Patterns)",
        "%%%   Patterns use '#' as numeric wildcard.",
        "%%% exclusion_group_items(+GroupId, +ApplicableItems)",
        "%%%   Only present when group is restricted to specific item types.",
        "%%% exclusion_group_tag(+GroupId, +Tag)",
        "%%%   Only present for tag-based exclusion groups.",
        "%%%",
        "%%% Two mods whose stat_text matches different patterns in the same",
        "%%% group cannot coexist on the same item (within the same affix type).",
        "%%% Use match_exclusion_pattern/2 (in poe2_crafting.pl) for matching.",
        "",
    ]

    for idx, group in enumerate(data):
        desc = group.get("description", "")
        patterns = group.get("patterns", [])
        applicable = group.get("applicable_items", [])
        tag = group.get("tags", "")

        # exclusion_group/3
        lines.append(
            f"exclusion_group({idx}, {prolog_atom(desc)}, {prolog_list(patterns)})."
        )

        # exclusion_group_items/2 (only if restricted)
        if applicable:
            lines.append(
                f"exclusion_group_items({idx}, {prolog_list(applicable)})."
            )

        # exclusion_group_tag/2 (only if tag-based)
        if tag:
            lines.append(
                f"exclusion_group_tag({idx}, {prolog_atom(tag)})."
            )

        lines.append("")  # blank line between groups

    return "\n".join(lines)


def generate_modifier_exclusions(data: list[dict]) -> str:
    """Generate Prolog facts for modifier exclusions."""
    lines = [
        "%%% Auto-generated modifier exclusion facts from PathOfCrafting",
        "%%% modifier_excluded_from(+StatPattern, +ExcludeFrom)",
        "%%%   StatPattern uses '{}' as numeric wildcard.",
        "%%%   These modifiers simply cannot roll on the listed item types.",
        "",
    ]

    for entry in data:
        stat_text = entry.get("stat_text", "")
        exclude_from = entry.get("exclude_from", [])
        comment = entry.get("comment", "")

        if comment:
            lines.append(f"%% {comment}")

        lines.append(
            f"modifier_excluded_from({prolog_atom(stat_text)}, {prolog_list(exclude_from)})."
        )
        lines.append("")

    return "\n".join(lines)


def main():
    # Load source data
    if not EXCLUSION_GROUPS_SRC.exists():
        print(f"ERROR: {EXCLUSION_GROUPS_SRC} not found", file=sys.stderr)
        sys.exit(1)
    if not MODIFIER_EXCLUSIONS_SRC.exists():
        print(f"ERROR: {MODIFIER_EXCLUSIONS_SRC} not found", file=sys.stderr)
        sys.exit(1)

    with open(EXCLUSION_GROUPS_SRC, "r", encoding="utf-8") as f:
        exclusion_groups = json.load(f)
    with open(MODIFIER_EXCLUSIONS_SRC, "r", encoding="utf-8") as f:
        modifier_exclusions = json.load(f)

    print(f"Loaded {len(exclusion_groups)} exclusion groups")
    print(f"Loaded {len(modifier_exclusions)} modifier exclusions")

    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Generate and write exclusion_groups.pl
    eg_pl = generate_exclusion_groups(exclusion_groups)
    with open(EXCLUSION_GROUPS_OUT, "w", encoding="utf-8") as f:
        f.write(eg_pl)
    print(f"Wrote {EXCLUSION_GROUPS_OUT}")

    # Generate and write modifier_exclusions.pl
    me_pl = generate_modifier_exclusions(modifier_exclusions)
    with open(MODIFIER_EXCLUSIONS_OUT, "w", encoding="utf-8") as f:
        f.write(me_pl)
    print(f"Wrote {MODIFIER_EXCLUSIONS_OUT}")

    # Summary statistics
    total_patterns = sum(len(g.get("patterns", [])) for g in exclusion_groups)
    groups_with_items = sum(1 for g in exclusion_groups if g.get("applicable_items"))
    groups_with_tags = sum(1 for g in exclusion_groups if g.get("tags"))
    print(f"\nSummary:")
    print(f"  Exclusion groups: {len(exclusion_groups)} total")
    print(f"    - {total_patterns} patterns across all groups")
    print(f"    - {groups_with_items} groups restricted to specific item types")
    print(f"    - {groups_with_tags} groups using tag-based matching")
    print(f"  Modifier exclusions: {len(modifier_exclusions)} entries")


if __name__ == "__main__":
    main()
