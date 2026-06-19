%%% Mod data for bow
%%% Source: POE2-PathOfCrafting (frankthetank001/POE2-PathOfCrafting)
%%% Original data: poe2db.tw via weights.csv
%%% Auto-imported by import_from_pathofcrafting.py

%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)

mod_pool_weight_sum(bow, prefix, 7100).
mod_pool_weight_sum(bow, suffix, 11900).

mod_group(bow, 'PercentIncreasedElementalDamageWithAttacks', '#% increased Elemental Damage with Attacks', [attack, damage], 500, 100, 6, prefix).
mod_group(bow, 'PercentIncreasedPhysicalDamage', '#% increased Physical Damage', [physical, damage], 1000, 100, 8, prefix).
mod_group(bow, 'PercentIncreasedPhysicalDamageFlattoAccuracyRating', '#% increased Physical Damage, # to Accuracy Rating', [physical, damage, accuracy], 1000, 100, 8, prefix).
mod_group(bow, 'FlattoAccuracyRating', '# to Accuracy Rating', [accuracy], 800, 100, 10, prefix).
mod_group(bow, 'AddsFlattoflatColdDamage', 'Adds # to # Cold Damage', [cold, damage], 800, 100, 10, prefix).
mod_group(bow, 'AddsFlattoflatFireDamage', 'Adds # to # Fire Damage', [fire, damage], 800, 100, 10, prefix).
mod_group(bow, 'AddsFlattoflatLightningDamage', 'Adds # to # Lightning Damage', [lightning, damage], 1200, 100, 10, prefix).
mod_group(bow, 'AddsFlattoflatPhysicalDamage', 'Adds # to # Physical Damage', [physical, damage], 1000, 100, 9, prefix).

mod_group(bow, 'PercentIncreasedAttackSpeed', '#% increased Attack Speed', [attack, speed], 1000, 100, 5, suffix).
mod_group(bow, 'FlattoAccuracyRatingPercentIncreasedLightRadius', '# to Accuracy Rating, #% increased Light Radius', [accuracy], 1000, 100, 3, suffix).
mod_group(bow, 'PercentReducedAttributeRequirements', '#% reduced Attribute Requirements', [], 1000, 100, 5, suffix).
mod_group(bow, 'FlattoDexterity', '# to Dexterity', [attribute], 1000, 100, 8, suffix).
mod_group(bow, 'FlattoLevelOfAllProjectileSkills', '# to Level of all Projectile Skills', [], 1000, 100, 5, suffix).
mod_group(bow, 'PercentToCriticalDamageBonus', '#% to Critical Damage Bonus', [critical, damage], 1000, 100, 6, suffix).
mod_group(bow, 'PercentToCriticalHitChance', '#% to Critical Hit Chance', [critical], 1000, 100, 6, suffix).
mod_group(bow, 'PercentSurpassingChanceToFireAnAdditionalArrow', '#% Surpassing chance to fire an additional Arrow', [fire], 400, 100, 4, suffix).
mod_group(bow, 'GainFlatLifePerEnemyKilled', 'Gain # Life per Enemy Killed', [life], 750, 100, 8, suffix).
mod_group(bow, 'GainFlatManaPerEnemyKilled', 'Gain # Mana per Enemy Killed', [mana], 750, 100, 8, suffix).
mod_group(bow, 'GrantsFlatLifePerEnemyHit', 'Grants # Life per Enemy Hit', [life], 1000, 100, 4, suffix).
mod_group(bow, 'LeechesPercentOfPhysicalDamageAsLife', 'Leeches #% of Physical Damage as Life', [life, physical, damage, leech], 1000, 100, 4, suffix).
mod_group(bow, 'LeechesPercentOfPhysicalDamageAsMana', 'Leeches #% of Physical Damage as Mana', [mana, physical, damage, leech], 1000, 100, 4, suffix).

