%%% Auto-generated exclusion group facts from PathOfCrafting
%%% exclusion_group(+GroupId, +Description, +Patterns)
%%%   Patterns use '#' as numeric wildcard.
%%% exclusion_group_items(+GroupId, +ApplicableItems)
%%%   Only present when group is restricted to specific item types.
%%% exclusion_group_tag(+GroupId, +Tag)
%%%   Only present for tag-based exclusion groups.
%%%
%%% Two mods whose stat_text matches different patterns in the same
%%% group cannot coexist on the same item (within the same affix type).
%%% Use match_exclusion_pattern/2 (in poe2_crafting.pl) for matching.

exclusion_group(0, 'Ailment mods within same type (prefix/suffix)', []).
exclusion_group_tag(0, 'ailment').

exclusion_group(1, 'Hybrid attributes - Str+Dex vs Str+Int', ['+# to Strength and Dexterity', '+# to Strength and Intelligence']).

exclusion_group(2, 'Dodge roll mods', ['#% increased Mana Cost Efficiency if you have Dodge Rolled Recently', '# metres to Dodge Roll distance']).

exclusion_group(3, 'Flask recovery amount variations', ['#% increased Amount Recovered', '#% increased Life Recovered, Removes #% of Life Recovered from Mana when used', '#% more Recovery if used while on Low Life']).

exclusion_group(4, 'Flask recovery rate vs instant', ['#% increased Recovery rate', '#% of Recovery applied Instantly']).

exclusion_group(5, 'Flask charge gain mechanics', ['#% Chance to gain a Charge when you Kill an Enemy', '#% increased Charges gained']).

exclusion_group(6, 'Skill gem levels', ['+# to Level of all Melee Skills', '+# to Level of all Minion Skills', '+# to Level of all Projectile Skills', '+# to Level of all Spell Skills', '+# to Level of all Skills']).

exclusion_group(7, 'Hybrid attributes - Dex+Int vs Int', ['+# to Dexterity and Intelligence', '+# to Intelligence']).

exclusion_group(8, 'Thorns damage types', ['# to # Physical Thorns damage', '# to # Fire Thorns damage per 100 maximum Life']).

exclusion_group(9, 'Flask recovery rate - Life vs Mana', ['#% increased Flask Mana Recovery rate', '#% increased Flask Life Recovery rate']).

exclusion_group(10, 'Armour sources', ['+# to Armour', 'Gain (#-#)% of Maximum Mana as Armour']).

exclusion_group(11, 'Flask charge generation - Life vs Mana', ['Life Flasks gain (#-#) charges per Second', 'Mana Flasks gain (#-#) charges per Second']).

exclusion_group(12, 'Life leech variations', ['Leech #% of Physical Attack Damage as Life', '(#-#)% increased amount of Life Leeched']).

exclusion_group(13, 'Focus - Elemental spell damage types', ['#% increased Chaos Damage', '#% increased Cold Damage', '#% increased Fire Damage', '#% increased Lightning Damage', '#% increased Spell Physical Damage']).
exclusion_group_items(13, ['focus']).

exclusion_group(14, 'Spell damage variations', ['#% increased Spell Damage', 'Invocated Spells deal (#-#)% increased Damage']).

exclusion_group(15, 'Mana cost efficiency tiers', ['(#-#)% increased Mana Cost Efficiency', '(#-#)% increased Mana Cost Efficiency']).

exclusion_group(16, 'Minion vs Spell skill levels', ['+(#-#) to Level of all Minion Skills', '+# to Level of all Spell Skills']).

exclusion_group(17, 'Critical damage bonus variations', ['#% increased Critical Damage Bonus for Attack Damage', '#% to Critical Damage Bonus', 'Projectiles have (#-#)% increased Critical Damage Bonus against Enemies within 2m']).

exclusion_group(18, 'Critical hit chance variations', ['#% increased Critical Hit Chance for Attacks', 'Projectiles have (#-#)% increased Critical Hit Chance against Enemies further than 6m']).

exclusion_group(19, 'Projectile damage variations', ['Increases and Reductions to Projectile Speed also apply to Damage with Bows', 'Projectiles deal (#-#)% increased Damage with Hits against Enemies further than 6m', 'Projectiles deal (#-#)% increased Damage with Hits against Enemies within 2m']).

exclusion_group(20, 'Maximum resistances', ['+#% to all Maximum Elemental Resistances', '+#% to all maximum Resistances']).

exclusion_group(21, 'Parried debuff variations', ['(#-#)% increased Parried Debuff Duration', '(#-#)% increased Parried Debuff Magnitude']).

exclusion_group(22, 'Cold damage vs elemental damage', ['#% increased Cold Damage', '(#-#)% increased Elemental Damage']).

exclusion_group(23, 'Spell damage variations - extended', ['#% increased Spell Damage', '(#-#)% increased Spell Damage with Spells that cost Life', 'Invocated Spells deal (#-#)% increased Damage', 'Minions deal (#-#)% increased Damage, (#-#)% increased Spell Damage']).

exclusion_group(24, 'Cast speed variations', ['#% increased Cast Speed', '(#-#)% increased Cast Speed for each different Non-Instant Spell you\'ve Cast Recently', '(#-#)% increased Cast Speed while on Full Mana']).

exclusion_group(25, 'all spell levels', ['+# to Level of all Cold Spell Skills', '+# to Level of all Fire Spell Skills', '+# to Level of all Lightning Spell Skills', '+# to Level of all Physical Spell Skills', '+# to Level of all Chaos Spell Skills', '+# to Level of all Spell Skills', '+# to Level of all Melee Skills', '+# to Level of all Projectile Skills', '+# to Level of all Attack Skills', '+# to Level of all Minion Skills']).

exclusion_group(26, 'Break armour mechanics', ['Break (#-#)% increased Armour', 'Break Armour on Critical Hit with Spells equal to (#-#)% of Physical Damage dealt']).

exclusion_group(27, 'Hindered enemy damage increases', ['Enemies Hindered by you take (#-#)% increased Chaos Damage', 'Enemies Hindered by you take (#-#)% increased Elemental Damage', 'Enemies Hindered by you take (#-#)% increased Physical Damage']).

exclusion_group(28, 'Extra damage as element', ['Gain (#-#)% of Damage as Extra Cold Damage', 'Gain (#-#)% of Damage as Extra Fire Damage', 'Gain (#-#)% of Damage as Extra Lightning Damage', 'Gain (#-#)% of Damage as Extra Physical Damage']).
exclusion_group_items(28, ['flail', 'axe', 'sword', 'spear', 'bow', 'crossbow', 'warstaff']).

exclusion_group(29, 'Physical damage variations - mace', ['#% increased Physical Damage', '(#-#)% increased Physical Damage, #% reduced Attack Speed']).
exclusion_group_items(29, ['mace']).

exclusion_group(30, 'Melee vs attack skill levels', ['+# to Level of all Melee Skills', '+# to Level of all Attack Skills']).

exclusion_group(31, 'Fire damage vs elemental damage - wand', ['#% increased Fire Damage', '(#-#)% increased Elemental Damage']).
exclusion_group_items(31, ['wand']).

exclusion_group(32, 'Attack speed variations - companion', ['#% increased Attack Speed', '(#-#)% increased Attack Speed, (#-#)% increased Attack Speed while your Companion is in your Presence', '(#-#)% increased Attack Speed, Companions have (#-#)% increased Attack Speed']).

exclusion_group(33, 'Critical hit chance - projectiles', ['+#% to Critical Hit Chance', 'Projectiles have (#-#)% increased Critical Hit Chance against Enemies further than 6m']).

exclusion_group(34, 'Bow additional arrows', ['Bow Attacks fire 2 additional Arrows', 'Bow Attacks fire an additional Arrow']).
exclusion_group_items(34, ['bow']).

exclusion_group(35, 'Spell damage variations - per stat', ['#% increased Spell Damage', '(#-#)% increased Spell Damage per 100 Maximum Life', '(#-#)% increased Spell Damage per 100 maximum Mana', '(#-#)% increased Spell Damage with Spells that cost Life']).

exclusion_group(36, 'Crossbow additional bolts', ['Loads 2 additional bolts', 'Loads an additional bolt']).
exclusion_group_items(36, ['crossbow']).

exclusion_group(37, 'Crossbow reload mechanics', ['(#-#)% chance when you Reload a Crossbow to be immediate', '(#-#)% increased Reload Speed']).
exclusion_group_items(37, ['crossbow']).

exclusion_group(38, 'Recover when expend combo', ['Recover (#-#)% of Maximum Life when you expend at least 10 Combo', 'Recover (#-#)% of Maximum Mana when you expend at least 10 Combo']).

exclusion_group(39, 'Global defences', ['#% increased Global Defences', '#% increased Global Defences']).
