%%% Mod data for boots_str
%%% Source: POE2-PathOfCrafting (frankthetank001/POE2-PathOfCrafting)
%%% Original data: poe2db.tw via weights.csv
%%% Imported: 2026-06-09

%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)

mod_pool_weight_sum(boots_str, prefix, 6000).
mod_pool_weight_sum(boots_str, suffix, 10300).

mod_group(boots_str, PercentIncreasedArmour, '#% increased Armour', [armour], 1000, 100, 7, prefix).
mod_group(boots_str, PercentIncreasedArmourFlattoStunThreshold, '#% increased Armour, # to Stun Threshold', [armour], 1000, 100, 6, prefix).
mod_group(boots_str, PercentIncreasedMovementSpeed, '#% increased Movement Speed', [speed], 1000, 100, 6, prefix).
mod_group(boots_str, FlattoArmour, '# to Armour', [armour], 1000, 100, 7, prefix).
mod_group(boots_str, FlattoMaximumLife, '# to maximum Life', [life], 1000, 100, 9, prefix).
mod_group(boots_str, FlattoMaximumMana, '# to maximum Mana', [mana], 1000, 100, 9, prefix).
mod_group(boots_str, FlatLifeRegenerationPerSecond, '# Life Regeneration per second', [life], 1000, 100, 8, suffix).
mod_group(boots_str, PercentIncreasedRarityOfItemsFound, '#% increased Rarity of Items found', [], 1000, 100, 3, suffix).
mod_group(boots_str, PercentReducedAttributeRequirements, '#% reduced Attribute Requirements', [attribute], 750, 100, 5, suffix).
mod_group(boots_str, PercentReducedChillDurationOnYou, '#% reduced Chill Duration on you', [], 500, 100, 5, suffix).
mod_group(boots_str, PercentReducedFreezeDurationOnYou, '#% reduced Freeze Duration on you', [], 500, 100, 5, suffix).
mod_group(boots_str, PercentReducedShockDurationOnYou, '#% reduced Shock duration on you', [], 500, 100, 5, suffix).
mod_group(boots_str, FlattoStrength, '# to Strength', [attribute], 1000, 100, 8, suffix).
mod_group(boots_str, FlattoStunThreshold, '# to Stun Threshold', [], 800, 100, 11, suffix).
mod_group(boots_str, PercentToChaosResistance, '#% to Chaos Resistance', [chaos, resistance], 250, 100, 6, suffix).
mod_group(boots_str, PercentToColdResistance, '#% to Cold Resistance', [cold, resistance], 1000, 100, 8, suffix).
mod_group(boots_str, PercentToFireResistance, '#% to Fire Resistance', [fire, resistance], 1000, 100, 8, suffix).
mod_group(boots_str, PercentToLightningResistance, '#% to Lightning Resistance', [lightning, resistance], 1000, 100, 8, suffix).
mod_group(boots_str, PercentOfArmourAlsoAppliesToElementalDamage, '#% of Armour also applies to Elemental Damage', [armour, damage], 1000, 100, 5, suffix).
