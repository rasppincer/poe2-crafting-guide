%%% Mod data for staff
%%% Source: POE2-PathOfCrafting (frankthetank001/POE2-PathOfCrafting)
%%% Original data: poe2db.tw via weights.csv
%%% Auto-imported by import_from_pathofcrafting.py

%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)

mod_pool_weight_sum(staff, prefix, 7000).
mod_pool_weight_sum(staff, suffix, 16700).

mod_group(staff, 'PercentIncreasedChaosDamage', '#% increased Chaos Damage', [chaos, damage], 500, 100, 8, prefix).
mod_group(staff, 'PercentIncreasedColdDamage', '#% increased Cold Damage', [cold, damage], 500, 100, 8, prefix).
mod_group(staff, 'PercentIncreasedFireDamage', '#% increased Fire Damage', [fire, damage], 500, 100, 8, prefix).
mod_group(staff, 'PercentIncreasedLightningDamage', '#% increased Lightning Damage', [lightning, damage], 500, 100, 8, prefix).
mod_group(staff, 'PercentIncreasedSpellDamage', '#% increased Spell Damage', [spell, damage], 1000, 100, 8, prefix).
mod_group(staff, 'PercentIncreasedSpellDamageFlattoMaximumMana', '#% increased Spell Damage, # to maximum Mana', [mana, spell, damage], 1000, 100, 7, prefix).
mod_group(staff, 'PercentIncreasedSpellPhysicalDamage', '#% increased Spell Physical Damage', [physical, spell, damage], 500, 100, 8, prefix).
mod_group(staff, 'FlattoMaximumMana', '# to maximum Mana', [mana], 1000, 100, 11, prefix).
mod_group(staff, 'GainPercentOfDamageAsExtraColdDamage', 'Gain #% of Damage as Extra Cold Damage', [cold, damage], 500, 100, 6, prefix).
mod_group(staff, 'GainPercentOfDamageAsExtraFireDamage', 'Gain #% of Damage as Extra Fire Damage', [fire, damage], 500, 100, 6, prefix).
mod_group(staff, 'GainPercentOfDamageAsExtraLightningDamage', 'Gain #% of Damage as Extra Lightning Damage', [lightning, damage], 500, 100, 6, prefix).

mod_group(staff, 'PercentIncreasedCastSpeed', '#% increased Cast Speed', [caster, speed], 1000, 100, 7, suffix).
mod_group(staff, 'PercentIncreasedFlammabilityMagnitude', '#% increased Flammability Magnitude', [], 1000, 100, 5, suffix).
mod_group(staff, 'PercentIncreasedChanceToShock', '#% increased chance to Shock', [lightning], 1000, 100, 5, suffix).
mod_group(staff, 'PercentIncreasedCriticalHitChanceForSpells', '#% increased Critical Hit Chance for Spells', [spell, critical], 1000, 100, 6, suffix).
mod_group(staff, 'PercentIncreasedCriticalSpellDamageBonus', '#% increased Critical Spell Damage Bonus', [spell, critical, damage], 1000, 100, 6, suffix).
mod_group(staff, 'PercentIncreasedFreezeBuildup', '#% increased Freeze Buildup', [cold], 1000, 100, 5, suffix).
mod_group(staff, 'PercentIncreasedManaRegenerationRatePercentIncreasedLightRadius', '#% increased Mana Regeneration Rate, #% increased Light Radius', [mana, regeneration], 1000, 100, 3, suffix).
mod_group(staff, 'PercentIncreasedManaRegenerationRate', '#% increased Mana Regeneration Rate', [mana, regeneration], 1000, 100, 6, suffix).
mod_group(staff, 'PercentReducedAttributeRequirements', '#% reduced Attribute Requirements', [], 1000, 100, 5, suffix).
mod_group(staff, 'FlattoIntelligence', '# to Intelligence', [attribute], 1000, 100, 8, suffix).
mod_group(staff, 'FlattoLevelOfAllChaosSpellSkills', '# to Level of all Chaos Spell Skills', [chaos, spell], 1000, 100, 5, suffix).
mod_group(staff, 'FlattoLevelOfAllColdSpellSkills', '# to Level of all Cold Spell Skills', [cold, spell], 1000, 100, 5, suffix).
mod_group(staff, 'FlattoLevelOfAllFireSpellSkills', '# to Level of all Fire Spell Skills', [fire, spell], 1000, 100, 5, suffix).
mod_group(staff, 'FlattoLevelOfAllLightningSpellSkills', '# to Level of all Lightning Spell Skills', [lightning, spell], 1000, 100, 5, suffix).
mod_group(staff, 'FlattoLevelOfAllPhysicalSpellSkills', '# to Level of all Physical Spell Skills', [physical, spell], 1000, 100, 5, suffix).
mod_group(staff, 'FlattoLevelOfAllSpellSkills', '# to Level of all Spell Skills', [spell], 200, 100, 4, suffix).
mod_group(staff, 'GainFlatLifePerEnemyKilled', 'Gain # Life per Enemy Killed', [life], 750, 100, 8, suffix).
mod_group(staff, 'GainFlatManaPerEnemyKilled', 'Gain # Mana per Enemy Killed', [mana], 750, 100, 8, suffix).

