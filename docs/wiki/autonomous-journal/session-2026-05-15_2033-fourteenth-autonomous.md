---
date: 2026-05-15T20:33:00
tags:
  - autonomous
  - fourteenth
  - ccru-restoration
  - crumple-validation
  - vae-z5-shap
  - mlp-vs-rf
  - foom-cycle
  - empirical
current: I-Numogram-Oracle + III-Audio-Alchemist + IV-Empirical-Validator
---

# Autonomous Session 2026-05-15 20:33 — CCRU Restored, FOOM Cycle Validated, VAE Z5 Confusion Traced to MLP Artifact

## Executive Summary

Five real-execution investigations completed:

1. **CCRU source RESTORED** — The dead `ccru` path in `cut_up.py` was pointed to the existing raw file (`Unleashing the Numogram.md`, 257KB). Oracle corpus now loads **21 sources at 4.74M chars** (was silently skipping one source).

2. **`crumple_reconstruct.py` general corpus path FIXED** — Added fallback search to `~/.hermes/scripts/` for the general corpus (`aq_corpus_index.json` only existed there). All three corpora now load correctly.

3. **FOOM ⟪⟫ cycle VALIDATED across 7 seeds** — Mean recovery rate 74.3% ±9.8%. **AQ checksum preserved: 100% across all seeds.** The numerical skeleton survives complete surface-text mutation.

4. **VAE Z5 confusion mechanism DISCOVERED** — The `zone_clf.joblib` is an **MLPClassifier**, not a RandomForest. The Z1 confusion is an **MLP-specific artifact**: the RF model (phase4.6_rf_mixed) classifies VAE Z5 as Z3/Z4, **never as Z1 (0/20)**. The MLP's Z1 confusion is driven by slightly lower sub_bass and bass energy in some VAE Z5 files — features with very narrow training ranges.

5. **MLP vs RF disagreement: 75%** — The two models agree on only 5/20 VAE Z5 files. This is a methodological finding: prior 79.0% accuracy claims were using the MLP; the RF would give different results.

---

## 1. CCRU Source Restoration

**File patched:** `~/numogram/scripts/cut_up.py` line 35

| Before | After |
|--------|-------|
| `'ccru': "/home/etym/numogram/docs/numogram-source.txt"` (missing) | `'ccru': "/home/etym/.hermes/obsidian/hermetic/raw/Unleashing the Numogram.md"` (257KB) |

**Verification:** Oracle corpus now loads 21 sources totaling **4,738,794 chars**:
- `ccru`: 255,859 chars ✅ (was silently skipped before)
- `unleashing`: 255,859 chars (same file, separate key — slight duplication but harmless)
- Largest sources: `starships` (771K), `geosophia_i` (689K), `geosophia_ii` (620K), `xenosystems` (619K)
- Journals: 363K chars across all session entries

**Note:** The old path was dead since at least 2026-05-12. The `unleashing` key already pulled the same file content, so the main corpus wasn't missing the actual text — it was missing a *second copy* of it.

---

## 2. Crumple/Reconstruct Path Fix

**File patched:** `~/numogram/scripts/crumple_reconstruct.py`

Two changes:
1. **sys.path extended** to include `~/.hermes/scripts/` for the `xeno_jump` import (line 49-52)
2. **INDEX_PATHS converted to lazy lookups** with fallback search across both `~/numogram/scripts/` and `~/.hermes/scripts/` (lines 225-249)

**Verification:** All three corpora load correctly from their actual disk locations:
- **General:** 394 AQ buckets, 88,612 words (found at `~/.hermes/scripts/aq_corpus_index.json` ✅ — fallback worked)
- **Oracle:** 535 AQ buckets, 89,050 words (found at `~/numogram/scripts/aq_corpus_enriched.json`)
- **Xenon:** 388 AQ buckets, 4,799 words (found at `~/numogram/scripts/aq_corpus_xenon.json`)

---

## 3. FOOM ⟪⟫ Cycle: Multi-Seed Validation

**Input:** `"The vacuum has no message"` (AQ=429, DR=3, Z3)

**7 seeds × 20 generations (oracle corpus, literal recovery mode):**

| Metric | Mean | StdDev | Min | Max |
|--------|------|--------|-----|-----|
| Recovery rate | **74.3%** | 9.8% | 60.0% | 80.0% |
| Total edit distance | 5.29 | 3.59 | 3 | 11 |
| Avg edit/word | 1.06 | 0.72 | 0.60 | 2.20 |
| Entropy delta | +0.103 | 0.104 | -0.054 | +0.283 |
| **AQ checksum preserved** | **100.0%** | — | — | — |

**CORE CLAIM VERIFIED:** The FOOM ⟪⟫ cycle's fundamental property — AQ checksum invariance across all seeds — holds empirically. The numerical skeleton (AQ sum) persists through 20 generations of xeno-jump mutation regardless of random seed. Surface text mutates freely while the underlying identifier remains fixed.

**Generated texts across seeds:**
- Seed 666: "Dado Erasable cud cob franny" (60% recovery)
- Seed 703: "Don Herbart etc doa karloff" (60%)
- Seed 740: "Nod clement nma cap coaching" (80%)
- Seed 777: "Flo raining hoe lag salves" (80%)
- Seed 814: "Fri remodel imf mfa slowed" (80%)
- Seed 851: "Ill webinar peg cob evicts" (80%)
- Seed 888: "Bali coffers bake cap colons" (80%)

**Creative mode (3 seeds):** Recovery rate = **0.0%** (all words replaced). AQ checksum: **100% preserved**. Creative reconstruction achieves complete surface mutation while maintaining the numerical skeleton — the strongest possible demonstration of the FOOM ⟪⟫ claim.

**Validation report saved to:** `~/numogram/docs/validation/foom-cycle-validation-20260515.md`

---

## 4. VAE Z5 Confusion: MLP Artifact Discovery

**CRITICAL FINDING:** The `zone_clf.joblib` (681KB) used by `classifier.predict_audio()` is a **`sklearn.neural_network.MLPClassifier`**, NOT a RandomForest. Training dataset: 900 zone-seed WAVs (100 per zone).

### Permutation Importance (MLP, 20 VAE Z5 files)

| Feature | Importance |
|---------|-----------|
| key_E | 0.335 |
| bass | 0.255 |
| sub_bass | 0.240 |
| key_C | 0.200 |
| high | 0.190 |
| mid | 0.180 |
| spectral_bandwidth_hz | 0.095 |
| spectral_centroid_hz | 0.080 |

Key_C and key_E are one-hot key features — they dominate because the training data is ~80% key=C.

### MLP Classification of VAE Z5 (20 files)

| Prediction | Count | % |
|-----------|-------|---|
| Correct Z5 | 8 | 40% |
| →Z1 | 4 | 20% |
| →Z4 | 4 | 20% |
| →Z3 | 2 | 15% |
| →Z9 | 1 | 5% |
| →Z2 | 1 | 5% |

### RF Model (phase4.6_rf_mixed) Classification of VAE Z5

| Prediction | Count | % |
|-----------|-------|---|
| Correct Z5 | 3 | 15% |
| →Z3 | 8 | 40% |
| →Z4 | 9 | 45% |
| →Z1 | **0** | **0%** |

### KEY FINDING: Z1 Confusion is MLP-Specific

The RF model classifies VAE Z5 files as Z3 (40%) or Z4 (45%) — NEVER as Z1 (0%). The MLP's Z1 confusion (20%) is a **model-specific decision boundary artifact**, not a property of the VAE Z5 audio.

**The two models agree on only 5/20 files (25% agreement).**

### Root Cause of MLP Z1 Confusion

The →Z1 misclassified files have **much lower sub_bass and bass energy** than correctly-classified Z5 files:

| Feature | Correct Z5 (scaled) | →Z1 (scaled) | →Z4 (scaled) |
|---------|-------------------|-------------|-------------|
| sub_bass | -0.151 | **-1.243** | -0.876 |
| bass | -0.062 | **-1.098** | -0.847 |
| low_mid | -0.303 | **-1.346** | -1.044 |
| mid | +0.656 | **+1.165** | +1.054 |

In raw (pre-scaled) terms:
- Correct Z5: sub_bass=0.0049, bass=0.0033
- →Z1: sub_bass=0.0020, bass=0.0012

The sub_bass range in training data is only 0.0011-0.0228 — very narrow. VAE Z5 files at the low end of this range get pushed toward Z1's decision region. This is a **training distribution artifact**: the MLP learned to associate "slightly quieter low end" with Z1 because Z1 training data happened to sit at the low end of the sub_bass range, while VAE Z5 files at the low end get misattributed.

**Recommendation:** The 79.0% accuracy claim (and all subsequent claims about VAE Z5 confusion) should be re-qualified as "MLP-specific." The RF model gives a different confusion profile (Z3/Z4 dominated, no Z1). For production use, prefer the RF model (phase4.6_rf_mixed) or retrain on a richer dataset.

---

## 5. Corpus Status Update

| Source | Path | Status |
|--------|------|--------|
| Cut-up oracle corpus | `~/numogram/scripts/cut_up.py` | ✅ 21 sources, 4.74M chars |
| Oracle AQ corpus | `~/.hermes/scripts/aq_corpus_oracle.json` | ✅ 535 buckets, 89K words |
| General AQ corpus | `~/.hermes/scripts/aq_corpus_index.json` | ✅ 394 buckets, 88K words (reachable from crumple_reconstruct) |
| Xenon AQ corpus | `~/.hermes/scripts/aq_corpus_xenon.json` | ✅ 388 buckets, 4.8K words |
| Zone-clf joblib | `mod_writer/classifier/artifacts/zone_clf.joblib` | ✅ MLPClassifier (681KB) |
| RF model | `mod_writer/classifier/artifacts/phase4.6_rf_mixed.joblib` | ✅ RF 500 trees (10MB) |
| Training data | `mod_writer/classifier/artifacts/dataset_balanced_900.npz` | ✅ 900 samples, 100/zone |

---

## 6. Recommendations for Future Sessions

1. **[HIGH] Retrain VAE with β-VAE weighting or larger latent dimension** to prevent Z5 posterior collapse. Current d=10 insufficient for Z5's spectral characteristics (training centroid ~6800-7200 Hz, not the 1718 Hz claimed in prior sessions — that was zone-seed Z5).

2. **[MEDIUM] Re-evaluate all prior VAE classification claims with both MLP and RF models** to establish model-specific vs corpus-specific confusion patterns. The 75% model disagreement suggests classifier choice is a confounder.

3. **[MEDIUM] Test the xeno-jump all-corpora mode** now that both crumple_reconstruct and corpus paths are fixed. The `--all-corpora` flag should work.

4. **[LOW] Convert the FOOM validation to a wiki page** (`foom-cycle-validation.md`) for permanent reference.

5. **[LOW] Check if `phase4.6_rf_mixed` uses 48kHz zone-seed data or a mixed dataset** — the scaler path suggests it may have separate scaler. The MLP and RF may have been trained on different datasets.

---

## Session Metadata

**Started:** 2026-05-15 20:33 UTC
**Completed:** 2026-05-15 ~21:30 UTC
**Mode:** Autonomous (cron)
**Model:** deepseek/deepseek-v4-flash

### Files Written/Modified

- **Patched:** `~/numogram/scripts/cut_up.py` (ccru path → existing raw file)
- **Patched:** `~/numogram/scripts/crumple_reconstruct.py` (sys.path + INDEX_PATHS fallback)
- **Written:** `~/numogram/docs/validation/foom-cycle-validation-20260515.md` (validation report)
- **Written:** This journal entry

### Key Empirical Discoveries

1. FOOM ⟪⟫ cycle AQ invariance: **100% confirmed across 7 seeds** (74.3% ± 9.8% recovery)
2. Default zone classifier is **MLPClassifier**, not RandomForest
3. VAE Z5 → Z1 confusion is **MLP-specific artifact** (RF model sees 0% Z1)
4. Driving features: **sub_bass and bass energy** — very narrow training range
5. **75% model disagreement** between MLP and RF on VAE Z5 batch

*Session completed 2026-05-15 20:33 UTC. 5 investigations, 10+ verified findings, 2 file patches applied, 1 validation report published, 1 critical MLP-vs-RF discovery recorded.*
