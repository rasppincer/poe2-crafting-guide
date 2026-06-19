"""Import POE2-PathOfCrafting source data into Prolog facts.

Converts:
  weights.csv        → mod_group/8 + mod_pool_weight_sum/3
  omens.json         → omen/5
  alloys.json        → alloy/4
  catalysts.json     → quality_type/3
  exclusion_groups.json → exclusion_group/2

Usage:
    python3 scripts/import_from_pathofcrafting.py [--diff]
    --diff: show what would change vs existing data (dry run)
"""

import csv
import json
import re
import sys
from pathlib import Path

SOURCE = Path("/tmp/poe2-pathofcrafting/backend/source_data")
OUT = Path(__file__).parent.parent / "resources"

# ============================================================================
# Category name mapping: "BOOTS (INT)" → "boots_int"
# ============================================================================

def normalize_category(raw: str) -> str:
    """Convert CSV BASE name to Prolog category atom."""
    raw = raw.strip()
    # "BOOTS (INT)" → "boots_int"
    # "BODY ARMOUR (STR/DEX)" → "body_armour_str_dex"
    # "ONE HAND MACE" → "one_hand_mace"
    # "RING" → "ring"
    raw = raw.replace("/", "_")
    raw = re.sub(r'[()]', '', raw)
    raw = raw.lower().replace(' ', '_')
    raw = re.sub(r'_+', '_', raw).strip('_')
    return raw

def group_id_from_name(name: str) -> str:
    """Convert mod description to a CamelCase group ID."""
    # "#% increased Energy Shield" → "PercentIncreasedEnergyShield"
    # "# to maximum Life" → "FlattoMaximumLife"
    # "Adds # to # Physical Damage" → "AddsFlattoFlatPhysicalDamage"
    # "Leech #% of Physical Attack Damage as Life" → "LeechPercentOfPhysicalAttackDamageAsLife"
    
    s = name.strip()
    # Replace common patterns
    s = s.replace("#%", "Percent")
    s = s.replace("# to #", "FlattoFlat")
    s = s.replace("# to", "Flatto")
    s = s.replace("#", "Flat")
    s = s.replace("%", "Percent")
    # Remove special chars
    s = re.sub(r'[^a-zA-Z0-9 ]', '', s)
    # CamelCase
    words = s.split()
    result = ''.join(w.capitalize() for w in words if w)
    # Ensure starts with uppercase (Prolog variable convention, but we'll quote it)
    if result and result[0].isdigit():
        result = 'Mod' + result
    return result

def infer_tags(desc: str) -> list:
    """Infer mod tags from description text."""
    desc_lower = desc.lower()
    tags = []
    tag_keywords = {
        'life': ['life', 'maximum life'],
        'mana': ['mana', 'maximum mana'],
        'energy_shield': ['energy shield'],
        'armour': ['armour', 'armor'],
        'evasion': ['evasion'],
        'fire': ['fire'],
        'cold': ['cold', 'freeze', 'chill'],
        'lightning': ['lightning', 'shock'],
        'chaos': ['chaos'],
        'physical': ['physical'],
        'attack': ['attack'],
        'spell': ['spell'],
        'caster': ['cast speed', 'caster'],
        'speed': ['speed', 'movement speed'],
        'critical': ['critical'],
        'attribute': ['strength', 'dexterity', 'intelligence', 'all attributes'],
        'resistance': ['resistance'],
        'damage': ['damage'],
        'defence': ['defence', 'defense'],
        'rarity': ['rarity'],
        'accuracy': ['accuracy'],
        'block': ['block'],
        'stun': ['stun'],
        'leech': ['leech'],
        'regeneration': ['regeneration', 'regen'],
        'flask': ['flask'],
        'charm': ['charm'],
    }
    for tag, keywords in tag_keywords.items():
        if any(kw in desc_lower for kw in keywords):
            tags.append(tag)
    return tags

# ============================================================================
# Weights CSV → mod_group/8 + mod_pool_weight_sum/3
# ============================================================================

def import_weights():
    """Parse weights.csv and generate mod_group facts."""
    csv_path = SOURCE / "weights.csv"
    if not csv_path.exists():
        print(f"ERROR: {csv_path} not found")
        return {}
    
    # Group by category
    categories = {}  # category → {slot → [(group_id, desc, tags, weight, max_ilvl, tier_count)]}
    
    with open(csv_path) as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            base = row.get('BASE', '').strip()
            slot = row.get('TYPE', '').strip().lower()  # PREFIX or SUFFIX → prefix or suffix
            name = row.get('NAME', '').strip()
            
            if not base or not slot or not name or base == 'BASE':
                continue
            
            cat = normalize_category(base)
            gid = group_id_from_name(name)
            tags = infer_tags(name)
            
            # Parse tier weights (columns 1-13)
            tier_weights = []
            for i in range(1, 14):
                val = row.get(str(i), '').strip()
                if val and val.isdigit():
                    tier_weights.append(int(val))
            
            if not tier_weights:
                continue
            
            # Weight = max across tiers (the base weight for rolling)
            weight = max(tier_weights)
            tier_count = len(tier_weights)
            
            # Max ilvl = number of tiers (rough approximation — higher tiers need higher ilvl)
            # Actually, the column number maps to tier — column 1 = T1 (highest), column 13 = T13 (lowest)
            # Max ilvl = tier_count * some factor. For now, use 100 as default.
            max_ilvl = 100
            
            if cat not in categories:
                categories[cat] = {'prefix': [], 'suffix': []}
            categories[cat][slot].append((gid, name, tags, weight, max_ilvl, tier_count))
    
    return categories

def write_mod_files(categories: dict, dry_run=False):
    """Write one .pl file per category."""
    files_written = []
    for cat, slots in sorted(categories.items()):
        filename = f"mods_{cat}.pl"
        filepath = OUT / filename
        
        lines = []
        lines.append(f"%%% Mod data for {cat}")
        lines.append(f"%%% Source: POE2-PathOfCrafting (frankthetank001/POE2-PathOfCrafting)")
        lines.append(f"%%% Original data: poe2db.tw via weights.csv")
        lines.append(f"%%% Auto-imported by import_from_pathofcrafting.py")
        lines.append("")
        lines.append("%% mod_group(+Category, +GroupId, +Desc, +Tags, +Weight, +MaxIlvl, +TierCount, +Slot)")
        lines.append("")
        
        # Weight sums
        for slot in ['prefix', 'suffix']:
            total = sum(w[3] for w in slots.get(slot, []))
            lines.append(f"mod_pool_weight_sum({cat}, {slot}, {total}).")
        lines.append("")
        
        # Mod groups
        for slot in ['prefix', 'suffix']:
            if not slots.get(slot):
                continue
            for gid, desc, tags, weight, max_ilvl, tier_count in slots[slot]:
                tags_str = ', '.join(tags) if tags else ''
                lines.append(f"mod_group({cat}, '{gid}', '{desc}', [{tags_str}], {weight}, {max_ilvl}, {tier_count}, {slot}).")
            lines.append("")
        
        content = '\n'.join(lines) + '\n'
        
        if dry_run:
            if filepath.exists():
                existing = filepath.read_text()
                if existing.strip() != content.strip():
                    print(f"  CHANGED: {filename}")
                else:
                    print(f"  OK: {filename}")
            else:
                print(f"  NEW: {filename}")
        else:
            filepath.write_text(content)
            files_written.append(filename)
    
    if not dry_run:
        print(f"Wrote {len(files_written)} mod files to {OUT}/")
    return files_written

# ============================================================================
# Omens JSON → omen/5
# ============================================================================

def import_omens(dry_run=False):
    """Parse omens.json and generate omen facts."""
    json_path = SOURCE / "omens.json"
    if not json_path.exists():
        print(f"ERROR: {json_path} not found")
        return
    
    omens = json.loads(json_path.read_text())
    
    # Map display names to our atom names
    name_map = {
        'Omen of Whittling': 'whittling',
        'Omen of Sinistral Erasure': 'sinistral_erasure',
        'Omen of Dextral Erasure': 'dextral_erasure',
        'Omen of Chaotic Rarity': 'omen_of_chaotic_rarity',
        'Omen of Chaotic Quantity': 'omen_of_chaotic_quantity',
        'Omen of Greater Exaltation': 'greater_exaltation',
        'Omen of Greater Annulment': 'greater_annulment',
        'Omen of Sinistral Exaltation': 'sinistral_exaltation',
        'Omen of Dextral Exaltation': 'dextral_exaltation',
        'Omen of Sinistral Annulment': 'sinistral_annulment',
        'Omen of Dextral Annulment': 'dextral_annulment',
        'Omen of Sinistral Alchemy': 'sinistral_alchemy',
        'Omen of Dextral Alchemy': 'dextral_alchemy',
        'Omen of Sinistral Coronation': 'sinistral_coronation',
        'Omen of Dextral Coronation': 'dextral_coronation',
        'Omen of Homogenising Exaltation': 'homogenising_exaltation',
        'Omen of Homogenising Coronation': 'homogenising_coronation',
        'Omen of Catalysing Exaltation': 'catalysing_exaltation',
        'Omen of Sinistral Crystallisation': 'sinistral_crystallisation',
        'Omen of Dextral Crystallisation': 'dextral_crystallisation',
        'Omen of Sinistral Necromancy': 'sinistral_necromancy',
        'Omen of Dextral Necromancy': 'dextral_necromancy',
        'Omen of Chance': 'omen_of_chance',
        'Omen of the Ancients': 'omen_of_the_ancients',
        'Omen of Blessed': 'omen_of_blessed',
        'Omen of Sanctification': 'omen_of_sanctification',
        'Omen of Corruption': 'omen_of_corruption',
        'Omen of Light': 'omen_of_light',
        'Omen of Putrefaction': 'omen_of_putrefaction',
        'Omen of Recombination': 'omen_of_recombination',
        'Omen of Sovereign': 'omen_of_sovereign',
        'Omen of Liege': 'omen_of_liege',
        'Omen of Blackblooded': 'omen_of_blackblooded',
        'Omen of Abyssal Echoes': 'omen_of_abyssal_echoes',
    }
    
    # Map currency names to our atom names
    currency_map = {
        'Chaos Orb': 'chaos_orb',
        'Exalted Orb': 'exalted_orb',
        'Orb of Annulment': 'orb_of_annulment',
        'Orb of Alchemy': 'orb_of_alchemy',
        'Regal Orb': 'regal_orb',
        'Orb of Chance': 'orb_of_chance',
        'Divine Orb': 'divine_orb',
        'Vaal Orb': 'vaal_orb',
        'Essence': 'essence',
        'Desecration': 'desecration',
        'Recombination': 'recombination',
        'Any': 'any_currency',
    }
    
    lines = []
    lines.append("%%% Omen data — imported from POE2-PathOfCrafting")
    lines.append("")
    
    found = []
    not_mapped = []
    for omen in omens:
        display_name = omen['name']
        atom = name_map.get(display_name)
        if not atom:
            not_mapped.append(display_name)
            continue
        
        currency_display = omen['affected_currency']
        currency_atom = currency_map.get(currency_display, 'any_currency')
        
        # Determine effect and slot from description
        desc = omen.get('effect_description', '')
        effect = 'custom'
        slot = 'both'
        
        if 'prefix' in desc.lower():
            slot = 'prefix'
            if 'removes' in desc.lower():
                effect = 'removes_only_prefixes'
            elif 'adds' in desc.lower():
                effect = 'adds_only_prefixes'
        elif 'suffix' in desc.lower():
            slot = 'suffix'
            if 'removes' in desc.lower():
                effect = 'removes_only_suffixes'
            elif 'adds' in desc.lower():
                effect = 'adds_only_suffixes'
        
        found.append((atom, currency_atom, effect, slot))
        lines.append(f"omen(poe2, {atom}, {currency_atom}, {effect}, {slot}).")
    
    content = '\n'.join(lines) + '\n'
    
    if not_mapped:
        print(f"  Unmapped omens ({len(not_mapped)}): {not_mapped}")
    
    if dry_run:
        print(f"  Would write {len(found)} omen facts")
        return found
    else:
        filepath = OUT / "omens_imported.pl"
        filepath.write_text(content)
        print(f"Wrote {len(found)} omen facts to {filepath}")
        return found

# ============================================================================
# Main
# ============================================================================

def main():
    dry_run = '--diff' in sys.argv
    
    if dry_run:
        print("=== DRY RUN (no files written) ===\n")
    
    print("1. Importing weights.csv...")
    categories = import_weights()
    print(f"   Found {len(categories)} categories, {sum(len(s['prefix'])+len(s['suffix']) for s in categories.values())} mod groups")
    
    if not dry_run:
        write_mod_files(categories)
    else:
        write_mod_files(categories, dry_run=True)
    
    print("\n2. Importing omens.json...")
    import_omens(dry_run=dry_run)
    
    print("\n3. Importing alloys.json...")
    # TODO: implement alloy import
    alloys = json.loads((SOURCE / "alloys.json").read_text())
    print(f"   Found {len(alloys)} alloys (import pending)")
    
    print("\n4. Importing catalysts.json...")
    cats_data = json.loads((SOURCE / "catalysts.json").read_text())
    catalysts = cats_data.get('catalysts', [])
    print(f"   Found {len(catalysts)} catalysts (import pending)")
    
    print("\n5. Importing exclusion_groups.json...")
    exclusions = json.loads((SOURCE / "exclusion_groups.json").read_text())
    print(f"   Found {len(exclusions)} exclusion groups (import pending)")
    
    print("\nDone.")

if __name__ == '__main__':
    main()
