%%% Mod data for ring
%%% Source: POE2-PathOfCrafting (frankthetank001/POE2-PathOfCrafting)
%%% Original data: poe2db.tw via weights.csv
%%% Auto-imported by import_from_pathofcrafting.py

%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)

mod_pool_weight_sum(ring, prefix, 9300).
mod_pool_weight_sum(ring, suffix, 15950).

mod_group(ring, 'PercentIncreasedChaosDamage', '#% increased Chaos Damage', [chaos, damage], 500, 100, 6, prefix).
mod_group(ring, 'PercentIncreasedColdDamage', '#% increased Cold Damage', [cold, damage], 500, 100, 6, prefix).
mod_group(ring, 'PercentIncreasedFireDamage', '#% increased Fire Damage', [fire, damage], 500, 100, 6, prefix).
mod_group(ring, 'PercentIncreasedLightningDamage', '#% increased Lightning Damage', [lightning, damage], 500, 100, 6, prefix).
mod_group(ring, 'PercentIncreasedRarityOfItemsFound', '#% increased Rarity of Items found', [rarity], 1000, 100, 3, prefix).
mod_group(ring, 'FlattoAccuracyRating', '# to Accuracy Rating', [accuracy], 800, 100, 8, prefix).
mod_group(ring, 'FlattoEvasionRating', '# to Evasion Rating', [evasion], 1000, 100, 9, prefix).
mod_group(ring, 'FlattoMaximumLife', '# to maximum Life', [life], 1000, 100, 8, prefix).
mod_group(ring, 'FlattoMaximumMana', '# to maximum Mana', [mana], 1000, 100, 12, prefix).
mod_group(ring, 'AddsFlattoflatColdDamageToAttacks', 'Adds # to # Cold damage to Attacks', [cold, attack, damage], 500, 100, 9, prefix).
mod_group(ring, 'AddsFlattoflatFireDamageToAttacks', 'Adds # to # Fire damage to Attacks', [fire, attack, damage], 500, 100, 9, prefix).
mod_group(ring, 'AddsFlattoflatLightningDamageToAttacks', 'Adds # to # Lightning damage to Attacks', [lightning, attack, damage], 500, 100, 9, prefix).
mod_group(ring, 'AddsFlattoflatPhysicalDamageToAttacks', 'Adds # to # Physical Damage to Attacks', [physical, attack, damage], 1000, 100, 9, prefix).

mod_group(ring, 'FlatLifeRegenerationPerSecond', '# Life Regeneration per second', [life, regeneration], 1000, 100, 7, suffix).
mod_group(ring, 'PercentIncreasedCastSpeed', '#% increased Cast Speed', [caster, speed], 1000, 100, 4, suffix).
mod_group(ring, 'PercentIncreasedManaRegenerationRatePercentIncreasedLightRadius', '#% increased Mana Regeneration Rate, #% increased Light Radius', [mana, regeneration], 1000, 100, 3, suffix).
mod_group(ring, 'PercentIncreasedManaRegenerationRate', '#% increased Mana Regeneration Rate', [mana, regeneration], 1000, 100, 6, suffix).
mod_group(ring, 'PercentIncreasedRarityOfItemsFound', '#% increased Rarity of Items found', [rarity], 1000, 100, 3, suffix).
mod_group(ring, 'FlattoAllAttributes', '# to all Attributes', [attribute], 400, 100, 4, suffix).
mod_group(ring, 'FlattoDexterity', '# to Dexterity', [attribute], 1000, 100, 8, suffix).
mod_group(ring, 'FlattoIntelligence', '# to Intelligence', [attribute], 1000, 100, 8, suffix).
mod_group(ring, 'FlattoStrength', '# to Strength', [attribute], 1000, 100, 8, suffix).
mod_group(ring, 'PercentToAllElementalResistances', '#% to all Elemental Resistances', [resistance], 800, 100, 5, suffix).
mod_group(ring, 'PercentToChaosResistance', '#% to Chaos Resistance', [chaos, resistance], 250, 100, 6, suffix).
mod_group(ring, 'PercentToColdResistance', '#% to Cold Resistance', [cold, resistance], 1000, 100, 8, suffix).
mod_group(ring, 'PercentToFireResistance', '#% to Fire Resistance', [fire, resistance], 1000, 100, 8, suffix).
mod_group(ring, 'PercentToLightningResistance', '#% to Lightning Resistance', [lightning, resistance], 1000, 100, 8, suffix).
mod_group(ring, 'GainFlatLifePerEnemyKilled', 'Gain # Life per Enemy Killed', [life], 750, 100, 6, suffix).
mod_group(ring, 'GainFlatManaPerEnemyKilled', 'Gain # Mana per Enemy Killed', [mana], 750, 100, 6, suffix).
mod_group(ring, 'LeechPercentOfPhysicalAttackDamageAsLife', 'Leech #% of Physical Attack Damage as Life', [life, physical, attack, damage, leech], 1000, 100, 3, suffix).
mod_group(ring, 'LeechPercentOfPhysicalAttackDamageAsMana', 'Leech #% of Physical Attack Damage as Mana', [mana, physical, attack, damage, leech], 1000, 100, 3, suffix).

