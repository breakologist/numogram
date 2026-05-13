#!/usr/bin/env python3
"""
Oracle-Seeded Text Generator

Pipeline: Seed → Oracle Reading → Text Recombination → Output

1. Take a seed (word, phrase, or number)
2. Run numogram-oracle/oracle.py to get the reading
3. Extract zone descriptions, path text, reading text, quasiphonic sounds
4. Feed the oracle's own words back into xeno-jump and cut-up engines
5. Output: alien text informed by the oracle's zone

Usage:
  python3 oracle_text_seed.py --seed 192855           # Oracle reading + xeno-jump
  python3 oracle_text_seed.py --text "Xenotation"     # AQ→Zone + xeno-jump
  python3 oracle_text_seed.py --seed 666 --steps 20    # Longer chain
  python3 oracle_text_seed.py --seed 42 --cutup all    # Oracle reading + zone cut-up
  python3 oracle_text_seed.py --random                 # Random.org seed
  python3 oracle_text_seed.py --hardware               # Machine entropy seed
  python3 oracle_text_seed.py --blockchain             # BTC hash seed

Output goes to stdout and optionally to a file.
"""

import os
import sys
import subprocess
import json
import argparse
import datetime
import random

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from xeno_jump import load_index, process_text, get_aq
import cut_up

# ═══════════════════════════════════════════
# ORACLE INTERACTION
# ═══════════════════════════════════════════

ORACLE_SCRIPT = os.path.expanduser('~/.hermes/skills/numogram-oracle/oracle.py')

ZONES = {
    0: {"name": "eiaoung", "polarity": "−", "current": "Plex",   "region": "Plex"},
    1: {"name": "gl",      "polarity": "+", "current": "Sink",   "region": "Time-Circuit"},
    2: {"name": "dt",      "polarity": "−", "current": "Hold",   "region": "Time-Circuit"},
    3: {"name": "zx",      "polarity": "+", "current": "Warp",   "region": "Warp"},
    4: {"name": "skr",     "polarity": "−", "current": "Sink",   "region": "Time-Circuit"},
    5: {"name": "ktt",     "polarity": "+", "current": "Hold",   "region": "Time-Circuit"},
    6: {"name": "tch",     "polarity": "−", "current": "Warp",   "region": "Warp"},
    7: {"name": "pb",      "polarity": "+", "current": "Rise",   "region": "Time-Circuit"},
    8: {"name": "mnm",     "polarity": "−", "current": "Rise",   "region": "Time-Circuit"},
    9: {"name": "tn",      "polarity": "+", "current": "Plex",   "region": "Plex"},
}

def fetch_seed(args):
    """Get seed from various entropy sources"""
    if args.random:
        import urllib.request
        resp = urllib.request.urlopen(
            "https://www.random.org/integers/?num=1&min=0&max=999999&col=1&base=10&format=plain&rnd=new",
            timeout=10)
        return int(resp.read().strip()), "random.org"
    elif args.blockchain:
        import urllib.request
        resp = urllib.request.urlopen("https://blockchain.info/latestblock", timeout=10)
        data = json.loads(resp.read())
        return int(data["hash"][:8], 16), "blockchain"
    elif args.hardware:
        try:
            result = subprocess.run(
                ["python3", os.path.expanduser("~/.hermes/tools/hardware_entropy.py")],
                capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if 'Seed:' in line:
                        hex_str = line.split('Seed:')[1].strip()
                        return int(hex_str[:12], 16), "hardware"
        except:
            pass
        import time
        return int(time.time_ns()) % 1000000, "time"
    return args.seed, "manual"

def run_oracle(seed, source="manual"):
    """Run oracle.py and parse its output"""
    result = subprocess.run(
        ["python3", ORACLE_SCRIPT, "--seed", str(seed)],
        capture_output=True, text=True, timeout=30)
    
    output = result.stdout
    reading_raw = output
    
    # Parse key fields
    zone = None
    reading_text = ""
    path_text = ""
    sound_name = ""
    
    for line in output.split('\n'):
        if 'Zone:' in line:
            # Extract zone number
            import re
            m = re.search(r'Zone:\s+(\d+)', line)
            if m:
                zone = int(m.group(1))
        elif line.startswith('  Zone:') and '(' in line:
            import re
            m = re.search(r'Zone:\s+(\d+)\s+\((\w+)\s*—\s*(.+?)\)', line)
            if m:
                zone = int(m.group(1))
                try:
                    ZONES[zone]["name"] = m.group(2)
                    ZONES[zone]["desc"] = m.group(3)
                except:
                    pass
        elif 'Book of Paths:' in line:
            path_text = line.split('Book of Paths:')[1].strip()
    
    if zone is not None and 0 <= zone <= 9:
        z = ZONES[zone]
        reading_text = z.get("reading", f"Zone {zone} ({z['name']}) — {z['region']} {z['current']} current.")
        path_text = z.get("path", path_text)
        sound_name = z["name"]
    else:
        z = None
    
    return {
        "seed": seed,
        "source": source,
        "zone": zone,
        "zone_data": z,
        "reading": reading_text,
        "path": path_text,
        "sound": sound_name,
        "raw": reading_raw,
    }

def build_corpus(oracle_result):
    """Build a corpus from oracle reading for cut-up/xeno-jump"""
    parts = []
    
    # The oracle's own reading
    if oracle_result["reading"]:
        parts.append(oracle_result["reading"])
    
    # Path text
    if oracle_result["path"]:
        parts.append(oracle_result["path"])
    
    # Zone description
    if oracle_result["zone_data"]:
        z = oracle_result["zone_data"]
        parts.append(f"Zone {oracle_result['zone']} — {z['name']}: {z.get('desc', '')}")
        parts.append(f"Current: {z['current']}, Region: {z['region']}, Polarity: {z['polarity']}")
    
    # Raw oracle output (filtered to clean text)
    raw_lines = oracle_result["raw"].split('\n')
    for line in raw_lines:
        line = line.strip()
        # Keep reading/Book of Paths lines
        if any(kw in line for kw in ['The ', 'Descent', 'Waiting', 'The Warp', 'Rising',
           'Pressure', 'The lullaby', 'The Pandemonium', 'Original Sub', 'Extreme',
           'Abysmal', 'Primordial', 'Slipping', 'Attaining', 'Progressive', 'Eternal',
           'Sudden Flight', 'Plex', 'Abyss']):
            parts.append(line)
    
    # The seed itself as AQ text
    parts.append(f"Seed {oracle_result['seed']} → Zone {oracle_result['zone']}")
    
    # Combine
    corpus = '\n'.join(parts)
    return corpus

def xeno_jump_from_oracle(oracle_result, corpus, steps=10, seed=666):
    """Run xeno-jump using oracle text as source"""
    # Extract key words/phrases from oracle output
    key_phrases = [
        oracle_result["reading"],
        oracle_result["path"],
        oracle_result["sound"],
    ]
    
    results = []
    
    for phrase in key_phrases:
        if not phrase or len(phrase) < 5:
            continue
        
        # Xeno-jump the phrase
        result, jumps = process_text(phrase, MockIndex(load_index()), mode='all', seed=seed)
        
        results.append({
            "source": phrase,
            "jumped": result,
            "jumps": jumps,
        })
    
    return results

def cutup_from_oracle(oracle_result, corpus, mode='all', seed=666):
    """Run zone-profiled cut-up on oracle text"""
    results = []
    
    zone = oracle_result["zone"]
    if zone is None or mode == 'all':
        zones_to_run = range(10)
    else:
        zones_to_run = [zone]
    
    cleaned = corpus.replace('\\n', '\n')
    frags = cut_up.fragment(cleaned, 'sentence')
    
    for z_num in zones_to_run:
        z = cut_up.ZONES[z_num]
        frags = cut_up.fragment(cleaned, z['mode'])
        kept = cut_up.cut(frags, z['cut'])
        if z.get('rec'):
            kept = cut_up.recombine(kept, z.get('rs', 'echo'))
        if z['xen']:
            kept = [cut_up.xenotate(f, z.get('xmode', 'sparse')) for f in kept]
        kept = kept[:12]
        if z.get('prefix'):
            kept = [z['prefix'] + k for k in kept]
        result = z['sep'].join(kept)
        results.append((z_num, z['name'], result))
    
    return results

class MockIndex:
    def __init__(self, d): self.data = d
    def get(self, k, d=None): return self.data.get(k, d)

def main():
    parser = argparse.ArgumentParser(description="Oracle-Seeded Text Generator")
    parser.add_argument("--seed", type=int, default=192855, help="Seed number")
    parser.add_argument("--text", type=str, help="Seed text (computes AQ)")
    parser.add_argument("--steps", type=int, default=20, help="Xeno-jump steps")
    parser.add_argument("--random", action='store_true', help="Random.org seed")
    parser.add_argument("--hardware", action='store_true', help="Machine entropy seed")
    parser.add_argument("--blockchain", action='store_true', help="BTC hash seed")
    parser.add_argument("--cutup", choices=['zone', 'all'], help="Run cut-up (zone=only oracle zone, all=all zones)")
    parser.add_argument("--output", type=str, help="Output file path")
    parser.add_argument("--quiet", action='store_true', help="Suppress verbose output")
    
    args = parser.parse_args()
    
    # Get seed
    seed, source = fetch_seed(args)
    if source != "manual":
        args.seed = seed
    
    # Run oracle
    if not args.quiet:
        print(f"\n╔════════════════════════════════════════════════╗")
        print("║     ORACLE-SEEDED TEXT GENERATOR             ║")
        print("╚════════════════════════════════════════════════╝")
        print(f"  Seed: {seed} ({source})")
        print(f"  Steps: {args.steps}")
        print()
    
    oracle = run_oracle(seed, source)
    
    # Print oracle reading
    if not args.quiet:
        print(f"  Oracle Reading:")
        print(f"  ─────────────────────────")
        if oracle["raw"]:
            print(f"{oracle['raw']}")
    
    # Build corpus from oracle output
    corpus = build_corpus(oracle)
    
    # Run xeno-jump on oracle text
    jump_results = xeno_jump_from_oracle(oracle, corpus, steps=args.steps, seed=seed)
    
    if not args.quiet:
        print(f"\n  Xeno-Jump from Oracle Text:")
        print(f"  ─────────────────────────")
        for jr in jump_results:
            print(f"\n  Source: {jr['source']}")
            print(f"  Jumped: {jr['jumped']}")
            if jr['jumps'][:5]:
                print(f"  Jumps:")
                for orig, new, aq, z in jr['jumps'][:5]:
                    print(f"    {orig} (AQ={aq}, Z{z}) → {new}")
    
    # Run cut-up on oracle text
    if args.cutup:
        cutup_results = cutup_from_oracle(oracle, corpus, mode=args.cutup, seed=seed)
        
        if not args.quiet:
            print(f"\n  Zone Cut-Up from Oracle Text:")
            print(f"  ─────────────────────────")
            for z_num, z_name, result in cutup_results:
                print(f"\n  ZONE {z_num} [{z_name}]")
                print(f"  {result}")
    
    # Save full output to file if requested
    if args.output:
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        full_output = f"Oracle-Seeded Text Output ({timestamp})\n"
        full_output += f"Seed: {seed} ({source})\n"
        full_output += f"Zone: {oracle['zone']} ({oracle['sound']})\n"
        full_output += "=" * 60 + "\n\n"
        full_output += f"ORACLE READING:\n{oracle['raw']}\n\n"
        full_output += f"XENO-JUMP RESULTS:\n"
        for jr in jump_results:
            full_output += f"  Source: {jr['source']}\n"
            full_output += f"  Jumped: {jr['jumped']}\n"
            if jr['jumps']:
                full_output += f"  Jumps: {', '.join(f'{o}→{n}' for o,n,_,_ in jr['jumps'][:10])}\n"
            full_output += "\n"
        
        if args.cutup:
            full_output += f"ZONE CUT-UP RESULTS:\n"
            for z_num, z_name, result in cutup_results:
                full_output += f"\nZONE {z_num} [{z_name}]:\n{result}\n"
        
        with open(args.output, 'w') as f:
            f.write(full_output)
        print(f"\n  ✅ Output saved to {args.output}")

if __name__ == '__main__':
    main()
