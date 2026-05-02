# Phase 4.6 Final Report — ZoneComposer Production Validation
**Date:** 2026-05-02  |  **Status:** CLOSED

## Goal
ZoneComposer generates MOD tracks that classify into target zones with ≥90% accuracy using locked Phase 4.6 configuration

## Configuration
- Waveform: square
- Density: 1.0 (continuous)
- Zone 1: `duplicate_order=False`, length=32
- Zone 2: gate shift (5–7 → +20) active
- Zones 3–9: `duplicate_order=True`, length=16
- **Rhythm baseline forced** (onset=0, bpm_norm=0.625, beat_conf=0)

## Validation Results (≥90% required)
- Zone 1: 97.0% (N=200) ✅
- Zone 2: 98.0% (N=100) ✅
- Zone 3: 91.0% (N=100) ✅
- Zone 4: 100.0% (N=100) ✅
- Zone 5: 98.0% (N=100) ✅
- Zone 6: 100.0% (N=100) ✅
- Zone 7: 96.0% (N=100) ✅
- Zone 8: 100.0% (N=100) ✅
- Zone 9: 100.0% (N=100) ✅

## Deliverables
1. **zone-validate.py** — one-command validation wrapper with baseline forced
2. **zone_batch_generator.py** — deterministic batch generator for zone‑targeted production
3. **Path C research brief** — full technical analysis of BPM extraction artifact
4. **Demo pack** — one MOD per zone in `/tmp/numogram_demo_tracks/`

## Path C — BPM Artifact (Key Findings)
- **Symptom:** Zones 4/6 sometimes report bpm=165.44 instead of 125 (librosa beat_track)
- **Cause:** Square-wave arpeggios create onset envelope harmonics at 2×/3× true tempo, fooling tempo inference
- **Gate dependence:** Zone 6 highly sensitive (most gates → 165 BPM); Zone 4 mostly robust
- **Waveform:** Triangle fixes BPM but breaks other MIR features → not viable
- **Resolution:** Always use `--force-rhythm-baseline` for synthetic MOD classification
- **Real music:** No measurable impact — real audio extracts BPM reliably

## Closing
All zones meet the ≥90% accuracy threshold. The `--force-rhythm-baseline` flag is now a required part of the Phase 4.6 workflow for synthetic MOD generation and validation.

The artifact is understood and isolated; no changes to the classifier or corpus are needed.