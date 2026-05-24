---
tags: [classifier, mlp, random-forest, vae, empirical, comparison]
---

# MLP vs RandomForest Classifier Comparison (VAE Batch)

**Date:** 2026-05-15  
**Dataset:** 100 VAE-generated WAV files (z3, z4, z5, z8, z9 × 20 each)  
**Models:** `zone_clf.joblib` (MLPClassifier 256→128) vs `phase4.6_rf_mixed.joblib` (RF 500 trees)

## Overall Results

| Metric | MLP | RF |
|--------|-----|----|
| **Overall accuracy** | **79.0%** | **63.0%** |
| Model agreement | — | 71.0% |

The MLP **outperforms** the RF on this VAE batch by 16 percentage points. This contradicts the implication from prior sessions that the RF might give superior results.

## Per-Zone Breakdown

| Zone | MLP Accuracy | RF Accuracy | MLP Confusions | RF Confusions |
|------|-------------|-------------|----------------|---------------|
| Z3 | 80% (16/20) | 55% (11/20) | →Z1:1, →Z4:3 | →Z1:6, →Z2:1, →Z4:1, →Z5:1 |
| Z4 | 75% (15/20) | 40% (8/20) | →Z3:5 | →Z1:2, →Z2:1, →Z3:6, →Z5:3 |
| Z5 | 40% (8/20) | 20% (4/20) | →Z1:4, →Z2:1, →Z3:2, →Z4:4, →Z9:1 | →Z2:1, →Z3:6, →Z4:9 |
| Z8 | **100%** | **100%** | — | — |
| Z9 | **100%** | **100%** | — | — |

## Z5 Confusion: MLP-Specific Artifact Confirmed

Prior findings hold: The **RF NEVER predicts Z1** for VAE Z5 files (0/20), while the MLP does (4/20).

However, the RF is **worse overall** on Z5 (20% vs 40%). The RF's Z5 predictions cluster on Z3 (6/20) and Z4 (9/20). Neither model correctly captures Z5 from VAE audio — the VAE's posterior collapse is a spectral generation failure, not primarily a classifier issue.

## Training Data Provenance

| Model | Training Data | Labels | Scaling |
|-------|--------------|--------|---------|
| MLP (zone_clf.joblib) | `dataset_balanced_900.npz` — 900 zone-seed MOD renders (100/zone) | Zones 1-9 | `zone_scaler.joblib` (StandardScaler) |
| RF (phase4.6_rf_mixed) | Same 900 zone-seed MODs ×1.0 weight + 40 real audio tracks ×0.5 weight | MLP-pseudo-labeled | None (RF is scale-invariant) |

Both models share the same synthetic core (900 zone-seed WAVs at 48 kHz, balanced). The RF gets an additional 40 real audio tracks at half weight.

## Key Findings

1. **MLP is the better model** for the VAE batch (79% vs 63%)
2. **Both models master Z8 and Z9** (100% accuracy — these zones have the most distinctive spectral signatures)
3. **Z5 is the hardest zone** for both models (40% MLP, 20% RF) — the VAE's Z5 generation produces broadband noise (centroid ~8468 Hz) vs training data (centroid ~1718 Hz), a 5× spectral mismatch
4. **The Z1 confusion claim** was correct but narrow — the MLP confuses VAE Z5→Z1 in 4/20 cases while the RF never does, but the RF's overall Z5 performance is worse
5. **Model disagreement is moderate**: 71% agreement across all 100 files, 65% agreement on Z5 specifically
