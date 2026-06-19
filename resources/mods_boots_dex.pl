%%% Mod data for boots_dex
%%% Source: POE2-PathOfCrafting (frankthetank001/POE2-PathOfCrafting)
%%% Original data: poe2db.tw via weights.csv
%%% Auto-imported by import_from_pathofcrafting.py

%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)

mod_pool_weight_sum(boots_dex, prefix, 6000).
mod_pool_weight_sum(boots_dex, suffix, 10300).

mod_group(boots_dex, 'PercentIncreasedEvasionRating', '#% increased Evasion Rating', [evasion], 1000, 100, 7, prefix).
mod_group(boots_dex, 'PercentIncreasedEvasionRatingFlattoStunThreshold', '#% increased Evasion Rating, # to Stun Threshold', [evasion, stun], 1000, 100, 6, prefix).
mod_group(boots_dex, 'PercentIncreasedMovementSpeed', '#% increased Movement Speed', [speed], 1000, 100, 6, prefix).
mod_group(boots_dex, 'FlattoEvasionRating', '# to Evasion Rating', [evasion], 1000, 100, 7, prefix).
mod_group(boots_dex, 'FlattoMaximumLife', '# to maximum Life', [life], 1000, 100, 9, prefix).
mod_group(boots_dex, 'FlattoMaximumMana', '# to maximum Mana', [mana], 1000, 100, 9, prefix).

mod_group(boots_dex, 'FlatLifeRegenerationPerSecond', '# Life Regeneration per second', [life, regeneration], 1000, 100, 8, suffix).
mod_group(boots_dex, 'PercentIncreasedRarityOfItemsFound', '#% increased Rarity of Items found', [rarity], 1000, 100, 3, suffix).
mod_group(boots_dex, 'PercentReducedAttributeRequirements', '#% reduced Attribute Requirements', [], 750, 100, 5, suffix).
mod_group(boots_dex, 'PercentReducedChillDurationOnYou', '#% reduced Chill Duration on you', [cold], 500, 100, 5, suffix).
mod_group(boots_dex, 'PercentReducedFreezeDurationOnYou', '#% reduced Freeze Duration on you', [cold], 500, 100, 5, suffix).
mod_group(boots_dex, 'PercentReducedShockDurationOnYou', '#% reduced Shock duration on you', [lightning], 500, 100, 5, suffix).
mod_group(boots_dex, 'FlattoDexterity', '# to Dexterity', [attribute], 1000, 100, 8, suffix).
mod_group(boots_dex, 'FlattoStunThreshold', '# to Stun Threshold', [stun], 800, 100, 11, suffix).
mod_group(boots_dex, 'PercentToChaosResistance', '#% to Chaos Resistance', [chaos, resistance], 250, 100, 6, suffix).
mod_group(boots_dex, 'PercentToColdResistance', '#% to Cold Resistance', [cold, resistance], 1000, 100, 8, suffix).
mod_group(boots_dex, 'PercentToFireResistance', '#% to Fire Resistance', [fire, resistance], 1000, 100, 8, suffix).
mod_group(boots_dex, 'PercentToLightningResistance', '#% to Lightning Resistance', [lightning, resistance], 1000, 100, 8, suffix).
mod_group(boots_dex, 'GainDeflectionRatingEqualToPercentOfEvasionRating', 'Gain Deflection Rating equal to #% of Evasion Rating', [evasion], 1000, 100, 5, suffix).

