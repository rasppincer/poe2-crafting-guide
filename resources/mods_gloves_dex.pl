%%% Mod data for gloves_dex
%%% Source: POE2-PathOfCrafting (frankthetank001/POE2-PathOfCrafting)
%%% Original data: poe2db.tw via weights.csv
%%% Imported: 2026-06-09

%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)

mod_pool_weight_sum(gloves_dex, prefix, 6200).
mod_pool_weight_sum(gloves_dex, suffix, 12450).

mod_group(gloves_dex, PercentIncreasedEvasionRating, '#% increased Evasion Rating', [evasion], 1000, 100, 7, prefix).
mod_group(gloves_dex, PercentIncreasedEvasionRatingFlattoMaximumLife, '#% increased Evasion Rating, # to maximum Life', [life, evasion], 1000, 100, 6, prefix).
mod_group(gloves_dex, FlattoAccuracyRating, '# to Accuracy Rating', [accuracy], 200, 100, 9, prefix).
mod_group(gloves_dex, FlattoEvasionRating, '# to Evasion Rating', [evasion], 1000, 100, 7, prefix).
mod_group(gloves_dex, FlattoMaximumLife, '# to maximum Life', [life], 1000, 100, 9, prefix).
mod_group(gloves_dex, FlattoMaximumMana, '# to maximum Mana', [mana], 1000, 100, 9, prefix).
mod_group(gloves_dex, AddsFlattoFlatColdDamageToAttacks, 'Adds # to # Cold damage to Attacks', [cold, attack, damage], 200, 100, 9, prefix).
mod_group(gloves_dex, AddsFlattoFlatFireDamageToAttacks, 'Adds # to # Fire damage to Attacks', [fire, attack, damage], 200, 100, 9, prefix).
mod_group(gloves_dex, AddsFlattoFlatLightningDamageToAttacks, 'Adds # to # Lightning damage to Attacks', [lightning, attack, damage], 200, 100, 9, prefix).
mod_group(gloves_dex, AddsFlattoFlatPhysicalDamageToAttacks, 'Adds # to # Physical Damage to Attacks', [physical, attack, damage], 400, 100, 9, prefix).
mod_group(gloves_dex, PercentIncreasedAttackSpeed, '#% increased Attack Speed', [attack, speed], 500, 100, 4, suffix).
mod_group(gloves_dex, PercentIncreasedCriticalDamageBonus, '#% increased Critical Damage Bonus', [critical, damage], 250, 100, 5, suffix).
mod_group(gloves_dex, PercentIncreasedRarityOfItemsFound, '#% increased Rarity of Items found', [], 1000, 100, 3, suffix).
mod_group(gloves_dex, PercentReducedAttributeRequirements, '#% reduced Attribute Requirements', [attribute], 700, 100, 5, suffix).
mod_group(gloves_dex, FlattoDexterity, '# to Dexterity', [attribute], 1000, 100, 9, suffix).
mod_group(gloves_dex, FlattoLevelOfAllMeleeSkills, '# to Level of all Melee Skills', [], 250, 100, 2, suffix).
mod_group(gloves_dex, PercentToChaosResistance, '#% to Chaos Resistance', [chaos, resistance], 250, 100, 6, suffix).
mod_group(gloves_dex, PercentToColdResistance, '#% to Cold Resistance', [cold, resistance], 1000, 100, 8, suffix).
mod_group(gloves_dex, PercentToFireResistance, '#% to Fire Resistance', [fire, resistance], 1000, 100, 8, suffix).
mod_group(gloves_dex, PercentToLightningResistance, '#% to Lightning Resistance', [lightning, resistance], 1000, 100, 8, suffix).
mod_group(gloves_dex, GainFlatLifePerEnemyHitWithAttacks, 'Gain # Life per Enemy Hit with Attacks', [life, attack], 1000, 100, 4, suffix).
mod_group(gloves_dex, GainFlatLifePerEnemyKilled, 'Gain # Life per Enemy Killed', [life], 750, 100, 8, suffix).
mod_group(gloves_dex, GainFlatManaPerEnemyKilled, 'Gain # Mana per Enemy Killed', [mana], 750, 100, 8, suffix).
mod_group(gloves_dex, LeechPercentOfPhysicalAttackDamageAsLife, 'Leech #% of Physical Attack Damage as Life', [life, physical, attack, damage], 1000, 100, 5, suffix).
mod_group(gloves_dex, LeechPercentOfPhysicalAttackDamageAsMana, 'Leech #% of Physical Attack Damage as Mana', [mana, physical, attack, damage], 1000, 100, 5, suffix).
mod_group(gloves_dex, GainDeflectionRatingEqualToPercentOfEvasionRating, 'Gain Deflection Rating equal to #% of Evasion Rating', [evasion], 1000, 100, 5, suffix).
