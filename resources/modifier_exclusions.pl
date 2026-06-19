%% modifier_exclusions.pl — imported from POE2-PathOfCrafting
%% Specific modifiers excluded from certain base item types.
%% modifier_exclusion(+Game, +StatPattern, +ExcludeFromList, +Comment)

modifier_exclusion(poe2, '{}% increased Energy Shield, +{} to maximum Life', [boots, gloves], 'ES hybrid mods should only appear on body armour, not boots/gloves/helmet').
modifier_exclusion(poe2, '{}% increased Energy Shield, +{} to maximum Mana', [boots, gloves], 'ES hybrid mods should only appear on body armour, not boots/gloves/helmet').
modifier_exclusion(poe2, '+{} to maximum Energy Shield, {}% increased Energy Shield', [boots, gloves], 'ES hybrid mods should only appear on body armour, not boots/gloves/helmet').
