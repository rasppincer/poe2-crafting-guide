# Architecture — PoE 2 Crafting Knowledge Base

## Overview

The project has three layers. **This is a pure API server** — no frontend.
The UI lives in the [One Ring](../../one-ring/) dashboard project.

```
┌─────────────────────────────────────────────┐
│  API Server (Flask, port 8322)              │  app.py
│  JSON endpoints for DB, recipes, optimizer  │
│  Standalone: http://localhost:8322/api/     │
│  Via nginx:  /poe2-crafting/api/            │
├─────────────────────────────────────────────┤
│  Tests (pytest, 89 tests)                   │  tests/test_crafting_kb.py
│  Data integrity / Recipe validation / Omen  │  tests/test_recipes.py
│  versioning / Mod pool verification         │
├─────────────────────────────────────────────┤
│  Prolog KB (SWI-Prolog, 1005 lines)         │  poe2_crafting.pl
│  Primitives / Mod data / Currency rules     │  resources/mods_*.pl (7 files)
│  Omens / Alloys / Quality / Rolling engine  │
├─────────────────────────────────────────────┤
│  Source Data (JSON, from poe2db.tw)          │  resources/mods_*.json (7 files)
│  Omens / Alloys / Quality mechanics docs    │  resources/*.json, resources/*.md
└─────────────────────────────────────────────┘
```

## API Architecture Pattern

This project follows the **API-only** pattern from the One Ring hub:

- **Sub-projects** (this one, dax-losers, etc.) = pure API servers, no frontend
- **One Ring** = the frontend/dashboard layer that consumes APIs
- **nginx** = reverse proxy, routes requests to the right backend

Benefits:
- Each API is testable via curl/CLI, no browser needed
- nginx config is simple proxy_pass, no URL rewriting (sub_filter)
- Frontend is centralized — one place to update UI across all projects
- APIs work standalone (dev/testing) or through nginx (production)

## File Inventory

| File | Purpose |
|------|---------|
| `app.py` | Flask API server (no templates, no static files) |
| `poe2_crafting.pl` | Main Prolog KB — primitives, currency rules, engine |
| `resources/mods_*.pl` | Per-category mod data (consulted by main file) |
| `resources/mods_*.json` | Raw scraped data from poe2db (source of truth) |
| `resources/omens.json` | Full omen list from poe2db |
| `resources/alloys.json` | Alloy data |
| `resources/quality_mechanics.md` | Catalyst/quality system docs |
| `resources/version_050_changes.md` | 0.5.0 patch changes |
| `resources/patch_050_status.md` | Current system status |
| `primitives.md` | Human-readable primitive definitions (12 sections) |
| `recipes/` | Saved recipes (JSON, from Recipe Builder API) |
| `optimizer.py` | Recipe optimization engine |
| `verifier.py` | State-tracking recipe verification |
| `tests/test_crafting_kb.py` | Data integrity + Prolog syntax tests |
| `tests/test_recipes.py` | Recipe validation tests |

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Service info + available endpoints |
| `/health` | GET | Health check (returns mod_groups count) |
| `/api/database?game=poe1\|poe2\|all` | GET | Full DB dump (mod groups, omens, alloys, currencies) |
| `/api/database/refresh` | POST | Reload data from disk |
| `/api/recipes` | GET | All recipes (test fixtures + saved) |
| `/api/recipes/<name>` | GET | Single recipe by name |
| `/api/recipe/verify` | POST | Verify recipe steps against KB |
| `/api/optimize` | GET | Evaluate all recipes |
| `/api/optimize/<name>` | GET | Evaluate single recipe |
| `/api/mod_pool/<category>` | GET | Mod groups for a category |
| `/api/mod_probability/<cat>/<mod>` | GET | Probability of rolling a mod |
| `/api/prolog` | GET | Raw Prolog content |
| `/api/recipe-builder/list` | GET | List saved builder recipes |
| `/api/recipe-builder/save` | POST | Save a recipe |
| `/api/recipe-builder/load/<file>` | GET | Load a saved recipe |
| `/api/recipe-builder/delete/<file>` | DELETE | Delete a saved recipe |
| `/api/recipe-builder/export-prolog` | POST | Export recipe as Prolog facts |

## Prolog KB Structure

### Predicate Signatures

```prolog
% Primitives
rarity(+Rarity)                         % normal | magic | rare | unique
max_prefixes(+Rarity, -Max)
max_suffixes(+Rarity, -Max)
item_property(+Prop)                    % identified, corrupted, mirrored, ...
influence_type(+Type)                   % shaper, elder, crusader, ...
slot_type(+Slot)                        % prefix, suffix, implicit, ...

% Base Types
base_type(+BaseId, -info(Game, Category, ImplicitDesc))
base_category(+BaseId, -Category)       % ring, body_armour, weapon, ...
base_mod_pool(+BaseId, -ModPoolCat)     % ring, body_armour_str, weapon_sword, ...
mod_pool(+BaseCat, +Variant, -ModPool)  % body_armour × str → body_armour_str

% Mod Data (mod_group/8 — the core data predicate)
mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)
mod_pool_weight_sum(+Category, +Slot, -TotalWeight)
mod_tags(+Category, +ModGroup, -Tags)
mod_domain(+Category, +ModGroup, -Slot)
mod_weight(+Category, +ModGroup, -Weight)

% Rolling Engine (weighted random selection)
roll_mod(+Category, +Slot, +Ilvl, -ModGroup)
roll_prefixes(+Category, +Ilvl, +SeedGroups, -FinalGroups)
roll_suffixes(+Category, +Ilvl, +PrefixGroups, -SuffixGroups)
random_mod_for_slot(+Category, +Slot, +Ilvl, +Existing, -NewGroup)
roll_n_mods(+Category, +Slot, +Ilvl, +Already, +N, -Groups)
roll_probability(+Category, +ModGroup, -Prob)

% Item State
item_state(+Base, +Rarity, +Ilvl, +Influence, +Props, +Prefixes, +Suffixes, +Implicit)
has_open_slot(+Item, +SlotType)
count_mods(+Item, +Slot, -Count)

% Currencies
currency(+Game, +Name)
currency_precondition(+Currency, +ItemState)
currency_postcondition(+Currency, +OldItem, -NewItem)
can_apply(+Currency, +Item)
apply_currency(+Currency, +OldItem, -NewItem)

% Omens
omen(+Game, +Name, +Currency, +Effect, +SlotRestriction)
omen_disabled(+Name, +VersionDisabled)
omen_active(+Game, +Name, -Effect, -Slot)
can_use_omen(+Game, +Omen, +Currency)
omen_crafting_pairs(+Game, +Currency, -Sinistral, -Dextral)

% Alloys
alloy(+Game, +Name, +GuaranteedTag, +Description)
alloy_precondition(+Alloy, +Item)
alloy_postcondition(+Alloy, +OldItem, -NewItem)

% Quality
quality_type(+Game, +CatalystType, +TagsEnhanced)
quality_max(+ItemType, -MaxPercent)
quality_effect(+QualityPct, +ModTags, +CatalystType, -Multiplier)
```

### Item State Representation

```prolog
item_state(
    BaseId,      % atom: spirit_blade, jade_ring, plate_vest, ...
    Rarity,      % normal | magic | rare | unique
    Ilvl,        % integer: item level
    Influence,   % none | shaper | elder | crusader | ...
    Properties,  % list: [identified, corrupted, fractured, ...]
    Prefixes,    % list: [1IncreasedLife, 2FireResistance, ...]
    Suffixes,    % list: [2Strength, 2FireResistance, ...]
    Implicit     % implicit('description') | none
)
```

Quality is tracked separately (not in item_state) via `item_quality/3`.

### Weighted Rolling

Rolling uses real poe2db weights. A mod with weight 13000 in a pool of 54000
has a 24.1% chance of being selected. The engine expands weights into a flat
list where each atom appears `Weight` times, then picks randomly.

This means: **Life prefix on body_armour_str = 13000/54000 = 24.1%**
But: **Life prefix on ring = 8000/69500 = 11.5%** (different pool)

### Category → Mod Pool Mapping

```
base_type category → mod_pool/3 → mod pool category
ring → ring
body_armour × str → body_armour_str
body_armour × dex → body_armour_dex (not yet scraped)
helmet × str → helmet_str
weapon × str_dex → weapon_sword
```

## Design Decisions

1. **mod_group/8 includes category** — allows multiple item types in one KB
2. **Weight sums stored per category** — enables probability calculations
3. **Game versioning** — `current_game/1` + game-tagged data predicates (currency/2, omen/5, alloy/4, quality_type/3). Enforces PoE1 vs PoE2 separation at the data level.
4. **Quality NOT in item_state** — it's a post-roll multiplier, not a state
5. **Consulted .pl files** — data files loaded at startup, not hardcoded
6. **Recipes live in test files** — not in Prolog (yet), validated by pytest
7. **API-only, no frontend** — UI lives in One Ring dashboard, this project serves JSON
