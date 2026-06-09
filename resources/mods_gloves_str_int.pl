%%% Mod data for gloves_str_int
%%% Source: POE2-PathOfCrafting (frankthetank001/POE2-PathOfCrafting)
%%% Original data: poe2db.tw via weights.csv
%%% Imported: 2026-06-09

%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)

mod_pool_weight_sum(gloves_str_int, prefix, 6200).
mod_pool_weight_sum(gloves_str_int, suffix, 13450).

mod_group(gloves_str_int, PercentIncreasedArmourAndEnergyShield, '#% increased Armour and Energy Shield', [armour, energy_shield], 1000, 100, 7, prefix).
mod_group(gloves_str_int, PercentIncreasedArmourAndEnergyShieldFlattoMaximumLife, '#% increased Armour and Energy Shield, # to maximum Life', [life, armour, energy_shield], 1000, 100, 6, prefix).
mod_group(gloves_str_int, FlattoAccuracyRating, '# to Accuracy Rating', [accuracy], 200, 100, 9, prefix).
mod_group(gloves_str_int, FlattoArmourFlattoMaximumEnergyShield, '# to Armour, # to maximum Energy Shield', [armour, energy_shield], 1000, 100, 4, prefix).
mod_group(gloves_str_int, FlattoMaximumLife, '# to maximum Life', [life], 1000, 100, 9, prefix).
mod_group(gloves_str_int, FlattoMaximumMana, '# to maximum Mana', [mana], 1000, 100, 9, prefix).
mod_group(gloves_str_int, AddsFlattoFlatColdDamageToAttacks, 'Adds # to # Cold damage to Attacks', [cold, attack, damage], 200, 100, 9, prefix).
mod_group(gloves_str_int, AddsFlattoFlatFireDamageToAttacks, 'Adds # to # Fire damage to Attacks', [fire, attack, damage], 200, 100, 9, prefix).
mod_group(gloves_str_int, AddsFlattoFlatLightningDamageToAttacks, 'Adds # to # Lightning damage to Attacks', [lightning, attack, damage], 200, 100, 9, prefix).
mod_group(gloves_str_int, AddsFlattoFlatPhysicalDamageToAttacks, 'Adds # to # Physical Damage to Attacks', [physical, attack, damage], 400, 100, 9, prefix).
mod_group(gloves_str_int, PercentIncreasedAttackSpeed, '#% increased Attack Speed', [attack, speed], 500, 100, 4, suffix).
mod_group(gloves_str_int, PercentIncreasedCriticalDamageBonus, '#% increased Critical Damage Bonus', [critical, damage], 250, 100, 5, suffix).
mod_group(gloves_str_int, PercentIncreasedRarityOfItemsFound, '#% increased Rarity of Items found', [], 1000, 100, 3, suffix).
mod_group(gloves_str_int, PercentReducedAttributeRequirements, '#% reduced Attribute Requirements', [attribute], 700, 100, 5, suffix).
mod_group(gloves_str_int, FlattoDexterity, '# to Dexterity', [attribute], 1000, 100, 9, suffix).
mod_group(gloves_str_int, FlattoIntelligence, '# to Intelligence', [attribute], 500, 100, 8, suffix).
mod_group(gloves_str_int, FlattoLevelOfAllMeleeSkills, '# to Level of all Melee Skills', [], 250, 100, 2, suffix).
mod_group(gloves_str_int, FlattoStrength, '# to Strength', [attribute], 500, 100, 8, suffix).
mod_group(gloves_str_int, PercentToChaosResistance, '#% to Chaos Resistance', [chaos, resistance], 250, 100, 6, suffix).
mod_group(gloves_str_int, PercentToColdResistance, '#% to Cold Resistance', [cold, resistance], 1000, 100, 8, suffix).
mod_group(gloves_str_int, PercentToFireResistance, '#% to Fire Resistance', [fire, resistance], 1000, 100, 8, suffix).
mod_group(gloves_str_int, PercentToLightningResistance, '#% to Lightning Resistance', [lightning, resistance], 1000, 100, 8, suffix).
mod_group(gloves_str_int, GainFlatLifePerEnemyHitWithAttacks, 'Gain # Life per Enemy Hit with Attacks', [life, attack], 1000, 100, 4, suffix).
mod_group(gloves_str_int, GainFlatLifePerEnemyKilled, 'Gain # Life per Enemy Killed', [life], 750, 100, 8, suffix).
mod_group(gloves_str_int, GainFlatManaPerEnemyKilled, 'Gain # Mana per Enemy Killed', [mana], 750, 100, 8, suffix).
mod_group(gloves_str_int, LeechPercentOfPhysicalAttackDamageAsLife, 'Leech #% of Physical Attack Damage as Life', [life, physical, attack, damage], 1000, 100, 5, suffix).
mod_group(gloves_str_int, LeechPercentOfPhysicalAttackDamageAsMana, 'Leech #% of Physical Attack Damage as Mana', [mana, physical, attack, damage], 1000, 100, 5, suffix).
mod_group(gloves_str_int, PercentIncreasedEnergyShieldRechargeRate, '#% increased Energy Shield Recharge Rate', [energy_shield], 500, 100, 4, suffix).
mod_group(gloves_str_int, PercentOfArmourAlsoAppliesToElementalDamage, '#% of Armour also applies to Elemental Damage', [armour, damage], 500, 100, 5, suffix).
