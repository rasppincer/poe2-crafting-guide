%%% Mod data for gloves_dex_int
%%% Source: POE2-PathOfCrafting (frankthetank001/POE2-PathOfCrafting)
%%% Original data: poe2db.tw via weights.csv
%%% Auto-imported by import_from_pathofcrafting.py

%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)

mod_pool_weight_sum(gloves_dex_int, prefix, 8300).
mod_pool_weight_sum(gloves_dex_int, suffix, 13950).

mod_group(gloves_dex_int, 'PercentIncreasedEvasionAndEnergyShield', '#% increased Evasion and Energy Shield', [energy_shield, evasion], 1000, 100, 7, prefix).
mod_group(gloves_dex_int, 'PercentIncreasedEvasionAndEnergyShieldFlattoMaximumLife', '#% increased Evasion and Energy Shield, # to maximum Life', [life, energy_shield, evasion], 1000, 100, 6, prefix).
mod_group(gloves_dex_int, 'FlattoAccuracyRating', '# to Accuracy Rating', [accuracy], 800, 100, 9, prefix).
mod_group(gloves_dex_int, 'FlattoEvasionRatingFlattoMaximumEnergyShield', '# to Evasion Rating, # to maximum Energy Shield', [energy_shield, evasion], 1000, 100, 4, prefix).
mod_group(gloves_dex_int, 'FlattoMaximumLife', '# to maximum Life', [life], 1000, 100, 9, prefix).
mod_group(gloves_dex_int, 'FlattoMaximumMana', '# to maximum Mana', [mana], 1000, 100, 9, prefix).
mod_group(gloves_dex_int, 'AddsFlattoflatColdDamageToAttacks', 'Adds # to # Cold damage to Attacks', [cold, attack, damage], 500, 100, 9, prefix).
mod_group(gloves_dex_int, 'AddsFlattoflatFireDamageToAttacks', 'Adds # to # Fire damage to Attacks', [fire, attack, damage], 500, 100, 9, prefix).
mod_group(gloves_dex_int, 'AddsFlattoflatLightningDamageToAttacks', 'Adds # to # Lightning damage to Attacks', [lightning, attack, damage], 500, 100, 9, prefix).
mod_group(gloves_dex_int, 'AddsFlattoflatPhysicalDamageToAttacks', 'Adds # to # Physical Damage to Attacks', [physical, attack, damage], 1000, 100, 9, prefix).

mod_group(gloves_dex_int, 'PercentIncreasedAttackSpeed', '#% increased Attack Speed', [attack, speed], 500, 100, 4, suffix).
mod_group(gloves_dex_int, 'PercentIncreasedCriticalDamageBonus', '#% increased Critical Damage Bonus', [critical, damage], 1000, 100, 5, suffix).
mod_group(gloves_dex_int, 'PercentIncreasedRarityOfItemsFound', '#% increased Rarity of Items found', [rarity], 1000, 100, 3, suffix).
mod_group(gloves_dex_int, 'PercentReducedAttributeRequirements', '#% reduced Attribute Requirements', [], 700, 100, 5, suffix).
mod_group(gloves_dex_int, 'FlattoDexterity', '# to Dexterity', [attribute], 1000, 100, 9, suffix).
mod_group(gloves_dex_int, 'FlattoIntelligence', '# to Intelligence', [attribute], 500, 100, 8, suffix).
mod_group(gloves_dex_int, 'FlattoLevelOfAllMeleeSkills', '# to Level of all Melee Skills', [], 500, 100, 2, suffix).
mod_group(gloves_dex_int, 'PercentToChaosResistance', '#% to Chaos Resistance', [chaos, resistance], 250, 100, 6, suffix).
mod_group(gloves_dex_int, 'PercentToColdResistance', '#% to Cold Resistance', [cold, resistance], 1000, 100, 8, suffix).
mod_group(gloves_dex_int, 'PercentToFireResistance', '#% to Fire Resistance', [fire, resistance], 1000, 100, 8, suffix).
mod_group(gloves_dex_int, 'PercentToLightningResistance', '#% to Lightning Resistance', [lightning, resistance], 1000, 100, 8, suffix).
mod_group(gloves_dex_int, 'GainFlatLifePerEnemyHitWithAttacks', 'Gain # Life per Enemy Hit with Attacks', [life, attack], 1000, 100, 4, suffix).
mod_group(gloves_dex_int, 'GainFlatLifePerEnemyKilled', 'Gain # Life per Enemy Killed', [life], 750, 100, 8, suffix).
mod_group(gloves_dex_int, 'GainFlatManaPerEnemyKilled', 'Gain # Mana per Enemy Killed', [mana], 750, 100, 8, suffix).
mod_group(gloves_dex_int, 'LeechPercentOfPhysicalAttackDamageAsLife', 'Leech #% of Physical Attack Damage as Life', [life, physical, attack, damage, leech], 1000, 100, 5, suffix).
mod_group(gloves_dex_int, 'LeechPercentOfPhysicalAttackDamageAsMana', 'Leech #% of Physical Attack Damage as Mana', [mana, physical, attack, damage, leech], 1000, 100, 5, suffix).
mod_group(gloves_dex_int, 'PercentIncreasedEnergyShieldRechargeRate', '#% increased Energy Shield Recharge Rate', [energy_shield], 500, 100, 4, suffix).
mod_group(gloves_dex_int, 'GainDeflectionRatingEqualToPercentOfEvasionRating', 'Gain Deflection Rating equal to #% of Evasion Rating', [evasion], 500, 100, 5, suffix).

