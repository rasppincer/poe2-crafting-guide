%%% Mod data for sceptre
%%% Source: POE2-PathOfCrafting (frankthetank001/POE2-PathOfCrafting)
%%% Original data: poe2db.tw via weights.csv
%%% Auto-imported by import_from_pathofcrafting.py

%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)

mod_pool_weight_sum(sceptre, prefix, 6000).
mod_pool_weight_sum(sceptre, suffix, 12050).

mod_group(sceptre, 'PercentIncreasedSpirit', '#% increased Spirit', [], 1000, 100, 8, prefix).
mod_group(sceptre, 'PercentIncreasedSpiritFlattoMaximumMana', '#% increased Spirit, # to maximum Mana', [mana], 1000, 100, 7, prefix).
mod_group(sceptre, 'FlattoMaximumMana', '# to maximum Mana', [mana], 1000, 100, 11, prefix).
mod_group(sceptre, 'AlliesInYourPresenceDealFlattoflatAddedAttackColdDamage', 'Allies in your Presence deal # to # added Attack Cold Damage', [cold, attack, damage], 500, 100, 9, prefix).
mod_group(sceptre, 'AlliesInYourPresenceDealFlattoflatAddedAttackFireDamage', 'Allies in your Presence deal # to # added Attack Fire Damage', [fire, attack, damage], 500, 100, 9, prefix).
mod_group(sceptre, 'AlliesInYourPresenceDealFlattoflatAddedAttackLightningDamage', 'Allies in your Presence deal # to # added Attack Lightning Damage', [lightning, attack, damage], 500, 100, 9, prefix).
mod_group(sceptre, 'AlliesInYourPresenceDealFlattoflatAddedAttackPhysicalDamage', 'Allies in your Presence deal # to # added Attack Physical Damage', [physical, attack, damage], 500, 100, 9, prefix).
mod_group(sceptre, 'AlliesInYourPresenceDealPercentIncreasedDamage', 'Allies in your Presence deal #% increased Damage', [damage], 1000, 100, 8, prefix).

mod_group(sceptre, 'PercentIncreasedManaRegenerationRatePercentIncreasedLightRadius', '#% increased Mana Regeneration Rate, #% increased Light Radius', [mana, regeneration], 1000, 100, 3, suffix).
mod_group(sceptre, 'PercentIncreasedManaRegenerationRate', '#% increased Mana Regeneration Rate', [mana, regeneration], 1000, 100, 6, suffix).
mod_group(sceptre, 'PercentIncreasedPresenceAreaOfEffect', '#% increased Presence Area of Effect', [], 500, 100, 4, suffix).
mod_group(sceptre, 'PercentReducedAttributeRequirements', '#% reduced Attribute Requirements', [], 1000, 100, 5, suffix).
mod_group(sceptre, 'FlattoIntelligence', '# to Intelligence', [attribute], 750, 100, 8, suffix).
mod_group(sceptre, 'FlattoLevelOfAllMinionSkills', '# to Level of all Minion Skills', [], 750, 100, 4, suffix).
mod_group(sceptre, 'FlattoStrength', '# to Strength', [attribute], 250, 100, 8, suffix).
mod_group(sceptre, 'AlliesInYourPresenceHavePercentIncreasedAttackSpeed', 'Allies in your Presence have #% increased Attack Speed', [attack, speed], 1000, 100, 4, suffix).
mod_group(sceptre, 'AlliesInYourPresenceHavePercentIncreasedCastSpeed', 'Allies in your Presence have #% increased Cast Speed', [caster, speed], 1000, 100, 4, suffix).
mod_group(sceptre, 'AlliesInYourPresenceHavePercentIncreasedCriticalDamageBonus', 'Allies in your Presence have #% increased Critical Damage Bonus', [critical, damage], 1000, 100, 6, suffix).
mod_group(sceptre, 'AlliesInYourPresenceHavePercentIncreasedCriticalHitChance', 'Allies in your Presence have #% increased Critical Hit Chance', [critical], 1000, 100, 6, suffix).
mod_group(sceptre, 'AlliesInYourPresenceHavePercentToAllElementalResistances', 'Allies in your Presence have #% to all Elemental Resistances', [resistance], 800, 100, 6, suffix).
mod_group(sceptre, 'AlliesInYourPresenceRegenerateFlatLifePerSecond', 'Allies in your Presence Regenerate # Life per second', [life, regeneration], 1000, 100, 10, suffix).
mod_group(sceptre, 'MinionsHavePercentIncreasedMaximumLife', 'Minions have #% increased maximum Life', [life], 1000, 100, 6, suffix).

