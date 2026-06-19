%%% Mod data for shield_str_dex
%%% Source: POE2-PathOfCrafting (frankthetank001/POE2-PathOfCrafting)
%%% Original data: poe2db.tw via weights.csv
%%% Auto-imported by import_from_pathofcrafting.py

%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)

mod_pool_weight_sum(shield_str_dex, prefix, 6000).
mod_pool_weight_sum(shield_str_dex, suffix, 8650).

mod_group(shield_str_dex, 'FlattoflatPhysicalThornsDamage', '# to # Physical Thorns damage', [physical, damage], 1000, 100, 7, prefix).
mod_group(shield_str_dex, 'PercentIncreasedArmourAndEvasion', '#% increased Armour and Evasion', [armour, evasion], 1000, 100, 8, prefix).
mod_group(shield_str_dex, 'PercentIncreasedArmourAndEvasionFlattoStunThreshold', '#% increased Armour and Evasion, # to Stun Threshold', [armour, evasion, stun], 1000, 100, 6, prefix).
mod_group(shield_str_dex, 'PercentIncreasedBlockChance', '#% increased Block chance', [block], 1000, 100, 3, prefix).
mod_group(shield_str_dex, 'FlattoArmourFlattoEvasionRating', '# to Armour, # to Evasion Rating', [armour, evasion], 1000, 100, 7, prefix).
mod_group(shield_str_dex, 'FlattoMaximumLife', '# to maximum Life', [life], 1000, 100, 11, prefix).

mod_group(shield_str_dex, 'PercentReducedAttributeRequirements', '#% reduced Attribute Requirements', [], 800, 100, 5, suffix).
mod_group(shield_str_dex, 'FlattoDexterity', '# to Dexterity', [attribute], 500, 100, 8, suffix).
mod_group(shield_str_dex, 'FlattoStrength', '# to Strength', [attribute], 500, 100, 8, suffix).
mod_group(shield_str_dex, 'FlattoStunThreshold', '# to Stun Threshold', [stun], 800, 100, 10, suffix).
mod_group(shield_str_dex, 'PercentToAllMaximumElementalResistances', '#% to all Maximum Elemental Resistances', [resistance], 125, 100, 2, suffix).
mod_group(shield_str_dex, 'PercentToChaosResistance', '#% to Chaos Resistance', [chaos, resistance], 250, 100, 6, suffix).
mod_group(shield_str_dex, 'PercentToColdResistance', '#% to Cold Resistance', [cold, resistance], 1000, 100, 8, suffix).
mod_group(shield_str_dex, 'PercentToFireResistance', '#% to Fire Resistance', [fire, resistance], 1000, 100, 8, suffix).
mod_group(shield_str_dex, 'PercentToLightningResistance', '#% to Lightning Resistance', [lightning, resistance], 1000, 100, 8, suffix).
mod_group(shield_str_dex, 'PercentToMaximumChaosResistance', '#% to Maximum Chaos Resistance', [chaos, resistance], 125, 100, 3, suffix).
mod_group(shield_str_dex, 'PercentToMaximumColdResistance', '#% to Maximum Cold Resistance', [cold, resistance], 250, 100, 3, suffix).
mod_group(shield_str_dex, 'PercentToMaximumFireResistance', '#% to Maximum Fire Resistance', [fire, resistance], 250, 100, 3, suffix).
mod_group(shield_str_dex, 'PercentToMaximumLightningResistance', '#% to Maximum Lightning Resistance', [lightning, resistance], 250, 100, 3, suffix).
mod_group(shield_str_dex, 'HitsAgainstYouHavePercentReducedCriticalDamageBonus', 'Hits against you have #% reduced Critical Damage Bonus', [critical, damage], 800, 100, 5, suffix).
mod_group(shield_str_dex, 'PercentOfArmourAlsoAppliesToElementalDamage', '#% of Armour also applies to Elemental Damage', [armour, damage], 500, 100, 6, suffix).
mod_group(shield_str_dex, 'GainDeflectionRatingEqualToPercentOfEvasionRating', 'Gain Deflection Rating equal to #% of Evasion Rating', [evasion], 500, 100, 6, suffix).

