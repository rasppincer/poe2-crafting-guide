%%% Mod data for helmet_str_int
%%% Source: POE2-PathOfCrafting (frankthetank001/POE2-PathOfCrafting)
%%% Original data: poe2db.tw via weights.csv
%%% Auto-imported by import_from_pathofcrafting.py

%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)

mod_pool_weight_sum(helmet_str_int, prefix, 7800).
mod_pool_weight_sum(helmet_str_int, suffix, 11050).

mod_group(helmet_str_int, 'PercentIncreasedArmourAndEnergyShield', '#% increased Armour and Energy Shield', [energy_shield, armour], 1000, 100, 7, prefix).
mod_group(helmet_str_int, 'PercentIncreasedArmourAndEnergyShieldFlattoMaximumLife', '#% increased Armour and Energy Shield, # to maximum Life', [life, energy_shield, armour], 1000, 100, 6, prefix).
mod_group(helmet_str_int, 'PercentIncreasedArmourAndEnergyShieldFlattoMaximumMana', '#% increased Armour and Energy Shield, # to maximum Mana', [mana, energy_shield, armour], 1000, 100, 6, prefix).
mod_group(helmet_str_int, 'PercentIncreasedRarityOfItemsFound', '#% increased Rarity of Items found', [rarity], 1000, 100, 3, prefix).
mod_group(helmet_str_int, 'FlattoAccuracyRating', '# to Accuracy Rating', [accuracy], 800, 100, 9, prefix).
mod_group(helmet_str_int, 'FlattoArmourFlattoMaximumEnergyShield', '# to Armour, # to maximum Energy Shield', [energy_shield, armour], 1000, 100, 5, prefix).
mod_group(helmet_str_int, 'FlattoMaximumLife', '# to maximum Life', [life], 1000, 100, 10, prefix).
mod_group(helmet_str_int, 'FlattoMaximumMana', '# to maximum Mana', [mana], 1000, 100, 10, prefix).

mod_group(helmet_str_int, 'FlatLifeRegenerationPerSecond', '# Life Regeneration per second', [life, regeneration], 1000, 100, 8, suffix).
mod_group(helmet_str_int, 'PercentIncreasedCriticalHitChance', '#% increased Critical Hit Chance', [critical], 1000, 100, 5, suffix).
mod_group(helmet_str_int, 'FlattoAccuracyRatingPercentIncreasedLightRadius', '# to Accuracy Rating, #% increased Light Radius', [accuracy], 1000, 100, 3, suffix).
mod_group(helmet_str_int, 'PercentIncreasedRarityOfItemsFound', '#% increased Rarity of Items found', [rarity], 1000, 100, 3, suffix).
mod_group(helmet_str_int, 'PercentReducedAttributeRequirements', '#% reduced Attribute Requirements', [], 800, 100, 5, suffix).
mod_group(helmet_str_int, 'FlattoIntelligence', '# to Intelligence', [attribute], 1000, 100, 9, suffix).
mod_group(helmet_str_int, 'FlattoLevelOfAllMinionSkills', '# to Level of all Minion Skills', [], 500, 100, 2, suffix).
mod_group(helmet_str_int, 'FlattoStrength', '# to Strength', [attribute], 500, 100, 8, suffix).
mod_group(helmet_str_int, 'PercentToChaosResistance', '#% to Chaos Resistance', [chaos, resistance], 250, 100, 6, suffix).
mod_group(helmet_str_int, 'PercentToColdResistance', '#% to Cold Resistance', [cold, resistance], 1000, 100, 8, suffix).
mod_group(helmet_str_int, 'PercentToFireResistance', '#% to Fire Resistance', [fire, resistance], 1000, 100, 8, suffix).
mod_group(helmet_str_int, 'PercentToLightningResistance', '#% to Lightning Resistance', [lightning, resistance], 1000, 100, 8, suffix).
mod_group(helmet_str_int, 'PercentIncreasedEnergyShieldRechargeRate', '#% increased Energy Shield Recharge Rate', [energy_shield], 500, 100, 4, suffix).
mod_group(helmet_str_int, 'PercentOfArmourAlsoAppliesToElementalDamage', '#% of Armour also applies to Elemental Damage', [armour, damage], 500, 100, 5, suffix).

