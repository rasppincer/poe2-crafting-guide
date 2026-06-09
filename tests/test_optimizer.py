"""Tests for the recipe optimizer."""

import pytest
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


class TestOptimizerDataLoading:
    """Optimizer should load mod data correctly."""

    def test_optimizer_loads_mod_groups(self):
        from optimizer import RecipeOptimizer
        opt = RecipeOptimizer()
        assert len(opt.mod_groups) > 200, f"Expected 200+ mod groups, got {len(opt.mod_groups)}"

    def test_optimizer_loads_weight_sums(self):
        from optimizer import RecipeOptimizer
        opt = RecipeOptimizer()
        assert "ring" in opt.weight_sums
        assert "prefix" in opt.weight_sums["ring"]
        assert opt.weight_sums["ring"]["prefix"] > 0

    def test_optimizer_loads_tier_details(self):
        from optimizer import RecipeOptimizer
        opt = RecipeOptimizer()
        assert len(opt.tier_details) > 10, f"Expected 10+ tier details, got {len(opt.tier_details)}"


class TestModProbability:
    """Mod probability calculations should be correct."""

    def test_life_prefix_on_ring(self):
        from optimizer import RecipeOptimizer
        opt = RecipeOptimizer()
        prob = opt.mod_probability("ring", "1IncreasedLife")
        assert prob is not None
        assert 0.08 < prob.probability < 0.20, f"Life prob {prob.probability} outside expected range"
        assert 5 < prob.expected_attempts < 15

    def test_life_prefix_on_body_armour(self):
        from optimizer import RecipeOptimizer
        opt = RecipeOptimizer()
        prob = opt.mod_probability("body_armour_str", "1IncreasedLife")
        assert prob is not None
        assert 0.20 < prob.probability < 0.30, f"Body armour life prob {prob.probability}"

    def test_nonexistent_mod_returns_none(self):
        from optimizer import RecipeOptimizer
        opt = RecipeOptimizer()
        prob = opt.mod_probability("ring", "NonExistentMod")
        assert prob is None

    def test_fire_res_suffix_on_ring(self):
        from optimizer import RecipeOptimizer
        opt = RecipeOptimizer()
        prob = opt.mod_probability("ring", "2FireResistance")
        assert prob is not None
        assert prob.slot == "suffix"
        assert 0.05 < prob.probability < 0.15


class TestCombinedProbability:
    """Combined probability for multiple target mods."""

    def test_life_plus_fire_on_ring(self):
        from optimizer import RecipeOptimizer
        opt = RecipeOptimizer()
        p = opt.combined_probability("ring", [
            ("1IncreasedLife", "prefix"),
            ("2FireResistance", "suffix"),
        ])
        # Should be around 11.5% * 9.2% ≈ 1.06%
        assert 0.005 < p < 0.02, f"Combined prob {p} outside expected range"

    def test_single_mod_combined(self):
        from optimizer import RecipeOptimizer
        opt = RecipeOptimizer()
        p = opt.combined_probability("body_armour_str", [
            ("1IncreasedLife", "prefix"),
        ])
        assert 0.20 < p < 0.30


class TestCostEstimation:
    """Cost estimates should be reasonable."""

    def test_chaos_spam_ring_life_fire(self):
        from optimizer import RecipeOptimizer
        opt = RecipeOptimizer()
        cost = opt.estimate_chaos_spam_cost("ring", ["1IncreasedLife"], ["2FireResistance"])
        assert cost.total_steps > 0
        assert cost.total_expected["chaos_orb"] > 10  # Should need many attempts
        assert cost.total_expected["chaos_orb"] < 500

    def test_chaos_spam_body_armour_life(self):
        from optimizer import RecipeOptimizer
        opt = RecipeOptimizer()
        cost = opt.estimate_chaos_spam_cost("body_armour_str", ["1IncreasedLife"], [])
        # Life is 24% on body armour, so ~4 chaos expected
        assert 2 < cost.total_expected["chaos_orb"] < 20

    def test_essence_guarantees_mod(self):
        from optimizer import RecipeOptimizer
        opt = RecipeOptimizer()
        cost = opt.estimate_essence_cost("body_armour_str", "1IncreasedLife", ["1IncreasedLife"], [])
        # Essence alone should suffice
        assert cost.total_steps == 2
        assert "chaos_orb" not in cost.total_expected


class TestRecipeEvaluation:
    """Recipe evaluation should produce valid results."""

    def test_evaluate_all_recipes(self):
        from optimizer import evaluate_all_recipes
        results = evaluate_all_recipes()
        assert len(results) >= 5
        for name, evaluation in results.items():
            assert evaluation.score >= 0
            assert evaluation.score <= 100
            assert evaluation.goal in ("minimum_cost", "minimum_interactions", "maximum_values")

    def test_body_armour_recipe_is_suboptimal(self):
        """The body armour recipe should be flagged as suboptimal (essence alone is better)."""
        from optimizer import RecipeOptimizer
        from tests.test_recipes import RECIPES
        opt = RecipeOptimizer()
        evaluation = opt.evaluate_recipe(RECIPES["body_armour_deterministic_life"])
        # Score should be < 100 because essence alone uses fewer steps
        assert evaluation.score < 100, "Body armour recipe should be suboptimal"
        assert any("Essence" in r for r in evaluation.recommendations)

    def test_alloy_recipe_is_optimal(self):
        """The alloy recipe has no better alternative."""
        from optimizer import RecipeOptimizer
        from tests.test_recipes import RECIPES
        opt = RecipeOptimizer()
        evaluation = opt.evaluate_recipe(RECIPES["weapon_alloy_craft"])
        assert evaluation.score == 100


class TestOptimizerAPI:
    """Test the optimizer API endpoints."""

    def test_optimize_all_endpoint(self, client):
        resp = client.get("/api/optimize")
        assert resp.status_code == 200
        data = resp.get_json()
        assert isinstance(data, list)
        assert len(data) >= 5
        assert "score" in data[0]

    def test_optimize_single_recipe(self, client):
        resp = client.get("/api/optimize/ring_life_fire_res")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "score" in data
        assert "alternatives" in data
        assert "recommendations" in data

    def test_optimize_nonexistent_recipe(self, client):
        resp = client.get("/api/optimize/nonexistent_recipe")
        assert resp.status_code == 404

    def test_mod_probability_endpoint(self, client):
        resp = client.get("/api/mod_probability/ring/1IncreasedLife")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "probability" in data
        assert "expected_attempts" in data
        assert 0.08 < data["probability"] < 0.20

    def test_mod_probability_not_found(self, client):
        resp = client.get("/api/mod_probability/ring/NonExistentMod")
        assert resp.status_code == 404


@pytest.fixture
def client():
    """Flask test client."""
    import sys
    sys.path.insert(0, str(PROJECT_ROOT))
    from app import app
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c
