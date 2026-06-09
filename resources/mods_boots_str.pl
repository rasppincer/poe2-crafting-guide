%%% Mod data for boots_str
%%% Source: https://poe2db.tw/us/Boots_str
%%% Extracted: 2026-06-09

%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)

mod_pool_weight_sum(boots_str, prefix, 44000).
mod_pool_weight_sum(boots_str, suffix, 69550).

mod_group(boots_str, 1IncreasedLife, '# to maximum Life', [life], 9000, 60, 9, prefix).
mod_group(boots_str, 1IncreasedMana, '# to maximum Mana', [mana], 9000, 60, 9, prefix).
mod_group(boots_str, 1BaseLocalDefences, '# to Armour', [armour], 7000, 54, 7, prefix).
mod_group(boots_str, 1DefencesPercent, '#% increased Armour', [armour], 7000, 65, 7, prefix).
mod_group(boots_str, 1DefencesPercentAndStunThreshold, '#% increased Armour, # to Stun Threshold', [armour], 6000, 74, 6, prefix).
mod_group(boots_str, 1MovementVelocity, '#% increased Movement Speed', [speed], 6000, 82, 6, prefix).

mod_group(boots_str, 2Strength, '# to Strength', [attribute], 8000, 74, 8, suffix).
mod_group(boots_str, 2FireResistance, '#% to Fire Resistance', [elemental, fire, resistance], 8000, 82, 8, suffix).
mod_group(boots_str, 2ColdResistance, '#% to Cold Resistance', [elemental, cold, resistance], 8000, 82, 8, suffix).
mod_group(boots_str, 2LightningResistance, '#% to Lightning Resistance', [elemental, lightning, resistance], 8000, 82, 8, suffix).
mod_group(boots_str, 2ChaosResistance, '#% to Chaos Resistance', [chaos, resistance], 1500, 81, 6, suffix).
mod_group(boots_str, 2LocalAttributeRequirements, '#% reduced Attribute Requirements', [], 3750, 60, 5, suffix).
mod_group(boots_str, 2StunThreshold, '# to Stun Threshold', [], 8800, 80, 11, suffix).
mod_group(boots_str, 2LifeRegeneration, '# Life Regeneration per second', [life], 8000, 58, 8, suffix).
mod_group(boots_str, 2ItemFoundRarityIncrease, '#% increased Rarity of Items found', [], 3000, 40, 3, suffix).
mod_group(boots_str, 2ReducedAilmentDuration, '#% reduced Shock/Chill/Freeze Duration on you', [elemental, lightning, cold, ailment], 7500, 75, 15, suffix).
mod_group(boots_str, 2ArmourAppliesToElementalDamage, '#% of Armour also applies to Elemental Damage', [armour, elemental], 5000, 66, 5, suffix).
