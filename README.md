# PoE 2 Crafting Compendium

A curated collection of crafting algorithms, methods, and theorycrafting for **Path of Exile 2**.

## Goal

Document deterministic and probabilistic crafting workflows for Path of Exile 2 — step-by-step recipes for producing specific items, along with the reasoning behind each decision.

**Recipes are evaluated against optimization goals:**
- **`minimum_cost`** — cheapest method in expected currency expenditure
- **`minimum_interactions`** — fewest crafting steps (clicks) to reach the target
- **`maximum_values`** — highest possible numeric rolls on target mods

Each recipe declares its optimization goal and is validated against it. A recipe that achieves the target but uses 20 chaos orbs when 5 would suffice is flagged as suboptimal. The Prolog KB and test suite verify correctness; the optimization layer verifies efficiency.

**Every recipe must specify which game it's for** (`poe1` or `poe2`). PoE 1 and PoE 2 have fundamentally different crafting systems — mixing them produces invalid recipes.

## Scope

- **Crafting algorithms** — ordered sequences of steps (currency usage, bench crafts, essences, omens, recombinators, etc.) to produce target items
- **Theorycrafting** — probability analysis, expected cost calculations, method comparisons, and optimization
- **Base item knowledge** — item level breakpoints, mod tags, mod pool sizes, influence interactions
- **League-specific mechanics** — anything introduced in current or past PoE 2 leagues that affects crafting

## Sources

| Source | URL | Notes |
|--------|-----|-------|
| PoE 2 Wiki | https://www.poe2wiki.net/wiki/Path_of_Exile_2_Wiki | Game mechanics, mod lists, item bases |
| Craft of Exile (PoE 2) | https://www.craftofexile.com/?game=poe2 | Simulator, probability calculator, mod weights |
| poe2db.tw | https://poe2db.tw/ | Datamined mod tables, item bases, skill data |
| Official PoE 2 site | https://www.pathofexile2.com/ | Patch notes, league announcements |
| r/pathofexile2 | https://www.reddit.com/r/pathofexile2/ | Community discoveries, crafting showcases |
| PoE 2 Build Discords | various | Real-time crafting theorycrafting |

## API Server

This project is a **pure JSON API** — no frontend. The UI lives in the
[One Ring](https://github.com/rasppincer/one-ring) dashboard.

**Standalone** (direct access):
```
http://localhost:8322/api/database?game=poe2
http://localhost:8322/api/recipes
http://localhost:8322/api/optimize
http://localhost:8322/health
```

**Via nginx** (through One Ring hub):
```
http://localhost/poe2-crafting/api/database?game=poe2
http://localhost/poe2-crafting/api/recipes
```

Full API docs: `http://localhost:8322/` (returns endpoint list) or see
[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Structure

```
poe2-crafting-guide/
├── README.md                  ← you are here
├── app.py                     ← Flask API server (no templates)
├── poe2_crafting.pl           ← Prolog knowledge base
├── optimizer.py               ← Recipe optimization engine
├── verifier.py                ← State-tracking recipe verification
├── resources/                 ← Source data + Prolog data files
│   ├── mods_*.json            ← Raw scraped mod data from poe2db
│   ├── mods_*.pl              ← Prolog mod data (consulted at startup)
│   ├── omens.json
│   ├── alloys.json
│   └── *.md                   ← Mechanics documentation
├── recipes/                   ← Saved recipes (JSON, from Recipe Builder)
├── tests/                     ← pytest test suite (89 tests)
├── mechanics/                 ← how each crafting system works
├── algorithms/                ← step-by-step craft recipes
├── theorycraft/               ← probability, cost analysis, comparisons
└── resources/                 ← reference tables, mod lists, links
```

## Conventions

- Each algorithm file follows the template:
  1. **Target item** — base, mods, ilvl
  2. **Estimated cost** — average and worst-case
  3. **Steps** — numbered, each with rationale
  4. **Probability breakdown** — where applicable
  5. **Alternative methods** — trade-offs vs. the recommended path
  6. **Source/credit** — where the method was learned or tested

## Status

🟢 Project started — 2026-06-09

Contributing: add new algorithms as standalone files in `algorithms/`, update mechanics docs as game patches land.
