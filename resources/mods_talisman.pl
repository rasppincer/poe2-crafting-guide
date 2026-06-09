%%% Mod data for talisman
%%% Source: POE2-PathOfCrafting (frankthetank001/POE2-PathOfCrafting)
%%% Original data: poe2db.tw via weights.csv
%%% Imported: 2026-06-09

%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)

mod_pool_weight_sum(talisman, prefix, 1215).
mod_pool_weight_sum(talisman, suffix, 9950).

mod_group(talisman, PercentIncreasedElementalDamageWithAttacks, '#% increased Elemental Damage with Attacks', [attack, damage], 500, 100, 6, prefix).
mod_group(talisman, PercentIncreasedPhysicalDamage, '#% increased Physical Damage', [physical, damage], 25, 100, 8, prefix).
mod_group(talisman, PercentIncreasedPhysicalDamageFlattoAccuracyRating, '#% increased Physical Damage, # to Accuracy Rating', [physical, damage, accuracy], 100, 100, 8, prefix).
mod_group(talisman, FlattoAccuracyRating, '# to Accuracy Rating', [accuracy], 200, 100, 9, prefix).
mod_group(talisman, AddsFlattoFlatColdDamage, 'Adds # to # Cold Damage', [cold, damage], 100, 100, 10, prefix).
mod_group(talisman, AddsFlattoFlatFireDamage, 'Adds # to # Fire Damage', [fire, damage], 110, 100, 10, prefix).
mod_group(talisman, AddsFlattoFlatLightningDamage, 'Adds # to # Lightning Damage', [lightning, damage], 80, 100, 10, prefix).
mod_group(talisman, AddsFlattoFlatPhysicalDamage, 'Adds # to # Physical Damage', [physical, damage], 100, 100, 9, prefix).
mod_group(talisman, PercentIncreasedAttackSpeed, '#% increased Attack Speed', [attack, speed], 100, 100, 8, suffix).
mod_group(talisman, FlattoAccuracyRatingPercentIncreasedLightRadius, '# to Accuracy Rating, #% increased Light Radius', [accuracy], 1000, 100, 3, suffix).
mod_group(talisman, PercentIncreasedStunDuration, '#% increased Stun Duration', [], 1000, 100, 6, suffix).
mod_group(talisman, PercentReducedAttributeRequirements, '#% reduced Attribute Requirements', [attribute], 1000, 100, 5, suffix).
mod_group(talisman, FlattoLevelOfAllMeleeSkills, '# to Level of all Melee Skills', [], 100, 100, 5, suffix).
mod_group(talisman, FlattoStrength, '# to Strength', [attribute], 600, 100, 8, suffix).
mod_group(talisman, FlattoIntelligence, '# to Intelligence', [attribute], 400, 100, 8, suffix).
mod_group(talisman, PercentToCriticalDamageBonus, '#% to Critical Damage Bonus', [critical, damage], 125, 100, 6, suffix).
mod_group(talisman, PercentToCriticalHitChance, '#% to Critical Hit Chance', [critical], 125, 100, 6, suffix).
mod_group(talisman, CausesPercentIncreasedStunBuildup, 'Causes #% increased Stun Buildup', [], 1000, 100, 6, suffix).
mod_group(talisman, GainFlatLifePerEnemyKilled, 'Gain # Life per Enemy Killed', [life], 750, 100, 8, suffix).
mod_group(talisman, GainFlatManaPerEnemyKilled, 'Gain # Mana per Enemy Killed', [mana], 750, 100, 8, suffix).
mod_group(talisman, GrantsFlatLifePerEnemyHit, 'Grants # Life per Enemy Hit', [life], 1000, 100, 4, suffix).
mod_group(talisman, LeechesPercentOfPhysicalDamageAsLife, 'Leeches #% of Physical Damage as Life', [life, physical, damage], 1000, 100, 5, suffix).
mod_group(talisman, LeechesPercentOfPhysicalDamageAsMana, 'Leeches #% of Physical Damage as Mana', [mana, physical, damage], 1000, 100, 5, suffix).
