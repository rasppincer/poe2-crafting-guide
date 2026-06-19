%%% Mod data for boots_str_dex
%%% Source: POE2-PathOfCrafting (frankthetank001/POE2-PathOfCrafting)
%%% Original data: poe2db.tw via weights.csv
%%% Auto-imported by import_from_pathofcrafting.py

%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)

mod_pool_weight_sum(boots_str_dex, prefix, 6000).
mod_pool_weight_sum(boots_str_dex, suffix, 10300).

mod_group(boots_str_dex, 'PercentIncreasedArmourAndEvasion', '#% increased Armour and Evasion', [armour, evasion], 1000, 100, 7, prefix).
mod_group(boots_str_dex, 'PercentIncreasedArmourAndEvasionFlattoStunThreshold', '#% increased Armour and Evasion, # to Stun Threshold', [armour, evasion, stun], 1000, 100, 6, prefix).
mod_group(boots_str_dex, 'PercentIncreasedMovementSpeed', '#% increased Movement Speed', [speed], 1000, 100, 6, prefix).
mod_group(boots_str_dex, 'FlattoArmourFlattoEvasionRating', '# to Armour, # to Evasion Rating', [armour, evasion], 1000, 100, 4, prefix).
mod_group(boots_str_dex, 'FlattoMaximumLife', '# to maximum Life', [life], 1000, 100, 9, prefix).
mod_group(boots_str_dex, 'FlattoMaximumMana', '# to maximum Mana', [mana], 1000, 100, 9, prefix).

mod_group(boots_str_dex, 'FlatLifeRegenerationPerSecond', '# Life Regeneration per second', [life, regeneration], 1000, 100, 8, suffix).
mod_group(boots_str_dex, 'PercentIncreasedRarityOfItemsFound', '#% increased Rarity of Items found', [rarity], 1000, 100, 3, suffix).
mod_group(boots_str_dex, 'PercentReducedAttributeRequirements', '#% reduced Attribute Requirements', [], 750, 100, 5, suffix).
mod_group(boots_str_dex, 'PercentReducedChillDurationOnYou', '#% reduced Chill Duration on you', [cold], 500, 100, 5, suffix).
mod_group(boots_str_dex, 'PercentReducedFreezeDurationOnYou', '#% reduced Freeze Duration on you', [cold], 500, 100, 5, suffix).
mod_group(boots_str_dex, 'PercentReducedShockDurationOnYou', '#% reduced Shock duration on you', [lightning], 500, 100, 5, suffix).
mod_group(boots_str_dex, 'FlattoDexterity', '# to Dexterity', [attribute], 500, 100, 8, suffix).
mod_group(boots_str_dex, 'FlattoStrength', '# to Strength', [attribute], 500, 100, 8, suffix).
mod_group(boots_str_dex, 'FlattoStunThreshold', '# to Stun Threshold', [stun], 800, 100, 11, suffix).
mod_group(boots_str_dex, 'PercentToChaosResistance', '#% to Chaos Resistance', [chaos, resistance], 250, 100, 6, suffix).
mod_group(boots_str_dex, 'PercentToColdResistance', '#% to Cold Resistance', [cold, resistance], 1000, 100, 8, suffix).
mod_group(boots_str_dex, 'PercentToFireResistance', '#% to Fire Resistance', [fire, resistance], 1000, 100, 8, suffix).
mod_group(boots_str_dex, 'PercentToLightningResistance', '#% to Lightning Resistance', [lightning, resistance], 1000, 100, 8, suffix).
mod_group(boots_str_dex, 'PercentOfArmourAlsoAppliesToElementalDamage', '#% of Armour also applies to Elemental Damage', [armour, damage], 500, 100, 5, suffix).
mod_group(boots_str_dex, 'GainDeflectionRatingEqualToPercentOfEvasionRating', 'Gain Deflection Rating equal to #% of Evasion Rating', [evasion], 500, 100, 5, suffix).

