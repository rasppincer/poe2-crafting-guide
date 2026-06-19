%%% Mod data for helmet_str
%%% Source: POE2-PathOfCrafting (frankthetank001/POE2-PathOfCrafting)
%%% Original data: poe2db.tw via weights.csv
%%% Auto-imported by import_from_pathofcrafting.py

%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)

mod_pool_weight_sum(helmet_str, prefix, 7800).
mod_pool_weight_sum(helmet_str, suffix, 11550).

mod_group(helmet_str, 'PercentIncreasedArmour', '#% increased Armour', [armour], 1000, 100, 7, prefix).
mod_group(helmet_str, 'PercentIncreasedArmourFlattoMaximumLife', '#% increased Armour, # to maximum Life', [life, armour], 1000, 100, 6, prefix).
mod_group(helmet_str, 'PercentIncreasedArmourFlattoMaximumMana', '#% increased Armour, # to maximum Mana', [mana, armour], 1000, 100, 6, prefix).
mod_group(helmet_str, 'PercentIncreasedRarityOfItemsFound', '#% increased Rarity of Items found', [rarity], 1000, 100, 3, prefix).
mod_group(helmet_str, 'FlattoAccuracyRating', '# to Accuracy Rating', [accuracy], 800, 100, 9, prefix).
mod_group(helmet_str, 'FlattoArmour', '# to Armour', [armour], 1000, 100, 8, prefix).
mod_group(helmet_str, 'FlattoMaximumLife', '# to maximum Life', [life], 1000, 100, 10, prefix).
mod_group(helmet_str, 'FlattoMaximumMana', '# to maximum Mana', [mana], 1000, 100, 10, prefix).

mod_group(helmet_str, 'FlatLifeRegenerationPerSecond', '# Life Regeneration per second', [life, regeneration], 1000, 100, 8, suffix).
mod_group(helmet_str, 'PercentIncreasedCriticalHitChance', '#% increased Critical Hit Chance', [critical], 1000, 100, 5, suffix).
mod_group(helmet_str, 'FlattoAccuracyRatingPercentIncreasedLightRadius', '# to Accuracy Rating, #% increased Light Radius', [accuracy], 1000, 100, 3, suffix).
mod_group(helmet_str, 'PercentIncreasedRarityOfItemsFound', '#% increased Rarity of Items found', [rarity], 1000, 100, 3, suffix).
mod_group(helmet_str, 'PercentReducedAttributeRequirements', '#% reduced Attribute Requirements', [], 800, 100, 5, suffix).
mod_group(helmet_str, 'FlattoIntelligence', '# to Intelligence', [attribute], 1000, 100, 9, suffix).
mod_group(helmet_str, 'FlattoLevelOfAllMinionSkills', '# to Level of all Minion Skills', [], 500, 100, 2, suffix).
mod_group(helmet_str, 'FlattoStrength', '# to Strength', [attribute], 1000, 100, 8, suffix).
mod_group(helmet_str, 'PercentToChaosResistance', '#% to Chaos Resistance', [chaos, resistance], 250, 100, 6, suffix).
mod_group(helmet_str, 'PercentToColdResistance', '#% to Cold Resistance', [cold, resistance], 1000, 100, 8, suffix).
mod_group(helmet_str, 'PercentToFireResistance', '#% to Fire Resistance', [fire, resistance], 1000, 100, 8, suffix).
mod_group(helmet_str, 'PercentToLightningResistance', '#% to Lightning Resistance', [lightning, resistance], 1000, 100, 8, suffix).
mod_group(helmet_str, 'PercentOfArmourAlsoAppliesToElementalDamage', '#% of Armour also applies to Elemental Damage', [armour, damage], 1000, 100, 5, suffix).

