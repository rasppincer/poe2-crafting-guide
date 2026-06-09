%%% Mod data for shield_str
%%% Source: POE2-PathOfCrafting (frankthetank001/POE2-PathOfCrafting)
%%% Original data: poe2db.tw via weights.csv
%%% Imported: 2026-06-09

%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)

mod_pool_weight_sum(shield_str, prefix, 6000).
mod_pool_weight_sum(shield_str, suffix, 8650).

mod_group(shield_str, FlattoFlatPhysicalThornsDamage, '# to # Physical Thorns damage', [physical, damage], 1000, 100, 7, prefix).
mod_group(shield_str, PercentIncreasedArmour, '#% increased Armour', [armour], 1000, 100, 8, prefix).
mod_group(shield_str, PercentIncreasedArmourFlattoStunThreshold, '#% increased Armour, # to Stun Threshold', [armour], 1000, 100, 6, prefix).
mod_group(shield_str, PercentIncreasedBlockChance, '#% increased Block chance', [block], 1000, 100, 3, prefix).
mod_group(shield_str, FlattoArmour, '# to Armour', [armour], 1000, 100, 10, prefix).
mod_group(shield_str, FlattoMaximumLife, '# to maximum Life', [life], 1000, 100, 11, prefix).
mod_group(shield_str, PercentAdditionalPhysicalDamageReduction, '#% additional Physical Damage Reduction', [physical, damage], 800, 100, 5, suffix).
mod_group(shield_str, PercentReducedAttributeRequirements, '#% reduced Attribute Requirements', [attribute], 800, 100, 5, suffix).
mod_group(shield_str, FlattoStrength, '# to Strength', [attribute], 1000, 100, 8, suffix).
mod_group(shield_str, FlattoStunThreshold, '# to Stun Threshold', [], 800, 100, 10, suffix).
mod_group(shield_str, PercentToAllMaximumElementalResistances, '#% to all Maximum Elemental Resistances', [resistance], 125, 100, 2, suffix).
mod_group(shield_str, PercentToChaosResistance, '#% to Chaos Resistance', [chaos, resistance], 250, 100, 6, suffix).
mod_group(shield_str, PercentToColdResistance, '#% to Cold Resistance', [cold, resistance], 1000, 100, 8, suffix).
mod_group(shield_str, PercentToFireResistance, '#% to Fire Resistance', [fire, resistance], 1000, 100, 8, suffix).
mod_group(shield_str, PercentToLightningResistance, '#% to Lightning Resistance', [lightning, resistance], 1000, 100, 8, suffix).
mod_group(shield_str, PercentToMaximumChaosResistance, '#% to Maximum Chaos Resistance', [chaos, resistance], 125, 100, 3, suffix).
mod_group(shield_str, PercentToMaximumColdResistance, '#% to Maximum Cold Resistance', [cold, resistance], 250, 100, 3, suffix).
mod_group(shield_str, PercentToMaximumFireResistance, '#% to Maximum Fire Resistance', [fire, resistance], 250, 100, 3, suffix).
mod_group(shield_str, PercentToMaximumLightningResistance, '#% to Maximum Lightning Resistance', [lightning, resistance], 250, 100, 3, suffix).
mod_group(shield_str, PercentOfArmourAlsoAppliesToElementalDamage, '#% of Armour also applies to Elemental Damage', [armour, damage], 1000, 100, 6, suffix).
