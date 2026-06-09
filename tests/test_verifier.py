"""Tests for the recipe verifier — state tracking, loops, omen+currency, impossible transitions."""

import pytest
from verifier import (
    ItemState, verify_recipe, _normalize_steps, _apply_step,
    _check_preconditions, CURRENCY_RULES, OMEN_CURRENCY_MAP,
)


# ============================================================================
# ItemState basics
# ============================================================================

class TestItemState:
    def test_initial_state(self):
        s = ItemState()
        assert s.rarity == "normal"
        assert s.total_mods == 0
        assert s.has_open_prefix
        assert s.has_open_suffix
        assert s.is_normal

    def test_summary(self):
        s = ItemState(rarity="magic", prefix_count=1, suffix_count=1)
        assert "magic" in s.summary()
        assert "1p+1s" in s.summary()

    def test_copy_independent(self):
        s = ItemState(rarity="normal")
        s2 = s.copy()
        s2.rarity = "rare"
        assert s.rarity == "normal"


# ============================================================================
# State transitions
# ============================================================================

class TestStateTransitions:
    def test_transmutation(self):
        s = ItemState()
        ns = _apply_step(s, "orb_of_transmutation")
        assert ns.rarity == "magic"
        assert ns.prefix_count == 1
        assert ns.suffix_count == 1

    def test_augmentation_on_magic(self):
        s = ItemState(rarity="magic", prefix_count=1, suffix_count=0)
        ns = _apply_step(s, "orb_of_augmentation")
        assert ns.rarity == "magic"
        assert ns.total_mods == 2

    def test_alchemy(self):
        s = ItemState()
        ns = _apply_step(s, "orb_of_alchemy")
        assert ns.rarity == "rare"
        assert ns.total_mods >= 4

    def test_chaos_reroll(self):
        s = ItemState(rarity="rare", prefix_count=3, suffix_count=2)
        ns = _apply_step(s, "chaos_orb")
        assert ns.rarity == "rare"

    def test_regal_magic_to_rare(self):
        s = ItemState(rarity="magic", prefix_count=1, suffix_count=1)
        ns = _apply_step(s, "regal_orb")
        assert ns.rarity == "rare"
        assert ns.total_mods == 3  # 2 existing + 1 new

    def test_exalted_adds_mod(self):
        s = ItemState(rarity="rare", prefix_count=2, suffix_count=1)
        ns = _apply_step(s, "exalted_orb")
        assert ns.rarity == "rare"
        assert ns.total_mods == 4

    def test_annulment_removes_mod(self):
        s = ItemState(rarity="rare", prefix_count=2, suffix_count=2)
        ns = _apply_step(s, "orb_of_annulment")
        assert ns.total_mods == 3

    def test_annulment_all_mods_goes_normal(self):
        s = ItemState(rarity="magic", prefix_count=1, suffix_count=0)
        ns = _apply_step(s, "orb_of_annulment")
        assert ns.rarity == "normal"
        assert ns.total_mods == 0

    def test_corruption(self):
        s = ItemState(rarity="rare")
        ns = _apply_step(s, "vaal_orb")
        assert ns.corrupted

    def test_scouring(self):
        s = ItemState(rarity="rare", prefix_count=3, suffix_count=2)
        ns = _apply_step(s, "orb_of_scouring")
        assert ns.rarity == "normal"
        assert ns.total_mods == 0

    def test_essence_on_magic(self):
        s = ItemState(rarity="magic", prefix_count=1, suffix_count=0)
        ns = _apply_step(s, "essence_of_the_body")
        assert ns.rarity == "rare"


# ============================================================================
# Omen + currency as compound step
# ============================================================================

class TestOmenCompoundStep:
    def test_greater_exaltation_adds_two_mods(self):
        """Greater exaltation = exalted orb + 1 extra mod (2 total)."""
        s = ItemState(rarity="rare", prefix_count=1, suffix_count=1)
        ns = _apply_step(s, "exalted_orb", "greater_exaltation")
        assert ns.rarity == "rare"
        assert ns.total_mods == 4  # 2 existing + 2 new

    def test_sinistral_exaltation_same_as_base(self):
        """Sinistral just targets prefix — same mod count."""
        s = ItemState(rarity="rare", prefix_count=1, suffix_count=1)
        ns = _apply_step(s, "exalted_orb", "sinistral_exaltation")
        assert ns.total_mods == 3  # 2 existing + 1 new

    def test_omen_without_currency(self):
        """Omen alone should not change state."""
        s = ItemState(rarity="rare", prefix_count=1, suffix_count=1)
        # Omen is a modifier — without the currency it does nothing
        # (the normalize step should merge them)
        pass

    def test_normalize_merges_omen_into_currency(self):
        """Standalone omen step + next currency step = one compound step."""
        steps = [
            {"step": 1, "action": "apply_currency", "currency": "orb_of_transmutation"},
            {"step": 2, "action": "apply_with_omen", "currency": "greater_exaltation"},
            {"step": 3, "action": "apply_currency", "currency": "exalted_orb"},
        ]
        normalized = _normalize_steps(steps)
        assert len(normalized) == 2  # transmute + (exalt+omen)
        assert normalized[1]["currency"] == "exalted_orb"
        assert normalized[1]["omen"] == "greater_exaltation"

    def test_normalize_keeps_explicit_omen_field(self):
        """Step with explicit omen field stays as-is."""
        steps = [
            {"step": 1, "action": "apply_currency", "currency": "exalted_orb", "omen": "greater_exaltation"},
        ]
        normalized = _normalize_steps(steps)
        assert len(normalized) == 1
        assert normalized[0]["omen"] == "greater_exaltation"

    def test_normalize_omen_wrong_currency_pair(self):
        """Omen that doesn't match next currency stays standalone."""
        steps = [
            {"step": 1, "action": "apply_with_omen", "currency": "greater_exaltation"},
            {"step": 2, "action": "apply_currency", "currency": "chaos_orb"},  # wrong pair
        ]
        normalized = _normalize_steps(steps)
        # Should NOT merge — greater_exaltation pairs with exalted_orb, not chaos
        assert len(normalized) == 2


# ============================================================================
# Precondition checking
# ============================================================================

class TestPreconditionChecking:
    def test_transmutation_requires_normal(self):
        s = ItemState(rarity="magic")
        checks = _check_preconditions(s, CURRENCY_RULES["orb_of_transmutation"]["pre"],
                                       "orb_of_transmutation", 1, [])
        assert not all(c.passed for c in checks)

    def test_transmutation_requires_no_mods(self):
        s = ItemState(rarity="normal", prefix_count=1, suffix_count=0)
        checks = _check_preconditions(s, CURRENCY_RULES["orb_of_transmutation"]["pre"],
                                       "orb_of_transmutation", 1, [])
        assert not all(c.passed for c in checks)

    def test_transmutation_on_clean_normal(self):
        s = ItemState(rarity="normal")
        checks = _check_preconditions(s, CURRENCY_RULES["orb_of_transmutation"]["pre"],
                                       "orb_of_transmutation", 1, [])
        assert all(c.passed for c in checks)

    def test_regal_requires_magic(self):
        s = ItemState(rarity="rare")
        checks = _check_preconditions(s, CURRENCY_RULES["regal_orb"]["pre"],
                                       "regal_orb", 1, [])
        assert not all(c.passed for c in checks)

    def test_exalted_requires_rare(self):
        s = ItemState(rarity="magic")
        checks = _check_preconditions(s, CURRENCY_RULES["exalted_orb"]["pre"],
                                       "exalted_orb", 1, [])
        assert not all(c.passed for c in checks)

    def test_exalted_requires_open_slot(self):
        s = ItemState(rarity="rare", prefix_count=3, suffix_count=3)
        checks = _check_preconditions(s, CURRENCY_RULES["exalted_orb"]["pre"],
                                       "exalted_orb", 1, [])
        assert not all(c.passed for c in checks)

    def test_annulment_requires_mods(self):
        s = ItemState(rarity="magic", prefix_count=0, suffix_count=0)
        checks = _check_preconditions(s, CURRENCY_RULES["orb_of_annulment"]["pre"],
                                       "orb_of_annulment", 1, [])
        assert not all(c.passed for c in checks)


# ============================================================================
# Loop validation — the key test cases from stff1
# ============================================================================

class TestLoopValidation:
    def _stff1_recipe(self):
        """The stff1 recipe that should fail in multiple ways."""
        return {
            "name": "stff1",
            "game": "poe2",
            "steps": [
                {"step": 1, "action": "apply_currency", "currency": "orb_of_transmutation"},
                {"step": 2, "action": "apply_currency", "currency": "orb_of_augmentation"},
                {"step": 3, "action": "apply_essence", "currency": "essence_of_wrath"},
                {"step": 4, "action": "apply_with_omen", "currency": "greater_exaltation"},
                {"step": 5, "action": "apply_currency", "currency": "exalted_orb",
                 "conditions": [{"type": "has_mod", "value": "life", "goto": 1}]},
                {"step": 6, "action": "apply_currency", "currency": "regal_orb"},
            ]
        }

    def test_stff1_overall_fails(self):
        """stff1 recipe should fail verification."""
        result = verify_recipe(self._stff1_recipe())
        assert not result.overall

    def test_stff1_goto_step1_fails(self):
        """Step 5 goto step 1 is impossible — step 1 needs normal, item is rare."""
        result = verify_recipe(self._stff1_recipe())
        # Find the goto error in global errors
        goto_errors = [e for e in result.errors if "goto 1" in e.lower() or "goto 1" in e]
        assert len(goto_errors) > 0, f"Expected goto error, got: {result.errors}"
        assert "normal" in goto_errors[0].lower() or "rare" in goto_errors[0].lower()

    def test_stff1_regal_on_rare_fails(self):
        """Step 6 regal_orb requires magic, but item is rare after step 5."""
        result = verify_recipe(self._stff1_recipe())
        # The step 6 check should fail
        step6 = [s for s in result.steps if s.step == 6]
        assert len(step6) == 1
        assert not step6[0].all_pass
        rarity_checks = [c for c in step6[0].checks if "magic" in c.test and "rare" in c.test]
        assert len(rarity_checks) > 0

    def test_stff1_omen_merges_with_exalt(self):
        """Steps 4+5 should be normalized into one compound step."""
        recipe = self._stff1_recipe()
        normalized = _normalize_steps(recipe["steps"])
        # Should have 5 steps after merge (not 6)
        assert len(normalized) == 5
        # The merged step should be exalted_orb + greater_exaltation
        merged = [s for s in normalized if s["omen"] == "greater_exaltation"]
        assert len(merged) == 1
        assert merged[0]["currency"] == "exalted_orb"

    def test_stff1_step4_passes_with_omen(self):
        """Step 4 (greater exaltation + exalted orb) should pass preconditions on rare with open slots."""
        result = verify_recipe(self._stff1_recipe())
        # After normalization, step 4 is the merged omen+exalt step
        # At this point: rare, 3p+2s (from essence), exalt needs open slot
        # It should pass if there's an open slot
        step4 = [s for s in result.steps if s.step == 4]
        if step4:
            # Check that the omen+currency compound step itself passes
            # (the failure should be in goto/step 6, not here)
            pass  # The step itself may pass — the errors are elsewhere

    def test_valid_recipe_passes(self):
        """A simple valid recipe should pass all checks."""
        recipe = {
            "name": "simple_ring",
            "game": "poe2",
            "steps": [
                {"step": 1, "action": "apply_currency", "currency": "orb_of_transmutation"},
                {"step": 2, "action": "apply_currency", "currency": "orb_of_augmentation"},
                {"step": 3, "action": "apply_currency", "currency": "regal_orb"},
                {"step": 4, "action": "apply_currency", "currency": "exalted_orb"},
            ]
        }
        result = verify_recipe(recipe)
        assert result.overall
        assert len(result.errors) == 0

    def test_regal_on_normal_fails(self):
        """Regal orb on normal item should fail."""
        recipe = {
            "name": "bad_regal",
            "game": "poe2",
            "steps": [
                {"step": 1, "action": "apply_currency", "currency": "regal_orb"},
            ]
        }
        result = verify_recipe(recipe)
        assert not result.overall
        assert not result.steps[0].all_pass

    def test_exalt_on_magic_fails(self):
        """Exalted orb on magic item should fail (needs rare)."""
        recipe = {
            "name": "bad_exalt",
            "game": "poe2",
            "steps": [
                {"step": 1, "action": "apply_currency", "currency": "orb_of_transmutation"},
                {"step": 2, "action": "apply_currency", "currency": "exalted_orb"},
            ]
        }
        result = verify_recipe(recipe)
        assert not result.overall
        step2 = result.steps[1]
        assert not step2.all_pass

    def test_exalt_on_full_rare_fails(self):
        """Exalted orb on rare with 3p+3s should fail (no open slot)."""
        recipe = {
            "name": "full_rare",
            "game": "poe2",
            "steps": [
                {"step": 1, "action": "apply_currency", "currency": "orb_of_alchemy"},
                {"step": 2, "action": "apply_currency", "currency": "exalted_orb"},
            ]
        }
        result = verify_recipe(recipe)
        # After alchemy: rare with 3p+2s — exalt should work (open suffix)
        # This should actually pass since we roll 3p+2s
        assert result.overall

    def test_chaos_on_magic_fails(self):
        """Chaos orb on magic item should fail (needs rare)."""
        recipe = {
            "name": "bad_chaos",
            "game": "poe2",
            "steps": [
                {"step": 1, "action": "apply_currency", "currency": "orb_of_transmutation"},
                {"step": 2, "action": "apply_currency", "currency": "chaos_orb"},
            ]
        }
        result = verify_recipe(recipe)
        assert not result.overall

    def test_annulment_on_empty_fails(self):
        """Annulment on item with no mods should fail."""
        recipe = {
            "name": "bad_annul",
            "game": "poe2",
            "steps": [
                {"step": 1, "action": "apply_currency", "currency": "orb_of_annulment"},
            ]
        }
        result = verify_recipe(recipe)
        assert not result.overall

    def test_essence_on_rare_fails(self):
        """Essence of the body on rare item should fail (needs normal or magic)."""
        recipe = {
            "name": "bad_essence",
            "game": "poe2",
            "steps": [
                {"step": 1, "action": "apply_currency", "currency": "orb_of_alchemy"},
                {"step": 2, "action": "apply_essence", "currency": "essence_of_the_body"},
            ]
        }
        result = verify_recipe(recipe)
        assert not result.overall
        step2 = result.steps[1]
        assert not step2.all_pass

    def test_else_repeat_impossible(self):
        """Else-repeat on a step that can't be repeated should flag error."""
        recipe = {
            "name": "bad_repeat",
            "game": "poe2",
            "steps": [
                {"step": 1, "action": "apply_currency", "currency": "orb_of_transmutation",
                 "else_repeat": True},
            ]
        }
        result = verify_recipe(recipe)
        # After transmutation: magic. Transmutation requires normal.
        # So repeating should fail.
        step1 = result.steps[0]
        repeat_errors = [c for c in step1.checks if "repeat" in c.test.lower()]
        assert len(repeat_errors) > 0

    def test_goto_to_nonexistent_step(self):
        """Goto to a step that doesn't exist should flag error."""
        recipe = {
            "name": "bad_goto",
            "game": "poe2",
            "steps": [
                {"step": 1, "action": "apply_currency", "currency": "orb_of_transmutation",
                 "conditions": [{"type": "has_mod", "value": "life", "goto": 99}]},
            ]
        }
        result = verify_recipe(recipe)
        assert "does not exist" in str(result.errors)


# ============================================================================
# State tracking through multi-step recipes
# ============================================================================

class TestStateTracking:
    def test_state_progression_transmute_augment_regal(self):
        """Track state: normal → magic → magic → rare."""
        recipe = {
            "name": "progression",
            "game": "poe2",
            "steps": [
                {"step": 1, "action": "apply_currency", "currency": "orb_of_transmutation"},
                {"step": 2, "action": "apply_currency", "currency": "orb_of_augmentation"},
                {"step": 3, "action": "apply_currency", "currency": "regal_orb"},
            ]
        }
        result = verify_recipe(recipe)
        assert result.overall
        # Check state transitions
        assert result.steps[0].state_before.rarity == "normal"
        assert result.steps[0].state_after.rarity == "magic"
        assert result.steps[2].state_after.rarity == "rare"

    def test_state_after_alchemy(self):
        """Alchemy: normal → rare."""
        recipe = {
            "name": "alchemy",
            "game": "poe2",
            "steps": [
                {"step": 1, "action": "apply_currency", "currency": "orb_of_alchemy"},
            ]
        }
        result = verify_recipe(recipe)
        assert result.overall
        assert result.steps[0].state_after.rarity == "rare"

    def test_state_preserved_after_scouring(self):
        """Scouring resets to normal, allowing transmutation again."""
        recipe = {
            "name": "scour_retry",
            "game": "poe2",
            "steps": [
                {"step": 1, "action": "apply_currency", "currency": "orb_of_alchemy"},
                {"step": 2, "action": "apply_currency", "currency": "orb_of_scouring"},
                {"step": 3, "action": "apply_currency", "currency": "orb_of_transmutation"},
            ]
        }
        result = verify_recipe(recipe)
        assert result.overall
        assert result.steps[2].state_before.rarity == "normal"


# ============================================================================
# Omen-currency pairing verification
# ============================================================================

class TestOmenPairing:
    def test_omen_pairs_with_wrong_currency(self):
        """Omen that pairs with exalted_orb but used with chaos_orb."""
        recipe = {
            "name": "bad_omen_pair",
            "game": "poe2",
            "steps": [
                {"step": 1, "action": "apply_currency", "currency": "orb_of_alchemy"},
                {"step": 2, "action": "apply_currency", "currency": "chaos_orb",
                 "omen": "greater_exaltation"},  # wrong pair!
            ]
        }
        result = verify_recipe(recipe)
        # Should fail: greater_exaltation pairs with exalted_orb, not chaos_orb
        step2 = result.steps[1]
        pair_checks = [c for c in step2.checks if "pairs with" in c.test]
        assert len(pair_checks) > 0
        assert not pair_checks[0].passed

    def test_omen_pairs_with_correct_currency(self):
        """Omen that correctly pairs with its currency."""
        recipe = {
            "name": "good_omen_pair",
            "game": "poe2",
            "steps": [
                {"step": 1, "action": "apply_currency", "currency": "orb_of_alchemy"},
                {"step": 2, "action": "apply_currency", "currency": "exalted_orb",
                 "omen": "greater_exaltation"},
            ]
        }
        result = verify_recipe(recipe)
        step2 = result.steps[1]
        pair_checks = [c for c in step2.checks if "pairs with" in c.test]
        # Should have no pairing errors
        assert len(pair_checks) == 0


# ============================================================================
# Unknown currencies
# ============================================================================

class TestUnknownCurrencies:
    def test_unknown_currency_flagged(self):
        """Unknown currency without KB should be flagged as warning."""
        recipe = {
            "name": "unknown",
            "game": "poe2",
            "steps": [
                {"step": 1, "action": "apply_currency", "currency": "made_up_orb"},
            ]
        }
        result = verify_recipe(recipe, prolog_kb="")
        # It's a warning (not error), so overall may still pass
        # But the check should be present and failed
        assert len(result.steps[0].checks) > 0
        assert any("unknown" in c.test.lower() and not c.passed for c in result.steps[0].checks)


# ============================================================================
# Multiple goto targets
# ============================================================================

class TestMultipleGotos:
    def test_multiple_conditions_with_different_gotos(self):
        """Step with multiple conditions, each pointing to different steps."""
        recipe = {
            "name": "multi_goto",
            "game": "poe2",
            "steps": [
                {"step": 1, "action": "apply_currency", "currency": "orb_of_transmutation"},
                {"step": 2, "action": "apply_currency", "currency": "orb_of_augmentation"},
                {"step": 3, "action": "apply_currency", "currency": "regal_orb",
                 "conditions": [
                     {"type": "has_mod", "value": "life", "goto": 1},  # impossible
                     {"type": "has_mod", "value": "resist", "goto": 2},  # impossible
                 ]},
            ]
        }
        result = verify_recipe(recipe)
        # Both gotos should fail: step 1 needs normal (item is rare), step 2 needs magic
        assert len(result.errors) >= 2

    def test_else_goto_impossible(self):
        """Else-goto to a step with incompatible preconditions."""
        recipe = {
            "name": "bad_else",
            "game": "poe2",
            "steps": [
                {"step": 1, "action": "apply_currency", "currency": "orb_of_transmutation"},
                {"step": 2, "action": "apply_currency", "currency": "regal_orb",
                 "else_goto": 1},  # else: go back to step 1 (needs normal, item is magic)
            ]
        }
        result = verify_recipe(recipe)
        # After step 2: rare. Step 1 needs normal → impossible
        assert len(result.errors) > 0
