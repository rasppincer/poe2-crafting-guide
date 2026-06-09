# Scraping Mod Data from poe2db.tw

## Overview

Mod data is scraped from poe2db.tw's crafting calculator UI. Each item category
page has a "Modifiers Calc" tab that shows all available mod groups with their
weights, tiers, and tags.

## Step-by-Step

### 1. Navigate to the page

```
https://poe2db.tw/us/{Category}
```

Examples:
- `Body_Armours_str` — str body armours
- `Rings` — all rings
- `One_Hand_Swords` — 1H swords

### 2. Accept cookies if prompted

Click "Update cookie preferences" button if a consent banner appears.

### 3. Extract mod data via browser console

The page uses Bootstrap modals and dynamic rendering. The most reliable
extraction method is via JavaScript in the browser console:

```javascript
(function() {
    const mods = [];
    document.querySelectorAll('.mod-title.explicitMod').forEach(el => {
        const group = el.dataset.gengroup || '';
        const badges = el.querySelectorAll('.badge[data-tag]');
        const allBadges = el.querySelectorAll('.badge');

        // Extract tags
        const tags = Array.from(badges).map(b => b.dataset.tag);

        // Get weight/ilvl/tiers from the numeric badges
        const weight = parseInt(allBadges[0]?.textContent) || 0;
        const maxIlvl = parseInt(allBadges[1]?.textContent) || 0;
        const tierCount = parseInt(allBadges[2]?.textContent) || 0;

        // Get description text (before tag badges)
        const descContainer = el.querySelector('span:not(.float-end)');
        let desc = '';
        if (descContainer) {
            for (const c of descContainer.childNodes) {
                if (c.nodeType === 3) desc += c.textContent.trim() + ' ';
            }
        }

        // Determine section (prefix/suffix)
        const col = el.closest('.col-lg-6');
        const h5 = col ? col.querySelector('h5') : null;
        const section = h5 ? h5.textContent.trim() : '';
        const isPrefix = section.toLowerCase().includes('prefix');

        if (weight > 0) {
            mods.push({
                group, desc: desc.trim(), tags, weight, maxIlvl, tierCount,
                slot: isPrefix ? 'prefix' : 'suffix',
                section
            });
        }
    });

    // Get weight sums
    const totals = {};
    document.querySelectorAll('.mod-total').forEach(el => {
        const col = el.closest('.col-lg-6');
        const h5 = col ? col.querySelector('h5') : null;
        const section = h5 ? h5.textContent.trim() : '';
        const badge = el.querySelector('.badge.bg-danger');
        if (badge && section) {
            totals[section] = parseInt(badge.textContent) || 0;
        }
    });

    console.log(JSON.stringify({mods, totals}, null, 2));
})();
```

### 4. Copy the output

The output appears in the browser console. Copy it and save to a JSON file.

### 5. Clean and save

Save to `resources/mods_{category}.json` with this structure:

```json
{
  "item_category": "ring",
  "source": "https://poe2db.tw/us/Rings",
  "extracted": "2026-06-09",
  "base_prefixes": [...],
  "base_suffixes": [...],
  "weight_sum_prefixes": 69500,
  "weight_sum_suffixes": 87105
}
```

### 6. Generate Prolog file

Convert JSON to Prolog facts:

```bash
python3 -c "
import json
with open('resources/mods_ring.json') as f:
    d = json.load(f)
cat = d['item_category']
lines = [f'mod_pool_weight_sum({cat}, prefix, {d[\"weight_sum_prefixes\"]}).']
lines.append(f'mod_pool_weight_sum({cat}, suffix, {d[\"weight_sum_suffixes\"]}).')
for m in d['base_prefixes'] + d['base_suffixes']:
    tags = ', '.join(m['tags']) if m['tags'] else ''
    lines.append(f\"mod_group({cat}, {m['group']}, '{m['description']}', [{tags}], {m['weight']}, {m['maxIlvl']}, {m['tierCount']}, {m['slot']}).\")
with open(f'resources/mods_{cat}.pl', 'w') as f:
    f.write('\n'.join(lines) + '\n')
"
```

## Known Issues

- **Weight scale varies by category.** Body armour weights are ~1000-13000,
  weapon weights are ~5-15. This is a poe2db display difference, not a bug.
  The ratios within a category are what matter for probability calculations.

- **Tags may be incomplete.** Some mods on poe2db don't show tags in the UI.
  Cross-reference with the tag filter buttons at the top of the page.

- **Multi-line mods.** Some mods (like ailment resistance) span multiple lines
  in the poe2db UI. The description is concatenated.

- **Desecrated/Medved/Essence mods** are in separate sections with weight 0.
  These are special crafting outcomes, not natural rolls. We skip them for
  the base mod pool but they're still scraped in the JSON.

## Automation Notes

The scraping was done via Hermes Agent browser tools. The key DOM selectors are:
- `.mod-title.explicitMod` — each mod row
- `[data-gengroup]` — mod group ID attribute
- `.badge.bg-danger` — weight
- `.badge.bg-secondary` — max ilvl
- `.badge.bg-success` — tier count
- `.badge[data-tag]` — crafting tag
- `.mod-total .badge.bg-danger` — section weight sum
- `h5` — section headers ("Base Prefix", "Base Suffix")
