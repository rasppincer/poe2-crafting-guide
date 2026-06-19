%%% Mod data for focus
%%% Source: POE2-PathOfCrafting (frankthetank001/POE2-PathOfCrafting)
%%% Original data: poe2db.tw via weights.csv
%%% Auto-imported by import_from_pathofcrafting.py

%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)

mod_pool_weight_sum(focus, prefix, 7500).
mod_pool_weight_sum(focus, suffix, 11550).

mod_group(focus, 'PercentIncreasedChaosDamage', '#% increased Chaos Damage', [chaos, damage], 500, 100, 6, prefix).
mod_group(focus, 'PercentIncreasedColdDamage', '#% increased Cold Damage', [cold, damage], 500, 100, 6, prefix).
mod_group(focus, 'PercentIncreasedEnergyShield', '#% increased Energy Shield', [energy_shield], 1000, 100, 7, prefix).
mod_group(focus, 'PercentIncreasedEnergyShieldFlattoMaximumMana', '#% increased Energy Shield, # to maximum Mana', [mana, energy_shield], 1000, 100, 6, prefix).
mod_group(focus, 'PercentIncreasedFireDamage', '#% increased Fire Damage', [fire, damage], 500, 100, 6, prefix).
mod_group(focus, 'PercentIncreasedLightningDamage', '#% increased Lightning Damage', [lightning, damage], 500, 100, 6, prefix).
mod_group(focus, 'PercentIncreasedSpellDamage', '#% increased Spell Damage', [spell, damage], 1000, 100, 6, prefix).
mod_group(focus, 'PercentIncreasedSpellPhysicalDamage', '#% increased Spell Physical Damage', [physical, spell, damage], 500, 100, 6, prefix).
mod_group(focus, 'FlattoMaximumEnergyShield', '# to maximum Energy Shield', [energy_shield], 1000, 100, 10, prefix).
mod_group(focus, 'FlattoMaximumMana', '# to maximum Mana', [mana], 1000, 100, 11, prefix).

mod_group(focus, 'PercentIncreasedCastSpeed', '#% increased Cast Speed', [caster, speed], 1000, 100, 6, suffix).
mod_group(focus, 'PercentIncreasedCriticalHitChanceForSpells', '#% increased Critical Hit Chance for Spells', [spell, critical], 1000, 100, 5, suffix).
mod_group(focus, 'PercentIncreasedCriticalSpellDamageBonus', '#% increased Critical Spell Damage Bonus', [spell, critical, damage], 1000, 100, 5, suffix).
mod_group(focus, 'PercentIncreasedEnergyShieldRechargeRate', '#% increased Energy Shield Recharge Rate', [energy_shield], 1000, 100, 6, suffix).
mod_group(focus, 'PercentIncreasedManaRegenerationRate', '#% increased Mana Regeneration Rate', [mana, regeneration], 1000, 100, 6, suffix).
mod_group(focus, 'PercentReducedAttributeRequirements', '#% reduced Attribute Requirements', [], 800, 100, 5, suffix).
mod_group(focus, 'FlattoIntelligence', '# to Intelligence', [attribute], 1000, 100, 8, suffix).
mod_group(focus, 'FlattoLevelOfAllSpellSkills', '# to Level of all Spell Skills', [spell], 500, 100, 2, suffix).
mod_group(focus, 'PercentToChaosResistance', '#% to Chaos Resistance', [chaos, resistance], 250, 100, 6, suffix).
mod_group(focus, 'PercentToColdResistance', '#% to Cold Resistance', [cold, resistance], 1000, 100, 8, suffix).
mod_group(focus, 'PercentToFireResistance', '#% to Fire Resistance', [fire, resistance], 1000, 100, 8, suffix).
mod_group(focus, 'PercentToLightningResistance', '#% to Lightning Resistance', [lightning, resistance], 1000, 100, 8, suffix).
mod_group(focus, 'PercentFasterStartOfEnergyShieldRecharge', '#% faster start of Energy Shield Recharge', [energy_shield], 1000, 100, 6, suffix).

