%%% Mod data for body_armour_dex
%%% Source: POE2-PathOfCrafting (frankthetank001/POE2-PathOfCrafting)
%%% Original data: poe2db.tw via weights.csv
%%% Auto-imported by import_from_pathofcrafting.py

%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)

mod_pool_weight_sum(body_armour_dex, prefix, 6500).
mod_pool_weight_sum(body_armour_dex, suffix, 9450).

mod_group(body_armour_dex, 'FlattoflatPhysicalThornsDamage', '# to # Physical Thorns damage', [physical, damage], 1000, 100, 7, prefix).
mod_group(body_armour_dex, 'PercentIncreasedEvasionRating', '#% increased Evasion Rating', [evasion], 1000, 100, 8, prefix).
mod_group(body_armour_dex, 'FlattoEvasionRatingPercentIncreasedEvasionRating', '# to Evasion Rating, #% increased Evasion Rating', [evasion], 1000, 100, 6, prefix).
mod_group(body_armour_dex, 'PercentIncreasedEvasionRatingFlattoMaximumLife', '#% increased Evasion Rating, # to maximum Life', [life, evasion], 1000, 100, 6, prefix).
mod_group(body_armour_dex, 'FlattoEvasionRating', '# to Evasion Rating', [evasion], 1000, 100, 11, prefix).
mod_group(body_armour_dex, 'FlattoMaximumLife', '# to maximum Life', [life], 1000, 100, 13, prefix).
mod_group(body_armour_dex, 'FlattoSpirit', '# to Spirit', [], 500, 100, 8, prefix).

mod_group(body_armour_dex, 'FlatLifeRegenerationPerSecond', '# Life Regeneration per second', [life, regeneration], 1000, 100, 11, suffix).
mod_group(body_armour_dex, 'PercentReducedAttributeRequirements', '#% reduced Attribute Requirements', [], 900, 100, 5, suffix).
mod_group(body_armour_dex, 'PercentReducedDurationOfBleedingOnYou', '#% reduced Duration of Bleeding on You', [], 500, 100, 5, suffix).
mod_group(body_armour_dex, 'PercentReducedIgniteDurationOnYou', '#% reduced Ignite Duration on you', [], 500, 100, 5, suffix).
mod_group(body_armour_dex, 'PercentReducedPoisonDurationOnYou', '#% reduced Poison Duration on you', [], 500, 100, 5, suffix).
mod_group(body_armour_dex, 'FlattoDexterity', '# to Dexterity', [attribute], 1000, 100, 8, suffix).
mod_group(body_armour_dex, 'FlattoStunThreshold', '# to Stun Threshold', [stun], 800, 100, 10, suffix).
mod_group(body_armour_dex, 'PercentToChaosResistance', '#% to Chaos Resistance', [chaos, resistance], 250, 100, 6, suffix).
mod_group(body_armour_dex, 'PercentToColdResistance', '#% to Cold Resistance', [cold, resistance], 1000, 100, 8, suffix).
mod_group(body_armour_dex, 'PercentToFireResistance', '#% to Fire Resistance', [fire, resistance], 1000, 100, 8, suffix).
mod_group(body_armour_dex, 'PercentToLightningResistance', '#% to Lightning Resistance', [lightning, resistance], 1000, 100, 8, suffix).
mod_group(body_armour_dex, 'GainDeflectionRatingEqualToPercentOfEvasionRating', 'Gain Deflection Rating equal to #% of Evasion Rating', [evasion], 1000, 100, 6, suffix).

