%%% Mod data for shield_str_int
%%% Source: POE2-PathOfCrafting (frankthetank001/POE2-PathOfCrafting)
%%% Original data: poe2db.tw via weights.csv
%%% Auto-imported by import_from_pathofcrafting.py

%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)

mod_pool_weight_sum(shield_str_int, prefix, 6000).
mod_pool_weight_sum(shield_str_int, suffix, 8650).

mod_group(shield_str_int, 'FlattoflatPhysicalThornsDamage', '# to # Physical Thorns damage', [physical, damage], 1000, 100, 7, prefix).
mod_group(shield_str_int, 'PercentIncreasedArmourAndEnergyShield', '#% increased Armour and Energy Shield', [energy_shield, armour], 1000, 100, 8, prefix).
mod_group(shield_str_int, 'PercentIncreasedArmourAndEnergyShieldFlattoStunThreshold', '#% increased Armour and Energy Shield, # to Stun Threshold', [energy_shield, armour, stun], 1000, 100, 6, prefix).
mod_group(shield_str_int, 'PercentIncreasedBlockChance', '#% increased Block chance', [block], 1000, 100, 3, prefix).
mod_group(shield_str_int, 'FlattoArmourFlattoMaximumEnergyShield', '# to Armour, # to maximum Energy Shield', [energy_shield, armour], 1000, 100, 7, prefix).
mod_group(shield_str_int, 'FlattoMaximumLife', '# to maximum Life', [life], 1000, 100, 11, prefix).

mod_group(shield_str_int, 'PercentReducedAttributeRequirements', '#% reduced Attribute Requirements', [], 800, 100, 5, suffix).
mod_group(shield_str_int, 'FlattoIntelligence', '# to Intelligence', [attribute], 500, 100, 8, suffix).
mod_group(shield_str_int, 'FlattoStrength', '# to Strength', [attribute], 500, 100, 8, suffix).
mod_group(shield_str_int, 'FlattoStunThreshold', '# to Stun Threshold', [stun], 800, 100, 10, suffix).
mod_group(shield_str_int, 'PercentToAllElementalResistances', '#% to all Elemental Resistances', [resistance], 800, 100, 6, suffix).
mod_group(shield_str_int, 'PercentToAllMaximumElementalResistances', '#% to all Maximum Elemental Resistances', [resistance], 125, 100, 2, suffix).
mod_group(shield_str_int, 'PercentToChaosResistance', '#% to Chaos Resistance', [chaos, resistance], 250, 100, 6, suffix).
mod_group(shield_str_int, 'PercentToColdResistance', '#% to Cold Resistance', [cold, resistance], 1000, 100, 8, suffix).
mod_group(shield_str_int, 'PercentToFireResistance', '#% to Fire Resistance', [fire, resistance], 1000, 100, 8, suffix).
mod_group(shield_str_int, 'PercentToLightningResistance', '#% to Lightning Resistance', [lightning, resistance], 1000, 100, 8, suffix).
mod_group(shield_str_int, 'PercentToMaximumChaosResistance', '#% to Maximum Chaos Resistance', [chaos, resistance], 125, 100, 3, suffix).
mod_group(shield_str_int, 'PercentToMaximumColdResistance', '#% to Maximum Cold Resistance', [cold, resistance], 250, 100, 3, suffix).
mod_group(shield_str_int, 'PercentToMaximumFireResistance', '#% to Maximum Fire Resistance', [fire, resistance], 250, 100, 3, suffix).
mod_group(shield_str_int, 'PercentToMaximumLightningResistance', '#% to Maximum Lightning Resistance', [lightning, resistance], 250, 100, 3, suffix).
mod_group(shield_str_int, 'PercentIncreasedEnergyShieldRechargeRate', '#% increased Energy Shield Recharge Rate', [energy_shield], 500, 100, 6, suffix).
mod_group(shield_str_int, 'PercentOfArmourAlsoAppliesToElementalDamage', '#% of Armour also applies to Elemental Damage', [armour, damage], 500, 100, 6, suffix).

