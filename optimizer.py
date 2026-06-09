"""Recipe Optimizer — evaluates crafting recipes against optimization goals.

Three optimization goals:
  - minimum_cost: cheapest method in expected currency
  - minimum_interactions: fewest crafting steps
  - maximum_values: highest possible numeric rolls

The optimizer loads mod weights from the Prolog data files to calculate
hit probabilities, expected attempts, and cost comparisons.
"""

import re
import math
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

PROJECT_ROOT = Path(__file__).parent
RESOURCES = PROJECT_ROOT / "resources"
PROLOG_FILE = PROJECT_ROOT / "poe2_crafting.pl"


# ============================================================================
# Data Loading
# ============================================================================

def load_mod_data():
    """Load all mod group data from Prolog files."""
    pl = PROLOG_FILE.read_text()
    # Load consulted data files
    for consult in re.findall(r":- consult\('([^']+)'\)", pl):
        data_path = PROJECT_ROOT / consult
        if data_path.exists():
            pl += "\n" + data_path.read_text()

    mod_groups = []
    for m in re.finditer(
        r"mod_group\((\w+),\s*(\w+),\s*'([^']*)',\s*\[([^\]]*)\],\s*(\d+),\s*(\d+),\s*(\d+),\s*(\w+)\)",
        pl
    ):
        tags = [t.strip() for t in m.group(4).split(",") if t.strip()]
        mod_groups.append({
            "category": m.group(1),
            "group": m.group(2),
            "description": m.group(3),
            "tags": tags,
            "weight": int(m.group(5)),
            "maxIlvl": int(m.group(6)),
            "tierCount": int(m.group(7)),
            "slot": m.group(8),
        })

    weight_sums = {}
    for m in re.finditer(r"mod_pool_weight_sum\((\w+),\s*(\w+),\s*(\d+)\)", pl):
        cat = m.group(1)
        weight_sums.setdefault(cat, {})[m.group(2)] = int(m.group(3))

    tier_details = []
    for m in re.finditer(
        r"mod_tier_detail\((\w+),\s*(\d+),\s*(\w+),\s*(\d+),\s*(\d+)-(\d+)\)",
        pl
    ):
        tier_details.append({
            "mod_group": m.group(1),
            "tier": int(m.group(2)),
            "name": m.group(3),
            "min_ilvl": int(m.group(4)),
            "range_min": int(m.group(5)),
            "range_max": int(m.group(6)),
        })

    return mod_groups, weight_sums, tier_details


# ============================================================================
# Core Calculations
# ============================================================================

@dataclass
class ModProbability:
    """Probability of rolling a specific mod."""
    mod_group: str
    category: str
    slot: str
    weight: int
    total_weight: int
    probability: float  # 0.0 to 1.0
    expected_attempts: float  # 1/probability


@dataclass
class CostEstimate:
    """Estimated cost for a crafting method."""
    method_name: str
    steps: list  # list of (action, currency, count) tuples
    total_expected: dict  # currency → expected count
    total_steps: int
    description: str


@dataclass
class RecipeEvaluation:
    """Full evaluation of a recipe against its goal."""
    recipe_name: str
    goal: str
    current_method: CostEstimate
    alternatives: list  # list of CostEstimate
    recommendations: list  # list of strings
    score: float  # 0-100, how optimal the current method is


class RecipeOptimizer:
    """Evaluates crafting recipes for optimality."""

    def __init__(self):
        self.mod_groups, self.weight_sums, self.tier_details = load_mod_data()
        self._build_indexes()

    def _build_indexes(self):
        """Build lookup indexes for fast access."""
        # Index: (category, slot) → list of mod_groups
        self.by_cat_slot = {}
        for mg in self.mod_groups:
            key = (mg["category"], mg["slot"])
            self.by_cat_slot.setdefault(key, []).append(mg)

        # Index: (category, mod_group_name) → mod_group
        self.by_name = {}
        for mg in self.mod_groups:
            self.by_name[(mg["category"], mg["group"])] = mg

    def mod_probability(self, category: str, mod_group_name: str) -> Optional[ModProbability]:
        """Calculate the probability of rolling a specific mod in its pool."""
        mg = self.by_name.get((category, mod_group_name))
        if not mg:
            return None

        slot = mg["slot"]
        total = self.weight_sums.get(category, {}).get(slot, 1)

        return ModProbability(
            mod_group=mod_group_name,
            category=category,
            slot=slot,
            weight=mg["weight"],
            total_weight=total,
            probability=mg["weight"] / total if total > 0 else 0,
            expected_attempts=total / mg["weight"] if mg["weight"] > 0 else float("inf"),
        )

    def combined_probability(self, category: str, target_mods: list[tuple[str, str]]) -> float:
        """Calculate probability of hitting a combination of mods.

        Args:
            category: e.g. 'ring'
            target_mods: list of (mod_group_name, slot) e.g. [('1IncreasedLife', 'prefix'), ('2FireResistance', 'suffix')]

        Returns:
            Probability of all target mods appearing in a single roll.
        """
        # Group by slot
        slot_targets = {}
        for mod_name, slot in target_mods:
            slot_targets.setdefault(slot, []).append(mod_name)

        combined_p = 1.0
        for slot, mod_names in slot_targets.items():
            total = self.weight_sums.get(category, {}).get(slot, 1)
            for mod_name in mod_names:
                mg = self.by_name.get((category, mod_name))
                if mg:
                    combined_p *= mg["weight"] / total if total > 0 else 0

        return combined_p

    def estimate_chaos_spam_cost(self, category: str, target_prefixes: list[str],
                                  target_suffixes: list[str]) -> CostEstimate:
        """Estimate cost of chaos spam to hit target mods.

        For chaos spam, each attempt rerolls all mods. We need to hit
        at least the target mods (other mods can be anything).
        """
        # Calculate probability of hitting all target mods in one roll
        target_mods = [(m, "prefix") for m in target_prefixes] + \
                      [(m, "suffix") for m in target_suffixes]

        p = self.combined_probability(category, target_mods)

        if p <= 0:
            return CostEstimate(
                method_name="Chaos Spam",
                steps=[],
                total_expected={"chaos_orb": float("inf")},
                total_steps=0,
                description="Target mods not achievable via chaos spam",
            )

        expected_attempts = 1 / p

        return CostEstimate(
            method_name="Chaos Spam",
            steps=[
                ("apply_currency", "orb_of_transmutation", 1),
                ("apply_currency", "orb_of_alchemy", 1),
                ("spam", "chaos_orb", math.ceil(expected_attempts)),
            ],
            total_expected={
                "orb_of_transmutation": 1,
                "orb_of_alchemy": 1,
                "chaos_orb": math.ceil(expected_attempts),
            },
            total_steps=2 + math.ceil(expected_attempts),
            description=f"~{math.ceil(expected_attempts)} chaos orbs expected (p={p:.4f})",
        )

    def estimate_essence_cost(self, category: str, essence_target_mod: str,
                               target_prefixes: list[str], target_suffixes: list[str]) -> CostEstimate:
        """Estimate cost using an essence to guarantee one mod, then chaos for the rest.

        Essences guarantee one mod and upgrade magic→rare. The remaining mods
        are random from the pool.
        """
        # The essence guarantees essence_target_mod. We still need the other mods.
        other_prefixes = [m for m in target_prefixes if m != essence_target_mod]
        other_suffixes = target_suffixes

        if not other_prefixes and not other_suffixes:
            # Essence alone is sufficient
            return CostEstimate(
                method_name="Essence (Guaranteed)",
                steps=[
                    ("apply_currency", "orb_of_transmutation", 1),
                    ("apply_currency", "essence", 1),
                ],
                total_expected={
                    "orb_of_transmutation": 1,
                    "essence": 1,
                },
                total_steps=2,
                description="Essence guarantees the target mod in 1 attempt",
            )

        # Need additional mods after essence. These are random rolls.
        # Calculate probability of the remaining combination
        remaining = [(m, "prefix") for m in other_prefixes] + \
                    [(m, "suffix") for m in other_suffixes]

        p_remaining = self.combined_probability(category, remaining)

        if p_remaining <= 0:
            return CostEstimate(
                method_name="Essence + Chaos",
                steps=[],
                total_expected={"essence": 1, "chaos_orb": float("inf")},
                total_steps=0,
                description="Remaining target mods not achievable",
            )

        # After essence makes it rare, we chaos spam for the rest
        expected_chaos = 1 / p_remaining

        return CostEstimate(
            method_name="Essence + Chaos",
            steps=[
                ("apply_currency", "orb_of_transmutation", 1),
                ("apply_currency", "essence", 1),
                ("spam", "chaos_orb", math.ceil(expected_chaos)),
            ],
            total_expected={
                "orb_of_transmutation": 1,
                "essence": 1,
                "chaos_orb": math.ceil(expected_chaos),
            },
            total_steps=2 + math.ceil(expected_chaos),
            description=f"Essence guarantees 1 mod, ~{math.ceil(expected_chaos)} chaos for the rest (p={p_remaining:.4f})",
        )

    def count_recipe_steps(self, recipe: dict) -> int:
        """Count the number of interaction steps in a recipe."""
        return len(recipe.get("steps", []))

    def evaluate_recipe(self, recipe: dict) -> RecipeEvaluation:
        """Evaluate a recipe against its optimization goal.

        Args:
            recipe: A recipe dict from test_recipes.py RECIPES

        Returns:
            RecipeEvaluation with current method, alternatives, and recommendations.
        """
        goal = recipe.get("goal", "minimum_cost")
        category = recipe.get("category", "")
        steps = recipe.get("steps", [])

        # Build current method cost estimate
        current_total = {}
        current_steps_list = []
        for step in steps:
            action = step.get("action", "")
            currency = step.get("currency", step.get("alloy", step.get("catalyst", "")))
            current_steps_list.append((action, currency, 1))
            current_total[currency] = current_total.get(currency, 0) + 1

        current = CostEstimate(
            method_name="Current Recipe",
            steps=current_steps_list,
            total_expected=current_total,
            total_steps=len(steps),
            description=f"{len(steps)} steps",
        )

        # Generate alternatives based on goal
        alternatives = []
        recommendations = []

        # Find target mods from recipe description
        target_prefixes, target_suffixes = self._extract_target_mods(recipe, category)

        if target_prefixes or target_suffixes:
            # Alternative 1: Chaos spam
            chaos_est = self.estimate_chaos_spam_cost(category, target_prefixes, target_suffixes)
            alternatives.append(chaos_est)

            # Alternative 2: Essence + chaos (if applicable)
            essence_mod = self._find_essence_for_mod(target_prefixes, category)
            if essence_mod:
                essence_est = self.estimate_essence_cost(
                    category, essence_mod, target_prefixes, target_suffixes
                )
                alternatives.append(essence_est)

            # Generate recommendations based on goal
            if goal == "minimum_cost":
                best = min(alternatives + [current],
                          key=lambda c: sum(v for v in c.total_expected.values()
                                          if isinstance(v, (int, float)) and v < 10000))
                if best.method_name != "Current Recipe":
                    recommendations.append(
                        f"Consider {best.method_name}: {best.description}"
                    )

            elif goal == "minimum_interactions":
                best = min(alternatives + [current], key=lambda c: c.total_steps)
                if best.total_steps < current.total_steps:
                    recommendations.append(
                        f"{best.method_name} uses {best.total_steps} steps vs {current.total_steps} current"
                    )

            elif goal == "maximum_values":
                recommendations.append(
                    "For maximum values: use essences for guaranteed T1 mods, "
                    "then omen-controlled exalts for remaining slots"
                )

        # Score: how close to optimal
        score = 100.0  # Start perfect
        if alternatives:
            best_cost = min(
                sum(v for v in a.total_expected.values()
                    if isinstance(v, (int, float)) and v < 10000)
                for a in alternatives
            )
            current_cost = sum(v for v in current.total_expected.values()
                             if isinstance(v, (int, float)) and v < 10000)
            if current_cost > 0 and best_cost > 0:
                ratio = best_cost / current_cost
                score = max(0, min(100, ratio * 100))

        return RecipeEvaluation(
            recipe_name=recipe.get("name", "Unknown"),
            goal=goal,
            current_method=current,
            alternatives=alternatives,
            recommendations=recommendations,
            score=score,
        )

    def _extract_target_mods(self, recipe: dict, category: str) -> tuple[list[str], list[str]]:
        """Extract target mod group names from recipe context."""
        target_prefixes = []
        target_suffixes = []

        # Check recipe name and target for clues
        name = recipe.get("name", "").lower()
        target = recipe.get("target", "").lower()

        if "life" in name or "life" in target:
            # Find the life prefix for this category
            for mg in self.mod_groups:
                if mg["category"] == category and mg["slot"] == "prefix":
                    if "life" in mg["group"].lower() and "regen" not in mg["group"].lower():
                        target_prefixes.append(mg["group"])
                        break

        if "fire" in name or "fire" in target:
            for mg in self.mod_groups:
                if mg["category"] == category and mg["slot"] == "suffix":
                    if "fire" in mg["group"].lower() and "resist" in mg["group"].lower():
                        target_suffixes.append(mg["group"])
                        break

        return target_prefixes, target_suffixes

    def _find_essence_for_mod(self, target_prefixes: list[str], category: str) -> Optional[str]:
        """Find which essence can guarantee a target mod."""
        # Map mod groups to their essence equivalents
        # This is a simplified mapping — in practice, each essence has specific mods
        for mod_name in target_prefixes:
            if "life" in mod_name.lower():
                return mod_name  # Essence of the Body guarantees life
        return None


# ============================================================================
# Convenience Functions
# ============================================================================

def evaluate_all_recipes():
    """Evaluate all recipes and return results."""
    from tests.test_recipes import RECIPES

    optimizer = RecipeOptimizer()
    results = {}

    for name, recipe in RECIPES.items():
        results[name] = optimizer.evaluate_recipe(recipe)

    return results


def print_evaluation_report():
    """Print a human-readable evaluation report for all recipes."""
    results = evaluate_all_recipes()

    for name, eval_result in results.items():
        print(f"\n{'='*60}")
        print(f"Recipe: {eval_result.recipe_name}")
        print(f"Goal: {eval_result.goal}")
        print(f"Score: {eval_result.score:.0f}/100")
        print(f"Current: {eval_result.current_method.description}")

        if eval_result.alternatives:
            print("\nAlternatives:")
            for alt in eval_result.alternatives:
                print(f"  - {alt.method_name}: {alt.description}")

        if eval_result.recommendations:
            print("\nRecommendations:")
            for rec in eval_result.recommendations:
                print(f"  → {rec}")

    print(f"\n{'='*60}")
    print(f"Total recipes evaluated: {len(results)}")


if __name__ == "__main__":
    print_evaluation_report()
