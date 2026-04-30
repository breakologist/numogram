---
title: Audio → AQ Mapping
author: Hermes Agent
created: 2026-04-30
status: draft
tags: [mod-writer, mir, machine-learning, audio-to-aq]
---

# Audio → AQ Mapping (mod-writer deep ears)

**Goal:** Given any audio recording, predict the numogram zone/gate/current
that *best describes* its musical character, then generate a `.mod` file in that
signature — effectively *translating* the audio into numogram‑native tracker
composition.

This is the counterpart to `--mir-seed`: instead of a textual AQ seed, we use
the audio's own perceptual fingerprint as the seed.

---

## The Mapping Problem

We want a function:

```
MIR_features(wav) → zone (1–9), gate (0–36), current (A/B/C)
```

Given our corpus of existing generated modules (each with a known AQ), we can
train this as a **multi‑output regression** (for zone/gate as continuous) or
**multi‑label classification** (for discrete buckets).

### Input Feature Vector (≈ 150–2000 dimensions)

Depends on installed MIR stack:

- **Librosa baseline**: MFCC (13), chroma (12), spectral contrast (6), tempo (1),
  onset density (1) → ~33 features
- **Essentia**: 2000+ descriptors — we'll select a subset (low‑dimensionality PCA)
- **musicnn embeddings**: 2048‑D activations from penultimate layer

We'll normalise all features to zero mean, unit variance across the corpus.

### Targets

For each training example (a generated `.mod` file):

```python
{
  "zone": 3,          # integer 1–9
  "gate": 14,         # integer 0–36
  "current": "B",     # A, B, or C
  "aq_seed": "3.14.f",  # original seed string
  "file": "examples/warp-001.mod"
}
```

---

## Training Pipeline

### 1. Corpus Assembly

All `.mod` files under `examples/` (and optionally `mod-imports/`) are converted
to WAV for MIR analysis. Script: `scripts/build_mir_corpus.py`.

Output: `corpus/metadata.csv` with columns:
`filepath, zone, gate, current, aq_seed, wav_path`

### 2. Feature Extraction

For each WAV, run the full MIR pipeline (with *all* optional deps installed on
the training machine). Cache results to `corpus/features/<hash>.json` to avoid
re‑processing.

Aggregate into a design matrix `X (n_samples, n_features)` and label vectors
`y_zone, y_gate, y_current`.

### 3. Model Selection

We'll try:

- **Random Forest** (sklearn) — interpretable, handles mixed scales well
- **MLP Regressor** (sklearn) — small 2‑layer network for non‑linear mapping
- **Gradient Boosting** (XGBoost) — if we add more high‑level features

For `current` (A/B/C) we train a 3‑way softmax classifier; for zone/gate we
train separate regressors and bucket outputs to nearest integer.

### 4. Evaluation

Hold out 20% of the corpus. Metrics:

- Zone accuracy: ±1 discrete error allowed (1 off is still meaningful)
- Gate MAE (mean absolute error) — target ≤ 3.0 gates
- Current classification accuracy — target ≥ 85%

If baseline (random) is 33% for current, we want significantly better.

### 5. Deployment

Save best model pair to `mod-writer/models/mir2aq.pkl`:
```python
{
  "zone_model": RandomForestRegressor(...),
  "gate_model": RandomForestRegressor(...),
  "current_model": LogisticRegression(...),
  "scaler": StandardScaler(...),
  "feature_names": [...],
  "training_metadata": {...}
}
```

At runtime, `MIRFeatureExtractor.predict_aq(wav_path)` loads the model (if
present) and returns `(zone, gate, current, confidence)`.

---

## Using `--mir-seed`

```bash
# Extract MIR features from an audio file, predict AQ, generate a module
mod-writer --mir-seed ballad_of_hermes.wav --triad-motif Warp --output sibling.mod

# With just intonation
mod-writer --mir-seed ballad.wav --just-intonation

# Override the motif selection, keep the seed
mod-writer --mir-seed ballad.wav --triad-motif Mesh --output sibling-mesh.mod
```

If the mapping model is not installed, `--mir-seed` falls back to:  
`hash(MIR_feature_vector)[:8]` → numeric seed → convert to AQ via zone
conversion. Still deterministic, less semantically meaningful.

---

## Expected Behaviour

Given an audio file with:
- **Low‑frequency emphasis** (sub‑bass dominant)
- **Slow tempo** (~100 BPM)
- **Ambient genre tags** (ambient, drone, dark)
- **No chord changes** (static harmony)
- **Long sustained notes**

Predicted mapping should lean toward:
- **Zone 0 or 2** (voidal / generative drones)
- **Gate ≈ 10–14** (sliding pitch effects, sustained)
- **Current A** (square, clean tones)

Generated module will then use a motif that favours long, low, slowly evolving
patterns — a *sonic translation* of the input's mood.

---

## Roadmap to Full Corpus

Immediate next steps (v0.6.1):

1. Run MIR profiling on all existing `examples/*.mod` (convert to WAV)
2. Export CSV `corpus/metadata.csv` with known AQ labels
3. Train baseline Random Forest on Librosa features only
4. Evaluate accuracy
5. Document findings in this page

Longer-term (v0.7.0+):
- Add Essentia features, retrain
- Add deep embeddings (musicnn), fine‑tune on our corpus
- Publish the trained model for community use
- Consider *inverse* model: from AQ → audio feature constraints (guiding
  generation to match a reference track's timbre/rhythm)

---

## See Also

- `mod-writer-mir-profile.md` — the MIR feature extraction layer
- `mod-writer-reverse-transcription.md` — direct audio → pattern mapping (rows ← peaks)
- `mod-writer-audio-renderer.md` — original signal analysis foundation
- External: [librosa](https://librosa.org/), [Essentia](https://essentia.upf.edu/),
  [musicnn](https://github.com/MTG/musicnn)

