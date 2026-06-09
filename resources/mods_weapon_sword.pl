%%% Mod data for weapon_sword
%%% Source: https://poe2db.tw/us/One_Hand_Swords
%%% Extracted: 2026-06-09

%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)

mod_pool_weight_sum(weapon_sword, prefix, 70).
mod_pool_weight_sum(weapon_sword, suffix, 88).

mod_group(weapon_sword, 1PhysicalDamage, 'Adds # to # Physical Damage', [damage, physical, attack], 9, 75, 9, prefix).
mod_group(weapon_sword, 1FireDamage, 'Adds # to # Fire Damage', [damage, elemental, fire, attack], 10, 81, 10, prefix).
mod_group(weapon_sword, 1ColdDamage, 'Adds # to # Cold Damage', [damage, elemental, cold, attack], 10, 81, 10, prefix).
mod_group(weapon_sword, 1LightningDamage, 'Adds # to # Lightning Damage', [damage, elemental, lightning, attack], 10, 81, 10, prefix).
mod_group(weapon_sword, 1LocalPhysicalDamagePercent, '#% increased Physical Damage', [damage, physical, attack], 8, 82, 8, prefix).
mod_group(weapon_sword, 1LocalIncreasedPhysicalDamagePercentAndAccuracyRating, '#% increased Physical Damage# to Accuracy Rating', [damage, physical, attack], 8, 81, 8, prefix).
mod_group(weapon_sword, 1IncreasedAccuracy, '# to Accuracy Rating', [attack], 9, 76, 9, prefix).
mod_group(weapon_sword, 1IncreasedWeaponElementalDamagePercent, '#% increased Elemental Damage with Attacks', [damage, elemental, fire, cold, lightning], 6, 81, 6, prefix).

mod_group(weapon_sword, 2Strength, '# to Strength', [attribute], 8, 74, 8, suffix).
mod_group(weapon_sword, 2Dexterity, '# to Dexterity', [attribute], 8, 74, 8, suffix).
mod_group(weapon_sword, 2LocalAttributeRequirements, '#% reduced Attribute Requirements', [], 5, 60, 5, suffix).
mod_group(weapon_sword, 2IncreaseSocketedGemLevel, '# to Level of all Melee Skills', [attack], 4, 81, 4, suffix).
mod_group(weapon_sword, 2LifeLeech, 'Leeches #% of Physical Damage as Life', [life, physical, attack], 4, 65, 4, suffix).
mod_group(weapon_sword, 2ManaLeech, 'Leeches #% of Physical Damage as Mana', [mana, physical, attack], 4, 65, 4, suffix).
mod_group(weapon_sword, 2LifeGainedFromEnemyDeath, 'Gain # Life per enemy killed', [life], 8, 77, 8, suffix).
mod_group(weapon_sword, 2ManaGainedFromEnemyDeath, 'Gain # Mana per enemy killed', [mana], 8, 78, 8, suffix).
mod_group(weapon_sword, 2LifeGainPerTarget, 'Grants # Life per Enemy Hit', [life, attack], 4, 40, 4, suffix).
mod_group(weapon_sword, 2IncreasedAttackSpeed, '#% increased Attack Speed', [attack, speed], 8, 77, 8, suffix).
mod_group(weapon_sword, 2CriticalStrikeChanceIncrease, '#% to Critical Hit Chance', [attack, critical], 6, 73, 6, suffix).
mod_group(weapon_sword, 2CriticalStrikeMultiplier, '#% to Critical Damage Bonus', [damage, attack, critical], 6, 73, 6, suffix).
mod_group(weapon_sword, 2LightRadiusAndAccuracy, '# to Accuracy Rating#% increased Light Radius', [attack], 3, 30, 3, suffix).
mod_group(weapon_sword, 2StunDurationIncreasePercent, '#% increased Stun Duration', [], 6, 71, 6, suffix).
mod_group(weapon_sword, 2StunDamageIncrease, 'Causes #% increased Stun Buildup', [], 6, 74, 6, suffix).
