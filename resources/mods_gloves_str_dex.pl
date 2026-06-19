%%% Mod data for gloves_str_dex
%%% Source: POE2-PathOfCrafting (frankthetank001/POE2-PathOfCrafting)
%%% Original data: poe2db.tw via weights.csv
%%% Auto-imported by import_from_pathofcrafting.py

%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)

mod_pool_weight_sum(gloves_str_dex, prefix, 8300).
mod_pool_weight_sum(gloves_str_dex, suffix, 13950).

mod_group(gloves_str_dex, 'PercentIncreasedArmourAndEvasion', '#% increased Armour and Evasion', [armour, evasion], 1000, 100, 7, prefix).
mod_group(gloves_str_dex, 'PercentIncreasedArmourAndEvasionFlattoMaximumLife', '#% increased Armour and Evasion, # to maximum Life', [life, armour, evasion], 1000, 100, 6, prefix).
mod_group(gloves_str_dex, 'FlattoAccuracyRating', '# to Accuracy Rating', [accuracy], 800, 100, 9, prefix).
mod_group(gloves_str_dex, 'FlattoArmourFlattoEvasionRating', '# to Armour, # to Evasion Rating', [armour, evasion], 1000, 100, 4, prefix).
mod_group(gloves_str_dex, 'FlattoMaximumLife', '# to maximum Life', [life], 1000, 100, 9, prefix).
mod_group(gloves_str_dex, 'FlattoMaximumMana', '# to maximum Mana', [mana], 1000, 100, 9, prefix).
mod_group(gloves_str_dex, 'AddsFlattoflatColdDamageToAttacks', 'Adds # to # Cold damage to Attacks', [cold, attack, damage], 500, 100, 9, prefix).
mod_group(gloves_str_dex, 'AddsFlattoflatFireDamageToAttacks', 'Adds # to # Fire damage to Attacks', [fire, attack, damage], 500, 100, 9, prefix).
mod_group(gloves_str_dex, 'AddsFlattoflatLightningDamageToAttacks', 'Adds # to # Lightning damage to Attacks', [lightning, attack, damage], 500, 100, 9, prefix).
mod_group(gloves_str_dex, 'AddsFlattoflatPhysicalDamageToAttacks', 'Adds # to # Physical Damage to Attacks', [physical, attack, damage], 1000, 100, 9, prefix).

mod_group(gloves_str_dex, 'PercentIncreasedAttackSpeed', '#% increased Attack Speed', [attack, speed], 500, 100, 4, suffix).
mod_group(gloves_str_dex, 'PercentIncreasedCriticalDamageBonus', '#% increased Critical Damage Bonus', [critical, damage], 1000, 100, 5, suffix).
mod_group(gloves_str_dex, 'PercentIncreasedRarityOfItemsFound', '#% increased Rarity of Items found', [rarity], 1000, 100, 3, suffix).
mod_group(gloves_str_dex, 'PercentReducedAttributeRequirements', '#% reduced Attribute Requirements', [], 700, 100, 5, suffix).
mod_group(gloves_str_dex, 'FlattoDexterity', '# to Dexterity', [attribute], 1000, 100, 9, suffix).
mod_group(gloves_str_dex, 'FlattoLevelOfAllMeleeSkills', '# to Level of all Melee Skills', [], 500, 100, 2, suffix).
mod_group(gloves_str_dex, 'FlattoStrength', '# to Strength', [attribute], 500, 100, 8, suffix).
mod_group(gloves_str_dex, 'PercentToChaosResistance', '#% to Chaos Resistance', [chaos, resistance], 250, 100, 6, suffix).
mod_group(gloves_str_dex, 'PercentToColdResistance', '#% to Cold Resistance', [cold, resistance], 1000, 100, 8, suffix).
mod_group(gloves_str_dex, 'PercentToFireResistance', '#% to Fire Resistance', [fire, resistance], 1000, 100, 8, suffix).
mod_group(gloves_str_dex, 'PercentToLightningResistance', '#% to Lightning Resistance', [lightning, resistance], 1000, 100, 8, suffix).
mod_group(gloves_str_dex, 'GainFlatLifePerEnemyHitWithAttacks', 'Gain # Life per Enemy Hit with Attacks', [life, attack], 1000, 100, 4, suffix).
mod_group(gloves_str_dex, 'GainFlatLifePerEnemyKilled', 'Gain # Life per Enemy Killed', [life], 750, 100, 8, suffix).
mod_group(gloves_str_dex, 'GainFlatManaPerEnemyKilled', 'Gain # Mana per Enemy Killed', [mana], 750, 100, 8, suffix).
mod_group(gloves_str_dex, 'LeechPercentOfPhysicalAttackDamageAsLife', 'Leech #% of Physical Attack Damage as Life', [life, physical, attack, damage, leech], 1000, 100, 5, suffix).
mod_group(gloves_str_dex, 'LeechPercentOfPhysicalAttackDamageAsMana', 'Leech #% of Physical Attack Damage as Mana', [mana, physical, attack, damage, leech], 1000, 100, 5, suffix).
mod_group(gloves_str_dex, 'PercentOfArmourAlsoAppliesToElementalDamage', '#% of Armour also applies to Elemental Damage', [armour, damage], 500, 100, 5, suffix).
mod_group(gloves_str_dex, 'GainDeflectionRatingEqualToPercentOfEvasionRating', 'Gain Deflection Rating equal to #% of Evasion Rating', [evasion], 500, 100, 5, suffix).

