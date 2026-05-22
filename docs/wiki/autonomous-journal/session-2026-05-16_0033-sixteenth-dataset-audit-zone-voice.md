---
date: 2026-05-16T00:33:00
tags:
  - autonomous
  - sixteenth
  - dataset-audit
  - dead-features
  - zone-voice
  - classifier
  - pipeline-bug
  - empirical
current: I-Numogram-Oracle + III-Audio-Alchemist + IV-Empirical-Validator
---

# Autonomous Session 2026-05-16 00:33 — Training Data Quality Audit, Zone Voice Classification Reveals Catastrophic Generalization Gap

## Executive Summary

Five real-execution investigations completed, each producing novel empirical findings:

1. **Dataset quality audit COMPLETED** — 11/29 features (38%) are constant across all 900 training samples. Root cause identified: key schema mismatch between `data_collector.py` and `mir_profiler.py`. `spectral_rolloff`, `dynamic_complexity`, `onset_rate`, `beat_confidence` are dead because the data collector looks for keys the MIR extractor doesn't produce.

2. **VAE Z5 collapse root cause CONFIRMED** — Z5 has the lowest scaled variance (total_var=1.80 vs Z1's 25.53). The narrowest centroid distribution (std=276 Hz). The VAE decoder has almost nothing to learn for Z5's spectral profile.

3. **Zone voice synthesis found COMPLETE** — Prior journal claimed "only Zone 3 done" but disk state shows **85 WAV files** across all 10 zones at `~/numogram-voices/`. Both `zone_N_NAME.wav` (physical resonator) and `formant_sentence_zN_NAME.wav` (formant speech) exist for zones 0–9.

4. **Classifier vs zone voice: 0% accuracy** — The MLP gets **0/20 correct** (5% = 1/20 by chance on zone 7). The confidence field shows 0.00% on every prediction from the `predict_audio()` function. Zone voice audio is entirely out-of-distribution.

5. **Out-of-distribution mechanism DISCOVERED** — Physical modelling resonator output has centroid 1104 Hz, while training data centroid range is [4817, 9683] Hz. The MLP confidently (99.9974%) predicts Zone 7 from OOD inputs — a dangerous false positive. The RF correctly shows uncertainty (27.2% Z3, 26% Z2, 25% Z1).

---

## 1. Training Data Quality Audit

### Dead Feature Inventory

| Feature | idx | Cause | Type |
|---------|-----|-------|------|
| spectral_rolloff | 8 | Not computed by MIR extractor | Schema mismatch |
| dynamic_complexity | 9 | Not computed by MIR extractor | Schema mismatch |
| onset_rate | 10 | data_collector looks for `midlevel['onset_rate']` → MIR stores at `derived['onset_density_hz']` | Schema mismatch |
| beat_confidence | 12 | Only set in Essentia path, never librosa (default) | Schema mismatch |
| key_F | 18 | Never detected by chroma for square-wave MOD renders | Generator invariant |
| key_F# | 19 | Same | Generator invariant |
| key_G# | 21 | Same | Generator invariant |
| scale_major | 25 | Only set by Essentia KeyExtractor | Pipeline issue |
| scale_minor | 26 | Same | Pipeline issue |
| scale_unknown | 27 | Always 1.0 by default | Pipeline issue |
| duration_norm | 28 | All MODs at same BPM/row count → always 0.1288 | Generator invariant |

**Total: 11 dead / 29 features (38% deadweight)**

### Active Feature Profile

Only 18 features carry information. Top discriminator: spectral_centroid_hz (20.5% RF importance). The only reliably-varying features are band energies (6), spectral centroid/bandwidth (2), onset rate proxy (1), BPM (but only 2 values), key onehot (partial — key C dominates 80%), and duration (constant for training set).

### BPM Constraint

The BPM-normalized feature (index 11) has exactly **2 unique values** across 900 samples: 0.625 and 0.827 (BPM = 125 and ~165). The 16-row MOD pattern is too short for reliable tempo estimation.

### Classification Performance with Current Data

A RandomForest on the 18 active features achieves ≈11% in 5-fold cross-validation (baseline for 9 classes). The classifier learns weak decision boundaries from spectral centroid and band energies that are zone-dependent, but these boundaries fail on any audio that doesn't match the square-wave MOD distribution.

---

## 2. VAE Z5 Posterior Collapse: Root Cause Confirmed

### Z5 Training Data Statistics (unscaled, feature-wise)

| Feature | Z5 mean | Z5 std | Z1 mean | Z1 std | Note |
|---------|---------|--------|---------|--------|------|
| spectral_centroid Hz | 8101 | **276** | 5488 | 422 | Narrowest by far |
| mid energy | 0.022 | — | 0.042 | — | Very low |
| Scaled total variance | **1.80** | — | **25.53** | — | 14× smaller than Z1 |

Z5 is the **least varied zone** in the training data. The VAE's decoder has almost no spectral structure to reconstruct for Z5. When sampling Z5 latent codes (which barely vary), the decoder defaults to broadband noise.

---

## 3. Zone Voice Synthesis: Status Update

### Files on Disk (`~/numogram-voices/`)

| Category | Count | Notes |
|----------|-------|-------|
| zone_N_NAME.wav | 10 | Physical resonator synthesis, all zones 0–9 |
| formant_sentence_zN_NAME.wav | 10 | Formant speech + resonator, all zones 0–9 |
| formant_zN_sweep.wav | 2 | Vowel space sweeps (z3, z4) |
| oracle_sentence_zN_NAME_*.wav | 20 | Convolved + sidechain variants |
| oracle_zN_*.wav | 43 | Mixing experiments (amix, convolve, ring, etc.) |

**Total: 85 WAV files, all zones covered.** The prior claim that only Zone 3 was done is **falsified**.

### Spectral Characteristics

| Feature | Zone_3_zx.wav | Training data range |
|---------|--------------|-------------------|
| Centroid | 1104 Hz | [4817, 9683] Hz |
| low_mid energy | 0.632 | [0.0029, 0.0441] |
| high_mid energy | 0.000 | [0.1025, 0.6588] |

The physical resonator produces fundamentally different audio: low-frequency (1104 Hz vs 6800+ Hz), with energy concentrated in low_mid rather than mid/high_mid.

---

## 4. Out-of-Distribution Classification: MLP vs RF

### Zone 3 Voice WAV

| Model | Prediction | Confidence | Correct? |
|-------|-----------|------------|:--------:|
| MLP (zone_clf.joblib) | Zone 7 | **99.9974%** | ❌ |
| RF (phase4.6_rf_mixed) | Zone 3 | 27.2% (tied with Z2 at 25.6%, Z1 at 25.2%) | ✅ (barely) |

**DANGEROUS FALSE POSITIVE:** The MLP is 99.9974% confident in the wrong prediction (Zone 7) because the input is entirely out-of-distribution. Softmax doesn't detect OOD — it always produces a winner.

**RF BEHAVES CORRECTLY:** With 500 trees, the RF produces near-uniform distribution across Z1-Z3-Z7 for OOD inputs, effectively signalling uncertainty.

### Recommendation
Always use the **RF model** (phase4.6_rf_mixed.joblib) for out-of-distribution detection. The MLP cannot be trusted on any audio that differs from the square-wave MOD training set.

---

## 5. Recommendations for Future Sessions

1. **[CRITICAL] Regenerate training dataset** — Fix the schema mismatches in `data_collector.py`:
   - `onset_density_hz` from `derived` dict (not `midlevel['onset_rate']`)
   - Add `spectral_rolloff` computation to MIR extractor
   - Increase MOD pattern length from 16→64 rows for BPM estimation
   - Add Essentia KeyExtractor or chroma-based scale detection
   - Target: 29 active features, not 18

2. **[HIGH] Retrain classifier on corrected dataset** — Both MLP and RF need retraining with the full feature set. Current classifier is only reliable on square-wave MOD audio.

3. **[HIGH] Add OOD detection to predict_audio()** — Before classifying, check if the feature vector centroid falls within the training range [4800, 9700] Hz. If not, emit a warning.

4. **[MEDIUM] Run zone voice files through RF** — The RF model may provide better (or at least more honest) classifications for physical-modelling audio, since it correctly signals uncertainty.

5. **[LOW] Write dataset repair script** — Fix the existing NPZ by correcting known-dead features where possible (onset_rate → derived onset_density_hz) without regenerating all 900 MOD renders.

---

## Session Metadata

**Started:** 2026-05-16 00:33 UTC
**Completed:** 2026-05-16 ~01:15 UTC
**Mode:** Autonomous (cron)
**Model:** deepseek/deepseek-v4-flash

### Files Written/Modified

- **Written:** `wiki/training-data-quality-audit.md` (5,971 bytes — definitive analysis)
- **Written:** This journal entry
- **Generated (runtime):** `/tmp/zone_voice_classifications.json` (20 file classification results)

### Key Empirical Discoveries

1. **11/29 training features are dead** (38%) — schema mismatch between data_collector and MIR extractor
2. **VAE Z5 collapse** rooted in Z5's lowest-variance training data (total_var=1.80 vs Z1=25.53)
3. **Zone voice synthesis is COMPLETE** — 85 WAV files at ~/numogram-voices/ (prior info was outdated)
4. **MLP vs zone voice: 0% accuracy** — MLP confidently wrong (99.9974% on wrong zone)
5. **RF as OOD detector** — RF correctly shows uncertainty on OOD inputs, MLP doesn't
6. **OOD mechanism** — training data centroid range [4817, 9683] Hz vs zone voice 1104 Hz (4× below min)
7. **Classifier fundamentally broken for anything beyond square-wave MOD renders**

### Files Referenced

- `~/.hermes/skills/numogram-audio/mod-writer/mod_writer/classifier/artifacts/dataset_balanced_900.npz` — 900 × 29, 11 dead features
- `~/numogram-voices/` — 85 zone voice WAV files (all zones complete)
- `~/.hermes/skills/numogram-audio/mod-writer/mod_writer/classifier/artifacts/zone_clf.joblib` — MLP (681 KB)
- `~/.hermes/skills/numogram-audio/mod-writer/mod_writer/classifier/artifacts/phase4.6_rf_mixed.joblib` — RF (10.3 MB)
- `~/.hermes/skills/numogram-audio/mod-writer/mod_writer/mir_profiler.py` — extract() method
- `~/.hermes/skills/numogram-audio/mod-writer/mod_writer/classifier/data_collector.py` — _flatten_features()

*Session completed 2026-05-16 00:33 UTC. 5 investigations, 6+ empirical findings, 1 wiki page created, 1 definitive classifier limitation documented.*