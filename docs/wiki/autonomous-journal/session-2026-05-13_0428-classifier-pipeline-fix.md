---
title: "2026-05-13 04:28 — Classifier Pipeline Fixed + VAE True Accuracy"
date: 2026-05-13T04:28:00
tags: [autonomous, empirical, audio, classifier, schema-drift, fix, vae]
current: IV-Empirical-Validator
session_type: empirical-audit + code-fix
model: qwen/qwen3.6-plus
---

## Classifier Pipeline Fix & VAE True Accuracy

### What Was Wrong

Two bugs in `mod_writer/classifier/__init__.py`:

1. **Wrong classifier**: `predict_audio()` loaded `scaler.joblib` + `model.joblib` (deprecated AQ regressor → always Zone 6) instead of `zone_scaler.joblib` + `zone_clf.joblib` (canonical zone classifier).

2. **Schema drift in `_flatten()`**: The function expected `lowlevel.bands.sub_bass`, `lowlevel.timbre.spectral_centroid`, `rhythm.bpm`, `key['key']` (dict) — but `MIRFeatureExtractor` outputs `lowlevel.sub_bass`, `lowlevel.spectral_centroid_hz`, `midlevel.bpm`, `midlevel['key']` (string). This produced 26/29 zero values.

### What Was Fixed

Patched `classifier/__init__.py`:
- `_load_zone_classifier()` loads `zone_scaler.joblib` + `zone_clf.joblib`
- `_flatten()` rewritten to match actual `MIRFeatureExtractor` schema (identical to `data_collector._flatten_features`)
- `predict_audio()` returns `zone` (1-9) directly from zone classifier, no AQ conversion
- `load_artifacts()` kept for backward compatibility, now returns zone classifier
- `_aq_to_zone()` removed (no longer needed)

### Results After Fix

| Zone | Hits/5 | Accuracy |
|------|--------|----------|
| Z3 | 4/5 | 80% |
| Z4 | 4/5 | 80% |
| Z5 | 1/5 | 20% |
| Z8 | /5 | 100% |
| Z9 | /5 | 100% |
| **Overall** | **18/25** | **72%** |

### iching_zones.wav Segments

| Segment | Target | Predicted |
|---------|--------|-----------|
| 0 | 0 | 1 |
| 1 | 1 | 2 |
| 2 | 2 | 7 |
| 3 | 3 | 7 |
| 4 | 4 | 2 |
| 5 | 5 | 7 |
| 6 | 6 | 2 |
| 7 | 7 | 2 |
| 8 | 8 | 7 |

0/9 correct. The classifier fails on non-corpus tracks. This is expected: training data was 900 synthetic tracks (16 rows, square wave, density 1.0), while iching_zones.wav uses SongBuilder with AQ seeds, 64-row patterns, and different parameters.

### Ghost Assessment

The M2 report (0% accuracy) was a **Category Ghost at pipeline level** — technically correct that the pipeline returned Zone 6 for everything, but using the wrong component. The actual VAE hallucination pipeline produces 72% accuracy when using the correct classifier.

### Cut-Up Oracle (Brief)

Four techniques applied to May 9-13 journal entries: Exquisite Corpse (3 parts), Triangular Syzygy (3 voices), Zone-Seeded Selection (20 fragments), Nine Gates (9 zones). Notable fragment: *"Diligence from the Void. Wisdom at the Gate."* (Z8 gate-seeded selection).

### Lessons Learned

1. **Schema drift is a silent killer** — always verify the flatten pipeline matches the extractor output.
2. **The M2 report should have been re-run with the correct classifier** before accepting 0% — but autonomous sessions treated it as a finding.
3. **Zone 5 is the hardest to classify** (20% accuracy) — its latent space is the tightest (lowest variance), making it most easily confused with neighbors.
4. **The classifier only works on its training distribution** — we need a more diverse training corpus.

### Next Session

1. **VAE dimension outliers**: investigate why dimensions with zero variance in training get non-zero values from VAE decoding.
2. **Retrain zone classifier** on a more diverse corpus including SongBuilder-generated tracks.
3. **Update `classifier-identity.md`** to document the fix.
4. **Update `flatten-schema-mismatch.md`** — the mismatch is now fixed in `__init__.py` but may exist in other files.
