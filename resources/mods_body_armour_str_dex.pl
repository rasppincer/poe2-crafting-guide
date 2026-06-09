%%% Mod data for body_armour_str_dex
%%% Source: POE2-PathOfCrafting (frankthetank001/POE2-PathOfCrafting)
%%% Original data: poe2db.tw via weights.csv
%%% Imported: 2026-06-09

%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)

mod_pool_weight_sum(body_armour_str_dex, prefix, 6100).
mod_pool_weight_sum(body_armour_str_dex, suffix, 9450).

mod_group(body_armour_str_dex, FlattoFlatPhysicalThornsDamage, '# to # Physical Thorns damage', [physical, damage], 1000, 100, 7, prefix).
mod_group(body_armour_str_dex, PercentIncreasedArmourAndEvasion, '#% increased Armour and Evasion', [armour, evasion], 1000, 100, 8, prefix).
mod_group(body_armour_str_dex, FlattoArmourFlattoEvasionRatingPercentIncreasedArmourAndEvasion, '# to Armour, # to Evasion Rating, #% increased Armour and Evasion', [armour, evasion], 1000, 100, 6, prefix).
mod_group(body_armour_str_dex, PercentIncreasedArmourAndEvasionFlattoMaximumLife, '#% increased Armour and Evasion, # to maximum Life', [life, armour, evasion], 1000, 100, 6, prefix).
mod_group(body_armour_str_dex, FlattoArmourFlattoEvasionRating, '# to Armour, # to Evasion Rating', [armour, evasion], 1000, 100, 8, prefix).
mod_group(body_armour_str_dex, FlattoMaximumLife, '# to maximum Life', [life], 1000, 100, 13, prefix).
mod_group(body_armour_str_dex, FlattoSpirit, '# to Spirit', [spirit], 100, 100, 8, prefix).
mod_group(body_armour_str_dex, FlatLifeRegenerationPerSecond, '# Life Regeneration per second', [life], 1000, 100, 11, suffix).
mod_group(body_armour_str_dex, PercentReducedAttributeRequirements, '#% reduced Attribute Requirements', [attribute], 900, 100, 5, suffix).
mod_group(body_armour_str_dex, PercentReducedDurationOfBleedingOnYou, '#% reduced Duration of Bleeding on You', [], 500, 100, 5, suffix).
mod_group(body_armour_str_dex, PercentReducedIgniteDurationOnYou, '#% reduced Ignite Duration on you', [], 500, 100, 5, suffix).
mod_group(body_armour_str_dex, PercentReducedPoisonDurationOnYou, '#% reduced Poison Duration on you', [], 500, 100, 5, suffix).
mod_group(body_armour_str_dex, FlattoDexterity, '# to Dexterity', [attribute], 500, 100, 8, suffix).
mod_group(body_armour_str_dex, FlattoStrength, '# to Strength', [attribute], 500, 100, 8, suffix).
mod_group(body_armour_str_dex, FlattoStunThreshold, '# to Stun Threshold', [], 800, 100, 10, suffix).
mod_group(body_armour_str_dex, PercentToChaosResistance, '#% to Chaos Resistance', [chaos, resistance], 250, 100, 6, suffix).
mod_group(body_armour_str_dex, PercentToColdResistance, '#% to Cold Resistance', [cold, resistance], 1000, 100, 8, suffix).
mod_group(body_armour_str_dex, PercentToFireResistance, '#% to Fire Resistance', [fire, resistance], 1000, 100, 8, suffix).
mod_group(body_armour_str_dex, PercentToLightningResistance, '#% to Lightning Resistance', [lightning, resistance], 1000, 100, 8, suffix).
mod_group(body_armour_str_dex, PercentOfArmourAlsoAppliesToElementalDamage, '#% of Armour also applies to Elemental Damage', [armour, damage], 500, 100, 6, suffix).
mod_group(body_armour_str_dex, GainDeflectionRatingEqualToPercentOfEvasionRating, 'Gain Deflection Rating equal to #% of Evasion Rating', [evasion], 500, 100, 6, suffix).
