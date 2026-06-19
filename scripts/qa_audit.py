#!/usr/bin/env python3
"""QA Audit Script — cross-reference validation against external sources.

Tier 2 of the QA system. Standalone script, no pytest dependency.
Compares the KB against PathOfCrafting source data and optionally poe2db.

Usage:
    python3 scripts/qa_audit.py              # Full audit (local sources)
    python3 scripts/qa_audit.py --quick      # Quick check (counts only)
    python3 scripts/qa_audit.py --json       # Machine-readable output

Exit codes:
    0 = all checks passed
    1 = warnings found (non-critical)
    2 = errors found (data corruption)
"""

import argparse
import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import NamedTuple

PROJECT_ROOT = Path(__file__).parent.parent
RESOURCES = PROJECT_ROOT / "resources"
PROLOG_FILE = PROJECT_ROOT / "poe2_crafting.pl"
POC_ROOT = Path.home() / "projects" / "POE2-PathOfCrafting"


class AuditResult(NamedTuple):
    check: str
    status: str  # "pass", "warn", "fail"
    message: str
    details: list[str]


# ============================================================================
# Prolog parser (same as test_data_fidelity.py)
# ============================================================================

def split_args(s: str) -> list[str]:
    args = []
    depth_paren = 0
    depth_bracket = 0
    current = []
    in_quote = False
    quote_char = None
    for ch in s:
        if in_quote:
            current.append(ch)
            if ch == quote_char and (len(current) < 2 or current[-2] != '\\'):
                in_quote = False
            continue
        if ch in ("'", '"'):
            in_quote = True
            quote_char = ch
            current.append(ch)
        elif ch == '(':
            depth_paren += 1
            current.append(ch)
        elif ch == ')':
            depth_paren -= 1
            current.append(ch)
        elif ch == '[':
            depth_bracket += 1
            current.append(ch)
        elif ch == ']':
            depth_bracket -= 1
            current.append(ch)
        elif ch == ',' and depth_paren == 0 and depth_bracket == 0:
            args.append(''.join(current).strip())
            current = []
        else:
            current.append(ch)
    if current:
        args.append(''.join(current).strip())
    return args


def parse_facts(content: str, predicate: str) -> list[list[str]]:
    results = []
    pattern = re.compile(rf'^{re.escape(predicate)}\(', re.MULTILINE)
    for m in pattern.finditer(content):
        start = m.end() - 1
        depth = 0
        pos = start
        while pos < len(content):
            if content[pos] == '(':
                depth += 1
            elif content[pos] == ')':
                depth -= 1
                if depth == 0:
                    args_str = content[start + 1:pos]
                    results.append(split_args(args_str))
                    break
            pos += 1
    return results


def extract_list_items(s: str) -> list[str]:
    s = s.strip()
    if not s.startswith('[') or not s.endswith(']'):
        return []
    inner = s[1:-1].strip()
    if not inner:
        return []
    return [x.strip().strip("'\"") for x in split_args(inner)]


# ============================================================================
# Data loading
# ============================================================================

def load_kb_mod_groups() -> dict[str, list[tuple[str, str, str]]]:
    """Load all mod_groups from resource files. Returns category -> [(group, weight, slot)]."""
    result = defaultdict(list)
    for f in RESOURCES.glob("mods_*.pl"):
        content = f.read_text()
        for args in parse_facts(content, "mod_group"):
            if len(args) >= 8:
                result[args[0]].append((args[1], args[4], args[7]))
    return dict(result)


def load_kb_catalysts() -> dict[str, set[str]]:
    """Load quality_type facts. Returns name -> tags."""
    content = PROLOG_FILE.read_text()
    result = {}
    for args in parse_facts(content, "quality_type"):
        if len(args) >= 3:
            tags = set(extract_list_items(args[2]))
            result[args[1]] = tags
    return result


def load_kb_exclusion_groups() -> list[tuple[str, str, list[str]]]:
    """Load exclusion_group facts. Returns [(id, description, patterns)]."""
    eg_file = RESOURCES / "exclusion_groups.pl"
    if not eg_file.exists():
        return []
    content = eg_file.read_text()
    results = []
    for args in parse_facts(content, "exclusion_group"):
        if len(args) >= 4:
            patterns = extract_list_items(args[3])
            results.append((args[1], args[2], patterns))
    return results


def load_poc_weights() -> dict[str, int]:
    """Load PathOfCrafting weights.csv. Returns category -> row count."""
    csv_path = POC_ROOT / "backend" / "source_data" / "weights.csv"
    if not csv_path.exists():
        return {}
    counts = defaultdict(int)
    with open(csv_path) as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            cat = row.get("BASE", row.get("category", row.get("Category", "")))
            if cat:
                # Normalize: "BOOTS (STR/DEX)" -> "boots_str_dex"
                normalized = (cat.lower()
                    .replace(" (", "_")
                    .replace(")", "")
                    .replace("/", "_")
                    .replace(" ", "_"))
                counts[normalized] += 1
    return dict(counts)


def load_poc_catalysts() -> dict[str, set[str]]:
    """Load PathOfCrafting catalysts.json. Returns name -> matching_tags."""
    cat_path = POC_ROOT / "backend" / "source_data" / "catalysts.json"
    if not cat_path.exists():
        return {}
    data = json.loads(cat_path.read_text())
    result = {}
    for cat in data.get("catalysts", []):
        result[cat["name"]] = set(cat.get("matching_tags", []))
    return result


def load_poc_exclusion_groups() -> list[dict]:
    """Load PathOfCrafting exclusion_groups.json."""
    eg_path = POC_ROOT / "backend" / "source_data" / "exclusion_groups.json"
    if not eg_path.exists():
        return []
    return json.loads(eg_path.read_text())


# ============================================================================
# Audit checks
# ============================================================================

def audit_mod_group_counts(kb_groups: dict, poc_counts: dict) -> AuditResult:
    """Compare mod group counts per category against PathOfCrafting source."""
    if not poc_counts:
        return AuditResult("mod_group_counts", "warn",
                           "PathOfCrafting weights.csv not available", [])

    diffs = []
    for cat, expected in sorted(poc_counts.items()):
        actual = len(kb_groups.get(cat, []))
        if actual != expected:
            diffs.append(f"  {cat}: KB={actual}, source={expected} (diff={actual - expected:+d})")

    if not diffs:
        return AuditResult("mod_group_counts", "pass",
                           f"All {len(poc_counts)} categories match source counts", [])
    return AuditResult("mod_group_counts", "warn",
                       f"{len(diffs)} category count mismatches", diffs)


def audit_catalyst_tags(kb_cats: dict, poc_cats: dict) -> AuditResult:
    """Compare catalyst tags against PathOfCrafting source."""
    if not poc_cats:
        return AuditResult("catalyst_tags", "warn",
                           "PathOfCrafting catalysts.json not available", [])

    mismatches = []
    # Direct name mapping (handles possessives, hyphens, etc.)
    NAME_MAP = {
        "flesh catalyst": "flesh_catalyst",
        "neural catalyst": "neural_catalyst",
        "carapace catalyst": "carapace_catalyst",
        "uul-netol's catalyst": "uul_netol_catalyst",
        "xoph's catalyst": "xophs_catalyst",
        "tul's catalyst": "tuls_catalyst",
        "esh's catalyst": "eshs_catalyst",
        "chayula's catalyst": "chayulas_catalyst",
        "reaver catalyst": "reaver_catalyst",
        "sibilant catalyst": "sibilant_catalyst",
        "skittering catalyst": "skittering_catalyst",
        "adaptive catalyst": "adaptive_catalyst",
    }

    for poc_name, poc_tags in sorted(poc_cats.items()):
        kb_key = NAME_MAP.get(poc_name.lower())
        kb_tags = kb_cats.get(kb_key, set()) if kb_key else set()

        if kb_tags:
            missing = poc_tags - kb_tags
            extra = kb_tags - poc_tags
            if missing or extra:
                parts = []
                if missing:
                    parts.append(f"missing={missing}")
                if extra:
                    parts.append(f"extra={extra}")
                mismatches.append(f"  {poc_name}: {', '.join(parts)}")
        else:
            mismatches.append(f"  {poc_name}: NOT FOUND in KB")

    if not mismatches:
        return AuditResult("catalyst_tags", "pass",
                           f"All {len(poc_cats)} catalysts match source tags", [])
    return AuditResult("catalyst_tags", "warn",
                       f"{len(mismatches)} catalyst tag mismatches", mismatches)


def audit_exclusion_group_counts(kb_groups: list, poc_groups: list) -> AuditResult:
    """Compare exclusion group counts against PathOfCrafting source."""
    if not poc_groups:
        return AuditResult("exclusion_group_counts", "warn",
                           "PathOfCrafting exclusion_groups.json not available", [])

    kb_count = len(kb_groups)
    poc_count = len(poc_groups)

    if kb_count == poc_count:
        return AuditResult("exclusion_group_counts", "pass",
                           f"{kb_count} exclusion groups match source", [])
    return AuditResult("exclusion_group_counts", "fail",
                       f"KB has {kb_count} exclusion groups, source has {poc_count}",
                       [f"  Difference: {kb_count - poc_count:+d}"])


def audit_weight_sanity(kb_groups: dict) -> AuditResult:
    """Check for suspicious weight patterns."""
    issues = []
    for cat, groups in sorted(kb_groups.items()):
        weights = [int(w) for _, w, _ in groups]
        if not weights:
            continue

        total = sum(weights)
        zero_count = sum(1 for w in weights if w == 0)
        negative_count = sum(1 for w in weights if w < 0)
        max_weight = max(weights)

        if negative_count:
            issues.append(f"  {cat}: {negative_count} negative weights")
        if max_weight > 10000:
            issues.append(f"  {cat}: max weight {max_weight} exceeds 10000")
        if total > 0:
            for group, w, slot in groups:
                wi = int(w)
                if wi > 0 and wi / total > 0.5:
                    issues.append(f"  {cat}/{group}: {wi} = {wi/total*100:.0f}% of total {total}")

    if not issues:
        return AuditResult("weight_sanity", "pass",
                           f"All {sum(len(v) for v in kb_groups.values())} weights in valid range", [])
    return AuditResult("weight_sanity", "warn",
                       f"{len(issues)} weight anomalies", issues)


def audit_slot_balance(kb_groups: dict) -> AuditResult:
    """Check prefix/suffix balance per category."""
    warnings = []
    for cat, groups in sorted(kb_groups.items()):
        prefixes = sum(1 for _, _, s in groups if s == "prefix")
        suffixes = sum(1 for _, _, s in groups if s == "suffix")
        total = len(groups)
        if total >= 10:
            ratio = min(prefixes, suffixes) / max(prefixes, suffixes) if max(prefixes, suffixes) > 0 else 0
            if ratio < 0.3:
                warnings.append(
                    f"  {cat}: {prefixes}P/{suffixes}S (ratio {ratio:.2f})"
                )

    if not warnings:
        return AuditResult("slot_balance", "pass",
                           "All categories have reasonable prefix/suffix balance", [])
    return AuditResult("slot_balance", "warn",
                       f"{len(warnings)} categories with skewed prefix/suffix ratio",
                       warnings)


def audit_orphan_references() -> AuditResult:
    """Check that all load_files directives reference existing files."""
    content = PROLOG_FILE.read_text()
    referenced = re.findall(r"load_files\('resources/([^']+)'\)", content)

    missing = []
    for ref in referenced:
        if not (RESOURCES / ref).exists():
            missing.append(f"  resources/{ref}")

    if not missing:
        return AuditResult("orphan_references", "pass",
                           f"All {len(referenced)} load_files targets exist", [])
    return AuditResult("orphan_references", "fail",
                       f"{len(missing)} missing resource files", missing)


# ============================================================================
# Main
# ============================================================================

def run_audit(quick: bool = False) -> list[AuditResult]:
    """Run all audit checks."""
    results = []

    # Load data
    kb_groups = load_kb_mod_groups()
    kb_cats = load_kb_catalysts()
    kb_excl = load_kb_exclusion_groups()

    # Core structural checks (always run)
    results.append(audit_orphan_references())
    results.append(audit_weight_sanity(kb_groups))
    results.append(audit_slot_balance(kb_groups))

    if quick:
        return results

    # Cross-reference checks (need PathOfCrafting source)
    poc_counts = load_poc_weights()
    poc_cats = load_poc_catalysts()
    poc_excl = load_poc_exclusion_groups()

    results.append(audit_mod_group_counts(kb_groups, poc_counts))
    results.append(audit_catalyst_tags(kb_cats, poc_cats))
    results.append(audit_exclusion_group_counts(kb_excl, poc_excl))

    return results


def print_report(results: list[AuditResult], as_json: bool = False):
    """Print audit report."""
    if as_json:
        output = []
        for r in results:
            output.append({
                "check": r.check,
                "status": r.status,
                "message": r.message,
                "details": r.details,
            })
        print(json.dumps(output, indent=2))
        return

    # Terminal output
    icons = {"pass": "✓", "warn": "⚠", "fail": "✗"}
    colors = {"pass": "\033[32m", "warn": "\033[33m", "fail": "\033[31m"}
    reset = "\033[0m"

    print("=" * 60)
    print("  QA AUDIT REPORT — poe2-crafting-guide")
    print("=" * 60)
    print()

    pass_count = sum(1 for r in results if r.status == "pass")
    warn_count = sum(1 for r in results if r.status == "warn")
    fail_count = sum(1 for r in results if r.status == "fail")

    for r in results:
        icon = icons.get(r.status, "?")
        color = colors.get(r.status, "")
        print(f"  {color}{icon}{reset} [{r.check}] {r.message}")
        for detail in r.details[:10]:
            print(f"    {detail}")
        if len(r.details) > 10:
            print(f"    ... and {len(r.details) - 10} more")

    print()
    print("-" * 60)
    print(f"  {pass_count} passed, {warn_count} warnings, {fail_count} failures")
    print("-" * 60)

    if fail_count:
        print(f"\n  \033[31mAUDIT FAILED\033[0m — {fail_count} critical issues found")
    elif warn_count:
        print(f"\n  \033[33mAUDIT PASSED WITH WARNINGS\033[0m — {warn_count} non-critical issues")
    else:
        print(f"\n  \033[32mAUDIT PASSED\033[0m — all checks clean")


def main():
    parser = argparse.ArgumentParser(description="QA audit for poe2-crafting-guide")
    parser.add_argument("--quick", action="store_true", help="Quick check (local only)")
    parser.add_argument("--json", action="store_true", help="Machine-readable JSON output")
    args = parser.parse_args()

    results = run_audit(quick=args.quick)
    print_report(results, as_json=args.json)

    fail_count = sum(1 for r in results if r.status == "fail")
    warn_count = sum(1 for r in results if r.status == "warn")

    if fail_count:
        sys.exit(2)
    elif warn_count:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
