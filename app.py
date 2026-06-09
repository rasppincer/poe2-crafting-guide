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
    """Extract omen/4 and omen_disabled/2 facts."""
    omens = []
    disabled = set()
    for m in re.finditer(r"omen_disabled\((\w+),\s*'([^']+)'\)", pl_content):
        disabled.add(m.group(1))
    for m in re.finditer(
        r"^omen\((\w+),\s*(\w+),\s*(\w+),\s*(\w+)\)",
        pl_content,
        re.MULTILINE
    ):
        name = m.group(1)
        omens.append({
            "name": name,
            "currency": m.group(2),
            "effect": m.group(3),
            "slot": m.group(4),
            "disabled": name in disabled,
            "disabled_version": next((v for n, v in re.findall(
                r"omen_disabled\((\w+),\s*'([^']+)'\)", pl_content
            ) if n == name), None),
        })
    return omens

def parse_alloys(pl_content):
    alloys = []
    for m in re.finditer(
        r"^alloy\((\w+),\s*(\w+),\s*'([^']*)'\)",
        pl_content, re.MULTILINE
    ):
        alloys.append({
            "name": m.group(1),
            "tag": m.group(2),
            "description": m.group(3),
        })
    return alloys

def parse_quality_types(pl_content):
    types = []
    for m in re.finditer(
        r"^quality_type\((\w+),\s*\[([^\]]*)\]\)",
        pl_content, re.MULTILINE
    ):
        tags = [t.strip() for t in m.group(2).split(",") if t.strip()]
        types.append({"name": m.group(1), "tags": tags})
    return types

def parse_currencies(pl_content):
    currencies = []
    for m in re.finditer(r"^currency\((\w+)\)", pl_content, re.MULTILINE):
        name = m.group(1)
        # Check for precondition
        has_pre = f"currency_precondition({name}," in pl_content
        has_post = f"currency_postcondition({name}," in pl_content
        currencies.append({
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
    """Return all DB data for the explorer tab."""
    return jsonify({
        "mod_groups": DATA["mod_groups"],
        "omens": DATA["omens"],
        "alloys": DATA["alloys"],
        "quality_types": DATA["quality_types"],
        "currencies": DATA["currencies"],
        "weight_sums": DATA["weight_sums"],
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
    results = []

    for i, step in enumerate(recipe.get("steps", [])):
        checks = []
        action = step.get("action", "")

        # Check currency exists
        if "currency" in step:
            curr = step["currency"]
            exists = f"currency({curr})" in pl
            checks.append({
                "test": f"Currency '{curr}' exists",
                "pass": exists,
            })
            has_pre = f"currency_precondition({curr}," in pl
            checks.append({
                "test": f"Currency '{curr}' has precondition rules",
                "pass": has_pre,
            })

        # Check omen exists and is active
        if "omen" in step:
            omen = step["omen"]
            exists = f"omen({omen}," in pl
            disabled = f"omen_disabled({omen}" in pl
            checks.append({
                "test": f"Omen '{omen}' exists",
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

        # Check alloy exists
        if "alloy" in step:
            alloy = step["alloy"]
            exists = f"alloy({alloy}," in pl
            checks.append({
                "test": f"Alloy '{alloy}' exists",
                "pass": exists,
            })

        # Check catalyst exists
        if "catalyst" in step:
            cat = step["catalyst"]
            exists = f"quality_type({cat}," in pl
            checks.append({
                "test": f"Catalyst '{cat}' exists",
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
# Main
# ============================================================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8322, debug=False)
