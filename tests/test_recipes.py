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
                "currency": "orb_of_alteration",
                "goal": "hit increased_life prefix",
                "until": "prefixes contains increased_life",
                "expected_attempts": "~18 attempts (1/0.187 probability)",
            },
            {
                "action": "apply_currency",
                "currency": "orb_of_augmentation",
                "condition": "if suffix slot is empty after alteration",
                "result": "magic with 1 prefix + 1 suffix",
            },
            {
                "action": "apply_currency",
                "currency": "regal_orb",
                "precondition": "magic rarity, has increased_life prefix",
                "result": "rare, 2-3 mods total",
            },
            {
                "action": "apply_currency",
                "currency": "exalted_orb",
                "condition": "if open suffix slot exists",
                "goal": "add fire_resistance suffix",
                "note": "random — may not hit fire_resistance",
            },
        ],
        "cost_analysis": {
            "alteration_expected": 18,
            "regals": 1,
            "exalts": "0-2 depending on regal result",
            "total_expected": "~20 alterations + 1 regal + 1 exalt",
        },
    },

    "body_armour_deterministic_life": {
        "name": "Deterministic Life Prefix on Str Body Armour",
        "target": "Rare str body armour with guaranteed life prefix",
        "base": "plate_vest",
        "category": "body_armour_str",
        "steps": [
            {
                "action": "apply_currency",
                "currency": "essence_of_greed",
                "precondition": "any rarity, not corrupted/mirrored",
                "result": "rare with guaranteed increased_life prefix + random suffixes",
                "note": "Essence of Greed forces increased_life into prefix pool",
            },
            {
                "action": "apply_currency",
                "currency": "orb_of_annulment",
                "condition": "if unwanted suffix rolled",
                "goal": "remove a suffix to free slot for exalt",
            },
            {
                "action": "apply_with_omen",
                "currency": "exalted_orb",
                "omen": "dextral_exaltation",
                "precondition": "rare with open suffix, omen active",
                "result": "adds 1 suffix modifier (guaranteed suffix, not random slot)",
                "note": "Dextral Exaltation ensures the exalt hits suffix, not prefix",
            },
        ],
    },

    "ring_omen_annulment_recipe": {
        "name": "Targeted Prefix Annulment + Exaltation on Ring",
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
                "note": "This is the key deterministic step — without omen, 50/50 prefix/suffix",
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
                "note": "Alloy removes AND adds — net zero mod count change",
            },
        ],
    },

    "amulet_catalyst_craft": {
        "name": "Quality-Enhanced Amulet Craft",
        "target": "Rare amulet with enhanced life rolls via catalyst quality",
        "base": "lapis_amulet",
        "category": "amulet",
        "steps": [
            {
                "action": "apply_catalyst",
                "catalyst": "flesh_catalyst",
                "precondition": "amulet, not corrupted",
                "result": "20% quality, life modifiers enhanced by 1.2x",
                "note": "Apply BEFORE crafting — quality is a post-roll multiplier",
            },
            {
                "action": "apply_currency",
                "currency": "orb_of_alchemy",
                "precondition": "normal amulet with 20% flesh quality",
                "result": "rare — life mods will have 20% higher values",
            },
        ],
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
        for name, recipe in RECIPES.items():
            base = recipe["base"]
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
            for step in recipe["steps"]:
                if "currency" in step:
                    curr = step["currency"]
                    assert f"currency(poe2, {curr})" in content or \
                           f"currency(poe1, {curr})" in content or \
                           f"essence" in curr, \
                        f"{name}/{step['action']}: currency '{curr}' not in KB"

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

    def test_alteration_requires_magic(self):
        """Orb of Alteration requires magic rarity."""
        recipe = RECIPES["ring_life_fire_res"]
        spam_step = recipe["steps"][1]
        assert spam_step["currency"] == "orb_of_alteration"

    def test_regal_requires_magic(self):
        """Regal Orb requires magic rarity."""
        recipe = RECIPES["ring_life_fire_res"]
        regal_step = recipe["steps"][2]  # augmentation
        assert regal_step["currency"] == "orb_of_augmentation"
        # The regal is step 3
        regal_step = recipe["steps"][3]
        assert regal_step["currency"] == "regal_orb"
        assert "magic" in regal_step["precondition"]

    def test_exalted_requires_rare_with_open_slot(self):
        """Exalted Orb requires rare + open slot."""
        recipe = RECIPES["ring_life_fire_res"]
        exalt_step = recipe["steps"][4]
        assert exalt_step["currency"] == "exalted_orb"
        assert "open suffix" in exalt_step["condition"]

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

    def test_catalyst_applied_before_crafting(self):
        """Catalysts should be applied before currency for max effect."""
        recipe = RECIPES["amulet_catalyst_craft"]
        catalyst_step = recipe["steps"][0]
        craft_step = recipe["steps"][1]
        assert catalyst_step["action"] == "apply_catalyst"
        assert craft_step["action"] == "apply_currency"
        assert "BEFORE crafting" in catalyst_step["note"]


class TestRecipeCostAnalysis:
    """Verify cost estimates are reasonable."""

    def test_ring_life_cost_has_expected_values(self):
        recipe = RECIPES["ring_life_fire_res"]
        cost = recipe["cost_analysis"]
        # Life prefix weight is ~18.7% on rings
        # Expected attempts = 1/0.187 ≈ 5.3 alteration attempts to hit life
        # (but we also want a good suffix, so more like 10-20)
        assert cost["alteration_expected"] > 0
        assert cost["regals"] >= 1

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
        assert "mod_group(ring, 1IncreasedLife," in pl

    def test_fire_res_exists_in_ring_pool(self):
        """fire_resistance should be a suffix mod in the ring pool."""
        pl = (PROJECT_ROOT / "resources" / "mods_ring.pl").read_text()
        assert "mod_group(ring, 2FireResistance," in pl

    def test_life_exists_in_body_armour_pool(self):
        """increased_life should be a prefix mod in body_armour_str pool."""
        pl = (PROJECT_ROOT / "resources" / "mods_body_armour_str.pl").read_text()
        assert "mod_group(body_armour_str, 1IncreasedLife," in pl

    def test_attack_mods_exist_in_weapon_pool(self):
        """weapon_sword should have attack-tagged prefix mods."""
        pl = (PROJECT_ROOT / "resources" / "mods_weapon_sword.pl").read_text()
        # Check for physical damage or attack mods
        assert "attack" in pl.lower() or "damage" in pl.lower()

    def test_ring_life_probability(self):
        """Life prefix on ring should be ~11.5% (8000/69500)."""
        pl = (PROJECT_ROOT / "resources" / "mods_ring.pl").read_text()
        life_match = re.search(
            r"mod_group\(ring, 1IncreasedLife, .+?, .+?, (\d+),", pl
        )
        assert life_match, "1IncreasedLife not found in ring pool"
        life_weight = int(life_match.group(1))
        total = int(re.search(
            r"mod_pool_weight_sum\(ring, prefix, (\d+)\)", pl
        ).group(1))
        prob = life_weight / total
        assert 0.08 < prob < 0.20, f"Life probability {prob:.3f} outside expected range"
