%%% ==========================================================================
%%% poe2_crafting.pl — PoE 2 Crafting Knowledge Base
%%% ==========================================================================
%%% A formal model of PoE 2 item state and currency transitions.
%%% Loads in SWI-Prolog:  [poe2_crafting].
%%%
%%% Structure:
%%%   1. Primitives (rarity, properties, mod slots, tags, tiers, influence, bases)
%%%   2. Placeholder mod database
%%%   3. Item state representation
%%%   4. Currency preconditions / postconditions
%%%   5. can_apply/2 and apply_currency/3
%%%   6. Example items and queries
%%% ==========================================================================

:- module(poe2_crafting, [
    % --- rarity ---
    rarity/1,
    max_prefixes/2,
    max_suffixes/2,

    % --- properties ---
    item_property/1,
    blocks_modification/2,

    % --- quality ---
    quality_type/2,
    quality_max/2,
    quality_effect/4,

    % --- omens ---
    omen/4,
    can_use_omen/2,
    omen_active/3,
    omen_disabled/2,
    omen_crafting_pairs/3,

    % --- alloys ---
    alloy/3,
    alloy_precondition/2,
    alloy_postcondition/3,

    % --- mod slots ---
    slot_type/1,
    mod_is_prefix/2,
    mod_is_suffix/2,

    % --- mod data ---
    mod_group/8,
    mod_tags/3,
    mod_tier_available/2,
    mod_tier_detail/5,
    mod_domain/3,
    mod_weight/3,
    mod_pool_weight_sum/3,
    roll_probability/3,

    % --- influence ---
    influence_type/1,

    % --- base types ---
    base_type/2,
    base_implicit/2,
    base_category/2,
    base_mod_pool/2,
    mod_pool/3,

    % --- currency catalogue ---
    currency/1,
    currency_precondition/2,
    currency_postcondition/3,

    % --- core engine ---
    item_state/8,
    can_apply/2,
    apply_currency/3,

    % --- helpers ---
    count_mods/3,
    has_open_slot/2,
    roll_mod/4,
    roll_n_mods/6,
    roll_prefixes/4,
    roll_suffixes/4,
    random_mod_for_slot/5
]).


%% ==========================================================================
%% VERSION STATUS: Path of Exile 2 — Patch 0.5.0 (Return of the Ancients)
%% Released: 2026-05-28
%% ==========================================================================
%% This knowledge base reflects the 0.5.0 crafting system.
%% Key facts:
%%   - 8 omens disabled (see omen_disabled/2)
%%   - Alloys introduced (13 types, replace Entities/Recombination)
%%   - Desecrated modifiers: 1 per item, separate from crafted modifier
%%   - Crafted modifier limit: 1 per item
%%   - Recombination disabled
%%   - Expedition temporarily integrated into Runes of Aldur
%%   - Essence nerfs: Perfect Essence of Battle, Essence of Hysteria
%% ==========================================================================

:- use_module(library(lists)).
:- use_module(library(random)).
:- use_module(library(aggregate)).

%%% ==========================================================================
%%% 1. PRIMITIVES
%%% ==========================================================================

%% --- 1a. Rarity ---

rarity(normal).
rarity(magic).
rarity(rare).
rarity(unique).

max_prefixes(normal, 0).
max_prefixes(magic,  1).
max_prefixes(rare,   3).
max_prefixes(unique, 0).  % uniques have fixed mods, not counted

max_suffixes(normal, 0).
max_suffixes(magic,  1).
max_suffixes(rare,   3).
max_suffixes(unique, 0).

%% --- 1b. Item Properties ---

item_property(identified).
item_property(corrupted).
item_property(mirrored).
item_property(fractured).
item_property(influenced).
item_property(synthesised).
item_property(sanctified).        % from Omen of Sanctification
item_property(desecrated).        % has desecrated modifiers

%% --- 1b2. Quality System ---
%% Quality increases modifier magnitude for matching tags.
%% Applied via Catalysts (rings/amulets) or Whetstones/Scrap (weapons/armour).
%% Does NOT affect mod weights — only post-roll numeric values.

quality_type(armourer_scrap,   [armour, evasion, energy_shield, runic_ward]).
quality_type(blacksmith_whetstone, [physical]).
quality_type(arcanist_etcher,  [gem_level]).
quality_type(flesh_catalyst,   [life]).
quality_type(neural_catalyst,  [mana]).
quality_type(carapace_catalyst,[armour, evasion, energy_shield]).
quality_type(uul_netol_catalyst, [physical]).
quality_type(xophs_catalyst,   [fire]).
quality_type(tuls_catalyst,    [cold]).
quality_type(eshs_catalyst,    [lightning]).
quality_type(chayulas_catalyst,[chaos]).
quality_type(reaver_catalyst,  [attack]).
quality_type(sibilant_catalyst,[caster]).
quality_type(skittering_catalyst, [speed]).
quality_type(adaptive_catalyst,[attribute]).

%% Quality caps by item type
quality_max(ring,              20).
quality_max(breach_ring,       40).
quality_max(refined_breach_ring, 45).
quality_max(amulet,            20).
quality_max(belt,              0).   % belts CANNOT have quality in PoE 2
quality_max(weapon,            20).
quality_max(body_armour,       20).
quality_max(helmet,            20).
quality_max(gloves,            20).
quality_max(boots,             20).
quality_max(shield,            20).

%% quality_effect(+QualityPercent, +ModTags, +CatalystType, -MagnitudeMultiplier)
%%   1% quality = 1% increased modifier magnitude for matching tags.
%%   Multiplier = 1 + (quality/100) if any mod tag matches catalyst tags.
quality_effect(QualityPct, ModTags, CatalystType, Multiplier) :-
    quality_type(CatalystType, CatalystTags),
    (   member(Tag, ModTags), member(Tag, CatalystTags)
    ->  Multiplier is 1 + QualityPct / 100
    ;   Multiplier = 1.0
    ).

%% --- 1b3. Omens ---
%% Omens modify the behavior of the next currency orb used.
%% Right-click to activate, stays in inventory until triggered, consumed on use.
%%
%% omen(+Name, +TargetCurrency, +Effect, +SlotRestriction)
%%   SlotRestriction: prefix | suffix | both | none | specific

% Sinistral/Dextral pairs — the core of deterministic crafting
omen(sinistral_erasure,     chaos_orb,      removes_only_prefixes,       prefix).
omen(dextral_erasure,       chaos_orb,      removes_only_suffixes,       suffix).
omen(sinistral_alchemy,  % DISABLED 0.3-0.5     orb_of_alchemy, max_prefixes,                prefix).
omen(dextral_alchemy,  % DISABLED 0.3-0.5       orb_of_alchemy, max_suffixes,                suffix).
omen(sinistral_coronation,  % DISABLED 0.3-0.5  regal_orb,      adds_only_prefixes,          prefix).
omen(dextral_coronation,  % DISABLED 0.3-0.5    regal_orb,      adds_only_suffixes,          suffix).
omen(sinistral_exaltation,  exalted_orb,    adds_only_prefixes,          prefix).
omen(dextral_exaltation,    exalted_orb,    adds_only_suffixes,          suffix).
omen(sinistral_annulment,   orb_of_annulment, removes_only_prefixes,     prefix).
omen(dextral_annulment,     orb_of_annulment, removes_only_suffixes,     suffix).
omen(sinistral_crystallisation, essence,    removes_only_prefixes,       prefix).
omen(dextral_crystallisation,   essence,    removes_only_suffixes,       suffix).
omen(sinistral_necromancy,  desecration,    adds_only_prefixes,          prefix).
omen(dextral_necromancy,    desecration,    adds_only_suffixes,          suffix).

% Power omens
omen(greater_exaltation,    exalted_orb,    adds_two_mods,               both).
omen(greater_annulment,  % DISABLED 0.3-0.5     orb_of_annulment, removes_two_mods,          both).
omen(homogenising_exaltation,  % DISABLED 0.3-0.5 exalted_orb,  adds_same_tag_mod,           both).
omen(homogenising_coronation,  % DISABLED 0.3-0.5 regal_orb,    adds_same_tag_mod,           both).
omen(catalysing_exaltation, exalted_orb,    consumes_quality_for_targeting, both).
omen(whittling,             chaos_orb,      removes_lowest_level_mod,    both).

% Special omens
omen(omen_of_chance,        orb_of_chance,  wont_destroy_item,           both).
omen(omen_of_the_ancients,  orb_of_chance,  upgrades_to_random_unique,   both).
omen(omen_of_blessed,       divine_orb,     rerolls_implicit_only,       both).
omen(omen_of_sanctification, divine_orb,    sanctifies_item,             both).
omen(omen_of_corruption,  % DISABLED 0.3-0.5    vaal_orb,       always_changes,              both).
omen(omen_of_light,         orb_of_annulment, removes_desecrated_only,   both).
omen(omen_of_putrefaction,  desecration,    replaces_all_mods_and_corrupts, both).
omen(omen_of_recombination,  % DISABLED 0.3-0.5 recombination,  enables_recombination,       both).

% Abyssal desecration omens
omen(omen_of_sovereign,     desecration,    guarantees_ulaman_mod,       both).
omen(omen_of_liege,         desecration,    guarantees_amanamu_mod,      both).
omen(omen_of_blackblooded,  desecration,    guarantees_kurgal_mod,       both).
omen(omen_of_abyssal_echoes, desecration,   reroll_desecrated_options,   both).

%% --- Disabled Omens (as of 0.5.0) ---
%% These can no longer drop but existing ones may still function.
omen_disabled(omen_of_corruption,        '0.5.0').
omen_disabled(dextral_alchemy,           '0.3.0').
omen_disabled(sinistral_alchemy,         '0.3.0').
omen_disabled(dextral_coronation,        '0.3.0').
omen_disabled(sinistral_coronation,      '0.3.0').
omen_disabled(greater_annulment,         '0.3.0').
omen_disabled(homogenising_coronation,   '0.4.0').
omen_disabled(homogenising_exaltation,   '0.4.0').
omen_disabled(omen_of_recombination,     '0.5.0').  % Recombinator disabled entirely

%% can_use_omen(+OmenName, +Currency)
%%   An omen can be used with a currency if the currency_target matches.
%%   Excludes disabled omens (can still exist in Standard but cannot drop).
can_use_omen(OmenName, Currency) :-
    omen(OmenName, Currency, _, _),
    \+ omen_disabled(OmenName, _).
can_use_omen(OmenName, Currency) :-
    omen(OmenName, any_currency, _, _),
    \+ omen_disabled(OmenName, _).

%% omen_active(+OmenName, -Effect, -SlotRestriction)
%%   Only returns omens that can still drop in 0.5.0.
omen_active(OmenName, Effect, Slot) :-
    omen(OmenName, _, Effect, Slot),
    \+ omen_disabled(OmenName, _).

%% omen_crafting_pairs(+Currency, -Sinistral, -Dextral)
%%   Returns the sinistral/dextral pair for a currency, if both are active.
omen_crafting_pairs(Currency, Sinistral, Dextral) :-
    omen_active(sinistral_omen, removes_only_prefixes, prefix),
    omen_active(dextral_omen, removes_only_suffixes, suffix),
    omen(sinistral_omen, Currency, removes_only_prefixes, prefix),
    omen(dextral_omen, Currency, removes_only_suffixes, suffix),
    Sinistral = sinistral_omen,
    Dextral = dextral_omen.

%% --- 1b4. Alloys ---
%% Alloys are a PoE 2 patch 0.5 crafting currency.
%% Apply to rare item → removes one random mod → adds a guaranteed mod.
%% Obtained from Remnant encounters or rune recipes.
%%
%% alloy(+Name, +GuaranteedModTag, +Description)

alloy(runic_alloy,          runic_ward,     'Adds Runic Ward modifier').
alloy(adaptive_alloy,       attribute,      'Adds attribute modifier').
alloy(protective_alloy,     defence,        'Adds defence modifier').
alloy(expansive_alloy,      life,           'Adds life modifier').
alloy(swift_alloy,          speed,          'Adds speed modifier').
alloy(cyclonic_alloy,       physical,       'Adds physical modifier').
alloy(prismatic_alloy,      elemental,      'Adds elemental modifier').
alloy(mystic_alloy,         caster,         'Adds caster modifier').
alloy(sovereign_alloy,      attack,         'Adds attack modifier').
alloy(celestial_alloy,      resistance,     'Adds resistance modifier').
alloy(transcendent_alloy,   gem_level,      'Adds gem level modifier').
alloy(runebinder_alloy,     rune,           'Adds rune modifier').
alloy(runefather_alloy,     rune,           'Adds enhanced rune modifier').

%% alloy_precondition(+AlloyName, +ItemState)
%%   Alloys only work on rare items that are not corrupted/mirrored.
alloy_precondition(_, item_state(_, rare, _, _, Props, _, _, _)) :-
    \+ member(corrupted, Props),
    \+ member(mirrored, Props).

%% alloy_postcondition(+AlloyName, +OldItemState, -NewItemState)
%%   Removes one random mod, adds a guaranteed mod matching the alloy's tag.
%%   Simplified: we model it as removing a random mod and marking the item.
alloy_postcondition(AlloyName,
    item_state(Base, rare, Ilvl, Inf, Props, OldPre, OldSuf, Impl),
    item_state(Base, rare, Ilvl, Inf, Props, NewPre, NewSuf, Impl)) :-
    alloy(AlloyName, _, _),
    append(OldPre, OldSuf, AllMods),
    AllMods \= [],
    random_member(_Removed, AllMods),
    % Remove one mod (simplified — real implementation tracks specific mod)
    (   OldPre \= []
    ->  select(_R1, OldPre, NewPre), NewSuf = OldSuf
    ;   select(_R2, OldSuf, NewSuf), NewPre = OldPre
    ).
    % NOTE: In full implementation, the removed mod is random and the
    % added mod is guaranteed to have the alloy's tag.

% blocks_modification(+Property, +Currency)
%   Mirrored blocks everything.  Corrupted blocks everything except tainted.
blocks_modification(mirrored, _).
blocks_modification(corrupted, Currency) :-
    \+ is_tainted_currency(Currency).

is_tainted_currency(tainted_currency_orb).
is_tainted_currency(tainted_armourers_scrap).
is_tainted_currency(tainted_blacksmith_whetstone).
is_tainted_currency(tainted_chaos_orb).
is_tainted_currency(tainted_exalted_orb).
is_tainted_currency(tainted_annulment_orb).

%% --- 1c. Modifier Slots ---

slot_type(prefix).
slot_type(suffix).
slot_type(implicit).
slot_type(enchantment).
slot_type(rune).

%% --- 1d. Mod Tags ---
%% Tags are now stored in mod_group/8 (field 4: Tags list).
%% Convenience accessor:
mod_tags(Category, ModGroup, Tags) :-
    mod_group(Category, ModGroup, _, Tags, _, _, _, _).

%% --- 1e. Mod Tiers ---
%% Tier details stored in mod_tier_detail/5 (see Section 2d).
mod_tier_available(ModGroup, Ilvl) :-
    mod_tier_detail(ModGroup, _, _, TierIlvl, _),
    Ilvl >= TierIlvl.

%% --- 1f. Mod Domain (prefix vs suffix) ---
%% Slot is now stored in mod_group/8 (field 8: Slot).
mod_domain(Category, ModGroup, Slot) :-
    mod_group(Category, ModGroup, _, _, _, _, _, Slot).

mod_is_prefix(Cat, Mod) :- mod_domain(Cat, Mod, prefix).
mod_is_suffix(Cat, Mod) :- mod_domain(Cat, Mod, suffix).

%% --- 1g. Influence Types ---

influence_type(shaper).
influence_type(elder).
influence_type(crusader).
influence_type(redeemer).
influence_type(hunter).
influence_type(warlord).
influence_type(none).

%% --- 1h. Base Types ---
% base_type(+BaseId, -info(Game, Category, ImplicitDesc))

base_type(spirit_blade,   info(poe2, weapon,      'Adds 12-18 Physical Damage')).
base_type(karui_chopper,  info(poe2, weapon,      'Adds 16-24 Physical Damage')).
base_type(lapis_amulet,   info(poe2, amulet,      '+22-30 to Intelligence')).
base_type(jade_ring,      info(poe2, ring,        '+20-30 to Dexterity')).
base_type(iron_ring,      info(poe2, ring,        'Adds 1-4 Physical Damage to Attacks')).
base_type(vaal_buckler,   info(poe2, shield,      '+3% to Chance to Block')).
base_type(lacquered_garb, info(poe2, body_armour, '74-86 Evasion Rating')).
base_type(plate_vest,     info(poe2, body_armour, '15-20 Armour')).
base_type(iron_hat,       info(poe2, helmet,      '+6-12 Armour')).
base_type(trapper_gloves, info(poe2, gloves,      '+14-20 Evasion Rating')).
base_type(iron_greaves,   info(poe2, boots,       '+6-12 Armour')).
base_type(cobalt_jewel,   info(poe2, jewel,       none)).
base_type(heavy_belt,     info(poe2, belt,        '+20-30 to Strength')).

% Convenience accessors
base_implicit(BaseId, Implicit) :-
    base_type(BaseId, info(_, _, Implicit)).
base_category(BaseId, Category) :-
    base_type(BaseId, info(_, Category, _)).

%% --- 1i. Category → Mod Pool Mapping ---
%% Maps base_type category to the specific mod pool category.
%% This is needed because e.g. "helmet" can be str/dex/int variant,
%% each with different mod pools.
%%
%% mod_pool(+BaseCategory, +Variant, -ModPoolCategory)
%%   Variant is str, dex, int, str_dex, str_int, dex_int, str_dex_int
%%   For items without variants (rings, amulets), variant = none.

mod_pool(body_armour, str,       body_armour_str).
mod_pool(body_armour, dex,       body_armour_dex).     % not yet scraped
mod_pool(body_armour, int,       body_armour_int).     % not yet scraped
mod_pool(helmet,     str,       helmet_str).
mod_pool(gloves,     str,       gloves_str).
mod_pool(boots,      str,       boots_str).
mod_pool(ring,       none,      ring).
mod_pool(amulet,     none,      amulet).
mod_pool(weapon,     str_dex,   weapon_sword).         % 1H swords are str_dex

%% Default variant lookup (for when we don't care about variant):
%% base_mod_pool(+BaseId, -ModPoolCategory)
base_mod_pool(BaseId, ModPool) :-
    base_category(BaseId, Cat),
    (   mod_pool(Cat, none, ModPool)
    ->  true
    ;   mod_pool(Cat, str, ModPool)   % default to str variant
    ).


%%% ==========================================================================
%%% 2. MOD DATABASE — from poe2db.tw (7 categories)
%%% ==========================================================================
%%% Each mod group has:
%%%   mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)
%%%
%%% Weight determines roll probability relative to other mods in the same pool.
%%% Categories: body_armour_str, helmet_str, gloves_str, boots_str,
%%%             ring, amulet, weapon_sword
%%%
%%% Per-category data files are in resources/mods_*.pl.
%%% Load the ones you need:
%%%   :- consult('resources/mods_ring.pl').
%%%   :- consult('resources/mods_amulet.pl').
%%%   etc.

%% --- 2a. Load all category data files ---

:- consult('resources/mods_body_armour_str.pl').
:- consult('resources/mods_helmet_str.pl').
:- consult('resources/mods_gloves_str.pl').
:- consult('resources/mods_boots_str.pl').
:- consult('resources/mods_ring.pl').
:- consult('resources/mods_amulet.pl').
:- consult('resources/mods_weapon_sword.pl').

%% --- 2b. Mod Weight (convenience lookup) ---
mod_weight(Category, ModGroup, Weight) :-
    mod_group(Category, ModGroup, _, _, Weight, _, _, _).

%% --- 2c. Roll Probability ---
%% roll_probability(+Category, +ModGroup, -Prob)
roll_probability(Category, ModGroup, Prob) :-
    mod_group(Category, ModGroup, _, _, Weight, _, _, Slot),
    mod_pool_weight_sum(Category, Slot, Total),
    Prob is Weight / Total.

%% --- 2d. Life Prefix Tiers (complete data from poe2db) ---
%%   mod_tier_detail(+ModGroup, +Tier, +Name, +MinIlvl, +Range)

mod_tier_detail(increased_life, 13, hale,       1,  10-19).
mod_tier_detail(increased_life, 12, healthy,    5,  20-29).
mod_tier_detail(increased_life, 11, vigorous,   11, 30-39).
mod_tier_detail(increased_life, 10, rugged,     18, 40-49).
mod_tier_detail(increased_life,  9, robust,     24, 50-59).
mod_tier_detail(increased_life,  8, stalwart,   30, 60-69).
mod_tier_detail(increased_life,  7, sturdy,     36, 70-79).
mod_tier_detail(increased_life,  6, hearty,     42, 80-89).
mod_tier_detail(increased_life,  5, fiery,      48, 90-99).
mod_tier_detail(increased_life,  4, strapping,  54, 100-109).
mod_tier_detail(increased_life,  3, athletes,   60, 110-129).
mod_tier_detail(increased_life,  2, fecund,     70, 130-169).
mod_tier_detail(increased_life,  1, prime,      80, 170-214).

%% --- 2e. Roll Ranges (T1-T2 for key mods) ---

mod_roll_range(inc_life_t1,               170, 214).
mod_roll_range(inc_life_t2,               130, 169).
mod_roll_range(inc_life_t3,               110, 129).

mod_roll_range(fire_res_t1,                41,  45).
mod_roll_range(fire_res_t2,                36,  40).
mod_roll_range(cold_res_t1,                41,  45).
mod_roll_range(cold_res_t2,                36,  40).
mod_roll_range(lightning_res_t1,           41,  45).
mod_roll_range(lightning_res_t2,           36,  40).
mod_roll_range(chaos_res_t1,               24,  27).
mod_roll_range(chaos_res_t2,               18,  23).

mod_roll_range(strength_t1,                31,  33).
mod_roll_range(strength_t2,                28,  30).


%%% ==========================================================================
%%% 3. ITEM STATE REPRESENTATION
%%% ==========================================================================

%% item_state(BaseId, Rarity, Ilvl, Influence, Properties, Prefixes, Suffixes, Implicit)
%% item_state(BaseId, Rarity, Ilvl, Influence, Properties, Prefixes, Suffixes, Implicit)
%%   BaseId      - atom identifying the base type (see base_type/2)
%%   Rarity      - normal | magic | rare | unique
%%   Ilvl        - integer item level
%%   Influence   - atom from influence_type/1 (or none)
%%   Properties  - list of item_property atoms
%%   Prefixes    - list of prefix mod group atoms (max 3 on rare)
%%   Suffixes    - list of suffix mod group atoms (max 3 on rare)
%%   Implicit    - atom: implicit(BaseImplicitDesc) or none
%%
%% NOTE: Quality is tracked separately via item_quality/3:
%%   item_quality(ItemId, CatalystType, QualityPercent)
%%
%% Example: a rare spirit blade, ilvl 86, no influence, identified,
%%          with t1 life + t2 fire res as prefixes, t1 crit multi as suffix.

sample_item(Item) :-
    Item = item_state(
        spirit_blade,                              % base
        rare,                                       % rarity
        86,                                         % ilvl
        none,                                       % influence
        [identified],                               % properties
        [increased_life, fire_resistance],           % prefixes (mod group names)
        [strength],                                  % suffixes
        implicit('Adds 12-18 Physical Damage')      % implicit
    ).

%% A normal item (just transmuted base, ready for crafting):
fresh_base(Item) :-
    Item = item_state(
        spirit_blade,
        normal,
        86,
        none,
        [],
        [],
        [],
        implicit('Adds 12-18 Physical Damage')
    ).

%% A magic item (after transmutation):
magic_item(Item) :-
    Item = item_state(
        spirit_blade,
        magic,
        86,
        none,
        [identified],
        [increased_life],
        [fire_resistance],
        implicit('Adds 12-18 Physical Damage')
    ).


%%% ==========================================================================
%%% 4. HELPER PREDICATES
%%% ==========================================================================

%% count_mods(+ItemState, +Slot, -Count)
count_mods(item_state(_, _, _, _, _, Prefixes, _, _), prefix, N) :-
    length(Prefixes, N).
count_mods(item_state(_, _, _, _, _, _, Suffixes, _), suffix, N) :-
    length(Suffixes, N).

%% has_open_slot(+ItemState, +SlotType)
has_open_slot(Item, prefix) :-
    Item = item_state(_, Rarity, _, _, _, Prefixes, _, _),
    max_prefixes(Rarity, Max),
    length(Prefixes, N),
    N < Max.
has_open_slot(Item, suffix) :-
    Item = item_state(_, Rarity, _, _, _, _, Suffixes, _),
    max_suffixes(Rarity, Max),
    length(Suffixes, N),
    N < Max.

%% rollable_group(+Category, +ModGroup, +Ilvl)
%%   A mod group can roll if ilvl is within range.
rollable_group(Category, ModGroup, Ilvl) :-
    mod_group(Category, ModGroup, _, _, _, MaxIlvl, _, _),
    Ilvl =< MaxIlvl.

%% roll_mod(+Category, +Slot, +Ilvl, -ModGroup)
%%   Pick a random mod group for the given slot, weighted by poe2db weights.
roll_mod(Category, Slot, Ilvl, ModGroup) :-
    findall(W-G, (
        mod_group(Category, G, _, _, W, _, _, Slot),
        rollable_group(Category, G, Ilvl)
    ), WeightedPairs),
    WeightedPairs \= [],
    weighted_pairs_to_list(WeightedPairs, Candidates),
    random_member(ModGroup, Candidates).

%% weighted_pairs_to_list(+WeightedPairs, -FlatList)
weighted_pairs_to_list([], []).
weighted_pairs_to_list([W-G|Rest], Expanded) :-
    length(OneGroup, W),
    maplist(=(G), OneGroup),
    weighted_pairs_to_list(Rest, RestExpanded),
    append(OneGroup, RestExpanded, Expanded).

%% random_mod_for_slot(+Category, +Slot, +Ilvl, +ExistingGroups, -NewGroup)
random_mod_for_slot(Category, Slot, Ilvl, Existing, NewGroup) :-
    findall(W-G, (
        mod_group(Category, G, _, _, W, _, _, Slot),
        rollable_group(Category, G, Ilvl),
        \+ member(G, Existing)
    ), WeightedPairs),
    (   WeightedPairs \= []
    ->  weighted_pairs_to_list(WeightedPairs, Candidates),
        random_member(NewGroup, Candidates)
    ;   roll_mod(Category, Slot, Ilvl, NewGroup)
    ).

%% roll_n_mods(+Category, +Slot, +Ilvl, +AlreadyPicked, +N, -Groups)
roll_n_mods(_, _, _, _, 0, []) :- !.
roll_n_mods(Category, Slot, Ilvl, Already, N, [Group|Rest]) :-
    N > 0,
    random_mod_for_slot(Category, Slot, Ilvl, Already, Group),
    N1 is N - 1,
    roll_n_mods(Category, Slot, Ilvl, [Group|Already], N1, Rest).

%% roll_prefixes(+Category, +Ilvl, +SeedGroups, -FinalGroups)
roll_prefixes(Category, Ilvl, Seed, Final) :-
    length(Seed, SeedN),
    Remaining is 3 - SeedN,
    (   Remaining > 0
    ->  random_between(0, Remaining, ExtraN),
        roll_n_mods(Category, prefix, Ilvl, Seed, ExtraN, Extra),
        append(Seed, Extra, Final)
    ;   Final = Seed
    ).

%% roll_suffixes(+Category, +Ilvl, +PrefixGroups, -SuffixGroups)
roll_suffixes(Category, Ilvl, _Prefixes, Suffixes) :-
    random_between(1, 3, N),
    roll_n_mods(Category, suffix, Ilvl, [], N, Suffixes).


%%% ==========================================================================
%%% 5. CURRENCY TRANSITION RULES
%%% ==========================================================================

%% currency(+Name)
%%   Complete catalogue of implemented currencies.

currency(orb_of_transmutation).
currency(orb_of_alteration).
currency(orb_of_alchemy).
currency(chaos_orb).
currency(regal_orb).
currency(exalted_orb).
currency(orb_of_annulment).
currency(orb_of_scouring).
currency(divine_orb).
currency(vaal_orb).
currency(orb_of_augmentation).
currency(orb_of_chance).
% currency(fusing_orb).  % removed — PoE 1 only
% currency(jewellers_orb).  % removed — PoE 1 only
% currency(chromatic_orb).  % removed — PoE 1 only
currency(essence_of_greed).
currency(essence_of_wrath).
currency(fracturing_orb).


%% ---------- Orb of Transmutation ----------
%% normal → magic, roll 1 prefix + 1 suffix (or 1-2 of one type)

currency_precondition(orb_of_transmutation, item_state(_, normal, _, _, Props, [], [], _)) :-
    \+ member(corrupted, Props),
    \+ member(mirrored, Props).

currency_postcondition(orb_of_transmutation,
    item_state(Base, normal, Ilvl, Inf, Props, [], [], Impl),
    item_state(Base, magic, Ilvl, Inf, [identified|NewProps], [NewPre], [NewSuf], Impl)) :-
    subtract(Props, [identified], Props0),
    NewProps = [identified|Props0],
    base_mod_pool(Base, Cat),
    random_mod_for_slot(Cat, prefix, Ilvl, [], NewPre),
    random_mod_for_slot(Cat, suffix, Ilvl, [NewPre], NewSuf).

%% ---------- Orb of Alteration ----------
%% magic → magic (reroll), 1 prefix + 1 suffix

currency_precondition(orb_of_alteration, item_state(_, magic, _, _, Props, _, _, _)) :-
    \+ member(corrupted, Props),
    \+ member(mirrored, Props).

currency_postcondition(orb_of_alteration,
    item_state(Base, magic, Ilvl, Inf, Props, _, _, Impl),
    item_state(Base, magic, Ilvl, Inf, [identified|NewProps], [NewPre], [NewSuf], Impl)) :-
    include(\==(identified), Props, Props0),
    NewProps = [identified|Props0],
    base_mod_pool(Base, Cat),
    random_mod_for_slot(Cat, prefix, Ilvl, [], NewPre),
    random_mod_for_slot(Cat, suffix, Ilvl, [NewPre], NewSuf).

%% ---------- Orb of Alchemy ----------
%% normal → rare, 4-6 mods (3 pre + 3 suf max)

currency_precondition(orb_of_alchemy, item_state(_, normal, _, _, Props, [], [], _)) :-
    \+ member(corrupted, Props),
    \+ member(mirrored, Props).

currency_postcondition(orb_of_alchemy,
    item_state(Base, normal, Ilvl, Inf, Props, [], [], Impl),
    item_state(Base, rare, Ilvl, Inf, [identified|NewProps], NewPrefixes, NewSuffixes, Impl)) :-
    include(\==(identified), Props, Props0),
    NewProps = [identified|Props0],
    base_mod_pool(Base, Cat),
    roll_prefixes(Cat, Ilvl, [], NewPrefixes),
    roll_suffixes(Cat, Ilvl, NewPrefixes, NewSuffixes).

%% ---------- Chaos Orb ----------
%% rare → rare (reroll all mods)

currency_precondition(chaos_orb, item_state(_, rare, _, _, Props, _, _, _)) :-
    \+ member(corrupted, Props),
    \+ member(mirrored, Props).

currency_postcondition(chaos_orb,
    item_state(Base, rare, Ilvl, Inf, Props, _, _, Impl),
    item_state(Base, rare, Ilvl, Inf, [identified|NewProps], NewPrefixes, NewSuffixes, Impl)) :-
    include(\==(identified), Props, Props0),
    NewProps = [identified|Props0],
    base_mod_pool(Base, Cat),
    roll_prefixes(Cat, Ilvl, [], NewPrefixes),
    roll_suffixes(Cat, Ilvl, NewPrefixes, NewSuffixes).

%% ---------- Regal Orb ----------
%% magic → rare, add 1 random mod

currency_precondition(regal_orb, item_state(_, magic, _, _, Props, _, _, _)) :-
    \+ member(corrupted, Props),
    \+ member(mirrored, Props).

currency_postcondition(regal_orb,
    item_state(Base, magic, Ilvl, Inf, Props, OldPre, OldSuf, Impl),
    item_state(Base, rare, Ilvl, Inf, [identified|NewProps], NewPre, NewSuf, Impl)) :-
    include(\==(identified), Props, Props0),
    NewProps = [identified|Props0],
    base_mod_pool(Base, Cat),
    random_member(Slot, [prefix, suffix]),
    (   Slot = prefix
    ->  random_mod_for_slot(Cat, prefix, Ilvl, OldPre, AddedPre),
        append(OldPre, [AddedPre], NewPre),
        NewSuf = OldSuf
    ;   random_mod_for_slot(Cat, suffix, Ilvl, OldSuf, AddedSuf),
        append(OldSuf, [AddedSuf], NewSuf),
        NewPre = OldPre
    ).

%% ---------- Exalted Orb ----------
%% rare + has open prefix OR open suffix → rare, add 1 random mod

currency_precondition(exalted_orb, Item) :-
    Item = item_state(_, rare, _, _, Props, Prefixes, Suffixes, _),
    \+ member(corrupted, Props),
    \+ member(mirrored, Props),
    (   has_open_slot(Item, prefix)
    ;   has_open_slot(Item, suffix)
    ).

currency_postcondition(exalted_orb,
    item_state(Base, rare, Ilvl, Inf, Props, OldPre, OldSuf, Impl),
    item_state(Base, rare, Ilvl, Inf, [identified|NewProps], NewPre, NewSuf, Impl)) :-
    include(\==(identified), Props, Props0),
    NewProps = [identified|Props0],
    length(OldPre, PreN),
    length(OldSuf, SufN),
    max_prefixes(rare, MaxPre),
    max_suffixes(rare, MaxSuf),
    base_mod_pool(Base, Cat),
    (   PreN < MaxPre, SufN < MaxSuf
    ->  random_member(Slot, [prefix, suffix])
    ;   PreN < MaxPre
    ->  Slot = prefix
    ;   Slot = suffix
    ),
    (   Slot = prefix
    ->  random_mod_for_slot(Cat, prefix, Ilvl, OldPre, AddedPre),
        append(OldPre, [AddedPre], NewPre),
        NewSuf = OldSuf
    ;   random_mod_for_slot(Cat, suffix, Ilvl, OldSuf, AddedSuf),
        append(OldSuf, [AddedSuf], NewSuf),
        NewPre = OldPre
    ).

%% ---------- Orb of Annulment ----------
%% magic or rare, has at least 1 mod → remove 1 random mod

currency_precondition(orb_of_annulment, item_state(_, Rarity, _, _, Props, Prefixes, Suffixes, _)) :-
    \+ member(corrupted, Props),
    \+ member(mirrored, Props),
    memberchk(Rarity, [magic, rare]),
    append(Prefixes, Suffixes, All),
    All \= [].

currency_postcondition(orb_of_annulment,
    item_state(Base, Rarity, Ilvl, Inf, Props, OldPre, OldSuf, Impl),
    item_state(Base, Rarity, Ilvl, Inf, Props, NewPre, NewSuf, Impl)) :-
    append(OldPre, OldSuf, All),
    random_member(Removed, All),
    (   member(Removed, OldPre)
    ->  select(Removed, OldPre, NewPre),
        NewSuf = OldSuf
    ;   select(Removed, OldSuf, NewSuf),
        NewPre = OldPre
    ).

%% ---------- Orb of Scouring ----------
%% magic or rare → normal, remove all mods

currency_precondition(orb_of_scouring, item_state(_, Rarity, _, _, Props, _, _, _)) :-
    \+ member(corrupted, Props),
    \+ member(mirrored, Props),
    memberchk(Rarity, [magic, rare]).

currency_postcondition(orb_of_scouring,
    item_state(Base, _, Ilvl, Inf, Props, _, _, Impl),
    item_state(Base, normal, Ilvl, Inf, NewProps, [], [], Impl)) :-
    include(\==(identified), Props, NewProps).

%% ---------- Divine Orb ----------
%% reroll numeric values of existing mods (mod list unchanged)

currency_precondition(divine_orb, item_state(_, Rarity, _, _, Props, Prefixes, Suffixes, _)) :-
    \+ member(corrupted, Props),
    \+ member(mirrored, Props),
    memberchk(Rarity, [magic, rare, unique]),
    append(Prefixes, Suffixes, All),
    All \= [].  % must have mods to reroll

% Divine preserves mod IDs; only numeric ranges change.
% In this formal model we represent that as an identity transform on the mod list.
currency_postcondition(divine_orb,
    item_state(Base, Rarity, Ilvl, Inf, Props, Pre, Suf, Impl),
    item_state(Base, Rarity, Ilvl, Inf, Props, Pre, Suf, Impl)).

%% ---------- Vaal Orb ----------
%% Not corrupted → random corruption effect

currency_precondition(vaal_orb, item_state(_, _, _, _, Props, _, _, _)) :-
    \+ member(corrupted, Props),
    \+ member(mirrored, Props).

% Simplified: Vaal always corrupts.  Real PoE 2 has 4 possible outcomes.
% We model the most common: item becomes corrupted with mods unchanged.
currency_postcondition(vaal_orb,
    item_state(Base, Rarity, Ilvl, Inf, Props, Pre, Suf, Impl),
    item_state(Base, Rarity, Ilvl, Inf, [corrupted|NewProps], Pre, Suf, Impl)) :-
    include(\==(corrupted), Props, NewProps).

%% ---------- Orb of Augmentation ----------
%% magic + has open slot → magic, add 1 mod to that slot

currency_precondition(orb_of_augmentation, item_state(_, magic, _, _, Props, Prefixes, Suffixes, _)) :-
    \+ member(corrupted, Props),
    \+ member(mirrored, Props),
    (   has_open_slot(item_state(_, magic, _, _, Props, Prefixes, Suffixes, _), prefix)
    ;   has_open_slot(item_state(_, magic, _, _, Props, Prefixes, Suffixes, _), suffix)
    ).

currency_postcondition(orb_of_augmentation,
    item_state(Base, magic, Ilvl, Inf, Props, OldPre, OldSuf, Impl),
    item_state(Base, magic, Ilvl, Inf, [identified|NewProps], NewPre, NewSuf, Impl)) :-
    include(\==(identified), Props, Props0),
    NewProps = [identified|Props0],
    length(OldPre, PreN),
    max_prefixes(magic, MaxPre),
    base_mod_pool(Base, Cat),
    (   PreN < MaxPre
    ->  random_mod_for_slot(Cat, prefix, Ilvl, OldPre, Added),
        append(OldPre, [Added], NewPre),
        NewSuf = OldSuf
    ;   random_mod_for_slot(Cat, suffix, Ilvl, OldSuf, Added),
        append(OldSuf, [Added], NewSuf),
        NewPre = OldPre
    ).

%% ---------- Orb of Chance ----------
%% normal → random (normal / magic / rare / unique)

currency_precondition(orb_of_chance, item_state(_, normal, _, _, Props, [], [], _)) :-
    \+ member(corrupted, Props),
    \+ member(mirrored, Props).

currency_postcondition(orb_of_chance,
    item_state(Base, normal, Ilvl, Inf, Props, [], [], Impl),
    item_state(Base, NewRarity, Ilvl, Inf, FinalProps, FinalPre, FinalSuf, Impl)) :-
    base_mod_pool(Base, Cat),
    random_member(NewRarity, [normal, magic, rare]),
    (   NewRarity = normal
    ->  FinalProps = Props, FinalPre = [], FinalSuf = []
    ;   NewRarity = magic
    ->  FinalProps = [identified|Props],
        random_mod_for_slot(Cat, prefix, Ilvl, [], NewPre),
        random_mod_for_slot(Cat, suffix, Ilvl, [NewPre], NewSuf),
        FinalPre = [NewPre], FinalSuf = [NewSuf]
    ;   NewRarity = rare
    ->  FinalProps = [identified|Props],
        roll_prefixes(Cat, Ilvl, [], FinalPre),
        roll_suffixes(Cat, Ilvl, FinalPre, FinalSuf)
    ).

%% ---------- Essence of Greed ----------
%% On any rarity item: guarantees a life-tagged prefix. Here: force t1_life prefix.

currency_precondition(essence_of_greed, item_state(_, _, _, _, Props, _, _, _)) :-
    \+ member(corrupted, Props),
    \+ member(mirrored, Props).

currency_postcondition(essence_of_greed,
    item_state(Base, _, Ilvl, Inf, Props, _, Suffixes, Impl),
    item_state(Base, rare, Ilvl, Inf, [identified|NewProps], [increased_life|NewPre], Suffixes, Impl)) :-
    include(\==(identified), Props, Props0),
    NewProps = [identified|Props0],
    base_mod_pool(Base, Cat),
    roll_prefixes(Cat, Ilvl, [increased_life], NewPre).  % additional prefixes beyond the guaranteed one

%% ---------- Essence of Wrath ----------
%% Guarantees a lightning-tagged suffix.

currency_precondition(essence_of_wrath, item_state(_, _, _, _, Props, _, _, _)) :-
    \+ member(corrupted, Props),
    \+ member(mirrored, Props).

currency_postcondition(essence_of_wrath,
    item_state(Base, _, Ilvl, Inf, Props, Prefixes, _, Impl),
    item_state(Base, rare, Ilvl, Inf, [identified|NewProps], Prefixes, [lightning_resistance|NewSuf], Impl)) :-
    include(\==(identified), Props, Props0),
    NewProps = [identified|Props0],
    base_mod_pool(Base, Cat),
    roll_suffixes(Cat, Ilvl, Prefixes, NewSuf).

%% ---------- Fracturing Orb ----------
%% Locks one random mod as fractured.

currency_precondition(fracturing_orb, item_state(_, rare, _, _, Props, Prefixes, Suffixes, _)) :-
    \+ member(corrupted, Props),
    \+ member(mirrored, Props),
    \+ member(fractured, Props),
    append(Prefixes, Suffixes, All),
    All \= [].

currency_postcondition(fracturing_orb,
    item_state(Base, rare, Ilvl, Inf, Props, Prefixes, Suffixes, Impl),
    item_state(Base, rare, Ilvl, Inf, [fractured|NewProps], Prefixes, Suffixes, Impl)) :-
    include(\==(fractured), Props, NewProps).
    % NOTE: full implementation would mark a specific mod as fractured;
    % for now we add the fractured flag. Mod locking tracked externally.


%%% ==========================================================================
%%% 6. CORE ENGINE: can_apply/2 and apply_currency/3
%%% ==========================================================================

%% can_apply(+Currency, +ItemState)
%%   True if the currency's preconditions are satisfied for this item.
can_apply(Currency, Item) :-
    currency(Currency),
    currency_precondition(Currency, Item).

%% apply_currency(+Currency, +OldItemState, -NewItemState)
%%   Applies a currency to an item, producing the transformed item state.
%%   Fails if can_apply/2 fails.
apply_currency(Currency, OldItem, NewItem) :-
    can_apply(Currency, OldItem),
    currency_postcondition(Currency, OldItem, NewItem).


%%% ==========================================================================
%%% 7. EXAMPLE QUERIES (run at SWI-Prolog prompt)
%%% ==========================================================================

%!  ?- [poe2_crafting].
%!
%!  % Check if a currency can be applied:
%!  ?- sample_item(Item), can_apply(chaos_orb, Item).
%!
%!  % Transmute a normal base:
%!  ?- fresh_base(Item), apply_currency(orb_of_transmutation, Item, Magic).
%!
%!  % Regal a magic item to rare:
%!  ?- magic_item(Item), apply_currency(regal_orb, Item, Rare).
%!
%!  % Corrupt an item:
%!  ?- sample_item(Item), apply_currency(vaal_orb, Item, Corrupted).
%!
%!  % Alchemy a normal base:
%!  ?- fresh_base(Item), apply_currency(orb_of_alchemy, Item, Rare).
%!
%!  % Annul a random mod:
%!  ?- magic_item(Item), apply_currency(orb_of_annulment, Item, Result).
%!
%!  % Check roll probability of a mod group:
%!  ?- roll_probability(body_armour_str, increased_life, Prob).
%!  % Prob = 0.2407...
%!
%!  % Check what tags a mod has:
%!  ?- mod_tags(body_armour_str, fire_resistance, Tags).
%!  % Tags = [elemental, fire, resistance]
%!
%!  % List all suffix mod groups for rings:
%!  ?- mod_group(ring, G, Desc, _, W, _, _, suffix), format("~w: ~w (weight ~w)~n", [G, Desc, W]), fail.
%!
%!  % Compare Life prefix probability across categories:
%!  ?- roll_probability(Cat, increased_life, Prob), format("~w: ~4f~n", [Cat, Prob]), fail.
%
