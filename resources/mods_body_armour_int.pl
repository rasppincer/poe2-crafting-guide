%%% Mod data for body_armour_int
%%% Source: POE2-PathOfCrafting (frankthetank001/POE2-PathOfCrafting)
%%% Original data: poe2db.tw via weights.csv
%%% Auto-imported by import_from_pathofcrafting.py

%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)

mod_pool_weight_sum(body_armour_int, prefix, 6500).
mod_pool_weight_sum(body_armour_int, suffix, 9450).

mod_group(body_armour_int, 'FlattoflatPhysicalThornsDamage', '# to # Physical Thorns damage', [physical, damage], 1000, 100, 7, prefix).
mod_group(body_armour_int, 'PercentIncreasedEnergyShield', '#% increased Energy Shield', [energy_shield], 1000, 100, 8, prefix).
mod_group(body_armour_int, 'FlattoMaximumEnergyShieldPercentIncreasedEnergyShield', '# to maximum Energy Shield, #% increased Energy Shield', [energy_shield], 1000, 100, 6, prefix).
mod_group(body_armour_int, 'PercentIncreasedEnergyShieldFlattoMaximumLife', '#% increased Energy Shield, # to maximum Life', [life, energy_shield], 1000, 100, 6, prefix).
mod_group(body_armour_int, 'FlattoMaximumEnergyShield', '# to maximum Energy Shield', [energy_shield], 1000, 100, 11, prefix).
mod_group(body_armour_int, 'FlattoMaximumLife', '# to maximum Life', [life], 1000, 100, 13, prefix).
mod_group(body_armour_int, 'FlattoSpirit', '# to Spirit', [], 500, 100, 8, prefix).

mod_group(body_armour_int, 'FlatLifeRegenerationPerSecond', '# Life Regeneration per second', [life, regeneration], 1000, 100, 11, suffix).
mod_group(body_armour_int, 'PercentReducedAttributeRequirements', '#% reduced Attribute Requirements', [], 900, 100, 5, suffix).
mod_group(body_armour_int, 'PercentReducedDurationOfBleedingOnYou', '#% reduced Duration of Bleeding on You', [], 500, 100, 5, suffix).
mod_group(body_armour_int, 'PercentReducedIgniteDurationOnYou', '#% reduced Ignite Duration on you', [], 500, 100, 5, suffix).
mod_group(body_armour_int, 'PercentReducedPoisonDurationOnYou', '#% reduced Poison Duration on you', [], 500, 100, 5, suffix).
mod_group(body_armour_int, 'FlattoIntelligence', '# to Intelligence', [attribute], 1000, 100, 8, suffix).
mod_group(body_armour_int, 'FlattoStunThreshold', '# to Stun Threshold', [stun], 800, 100, 10, suffix).
mod_group(body_armour_int, 'PercentToChaosResistance', '#% to Chaos Resistance', [chaos, resistance], 250, 100, 6, suffix).
mod_group(body_armour_int, 'PercentToColdResistance', '#% to Cold Resistance', [cold, resistance], 1000, 100, 8, suffix).
mod_group(body_armour_int, 'PercentToFireResistance', '#% to Fire Resistance', [fire, resistance], 1000, 100, 8, suffix).
mod_group(body_armour_int, 'PercentToLightningResistance', '#% to Lightning Resistance', [lightning, resistance], 1000, 100, 8, suffix).
mod_group(body_armour_int, 'PercentFasterStartOfEnergyShieldRecharge', '#% faster start of Energy Shield Recharge', [energy_shield], 1000, 100, 6, suffix).

