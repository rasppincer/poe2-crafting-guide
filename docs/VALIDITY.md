# VALIDITY.md — Version-Aware Fact Checking

**Read this before adding ANY crafting fact, recipe, or mechanic to the knowledge base.**

---

## The Problem

PoE 2 is a live game. Crafting systems change between patches:
- Omens get disabled (8 were disabled between 0.3.0 and 0.5.0)
- Essences get nerfed (values reduced, mechanics changed)
- Entire systems get removed (Recombination disabled in 0.5.0)
- New systems get added (Alloys in 0.5.0)
- League mechanics rotate (Expedition temporarily disabled on Standard)

A recipe that worked in January 2026 may be **completely broken** in the current patch.
A crafting guide from Reddit/YouTube may reference omens that no longer drop.
A poe2db page may show mods that were removed last patch.

**Always check the version. Always check the validity layer.**

---

## Before Adding Anything — Checklist

### 1. What version is the source from?

If the source doesn't state a version, **assume it may be outdated** and verify:
- Check `poe2_crafting.pl` → `current_version/1` for the current patch
- Check `disabled/3` for entities that no longer exist
- Check `nerfed/4` for entities that were weakened
- Check `resources/version_050_changes.md` for the latest changes

### 2. Does the recipe reference any disabled entity?

Run this mental check against the disabled list:
- **Disabled omens** (as of 0.5.0): sinistral_alchemy, dextral_alchemy, sinistral_coronation, dextral_coronation, greater_annulment, homogenising_coronation, homogenising_exaltation, omen_of_corruption
- **Disabled mechanics**: recombination
- **Nerfed essences**: perfect_essence_of_battle, essence_of_hysteria

If a recipe uses any of these, it's **invalid for 0.5.0**. Don't add it without marking it as version-specific.

### 3. Is the mod pool still accurate?

Mod weights and available mods can change between patches. If pulling from:
- **poe2db.tw** — usually current, but verify the page title shows the right version
- **Craft of Exile** — verify it's set to PoE 2 (not PoE 1)
- **Reddit/YouTube** — always cross-reference with poe2db for current data
- **Old session transcripts** — may reference data from a previous patch

### 4. Is this a PoE 1 or PoE 2 mechanic?

Common confusion points:
- PoE 1 has "prefixes cannot be changed" bench craft → PoE 2 uses **omens** instead
- PoE 1 has catalyst quality on belts → PoE 2 **belts cannot have quality**
- PoE 1 has recombinators → PoE 2 recombination is **disabled**
- PoE 1 influence system differs from PoE 2

---

## How to Validate

### Quick check (5 seconds)
```
grep "disabled(" poe2_crafting.pl
grep "nerfed(" poe2_crafting.pl
```

### Recipe validation (automated)
The web UI's "Verify Recipe" button checks:
- All currencies exist and have rules
- All omens exist and are not disabled
- All alloys exist
- All catalysts exist

### Full version audit
Read `resources/version_050_changes.md` for the complete list of 0.5.0 changes.

---

## When You Find an Invalid Source

If a recipe or fact references something disabled:

1. **Don't add it as-is** — it will pollute the KB with stale data
2. **Check if there's a current equivalent** — e.g., the sinistral/dextral pairs that ARE still active (erasure, exaltation, annulment, crystallisation, necromancy)
3. **If adding historical data**, mark it clearly:
   - In Prolog: add a `% DISABLED IN 0.5.0` comment
   - In recipes: add a `version_note` field
   - In JSON: add a `"valid_from": "0.3.0", "valid_until": "0.4.0"` pair
4. **Update the validity layer** — add a `disabled/3` fact if you discover a new disable

---

## Version History Quick Reference

| Patch | Date | Key Crafting Changes |
|-------|------|---------------------|
| 0.3.0 | ~2026-01 | 5 omens disabled (alchemy, coronation, greater_annulment) |
| 0.4.0 | ~2026-03 | 2 homogenising omens disabled |
| 0.5.0 | 2026-05-28 | Recombination disabled, Alloys introduced, 2 omens disabled, essence nerfs |

---

## The Rule

**If you can't confirm a fact is valid for `current_version`, don't add it unconditionally.**

When in doubt:
1. Check `disabled/3` and `nerfed/4` in the Prolog KB
2. Check `resources/version_050_changes.md`
3. Cross-reference with poe2db.tw (usually current)
4. Ask the user to confirm the version if the source is ambiguous
