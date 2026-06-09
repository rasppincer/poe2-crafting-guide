%%% Mod data for helmet_int
%%% Source: POE2-PathOfCrafting (frankthetank001/POE2-PathOfCrafting)
%%% Original data: poe2db.tw via weights.csv
%%% Imported: 2026-06-09

%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)

mod_pool_weight_sum(helmet_int, prefix, 7200).
mod_pool_weight_sum(helmet_int, suffix, 9550).

mod_group(helmet_int, PercentIncreasedEnergyShield, '#% increased Energy Shield', [energy_shield], 1000, 100, 7, prefix).
mod_group(helmet_int, PercentIncreasedEnergyShieldFlattoMaximumLife, '#% increased Energy Shield, # to maximum Life', [life, energy_shield], 1000, 100, 6, prefix).
mod_group(helmet_int, PercentIncreasedEnergyShieldFlattoMaximumMana, '#% increased Energy Shield, # to maximum Mana', [mana, energy_shield], 1000, 100, 6, prefix).
mod_group(helmet_int, PercentIncreasedRarityOfItemsFound, '#% increased Rarity of Items found', [], 1000, 100, 3, prefix).
mod_group(helmet_int, FlattoAccuracyRating, '# to Accuracy Rating', [accuracy], 200, 100, 9, prefix).
mod_group(helmet_int, FlattoMaximumEnergyShield, '# to maximum Energy Shield', [energy_shield], 1000, 100, 8, prefix).
mod_group(helmet_int, FlattoMaximumLife, '# to maximum Life', [life], 1000, 100, 10, prefix).
mod_group(helmet_int, FlattoMaximumMana, '# to maximum Mana', [mana], 1000, 100, 10, prefix).
mod_group(helmet_int, FlatLifeRegenerationPerSecond, '# Life Regeneration per second', [life], 1000, 100, 8, suffix).
mod_group(helmet_int, PercentIncreasedCriticalHitChance, '#% increased Critical Hit Chance', [critical], 250, 100, 5, suffix).
mod_group(helmet_int, FlattoAccuracyRatingPercentIncreasedLightRadius, '# to Accuracy Rating, #% increased Light Radius', [accuracy], 1000, 100, 3, suffix).
mod_group(helmet_int, PercentIncreasedRarityOfItemsFound, '#% increased Rarity of Items found', [], 1000, 100, 3, suffix).
mod_group(helmet_int, PercentReducedAttributeRequirements, '#% reduced Attribute Requirements', [attribute], 800, 100, 5, suffix).
mod_group(helmet_int, FlattoIntelligence, '# to Intelligence', [attribute], 1000, 100, 9, suffix).
mod_group(helmet_int, FlattoLevelOfAllMinionSkills, '# to Level of all Minion Skills', [], 250, 100, 2, suffix).
mod_group(helmet_int, PercentToChaosResistance, '#% to Chaos Resistance', [chaos, resistance], 250, 100, 6, suffix).
mod_group(helmet_int, PercentToColdResistance, '#% to Cold Resistance', [cold, resistance], 1000, 100, 8, suffix).
mod_group(helmet_int, PercentToFireResistance, '#% to Fire Resistance', [fire, resistance], 1000, 100, 8, suffix).
mod_group(helmet_int, PercentToLightningResistance, '#% to Lightning Resistance', [lightning, resistance], 1000, 100, 8, suffix).
mod_group(helmet_int, PercentIncreasedEnergyShieldRechargeRate, '#% increased Energy Shield Recharge Rate', [energy_shield], 1000, 100, 4, suffix).
