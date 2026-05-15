#!/usr/bin/env python3
"""
text_pipeline.py -- Two-stage recombination pipeline
  Stage 1: Xeno-Jump (AQ-preserving mutation through corpus)  [corpus]
  Stage 2: Zone Cut-Up (fragment & reassemble jumped text)   [cut]

Usage:
  python3 text_pipeline.py "The machine speaks from the abyss" --corpus oracle --zones 0,6,9
  python3 text_pipeline.py --all --zones 3,6,9 --generations 7
"""

import os, re, random, sys, json


# ═══════════════════════════════════════════
# AQ MATH (same as xeno_jump.py)
# ═══════════════════════════════════════════
def get_aq(word):
    return sum(ord(c.upper()) - 55 for c in word if c.isalpha())

def digital_root(n):
    if n == 0:
        return 0
    return (n - 1) % 9 + 1

# ═══════════════════════════════════════════
# CORPUS INDEX LOADING
# ═══════════════════════════════════════════
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CORPUS_FILES = {
    'oracle': os.path.join(SCRIPT_DIR, 'aq_corpus_oracle.json'),
    'xenon': os.path.join(SCRIPT_DIR, 'aq_corpus_xenon.json'),
    'general': os.path.join(SCRIPT_DIR, 'aq_corpus_index.json'),
}

def load_index(name='oracle'):
    path = CORPUS_FILES.get(name, CORPUS_FILES['oracle'])
    with open(path) as f:
        data = json.load(f)
    # Normalize keys to int
    return {int(k): v for k, v in data.items()}

# ═══════════════════════════════════════════
# STAGE 1: XENO-JUMP
# ═══════════════════════════════════════════
def xeno_jump_single(text, idx, strategy='longest'):
    """Jump one word in text to same-AQ alternative."""
    tokens = re.findall(r"[a-zA-Z]+|[^a-zA-Z]+", text)
    if not tokens:
        return False, text

    # Get all alpha token positions
    alpha_positions = [(i, t) for i, t in enumerate(tokens) if t.isalpha()]
    if not alpha_positions:
        return False, text

    # Score by strategy
    if strategy == 'longest':
        scored = sorted(alpha_positions, key=lambda x: len(x[1]), reverse=True)
    elif strategy == 'shortest':
        scored = sorted(alpha_positions, key=lambda x: len(x[1]))
    else:  # random
        random.shuffle(alpha_positions)
        scored = alpha_positions

    for pos, word in scored:
        clean = word.lower()
        val = get_aq(word)
        if val <= 0 or val not in idx:
            continue
        pool = [w for w in idx[val] if w.lower() != clean]
        if pool:
            replacement = random.choice(pool)
            if word[0].isupper():
                replacement = replacement.capitalize()
            if word.isupper() and len(word) > 1:
                replacement = replacement.upper()
            tokens[pos] = replacement
            return True, ''.join(tokens)

    return False, text

def xeno_jump_recursive(seed, corpus='oracle', generations=5, strategy='longest'):
    idx = load_index(corpus)
    history = [seed]
    current = seed
    for gen in range(generations):
        changed, jumped = xeno_jump_single(current, idx, strategy)
        if not changed:
            break  # Fixed point
        current = jumped
        history.append(current)
    return history

# ═══════════════════════════════════════════
# STAGE 2: ZONE CUT-UP (inline from cut_up.py)
# ═══════════════════════════════════════════
ZONES = {
    0: {"name": "Void",    "cut": 0.90, "mode": "word",        "sep": "\n",    "prefix": "\u00b7 ",  "xen": True,  "xmode": "heavy"},
    1: {"name": "Surge",    "cut": 0.50, "mode": "phrase",      "sep": " ",     "rec": True,  "rs": "echo"},
    2: {"name": "Separation","cut": 0.60, "mode": "clause",     "sep": " / ",   "rec": True,  "rs": "bridge"},
    3: {"name": "Warp",     "cut": 0.40, "mode": "mid-sentence","sep": " \u2192 ","rec": True,   "rs": "splice", "xen": True, "xmode": "verb"},
    4: {"name": "Gate",     "cut": 0.55, "mode": "sentence",    "sep": ""},
    5: {"name": "Pressure", "cut": 0.35, "mode": "paragraph",   "sep": "\n\n"},
    6: {"name": "Abstraction","cut": 0.45, "mode": "term",      "sep": " :: ",  "xen": True,  "xmode": "heavy"},
    7: {"name": "Blood",    "cut": 0.50, "mode": "phrase",      "sep": " "},
    8: {"name": "Multiplicity","cut": 0.20, "mode": "keep",     "sep": "\n", "rec": True,   "rs": "duplicate"},
    9: {"name": "Plex",     "cut": 0.10, "mode": "recursive",   "sep": " ",     "rec": True,  "rs": "palindrome", "xen": True, "xmode": "total"},
}

def fragment(text, mode):
    if mode == "word":
        return text.split()
    elif mode == "phrase":
        return [p.strip() for p in re.split(r"(?<=[,;\u2014\u2013-])\s+", text) if p.strip()]
    elif mode == "mid-sentence":
        parts = re.split(r"(?<=[ ,])", text)
        return parts[::2]
    elif mode == "clause":
        return [s.strip() for s in re.split(r"(?<=[.!?])\s*", text) if len(s.strip()) > 10]
    elif mode == "term":
        return re.findall(r"\b[A-Z][a-zA-Z]{3,}\b|\b[a-z]{4,}\b", text)
    elif mode == "sentence":
        return [s.strip() for s in re.split(r"(?<=[.!??:])\s+", text) if len(s.strip()) > 10]
    elif mode == "paragraph":
        return [p.strip() for p in text.split("\n\n") if p.strip()]
    return text.split()

def cut_fragment(frags, ratio=0.50):
    keep = max(1, int(len(frags) * (1.0 - ratio)))
    random.shuffle(frags)
    return frags[:keep]

def xenotate_simple(word, mode="sparse"):
    if mode == "verb":
        return "\u221e " + word + " \u00b9"
    elif mode == "heavy":
        return "\u221e " + word + " \u221e"
    elif mode == "total":
        return "\u221e" + word + "\u221e"
    return "\u221e " + word

def recombine(frags, style="echo"):
    if style == "echo":
        out = []
        for f in frags:
            out.append(f)
            out.append(f + "\u2014")
        return out
    elif style == "splice":
        out = []
        for i in range(0, len(frags) - 1, 2):
            if i + 1 < len(frags):
                a, b = frags[i], frags[i+1]
                mid = len(a) // 2
                sp = mid
                for j in range(mid, len(a)):
                    if a[j] in ",; ":
                        sp = j
                        break
                out.append(a[:sp] + b[sp:])
            else:
                out.append(frags[i])
        return out
    elif style == "bridge":
        return [" / ".join(frags[i:i+2]) for i in range(0, len(frags), 2)]
    elif style == "palindrome":
        front = frags[:len(frags) // 2]
        back = frags[len(frags) // 2:]
        return front + back[::-1]
    elif style == "duplicate":
        out = []
        for f in frags:
            out.append(f)
            out.append(f)
        return out
    return frags

def cut_zone(text, zone, length=30, seed=666):
    random.seed(seed)
    z = ZONES[zone]
    frags = fragment(text, z["mode"])
    frags = cut_fragment(frags, z["cut"])
    if z.get("rec"):
        frags = recombine(frags, z.get("rs", "echo"))
    if z.get("xen"):
        frags = [xenotate_simple(f, z.get("xmode", "sparse")) for f in frags]
    prefix = z.get("prefix", "")
    frags = [prefix + f for f in frags]
    frags = frags[:length]
    return z["sep"].join(frags)

# ═══════════════════════════════════════════
# PIPELINE
# ═══════════════════════════════════════════
def run_pipeline(seed_text, corpus='oracle', zones=None, strategy='longest',
                 generations=5, length=30, cut_seed=666):
    if zones is None:
        zones = [0, 6, 9]

    sep = "\u2501" * 60
    print(f"\n\u250f{sep}")
    print(f"\u2503  SEED: {seed_text}")
    print(f"\u2503  CORPUS: {corpus}  STRATEGY: {strategy}  GENS: {generations}")
    print(f"\u2517{sep}")

    # Stage 1: Recursive xeno-jump
    history = xeno_jump_recursive(seed_text, corpus, generations, strategy)
    final = history[-1]

    if len(history) > 1:
        print(f"\n  STAGE 1: RECURSIVE XENO-JUMP ({corpus})")
        for i, text in enumerate(history[:-1]):
            print(f"    [{i}] {text}")
        print(f"    [{len(history)-1}] \u2192 {final}")
    else:
        print(f"\n  STAGE 1: XENO-JUMP  \u2192 fixed point (no change)")
        print(f"    {final}")

    # Stage 2: Cut-up through zones
    print(f"\n  STAGE 2: ZONE CUT-UP OF JUMPED TEXT")
    print(f"  \u2500" * 30)
    for z in zones:
        zname = ZONES[z]["name"].upper()
        result = cut_zone(final, z, length, cut_seed)
        print(f"    ZONE {z} [{zname}]:")
        print(f"    {result}")
        print()

    return final

def run_multi_corpora(seed_text, zones=None, strategy='longest',
                      generations=5, length=30, cut_seed=666):
    double_line = "\u2550" * 60
    for corpus in ['general', 'oracle', 'xenon']:
        run_pipeline(seed_text, corpus, zones, strategy,
                     generations, length, cut_seed)
        print(f"\n{double_line}\n")


# ═══════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════
if __name__ == '__main__':
    import argparse

    p = argparse.ArgumentParser(description="Two-stage text recombination pipeline")
    p.add_argument("seed", nargs="?", default="The machine speaks from the void",
                   help="Seed text to mutate")
    p.add_argument("--corpus", choices=['general', 'oracle', 'xenon', 'all'],
                   default='oracle', help="Corpus for xeno-jump")
    p.add_argument("--zones", default="0,6,9",
                   help="Zones for cut-up (comma-separated)")
    p.add_argument("--strategy", choices=['longest', 'shortest', 'random'],
                   default='longest', help="Jump strategy")
    p.add_argument("--generations", type=int, default=5,
                   help="Number of recursive generations")
    p.add_argument("--length", type=int, default=30,
                   help="Cut-up output length")
    p.add_argument("--seed-rand", type=int, default=666,
                   help="Random seed for cut-up")
    args = p.parse_args()

    zones = [int(z) for z in args.zones.split(",") if z.strip().isdigit()]

    if args.corpus == 'all':
        double_sep = "\u2550" * 60
        run_multi_corpora(args.seed, zones, args.strategy,
                          args.generations, args.length, args.seed_rand)
        print(f"\n{double_sep}\n")

    else:
        run_pipeline(args.seed, args.corpus, zones, args.strategy,
                     args.generations, args.length, args.seed_rand)
