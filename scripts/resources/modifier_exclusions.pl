%%% Auto-generated modifier exclusion facts from PathOfCrafting
%%% modifier_excluded_from(+StatPattern, +ExcludeFrom)
%%%   StatPattern uses '{}' as numeric wildcard.
%%%   These modifiers simply cannot roll on the listed item types.

%% ES hybrid mods should only appear on body armour, not boots/gloves/helmet
modifier_excluded_from('{}% increased Energy Shield, +{} to maximum Life', ['boots', 'gloves']).

%% ES hybrid mods should only appear on body armour, not boots/gloves/helmet
modifier_excluded_from('{}% increased Energy Shield, +{} to maximum Mana', ['boots', 'gloves']).

%% ES hybrid mods should only appear on body armour, not boots/gloves/helmet
modifier_excluded_from('+{} to maximum Energy Shield, {}% increased Energy Shield', ['boots', 'gloves']).
