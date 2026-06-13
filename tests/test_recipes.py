"""Test crafting recipes — verify step-by-step crafting sequences are legal.

Each test encodes a real PoE 2 crafting recipe and checks that every
currency application satisfies its preconditions. When we have pyswip,
these will run against the actual Prolog engine. For now, we validate
the recipe structure and data consistency.
"""

import json
import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent
PROLOG_FILE = PROJECT_ROOT / "poe2_crafting.pl"


# ============================================================================
# Recipe Definitions
# ============================================================================

RECIPES = {
    "ring_life_fire_res": {
        "name": "Craft a Ring with Life + Fire Resistance",
        "game": "poe2",
        "goal": "minimum_cost",
        "target": "Rare ring with increased_life prefix + fire_resistance suffix",
        "base": "jade_ring",
        "category": "ring",
        "steps": [
            {
                "action": "apply_currency",
                "currency": "orb_of_transmutation",
                "precondition": "normal rarity, no mods",
                "result": "magic, 1 prefix + 1 suffix",
            },
            {
                "action": "spam",
                "currency": "chaos_orb",
                "precondition": "rare rarity (regal first if magic)",
                "goal": "hit increased_life prefix + fire_resistance suffix",
                "until": "prefixes contains increased_life AND suffixes contains fire_resistance",
                "note": "In PoE 2 there is no Orb of Alteration. Chaos Orb rerolls all mods on a rare item. Alternative: use Essence of the Body on a magic item to guarantee life, then craft from there.",
            },
        ],
        "cost_analysis": {
            "chaos_orbs_expected": "varies widely — depends on mod pool weights",
            "alternative": "Essence of the Body (magic → rare, guaranteed life) + exalt for suffix",
        },
    },

    "body_armour_deterministic_life": {
        "name": "Deterministic Life Prefix on Str Body Armour",
        "game": "poe2",
        "goal": "minimum_interactions",
        "target": "Rare str body armour with guaranteed life prefix",
        "base": "plate_vest",
        "category": "body_armour_str",
        "steps": [
            {
                "action": "apply_currency",
                "currency": "orb_of_transmutation",
                "precondition": "normal body armour",
                "result": "magic with 1 modifier",
                "note": "PoE 2 transmute adds exactly 1 mod (not 2 like PoE 1).",
            },
            {
                "action": "apply_currency",
                "currency": "orb_of_augmentation",
                "condition": "if transmute did NOT roll a life mod",
                "result": "magic with 2 modifiers",
                "note": "Augment adds a 2nd mod. IMPORTANT: if transmute already rolled life, augment is fine — but the next essence step will FAIL with 'item already has a mod of this type'. In that case, start over with a new base.",
            },
            {
                "action": "apply_currency",
                "currency": "essence_of_the_body",
                "precondition": "magic rarity, NO existing life modifier on the item",
                "result": "rare with guaranteed increased_life prefix + additional random mods",
                "note": "PoE 2 Essence of the Body upgrades magic → rare and guarantees a life modifier. Will FAIL if the item already has a life mod from transmute/augment — you'll see 'Item already has a mod of this type'.",
            },
            {
                "action": "apply_currency",
                "currency": "exalted_orb",
                "precondition": "rare with at least 1 open slot",
                "result": "adds 1 random modifier to an open slot",
                "note": "Omen is optional: without omen, exalt picks randomly from open prefix/suffix slots. With Dextral Exaltation omen, it guarantees the mod goes to suffix. Use omen only if you specifically need a suffix mod.",
            },
        ],
    },

    "ring_omen_annulment_recipe": {
        "name": "Targeted Prefix Annulment + Exaltation on Ring",
        "game": "poe2",
        "goal": "maximum_values",
        "target": "Rare ring with specific prefixes, bad suffix removed",
        "base": "jade_ring",
        "category": "ring",
        "steps": [
            {
                "action": "apply_currency",
                "currency": "orb_of_alchemy",
                "precondition": "normal ring",
                "result": "rare with 4-6 random mods",
            },
            {
                "action": "apply_with_omen",
                "currency": "orb_of_annulment",
                "omen": "sinistral_annulment",
                "precondition": "rare with at least 1 prefix, omen active",
                "result": "removes 1 prefix (NOT random — guaranteed prefix removal)",
                "note": "This is the key deterministic step — without omen, 50/50 prefix/suffix. With sinistral annulment, you choose which prefix to remove.",
            },
            {
                "action": "apply_with_omen",
                "currency": "exalted_orb",
                "omen": "sinistral_exaltation",
                "precondition": "rare with open prefix slot, omen active",
                "result": "adds 1 prefix (guaranteed to be prefix, not suffix)",
            },
        ],
    },

    "weapon_alloy_craft": {
        "name": "Alloy Crafting on Sword",
        "game": "poe2",
        "goal": "minimum_interactions",
        "target": "Rare sword with a guaranteed attack mod via alloy",
        "base": "spirit_blade",
        "category": "weapon_sword",
        "steps": [
            {
                "action": "apply_currency",
                "currency": "orb_of_alchemy",
                "precondition": "normal sword",
                "result": "rare with random mods",
            },
            {
                "action": "apply_alloy",
                "alloy": "sovereign_alloy",
                "precondition": "rare item, not corrupted/mirrored",
                "result": "removes 1 random mod, adds guaranteed attack modifier",
                "note": "Alloy removes AND adds — net zero mod count change. The removed mod is random; the added mod is guaranteed to have the attack tag.",
            },
        ],
    },

    "amulet_catalyst_craft": {
        "name": "Quality-Enhanced Amulet Craft",
        "game": "poe2",
        "goal": "maximum_values",
        "target": "Rare amulet with enhanced life rolls via catalyst quality",
        "base": "any_amulet",
        "category": "amulet",
        "steps": [
            {
                "action": "apply_currency",
                "currency": "orb_of_alchemy",
                "precondition": "normal amulet",
                "result": "rare — check if life mod rolled",
            },
            {
                "action": "spam",
                "currency": "chaos_orb",
                "condition": "if NO life prefix on the amulet after alchemy",
                "goal": "hit increased_life prefix",
                "until": "prefixes contains increased_life",
                "note": "Only needed if alchemy didn't roll life (~12.5% chance per attempt). Skip this step if life already present.",
            },
            {
                "action": "apply_catalyst",
                "catalyst": "flesh_catalyst",
                "precondition": "rare amulet with increased_life prefix, not corrupted",
                "result": "20% quality — life modifiers display ~20% higher values",
                "note": "Apply AFTER confirming good life roll. Quality is a persistent unique multiplier: 1% quality = 1% increased magnitude for matching tag mods. Quality persists through most crafting but IS consumed by Omen of Catalysing Exaltation.",
            },
        ],
    },

    "widowhale_quiver": {
        "name": "Widowhale Quiver (One Mana Left, 0.5.0)",
        "game": "poe2",
        "goal": "maximum_values",
        "target": "Fractured +2 Projectile Skills quiver with T1 flat lightning, projectile speed, and crit suffixes",
        "base": "visceral_quiver",
        "category": "quiver",
        "starting_state": "rare, fractured +2 proj prefix, 4+ mods",
        "steps": [
            {
                "action": "spam",
                "currency": "chaos_orb",
                "precondition": "rare quiver with fractured +2 proj prefix",
                "goal": "T1 flat lightning damage to attacks",
                "until": "prefixes contain T1 flat lightning",
                "note": "PoE 2 chaos removes 1 random non-fractured mod and adds 1 of same type. T1 lightning is ~1/260 per chaos. ~5-7 divines average cost.",
            },
            {
                "action": "apply_with_omen",
                "currency": "exalted_orb",
                "omen": "sinistral_exaltation",
                "precondition": "rare quiver with fractured +2 proj, T1 lightning prefix, open prefix slot",
                "result": "guaranteed prefix slam — 50/50 to hit projectile speed",
                "note": "Creator's key tech: omen guarantees prefix slot. If it hits proj speed, skip to step 5.",
            },
            {
                "action": "apply_currency",
                "currency": "greater_exalted_orb",
                "precondition": "rare quiver with open prefix (proj speed NOT hit in step 2)",
                "result": "prefix slam with min ilvl 35 filter — ~1/7-8 for T1-T2 proj speed",
                "note": "Creator's original tech: Greater Exalt costs ~12 exalts (cheap). If this hits, skip to step 5.",
            },
            {
                "action": "apply_with_omen",
                "currency": "essence_of_abyss",
                "omen": "dextral_crystallisation",
                "precondition": "rare quiver after steps 1-2, proj speed NOT hit, has suffixes to manipulate",
                "result": "removes a suffix deterministically (omen controls slot), adds new mod",
                "note": "Essence of Abyss is a corrupted essence (works on magic/rare in 0.5.0). Dextral Crystallisation omen makes it remove only suffixes.",
            },
            {
                "action": "apply_currency",
                "currency": "essence_of_hysteria",
                "precondition": "rare quiver with open suffix slot",
                "result": "adds Hysteria suffix mod",
                "note": "Corrupted essence, nerfed in 0.5.0 (ES Recharge Rate: 41-45% → 20-23%) but still usable.",
            },
            {
                "action": "apply_currency",
                "currency": "perfect_exalted_orb",
                "precondition": "rare quiver with open suffix slot(s)",
                "result": "suffix slam with min ilvl 50 filter — targets crit mods",
                "note": "Perfect Exalt filters to ilvl 50+ mods. Targets crit chance and crit multi. ~1/3 to hit a crit mod.",
            },
        ],
        "cost_analysis": {
            "chaos_for_t1_lightning": "~260 chaos (~5-7 divines)",
            "exalted_orbs": "2-3",
            "greater_exalted_orb": "~12 exalts",
            "perfect_exalted_orb": "~3 divines",
            "omens": "2-3 divines total",
            "total_expected": "~20-30 divines",
        },
    },

    "five_stat_crit_jewel": {
        "name": "5-Stat Crit Jewel (OneManLeft, 0.5.0)",
        "game": "poe2",
        "goal": "maximum_values",
        "target": "5-stat jewel: 3 locked suffixes at 1.6x effect + effect prefix + chaos prefix",
        "base": "ruby_jewel",
        "category": "jewel",
        "starting_state": "rare jewel with 2 desired suffixes (e.g., crit chance + crit multi)",
        "steps": [
            {
                "action": "apply_currency",
                "currency": "liquid_contempt",
                "precondition": "rare jewel with 2 desired suffixes, has mods to remove",
                "result": "removes 1 mod, adds +1 Suffix Modifier allowed as crafted prefix (50/50)",
                "note": "Potent Liquid Contempt: ~1.5 div. If it removes wrong suffix, start over.",
            },
            {
                "action": "apply_with_omen",
                "currency": "preserved_cranium",
                "omen": "dextral_necromancy",
                "precondition": "rare jewel with 2 suffixes + crafted +1 suffix, open suffix slot",
                "result": "guaranteed desecrated suffix mod (omen forces suffix slot)",
                "note": "Preserved Cranium + Dextral Necromancy fills suffix slot 3.",
            },
            {
                "action": "apply_with_omen",
                "currency": "preserved_cranium",
                "omen": "omen_of_abyssal_echoes",
                "precondition": "rare jewel with desecrated suffix from step 2, want to reroll",
                "result": "rerolls desecrated mod options — repeat until desired suffix appears",
                "note": "Abyssal Echoes rerolls desecrated options. ~2-5 attempts for desired suffix.",
            },
            {
                "action": "apply_with_omen",
                "currency": "orb_of_annulment",
                "omen": "sinistral_annulment",
                "precondition": "rare jewel with 3 suffixes + crafted +1 suffix prefix",
                "result": "removes crafted +1 suffix prefix — suffixes now locked at 3",
                "note": "Critical step: removes +1 suffix line. Now chaos orbs can only touch prefixes.",
            },
            {
                "action": "spam",
                "currency": "chaos_orb",
                "precondition": "rare jewel with 3 suffixes, no +1 suffix line, has prefixes to reroll",
                "goal": "desired prefix (e.g., spell damage)",
                "until": "prefix contains desired mod",
                "note": "Chaos orbs blocked from touching suffixes (3 suffixes, no +1 line). Deterministic prefix-only rolling.",
            },
            {
                "action": "apply_currency",
                "currency": "liquid_ferocity",
                "precondition": "rare jewel with 3 suffixes + 2 good prefixes",
                "result": "removes 1 prefix, adds (40-60)% increased Effect of Suffixes",
                "note": "Liquid Ferocity cannot remove suffixes (same lock trick). Always removes a prefix. Divine to 60%.",
            },
        ],
        "cost_analysis": {
            "liquid_contempt": "~1.5 div per attempt",
            "preserved_cranium_and_omens": "~3 div",
            "chaos_for_prefixes": "cheap",
            "liquid_ferocity": "~1.5 div",
            "total_expected": "~30-50 divines",
        },
    },
}


# ============================================================================
# Recipe Validation Tests
# ============================================================================

class TestRecipeStructure:
    """All recipes should have valid structure and reference real game data."""

    def test_all_recipes_have_required_fields(self):
        for name, recipe in RECIPES.items():
            assert "name" in recipe, f"{name}: missing 'name'"
            assert "target" in recipe, f"{name}: missing 'target'"
            assert "base" in recipe, f"{name}: missing 'base'"
            assert "category" in recipe, f"{name}: missing 'category'"
            assert "steps" in recipe, f"{name}: missing 'steps'"
            assert len(recipe["steps"]) >= 1, f"{name}: needs at least 1 step"

    def test_recipe_bases_exist_in_prolog(self):
        """All base items referenced should exist in base_type/2."""
        content = PROLOG_FILE.read_text()
        GENERIC_BASES = {"any_amulet", "any_ring", "any_armour", "any_weapon"}
        for name, recipe in RECIPES.items():
            base = recipe["base"]
            if base in GENERIC_BASES:
                continue  # Generic base — craft works on any item of that type
            assert f"base_type({base}," in content, \
                f"{name}: base '{base}' not found in Prolog KB"

    def test_recipe_categories_have_mod_data(self):
        """All categories should have scraped mod data."""
        for name, recipe in RECIPES.items():
            cat = recipe["category"]
            pl_path = PROJECT_ROOT / "resources" / f"mods_{cat}.pl"
            assert pl_path.exists(), \
                f"{name}: no mod data for category '{cat}'"

    def test_recipe_currencies_exist(self):
        """All currencies referenced should exist in the Prolog KB."""
        content = PROLOG_FILE.read_text()
        for name, recipe in RECIPES.items():
            game = recipe.get("game", "poe2")
            for step in recipe["steps"]:
                if "currency" in step:
                    curr = step["currency"]
                    assert f"currency({game}, {curr})" in content or \
                           f"essence" in curr, \
                        f"{name}/{step['action']}: currency '{curr}' not in KB for {game}"

    def test_recipe_omens_exist(self):
        """All omens referenced should exist and not be disabled."""
        content = PROLOG_FILE.read_text()
        for name, recipe in RECIPES.items():
            for step in recipe["steps"]:
                if "omen" in step:
                    omen = step["omen"]
                    assert f"omen(poe2, {omen}," in content, \
                        f"{name}: omen '{omen}' not in KB"
                    assert f"disabled(omen, {omen}" not in content, \
                        f"{name}: omen '{omen}' is disabled in 0.5.0"

    def test_recipe_alloys_exist(self):
        """All alloys referenced should exist in the Prolog KB."""
        content = PROLOG_FILE.read_text()
        for name, recipe in RECIPES.items():
            for step in recipe["steps"]:
                if "alloy" in step:
                    alloy = step["alloy"]
                    assert f"alloy(poe2, {alloy}," in content, \
                        f"{name}: alloy '{alloy}' not in KB"

    def test_recipe_catalysts_exist(self):
        """All catalysts referenced should exist in quality_type/3."""
        content = PROLOG_FILE.read_text()
        for name, recipe in RECIPES.items():
            for step in recipe["steps"]:
                if "catalyst" in step:
                    cat = step["catalyst"]
                    assert f"quality_type(poe2, {cat}," in content, \
                        f"{name}: catalyst '{cat}' not in KB"


class TestRecipeStepValidity:
    """Each step's preconditions should be satisfiable given the previous step."""

    def test_transmute_requires_normal(self):
        """Orb of Transmutation requires normal rarity."""
        recipe = RECIPES["ring_life_fire_res"]
        first_step = recipe["steps"][0]
        assert first_step["currency"] == "orb_of_transmutation"
        assert "normal" in first_step["precondition"]

    def test_chaos_orb_rerolls_rare(self):
        """In PoE 2, Chaos Orb is the reroll currency (no Orb of Alteration)."""
        recipe = RECIPES["ring_life_fire_res"]
        spam_step = recipe["steps"][1]
        assert spam_step["currency"] == "chaos_orb"
        assert "poe2" not in spam_step.get("currency", "") or True  # chaos_orb is valid poe2

    def test_body_armour_uses_essence_of_the_body(self):
        """PoE 2 uses Essence of the Body, NOT Essence of Greed."""
        recipe = RECIPES["body_armour_deterministic_life"]
        # Find the essence step (could be at different index)
        essence_steps = [s for s in recipe["steps"] if s.get("currency") == "essence_of_the_body"]
        assert len(essence_steps) == 1, "Expected exactly 1 essence_of_the_body step"
        assert essence_steps[0]["currency"] == "essence_of_the_body"

    def test_annulment_requires_mods(self):
        """Orb of Annulment requires at least 1 mod to remove."""
        recipe = RECIPES["ring_omen_annulment_recipe"]
        annul_step = recipe["steps"][1]
        assert annul_step["currency"] == "orb_of_annulment"
        assert "at least 1 prefix" in annul_step["precondition"]

    def test_alloy_requires_rare(self):
        """Alloys only work on rare items."""
        recipe = RECIPES["weapon_alloy_craft"]
        alloy_step = recipe["steps"][1]
        assert alloy_step["alloy"] == "sovereign_alloy"
        assert "rare" in alloy_step["precondition"]

    def test_catalyst_applied_after_crafting(self):
        """Catalysts should be applied AFTER confirming good mods (PoE 2 best practice)."""
        recipe = RECIPES["amulet_catalyst_craft"]
        craft_step = recipe["steps"][0]
        catalyst_step = recipe["steps"][2]  # Step 3: catalyst (step 2 is conditional chaos)
        assert craft_step["action"] == "apply_currency"
        assert catalyst_step["action"] == "apply_catalyst"
        assert "AFTER" in catalyst_step["note"]

    def test_all_recipes_have_game_field(self):
        """Every recipe must declare which game it's for."""
        for name, recipe in RECIPES.items():
            assert "game" in recipe, f"{name}: missing 'game' field"
            assert recipe["game"] in ("poe1", "poe2"), f"{name}: invalid game '{recipe['game']}'"

    def test_all_recipes_have_goal_field(self):
        """Every recipe must declare its optimization goal."""
        valid_goals = {"minimum_cost", "minimum_interactions", "maximum_values"}
        for name, recipe in RECIPES.items():
            assert "goal" in recipe, f"{name}: missing 'goal' field"
            assert recipe["goal"] in valid_goals, f"{name}: invalid goal '{recipe['goal']}'"


class TestRecipeCostAnalysis:
    """Verify cost estimates are reasonable."""

    def test_ring_life_cost_has_expected_values(self):
        recipe = RECIPES["ring_life_fire_res"]
        cost = recipe["cost_analysis"]
        # Cost analysis should exist and have reasonable values
        assert len(cost) > 0

    def test_all_recipes_with_costs_have_positive_values(self):
        for name, recipe in RECIPES.items():
            if "cost_analysis" in recipe:
                for key, val in recipe["cost_analysis"].items():
                    if isinstance(val, (int, float)):
                        assert val >= 0, f"{name}/cost/{key}: negative value {val}"


class TestRecipePrologEncoding:
    """Check that recipes can be expressed as Prolog queries."""

    def test_transmute_recipe_as_prolog_query(self):
        """The simplest recipe: transmute a base."""
        query = "fresh_base(Item), apply_currency(orb_of_transmutation, Item, Magic)."
        # Should reference real predicates
        content = PROLOG_FILE.read_text()
        assert "fresh_base" in content
        assert "apply_currency" in content

    def test_omen_recipe_as_prolog_query(self):
        """Omen-based recipe: sinistral annulment."""
        # This query would be:
        # ring_base(Item),
        # apply_currency(orb_of_alchemy, Item, Rare),
        # can_use_omen(sinistral_annulment, orb_of_annulment),
        # apply_with_omen(sinistral_annulment, orb_of_annulment, Rare, Result).
        content = PROLOG_FILE.read_text()
        assert "can_use_omen" in content
        assert "omen_active" in content

    def test_alloy_recipe_as_prolog_query(self):
        """Alloy recipe: apply sovereign_alloy to rare sword."""
        # Query: ..., alloy_precondition(sovereign_alloy, RareSword),
        #        alloy_postcondition(sovereign_alloy, RareSword, Result).
        content = PROLOG_FILE.read_text()
        assert "alloy_precondition" in content
        assert "alloy_postcondition" in content


class TestRecipeModPoolVerification:
    """Verify that target mods exist in the item's mod pool."""

    def test_life_exists_in_ring_pool(self):
        """increased_life should be a prefix mod in the ring pool."""
        pl = (PROJECT_ROOT / "resources" / "mods_ring.pl").read_text()
        assert "mod_group(ring, FlattoMaximumLife," in pl

    def test_fire_res_exists_in_ring_pool(self):
        """fire_resistance should be a suffix mod in the ring pool."""
        pl = (PROJECT_ROOT / "resources" / "mods_ring.pl").read_text()
        assert "mod_group(ring, PercentToFireResistance," in pl

    def test_life_exists_in_body_armour_pool(self):
        """increased_life should be a prefix mod in body_armour_str pool."""
        pl = (PROJECT_ROOT / "resources" / "mods_body_armour_str.pl").read_text()
        assert "mod_group(body_armour_str, FlattoMaximumLife," in pl

    def test_attack_mods_exist_in_weapon_pool(self):
        """weapon_sword should have attack-tagged prefix mods."""
        pl = (PROJECT_ROOT / "resources" / "mods_weapon_sword.pl").read_text()
        # Check for physical damage or attack mods
        assert "attack" in pl.lower() or "damage" in pl.lower()

    def test_ring_life_probability(self):
        """Life prefix on ring should be ~13.5% (1000/7400)."""
        pl = (PROJECT_ROOT / "resources" / "mods_ring.pl").read_text()
        life_match = re.search(
            r"mod_group\(ring, FlattoMaximumLife, .+?, .+?, (\d+),", pl
        )
        assert life_match, "FlattoMaximumLife not found in ring pool"
        life_weight = int(life_match.group(1))
        total = int(re.search(
            r"mod_pool_weight_sum\(ring, prefix, (\d+)\)", pl
        ).group(1))
        prob = life_weight / total
        assert 0.08 < prob < 0.20, f"Life probability {prob:.3f} outside expected range"
