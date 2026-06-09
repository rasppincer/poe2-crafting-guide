# Adding New Item Categories

## Quick Steps

1. Scrape mod data from poe2db
2. Save as JSON + Prolog
3. Add consult directive to main KB
4. Add mod_pool/3 mapping
5. Add base_type/2 facts
6. Run tests

## 1. Scrape from poe2db

Navigate to the item category page. URLs follow this pattern:

```
https://poe2db.tw/us/{Category}
```

Known URLs:
- `Body_Armours_str`, `Body_Armours_dex`, `Body_Armours_int`
- `Helmets_str`, `Helmets_dex`, `Helmets_int`
- `Gloves_str`, `Gloves_dex`, `Gloves_int`
- `Boots_str`, `Boots_dex`, `Boots_int`
- `Rings`, `Amulets`, `Belts`
- `One_Hand_Swords`, `Two_Hand_Swords`, `One_Hand_Axes`, etc.
- `Shields_str`, `Shields_dex`, `Shields_int`

### DOM Extraction

Each mod is a `div.mod-title.explicitMod` element with:
- `data-gengroup` attribute = mod group ID (e.g. `1IncreasedLife`)
- `.badge.bg-danger` = weight (e.g. 13000)
- `.badge.bg-secondary` = max item level (e.g. 80)
- `.badge.bg-success` = tier count (e.g. 13)
- `.badge[data-tag]` = crafting tags (e.g. `life`, `armour`)

Extract via browser console:
```javascript
document.querySelectorAll('.mod-title.explicitMod').forEach(el => {
    const group = el.dataset.gengroup;
    const badges = el.querySelectorAll('.badge');
    const weight = parseInt(badges[0]?.textContent) || 0;
    const maxIlvl = parseInt(badges[1]?.textContent) || 0;
    const tiers = parseInt(badges[2]?.textContent) || 0;
    const tags = Array.from(el.querySelectorAll('.badge[data-tag]'))
        .map(b => b.dataset.tag);
    // ... collect into array
});
```

### Determine Section (Prefix/Suffix)

The mod is inside a `.col-lg-6` container with an `h5` header:
- "Base Prefix" → prefix
- "Base Suffix" → suffix

### Get Weight Sum

The `div.mod-total` at the bottom of each section has the total weight.

## 2. Save JSON

Save to `resources/mods_{category}.json`:

```json
{
  "item_category": "helmet_str",
  "source": "https://poe2db.tw/us/Helmets_str",
  "extracted": "2026-06-09",
  "base_prefixes": [
    {
      "group": "1IncreasedLife",
      "description": "+# to maximum Life",
      "tags": ["life"],
      "weight": 13000,
      "maxIlvl": 80,
      "tierCount": 13,
      "slot": "prefix"
    }
  ],
  "base_suffixes": [...],
  "weight_sum_prefixes": 54000,
  "weight_sum_suffixes": 73000
}
```

## 3. Generate Prolog File

Run the generator script (or manually create `resources/mods_{category}.pl`):

```prolog
%%% Mod data for helmet_str
%%% Source: https://poe2db.tw/us/Helmets_str

mod_pool_weight_sum(helmet_str, prefix, 56200).
mod_pool_weight_sum(helmet_str, suffix, 70000).

mod_group(helmet_str, 1IncreasedLife, '+# to maximum Life', [life], 13000, 80, 13, prefix).
mod_group(helmet_str, 2FireResistance, '#% to Fire Resistance', [elemental, fire, resistance], 8000, 82, 8, suffix).
```

## 4. Add Consult Directive

In `poe2_crafting.pl`, add:

```prolog
:- consult('resources/mods_helmet_str.pl').
```

## 5. Add Mod Pool Mapping

```prolog
mod_pool(helmet, str, helmet_str).
mod_pool(helmet, dex, helmet_dex).   % if scraped
```

## 6. Add Base Types

```prolog
base_type(iron_hat, info(poe2, helmet, '+6-12 Armour')).
```

## 7. Update Tests

Add the new category to `TestRecipeStructure::test_recipe_categories_have_mod_data`
if you're adding recipes that use it.

## Current Coverage

| Category | Status | Prefix | Suffix |
|----------|--------|--------|--------|
| body_armour_str | ✅ scraped | 7 | 10 |
| helmet_str | ✅ scraped | 8 | 13 |
| gloves_str | ✅ scraped | 10 | 17 |
| boots_str | ✅ scraped | 6 | 11 |
| ring | ✅ scraped | 13 | 18 |
| amulet | ✅ scraped | 12 | 18 |
| weapon_sword | ✅ scraped | 8 | 15 |
| body_armour_dex | ❌ not scraped | | |
| body_armour_int | ❌ not scraped | | |
| helmet_dex | ❌ not scraped | | |
| helmet_int | ❌ not scraped | | |
| shield_str | ❌ not scraped | | |
| belt | ❌ not scraped | | |
| weapon_bow | ❌ not scraped | | |
| weapon_staff | ❌ not scraped | | |
