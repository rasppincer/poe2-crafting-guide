%%% Mod data for quiver
%%% Source: POE2-PathOfCrafting (frankthetank001/POE2-PathOfCrafting)
%%% Original data: poe2db.tw via weights.csv
%%% Auto-imported by import_from_pathofcrafting.py

%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)

mod_pool_weight_sum(quiver, prefix, 4800).
mod_pool_weight_sum(quiver, suffix, 6000).

mod_group(quiver, 'PercentIncreasedDamageWithBowSkills', '#% increased Damage with Bow Skills', [damage], 500, 100, 6, prefix).
mod_group(quiver, 'PercentIncreasedProjectileSpeed', '#% increased Projectile Speed', [speed], 1000, 100, 3, prefix).
mod_group(quiver, 'FlattoAccuracyRating', '# to Accuracy Rating', [accuracy], 800, 100, 9, prefix).
mod_group(quiver, 'AddsFlattoflatColdDamageToAttacks', 'Adds # to # Cold damage to Attacks', [cold, attack, damage], 500, 100, 9, prefix).
mod_group(quiver, 'AddsFlattoflatFireDamageToAttacks', 'Adds # to # Fire damage to Attacks', [fire, attack, damage], 500, 100, 9, prefix).
mod_group(quiver, 'AddsFlattoflatLightningDamageToAttacks', 'Adds # to # Lightning damage to Attacks', [lightning, attack, damage], 500, 100, 9, prefix).
mod_group(quiver, 'AddsFlattoflatPhysicalDamageToAttacks', 'Adds # to # Physical Damage to Attacks', [physical, attack, damage], 1000, 100, 9, prefix).

mod_group(quiver, 'PercentChanceToPierceAnEnemy', '#% chance to Pierce an Enemy', [], 500, 100, 5, suffix).
mod_group(quiver, 'PercentIncreasedAttackSpeed', '#% increased Attack Speed', [attack, speed], 500, 100, 4, suffix).
mod_group(quiver, 'PercentIncreasedCriticalDamageBonusForAttackDamage', '#% increased Critical Damage Bonus for Attack Damage', [attack, critical, damage], 1000, 100, 6, suffix).
mod_group(quiver, 'PercentIncreasedCriticalHitChanceForAttacks', '#% increased Critical Hit Chance for Attacks', [attack, critical], 1000, 100, 6, suffix).
mod_group(quiver, 'FlattoDexterity', '# to Dexterity', [attribute], 1000, 100, 8, suffix).
mod_group(quiver, 'FlattoLevelOfAllProjectileSkills', '# to Level of all Projectile Skills', [], 500, 100, 2, suffix).
mod_group(quiver, 'GainFlatLifePerEnemyKilled', 'Gain # Life per Enemy Killed', [life], 750, 100, 6, suffix).
mod_group(quiver, 'GainFlatManaPerEnemyKilled', 'Gain # Mana per Enemy Killed', [mana], 750, 100, 6, suffix).

