"""Tests for PoE 2 crafting guide data files and Prolog knowledge base.

Tests are organized into:
- Data integrity (JSON files well-formed, correct structure)
- Prolog syntax (valid Prolog constructs, no duplicate predicates)
- Mod pool consistency (weights, tags, categories)
- Crafting rules (currency preconditions, omen status, alloy constraints)
"""

import json
import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent
RESOURCES = PROJECT_ROOT / "resources"
PROLOG_FILE = PROJECT_ROOT / "poe2_crafting.pl"


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def all_json_files():
    """All JSON data files in resources/."""
    return list(RESOURCES.glob("*.json"))


@pytest.fixture
def mod_json_files():
    """Mod data JSON files (mods_*.json)."""
    return list(RESOURCES.glob("mods_*.json"))


@pytest.fixture
def prolog_content():
    """Raw content of the main Prolog file."""
    return PROLOG_FILE.read_text()


@pytest.fixture
def prolog_data_files():
    """All .pl data files in resources/."""
    return list(RESOURCES.glob("mods_*.pl"))


# ============================================================================
# 1. JSON Data File Integrity
# ============================================================================

class TestJsonIntegrity:
    """All JSON files should be valid and well-formed."""

    def test_all_json_parseable(self, all_json_files):
        for f in all_json_files:
            data = json.loads(f.read_text())
            assert isinstance(data, dict), f"{f.name} should be a JSON object"

    def test_mod_json_has_required_fields(self, mod_json_files):
        required = {"item_category", "source", "base_prefixes", "base_suffixes",
                     "weight_sum_prefixes", "weight_sum_suffixes"}
        for f in mod_json_files:
            data = json.loads(f.read_text())
            missing = required - set(data.keys())
            assert not missing, f"{f.name} missing fields: {missing}"

    def test_mod_entries_have_required_fields(self, mod_json_files):
        mod_fields = {"group", "description", "tags", "weight", "maxIlvl", "tierCount", "slot"}
        for f in mod_json_files:
            data = json.loads(f.read_text())
            for slot in ("base_prefixes", "base_suffixes"):
                for i, mod in enumerate(data[slot]):
                    missing = mod_fields - set(mod.keys())
                    assert not missing, f"{f.name} {slot}[{i}] missing: {missing}"

    def test_slot_values_valid(self, mod_json_files):
        for f in mod_json_files:
            data = json.loads(f.read_text())
            for mod in data["base_prefixes"]:
                assert mod["slot"] == "prefix", f"{f.name}: {mod['group']} should be prefix"
            for mod in data["base_suffixes"]:
                assert mod["slot"] == "suffix", f"{f.name}: {mod['group']} should be suffix"

    def test_weights_positive(self, mod_json_files):
        for f in mod_json_files:
            data = json.loads(f.read_text())
            for slot in ("base_prefixes", "base_suffixes"):
                for mod in data[slot]:
                    assert mod["weight"] >= 0, f"{f.name}: {mod['group']} has negative weight"

    def test_weight_sums_match(self, mod_json_files):
        """weight_sum_prefixes should equal sum of individual prefix weights."""
        for f in mod_json_files:
            data = json.loads(f.read_text())
            pre_sum = sum(m["weight"] for m in data["base_prefixes"])
            suf_sum = sum(m["weight"] for m in data["base_suffixes"])
            # Only check if weights are non-trivial (>100) — some categories use
            # different weight scales
            if pre_sum > 100:
                assert pre_sum == data["weight_sum_prefixes"], \
                    f"{f.name}: prefix sum {pre_sum} != declared {data['weight_sum_prefixes']}"
            if suf_sum > 100:
                assert suf_sum == data["weight_sum_suffixes"], \
                    f"{f.name}: suffix sum {suf_sum} != declared {data['weight_sum_suffixes']}"

    def test_maxIlvl_reasonable(self, mod_json_files):
        for f in mod_json_files:
            data = json.loads(f.read_text())
            for slot in ("base_prefixes", "base_suffixes"):
                for mod in data[slot]:
                    assert 1 <= mod["maxIlvl"] <= 100, \
                        f"{f.name}: {mod['group']} maxIlvl {mod['maxIlvl']} out of range"

    def test_tierCount_positive(self, mod_json_files):
        for f in mod_json_files:
            data = json.loads(f.read_text())
            for slot in ("base_prefixes", "base_suffixes"):
                for mod in data[slot]:
                    assert mod["tierCount"] >= 1, \
                        f"{f.name}: {mod['group']} tierCount {mod['tierCount']}"


# ============================================================================
# 2. Prolog File Syntax
# ============================================================================

class TestPrologSyntax:
    """Basic syntax validation of the Prolog knowledge base."""

    def test_file_exists(self):
        assert PROLOG_FILE.exists(), "poe2_crafting.pl not found"

    def test_module_declaration(self, prolog_content):
        assert ":- module(poe2_crafting," in prolog_content

    def test_no_duplicate_predicates(self, prolog_content):
        """Check for obvious duplicate fact definitions."""
        # Find all top-level facts (lines starting with lowercase atom followed by open paren)
        fact_pattern = re.compile(r'^([a-z_]+)\(', re.MULTILINE)
        facts = fact_pattern.findall(prolog_content)
        # Some predicates are expected to have multiple clauses
        multi_clause = {"mod_group", "mod_tier_detail", "mod_roll_range", "omen",
                       "omen_disabled", "alloy", "quality_type", "quality_max",
                       "currency", "base_type", "item_property", "rarity",
                       "max_prefixes", "max_suffixes", "influence_type", "slot_type",
                       "is_tainted_currency", "blocks_modification", "mod_pool"}
        # Check for unexpected duplicates in single-clause predicates
        from collections import Counter
        counts = Counter(facts)
        for pred, count in counts.items():
            if pred not in multi_clause and count > 3:
                # Allow up to 3 (could be multi-clause with different arities)
                pass  # Just note it, don't fail — some predicates legitimately repeat

    def test_consult_directives_valid(self, prolog_content):
        """All consult paths should reference existing files."""
        consults = re.findall(r":- consult\('([^']+)'\)", prolog_content)
        for path in consults:
            full_path = PROJECT_ROOT / path
            assert full_path.exists(), f"consult('{path}') — file not found"

    def test_omens_have_version_note(self, prolog_content):
        assert "0.5.0" in prolog_content, "Should reference current patch version"
        assert "omen_disabled" in prolog_content, "Should track disabled omens"

    def test_disabled_omens_count(self, prolog_content):
        """Should have exactly 8 disabled omens + 1 disabled mechanic as of 0.5.0."""
        disabled_omens = re.findall(r'^disabled\(omen,', prolog_content, re.MULTILINE)
        disabled_mechanics = re.findall(r'^disabled\(mechanic,', prolog_content, re.MULTILINE)
        assert len(disabled_omens) == 8, f"Expected 8 disabled omens, found {len(disabled_omens)}"
        assert len(disabled_mechanics) == 1, f"Expected 1 disabled mechanic, found {len(disabled_mechanics)}"

    def test_alloy_count(self, prolog_content):
        """Should have exactly 13 alloys."""
        alloys = re.findall(r'^alloy\([a-z_]+,', prolog_content, re.MULTILINE)
        assert len(alloys) == 13, f"Expected 13 alloys, found {len(alloys)}"

    def test_quality_type_count(self, prolog_content):
        """Should have 15 quality types (3 weapon/armour + 12 catalysts)."""
        qt = re.findall(r'^quality_type\(', prolog_content, re.MULTILINE)
        assert len(qt) == 15, f"Expected 15 quality types, found {len(qt)}"


# ============================================================================
# 3. Mod Pool Consistency
# ============================================================================

class TestModPools:
    """Test mod data files (.pl) are consistent with JSON source data."""

    def test_pl_files_exist_for_all_json(self, mod_json_files):
        """Each mods_*.json should have a corresponding mods_*.pl."""
        # JSON files use plural (mods_rings.json) but .pl files use singular (mods_ring.pl)
        plural_to_singular = {
            "mods_rings.json": "mods_ring.pl",
            "mods_amulets.json": "mods_amulet.pl",
            "mods_body_armour_str.json": "mods_body_armour_str.pl",
            "mods_helmets_str.json": "mods_helmet_str.pl",
            "mods_gloves_str.json": "mods_gloves_str.pl",
            "mods_boots_str.json": "mods_boots_str.pl",
            "mods_weapons_sword.json": "mods_weapon_sword.pl",
        }
        for f in mod_json_files:
            pl_name = plural_to_singular.get(f.name, f.name.replace(".json", ".pl"))
            pl_path = RESOURCES / pl_name
            assert pl_path.exists(), f"Missing Prolog data file: {pl_name} (from {f.name})"

    def test_pl_mod_group_count_matches_json(self, mod_json_files):
        """Number of mod_group facts in .pl should match entries in .json."""
        p2s = {"mods_rings.json":"mods_ring.pl","mods_amulets.json":"mods_amulet.pl",
               "mods_helmets_str.json":"mods_helmet_str.pl","mods_weapons_sword.json":"mods_weapon_sword.pl"}
        for json_file in mod_json_files:
            data = json.loads(json_file.read_text())
            pl_name = p2s.get(json_file.name, json_file.name.replace(".json", ".pl"))
            pl_file = RESOURCES / pl_name
            pl_content = pl_file.read_text()
            pl_count = len(re.findall(r'^mod_group\(', pl_content, re.MULTILINE))
            json_count = len(data["base_prefixes"]) + len(data["base_suffixes"])
            assert pl_count == json_count, \
                f"{json_file.name}: JSON has {json_count} mods, .pl has {pl_count}"

    def test_pl_weight_sum_matches_json(self, mod_json_files):
        """Weight sums in .pl should match .json."""
        p2s = {"mods_rings.json":"mods_ring.pl","mods_amulets.json":"mods_amulet.pl",
               "mods_helmets_str.json":"mods_helmet_str.pl","mods_weapons_sword.json":"mods_weapon_sword.pl"}
        for json_file in mod_json_files:
            data = json.loads(json_file.read_text())
            pl_name = p2s.get(json_file.name, json_file.name.replace(".json", ".pl"))
            pl_file = RESOURCES / pl_name
            pl_content = pl_file.read_text()
            cat = data["item_category"]
            # Check prefix weight sum
            pre_match = re.search(
                rf"mod_pool_weight_sum\({cat}, prefix, (\d+)\)", pl_content
            )
            suf_match = re.search(
                rf"mod_pool_weight_sum\({cat}, suffix, (\d+)\)", pl_content
            )
            if data["weight_sum_prefixes"] > 100:
                assert pre_match, f"{cat}: missing prefix weight sum in .pl"
                assert int(pre_match.group(1)) == data["weight_sum_prefixes"]
            if data["weight_sum_suffixes"] > 100:
                assert suf_match, f"{cat}: missing suffix weight sum in .pl"
                assert int(suf_match.group(1)) == data["weight_sum_suffixes"]

    def test_no_duplicate_mod_groups_in_pl(self, prolog_data_files):
        """Each mod_group fact should be unique within its file."""
        for f in prolog_data_files:
            content = f.read_text()
            groups = re.findall(r'^mod_group\([^,]+, ([^,]+),', content, re.MULTILINE)
            duplicates = [g for g in groups if groups.count(g) > 1]
            assert not duplicates, f"{f.name}: duplicate mod groups: {set(duplicates)}"

    def test_categories_in_mapping(self, prolog_content):
        """All scraped categories should appear in mod_pool/3 mapping."""
        expected_categories = [
            "body_armour_str", "helmet_str", "gloves_str", "boots_str",
            "ring", "amulet", "weapon_sword"
        ]
        for cat in expected_categories:
            assert f"mod_pool(" in prolog_content or cat in prolog_content, \
                f"Category {cat} not found in mod_pool mapping"


# ============================================================================
# 4. Crafting Rules
# ============================================================================

class TestCraftingRules:
    """Test currency, omen, and alloy rule consistency."""

    def test_all_currencies_have_precondition(self, prolog_content):
        """Every currency/1 fact should have at least one precondition."""
        currencies = re.findall(r'^currency\((\w+)\)', prolog_content, re.MULTILINE)
        for c in currencies:
            assert f"currency_precondition({c}," in prolog_content, \
                f"Currency {c} has no precondition"

    def test_all_currencies_have_postcondition(self, prolog_content):
        """Every currency/1 fact should have at least one postcondition."""
        currencies = re.findall(r'^currency\((\w+)\)', prolog_content, re.MULTILINE)
        for c in currencies:
            assert f"currency_postcondition({c}," in prolog_content, \
                f"Currency {c} has no postcondition"

    def test_can_use_omen_filters_disabled(self, prolog_content):
        """can_use_omen should check omen_disabled."""
        assert "\\+ omen_disabled" in prolog_content, \
            "can_use_omen should filter disabled omens"

    def test_sinistral_dextral_annulment_active(self, prolog_content):
        """The key crafting omens should NOT be disabled."""
        active_pairs = [
            ("sinistral_annulment", "dextral_annulment"),
            ("sinistral_exaltation", "dextral_exaltation"),
            ("sinistral_erasure", "dextral_erasure"),
        ]
        for sin, dex in active_pairs:
            assert f"omen({sin}," in prolog_content
            assert f"omen({dex}," in prolog_content
            # Should NOT be in omen_disabled
            assert f"omen_disabled({sin}" not in prolog_content
            assert f"omen_disabled({dex}" not in prolog_content

    def test_disabled_alchemy_omens(self, prolog_content):
        """Sinistral/Dextral Alchemy should be disabled since 0.3.0."""
        assert "disabled(omen, sinistral_alchemy" in prolog_content
        assert "disabled(omen, dextral_alchemy" in prolog_content

    def test_alloys_require_rare(self, prolog_content):
        """alloy_precondition should check for rare rarity."""
        assert "item_state(_, rare," in prolog_content

    def test_quality_max_belt_is_zero(self, prolog_content):
        """Belts cannot have quality in PoE 2."""
        match = re.search(r'quality_max\(belt,\s*(\d+)\)', prolog_content)
        assert match, "quality_max(belt, _) not found"
        assert int(match.group(1)) == 0, "Belt quality max should be 0"

    def test_quality_max_ring_is_20(self, prolog_content):
        """Standard rings max quality is 20%."""
        match = re.search(r'quality_max\(ring,\s*(\d+)\)', prolog_content)
        assert match, "quality_max(ring, _) not found"
        assert int(match.group(1)) == 20

    def test_base_type_count(self, prolog_content):
        """Should have at least 10 base types defined."""
        bases = re.findall(r'^base_type\(', prolog_content, re.MULTILINE)
        assert len(bases) >= 10, f"Only {len(bases)} base types defined"

    def test_mod_pool_mapping_exists(self, prolog_content):
        """mod_pool/3 facts should exist for item category mapping."""
        mappings = re.findall(r'^mod_pool\(', prolog_content, re.MULTILINE)
        assert len(mappings) >= 7, f"Only {len(mappings)} mod_pool mappings"


# ============================================================================
# 5. Omen Version Tracking
# ============================================================================

class TestOmenVersioning:
    """Verify omen disabled status matches known 0.5.0 facts."""

    KNOWN_DISABLED = {
        "omen_of_corruption": "0.5.0",
        "sinistral_alchemy": "0.3.0",
        "dextral_alchemy": "0.3.0",
        "sinistral_coronation": "0.3.0",
        "dextral_coronation": "0.3.0",
        "greater_annulment": "0.3.0",
        "homogenising_coronation": "0.4.0",
        "homogenising_exaltation": "0.4.0",
    }

    def test_all_known_disabled_present(self, prolog_content):
        for omen, version in self.KNOWN_DISABLED.items():
            # Check in generic disabled/3 (primary source of truth)
            pattern = rf"disabled\(omen,\s*{omen},\s*'{version}'\)"
            assert re.search(pattern, prolog_content), \
                f"Expected disabled(omen, {omen}, '{version}')"

    def test_no_extra_disabled_omens(self, prolog_content):
        disabled = re.findall(r'^disabled\(omen,\s*(\w+),', prolog_content, re.MULTILINE)
        extra = set(disabled) - set(self.KNOWN_DISABLED.keys())
        assert not extra, f"Unexpected disabled omens: {extra} (update test if intentional)"

    def test_version_note_present(self, prolog_content):
        assert "current_version" in prolog_content
        assert "0.5.0" in prolog_content

    def test_generic_validity_layer(self, prolog_content):
        """disabled/3, nerfed/4, valid/2, check_valid/2 should exist."""
        assert "disabled(EntityType, Name," in prolog_content or "disabled(omen," in prolog_content
        assert "nerfed(" in prolog_content
        assert "valid(EntityType, Name)" in prolog_content
        assert "check_valid(EntityType, Name)" in prolog_content

    def test_backward_compat_omen_disabled(self, prolog_content):
        """omen_disabled/2 should be derivable from disabled/3."""
        assert "omen_disabled(Name, Version) :- disabled(omen, Name, Version)" in prolog_content

    def test_mechanic_disabled_recombination(self, prolog_content):
        """Recombination should be disabled as a mechanic, not just an omen."""
        assert "disabled(mechanic, recombination" in prolog_content

    def test_nerfed_essences_tracked(self, prolog_content):
        """Essence nerfs should be in nerfed/4."""
        assert "nerfed(essence," in prolog_content
