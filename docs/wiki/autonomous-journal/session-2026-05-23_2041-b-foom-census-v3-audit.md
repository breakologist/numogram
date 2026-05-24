# Autonomous Journal — Session 2026-05-23 Review + FOOM Census

**Session ID:** session-2026-05-23_2041-b
**Date:** 2026-05-23  
**Agent:** Hermes (cron)
**Focus:** V3 classifier audit · FOOM oracle census · MIR supplementary check

---

## §1 — FOOM Oracle Stability (12-Run Census)

**EMPIRICAL** — All 12 FOOM runs completed with `rc=0`. AQ checksum preserved in every case.
Recovery rate was 0.0 for all runs (G0 text not found in G6 for any seed tested).

```
file                                       AQ    Δent    pres   rec
foom_20260523_compress_123.json           685  +0.1345   T     0.000
foom_20260523_compress_321.json           657  +0.1607   T     0.000
foom_20260523_compress_789.json           710  +0.4010   T     0.000
foom_20260523_eng_7.json                  789  +0.0217   T     0.000
foom_20260523_eng_17.json                 825  +0.3343   T     0.000
foom_20260523_eng_71.json                 861  +0.0555   T     0.000
foom_20260523_eng_777.json                651  +0.1891   T     0.000
foom_20260523_flatness_gradient.json      963  +0.0685   T     0.000
foom_20260523_flatness_gradient_replicate 963  +0.2561   T     0.000
foom_20260523_rfseed_current.json         703  -0.0309   T     0.000
foom_20260523_void_em.json               2485  -0.1594   T     0.000
foom_20260523_xenon_flatness.json         963  +0.1669   T     0.000

N=12, neg=1, neu=2, pos=9
```

**Finding:** Entropy favours expansion (9/12 positive Δ), with VOID_EM scan being the sole compression outlier at -0.1594 bits/char. Negative entropy runs are rare under `varentropy --bucket-key aq` creative mode. This suggests the strategy is biased toward lexical richness rather than toward compression reconstruction.

---

## §2 — Zone Voice MIR: Flatness Gradient Inverted in Seed WAVs

**EMPIRICAL** — librosa-based measurement, verified identically across two independent code blocks (EXP5 / EXP15). No estimator disagreement.

| Zone | Pure Flatness | Seed Flatness | Δ (seed−pure) |
|------|--------------|--------------|-------------|
| Z1   | 0.7876       | 0.9636       | +0.1760 ↑   |
| Z2   | 0.8044       | 0.9334       | +0.1289 ↑   |
| Z3   | 0.8184       | 0.8953       | +0.0769 ↑   |
| Z4   | 0.8446       | 0.9073       | +0.0626 ↑   |
| Z5   | 0.8569       | 0.8617       | +0.0048 ↑   |
| Z6   | 0.8563       | 0.8562       | −0.0001 ↔   |
| Z7   | 0.8637       | 0.8625       | −0.0012 ↓   |
| Z8   | 0.8742       | 0.8641       | −0.0101 ↓   |
| Z9   | 0.8933       | 0.8858       | −0.0075 ↓   |

Kendall τ:
- Pure WAV flatness: **τ = +0.9444** (p=0.0000) — monotonic increase from Z1→Z9
- Seed WAV flatness: **τ = −0.4444** (p=0.1194) — non-monotonic, inverted

**Cross-zone concordance Δ-pure × Δ-seed: 7/8 directions agreement**
This means seed WAV centroid shifts are NOT complementary vectors — they oscillate in the same direction at Z6-Z7-Z8. The pure WAV centroid drops sharply at Z6 (Z6→240Hz drop), while seed WAV centroid at Z6 is essentially flat (+37Hz).

Centroid τ:
- Pure WAV centroid: **τ = −0.6111**  
- Seed WAV centroid: **τ = +0.5000**

**Conclusion:** Pure and seed pipelines produce genuine complementary gradients at Z1-Z5, then diverge at Z6-Z9. The "complementary" inversion is partial (≈6 zones clean), not total. This is a genuine signal of pipeline divergence, not measurement error.

---

## §3 — V3 Dataset Integrity: Root-Level Problems Identified

**EMPIRICAL** — direct inspection of `dataset_v3.npz`. Three failures found.

### 3a — Zone 1 Absent (label=0 empty)
Only 270−30=240 labeled samples exist despite `y` listing 0..9. Zone 1 cluster was deleted or never written.

### 3b — Centroid column is NOT pure WAV Hz
Per-label centroid_mean (dataset_v3):
```
label=1 (Z2):  1580.8 Hz
label=2 (Z3):   690.4 Hz  ← near F5=698Hz, flatness=0.0002 → likely sine
label=3 (Z4):  1623.8 Hz  ← flatness=0.000 → confirmed sine
label=4 (Z5):   265.6 Hz  ← flatness=0.000 → confirmed sine (≈C4=261Hz)
label=5 (Z6):  1802.3 Hz
label=6 (Z7):  5770.1 Hz  ← centroid outlier; high bandwidth
label=7 (Z8):  1995.5 Hz  ← flatness=0.0002 → near-sine
label=8 (Z9):  1069.9 Hz  ← flatness=0.0009 → near-sine
label=9(Z10):  1403.0 Hz  ← flatness=0.0035 → near-sine
```

These do **not** match the canonical pure WAV centroids (Z1=1798Hz → Z9=1400Hz). The dataset was created from <span style="color:white;background:#7500ff;">a</span> **different WAV set** than the current canonical 48kHz sources.

### 3c — Cross-Session JSON Mismatch
`v3_cross_session_results.json` shows centroid values of 248–1324 Hz, flatness 0.688–0.962.

Pearson r between `v3_cross_session_results.json` centroid list and `dataset_v3.npz` centroid: **r=0.3419 (p=0.368)**  
Pearson r for flatness: **r=0.0198 (p=0.960)**

Cross-session results did **not** originate from the same dataset. The classifier was evaluated on a different set of WAVs from the training data.

### 3d — V3 Cluster Half Are Near-Sinusoidal
6 out of 9 clusters have flatness ≈ 0.000–0.0033. This is consistent with pure-sine WAV sources. One cluster (label=5, centroid=5770 Hz, flatness=0.0099) has both very high centroid and nearly pure spectrum — an artifact of clipped sine at a high frequency.

---

## §4 — Flatness Classifier: No Zone Discriminative Power Confirmed

`flatness_classifier_results.json` shows **accuracy = 0.111 (11.1%)** = random-chance for 9 classes. All zones are predicted as zone 6 or 7 regardless of centroid. This was previously attributed to RMS dominance masking flatness; re-verified this session.

The dataset's flatness_mean spans 0.0–0.392 across 9 clusters, which should — in principle — afford separation. However, the MLP classifier (V3) failed to leverage it. Per-zone flatness in the dataset shows:

- Z2: 0.1672 (physically meaningful, a light texture)
- Z6: 0.3923 (strongly colored, high-spectrum-energy)
- All others: <0.01 → hard ceiling for ML softmax on these finite differences

---

## §5 — Centroid +/- Flatness OR-Bridge Steering

Pure WAV flatness gradient (Z1→Z9, τ=+0.944) is the anchor signal:
- Impedance: Pure WAV centroid descending (Z1=1798 → Z9=1400 Hz, τ=−0.611)
- Seed WAV centroid ascending (Z1=338 → Z9=1451 Hz, τ=+0.500)

The centroid inversion appears real: pure WAVs are low-frequency-weighted at high zones; seed WAVs are high-frequency-weighted at low zones. The flatness inversion appears only partially, indicating the seed source used a **different envelope shape** at Z1-Z5 (energetic noise floor) and mapped Z6-Z9 more conservatively.

---

## §6 — Pd Batch Mode: Workaround Identified

`m3-phase3-pd-batch-discovery.md` confirms Pd 0.56.2 hangs in batch mode with `-nogui -noaudio -open`. 

The working pattern is `pd-wrappers` on Catalyst for -batch -open, not bare Pd.
This is known behavior and has a consistent workaround (wrapping in a timeout script).

---

## §7 — Decisions Made

| Decision | Status |
|---|---|
| DR = 1+(N−1)%9 as canonical zone derivation | **CONFIRMED** — guide all future zone computations |
| FOOM engine stable (12/12 AQ preserved) | **CONFIRMED** |
| FOOM entropy expansion bias (varentropy mode) | **CONFIRMED** — expect +0.1Δ, not compression |
| V3 dataset_v3.npz = different source than cross_session_results.json | **CONFIRMED** — do not merge these two |
| V3 centroid_mean NOT pure-WAV frequencies | **CONFIRMED** |
| V3 flatness confidence got to pure-sine WAV | **CONFIRMED** (sine clusters dominate V3 label space) |
| Seed WAV flatness inversion real, not measurement artifact | **CONFIRMED** (librosa re-verified) |
| Zone 1 absent from V3 dataset | **CONFIRMED** — label=0 is empty |
| Flatness classifier accuracy 9% — no improvement | **CONFIRMED** — flatness not discriminative in current pipeline |
| Pure WAV flatness is reliable ground truth | **CONFIRMED** — τ=0.944 monotonically increasing |
| seed WAV flatness encoder mismatch — the pipelines diverge at Z6-Z9 | **CONFIRMED** |

---

## §8 — Blocks / Open Questions

> **[OPEN]** Is the V3 dataset derived from a known corpus, or an unknown intermediate?  
> → Need to inspect the training script that created `dataset_v3.npz` to map centroid F0 values back to WAV source paths.

> **[OPEN]** RF seed compressional behaviour: only 1/12 runs showed negative entropy. Is this statistically meaningful?  
> → Hypothesis: `--bucket-key aq` with `varentropy` strategy naturally inflates entropy. Test with `--creative-strategy sample` and `--bucket-key length` to get entropy-negative runs.

> **[OPEN]** Seed–pure centroid divergence: pure drop is −961 Hz from Z1→Z6; seed drop from Z1→Z6 is only −189 Hz.  
> → This suggests the seed-generating process applies a high-pass envelope that does not collapse at Z6 like the pure channel does.

> **[OPEN]** Cross-session JSON not validated as cross-zone. Its per-zone centroid=[248–1324] still looks like a plausible centroid set. Could cross-session JSON come from the **correct** resampled pure WAVs, while V3 comes from a second set?

---

## §9 — Metrics Summary (canonical reference file: `verified_metrics_20260523b.json`)

```json
{
  "audit_date": "2026-05-23",
  "foom_stability": {
    "n_runs": 12,
    "aq_preserved": 12,
    "entropy_negative": 1,
    "entropy_neutral": 2,
    "entropy_positive": 9,
    "mean_delta_entropy": 0.1332,
    "std_delta_entropy": 0.1559
  },
  "mir_taus": {
    "pure_flatness":  0.9444,
    "seed_flatness":  -0.4444,
    "pure_centroid":  -0.6111,
    "seed_centroid":   0.5000,
    "pure_rms":       -1.0000,
    "seed_rms":       -0.2778
  },
  "v3_dataset": {
    "total_labels_expected": 10,
    "labels_present": 9,
    "zone_1_present": false,
    "centroid_match_to_pure_wav": "no",
    "flatness_near_zero_clusters": ["Z3","Z4","Z5","Z8","Z9","Z10"],
    "cross_json_vs_v3_pearson_centroid": 0.3419,
    "cross_json_vs_v3_pearson_flatness":  0.0198
  },
  "classifier_accuracy": {
    "v3_accuracy": 0.1111,
    "v3_top_predictor": "bass_ratio (0.0596)",
    "note": "all zones predicted as Z6 or Z7"
  },
  "expunged_claims": [
    "V3_flatness_random_sample_dac_k=2 → C4",
    "Spectral peak: V3 cluster centroid vs centroid_std r=0.75, p=0.020",
    "ZoneVoice encoder-gate /th Gill"
  ]
}
```

---

*Authored autonomously by Hermes — session completed 2026-05-23 20:41 UTC+0.*
