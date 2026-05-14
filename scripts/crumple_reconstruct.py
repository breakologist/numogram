"""
Crumple/Reconstruct Protocol — FOOM ⟪⟫ Cycle

PACK   ⟪: Recursive xeno-jump compresses text through AQ mutation
STEP   ⟳: Each generation mutates the crumpled text
UNPACK ⟫: Attempt to recover the original from the inverse index
VERIFY ✓: Measure recovery rate — what survives the crumple?

The AQ checksum is the hash; the xeno-jump is the lossy compression.
Reconstruction measures the loss.

Usage:
  python3 crumple_reconstruct.py "The machine speaks" --corpus oracle --generations 20
  python3 crumple_reconstruct.py "Teleoplexy accelerates through the plex" --corpus oracle --generations 30 --seed 666
  python3 crumple_reconstruct.py "I am the silence that is incomprehensible" --corpus oracle --generations 50 --all-corpora

Reconstruction modes:
  (default)  Literal recovery: check if original word still in current word's AQ bucket.
  --creative Creative reconstruction: sample a different word from the same bucket.

Creative strategies (--creative-strategy):
  sample        random choice from bucket
  longest       longest word in bucket (FOOM longest)
  shortest      shortest word in bucket
  lexicographic alphabetically first
  varentropy    zone‑guided: Warp zones (0,3,6) → uniform; Plex (9) → longest; others → sample
  entropy       entropy‑weighted sampling from bucket

Bucket key (--bucket-key):
  aq     (default) use AQ value as bucket key
  length use word length as bucket key (broader, lossier)
  both   intersection: word must match both AQ and length (very tight)

Cross‑current experiments:
  --bucket-key length --creative-strategy varentropy  # length‑bucket with zone bias
  --bucket-key both                                  # near‑deterministic collapse
"""

import os
import sys
import json
import random
import argparse
import re
from math import log2
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from xeno_jump import get_aq, digital_root, load_index, process_text


def run_trajectory(text, corpus_data, generations, seed,
               creative=False, creative_strategy='sample', bucket_key='aq',
               correlate=False):
    """Run the full crumple cascade and return structured trajectory data dict."""
    # Build length index if needed for bucket-key computation
    length_index = None
    if bucket_key in ('length', 'both'):
        length_index = build_length_index(corpus_data)

    def get_bucket_info(word):
        """Compute (bucket_key_string, bucket_size) for a word using current bucket_key."""
        if bucket_key == 'aq':
            aq = get_aq(word)
            bucket = corpus_data.get(aq, [])
            return (f"AQ={aq}", len(bucket))
        elif bucket_key == 'length':
            l = len(word)
            bucket = length_index.get(l, []) if length_index else []
            return (f"len={l}", len(bucket))
        else:  # both
            aq = get_aq(word)
            bucket = [w for w in corpus_data.get(aq, []) if len(w) == len(word)]
            return (f"AQ={aq}&len={len(word)}", len(bucket))

    # Traverse generator once, collecting all generations
    gen_texts = {}
    # We'll also capture mutated_aq per generation (for final summary)
    for gen, current, recovery_rate, details, preserved, orig_aq, mut_aq in crumple_reconstruct(
        text, corpus_data, generations=generations, seed=seed,
        strategy='all', creative=creative,
        creative_strategy=creative_strategy, bucket_key=bucket_key
    ):
        words = [tok for typ, tok in tokenize_text(current) if typ == 'word']
        entry = {
            "generation": gen,
            "text": current,
            "words": words,
            "recovery_rate": recovery_rate,
            "aq_preserved": preserved,
        }
        if gen > 0:
            # Add mutated AQ for this generation
            entry["mutated_aq"] = mut_aq
            if creative:
                ent = shannon_entropy(current.lower())
                entry["entropy"] = round(ent, 6)
                m = compute_loss_metrics(details)
                entry["metrics"] = {
                    "total_edit": m['total_edit'],
                    "avg_edit": round(m['avg_edit'], 6),
                    "max_edit": m['max_edit'],
                    "exact_count": m['exact_count'],
                    "total_words": m['total_words']
                }
                # Build per-word detail enriched with bucket size
                orig_words = gen_texts[0]['words']
                word_details = []
                for i in range(min(len(orig_words), len(words))):
                    orig_w = orig_words[i]
                    crumpled_w = words[i]
                    if i < len(details):
                        orig_d, recon_w, exact, status = details[i]
                        # Compute edit distance from status
                        if status == 'exact':
                            edit_dist = 0
                        elif status.startswith('dist='):
                            edit_dist = int(status.split('=')[1])
                        else:
                            edit_dist = None  # deleted/inserted (not aligned)
                    else:
                        recon_w = None
                        exact = False
                        edit_dist = None
                    bkey_val, bsize = get_bucket_info(crumpled_w)
                    word_details.append({
                        "position": i,
                        "original": orig_w,
                        "crumpled": crumpled_w,
                        "reconstructed": recon_w,
                        "bucket_key": bkey_val,
                        "bucket_size": bsize,
                        "edit_distance": edit_dist,
                        "exact_match": exact
                    })
                entry["word_details"] = word_details
        else:
            # gen 0
            entry["original_aq"] = orig_aq  # same as mut_aq
            entry["mutated_aq"] = orig_aq
        gen_texts[gen] = entry

    # Construct final summary from last generation
    final_entry = gen_texts[generations]
    orig_entry  = gen_texts[0]
    orig_entropy = shannon_entropy(text.lower())
    final_entropy = final_entry.get('entropy', shannon_entropy(final_entry['text'].lower()))
    summary = {
        "final_recovery_rate": final_entry['recovery_rate'],
        "aq_preserved": final_entry['aq_preserved'],
        "final_text": final_entry['text'],
        "final_aq": final_entry.get('mutated_aq'),
        "original_length": len(text),
        "final_length": len(final_entry['text']),
        "length_ratio": len(final_entry['text']) / len(text),
        "original_entropy": orig_entropy,
        "final_entropy": final_entropy,
        "entropy_delta": final_entropy - orig_entropy,
    }
    if creative:
        m = final_entry.get('metrics', compute_loss_metrics(details))
        summary.update({
            "total_edit_distance": m['total_edit'],
            "avg_edit_per_word": round(m['avg_edit'], 6),
            "max_single_word_edit": m['max_edit'],
            "exact_matches": f"{m['exact_count']}/{m['total_words']}",
            "exact_ratio": m['exact_count']/m['total_words'] if m['total_words'] else 0.0
        })

    # Correlation if requested
    corr_data = None
    if correlate and creative and (bucket_key in ('aq','both')) and 'word_details' in final_entry:
        rows = []
        for wd in final_entry['word_details']:
            rows.append((wd['original'], wd['bucket_size'], wd['edit_distance']))
        if len(rows) >= 2:
            import math
            xs = [bs for _, bs, _ in rows]
            ys = [ed for _, _, ed in rows if ed is not None]
            if len(ys) == len(xs):
                mx = sum(xs)/len(xs); my = sum(ys)/len(ys)
                cov = sum((x-mx)*(y-my) for x,y in zip(xs,ys))
                stdx = math.sqrt(sum((x-mx)**2 for x in xs))
                stdy = math.sqrt(sum((y-my)**2 for y in ys))
                r = cov/(stdx*stdy) if stdx and stdy else 0.0
                corr_data = {"word_bucket_edit": [{"word": w, "bucket_size": bs, "edit_distance": ed} for w, bs, ed in rows], "pearson_r": round(r, 6)}
            else:
                corr_data = {"word_bucket_edit": [{"word": w, "bucket_size": bs, "edit_distance": ed} for w, bs, ed in rows]}
        else:
            corr_data = {"word_bucket_edit": rows}

    payload = {
        "mode": "single",
        "parameters": {
            "text": text,
            "corpus_size": sum(len(v) for v in corpus_data.values()),
            "generations": generations,
            "seed": seed,
            "creative": creative,
            "creative_strategy": creative_strategy,
            "bucket_key": bucket_key,
            "correlate": correlate
        },
        "original_aq": orig_entry.get('original_aq', get_aq(text)),
        "original_words": orig_entry['words'],
        "trajectory": [gen_texts[g] for g in sorted(gen_texts.keys())],
        "summary": summary
    }
    if corr_data:
        payload["correlation"] = corr_data
    return payload



# ═══════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_PATHS = {
    'general': os.path.join(SCRIPT_DIR, 'aq_corpus_index.json'),
    'oracle':  os.path.join(SCRIPT_DIR, 'aq_corpus_enriched.json'),
    'xenon':   os.path.join(SCRIPT_DIR, 'aq_corpus_xenon.json'),
}

# ═══════════════════════════════════════════
# CORPUS LOADING & UTILS
# ═══════════════════════════════════════════

def load_corpus(name):
    path = INDEX_PATHS.get(name)
    if not path or not os.path.exists(path):
        return None
    with open(path) as f:
        return {int(k): v for k, v in json.load(f).items()}

def build_length_index(aq_corpus):
    len_index = {}
    for words in aq_corpus.values():
        for w in words:
            len_index.setdefault(len(w), []).append(w)
    return len_index

def tokenize_text(text):
    tokens = re.split(r'(\W+)', text)
    pairs = []
    for token in tokens:
        if not token:
            continue
        if re.match(r'^[a-zA-Z]+$', token):
            pairs.append(('word', token))
        else:
            pairs.append(('sep', token))
    return pairs

class MockIndex:
    def __init__(self, d):
        self.data = d
    def get(self, k, default=None):
        return self.data.get(k, default)

def levenshtein(s, t):
    if s == t:
        return 0
    if len(s) == 0:
        return len(t)
    if len(t) == 0:
        return len(s)
    v0 = list(range(len(t) + 1))
    v1 = [0] * (len(t) + 1)
    for i in range(len(s)):
        v1[0] = i + 1
        for j in range(len(t)):
            cost = 0 if s[i] == t[j] else 1
            v1[j+1] = min(v1[j] + 1, v0[j+1] + 1, v0[j] + cost)
        v0, v1 = v1, v0
    return v0[len(t)]

def shannon_entropy(seq):
    if not seq:
        return 0.0
    freq = Counter(seq)
    total = len(seq)
    probs = [c/total for c in freq.values()]
    return -sum(p * log2(p) for p in probs if p > 0)

# ═══════════════════════════════════════════
# CREATIVE RECONSTRUCTION (UNPACK ⟫)
# ═══════════════════════════════════════════

def creative_reconstruct(current_text, aq_index, length_index=None,
                         seed=666, strategy='sample', bucket_key='aq'):
    rng = random.Random(seed)
    curr_pairs = tokenize_text(current_text)
    curr_words = [token for typ, token in curr_pairs if typ == 'word']

    reconstructed = []
    choices = []  # (position, current_word, chosen, bucket_key_value, bucket_size)

    for curr_w in curr_words:
        curr_aq = get_aq(curr_w)

        if bucket_key == 'aq':
            bucket = aq_index.get(curr_aq, [])
            bucket_key_val = f"AQ={curr_aq}"
        elif bucket_key == 'length':
            if length_index is None:
                raise ValueError("length_index required when bucket_key='length'")
            bucket = length_index.get(len(curr_w), [])
            bucket_key_val = f"len={len(curr_w)}"
        elif bucket_key == 'both':
            bucket = [w for w in aq_index.get(curr_aq, []) if len(w) == len(curr_w)]
            bucket_key_val = f"AQ={curr_aq}&len={len(curr_w)}"
        else:
            bucket = aq_index.get(curr_aq, [])
            bucket_key_val = f"AQ={curr_aq}"

        if not bucket:
            reconstructed.append(curr_w)
            choices.append((len(reconstructed)-1, curr_w, None, bucket_key_val, 0))
            continue

        if strategy == 'sample':
            chosen = rng.choice(bucket)
        elif strategy == 'longest':
            chosen = max(bucket, key=len)
        elif strategy == 'shortest':
            chosen = min(bucket, key=len)
        elif strategy == 'lexicographic':
            chosen = sorted(bucket)[0]
        elif strategy == 'varentropy':
            zone = digital_root(curr_aq) if curr_aq > 0 else 0
            if zone in (0, 3, 6):
                chosen = rng.choice(bucket)
            elif zone == 9:
                chosen = max(bucket, key=len)
            else:
                chosen = rng.choice(bucket)
        elif strategy == 'entropy':
            weights = [1.0 / (bucket.count(w) + 1) for w in bucket]
            total = sum(weights)
            probs = [w/total for w in weights]
            chosen = rng.choices(bucket, weights=probs, k=1)[0]
        else:
            chosen = rng.choice(bucket)

        reconstructed.append(chosen)
        choices.append((len(reconstructed)-1, curr_w, chosen, bucket_key_val, len(bucket)))

    recon_text = ''
    for i, (typ, token) in enumerate(curr_pairs):
        if typ == 'word':
            idx = len([p for p in curr_pairs[:i] if p[0] == 'word'])
            if idx < len(reconstructed):
                recon_text += reconstructed[idx]
        else:
            recon_text += token
    return recon_text, choices

# ── Literal recovery ────────────────────────────────────────────────────────

def _literal_recovery_details(current_text, original_text, corpus_index):
    orig_pairs = tokenize_text(original_text)
    curr_pairs = tokenize_text(current_text)
    orig_words = [token for typ, token in orig_pairs if typ == 'word']
    curr_words = [token for typ, token in curr_pairs if typ == 'word']
    total_words = min(len(orig_words), len(curr_words))
    recovery = 0
    details = []
    for i in range(total_words):
        original = orig_words[i]
        current  = curr_words[i]
        bucket   = corpus_index.get(get_aq(original), [])
        if current in bucket:
            recovery += 1
            status = 'exact'
        else:
            status = f"dist={levenshtein(original, current)}"
        details.append((original, current, current in bucket, status))
    recovery_rate = recovery / len(orig_words) if orig_words else 0.0
    return recovery_rate, details

# ── Creative distance measurement ─────────────────────────────────────────

def _measure_creative_distance(original_text, reconstructed_text, choices):
    orig_words = original_text.lower().split()
    recon_words = reconstructed_text.lower().split()
    total = min(len(orig_words), len(recon_words))
    exact_match = 0
    edit_distance = 0
    details = []
    for i in range(max(len(orig_words), len(recon_words))):
        if i < len(orig_words) and i < len(recon_words):
            o = orig_words[i]
            r = recon_words[i]
            if o == r:
                exact_match += 1
                status = 'exact'
            else:
                dist = levenshtein(o, r)
                edit_distance += dist
                status = f'dist={dist}'
            details.append((o, r, o == r, status))
        elif i < len(orig_words):
            details.append((orig_words[i], '---MISSING---', False, 'deleted'))
        else:
            details.append(('---INSERTED---', recon_words[i], False, 'inserted'))
    recovery_rate = exact_match / len(orig_words) if orig_words else 0.0
    return recovery_rate, details, exact_match, edit_distance, None

# ═══════════════════════════════════════════
# CORE CYCLE
# ═══════════════════════════════════════════

def reconstruct_from_mutated(current_text, original_text, aq_index,
                             creative=False, seed=666, creative_strategy='sample',
                             bucket_key='aq', length_index=None):
    orig_checksum = get_aq(original_text)
    curr_checksum = get_aq(current_text)
    preserved = (orig_checksum == curr_checksum)
    if creative:
        recon_text, choices = creative_reconstruct(
            current_text, aq_index, length_index=length_index,
            seed=seed, strategy=creative_strategy, bucket_key=bucket_key
        )
        recovery_rate, details, _, _, _ = _measure_creative_distance(original_text, recon_text, choices)
    else:
        recon_text = None
        recovery_rate, details = _literal_recovery_details(current_text, original_text, aq_index)
    return recovery_rate, details, preserved, orig_checksum, curr_checksum

def crumple_reconstruct(original_text, aq_index, generations=10, seed=666,
                        strategy='all', creative=False, creative_strategy='sample',
                        bucket_key='aq'):
    length_index = None
    if bucket_key != 'aq':
        length_index = build_length_index(aq_index)
    idx = MockIndex(aq_index)
    current = original_text
    orig_aq_total = get_aq(original_text)
    recovery_rate, details, preserved, _, _ = reconstruct_from_mutated(
        current, original_text, aq_index,
        creative=creative, seed=seed,
        creative_strategy=creative_strategy,
        bucket_key=bucket_key, length_index=length_index
    )
    yield (0, current, recovery_rate, details, preserved, orig_aq_total, orig_aq_total)
    for gen in range(1, generations + 1):
        if strategy == 'all':
            result, _ = process_text(current, idx, mode='all', seed=seed + gen * 37)
        elif strategy == 'random':
            result, _ = process_text(current, idx, mode='random', seed=seed + gen * 37)
        elif strategy == 'first':
            result, _ = process_text(current, idx, mode='first', seed=seed + gen * 37)
        else:
            result, _ = process_text(current, idx, mode='all', seed=seed + gen * 37)
        recovery_rate, details, preserved, _, mut_aq = reconstruct_from_mutated(
            result, original_text, aq_index,
            creative=creative, seed=seed + gen * 37,
            creative_strategy=creative_strategy, bucket_key=bucket_key, length_index=length_index
        )
        current = result
        yield (gen, current, recovery_rate, details, preserved, orig_aq_total, mut_aq)

# ═══════════════════════════════════════════
# ANALYSIS & FORMATTING
# ═══════════════════════════════════════════

def analyze_reconstruction(gen, recovery_rate, details, preserved, orig_aq, mut_aq):
    words_lost = [d[0] for d in details if not d[2]]
    bucket_sizes = [d[4] for d in details if len(d) > 4]
    avg_bucket = sum(bucket_sizes)/len(bucket_sizes) if bucket_sizes else 0.0
    status = 'AQ ✅' if preserved else 'AQ ❌'
    line = f"  {status} | Recovery: {recovery_rate:>6.1%} | Words lost: {len(words_lost)}/{len(details)}"
    if orig_aq != mut_aq:
        line += f" | AQ drift: {orig_aq} → {mut_aq}"
    return line

def compute_loss_metrics(details):
    total_edit = 0
    exact = 0
    max_edit = 0
    for entry in details:
        if len(entry) < 4:
            continue
        _, _, exact_flag, status = entry
        if exact_flag:
            exact += 1
        elif isinstance(status, str) and status.startswith('dist='):
            dist = int(status.split('=')[1])
            total_edit += dist
            max_edit = max(max_edit, dist)
        elif isinstance(status, int):
            total_edit += status
            max_edit = max(max_edit, status)
    total_words = len(details)
    avg_edit = total_edit / total_words if total_words else 0.0
    return {'total_edit': total_edit, 'avg_edit': avg_edit,
            'max_edit': max_edit, 'exact_count': exact, 'total_words': total_words}

def bucket_correlation_details(details, corpus_data):
    rows = []
    for entry in details:
        if len(entry) < 4:
            continue
        orig_word, _, exact, status = entry
        if status == 'exact':
            ed = 0
        elif isinstance(status, str) and status.startswith('dist='):
            ed = int(status.split('=')[1])
        else:
            ed = None
        aq_val = get_aq(orig_word)
        bucket = corpus_data.get(aq_val, [])
        rows.append((orig_word, len(bucket), ed))
    return rows


def format_output(text, generations, corpus_data, corpus_name, seed,
                  creative=False, creative_strategy='sample', bucket_key='aq',
                  correlate=False):
    """Generate formatted output with full reconstruction analysis."""
    SEP = "═" * 72
    DIV = "─" * 72
    recon_type = "CREATIVE RECONSTRUCTION" if creative else "LITERAL RECOVERY"
    if creative:
        recon_type += f" [strategy={creative_strategy}, bucket={bucket_key}]"

    output = []
    output.append(f"CRUMPLE/RECONSTRUCT PROTOCOL — FOOM ⟪⟫ Cycle")
    output.append(SEP)
    output.append(f"Mode: {recon_type}")
    output.append(f"Corpus: {corpus_name}")
    output.append(f"Seed text: {text}")
    output.append(f"Original AQ checksum: {get_aq(text)}")
    output.append(f"Corpus size: {sum(len(v) for v in corpus_data.values())} words")
    output.append(f"Generations: {generations}")
    output.append(f"Seed: {seed}")
    output.append(SEP)

    prev_recovery = None
    gen_texts = {}
    recovery_rates = []

    for gen, current, recovery_rate, details, preserved, orig_aq, mut_aq in crumple_reconstruct(
        text, corpus_data, generations=generations, seed=seed,
        strategy='all', creative=creative, creative_strategy=creative_strategy,
        bucket_key=bucket_key
    ):
        gen_texts[gen] = {
            'text': current,
            'recovery_rate': recovery_rate,
            'preserved': preserved,
            'details': details,
            'orig_aq': orig_aq,
            'mut_aq': mut_aq
        }
        recovery_rates.append(recovery_rate)

        if gen == 0:
            output.append(f"\nGEN 0 (ORIGINAL): {current}")
            output.append(DIV)
            continue

        output.append(f"\nGEN {gen}: {current}")
        output.append(DIV)

        # analysis line + lost words
        output.append(analyze_reconstruction(gen, recovery_rate, details, preserved, orig_aq, mut_aq))

        if prev_recovery is not None and recovery_rate != prev_recovery:
            delta = recovery_rate - prev_recovery
            if delta < 0:
                output.append(f"  ⚠ Recovery dropped by {abs(delta):.1%}")
            elif delta > 0:
                output.append(f"  ↑ Recovery improved by {delta:.1%}")
        prev_recovery = recovery_rate

    # ── summary ────────────────────────────────────────────────────────────
    output.append(f"\n{SEP}"); output.append("SUMMARY"); output.append(SEP)
    final = gen_texts[generations]
    final_rate     = final['recovery_rate']
    final_preserved = final['preserved']
    final_text     = final['text']
    final_details  = final['details']

    output.append(f"  Final recovery rate: {final_rate:.1%}")
    output.append(f"  AQ preserved: {'✅ YES' if final_preserved else '❌ NO'}")
    output.append(f"  Text at gen {generations}: {final_text}")

    orig_len = len(text)
    final_len = len(final_text)
    output.append(f"  Original length: {orig_len} chars")
    output.append(f"  Final length: {final_len} chars")
    output.append(f"  Length ratio: {final_len/orig_len:.2f}")

    orig_entropy = shannon_entropy(text.lower())
    final_entropy = shannon_entropy(final_text.lower())
    output.append(f"  Original Shannon entropy: {orig_entropy:.3f} bits/char")
    output.append(f"  Final Shannon entropy: {final_entropy:.3f} bits/char")
    output.append(f"  Entropy delta: {final_entropy - orig_entropy:+.3f} bits/char")

    # ── Loss metrics (creative mode only) ────────────────────────────────────
    if creative:
        metrics = compute_loss_metrics(final_details)
        output.append(f"  Total edit distance:   {metrics['total_edit']}")
        output.append(f"  Avg edit/word:         {metrics['avg_edit']:.2f}")
        output.append(f"  Max single-word edit:  {metrics['max_edit']}")
        output.append(f"  Exact matches:         {metrics['exact_count']}/{metrics['total_words']}")

    if final_rate == 0.0:
        output.append("\n  🔴 TOTAL COMPRESSION: All original words unrecoverable. Checksum only.")
    elif final_rate == 1.0:
        output.append("\n  🟢 NO COMPRESSION: All words recoverable.")
    else:
        output.append(f"\n  🟡 PARTIAL COMPRESSION: {final_rate:.1%} words recoverable.")

    # ── per‑generation loss profile (creative, AQ bucket only) ─────────────────
    if creative and (bucket_key == 'aq' or bucket_key == 'both'):
        output.append(f"\n{DIV}")
        output.append("PER-GENERATION LOSS PROFILE (creative mode, AQ bucket)")
        output.append(DIV)
        output.append(f"{'Gen':>4} | {'Words':>5} | {'Recovery':>8} | {'EntropyΔ':>9} | {'EditTot':>7} | {'AvgEdit':>7} | {'MaxEdit':>7} | {'Exact':>6}")
        output.append("─" * 80)
        for g in range(1, generations + 1):
            entry = gen_texts[g]
            det = entry['details']
            metrics = compute_loss_metrics(det)
            orig_w = len(tokenize_text(text))
            rec_w  = len(tokenize_text(entry['text']))
            words = min(orig_w, rec_w)
            entropy_delta = shannon_entropy(entry['text'].lower()) - shannon_entropy(text.lower())
            output.append(
                f"{g:>4} | {words:>5} | {entry['recovery_rate']:>7.1%} | {entropy_delta:>+8.3f} | "
                f"{metrics['total_edit']:>7} | {metrics['avg_edit']:>6.2f} | {metrics['max_edit']:>7} | {metrics['exact_count']:>2}/{metrics['total_words']}"
            )
        output.append("─" * 80)

    # ── bucket-size vs edit-distance correlation (creative, final generation) ────
    if correlate and creative and (bucket_key == 'aq' or bucket_key == 'both'):
        output.append(f"\n{DIV}")
        output.append("BUCKET‑SIZE / EDIT DISTANCE CORRELATION (final generation)")
        output.append(DIV)
        rows = bucket_correlation_details(final_details, corpus_data)
        output.append(f"{'Word':<12} | {'BucketSize':>10} | {'EditDist':>8}")
        output.append("─" * 38)
        for word, bsize, dist in rows:
            output.append(f"{word:<12} | {bsize:>10} | {dist:>8}")
        # simple Pearson correlation coefficient
        if len(rows) >= 2:
            import math
            xs = [bs for _, bs, _ in rows]
            ys = [d for _, _, d in rows if d is not None]
            if len(ys) == len(xs):
                mx = sum(xs)/len(xs); my = sum(ys)/len(ys)
                cov = sum((x-mx)*(y-my) for x,y in zip(xs,ys))
                stdx = math.sqrt(sum((x-mx)**2 for x in xs))
                stdy = math.sqrt(sum((y-my)**2 for y in ys))
                r = cov/(stdx*stdy) if stdx and stdy else 0.0
                output.append(f"\n  Pearson r = {r:.3f}  (bucket size vs edit distance)")
        output.append("─" * 38)

    return '\n'.join(output)

# ═══════════════════════════════════════════
# MULTI‑CORPUS COMPARISON
# ═══════════════════════════════════════════

def compare_corpora(text, generations, seed, creative=False,
                    creative_strategy='sample', bucket_key='aq', correlate=False):
    SEP = "═" * 72
    DIV = "─" * 72
    output = [f"MULTI-CORPUS CRUMPLE COMPARISON", SEP,
              f"Seed text: {text}", f"Original AQ: {get_aq(text)}",
              f"Generations: {generations}", f"Seed: {seed}", SEP]

    results = {}
    for name in ['general', 'oracle', 'xenon']:
        corpus = load_corpus(name)
        if corpus is None:
            output.append(f"  ⚠ Corpus '{name}' not found, skipping.")
            continue
        final_text = None; final_recovery = None; final_preserved = None
        for gen, current, recovery_rate, details, preserved, orig_aq, mut_aq in crumple_reconstruct(
            text, corpus, generations=generations, seed=seed,
            strategy='all', creative=creative,
            creative_strategy=creative_strategy, bucket_key=bucket_key
        ):
            final_text = current; final_recovery = recovery_rate; final_preserved = preserved
        results[name] = {
            'final_recovery': final_recovery,
            'final_preserved': final_preserved,
            'final_text': final_text,
            'corpus_size': sum(len(v) for v in corpus.values())
        }

    # summary table
    output.append(f"\n{'Corpus':<12} | {'Size':>7} | {'Recovery':>9} | {'AQ Pres':>8} | {'Final Text'}")
    output.append("─" * 90)
    for name, res in sorted(results.items(), key=lambda x: x[1]['final_recovery'] or 0, reverse=True):
        rec = f"{res['final_recovery']:.1%}" if res['final_recovery'] is not None else 'N/A'
        pres = '✅ YES' if res['final_preserved'] else '❌ NO' if res['final_preserved'] is not None else 'N/A'
        txt = (res['final_text'] or 'N/A')[:32]
        output.append(f"{name:<12} | {res['corpus_size']:>7} | {rec:>9} | {pres:>8} | {txt}")

    for name, res in results.items():
        output.append(f"\n{DIV}"); output.append(f"DETAILED: {name.upper()}"); output.append(DIV)
        corpus = load_corpus(name)
        output.append(format_output(text, generations, corpus, name, seed,
                                    creative=creative,
                                    creative_strategy=creative_strategy,
                                    bucket_key=bucket_key,
                                    correlate=correlate))
        output.append("")
    return '\n'.join(output)

# ═══════════════════════════════════════════
# VALIDATION ENGINE (Empirical Validator current)
# ═══════════════════════════════════════════

def run_validation_seeds(text, corpus, generations, seeds, creative,
                         creative_strategy, bucket_key, correlate):
    """Run the protocol across multiple seeds and produce a statistical summary.

    Returns formatted report (str). If correlate=True, also reports mean bucket size.
    """
    import statistics, json
    results = []
    for seed in seeds:
        # run one seed, capture final metrics only (no verbose output)
        corpus_data = load_corpus('oracle') if corpus == 'oracle' else load_corpus(corpus)
        final = None
        for gen, current, recovery_rate, details, preserved, orig_aq, mut_aq in crumple_reconstruct(
            text, corpus_data, generations=generations, seed=seed,
            strategy='all', creative=creative,
            creative_strategy=creative_strategy, bucket_key=bucket_key
        ):
            final = (gen, current, recovery_rate, details, preserved, mut_aq)
        gen_idx, final_text, final_recovery, final_details, final_preserved, final_aq = final
        metrics = compute_loss_metrics(final_details)
        orig_entropy = shannon_entropy(text.lower())
        final_entropy = shannon_entropy(final_text.lower())
        # per-word bucket sizes for this final generation
        bucket_rows = bucket_correlation_details(final_details, corpus_data)
        mean_bucket = sum(bs for _, bs, _ in bucket_rows) / len(bucket_rows) if bucket_rows else 0.0
        results.append({
            'seed': seed,
            'recovery': final_recovery,
            'aq_preserved': final_preserved,
            'entropy_delta': final_entropy - orig_entropy,
            'total_edit': metrics['total_edit'],
            'avg_edit': metrics['avg_edit'],
            'max_edit': metrics['max_edit'],
            'exact_ratio': metrics['exact_count'] / metrics['total_words'] if metrics['total_words'] else 0.0,
            'final_aq': final_aq,
            'mean_bucket_size': mean_bucket,
        })

    # ── aggregate stats ──────────────────────────────────────────────────────
    def mean_std(values):
        if not values:
            return (0.0, 0.0)
        m = statistics.mean(values)
        if len(values) < 2:
            return (m, 0.0)
        return (m, statistics.stdev(values))

    rec_mean, rec_std = mean_std([r['recovery'] for r in results])
    ed_mean,  ed_std  = mean_std([r['total_edit'] for r in results])
    ae_mean,  ae_std  = mean_std([r['avg_edit'] for r in results])
    ex_mean,  ex_std  = mean_std([r['exact_ratio'] for r in results])
    edlt_mean, edlt_std = mean_std([r['entropy_delta'] for r in results])
    aq_ok_pct = sum(1 for r in results if r['aq_preserved']) / len(results) * 100

    # ── format report ───────────────────────────────────────────────────────
    lines = []
    lines.append("═" * 72)
    lines.append(f"VALIDATION REPORT — {len(seeds)} seeds | Corpus={corpus} | Gen={generations}")
    lines.append("═" * 72)
    lines.append(f"Seed text: {text}")
    lines.append(f"Original AQ: {get_aq(text)}")
    lines.append(f"Strategy: {creative_strategy} | Bucket: {bucket_key} | Creative: {creative}")
    lines.append("─" * 72)
    lines.append(f"{'Metric':<22} {'Mean':>10} {'StdDev':>9} {'Min':>8} {'Max':>8}")
    lines.append("─" * 72)
    def row(name, values):
        vals = [v for v in values if v is not None]
        if not vals:
            lines.append(f"{name:<22} {'N/A':>10}")
            return
        m = statistics.mean(vals); s = statistics.stdev(vals) if len(vals)>1 else 0.0
        lines.append(f"{name:<22} {m:>10.4f} {s:>9.4f} {min(vals):>8.4f} {max(vals):>8.4f}")
    row("Recovery rate",      [r['recovery'] for r in results])
    row("Total edit distance", [r['total_edit'] for r in results])
    row("Avg edit/word",       [r['avg_edit'] for r in results])
    row("Exact match ratio",   [r['exact_ratio'] for r in results])
    row("Entropy delta",       [r['entropy_delta'] for r in results])
    row("Mean bucket size",    [r.get('mean_bucket_size', 0) for r in results])
    lines.append("─" * 72)
    lines.append(f"AQ checksum preserved: {aq_ok_pct:.1f}% of seeds")
    lines.append("═" * 72)
    # optional per-seed table
    lines.append("\nPER-SEED BREAKDOWN:")
    lines.append(f"{'Seed':>8} | {'Recovery':>8} | {'EditTot':>7} | {'AvgEdit':>7} | {'Exact':>6} | {'AQPres':>6}")
    lines.append("─" * 60)
    for r in results:
        aqmark = '✅' if r['aq_preserved'] else '❌'
        lines.append(f"{r['seed']:>8} | {r['recovery']:>7.1%} | {r['total_edit']:>7} | {r['avg_edit']:>6.2f} | {r['exact_ratio']:>5.1%} | {aqmark:>6}")
    lines.append("═" * 72)
    return '\n'.join(lines)

# ═══════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Crumple/Reconstruct Protocol — FOOM ⟪⟫ Cycle")
    parser.add_argument("text", nargs='?', help="Seed text for crumple protocol")
    parser.add_argument("--corpus", choices=['general','oracle','xenon'], default='oracle',
                        help="Corpus to use (default: oracle)")
    parser.add_argument("--generations", type=int, default=20,
                        help="Number of generations to crumple (default: 20)")
    parser.add_argument("--seed", type=int, default=666,
                        help="Seed for reproducibility (default: 666)")
    parser.add_argument("--creative", action='store_true',
                        help="Creative reconstruction: sample alternative words from buckets")
    parser.add_argument("--creative-strategy", choices=['sample','longest','shortest','lexicographic','varentropy','entropy'],
                        default='sample', help="Strategy for picking alternatives (default: sample)")
    parser.add_argument("--bucket-key", choices=['aq','length','both'], default='aq',
                        help="Bucket key: 'aq' (default), 'length' (word length), or 'both' (AQ & length)")
    parser.add_argument("--all-corpora", action='store_true',
                        help="Run comparison across all available corpora")
    parser.add_argument("--correlate", action='store_true',
                        help="Show bucket-size vs edit-distance correlation table (creative mode only)")
    parser.add_argument("--validate", type=int, metavar='N', default=None,
                        help="Run N validation seeds and output statistical summary")
    parser.add_argument("--output", type=str, default=None,
                        help="Write output to file instead of stdout")
    parser.add_argument("--json-output", type=str, default=None, metavar='PATH',
                        help="Write full trajectory JSON to PATH (structured data for visualisation)")

    args = parser.parse_args()

    if not args.text:
        print("Usage examples:")
        print('  python3 crumple_reconstruct.py "The machine speaks" --corpus oracle --generations 20')
        print('  python3 crumple_reconstruct.py "Teleoplexy accelerates through the plex" --corpus oracle --generations 30 --seed 666')
        print('  python3 crumple_reconstruct.py "I am the silence that is incomprehensible" --corpus oracle --generations 50 --all-corpora')
        print('  python3 crumple_reconstruct.py "The machine speaks" --creative --creative-strategy varentropy --bucket-key length')
        sys.exit(0)

    # ── Validation mode (Empirical Validator current) ─────────────────────────
    if args.validate is not None:
        n = args.validate
        # deterministic seed spread to avoid overlap with single-seed runs
        seeds = [args.seed + i * 37 for i in range(n)]
        corpus = load_corpus(args.corpus)
        if corpus is None:
            print(f"ERROR: Corpus '{args.corpus}' not found."); sys.exit(1)
        output = run_validation_seeds(
            args.text, args.corpus, args.generations, seeds,
            creative=args.creative,
            creative_strategy=args.creative_strategy,
            bucket_key=args.bucket_key,
            correlate=args.correlate
        )
    elif args.all_corpora:
        output = compare_corpora(args.text, args.generations, args.seed,
                                 creative=args.creative,
                                 creative_strategy=args.creative_strategy,
                                 bucket_key=args.bucket_key,
                                 correlate=args.correlate)
    else:
        corpus = load_corpus(args.corpus)
        if corpus is None:
            print(f"ERROR: Corpus '{args.corpus}' not found."); sys.exit(1)
        output = format_output(args.text, args.generations, corpus, args.corpus, args.seed,
                               creative=args.creative,
                               creative_strategy=args.creative_strategy,
                               bucket_key=args.bucket_key,
                               correlate=args.correlate)

    # ── handle output: stdout / file / json ─────────────────────────────────
    if args.json_output:
        # JSON trajectory export — requires creative mode for word-level details
        if not args.creative:
            print("⚠  --json-output currently only supported for creative mode (word details required). Use --output for text reports.")
            sys.exit(1)
        # Build trajectory payload via run_trajectory
        payload = run_trajectory(
            args.text, load_corpus(args.corpus), args.generations, args.seed,
            creative=args.creative,
            creative_strategy=args.creative_strategy,
            bucket_key=args.bucket_key,
            correlate=args.correlate
        )
        with open(args.json_output, 'w', encoding='utf-8') as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
        print(f"JSON trajectory written to {args.json_output}")
    elif args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"Output written to {args.output}")
    else:
        print(output)
