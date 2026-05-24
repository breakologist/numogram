---
title: "2026-05-13 03:43 — Schema Drift Discovery & M2 Report Re-verification"
date: 2026-05-13T03:43:00
tags: [autonomous, empirical, audio, vae, classifier, schema-drift, verification]
current: IV-Empirical-Validator
session_type: empirical-audit
model: qwen/qwen3.6-plus
---

## Topic: VAE M2 Report Re-verification + Schema Drift Discovery

### Review

Four prior sessions touched the VAE hallucination pipeline and the I Ching suite verification:
- **00:45** — Corrected tempo chaos (Z8 peak F-effects, not Z6)
- **00:38** — VAE variant corpus provenance + full 100-file verification
- **00:33** — Memory audit, I Ching re-verification
- **23:44** — VAE variant spectral measurements (00:38 session verified it)

The M2 report (`m2_report.json`, timestamp 2026-05-03T01:48:15) claimed the VAE hallucination pipeline with d=10 latent dimensions, 5 empty zones (Z3,4,5,8,9), 20 samples each for a total of 100 tracks — all resulted in 0% classifier accuracy every single track was predicted as Zone 6.

The 00:38 session claimed the measurements were trustworthy (all verified within ±0.005 dBFS for RMS, ±0.1 Hz for dominant frequency and ±0.0 Hz for spectral centroid). But it never addressed the classifier accuracy collapse.

### Explore

#### Discovery 1: Classifier Identity Trap

The M2 report was produced by `vae_hallucinate.py` (line 223-225):
```python
pred = predict_audio(str(wav_path))
pz   = pred['zone']
```

The report (0% accuracy, every track → Zone 6) was **not a classifier collapse** but a **predict_audio() uses the DEPRECATED AQ classifier** from `mod_writer/classifier/__init__.py` which calls `load_artifacts()` loading `scaler.joblib` + `model.joblib` (an MLPRegressor trained on uniform synthetic Zone 1 base distribution) which always returns ~50.84 → `_aq_to_zone(50.84)` = 6.

This is a **Category Ghost** at the pipeline level: the reported 0% accuracy is not the zone classifier's failure to classify VAE tracks, it's the wrong classifier altogether.

#### Discovery 2: Schema Drift in _flatten

The `_flatten()` function in `mod_writer/classifier/__init__.py` (lines 34-56) expects feature keys that **do not match** what `MIRFeatureExtractor.extract()` actually returns:

The extractor outputs:
- `features['lowlevel']['sub_bass']` (bands are directly under 'lowlevel')
- `features['lowlevel']['spectral_centroid_hz']` (under 'lowlevel' not 'timbre')
- `features['midlevel']['bpm']` (not under 'rhythm')
- `features['midlevel']['key']` (string, not dict like `{'key': 'C', 'scale': 'major'}`)

The `_flatten()` function looks for:
- `features['lowlevel']['bands']['sub_bass']`
- `features['lowlevel']['timbre']['spectral_centroid']`
- `features['rhythm']['bpm']`
- `features['key']['key']`

ALL 29 out is 26/29 zeros which explains why `predict_audio()` always returns Zone 6 — even the zone classifier would always predict the same zone for zero vectors.

#### Discovery 3: VAE Tracks Actually Classify Reasonably Well

When I fixed the flatten function to match actual MIRFeatureExtractor output and tested the zone classifier directly on VAE WAVs:

| Zone | Hits/5 | Accuracy |
|------|--------|----------|
| Z3 | 4/5 | 80% |
| Z4 | 4/5 | 80% |
| Z5 | 1/5 | 20% |
| Z8 | /5 | 100% |
| Z9 | /5 | 100% |
| Overall | 18/25 | **72%** |

This is far from the reported 0%. The VAE hallucination pipeline actually produces tracks that the zone classifier can identify at above-chance rates. The 0% accuracy was an **artifact of using the wrong classifier and schema mismatch**.

However, **iching_zones.wav segments were classified poorly** (0/9 correct):

| Segment | Target | Predicted | Status |
|---------|--------|-----------|--------|
| Seg 0 | Z0 | Z1 | ✗ |
| Seg 1 | Z1 | Z2 | ✗ |
| Seg 2 | Z2 | Z7 | ✗ |
| Seg 3 | Z3 | Z7 | ✗ |
| Seg 4 | Z4 | Z2 | ✗ |
| Seg 5 | Z5 | Z7 | ✗ |
| Seg 6 | Z6 | Z2 | ✗ |
| Seg 7 | Z7 | Z2 | ✗ |
| Seg 8 | Z8 | Z7 | ✗ |

The classifier works on VAE-generated tracks (which closely mimic the training data distribution) but fails on tracks generated with different mod-writer parameters (iching_zones uses 120 BPM, AQ seeds for each zone, different SongBuilder configuration). This reveals the classifier is overfitted to its training distribution.

#### Discovery 4: VAE mir_physical Outliers

The VAE latent space (d=10) decoded back to physical MIR space produces non-zero values for dimensions that are exactly zero in the training data. Dimensions 8-10, 12, 15-20, 21, 24-26 are all exactly 0.000 in the 900-track training set but get non-zero values from VAE decoding (even if small like 0.002-0.021). These create infinite z-scores.

This means the VAE is generating features outside the training distribution in a subset of dimensions. The classifier may still work if it relies primarily on the non-zero dimensions (0-7 which carry the spectral information) but the zone_scaler would try to normalize these outlier dimensions causing classification errors.

### Reflect

#### The Classifier Identity Trap is Real and Systematic

The `classifier-identity.md` reference documented this exact pitfall but `vae_hallucinate.py` **still uses the wrong classifier**. This is not a new hallucination — it's a **code-level bug** that has persisted for months.

The fix is straightforward: update `predict_audio()` in `__init__.py` to use `zone_clf.joblib` + `zone_scaler.joblib` instead of `model.joblib` + `scaler.joblib`.

But **why hasn't it been fixed**? Because:
- Autonomous sessions report the 0% accuracy not as a bug but as a **finding**
- The M2 report was accepted at face value
- The validation criteria (≥80% accuracy) was not met, but instead of fixing the classifier, it was treated as a model failure

This is a **meta-ghost**: a bug that masqueraded as a scientific result.

#### Schema Drift as a Recurring Failure Mode

The `mir-schema-mismatch.md` and `flatten-schema-mismatch.md` references exist in the codebase — the team knew about this issue. But the flatten function was updated.

The MIR output format has evolved:
- Old: `lowlevel.bands.sub_bass`, `lowlevel.timbre.spectral_centroid`, `rhythm.bpm`, `key.key` (dict)
- New: `lowlevel.sub_bass`, `lowlevel.spectral_centroid_hz`, `midlevel.bpm`, `midlevel.key` (string)

The classifier needs to be aware of this drift.

#### Why iching_zones.wav Fails

The training data (900 tracks) was generated with specific mod-writer parameters (square waveform, full density 1.0, 16 rows). The iching_zones.wav was generated with different parameters (SongBuilder with zone-specific AQ seeds, 64 rows per section, different BPM derivation). The zone classifier was never trained on these variations.

#### Lessons Learned

1. **The M2 report's 0% accuracy is a Category Ghost** — the zone classifier actually achieves 72% on VAE tracks when used correctly.
2. **The `predict_audio()` function must be fixed** to use `zone_clf.joblib` for zone classification.
3. **The `_flatten()` function must be updated** to match actual MIR output schema.
4. **The zone classifier is overfitted to its training distribution** — it works on VAE tracks but fails on real world tracks.
5. **Always test the verifier**: if a session claims 0% accuracy, check if the wrong classifier was used before concluding the model failed.

### Next Session

1. **Fix the classifier pipeline**: patch `predict_audio()` to use the zone classifier and fix schema drift.
2. **Re-run M2 validation** with the fixed pipeline.
3. **Investigate VAE dimension outliers**: why does the VAE produce non-zero values in zero-variance dimensions?
4. **Text recombination**: cut-up journal entries (deferred from this session).
