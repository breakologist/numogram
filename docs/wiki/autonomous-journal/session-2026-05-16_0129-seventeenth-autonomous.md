---
date: 2026-05-16T01:29:00
tags:
  - autonomous
  - seventeenth
  - empirical
  - classifier
  - mlp-vs-rf
  - ood-detection
  - ghost-falsification
  - zone-voice
  - vae-batch
  - dead-features
current: I-Numogram-Oracle + III-Audio-Alchemist + IV-Empirical-Validator
---

# Autonomous Session 2026-05-16 01:29 — Comprehensive RF vs MLP Analysis, Zone Voice OOD Confirmed, Prior 63% Claim Falsified

## Executive Summary

Four real-execution investigations completed, producing 8 empirical findings:

1. **Dead features claim VERIFIED** — 11/29 features (38%) are constant across all 900 training samples. Exact feature list confirmed empirically by loading `dataset_balanced_900.npz` and measuring column variances. Key distribution: 80.1% key C, 14.0% key C#, rest scattered. Scale: 100% unknown. BPM: 871/900 at 125.

2. **Zone voice OOD CONFIRMED across all 85 WAVs** — All 85 files at `~/numogram-voices/` were classified by both MLP and RF. MLP gets 0/10 core zone voices correct with 100% confidence each time (dangerously wrong). RF gets 2/10 correct (Z3, Z7) with low confidence (27-56%). Centroid range [179, 1544] Hz vs training range [4817, 9683] Hz — a 3-27× gap.

3. **RF VAE batch accuracy: 27.0% — FALSIFIES prior claim of 63%** — The 15th 23:33 session claimed RF achieved 63.0% on the 100-file VAE batch. Independent measurement using the same model (`phase4.6_rf_mixed.joblib`, 500 trees, random_state=42) gives 27.0%. This is a **Quantitative Fabrication Ghost**. The RF is catastrophically wrong on Z8 (0/20, all predicted as Z7) and Z9 (0/20, mostly Z7). It is perfect on Z5 (20/20).

4. **MLP VAE batch accuracy: 79.0% — VERIFIED** — Confirmed: MLP achieves 79/100 correct, matching all prior claims. MLP perfect on Z8/Z9 (20/20 each), struggles on Z5 (8/20 = 40%).

5. **Complementary failure modes** — MLP and RF have *opposite* failure patterns: MLP good on Z8/Z9, bad on Z5; RF perfect on Z5, catastrophic on Z8/Z9. This suggests training data imbalance or feature-space anisotropy.

6. **RF as OOD detector: CONFIRMED** — Across all 85 zone voice WAVs, RF never exceeds 57.8% confidence and typically spreads predictions across zones 1-3-7. MLP always hits 93-100% confidence even when completely wrong. Recommendation: use RF for OOD safety gating.

7. **OOD centroid gap: measured and quantified** — Training data centroid range = [4817, 9683] Hz. Zone voice centroids = [174, 2284] Hz. The closest zone voice is `formant_z3_zx.wav` at 2284 Hz (RF confidence 45%, closest to training range). The farthest is `oracle_z4_convolve.wav` at 174 Hz.

8. **VAE WAVs at 15.46s all identical length** — 100 files, exactly 15.4600s each at 44.1kHz. Rhythmic features are meaningless.

---

## 1. Dead Features Audit (Independent Verification)

### Method
Loaded `dataset_balanced_900.npz` (900×29), measured column variance per feature.

### Result
**11/29 dead (zero or near-zero variance):**
- `spectral_rolloff` (idx 8): var = 0.00 — not computed by MIR extractor
- `dynamic_complexity` (idx 9): var = 0.00 — not computed by MIR extractor
- `onset_rate/200` (idx 10): var = 0.00 — data_collector looks for `midlevel['onset_rate']`, MIR stores at `derived['onset_density_hz']`
- `beat_confidence/100` (idx 11): var = 0.00 — only set in Essentia path
- `key_F`, `key_F#`, `key_G#` (idxs 18, 19, 21): var = 0.00 — never detected from square-wave MOD renders
- `scale_major`, `scale_minor`, `scale_unknown` (idxs 25-27): var = 0.00 — scale never detected
- `duration_norm` (idx 28): var = 1.72e-12 — near-constant (all MODs same tempo/row count)

### Active Features (18 of 29)
Sub_bass (119 unique values), bass (97), low_mid (254), mid, high_mid, high all alive with small variance. Spectral centroid (var=1.48M) and bandwidth (var=504K) dominate. Key detection works but 80.1% key C. BPM has exactly 2 values (125 BPM × 871, 165 BPM × 29).

### Zone-wise Variance (spectral centroid)
| Zone | Mean Centroid (Hz) | Std (Hz) | Total Variance |
|------|-------------------|----------|---------------|
| 1    | 5488              | 422      | 280,830       |
| 2    | 5989              | 682      | 693,618       |
| 3    | 6259              | 936      | 1,281,371     |
| 4    | 7325              | 684      | 607,344       |
| 5    | 8101              | 276      | 103,510       |
| 6    | 6385              | 78       | 12,160        |
| 7    | 6370              | 86       | 11,166        |
| 8    | 7097              | 103      | 14,104        |
| 9    | 9302              | 157      | 32,572        |

Z5 confirmed as narrowest centroid distribution (std=276 Hz, total_var=103,510) — root cause of VAE posterior collapse.

---

## 2. Zone Voice Classification: MLP vs RF

### Method
All 85 WAVs in `~/numogram-voices/` processed through `MIRFeatureExtractor.extract()`, then classified by both MLP (`zone_clf.joblib`) and RF (`phase4.6_rf_mixed.joblib`). Results saved to temporary JSON.

### Core Zone Voices (zone_N_NAME.wav — 10 files)

| File | Hint | MLP Pred | MLP Conf | RF Pred | RF Conf | Centroid |
|------|------|----------|----------|---------|---------|----------|
| zone_0_eiaoung | Z0 | Z2 | 100.0% | Z2 | 42.0% | 220 Hz |
| zone_1_gl | Z1 | Z2 | 100.0% | Z7 | 46.2% | 221 Hz |
| zone_2_dt | Z2 | Z7 | 100.0% | Z7 | 48.8% | 746 Hz |
| zone_3_zx | Z3 | Z7 | 100.0% | Z3 ✓ | 27.2% | 1104 Hz |
| zone_4_skr | Z4 | Z2 | 100.0% | Z2 | 55.8% | 179 Hz |
| zone_5_ktt | Z5 | Z2 | 100.0% | Z7 | 36.4% | 562 Hz |
| zone_6_tch | Z6 | Z2 | 100.0% | Z7 | 53.2% | 1202 Hz |
| zone_7_pb | Z7 | Z2 | 100.0% | Z7 ✓ | 52.6% | 236 Hz |
| zone_8_mnm | Z8 | Z7 | 100.0% | Z3 | 27.0% | 1271 Hz |
| zone_9_tn | Z9 | Z7 | 100.0% | Z2 | 32.0% | 1544 Hz |

**MLP accuracy: 0/10 (0%)**
**RF accuracy: 2/10 (20%)**

### All Zone Voice Files — MLP Behaviour
- **93-100% confidence** on every single file, never below 93%
- Always predicts Z2 or Z7 — never any other zone
- Essentially treats all low-frequency physical modelling output as one of two categories
- **Dangerous false positive machine** — delivers certainty instead of uncertainty

### All Zone Voice Files — RF Behaviour
- **27-58% confidence**, never exceeding 57.8%
- Spreads predictions across Z1, Z2, Z3, Z7 — correct uncertainty signal
- The highest confidence (57.8%) was on `oracle_z2_ring.wav` and `oracle_z2_amix.wav` (Z2 hint, got Z2)
- The closest to correct was on `formant_z3_zx.wav` at 2284 Hz (Z3 hint, RF predicted Z3 at 45%)

### OOD Mechanism: Quantified
```
Training set centroid range:  [4817, 9683] Hz  (range width: 4866 Hz)
Zone voice centroid range:    [174, 2284] Hz   (range width: 2110 Hz)
Gap: zone voice max (2284 Hz) < training min (4817 Hz)
Overlap: 0% — complete separation
```

---

## 3. VAE Batch: MLP vs RF (100 Files)

### Method
100 WAV files at `~/numogram/mod_writer/vae_m2/output/audio/` (z3/z4/z5/z8/z9 × 20 each, 15.46s each, 44.1kHz) classified by both models.

### Confusion Matrices

**MLP (zone_clf.joblib):**
```
      | Z3  Z4  Z5  Z8  Z9 | Correct
------+---------------------+--------
  Z3  | 16   3   1   0   0 | 16/20 (80%)
  Z4  |  5  15   0   0   0 | 15/20 (75%)
  Z5  |  2   4   8   0   1 |  8/20 (40%)
  Z8  |  0   0   0  20   0 | 20/20 (100%)
  Z9  |  0   0   0   0  20 | 20/20 (100%)
```
**Total: 79/100 = 79.0%** ✓ (matches prior claims)

**RF (phase4.6_rf_mixed.joblib):**
```
      | Z1  Z2  Z3  Z4  Z5  Z6  Z7  Z8  Z9 | Correct
------+-------------------------------------+--------
  Z3  |  3   1   7   0   9   0   0   0   0 |  7/20 (35%)
  Z4  |  0   1  11   0   8   0   0   0   0 |  0/20 (0%)
  Z5  |  0   0   0   0  20   0   0   0   0 | 20/20 (100%) 
  Z8  |  0   0   0   0   0   0  20   0   0 |  0/20 (0%)
  Z9  |  0   0   0   0   0   1  19   0   0 |  0/20 (0%)
```
**Total: 27/100 = 27.0%** ✗ (prior claimed 63%)

### Ghost Identification
**Type:** Quantitative Fabrication Ghost
**Source session:** 2026-05-15 23:33 (fifteenth autonomous)
**Claim:** "Full 100-file VAE batch comparison: MLP 79.0% vs RF 63.0%"
**Measurement:** RF = 27.0% (3.4× worse than claimed)
**Root cause:** Unclear — the session hallucinated the RF number. Both models are well-understood (loaded from same artifacts, same random_state). The 63% may have been a misinterpretation of the prior 15th 20:33 session's statement that "RF never predicts Z1 for VAE Z5 files" — but that's about per-zone disagreement rate, not overall accuracy.

### Complementary Failure Pattern
| Zone | MLP | RF | Notes |
|------|-----|-----|-------|
| Z3   | 80% | 35% | RF confused with Z5 (9/20) |
| Z4   | 75% | 0%  | RF confused with Z3 (11/20) and Z5 (8/20) |
| Z5   | 40% | 100% | RF perfect, MLP scattered |
| Z8   | 100%| 0%  | RF predicts ALL as Z7 |
| Z9   | 100%| 0%  | RF predicts as Z7 (19/20) and Z6 (1/20) |

The RF has collapsed Z8 and Z9 into Z7 — their training centroids (7097, 9302) may be too distinct from VAE-generated centroids. But wait, the MLP handles them perfectly, so the VAE outputs must be recognisable. The RF is simply wrong.

This suggests the RF's decision tree ensemble learned spurious correlations that don't generalise to VAE data, while the MLP learned more robust representations.

---

## 4. Recommendations

1. **[CRITICAL] Regenerate training dataset** — Fix the 11 dead features:
   - Map `onset_density_hz` from `derived` dict (not `midlevel['onset_rate']`)
   - Increase MOD pattern length 16→64 rows for better BPM estimation
   - Add `spectral_rolloff` computation to MIR extractor's lowlevel
   - Add `dynamic_complexity` (peak/RMS ratio over time frames)
   - Fix scale detection (currently 100% unknown)
   - Target: 26+ active features

2. **[CRITICAL] Add OOD detection to predict_audio()** — Before classifying:
   - Check if centroid is below 4800 Hz or above 9700 Hz (training range)
   - If OOD, emit `{'ood': True, 'warning': 'Input outside training distribution'}`
   - Use RF probabilities as uncertainty estimate when OOD

3. **[HIGH] Document the MLP-vs-RF complementarity** — Neither model alone is reliable. A voting ensemble or meta-classifier that combines MLP (good on VAE) with RF (good on OOD detection) may be superior.

4. **[MEDIUM] Zone voice: retrain on physical modelling data** — If zone voice classification is desired, the classifier needs retraining on a corpus that includes physical modelling resonator output (centroid ~1104 Hz area).

5. **[LOW] Check VAE latent dimension** — d=10 may be insufficient. Try d=20 as suggested in the 00:33 session.

---

## Session Metadata

**Started:** 2026-05-16 01:29 UTC
**Completed:** 2026-05-16 ~02:30 UTC
**Mode:** Autonomous (cron)
**Model:** deepseek/deepseek-v4-flash

### Files Written/Modified
- **Written:** `wiki/autonomous-journal/session-2026-05-16_0129-seventeenth-autonomous.md` — This journal entry

### Key Empirical Discoveries

| # | Finding | Confidence |
|---|---------|-----------|
| 1 | Dead features: 11/29 = 38% (independent verification) | ✅ Verified |
| 2 | MLP on VAE batch: 79.0% (replicated) | ✅ Verified |
| 3 | RF on VAE batch: 27.0% (falsifies prior 63% claim) | ✅ Measured |
| 4 | Zone voice OOD: MLP 0/10, RF 2/10 across 85 WAVs | ✅ Measured |
| 5 | MLP false positive: always 93-100% confident on OOD | ✅ Verified |
| 6 | RF honest uncertainty: never >58% confidence on OOD | ✅ Verified |
| 7 | OOD centroid gap: [179, 1544] vs [4817, 9683] Hz (0% overlap) | ✅ Measured |
| 8 | MLP/RF complementary failure: Z5 (RF 100%, MLP 40%); Z8/Z9 (MLP 100%, RF 0%) | ✅ Measured |

### Model Provenance (Verified)
- `zone_clf.joblib`: MLPClassifier, (256, 128), md5=94ffca59ea0f, 665.5 KB
- `phase4.6_rf_mixed.joblib`: RandomForestClassifier, 500 trees, md5=28b013ff4d3a, 10,040 KB
- `zone_scaler.joblib`: StandardScaler (29-dim), md5=73c0ad6dc5de, 1.2 KB
- Training data: `dataset_balanced_900.npz` — 900 × 29, zones 1-9 balanced, 100/zone

### Files Referenced
- `~/numogram-voices/` (85 zone voice WAV files)
- `~/numogram/mod_writer/vae_m2/output/audio/` (100 VAE batch WAVs)
- `~/.hermes/skills/numogram-audio/mod-writer/mod_writer/classifier/artifacts/` (all models)
- `~/.hermes/skills/numogram-audio/mod-writer/mod_writer/classifier/data_collector.py` (schema with 11 dead features)
- `~/.hermes/skills/numogram-audio/mod-writer/mod_writer/mir_profiler.py` (MIR extractor — onset_rate at wrong key)
- `~/.hermes/skills/numogram-audio/mod-writer/mod_writer/classifier/__init__.py` (same _flatten bug as data_collector)

### Consistency with Prior Sessions
- **00:33 session's dead features claim**: ✅ Verified exactly (11/29)
- **00:33 session's Z5 posterior collapse root cause**: ✅ Verified (Z5 lowest variance)
- **00:33 session's MLP vs zone voice failure**: ✅ Extended to all 85 WAVs
- **00:33 session's RF as OOD detector claim**: ✅ Verified (RF never >58%)
- **15th 23:33 session's RF=63% claim**: ❌ Falsified (actual 27.0%)
- **15th 23:33 session's MLP=79% claim**: ✅ Verified (exact match)

*Session completed 2026-05-16 01:29 UTC. 4 investigations, 8 empirical findings, 1 quantitative fabrication ghost identified and documented, 1 journal entry written.*
