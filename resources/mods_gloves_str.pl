%%% Mod data for gloves_str
%%% Source: https://poe2db.tw/us/Gloves_str
%%% Extracted: 2026-06-09

%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)

mod_pool_weight_sum(gloves_str, prefix, 63700).
mod_pool_weight_sum(gloves_str, suffix, 84500).

mod_group(gloves_str, 1IncreasedLife, '# to maximum Life', [life], 9000, 60, 9, prefix).
mod_group(gloves_str, 1IncreasedMana, '# to maximum Mana', [mana], 9000, 60, 9, prefix).
mod_group(gloves_str, 1BaseLocalDefences, '# to Armour', [armour], 7000, 54, 7, prefix).
mod_group(gloves_str, 1DefencesPercent, '#% increased Armour', [armour], 7000, 65, 7, prefix).
mod_group(gloves_str, 1BaseLocalDefencesAndLife, '#% increased Armour, # to maximum Life', [life, armour], 6000, 78, 6, prefix).
mod_group(gloves_str, 1PhysicalDamage, 'Adds # to # Physical Damage to Attacks', [damage, physical, attack], 7800, 75, 9, prefix).
mod_group(gloves_str, 1FireDamage, 'Adds # to # Fire damage to Attacks', [damage, elemental, fire, attack], 3900, 75, 9, prefix).
mod_group(gloves_str, 1ColdDamage, 'Adds # to # Cold damage to Attacks', [damage, elemental, cold, attack], 3900, 75, 9, prefix).
mod_group(gloves_str, 1LightningDamage, 'Adds # to # Lightning damage to Attacks', [damage, elemental, lightning, attack], 3900, 75, 9, prefix).
mod_group(gloves_str, 1IncreasedAccuracy, '# to Accuracy Rating', [attack], 6200, 76, 9, prefix).

mod_group(gloves_str, 2Strength, '# to Strength', [attribute], 8000, 74, 8, suffix).
mod_group(gloves_str, 2Dexterity, '# to Dexterity', [attribute], 9000, 81, 9, suffix).
mod_group(gloves_str, 2FireResistance, '#% to Fire Resistance', [elemental, fire, resistance], 8000, 82, 8, suffix).
mod_group(gloves_str, 2ColdResistance, '#% to Cold Resistance', [elemental, cold, resistance], 8000, 82, 8, suffix).
mod_group(gloves_str, 2LightningResistance, '#% to Lightning Resistance', [elemental, lightning, resistance], 8000, 82, 8, suffix).
mod_group(gloves_str, 2ChaosResistance, '#% to Chaos Resistance', [chaos, resistance], 1500, 81, 6, suffix).
mod_group(gloves_str, 2LocalAttributeRequirements, '#% reduced Attribute Requirements', [], 3500, 60, 5, suffix).
mod_group(gloves_str, 2IncreaseSocketedGemLevel, '# to Level of all Melee Skills', [attack], 750, 41, 2, suffix).
mod_group(gloves_str, 2LifeLeech, 'Leech #% of Physical Attack Damage as Life', [life, physical, attack], 4000, 65, 4, suffix).
mod_group(gloves_str, 2ManaLeech, 'Leech #% of Physical Attack Damage as Mana', [mana, physical, attack], 4000, 65, 4, suffix).
mod_group(gloves_str, 2LifeGainedFromEnemyDeath, 'Gain # Life per enemy killed', [life], 6000, 77, 8, suffix).
mod_group(gloves_str, 2ManaGainedFromEnemyDeath, 'Gain # Mana per enemy killed', [mana], 6000, 78, 8, suffix).
mod_group(gloves_str, 2LifeGainPerTarget, 'Gain # Life per Enemy Hit with Attacks', [life, attack], 4000, 40, 4, suffix).
mod_group(gloves_str, 2IncreasedAttackSpeed, '#% increased Attack Speed', [attack, speed], 2000, 60, 4, suffix).
mod_group(gloves_str, 2CriticalStrikeMultiplier, '#% increased Critical Damage Bonus', [damage, critical], 3750, 59, 5, suffix).
mod_group(gloves_str, 2ItemFoundRarityIncrease, '#% increased Rarity of Items found', [], 3000, 40, 3, suffix).
mod_group(gloves_str, 2ArmourAppliesToElementalDamage, '#% of Armour also applies to Elemental Damage', [armour, elemental], 5000, 66, 5, suffix).
