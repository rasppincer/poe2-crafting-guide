"""PoE 2 Crafting Guide — Web UI

Serves a single-page app with three tabs:
  1. Database Explorer — browse mod groups, currencies, omens, alloys, quality
  2. Recipes — list of crafting recipes with details
  3. Recipe Tester — step through a recipe, adjust steps, test preconditions
"""

import json
import re
from pathlib import Path
from flask import Flask, render_template, jsonify, request

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
    return render_template("index.html")


@app.route("/api/database")
def api_database():
    """Return all DB data for the explorer tab. Supports ?game=poe1|poe2|all filter."""
    game = request.args.get("game", "all")
    def by_game(items):
        return [i for i in items if i.get("game") == game] if game != "all" else items
    return jsonify({
        "mod_groups": DATA["mod_groups"],
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
    """Return all recipes."""
    # Import from test file
    from tests.test_recipes import RECIPES
    return jsonify(RECIPES)


@app.route("/api/recipes/<name>")
def api_recipe(name):
    """Return a single recipe."""
    from tests.test_recipes import RECIPES
    if name not in RECIPES:
        return jsonify({"error": "Recipe not found"}), 404
    return jsonify(RECIPES[name])


@app.route("/api/recipe/verify", methods=["POST"])
def api_verify_recipe():
    """Verify a recipe's steps against the KB."""
    recipe = request.json
    pl = DATA["prolog"]
    game = recipe.get("game", "poe2")  # Game context for this recipe
    results = []

    for i, step in enumerate(recipe.get("steps", [])):
        checks = []
        action = step.get("action", "")

        # Check currency exists AND is valid for the selected game
        if "currency" in step:
            curr = step["currency"]
            exists = f"currency({game}, {curr})" in pl
            checks.append({
                "test": f"Currency '{curr}' exists in {game.upper()}",
                "pass": exists,
            })
            if not exists:
                # Check if it exists in the OTHER game (stale source warning)
                other_game = "poe1" if game == "poe2" else "poe2"
                exists_other = f"currency({other_game}, {curr})" in pl
                if exists_other:
                    checks.append({
                        "test": f"⚠ STALE: '{curr}' exists in {other_game.upper()} but not {game.upper()} — likely from old source",
                        "pass": False,
                    })
            has_pre = f"currency_precondition({curr}," in pl
            checks.append({
                "test": f"Currency '{curr}' has precondition rules",
                "pass": has_pre,
            })

        # Check omen exists and is active for the selected game
        if "omen" in step:
            omen = step["omen"]
            exists = f"omen({game}, {omen}," in pl
            disabled = f"disabled(omen, {omen}" in pl
            checks.append({
                "test": f"Omen '{omen}' exists in {game.upper()}",
                "pass": exists,
            })
            checks.append({
                "test": f"Omen '{omen}' is not disabled",
                "pass": not disabled,
            })
            can_use = f"can_use_omen({omen}," in pl or "can_use_omen" in pl
            checks.append({
                "test": f"can_use_omen/2 available",
                "pass": can_use,
            })

        # Check alloy exists for the selected game
        if "alloy" in step:
            alloy = step["alloy"]
            exists = f"alloy({game}, {alloy}," in pl
            checks.append({
                "test": f"Alloy '{alloy}' exists in {game.upper()}",
                "pass": exists,
            })

        # Check catalyst exists for the selected game
        if "catalyst" in step:
            cat = step["catalyst"]
            exists = f"quality_type({game}, {cat}," in pl
            checks.append({
                "test": f"Catalyst '{cat}' exists in {game.upper()}",
                "pass": exists,
            })

        all_pass = all(c["pass"] for c in checks)
        results.append({
            "step": i + 1,
            "action": action,
            "currency": step.get("currency", step.get("alloy", step.get("catalyst", ""))),
            "checks": checks,
            "all_pass": all_pass,
        })

    overall = all(r["all_pass"] for r in results)
    return jsonify({"overall": overall, "steps": results})


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
