%%% Mod data for ring
%%% Source: https://poe2db.tw/us/Rings
%%% Extracted: 2026-06-09

%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)

mod_pool_weight_sum(ring, prefix, 69500).
mod_pool_weight_sum(ring, suffix, 87105).

mod_group(ring, 1IncreasedLife, '# to maximum Life', [life], 8000, 54, 8, prefix).
mod_group(ring, 1IncreasedMana, '# to maximum Mana', [mana], 12000, 75, 12, prefix).
mod_group(ring, 1IncreasedEvasionRating, '# to Evasion Rating', [evasion], 9000, 70, 9, prefix).
mod_group(ring, 1PhysicalDamage, 'Adds # to # Physical Damage to Attacks', [damage, physical, attack], 7800, 75, 9, prefix).
mod_group(ring, 1FireDamage, 'Adds # to # Fire damage to Attacks', [damage, elemental, fire, attack], 3900, 75, 9, prefix).
mod_group(ring, 1ColdDamage, 'Adds # to # Cold damage to Attacks', [damage, elemental, cold, attack], 3900, 75, 9, prefix).
mod_group(ring, 1LightningDamage, 'Adds # to # Lightning damage to Attacks', [damage, elemental, lightning, attack], 3900, 75, 9, prefix).
mod_group(ring, 1IncreasedAccuracy, '# to Accuracy Rating', [attack], 6000, 67, 8, prefix).
mod_group(ring, 1ItemFoundRarityIncreasePrefix, '#% increased Rarity of Items found', [], 3000, 47, 3, prefix).
mod_group(ring, 1FireDamagePercentage, '#% increased Fire Damage', [damage, elemental, fire], 3000, 75, 6, prefix).
mod_group(ring, 1ColdDamagePercentage, '#% increased Cold Damage', [damage, elemental, cold], 3000, 75, 6, prefix).
mod_group(ring, 1LightningDamagePercentage, '#% increased Lightning Damage', [damage, elemental, lightning], 3000, 75, 6, prefix).
mod_group(ring, 1IncreasedChaosDamage, '#% increased Chaos Damage', [damage, chaos], 3000, 75, 6, prefix).

mod_group(ring, 2Strength, '# to Strength', [attribute], 8000, 74, 8, suffix).
mod_group(ring, 2Dexterity, '# to Dexterity', [attribute], 8000, 74, 8, suffix).
mod_group(ring, 2Intelligence, '# to Intelligence', [attribute], 8000, 74, 8, suffix).
mod_group(ring, 2AllAttributes, '# to all Attributes', [attribute], 1600, 33, 4, suffix).
mod_group(ring, 2FireResistance, '#% to Fire Resistance', [elemental, fire, resistance], 8000, 82, 8, suffix).
mod_group(ring, 2ColdResistance, '#% to Cold Resistance', [elemental, cold, resistance], 8000, 82, 8, suffix).
mod_group(ring, 2LightningResistance, '#% to Lightning Resistance', [elemental, lightning, resistance], 8000, 82, 8, suffix).
mod_group(ring, 2AllResistances, '#% to all Elemental Resistances', [elemental, fire, cold, lightning, resistance], 4000, 68, 5, suffix).
mod_group(ring, 2ChaosResistance, '#% to Chaos Resistance', [chaos, resistance], 1500, 81, 6, suffix).
mod_group(ring, 2LifeRegeneration, '# Life Regeneration per second', [life], 7000, 47, 7, suffix).
mod_group(ring, 2ManaRegeneration, '#% increased Mana Regeneration Rate', [mana], 6000, 79, 6, suffix).
mod_group(ring, 2LifeLeech, 'Leech #% of Physical Attack Damage as Life', [life, physical, attack], 2000, 38, 2, suffix).
mod_group(ring, 2ManaLeech, 'Leech #% of Physical Attack Damage as Mana', [mana, physical, attack], 2000, 38, 2, suffix).
mod_group(ring, 2LifeGainedFromEnemyDeath, 'Gain # Life per enemy killed', [life], 4500, 55, 6, suffix).
mod_group(ring, 2ManaGainedFromEnemyDeath, 'Gain # Mana per enemy killed', [mana], 4500, 56, 6, suffix).
mod_group(ring, 2ItemFoundRarityIncrease, '#% increased Rarity of Items found', [], 3000, 40, 3, suffix).
mod_group(ring, 2LightRadiusAndManaRegeneration, '#% increased Mana Regeneration Rate#% increased Light Radius', [mana], 3000, 30, 3, suffix).
mod_group(ring, 2IncreasedCastSpeed, '#% increased Cast Speed', [caster, speed], 5, 60, 5, suffix).
