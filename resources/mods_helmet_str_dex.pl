%%% Mod data for helmet_str_dex
%%% Source: POE2-PathOfCrafting (frankthetank001/POE2-PathOfCrafting)
%%% Original data: poe2db.tw via weights.csv
%%% Imported: 2026-06-09

%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)

mod_pool_weight_sum(helmet_str_dex, prefix, 7200).
mod_pool_weight_sum(helmet_str_dex, suffix, 10550).

mod_group(helmet_str_dex, PercentIncreasedArmourAndEvasion, '#% increased Armour and Evasion', [armour, evasion], 1000, 100, 7, prefix).
mod_group(helmet_str_dex, PercentIncreasedArmourAndEvasionFlattoMaximumLife, '#% increased Armour and Evasion, # to maximum Life', [life, armour, evasion], 1000, 100, 6, prefix).
mod_group(helmet_str_dex, PercentIncreasedArmourAndEvasionFlattoMaximumMana, '#% increased Armour and Evasion, # to maximum Mana', [mana, armour, evasion], 1000, 100, 6, prefix).
mod_group(helmet_str_dex, PercentIncreasedRarityOfItemsFound, '#% increased Rarity of Items found', [], 1000, 100, 3, prefix).
mod_group(helmet_str_dex, FlattoAccuracyRating, '# to Accuracy Rating', [accuracy], 200, 100, 9, prefix).
mod_group(helmet_str_dex, FlattoArmourFlattoEvasionRating, '# to Armour, # to Evasion Rating', [armour, evasion], 1000, 100, 5, prefix).
mod_group(helmet_str_dex, FlattoMaximumLife, '# to maximum Life', [life], 1000, 100, 10, prefix).
mod_group(helmet_str_dex, FlattoMaximumMana, '# to maximum Mana', [mana], 1000, 100, 10, prefix).
mod_group(helmet_str_dex, FlatLifeRegenerationPerSecond, '# Life Regeneration per second', [life], 1000, 100, 8, suffix).
mod_group(helmet_str_dex, PercentIncreasedCriticalHitChance, '#% increased Critical Hit Chance', [critical], 250, 100, 5, suffix).
mod_group(helmet_str_dex, FlattoAccuracyRatingPercentIncreasedLightRadius, '# to Accuracy Rating, #% increased Light Radius', [accuracy], 1000, 100, 3, suffix).
mod_group(helmet_str_dex, PercentIncreasedRarityOfItemsFound, '#% increased Rarity of Items found', [], 1000, 100, 3, suffix).
mod_group(helmet_str_dex, PercentReducedAttributeRequirements, '#% reduced Attribute Requirements', [attribute], 800, 100, 5, suffix).
mod_group(helmet_str_dex, FlattoDexterity, '# to Dexterity', [attribute], 500, 100, 8, suffix).
mod_group(helmet_str_dex, FlattoIntelligence, '# to Intelligence', [attribute], 1000, 100, 9, suffix).
mod_group(helmet_str_dex, FlattoLevelOfAllMinionSkills, '# to Level of all Minion Skills', [], 250, 100, 2, suffix).
mod_group(helmet_str_dex, FlattoStrength, '# to Strength', [attribute], 500, 100, 8, suffix).
mod_group(helmet_str_dex, PercentToChaosResistance, '#% to Chaos Resistance', [chaos, resistance], 250, 100, 6, suffix).
mod_group(helmet_str_dex, PercentToColdResistance, '#% to Cold Resistance', [cold, resistance], 1000, 100, 8, suffix).
mod_group(helmet_str_dex, PercentToFireResistance, '#% to Fire Resistance', [fire, resistance], 1000, 100, 8, suffix).
mod_group(helmet_str_dex, PercentToLightningResistance, '#% to Lightning Resistance', [lightning, resistance], 1000, 100, 8, suffix).
mod_group(helmet_str_dex, PercentOfArmourAlsoAppliesToElementalDamage, '#% of Armour also applies to Elemental Damage', [armour, damage], 500, 100, 5, suffix).
mod_group(helmet_str_dex, GainDeflectionRatingEqualToPercentOfEvasionRating, 'Gain Deflection Rating equal to #% of Evasion Rating', [evasion], 500, 100, 5, suffix).
