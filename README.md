# PoE 2 Crafting Compendium

A curated collection of crafting algorithms, methods, and theorycrafting for **Path of Exile 2**.

## Goal

Document deterministic and probabilistic crafting workflows — step-by-step recipes for producing specific items, along with the reasoning behind each decision (why a particular method is chosen over alternatives, expected costs, probability math, etc.).

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

## Structure

```
poe2-crafting-guide/
├── README.md                  ← you are here
├── mechanics/                 ← how each crafting system works
│   ├── currency.md
│   ├── essences.md
│   ├── omens.md
│   ├── recombinators.md
│   └── bench-crafts.md
├── algorithms/                ← step-by-step craft recipes
│   ├── <item-type>/<specific-craft>.md
│   └── ...
├── theorycraft/               ← probability, cost analysis, comparisons
│   ├── expected-cost-methods.md
│   └── mod-weight-math.md
└── resources/                 ← reference tables, mod lists, links
    ├── mod-tags.md
    └── ilvl-breakpoints.md
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
