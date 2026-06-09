%%% Mod data for boots_int
%%% Source: POE2-PathOfCrafting (frankthetank001/POE2-PathOfCrafting)
%%% Original data: poe2db.tw via weights.csv
%%% Imported: 2026-06-09

%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)

mod_pool_weight_sum(boots_int, prefix, 6000).
mod_pool_weight_sum(boots_int, suffix, 10300).

mod_group(boots_int, PercentIncreasedEnergyShield, '#% increased Energy Shield', [energy_shield], 1000, 100, 7, prefix).
mod_group(boots_int, PercentIncreasedEnergyShieldFlattoStunThreshold, '#% increased Energy Shield, # to Stun Threshold', [energy_shield], 1000, 100, 6, prefix).
mod_group(boots_int, PercentIncreasedMovementSpeed, '#% increased Movement Speed', [speed], 1000, 100, 6, prefix).
mod_group(boots_int, FlattoMaximumEnergyShield, '# to maximum Energy Shield', [energy_shield], 1000, 100, 7, prefix).
mod_group(boots_int, FlattoMaximumLife, '# to maximum Life', [life], 1000, 100, 9, prefix).
mod_group(boots_int, FlattoMaximumMana, '# to maximum Mana', [mana], 1000, 100, 9, prefix).
mod_group(boots_int, FlatLifeRegenerationPerSecond, '# Life Regeneration per second', [life], 1000, 100, 8, suffix).
mod_group(boots_int, PercentIncreasedRarityOfItemsFound, '#% increased Rarity of Items found', [], 1000, 100, 3, suffix).
mod_group(boots_int, PercentReducedAttributeRequirements, '#% reduced Attribute Requirements', [attribute], 750, 100, 5, suffix).
mod_group(boots_int, PercentReducedChillDurationOnYou, '#% reduced Chill Duration on you', [], 500, 100, 5, suffix).
mod_group(boots_int, PercentReducedFreezeDurationOnYou, '#% reduced Freeze Duration on you', [], 500, 100, 5, suffix).
mod_group(boots_int, PercentReducedShockDurationOnYou, '#% reduced Shock duration on you', [], 500, 100, 5, suffix).
mod_group(boots_int, FlattoIntelligence, '# to Intelligence', [attribute], 1000, 100, 8, suffix).
mod_group(boots_int, FlattoStunThreshold, '# to Stun Threshold', [], 800, 100, 11, suffix).
mod_group(boots_int, PercentToChaosResistance, '#% to Chaos Resistance', [chaos, resistance], 250, 100, 6, suffix).
mod_group(boots_int, PercentToColdResistance, '#% to Cold Resistance', [cold, resistance], 1000, 100, 8, suffix).
mod_group(boots_int, PercentToFireResistance, '#% to Fire Resistance', [fire, resistance], 1000, 100, 8, suffix).
mod_group(boots_int, PercentToLightningResistance, '#% to Lightning Resistance', [lightning, resistance], 1000, 100, 8, suffix).
mod_group(boots_int, PercentIncreasedEnergyShieldRechargeRate, '#% increased Energy Shield Recharge Rate', [energy_shield], 1000, 100, 4, suffix).
