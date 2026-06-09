%%% Mod data for body_armour_dex_int
%%% Source: POE2-PathOfCrafting (frankthetank001/POE2-PathOfCrafting)
%%% Original data: poe2db.tw via weights.csv
%%% Imported: 2026-06-09

%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)

mod_pool_weight_sum(body_armour_dex_int, prefix, 6100).
mod_pool_weight_sum(body_armour_dex_int, suffix, 9450).

mod_group(body_armour_dex_int, FlattoFlatPhysicalThornsDamage, '# to # Physical Thorns damage', [physical, damage], 1000, 100, 7, prefix).
mod_group(body_armour_dex_int, PercentIncreasedEvasionAndEnergyShield, '#% increased Evasion and Energy Shield', [evasion, energy_shield], 1000, 100, 8, prefix).
mod_group(body_armour_dex_int, FlattoEvasionRatingFlattoMaximumEnergyShieldPercentIncreasedEvasionAndEnergyShield, '# to Evasion Rating, # to maximum Energy Shield, #% increased Evasion and Energy Shield', [evasion, energy_shield], 1000, 100, 6, prefix).
mod_group(body_armour_dex_int, PercentIncreasedEvasionAndEnergyShieldFlattoMaximumLife, '#% increased Evasion and Energy Shield, # to maximum Life', [life, evasion, energy_shield], 1000, 100, 6, prefix).
mod_group(body_armour_dex_int, FlattoEvasionRatingFlattoMaximumEnergyShield, '# to Evasion Rating, # to maximum Energy Shield', [evasion, energy_shield], 1000, 100, 8, prefix).
mod_group(body_armour_dex_int, FlattoMaximumLife, '# to maximum Life', [life], 1000, 100, 13, prefix).
mod_group(body_armour_dex_int, FlattoSpirit, '# to Spirit', [spirit], 100, 100, 8, prefix).
mod_group(body_armour_dex_int, FlatLifeRegenerationPerSecond, '# Life Regeneration per second', [life], 1000, 100, 11, suffix).
mod_group(body_armour_dex_int, PercentReducedAttributeRequirements, '#% reduced Attribute Requirements', [attribute], 900, 100, 5, suffix).
mod_group(body_armour_dex_int, PercentReducedDurationOfBleedingOnYou, '#% reduced Duration of Bleeding on You', [], 500, 100, 5, suffix).
mod_group(body_armour_dex_int, PercentReducedIgniteDurationOnYou, '#% reduced Ignite Duration on you', [], 500, 100, 5, suffix).
mod_group(body_armour_dex_int, PercentReducedPoisonDurationOnYou, '#% reduced Poison Duration on you', [], 500, 100, 5, suffix).
mod_group(body_armour_dex_int, FlattoDexterity, '# to Dexterity', [attribute], 500, 100, 8, suffix).
mod_group(body_armour_dex_int, FlattoIntelligence, '# to Intelligence', [attribute], 500, 100, 8, suffix).
mod_group(body_armour_dex_int, FlattoStunThreshold, '# to Stun Threshold', [], 800, 100, 10, suffix).
mod_group(body_armour_dex_int, PercentToChaosResistance, '#% to Chaos Resistance', [chaos, resistance], 250, 100, 6, suffix).
mod_group(body_armour_dex_int, PercentToColdResistance, '#% to Cold Resistance', [cold, resistance], 1000, 100, 8, suffix).
mod_group(body_armour_dex_int, PercentToFireResistance, '#% to Fire Resistance', [fire, resistance], 1000, 100, 8, suffix).
mod_group(body_armour_dex_int, PercentToLightningResistance, '#% to Lightning Resistance', [lightning, resistance], 1000, 100, 8, suffix).
mod_group(body_armour_dex_int, PercentFasterStartOfEnergyShieldRecharge, '#% faster start of Energy Shield Recharge', [energy_shield], 500, 100, 6, suffix).
mod_group(body_armour_dex_int, GainDeflectionRatingEqualToPercentOfEvasionRating, 'Gain Deflection Rating equal to #% of Evasion Rating', [evasion], 500, 100, 6, suffix).
