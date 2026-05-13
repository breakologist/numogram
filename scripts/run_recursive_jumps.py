"""
Recursive Xeno-Jump — Multi-Method Generator

Produces multiple output files with different transform setups:
  1. fixed_chain.txt      Full sentence AQ-preserving cascade
  2. phrase_jump.txt      One-word-per-step mutation
  3. word_triangular.txt  Triangular zone drift from seed words
  4. word_syzygy.txt      Syzygy oscillation from seed words
  5. word_entropy.txt     Hardware entropy walk from seed words
  6. beat_poem.txt        AQ-preserved beat poetry from chains
  7. all_zones_cutup.txt  Zone-profile cut-up from jumped text

Usage:
  python3 run_recursive_jumps.py
"""

import os, sys, json, random, datetime

sys.path.insert(0, os.path.dirname(__file__))
from xeno_jump import load_index, process_text, get_aq
import cut_up

# ═══════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════

OUTPUT_DIR = '/tmp/xeno-jump-results'
os.makedirs(OUTPUT_DIR, exist_ok=True)

STEPS = 69          # Generations for chains
SEED = 333          # Base seed

# Source texts for fixed chain
SOURCE_SENTENCES = [
    "Iota Alpha Omega",
    "Hermetic Cosmology",
    "of man's first disobediance and the fruit",
    "to be or not to be, that is the question",
    "two five dual snakes",
    "the three sided shapes",
    "do what thou wilt shall be the whole of the law",
    "And God said, Let there be light, and there was light",
    "ordo amoris integrates good and evil spirits alike",
    "The CCRU dissolved before it finished. That is why it still works",
    "Katak and Oddubb: the twin serpents of the decimal deep.",
    "Xenotation writes in a language that hasn't been invented yet.",
    "It could all become One, but why stop there?", 
    "Palindromic self-mirrors are gates that open from both sides simultaneously",
]

# Seed words for word-level transforms
SEED_WORDS = [
    "Xenotation", "Pandemonium", "Katak", "Djynxx", "Nullotation", "Anglossic", "Beast", "Pulse", 
    "Syzygy", "Hyperstition", "Void", "Plex", "Warp", "Autism", "Angelic Materialism", "true faith", "Xenocosmography", 
]

# ═══════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════

def zone(n):
    if n <= 0: return 9
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
    print(f"  ✅ {filename} ({len(content)} chars)")

class MockIndex:
    def __init__(self, d): self.data = d
    def get(self, k, d=None): return self.data.get(k, d)

# Load both indices
with open(os.path.dirname(__file__) + '/aq_corpus_index.json') as f:
    uni_data = {int(k): v for k, v in json.load(f).items()}
    uni_idx = MockIndex(uni_data)

enr_path = os.path.dirname(__file__) + '/aq_corpus_enriched.json'
if os.path.exists(enr_path):
    with open(enr_path) as f:
        enr_data = {int(k): v for k, v in json.load(f).items()}
else:
    enr_data = uni_data
enr_idx = MockIndex(enr_data)

timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
SEP = "═" * 64
DIV = "─" * 64
ARROW = chr(8594)

print(f"Generating recursive xeno-jump results...")
print(f"  Steps: {STEPS} | Seed: {SEED} | Time: {timestamp}\n")

# ═══════════════════════════════════════════
# 1. FIXED AQ CHAIN — Full sentence
# ═══════════════════════════════════════════

lines = [
    f"FIXED AQ CHAIN — Recursive Xeno-Jump ({timestamp})",
    SEP,
    f"AQ checksum never changes. Vocabulary cascades.",
    f"Engine: xeno_jump.py (all-word mode, seed {SEED})"
]

for src in SOURCE_SENTENCES:
    base_aq = get_aq(src)
    lines.append(f"\n{DIV}")
    lines.append(f"SOURCE (AQ={base_aq}, Z{zone(base_aq)}): {src}")
    lines.append(DIV)
    
    current = src
    for step in range(1, STEPS + 1):
        result, _ = process_text(current, uni_idx, mode='all', seed=SEED + step * 37)
        chk = get_aq(result)
        mark = "✓" if chk == base_aq else "✗"
        lines.append(f"  [{step:3d}] {mark} {result}")
        current = result

save_file('01_fixed_chain.txt', '\n'.join(lines))

# ═══════════════════════════════════════════
# 2. PHRASE JUMP — One word per step
# ═══════════════════════════════════════════

lines = [
    f"PHRASE JUMP — One-Word Mutation ({timestamp})",
    SEP,
    f"Exactly one word jumps per generation. AQ drifts slowly.",
    f"Engine: xeno_jump.py (first-match mode, seed {SEED})"
]

for src in SOURCE_SENTENCES:
    base_aq = get_aq(src)
    lines.append(f"\n{DIV}")
    lines.append(f"SOURCE (AQ={base_aq}): {src}")
    lines.append(DIV)
    lines.append(f"  [  0]   {src}")
    
    current = src
    for step in range(1, STEPS + 1):
        result, jumps = process_text(current, uni_idx, mode='first', seed=SEED + step * 43)
        if jumps:
            orig, new, aq, z = jumps[0]
            drift = get_aq(result) - base_aq
            lines.append(f"  [{step:3d}] {orig} {ARROW} {new}  (drift {drift:+5d})  {result}")
        else:
            lines.append(f"  [{step:3d}] (stuck)  {result}")
        current = result

save_file('02_phrase_jump.txt', '\n'.join(lines))

# ═══════════════════════════════════════════
# 3. WORD TRIANGULAR DRIFT
# ═══════════════════════════════════════════

lines = [
    f"WORD TRIANGULAR DRIFT ({timestamp})",
    SEP,
    f"Seed word zone follows T(n) mod 9: 1{ARROW}3{ARROW}6{ARROW}1{ARROW}6{ARROW}3...",
    f"Engine: zone-targeted word selection, seed {SEED}"
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
        
        # Find word with target zone
        candidates = []
        for aq, words in uni_data.items():
            if zone(aq) == target_dr:
                candidates.extend(words)
        
        chosen = random.Random(SEED * 1000 + step * 37).choice(candidates) if candidates else "---"
        chosen_aq = get_aq(chosen)
        lines.append(f"  [{step:3d}] T({step})={t_raw:3d} {ARROW} Z{target_dr}: {current} {ARROW} {chosen}  (AQ={chosen_aq}, Z{zone(chosen_aq)})")
        current = chosen

save_file('03_word_triangular.txt', '\n'.join(lines))

# ═══════════════════════════════════════════
# 4. WORD SYZYGY OSCILLATION
# ═══════════════════════════════════════════

lines = [
    f"WORD SYZYGY OSCILLATION ({timestamp})",
    SEP,
    f"Each step jumps to the syzygy partner zone: Z(n) {ARROW} Z(9-n) {ARROW} Z(n)...",
    f"Engine: zone-targeted word selection, seed {SEED}"
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
        for aq, words in uni_data.items():
            if zone(aq) == target_z:
                candidates.extend(words)
        
        chosen = random.Random(SEED * 2000 + step * 37).choice(candidates) if candidates else "---"
        chosen_aq = get_aq(chosen)
        lines.append(f"  [{step:3d}] Z{current_z} {ARROW} Z{target_z}: {current} {ARROW} {chosen}  (AQ={chosen_aq}, Z{zone(chosen_aq)})")
        current = chosen
        current_z = target_z

save_file('04_word_syzygy.txt', '\n'.join(lines))

# ═══════════════════════════════════════════
# 5. BEAT POEM from AQ-preserved chains
# ═══════════════════════════════════════════

beat_words = ["door","Autism","Beast Pulse", "Hermetic"]

lines = [
    f"BEAT POEM — AQ-Preserved Seed Chains ({timestamp})",
    SEP,
    f"Words sharing AQ values, woven into verse.",
    f"Seeds: {', '.join(beat_words)}"
]

rng = random.Random(SEED)
chains = {}
for s in beat_words:
    aq = get_aq(s)
    bucket = uni_data.get(aq, [s])
    pool = [w for w in bucket if w.lower() != s.lower()] or bucket
    chain = [s]
    for i in range(STEPS):
        chain.append(rng.choice(pool))
    chains[s] = chain

for i, (seed_word, chain) in enumerate(chains.items()):
    aq = get_aq(seed_word)
    lines.append(f"\n{DIV}")
    lines.append(f"CHAIN: {seed_word} (AQ={aq}, Z{zone(aq)})")
    lines.append(DIV)
    chain_line = " → ".join(chain[:STEPS+2])
    lines.append(f"  {chain_line}")
    lines.append("")

# Compose poem
lines.append(f"\n{DIV}")
lines.append("COMPOSED VERSE")
lines.append(DIV)

em_dash = chr(9669)
for i in range(STEPS):
    w0 = chains[beat_words[0]][i % len(chains[beat_words[0]])]
    w1 = chains[beat_words[1]][i % len(chains[beat_words[1]])]
    w2 = chains[beat_words[2]][i % len(chains[beat_words[2]])]
    w3 = chains[beat_words[3]][i % len(chains[beat_words[3]])]
    
    pattern = i % 4
    if pattern == 0:
        lines.append(f"  {w0}")
    elif pattern == 1:
        lines.append(f"  the {w1.lower()} of {w0} {w2.lower()}")
    else:
        middle = (" %s " % em_dash).join([w1, w2])
        lines.append(f"  {w0} {em_dash} {middle}")

save_file('05_beat_poem.txt', '\n'.join(lines))

# ═══════════════════════════════════════════
# 6. ENRICHED INDEX COMPARISON — Same source, two indices
# ═══════════════════════════════════════════

lines = [
    f"ENRICHED vs UNIVERSAL — Side by Side ({timestamp})",
    SEP,
    f"Same seed, same source, different indices.",
    f"Universal: {sum(len(v) for v in uni_data.values())} words",
    f"Enriched:  {sum(len(v) for v in enr_data.values())} words"
]

for src in SOURCE_SENTENCES[:3]:
    lines.append(f"\n{DIV}")
    lines.append(f"SOURCE: {src}")
    lines.append(DIV)
    
    # Universal
    current_u = src
    # Enriched
    current_e = src
    
    for step in range(1, 11):
        r_u, _ = process_text(current_u, uni_idx, mode='all', seed=SEED + step * 37)
        r_e, _ = process_text(current_e, enr_idx, mode='all', seed=SEED + step * 37)
        lines.append(f"  [{step:3d}] UNI: {r_u}")
        lines.append(f"  [{step:3d}] ENR: {r_e}")
        current_u = r_u
        current_e = r_e

save_file('06_enriched_comparison.txt', '\n'.join(lines))

# ═══════════════════════════════════════════
# 7. ALL 10 ZONES CUT-UP from jumped text
# ═══════════════════════════════════════════

lines = [
    f"ZONE CUT-UP from Jumped Text ({timestamp})",
    SEP,
    f"Each zone's fragmentation profile applied to xeno-jumped text.",
]

for src in SOURCE_SENTENCES[:2]:
    # First jump the source
    jumped, _ = process_text(src, uni_idx, mode='all', seed=SEED + 7)
    
    lines.append(f"\n{DIV}")
    lines.append(f"SOURCE: {src}")
    lines.append(f"JUMPED: {jumped}")
    lines.append(DIV)
    
    # Run cut-up for each zone
    corpus = {'jumped': jumped}
    for z_num in range(10):
        z = cut_up.ZONES[z_num]
        text = jumped
        frags = cut_up.fragment(text, z['mode'])
        kept = cut_up.cut(frags, z['cut'])
        if z.get('rec'):
            kept = cut_up.recombine(kept, z.get('rs', 'echo'))
        if z['xen']:
            kept = [cut_up.xenotate(f, z.get('xmode', 'sparse')) for f in kept]
        kept = kept[:15]
        if z.get('prefix'):
            kept = [z['prefix'] + k for k in kept]
        result = z['sep'].join(kept)
        lines.append(f"\n  ZONE {z_num} [{z['name']}]")
        lines.append(f"  {result}")

save_file('07_zone_cutup.txt', '\n'.join(lines))

# ═══════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════

print(f"\n{'='*40}")
print(f"All files written to: {OUTPUT_DIR}")
print(f"Files:")
for fname in sorted(os.listdir(OUTPUT_DIR)):
    path = os.path.join(OUTPUT_DIR, fname)
    size = os.path.getsize(path)
    print(f"  {fname:<35s} {size:>6,} bytes")
