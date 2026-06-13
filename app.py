"""PoE 2 Crafting Guide — API Server

Pure JSON API for PoE 2 crafting data, recipes, and optimization.
No frontend — consumed by One Ring dashboard or direct API clients.

Standalone: http://localhost:8322/api/database?game=poe2
Via nginx:  http://localhost/poe2-crafting/api/database?game=poe2
"""

import json
import re
from pathlib import Path
from flask import Flask, jsonify, request

app = Flask(__name__)
ROOT = Path(__file__).parent
RESOURCES = ROOT / "resources"
PROLOG_FILE = ROOT / "poe2_crafting.pl"

# Lazy-load optimizer
_optimizer = None
def get_optimizer():
    global _optimizer
    if _optimizer is None:
        from optimizer import RecipeOptimizer
        _optimizer = RecipeOptimizer()
    return _optimizer


# ============================================================================
# Data Loading
# ============================================================================

def load_json(name):
    return json.loads((RESOURCES / name).read_text())

def load_prolog():
    return PROLOG_FILE.read_text()

def parse_mod_groups(pl_content):
    """Extract mod_group/8 facts from Prolog content."""
    sums = parse_weight_sums(pl_content)
    groups = []
    for m in re.finditer(
        r"mod_group\((\w+),\s*(\w+),\s*'([^']*)',\s*\[([^\]]*)\],\s*(\d+),\s*(\d+),\s*(\d+),\s*(\w+)\)",
        pl_content
    ):
        tags = [t.strip() for t in m.group(4).split(",") if t.strip()]
        cat = m.group(1)
        slot = m.group(8)
        weight = int(m.group(5))
        total = sums.get(cat, {}).get(slot, 1)
        pct = round(weight / total * 100, 2) if total > 0 else 0
        groups.append({
            "category": cat,
            "group": m.group(2),
            "description": m.group(3),
            "tags": tags,
            "weight": weight,
            "maxIlvl": int(m.group(6)),
            "tierCount": int(m.group(7)),
            "slot": slot,
            "weight_pct": pct,
        })
    return groups

def parse_omens(pl_content):
    """Extract omen/5 and omen_disabled/2 facts."""
    omens = []
    disabled = set()
    for m in re.finditer(r"omen_disabled\((\w+),\s*'([^']+)'\)", pl_content):
        disabled.add(m.group(1))
    for m in re.finditer(
        r"^omen\((\w+),\s*(\w+),\s*(\w+),\s*(\w+),\s*(\w+)\)",
        pl_content,
        re.MULTILINE
    ):
        game = m.group(1)
        name = m.group(2)
        omens.append({
            "game": game,
            "name": name,
            "currency": m.group(3),
            "effect": m.group(4),
            "slot": m.group(5),
            "disabled": name in disabled,
            "disabled_version": next((v for n, v in re.findall(
                r"omen_disabled\((\w+),\s*'([^']+)'\)", pl_content
            ) if n == name), None),
        })
    return omens

def parse_alloys(pl_content):
    alloys = []
    for m in re.finditer(
        r"^alloy\((\w+),\s*(\w+),\s*(\w+),\s*'([^']*)'\)",
        pl_content, re.MULTILINE
    ):
        alloys.append({
            "game": m.group(1),
            "name": m.group(2),
            "tag": m.group(3),
            "description": m.group(4),
        })
    return alloys

def parse_quality_types(pl_content):
    types = []
    for m in re.finditer(
        r"^quality_type\((\w+),\s*(\w+),\s*\[([^\]]*)\]\)",
        pl_content, re.MULTILINE
    ):
        tags = [t.strip() for t in m.group(3).split(",") if t.strip()]
        types.append({"game": m.group(1), "name": m.group(2), "tags": tags})
    return types

def parse_currencies(pl_content):
    currencies = []
    for m in re.finditer(r"^currency\((\w+),\s*(\w+)\)", pl_content, re.MULTILINE):
        game = m.group(1)
        name = m.group(2)
        # Check for precondition
        has_pre = f"currency_precondition({name}," in pl_content
        has_post = f"currency_postcondition({name}," in pl_content
        currencies.append({
            "game": game,
            "name": name,
            "has_rules": has_pre and has_post,
        })
    return currencies

def parse_weight_sums(pl_content):
    sums = {}
    for m in re.finditer(
        r"mod_pool_weight_sum\((\w+),\s*(\w+),\s*(\d+)\)", pl_content
    ):
        cat = m.group(1)
        if cat not in sums:
            sums[cat] = {}
        sums[cat][m.group(2)] = int(m.group(3))
    return sums


def get_all_data():
    """Load everything once and return a dict."""
    pl = load_prolog()

    # Also load all consulted .pl data files
    all_pl = pl
    for consult in re.findall(r":- consult\('([^']+)'\)", pl):
        data_path = ROOT / consult
        if data_path.exists():
            all_pl += "\n" + data_path.read_text()

    # Load mod JSON files for weight percentages
    mod_jsons = {}
    for f in RESOURCES.glob("mods_*.json"):
        data = json.loads(f.read_text())
        mod_jsons[data["item_category"]] = data

    return {
        "prolog": all_pl,
        "mod_groups": parse_mod_groups(all_pl),
        "omens": parse_omens(all_pl),
        "alloys": parse_alloys(all_pl),
        "quality_types": parse_quality_types(all_pl),
        "currencies": parse_currencies(all_pl),
        "weight_sums": parse_weight_sums(all_pl),
        "recipes": load_json("recipes.json") if (RESOURCES / "recipes.json").exists() else {},
    }


# Cache data at startup
DATA = get_all_data()

# ============================================================================
# Routes
# ============================================================================

@app.route("/")
def index():
    """API info endpoint."""
    return jsonify({
        "service": "poe2-crafting-guide",
        "version": "0.6.0",
        "description": "PoE 2 Crafting Guide API — no frontend, use One Ring dashboard",
        "endpoints": {
            "database": "/api/database?game=poe1|poe2|all",
            "recipes": "/api/recipes",
            "optimize": "/api/optimize",
            "currency_palette": "/api/currency-palette",
            "omen_map": "/api/omen-map",
            "verify": "/api/recipe/verify",
            "health": "/health",
        },
    })


@app.route("/health")
def health():
    return jsonify({"status": "ok", "mod_groups": len(DATA["mod_groups"])})


@app.route("/api/database")
def api_database():
    """Return all DB data for the explorer tab. Supports ?game=poe1|poe2|all filter.

    Query params (all optional):
      ?game=poe1|poe2|all  — filter by game
      ?category=ring       — filter mod_groups by category
      ?slot=prefix|suffix  — filter mod_groups by slot
      ?tag=life            — filter mod_groups by tag (partial match)
      ?text=fire           — search in group name, description, category
    """
    game = request.args.get("game", "all")
    category = request.args.get("category", "").strip()
    slot = request.args.get("slot", "").strip()
    tag = request.args.get("tag", "").strip()
    text = request.args.get("text", "").strip().lower()

    def by_game(items):
        return [i for i in items if i.get("game") == game] if game != "all" else items

    # Filter mod_groups
    mod_groups = DATA["mod_groups"]
    if category:
        mod_groups = [g for g in mod_groups if g["category"] == category]
    if slot:
        mod_groups = [g for g in mod_groups if g["slot"] == slot]
    if tag:
        tag_lower = tag.lower()
        mod_groups = [g for g in mod_groups if any(tag_lower in t.lower() for t in g.get("tags", []))]
    if text:
        mod_groups = [
            g for g in mod_groups
            if text in g.get("group", "").lower()
            or text in g.get("description", "").lower()
            or text in g.get("category", "").lower()
        ]

    return jsonify({
        "mod_groups": mod_groups,
        "omens": by_game(DATA["omens"]),
        "alloys": by_game(DATA["alloys"]),
        "quality_types": by_game(DATA["quality_types"]),
        "currencies": by_game(DATA["currencies"]),
        "weight_sums": DATA["weight_sums"],
        "current_game": game,
    })


@app.route("/api/database/refresh", methods=["POST"])
def api_refresh():
    """Reload data from disk."""
    global DATA
    DATA = get_all_data()
    return jsonify({"status": "ok", "mod_groups": len(DATA["mod_groups"])})


@app.route("/api/recipes")
def api_recipes():
    """Return all recipes — merged from test fixtures + recipes/ directory."""
    from tests.test_recipes import RECIPES
    all_recipes = dict(RECIPES)
    # Load from recipes/ directory (saved by Recipe Builder)
    RECIPES_DIR.mkdir(exist_ok=True)
    for f in sorted(RECIPES_DIR.glob("*.json")):
        try:
            data = json.loads(f.read_text())
            key = f.stem  # filename without .json
            all_recipes[key] = data
        except Exception:
            continue
    return jsonify(all_recipes)


@app.route("/api/recipes/<name>")
def api_recipe(name):
    """Return a single recipe — check test fixtures first, then recipes/ dir."""
    from tests.test_recipes import RECIPES
    if name in RECIPES:
        return jsonify(RECIPES[name])
    filepath = RECIPES_DIR / f"{name}.json"
    if filepath.exists():
        return jsonify(json.loads(filepath.read_text()))
    return jsonify({"error": "Recipe not found"}), 404


def _format_condition_label(cond):
    """Format a condition dict into a human-readable label (like JS formatCondition)."""
    ctype = cond.get("type", "")
    value = cond.get("value", "")
    if ctype == "has_mod":
        return f"has [{value}]"
    elif ctype == "not_has_mod":
        return f"NOT has [{value}]"
    elif ctype == "prefix_count_gte":
        return f"prefix_count >= {value}"
    elif ctype == "suffix_count_gte":
        return f"suffix_count >= {value}"
    elif ctype == "prefix_count_lte":
        return f"prefix_count <= {value}"
    elif ctype == "suffix_count_lte":
        return f"suffix_count <= {value}"
    elif ctype == "rarity_is":
        return f"rarity == {value}"
    elif ctype == "rarity_not":
        return f"rarity != {value}"
    elif ctype == "custom":
        return str(value)
    else:
        return f"{ctype}: {value}"


@app.route("/api/recipe/verify", methods=["POST"])
def api_verify_recipe():
    """Verify a recipe's steps against the KB using state-tracking verifier."""
    recipe = request.json
    pl = DATA["prolog"]
    from verifier import verify_recipe
    result = verify_recipe(recipe, prolog_kb=pl)
    result_dict = result.to_dict()

    # Add condition_label to each condition in the response
    # Conditions come from the original recipe steps (pre-normalization)
    steps_input = recipe.get("steps", [])
    for i, step_data in enumerate(steps_input):
        conditions = step_data.get("conditions", [])
        if conditions and i < len(result_dict["steps"]):
            result_dict["steps"][i]["conditions"] = [
                {**cond, "condition_label": _format_condition_label(cond)}
                for cond in conditions
            ]

    return jsonify(result_dict)


@app.route("/api/mod_pool/<category>")
def api_mod_pool(category):
    """Return mod groups for a specific category."""
    groups = [g for g in DATA["mod_groups"] if g["category"] == category]
    sums = DATA["weight_sums"].get(category, {})
    # Calculate weight percentages
    for g in groups:
        total = sums.get(g["slot"], 1)
        g["weight_pct"] = round(g["weight"] / total * 100, 2) if total > 0 else 0
    return jsonify({"category": category, "groups": groups, "weight_sums": sums})


@app.route("/api/prolog")
def api_prolog():
    """Return raw Prolog content."""
    return jsonify({"content": DATA["prolog"]})


# ============================================================================
# Currency Palette & Omen Map (Recipe Builder support)
# ============================================================================

# Catalyst names used for action_type detection
CATALYST_NAMES = {
    "flesh_catalyst", "neural_catalyst", "carapace_catalyst",
    "uul_netol_catalyst", "xophs_catalyst", "tuls_catalyst",
    "eshs_catalyst", "chayulas_catalyst", "reaver_catalyst",
    "sibilant_catalyst", "skittering_catalyst", "adaptive_catalyst",
    "armourer_scrap", "blacksmith_whetstone", "arcanist_etcher",
}

# Static basic orbs definition
BASIC_ORBS = [
    {"name": "orb_of_transmutation", "icon": "🔵", "label": "Transmutation"},
    {"name": "orb_of_augmentation", "icon": "🔵", "label": "Augmentation"},
    {"name": "orb_of_alchemy", "icon": "🟡", "label": "Alchemy"},
    {"name": "chaos_orb", "icon": "🟣", "label": "Chaos"},
    {"name": "regal_orb", "icon": "🟡", "label": "Regal"},
    {"name": "exalted_orb", "icon": "⭐", "label": "Exalted"},
    {"name": "orb_of_annulment", "icon": "🔴", "label": "Annulment"},
    {"name": "divine_orb", "icon": "✨", "label": "Divine"},
    {"name": "vaal_orb", "icon": "💀", "label": "Vaal"},
    {"name": "orb_of_chance", "icon": "🎲", "label": "Chance"},
    {"name": "fracturing_orb", "icon": "💎", "label": "Fracturing"},
]

# Static essences definition
ESSENCES = [
    {"name": "essence_of_the_body", "icon": "💚", "label": "Essence of the Body"},
    {"name": "essence_of_wrath", "icon": "⚡", "label": "Essence of Wrath"},
]


def _guess_action_type(currency_name):
    """Determine action_type from a currency name (moved from JS guessActionType)."""
    if currency_name.startswith("essence_"):
        return "apply_essence"
    if currency_name in CATALYST_NAMES:
        return "apply_catalyst"
    return "apply_currency"


def _omen_label(name):
    """Generate a human-readable label from an omen snake_case name."""
    return name.replace("_", " ").title()


@app.route("/api/currency-palette")
def api_currency_palette():
    """Return currency categorization for the recipe builder palette.

    Structure: { categories: { "Basic Orbs": {type, items}, ... } }
    Each item: {name, icon, label, action_type}
    """
    # Basic orbs — static list
    basic_items = [
        {**orb, "action_type": _guess_action_type(orb["name"])}
        for orb in BASIC_ORBS
    ]

    # Essences — static list
    essence_items = [
        {**ess, "action_type": _guess_action_type(ess["name"])}
        for ess in ESSENCES
    ]

    # Omens — from DB, active only
    omen_items = []
    for omen in DATA["omens"]:
        if omen.get("disabled"):
            continue
        name = omen["name"]
        omen_items.append({
            "name": name,
            "icon": "🟢",
            "label": _omen_label(name),
            "action_type": _guess_action_type(name),
        })

    # Catalysts — from DB quality_types
    catalyst_items = []
    for qt in DATA["quality_types"]:
        name = qt["name"]
        catalyst_items.append({
            "name": name,
            "icon": "🧪",
            "label": _omen_label(name),
            "action_type": _guess_action_type(name),
        })

    return jsonify({
        "categories": {
            "Basic Orbs": {"type": "basic", "items": basic_items},
            "Essences": {"type": "essence", "items": essence_items},
            "Omens": {"type": "omen", "items": omen_items},
            "Catalysts & Quality": {"type": "catalyst", "items": catalyst_items},
        }
    })


# Omen → currency pairing map (static, from JS frontend)
OMEN_CURRENCY_MAP = {
    "sinistral_exaltation": "exalted_orb",
    "dextral_exaltation": "exalted_orb",
    "greater_exaltation": "exalted_orb",
    "catalysing_exaltation": "exalted_orb",
    "sinistral_annulment": "orb_of_annulment",
    "dextral_annulment": "orb_of_annulment",
    "sinistral_crystallisation": "exalted_orb",
    "dextral_crystallisation": "exalted_orb",
    "sinistral_erasure": "chaos_orb",
    "dextral_erasure": "chaos_orb",
    "sinistral_necromancy": "chaos_orb",
    "dextral_necromancy": "chaos_orb",
    "greater_annulment": "orb_of_annulment",
    "omen_of_chance": "orb_of_chance",
    "omen_of_the_ancients": "orb_of_chance",
    "omen_of_blessed": "divine_orb",
    "omen_of_sanctification": "vaal_orb",
    "whittling": "exalted_orb",
}


@app.route("/api/omen-map")
def api_omen_map():
    """Return omen→currency pairing map.

    Maps omen names to the currency they pair with.
    """
    return jsonify(OMEN_CURRENCY_MAP)


# ============================================================================
# Optimizer Endpoints
# ============================================================================

@app.route("/api/optimize/<name>")
def api_optimize(name):
    """Evaluate a recipe for optimality."""
    from tests.test_recipes import RECIPES
    if name not in RECIPES:
        return jsonify({"error": "Recipe not found"}), 404

    opt = get_optimizer()
    evaluation = opt.evaluate_recipe(RECIPES[name])

    return jsonify({
        "recipe_name": evaluation.recipe_name,
        "goal": evaluation.goal,
        "score": evaluation.score,
        "current_method": {
            "name": evaluation.current_method.method_name,
            "steps": evaluation.current_method.steps,
            "total_expected": evaluation.current_method.total_expected,
            "total_steps": evaluation.current_method.total_steps,
            "description": evaluation.current_method.description,
        },
        "alternatives": [
            {
                "name": a.method_name,
                "steps": a.steps,
                "total_expected": a.total_expected,
                "total_steps": a.total_steps,
                "description": a.description,
            }
            for a in evaluation.alternatives
        ],
        "recommendations": evaluation.recommendations,
    })


@app.route("/api/optimize")
def api_optimize_all():
    """Evaluate all recipes."""
    from tests.test_recipes import RECIPES

    opt = get_optimizer()
    results = []
    for name, recipe in RECIPES.items():
        evaluation = opt.evaluate_recipe(recipe)
        results.append({
            "recipe_name": evaluation.recipe_name,
            "recipe_id": name,
            "goal": evaluation.goal,
            "score": evaluation.score,
            "current_steps": evaluation.current_method.total_steps,
            "alternatives_count": len(evaluation.alternatives),
            "recommendations": evaluation.recommendations,
        })
    return jsonify(results)


@app.route("/api/mod_probability/<category>/<mod_group>")
def api_mod_probability(category, mod_group):
    """Get the probability of rolling a specific mod."""
    opt = get_optimizer()
    prob = opt.mod_probability(category, mod_group)
    if not prob:
        return jsonify({"error": f"Mod '{mod_group}' not found in category '{category}'"}), 404
    return jsonify({
        "mod_group": prob.mod_group,
        "category": prob.category,
        "slot": prob.slot,
        "weight": prob.weight,
        "total_weight": prob.total_weight,
        "probability": round(prob.probability, 6),
        "expected_attempts": round(prob.expected_attempts, 1),
    })


# ============================================================================
# Recipe Builder Endpoints
# ============================================================================

RECIPES_DIR = ROOT / "recipes"

@app.route("/api/recipe-builder/list")
def api_recipe_builder_list():
    """List all saved builder recipes."""
    RECIPES_DIR.mkdir(exist_ok=True)
    recipes = []
    for f in sorted(RECIPES_DIR.glob("*.json")):
        try:
            data = json.loads(f.read_text())
            recipes.append({
                "filename": f.name,
                "name": data.get("name", f.stem),
                "goal": data.get("goal", ""),
                "base": data.get("base", ""),
                "category": data.get("category", ""),
                "step_count": len(data.get("steps", [])),
            })
        except Exception:
            pass
    return jsonify(recipes)


@app.route("/api/recipe-builder/save", methods=["POST"])
def api_recipe_builder_save():
    """Save a recipe to JSON file."""
    data = request.json
    if not data or "name" not in data:
        return jsonify({"error": "Missing recipe name"}), 400
    RECIPES_DIR.mkdir(exist_ok=True)
    # Sanitize filename
    safe_name = re.sub(r'[^a-zA-Z0-9_]', '_', data["name"].lower()).strip('_')
    if not safe_name:
        safe_name = "unnamed_recipe"
    filepath = RECIPES_DIR / f"{safe_name}.json"
    filepath.write_text(json.dumps(data, indent=2))
    return jsonify({"status": "ok", "filename": filepath.name, "path": str(filepath)})


@app.route("/api/recipe-builder/load/<filename>")
def api_recipe_builder_load(filename):
    """Load a saved recipe."""
    filepath = RECIPES_DIR / filename
    if not filepath.exists():
        return jsonify({"error": "Recipe not found"}), 404
    return jsonify(json.loads(filepath.read_text()))


@app.route("/api/recipe-builder/delete/<filename>", methods=["DELETE"])
def api_recipe_builder_delete(filename):
    """Delete a saved recipe."""
    filepath = RECIPES_DIR / filename
    if not filepath.exists():
        return jsonify({"error": "Recipe not found"}), 404
    filepath.unlink()
    return jsonify({"status": "ok"})


@app.route("/api/recipe-builder/export-prolog", methods=["POST"])
def api_recipe_builder_export_prolog():
    """Export a recipe as Prolog facts."""
    data = request.json
    if not data:
        return jsonify({"error": "No recipe data"}), 400

    name = data.get("name", "unnamed")
    goal = data.get("goal", "minimum_cost")
    steps = data.get("steps", [])

    # Build Prolog fact
    safe_name = re.sub(r'[^a-zA-Z0-9_]', '_', name.lower()).strip('_')
    step_facts = []
    for i, s in enumerate(steps):
        curr = s.get("currency", "unknown")
        desc = s.get("description", s.get("action", "apply"))
        desc_escaped = desc.replace("'", "\\'")
        step_facts.append(f"    step({i+1}, {curr}, '{desc_escaped}')")

    steps_str = ",\n".join(step_facts)
    prolog = f"""% Recipe: {name}
% Generated by PoE 2 Crafting Guide Recipe Builder

recipe({safe_name}, poe2, {goal}, [
{steps_str}
]).
"""
    return jsonify({"prolog": prolog, "recipe_name": safe_name})


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8322, debug=False)
