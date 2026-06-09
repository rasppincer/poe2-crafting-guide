%%% Mod data for gloves_str
%%% Source: POE2-PathOfCrafting (frankthetank001/POE2-PathOfCrafting)
%%% Original data: poe2db.tw via weights.csv
%%% Imported: 2026-06-09

%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)

mod_pool_weight_sum(gloves_str, prefix, 6200).
mod_pool_weight_sum(gloves_str, suffix, 13450).

mod_group(gloves_str, PercentIncreasedArmour, '#% increased Armour', [armour], 1000, 100, 7, prefix).
mod_group(gloves_str, PercentIncreasedArmourFlattoMaximumLife, '#% increased Armour, # to maximum Life', [life, armour], 1000, 100, 6, prefix).
mod_group(gloves_str, FlattoAccuracyRating, '# to Accuracy Rating', [accuracy], 200, 100, 9, prefix).
mod_group(gloves_str, FlattoArmour, '# to Armour', [armour], 1000, 100, 7, prefix).
mod_group(gloves_str, FlattoMaximumLife, '# to maximum Life', [life], 1000, 100, 9, prefix).
mod_group(gloves_str, FlattoMaximumMana, '# to maximum Mana', [mana], 1000, 100, 9, prefix).
mod_group(gloves_str, AddsFlattoFlatColdDamageToAttacks, 'Adds # to # Cold damage to Attacks', [cold, attack, damage], 200, 100, 9, prefix).
mod_group(gloves_str, AddsFlattoFlatFireDamageToAttacks, 'Adds # to # Fire damage to Attacks', [fire, attack, damage], 200, 100, 9, prefix).
mod_group(gloves_str, AddsFlattoFlatLightningDamageToAttacks, 'Adds # to # Lightning damage to Attacks', [lightning, attack, damage], 200, 100, 9, prefix).
mod_group(gloves_str, AddsFlattoFlatPhysicalDamageToAttacks, 'Adds # to # Physical Damage to Attacks', [physical, attack, damage], 400, 100, 9, prefix).
mod_group(gloves_str, PercentIncreasedAttackSpeed, '#% increased Attack Speed', [attack, speed], 500, 100, 4, suffix).
mod_group(gloves_str, PercentIncreasedCriticalDamageBonus, '#% increased Critical Damage Bonus', [critical, damage], 250, 100, 5, suffix).
mod_group(gloves_str, PercentIncreasedRarityOfItemsFound, '#% increased Rarity of Items found', [], 1000, 100, 3, suffix).
mod_group(gloves_str, PercentReducedAttributeRequirements, '#% reduced Attribute Requirements', [attribute], 700, 100, 5, suffix).
mod_group(gloves_str, FlattoDexterity, '# to Dexterity', [attribute], 1000, 100, 9, suffix).
mod_group(gloves_str, FlattoLevelOfAllMeleeSkills, '# to Level of all Melee Skills', [], 250, 100, 2, suffix).
mod_group(gloves_str, FlattoStrength, '# to Strength', [attribute], 1000, 100, 8, suffix).
mod_group(gloves_str, PercentToChaosResistance, '#% to Chaos Resistance', [chaos, resistance], 250, 100, 6, suffix).
mod_group(gloves_str, PercentToColdResistance, '#% to Cold Resistance', [cold, resistance], 1000, 100, 8, suffix).
mod_group(gloves_str, PercentToFireResistance, '#% to Fire Resistance', [fire, resistance], 1000, 100, 8, suffix).
mod_group(gloves_str, PercentToLightningResistance, '#% to Lightning Resistance', [lightning, resistance], 1000, 100, 8, suffix).
mod_group(gloves_str, GainFlatLifePerEnemyHitWithAttacks, 'Gain # Life per Enemy Hit with Attacks', [life, attack], 1000, 100, 4, suffix).
mod_group(gloves_str, GainFlatLifePerEnemyKilled, 'Gain # Life per Enemy Killed', [life], 750, 100, 8, suffix).
mod_group(gloves_str, GainFlatManaPerEnemyKilled, 'Gain # Mana per Enemy Killed', [mana], 750, 100, 8, suffix).
mod_group(gloves_str, LeechPercentOfPhysicalAttackDamageAsLife, 'Leech #% of Physical Attack Damage as Life', [life, physical, attack, damage], 1000, 100, 5, suffix).
mod_group(gloves_str, LeechPercentOfPhysicalAttackDamageAsMana, 'Leech #% of Physical Attack Damage as Mana', [mana, physical, attack, damage], 1000, 100, 5, suffix).
mod_group(gloves_str, PercentOfArmourAlsoAppliesToElementalDamage, '#% of Armour also applies to Elemental Damage', [armour, damage], 1000, 100, 5, suffix).
