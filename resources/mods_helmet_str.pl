%%% Mod data for helmet_str
%%% Source: https://poe2db.tw/us/Helmets_str
%%% Extracted: 2026-06-09

%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)

mod_pool_weight_sum(helmet_str, prefix, 56200).
mod_pool_weight_sum(helmet_str, suffix, 70000).

mod_group(helmet_str, 1IncreasedLife, '# to maximum Life', [life], 10000, 65, 10, prefix).
mod_group(helmet_str, 1IncreasedMana, '# to maximum Mana', [mana], 10000, 65, 10, prefix).
mod_group(helmet_str, 1BaseLocalDefences, '# to Armour', [armour], 8000, 60, 8, prefix).
mod_group(helmet_str, 1DefencesPercent, '#% increased Armour', [armour], 7000, 65, 7, prefix).
mod_group(helmet_str, 1BaseLocalDefencesAndLife, '#% increased Armour, # to maximum Life', [life, armour], 6000, 78, 6, prefix).
mod_group(helmet_str, 1BaseLocalDefencesAndMana, '#% increased Armour, # to maximum Mana', [mana, armour], 6000, 78, 6, prefix).
mod_group(helmet_str, 1IncreasedAccuracy, '# to Accuracy Rating', [attack], 6200, 76, 9, prefix).
mod_group(helmet_str, 1ItemFoundRarityIncreasePrefix, '#% increased Rarity of Items found', [], 3000, 47, 3, prefix).

mod_group(helmet_str, 2Strength, '# to Strength', [attribute], 8000, 74, 8, suffix).
mod_group(helmet_str, 2Intelligence, '# to Intelligence', [attribute], 9000, 81, 9, suffix).
mod_group(helmet_str, 2FireResistance, '#% to Fire Resistance', [elemental, fire, resistance], 8000, 82, 8, suffix).
mod_group(helmet_str, 2ColdResistance, '#% to Cold Resistance', [elemental, cold, resistance], 8000, 82, 8, suffix).
mod_group(helmet_str, 2LightningResistance, '#% to Lightning Resistance', [elemental, lightning, resistance], 8000, 82, 8, suffix).
mod_group(helmet_str, 2ChaosResistance, '#% to Chaos Resistance', [chaos, resistance], 1500, 81, 6, suffix).
mod_group(helmet_str, 2LocalAttributeRequirements, '#% reduced Attribute Requirements', [], 4000, 60, 5, suffix).
mod_group(helmet_str, 2IncreaseSocketedGemLevel, '# to Level of all Minion Skills', [minion, gem], 750, 41, 2, suffix).
mod_group(helmet_str, 2LifeRegeneration, '# Life Regeneration per second', [life], 8000, 58, 8, suffix).
mod_group(helmet_str, 2CriticalStrikeChanceIncrease, '#% increased Critical Hit Chance', [critical], 3750, 58, 5, suffix).
mod_group(helmet_str, 2ItemFoundRarityIncrease, '#% increased Rarity of Items found', [], 3000, 40, 3, suffix).
mod_group(helmet_str, 2LightRadiusAndAccuracy, '# to Accuracy Rating, #% increased Light Radius', [attack], 3000, 30, 3, suffix).
mod_group(helmet_str, 2ArmourAppliesToElementalDamage, '#% of Armour also applies to Elemental Damage', [armour, elemental], 5000, 66, 5, suffix).
