%%% Mod data for physical_wand
%%% Source: POE2-PathOfCrafting (frankthetank001/POE2-PathOfCrafting)
%%% Original data: poe2db.tw via weights.csv
%%% Imported: 2026-06-09

%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)

mod_pool_weight_sum(physical_wand, prefix, 2700).
mod_pool_weight_sum(physical_wand, suffix, 6150).

mod_group(physical_wand, PercentIncreasedSpellPhysicalDamage, '#% increased Spell Physical Damage', [physical, spell, damage], 50, 100, 8, prefix).
mod_group(physical_wand, PercentIncreasedSpellDamage, '#% increased Spell Damage', [spell, damage], 50, 100, 8, prefix).
mod_group(physical_wand, PercentIncreasedSpellDamageFlattoMaximumMana, '#% increased Spell Damage, # to maximum Mana', [mana, spell, damage], 100, 100, 7, prefix).
mod_group(physical_wand, FlattoMaximumMana, '# to maximum Mana', [mana], 1000, 100, 11, prefix).
mod_group(physical_wand, GainPercentOfDamageAsExtraColdDamage, 'Gain #% of Damage as Extra Cold Damage', [cold, damage], 500, 100, 6, prefix).
mod_group(physical_wand, GainPercentOfDamageAsExtraFireDamage, 'Gain #% of Damage as Extra Fire Damage', [fire, damage], 500, 100, 6, prefix).
mod_group(physical_wand, GainPercentOfDamageAsExtraLightningDamage, 'Gain #% of Damage as Extra Lightning Damage', [lightning, damage], 500, 100, 6, prefix).
mod_group(physical_wand, PercentIncreasedCastSpeed, '#% increased Cast Speed', [speed], 250, 100, 7, suffix).
mod_group(physical_wand, PercentIncreasedCriticalHitChanceForSpells, '#% increased Critical Hit Chance for Spells', [critical, spell], 125, 100, 6, suffix).
mod_group(physical_wand, PercentIncreasedCriticalSpellDamageBonus, '#% increased Critical Spell Damage Bonus', [critical, spell, damage], 125, 100, 6, suffix).
mod_group(physical_wand, PercentIncreasedManaRegenerationRatePercentIncreasedLightRadius, '#% increased Mana Regeneration Rate, #% increased Light Radius', [mana], 1000, 100, 3, suffix).
mod_group(physical_wand, PercentIncreasedManaRegenerationRate, '#% increased Mana Regeneration Rate', [mana], 1000, 100, 6, suffix).
mod_group(physical_wand, PercentReducedAttributeRequirements, '#% reduced Attribute Requirements', [attribute], 1000, 100, 5, suffix).
mod_group(physical_wand, FlattoIntelligence, '# to Intelligence', [attribute], 1000, 100, 8, suffix).
mod_group(physical_wand, FlattoLevelOfAllPhysicalSpellSkills, '# to Level of all Physical Spell Skills', [physical, spell], 100, 100, 5, suffix).
mod_group(physical_wand, FlattoLevelOfAllSpellSkills, '# to Level of all Spell Skills', [spell], 50, 100, 4, suffix).
mod_group(physical_wand, GainFlatLifePerEnemyKilled, 'Gain # Life per Enemy Killed', [life], 750, 100, 8, suffix).
mod_group(physical_wand, GainFlatManaPerEnemyKilled, 'Gain # Mana per Enemy Killed', [mana], 750, 100, 8, suffix).
