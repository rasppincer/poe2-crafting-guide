%%% Mod data for body_armour_str
%%% Source: https://poe2db.tw/us/Body_Armours_str
%%% Extracted: 2026-06-09

%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)

mod_pool_weight_sum(body_armour_str, prefix, 54000).
mod_pool_weight_sum(body_armour_str, suffix, 70500).

mod_group(body_armour_str, 1IncreasedLife, '+# to maximum Life', [life], 13000, 80, 13, prefix).
mod_group(body_armour_str, 1BaseLocalDefences, '+# to Armour', [armour], 11000, 79, 11, prefix).
mod_group(body_armour_str, 1DefencesPercent, '#% increased Armour', [armour], 8000, 75, 8, prefix).
mod_group(body_armour_str, 1BaseLocalDefencesAndLife, '#% increased Armour / +# to maximum Life (hybrid)', [life, armour], 6000, 78, 6, prefix).
mod_group(body_armour_str, 1BaseLocalDefencesAndDefencePercent, '+# to Armour / #% increased Armour (hybrid)', [armour], 6000, 78, 6, prefix).
mod_group(body_armour_str, 1Thorns, '+# to # Physical Thorns damage', [damage, physical], 7000, 74, 7, prefix).
mod_group(body_armour_str, 1BaseSpirit, '+# to Spirit', [], 3000, 78, 8, prefix).

mod_group(body_armour_str, 2Strength, '+# to Strength', [attribute], 8000, 74, 8, suffix).
mod_group(body_armour_str, 2FireResistance, '#% to Fire Resistance', [elemental, fire, resistance], 8000, 82, 8, suffix).
mod_group(body_armour_str, 2ColdResistance, '#% to Cold Resistance', [elemental, cold, resistance], 8000, 82, 8, suffix).
mod_group(body_armour_str, 2LightningResistance, '#% to Lightning Resistance', [elemental, lightning, resistance], 8000, 82, 8, suffix).
mod_group(body_armour_str, 2ChaosResistance, '#% to Chaos Resistance', [chaos, resistance], 1500, 81, 6, suffix).
mod_group(body_armour_str, 2LocalAttributeRequirements, '#% reduced Attribute Requirements', [], 4500, 60, 5, suffix).
mod_group(body_armour_str, 2StunThreshold, '+# to Stun Threshold', [], 8000, 72, 10, suffix).
mod_group(body_armour_str, 2LifeRegeneration, '# Life Regeneration per second', [life], 11000, 81, 11, suffix).
mod_group(body_armour_str, 2ReducedAilmentDuration, '#% reduced Duration of Bleeding/Poison/Ignite on You', [physical, ailment, chaos, elemental, fire], 7500, 76, 15, suffix).
mod_group(body_armour_str, 2ArmourAppliesToElementalDamage, '#% of Armour also applies to Elemental Damage', [armour, elemental], 6000, 81, 6, suffix).
