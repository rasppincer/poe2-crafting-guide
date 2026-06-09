# Primitives — The Building Blocks of PoE 2 Crafting

Everything in crafting is a **state machine**. An item sits in a state defined by
its properties. A currency orb (or bench craft) is a **transition** that requires
certain preconditions and produces postconditions.

This file defines the vocabulary. Future Prolog rules will consume these directly.

---

## 1. Item Rarity

The most fundamental property. Determines mod capacity and what currencies apply.

| Rarity   | Explicit Mod Capacity          | Notes                                      |
|----------|-------------------------------|-------------------------------------------|
| normal   | 0 prefixes, 0 suffixes        | No explicit mods. Base + implicit only.    |
| magic    | up to 1 prefix, 1 suffix      | Identified. Can be upgraded to rare.       |
| rare     | up to 3 prefixes, 3 suffixes  | Identified. Most currencies target this.   |
| unique   | fixed (item-specific)         | Cannot be altered by most currencies.      |

### Rarity Transitions

```
normal  --[Orb of Transmutation]-->  magic
normal  --[Orb of Alchemy]------->  rare
magic   --[Regal Orb]------------>  rare
magic   --[Orb of Chance]------->  random (normal/magic/rare/unique)
rare    --[Orb of Scouring]----->  normal
any     --[Orb of Chance]------->  random
```

**Prolog sketch:**
```prolog
rarity(normal).
rarity(magic).
rarity(rare).
rarity(unique).

max_prefixes(normal, 0).
max_prefixes(magic, 1).
max_prefixes(rare, 3).
% uniques: fixed, not counted

max_suffixes(normal, 0).
max_suffixes(magic, 1).
max_suffixes(rare, 3).
```

---

## 2. Item Properties

Binary flags on an item. Most are mutually exclusive or interact with each other.

| Property      | Description                                          |
|---------------|------------------------------------------------------|
| identified    | Mod values visible. Required for most crafting.      |
| corrupted     | Cannot be further modified by most currencies.       |
| mirrored      | Cannot be modified at all. Copy of another item.     |
| fractured     | One mod is locked (cannot be changed/removed).       |
| influenced    | Has an influence type (expands mod pool).            |
| synthesised   | Has synthesised implicits (replaces base implicit).  |

### Property Interactions

- `corrupted` blocks most currencies (exceptions: Tainted currencies)
- `mirrored` blocks all modifications
- `fractured` locks exactly one mod; rest behave normally
- `influenced` adds influence-specific mods to the pool
- `synthesised` replaces implicit; mutually exclusive with influenced

**Prolog sketch:**
```prolog
% Property facts: item_has_prop(Item, Prop).
blocks_modification(corrupted, _).   % blocks everything (except tainted)
blocks_modification(mirrored, _).    % blocks everything
blocks_modification(_, _) :- fail.   % default

% A currency can only apply if no blocking property exists.
can_apply(Item, Currency) :-
    \+ (item_has_prop(Item, P), blocks_modification(P, Currency)).
```

---

## 3. Modifier Slots

Explicit mods occupy **prefix** or **suffix** slots. Implicit mods are separate.

| Slot Type   | Max on Rare | Source Examples                    |
|-------------|-------------|-----------------------------------|
| prefix      | 3           | Explicit (rolled)                 |
| suffix      | 3           | Explicit (rolled)                 |
| implicit    | 1 (base)    | Base item type                    |
| enchantment | varies      | Labyrinth, Omen                   |
| rune        | varies      | Rune socket                       |

### Slot Awareness

Currencies that "add a modifier" care about available slots:
- If 3 prefixes are full, an Orb of Alteration cannot roll a prefix
- "Suffixes Cannot Be Changed" (metacraft) protects suffix slots
- Fractured mod occupies a slot but cannot be changed

**Prolog sketch:**
```prolog
slot_type(prefix).
slot_type(suffix).
slot_type(implicit).
slot_type(enchantment).
slot_type(rune).

mod_slot(Item, Mod, prefix) :- ...   % determined by mod data
mod_slot(Item, Mod, suffix) :- ...

count_prefixes(Item, N) :- aggregate_all(count, mod_slot(Item, _, prefix), N).
count_suffixes(Item, N) :- aggregate_all(count, mod_slot(Item, _, suffix), N).

has_open_prefix(Item) :- count_prefixes(Item, N), max_prefixes(Rarity, Max), N < Max.
has_open_suffix(Item) :- count_suffixes(Item, N), max_suffixes(Rarity, Max), N < Max.
```

---

## 4. Modifier Tags

Every mod has **tags** that determine interactions with currencies.
Tags are the backbone of targeted crafting.

| Tag Category    | Examples                              | Used By                |
|-----------------|---------------------------------------|------------------------|
| Element         | fire, cold, lightning, chaos          | Essences, fossils      |
| Defense         | armour, evasion, energy_shield, ward  | Essences, fossils      |
| Attack          | attack, physical, speed               | Essences, fossils      |
| Caster          | caster, spell, curse                  | Essences, fossils      |
| Attribute       | strength, dexterity, intelligence     | Essences, attribute catalysts |
| Life/Mana       | life, mana                            | Essences, fossils      |
| Critical        | critical                              | Essences               |
| Gem             | gem_level                             | Specific currencies    |
| Resistance      | fire_res, cold_res, lightning_res, chaos_res | Essences, fossils |

### Tag → Currency Interactions

```
Essence of Greed    → guarantees "life" tagged mod
Essence of Wrath    → guarantees "lightning" tagged mod
Fracturing Orb      → locks a random mod (any tag)
Orb of Annulment    → removes a random mod (no tag preference)
```

**Prolog sketch:**
```prolog
% mod_tags(ModId, [tag1, tag2, ...]).
mod_tags(t1_life, [life, defence]).
mod_tags(t1_fire_res, [fire, resistance]).

% Essence guarantees a tag:
essence_target(essence_of_greed, life).
essence_target(essence_of_wrath, lightning).
```

---

## 5. Mod Tiers

Each mod has a **tier** (T1 being best). Tier is determined by item level.

| Tier | ilvl Requirement | Typical Power | Example (Life prefix) |
|------|-----------------|---------------|----------------------|
| T1   | 84+             | Highest       | +100-109 max life    |
| T2   | 73+             | High          | +84-99 max life      |
| T3   | 64+             | Mid           | +68-83 max life      |
| T4   | 55+             | Low           | +50-67 max life      |
| T5   | 44+             | Lower         | +34-49 max life      |
| T6   | 1+              | Lowest        | +15-33 max life      |

**Prolog sketch:**
```prolog
% mod_tier(ModId, Tier, MinIlvl).
mod_tier(t1_life, 1, 84).
mod_tier(t2_life, 2, 73).

% A mod is rollable on an item if ilvl >= min_ilvl:
rollable(Mod, Item) :-
    mod_tier(Mod, _, MinIlvl),
    item_ilvl(Item, Ilvl),
    Ilvl >= MinIlvl.
```

---

## 6. Influence Types

Influence expands the mod pool with exclusive modifiers.

| Influence   | Exclusive Mod Examples                    |
|-------------|-------------------------------------------|
| shaper       | "Socketed Gems deal more spell damage"   |
| elder        | "Socketed Gems are supported by X"       |
| crusader     | Lightning-themed                         |
| redeemer     | Cold-themed                              |
| hunter       | Chaos-themed                             |
| warlord      | Physical / Fire-themed                   |

**PoE 2 specific:** influence system may differ from PoE 1 — verify against wiki.

---

## 7. Item Categories (Base Types)

Base type determines:
- Implicit modifier
- Which mods can roll (weapon vs armour vs jewelry)
- Defense stat weighting (armour base → armour mods weighted higher)

| Category     | Examples                          |
|--------------|-----------------------------------|
| weapon       | sword, axe, mace, bow, wand, etc |
| body_armour  | str, dex, int, hybrid             |
| helmet       | str, dex, int, hybrid             |
| gloves       | str, dex, int, hybrid             |
| boots        | str, dex, int, hybrid             |
| shield       | str, dex, int, hybrid             |
| ring         | two variants (left/right or types)|
| amulet       |                                   |
| belt         |                                   |
| jewel        |                                   |

---

## 8. State Representation (Proposed)

An item's complete crafting-relevant state as a Prolog term:

```prolog
% item(Base, Rarity, Ilvl, Influence, Props, Prefixes, Suffixes, Implicit)
item(
    item_base(poe2, spirit_blade, 84),       % game, base, ilvl
    rare,                                      % rarity
    [fractured, identified],                   % properties
    [t1_flat_phys, t2_attack_speed],           % prefixes
    [t1_crit_multi, t3_accuracy],              % suffixes
    implicit(spirit_blade_inherent)            % implicit
).
```

This single term captures everything a crafting rule needs to check.

---

## 9. Currency Orb Catalogue (Stubs)

Each currency is a **transition rule**: `preconditions → postconditions`.

| Currency               | Precondition                     | Effect                                |
|------------------------|----------------------------------|---------------------------------------|
| Orb of Transmutation   | item is normal                   | → magic, roll 1-2 explicit mods       |
| Orb of Alteration      | item is magic                    | → magic, reroll all explicit mods     |
| Orb of Alchemy         | item is normal                   | → rare, roll 4-6 explicit mods        |
| Chaos Orb              | item is rare                     | → rare, reroll all explicit mods      |
| Regal Orb              | item is magic                    | → rare, add 1 random explicit mod     |
| Exalted Orb            | item is rare, has open slot      | → rare, add 1 random explicit mod     |
| Orb of Annulment       | item is magic or rare            | → same, remove 1 random explicit mod  |
| Orb of Scouring        | item is magic or rare            | → normal, remove all explicit mods    |
| Divine Orb             | item has numeric mod values      | → same, reroll numeric values         |
| Vaal Orb              | item is not corrupted            | → possibly corrupted, random effect   |
| Orb of Augmentation    | item is magic, open slot         | → magic, add 1 random explicit mod    |

*(PoE 2 specific currencies — omens, essences, recombinators — will get their own detailed files.)*

---

## 10. Quality System

Quality increases modifier **magnitude** (numeric values), not mod weights.
Applied via Catalysts (rings/amulets) or Whetstones/Scrap (weapons/armour).

| Item Type | Currency | Effect per 1% Quality | Max |
|-----------|----------|----------------------|-----|
| Rings | Catalysts | +1% modifier magnitude (tag-specific) | 20% |
| Breach Rings | Catalysts | +1% modifier magnitude | 40% (45% refined) |
| Amulets | Catalysts | +1% modifier magnitude (tag-specific) | 20% |
| **Belts** | **N/A** | **Cannot have quality** | **0%** |
| Weapons | Whetstone | +1% local Physical Damage | 20% |
| Armour | Scrap | +1% local Defence | 20% |

### Catalyst Types (12)

| Catalyst | Tag Enhanced |
|----------|-------------|
| Flesh | life |
| Neural | mana |
| Carapace | armour, evasion, energy_shield |
| Uul-Netol's | physical |
| Xoph's | fire |
| Tul's | cold |
| Esh's | lightning |
| Chayula's | chaos |
| Reaver | attack |
| Sibilant | caster |
| Skittering | speed |
| Adaptive | attribute |

### Key Rules
- Quality is a **unique multiplier** applied after all other modifiers
- Different catalyst type **replaces** existing quality type and resets to 0%
- Apply quality **before** crafting for maximum effect
- Values are **truncated** (rounded down) after quality applied

**Prolog sketch:**
```prolog
quality_max(ring, 20).
quality_max(belt, 0).  % cannot have quality

quality_effect(20, [life, defence], flesh_catalyst, 1.2).
quality_effect(20, [fire, resistance], xophs_catalyst, 1.2).
quality_effect(20, [fire, resistance], flesh_catalyst, 1.0).  % no match
```

---

## 11. Omens

Omens modify the behavior of the next currency orb used.
Right-click to activate → stays in inventory → consumed when triggered.

### Sinistral/Dextral Pairs (prefix/suffix targeting)

| Omen | Currency | Effect |
|------|----------|--------|
| Sinistral Erasure | Chaos Orb | Removes only prefixes |
| Dextral Erasure | Chaos Orb | Removes only suffixes |
| Sinistral Alchemy | Orb of Alchemy | Max prefixes |
| Dextral Alchemy | Orb of Alchemy | Max suffixes |
| Sinistral Coronation | Regal Orb | Adds only prefixes |
| Dextral Coronation | Regal Orb | Adds only suffixes |
| Sinistral Exaltation | Exalted Orb | Adds only prefixes |
| Dextral Exaltation | Exalted Orb | Adds only suffixes |
| Sinistral Annulment | Orb of Annulment | Removes only prefixes |
| Dextral Annulment | Orb of Annulment | Removes only suffixes |

### Power Omens

| Omen | Currency | Effect |
|------|----------|--------|
| Greater Exaltation | Exalted Orb | Adds **two** mods |
| Greater Annulment | Orb of Annulment | Removes **two** mods |
| Homogenising Exaltation | Exalted Orb | Adds same-tag mod |
| Catalysing Exaltation | Exalted Orb | Consumes quality for targeting |
| Whittling | Chaos Orb | Removes lowest level mod |

### Why Omens Matter for Crafting

Without omens, Orb of Annulment removes a random mod (50/50 prefix/suffix).
With Sinistral Annulment, it **always** removes a prefix — deterministic control.
This is the backbone of "prefixes cannot be changed" style crafting from PoE 1,
but even more powerful since it targets specific slots.

**Prolog sketch:**
```prolog
omen(sinistral_annulment, orb_of_annulment, removes_only_prefixes, prefix).

% An omen+currency combo is a "modified currency action":
apply_with_omen(sinistral_annulment, orb_of_annulment, Item, NewItem) :-
    omen(sinistral_annulment, orb_of_annulment, removes_only_prefixes, prefix),
    can_apply(orb_of_annulment, Item),
    Item = item_state(Base, R, Ilvl, Inf, Props, [FirstPrefix|Rest], Suf, Impl),
    NewItem = item_state(Base, R, Ilvl, Inf, Props, Rest, Suf, Impl).
```

---

## 12. Alloys

Alloys are a PoE 2 patch 0.5 crafting currency.
Apply to rare item → removes one random mod → adds a guaranteed mod of specific tag.

| Alloy | Guaranteed Tag |
|-------|---------------|
| Runic | runic_ward |
| Adaptive | attribute |
| Protective | defence |
| Expansive | life |
| Swift | speed |
| Cyclonic | physical |
| Prismatic | elemental |
| Mystic | caster |
| Sovereign | attack |
| Celestial | resistance |
| Transcendent | gem_level |
| Runebinder | rune |
| Runefather | rune (enhanced) |

**Restrictions:** Rare items only, not corrupted/mirrored.

**Prolog sketch:**
```prolog
alloy(expansive_alloy, life, 'Adds life modifier').
alloy_precondition(_, item_state(_, rare, _, _, Props, _, _, _)) :-
    \+ member(corrupted, Props).
```

---

## Next Steps (updated)

1. ~~Verify against PoE 2~~ — done, poe2db data integrated
2. ~~Populate mod tables~~ — 7 categories, 166 mod_group facts
3. ~~Encode currency rules~~ — 18 currencies + omens + alloys
4. ~~Implement Prolog engine~~ — 939-line KB with weighted rolling
5. **Write first recipe** — test end-to-end with a simple craft algorithm
6. Scrape remaining categories (shields, belts, bows, crossbows)
7. Encode omen-modified currency rules (sinistral annulment etc.)
8. Add more tier data (only Life prefix has complete tiers currently)
