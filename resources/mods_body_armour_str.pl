%%% Mod data for body_armour_str
%%% Source: POE2-PathOfCrafting (frankthetank001/POE2-PathOfCrafting)
%%% Original data: poe2db.tw via weights.csv
%%% Auto-imported by import_from_pathofcrafting.py

%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)

mod_pool_weight_sum(body_armour_str, prefix, 6500).
mod_pool_weight_sum(body_armour_str, suffix, 9450).

mod_group(body_armour_str, 'FlattoflatPhysicalThornsDamage', '# to # Physical Thorns damage', [physical, damage], 1000, 100, 7, prefix).
mod_group(body_armour_str, 'PercentIncreasedArmour', '#% increased Armour', [armour], 1000, 100, 8, prefix).
mod_group(body_armour_str, 'FlattoArmourPercentIncreasedArmour', '# to Armour, #% increased Armour', [armour], 1000, 100, 6, prefix).
mod_group(body_armour_str, 'PercentIncreasedArmourFlattoMaximumLife', '#% increased Armour, # to maximum Life', [life, armour], 1000, 100, 6, prefix).
mod_group(body_armour_str, 'FlattoArmour', '# to Armour', [armour], 1000, 100, 11, prefix).
mod_group(body_armour_str, 'FlattoMaximumLife', '# to maximum Life', [life], 1000, 100, 13, prefix).
mod_group(body_armour_str, 'FlattoSpirit', '# to Spirit', [], 500, 100, 8, prefix).

mod_group(body_armour_str, 'FlatLifeRegenerationPerSecond', '# Life Regeneration per second', [life, regeneration], 1000, 100, 11, suffix).
mod_group(body_armour_str, 'PercentReducedAttributeRequirements', '#% reduced Attribute Requirements', [], 900, 100, 5, suffix).
mod_group(body_armour_str, 'PercentReducedDurationOfBleedingOnYou', '#% reduced Duration of Bleeding on You', [], 500, 100, 5, suffix).
mod_group(body_armour_str, 'PercentReducedIgniteDurationOnYou', '#% reduced Ignite Duration on you', [], 500, 100, 5, suffix).
mod_group(body_armour_str, 'PercentReducedPoisonDurationOnYou', '#% reduced Poison Duration on you', [], 500, 100, 5, suffix).
mod_group(body_armour_str, 'FlattoStrength', '# to Strength', [attribute], 1000, 100, 8, suffix).
mod_group(body_armour_str, 'FlattoStunThreshold', '# to Stun Threshold', [stun], 800, 100, 10, suffix).
mod_group(body_armour_str, 'PercentToChaosResistance', '#% to Chaos Resistance', [chaos, resistance], 250, 100, 6, suffix).
mod_group(body_armour_str, 'PercentToColdResistance', '#% to Cold Resistance', [cold, resistance], 1000, 100, 8, suffix).
mod_group(body_armour_str, 'PercentToFireResistance', '#% to Fire Resistance', [fire, resistance], 1000, 100, 8, suffix).
mod_group(body_armour_str, 'PercentToLightningResistance', '#% to Lightning Resistance', [lightning, resistance], 1000, 100, 8, suffix).
mod_group(body_armour_str, 'PercentOfArmourAlsoAppliesToElementalDamage', '#% of Armour also applies to Elemental Damage', [armour, damage], 1000, 100, 6, suffix).

