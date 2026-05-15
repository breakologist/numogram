"""
Xeno-Jump: AQ-Preserving Text Mutation via Corpus Selection

Takes a text and replaces words with other words/phrases from our corpus(es)
that share the same AQ value (Sum of 10-35 per char).
The "numerical skeleton" of the text remains identical, but the vocabulary mutates.

The key difference from v1: we now support three distinct corpora, each giving
the mutated text a different flavor:
  - general   : Full English dictionary (88K words)
  - oracle    : Hyperstitional, arcane, system-native (9.7K words)  
  - xenon     : Zone texts, DSP, ML, tracker code (6.6K words)

Usage:
  python xeno_jump.py "The time is now" --corpus oracle
  python xeno_jump.py "The time is now" --mix oracle:0.7,xenon:0.3
  python xeno_jump.py "The time is now" --mode all --corpus xenon --zone 4,7
  python xeno_jump.py --mode all --corpus oracle "The machine speaks"
  python xeno_jump.py --recursive --generations 5 --corpus oracle "Void opens"
"""

import os
import re
import json
import random
import argparse
import sys
from collections import defaultdict

# ═══════════════════════════════════════════
# CORPUS PATHS
# ═══════════════════════════════════════════
CORPUS_DIR = os.path.dirname(os.path.abspath(__file__))

CORPUS_FILES = {
    'general': os.path.join(CORPUS_DIR, 'aq_corpus_index.json'),
    'oracle':  os.path.join(CORPUS_DIR, 'aq_corpus_oracle.json'),
    'xenon':   os.path.join(CORPUS_DIR, 'aq_corpus_xenon.json'),
}

# ═══════════════════════════════════════════
# CORE MATH
# ═══════════════════════════════════════════
def get_aq(word):
    """
    Canonical CCRU AQ Algorithm:
    A=10, B=11 ... Z=35.
    Non-alpha characters are ignored in the sum.
    """
    return sum(ord(c.upper()) - 55 for c in word if c.isalpha())

def digital_root(n):
    """Masonic Addition / Digital Root."""
    if n == 0: return 0
    return (n - 1) % 9 + 1

def zone_from_aq(aq_val):
    """Get zone from AQ value (digital root, 0 for 0)."""
    if aq_val <= 0:
        return 0
    dr = digital_root(aq_val)
    return dr

ZONE_NAMES = {
    0: "eiaoung", 1: "gl", 2: "dt", 3: "zx", 4: "skr",
    5: "ktt", 6: "tch", 7: "pb", 8: "mnm", 9: "tn"
}

# ═══════════════════════════════════════════
# CORPUS LOADING
# ═══════════════════════════════════════════
def load_corpus(name='general'):
    """Load a single corpus index."""
    path = CORPUS_FILES.get(name)
    if not path or not os.path.exists(path):
        raise FileNotFoundError(f"Corpus '{name}' not found at {path}")
    
    with open(path) as f:
        raw = json.load(f)
    return {int(k): v for k, v in raw.items()}

def load_blend(spec_str):
    """
    Load a blended corpus from spec like 'oracle:0.7,xenon:0.3'
    Returns a merged index with entries from all specified corpora.
    """
    parts = spec_str.split(',')
    indices = {}
    
    for part in parts:
        if ':' in part:
            name, weight = part.rsplit(':', 1)
        else:
            name = part.strip()
            weight = 1.0
        
        name = name.strip().lower()
        if name in CORPUS_FILES:
            indices[name] = load_corpus(name)
        else:
            raise ValueError(f"Unknown corpus: {name}")
    
    # Merge indices — combine word lists from all specified corpora
    merged = defaultdict(set)
    for name, idx in indices.items():
        for key, values in idx.items():
            for v in values:
                merged[key].add(v.lower())
    
    # Deduplicate and sort
    result = {}
    for key, values in merged.items():
        result[key] = sorted(list(values))
    
    return result

def load_corpus_or_blend(corp_spec):
    """Load single corpus or blend based on spec string."""
    if ':' in corp_spec or ',' in corp_spec:
        return load_blend(corp_spec)
    else:
        return load_corpus(corp_spec)

# ═══════════════════════════════════════════
# XENO-JUMP LOGIC
# ═══════════════════════════════════════════
def jump_word(word, index, strategy='random', seed=None, zone_filter=None):
    """
    Jump a single word to another with same AQ value.
    
    Args:
        word: The word to mutate
        index: AQ corpus index
        strategy: 'random', 'lexicographical', 'shortest', 'longest'
        seed: Random seed for reproducibility
        zone_filter: Optional list of zones to restrict to
    
    Returns:
        (new_word, jumped_bool, aq_value)
    """
    if seed is not None:
        random.seed(seed)
    
    val = get_aq(word)
    candidates = index.get(val, [])
    
    if not candidates:
        return word, False, val
    
    # Filter out the word itself
    options = [c for c in candidates if c.lower() != word.lower()]
    if not options:
        return word, False, val
    
    # Apply zone filter if specified
    if zone_filter:
        options = [o for o in options if zone_from_aq(val) in zone_filter]
        if not options:
            return word, False, val
    
    if strategy == 'random':
        new_word = random.choice(options)
    elif strategy == 'lexicographical':
        sorted_opts = sorted(options)
        for o in sorted_opts:
            if o > word.lower():
                new_word = o
                break
        else:
            new_word = sorted_opts[0]  # Wrap around
    elif strategy == 'shortest':
        new_word = min(options, key=len)
    elif strategy == 'longest':
        new_word = max(options, key=len)
    else:
        new_word = random.choice(options)
    
    # Preserve case styling
    if word[0].isupper():
        new_word = new_word.capitalize()
    elif word.isupper():
        new_word = new_word.upper()
    
    return new_word, True, val

def process_text(text, index, mode='all', seed=None, target_word=None, 
                 zone_filter=None, strategy='random'):
    """
    Process text and perform jumps.
    
    mode='all': Jump every word that has a match.
    mode='random': Jump words with 30% probability.
    mode='first': Jump the first match.
    mode='target': Only jump 'target_word'.
    """
    tokens = re.split(r'(\W+)', text)  # Split keeping separators
    result = []
    jump_info = []  # (Original, New, AQ Value, Zone)
    
    first_jumped = False
    for token in tokens:
        # Is it a word?
        if re.match(r'^[a-zA-Z]+$', token):
            should_jump = False
            
            if target_word and token.lower() == target_word.lower():
                should_jump = True
            elif mode == 'all':
                should_jump = True
            elif mode == 'random' and random.random() < 0.3:
                should_jump = True
            elif mode == 'first' and not first_jumped:
                should_jump = True
            
            if should_jump:
                new_w, hit, val = jump_word(token, index, strategy=strategy, 
                                           seed=seed, zone_filter=zone_filter)
                if hit:
                    result.append(new_w)
                    zone = zone_from_aq(val)
                    jump_info.append((token, new_w, val, zone))
                    first_jumped = True
                    continue
            
            result.append(token)
        else:
            result.append(token)
    
    return "".join(result), jump_info

def recursive_jump(text, index, generations=5, mode='random', seed=None, 
                   zone_filter=None, strategy='random', verbose=False):
    """
    Run xeno-jump recursively, feeding output back into itself.
    AQ skeleton preserved across all generations.
    """
    current = text
    all_info = []
    
    for gen in range(generations):
        gen_seed = seed if seed is not None else None
        if seed is not None:
            gen_seed = seed + gen
        
        new_text, jumps = process_text(current, index, mode=mode, seed=gen_seed, 
                                      zone_filter=zone_filter, strategy=strategy)
        all_info.append((gen + 1, current, new_text, jumps))
        
        if verbose:
            z_str = ", ".join(f"{orig}→{new}" for orig, new, _, _ in jumps[:5])
            print(f"  Gen {gen+1}: {z_str}")
        
        current = new_text
    
    return current, all_info

# ═══════════════════════════════════════════
# OUTPUT FORMATTING
# ═══════════════════════════════════════════
def format_output(original, new_text, jump_info, corpus_name, show_zones=False):
    """Format the xeno-jump output."""
    lines = []
    lines.append(f"\u256d\u2500 Xeno-Jump [{corpus_name}]")
    lines.append(f"\u2502 Original: {original}")
    lines.append(f"\u2502 Xeno:     {new_text}")
    bar = '\u2500' * 40
    lines.append(f"╰{bar}")
    
    if jump_info and show_zones:
        lines.append("\nJumps:")
        for orig, new, val, zone in jump_info:
            zname = ZONE_NAMES.get(zone, "??")
            lines.append(f"  {orig} (AQ {val}, Z{zone} {zname}) \u2192 {new}")
    
    return "\n".join(lines)

# ═══════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Xeno-Jump: AQ-Preserving Text Mutation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Corpora:
  general   : Full English dictionary (88K words)
  oracle    : Hyperstitional, arcane, system-native (9.7K words)  
  xenon     : Zone texts, DSP, ML, tracker code (6.6K words)

Examples:
  %(prog)s "The time is now"
  %(prog)s --corpus oracle "The machine speaks"
  %(prog)s --mix oracle:0.7,xenon:0.3 "Void opens"
  %(prog)s --mode all --recursive --generations 5 "Time circuit"
  %(prog)s --zone 4,7 --corpus oracle "Gnostic Calvinism"
        """
    )
    
    parser.add_argument("text", nargs='?', help="Input text or phrase")
    parser.add_argument("--mode", choices=['all', 'random', 'target', 'first'], 
                       default='random', help="Jump mode (default: random)")
    parser.add_argument("--target", type=str, help="Word to target specifically")
    parser.add_argument("--seed", type=int, default=None, help="Random seed")
    parser.add_argument("--corpus", default='general', 
                       help="Corpus to use: general, oracle, xenon (default: general)")
    parser.add_argument("--mix", type=str, 
                       help="Blended corpus spec, e.g. 'oracle:0.7,xenon:0.3'")
    parser.add_argument("--zone", type=str, 
                       help="Restrict jumps to specific zones, e.g. '4,7'")
    parser.add_argument("--recursive", action='store_true', help="Recursive jumping")
    parser.add_argument("--generations", type=int, default=5, 
                       help="Generations for recursive mode")
    parser.add_argument("--verbose", action='store_true', help="Verbose output")
    parser.add_argument("--strategy", default='random',
                       choices=['random', 'lexicographical', 'shortest', 'longest'],
                       help="Word selection strategy")
    parser.add_argument("--zones", action='store_true', dest='show_zones',
                       help="Show zone information in output")
    parser.add_argument("--all-corpora", action='store_true',
                       help="Run through all corpora and show all results")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
    
    args = parser.parse_args()
    
    if not args.text:
        print("Error: Please provide text.")
        sys.exit(1)
    
    # Parse zone filter
    zone_filter = None
    if args.zone:
        try:
            zone_filter = [int(z) for z in args.zone.split(',')]
            if args.verbose:
                print(f"Zone filter: {zone_filter}")
        except ValueError:
            print(f"Error: Invalid zone spec: {args.zone}")
            sys.exit(1)
    
    # --all-corpora mode
    if args.all_corpora:
        for corp in ['general', 'oracle', 'xenon']:
            try:
                idx = load_corpus(corp)
                if args.recursive:
                    final, all_info = recursive_jump(args.text, idx, 
                        generations=args.generations, mode=args.mode, seed=args.seed,
                        zone_filter=zone_filter, strategy=args.strategy, verbose=args.verbose)
                    print(format_output(args.text, final, all_info[-1][3], corp, 
                                       show_zones=args.show_zones))
                else:
                    result_text, result_jumps = process_text(args.text, idx, mode=args.mode,
                        seed=args.seed, zone_filter=zone_filter, strategy=args.strategy)
                    print(format_output(args.text, result_text, result_jumps, corp, 
                                       show_zones=args.show_zones))
                print()
            except Exception as e:
                print(f"[{corp}] Error: {e}")
        sys.exit(0)
    
    # Determine corpus spec
    corp_spec = args.mix if args.mix else args.corpus
    
    try:
        index = load_corpus_or_blend(corp_spec)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    # Show what corpus we're using
    total_words = sum(len(v) for v in index.values())
    num_buckets = len(index)
    
    # Track output for verbose zone distribution
    result_text = ""
    result_jumps = []
    
    if args.recursive:
        result_text, all_info = recursive_jump(args.text, index, 
            generations=args.generations, mode=args.mode, seed=args.seed,
            zone_filter=zone_filter, strategy=args.strategy, verbose=args.verbose)
        result_jumps = all_info[-1][3]
        print(format_output(args.text, result_text, result_jumps, 
                           corp_spec, show_zones=args.show_zones))
    else:
        result_text, result_jumps = process_text(args.text, index, mode=args.mode,
            seed=args.seed, zone_filter=zone_filter, strategy=args.strategy)
        print(format_output(args.text, result_text, result_jumps, corp_spec, 
                           show_zones=args.show_zones))
    
    if args.verbose:
        print(f"\nCorpus: {corp_spec}")
        print(f"  {num_buckets} AQ buckets, {total_words} entries")
        if result_jumps:
            zone_counts = defaultdict(int)
            for _, _, _, z in result_jumps:
                zone_counts[z] += 1
            print(f"  Zone distribution: ", end="")
            for z in range(1, 10):
                if zone_counts[z]:
                    print(f"Z{z}={zone_counts[z]} ", end="")
            print()
