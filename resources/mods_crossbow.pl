%%% Mod data for crossbow
%%% Source: POE2-PathOfCrafting (frankthetank001/POE2-PathOfCrafting)
%%% Original data: poe2db.tw via weights.csv
%%% Auto-imported by import_from_pathofcrafting.py

%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)

mod_pool_weight_sum(crossbow, prefix, 7100).
mod_pool_weight_sum(crossbow, suffix, 11750).

mod_group(crossbow, 'PercentIncreasedElementalDamageWithAttacks', '#% increased Elemental Damage with Attacks', [attack, damage], 500, 100, 6, prefix).
mod_group(crossbow, 'PercentIncreasedPhysicalDamage', '#% increased Physical Damage', [physical, damage], 1000, 100, 8, prefix).
mod_group(crossbow, 'PercentIncreasedPhysicalDamageFlattoAccuracyRating', '#% increased Physical Damage, # to Accuracy Rating', [physical, damage, accuracy], 1000, 100, 8, prefix).
mod_group(crossbow, 'FlattoAccuracyRating', '# to Accuracy Rating', [accuracy], 800, 100, 10, prefix).
mod_group(crossbow, 'AddsFlattoflatColdDamage', 'Adds # to # Cold Damage', [cold, damage], 800, 100, 10, prefix).
mod_group(crossbow, 'AddsFlattoflatFireDamage', 'Adds # to # Fire Damage', [fire, damage], 1000, 100, 10, prefix).
mod_group(crossbow, 'AddsFlattoflatLightningDamage', 'Adds # to # Lightning Damage', [lightning, damage], 1000, 100, 10, prefix).
mod_group(crossbow, 'AddsFlattoflatPhysicalDamage', 'Adds # to # Physical Damage', [physical, damage], 1000, 100, 9, prefix).

mod_group(crossbow, 'PercentIncreasedAttackSpeed', '#% increased Attack Speed', [attack, speed], 1000, 100, 5, suffix).
mod_group(crossbow, 'FlattoAccuracyRatingPercentIncreasedLightRadius', '# to Accuracy Rating, #% increased Light Radius', [accuracy], 1000, 100, 3, suffix).
mod_group(crossbow, 'PercentReducedAttributeRequirements', '#% reduced Attribute Requirements', [], 1000, 100, 5, suffix).
mod_group(crossbow, 'FlattoDexterity', '# to Dexterity', [attribute], 500, 100, 8, suffix).
mod_group(crossbow, 'FlattoLevelOfAllProjectileSkills', '# to Level of all Projectile Skills', [], 1000, 100, 5, suffix).
mod_group(crossbow, 'FlattoStrength', '# to Strength', [attribute], 500, 100, 8, suffix).
mod_group(crossbow, 'PercentToCriticalDamageBonus', '#% to Critical Damage Bonus', [critical, damage], 1000, 100, 6, suffix).
mod_group(crossbow, 'PercentToCriticalHitChance', '#% to Critical Hit Chance', [critical], 1000, 100, 6, suffix).
mod_group(crossbow, 'GainFlatLifePerEnemyKilled', 'Gain # Life per Enemy Killed', [life], 750, 100, 8, suffix).
mod_group(crossbow, 'GainFlatManaPerEnemyKilled', 'Gain # Mana per Enemy Killed', [mana], 750, 100, 8, suffix).
mod_group(crossbow, 'GrantsFlatLifePerEnemyHit', 'Grants # Life per Enemy Hit', [life], 1000, 100, 4, suffix).
mod_group(crossbow, 'LeechesPercentOfPhysicalDamageAsLife', 'Leeches #% of Physical Damage as Life', [life, physical, damage, leech], 1000, 100, 4, suffix).
mod_group(crossbow, 'LeechesPercentOfPhysicalDamageAsMana', 'Leeches #% of Physical Damage as Mana', [mana, physical, damage, leech], 1000, 100, 4, suffix).
mod_group(crossbow, 'LoadsFlatAdditionalBolts', 'Loads # additional bolts', [], 250, 100, 2, suffix).

