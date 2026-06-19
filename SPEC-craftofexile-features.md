# Craft of Exile Feature Spec — PoE 2 Crafting Guide

## Part 1: External Data Sources

### Ranked Sources for Knowledge Base Enrichment

| # | Source | URL | What It Has | Format | License | Freshness |
|---|--------|-----|-------------|--------|---------|-----------|
| **1** | **POE2-PathOfCrafting** | github.com/frankthetank001/POE2-PathOfCrafting | weights.csv, omens.json, alloys.json, catalysts.json, currency_configs.json, exclusion_groups.json, modifier_exclusions.json | JSON/CSV | Check repo | Updated daily (PoE 2 0.5.0) |
| **2** | **Path of Building PoE2** | github.com/PathOfBuildingCommunity/PathOfBuilding-PoE2 | Item bases (Lua tables per type: ring, amulet, belt, body, boots, etc.), essences, uniques, stat descriptions | Lua | MIT | 5 days ago, 1.8k stars |
| **3** | **poe2db.tw** | poe2db.tw/us/ | Mod pools by item type with tags, tiers, weights, ilvl requirements | HTML (scrape) | CC BY-NC-SA 3.0 | Current (0.5.0) |
| **4** | **poe2wiki.net** | poe2wiki.net/wiki/ | Crafting mechanics, currency effects, omen descriptions, alloy/catalyst/rune docs | MediaWiki | Wiki default | Current (0.5.0) |
| **5** | **GGG Official API** | api.pathofexile.com | Currency exchange prices only — NO mod/crafting data | JSON | OAuth | Current |

### Source 1: POE2-PathOfCrafting (PRIMARY — the gold mine)

This is an open-source PoE 2 crafting simulator with a Python backend. Its `backend/source_data/` directory has **exactly the structured data we need**:

| File | What It Contains | Our Equivalent | Gap |
|------|-----------------|----------------|-----|
| `weights.csv` | Mod weights per item type | `resources/mods_*.pl` | We have 9/56 files loaded; this has ALL types |
| `omens.json` | Omen definitions + effects | `omen/5` facts in PL | We have 32 omens; verify completeness |
| `alloys.json` | Alloy definitions | `alloy/4` facts in PL | We have 13; verify completeness |
| `catalysts.json` | Catalyst definitions | `quality_type/3` facts | We have 12 catalysts; verify |
| `currency_configs.json` | Currency behavior rules | `currency_precondition/postcondition` | Our rules are manually written; this has structured configs |
| `exclusion_groups.json` | Mod exclusion groups | Not tracked | **Missing from our KB entirely** |
| `modifier_exclusions.json` | Modifier exclusion rules | Not tracked | **Missing from our KB entirely** |
| `desecration_bones.json` | Desecrated mod data | Not tracked | PoE 2 mechanic we don't model |

**Action**: Clone repo, write import script (similar to existing `scripts/import_from_tradecraft.py`), convert to Prolog facts.

### Source 2: Path of Building PoE2

MIT-licensed Lua data files. Most useful for **item bases** (which we're missing many of):

- `src/Data/Bases/Ring.lua`, `Amulet.lua`, `Belt.lua`, etc. — base item stats, requirements, implicit mods
- `src/Data/Essence.lua` — essence definitions
- Does NOT have mod weights or crafting behavior

**Action**: Parse Lua tables for item base definitions we're missing (belts, all weapon types, shields, focus, sceptre, etc.).

### Source 3: poe2db.tw

The canonical datamined source. HTML tables with mod pools per item type. Our skill already has scraping patterns.

**Action**: Use for validation. Compare our mod_group counts and weights against poe2db for the categories we already have.

---

## Part 2: Internal Audit Findings

### 🔴 Critical Issues

| # | Issue | Impact | Fix |
|---|-------|--------|-----|
| 1 | **Jewel mods NOT loaded** — `mods_jewel.pl` exists but no `consult` directive in `poe2_crafting.pl` | Jewel crafting completely broken | Add `:- consult('resources/mods_jewel.pl').` |
| 2 | **`omen_crafting_pairs/4` is buggy** — binds to `sinistral_omen`/`dextral_omen` (non-existent atoms) instead of actual omen names | Omen pairing logic never succeeds | Rewrite to use actual omen names from `omen/5` facts |
| 3 | **Dangling `nerfed(omen, uhtreds_saga)`** — no corresponding `omen/5` fact | Test assertion may fail or be misleading | Add the omen fact or remove the nerf record |

### 🟡 Moderate Issues

| # | Issue | Impact | Fix |
|---|-------|--------|-----|
| 4 | **Only str variants loaded** — body_armour_str, helmet_str, gloves_str, boots_str, weapon_sword. All dex/int/hybrid variants (47 files) NOT loaded | Can't craft on dex, int, or hybrid bases | Load more variants via consult directives + mod_pool mappings |
| 5 | **Missing mod_pool/3 mappings** — only 11 exist. Missing: belt, shields, talisman, most weapon types | base_mod_pool → roll_mod fails for unlisted categories | Add mod_pool facts for all loaded categories |
| 6 | **Missing base_type/2 definitions** — only 17 bases. No focus, sceptre, bow, crossbow, staff, wand, mace, spear bases | Recipe verification can't resolve base names | Import base definitions from Path of Building |
| 7 | **weapon_sword weight sums very low** — prefix=70, suffix=88 vs 6000-16000 for other categories | Probability calculations will be wildly wrong | Re-scrape or import from POE2-PathOfCrafting weights.csv |
| 8 | **essence_of_wrath has no rarity check** — accepts normal rarity but postcondition produces rare | Skipping magic stage entirely | Add rarity precondition (magic or rare) |
| 9 | **No exclusion groups tracked** | Mods that should block each other can co-occur | Import exclusion_groups.json from POE2-PathOfCrafting |

### 🟢 Minor Issues

| # | Issue | Impact |
|---|-------|--------|
| 10 | No data for flasks, charms, tablets, waystones | Can't craft these item types |
| 11 | orb_of_scouring has pre/postcondition but is poe1-only (dead rules) | Clutter, not functional |
| 12 | Tests are regex-based only, no actual Prolog query execution | Can't validate rule correctness |

### Coverage Summary

| Category | Mod Files | Loaded | mod_pool | base_type |
|----------|-----------|--------|----------|-----------|
| body_armour (str) | ✅ | ✅ | ✅ | ✅ |
| body_armour (dex/int/hybrid) | ✅ (5 files) | ❌ | ❌ | ❌ |
| helmet (str) | ✅ | ✅ | ✅ | ✅ |
| helmet (dex/int/hybrid) | ✅ (5 files) | ❌ | ❌ | ❌ |
| gloves (str) | ✅ | ✅ | ✅ | ✅ |
| gloves (dex/int/hybrid) | ✅ (5 files) | ❌ | ❌ | ❌ |
| boots (str) | ✅ | ✅ | ✅ | ✅ |
| boots (dex/int/hybrid) | ✅ (5 files) | ❌ | ❌ | ❌ |
| rings | ✅ | ✅ | ✅ | ✅ (2 bases) |
| amulets | ✅ | ✅ | ✅ | ✅ (1 base) |
| belts | ✅ | ❌ | ❌ | ✅ (1 base) |
| jewels | ✅ | ❌ (no consult!) | ✅ | ✅ (4 bases) |
| weapons (sword) | ✅ | ✅ | ✅ | ✅ (2 bases) |
| weapons (bow/xbow/staff/wand/mace/spear) | ✅ (19 files) | ❌ | ❌ | ❌ |
| offhands (shields/buckler/focus) | ✅ (5 files) | ❌ | ❌ | ❌ |
| quivers | ✅ | ✅ | ✅ | ✅ |
| talismans | ✅ | ❌ | ❌ | ❌ |
| flasks | ❌ | ❌ | ❌ | ❌ |
| charms | ❌ | ❌ | ❌ | ❌ |
| tablets | ❌ | ❌ | ❌ | ❌ |
| waystones | ❌ | ❌ | ❌ | ❌ |

**Loaded: 9/56 mod files (16%). Missing: 47 mod files, ~40 base types, exclusion groups.**

---

## Part 3: Feature Phases (Detailed Tasks)

### Phase 0: Data Quality Fix (DO FIRST)

The KB has critical bugs and only 16% coverage. Fix before building new features.

- [ ] **0.1** Add `:- consult('resources/mods_jewel.pl').` to poe2_crafting.pl
- [ ] **0.2** Add `:- consult('resources/mods_belt.pl').` to poe2_crafting.pl
- [ ] **0.3** Fix `omen_crafting_pairs/4` — rewrite to use actual omen names
- [ ] **0.4** Fix dangling `nerfed(omen, uhtreds_saga)` — add the omen fact or remove nerf
- [ ] **0.5** Add `mod_pool/3` mappings for belt, jewel, and any other missing categories
- [ ] **0.6** Add `base_type/2` definitions for belt bases (heavy_belt, chain_belt, leather_belt, etc.)
- [ ] **0.7** Fix weapon_sword weight sums — verify against poe2db or re-scrape
- [ ] **0.8** Add rarity check to `essence_of_wrath` precondition (require magic+)
- [ ] **0.9** Run all tests, fix any breakage from the above changes
- [ ] **0.10** Verify jewel crafting end-to-end (jewel mod lookup, roll, recipe)

### Phase 0.5: Data Enrichment (Import from External Sources)

- [ ] **0.5.1** Clone `frankthetank001/POE2-PathOfCrafting` repo
- [ ] **0.5.2** Write import script: `scripts/import_from_pathofcrafting.py`
  - Convert `weights.csv` → `mod_group/8` Prolog facts (ALL categories, not just str)
  - Convert `omens.json` → `omen/5` facts (merge with existing, flag new/discrepancies)
  - Convert `alloys.json` → `alloy/4` facts (merge)
  - Convert `catalysts.json` → `quality_type/3` facts (merge)
  - Convert `currency_configs.json` → currency preconditions/postconditions (diff against ours)
  - Convert `exclusion_groups.json` → NEW `exclusion_group/2` Prolog predicate
- [ ] **0.5.3** Add missing mod_pool/3 mappings for all newly imported categories
- [ ] **0.5.4** Add base_type/2 definitions — parse from Path of Building Lua files OR from POE2-PathOfCrafting
- [ ] **0.5.5** Add missing consult directives for all new mod data files
- [ ] **0.5.6** Update tests: new category counts, exclusion group tests, weight sum validation
- [ ] **0.5.7** Validate imported data against poe2db.tw for 3-5 categories (spot check)
- [ ] **0.5.8** Update `app.py` to parse and serve exclusion groups via API

### Phase A: Crafting Simulator

The biggest gap — our recipes are data structures, not executable. This adds the execution engine.

#### A.1: Weighted Rolling Engine
- [ ] **A.1.1** Create `simulator.py` with `weighted_roll(items)` function
- [ ] **A.1.2** Implement `roll_mod(category, slot, ilvl, exclude=None, guarantee=None)` — weighted random mod selection from Prolog data
- [ ] **A.1.3** Implement multi-mod rolling: transmute (1-2 mods), alchemy (4-6 mods), exalt (1 mod), chaos (reroll all)
- [ ] **A.1.4** Implement essence rolling: guarantee one mod group, roll rest from pool
- [ ] **A.1.5** Implement omen-modified rolling: sinistral (prefix only), dextral (suffix only), etc.
- [ ] **A.1.6** Add exclusion group support: don't roll mods that conflict with existing ones
- [ ] **A.1.7** Unit tests for rolling engine: weight distributions, exclusion enforcement, essence guarantees

#### A.2: Sequence Executor
- [ ] **A.2.1** `CraftingSimulator.run_single(base, ilvl, steps)` — execute one crafting sequence
- [ ] **A.2.2** Implement step types: apply_currency, apply_essence, apply_catalyst, spam (repeat until condition)
- [ ] **A.2.3** Implement condition checking: has_mod, not_has_mod, prefix_count, suffix_count, rarity_is
- [ ] **A.2.4** Implement branching: on_success (continue/goto), on_failure (loop/restart/abort)
- [ ] **A.2.5** Implement goto/loop with max-iteration guard (prevent infinite loops)
- [ ] **A.2.6** Track per-run: final item state, total cost (currency dict), steps executed, success/fail
- [ ] **A.2.7** Unit tests for sequence executor: simple sequences, loops, branching, edge cases

#### A.3: Monte Carlo Runner
- [ ] **A.3.1** `CraftingSimulator.run_sequence(base, ilvl, steps, n=1000)` — run N iterations
- [ ] **A.3.2** Aggregate results: success_rate, avg_cost, median_cost, cost_distribution (histogram buckets)
- [ ] **A.3.3** Track outcome distribution: which mod groups appeared most often
- [ ] **A.3.4** Track best/worst items produced
- [ ] **A.3.5** Configurable iteration count (default 1000, max 10000)
- [ ] **A.3.6** API endpoint: `POST /api/simulate` — accepts {base, ilvl, steps, iterations}
- [ ] **A.3.7** API endpoint: `POST /api/simulate/step` — single-step probability (Calculator mode)
- [ ] **A.3.8** Integration tests for the API

#### A.4: Simulator Frontend
- [ ] **A.4.1** Step builder UI: add/remove/reorder steps, each with method dropdown + condition builder
- [ ] **A.4.2** Run button → shows progress → displays results
- [ ] **A.4.3** Results panel: success rate, cost stats, histogram, outcome table
- [ ] **A.4.4** Flowchart visualization: SVG rendering of step sequence with condition branches
- [ ] **A.4.5** Import recipe from Recipe Builder → pre-fill step builder

### Phase B: Probability Calculator

Focused version of Simulator — "what are my odds for this ONE crafting method?"

- [ ] **B.1** `POST /api/calculate` endpoint — accepts {category, base, ilvl, method, target_mods, existing_mods}
- [ ] **B.2** Group logic (G1/G2/G3) — "any of group" vs "all groups required"
- [ ] **B.3** Implement probability calculation per method: chaos spam, essence+chaos, omen-assisted, exalt slam
- [ ] **B.4** Method comparison — show expected cost across all applicable methods for the same target
- [ ] **B.5** Calculator frontend: mod pool display (click to select targets), method dropdown, results panel
- [ ] **B.6** Mass simulation validation button — run 1M iterations to verify analytical calculation

### Phase C: Crafting Emulator / Sandbox

Manual crafting bench — click currencies, see random rolls, track spending.

- [ ] **C.1** `CraftingEmulator` class — item state machine with random rolling
- [ ] **C.2** `POST /api/emulator/create` — create sandbox item (base, ilvl)
- [ ] **C.3** `POST /api/emulator/apply` — apply currency with random roll, return result
- [ ] **C.4** `POST /api/emulator/undo` — revert last step
- [ ] **C.5** `GET /api/emulator/state` — current item state + history + spending
- [ ] **C.6** `GET /api/emulator/mod_pool` — available mods for current item state (filterable)
- [ ] **C.7** `POST /api/emulator/export` — export item as JSON (compatible with Simulator import)
- [ ] **C.8** Emulator frontend: item display panel, currency toolbar, mod pool panel, history, spending tracker
- [ ] **C.9** Item import: paste/import an in-game item to start crafting from
- [ ] **C.10** Cross-tool export: send Emulator item → Simulator for Monte Carlo validation

---

## Part 4: What Craft of Exile Does (Reference)

### Calculator
Select item base → browse mod pool → LEFT-click target mods (what you want) → RIGHT-click existing mods (blocks from pool) → pick crafting method → see probability + expected cost. Group columns (G1/G2/G3) let you say "any of these mods" vs "all groups required."

### Simulator
Create item → build a multi-step crafting sequence. Each step has: method (currency/craft), repeat count, conditions (stop when mod X appears), branching (on success: continue/goto step N; on failure: loop/restart). Run 1000+ iterations → see success rate, average cost, outcome distribution, flowchart.

### Emulator (Wraecrafter Ultra)
Manual sandbox. Create item → click currencies one at a time → see random rolls happen → view mod pool (prefixes/suffixes with weights) → history with undo → spending tracker → export item to Simulator.
