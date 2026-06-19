%%% Mod data for boots_dex_int
%%% Source: POE2-PathOfCrafting (frankthetank001/POE2-PathOfCrafting)
%%% Original data: poe2db.tw via weights.csv
%%% Auto-imported by import_from_pathofcrafting.py

%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)

mod_pool_weight_sum(boots_dex_int, prefix, 6000).
mod_pool_weight_sum(boots_dex_int, suffix, 10300).

mod_group(boots_dex_int, 'PercentIncreasedEvasionAndEnergyShield', '#% increased Evasion and Energy Shield', [energy_shield, evasion], 1000, 100, 7, prefix).
mod_group(boots_dex_int, 'PercentIncreasedEvasionAndEnergyShieldFlattoStunThreshold', '#% increased Evasion and Energy Shield, # to Stun Threshold', [energy_shield, evasion, stun], 1000, 100, 6, prefix).
mod_group(boots_dex_int, 'PercentIncreasedMovementSpeed', '#% increased Movement Speed', [speed], 1000, 100, 6, prefix).
mod_group(boots_dex_int, 'FlattoEvasionRatingFlattoMaximumEnergyShield', '# to Evasion Rating, # to maximum Energy Shield', [energy_shield, evasion], 1000, 100, 4, prefix).
mod_group(boots_dex_int, 'FlattoMaximumLife', '# to maximum Life', [life], 1000, 100, 9, prefix).
mod_group(boots_dex_int, 'FlattoMaximumMana', '# to maximum Mana', [mana], 1000, 100, 9, prefix).

mod_group(boots_dex_int, 'FlatLifeRegenerationPerSecond', '# Life Regeneration per second', [life, regeneration], 1000, 100, 8, suffix).
mod_group(boots_dex_int, 'PercentIncreasedRarityOfItemsFound', '#% increased Rarity of Items found', [rarity], 1000, 100, 3, suffix).
mod_group(boots_dex_int, 'PercentReducedAttributeRequirements', '#% reduced Attribute Requirements', [], 750, 100, 5, suffix).
mod_group(boots_dex_int, 'PercentReducedChillDurationOnYou', '#% reduced Chill Duration on you', [cold], 500, 100, 5, suffix).
mod_group(boots_dex_int, 'PercentReducedFreezeDurationOnYou', '#% reduced Freeze Duration on you', [cold], 500, 100, 5, suffix).
mod_group(boots_dex_int, 'PercentReducedShockDurationOnYou', '#% reduced Shock duration on you', [lightning], 500, 100, 5, suffix).
mod_group(boots_dex_int, 'FlattoDexterity', '# to Dexterity', [attribute], 500, 100, 8, suffix).
mod_group(boots_dex_int, 'FlattoIntelligence', '# to Intelligence', [attribute], 500, 100, 8, suffix).
mod_group(boots_dex_int, 'FlattoStunThreshold', '# to Stun Threshold', [stun], 800, 100, 11, suffix).
mod_group(boots_dex_int, 'PercentToChaosResistance', '#% to Chaos Resistance', [chaos, resistance], 250, 100, 6, suffix).
mod_group(boots_dex_int, 'PercentToColdResistance', '#% to Cold Resistance', [cold, resistance], 1000, 100, 8, suffix).
mod_group(boots_dex_int, 'PercentToFireResistance', '#% to Fire Resistance', [fire, resistance], 1000, 100, 8, suffix).
mod_group(boots_dex_int, 'PercentToLightningResistance', '#% to Lightning Resistance', [lightning, resistance], 1000, 100, 8, suffix).
mod_group(boots_dex_int, 'PercentIncreasedEnergyShieldRechargeRate', '#% increased Energy Shield Recharge Rate', [energy_shield], 500, 100, 4, suffix).
mod_group(boots_dex_int, 'GainDeflectionRatingEqualToPercentOfEvasionRating', 'Gain Deflection Rating equal to #% of Evasion Rating', [evasion], 500, 100, 5, suffix).

