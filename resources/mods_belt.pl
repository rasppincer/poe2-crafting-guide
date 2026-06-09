%%% Mod data for belt
%%% Source: POE2-PathOfCrafting (frankthetank001/POE2-PathOfCrafting)
%%% Original data: poe2db.tw via weights.csv
%%% Imported: 2026-06-09

%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)

mod_pool_weight_sum(belt, prefix, 6400).
mod_pool_weight_sum(belt, suffix, 9250).

mod_group(belt, FlattoFlatPhysicalThornsDamage, '# to # Physical Thorns damage', [physical, damage], 1000, 100, 7, prefix).
mod_group(belt, PercentIncreasedCharmEffectDuration, '#% increased Charm Effect Duration', [], 800, 100, 5, prefix).
mod_group(belt, PercentIncreasedFlaskLifeRecoveryRate, '#% increased Flask Life Recovery rate', [life], 800, 100, 6, prefix).
mod_group(belt, PercentIncreasedFlaskManaRecoveryRate, '#% increased Flask Mana Recovery rate', [mana], 800, 100, 6, prefix).
mod_group(belt, FlattoArmour, '# to Armour', [armour], 1000, 100, 10, prefix).
mod_group(belt, FlattoMaximumLife, '# to maximum Life', [life], 1000, 100, 10, prefix).
mod_group(belt, FlattoMaximumMana, '# to maximum Mana', [mana], 1000, 100, 9, prefix).
mod_group(belt, FlatLifeRegenerationPerSecond, '# Life Regeneration per second', [life], 1000, 100, 9, suffix).
mod_group(belt, PercentIncreasedCharmChargesGained, '#% increased Charm Charges gained', [], 800, 100, 6, suffix).
mod_group(belt, PercentIncreasedFlaskChargesGained, '#% increased Flask Charges gained', [], 800, 100, 6, suffix).
mod_group(belt, PercentReducedCharmChargesUsed, '#% reduced Charm Charges used', [], 800, 100, 6, suffix).
mod_group(belt, PercentReducedFlaskChargesUsed, '#% reduced Flask Charges used', [], 800, 100, 6, suffix).
mod_group(belt, FlattoStrength, '# to Strength', [attribute], 1000, 100, 9, suffix).
mod_group(belt, FlattoStunThreshold, '# to Stun Threshold', [], 800, 100, 10, suffix).
mod_group(belt, PercentToChaosResistance, '#% to Chaos Resistance', [chaos, resistance], 250, 100, 6, suffix).
mod_group(belt, PercentToColdResistance, '#% to Cold Resistance', [cold, resistance], 1000, 100, 8, suffix).
mod_group(belt, PercentToFireResistance, '#% to Fire Resistance', [fire, resistance], 1000, 100, 8, suffix).
mod_group(belt, PercentToLightningResistance, '#% to Lightning Resistance', [lightning, resistance], 1000, 100, 8, suffix).
