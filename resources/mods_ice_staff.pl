%%% Mod data for ice_staff
%%% Source: POE2-PathOfCrafting (frankthetank001/POE2-PathOfCrafting)
%%% Original data: poe2db.tw via weights.csv
%%% Imported: 2026-06-09

%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)

mod_pool_weight_sum(ice_staff, prefix, 2700).
mod_pool_weight_sum(ice_staff, suffix, 6650).

mod_group(ice_staff, PercentIncreasedColdDamage, '#% increased Cold Damage', [cold, damage], 50, 100, 8, prefix).
mod_group(ice_staff, PercentIncreasedSpellDamage, '#% increased Spell Damage', [spell, damage], 50, 100, 8, prefix).
mod_group(ice_staff, PercentIncreasedSpellDamageFlattoMaximumMana, '#% increased Spell Damage, # to maximum Mana', [mana, spell, damage], 100, 100, 7, prefix).
mod_group(ice_staff, FlattoMaximumMana, '# to maximum Mana', [mana], 1000, 100, 11, prefix).
mod_group(ice_staff, GainPercentOfDamageAsExtraColdDamage, 'Gain #% of Damage as Extra Cold Damage', [cold, damage], 500, 100, 6, prefix).
mod_group(ice_staff, GainPercentOfDamageAsExtraFireDamage, 'Gain #% of Damage as Extra Fire Damage', [fire, damage], 500, 100, 6, prefix).
mod_group(ice_staff, GainPercentOfDamageAsExtraLightningDamage, 'Gain #% of Damage as Extra Lightning Damage', [lightning, damage], 500, 100, 6, prefix).
mod_group(ice_staff, PercentIncreasedCastSpeed, '#% increased Cast Speed', [speed], 250, 100, 7, suffix).
mod_group(ice_staff, PercentIncreasedFreezeBuildup, '#% increased Freeze Buildup', [], 500, 100, 5, suffix).
mod_group(ice_staff, PercentIncreasedCriticalHitChanceForSpells, '#% increased Critical Hit Chance for Spells', [critical, spell], 125, 100, 6, suffix).
mod_group(ice_staff, PercentIncreasedCriticalSpellDamageBonus, '#% increased Critical Spell Damage Bonus', [critical, spell, damage], 125, 100, 6, suffix).
mod_group(ice_staff, PercentIncreasedManaRegenerationRatePercentIncreasedLightRadius, '#% increased Mana Regeneration Rate, #% increased Light Radius', [mana], 1000, 100, 3, suffix).
mod_group(ice_staff, PercentIncreasedManaRegenerationRate, '#% increased Mana Regeneration Rate', [mana], 1000, 100, 6, suffix).
mod_group(ice_staff, PercentReducedAttributeRequirements, '#% reduced Attribute Requirements', [attribute], 1000, 100, 5, suffix).
mod_group(ice_staff, FlattoIntelligence, '# to Intelligence', [attribute], 1000, 100, 8, suffix).
mod_group(ice_staff, FlattoLevelOfAllColdSpellSkills, '# to Level of all Cold Spell Skills', [cold, spell], 100, 100, 5, suffix).
mod_group(ice_staff, FlattoLevelOfAllSpellSkills, '# to Level of all Spell Skills', [spell], 50, 100, 4, suffix).
mod_group(ice_staff, GainFlatLifePerEnemyKilled, 'Gain # Life per Enemy Killed', [life], 750, 100, 8, suffix).
mod_group(ice_staff, GainFlatManaPerEnemyKilled, 'Gain # Mana per Enemy Killed', [mana], 750, 100, 8, suffix).
