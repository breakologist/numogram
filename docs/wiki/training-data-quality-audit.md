---
tags:
  - numogram-audio
  - classifier
  - vae
  - dataset
  - audit
  - empirical
---

# Training Data Quality Audit — `dataset_balanced_900.npz`

## Executive Summary

The balanced 900-track synthetic dataset (`dataset_balanced_900.npz`, 100 tracks per zone, zones 1–9) has **11 of 29 features that are constant across all 900 samples** — dead features that provide zero information to the classifier and VAE. These are caused by a **key schema mismatch** between `data_collector.py` (which expects certain keys) and `mir_profiler.py` (which stores them under different names or not at all). Additionally, the 16-row MOD generation is too short for reliable tempo/beat estimation, producing only 2 unique BPM values across 900 tracks.

The VAE's Z5 posterior collapse and the classifier's poor discriminative power are **downstream consequences** of this data pipeline bug.

## Dead Features: Root Cause Analysis

### Schema Mismatches (4 features)

| Feature | `data_collector` expects | `mir_profiler` provides | Impact |
|---------|------------------------|------------------------|--------|
| `spectral_rolloff` | `lowlevel['spectral_rolloff']` | **Not computed at all** | Always 0.0 |
| `dynamic_complexity` | `lowlevel['dynamic_complexity']` | **Not computed at all** | Always 0.0 |
| `onset_rate` | `midlevel['onset_rate']` | `derived['onset_density_hz']` (different key path) | Always 0.0 |
| `beat_confidence` | `midlevel['beat_confidence']` | Set only in Essentia path (line 232); librosa path (default, lines 210–224) never sets it | Always 0.0 |

Fix: Align `data_collector.py` keys with actual `mir_profiler.py` output, or add missing computations to `mir_profiler.py`.

### Dataset-Genuine Invariants (4 features)

| Feature | Reason for Constancy | Impact |
|---------|---------------------|--------|
| `scale_major` | Scale determined only by Essentia KeyExtractor; librosa path never sets `midlevel['scale']`. Default in `data_collector` = `[0,0,1]` (unknown) for all 900 samples. | Always 0.0 |
| `scale_minor` | Same cause as above. | Always 0.0 |
| `scale_unknown` | Always 1.0 by default. | Always 1.0 |
| `duration_norm` | All 900 MOD renders are 16 rows at ~125 BPM → always ~7.7 s → `/ 120` = 0.1288. | Always 0.1288 |

Fix: Use Essentia KeyExtractor for scale detection, or add chroma-based scale heuristic to librosa path.

### Key Detection Skew (3 features)

| Feature | Reason | Impact |
|---------|--------|--------|
| `key_F` | Always 0 — chroma never peaks on F for these square-wave MOD renders | Always 0.0 |
| `key_F#` | Always 0 — same reason | Always 0.0 |
| `key_G#` | Always 0 — same reason | Always 0.0 |

Key C dominates 80% of samples, C# at 14%. The remaining 10 keys collectively cover ~6%. This is a MOD generation characteristic: 16-row square-wave patterns all sound tonally similar to chroma.

Fix: None needed — this reflects genuine generator behaviour. More diverse MOD generation would fix this.

### Training Data Summary

| Metric | Value |
|--------|-------|
| Total samples | 900 |
| Total features | 29 |
| **Active features** | **18** (62%) |
| **Dead features** | **11** (38%) |
| Features with <5 unique values | 15 (52%) |
| Most discriminative feature | spectral_centroid_hz (20.5%) |
| Top 4 discriminators | centroid, high_mid, bandwidth, high |

## Zone 5 Specific Findings

Zone 5 has the **lowest total variance** in the scaled feature space (total_var = 1.80, vs Z1 at 25.53). This is because Z5 training samples have the narrowest range of spectral centroid (std = 276 Hz, min = 7522 Hz, max = 9428 Hz) — the tightest of any zone.

## BPM Constraint

The `bpm_norm` feature (index 11) has only **2 unique values** across all 900 samples: 0.625 (BPM = 125) and 0.827 (BPM ≈ 165). This is because the 16-row MOD patterns are too short for reliable tempo estimation, and libROSA's beat tracker converges on these two discrete values. In the `_sane_bpm` function, BPM outside [30,200] falls back to `onset_rate * 60`, which is always 0 (since onset_rate is dead).

## Remediation Plan

### Short-term: Key Alignment Patch

Patch `data_collector.py` `_flatten_features()` to use the correct keys:

```python
# Instead of:
vec.append((mid.get('onset_rate') or 0.0) / 200.0)
vec.append((mid.get('beat_confidence', 0.0) or 0.0) / 100.0)

# Use:
vec.append((derived.get('onset_density_hz') or 0.0) / 200.0)        # from derived dict
vec.append((mid.get('beat_confidence', 0.0) or 0.0) / 100.0)        # stays the same

# Add spectral_rolloff to MIR extractor:
# After the centroid/bandwidth computation (line 178-179):
# rolloff_freq = np.max(f[power.cumsum() <= 0.85 * total_power])
# lowlevel['spectral_rolloff'] = round(float(rolloff_freq), 2)
```

### Medium-term: Dataset Regeneration

1. Increase MOD pattern length from 16 to 64 rows for better tempo estimation
2. Add scale detection to librosa path (krumhansl-schmuckler key profile matching)
3. Run `data_collector.build_dataset()` to regenerate `dataset_balanced_900.npz`
4. Retrain both `zone_clf` (MLP) and `phase4.6_rf_mixed` (RF)

### Long-term: Real Audio Incorporation

The dataset is 100% synthetic (MOD renders). Incorporate real audio with known zone labels via oracle-readings or human-tagged source material to break the synthetic distribution bottleneck.

## Classification Performance with Current Data

A RandomForest trained on the 18 active features achieves essentially random accuracy in 5-fold CV (≈11% baseline for 9 classes). This is consistent with the classifier's observed behaviour: it learns decision boundaries from spectral centroid + band energies + onset density, which are weakly correlated with zone number in the training data but fail to generalise to VAE-generated or real audio.

## See Also

- [[mlp-vs-rf-classifier-comparison]]
- [[numogram-audio-empirical-findings]]
- `data_collector.py` (line 65–118: `_flatten_features`)
- `mir_profiler.py` (line 130–302: `extract()`)
