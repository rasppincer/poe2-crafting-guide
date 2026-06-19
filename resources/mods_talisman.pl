%%% Mod data for talisman
%%% Source: POE2-PathOfCrafting (frankthetank001/POE2-PathOfCrafting)
%%% Original data: poe2db.tw via weights.csv
%%% Auto-imported by import_from_pathofcrafting.py

%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)

mod_pool_weight_sum(talisman, prefix, 7200).
mod_pool_weight_sum(talisman, suffix, 13500).

mod_group(talisman, 'PercentIncreasedElementalDamageWithAttacks', '#% increased Elemental Damage with Attacks', [attack, damage], 500, 100, 6, prefix).
mod_group(talisman, 'PercentIncreasedPhysicalDamage', '#% increased Physical Damage', [physical, damage], 1000, 100, 8, prefix).
mod_group(talisman, 'PercentIncreasedPhysicalDamageFlattoAccuracyRating', '#% increased Physical Damage, # to Accuracy Rating', [physical, damage, accuracy], 1000, 100, 8, prefix).
mod_group(talisman, 'FlattoAccuracyRating', '# to Accuracy Rating', [accuracy], 800, 100, 9, prefix).
mod_group(talisman, 'AddsFlattoflatColdDamage', 'Adds # to # Cold Damage', [cold, damage], 1000, 100, 10, prefix).
mod_group(talisman, 'AddsFlattoflatFireDamage', 'Adds # to # Fire Damage', [fire, damage], 1100, 100, 10, prefix).
mod_group(talisman, 'AddsFlattoflatLightningDamage', 'Adds # to # Lightning Damage', [lightning, damage], 800, 100, 10, prefix).
mod_group(talisman, 'AddsFlattoflatPhysicalDamage', 'Adds # to # Physical Damage', [physical, damage], 1000, 100, 9, prefix).

mod_group(talisman, 'PercentIncreasedAttackSpeed', '#% increased Attack Speed', [attack, speed], 1000, 100, 8, suffix).
mod_group(talisman, 'FlattoAccuracyRatingPercentIncreasedLightRadius', '# to Accuracy Rating, #% increased Light Radius', [accuracy], 1000, 100, 3, suffix).
mod_group(talisman, 'PercentIncreasedStunDuration', '#% increased Stun Duration', [stun], 1000, 100, 6, suffix).
mod_group(talisman, 'PercentReducedAttributeRequirements', '#% reduced Attribute Requirements', [], 1000, 100, 5, suffix).
mod_group(talisman, 'FlattoLevelOfAllMeleeSkills', '# to Level of all Melee Skills', [], 1000, 100, 5, suffix).
mod_group(talisman, 'FlattoStrength', '# to Strength', [attribute], 600, 100, 8, suffix).
mod_group(talisman, 'FlattoIntelligence', '# to Intelligence', [attribute], 400, 100, 8, suffix).
mod_group(talisman, 'PercentToCriticalDamageBonus', '#% to Critical Damage Bonus', [critical, damage], 1000, 100, 6, suffix).
mod_group(talisman, 'PercentToCriticalHitChance', '#% to Critical Hit Chance', [critical], 1000, 100, 6, suffix).
mod_group(talisman, 'CausesPercentIncreasedStunBuildup', 'Causes #% increased Stun Buildup', [stun], 1000, 100, 6, suffix).
mod_group(talisman, 'GainFlatLifePerEnemyKilled', 'Gain # Life per Enemy Killed', [life], 750, 100, 8, suffix).
mod_group(talisman, 'GainFlatManaPerEnemyKilled', 'Gain # Mana per Enemy Killed', [mana], 750, 100, 8, suffix).
mod_group(talisman, 'GrantsFlatLifePerEnemyHit', 'Grants # Life per Enemy Hit', [life], 1000, 100, 4, suffix).
mod_group(talisman, 'LeechesPercentOfPhysicalDamageAsLife', 'Leeches #% of Physical Damage as Life', [life, physical, damage, leech], 1000, 100, 5, suffix).
mod_group(talisman, 'LeechesPercentOfPhysicalDamageAsMana', 'Leeches #% of Physical Damage as Mana', [mana, physical, damage, leech], 1000, 100, 5, suffix).

