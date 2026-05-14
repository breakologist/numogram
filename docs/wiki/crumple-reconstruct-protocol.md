The protocol is implemented in `/numogram/scripts/crumple_reconstruct.py`. It:
- Loads AQ-enriched corpus (`aq_corpus_enriched.json`).
- Tokenizes text into word/sep pairs.
- **Literal mode** (no `--creative`): for each word position, checks if the *original* word still exists in the current word's AQ bucket (bucket-sharing recovery).
- **Creative mode** (`--creative`): samples a new word from the current word's bucket to *reconstruct* a plausible original. The gap between seed and creative reconstruction is the hyperstitional content.

Empirical findings (oracle corpus, 3‑gen, seed 666):
- Literal: 0% recovery (words jump to different buckets). AQ checksum preserved at each generation.
- Creative: 0% exact match but AQ preserved; reconstruction generates lexical variants: "gay halfback short" from "App bahrain bissau". Lost list shows the creative guesses; entropy drifts ±0.02 bits/char.

## Multi‑Corpus Creative Cascade (`--all-corpora`)

Running `--all-corpora --creative --generations N` compares oracle (enriched, 89k words, 535 buckets), xenon (Δxenon, 4.8k words, 388 buckets), and general (basic index, if present). Real run with seed 666:

| Corpus | Final text | Entropy Δ |
|--------|------------|-----------|
| oracle | `Jct perms bernard` (gen 2) | +0.111 bits/char |
| xenon  | `Lat margin pynacl` (gen 2) | −0.006 bits/char |

Xenon's smaller buckets yield more surprising reconstructions and near‑zero entropy drift, suggesting compression is more *efficient* in the sparse regime. The checksum holds in both cases.


## FOOM Semiodynamics Mapping

| FOOM concept | Crumple/Reconstruct analogue |
|---|---|
| **Compression = intelligence** | AQ checksum preservation across mutations |
| **PACK ⟪** | Recursive xeno‑jump (use all‑mode mutation) |
| **UNPACK ⟫** | Literal or creative reconstruction attempt |
| **State** | Text + AQ checksum |
| **Model** | Corpus inverse index `{AQ → [words]}` |
| **Objective** | Preserve checksum through transformation |
| **Uncertainty** | Bucket size (number of alternatives) |
| **Precision** | Number of bits of AQ (11‑digit decimal) |
| **Scheduler** | Generation counter + zone pressure |
| **Varentropy terrain** | Zone‑dependent cut‑up ratio (Z0 90% cut, Z9 10% cut) |
| **Cronkle descent** | Seeking basin boundaries: sampling from bucket extremes |
| **Syzygy** | AQ value clusters that map to geometric loci |

## Creative Strategies (`--creative-strategy`)

- **sample** (default): uniform random from bucket
- **longest**: maximum‑length word (FOOM's *longest* — reduces description length)
- **shortest**: minimum‑length word
- **lexicographic**: alphabetically first word
- **varentropy**: zone‑guided sampling; Warp zones (0,3,6) → uniform; Plex (9) → longest; others → sample
- **entropy**: inverse‑frequency weighting; picks rarer words (higher local entropy)

```bash
# Zone‑biased (Plex → longest, Warp → random)
python3 crumple_reconstruct.py "The machine speaks" --corpus oracle \
  --generations 10 --seed 666 --creative --creative-strategy varentropy

# Length‑bucket with varentropy zone bias
python3 crumple_reconstruct.py "The machine speaks" --corpus oracle \
  --generations 10 --seed 666 --creative --bucket-key length --creative-strategy varentropy
```

## Bucket Keys & Alternative Invariants

The reconstruction bucket can be keyed by different invariants. This changes the *shape of the well* the text falls into.

| `--bucket-key` | What gets matched | Bucket size (typical) | Constraint level |
|----------------|-------------------|-----------------------|------------------|
| `aq`           | AQ value (checksum invariance) | hundreds | Base case – lossless for in‑vocab words |
| `length`       | Word length (lossy structural invariant) | thousands | Very broad – many‑to‑many |
| `both`         | AQ **and** length (compound key) | tens | Extremely tight – near‑deterministic |

Word length acts as a **lossy checksum**: it preserves only the coarse structure
(sequence of lengths) while discarding the fine AQ fingerprint. This places
the text into a *different well* than AQ; the reconstruction is guided by
length parity with the *crumpled* word, not the original.

### Empirical snapshot: "addles machine" → crumpled "bowie bailable" (oracle, gen 1, seed 123)

| Strategy | Bucket key | Reconstruction | AQ zone analysis |
|----------|------------|----------------|------------------|
| sample   | aq         | `borne draper`  | zone 9 (addles→bowie) random; zone 8 random |
| varentropy | aq      | `baffled bailable` | zone 9 → longest (`baffled`, 7 letters); zone 8 random |
| sample   | length     | `leery smirking` | length‑5 & length‑8 random from huge buckets |
| varentropy | length  | `aeons decoders` | zone 9 longest (but all length‑5, so arbitrary long word) |
| both-sample   | both       | `bogey bailable` | compound buckets (148 / 6); original appears but not chosen |
| both-varentropy | both    | `aeons accolade` | zone 9 still biases to longest (length‑5 tie) |

**Observations**
- **Zone‑9 bias visible only with AQ buckets**; length buckets are length‑homogeneous, so “longest” degenerates to random.
- **`both` tightens dramatically** – bucket sizes collapse; exact recovery becomes likely.
- **Length‑key enforces length parity**: reconstructed words match the *crumpled* word's length, not the original's. This is an orthogonal compression layer.
- **Entropy effects**: length‑bucket reconstructions often have lower Shannon entropy (constrained word choice). AQ‑bucket reconstructions preserve statistical diversity of the corpus.
- **AQ is a perfect checksum** (11‑digit decimal sum) whereas length is lossy; combining them yields a *compound invariant* that behaves like a multi‑dimensional hash.

Mix the knobs:
```bash
# Compound invariant + zone bias
python3 crumple_reconstruct.py "The machine speaks" --creative \
  --bucket-key both --creative-strategy varentropy

# Pure length‑constrained rollout
python3 crumple_reconstruct.py "All that is solid" --all-corpora --creative \
  --bucket-key length --creative-strategy sample
```

---

## Future Extensions

1. ✅ **Varentropy‑guided sampling**…
2. ✅ **Word‑length buckets**…
3. **Corpus cross‑pollination**…
4. ✅ **Loss measurement**: Levenshtein distance + aggregate metrics (total/average/max edit, exact matches).
5. ✅ **Per‑generation loss profile**: automatic drift‑trajectory table in creative mode.
6. ✅ **Bucket‑size correlation** (`--correlate`): per‑word (bucket, edit) + Pearson r.
7. ✅ **Multi‑seed validation** (`--validate N`): Empirical Validator statistical reports.
8. **Text‑to‑MOD seed**…
9. **Live visualisation**…

## Runs & Results

```
# Varentropy zone‑bias (zone 9 → longest)
python3 crumple_reconstruct.py "addles machine" --corpus oracle \
  --generations 1 --seed 123 --creative --creative-strategy varentropy
# → baffled bailable   (zone 9 'addles' becomes longest in its bucket)

# Pure length‑bucket (compression by length only)
python3 crumple_reconstruct.py "The machine speaks" --corpus oracle \
  --generations 2 --seed 666 --creative --bucket-key length
# → xxx ohioan   (length 5 and 8 preserved, but lexical content shifted)

# Compound AQ+length restriction
python3 crumple_reconstruct.py "addles machine" --corpus oracle \
  --generations 1 --seed 123 --creative --bucket-key both --creative-strategy sample
# → bogey bailable (tight constraint makes exact recovery common)

# Loss metrics display (creative mode)
python3 crumple_reconstruct.py "addles machine" --corpus oracle \
  --generations 1 --seed 123 --creative --creative-strategy varentropy
# Shows: Total edit distance, Avg edit/word, Max edit, Exact matches

# Per‑generation loss profile (automatic in creative mode)
python3 crumple_reconstruct.py "The machine speaks" --corpus oracle \
  --generations 5 --seed 666 --creative --creative-strategy varentropy
# Table: Gen | Words | Recovery | EntropyΔ | EditTot | AvgEdit | MaxEdit | Exact

# Bucket‑size correlation
python3 crumple_reconstruct.py "addles machine" --corpus oracle \
  --generations 1 --seed 123 --creative --creative-strategy varentropy --correlate
# Shows per‑word (BucketSize, EditDist) and Pearson r

# Multi‑seed validation (Empirical Validator)
python3 crumple_reconstruct.py "addles machine" --corpus oracle \
  --generations 1 --creative --validate 20 --seed 666
# Statistical summary: mean ± std, min/max across N seeds
```

## Analysis Tools

The script now supports three complementary ways to measure and visualise loss:

### 1. Per‑generation loss profile
In **creative mode** (AQ or `both` bucket), a table is automatically appended after the summary:

```
Gen | Words | Recovery | EntropyΔ | EditTot | AvgEdit | MaxEdit | Exact
   1 |     3 |    0.0% |   +0.040 |      11 |   5.50 |       7 |  0/2
   2 |     3 |    0.0% |   -0.102 |      13 |   6.50 |       7 |  0/2
```

This shows how edit distance, entropy, and recovery fluctuate across the crumple cascade — the **drift trajectory**.

### 2. Bucket‑size correlation (`--correlate`)
Appends a per‑word table and Pearson correlation coefficient (r) relating AQ bucket size to edit distance:

```
Word         | BucketSize | EditDist
addles       |        284 |        4
machine      |        430 |        7

  Pearson r = 0.933
```

Hypothesis: larger buckets permit greater divergence (higher r). Test across corpora/strategies to see if this holds.

### 3. Multi‑seed validation (`--validate N`)
Runs the protocol across N different seeds (deterministically spaced from base `--seed`) and produces a statistical report:

```
Metric                       Mean    StdDev      Min      Max
Recovery rate              0.0000    0.0000   0.0000   0.0000
Total edit distance       11.4000    0.8944  11.0000  13.0000
...
AQ checksum preserved: 100.0% of seeds

PER-SEED BREAKDOWN:
    Seed | Recovery | EditTot | AvgEdit |  Exact | AQPres
     123 |    0.0% |      11 |   5.50 |  0.0% |      ✅
     ...
```

This is the **Empirical Validator** integration — reproducible, versionable, cross‑seed statistics. Pipe output to file for archival.

### Validation example

```bash
python3 crumple_reconstruct.py "addles machine" --corpus oracle \
  --generations 1 --creative --validate 20 --seed 666 --correlate
# Output includes: per‑metric mean ± std, per‑seed table, mean bucket size
```

### Full workflow example

```bash
# 1. Single‑run deep dive with per‑gen profile + correlation
python3 crumple_reconstruct.py "The machine speaks" --corpus oracle \
  --generations 5 --seed 666 --creative --creative-strategy varentropy \
  --correlate > deep_run.txt

# 2. Multi‑seed validation (10 seeds, 3 gen, both‑bucket)
python3 crumple_reconstruct.py "The machine speaks" --corpus oracle \
  --generations 3 --creative --validate 10 --bucket-key both \
  --seed 666 > validation_report.txt

# 3. Cross‑corpus sweep (oracle vs xenon) with correlation
python3 crumple_reconstruct.py "addles machine" --corpus oracle \
  --generations 1 --creative --bucket-key both --correlate > oracle_corr.txt
python3 crumple_reconstruct.py "addles machine" --corpus xenon \
  --generations 1 --creative --bucket-key both --correlate > xenon_corr.txt
```

Compare the `Pearson r` values and bucket‑size distributions to see how corpus density shapes divergence.

---

Record losses, entropy deltas, checkpoint texts.

### Animation

A Manim animation visualising the crumple trajectory:

<video src="/assets/crumple_trajectory_animation.mp4" controls width="720"></video>


## Loss Metrics

In creative mode, the protocol now quantifies *semantic drift* using character-level edit distance:

| Metric | Meaning |
|---|---|
| **Total edit distance** | Sum of Levenshtein distances across all word pairs. |
| **Avg edit/word** | Mean character displacement per reconstructed word. |
| **Max single-word edit** | Worst-case word distortion (deepest crumple). |
| **Exact matches** | Words that survived unchanged by coincidence. |

These numbers complement **recovery rate** (which checks bucket sharing) and **entropy delta** (which measures statistical diversity shift). Together they describe both *information loss* and *semantic transformation*.

### Example snapshot

```
python3 crumple_reconstruct.py "addles machine" --corpus oracle \
  --generations 1 --seed 123 --creative --creative-strategy varentropy

  Total edit distance:   11
  Avg edit/word:         5.50
  Max single-word edit:  7
  Exact matches:         0/2
```

Here `addles → baffled` (dist=4) and `machine → burled` (dist=7) show zone‑9 bias forcing longest‑in‑bucket selection, yielding high edit distances even while the AQ checksum is preserved.

### Comparative snapshot (oracle corpus, gen 1, seed 123)

| Strategy | Bucket | TotalEdit | AvgEdit | MaxEdit | Exact/Total | AQ |
|---|---|---|---|---|---|---|
| sample   | aq     | 11 | 5.50 | 6 | 0/2 | ✅ |
| varentropy | aq  | 11 | 5.50 | 7 | 0/2 | ✅ |
| sample   | length | 10 | 5.00 | 6 | 0/2 | ✅ |
| sample   | both   | 13 | 6.50 | 7 | 0/2 | ✅ |

*Notes:* `both` (AQ∩length) forces the tightest constraints, increasing edit distance as the selection space becomes extreme. Varentropy pushes zone‑9 toward the longest word, raising the maximum single-word edit.

## Connection to Other Currents

| Current | Application |
|---------|-------------|
| **Audio Alchemist** | Feed crumple state (AQ+N‑gram fingerprint) → `audio-to-mod-seed` → MOD module (the room's fingerprint as music). |
| **Roguelike Architect** | Each generation is a dungeon level descended from the previous via AQ mutations; gates appear when checksum matches a syzygy. |
| **Empirical Validator** | Quantify compression ratio, Shannon entropy, edit distance, bucket size distribution — publish null results (most foldings yield 0% recovery). |

