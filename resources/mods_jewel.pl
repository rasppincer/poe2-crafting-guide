%%% Mod data for jewel
%%% Source: Jewels use Liquid Emotions + Desecrated modifiers (0.5.0)
%%% No traditional mod pool — mods are crafted via Liquid Emotions and desecration
%%% Imported: 2026-06-09

%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)

mod_pool_weight_sum(jewel, prefix, 1000).
mod_pool_weight_sum(jewel, suffix, 1000).

%% Liquid Emotion crafted mods (prefixes)
mod_group(jewel, CraftedPlusOneSuffix, '+1 Suffix Modifier allowed', [crafted], 0, 100, 1, prefix).
mod_group(jewel, CraftedIncreasedEffectOfSuffixes, '(40-60)% increased Effect of Suffixes', [crafted, effect], 0, 100, 1, prefix).
mod_group(jewel, CraftedArmour, '(10-20)% increased Armour', [defence, armour], 0, 100, 1, prefix).
mod_group(jewel, CraftedFireDamage, '(5-15)% increased Fire Damage', [fire, damage], 0, 100, 1, prefix).
mod_group(jewel, CraftedSpellDamage, '(5-15)% increased Spell Damage', [spell, damage, caster], 0, 100, 1, prefix).

%% Liquid Emotion crafted mods (suffixes)
mod_group(jewel, CraftedPlusOnePrefix, '+1 Prefix Modifier allowed', [crafted], 0, 100, 1, suffix).
mod_group(jewel, CraftedIncreasedEffectOfPrefixes, '(40-60)% increased Effect of Prefixes', [crafted, effect], 0, 100, 1, suffix).
mod_group(jewel, CraftedCastSpeed, '(2-4)% increased Cast Speed', [speed, caster], 0, 100, 1, suffix).
mod_group(jewel, CraftedAttackSpeed, '(2-4)% increased Attack Speed', [attack, speed], 0, 100, 1, suffix).

%% Natural jewel mods (from base game, traded on market)
mod_group(jewel, CriticalHitChance, '#% increased Critical Hit Chance', [attack, critical], 500, 100, 3, suffix).
mod_group(jewel, CriticalDamageBonus, '#% increased Critical Damage Bonus', [attack, critical, damage], 500, 100, 3, suffix).
mod_group(jewel, MaximumLife, '# to Maximum Life', [life], 500, 100, 3, prefix).
mod_group(jewel, SpellDamage, '#% increased Spell Damage', [spell, damage, caster], 300, 100, 3, prefix).
mod_group(jewel, FireResistance, '#% to Fire Resistance', [elemental, fire, resistance], 300, 100, 3, suffix).
mod_group(jewel, ColdResistance, '#% to Cold Resistance', [elemental, cold, resistance], 300, 100, 3, suffix).
mod_group(jewel, LightningResistance, '#% to Lightning Resistance', [elemental, lightning, resistance], 300, 100, 3, suffix).
mod_group(jewel, ManaOnKill, 'Recover # Mana on Kill', [mana], 200, 100, 2, suffix).
mod_group(jewel, LifeOnKill, 'Recover # Life on Kill', [life], 200, 100, 2, suffix).
