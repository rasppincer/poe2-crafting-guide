%%% Mod data for fire_staff
%%% Source: POE2-PathOfCrafting (frankthetank001/POE2-PathOfCrafting)
%%% Original data: poe2db.tw via weights.csv
%%% Imported: 2026-06-09

%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)

mod_pool_weight_sum(fire_staff, prefix, 2700).
mod_pool_weight_sum(fire_staff, suffix, 6650).

mod_group(fire_staff, PercentIncreasedFireDamage, '#% increased Fire Damage', [fire, damage], 50, 100, 8, prefix).
mod_group(fire_staff, PercentIncreasedSpellDamage, '#% increased Spell Damage', [spell, damage], 50, 100, 8, prefix).
mod_group(fire_staff, PercentIncreasedSpellDamageFlattoMaximumMana, '#% increased Spell Damage, # to maximum Mana', [mana, spell, damage], 100, 100, 7, prefix).
mod_group(fire_staff, FlattoMaximumMana, '# to maximum Mana', [mana], 1000, 100, 11, prefix).
mod_group(fire_staff, GainPercentOfDamageAsExtraColdDamage, 'Gain #% of Damage as Extra Cold Damage', [cold, damage], 500, 100, 6, prefix).
mod_group(fire_staff, GainPercentOfDamageAsExtraFireDamage, 'Gain #% of Damage as Extra Fire Damage', [fire, damage], 500, 100, 6, prefix).
mod_group(fire_staff, GainPercentOfDamageAsExtraLightningDamage, 'Gain #% of Damage as Extra Lightning Damage', [lightning, damage], 500, 100, 6, prefix).
mod_group(fire_staff, PercentIncreasedCastSpeed, '#% increased Cast Speed', [speed], 250, 100, 7, suffix).
mod_group(fire_staff, PercentIncreasedFlammabilityMagnitude, '#% increased Flammability Magnitude', [], 500, 100, 5, suffix).
mod_group(fire_staff, PercentIncreasedCriticalHitChanceForSpells, '#% increased Critical Hit Chance for Spells', [critical, spell], 125, 100, 6, suffix).
mod_group(fire_staff, PercentIncreasedCriticalSpellDamageBonus, '#% increased Critical Spell Damage Bonus', [critical, spell, damage], 125, 100, 6, suffix).
mod_group(fire_staff, PercentIncreasedManaRegenerationRatePercentIncreasedLightRadius, '#% increased Mana Regeneration Rate, #% increased Light Radius', [mana], 1000, 100, 3, suffix).
mod_group(fire_staff, PercentIncreasedManaRegenerationRate, '#% increased Mana Regeneration Rate', [mana], 1000, 100, 6, suffix).
mod_group(fire_staff, PercentReducedAttributeRequirements, '#% reduced Attribute Requirements', [attribute], 1000, 100, 5, suffix).
mod_group(fire_staff, FlattoIntelligence, '# to Intelligence', [attribute], 1000, 100, 8, suffix).
mod_group(fire_staff, FlattoLevelOfAllFireSpellSkills, '# to Level of all Fire Spell Skills', [fire, spell], 100, 100, 5, suffix).
mod_group(fire_staff, FlattoLevelOfAllSpellSkills, '# to Level of all Spell Skills', [spell], 50, 100, 4, suffix).
mod_group(fire_staff, GainFlatLifePerEnemyKilled, 'Gain # Life per Enemy Killed', [life], 750, 100, 8, suffix).
mod_group(fire_staff, GainFlatManaPerEnemyKilled, 'Gain # Mana per Enemy Killed', [mana], 750, 100, 8, suffix).
