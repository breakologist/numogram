"""
Seed Transforms — Gysin/Burroughs-style text permutation engine.

Four methods to mutate text through the numogram's arithmetic:

  1. FIXED AQ CHAIN  — Jump words in a sentence, AQ checksum never changes.
                      The vocabulary drifts but the numerical skeleton holds.
  2. TRIANGULAR DRIFT — Seed word's zone follows T(n) mod 9 sequence.
                       The triangular orbit: 1, 3, 6, 1, 6, 3, 1, 3, 6...
  3. SYZYGY WALK     — Each step jumps to the syzygy partner zone.
                       Oscillates: Z2 <-> Z7 <-> Z2 <-> Z7...
  4. ENTROPY WALK    — Hardware random noise shifts the AQ up/down.
                       Entropy drives the mutation; nothing is preserved.

Each method can run in two modes:
  - phrase: operates on an entire sentence
  - word: operates on a single seed word (the AQ seed itself transforms)

Usage:
    python seed_transforms.py                          # Demo with defaults
    python seed_transforms.py "your source text"        # Your phrase
    python seed_transforms.py --method fixed --steps 12
    python seed_transforms.py --mode word --seed Katak
    python seed_transforms.py --enriched               # Use enriched index
    python seed_transforms.py --beat Katak Pandemonium Xenotation
"""

import os
import sys
import json
import random
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from xeno_jump import load_index as load_xeno, process_text, get_aq, digital_root
import cut_up

# ═══════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════

ARROW = chr(8594)   # →
CHECK = chr(10003)  # ✓
CROSS = chr(10060)  # ❌
EM = chr(8212)      # —
LINE = chr(9472) * 64  # ────────────────────────────────────────────────────────────────

def zone(n):
    if n <= 0: return 9
    return (n - 1) % 9 + 1

def syzygy(z):
    """Return the syzygy partner of a zone."""
    s = 9 - z
    return 9 if s == 0 else s

def triangular(n):
    return n * (n + 1) // 2

def nearest_aq(target, index_dict, rng):
    """Find nearest AQ value with available words."""
    for delta in range(50):
        for d in (0, -1, 1, -2, 2, -3, 3, 4, -4, 5, -5):
            k = target + d
            if k in index_dict and index_dict[k]:
                return rng.choice(index_dict[k]), k
        target += rng.choice([-1, 1])
    return "---", target

def words_for_zone(target_zone, index_dict, rng):
    """Return a random word whose zone matches target_zone."""
    candidates = []
    for aq, words in index_dict.items():
        if zone(aq) == target_zone:
            candidates.extend(words)
    return rng.choice(candidates) if candidates else "---"

# ═══════════════════════════════════════════
# LOADER
# ═══════════════════════════════════════════

def load(enriched=False):
    if enriched:
        path = SCRIPT_DIR / "aq_corpus_enriched.json"
    else:
        path = SCRIPT_DIR / "aq_corpus_index.json"
    with open(path) as f:
        return {int(k): v for k, v in json.load(f).items()}

class MockIndex:
    def __init__(self, data): self.data = data
    def get(self, k, d=None): return self.data.get(k, d)

# ═══════════════════════════════════════════
# THE FOUR ENGINES
# ═══════════════════════════════════════════

def fixed_chain(source, index, steps=10, seed=666):
    """METHOD 1: Fixed AQ chain.
    Each step jumps words in the sentence. AQ checksum never changes."""
    idx = MockIndex(index)
    base_aq = get_aq(source)
    print()
    print(LINE)
    print("  METHOD 1: FIXED AQ CHAIN")
    print("  Source:", source)
    print("  AQ=%d  DR=%d  Z%d  [immutable]" % (base_aq, zone(base_aq), zone(base_aq)))
    print(LINE)

    current = source
    for step in range(1, steps + 1):
        result, jumps = process_text(current, idx, mode='all',
                                      seed=seed + step * 37)
        chk = get_aq(result)
        mark = CHECK if chk == base_aq else CROSS
        print("  [%3d] %s %s" % (step, mark, result))
        current = result

def triangular_drift(word, index, steps=10, seed=42):
    """METHOD 2: Triangular drift.
    Seed word zone follows T(n) mod 9: {1, 3, 6, 1, 6, 3, 1, 3, 6...}"""
    rng = random.Random(seed)
    t_n = triangular(seed)
    t_dr = zone(t_n)

    print()
    print(LINE)
    print("  METHOD 2: TRIANGULAR DRIFT")
    print("  Seed:", word, "  AQ=%d  DR=%d  Z%d" % (get_aq(word), zone(get_aq(word)), zone(get_aq(word))))
    print("  Triangular orbit: T(n) mod 9 =", t_dr)
    print(LINE)
    print("  T(n) sequence: 1, 3, 6, 10(1), 15(6), 21(3), 28(1)...")
    print("  Zone cycle:    1->3->6->1->6->3->1->3->6...")
    print()

    for step in range(1, steps + 1):
        t_raw = triangular(step)
        target_dr = zone(t_raw)
        candidates = []
        for aq, words in index.items():
            if zone(aq) == target_dr:
                candidates.extend(words)
        chosen = rng.choice(candidates) if candidates else "---"
        chosen_aq = get_aq(chosen)
        print("  [%3d] T(%d)=%3d %s Z%d: %s %s %s  (AQ=%d, DR=%d)" % (
            step, step, t_raw, ARROW, target_dr, word, ARROW, chosen, chosen_aq, zone(chosen_aq)))
        word = chosen  # feed forward

def syzygy_walk(word, index, steps=10, seed=42):
    """METHOD 3: Syzygy oscillation.
    Each step jumps to the syzygy partner of the current zone."""
    rng = random.Random(seed)
    start_dr = zone(get_aq(word))
    current_zone = start_dr

    print()
    print(LINE)
    print("  METHOD 3: SYZYGY WALK")
    print("  Seed:", word, "  initial Z%d, syzygy partner Z%d" % (start_dr, syzygy(start_dr)))
    print(LINE)
    print()

    for step in range(1, steps + 1):
        target = syzygy(current_zone)
        candidates = []
        for aq, words in index.items():
            if zone(aq) == target:
                candidates.extend(words)
        chosen = rng.choice(candidates) if candidates else "---"
        chosen_aq = get_aq(chosen)
        print("  [%3d] Z%d %s Z%d: %s %s %s  (AQ=%d, DR=%d)" % (
            step, current_zone, ARROW, target, word, ARROW, chosen, chosen_aq, zone(chosen_aq)))
        word = chosen
        current_zone = target  # will flip back next step

def entropy_walk(word, index, steps=10, seed=42):
    """METHOD 4: Entropy random walk.
    Hardware urandom shifts the AQ by [-100, +100] each step."""
    rng = random.Random(seed)
    current_aq = get_aq(word)

    print()
    print(LINE)
    print("  METHOD 4: ENTROPY WALK")
    print("  Seed:", word, "  AQ=%d  DR=%d  Z%d" % (current_aq, zone(current_aq), zone(current_aq)))
    print("  Entropy range: AQ +/-100 each step (os.urandom)")
    print(LINE)
    print()

    for step in range(1, steps + 1):
        # Hardware entropy
        try:
            raw = int.from_bytes(os.urandom(4), 'big')
        except:
            raw = rng.randint(0, 2**32)
        ent = (raw % 201) - 100  # -100 to +100
        new_aq = max(30, min(666, current_aq + ent))

        chosen, best_aq = nearest_aq(new_aq, index, rng)
        if chosen == "---":
            best_aq = new_aq

        chosen_aq = get_aq(chosen) if chosen != "---" else best_aq
        dr_val = zone(chosen_aq) if chosen != "---" else zone(best_aq)

        print("  [%3d] AQ %d %+4d %s %d (Z%d): %s %s %s" % (
            step, current_aq, ent, ARROW, best_aq, dr_val, word, ARROW, chosen))
        current_aq = best_aq
        word = chosen

# ═══════════════════════════════════════════
# PHRASE JUMP (single-word chain through a sentence)
# ═══════════════════════════════════════════

def phrase_jump(source, index, steps=10, seed=666):
    """Jump exactly one word per step. The sentence mutates slowly.
    AQ checksum drifts (one word changes at a time)."""
    idx = MockIndex(index)
    print()
    print(LINE)
    print("  PHRASE JUMP - one word per step")
    print(LINE)
    print("  [%3d]   %s" % (0, source))

    current = source
    base_aq = get_aq(source)
    for step in range(1, steps + 1):
        result, jumps = process_text(current, idx, mode='first',
                                     seed=seed + step * 43)
        if jumps:
            orig, new, aq, z = jumps[0]
            drift = get_aq(result) - base_aq
            print("  [%3d] %s %s %s  (AQ drift: %+4d)  %s" % (
                step, orig, ARROW, new, drift, result))
        else:
            print("  [%3d] (no jump)  %s" % (step, result))
        current = result

# ═══════════════════════════════════════════
# BEAT POEM COMPOSER
# ═══════════════════════════════════════════

def beat_poem(seeds, index, lines=8, seed=666):
    """Compose a beat poem from AQ-preserved seed chains."""
    em_dash = EM
    print()
    print(LINE)
    print("  BEAT POEM - %d voice chains" % len(seeds))
    parts = []
    for s in seeds:
        parts.append("%s: AQ=%d" % (s, get_aq(s)))
    print("  AQ values: %s" % ' | '.join(parts))
    print(LINE)
    print()

    # Build chains: each seed word walks its AQ bucket
    rng = random.Random(seed)
    chains = {}
    for s in seeds:
        aq = get_aq(s)
        bucket = index.get(aq, [s])
        pool = [w for w in bucket if w.lower() != s.lower()] or bucket
        chain = [s]
        for i in range(lines):
            chain.append(rng.choice(pool))
        chains[s] = chain

    for i in range(lines):
        # Get words for this line, cycling through chains
        words = [chains[s][i % len(chains[s])] for s in seeds]
        
        if len(seeds) == 1:
            # Single chain: just print the word on each line
            print("  %s" % words[0])
        else:
            pattern = i % 3
            if pattern == 0:
                print("  %s" % words[0])
            elif pattern == 1:
                print("  the %s of %s %s" % (words[1].lower(), words[0], words[-1].lower()))
            else:
                middle = (" %s " % em_dash).join(words[1:])
                print("  %s %s %s" % (words[0], em_dash, middle))
    print()

# ═══════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Seed Transforms engine")
    parser.add_argument("text", nargs='?',
                       default="The demon Katak carries the Warp current through the outer zones",
                       help="Source text or single word")
    parser.add_argument("--mode", choices=['phrase', 'word'], default='phrase',
                       help="phrase=full sentence, word=seed word only")
    parser.add_argument("--steps", type=int, default=10)
    parser.add_argument("--method",
                       choices=['fixed', 'triangular', 'syzygy', 'entropy', 'all'],
                       default='all')
    parser.add_argument("--enriched", action='store_true',
                       help="Use the enriched hyperstition index")
    parser.add_argument("--beat", type=str, nargs='+',
                       help="Words for beat poem composer")
    parser.add_argument("--seed", type=int, default=666)

    args = parser.parse_args()
    index = load(enriched=args.enriched)

    if args.beat:
        beat_poem(args.beat, index, seed=args.seed)
        sys.exit(0)

    if args.method == 'fixed':
        fixed_chain(args.text, index, args.steps, args.seed)
    elif args.method == 'triangular':
        triangular_drift(args.text, index, args.steps, args.seed)
    elif args.method == 'syzygy':
        syzygy_walk(args.text, index, args.steps, args.seed)
    elif args.method == 'entropy':
        entropy_walk(args.text, index, args.steps, args.seed)
    elif args.method == 'all':
        if args.mode == 'word':
            word = args.text.split()[0]
            triangular_drift(word, index, args.steps, args.seed)
            syzygy_walk(word, index, args.steps, args.seed)
            entropy_walk(word, index, args.steps, args.seed)
        else:
            # Phrase mode: fixed chain + phrase jump
            fixed_chain(args.text, index, args.steps, args.seed)
            phrase_jump(args.text, index, args.steps, args.seed)
