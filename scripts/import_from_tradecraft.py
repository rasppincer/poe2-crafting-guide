"""Import data from POE2-PathOfCrafting into our Prolog KB format.

Reads:
  - weights.csv → mod_group/8 facts + weight_sums
  - currency_configs.json → currency/2 facts + currency mechanics
  - omens.json → omen/5 facts
  - catalysts.json → quality_type/3 facts
  - exclusion_groups.json → exclusion_group facts

Writes:
  - resources/mods_<category>.pl — Prolog data files per category
  - resources/imported_omens.json — structured omen data
  - resources/imported_currencies.json — structured currency data
  - resources/imported_catalysts.json — structured catalyst data
  - resources/imported_exclusions.json — exclusion rules
"""

import csv
import json
import re
from pathlib import Path
from collections import defaultdict

SOURCE = Path.home() / "projects" / "POE2-PathOfCrafting" / "backend" / "source_data"
OUTPUT = Path(__file__).parent.parent / "resources"


def sanitize_name(name: str) -> str:
    """Convert a mod description to a Prolog-safe atom name."""
    # Remove special chars, replace spaces with underscores
    s = name.strip()
    s = s.replace("#%", "Percent")
    s = s.replace("# to", "FlatTo")
    s = s.replace("#", "Flat")
    s = re.sub(r'[^a-zA-Z0-9_]', '_', s)
    s = re.sub(r'_+', '_', s).strip('_')
    # Capitalize first letter of each word for readability
    parts = s.split('_')
    return ''.join(p.capitalize() for p in parts if p)


def base_to_category(base: str) -> str:
    """Convert a weights.csv base name to our category format."""
    # "BODY ARMOUR (STR)" → "body_armour_str"
    # "RING" → "ring"
    # "BOW" → "bow"
    s = base.strip().lower()
    s = s.replace('(', '').replace(')', '')
    s = s.replace('/', '_')
    s = s.replace(' ', '_')
    s = re.sub(r'_+', '_', s).strip('_')
    return s


def import_weights():
    """Import weights.csv into Prolog mod_group facts per category."""
    weights_file = SOURCE / "weights.csv"
    
    categories = defaultdict(lambda: {"prefixes": [], "suffixes": [], "prefix_sum": 0, "suffix_sum": 0})
    
    with open(weights_file, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        header = next(reader)  # Skip header
        
        for row in reader:
            if len(row) < 4:
                continue
            
            base = row[0].strip()
            mod_type = row[1].strip().lower()
            mod_name = row[2].strip()
            
            if not base or base == 'BASE' or not mod_type or not mod_name:
                continue
            
            # Parse tier weights (columns 3-15 = tiers 1-13)
            tier_weights = []
            for i in range(3, min(16, len(row))):
                val = row[i].strip()
                if val and val.isdigit():
                    tier_weights.append(int(val))
            
            if not tier_weights:
                continue
            
            # Use the highest tier weight as the representative weight
            # (higher tiers = higher ilvl, weight determines roll probability)
            weight = tier_weights[0]  # Tier 1 weight
            
            # Count non-zero tiers
            non_zero_tiers = sum(1 for w in tier_weights if w > 0)
            
            category = base_to_category(base)
            slot = "prefix" if mod_type == "prefix" else "suffix"
            group_name = sanitize_name(mod_name)
            
            # Extract tags from mod name
            tags = extract_tags(mod_name)
            
            entry = {
                "group": group_name,
                "description": mod_name,
                "tags": tags,
                "weight": weight,
                "maxIlvl": 100,  # Default — we don't have per-tier ilvl data in this format
                "tierCount": non_zero_tiers,
                "slot": slot,
                "tier_weights": tier_weights,
            }
            
            if slot == "prefix":
                categories[category]["prefixes"].append(entry)
                categories[category]["prefix_sum"] += weight
            else:
                categories[category]["suffixes"].append(entry)
                categories[category]["suffix_sum"] += weight
    
    return categories


def extract_tags(mod_name: str) -> list:
    """Extract mod tags from the description."""
    name_lower = mod_name.lower()
    tags = []
    
    tag_keywords = {
        'life': 'life', 'mana': 'mana', 'armour': 'armour', 'armor': 'armour',
        'evasion': 'evasion', 'energy shield': 'energy_shield',
        'fire': 'fire', 'cold': 'cold', 'lightning': 'lightning', 'chaos': 'chaos',
        'physical': 'physical', 'attack': 'attack', 'caster': 'caster',
        'speed': 'speed', 'critical': 'critical', 'spell': 'spell',
        'attribute': 'attribute', 'strength': 'attribute', 'dexterity': 'attribute',
        'intelligence': 'attribute', 'resistance': 'resistance',
        'damage': 'damage', 'defence': 'defence', 'runic': 'runic_ward',
        'spirit': 'spirit', 'accuracy': 'accuracy', 'block': 'block',
    }
    
    for keyword, tag in tag_keywords.items():
        if keyword in name_lower and tag not in tags:
            tags.append(tag)
    
    return tags


def write_prolog_files(categories: dict):
    """Write Prolog data files for each category."""
    OUTPUT.mkdir(parents=True, exist_ok=True)
    
    written = 0
    for category, data in sorted(categories.items()):
        if not data["prefixes"] and not data["suffixes"]:
            continue
        
        filepath = OUTPUT / f"mods_{category}.pl"
        lines = [
            f"%%% Mod data for {category}",
            f"%%% Source: POE2-PathOfCrafting (frankthetank001/POE2-PathOfCrafting)",
            f"%%% Original data: poe2db.tw via weights.csv",
            f"%%% Imported: 2026-06-09",
            f"",
            f"%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)",
            f"",
        ]
        
        # Weight sums
        if data["prefix_sum"] > 0:
            lines.append(f"mod_pool_weight_sum({category}, prefix, {data['prefix_sum']}).")
        if data["suffix_sum"] > 0:
            lines.append(f"mod_pool_weight_sum({category}, suffix, {data['suffix_sum']}).")
        lines.append("")
        
        # Prefix mods
        for entry in data["prefixes"]:
            tags_str = ", ".join(entry["tags"]) if entry["tags"] else ""
            lines.append(
                f"mod_group({category}, {entry['group']}, "
                f"'{entry['description']}', [{tags_str}], "
                f"{entry['weight']}, {entry['maxIlvl']}, {entry['tierCount']}, prefix)."
            )
        
        # Suffix mods
        for entry in data["suffixes"]:
            tags_str = ", ".join(entry["tags"]) if entry["tags"] else ""
            lines.append(
                f"mod_group({category}, {entry['group']}, "
                f"'{entry['description']}', [{tags_str}], "
                f"{entry['weight']}, {entry['maxIlvl']}, {entry['tierCount']}, suffix)."
            )
        
        filepath.write_text("\n".join(lines) + "\n")
        written += 1
    
    return written


def import_currencies():
    """Import currency_configs.json."""
    with open(SOURCE / "currency_configs.json") as f:
        data = json.load(f)
    
    # Group by currency_type for summary
    by_type = defaultdict(list)
    for c in data:
        by_type[c.get("currency_type", "unknown")].append(c)
    
    return data


def import_omens():
    """Import omens.json."""
    with open(SOURCE / "omens.json") as f:
        data = json.load(f)
    return data


def import_catalysts():
    """Import catalysts.json."""
    with open(SOURCE / "catalysts.json") as f:
        data = json.load(f)
    return data


def import_exclusions():
    """Import exclusion_groups.json."""
    with open(SOURCE / "exclusion_groups.json") as f:
        data = json.load(f)
    return data


def main():
    print("=== Importing POE2-PathOfCrafting data ===\n")
    
    # 1. Import weights
    print("1. Importing weights.csv...")
    categories = import_weights()
    print(f"   Found {len(categories)} base categories")
    
    for cat in sorted(categories.keys()):
        data = categories[cat]
        print(f"   - {cat}: {len(data['prefixes'])}P + {len(data['suffixes'])}S "
              f"(sum: {data['prefix_sum']}P/{data['suffix_sum']}S)")
    
    # Write Prolog files
    written = write_prolog_files(categories)
    print(f"\n   Wrote {written} Prolog data files to {OUTPUT}/")
    
    # 2. Import currencies
    print("\n2. Importing currency_configs.json...")
    currencies = import_currencies()
    print(f"   Found {len(currencies)} currency entries")
    
    # Save structured data
    with open(OUTPUT / "imported_currencies.json", 'w') as f:
        json.dump(currencies, f, indent=2)
    print(f"   Saved to {OUTPUT}/imported_currencies.json")
    
    # 3. Import omens
    print("\n3. Importing omens.json...")
    omens = import_omens()
    print(f"   Found {len(omens)} omens")
    
    with open(OUTPUT / "imported_omens.json", 'w') as f:
        json.dump(omens, f, indent=2)
    print(f"   Saved to {OUTPUT}/imported_omens.json")
    
    # 4. Import catalysts
    print("\n4. Importing catalysts.json...")
    catalysts = import_catalysts()
    print(f"   Found {len(catalysts)} catalysts")
    
    with open(OUTPUT / "imported_catalysts.json", 'w') as f:
        json.dump(catalysts, f, indent=2)
    print(f"   Saved to {OUTPUT}/imported_catalysts.json")
    
    # 5. Import exclusions
    print("\n5. Importing exclusion_groups.json...")
    exclusions = import_exclusions()
    print(f"   Found {len(exclusions)} exclusion groups")
    
    with open(OUTPUT / "imported_exclusions.json", 'w') as f:
        json.dump(exclusions, f, indent=2)
    print(f"   Saved to {OUTPUT}/imported_exclusions.json")
    
    # Summary
    total_mods = sum(
        len(d["prefixes"]) + len(d["suffixes"])
        for d in categories.values()
    )
    print(f"\n=== Import Complete ===")
    print(f"  Categories: {len(categories)}")
    print(f"  Total mods: {total_mods}")
    print(f"  Currencies: {len(currencies)}")
    print(f"  Omens: {len(omens)}")
    print(f"  Catalysts: {len(catalysts)}")
    print(f"  Exclusion groups: {len(exclusions)}")


if __name__ == "__main__":
    main()
