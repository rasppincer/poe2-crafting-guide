%%% Mod data for buckler
%%% Source: POE2-PathOfCrafting (frankthetank001/POE2-PathOfCrafting)
%%% Original data: poe2db.tw via weights.csv
%%% Imported: 2026-06-09

%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)

mod_pool_weight_sum(buckler, prefix, 6000).
mod_pool_weight_sum(buckler, suffix, 7850).

mod_group(buckler, FlattoFlatPhysicalThornsDamage, '# to # Physical Thorns damage', [physical, damage], 1000, 100, 7, prefix).
mod_group(buckler, PercentIncreasedBlockChance, '#% increased Block chance', [block], 1000, 100, 3, prefix).
mod_group(buckler, PercentIncreasedEvasionRating, '#% increased Evasion Rating', [evasion], 1000, 100, 8, prefix).
mod_group(buckler, PercentIncreasedEvasionRatingFlattoStunThreshold, '#% increased Evasion Rating, # to Stun Threshold', [evasion], 1000, 100, 6, prefix).
mod_group(buckler, FlattoEvasionRating, '# to Evasion Rating', [evasion], 1000, 100, 10, prefix).
mod_group(buckler, FlattoMaximumLife, '# to maximum Life', [life], 1000, 100, 11, prefix).
mod_group(buckler, PercentReducedAttributeRequirements, '#% reduced Attribute Requirements', [attribute], 800, 100, 5, suffix).
mod_group(buckler, FlattoDexterity, '# to Dexterity', [attribute], 1000, 100, 8, suffix).
mod_group(buckler, FlattoStunThreshold, '# to Stun Threshold', [], 800, 100, 10, suffix).
mod_group(buckler, PercentToAllMaximumElementalResistances, '#% to all Maximum Elemental Resistances', [resistance], 125, 100, 2, suffix).
mod_group(buckler, PercentToChaosResistance, '#% to Chaos Resistance', [chaos, resistance], 250, 100, 6, suffix).
mod_group(buckler, PercentToColdResistance, '#% to Cold Resistance', [cold, resistance], 1000, 100, 8, suffix).
mod_group(buckler, PercentToFireResistance, '#% to Fire Resistance', [fire, resistance], 1000, 100, 8, suffix).
mod_group(buckler, PercentToLightningResistance, '#% to Lightning Resistance', [lightning, resistance], 1000, 100, 8, suffix).
mod_group(buckler, PercentToMaximumChaosResistance, '#% to Maximum Chaos Resistance', [chaos, resistance], 125, 100, 3, suffix).
mod_group(buckler, PercentToMaximumColdResistance, '#% to Maximum Cold Resistance', [cold, resistance], 250, 100, 3, suffix).
mod_group(buckler, PercentToMaximumFireResistance, '#% to Maximum Fire Resistance', [fire, resistance], 250, 100, 3, suffix).
mod_group(buckler, PercentToMaximumLightningResistance, '#% to Maximum Lightning Resistance', [lightning, resistance], 250, 100, 3, suffix).
mod_group(buckler, GainDeflectionRatingEqualToPercentOfEvasionRating, 'Gain Deflection Rating equal to #% of Evasion Rating', [evasion], 1000, 100, 6, suffix).
