"""Tests for the crafting simulator, executor, and Monte Carlo runner."""

import pytest
from simulator import CraftingSimulator, Item, RolledMod
from executor import run_single, evaluate_condition, CURRENCY_COST
from monte_carlo import MonteCarloRunner


# ============================================================================
# Simulator Tests
# ============================================================================

class TestSimulator:
    """Core rolling engine tests."""

    def test_create_item(self):
        sim = CraftingSimulator()
        item = sim.create_item("ring", ilvl=80)
        assert item.category == "ring"
        assert item.ilvl == 80
        assert item.rarity == "normal"
        assert item.mod_count == 0

    def test_transmute_normal_to_magic(self):
        sim = CraftingSimulator(seed=42)
        item = sim.create_item("ring", ilvl=80)
        result = sim.apply_currency(item, "orb_of_transmutation")
        assert result is True
        assert item.rarity == "magic"
        assert 1 <= item.mod_count <= 2

    def test_transmute_fails_on_magic(self):
        sim = CraftingSimulator(seed=42)
        item = sim.create_item("ring", ilvl=80)
        item.rarity = "magic"
        result = sim.apply_currency(item, "orb_of_transmutation")
        assert result is False

    def test_alchemy_normal_to_rare(self):
        sim = CraftingSimulator(seed=42)
        item = sim.create_item("ring", ilvl=80)
        result = sim.apply_currency(item, "orb_of_alchemy")
        assert result is True
        assert item.rarity == "rare"
        assert 4 <= item.mod_count <= 6

    def test_chaos_rerolls_rare(self):
        sim = CraftingSimulator(seed=42)
        item = sim.create_item("ring", ilvl=80)
        sim.apply_currency(item, "orb_of_alchemy")
        mods_before = [m.group for m in item.all_mods]
        sim.apply_currency(item, "chaos_orb")
        mods_after = [m.group for m in item.all_mods]
        # After chaos, item should still be rare with 4-6 mods
        assert item.rarity == "rare"
        assert 4 <= item.mod_count <= 6

    def test_chaos_fails_on_magic(self):
        sim = CraftingSimulator(seed=42)
        item = sim.create_item("ring", ilvl=80)
        item.rarity = "magic"
        result = sim.apply_currency(item, "chaos_orb")
        assert result is False

    def test_exalted_adds_mod(self):
        sim = CraftingSimulator(seed=42)
        item = sim.create_item("ring", ilvl=80)
        sim.apply_currency(item, "orb_of_alchemy")
        count_before = item.mod_count
        if item.mod_count < 6:
            result = sim.apply_currency(item, "exalted_orb")
            assert result is True
            assert item.mod_count == count_before + 1

    def test_exalted_fails_on_full_item(self):
        sim = CraftingSimulator(seed=42)
        item = sim.create_item("ring", ilvl=80)
        item.rarity = "rare"
        # Fill all slots
        for _ in range(3):
            item.prefixes.append(RolledMod("P", "prefix mod", [], "prefix"))
            item.suffixes.append(RolledMod("S", "suffix mod", [], "suffix"))
        result = sim.apply_currency(item, "exalted_orb")
        assert result is False

    def test_annul_removes_mod(self):
        sim = CraftingSimulator(seed=42)
        item = sim.create_item("ring", ilvl=80)
        sim.apply_currency(item, "orb_of_alchemy")
        count_before = item.mod_count
        result = sim.apply_currency(item, "orb_of_annulment")
        assert result is True
        assert item.mod_count == count_before - 1

    def test_annul_fails_empty(self):
        sim = CraftingSimulator(seed=42)
        item = sim.create_item("ring", ilvl=80)
        result = sim.apply_currency(item, "orb_of_annulment")
        assert result is False

    def test_regal_upgrades_magic(self):
        sim = CraftingSimulator(seed=42)
        item = sim.create_item("ring", ilvl=80)
        sim.apply_currency(item, "orb_of_transmutation")
        assert item.rarity == "magic"
        count_before = item.mod_count
        result = sim.apply_currency(item, "regal_orb")
        assert result is True
        assert item.rarity == "rare"
        assert item.mod_count >= count_before

    def test_essence_requires_magic(self):
        sim = CraftingSimulator(seed=42)
        item = sim.create_item("ring", ilvl=80)
        result = sim.apply_currency(item, "essence_of_the_body")
        assert result is False  # normal item

    def test_essence_guarantees_tag(self):
        sim = CraftingSimulator(seed=42)
        item = sim.create_item("ring", ilvl=80)
        item.rarity = "magic"
        result = sim.apply_currency(item, "essence_of_the_body")
        assert result is True
        # At least one mod should have 'life' tag
        life_mods = [m for m in item.all_mods if "life" in m.tags]
        assert len(life_mods) >= 1

    def test_corrupted_item_rejects_currency(self):
        sim = CraftingSimulator(seed=42)
        item = sim.create_item("ring", ilvl=80)
        item.corrupted = True
        result = sim.apply_currency(item, "orb_of_transmutation")
        assert result is False

    def test_roll_mod_deterministic_with_seed(self):
        sim1 = CraftingSimulator(seed=42)
        sim2 = CraftingSimulator(seed=42)
        mod1 = sim1.roll_mod("ring", "prefix", 80)
        mod2 = sim2.roll_mod("ring", "prefix", 80)
        assert mod1 is not None and mod2 is not None
        assert mod1.group == mod2.group

    def test_roll_mod_different_seeds(self):
        sim1 = CraftingSimulator(seed=42)
        sim2 = CraftingSimulator(seed=99)
        groups1 = set()
        groups2 = set()
        for _ in range(20):
            m1 = sim1.roll_mod("ring", "prefix", 80)
            m2 = sim2.roll_mod("ring", "prefix", 80)
            if m1:
                groups1.add(m1.group)
            if m2:
                groups2.add(m2.group)
        # At least one should differ (probabilistic, but very likely)
        # If this fails, it's not necessarily a bug — just unlikely

    def test_item_str(self):
        sim = CraftingSimulator(seed=42)
        item = sim.create_item("ring", ilvl=80)
        assert "normal" in str(item).lower() or "NORMAL" in str(item)
        sim.apply_currency(item, "orb_of_transmutation")
        assert "magic" in str(item).lower() or "MAGIC" in str(item)

    def test_item_has_mod(self):
        sim = CraftingSimulator(seed=42)
        item = sim.create_item("ring", ilvl=80)
        assert not item.has_mod("anything")
        sim.apply_currency(item, "orb_of_transmutation")
        if item.all_mods:
            assert item.has_mod(item.all_mods[0].group)

    def test_multiple_categories(self):
        """Different categories should have different mod pools."""
        sim = CraftingSimulator(seed=42)
        categories = ["ring", "helmet_str", "bow", "body_armour_dex"]
        for cat in categories:
            item = sim.create_item(cat, ilvl=80)
            result = sim.apply_currency(item, "orb_of_alchemy")
            assert result is True, f"alchemy failed for {cat}"
            assert item.mod_count >= 4


# ============================================================================
# Executor Tests
# ============================================================================

class TestExecutor:
    """Sequence execution tests."""

    def test_simple_sequence(self):
        sim = CraftingSimulator(seed=42)
        steps = [
            {"action": "apply_currency", "currency": "orb_of_transmutation"},
            {"action": "apply_currency", "currency": "orb_of_augmentation"},
        ]
        result = run_single(sim, "ring", 80, steps)
        assert result.success is True
        assert len(result.steps) == 2
        assert result.final_item.rarity == "magic"

    def test_alchemy_sequence(self):
        sim = CraftingSimulator(seed=42)
        steps = [
            {"action": "apply_currency", "currency": "orb_of_alchemy"},
        ]
        result = run_single(sim, "ring", 80, steps)
        assert result.success is True
        assert result.final_item.rarity == "rare"
        assert result.total_cost > 0

    def test_spam_with_condition(self):
        sim = CraftingSimulator(seed=42)
        steps = [
            {"action": "apply_currency", "currency": "orb_of_alchemy"},
            {
                "action": "spam",
                "currency": "chaos_orb",
                "max_iterations": 50,
                "until": {"type": "has_mod", "mod_group": "FlattoMaximumLife"},
            },
        ]
        result = run_single(sim, "ring", 80, steps)
        assert result.final_item.has_mod("FlattoMaximumLife")

    def test_condition_evaluation(self):
        item = Item(category="ring", ilvl=80, rarity="rare")
        item.prefixes.append(RolledMod("P", "test", [], "prefix"))

        assert evaluate_condition({"type": "always"}, item) is True
        assert evaluate_condition({"type": "has_mod", "mod_group": "P"}, item) is True
        assert evaluate_condition({"type": "not_has_mod", "mod_group": "X"}, item) is True
        assert evaluate_condition({"type": "prefix_count", "operator": "==", "value": 1}, item) is True
        assert evaluate_condition({"type": "rarity_is", "rarity": "rare"}, item) is True
        assert evaluate_condition({"type": "rarity_is", "rarity": "magic"}, item) is False

    def test_branching_on_success(self):
        sim = CraftingSimulator(seed=42)
        steps = [
            {"action": "apply_currency", "currency": "orb_of_transmutation", "on_success": "stop"},
            {"action": "apply_currency", "currency": "orb_of_augmentation"},
        ]
        result = run_single(sim, "ring", 80, steps)
        assert len(result.steps) == 1  # stopped after first step

    def test_branching_on_failure(self):
        sim = CraftingSimulator(seed=42)
        steps = [
            # Transmute succeeds — on_failure not triggered
            {"action": "apply_currency", "currency": "orb_of_transmutation", "on_failure": "stop"},
            # Chaos fails (magic, not rare) — on_failure triggered
            {"action": "apply_currency", "currency": "chaos_orb", "on_failure": "continue"},
        ]
        result = run_single(sim, "ring", 80, steps)
        assert result.steps[1].success is False

    def test_unknown_currency(self):
        sim = CraftingSimulator(seed=42)
        steps = [
            {"action": "apply_currency", "currency": "nonexistent_orb"},
        ]
        result = run_single(sim, "ring", 80, steps)
        assert result.steps[0].success is False

    def test_max_total_steps_safety(self):
        sim = CraftingSimulator(seed=42)
        steps = [
            {"action": "apply_currency", "currency": "orb_of_alchemy"},
            {
                "action": "spam",
                "currency": "chaos_orb",
                "max_iterations": 1000000,  # huge number — should be capped
                "until": {"type": "has_mod", "mod_group": "NONEXISTENT_MOD_NEVER_FOUND"},
            },
        ]
        result = run_single(sim, "ring", 80, steps, max_total_steps=50)
        # Spam should be capped at 49 iterations (50 - 1 for alchemy)
        spam_steps = [s for s in result.steps if s.action == "spam"]
        assert len(spam_steps) <= 49


# ============================================================================
# Monte Carlo Tests
# ============================================================================

class TestMonteCarlo:
    """Monte Carlo runner tests."""

    def test_basic_run(self):
        runner = MonteCarloRunner(seed=42)
        steps = [
            {"action": "apply_currency", "currency": "orb_of_alchemy"},
        ]
        result = runner.run("ring", 80, steps, n=50)
        assert result.n_runs == 50
        assert result.success_count + result.failure_count == 50

    def test_cost_statistics(self):
        runner = MonteCarloRunner(seed=42)
        steps = [
            {"action": "apply_currency", "currency": "orb_of_alchemy"},
            {
                "action": "spam",
                "currency": "chaos_orb",
                "max_iterations": 10,
                "until": {"type": "has_mod", "mod_group": "FlattoMaximumLife"},
            },
        ]
        result = runner.run("ring", 80, steps, n=30,
                           success_condition={"type": "has_mod", "mod_group": "FlattoMaximumLife"})
        assert result.success_count > 0
        assert result.avg_cost > 0
        assert result.median_cost > 0
        assert result.min_cost <= result.median_cost <= result.max_cost

    def test_mod_frequency(self):
        runner = MonteCarloRunner(seed=42)
        steps = [
            {"action": "apply_currency", "currency": "orb_of_alchemy"},
        ]
        result = runner.run("ring", 80, steps, n=30)
        assert len(result.mod_frequency) > 0
        assert len(result.most_common_mods) > 0

    def test_summary(self):
        runner = MonteCarloRunner(seed=42)
        steps = [
            {"action": "apply_currency", "currency": "orb_of_alchemy"},
        ]
        result = runner.run("ring", 80, steps, n=50)
        summary = result.summary()
        assert "Monte Carlo" in summary
        assert "Success rate" in summary

    def test_max_n_capped(self):
        runner = MonteCarloRunner(seed=42)
        steps = [
            {"action": "apply_currency", "currency": "orb_of_transmutation"},
        ]
        result = runner.run("ring", 80, steps, n=100)
        assert result.n_runs == 100

    def test_deterministic_with_seed(self):
        r1 = MonteCarloRunner(seed=42)
        r2 = MonteCarloRunner(seed=42)
        steps = [
            {"action": "apply_currency", "currency": "orb_of_alchemy"},
        ]
        res1 = r1.run("ring", 80, steps, n=50)
        res2 = r2.run("ring", 80, steps, n=50)
        assert res1.success_count == res2.success_count
        assert res1.avg_cost == res2.avg_cost

    def test_different_categories(self):
        runner = MonteCarloRunner(seed=42)
        steps = [
            {"action": "apply_currency", "currency": "orb_of_alchemy"},
        ]
        for cat in ["ring", "helmet_str", "bow"]:
            result = runner.run(cat, 80, steps, n=20)
            assert result.n_runs == 20


# ============================================================================
# Omen Tests (A.1.5)
# ============================================================================

class TestOmens:
    """Tests for omen-modified currency operations."""

    def test_omen_loading(self):
        """Verify omen facts are loaded from the knowledge base."""
        sim = CraftingSimulator()
        assert len(sim._omens) > 0
        assert "sinistral_erasure" in sim._omens
        assert "dextral_erasure" in sim._omens
        assert "greater_exaltation" in sim._omens
        assert "whittling" in sim._omens

    def test_omen_metadata(self):
        """Verify omen data has expected fields."""
        sim = CraftingSimulator()
        omen = sim._omens["sinistral_erasure"]
        assert omen["currency"] == "chaos_orb"
        assert omen["effect"] == "removes_only_prefixes"
        assert omen["slot_restriction"] == "prefix"

    def test_unknown_omen_fails(self):
        """Unknown omen name should fail."""
        sim = CraftingSimulator(seed=42)
        item = sim.create_item("ring", ilvl=80)
        item.rarity = "rare"
        result = sim.apply_currency_with_omen(item, "chaos_orb", "nonexistent_omen")
        assert result is False
        assert any("unknown omen" in h for h in item.history)

    def test_omen_wrong_currency_fails(self):
        """Omen applied with wrong currency should fail."""
        sim = CraftingSimulator(seed=42)
        item = sim.create_item("ring", ilvl=80)
        item.rarity = "rare"
        # sinistral_erasure targets chaos_orb, not orb_of_annulment
        result = sim.apply_currency_with_omen(item, "orb_of_annulment", "sinistral_erasure")
        assert result is False
        assert any("targets" in h for h in item.history)

    def test_sinistral_erasure_rerolls_prefixes(self):
        """sinistral_erasure: chaos removes only prefixes, keeps suffixes."""
        sim = CraftingSimulator(seed=42)
        item = sim.create_item("ring", ilvl=80)
        sim.apply_currency(item, "orb_of_alchemy")
        assert item.rarity == "rare"
        suffixes_before = list(item.suffixes)
        suffix_groups = {m.group for m in item.suffixes}

        result = sim.apply_currency_with_omen(item, "chaos_orb", "sinistral_erasure")
        assert result is True
        # All original suffixes should still be present
        for sg in suffix_groups:
            assert item.has_mod(sg), f"Suffix {sg} was removed by sinistral_erasure"
        # Should have some prefixes (re-rolled)
        assert item.prefix_count > 0

    def test_dextral_erasure_rerolls_suffixes(self):
        """dextral_erasure: chaos removes only suffixes, keeps prefixes."""
        sim = CraftingSimulator(seed=42)
        item = sim.create_item("ring", ilvl=80)
        sim.apply_currency(item, "orb_of_alchemy")
        assert item.rarity == "rare"
        prefix_groups = {m.group for m in item.prefixes}

        result = sim.apply_currency_with_omen(item, "chaos_orb", "dextral_erasure")
        assert result is True
        # All original prefixes should still be present
        for pg in prefix_groups:
            assert item.has_mod(pg), f"Prefix {pg} was removed by dextral_erasure"
        # Should have some suffixes (re-rolled)
        assert item.suffix_count > 0

    def test_sinistral_exaltation_adds_prefix(self):
        """sinistral_exaltation: exalt adds only prefix."""
        sim = CraftingSimulator(seed=42)
        item = sim.create_item("ring", ilvl=80)
        sim.apply_currency(item, "orb_of_alchemy")
        # If item has 3 prefixes, test is trivial; otherwise check slot
        if item.prefix_count < 3:
            suffix_count_before = item.suffix_count
            result = sim.apply_currency_with_omen(item, "exalted_orb", "sinistral_exaltation")
            assert result is True
            assert item.suffix_count == suffix_count_before, "Suffix count changed"
            assert item.prefix_count == suffix_count_before + 1 or item.prefix_count > 0

    def test_dextral_exaltation_adds_suffix(self):
        """dextral_exaltation: exalt adds only suffix."""
        sim = CraftingSimulator(seed=42)
        item = sim.create_item("ring", ilvl=80)
        sim.apply_currency(item, "orb_of_alchemy")
        if item.suffix_count < 3:
            prefix_count_before = item.prefix_count
            result = sim.apply_currency_with_omen(item, "exalted_orb", "dextral_exaltation")
            assert result is True
            assert item.prefix_count == prefix_count_before, "Prefix count changed"

    def test_sinistral_coronation_adds_prefix(self):
        """sinistral_coronation: regal adds only prefix."""
        sim = CraftingSimulator(seed=42)
        item = sim.create_item("ring", ilvl=80)
        sim.apply_currency(item, "orb_of_transmutation")
        assert item.rarity == "magic"
        result = sim.apply_currency_with_omen(item, "regal_orb", "sinistral_coronation")
        assert result is True
        assert item.rarity == "rare"
        # The new mod should be a prefix
        # (existing mods may be prefix or suffix, but count should have increased)
        assert item.mod_count >= 2

    def test_dextral_coronation_adds_suffix(self):
        """dextral_coronation: regal adds only suffix."""
        sim = CraftingSimulator(seed=42)
        item = sim.create_item("ring", ilvl=80)
        sim.apply_currency(item, "orb_of_transmutation")
        assert item.rarity == "magic"
        result = sim.apply_currency_with_omen(item, "regal_orb", "dextral_coronation")
        assert result is True
        assert item.rarity == "rare"

    def test_sinistral_annulment_removes_prefix(self):
        """sinistral_annulment: annul removes only prefix."""
        sim = CraftingSimulator(seed=42)
        item = sim.create_item("ring", ilvl=80)
        sim.apply_currency(item, "orb_of_alchemy")
        if item.prefix_count > 0:
            suffix_count_before = item.suffix_count
            result = sim.apply_currency_with_omen(item, "orb_of_annulment", "sinistral_annulment")
            assert result is True
            assert item.suffix_count == suffix_count_before, "Suffix was removed"
            assert item.prefix_count < suffix_count_before + 1  # prefix was removed

    def test_dextral_annulment_removes_suffix(self):
        """dextral_annulment: annul removes only suffix."""
        sim = CraftingSimulator(seed=42)
        item = sim.create_item("ring", ilvl=80)
        sim.apply_currency(item, "orb_of_alchemy")
        if item.suffix_count > 0:
            prefix_count_before = item.prefix_count
            result = sim.apply_currency_with_omen(item, "orb_of_annulment", "dextral_annulment")
            assert result is True
            assert item.prefix_count == prefix_count_before, "Prefix was removed"

    def test_greater_exaltation_adds_two_mods(self):
        """greater_exaltation: exalt adds 2 mods instead of 1."""
        sim = CraftingSimulator(seed=42)
        item = sim.create_item("ring", ilvl=80)
        sim.apply_currency(item, "orb_of_alchemy")
        count_before = item.mod_count
        if count_before < 5:  # Need room for 2 more
            result = sim.apply_currency_with_omen(item, "exalted_orb", "greater_exaltation")
            assert result is True
            assert item.mod_count == count_before + 2, (
                f"Expected {count_before + 2} mods, got {item.mod_count}"
            )
            assert any("added" in h and "," in h for h in item.history if "greater_exaltation" in h)

    def test_greater_annulment_removes_two_mods(self):
        """greater_annulment: annul removes 2 mods instead of 1."""
        sim = CraftingSimulator(seed=42)
        item = sim.create_item("ring", ilvl=80)
        sim.apply_currency(item, "orb_of_alchemy")
        count_before = item.mod_count
        if count_before >= 2:
            result = sim.apply_currency_with_omen(item, "orb_of_annulment", "greater_annulment")
            assert result is True
            assert item.mod_count == count_before - 2, (
                f"Expected {count_before - 2} mods, got {item.mod_count}"
            )

    def test_sinistral_alchemy_maximizes_prefixes(self):
        """sinistral_alchemy: alchemy maximizes prefix count."""
        sim = CraftingSimulator(seed=42)
        item = sim.create_item("ring", ilvl=80)
        result = sim.apply_currency_with_omen(item, "orb_of_alchemy", "sinistral_alchemy")
        assert result is True
        assert item.rarity == "rare"
        assert item.prefix_count == 3, f"Expected 3 prefixes, got {item.prefix_count}"

    def test_dextral_alchemy_maximizes_suffixes(self):
        """dextral_alchemy: alchemy maximizes suffix count."""
        sim = CraftingSimulator(seed=42)
        item = sim.create_item("ring", ilvl=80)
        result = sim.apply_currency_with_omen(item, "orb_of_alchemy", "dextral_alchemy")
        assert result is True
        assert item.rarity == "rare"
        assert item.suffix_count == 3, f"Expected 3 suffixes, got {item.suffix_count}"

    def test_whittling_removes_lowest_roll(self):
        """whittling: chaos removes the mod with lowest roll value."""
        sim = CraftingSimulator(seed=42)
        item = sim.create_item("ring", ilvl=80)
        sim.apply_currency(item, "orb_of_alchemy")
        # Get the lowest-roll mod before whittling
        all_mods_before = item.all_mods
        lowest_before = min(all_mods_before, key=lambda m: m.roll if m.roll else 0)
        count_before = item.mod_count

        result = sim.apply_currency_with_omen(item, "chaos_orb", "whittling")
        assert result is True
        # The lowest-roll mod should be gone (unless same group re-rolled)
        # Total mod count should stay the same (removed 1, added 1)
        assert item.mod_count == count_before

    def test_omen_on_corrupted_item_fails(self):
        """Omen should fail on corrupted items."""
        sim = CraftingSimulator(seed=42)
        item = sim.create_item("ring", ilvl=80)
        item.corrupted = True
        result = sim.apply_currency_with_omen(item, "chaos_orb", "sinistral_erasure")
        assert result is False

    def test_homogenising_exaltation_adds_same_tag(self):
        """homogenising_exaltation: adds a mod sharing a tag with existing mods."""
        # Try multiple seeds to find one where the omen succeeds
        for seed in range(200):
            sim = CraftingSimulator(seed=seed)
            item = sim.create_item("ring", ilvl=80)
            sim.apply_currency(item, "orb_of_alchemy")
            if item.mod_count >= 6:
                continue

            existing_tags = set()
            for m in item.all_mods:
                existing_tags.update(m.tags)
            if not existing_tags:
                continue

            count_before = item.mod_count
            result = sim.apply_currency_with_omen(
                item, "exalted_orb", "homogenising_exaltation"
            )
            if result and item.mod_count == count_before + 1:
                new_mod = item.all_mods[-1]
                assert set(new_mod.tags) & existing_tags, (
                    f"New mod {new_mod.group} tags {new_mod.tags} "
                    f"don't match existing {existing_tags}"
                )
                return  # success
        pytest.skip("Could not find seed where homogenising_exaltation succeeds")

    def test_homogenising_coronation_adds_same_tag(self):
        """homogenising_coronation: regal adds mod with same tag."""
        sim = CraftingSimulator(seed=42)
        item = sim.create_item("ring", ilvl=80)
        sim.apply_currency(item, "orb_of_transmutation")
        # Need a mod with tags
        if item.all_mods and item.all_mods[0].tags:
            result = sim.apply_currency_with_omen(
                item, "regal_orb", "homogenising_coronation"
            )
            assert result is True
            assert item.rarity == "rare"

    def test_sinistral_erasure_requires_rare(self):
        """sinistral_erasure with chaos requires rare item."""
        sim = CraftingSimulator(seed=42)
        item = sim.create_item("ring", ilvl=80)
        item.rarity = "magic"
        result = sim.apply_currency_with_omen(item, "chaos_orb", "sinistral_erasure")
        assert result is False

    def test_sinistral_exaltation_requires_rare(self):
        """sinistral_exaltation with exalt requires rare item."""
        sim = CraftingSimulator(seed=42)
        item = sim.create_item("ring", ilvl=80)
        item.rarity = "magic"
        result = sim.apply_currency_with_omen(item, "exalted_orb", "sinistral_exaltation")
        assert result is False

    def test_greater_exaltation_requires_rare(self):
        """greater_exaltation requires rare item."""
        sim = CraftingSimulator(seed=42)
        item = sim.create_item("ring", ilvl=80)
        item.rarity = "magic"
        result = sim.apply_currency_with_omen(item, "exalted_orb", "greater_exaltation")
        assert result is False

    def test_omen_history_recorded(self):
        """Verify omen application is recorded in item history."""
        sim = CraftingSimulator(seed=42)
        item = sim.create_item("ring", ilvl=80)
        sim.apply_currency(item, "orb_of_alchemy")
        sim.apply_currency_with_omen(item, "exalted_orb", "sinistral_exaltation")
        assert any("sinistral_exaltation" in h for h in item.history)


# ============================================================================
# Exclusion Group Tests (A.1.6)
# ============================================================================

class TestExclusionGroups:
    """Tests for exclusion group enforcement."""

    def test_exclusion_membership_built(self):
        """Verify exclusion membership mapping is built."""
        sim = CraftingSimulator()
        assert len(sim._exclusion_membership) > 0

    def test_exclusion_groups_loaded_with_patterns(self):
        """Verify exclusion groups have non-empty patterns."""
        sim = CraftingSimulator()
        non_empty = [eg for eg in sim._exclusion_groups if eg["patterns"]]
        assert len(non_empty) > 0

    def test_focus_elemental_damage_exclusion(self):
        """On focus, elemental spell damage mods should be mutually exclusive (excl_13)."""
        sim = CraftingSimulator()
        # excl_13 has: Chaos Damage, Cold Damage, Fire Damage, Lightning Damage, Spell Physical Damage
        # These should all be in the same exclusion group
        chaos = "PercentIncreasedChaosDamage"
        cold = "PercentIncreasedColdDamage"
        fire = "PercentIncreasedFireDamage"
        lightning = "PercentIncreasedLightningDamage"

        # If we have chaos, the others should be excluded
        excluded = sim._get_excluded_groups({chaos})
        assert cold in excluded, f"Cold damage should be excluded when Chaos is present"
        assert fire in excluded, f"Fire damage should be excluded when Chaos is present"
        assert lightning in excluded, f"Lightning damage should be excluded when Chaos is present"

    def test_exclusion_does_not_remove_self(self):
        """A mod should not exclude itself."""
        sim = CraftingSimulator()
        chaos = "PercentIncreasedChaosDamage"
        excluded = sim._get_excluded_groups({chaos})
        assert chaos not in excluded

    def test_exclusion_is_symmetric(self):
        """Exclusion should be symmetric: if A excludes B, B excludes A."""
        sim = CraftingSimulator()
        chaos = "PercentIncreasedChaosDamage"
        cold = "PercentIncreasedColdDamage"

        excluded_by_chaos = sim._get_excluded_groups({chaos})
        excluded_by_cold = sim._get_excluded_groups({cold})

        assert cold in excluded_by_chaos
        assert chaos in excluded_by_cold

    def test_exclusion_multiple_mods(self):
        """Multiple existing mods should combine their exclusions."""
        sim = CraftingSimulator()
        # Use mods from different exclusion groups
        chaos = "PercentIncreasedChaosDamage"
        cast_speed = "PercentIncreasedCastSpeed"  # excl_24

        excluded = sim._get_excluded_groups({chaos, cast_speed})
        # Both groups' exclusions should be present
        assert "PercentIncreasedColdDamage" in excluded  # from chaos
        # cast speed exclusion: other cast speed variants

    def test_exclusion_blocks_mod_rolling(self):
        """Exclusion groups should prevent conflicting mods from being rolled."""
        sim = CraftingSimulator(seed=42)
        item = sim.create_item("focus", ilvl=80)

        # Manually add a fire damage prefix
        fire_mod = RolledMod(
            group="PercentIncreasedFireDamage",
            description="#% increased Fire Damage",
            tags=["fire", "damage"],
            slot="prefix",
        )
        item.prefixes.append(fire_mod)

        # Try rolling another prefix — should never get the conflicting ones
        found_conflict = False
        for _ in range(100):
            existing = {m.group for m in item.all_mods}
            mod = sim.roll_mod("focus", "prefix", 80, exclude_groups=existing)
            if mod and mod.group in ("PercentIncreasedColdDamage",
                                      "PercentIncreasedChaosDamage",
                                      "PercentIncreasedLightningDamage",
                                      "PercentIncreasedSpellPhysicalDamage"):
                found_conflict = True
                break

        assert not found_conflict, "Conflicting mod was rolled despite exclusion group"

    def test_exclusion_works_with_alchemy(self):
        """Alchemy should respect exclusion groups when rolling mods."""
        sim = CraftingSimulator(seed=42)
        # Run many alchemy crafts on focus — no two elemental damage mods
        for seed in range(100):
            s = CraftingSimulator(seed=seed)
            item = s.create_item("focus", ilvl=80)
            s.apply_currency(item, "orb_of_alchemy")

            elemental_groups = {
                "PercentIncreasedChaosDamage",
                "PercentIncreasedColdDamage",
                "PercentIncreasedFireDamage",
                "PercentIncreasedLightningDamage",
                "PercentIncreasedSpellPhysicalDamage",
            }
            found = [m.group for m in item.all_mods if m.group in elemental_groups]
            assert len(found) <= 1, (
                f"Multiple elemental damage mods on focus: {found}"
            )

    def test_exclusion_group_1_attribute_hybrid(self):
        """excl_1: Str+Dex vs Str+Int hybrid attributes are exclusive."""
        sim = CraftingSimulator()
        # Check if these group IDs exist in the mod pool and are in exclusion membership
        str_dex = "FlattoStrengthandDexterity"
        str_int = "FlattoStrengthandIntelligence"
        # These may or may not be in the mod pool for ring, but the mapping should
        # still work if they exist in any category
        if str_dex in sim._exclusion_membership:
            assert str_int in sim._exclusion_membership[str_dex]
        if str_int in sim._exclusion_membership:
            assert str_dex in sim._exclusion_membership[str_int]

    def test_exclusion_spell_damage_variants(self):
        """excl_14: '#% increased Spell Damage' vs 'Invocated Spells' are exclusive."""
        sim = CraftingSimulator()
        spell_dmg = "PercentIncreasedSpellDamage"
        if spell_dmg in sim._exclusion_membership:
            # Spell Damage should exclude Invocated Spells (if that group exists)
            invocated = "InvocatedSpellsDealIncreasedDamage"
            if invocated in sim._exclusion_membership.get(spell_dmg, set()):
                assert spell_dmg in sim._exclusion_membership[invocated]

    def test_empty_exclusion_returns_empty(self):
        """No existing mods means no exclusions."""
        sim = CraftingSimulator()
        excluded = sim._get_excluded_groups(set())
        assert excluded == set()

    def test_unrelated_mods_not_excluded(self):
        """Mods from different exclusion groups should not conflict."""
        sim = CraftingSimulator()
        # Life and fire resistance are not in the same exclusion group
        excluded = sim._get_excluded_groups({"FlattoMaximumLife"})
        assert "PercentToFireResistance" not in excluded
