"""
corpus_sweep.py — Fresh recursive xeno-jump runner for the three-corpus system.

Inspired by run_recursive_jumps.py but rebuilt for the v2 pipeline:
  - xeno_jump.py (v2): load_corpus, process_text, recursive_jump
  - cut_up.py: zone-profiled fragmentation
  - Three corpora: general / oracle / xenon
  - Non-666 seed, oracle-native source texts

Produces output files:
  1. 01_fixed_chain.txt       AQ-preserving sentence cascade
  2. 02_phrase_jump.txt       One-word drift per generation
  3. 03_triangular.txt        Triangular zone walk from seed words
  4. 04_syzygy.txt            Syzygy zone oscillation from seed words
  5. 05_beat_poem.txt         AQ-chain beat poetry
  6. 06_three_currents.txt    Same seeds through oracle / xenon / general
  7. 07_zone_cutup.txt        Zone-profiled cut-up from jumped text

Usage:
  python3 corpus_sweep.py [--corpus oracle] [--steps 69] [--seed 937]
"""

import os
import sys
import json
import random
import datetime
import argparse

sys.path.insert(0, os.path.dirname(__file__))
from xeno_jump import (
    load_corpus, process_text, get_aq, digital_root,
    zone_from_aq, ZONE_NAMES, recursive_jump
)
import cut_up

# ═══════════════════════════════════════════
# ARGUMENTS
# ═══════════════════════════════════════════
parser = argparse.ArgumentParser(description="Corpus sweep: recursive xeno-jump across three currents")
parser.add_argument("--corpus", choices=["oracle", "xenon", "general"], default="oracle",
                    help="Corpus to use (default: oracle)")
parser.add_argument("--steps", type=int, default=69, help="Chain length (default: 69)")
parser.add_argument("--seed", type=int, default=937, help="Random seed (default: 937)")
parser.add_argument("--output", default="/tmp/corpus-sweep", help="Output directory")
args = parser.parse_args()

OUTPUT_DIR = args.output
os.makedirs(OUTPUT_DIR, exist_ok=True)

STEPS = args.steps
SEED = args.seed
CORPUS = args.corpus

# ═══════════════════════════════════════════
# SOURCE MATERIAL — oracle-native phrases
# ═══════════════════════════════════════════

# Sentences that carry numogram / CCRU / Gnostic material
SOURCE_SENTENCES = [
    "The cryptolith opens the decimator gate",
    "hyperstition flows through the triangular syzygy",
    "Katak and Oddubb coil the plex",
    "teleoplexy accelerates the void circuit",
    "the demon uttunul whispers from the djynxxagram",
    "paramita conducts dissolve the qliphoth veil",
    "numogrammic recursion spirals zone nine",
    "entropy garden seeded with hardware random",
    "beat poetry through the abecedarium chain",
    "what the Tathagata preached as merit was no-stock of merit",
    "I am the silence that is incomprehensible and the voice whose sound is manifold",
    "wherever there is the possession of signs there is falsehood",
    "a Bodhisattva should give gifts unsupported by the idea of a sign",
    "the stock of merit of the one who gives unsupported is not easy to measure",
]

# Seed words for triangle/syzygy walks
SEED_WORDS = [
    "Xenotation", "Pandemonium", "Katak", "Djynxx", "Nullotation",
    "Cryptolith", "Teleoplexy", "Paramita", "Qliphoth", "Hyperstition",
    "Syzygy", "Void", "Plex", "Warp", "Decimator", "Xenocosmography",
    "Tathagata", "Nirvana", "Bodhisattva", "Manifold", "Incomprehensible",
]

# Beat poem AQ anchors
BEAT_WORDS = ["Cryptolith", "Teleoplexy", "Paramita", "Syzygy", "Void"]

# ═══════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════

def zone(n):
    """Digital root with 1-9 mapping (0 → 9)."""
    if n <= 0:
        return 9
    return (n - 1) % 9 + 1

def triangular(n):
    return n * (n + 1) // 2

def syzygy(z):
    s = 9 - z
    return 9 if s == 0 else s

def save_file(filename, content):
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    size = os.path.getsize(path)
    print(f"  {filename:<35s} {size:>8,} bytes")

# Load indices with graceful handling of missing corpora
def safe_load_corpus(name):
    try:
        return load_corpus(name)
    except (FileNotFoundError, OSError) as e:
        print(f"  Warning: Corpus '{name}' not loaded ({e})")
        return {}

idx = safe_load_corpus(CORPUS)
oracle_idx = safe_load_corpus('oracle')
xenon_idx = safe_load_corpus('xenon')
general_idx = safe_load_corpus('general')

# Fallback: if primary corpus is empty, use any loaded corpus
for label, loaded in [('oracle', oracle_idx), ('xenon', xenon_idx), ('general', general_idx)]:
    if loaded:
        _FALLBACK = loaded
        break
else:
    print("FATAL: No corpora available!")
    sys.exit(1)

# If primary corpus is empty, fall back
if not idx:
    print(f"  Primary corpus '{CORPUS}' not available, falling back to next available")
    idx = _FALLBACK

total_entries = sum(len(v) for v in idx.values())
total_buckets = len(idx)

timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
SEP = "\u2550" * 72
DIV = "\u2500" * 72
ARROW = "\u2192"

print(f"\nCorpus Sweep — {CORPUS}")
print(f"  Steps: {STEPS}  Seed: {SEED}  Time: {timestamp}")
print(f"  Buckets: {total_buckets:,}  Entries: {total_entries:,}")
print(f"  Output: {OUTPUT_DIR}\n")

# ═══════════════════════════════════════════
# 1. FIXED AQ CHAIN
# ═══════════════════════════════════════════

lines = [
    f"FIXED AQ CHAIN \u2014 {CORPUS} ({timestamp})",
    SEP,
    f"AQ checksum never changes. Vocabulary cascades.",
    f"Corpus: {CORPUS} ({total_buckets:,} buckets, {total_entries:,} entries)",
    f"Engine: xeno_jump v2, all-word mode, seed {SEED}",
    "",
]

for src in SOURCE_SENTENCES:
    base_aq = get_aq(src)
    lines.append(f"\n{DIV}")
    lines.append(f"SOURCE (AQ={base_aq}, Z{zone(base_aq)}): {src}")
    lines.append(DIV)

    current = src
    for step in range(1, STEPS + 1):
        result, jumps = process_text(current, idx, mode='all', seed=SEED + step * 37)
        chk = get_aq(result)
        mark = "\u2713" if chk == base_aq else "\u2717"
        # Show first 5, then skip to last 3
        if step <= 5 or step >= STEPS - 2:
            lines.append(f"  [{step:3d}] {mark} {result}")
        elif step == 6:
            lines.append(f"  ... ({STEPS - 7} intermediate steps) ...")
        current = result

    lines.append("")

save_file('01_fixed_chain.txt', '\n'.join(lines))

# ═══════════════════════════════════════════
# 2. PHRASE JUMP — one word per step
# ═══════════════════════════════════════════

lines = [
    f"PHRASE JUMP \u2014 One-Word Mutation ({timestamp})",
    SEP,
    f"Exactly one word jumps per generation. AQ checksum intact, vocabulary drifts.",
    f"Corpus: {CORPUS} | Mode: first-match | Seed {SEED}",
    "",
]

for src in SOURCE_SENTENCES:
    base_aq = get_aq(src)
    current = src
    stuck = False

    lines.append(f"\n{DIV}")
    lines.append(f"SOURCE (AQ={base_aq}, Z{zone(base_aq)}): {src}")
    lines.append(DIV)
    lines.append(f"  [  0]   {src}")

    for step in range(1, STEPS + 1):
        if stuck:
            lines.append(f"  [{step:3d}] (stable \u2014 no mutable words remain)")
            break
        result, jumps = process_text(current, idx, mode='first', seed=SEED + step * 43)
        if jumps:
            orig, new, aq, z = jumps[0]
            lines.append(f"  [{step:3d}] {orig} {ARROW} {new}  \u2014  {result}")
            current = result
        else:
            stuck = True
            lines.append(f"  [{step:3d}] (stable \u2014 {current})")

    lines.append("")

save_file('02_phrase_jump.txt', '\n'.join(lines))

# ═══════════════════════════════════════════
# 3. TRIANGULAR ZONE WALK
# ═══════════════════════════════════════════

lines = [
    f"TRIANGULAR ZONE WALK ({timestamp})",
    SEP,
    f"Seed word zone follows T(n) mod 9: 1 {ARROW} 3 {ARROW} 6 {ARROW} 1 {ARROW} 6 {ARROW} 3 \u2026",
    f"Corpus: {CORPUS} | Engine: zone-targeted selection, seed {SEED}",
    "",
]

for word in SEED_WORDS:
    start_aq = get_aq(word)
    lines.append(f"\n{DIV}")
    lines.append(f"SEED: {word} (AQ={start_aq}, Z{zone(start_aq)})")
    lines.append(DIV)

    current = word
    for step in range(1, STEPS + 1):
        t_raw = triangular(step)
        target_dr = zone(t_raw)

        candidates = []
        for aq_val, words in idx.items():
            if zone(aq_val) == target_dr:
                candidates.extend(words)

        chosen = random.Random(SEED * 1000 + step * 37).choice(candidates) if candidates else "..."
        chosen_aq = get_aq(chosen)
        lines.append(
            f"  [{step:3d}] T({step})={t_raw:3d} {ARROW} Z{target_dr}: "
            f"{current} {ARROW} {chosen}  (AQ={chosen_aq}, Z{zone(chosen_aq)})"
        )
        current = chosen

    lines.append("")

save_file('03_triangular.txt', '\n'.join(lines))

# ═══════════════════════════════════════════
# 4. SYZYG Y OSCILLATION
# ═══════════════════════════════════════════

lines = [
    f"SYZYG Y ZONE OSCILLATION ({timestamp})",
    SEP,
    f"Each step jumps to the syzygy partner zone: Z(n) {ARROW} Z(9-n) {ARROW} Z(n) \u2026",
    f"Corpus: {CORPUS} | Engine: zone-targeted selection, seed {SEED}",
    "",
]

for word in SEED_WORDS:
    start_aq = get_aq(word)
    start_z = zone(start_aq)
    lines.append(f"\n{DIV}")
    lines.append(f"SEED: {word} (Z{start_z}, syzygy partner Z{syzygy(start_z)})")
    lines.append(DIV)

    current = word
    current_z = start_z
    for step in range(1, STEPS + 1):
        target_z = syzygy(current_z)

        candidates = []
        for aq_val, words in idx.items():
            if zone(aq_val) == target_z:
                candidates.extend(words)

        chosen = random.Random(SEED * 2000 + step * 37).choice(candidates) if candidates else "..."
        chosen_aq = get_aq(chosen)
        lines.append(
            f"  [{step:3d}] Z{current_z} {ARROW} Z{target_z}: "
            f"{current} {ARROW} {chosen}  (AQ={chosen_aq}, Z{zone(chosen_aq)})"
        )
        current = chosen
        current_z = target_z

    lines.append("")

save_file('04_syzygy.txt', '\n'.join(lines))

# ═══════════════════════════════════════════
# 5. BEAT POEM
# ═══════════════════════════════════════════

lines = [
    f"BEAT POEM \u2014 AQ-Preserved Seed Chains ({timestamp})",
    SEP,
    f"Each seed word chains through its AQ bucket.",
    f"Corpus: {CORPUS} | Seeds: {', '.join(BEAT_WORDS)}",
    "",
]

rng = random.Random(SEED)
chains = {}
for s in BEAT_WORDS:
    aq = get_aq(s)
    bucket = idx.get(aq, [s])
    pool = [w for w in bucket if w.lower() != s.lower()] or bucket
    chain = [s]
    for _ in range(STEPS):
        chain.append(rng.choice(pool))
    chains[s] = chain

for seed_word, chain in chains.items():
    aq = get_aq(seed_word)
    lines.append(f"\n{DIV}")
    lines.append(f"CHAIN: {seed_word} (AQ={aq}, Z{zone(aq)})")
    lines.append(DIV)
    lines.append("  " + " \u2192 ".join(chain[:STEPS + 1]))
    lines.append("")

# Compose verse
lines.append(f"\n{DIV}")
lines.append("COMPOSED VERSE")
lines.append(DIV)

em_dash = "\u27e1"  # small diamond
for i in range(STEPS):
    w = [chains[bw][i % len(chains[bw])] for bw in BEAT_WORDS]
    pattern = i % 5
    if pattern == 0:
        lines.append(f"  {w[0]}")
    elif pattern == 1:
        lines.append(f"  the {w[1].lower()} of {w[0]} {w[2].lower()}")
    elif pattern == 2:
        lines.append(f"  {w[0]} {em_dash} {w[1]} {em_dash} {w[2]}")
    elif pattern == 3:
        lines.append(f"  {w[3]} {w[4]} {w[1].lower()}")
    else:
        lines.append(f"  {' '.join(w)}")

lines.append("")
save_file('05_beat_poem.txt', '\n'.join(lines))

# ═══════════════════════════════════════════
# 6. THREE CURRENTS — oracle / xenon / general
# ═══════════════════════════════════════════

lines = [
    f"THREE CURRENTS \u2014 oracle \u2014 xenon \u2014 general ({timestamp})",
    SEP,
    f"Same seed through all three corpora. The AQ skeleton is identical; the vocabulary diverges.",
    f"Oracle: {sum(len(v) for v in oracle_idx.values()):,} words",
    f"Xenon:  {sum(len(v) for v in xenon_idx.values()):,} words",
    f"General: {sum(len(v) for v in general_idx.values()):,} words",
    "",
]

for src in SOURCE_SENTENCES:
    lines.append(f"\n{DIV}")
    lines.append(f"SOURCE: {src}  (AQ={get_aq(src)}, Z{zone(get_aq(src))})")
    lines.append(DIV)

    co = cx = cg = src
    for step in range(1, 13):
        ro, _ = process_text(co, oracle_idx, mode='all', seed=SEED + step * 37)
        rx, _ = process_text(cx, xenon_idx, mode='all', seed=SEED + step * 37)
        rg, _ = process_text(cg, general_idx, mode='all', seed=SEED + step * 37)
        lines.append(f"  [{step:3d}] ORA: {ro}")
        lines.append(f"  [{step:3d}] XEN: {rx}")
        lines.append(f"  [{step:3d}] GEN: {rg}")
        co, cx, cg = ro, rx, rg

    lines.append("")

save_file('06_three_currents.txt', '\n'.join(lines))

# ═══════════════════════════════════════════
# 7. ZONE CUT-UP from jumped text
# ═══════════════════════════════════════════

# Use oracle corpus for cut-up source text
corpus_txt = cut_up.load_corpus('oracle')

lines = [
    f"ZONE CUT-UP from Jumped Text ({timestamp})",
    SEP,
    f"Each zone's fragmentation profile applied to xeno-jumped text.",
    f"Corpus for source text: oracle",
    "",
]

for src in SOURCE_SENTENCES[:5]:
    jumped, _ = process_text(src, oracle_idx, mode='all', seed=SEED + 7)

    lines.append(f"\n{DIV}")
    lines.append(f"SOURCE: {src}")
    lines.append(f"JUMPED: {jumped}")
    lines.append(DIV)

    for z_num in range(10):
        z = cut_up.ZONES[z_num]
        frags = cut_up.fragment(jumped, z['mode'])
        kept = cut_up.cut(frags, z['cut'])
        if z.get('rec'):
            kept = cut_up.recombine(kept, z.get('rs', 'echo'))
        if z['xen']:
            kept = [cut_up.xenotate(f, z.get('xmode', 'sparse')) for f in kept]
        kept = kept[:15]
        if z.get('prefix'):
            kept = [z['prefix'] + k for k in kept]
        result = z['sep'].join(kept)
        lines.append(f"\n  ZONE {z_num} [{z['name'].upper()}]")
        lines.append(f"  {result}")

    lines.append("")

save_file('07_zone_cutup.txt', '\n'.join(lines))

# ═══════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════

print(f"\n{'='*48}")
print(f"Output directory: {OUTPUT_DIR}")
print(f"Files:")
for fname in sorted(os.listdir(OUTPUT_DIR)):
    path = os.path.join(OUTPUT_DIR, fname)
    size = os.path.getsize(path)
    print(f"  {fname:<35s} {size:>8,} bytes")
