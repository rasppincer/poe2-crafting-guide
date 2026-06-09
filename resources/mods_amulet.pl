%%% Mod data for amulet
%%% Source: https://poe2db.tw/us/Amulets
%%% Extracted: 2026-06-09

%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)

mod_pool_weight_sum(amulet, prefix, 72200).
mod_pool_weight_sum(amulet, suffix, 96656).

mod_group(amulet, 1IncreasedLife, '# to maximum Life', [life], 9000, 60, 9, prefix).
mod_group(amulet, 1MaximumLifeIncreasePercent, '#% increased maximum Life', [life], 900, 75, 3, prefix).
mod_group(amulet, 1IncreasedMana, '# to maximum Mana', [mana], 13000, 82, 13, prefix).
mod_group(amulet, 1MaximumManaIncreasePercent, '#% increased maximum Mana', [mana], 900, 75, 3, prefix).
mod_group(amulet, 1IncreasedEnergyShield, '# to maximum Energy Shield', [energy_shield], 10000, 80, 10, prefix).
mod_group(amulet, 1IncreasedPhysicalDamageReductionRatingPercent, '#% increased Armour', [armour], 7000, 75, 7, prefix).
mod_group(amulet, 1EvasionRatingPercent, '#% increased Evasion Rating', [evasion], 7000, 77, 7, prefix).
mod_group(amulet, 1EnergyShieldPercent, '#% increased maximum Energy Shield', [energy_shield], 7000, 75, 7, prefix).
mod_group(amulet, 1IncreasedAccuracy, '# to Accuracy Rating', [attack], 6000, 67, 8, prefix).
mod_group(amulet, 1ItemFoundRarityIncreasePrefix, '#% increased Rarity of Items found', [], 3000, 47, 3, prefix).
mod_group(amulet, 1BaseSpirit, '# to Spirit', [], 2400, 54, 5, prefix).
mod_group(amulet, 1SpellDamage, '#% increased Spell Damage', [damage, caster], 6000, 75, 6, prefix).

mod_group(amulet, 2Strength, '# to Strength', [attribute], 8000, 74, 8, suffix).
mod_group(amulet, 2Dexterity, '# to Dexterity', [attribute], 8000, 74, 8, suffix).
mod_group(amulet, 2Intelligence, '# to Intelligence', [attribute], 8000, 74, 8, suffix).
mod_group(amulet, 2AllAttributes, '# to all Attributes', [attribute], 7200, 82, 9, suffix).
mod_group(amulet, 2FireResistance, '#% to Fire Resistance', [elemental, fire, resistance], 8000, 82, 8, suffix).
mod_group(amulet, 2ColdResistance, '#% to Cold Resistance', [elemental, cold, resistance], 8000, 82, 8, suffix).
mod_group(amulet, 2LightningResistance, '#% to Lightning Resistance', [elemental, lightning, resistance], 8000, 82, 8, suffix).
mod_group(amulet, 2AllResistances, '#% to all Elemental Resistances', [elemental, fire, cold, lightning, resistance], 4800, 80, 6, suffix).
mod_group(amulet, 2ChaosResistance, '#% to Chaos Resistance', [chaos, resistance], 1500, 81, 6, suffix).
mod_group(amulet, 2IncreaseSocketedGemLevel, '# to Level of all Spell Skills', [caster, gem, minion, gem, attack], 3400, 75, 12, suffix).
mod_group(amulet, 2LifeRegeneration, '# Life Regeneration per second', [life], 10000, 75, 10, suffix).
mod_group(amulet, 2ManaRegeneration, '#% increased Mana Regeneration Rate', [mana], 6000, 79, 6, suffix).
mod_group(amulet, 2CriticalStrikeChanceIncrease, '#% increased Critical Hit Chance', [critical], 3875, 72, 6, suffix).
mod_group(amulet, 2CriticalStrikeMultiplier, '#% increased Critical Damage Bonus', [damage, critical], 3875, 74, 6, suffix).
mod_group(amulet, 2ItemFoundRarityIncrease, '#% increased Rarity of Items found', [], 3000, 40, 3, suffix).
mod_group(amulet, 2DamageTakenGainedAsLife, '#% of Damage taken Recouped as Life', [life], 2500, 79, 5, suffix).
mod_group(amulet, 2PercentDamageGoesToMana, '#% of Damage taken Recouped as Mana', [life, mana], 2500, 80, 5, suffix).
mod_group(amulet, 2IncreasedCastSpeed, '#% increased Cast Speed', [caster, speed], 6, 66, 6, suffix).
