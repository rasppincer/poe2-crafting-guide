%%% Mod data for helmet_dex_int
%%% Source: POE2-PathOfCrafting (frankthetank001/POE2-PathOfCrafting)
%%% Original data: poe2db.tw via weights.csv
%%% Imported: 2026-06-09

%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)

mod_pool_weight_sum(helmet_dex_int, prefix, 7200).
mod_pool_weight_sum(helmet_dex_int, suffix, 10050).

mod_group(helmet_dex_int, PercentIncreasedEvasionAndEnergyShield, '#% increased Evasion and Energy Shield', [evasion, energy_shield], 1000, 100, 7, prefix).
mod_group(helmet_dex_int, PercentIncreasedEvasionAndEnergyShieldFlattoMaximumLife, '#% increased Evasion and Energy Shield, # to maximum Life', [life, evasion, energy_shield], 1000, 100, 6, prefix).
mod_group(helmet_dex_int, PercentIncreasedEvasionAndEnergyShieldFlattoMaximumMana, '#% increased Evasion and Energy Shield, # to maximum Mana', [mana, evasion, energy_shield], 1000, 100, 6, prefix).
mod_group(helmet_dex_int, PercentIncreasedRarityOfItemsFound, '#% increased Rarity of Items found', [], 1000, 100, 3, prefix).
mod_group(helmet_dex_int, FlattoAccuracyRating, '# to Accuracy Rating', [accuracy], 200, 100, 9, prefix).
mod_group(helmet_dex_int, FlattoEvasionRatingFlattoMaximumEnergyShield, '# to Evasion Rating, # to maximum Energy Shield', [evasion, energy_shield], 1000, 100, 5, prefix).
mod_group(helmet_dex_int, FlattoMaximumLife, '# to maximum Life', [life], 1000, 100, 10, prefix).
mod_group(helmet_dex_int, FlattoMaximumMana, '# to maximum Mana', [mana], 1000, 100, 10, prefix).
mod_group(helmet_dex_int, FlatLifeRegenerationPerSecond, '# Life Regeneration per second', [life], 1000, 100, 8, suffix).
mod_group(helmet_dex_int, PercentIncreasedCriticalHitChance, '#% increased Critical Hit Chance', [critical], 250, 100, 5, suffix).
mod_group(helmet_dex_int, FlattoAccuracyRatingPercentIncreasedLightRadius, '# to Accuracy Rating, #% increased Light Radius', [accuracy], 1000, 100, 3, suffix).
mod_group(helmet_dex_int, PercentIncreasedRarityOfItemsFound, '#% increased Rarity of Items found', [], 1000, 100, 3, suffix).
mod_group(helmet_dex_int, PercentReducedAttributeRequirements, '#% reduced Attribute Requirements', [attribute], 800, 100, 5, suffix).
mod_group(helmet_dex_int, FlattoDexterity, '# to Dexterity', [attribute], 500, 100, 8, suffix).
mod_group(helmet_dex_int, FlattoIntelligence, '# to Intelligence', [attribute], 1000, 100, 9, suffix).
mod_group(helmet_dex_int, FlattoLevelOfAllMinionSkills, '# to Level of all Minion Skills', [], 250, 100, 2, suffix).
mod_group(helmet_dex_int, PercentToChaosResistance, '#% to Chaos Resistance', [chaos, resistance], 250, 100, 6, suffix).
mod_group(helmet_dex_int, PercentToColdResistance, '#% to Cold Resistance', [cold, resistance], 1000, 100, 8, suffix).
mod_group(helmet_dex_int, PercentToFireResistance, '#% to Fire Resistance', [fire, resistance], 1000, 100, 8, suffix).
mod_group(helmet_dex_int, PercentToLightningResistance, '#% to Lightning Resistance', [lightning, resistance], 1000, 100, 8, suffix).
mod_group(helmet_dex_int, PercentIncreasedEnergyShieldRechargeRate, '#% increased Energy Shield Recharge Rate', [energy_shield], 500, 100, 4, suffix).
mod_group(helmet_dex_int, GainDeflectionRatingEqualToPercentOfEvasionRating, 'Gain Deflection Rating equal to #% of Evasion Rating', [evasion], 500, 100, 5, suffix).
