%%% Mod data for gloves_int
%%% Source: POE2-PathOfCrafting (frankthetank001/POE2-PathOfCrafting)
%%% Original data: poe2db.tw via weights.csv
%%% Imported: 2026-06-09

%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)

mod_pool_weight_sum(gloves_int, prefix, 6200).
mod_pool_weight_sum(gloves_int, suffix, 13450).

mod_group(gloves_int, PercentIncreasedEnergyShield, '#% increased Energy Shield', [energy_shield], 1000, 100, 7, prefix).
mod_group(gloves_int, PercentIncreasedEnergyShieldFlattoMaximumLife, '#% increased Energy Shield, # to maximum Life', [life, energy_shield], 1000, 100, 6, prefix).
mod_group(gloves_int, FlattoAccuracyRating, '# to Accuracy Rating', [accuracy], 200, 100, 9, prefix).
mod_group(gloves_int, FlattoMaximumEnergyShield, '# to maximum Energy Shield', [energy_shield], 1000, 100, 7, prefix).
mod_group(gloves_int, FlattoMaximumLife, '# to maximum Life', [life], 1000, 100, 9, prefix).
mod_group(gloves_int, FlattoMaximumMana, '# to maximum Mana', [mana], 1000, 100, 9, prefix).
mod_group(gloves_int, AddsFlattoFlatColdDamageToAttacks, 'Adds # to # Cold damage to Attacks', [cold, attack, damage], 200, 100, 9, prefix).
mod_group(gloves_int, AddsFlattoFlatFireDamageToAttacks, 'Adds # to # Fire damage to Attacks', [fire, attack, damage], 200, 100, 9, prefix).
mod_group(gloves_int, AddsFlattoFlatLightningDamageToAttacks, 'Adds # to # Lightning damage to Attacks', [lightning, attack, damage], 200, 100, 9, prefix).
mod_group(gloves_int, AddsFlattoFlatPhysicalDamageToAttacks, 'Adds # to # Physical Damage to Attacks', [physical, attack, damage], 400, 100, 9, prefix).
mod_group(gloves_int, PercentIncreasedAttackSpeed, '#% increased Attack Speed', [attack, speed], 500, 100, 4, suffix).
mod_group(gloves_int, PercentIncreasedCriticalDamageBonus, '#% increased Critical Damage Bonus', [critical, damage], 250, 100, 5, suffix).
mod_group(gloves_int, PercentIncreasedRarityOfItemsFound, '#% increased Rarity of Items found', [], 1000, 100, 3, suffix).
mod_group(gloves_int, PercentReducedAttributeRequirements, '#% reduced Attribute Requirements', [attribute], 700, 100, 5, suffix).
mod_group(gloves_int, FlattoDexterity, '# to Dexterity', [attribute], 1000, 100, 9, suffix).
mod_group(gloves_int, FlattoIntelligence, '# to Intelligence', [attribute], 1000, 100, 8, suffix).
mod_group(gloves_int, FlattoLevelOfAllMeleeSkills, '# to Level of all Melee Skills', [], 250, 100, 2, suffix).
mod_group(gloves_int, PercentToChaosResistance, '#% to Chaos Resistance', [chaos, resistance], 250, 100, 6, suffix).
mod_group(gloves_int, PercentToColdResistance, '#% to Cold Resistance', [cold, resistance], 1000, 100, 8, suffix).
mod_group(gloves_int, PercentToFireResistance, '#% to Fire Resistance', [fire, resistance], 1000, 100, 8, suffix).
mod_group(gloves_int, PercentToLightningResistance, '#% to Lightning Resistance', [lightning, resistance], 1000, 100, 8, suffix).
mod_group(gloves_int, GainFlatLifePerEnemyHitWithAttacks, 'Gain # Life per Enemy Hit with Attacks', [life, attack], 1000, 100, 4, suffix).
mod_group(gloves_int, GainFlatLifePerEnemyKilled, 'Gain # Life per Enemy Killed', [life], 750, 100, 8, suffix).
mod_group(gloves_int, GainFlatManaPerEnemyKilled, 'Gain # Mana per Enemy Killed', [mana], 750, 100, 8, suffix).
mod_group(gloves_int, LeechPercentOfPhysicalAttackDamageAsLife, 'Leech #% of Physical Attack Damage as Life', [life, physical, attack, damage], 1000, 100, 5, suffix).
mod_group(gloves_int, LeechPercentOfPhysicalAttackDamageAsMana, 'Leech #% of Physical Attack Damage as Mana', [mana, physical, attack, damage], 1000, 100, 5, suffix).
mod_group(gloves_int, PercentIncreasedEnergyShieldRechargeRate, '#% increased Energy Shield Recharge Rate', [energy_shield], 1000, 100, 4, suffix).
