%%% Mod data for chaos_staff
%%% Source: POE2-PathOfCrafting (frankthetank001/POE2-PathOfCrafting)
%%% Original data: poe2db.tw via weights.csv
%%% Auto-imported by import_from_pathofcrafting.py

%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)

mod_pool_weight_sum(chaos_staff, prefix, 5000).
mod_pool_weight_sum(chaos_staff, suffix, 9700).

mod_group(chaos_staff, 'PercentIncreasedChaosDamage', '#% increased Chaos Damage', [chaos, damage], 500, 100, 8, prefix).
mod_group(chaos_staff, 'PercentIncreasedSpellDamage', '#% increased Spell Damage', [spell, damage], 1000, 100, 8, prefix).
mod_group(chaos_staff, 'PercentIncreasedSpellDamageFlattoMaximumMana', '#% increased Spell Damage, # to maximum Mana', [mana, spell, damage], 1000, 100, 7, prefix).
mod_group(chaos_staff, 'FlattoMaximumMana', '# to maximum Mana', [mana], 1000, 100, 11, prefix).
mod_group(chaos_staff, 'GainPercentOfDamageAsExtraColdDamage', 'Gain #% of Damage as Extra Cold Damage', [cold, damage], 500, 100, 6, prefix).
mod_group(chaos_staff, 'GainPercentOfDamageAsExtraFireDamage', 'Gain #% of Damage as Extra Fire Damage', [fire, damage], 500, 100, 6, prefix).
mod_group(chaos_staff, 'GainPercentOfDamageAsExtraLightningDamage', 'Gain #% of Damage as Extra Lightning Damage', [lightning, damage], 500, 100, 6, prefix).

mod_group(chaos_staff, 'PercentIncreasedCastSpeed', '#% increased Cast Speed', [caster, speed], 1000, 100, 7, suffix).
mod_group(chaos_staff, 'PercentIncreasedCriticalHitChanceForSpells', '#% increased Critical Hit Chance for Spells', [spell, critical], 1000, 100, 6, suffix).
mod_group(chaos_staff, 'PercentIncreasedCriticalSpellDamageBonus', '#% increased Critical Spell Damage Bonus', [spell, critical, damage], 1000, 100, 6, suffix).
mod_group(chaos_staff, 'PercentIncreasedManaRegenerationRatePercentIncreasedLightRadius', '#% increased Mana Regeneration Rate, #% increased Light Radius', [mana, regeneration], 1000, 100, 3, suffix).
mod_group(chaos_staff, 'PercentIncreasedManaRegenerationRate', '#% increased Mana Regeneration Rate', [mana, regeneration], 1000, 100, 6, suffix).
mod_group(chaos_staff, 'PercentReducedAttributeRequirements', '#% reduced Attribute Requirements', [], 1000, 100, 5, suffix).
mod_group(chaos_staff, 'FlattoIntelligence', '# to Intelligence', [attribute], 1000, 100, 8, suffix).
mod_group(chaos_staff, 'FlattoLevelOfAllChaosSpellSkills', '# to Level of all Chaos Spell Skills', [chaos, spell], 1000, 100, 5, suffix).
mod_group(chaos_staff, 'FlattoLevelOfAllSpellSkills', '# to Level of all Spell Skills', [spell], 200, 100, 4, suffix).
mod_group(chaos_staff, 'GainFlatLifePerEnemyKilled', 'Gain # Life per Enemy Killed', [life], 750, 100, 8, suffix).
mod_group(chaos_staff, 'GainFlatManaPerEnemyKilled', 'Gain # Mana per Enemy Killed', [mana], 750, 100, 8, suffix).

