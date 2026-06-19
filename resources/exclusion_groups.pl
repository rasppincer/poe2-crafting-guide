%% exclusion_groups.pl — imported from POE2-PathOfCrafting
%% Groups of modifiers that cannot coexist on the same item.
%% exclusion_group(+Game, +GroupId, +Description, +Patterns)

exclusion_group(poe2, excl_0, 'Ailment mods within same type (prefix/suffix) (More than one ailment mod can\'t go together within the same type)', []).
exclusion_group(poe2, excl_1, 'Hybrid attributes - Str+Dex vs Str+Int', ['+# to Strength and Dexterity', '+# to Strength and Intelligence']).
exclusion_group(poe2, excl_2, 'Dodge roll mods', ['#% increased Mana Cost Efficiency if you have Dodge Rolled Recently', '# metres to Dodge Roll distance']).
exclusion_group(poe2, excl_3, 'Flask recovery amount variations', ['#% increased Amount Recovered', '#% increased Life Recovered, Removes #% of Life Recovered from Mana when used', '#% more Recovery if used while on Low Life']).
exclusion_group(poe2, excl_4, 'Flask recovery rate vs instant', ['#% increased Recovery rate', '#% of Recovery applied Instantly']).
exclusion_group(poe2, excl_5, 'Flask charge gain mechanics', ['#% Chance to gain a Charge when you Kill an Enemy', '#% increased Charges gained']).
exclusion_group(poe2, excl_6, 'Skill gem levels', ['+# to Level of all Melee Skills', '+# to Level of all Minion Skills', '+# to Level of all Projectile Skills', '+# to Level of all Spell Skills', '+# to Level of all Skills']).
exclusion_group(poe2, excl_7, 'Hybrid attributes - Dex+Int vs Int', ['+# to Dexterity and Intelligence', '+# to Intelligence']).
exclusion_group(poe2, excl_8, 'Thorns damage types', ['# to # Physical Thorns damage', '# to # Fire Thorns damage per 100 maximum Life']).
exclusion_group(poe2, excl_9, 'Flask recovery rate - Life vs Mana', ['#% increased Flask Mana Recovery rate', '#% increased Flask Life Recovery rate']).
exclusion_group(poe2, excl_10, 'Armour sources', ['+# to Armour', 'Gain (#-#)% of Maximum Mana as Armour']).
exclusion_group(poe2, excl_11, 'Flask charge generation - Life vs Mana', ['Life Flasks gain (#-#) charges per Second', 'Mana Flasks gain (#-#) charges per Second']).
exclusion_group(poe2, excl_12, 'Life leech variations', ['Leech #% of Physical Attack Damage as Life', '(#-#)% increased amount of Life Leeched']).
exclusion_group(poe2, excl_13, 'Focus - Elemental spell damage types (offhand > focus only)', ['#% increased Chaos Damage', '#% increased Cold Damage', '#% increased Fire Damage', '#% increased Lightning Damage', '#% increased Spell Physical Damage']).
exclusion_group(poe2, excl_14, 'Spell damage variations', ['#% increased Spell Damage', 'Invocated Spells deal (#-#)% increased Damage']).
exclusion_group(poe2, excl_15, 'Mana cost efficiency tiers', ['(#-#)% increased Mana Cost Efficiency', '(#-#)% increased Mana Cost Efficiency']).
exclusion_group(poe2, excl_16, 'Minion vs Spell skill levels', ['+(#-#) to Level of all Minion Skills', '+# to Level of all Spell Skills']).
exclusion_group(poe2, excl_17, 'Critical damage bonus variations', ['#% increased Critical Damage Bonus for Attack Damage', '#% to Critical Damage Bonus', 'Projectiles have (#-#)% increased Critical Damage Bonus against Enemies within 2m']).
exclusion_group(poe2, excl_18, 'Critical hit chance variations', ['#% increased Critical Hit Chance for Attacks', 'Projectiles have (#-#)% increased Critical Hit Chance against Enemies further than 6m']).
exclusion_group(poe2, excl_19, 'Projectile damage variations', ['Increases and Reductions to Projectile Speed also apply to Damage with Bows', 'Projectiles deal (#-#)% increased Damage with Hits against Enemies further than 6m', 'Projectiles deal (#-#)% increased Damage with Hits against Enemies within 2m']).
exclusion_group(poe2, excl_20, 'Maximum resistances', ['+#% to all Maximum Elemental Resistances', '+#% to all maximum Resistances']).
exclusion_group(poe2, excl_21, 'Parried debuff variations', ['(#-#)% increased Parried Debuff Duration', '(#-#)% increased Parried Debuff Magnitude']).
exclusion_group(poe2, excl_22, 'Cold damage vs elemental damage', ['#% increased Cold Damage', '(#-#)% increased Elemental Damage']).
exclusion_group(poe2, excl_23, 'Spell damage variations - extended', ['#% increased Spell Damage', '(#-#)% increased Spell Damage with Spells that cost Life', 'Invocated Spells deal (#-#)% increased Damage', 'Minions deal (#-#)% increased Damage, (#-#)% increased Spell Damage']).
exclusion_group(poe2, excl_24, 'Cast speed variations', ['#% increased Cast Speed', '(#-#)% increased Cast Speed for each different Non-Instant Spell you\'ve Cast Recently', '(#-#)% increased Cast Speed while on Full Mana']).
exclusion_group(poe2, excl_25, 'all spell levels', ['+# to Level of all Cold Spell Skills', '+# to Level of all Fire Spell Skills', '+# to Level of all Lightning Spell Skills', '+# to Level of all Physical Spell Skills', '+# to Level of all Chaos Spell Skills', '+# to Level of all Spell Skills', '+# to Level of all Melee Skills', '+# to Level of all Projectile Skills', '+# to Level of all Attack Skills', '+# to Level of all Minion Skills']).
exclusion_group(poe2, excl_26, 'Break armour mechanics', ['Break (#-#)% increased Armour', 'Break Armour on Critical Hit with Spells equal to (#-#)% of Physical Damage dealt']).
exclusion_group(poe2, excl_27, 'Hindered enemy damage increases', ['Enemies Hindered by you take (#-#)% increased Chaos Damage', 'Enemies Hindered by you take (#-#)% increased Elemental Damage', 'Enemies Hindered by you take (#-#)% increased Physical Damage']).
exclusion_group(poe2, excl_28, 'Extra damage as element (flail, axe, sword, spear, bow, crossbow, warstaff)', ['Gain (#-#)% of Damage as Extra Cold Damage', 'Gain (#-#)% of Damage as Extra Fire Damage', 'Gain (#-#)% of Damage as Extra Lightning Damage', 'Gain (#-#)% of Damage as Extra Physical Damage']).
exclusion_group(poe2, excl_29, 'Physical damage variations - mace (mace only)', ['#% increased Physical Damage', '(#-#)% increased Physical Damage, #% reduced Attack Speed']).
exclusion_group(poe2, excl_30, 'Melee vs attack skill levels', ['+# to Level of all Melee Skills', '+# to Level of all Attack Skills']).
exclusion_group(poe2, excl_31, 'Fire damage vs elemental damage - wand (wand only)', ['#% increased Fire Damage', '(#-#)% increased Elemental Damage']).
exclusion_group(poe2, excl_32, 'Attack speed variations - companion', ['#% increased Attack Speed', '(#-#)% increased Attack Speed, (#-#)% increased Attack Speed while your Companion is in your Presence', '(#-#)% increased Attack Speed, Companions have (#-#)% increased Attack Speed']).
exclusion_group(poe2, excl_33, 'Critical hit chance - projectiles', ['+#% to Critical Hit Chance', 'Projectiles have (#-#)% increased Critical Hit Chance against Enemies further than 6m']).
exclusion_group(poe2, excl_34, 'Bow additional arrows (bow only)', ['Bow Attacks fire 2 additional Arrows', 'Bow Attacks fire an additional Arrow']).
exclusion_group(poe2, excl_35, 'Spell damage variations - per stat', ['#% increased Spell Damage', '(#-#)% increased Spell Damage per 100 Maximum Life', '(#-#)% increased Spell Damage per 100 maximum Mana', '(#-#)% increased Spell Damage with Spells that cost Life']).
exclusion_group(poe2, excl_36, 'Crossbow additional bolts (crossbow only)', ['Loads 2 additional bolts', 'Loads an additional bolt']).
exclusion_group(poe2, excl_37, 'Crossbow reload mechanics (crossbow only)', ['(#-#)% chance when you Reload a Crossbow to be immediate', '(#-#)% increased Reload Speed']).
exclusion_group(poe2, excl_38, 'Recover when expend combo', ['Recover (#-#)% of Maximum Life when you expend at least 10 Combo', 'Recover (#-#)% of Maximum Mana when you expend at least 10 Combo']).
exclusion_group(poe2, excl_39, 'Global defences', ['#% increased Global Defences', '#% increased Global Defences']).
