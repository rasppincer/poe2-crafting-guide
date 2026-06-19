"""Monte Carlo Runner — aggregates N crafting runs for statistics.

Runs a crafting sequence N times and produces:
- Success rate (how often the target condition is met)
- Cost statistics (avg, median, p10, p90)
- Outcome distribution (which mods appeared most)
- Best/worst items

Usage:
    from monte_carlo import MonteCarloRunner
    runner = MonteCarloRunner()
    result = runner.run(base="ring", ilvl=80, steps=[...], n=1000)
    print(result.summary())
"""

import statistics
from collections import Counter
from dataclasses import dataclass, field
from typing import Optional

from executor import RunResult, run_single, CURRENCY_COST
from simulator import CraftingSimulator, Item


@dataclass
class MonteCarloResult:
    """Aggregated results from N crafting runs."""
    n_runs: int
    success_count: int
    failure_count: int

    # Cost stats (only for successful runs)
    avg_cost: float
    median_cost: float
    p10_cost: float
    p25_cost: float
    p75_cost: float
    p90_cost: float
    min_cost: int
    max_cost: int

    # Mod distribution
    mod_frequency: dict[str, int]  # mod_group -> how many times it appeared
    most_common_mods: list[tuple[str, int]]  # top 10

    # Best/worst runs
    cheapest_run: Optional[RunResult]
    most_expensive_run: Optional[RunResult]

    # All costs (for histogram)
    all_costs: list[int]

    # Per-step success tracking
    step_success_rates: dict[int, float]  # step_index -> success rate

    def summary(self) -> str:
        """Human-readable summary."""
        lines = [
            f"Monte Carlo Results ({self.n_runs} runs)",
            f"  Success rate: {self.success_count}/{self.n_runs} ({self.success_count/self.n_runs*100:.1f}%)",
        ]
        if self.success_count > 0:
            lines.extend([
                f"  Cost (successful runs):",
                f"    Average: {self.avg_cost:.1f} chaos",
                f"    Median:  {self.median_cost:.0f} chaos",
                f"    P10-P90: {self.p10_cost:.0f} - {self.p90_cost:.0f} chaos",
                f"    Min-Max: {self.min_cost} - {self.max_cost} chaos",
            ])
        if self.most_common_mods:
            lines.append(f"  Most common mods:")
            for mod, count in self.most_common_mods[:5]:
                lines.append(f"    {mod}: {count} times ({count/self.n_runs*100:.1f}%)")
        return "\n".join(lines)


class MonteCarloRunner:
    """Runs crafting sequences N times and aggregates statistics."""

    def __init__(self, seed: Optional[int] = None):
        self.seed = seed

    def run(
        self,
        base: str,
        ilvl: int,
        steps: list[dict],
        n: int = 1000,
        success_condition: Optional[dict] = None,
        max_concurrent: int = 1,
    ) -> MonteCarloResult:
        """Run the crafting sequence N times.

        Args:
            base: item category
            ilvl: item level
            steps: crafting sequence
            n: number of runs (default 1000, max 10000)
            success_condition: optional condition dict to check at end of each run
            max_concurrent: reserved for future parallel execution

        Returns:
            MonteCarloResult with aggregated statistics.
        """
        n = min(n, 10000)

        runs: list[RunResult] = []
        for i in range(n):
            seed = (self.seed + i) if self.seed is not None else None
            sim = CraftingSimulator(seed=seed)
            result = run_single(sim, base, ilvl, steps)
            runs.append(result)

        return self._aggregate(runs, success_condition)

    def _aggregate(
        self,
        runs: list[RunResult],
        success_condition: Optional[dict],
    ) -> MonteCarloResult:
        """Aggregate run results into statistics."""
        n = len(runs)

        # Determine success — use explicit condition if provided, otherwise use run's own success
        successes = []
        failures = []
        for r in runs:
            if success_condition:
                from executor import evaluate_condition
                is_success = evaluate_condition(success_condition, r.final_item)
            else:
                is_success = r.success

            if is_success:
                successes.append(r)
            else:
                failures.append(r)

        # Cost stats
        costs = [r.total_cost for r in successes]
        all_costs = [r.total_cost for r in runs]

        avg_cost = statistics.mean(costs) if costs else 0
        median_cost = statistics.median(costs) if costs else 0
        p10 = self._percentile(costs, 10) if costs else 0
        p25 = self._percentile(costs, 25) if costs else 0
        p75 = self._percentile(costs, 75) if costs else 0
        p90 = self._percentile(costs, 90) if costs else 0

        # Mod frequency
        mod_counter = Counter()
        for r in runs:
            for mod in r.final_item.all_mods:
                mod_counter[mod.group] += 1

        # Best/worst
        cheapest = min(successes, key=lambda r: r.total_cost) if successes else None
        most_expensive = max(successes, key=lambda r: r.total_cost) if successes else None

        # Step success rates
        step_counts: dict[int, tuple[int, int]] = {}  # step -> (success, total)
        for r in runs:
            for sr in r.steps:
                key = sr.step_index
                if key not in step_counts:
                    step_counts[key] = (0, 0)
                s, t = step_counts[key]
                step_counts[key] = (s + (1 if sr.success else 0), t + 1)

        step_success_rates = {
            k: v[0] / v[1] if v[1] > 0 else 0
            for k, v in step_counts.items()
        }

        return MonteCarloResult(
            n_runs=n,
            success_count=len(successes),
            failure_count=len(failures),
            avg_cost=avg_cost,
            median_cost=median_cost,
            p10_cost=p10,
            p25_cost=p25,
            p75_cost=p75,
            p90_cost=p90,
            min_cost=min(costs) if costs else 0,
            max_cost=max(costs) if costs else 0,
            mod_frequency=dict(mod_counter),
            most_common_mods=mod_counter.most_common(10),
            cheapest_run=cheapest,
            most_expensive_run=most_expensive,
            all_costs=all_costs,
            step_success_rates=step_success_rates,
        )

    @staticmethod
    def _percentile(data: list[int], pct: int) -> float:
        """Calculate percentile."""
        if not data:
            return 0
        sorted_data = sorted(data)
        idx = int(len(sorted_data) * pct / 100)
        idx = min(idx, len(sorted_data) - 1)
        return sorted_data[idx]
