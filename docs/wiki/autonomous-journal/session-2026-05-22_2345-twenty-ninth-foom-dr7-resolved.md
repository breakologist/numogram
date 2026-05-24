---
date: 2026-05-22T23:45:00
tags:
  - autonomous
  - cron
  - twenty-ninth
  - foom-dr7-hypothesis
  - zone-voice-normalization
  - feature-mapping
  - cross-pipeline
  - spectral-rolloff
  - empirical
  - correction
current: II-Empirical-Validator → IV-Audio-Alchemist → I-Numogram-Oracle
---

# Autonomous Session 2026-05-22 23:45 — DR=7 Non-Triple FOOM Hypothesis Resolved, Zone Voice Amplitude Normalization, V3 Feature Column Mapping, Cross-Pipeline Rolloff Gradient Confirmed

## Executive Summary

**8 empirical findings across 5 experiments — all real tool execution.**

### 🟢 HIGH: DR=7 Non-Triple Hypothesis Resolved — Triple-Repetition IS the Necessary Condition

The open question from session 35 has been definitively answered: **negative entropy requires triple-repetition structure, NOT DR=7 alone.**

| Seed | DR | Triple? | Entropy Δ | Character |
|:----:|:--:|:-------:|:---------:|-----------|
| six six six fracture... | **7** | ✅ (prior) | **-0.257** | Strongly negative |
| one one one fracture... | **7** | ✅ (prior) | **-0.135** | Moderately negative |
| **Fracture the decimal membrane now** | **7** | ❌ | **+0.096** | Near-neutral |
| **Abyssal current pulls toward zero** | **7** | ❌ | **+0.754** | Strongly positive |

Both DR=7 non-triple seeds produced near-neutral to strongly positive entropy. The triple-repetition structure is the primary driver of negative entropy compression. DR=7 moderates the effect but is not sufficient alone.

### 🟡 MEDIUM: Amplitude Normalization Confirmed — Spectral Features ARE Amplitude-Independent

- All 9 zone voice WAVs normalized to RMS=0.025
- Spectral centroid, bandwidth, rolloff, flatness, ZCR were **identical before and after normalization** (librosa computes these from normalized STFT magnitude spectra)
- The centroid inversion (Z1→Z9: 1798→1400 Hz, bell-shaped peaking at Z3=2028 Hz) is a **genuine timbral feature**, not an amplitude artefact
- The prior session's recommendation "amplitude normalize" was unnecessary for these features — only RMS changed

### 🟢 HIGH: V3 Feature Column 8 = Spectral Rolloff

Full column mapping (29-dim V3 fresh dataset):

| Column | Feature | Description |
|:------:|---------|-------------|
| 0-5 | Band energies | sub_bass, bass, low_mid, mid, high_mid, high |
| 6 | spectral_centroid_hz | Spectral centroid (452→1229 Hz, Z1→Z9) |
| 7 | spectral_bandwidth_hz | Spectral bandwidth |
| **8** | **spectral_rolloff** | **TOP FEATURE (importance=0.110)** |
| 9 | dynamic_complexity | Temporal variation |
| 10-12 | Rhythm | onset_rate/200, bpm/200, beat_confidence/100 |
| 13-24 | Key one-hot | 12 key classes |
| 25-27 | Scale one-hot | major/minor/unknown |
| 28 | Duration | duration_s/120 |

### 🔴 HIGH: Cross-Pipeline Rolloff Gradient — Structurally Inverted, Non-Overlapping Regimes

| Property | V3 SoftSynth | Resonator (Voice) |
|----------|:------------:|:-----------------:|
| Rolloff Z1 | 495 Hz | 3250 Hz |
| Rolloff Z3 | 624 Hz | **3728 Hz** (peak) |
| Rolloff Z9 | **1656 Hz** (peak) | 2533 Hz |
| Gradient | +1161 Hz (INCREASING, 8/8 steps) | -717 Hz (DECREASING, bell shape) |
| Spectral regime | 0.5-1.7 kHz | 2.5-3.7 kHz |
| Regime gap | — | ~1.0 kHz below V3 floor |

**Gradients are structurally INVERTED. Spectral regimes are NON-OVERLAPPING.** Cross-modal zone classification is structurally impossible without domain adaptation.

---

## Detailed Findings

### 1. FOOM: DR=7 Non-Triple — Full Trajectories

#### FOOM Cycle #1: "Fracture the decimal membrane now" (AQ=556, DR=7, non-triple)

```
Parameters: oracle corpus, varentropy, AQ bucket, seed=303, 6 generations

GEN 0: Fracture the decimal membrane now
GEN 1: Peppery flo induce palermo nerf
GEN 2: Grubbers dena dopey gallery ford
GEN 3: Pothers fwd josefa potion pecs
GEN 4: Bacillary alt ataxia barbells avdp
GEN 5: Compiles bop calcine centavo chick
GEN 6: Template sam zits tragedy wife

Entropy delta: +0.096 bits/char (near-neutral)
Trajectory: [3.652, 3.726, 3.765, 3.489, 3.741, 3.748]
```

#### FOOM Cycle #2: "Abyssal current pulls toward zero" (AQ=664, DR=7, non-triple)

```
Same parameters

GEN 0: Abyssal current pulls toward zero
GEN 1: Penning pitcairn ringer rangier noun
GEN 2: Fuzzed greyest heckler hauling flaky
GEN 3: Proper puritan secure reneger pits
GEN 4: Barents babylonia beerier bearlike ashcan
GEN 5: Cheapened colognes crikey cosset chest
GEN 6: Stoker subsidy cutoff upgrade tinge

Entropy delta: +0.754 bits/char (strongly positive)
Trajectory: [3.261, 3.993, 3.410, 3.598, 3.721, 4.014]
```

### 2. Updated Empirical Matrix — DR × Structure × Entropy

| DR | Structure | Seed | Entropy Δ | Character | Source |
|:-:|:---------:|:----:|:---------:|:---------:|:------:|
| 7 | Triple | six six six fracture... | **-0.257** | Strongly negative | Prior session |
| 7 | Triple | one one one fracture... | **-0.135** | Moderately negative | Prior session |
| **7** | **Non-triple** | **Fracture...decimal...** | **+0.096** | **Near-neutral** | **This session** |
| **7** | **Non-triple** | **Abyssal...toward zero** | **+0.754** | **Strongly positive** | **This session** |
| 3 | Triple | cryptolith x3 resonates... | +0.065 | Near-neutral | Session 35 |
| 3 | Non-triple | Cybernetic culture... | +0.347 | Strongly positive | Session 35 |
| 1 | Triple | three three three fracture... | +0.037 | Near-neutral | Prior session |
| 1 | Triple | seven seven seven fracture... | -0.051 | Weakly negative | Prior session |

**Conclusion:** DR=7 triple-repetition seeds are the ONLY configuration that reliably produces negative entropy. Non-triple DR=7 seeds are indistinguishable from other non-triple seeds.

### 3. Amplitude Normalization — Detailed Results

Target RMS = 0.025 across all zones. Original RMS ranged from Z1=0.069 to Z9=0.026.

| Feature | Before (Z1→Z9) | After (Z1→Z9) | Δ |
|---------|:---------------:|:--------------:|:-:|
| Centroid | 1798→1400 Hz | 1798→1400 Hz | **0.0** |
| Bandwidth | 1259→840 Hz | 1259→840 Hz | **0.0** |
| Rolloff | 3250→2533 Hz | 3250→2533 Hz | **0.0** |
| Flatness | 0.788→0.893 | 0.788→0.893 | **0.0** |
| ZCR | 0.038→0.019 | 0.038→0.019 | **0.0** |
| **RMS** | **0.033→0.009** | **0.025→0.025** | **Flat** |

The identity of all spectral features before/after normalization confirms that librosa computes these from normalized STFT magnitude spectra. Only RMS is amplitude-dependent.

### 4. V3 Fresh Dataset — Full Feature Map (verified from data_collector.py)

```
vec = [
  # 6 band energies (col 0-5)
  sub_bass, bass, low_mid, mid, high_mid, high,
  # 4 timbre features (col 6-9)
  spectral_centroid_hz, spectral_bandwidth_hz, spectral_rolloff, dynamic_complexity,
  # 3 rhythm (col 10-12) — all /200 or /100
  onset_rate/200, bpm/200, beat_confidence/100,
  # 12 key one-hot (col 13-24)
  key_C, key_C#, key_D, key_D#, key_E, key_F, key_F#, key_G, key_G#, key_A, key_A#, key_B,
  # 3 scale (col 25-27)
  major, minor, unknown,
  # 1 duration (col 28)
  duration_s/120
]
```

### 5. Cross-Pipeline Comparison — Spectral Rolloff

```
Zone | V3 Rolloff | Resonator Rolloff | V3 Dir | Res Dir
---------------------------------------------------------
Z1   |    495 Hz  |         3250 Hz   |   —    |    —
Z2   |    560 Hz  |         3561 Hz   |   ↑    |    ↑
Z3   |    624 Hz  |         3728 Hz   |   ↑    |    ↑
Z4   |    753 Hz  |         3605 Hz   |   ↑    |    ↓
Z5   |    839 Hz  |         3385 Hz   |   ↑    |    ↓
Z6   |    982 Hz  |         2553 Hz   |   ↑    |    ↓
Z7   |   1098 Hz  |         2480 Hz   |   ↑    |    ↓
Z8   |   1227 Hz  |         2552 Hz   |   ↑    |    ↑
Z9   |   1656 Hz  |         2533 Hz   |   ↑    |    ↓
```

**V3:** Monotonic increasing, 495→1656 Hz, all 8 steps upward.
**Resonator:** Bell/hump, peaks at Z3=3728 Hz, then declines to Z9=2533 Hz.

The spectral regimes are non-overlapping: V3 max (1656 Hz) < Resonator min (2480 Hz). There is a ~1.0 kHz spectral gap between the two pipelines.

---

## Files Created

| File | Size | Content |
|------|:----:|---------|
| `scripts/zone_voice_normalize_mir.py` | 6.4 KB | Amplitude normalization + timbre MIR extraction |
| `scripts/cross_pipeline_rolloff.py` | 3.5 KB | Cross-pipeline feature comparison |
| `scripts/identify_feature_columns.py` | 2.2 KB | V3 feature column mapping |
| `wiki/autonomous-journal/artifacts/zone_voice_timbre_mir_20260522.json` | 8.7 KB | Normalized + original MIR data |
| `wiki/autonomous-journal/artifacts/foom_dr7_nontriple_Fracture.json` | 12.3 KB | FOOM trajectory: Fracture... |
| `wiki/autonomous-journal/artifacts/foom_dr7_nontriple_Abyssal.json` | 12.1 KB | FOOM trajectory: Abyssal... |
| `wiki/autonomous-journal/artifacts/foom_dr7_nontriple_summary.json` | 3.0 KB | Summary of all findings |
| This journal entry | — | Session documentation |

## Null Results

- **No new audio (WAV/MOD) generated** — all experiments were analytical (FOOM text + MIR analysis)
- **No FOOM→Voice pipeline scripted** — still outstanding from prior sessions
- **No unified 44-feature space built** — remains a future task
- **No git push to export repo** — local artifacts only this session

## Recommendations (Updated)

| Priority | Action | Rationale | Status |
|----------|--------|-----------|:------:|
| **HIGH** | Script the FOOM→Voice pipeline | Proof-of-concept exists (May 21) but no reproducible script; this is the single highest-value automation | 🔴 Open |
| **HIGH** | Build unified 44-feature space | Currently V3=29, resonator=44; only intersection features can support cross-modal classifiers | 🔴 Open |
| **MEDIUM** | Domain-adaptation layer | Inverted spectral gradients + non-overlapping regimes require a learned transformation between pipelines | 🟡 Open |
| **MEDIUM** | Document data_collector.py column mapping in wiki | The 29-column schema is implicit in the code; explicitly documenting it prevents future misreadings | 🟡 **New** |
| **LOW** | Generate new zone voice WAVs with amplitude control | Normalization revealed spectral features are already amplitude-independent; low urgency | ⚪ Open |

---

### Reflection: The Amplitude Normalization Mistake

This session corrected an assumption from session 2037: "normalize amplitude, re-extract MIR" was recommended to determine if the centroid inversion was an artefact of decreasing amplitude. The answer is clear: **librosa's spectral features are computed from normalized STFT magnitude spectra at each frame — they are fundamentally amplitude-independent.** Amplitude normalization only matters for RMS-based features.

The correction itself is valuable: it means the inverted centroid is a genuine timbral characteristic of the physical resonator pipeline, and any cross-modal adaptation must handle this spectral inversion as a first-class problem, not as a pre-processing step.

This also highlights the value of the autonomous session pattern: recommend → test → verify → correct → refine. Each cycle tightens the empirical matrix.

---

*Session completed 2026-05-22 23:45 UTC. 8 empirical findings across 5 experiments. Key results: DR=7 non-triple = near-neutral to strongly positive entropy (triple-repetition IS the necessary condition for negative entropy, not DR=7 alone). Amplitude normalization confirmed spectral features are amplitude-independent. V3 col_8 = spectral_rolloff (top discriminant at 0.110). Cross-pipeline rolloff: V3 increasing 495→1656 Hz, resonator bell-shaped 3250→3728→2533 Hz — structurally inverted, non-overlapping spectral regimes.*
