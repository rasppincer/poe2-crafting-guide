# Writing Crafting Recipes

Recipes are defined in `tests/test_recipes.py` in the `RECIPES` dict.
Each recipe is a step-by-step crafting sequence that can be verified against the KB.

## Recipe Format

```python
"recipe_name": {
    "name": "Human-Readable Recipe Name",
    "target": "Description of the final item",
    "base": "base_type_id",          # must exist in base_type/2
    "category": "mod_pool_category", # e.g. ring, body_armour_str
    "steps": [
        {
            "action": "apply_currency|spam|apply_with_omen|apply_alloy|apply_catalyst",
            "currency": "orb_name",  # for currency actions
            "omen": "omen_name",     # for omen-modified actions
            "alloy": "alloy_name",   # for alloy actions
            "catalyst": "cat_name",  # for catalyst actions
            "precondition": "text describing what the item needs",
            "condition": "optional conditional text",
            "result": "text describing what happens",
            "goal": "optional — what you're trying to hit",
            "until": "optional — for spam actions, stopping condition",
            "note": "optional — crafting tip or warning",
        },
    ],
    "cost_analysis": {               # optional
        "alteration_expected": 18,
        "regals": 1,
        "total_expected": "~20 alterations + 1 regal",
    },
}
```

## Step Actions

| Action | Meaning |
|--------|---------|
| `apply_currency` | Use a single currency orb |
| `spam` | Repeatedly use a currency until a condition is met |
| `apply_with_omen` | Currency + omen combo (deterministic targeting) |
| `apply_alloy` | Use an alloy to replace a mod |
| `apply_catalyst` | Apply quality via catalyst |

## Verification

When you click "Verify Recipe" in the UI, the backend checks:
- Currency exists in `currency/1`
- Currency has `currency_precondition/2` and `currency_postcondition/3`
- Omen exists in `omen/4` and is NOT in `omen_disabled/2`
- Alloy exists in `alloy/3`
- Catalyst exists in `quality_type/2`
- `can_use_omen/2` is available for omen+currency combos

## Common Recipe Patterns

### Alteration Spam → Regal → Exalt

```python
{
    "steps": [
        {"action": "apply_currency", "currency": "orb_of_transmutation"},
        {"action": "spam", "currency": "orb_of_alteration", "until": "hit target prefix"},
        {"action": "apply_currency", "currency": "orb_of_augmentation"},
        {"action": "apply_currency", "currency": "regal_orb"},
        {"action": "apply_currency", "currency": "exalted_orb"},
    ]
}
```

### Essence → Omen Exaltation

```python
{
    "steps": [
        {"action": "apply_currency", "currency": "essence_of_greed"},
        {"action": "apply_with_omen", "currency": "exalted_orb", "omen": "dextral_exaltation"},
    ]
}
```

### Alchemy → Sinistral Annulment → Exaltation

```python
{
    "steps": [
        {"action": "apply_currency", "currency": "orb_of_alchemy"},
        {"action": "apply_with_omen", "currency": "orb_of_annulment", "omen": "sinistral_annulment"},
        {"action": "apply_with_omen", "currency": "exalted_orb", "omen": "sinistral_exaltation"},
    ]
}
```

### Catalyst → Alchemy (Quality-Enhanced)

```python
{
    "steps": [
        {"action": "apply_catalyst", "catalyst": "flesh_catalyst"},
        {"action": "apply_currency", "currency": "orb_of_alchemy"},
    ]
}
```

### Alloy Crafting

```python
{
    "steps": [
        {"action": "apply_currency", "currency": "orb_of_alchemy"},
        {"action": "apply_alloy", "alloy": "sovereign_alloy"},
    ]
}
```

## Adding a New Recipe

1. Open `tests/test_recipes.py`
2. Add a new entry to the `RECIPES` dict
3. Run `pytest tests/test_recipes.py -v` to verify
4. Refresh the web UI to see it in the Recipes tab

## Disabled Omens (Don't Use These)

These omens are disabled as of 0.5.0 and will fail verification:
- `sinistral_alchemy`, `dextral_alchemy` (since 0.3.0)
- `sinistral_coronation`, `dextral_coronation` (since 0.3.0)
- `greater_annulment` (since 0.3.0)
- `homogenising_coronation`, `homogenising_exaltation` (since 0.4.0)
- `omen_of_corruption` (since 0.5.0)
- `omen_of_recombination` (since 0.5.0)
