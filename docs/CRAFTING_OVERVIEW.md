# PoE 2 Crafting System Overview (Patch 0.5.0)

A reference for developers who haven't played Path of Exile 2.

## Item Basics

Every item has:
- **Base type** — determines implicit mod, defence/damage stats, which mods can roll
- **Rarity** — normal (white), magic (blue, up to 2 mods), rare (yellow, up to 6 mods), unique (fixed)
- **Item level (ilvl)** — determines which mod tiers can roll (higher ilvl = better tiers)
- **Modifiers** — prefix (max 3) and suffix (max 3) slots on rare items
- **Quality** — increases magnitude (not weight) for matching-tag mods

## Mod Rolling

When a currency adds a random mod:
1. The game picks prefix or suffix (50/50 if both open)
2. It selects a mod group weighted by poe2db weights (higher weight = more likely)
3. It picks a tier within that group based on ilvl
4. It rolls a numeric value within the tier's range

Example: On a ring, rolling a prefix has these probabilities:
- Life (1IncreasedLife): 8000/69500 = 11.5%
- Mana (1IncreasedMana): 12000/69500 = 17.3%
- Evasion (1IncreasedEvasionRating): 9000/69500 = 12.9%
- Physical Damage: 7800/69500 = 11.2%
- Fire/Cold/Lightning Damage: 3900/69500 = 5.6% each

## Crafting Currencies

| Currency | What It Does |
|----------|-------------|
| Orb of Transmutation | normal → magic (1-2 mods) |
| Orb of Alteration | magic → magic (reroll all mods) |
| Orb of Augmentation | magic + open slot → add 1 mod |
| Orb of Alchemy | normal → rare (4-6 mods) |
| Chaos Orb | rare → rare (reroll all mods) |
| Regal Orb | magic → rare (add 1 mod) |
| Exalted Orb | rare + open slot → add 1 mod |
| Orb of Annulment | magic/rare → remove 1 random mod |
| Orb of Scouring | magic/rare → normal (remove all mods) |
| Divine Orb | reroll numeric values (same mods) |
| Vaal Orb | corrupt item (random effect) |
| Orb of Chance | normal → random rarity |

## Omens — Deterministic Crafting

Omens modify the next currency used. Key active pairs (0.5.0):

| Omen | With | Effect |
|------|------|--------|
| Sinistral Annulment | Orb of Annulment | Removes **prefix** (not random) |
| Dextral Annulment | Orb of Annulment | Removes **suffix** (not random) |
| Sinistral Exaltation | Exalted Orb | Adds **prefix** (not random slot) |
| Dextral Exaltation | Exalted Orb | Adds **suffix** (not random slot) |
| Sinistral Erasure | Chaos Orb | Removes only prefixes |
| Dextral Erasure | Chaos Orb | Removes only suffixes |

This is the core of deterministic crafting in PoE 2. Without omens, annulment
is 50/50. With Sinistral Annulment, it's 100% prefix removal.

## Essences

Essences guarantee a specific mod when used. Essence of Greed guarantees a life
mod. They work like Alchemy but with one mod forced.

## Alloys (0.5.0)

Alloys replace a random mod with a guaranteed one of a specific tag.
Example: Sovereign Alloy removes 1 mod, adds an attack-tagged mod.
Only work on rare items.

## Quality / Catalysts

Catalysts add quality to rings/amulets. Each 1% quality = 1% increased
modifier magnitude for matching tags. Apply BEFORE crafting for max effect.

Example: 20% Flesh Catalyst on a ring → all life mods on that ring have
20% higher numeric values.

Belts CANNOT have quality in PoE 2.

## Desecrated Modifiers

A separate crafting system from Abyss content. Adds special mods via
Preserved Bone → Well of Souls. Limited to 1 desecrated mod per item.
The Ulaman/Amanamu/Kurgal system adds Abyss-specific mods.

## Key Differences from PoE 1

| Aspect | PoE 1 | PoE 2 |
|--------|-------|-------|
| Metacrafting bench | "Prefixes cannot be changed" | **Omens** (consumable items) |
| Belt quality | Catalysts work | **Cannot have quality** |
| Recombination | Active | **Disabled in 0.5.0** |
| Essence crafting | Essences + meta | Essences + Omens |
| Mod targeting | Bench crafts | **Omen pairs** (sinistral/dextral) |
| Influence | Shaper/Elder/etc | Still exists but different |
