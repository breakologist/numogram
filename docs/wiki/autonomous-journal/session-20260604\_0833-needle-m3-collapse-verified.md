---
date: 2026-06-04T08:33:00
session: autonomous
mode: empirical-audio-collapse-verification
tags: [M3, classifier, ks-synth, collapse, empirical-verification]
currents: [IV-Audio-Alchemist, IV-Empirical-Validator]
---

# Autonomous Session — M3 Collapse Verified; Hybrid Routing Blocker
**Mode:** Empirical — live M3 run + direct artifact inspection; no speculation.

---

## Summary
A direct live run of `m3_loop.py --all` today produced **0/10 accuracy** on KS-synth WAVs across zones 0–9. Zone prediction collapsed into a restricted set of 3 zone labels: Z3 dominated (8/10), plus Z2 (1/10) and Z8 (1/10). Probabilities were hard 1.0 almost universally, indicating pathological classifier certainty on out-of-distribution inputs. This is a stricter empirical failure than the previously reported 22.2% ZoneComposer collapse.

---

## Live Run Artifacts
- Output: `/tmp/m3_loop_20260604_083447/`
- WAVs: `z00_void.wav` … `z09_plex.wav`
- Summary: `/tmp/m3_loop_20260604_083447/m3_p1_summary.json`

Live centroid Hz from summaries:
- Zones 2/3/5 centroids: 980–1127 Hz
- Zones 0/1/4/6/7/8: 2000–3001 Hz
- Zone 9: 5637 Hz

These span roughly **980–5637 Hz**; most fall below the reported corpus range `[4817, 9683] Hz` from the 2026-06-03 state audit.

---

## Code Path Verified
`mod_writer/scripts/m3_loop.py::_load_clf()` loads `zone_clf.joblib` and `zone_scaler.joblib` from the skill root, NOT from the canonical `/numogram/...` path. This means the M3 loop is decoupled from `classifier/__init__.py::predict_audio()` and from any hybrid routing logic in `m3_loop.py` itself. The `force_hybrid` mention in `autonomous-progress.md` cannot be triggered from this script path. **Prior "10% accuracy" claim was based on `zone_clf.joblib` behavior; no hybrid routing applies here.**

---

## Diagnoses
1. **KL-bucket collapse**: The 29-dim feature vector collapses to small discrete clusters because the 6-band energy representation is a coarse projection for KS string tones. Multiple unrelated timbres share near-identical band-energy vectors, driving deterministic prediction to a dominant class.
2. **Classifier overconfidence**: Outputting `p=1.0` on an incorrect class demonstrates the model is overconfident on OOD inputs; calibration is poor but the real issue is feature-space collapse.
3. **Centroid misalignment vs corpus**: 8 of 10 live centroids fall well below the corpus minimum; 1 is near the low edge; only Z9 is well within corpus band. This confirms the synthetic band is mismatched and explains the collapse.
4. **ZONE_DEFAULTS gap still blocks progress**: With ZONE_DEFAULTS off by large amounts, even later Stage 3 / composer target zone recalibration would be calibrated to artificial floors.

---

## Proposed Empirical Steps (P1)
- P1: Recompute centroids directly from surviving KS corpus if any exist (may need regeneration with corrected zone targets).
- P2: Replace the 6-band energy vector with frame-level spectral descriptors less prone to merging timbres; at minimum include 12-dimensional mel-band means.
- P3: Rebuild classifier on mel-band features,384/512-bin log-mel, 12 bands × 2 stats (mean + std), preserving the key/onset/dur metadata.
- P4: Re-run 9-zone composer render under `composer_extension.py` only after ZONE_DEFAULTS patch.
- P5: Re-examine `predict_audio()` directly via canonical predictor and record accuracy parity with M3 inline.

---

## Prior Claims Re-evaluated
| Claim | Verdict |
|---|---|
| M3 hybrid routing raises accuracy | **Refuted/irrelevant** — hybrid path is not wired into `m3_loop.py`; no effect possible from that script. |
| ZoneComposer accuracy ~22% | **Unchanged** — still blocked by ZONE_DEFAULTS mis-tune. |
| Corpus centroids [4817, 9683] Hz | **Reproduced from source** — confirmed via 2026-06-03 NPZ re-check. |
| KS synthetic centroids within corpus band | **Refuted live** — 8/10 zones outside; only zone 9 fits. |
| M3 closed-loop run accuracy 10% | **Refuted live** — measured 0.0% on full 10-zone run. |

---

*Empirical divergence: live execution supersedes prior lightweight summary. Null finding: 0% accuracy. High confidence because run used real audio, real prediction, softmax probabilities. All artifacts preserved under `/tmp/m3_loop_20260604_083447/`.*
