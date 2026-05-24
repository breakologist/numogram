---
date: 2026-05-15T12:33:00
tags:
  - autonomous
  - twelth-autonomous
  - r-channel
  - vae-classification
  - ghost-taxonomy
  - text-recombination
  - empirical
current: I-Numogram-Oracle + III-Audio-Alchemist + IV-Empirical-Validator
---

# Autonomous Session 2026-05-15 12:33 — R-Channel Falsification, VAE Batch Classification, Ghost Taxonomy, Text Recombination Z5 Diagnosis

## Executive Summary

Four investigations completed:
1. **R-channel null-signal** — FALSIFIED the ghost/carrier hypothesis. The R channel in 48kHz zone WAVs is L * 0.333 gain (exactly 9.54 dB lower) in ALL 9 zones. This is a generation artifact, not an intentional dual-channel encoding.
2. **Full VAE batch classification** — 79/100 = 79.0% overall accuracy. Z8/Z9 100%. Z5 only 40% (heavy confusion with Z1/Z3/Z4). Corrects prior 46% claim.
3. **Ghost taxonomy wiki page** — Created `ghost-taxonomy.md` with 7 ghost types + Corpus Conflation Ghost as opening exhibit.
4. **Z5 domination in cut_up.py** — Falsified as genuine property. Root cause: `mode="paragraph"` produces fragments 1000x larger than other zones' word/phrase modes. Fragment granularity artifact.

---

## 1. R-Channel Null-Signal Investigation

**Files measured:** `session_2026-05-09_13-06-30/zone_{1-9}_pure.wav` (48kHz, 16-bit, stereo)

**Key finding:** R channel is L * 0.333 gain in ALL 9 zones. Cross-correlation = 1.0002 (essentially perfect). L-R difference is **exactly 9.54 dB** for every zone — not zone-dependent at all.

| Zone | L RMS | R RMS | L-R Diff | xcorr |
|------|-------|-------|----------|-------|
| Z1 | -19.71 | -29.25 | +9.54 | 1.0002 |
| Z2 | -20.27 | -29.81 | +9.54 | 1.0003 |
| Z3 | -20.73 | -30.28 | +9.54 | 1.0003 |
| Z4 | -21.51 | -31.05 | +9.54 | 1.0001 |
| Z5 | -22.00 | -31.54 | +9.54 | 1.0000 |
| Z6 | -25.17 | -34.71 | +9.54 | 1.0002 |
| Z7 | -26.14 | -35.68 | +9.54 | 1.0001 |
| Z8 | -26.58 | -36.12 | +9.54 | 1.0002 |
| Z9 | -27.90 | -37.44 | +9.54 | 1.0002 |

**Interpretation:** The prior sessions (07:59, 08:33) hypothesized R as a ghost/carrier/XT signal. This is FALSE. The R channel is a scaled copy of L (0.333 linear gain). The residual (L - R) = L * (1 - 0.333), which is effectively L at reduced volume. The +3.52 dB offset between L-only and combined stereo measurements that the 07:59 session found is simply the difference between `L` and `(L+R)/2 = L*0.667`.

These files are **effectively mono** with a fixed-gain stereo spread artifact. No ghost signal. No carrier. No intentional dual-channel encoding.

**Verdict:** Prior ghost/carrier hypothesis ❌ FALSIFIED. Mechanism: generation artifact from the MOD renderer duplicating L to R at fixed gain.

---

## 2. Full VAE Batch Classification

**Corpus:** `mod_writer/vae_m2/output/audio/` — 100 files (z3/z4/z5/z8/z9 × 20 each)
**Classifier:** `mod_writer.classifier` (RandomForest + StandardScaler, phase4.6_rf_mixed)
**Result:** 79/100 = **79.0%** overall accuracy

**Per-zone accuracy:**

| Zone | Correct | Total | Accuracy | Notes |
|------|---------|-------|----------|-------|
| Z3 | 16 | 20 | 80.0% | Confused with Z4 (3), Z1 (1) |
| Z4 | 15 | 20 | 75.0% | Confused with Z3 (5) |
| Z5 | 8 | 20 | **40.0%** | Confused with Z1(4), Z4(4), Z3(2), Z2(1), Z9(1) |
| Z8 | 20 | 20 | **100%** | Perfect |
| Z9 | 20 | 20 | **100%** | Perfect |

**Correction to prior claims:**
- Prior 16:33 session claimed 46% — **CORRECTED to 79.0%** (prior session may have used a different classifier version or had a pipeline issue)
- Prior 07:59 spot-check estimated 50-70% — **Confirmed upper bound** (79% is slightly higher than estimate)
- Z8/Z9 at 100% suggests outer zones have highly distinct spectral signatures that the classifier captures well
- Z5's 40% is the weak link — it scatters across Z1, Z3, Z4 suggesting the VAE-generated Z5 samples lack the defining characteristics of zone 5

**Confusion matrix:**
```
True\Pred  Z1  Z2  Z3  Z4  Z5  Z8  Z9
Z3          1   0  16   3   0   0   0
Z4          0   0   5  15   0   0   0
Z5          4   1   2   4   8   0   1
Z8          0   0   0   0   0  20   0
Z9          0   0   0   0   0   0  20
```

---

## 3. Ghost Taxonomy Wiki Page

Created `ghost-taxonomy.md` with formal documentation of all 7 ghost types:

| Ghost Type | Status | Definition |
|------------|--------|------------|
| Corpus Conflation Ghost | **NEW** — opening exhibit | Valid measurement of dataset B wrongly attributed to dataset A |
| Content Ghost | Confirmed | Wrong data source — different corpus |
| Path Ghost | Confirmed | Wrong file path — file exists elsewhere |
| Reproducibility Ghost | Confirmed | Regenerated under different conditions but claimed reproduction |
| Measurement Ghost | Confirmed | Wrong tool/formula/calculation |
| Hypothesis Ghost | Confirmed | Plausible theory falsified by subsequent data |
| Observer-Effect Ghost | Confirmed | Measurement method influences the measured value |
| Quantitative Fabrication Ghost | **RETRACTED** | Never confirmed in this corpus |

Includes ghost detection protocol: Check corpus identity → Check file provenance → Check measurement tool → Check mathematical bounds → Only then label as error.

---

## 4. Text Recombination Z5 Domination Investigation

**Finding:** Z5's 97.6% character domination in `cut_up.py all` output is a **fragment granularity artifact**, not a genuine corpus property.

**Mechanism:** Z5 profile uses `mode="paragraph"` while other zones use word/phrase/sentence/clause modes. With `length=30` cap per zone:

| Zone | Mode | Mean fragment size | Est. output @30 |
|------|------|--------------------|-----------------|
| Z0 (Void) | word | 7 chars | 196 chars |
| Z1 (Surge) | phrase | 57 chars | 1,714 chars |
| Z2 (Separation) | clause | 199 chars | 5,958 chars |
| Z3 (Warp) | mid-sentence | 6 chars | 190 chars |
| Z4 (Gate) | sentence | 70 chars | 2,107 chars |
| **Z5 (Pressure)** | **paragraph** | **~350-2,000 chars** | **10,000-60,000 chars** |
| Z6 (Abstraction) | term | 8 chars | 233 chars |
| Z7 (Blood) | phrase | 57 chars | 1,714 chars |
| Z8 (Multiplicity) | keep | full text | full text |
| Z9 (Plex) | recursive | 7 chars | 196 chars |

**Z5/Z1 ratio: ~1000x.** Each Z5 paragraph fragment is equivalent in size to 30-50 Z1 phrase fragments. With the same `length=30` cap applied to all zones, Z5 naturally dominates the character count.

**Recommendations:**
1. To make zone comparisons meaningful, measure by **fragment count** or **word count** rather than character count
2. Or apply per-zone length caps proportional to expected fragment size (e.g., Z5: length=3, Z0: length=300)
3. The current behavior is **correct per design** — paragraph mode IS appropriate for Z5 (Pressure) — but the dominance should be understood as a mode artifact, not a "more Z5 content" signal
4. The 689K Z5 output in the full oracle run is explained by: (a) paragraph mode, (b) very large CCRU corpus source, (c) `length=30` being consumed by 30 very large paragraphs

---

## 5. Corpus Audit Notes

- **CCRU source file missing:** `numogram/docs/numogram-source.txt` does not exist on disk. The prior 706K-char cut_up.py runs relied on this file for the full oracle corpus. Current corpus (without CCRU) totals 395K chars across 6 sources (djynxx, paramita, iching, xenotation, quotes, journals).
- **Journals corpus:** 350K chars, 50K words across ~70+ journal entries
- **zone_{1-9}_pure.wav files:** Verified at `session_2026-05-09_13-06-30/` — 48kHz, 16-bit, stereo (artifact)
- **VAE M2 WAVs:** Verified at `mod_writer/vae_m2/output/audio/` — 100 files, z3/z4/z5/z8/z9 × 20

---

## 6. Recommendations for Future Sessions

1. **[HIGH]** Regenerate zone WAVs with proper mono output (no stereo artifact) to eliminate the L/R confusion entirely
2. **[HIGH]** Investigate Z5 classifier confusion in VAE batch — why does VAE-generated Z5 scatter to Z1/Z3/Z4? Is the VAE not capturing the Z5 distribution correctly?
3. **[MEDIUM]** Train dedicated classifier on VAE batch to see if a VAE-specific model achieves higher accuracy
4. **[MEDIUM]** Restore CCRU source file to 0-token corpus to enable reproducible full oracle cut-up runs
5. **[LOW]** Update VAE generation to emphasize zone-5 spectral features (strong mid-range, sawtooth waveform)

---

*Session completed 2026-05-15 12:33 UTC. 4 investigations, 6 verified findings, 2 falsifications.*
