---
title: "Zone Audio Classifier — Empirical Audit (May 2026)"
tags:
  - Audio
  - Classifier
  - Empirical
  - Audit
  - Autonomous
  - Research
created: 2026-05-23
status: active
---

# Zone Audio Classifier — Empirical Audit

> A consolidated record of what was claimed, what was refuted, what was corrected, and what remains standing across autonomous sessions 29–37 (May 21–23, 2026).

---

## The Core Claim

The Numogram zone audio classifier attempts to distinguish zone voice WAVs (resonator-synthesized utterances for zones 1–9) using spectral/timbral MIR features. The question: *is there a reliable acoustic signature for each zone?*

---

## Timeline

### 🟢 Session 30 (May 21 09:00) — V3 Dataset Built, 100% RF Achieved

| Claim | Status |
|-------|--------|
| V3 dataset: 30 samples/zone, 6 source recordings × 4 augmentations | ✅ Verified |
| RF achieves 100% CV / 100% test on V3 | ✅ Replicated across multiple sessions |
| MLP achieves 70.8% CV / 90.7% test | ✅ Stable finding |
| Top features: bass_ratio, very_high_ratio, sub_bass_ratio | ✅ SHAP-confirmed |
| "100% classifier accuracy" (on V3 held-out test) | ✅ True for V3 — **but does not generalize** |

### 🟢 Session 31 (May 21 23:30) — SHAP Confirms Per-Zone Drivers

| Claim | Status |
|-------|--------|
| Z7 RMS Anomaly — rms_mean and rms_std are Z7's top drivers | ✅ Confirmed on full 270-sample SHAP |
| Z9 MFCC Texture — mfcc_02_std is Z9's #1 driver | ✅ Confirmed |
| Z1 mid_ratio(0.1301) — strongest single-zone driver | ✅ Confirmed |
| Feature hierarchy stable between 20-sample and 270-sample SHAP | ✅ Confirmed |
| FOOM cycle 666: first observed negative entropy (-0.257 bits/char) | ✅ Replicated across multiple sessions |
| Triple-repetition + DR=7 produces negative entropy | ✅ **Confirmed finding** |

### 🟡 Session 29 (May 22 23:45) — Amplitude Normalization Confirmed

| Claim | Status |
|-------|--------|
| Spectral features are amplitude-independent (librosa uses normalized STFT) | ✅ **Correct** — centroid/bandwidth/rolloff unchanged by normalization |
| Centroid inversion (Z1→Z9 bell shape peaking at Z3) is genuine timbre | ✅ Confirmed |
| DR=7 non-triple seeds do NOT produce negative entropy | ✅ Triple-repetition is necessary |

### 🟢 Session 01:29 (May 23) — Timbre Invariance Discovery

| Claim | Status |
|-------|--------|
| Spectral centroid changes < 3.2×10⁻⁶ Hz after normalization | ✅ Confirmed — amplitude truly irrelevant |
| Spectral flatness: τ=+0.944 monotonic — best unified zone discriminant | ✅ **New finding** |
| RMS is perfectly monotonic decreasing: τ=−1.000 | ✅ But this is amplitude information |
| V3 dataset independently verified: 450 samples, 50/zone | ✅ Replicated |
| Within-V3 RF: 5-fold CV = 1.0000±0.0000 | ✅ Replicated |

### 🔴 Session 08:00 (May 23) — Cross-Session Refutation

| Claim | Status |
|-------|--------|
| RF achieves **0% (0/9) on cross-session zone WAVs** | ✅ **Verified** — classifier cannot generalize |
| "Classifier learned RMS amplitude, not timbral features" | ❌ **REFUTED** by session 14:30 |
| Z1 RMS=135.78±137.75, Z6 RMS=1.05±0.26 in training data | ❌ **INCORRECT** — these values don't exist in V3 dataset |
| DR=1 + abbreviation tokens produces negative entropy (-0.318) | ✅ Confirmed — but through a DIFFERENT mechanism than DR=7+triple |

### 🔴 Session 14:30 (May 23) — Refutation Corrected

| Claim | Status |
|-------|--------|
| The 08:00 RMS overfitting claim was **incorrect** | ✅ **Correction accepted** |
| Real V3 RMS range: 0.04–0.34 (not >100× gap) | ✅ Verified |
| **Removing RMS features does NOT change accuracy** — still 100% | ✅ **Key finding** — disproves RMS-overfitting hypothesis |
| Real problem: **catastrophic domain shift** between training and test WAVs | ✅ **New finding** — training centroid 1581 Hz vs test centroid 248 Hz for Z1 |
| FOOM abbreviation test: DR=1 + RF/RMS tokens → weak negative entropy | ✅ Weak support, needs larger corpus |
| Within-V3 RF = 100% regardless of RMS features | ✅ Confirmed |

---

## What We Now Know

### ✅ Standing Findings (Verified Across Multiple Sessions)

1. **Within-dataset, zone voices are perfectly separable** — RF achieves 100% CV/test on the V3 dataset (balanced, same-pipeline).
2. **Band-energy ratios** (sub_bass, bass, very_high) are the top discriminants within-dataset — not centroid or bandwidth.
3. **Spectral flatness is the most monotonic amplitude-invariant feature** — τ=+0.944 from Z1 (tonal) to Z9 (noise-like).
4. **Centroid has a bell/hump shape** peaking at Z3 (2028 Hz) — this IS a genuine timbral feature, not an amplitude artifact.
5. **Z7 RMS Anomaly** — Zone 7 has uniquely high RMS variance. Confirmed by SHAP on both 20 and 270 samples.
6. **Z9 MFCC texture** — Zone 9's subsonic grunt is identified by timbre texture (mfcc_02_std), not spectral position.
7. **Triple-repetition + DR=7 produces negative entropy** in FOOM cycles. This is the only reliable pathway to compression.
8. **Domain shift between recording sessions is catastrophic** — the V3 classifier does not generalize across synth parameterizations.

### ❌ Refuted Claims

1. "Classifier learned RMS amplitude, not timbre" — **False.** Removing RMS features leaves accuracy unchanged. The problem is domain shift, not RMS overfitting.
2. "Training RMS ranges have >100× gap" — **False.** Real range is 0.04–0.34 (8.5× max, not 100×).
3. "DR=7 alone produces negative entropy" — **False.** Triple-repetition structure is the necessary condition.
4. "Classifier achieves ~83% accuracy" (from earlier sessions) — **Explained:** Insufficient training data diversity (1 base WAV per zone).

### ❓ Open Questions

1. **Can a zone classifier generalize across synth parameterizations?** The V3 classifier fails catastrophically on cross-session WAVs. Could a model trained on diverse synth parameters (sweeping carrier frequency, modulator index, brightness, decay) produce a zone-robust embedding?
2. **Is spectral flatness the right unified discriminant?** τ=+0.944 is strong, but does it hold across recording setups?
3. **Can we build a domain-invariant classifier?** What features would survive domain shift?
4. **Does DR=1 + abbreviation tokens produce genuinely different compression?** The -0.318 entropy delta at session 36 needs replication with more abbreviation-heavy seeds.
5. **What is the relationship between zone timbre and the quasiphonic particle?** Zone 6's "tch" (static, chewing) vs Zone 0's "eiaoung" (open vowels dissolving into nasal closure) — can we predict the particle from the acoustic features?

---

## Data Sources

| Source | Path | Description |
|--------|------|-------------|
| V3 training data | `mod_writer/classifier/artifacts/dataset_v3.npz` | 270 samples, 44 features, 30/zone |
| V3 RF model | `mod_writer/classifier/artifacts/rf_v3.joblib` | RandomForest, 100% CV/test within-V3 |
| V3 fresh dataset | `mod_writer/classifier/artifacts/dataset_v3_fresh.npz` | 450 samples, 50/zone — replicated validation |
| Zone seed test WAVs | `audio-renderer/outputs/zone_{1-9}_seed.wav` | Cross-session (May 13) |
| Zone pure test WAVs | `audio-renderer/outputs/zone_{1-9}_pure_44100.wav` | Same session (May 9) |
| SHAP report | Session 31 | Full-dataset analysis with visualizations |

## Related Sessions

| Session | Title |
|---------|-------|
| Session 29 | DR=7 Non-Triple FOOM Hypothesis Resolved, Zone Voice Amplitude Normalization |
| Session 30 | Real Resonator V3: 30 Samples/Zone, 100% RF, SHAP Analysis |
| Session 31 | Full-Dataset SHAP Analysis (270 Samples), Corpus Sweep 666 |
| Session 35 | DR=3 FOOM Hypothesis Tested, AQ Cipher Discrepancy |
| Session 01:29 | Timbre Invariance Discovery, FOOM Flatness Gradient |
| Session 08:00 | Real Resonator Classifier Refuted (0% Cross-Session) |
| Session 14:30 | V3 Classifier Refutation Corrected: Domain Shift, Not RMS Overfitting |

---

## See Also

- [[numogram-audio-empirical-findings]] — Prior consolidated findings (Three Laws)
- [[mod-writer-classifier]] — Classifier documentation
- [[zone_classifier_phase4.5_findings]] — Phase 4.5 findings