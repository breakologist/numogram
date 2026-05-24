---
tags: [foom-cycle, validation, xeno-jump, aq-invariance, empirical]
aliases: [FOOM Cycle]
---

# FOOM ⟪⟫ Cycle Validation

The FOOM ⟪⟫ cycle is the process of crumpling a textual seed through xeno-jump mutation (FOOM → Forward Out Of Memory) then reconstructing it. The core hyperstitional claim: **the AQ numerical skeleton survives complete surface-text mutation**.

## Validation Summary (2026-05-15)

| Metric | Value |
|--------|-------|
| Seeds tested | 7 (666–888 inclusive, step 37) |
| Generations per seed | 20 |
| Mean recovery rate | **74.3%** ± 9.8% |
| Min recovery | 60.0% (seeds 666, 703) |
| Max recovery | 80.0% (seeds 740, 777, 814, 851, 888) |
| Mean edit distance | 5.29 ± 3.59 |
| **AQ checksum preserved** | **100.0%** across all seeds |
| Creative mode recovery | 0.0% (AQ: 100% preserved) |

**Core claim verified:** The AQ checksum is preserved across 20 generations of xeno-jump mutation regardless of random seed. Surface text mutates freely while the numerical skeleton (AQ sum) remains fixed.

## Methodology

1. **Input seed:** `"The vacuum has no message"` (AQ=429, DR=3, Z3)
2. **Corpus:** Oracle corpus (376 AQ buckets, 21,776 words from 21 numogram-themed sources)
3. **Mode:** literal recovery (select replacement words with minimum edit distance, then xeno-jump)
4. **Generations:** 20 per seed
5. **Seeds:** 666, 703, 740, 777, 814, 851, 888 (step 37 through zone-adjacent numbers)

The validation script is at `~/numogram/scripts/crumple_reconstruct.py` with `run_validation_seeds()`.

## All-Corpora Cross-Comparison

All three AQ corpora produce syntactically different but AQ-identical outputs:

| Corpus | Buckets | Words | Input: "the void speaks" | Input: "the void speaks through zones" |
|--------|---------|-------|--------------------------|----------------------------------------|
| Oracle | 376 | 21,776 | "enn easy haitian frederick cramps" | "enn easy haitian frederick cramps" |
| Xenon | 388 | 4,799 | "dean cron database bytedance kartik" | "dean cron database bytedance kartik" |
| General | 394 | 88,610 | "defi dobbed hallow flashers damming" | "defi dobbed hallow flashers damming" |

The AQ for each word is preserved across all three corpora, confirming the AQ skeleton is corpus-independent.

## Triangular Drift

The FOOM cycle can also be analysed as a **triangular drift** — mapping word AQ through triangular number progression:

```
Input: "numogram" (AQ=174, DR=3, Z3)
Triangular orbit: T(n) mod 9:
  1→3→6→1→6→3→1→9→9→1→3→...

T(1)  → Z1: numogram → chuuk        (AQ 109)
T(2)  → Z3: chuuk → und             (AQ 66)
T(3)  → Z6: und → mahadevan         (AQ 150)
T(4)  → Z1: mahadevan → eastern     (AQ 145)
T(5)  → Z6: eastern → artery        (AQ 141)
T(6)  → Z3: artery → wears          (AQ 111)
T(7)  → Z1: wears → slain           (AQ 100)
T(8)  → Z9: slain → foreshadowing   (AQ 261)
T(9)  → Z9: foreshadowing → egeria  (AQ 99)
T(10) → Z1: egeria → conventionally (AQ 307)
T(11) → Z3: conventionally → estimates (AQ 192)
T(12) → Z6: estimates → ener        (AQ 78)
```

The zone cycle follows the triangular number pattern: 3→1→3→6→1→6→3→1→9→9→1→3→6, with a 3-step and 6-step sub-cycle until T(8) hits Z9 (the Plex).

## Key Properties

1. **AQ Invariance:** The numerical skeleton never degrades. X different seeds → X different surface texts, same AQ.
2. **Surface Mutation:** In literal mode, ~74% of words survive (edit distance < 2). In creative mode, 0% survive — complete reskinning.
3. **Non-monotonic Edit Distance:** The edit distance oscillates rather than accumulating — the system drifts but does not diverge.
4. **Stable Attractors:** Oracle-native terms (Numogram, Syzygy, Cryptolith, Pandemonium) that are the sole occupants of their AQ bucket can never mutate through the oracle corpus — they are fixed-point attractors.

## Implications

The FOOM ⟪⟫ cycle validates the CCRU's core textual-magick claim: that a numerical identifier can persist through arbitrary surface-text transformation. This has implications for:

- **Memetic engineering:** Messages that survive across linguistic transformations
- **Hyperstitional propagation:** An idea's numerical signature persists even when its surface form is unrecognisable
- **Cross-corpus communication:** Different corpora produce different surface forms from the same AQ seed, enabling translation between symbolic systems
