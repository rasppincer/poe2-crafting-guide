"""Sequence Executor — runs crafting sequences on the simulator.

A sequence is a list of steps, each specifying a currency operation
and optional conditions for branching/looping.

Step format:
    {
        "action": "apply_currency" | "apply_essence" | "spam",
        "currency": "chaos_orb" | "orb_of_transmutation" | ...,
        "condition": { ... },  # optional: check before applying
        "on_success": "continue" | "goto:N" | "stop",
        "on_failure": "continue" | "goto:N" | "loop:N" | "restart" | "abort",
        "max_iterations": 100,  # for spam action
    }

Condition format:
    {
        "type": "has_mod" | "not_has_mod" | "prefix_count" | "suffix_count" |
                "mod_count" | "rarity_is" | "always",
        "mod_group": "...",  # for has_mod/not_has_mod
        "operator": ">=" | "<=" | "==" | ">" | "<",  # for count checks
        "value": 3,  # for count checks
        "rarity": "rare",  # for rarity_is
    }
"""

from dataclasses import dataclass, field
from typing import Any, Optional

from simulator import CraftingSimulator, Item


@dataclass
class StepResult:
    """Result of executing a single step."""
    step_index: int
    action: str
    currency: str
    success: bool
    item_state: str  # snapshot of item after step
    mods_added: list[str] = field(default_factory=list)
    mods_removed: list[str] = field(default_factory=list)
    note: str = ""


@dataclass
class RunResult:
    """Result of a single crafting run."""
    success: bool
    steps: list[StepResult]
    total_cost: int  # in chaos equivalent
    final_item: Item
    stopped_reason: str = ""


# Currency costs in chaos equivalent (rough PoE 2 rates)
CURRENCY_COST = {
    "orb_of_transmutation": 0,
    "orb_of_augmentation": 0,
    "orb_of_alchemy": 1,
    "chaos_orb": 1,
    "regal_orb": 2,
    "exalted_orb": 15,
    "orb_of_annulment": 5,
    "orb_of_chance": 1,
    "divine_orb": 200,
    "vaal_orb": 3,
    "essence_of_the_body": 2,
    "essence_of_wrath": 2,
}


def evaluate_condition(condition: dict, item: Item) -> bool:
    """Evaluate a condition against the current item state."""
    ctype = condition.get("type", "always")

    if ctype == "always":
        return True
    elif ctype == "has_mod":
        return item.has_mod(condition["mod_group"])
    elif ctype == "not_has_mod":
        return not item.has_mod(condition["mod_group"])
    elif ctype == "prefix_count":
        return _compare(item.prefix_count, condition["operator"], condition["value"])
    elif ctype == "suffix_count":
        return _compare(item.suffix_count, condition["operator"], condition["value"])
    elif ctype == "mod_count":
        return _compare(item.mod_count, condition["operator"], condition["value"])
    elif ctype == "rarity_is":
        return item.rarity == condition["rarity"]
    elif ctype == "rarity_not":
        return item.rarity != condition["rarity"]
    return True


def _compare(a: int, op: str, b: int) -> bool:
    ops = {">=": a >= b, "<=": a <= b, "==": a == b, ">": a > b, "<": a < b, "!=": a != b}
    return ops.get(op, False)


def run_single(
    sim: CraftingSimulator,
    base: str,
    ilvl: int,
    steps: list[dict],
    max_total_steps: int = 10000,
) -> RunResult:
    """Execute a single crafting run.

    Args:
        sim: the crafting simulator
        base: item category (e.g. "ring")
        ilvl: item level
        steps: list of step dicts
        max_total_steps: safety limit to prevent infinite loops

    Returns:
        RunResult with final item state and step history.
    """
    item = sim.create_item(base, ilvl)
    step_results = []
    total_cost = 0
    pc = 0  # program counter
    total_executed = 0

    while pc < len(steps) and total_executed < max_total_steps:
        step = steps[pc]
        total_executed += 1

        action = step.get("action", "apply_currency")
        currency = step.get("currency", "")
        condition = step.get("condition")

        # Check condition if present
        if condition and not evaluate_condition(condition, item):
            # Condition failed — follow on_failure
            failure_action = step.get("on_failure", "continue")
            result = StepResult(
                step_index=pc, action=action, currency=currency,
                success=False, item_state=str(item),
                note=f"condition failed: {condition}"
            )
            step_results.append(result)

            pc = _handle_branch(failure_action, step, pc, steps)
            continue

        # Execute the action
        if action == "spam":
            remaining = max_total_steps - total_executed
            result, cost, stopped = _execute_spam(sim, item, step, max_remaining=remaining)
            step_results.extend(result)
            total_cost += cost
            total_executed += len(result)
            if stopped == "abort":
                return RunResult(
                    success=False, steps=step_results, total_cost=total_cost,
                    final_item=item, stopped_reason="spam aborted"
                )
            pc += 1
        else:
            # Single currency application
            mods_before = set(m.group for m in item.all_mods)
            success = sim.apply_currency(item, currency)
            mods_after = set(m.group for m in item.all_mods)
            cost = CURRENCY_COST.get(currency, 0)
            total_cost += cost

            added = list(mods_after - mods_before)
            removed = list(mods_before - mods_after)

            result = StepResult(
                step_index=pc, action=action, currency=currency,
                success=success, item_state=str(item),
                mods_added=added, mods_removed=removed,
            )
            step_results.append(result)

            # Handle branching
            if success:
                pc = _handle_branch(step.get("on_success", "continue"), step, pc, steps)
            else:
                pc = _handle_branch(step.get("on_failure", "continue"), step, pc, steps)

    stopped_reason = "completed" if pc >= len(steps) else "max_steps"
    return RunResult(
        success=pc >= len(steps),
        steps=step_results,
        total_cost=total_cost,
        final_item=item,
        stopped_reason=stopped_reason,
    )


def _execute_spam(
    sim: CraftingSimulator,
    item: Item,
    step: dict,
    max_remaining: int = 10000,
) -> tuple[list[StepResult], int, str]:
    """Execute a spam action (repeat currency until condition or max)."""
    currency = step.get("currency", "chaos_orb")
    max_iter = min(step.get("max_iterations", 100), max_remaining)
    until = step.get("until")  # condition to stop at
    cost = CURRENCY_COST.get(currency, 0)

    results = []
    total_cost = 0
    stopped = ""

    for i in range(max_iter):
        mods_before = set(m.group for m in item.all_mods)
        success = sim.apply_currency(item, currency)
        mods_after = set(m.group for m in item.all_mods)
        total_cost += cost

        added = list(mods_after - mods_before)
        removed = list(mods_before - mods_after)

        results.append(StepResult(
            step_index=step.get("_pc", 0), action="spam",
            currency=currency, success=success,
            item_state=str(item), mods_added=added, mods_removed=removed,
            note=f"iteration {i+1}/{max_iter}",
        ))

        # Check stop condition
        if until and evaluate_condition(until, item):
            stopped = "condition_met"
            break

    if not stopped:
        stopped = "max_iterations"

    return results, total_cost, stopped


def _handle_branch(action: str, step: dict, current_pc: int, steps: list[dict]) -> int:
    """Handle branching — return next PC."""
    if action == "continue":
        return current_pc + 1
    elif action == "stop":
        return len(steps)  # halt
    elif action.startswith("goto:"):
        target = int(action.split(":")[1])
        return target
    elif action.startswith("loop:"):
        # Loop back to current step, with max iterations
        max_loops = int(action.split(":")[1])
        # For simplicity, just go back — max_total_steps handles safety
        return current_pc
    elif action == "restart":
        return 0
    elif action == "abort":
        return len(steps)
    return current_pc + 1
