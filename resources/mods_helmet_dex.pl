%%% Mod data for helmet_dex
%%% Source: POE2-PathOfCrafting (frankthetank001/POE2-PathOfCrafting)
%%% Original data: poe2db.tw via weights.csv
%%% Auto-imported by import_from_pathofcrafting.py

%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)

mod_pool_weight_sum(helmet_dex, prefix, 7800).
mod_pool_weight_sum(helmet_dex, suffix, 11550).

mod_group(helmet_dex, 'PercentIncreasedEvasionRating', '#% increased Evasion Rating', [evasion], 1000, 100, 7, prefix).
mod_group(helmet_dex, 'PercentIncreasedEvasionRatingFlattoMaximumLife', '#% increased Evasion Rating, # to maximum Life', [life, evasion], 1000, 100, 6, prefix).
mod_group(helmet_dex, 'PercentIncreasedEvasionRatingFlattoMaximumMana', '#% increased Evasion Rating, # to maximum Mana', [mana, evasion], 1000, 100, 6, prefix).
mod_group(helmet_dex, 'PercentIncreasedRarityOfItemsFound', '#% increased Rarity of Items found', [rarity], 1000, 100, 3, prefix).
mod_group(helmet_dex, 'FlattoAccuracyRating', '# to Accuracy Rating', [accuracy], 800, 100, 9, prefix).
mod_group(helmet_dex, 'FlattoEvasionRating', '# to Evasion Rating', [evasion], 1000, 100, 8, prefix).
mod_group(helmet_dex, 'FlattoMaximumLife', '# to maximum Life', [life], 1000, 100, 10, prefix).
mod_group(helmet_dex, 'FlattoMaximumMana', '# to maximum Mana', [mana], 1000, 100, 10, prefix).

mod_group(helmet_dex, 'FlatLifeRegenerationPerSecond', '# Life Regeneration per second', [life, regeneration], 1000, 100, 8, suffix).
mod_group(helmet_dex, 'PercentIncreasedCriticalHitChance', '#% increased Critical Hit Chance', [critical], 1000, 100, 5, suffix).
mod_group(helmet_dex, 'FlattoAccuracyRatingPercentIncreasedLightRadius', '# to Accuracy Rating, #% increased Light Radius', [accuracy], 1000, 100, 3, suffix).
mod_group(helmet_dex, 'PercentIncreasedRarityOfItemsFound', '#% increased Rarity of Items found', [rarity], 1000, 100, 3, suffix).
mod_group(helmet_dex, 'PercentReducedAttributeRequirements', '#% reduced Attribute Requirements', [], 800, 100, 5, suffix).
mod_group(helmet_dex, 'FlattoDexterity', '# to Dexterity', [attribute], 1000, 100, 8, suffix).
mod_group(helmet_dex, 'FlattoIntelligence', '# to Intelligence', [attribute], 1000, 100, 9, suffix).
mod_group(helmet_dex, 'FlattoLevelOfAllMinionSkills', '# to Level of all Minion Skills', [], 500, 100, 2, suffix).
mod_group(helmet_dex, 'PercentToChaosResistance', '#% to Chaos Resistance', [chaos, resistance], 250, 100, 6, suffix).
mod_group(helmet_dex, 'PercentToColdResistance', '#% to Cold Resistance', [cold, resistance], 1000, 100, 8, suffix).
mod_group(helmet_dex, 'PercentToFireResistance', '#% to Fire Resistance', [fire, resistance], 1000, 100, 8, suffix).
mod_group(helmet_dex, 'PercentToLightningResistance', '#% to Lightning Resistance', [lightning, resistance], 1000, 100, 8, suffix).
mod_group(helmet_dex, 'GainDeflectionRatingEqualToPercentOfEvasionRating', 'Gain Deflection Rating equal to #% of Evasion Rating', [evasion], 1000, 100, 5, suffix).

