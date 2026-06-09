%%% Mod data for amulet
%%% Source: POE2-PathOfCrafting (frankthetank001/POE2-PathOfCrafting)
%%% Original data: poe2db.tw via weights.csv
%%% Imported: 2026-06-09

%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)

mod_pool_weight_sum(amulet, prefix, 9400).
mod_pool_weight_sum(amulet, suffix, 13300).

mod_group(amulet, PercentIncreasedArmour, '#% increased Armour', [armour], 1000, 100, 7, prefix).
mod_group(amulet, PercentIncreasedEvasionRating, '#% increased Evasion Rating', [evasion], 1000, 100, 7, prefix).
mod_group(amulet, PercentIncreasedMaximumEnergyShield, '#% increased maximum Energy Shield', [energy_shield], 1000, 100, 7, prefix).
mod_group(amulet, PercentIncreasedMaximumLife, '#% increased maximum Life', [life], 300, 100, 3, prefix).
mod_group(amulet, PercentIncreasedMaximumMana, '#% increased maximum Mana', [mana], 300, 100, 3, prefix).
mod_group(amulet, PercentIncreasedRarityOfItemsFound, '#% increased Rarity of Items found', [], 1000, 100, 3, prefix).
mod_group(amulet, PercentIncreasedSpellDamage, '#% increased Spell Damage', [spell, damage], 1000, 100, 6, prefix).
mod_group(amulet, FlattoAccuracyRating, '# to Accuracy Rating', [accuracy], 400, 100, 8, prefix).
mod_group(amulet, FlattoMaximumEnergyShield, '# to maximum Energy Shield', [energy_shield], 1000, 100, 10, prefix).
mod_group(amulet, FlattoMaximumLife, '# to maximum Life', [life], 1000, 100, 9, prefix).
mod_group(amulet, FlattoMaximumMana, '# to maximum Mana', [mana], 1000, 100, 13, prefix).
mod_group(amulet, FlattoSpirit, '# to Spirit', [spirit], 400, 100, 5, prefix).
mod_group(amulet, FlatLifeRegenerationPerSecond, '# Life Regeneration per second', [life], 1000, 100, 10, suffix).
mod_group(amulet, PercentIncreasedCastSpeed, '#% increased Cast Speed', [speed], 800, 100, 5, suffix).
mod_group(amulet, PercentIncreasedCriticalDamageBonus, '#% increased Critical Damage Bonus', [critical, damage], 125, 100, 6, suffix).
mod_group(amulet, PercentIncreasedCriticalHitChance, '#% increased Critical Hit Chance', [critical], 125, 100, 6, suffix).
mod_group(amulet, PercentIncreasedManaRegenerationRate, '#% increased Mana Regeneration Rate', [mana], 1000, 100, 6, suffix).
mod_group(amulet, PercentIncreasedRarityOfItemsFound, '#% increased Rarity of Items found', [], 1000, 100, 3, suffix).
mod_group(amulet, PercentOfDamageTakenRecoupedAsLife, '#% of Damage taken Recouped as Life', [life, damage], 500, 100, 5, suffix).
mod_group(amulet, PercentOfDamageTakenRecoupedAsMana, '#% of Damage taken Recouped as Mana', [mana, damage], 500, 100, 5, suffix).
mod_group(amulet, FlattoAllAttributes, '# to all Attributes', [attribute], 800, 100, 9, suffix).
mod_group(amulet, FlattoDexterity, '# to Dexterity', [attribute], 1000, 100, 8, suffix).
mod_group(amulet, FlattoIntelligence, '# to Intelligence', [attribute], 1000, 100, 8, suffix).
mod_group(amulet, FlattoLevelOfAllMeleeSkills, '# to Level of all Melee Skills', [], 100, 100, 3, suffix).
mod_group(amulet, FlattoLevelOfAllMinionSkills, '# to Level of all Minion Skills', [], 100, 100, 3, suffix).
mod_group(amulet, FlattoLevelOfAllProjectileSkills, '# to Level of all Projectile Skills', [], 100, 100, 3, suffix).
mod_group(amulet, FlattoLevelOfAllSpellSkills, '# to Level of all Spell Skills', [spell], 100, 100, 3, suffix).
mod_group(amulet, FlattoStrength, '# to Strength', [attribute], 1000, 100, 8, suffix).
mod_group(amulet, PercentToAllElementalResistances, '#% to all Elemental Resistances', [resistance], 800, 100, 6, suffix).
mod_group(amulet, PercentToChaosResistance, '#% to Chaos Resistance', [chaos, resistance], 250, 100, 6, suffix).
mod_group(amulet, PercentToColdResistance, '#% to Cold Resistance', [cold, resistance], 1000, 100, 8, suffix).
mod_group(amulet, PercentToFireResistance, '#% to Fire Resistance', [fire, resistance], 1000, 100, 8, suffix).
mod_group(amulet, PercentToLightningResistance, '#% to Lightning Resistance', [lightning, resistance], 1000, 100, 8, suffix).
