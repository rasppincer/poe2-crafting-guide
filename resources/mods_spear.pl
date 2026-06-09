%%% Mod data for spear
%%% Source: POE2-PathOfCrafting (frankthetank001/POE2-PathOfCrafting)
%%% Original data: poe2db.tw via weights.csv
%%% Imported: 2026-06-09

%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)

mod_pool_weight_sum(spear, prefix, 1205).
mod_pool_weight_sum(spear, suffix, 9950).

mod_group(spear, PercentIncreasedElementalDamageWithAttacks, '#% increased Elemental Damage with Attacks', [attack, damage], 500, 100, 6, prefix).
mod_group(spear, PercentIncreasedPhysicalDamage, '#% increased Physical Damage', [physical, damage], 25, 100, 8, prefix).
mod_group(spear, PercentIncreasedPhysicalDamageFlattoAccuracyRating, '#% increased Physical Damage, # to Accuracy Rating', [physical, damage, accuracy], 100, 100, 8, prefix).
mod_group(spear, FlattoAccuracyRating, '# to Accuracy Rating', [accuracy], 200, 100, 9, prefix).
mod_group(spear, AddsFlattoFlatColdDamage, 'Adds # to # Cold Damage', [cold, damage], 80, 100, 10, prefix).
mod_group(spear, AddsFlattoFlatFireDamage, 'Adds # to # Fire Damage', [fire, damage], 90, 100, 10, prefix).
mod_group(spear, AddsFlattoFlatLightningDamage, 'Adds # to # Lightning Damage', [lightning, damage], 110, 100, 10, prefix).
mod_group(spear, AddsFlattoFlatPhysicalDamage, 'Adds # to # Physical Damage', [physical, damage], 100, 100, 9, prefix).
mod_group(spear, PercentIncreasedAttackSpeed, '#% increased Attack Speed', [attack, speed], 100, 100, 8, suffix).
mod_group(spear, FlattoAccuracyRatingPercentIncreasedLightRadius, '# to Accuracy Rating, #% increased Light Radius', [accuracy], 1000, 100, 3, suffix).
mod_group(spear, PercentIncreasedStunDuration, '#% increased Stun Duration', [], 1000, 100, 6, suffix).
mod_group(spear, PercentReducedAttributeRequirements, '#% reduced Attribute Requirements', [attribute], 1000, 100, 5, suffix).
mod_group(spear, FlattoDexterity, '# to Dexterity', [attribute], 750, 100, 8, suffix).
mod_group(spear, FlattoLevelOfAllMeleeSkills, '# to Level of all Melee Skills', [], 50, 100, 5, suffix).
mod_group(spear, FlattoLevelOfAllProjectileSkills, '# to Level of all Projectile Skills', [], 50, 100, 5, suffix).
mod_group(spear, FlattoStrength, '# to Strength', [attribute], 250, 100, 8, suffix).
mod_group(spear, PercentToCriticalDamageBonus, '#% to Critical Damage Bonus', [critical, damage], 125, 100, 6, suffix).
mod_group(spear, PercentToCriticalHitChance, '#% to Critical Hit Chance', [critical], 125, 100, 6, suffix).
mod_group(spear, CausesPercentIncreasedStunBuildup, 'Causes #% increased Stun Buildup', [], 1000, 100, 6, suffix).
mod_group(spear, GainFlatLifePerEnemyKilled, 'Gain # Life per Enemy Killed', [life], 750, 100, 8, suffix).
mod_group(spear, GainFlatManaPerEnemyKilled, 'Gain # Mana per Enemy Killed', [mana], 750, 100, 8, suffix).
mod_group(spear, GrantsFlatLifePerEnemyHit, 'Grants # Life per Enemy Hit', [life], 1000, 100, 4, suffix).
mod_group(spear, LeechesPercentOfPhysicalDamageAsLife, 'Leeches #% of Physical Damage as Life', [life, physical, damage], 1000, 100, 5, suffix).
mod_group(spear, LeechesPercentOfPhysicalDamageAsMana, 'Leeches #% of Physical Damage as Mana', [mana, physical, damage], 1000, 100, 5, suffix).
