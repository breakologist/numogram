# Mod-Writer

## Overview
The Mod-Writer is a Python library and command-line tool for generating Protracker `.mod` files with numogram-native topological extensions. It maps numogram zones, gates, and currents to musical parameters, and supports advanced compositional transforms like syzygy harmony, entropy injection, triangular pattern lengths, and AQ‑seeded gate progressions.

## Provenance
Originally developed by **Hermes Agent** in collaboration with the **CCRU** (Cybernetic Culture Research Unit) lineage, the Mod-Writer integrates historical tracker music practice with numogram combinatorial topology. It is part of the `numogram-audio` skill suite in the Hermes Agent ecosystem.

## Navigation
- **[Usage Guide](mod-writer-usage.md)** — installation, CLI basics, examples.
- **[Motif Reference](mod-writer-motif-reference.md)** — full table of triad motifs (Sink, Warp, Hold, Rise, Void, Monochord, Pythagorean, Ptolemaic, Harmonic) with root, quality, octave, zone triple, and syzygy description.
- **[Triangular Semantics](mod-writer-triangular-semantics.md)** — explanation of triangular pattern length, the 64‑row cap, and its relationship to syzygy topology.
- **[Validation & Inspection](mod-writer-validation.md)** — using `--inspect-motif`, `--validate-motif`, `--validate-all`; examples and link to `canonical_vectors.json`.
- **[Audio Renderer](mod-writer-audio-renderer.md)** — Phase 4 pipeline: rendering to WAV, spectrograms, analysis, manifest generation, and outstanding TODOs.
- **[Just Intonation](mod-writer-just-intonation.md)** — pure-ratio triad tuning (`--just-intonation`) and its musical rationale.
- **[Development Guide](mod-writer-development.md)** — packaging, running tests, contributing, license details.

## Quick example
```bash
mod-writer --zone 3 --gate 6 --current A --syzygy --output chord.mod
```
Generates a four‑channel chord with syzygy harmony on channels 1‑3.

- `mod-writer-mir-profile.md` — MIR profiling API and schema
- `mod-writer-audio2aq.md` — training an audio → AQ mapping model
- `mod-writer-reverse-transcription.md` — `--from-audio` direct transcription

- [[mod-writer-classifier]] — MIR → AQ classifier prototype (Phase 3)
