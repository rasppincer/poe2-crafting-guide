# Path of Exile 2 - Quality Mechanics for Jewelry

> Sources: [PoE2DB](https://poe2db.tw/us/Catalysts), [PoE 2 Wiki](https://www.poe2wiki.net/wiki/Quality)
> Last updated: 2026-06-09

---

## Overview: Quality by Item Type

| Item Type | Currency Used | Effect per 1% Quality |
|---|---|---|
| Martial Weapons | Blacksmith's Whetstone | 1% more local Physical Damage |
| Wands, Sceptres, Staves | Arcanist's Etcher | +1% to inherent skill quality |
| Armour (equipment) | Armourer's Scrap | 1% more local Defence (Armour/Evasion/ES/Runic Ward) |
| **Rings & Amulets** | **Catalysts** | **1% increased modifier magnitude** (tag-specific) |
| Flasks | Glassblower's Bauble | 1% more local Life/Mana Recovery |
| Charms | (drops only) | 1% increased local Duration |
| Skill Gems | Gemcutter's Prism | Varies by skill |
| **Belts** | **N/A - Cannot have quality** | **No effect (exception item)** |
| Quivers | N/A - Cannot have quality | No effect (exception item) |
| Jewels | N/A - Cannot have quality | No effect (exception item) |

---

## Rings & Amulets: How Quality Works

### Core Mechanic
- Quality on rings and amulets **increases the magnitude of modifiers** that match a specific tag
- Each 1% quality = 1% increased modifier magnitude for the tagged modifier type
- Quality is applied as a **unique multiplier** after all other modifiers (including corruption/sanctification)
- Values are truncated after quality is applied

### Quality Types (Catalysts)
Catalysts are currency items that drop exclusively from the **Breach** mechanic. There are two categories:
1. **Jewellery Catalysts** - affect rings and amulets
2. **Jewel Catalysts** - affect jewels (separate system)

Using a different catalyst type **replaces** the existing quality type and resets to 0%.

### Jewellery Catalysts (for Rings & Amulets)

| Catalyst | Modifier Tag Enhanced | Stack Size |
|---|---|---|
| Flesh Catalyst | Life modifiers | 10 |
| Neural Catalyst | Mana modifiers | 10 |
| Carapace Catalyst | Armour, Evasion, Energy Shield modifiers | 10 |
| Uul-Netol's Catalyst | Physical modifiers | 10 |
| Xoph's Catalyst | Fire modifiers | 10 |
| Tul's Catalyst | Cold modifiers | 10 |
| Esh's Catalyst | Lightning modifiers | 10 |
| Chayula's Catalyst | Chaos modifiers | 10 |
| Reaver Catalyst | Attack modifiers | 10 |
| Sibilant Catalyst | Caster modifiers | 10 |
| Skittering Catalyst | Speed modifiers | 10 |
| Adaptive Catalyst | Attribute modifiers | 10 |

### Refined Catalysts (Higher Tier)
Refined versions of each catalyst exist (e.g., Refined Flesh Catalyst, Refined Xoph's Catalyst). These are higher-tier variants that provide more quality per use.

---

## Quality Caps & Maximum Values

| Item Type | Default Max | Special Max |
|---|---|---|
| Standard Rings & Amulets | 20% | — |
| Breach Rings | 20% (base) | **40%** (implicit modifier) |
| Refined Breach Rings | 20% (base) | **45%** (via Genesis Tree) |
| Items with Essence of the Breach | 20% (base) | **40%** (+20% crafted modifier) |
| Items from Infuser | up to **30%** | Random, may corrupt |

---

## Quality and Mod Weights

### How Quality Affects Crafting
- Quality does **NOT** change mod weights (the probability of rolling specific modifiers)
- Quality **increases the magnitude** (numerical values) of existing modifiers that match the catalyst's tag
- This is a **post-roll multiplier** — it enhances values after the mod is already on the item

### Crafting Implications
1. **Apply quality BEFORE crafting** - Since quality increases modifier magnitude, having quality on the item when you roll modifiers means those modifiers will have higher values
2. **Choose the right catalyst** - Match the catalyst to the modifiers you want to enhance
3. **Quality interacts with crafting** - When using currency like Orbs of Alchemy or Chaos Orbs, having quality already on the item means the resulting modifiers of the matching tag will be magnified

### Important Notes
- Quality is a **unique multiplier** — it does not stack additively with other increased modifier effects
- Quality is applied **after** all other modifiers including corruption/sanctification
- Values are **truncated** (rounded down) after quality is applied
- Higher item level items get less quality per catalyst use
- Catalysts have greater effect on lower item level, non-unique jewellery

---

## Belts: Quality Status

**Belts CANNOT have quality in Path of Exile 2.**

Belts are explicitly listed as exceptions alongside Quivers and Jewels. There is no currency item that can add quality to belts. This means:
- No Armourer's Scrap for belts
- No Catalyst for belts
- No quality-based modifier enhancement for belt crafting

---

## Practical Crafting Tips

### For Ring Crafting:
1. Decide which modifier type you want to enhance (e.g., Fire for fire resistance rings)
2. Apply the matching catalyst (e.g., Xoph's Catalyst for Fire) to 20% quality
3. Then proceed with crafting (Alchemy, Chaos, Essences, etc.)
4. Fire-tagged modifiers will have 20% higher values

### For Amulet Crafting:
1. Identify your build's primary needs (attributes, damage type, defences)
2. Apply the appropriate catalyst before crafting
3. For +skill level amulets, consider whether Caster or specific element catalysts apply

### Breach Ring Strategy:
- Breach rings can reach 40% quality (45% if Refined)
- This means up to 40-45% increased modifier magnitude
- Extremely powerful for stacking specific modifier types
- Worth investing in high-quality catalysts for Breach ring crafting

---

## Key Differences from PoE 1

| Aspect | PoE 1 | PoE 2 |
|---|---|---|
| Catalyst source | Ultimatum encounters | Breach mechanic |
| Catalyst types | Similar but different names | New naming scheme |
| Quality effect | Enhances modifier values | Same - enhances modifier values |
| Belt quality | Catalysts could be used on belts | **Belts cannot have quality** |
| Max quality (standard) | 20% | 20% |
| Max quality (Breach rings) | 40% | 40% (45% Refined) |

---

## Catalyst Drop Source

Catalysts are **exclusive drops from the Breach mechanic** in PoE 2. They scale with area item quantity.
