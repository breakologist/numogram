---
title: mod-writer MIR Profile Integration (Phase 4.2)
author: Hermes Agent
created: 2026-04-30
updated: 2026-04-30
status: in-progress
tags: [mod-writer, audio-analysis, mir, essentia, optional-dependencies, phase-4]
---

# Mod‑Writer MIR Profiling — Extended

**TL;DR:** `mod-writer` performs deep audio analysis using optional state-of-the-art
music information retrieval libraries. Use `--profile-audio FILE` to extract a full
feature set, or `--mir-seed FILE` to generate a module whose AQ seed is derived from
the audio's own perceptual fingerprint.

**Phase 4.2:** The `use_all=True` flag now invokes Essentia's `MusicExtractor`, adding
60–100+ scalar descriptors to the feature vector in a single call — opening the door
to high‑dimensional AQ prediction.

---

## Why MIR?

The original `audio-renderer` performs **signal‑level** analysis: RMS, broad‑band FFT,
onset detection. That tells us *how loud* and *when* but not *what*.

Music Information Retrieval adds the **semantic layer**:

| Signal analysis | MIR analysis |
|----------------|--------------|
| RMS envelope | Beat positions & tempo |
| 6‑band FFT | Chroma (key, chord progression) |
| Onset count | Downbeat structure & section boundaries |
| Peak amplitude | Instrument activation (which sounds are present) |
| Spectral centroid | Timbre descriptors (bright, warm, harsh) |
| — | Genre & mood classification |
| — | Pitch & melody contour |

With MIR, *The Ballad of Hermes* stops being "a 49 s file with low‑freq bias" and
becomes "a 104 BPM ambient‑drone in C minor with sparse sub‑bass pulses, synth‑pad
sustains, no discernible melody, and a dark‑ambient genre signature."

That's the level of *listening* we want the oracle to have.

---

## Optional Dependency Model

MIR libraries are **heavy** and **optional**. `mod-writer` keeps its core lightweight
(`numpy`, `scipy`) and layers optional extras with graceful degradation.

### Install Extras

```bash
# Basic MIR (librosa + madmom) — ~50 MB
pip install mod-writer[mir]

# Premium (Essentia + musicnn + openl3) — ~500 MB
pip install mod-writer[all]

# Or cherry-pick
pip install mod-writer[essentia]
pip install mod-writer[highlevel]
```

### What Each Extra Unlocks

| Extra  | Libraries | New `--profile-audio` fields | Fallback when missing |
|--------|-----------|------------------------------|----------------------|
| `mir`  | `librosa`, `madmom` | `beats`, `downbeats`, `chroma`, `chord_progression`, `segmentation` | Basic RMS/FFT/onsets only |
| `essentia` | `essentia` | `2000+` low/mid/high‑level features (instrument, danceability, tonal stability) | Librosa profile |
| `highlevel` | `musicnn`, `openl3` | `tags.{genre,mood,instruments}`, `embedding` vector | No tags, empty embedding |

---

## Feature Schema (v2.0 — `use_all=True` path)

All MIR profiles export to a single JSON schema, regardless of which libraries
are installed.

### Base profile (always populated)

```json
{
  "metadata": {
    "filename": "ballad_of_hermes.wav",
    "duration_s": 49.48,
    "sample_rate": 44100,
    "channels": 2,
    "peak_db": -1.2,
    "rms_db": -15.7
  },
  "lowlevel": {
    "bands": {"sub_bass":0.16,"bass":0.17,"low_mid":0.12,"mid":0.04,"high_mid":0.06,"high":0.05},
    "spectral_centroid_hz": 2150,
    "spectral_bandwidth_hz": 1800,
    "crest_factor": 12.2
  },
  "midlevel": {
    "bpm": 104.3,
    "beat_confidence": 0.87,
    "key": "C",
    "scale": "minor",
    "key_strength": 0.76
  },
  "highlevel": { ... },
  "derived": {
    "onset_density_hz": 0.64
  },
  "sources": {
    "librosa": true, "madmom": false, "essentia": false, "musicnn": false
  }
}
```

### Essentia full‑pool (`use_all=True`)

When `essentia` is installed **and** `MIRFeatureExtractor.extract(use_all=True)` is
called, the extractor runs Essentia's `MusicExtractor` with `lowlevelStats`,
`rhythmStats`, and `tonalStats` set to compute mean/stdev across frames. Every
**scalar** descriptor from the returned pool is flattened into a new top-level key:

```json
{
  "essentia_features": {
    "lowlevel.spectral_centroid_mean": 2150.0,
    "lowlevel.danceability": 0.42,
    "rhythm.bpm": 104.3,
    "tonal.key_key": 0,
    "tonal.key_scale": 2,
    "...": "~60–100 more scalar fields"
  },
  "sources": { "essentia_pool": true }
}
```

**Implementation:** Vector-valued descriptors are currently skipped; only scalars
(floats, ints, 1‑element arrays) are appended. The field names are Essentia's
canonical descriptor names (e.g. `lowlevel.spectral_contrast_mean`). Order is
sorted alphabetically when the feature vector is flattened by `_flatten_features()`.

**Impact:** Base vector (29) → ~29 + N Essentia scalars (typically 60–100 total).
No new dependencies beyond `essentia`; the same CLI flag (`--profile-audio`) picks
up the expanded profile automatically when `use_all=True` is passed from the
trainer/data‑collector pipeline.

---

## Python API

```python
from mod_writer.mir_profiler import MIRFeatureExtractor

# Base profile only (backward‑compatible)
features = MIRFeatureExtractor.extract("track.wav", use_all=False)
print(features['midlevel']['bpm'])          # → 104.3

# Full Essentia pool (Phase 4.2)
features_all = MIRFeatureExtractor.extract("track.wav", use_all=True)
essen = features_all.get('essentia_features', {})
print(f"Essentia contributed {len(essen)} scalar descriptors")
```

---

## CLI Usage

```bash
# Profile only (JSON to stdout)
mod-writer --profile-audio ballad.wav > ballad_profile.json

# Derive an AQ seed from the profile and generate a module
mod-writer --mir-seed ballad.wav --triad-motif Warp --output ballad-sibling.mod

# Combine with other flags
mod-writer --mir-seed ballad.wav --just-intonation --bpm 104 --output ballad-ji.mod

# Verbose: see which libraries were used
mod-writer --profile-audio ballad.wav --verbose 2>&1 | grep 'MIR sources'
```

Output is always valid JSON. Pipe to `jq` for inspection:

```bash
mod-writer --profile-audio file.wav | jq '.midlevel.bpm, .essentia_features | keys'
```

---

## Mapping Audio → AQ (the *deep ears* goal)

The long‑term vision: train a model that predicts a numogram signature
(zone/gate/current) directly from the MIR feature vector.

1. **Collect corpus**: run full MIR on every `.mod` in `examples/` (convert to WAV
   via `openmpt123` or `ffmpeg`).
2. **Label**: each example already has its generating AQ (zone/gate/current).
3. **Train**: a small random‑forest or 2‑layer MLP learns the mapping
   `MIR_features → (zone, gate, current)`.
4. **Invert**: feed any real audio through MIR → predict AQ → feed AQ back into
   `mod-writer`. The resulting module is a *translation* of the audio into
   numogram space.

This closes the loop: *any sound can become a seed*.

---

## Roadmap (Phase 4)

| Milestone                                   | Status |
|--------------------------------------------|--------|
| Phase 4.1 — Balanced multi‑zone dataset      | 🟡 in progress |
| Phase 4.2 — Essentia full‑pool integration   | 🟡 in progress |
| Phase 4.3 — Zone‑classifier training         | planned |
| Phase 4.4 — Vocal presence detection         | optional |
| Phase 4.5 — Validation suite + tuning        | planned |

Current milestone: **Phase 4.2** — hook Essentia's `MusicExtractor` into the trainer.

---

## See Also

- `mod-writer-classifier.md` — AQ/zone prediction pipeline
- `mod-writer-audio-renderer.md` — signal‑level analysis layer
- `mod-writer-just-intonation.md` — tuning system details
- External: [librosa](https://librosa.org/), [madmom](https://github.com/CPJKU/madmom),
  [Essentia](https://essentia.upf.edu/), [musicnn](https://github.com/MTG/musicnn)
