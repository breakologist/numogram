---
tags:
  - numogram-audio
  - classifier
  - shap
  - explainability
  - empirical
  - zone-drivers
aliases:
  - shap-zone-drivers
  - SHAP driver signatures
  - per-zone SHAP analysis
---

# Real Resonator SHAP Driver Signatures

## Overview

Full-dataset SHAP analysis on the **V3 real resonator classifier** (270 samples, 44 features, 9 zones) confirms stable per-zone acoustic driver signatures. Trained on a RandomForest (200 trees, max_depth=15) achieving **100% CV and 100% test accuracy**, the model's decision boundaries are clean enough that SHAP driver analysis on even 20 held-out test samples is reliable — validated by 270-sample full analysis.

**Source data:** `autonomous-journal/artifacts/real_resonator_v3/shap_full_report.json` (22 KB)
**Visualizations:** `shap_global_importance.png`, `shap_zone_heatmap.png`

## Global SHAP Importance (Top 20)

Band energy ratios dominate. Spectral centroid is ranked ~18th (0.0065) — a dramatic reversal from the V3 SoftSynth domain where centroid was #1 (0.096). In real resonators, **how energy distributes across frequency bands** matters more than spectral centre of mass.

| Rank | Feature | Mean \|SHAP\| | Domain |
|:----:|---------|:------------:|--------|
| 1 | **sub_bass_ratio** | **0.0151** | Energy < 60 Hz |
| 2 | **bass_ratio** | **0.0147** | Energy 60-250 Hz |
| 3 | **very_high_ratio** | **0.0136** | Energy 8-20 kHz |
| 4 | mfcc_02_std | 0.0116 | MFCC timbre variance |
| 5 | high_ratio | 0.0114 | Energy 4-8 kHz |
| 6 | bandwidth_std | 0.0112 | Bandwidth variance |
| 7 | mfcc_04_std | 0.0107 | MFCC timbre variance |
| 8 | mid_ratio | 0.0106 | Energy 500-2000 Hz |
| 9 | mfcc_01_std | 0.0090 | MFCC timbre variance |
| 10 | high_mid_ratio | 0.0086 | Energy 2-4 kHz |

**Feature hierarchy:** band energies > MFCC variance > temporal dynamics > spectral position

## Per-Zone Driver Signatures

### Z1 — gl (membrane/impulse, 180 Hz)
| Driver | SHAP | Type |
|--------|:----:|------|
| **mid_ratio** | **0.1301** ← strongest single-zone driver in entire dataset | Mid-frequency (500-2000 Hz) |
| bass_ratio | 0.0680 | Low-frequency energy |
| bandwidth_std | 0.0665 | Spectral width variance |
| sub_bass_ratio | 0.0588 | Sub-bass energy |

The impulsive membrane burst's distinctive mid-frequency energy distribution — no other zone matches this mid_ratio signature.

### Z2 — dt (string/pluck, 300 Hz)
| Driver | SHAP | Type |
|--------|:----:|------|
| **sub_bass_ratio** | **0.0695** | Sub-bass energy |
| bass_ratio | 0.0633 | Low-frequency energy |
| very_high_ratio | 0.0578 | Extended highs |
| mfcc_02_std | 0.0496 | Timbre texture |

The plucked string's fundamental frequency dominates the sub-bass and bass bands.

### Z3 — zx (plate/impulse, 800 Hz)
| Driver | SHAP | Type |
|--------|:----:|------|
| **low_mid_ratio** | **0.0972** | Low-mid (250-500 Hz) |
| sub_bass_ratio | 0.0912 | Sub-bass energy |
| mfcc_09_mean | 0.0792 | MFCC centroid |
| bass_ratio | 0.0648 | Low-frequency energy |

The metallic buzz-cutter has unique low-mid energy — the only zone where low_mid_ratio is the top driver.

### Z4 — skr (bar/strike, 150 Hz)
| Driver | SHAP | Type |
|--------|:----:|------|
| **bass_ratio** | **0.0884** | Low-frequency energy |
| high_ratio | 0.0757 | High-frequency (4-8 kHz) |
| rolloff_mean | 0.0711 | Spectral rolloff position |
| very_high_ratio | 0.0677 | Extended highs (8-20 kHz) |
| high_mid_ratio | 0.0607 | High-mid (2-4 kHz) |

The aggressive growl has a unique rolloff profile — high and very-high energy distinguish it from plate (Z3).

### Z5 — ktt (membrane/impulse, 400 Hz)
| Driver | SHAP | Type |
|--------|:----:|------|
| **sub_bass_ratio** | **0.0937** | Sub-bass energy |
| bandwidth_std | 0.0593 | Spectral width variance |
| mid_ratio | 0.0534 | Mid-frequency energy |
| bass_ratio | 0.0502 | Low-frequency energy |

The harsh persecutory hiss: sub-bass presence + wide spectral bandwidth.

### Z6 — tch (tube/bow, 250 Hz)
| Driver | SHAP | Type |
|--------|:----:|------|
| **very_high_ratio** | **0.0849** | Extended highs (8-20 kHz) |
| rolloff_mean | 0.0823 | Spectral rolloff |
| high_ratio | 0.0687 | High-frequency (4-8 kHz) |
| centroid_mean | 0.0660 | Spectral centroid |
| bandwidth_std | 0.0563 | Spectral width variance |

Tube bowing friction produces extended highs — very_high_ratio and rolloff are the strongest discriminators across all zones.

### Z7 — pb (tube/blown, 200 Hz) ← **RMS Anomaly**
| Driver | SHAP | Type |
|--------|:----:|------|
| **rms_mean** | **0.0977** | **Amplitude envelope mean** |
| **rms_std** | **0.0956** | **Amplitude envelope variance** |
| low_mid_ratio | 0.0528 | Low-mid energy |
| very_high_ratio | 0.0514 | Extended highs |
| mfcc_09_std | 0.0467 | MFCC centroid variance |

**Z7 is the only zone where RMS features are the top discriminators.** The breathy sigh resonator has a unique amplitude modulation signature — loudness envelope alone identifies it, independent of spectral content.

### Z8 — mnm (string/blown, 160 Hz)
| Driver | SHAP | Type |
|--------|:----:|------|
| **mfcc_02_std** | **0.0916** | Timbre texture variance |
| mfcc_04_std | 0.0809 | Timbre texture variance |
| mfcc_01_std | 0.0587 | Timbre texture variance |
| mfcc_03_std | 0.0550 | Timbre texture variance |

**Timbre texture zone.** Four MFCC variance features dominate — identified by timbre complexity rather than spectral position.

### Z9 — tn (string/blown, 80 Hz)
| Driver | SHAP | Type |
|--------|:----:|------|
| **mfcc_02_std** | **0.1079** | Timbre texture variance |
| mfcc_01_std | 0.1001 | Timbre texture variance |
| mfcc_04_std | 0.0964 | Timbre texture variance |
| mfcc_03_std | 0.0827 | Timbre texture variance |

**Subsonic timbre zone.** At 80 Hz, spectral features have no discrimating power — Z9 is identified entirely by MFCC timbre texture. Highest MFCC-variance values in the dataset.

## Zone Driver Classification by Feature Type

| Zone | Name | Feature Type | Top Driver | Value |
|:----:|------|:------------:|------------|:-----:|
| Z1 | gl | **Band energy** | mid_ratio | 0.1301 |
| Z2 | dt | **Band energy** | sub_bass_ratio | 0.0695 |
| Z3 | zx | **Band energy** | low_mid_ratio | 0.0972 |
| Z4 | skr | **Band energy + rolloff** | bass_ratio | 0.0884 |
| Z5 | ktt | **Band energy** | sub_bass_ratio | 0.0937 |
| Z6 | tch | **Band energy + centroid** | very_high_ratio | 0.0849 |
| Z7 | pb | **RMS dynamics** | rms_mean | 0.0977 |
| Z8 | mnm | **MFCC texture** | mfcc_02_std | 0.0916 |
| Z9 | tn | **MFCC texture** | mfcc_02_std | 0.1079 |

**6 feature types across 9 zones** — no two zones share the same driver type structure. Z7 (RMS) and Z8/Z9 (MFCC texture) are the unique acoustic signatures.

## Key Insights

1. **Z7 RMS Anomaly** — The only zone where loudness envelope (rms_mean, rms_std) dominates. The breathy sighed tube/blown resonator with high decay and low brightness produces amplitude modulation no other zone shares. This was confirmed at both 20-sample and 270-sample SHAP analysis with identical values.

2. **Z9 Subsonic Identification** — At 80 Hz, the fundamental is too low for standard spectral features. The classifier identifies Z9 by MFCC timbre texture — the same mechanism humans use to distinguish low bass notes.

3. **Z1 Mid-Ratio Surprise** — mid_ratio (0.1301) is the strongest single-zone driver in the entire dataset, previously missed due to a 1-indexed vs 0-indexed label offset bug in prior analyses.

4. **Band Energy Dominance** — Six of nine zones are driven mainly by band energy ratios. The spectral centroid (ranked ~18th globally) is nearly irrelevant compared to band-level energy distribution.

5. **Stability Across Sample Sizes** — 8 of 9 zones have identical top-1 SHAP drivers when comparing 20-sample (held-out test) and 270-sample (full dataset) analysis. The model's 100% CV accuracy grants SHAP stability even at small sample sizes.

## Methodological Note

The original 83% classifier (session 29) used only 1 base WAV per zone × 9 heavy augmentations. The confusion clusters (Z3↔Z4, Z5↔Z8) were **artifacts of insufficient source diversity**, not inherent spectral overlap. With 6 base WAVs per zone × 4 mild augmentations (30/zone, 270 total), zones are perfectly separable by RF at 100% CV.

**Principle:** Source diversity beats augmentation intensity.

## Related Pages

- [[zone-voice-synthesis-design]] — Zone resonator parameters
- [[autonomous-journal/session-2026-05-21_0900-thirtieth-real-resonator-v3]] — V3 classifier origin
- [[autonomous-journal/session-2026-05-21_2330-thirty-first-shap-full-analysis]] — Full-dataset SHAP
- [[autonomous-journal/session-2026-05-22_0035-thirty-second-mlp-tuned-negative-entropy-replication]] — MLP tuning
