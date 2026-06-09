%%% Mod data for warstaff
%%% Source: POE2-PathOfCrafting (frankthetank001/POE2-PathOfCrafting)
%%% Original data: poe2db.tw via weights.csv
%%% Imported: 2026-06-09

%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)

mod_pool_weight_sum(warstaff, prefix, 1205).
mod_pool_weight_sum(warstaff, suffix, 9950).

mod_group(warstaff, PercentIncreasedElementalDamageWithAttacks, '#% increased Elemental Damage with Attacks', [attack, damage], 500, 100, 6, prefix).
mod_group(warstaff, PercentIncreasedPhysicalDamage, '#% increased Physical Damage', [physical, damage], 25, 100, 8, prefix).
mod_group(warstaff, PercentIncreasedPhysicalDamageFlattoAccuracyRating, '#% increased Physical Damage, # to Accuracy Rating', [physical, damage, accuracy], 100, 100, 8, prefix).
mod_group(warstaff, FlattoAccuracyRating, '# to Accuracy Rating', [accuracy], 200, 100, 9, prefix).
mod_group(warstaff, AddsFlattoFlatColdDamage, 'Adds # to # Cold Damage', [cold, damage], 90, 100, 10, prefix).
mod_group(warstaff, AddsFlattoFlatFireDamage, 'Adds # to # Fire Damage', [fire, damage], 80, 100, 10, prefix).
mod_group(warstaff, AddsFlattoFlatLightningDamage, 'Adds # to # Lightning Damage', [lightning, damage], 110, 100, 10, prefix).
mod_group(warstaff, AddsFlattoFlatPhysicalDamage, 'Adds # to # Physical Damage', [physical, damage], 100, 100, 9, prefix).
mod_group(warstaff, PercentIncreasedAttackSpeed, '#% increased Attack Speed', [attack, speed], 100, 100, 8, suffix).
mod_group(warstaff, FlattoAccuracyRatingPercentIncreasedLightRadius, '# to Accuracy Rating, #% increased Light Radius', [accuracy], 1000, 100, 3, suffix).
mod_group(warstaff, PercentIncreasedStunDuration, '#% increased Stun Duration', [], 1000, 100, 6, suffix).
mod_group(warstaff, PercentReducedAttributeRequirements, '#% reduced Attribute Requirements', [attribute], 1000, 100, 5, suffix).
mod_group(warstaff, FlattoDexterity, '# to Dexterity', [attribute], 750, 100, 8, suffix).
mod_group(warstaff, FlattoIntelligence, '# to Intelligence', [attribute], 250, 100, 8, suffix).
mod_group(warstaff, FlattoLevelOfAllMeleeSkills, '# to Level of all Melee Skills', [], 100, 100, 5, suffix).
mod_group(warstaff, PercentToCriticalDamageBonus, '#% to Critical Damage Bonus', [critical, damage], 125, 100, 6, suffix).
mod_group(warstaff, PercentToCriticalHitChance, '#% to Critical Hit Chance', [critical], 125, 100, 6, suffix).
mod_group(warstaff, CausesPercentIncreasedStunBuildup, 'Causes #% increased Stun Buildup', [], 1000, 100, 6, suffix).
mod_group(warstaff, GainFlatLifePerEnemyKilled, 'Gain # Life per Enemy Killed', [life], 750, 100, 8, suffix).
mod_group(warstaff, GainFlatManaPerEnemyKilled, 'Gain # Mana per Enemy Killed', [mana], 750, 100, 8, suffix).
mod_group(warstaff, GrantsFlatLifePerEnemyHit, 'Grants # Life per Enemy Hit', [life], 1000, 100, 4, suffix).
mod_group(warstaff, LeechesPercentOfPhysicalDamageAsLife, 'Leeches #% of Physical Damage as Life', [life, physical, damage], 1000, 100, 5, suffix).
mod_group(warstaff, LeechesPercentOfPhysicalDamageAsMana, 'Leeches #% of Physical Damage as Mana', [mana, physical, damage], 1000, 100, 5, suffix).
