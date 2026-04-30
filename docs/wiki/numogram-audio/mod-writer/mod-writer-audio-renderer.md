# Audio Renderer Integration (Phase 4)

The `audio-renderer` skill provides the perception layer: conversion of binary `.mod` modules into linear PCM audio and extraction of visual/analytic artefacts.

## Rendering pipeline
`render_mod_to_wav(mod_path)` produces a 16‑bit mono WAV at 44.1 kHz.
- Primary backend: `ffmpeg` with `libopenmpt` decoder (recommended).
- Fallback: pure‑Python soft synth (`SoftSynth` from `synth.py`) if `ffmpeg` is unavailable.

Usage via CLI:
```bash
mod-writer --zone 3 --gate 6 --current A --render --output test.mod
```

## Spectrogram generation
`generate_spectrogram(wav_path, colormap='viridis', size='800x400')` emits a PNG spectrogram.
- Filter: `showspectrumpic=scale=log:color=<colormap>:size=<WxH>`
- Validated colormaps: `viridis`, `magma`, `plasma`, `cool`
- Output: `<wav>_spec.png`

Example:
```bash
mod-writer ... --render --spectrogram --colormap magma --spec-size 960x540
```

## Live playback
`play_audio(wav_path, player='ffplay')` sends audio to the system sound device.
Options: `ffplay`, `aplay`, `pw-play`, `mpg123`.

## Feature extraction and verification
`analyze_wav(wav_path)` returns a JSON‑serialisable dictionary with metrics:
- Duration, sample rate, bit depth (`ffprobe`)
- RMS, peak, true‑peak, crest factor (`ffmpeg astats`)
- Integrated loudness (LUFS) (`ffmpeg ebur128`)
- DC offset (`astats.mean`)
- Spectral centroid / roll‑off
- Onset density
- Quality flag: `pass` / `warning` / `fail` (clipping or DC offset)

Flags:
- `--analyze` → writes `<wav>_analysis.json`
- `--describe` → prints a one‑sentence oracle portrait (e.g. `"Zone 3::6 (A) renders a loud, saturated harmonic current…"`)
- `--verify` → exits with code 2 if quality != `pass`

## Manifest aggregation
`--manifest` writes `_manifest.json` bundling:
- Track metadata (zone/gate/current, hypersigil flags)
- File paths (`.mod`, `.wav`, `_spec.png`)
- Optional analysis block
- ISO timestamp

## Compact JSON for TouchDesigner
`--json` emits a small status file next to the `.mod` (or stdout) for TD/automation pipelines.

## Outstanding TODOs
- [ ] Cross‑platform audio player detection
- [ ] Optional higher‑resolution spectrogram (linear scale)
- [ ] Direct waveform visualisation (oscilloscope)
- [ ] Integrated MusicXML export for score rendering
