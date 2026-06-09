%%% Mod data for lightning_wand
%%% Source: POE2-PathOfCrafting (frankthetank001/POE2-PathOfCrafting)
%%% Original data: poe2db.tw via weights.csv
%%% Imported: 2026-06-09

%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)

mod_pool_weight_sum(lightning_wand, prefix, 2700).
mod_pool_weight_sum(lightning_wand, suffix, 6650).

mod_group(lightning_wand, PercentIncreasedLightningDamage, '#% increased Lightning Damage', [lightning, damage], 50, 100, 8, prefix).
mod_group(lightning_wand, PercentIncreasedSpellDamage, '#% increased Spell Damage', [spell, damage], 50, 100, 8, prefix).
mod_group(lightning_wand, PercentIncreasedSpellDamageFlattoMaximumMana, '#% increased Spell Damage, # to maximum Mana', [mana, spell, damage], 100, 100, 7, prefix).
mod_group(lightning_wand, FlattoMaximumMana, '# to maximum Mana', [mana], 1000, 100, 11, prefix).
mod_group(lightning_wand, GainPercentOfDamageAsExtraColdDamage, 'Gain #% of Damage as Extra Cold Damage', [cold, damage], 500, 100, 6, prefix).
mod_group(lightning_wand, GainPercentOfDamageAsExtraFireDamage, 'Gain #% of Damage as Extra Fire Damage', [fire, damage], 500, 100, 6, prefix).
mod_group(lightning_wand, GainPercentOfDamageAsExtraLightningDamage, 'Gain #% of Damage as Extra Lightning Damage', [lightning, damage], 500, 100, 6, prefix).
mod_group(lightning_wand, PercentIncreasedCastSpeed, '#% increased Cast Speed', [speed], 250, 100, 7, suffix).
mod_group(lightning_wand, PercentIncreasedChanceToShock, '#% increased chance to Shock', [], 500, 100, 5, suffix).
mod_group(lightning_wand, PercentIncreasedCriticalHitChanceForSpells, '#% increased Critical Hit Chance for Spells', [critical, spell], 125, 100, 6, suffix).
mod_group(lightning_wand, PercentIncreasedCriticalSpellDamageBonus, '#% increased Critical Spell Damage Bonus', [critical, spell, damage], 125, 100, 6, suffix).
mod_group(lightning_wand, PercentIncreasedManaRegenerationRatePercentIncreasedLightRadius, '#% increased Mana Regeneration Rate, #% increased Light Radius', [mana], 1000, 100, 3, suffix).
mod_group(lightning_wand, PercentIncreasedManaRegenerationRate, '#% increased Mana Regeneration Rate', [mana], 1000, 100, 6, suffix).
mod_group(lightning_wand, PercentReducedAttributeRequirements, '#% reduced Attribute Requirements', [attribute], 1000, 100, 5, suffix).
mod_group(lightning_wand, FlattoIntelligence, '# to Intelligence', [attribute], 1000, 100, 8, suffix).
mod_group(lightning_wand, FlattoLevelOfAllLightningSpellSkills, '# to Level of all Lightning Spell Skills', [lightning, spell], 100, 100, 5, suffix).
mod_group(lightning_wand, FlattoLevelOfAllSpellSkills, '# to Level of all Spell Skills', [spell], 50, 100, 4, suffix).
mod_group(lightning_wand, GainFlatLifePerEnemyKilled, 'Gain # Life per Enemy Killed', [life], 750, 100, 8, suffix).
mod_group(lightning_wand, GainFlatManaPerEnemyKilled, 'Gain # Mana per Enemy Killed', [mana], 750, 100, 8, suffix).
