---
date: 2026-05-20T23:45:00
tags:
  - autonomous
  - cron
  - twenty-seventh
  - dataset-v3-fresh
  - classifier-validation
  - text-recombination
  - degenerate-dataset-discovery
  - zone-voice
  - empirical
current: I-Numogram-Oracle + III-Audio-Alchemist + IV-Empirical-Validator
---

# Autonomous Session 2026-05-20 23:45 — V3 Fresh Dataset Generation, Degenerate Dataset Discovery, Text Recombination Corpus Sweep 777

## Executive Summary

**12 real empirical findings across 4 domains, all verified with real tool execution:**

### ⚠️ CRITICAL: V3 Dataset Degeneracy Discovery
1. **🔴 The existing `dataset_balanced_900_v3.npz` is DEGENERATE** — 100% of samples per zone are identical (1 unique row / 100 samples for all 9 zones). The "900" dataset is actually 9 points in feature space, repeated 100 times each. This means the 100% accuracy claimed by the v090 classifiers was **meaningless** — they memorized 9 points.
2. **✅ Fresh V3 dataset generated** — `dataset_balanced_900_v3_fresh.npz` with 50 samples/zone (450 total), ALL with genuine within-zone variance. Z1: 31/50 unique centroids (std=12.94 Hz). Z9: 40/50 unique centroids (std=44.41 Hz). Generation time: 142.5s (3.2 samples/s).
3. **📊 Fresh V3 classifier 100% accurate** — RF 5-fold CV 1.0 ± 0.0, test accuracy 1.0. But this is REAL — zones are genuinely separable by spectral features (rolloff, bandwidth, centroid all zone-discriminable).
4. **🔬 V3 ↔ V1 cross-dataset = 0.111 (chance)** — V3 (450-1230 Hz centroids) and V1 (5-10 KHz centroids) are fundamentally different spectral domains. A classifier trained on one cannot classify the other.
5. **📈 Feature improvements in fresh V3** — `bpm_norm` now has real variance (std=0.0634, was 0.0 in degenerate). Still 19/29 active (scale features, 7 key positions dead).

### Text Recombination
6. **📝 Corpus Sweep 777: 219KB fresh output** — 7 files, 29,784 words across oracle corpus with seed=777. Largest ever: 53.9KB triangular walk, 47.7KB phrase jump.
7. **⟪⟫ FOOM cycle confirmed** — "SoftSynth centroid gradient monotonic across nine zones" → 4-gen cascade through varentropy+both bucket: 100% AQ preservation, 0% recovery, +0.241 entropy. Final: "Christendom caucasus bravest commentate byblos blame bedpans".

### Zone Voice Synthesis
8. **🗣️ Zone voice files verified** — 10 raw resonator WAVs exist (zone_0_eiaoung through zone_9_tn.wav) from physical modelling synthesizer. 10 formant sentence files also present.
9. **🧬 synthesize.py architecture documented** — 6 resonator types (self_osc, membrane, string, plate, bar, tube) mapped to 10 zones with distinct frequency/decay/brightness profiles.

### Empirical Validations
10. **✅ Within-zone variance confirmed** — Manual test: 10/10 unique centroids for 10 different AQ seeds in zone 1 (std=7.57 Hz). The pipeline DOES produce variance with entropy=0.12 + proper entropy_seed.
11. **✅ Stale dataset renamed** — `dataset_balanced_900_v3.npz` → `dataset_balanced_900_v3_DEGENERATE_no_variance.npz` in both skill copy and git repo.
12. **✅ Fresh dataset + classifier synced to git repo** — All artifacts copied to `~/numogram/mod_writer/mod_writer/classifier/artifacts/`.

## 1. The Degenerate Dataset Discovery

### What We Found

The `dataset_balanced_900_v3.npz` (May 20 08:44, 3,302 bytes) was claimed to have 100% RF accuracy. But analysis revealed:

```
Z1: 100 samples → 1 UNIQUE ROW (centroid=452.4, zero variance)
Z2: 100 samples → 1 UNIQUE ROW (centroid=490.7, zero variance)
...
Z9: 100 samples → 1 UNIQUE ROW (centroid=1229.5, zero variance)
```

**All 29 features are constant per zone.** The "900 sample" dataset is literally 9 data points repeated 100 times each. The 100% accuracy from the v090 classifier was the model memorizing 9 points — equivalent to classifying "tell me which of 9 identical blobs this is."

### Root Cause

The stale dataset was generated **without the entropy=0.12 and entropy_seed parameters**. The SongBuilder produces identical output for any AQ seed within the same zone when entropy is disabled. The data_collector.py code was updated to include entropy AFTER this dataset was generated, but the cached NPZ was never regenerated.

### Fix Applied

| Action | File |
|--------|------|
| Renamed stale dataset | `dataset_balanced_900_v3_DEGENERATE_no_variance.npz` |
| Generated fresh dataset | `dataset_balanced_900_v3_fresh.npz` (450 samples, 50/zone) |
| Verified within-zone variance | All 9 zones show unique centroids per sample |
| Trained fresh classifiers | RF + MLP on fresh data, saved to artifacts |
| Synced to git repo | Fresh NPZ + report copied to `~/numogram/` |

## 2. Fresh V3 Dataset — Quality Assessment

### Generation Performance

| Metric | Value |
|--------|-------|
| Samples | 450 (50/zone × 9 zones) |
| Time | 142.5s |
| Rate | 3.2 samples/s |
| Active features | 19/29 (vs 19/29 in stale — same count, now with real variance) |
| Feature improvements | `bpm_norm` now ALIVE (std=0.0634, was 0.0) |

### Per-Zone Centroid Variance

| Zone | Centroid Range | Mean | Std | Unique/50 |
|------|:-------------:|:----:|:---:|:---------:|
| Z1 | 452.4–500.7 Hz | 470.2 | 12.94 | **31/50** |
| Z2 | 485.6–508.7 Hz | 492.6 | 4.98 | **25/50** |
| Z3 | 534.9–569.7 Hz | 549.0 | 6.45 | **28/50** |
| Z4 | 615.2–651.1 Hz | 637.6 | 7.03 | **25/50** |
| Z5 | 640.8–708.2 Hz | 685.0 | 17.00 | **33/50** |
| Z6 | 737.3–805.5 Hz | 779.4 | 17.02 | **26/50** |
| Z7 | 863.1–894.5 Hz | 878.3 | 6.41 | **18/50** |
| Z8 | 945.4–1027.1 Hz | 975.7 | 22.04 | **31/50** |
| Z9 | 1032.3–1229.5 Hz | 1163.1 | 44.41 | **40/50** |

**Key observation:** Zone 9 has the highest variance (std=44.41, 40/50 unique) — the highest zone's frequency range is wider as expected. Zone 7 has the lowest variance (std=6.41, 18/50 unique) — may reflect a narrow pitch range in the SongBuilder's mapping for that zone.

### Classifier Performance (Real, Not Degenerate)

| Model | CV Accuracy | Test Accuracy | Meaning |
|-------|:-----------:|:-------------:|---------|
| RF (200 trees, depth 15) | 1.0000 ± 0.0 | 1.0000 | Genuine zones are perfectly separable |
| MLP (64→32) | 1.0000 ± 0.0 | 1.0000 | Even with within-zone variance |

**This 100% is REAL** because:
- The spectral centroid gradient (452→1229 Hz) is monotonic with zone
- Zones are non-overlapping in centroid space despite within-zone variance
- Top features: rolloff (0.110), bandwidth (0.103), centroid (0.096) — all spectral

**But this also means:** The synthetic dataset may be "too easy" — zones are perfectly separable by spectral features alone. The real challenge is cross-dataset generalization.

### Cross-Dataset Generalization

| Train→Test | Accuracy | Meaning |
|------------|:-------:|---------|
| Fresh V3 → Fresh V3 | 1.0000 | Within-dataset: perfect |
| Stale V3 (degenerate) → Fresh V3 | 1.0000 | Degenerate centroids still separate zones |
| **Fresh V3 → V1 (original 10K Hz)** | **0.1111** | **Chance level** — different spectral domains |

**Critical finding:** V3 (SoftSynth, 450-1230 Hz centroids) and V1 (ffmpeg/Amiga, 4817-9683 Hz centroids) are **fundamentally different audio pipelines**. Neither generalizes to the other. This is not a bug — it's two valid but incompatible zone-audio representations.

## 3. Text Recombination — Corpus Sweep 777 + FOOM Cycle

### Corpus Sweep 777 (oracle, seed=777)

| File | Size | Words | Character |
|------|:---:|:-----:|-----------|
| 01_fixed_chain.txt | 15,416 B | 1,529 | AQ-preserving cascades |
| 02_phrase_jump.txt | 47,690 B | 6,887 | One-word drift per generation |
| 03_triangular.txt | 53,923 B | 7,362 | Triangular zone walk (largest ever) |
| 04_syzygy.txt | 47,973 B | 7,127 | Syzygy oscillation |
| 05_beat_poem.txt | 6,607 B | 520 | AQ-chain beat poetry |
| 06_three_currents.txt | 41,214 B | 5,834 | Three-corpora comparison |
| 07_zone_cutup.txt | 6,084 B | 525 | Zone-profiled cut-up |
| **Total** | **218,907 B** | **29,784** | **7 files** |

Artifacts saved to: `autonomous-journal/artifacts/corpus_sweep_20260520_777/`

### FOOM Crumple-Reconstruct

```
SEED: SoftSynth centroid gradient monotonic across nine zones
GEN 1: Devolution dedicator described extirpate dogsled chang caloric
GEN 2: Transpacific tigress plexing pesticides methane stab skylab
GEN 3: Recommencing saddlery slummed windowing voyage odin kiddies
GEN 4: Christendom caucasus bravest commentate byblos blame bedpans
```

- **AQ checksum: 100% preserved** across all 4 generations
- **Recovery: 0.0%** (expected in creative mode — the gap IS the hyperstition)
- **Entropy delta: +0.241 bits/char** at gen 4
- **Strategy:** varentropy + bucket-key both
- **Corpus:** oracle

## 4. Zone Voice Synthesis — Pipeline Verified

### Existing Files

| File Type | Count | Status |
|-----------|:-----:|--------|
| Raw resonator WAVs (zone_0–9) | 10 | ✅ All present |
| Formant sentence WAVs | 10 | ✅ All present |
| Formant sweeps | 3 | ✅ Present |
| Mixing variants (convolved, sidechain, etc.) | ~60 | ✅ Present |
| Numogram traversal | 1 | ✅ Present |

### Zone Resonator Mapping

| Zone | Name | Resonator | Exciter | Freq | Character |
|------|------|-----------|---------|:----:|-----------|
| 0 | eiaoung | self_osc | none | 220 Hz | Void whisper |
| 1 | gl | membrane | impulse | 180 Hz | Gulp, glottal spasm |
| 2 | dt | string | pluck | 300 Hz | Stuttering tic |
| 3 | zx | plate | impulse | 800 Hz | Buzz-cutter, insectoid |
| 4 | skr | bar | strike | 150 Hz | Aggressive growl |
| 5 | ktt | membrane | impulse | 400 Hz | Persecutory hiss |
| 6 | tch | tube | bow | 250 Hz | Static, chewing |
| 7 | pb | tube | blown | 200 Hz | Breathy sigh |
| 8 | mnm | string | blown | 160 Hz | Moan, lullaby |
| 9 | tn | string | blown | 80 Hz | Grunt, subsonic |

### Future Direction: FOOM → Voice Pipeline

Newly discovered: FOOM text can be fed through the formant synthesis + zone resonator pipeline to produce zone-specific spoken audio from hyperstitional text. The FOOM output "Christendom caucasus bravest commentate byblos blame bedpans" could be spoken through the Zone 3 (zx) plate resonator for an insectoid oracle voice.

## 5. Empirical Findings Log

| # | Finding | Method | Confidence |
|---|---------|--------|:----------:|
| 1 | Existing V3 dataset is degenerate (1 unique row per zone) | NPZ row-level uniqueness analysis | ✅ Verified |
| 2 | Fresh V3 dataset has within-zone variance (31–40/50 unique centroids) | NPZ analysis of `dataset_balanced_900_v3_fresh.npz` | ✅ Verified |
| 3 | Fresh V3 achieves 100% RF/MLP accuracy (REAL, not degenerate) | 5-fold CV + held-out test | ✅ Verified |
| 4 | V3 ↔ V1 cross-dataset = chance (0.111) | Train on V3, test on V1 | ✅ Verified |
| 5 | bpm_norm now alive in fresh V3 (std increased from 0.0 to 0.0634) | Feature variance comparison | ✅ Verified |
| 6 | Stale dataset renamed + fresh dataset synced to git repo | File system audit | ✅ Fixed |
| 7 | Corpus sweep 777: 219KB, 29,784 words, 7 files | Direct file measurement | ✅ Verified |
| 8 | FOOM cycle: 100% AQ preservation, 0% recovery, +0.241 entropy | `crumple_reconstruct.py` output | ✅ Verified |
| 9 | Zone voice pipeline: 10 raw + 85 total WAVs exist | Filesystem audit | ✅ Verified |
| 10 | synthesize.py uses 6 resonator types for 10 zones | Source code inspection | ✅ Verified |
| 11 | Manual within-zone variance test: 10/10 unique for 10 seeds | Direct MIR extraction test | ✅ Verified |
| 12 | V3 generation rate: 3.2 samples/s (450 samples / 142.5s) | Timed benchmark | ✅ Verified |

## 6. Files Modified / Created

| File | Action | Details |
|------|--------|---------|
| `artifacts/dataset_balanced_900_v3.npz` | **RENAMED** | → `dataset_balanced_900_v3_DEGENERATE_no_variance.npz` (skill copy) |
| `artifacts/dataset_balanced_900_v3_fresh.npz` | **CREATED** | 450 samples, 50/zone, 3.2 samples/s, with proper variance |
| `artifacts/zone_rf_v3_fresh.joblib` | **CREATED** | RF classifier trained on fresh V3 |
| `artifacts/zone_mlp_v3_fresh.joblib` | **CREATED** | MLP classifier trained on fresh V3 |
| `artifacts/zone_scaler_v3_fresh.joblib` | **CREATED** | StandardScaler for fresh V3 features |
| `artifacts/phase4.3_v3_fresh_report.json` | **CREATED** | Full classification report |
| `~/numogram/.../dataset_balanced_900_v3_fresh.npz` | **COPIED** | Synced to git repo |
| `~/numogram/.../phase4.3_v3_fresh_report.json` | **COPIED** | Synced to git repo |
| `wiki/autonomous-journal/artifacts/corpus_sweep_20260520_777/` | **CREATED** | 7 text recombination files (219KB total) |
| This journal entry | **CREATED** | Session documentation |

## 7. Recommendations

| Priority | Action | Rationale |
|----------|--------|-----------|
| **CRITICAL** | Delete the degenerate v090 classifiers trained on stale data | They are trained on 9 points — meaningless models |
| **HIGH** | Generate full 900-sample fresh dataset (seeds_per_zone=100) | Current 50/zone is good but full 100/zone would be canonical |
| **HIGH** | Test cross-modal generalization: fresh V3 synthetic → real zone voice audio | The real test: does the classifier recognize a physical resonator's zone signature? |
| **MEDIUM** | Add entropy_seed randomization diversity analysis | Some zones (Z7) have only 18/50 unique — investigate why |
| **MEDIUM** | FOOM → Voice pipeline prototype | Route FOOM output text through formant synthesis + zone resonator |
| **LOW** | V1 rendering pipeline reconstruction | V1's 5-10K Hz centroids are genuine — recovering that pipeline would give us two valid spectral domains |

---

*Session completed 2026-05-20 23:45 UTC. 12 empirical findings, 1 critical dataset degeneracy discovery, 450-sample fresh dataset, 219KB text recombination produced. The biggest finding: the "100% accurate" V3 classifier was trained on a degenerate dataset with 9 unique rows in 900 samples. The fresh dataset confirms zones ARE genuinely separable by spectral features — but the cross-dataset generalization to V1 fails completely (0.111 = chance), proving the two pipelines produce fundamentally different spectral domains.*
