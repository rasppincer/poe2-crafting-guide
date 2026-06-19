# TODO

Spec: `SPEC-craftofexile-features.md` — full details, external sources, audit findings

## Phase 0: Data Quality Fix (DO FIRST)

KB has critical bugs and 16% mod coverage. Fix before building new features.

- [x] 0.1 Add `consult('resources/mods_jewel.pl')` to poe2_crafting.pl
- [x] 0.2 Add `consult('resources/mods_belt.pl')` to poe2_crafting.pl
- [x] 0.3 Fix `omen_crafting_pairs/4` — rewrote with actual omen names + dual clauses (removes/adds)
- [x] 0.4 Commented out dangling `nerfed(omen, uhtreds_saga)` — no matching omen/5 fact
- [x] 0.5 Add missing `mod_pool/3` for belt (jewel already existed)
- [x] 0.6 `base_type/2` for heavy_belt already existed — no change needed
- [ ] 0.7 Fix weapon_sword weight sums (70/88 vs 6000+ for others — defer to Phase 0.5 import)
- [x] 0.8 Add rarity check to essence_of_wrath precondition (now requires magic, like essence_of_the_body)
- [x] 0.9 All 133 tests pass (118 KB/verifier/recipe + 15 optimizer; 5 Flask import errors are pre-existing)
- [x] 0.10 Jewel crafting verified: 4 bases (cobalt/ruby/sapphire/emerald), 18 mod groups, mod_pool resolves correctly

## Phase 0.5: Data Enrichment (External Import) ✅ DONE

Primary source: `frankthetank001/POE2-PathOfCrafting` — has weights.csv, omens.json, catalysts.json, currency_configs.json, exclusion_groups.json

- [x] 0.5.1 Imported 53 mod category files from PathOfCrafting (weights.csv) — 1,201 mod groups, 55 categories
- [x] 0.5.2 All resource files wired with load_files + module(poe2_crafting) directives
- [x] 0.5.3 Added mod_pool/3 for all 55 categories (ring, amulet, belt, all armour/weapon variants, shields, focus, sceptre, talisman)
- [x] 0.5.4 Imported 30 omen facts from omens.json (14 unmapped new PoE 2 omens — needs manual mapping)
- [x] 0.5.5 Fixed catalyst tags — added missing sub-tags (16 tags across 10 catalysts) per PathOfCrafting source
- [x] 0.5.6 Imported 40 exclusion groups — `exclusion_group/4` predicate (mutually exclusive mod patterns)
- [x] 0.5.7 Imported 3 modifier exclusions — `modifier_exclusion/4` predicate (ES hybrid mods restricted from boots/gloves)
- [x] 0.5.8 138 Python tests pass, SWI-Prolog loads 0 errors
- [ ] 0.5.9 Alloy tags need verification (8/13 may have wrong GuaranteedModTag — no alloys.json in PathOfCrafting source)
- [ ] 0.5.10 Spot-check imported data vs poe2db.tw (3-5 categories)
- [ ] 0.5.11 Serve exclusion groups via API + frontend display

## Phase A: Crafting Simulator (HIGH PRIORITY)

### A.1 Weighted Rolling Engine
- [x] A.1.1 Create `simulator.py` with `weighted_roll(items)` core
- [x] A.1.2 `roll_mod(category, slot, ilvl, exclude, guarantee)` — weighted random selection
- [x] A.1.3 Multi-mod rolling: transmute (1-2), alchemy (4-6), exalt (1), chaos (reroll)
- [x] A.1.4 Essence rolling: guarantee one mod, roll rest from pool
- [x] A.1.5 Omen-modified rolling: sinistral/dextral targeting (10 omen effect handlers, 24 tests)
- [x] A.1.6 Exclusion group enforcement — fuzzy stat_text→group mapping (40 groups, 12 tests)
- [x] A.1.7 Unit tests for rolling engine (19 tests)

### A.2 Sequence Executor
- [x] A.2.1 `run_single(base, ilvl, steps)` — execute one crafting sequence
- [x] A.2.2 Step types: apply_currency, apply_essence, apply_catalyst, spam
- [x] A.2.3 Condition checking: has_mod, not_has_mod, prefix_count, suffix_count, rarity_is
- [x] A.2.4 Branching: on_success continue/goto/stop, on_failure continue/loop/restart/abort
- [x] A.2.5 Goto/loop with max-iteration guard (max_total_steps)
- [x] A.2.6 Per-run tracking: item state, cost, steps, success/fail
- [x] A.2.7 Unit tests for executor (8 tests)

### A.3 Monte Carlo Runner
- [x] A.3.1 `run_sequence(base, ilvl, steps, n=1000)` — aggregate N runs
- [x] A.3.2 Results: success_rate, avg/median cost, cost histogram
- [x] A.3.3 Outcome distribution: which mods appeared most
- [x] A.3.4 Best/worst items across runs
- [x] A.3.5 Configurable iterations (1000 default, 10000 max)
- [x] A.3.6 `POST /api/simulate` endpoint
- [x] A.3.7 `POST /api/simulate/step` endpoint (Calculator mode)
- [x] A.3.8 API integration tests (7 tests)

### A.4 Simulator Frontend (in One Ring dashboard)
- [x] A.4.1 Step builder: add/remove/reorder, currency dropdown, omen dropdown, condition builder
- [x] A.4.2 Run button + progress + results display
- [x] A.4.3 Results: success rate, cost stats, histogram, outcome table
- [ ] A.4.4 Flowchart visualization (SVG)
- [x] A.4.5 Single Step Test button

## Phase B: Probability Calculator (MEDIUM PRIORITY)

- [ ] B.1 `POST /api/calculate` — single-step odds
- [ ] B.2 Group logic (G1/G2/G3) — "any of group" vs "all groups"
- [ ] B.3 Probability per method: chaos spam, essence+chaos, omen-assisted, exalt
- [ ] B.4 Method comparison table (expected cost across methods)
- [ ] B.5 Calculator frontend: mod pool, click-to-select, results
- [ ] B.6 Mass simulation validation (1M iterations to verify)

## Phase C: Crafting Emulator (LOWER PRIORITY)

- [ ] C.1 `CraftingEmulator` class — item state + random rolling
- [ ] C.2 `POST /api/emulator/create`
- [ ] C.3 `POST /api/emulator/apply`
- [ ] C.4 `POST /api/emulator/undo`
- [ ] C.5 `GET /api/emulator/state`
- [ ] C.6 `GET /api/emulator/mod_pool`
- [ ] C.7 `POST /api/emulator/export`
- [ ] C.8 Frontend: item display, currency toolbar, mod pool, history, spending
- [ ] C.9 Item import (in-game item → sandbox)
- [ ] C.10 Cross-tool: Emulator → Simulator export
