%%% Mod data for one_hand_mace
%%% Source: POE2-PathOfCrafting (frankthetank001/POE2-PathOfCrafting)
%%% Original data: poe2db.tw via weights.csv
%%% Auto-imported by import_from_pathofcrafting.py

%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)

mod_pool_weight_sum(one_hand_mace, prefix, 7100).
mod_pool_weight_sum(one_hand_mace, suffix, 13500).

mod_group(one_hand_mace, 'PercentIncreasedElementalDamageWithAttacks', '#% increased Elemental Damage with Attacks', [attack, damage], 500, 100, 6, prefix).
mod_group(one_hand_mace, 'PercentIncreasedPhysicalDamage', '#% increased Physical Damage', [physical, damage], 1000, 100, 8, prefix).
mod_group(one_hand_mace, 'PercentIncreasedPhysicalDamageFlattoAccuracyRating', '#% increased Physical Damage, # to Accuracy Rating', [physical, damage, accuracy], 1000, 100, 8, prefix).
mod_group(one_hand_mace, 'FlattoAccuracyRating', '# to Accuracy Rating', [accuracy], 800, 100, 9, prefix).
mod_group(one_hand_mace, 'AddsFlattoflatColdDamage', 'Adds # to # Cold Damage', [cold, damage], 800, 100, 10, prefix).
mod_group(one_hand_mace, 'AddsFlattoflatFireDamage', 'Adds # to # Fire Damage', [fire, damage], 1200, 100, 10, prefix).
mod_group(one_hand_mace, 'AddsFlattoflatLightningDamage', 'Adds # to # Lightning Damage', [lightning, damage], 800, 100, 10, prefix).
mod_group(one_hand_mace, 'AddsFlattoflatPhysicalDamage', 'Adds # to # Physical Damage', [physical, damage], 1000, 100, 9, prefix).

mod_group(one_hand_mace, 'PercentIncreasedAttackSpeed', '#% increased Attack Speed', [attack, speed], 1000, 100, 8, suffix).
mod_group(one_hand_mace, 'FlattoAccuracyRatingPercentIncreasedLightRadius', '# to Accuracy Rating, #% increased Light Radius', [accuracy], 1000, 100, 3, suffix).
mod_group(one_hand_mace, 'PercentIncreasedStunDuration', '#% increased Stun Duration', [stun], 1000, 100, 6, suffix).
mod_group(one_hand_mace, 'PercentReducedAttributeRequirements', '#% reduced Attribute Requirements', [], 1000, 100, 5, suffix).
mod_group(one_hand_mace, 'FlattoLevelOfAllMeleeSkills', '# to Level of all Melee Skills', [], 1000, 100, 5, suffix).
mod_group(one_hand_mace, 'FlattoStrength', '# to Strength', [attribute], 1000, 100, 8, suffix).
mod_group(one_hand_mace, 'PercentToCriticalDamageBonus', '#% to Critical Damage Bonus', [critical, damage], 1000, 100, 6, suffix).
mod_group(one_hand_mace, 'PercentToCriticalHitChance', '#% to Critical Hit Chance', [critical], 1000, 100, 6, suffix).
mod_group(one_hand_mace, 'CausesPercentIncreasedStunBuildup', 'Causes #% increased Stun Buildup', [stun], 1000, 100, 6, suffix).
mod_group(one_hand_mace, 'GainFlatLifePerEnemyKilled', 'Gain # Life per Enemy Killed', [life], 750, 100, 8, suffix).
mod_group(one_hand_mace, 'GainFlatManaPerEnemyKilled', 'Gain # Mana per Enemy Killed', [mana], 750, 100, 8, suffix).
mod_group(one_hand_mace, 'GrantsFlatLifePerEnemyHit', 'Grants # Life per Enemy Hit', [life], 1000, 100, 4, suffix).
mod_group(one_hand_mace, 'LeechesPercentOfPhysicalDamageAsLife', 'Leeches #% of Physical Damage as Life', [life, physical, damage, leech], 1000, 100, 5, suffix).
mod_group(one_hand_mace, 'LeechesPercentOfPhysicalDamageAsMana', 'Leeches #% of Physical Damage as Mana', [mana, physical, damage, leech], 1000, 100, 5, suffix).

