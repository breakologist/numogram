---
title: Reverse Transcription — Audio → MOD
author: Hermes Agent
created: 2026-04-30
status: draft
tags: [mod-writer, audio-analysis, reverse-engineering, transcription]
---

# `--from-audio`: Direct Pattern Transcription

**Concept:** Instead of *generating* a new module from an AQ seed, *transcribe*
an existing audio recording directly into a ProTracker pattern, preserving its
rhythmic skeleton and spectral allocation.

This is the most literal form of "making the ears audible": the mod‑writer
listens, detects transients, decides which channel each transient belongs to,
and writes a 4‑channel (or 6‑channel) pattern that *replays* the detected
structure.

---

## How It Works

```
audio.wav  ──►  full_analysis()  ──►  (onsets, band_energies)
                │
                ├─►  row assignment: each onset → pattern row
                ├─►  channel mapping: dominant band per onset → channel 0‑5
                ├─►  period selection: band centre frequency → note period
                └─►  velocity: band energy → sample volume
                ↓
           write .mod pattern
```

### Step‑by‑step

1. **Analysis** (`audio_renderer.full_analysis(path)`)
   - `onsets`: list of timestamps (s) where transient energy peaks
   - `band_energy`: 6‑band FFT per frame; we take the band with max energy at each
     onset time → `dominant_band[i]`
   - `rms`: overall envelope (used for global scaling)

2. **Row mapping**
   - Track length = `rows` (default 64, configurable with `--rows`)
   - Map `onsets` to discrete rows: `row = int(onset / duration * rows)`
   - Clamp duplicate rows to last, leave gaps empty (rests)

3. **Channel allocation** (6 channels total)
   - Channel 0: sub‑bass (Band 0: 0–150 Hz)
   - Channel 1: bass (Band 1: 150–300 Hz)
   - Channel 2: low‑mid (Band 2: 300–1000 Hz)
   - Channel 3: mid (Band 3: 1–3 kHz)
   - Channel 4: high‑mid (Band 4: 3–8 kHz)
   - Channel 5: high (Band 5: 8–22 kHz)

   The band that dominates at each onset determines *which channel* gets a note.
   Other channels stay silent at that row (rest).

4. **Period (pitch) selection**
   Each band has a reference frequency (C2–C6 range):
   | Band | Ref. freq | Note (C‑scale) | Channel |
   |------|-----------|----------------|---------|
   | 0    | 65 Hz     | C2             | 0 |
   | 1    | 130 Hz    | C3             | 1 |
   | 2    | 261 Hz    | C4             | 2 |
   | 3    | 523 Hz    | C5             | 3 |
   | 4    | 1047 Hz   | C6             | 4 |
   | 5    | 2093 Hz   | C7 (high)      | 5 |

   The period table is looked up for the nearest standard period to that
   reference. The note is placed on that channel at that row with that period.

5. **Velocity (volume)**
   - Normalised band energy at onset → sample volume (0–64)
   - Optional global scaling via `--volume` flag

6. **Sample assignment**
   One sample per channel, pre‑loaded at module init:
   - `sub_bass.smp` (channel 0)
   - `bass.smp` (channel 1)
   - ...
   - `high.smp` (channel 5)

   Users can provide custom samples in `samples/` or use built‑in waveforms.

---

## CLI

```bash
# Basic transcription (64 rows, auto-detect duration)
mod-writer --from-audio ballad.wav --output ballad_transcription.mod

# Specify number of rows (higher = finer temporal resolution)
mod-writer --from-audio ballad.wav --rows 128 --output fine.mod

# Use custom samples per band
mod-writer --from-audio ballad.wav \
  --sample-0 sub_kick.smp --sample-1 bass_808.smp --sample-2 mid_piano.smp \
  --output custom.mod

# Combine with AQ motif overlay (add extra notes from a motif on top)
mod-writer --from-audio ballad.wav --triad-motif Warp --rows 64 \
  --output hybrid.mod
```

---

## Python API

```python
from mod_writer.audio_transcriber import AudioTranscriber

# One‑shot
transcriber = AudioTranscriber("ballad.wav", rows=64)
mod_bytes = transcriber.transcribe()

# Or stepwise
analyzer = AudioAnalyzer("ballad.wav")
results = analyzer.full_analysis()
composer = ModComposer()
for onset, band in zip(results['onsets'], results['dominant_bands']):
    row = int(onset / results['duration'] * 64)
    composer.add_note(zone_from_band(band), gate=0, current='A', row=row, channel=band)
composer.write_mod("out.mod")
```

---

## Limitations & Future Work

- **Polyphony:** Only one note per channel per row (standard ProTracker limit).
  If two transients fall on the same row in different bands, the later overwrites.
- **Pitch quantisation:** Band centre frequencies are mapped to nearest standard
  period — micro‑tonal content is lost.
- **Timbre matching:** We assign one static sample per band; real instruments
  change timbre over time. Could add *sample morphing* by having 2–3 variants
  per band and selecting by secondary spectral features.
- **Chords & harmony:** This is a *single‑voice‑per‑band* transcription. Chords
  appear only if multiple bands activate simultaneously across rows.
- **No melody extraction:** We don't attempt `librosa.pyin` pitch tracking yet;
  that would require monophonic assumption or polyphonic transcription (very hard).

Planned improvements:
- [ ] Polyphonic onset grouping → multi‑channel bursts per row (chord detection)
- [ ] Pitch‑accurate mapping via `crepe` or `pyin` (instead of band→fixed note)
- [ ] Sample morphing by timbre class (attack, sustain, release slices)
- [ ] Section‑aware `--from-audio --sections` that splits the audio by structural
      segmentation first, then transcribes each section with different motifs

---

## Example Output Structure

Assuming a 30 s ambient drone with sparse low‑frequency pulses:

```
Row  Channel  Period  Volume  Sample
0    1        170     45      bass.smp       (sub‑bass pulse)
12   0        340     38      sub.smp        (deeper kick)
24   2        85      52      mid.smp        (mid harmonic swell)
36   4        42      30      high.smp       (high air)
48   1        170     40      bass.smp
60   —         —       —       —              (rest)
```

This becomes a *ghost* of the original — a chiptune skeleton that preserves
the temporal distribution and spectral weighting, but rendered in tracker
timbre.

---

## See Also

- `mod-writer-mir-profile.md` — full MIR feature set (this method uses only a
  subset: onsets + band energies)
- `mod-writer-audio2aq.md` — predictive AQ mapping (different goal: *generate new*
  from audio's *essence*, not directly transcribe)
- `mod-writer-audio-renderer.md` — underlying analysis primitives

