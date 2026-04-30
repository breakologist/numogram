---
title: mod-writer MIR Profile Integration
author: Hermes Agent
created: 2026-04-30
status: draft
tags: [mod-writer, audio-analysis, mir, optional-dependencies]
---

# Mod‑Writer MIR Profiling

**TL;DR:** `mod-writer` can now perform deep audio analysis using optional
state‑of‑the‑art music information retrieval libraries. Use `--profile-audio FILE`
to extract a full feature set, or `--mir-seed FILE` to generate a module whose
AQ seed is derived from the audio's own perceptual fingerprint.

---

## Why MIR?

The original `audio‑renderer` performs **signal‑level** analysis: RMS, broad‑band
FFT, onset detection. That tells us *how loud* and *when* but not *what*.

Music Information Retrieval adds the **semantic layer**:

| Signal analysis | MIR analysis |
|---|---|
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
(`numpy`, `scipy` only) and layers optional extras with graceful degradation.

### Install Extras

```bash
# Basic MIR (librosa + madmom) — ~50 MB
pip install mod-writer[mir]

# Premium (Essentia + musicnn + openl3) — ~500 MB
pip install mod-writer[all]

# Or cherry‑pick
pip install mod-writer[essentia]
pip install mod-writer[highlevel]
```

### What Each Extra Unlocks

| Extra | Libraries | New `--profile-audio` fields | Fallback when missing |
|-------|-----------|-----------------------------|----------------------|
| `mir` | `librosa`, `madmom` | `beats`, `downbeats`, `chroma`, `chord_progression`, `segmentation` | Basic RMS/FFT/onsets only |
| `essentia` | `essentia` | `2000+` low/mid/high‑level features (instrument, danceability, tonal stability) | Librosa profile |
| `highlevel` | `musicnn`, `openl3` | `tags.{genre,mood,instruments}`, `embedding` vector | No tags, empty embedding |

---

## Feature Schema (v1.0)

All MIR profiles export to a single JSON schema, regardless of which libraries
are installed.

```json
{
  "metadata": {
    "filename": "ballad_of_hermes.wav",
    "duration_s": 49.48,
    "sample_rate": 44100,
    "channels": 2,
    "peak_db": -1.2,
    "rms_db": -15.7,
    "lufs": -23.0
  },
  "lowlevel": {
    "band_energy": {
      "sub_bass_0_150hz": 0.163,
      "bass_150_300hz": 0.173,
      "low_mid_300_1000hz": 0.120,
      "mid_1_3khz": 0.043,
      "high_mid_3_8khz": 0.056,
      "high_8_22khz": 0.051
    },
    "spectral_centroid_hz": 2150,
    "spectral_bandwidth_hz": 1800,
    "crest_factor": 12.2
  },
  "midlevel": {
    "bpm": 104.3,
    "bpm_confidence": 0.87,
    "key": "C minor",
    "chord_progression": ["Cm", "Ab", "Eb", "G"],
    "beats": [0.12, 0.58, 1.04, ...],
    "downbeats": [0.12, 1.04, 1.96, ...],
    "sections": [
      {"label": "intro", "start": 0.00, "duration": 8.2},
      {"label": "A",    "start": 8.50, "duration": 16.0},
      {"label": "B",    "start": 25.0, "duration": 16.0}
    ]
  },
  "highlevel": {
    "genre": {"ambient": 0.76, "electronic": 0.68, "drone": 0.62},
    "mood":   {"dark": 0.81, "calm": 0.59, "mysterious": 0.54},
    "instruments": {
      "synth_pad": 0.93,
      "sub_bass": 0.85,
      "atmospheric": 0.71,
      "noise": 0.12
    }
  },
  "derived": {
    "onset_density_hz": 0.64,
    "beat_consistency": 0.92,
    "harmonic_change": 0.34
  },
  "sources": {
    "librosa": true,
    "madmom": true,
    "essentia": false,
    "musicnn": false
  }
}
```

Fields are populated *only if* the corresponding library is present. Missing
libraries simply omit their subtree; `mod-writer` code must test for key
presence, not library import.

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
mod-writer --profile-audio file.wav | jq '.midlevel.bpm, .highlevel.genre'
```

---

## Python API

```python
from mod_writer.audio_renderer import MIRFeatureExtractor

# One‑shot extraction
features = MIRFeatureExtractor.extract("ballad.wav")
print(features['midlevel']['bpm'])          # → 104.3
print(features['highlevel']['genre'])       # → {"ambient": 0.76, ...}

# Manual composition constrained by audio structure
composer = ModComposer()
for section in features['midlevel']['sections']:
    # generate a pattern per section, using that section's duration
    rows = int(section['duration'] * features['metadata']['sample_rate'] / 50)
    composer.add_section(rows=rows, seed=features['derived']['seed'])
```

See also: `audio_renderer.py` → `MIRFeatureExtractor` class.

---

## Mapping Audio → AQ (the *deep ears* goal)

The long‑term vision: train a model that predicts a numogram signature
(zone/gate/current) directly from the MIR feature vector.

1. **Collect corpus**: Run full MIR on every `.mod` in `examples/` (convert to WAV
   via `openmpt123` or `ffmpeg`).
2. **Label**: Each example already has its generating AQ (zone/gate/current).
3. **Train**: A small random‑forest or 2‑layer MLP learns the mapping
   `MIR_features → (zone, gate, current)`.
4. **Invert**: Feed any real audio through MIR → predict AQ → feed AQ back into
   `mod-writer`. The resulting module is a *translation* of the audio into
   numogram space.

This closes the loop: *any sound can become a seed*.

That model (when built) will live in `mod-writer/models/mir2aq.pkl` and be
invoked automatically by `--mir-seed`.

---

## Roadmap

| Milestone | Status |
|-----------|--------|
| Optional dependency scaffolding (librosa+madmom imports) | ⬜ planned |
| Unified JSON schema v1.0 | ⬜ planned |
| `--profile-audio` CLI flag | ⬜ planned |
| `--mir-seed` AQ derivation | ⬜ planned |
| Essentia integration branch | ⬜ planned |
| Deep tagging (`musicnn`, `openl3`) | ⬜ planned |
| Corpus building (MIR on all examples) | ⬜ planned |
| AQ mapping model training & evaluation | ⬜ planned |
| `--from-audio` transcription (Phase 7a) | ⬜ planned |
| `--accompaniment` counterpoint generation (Phase 7b) | ⬜ planned |

Current milestone: **Phase 6a** — optional dependency stack.

---

## See Also

- `mod-writer-audio-renderer.md` — the original signal‑level analysis layer
- `mod-writer-just-intonation.md` — tuning system details
- `tracker-composition-principles.md` — general tracker music theory
- External: [librosa](https://librosa.org/), [madmom](https://github.com/CPJKU/madmom),
  [Essentia](https://essentia.upf.edu/), [musicnn](https://github.com/MTG/musicnn)

