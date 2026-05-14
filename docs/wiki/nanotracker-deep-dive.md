---
title: "nanoTracker Deep Dive — Web-Based Tracker Architecture"
created: 2026-05-14
last_updated: 2026-05-14
tags: ["tracker", "demoscene", "mod", "web-audio", "javascript", "mod-writer-reference"]
source: "https://federatedindustrial.com/tracker (v2 React app by minexew)"
status: researched
---

# nanoTracker Deep Dive

## What Is It

nanoTracker at federatedindustrial.com/tracker is a **modern React-based web tracker DAW** built with Vite and the Web Audio API. It's the successor to the classic nanoTracker concept but completely reimagined as a full-featured browser-native production tool.

**Key stats:** 1.4 MB total JS across chunks, 894 KB tracker module, 284 Web Audio connect() calls, supports MOD/S3M/XM/IT import with offline rendering to WAV/MP3/OGG.

## Architecture

| Layer | Technology |
|-------|-----------|
| UI | React (JSX components, hooks) |
| Build | Vite (React, code-splitting via lazy chunks) |
| Audio | Web Audio API (OfflineAudioContext for rendering) |
| State | Context API + custom hooks + localStorage persistence |
| File I/O | JSZip for project files, native download/export |
| MIDI | Custom MIDI parser module + Web MIDI API |
| Threading | Web Workers (audio processing, cable physics simulation) |
| Effects | AudioWorklet (bitcrusher), WebAudio nodes for chain FX |

The app lazy-loads chunks: `mp3-D3ifiw-0.js`, `ogg-DNLS9CGd.js`, `workerClient-Bb78O8DW.js`, `midiParser-DuZR7ayc.js`. Only the core tracker loads initially.

## Format Support

### Import (File → Tracker)
| Format | Details |
|--------|---------|
| **MOD IN** | ProTracker / SoundTracker `.mod`. Supports tags: `M.K.`, `M!K!`, `FLT4`, `4CHN`, `6CHN`, `8CHN`, `FLT8`, plus arbitrary `xCHN` / `xxCHN` variants and untagged 15-sample SoundTracker files. Options: channel override (auto/4/6/8), period table (amiga/pc clones), truncated file handling (silent fill/abort), effect interpretation (protracker/noisetracker compat). |
| **S3M IN** | Scream Tracker 3 `.s3m`. Magic `SCRM`. Options: stereo handling (downmix/left/right), sample sign (auto/signed/unsigned), ADPCM samples (skip+warn/skip/abort), empty order list (insert[0]/abort). |
| **XM IN** | FastTracker 2 Extended Module `.xm`. Options: OpenMPT-compatible sample header size (40 bytes default / file-claimed), delta decoding (standard/disable), invalid notes (clamp), multi-sample instruments (full keymap), loop ping-pong. |
| **IT IN** | Impulse Tracker `.it`. "Robust IT2.14/2.15 decompression." |

### Project Save Format (.ftrk)
The native format uses magic `FTRK` with version tracking (max supported: 13). Contains block types:
- `FTRK` — main project file header
- `FXMX` — FX mixer state
- `INTB` — instrument table
- `WPBR` — waveform buffer (sample data)
- `PLGB` — plugin state
- `BNDT` — bind data (routing)
- `SEQB` — sequencer/pattern data
- `POVR` — play state / overlay data
- `PPRS` — project presets

Constants: `Aa=13` (max version), `dm=84` (max patterns), `id=5` (instrument default count).

### Export (Tracker → File)
| Preset | Format | Mode | Notes |
|--------|--------|------|-------|
| WAV 16-BIT | wav16 | offline | dither on, normalize off, 0.05s fade out |
| Shareable MP3 | mp3 | offline | 192 kbps |
| Mastering WAV 24-bit | wav24 | offline | high-res |
| Live Capture WAV 16 | wav16 | realtime | debug mode |
| Stems for DAW | wav24 | offline | individual track rendering |

Export features: dither (16/24-bit), normalization (off/peak/LUFS), tail seconds, fade in/out, stems rendering, metadata (cue points at patterns), ZIP bundling.

## Audio Engine

### Rendering Architecture
- **OfflineAudioContext** for non-realtime rendering (batch export)
- **AudioContext** for live playback with `latencyHint: "interactive"`
- **Bypass compressor** option during rendering for reference
- `sampleRateOverride` support for custom sample rates
- **DC blocker** enabled by default
- **Retro mode** (off by default) — bitcrushing, sample rate reduction, lowpass

### Signal Chain
`samples → channel gain → stereo panner → channel effects → bus effects → master compressor → destination`

284 `connect()` calls indicate a complex routed architecture with multiple effect sends and returns.

### Master Bus Defaults
```
sampleRateOverride: null
masterGainDb: 0
dcBlockerEnabled: false
retroMode: "off"
bitcrushEnabled: false
bitcrushBits: 8
bitcrushRate: 22050
retroLowpassEnabled: false
retroLowpassCutoff: 8000
stereoWidth: 1
panLaw: "equalPower"
analyzerFftSize: 256
analyzerUpdateHz: 30
```

## Effects System

### Pattern Effects (MOD commands, 0-F)
| Code | Name | Description |
|------|------|-------------|
| 0 | ARPEGGIO | Cycle through 3 notes |
| 1 | PORTA UP | Raise pitch by xx period units per tick |
| 2 | PORTA DOWN | Lower pitch by xx period units per tick |
| 3 | TONE PORTA | Glide toward note at speed xx (00 = reuse last) |
| 4 | VIBRATO | x: LFO speed, y: depth (400 continues last) |
| 5 | VOL SLIDE + PORTA | Continue porta 3 + volume slide |
| 6 | VOL SLIDE + VIBRATO | Continue vibrato 4 + volume slide |
| 7 | TREMOLO | Volume LFO, x: speed, y: depth |
| 8 | SET PANNING | 00=hard left, 80=center, FF=hard right |
| 9 | SAMPLE OFFSET | Start playback at xx×256 frames into sample |
| A | VOLUME SLIDE | x: add per tick, y: sub per tick |
| B | POSITION JUMP | Jump to order list position xx |
| C | SET VOLUME | Set channel volume 00–40 |
| D | PATTERN BREAK | End pattern early, row x×10+y |
| E | EXTENDED | Sub-effects Exy (see below) |
| F | SPEED/BPM | <20 = ticks/row, ≥20 = BPM |

### Extended Effects (E1x-E9x)
```
E0x  SET FILTER
E1x  FINE PORTA UP (x period units, once)
E2x  FINE PORTA DOWN (x period units, once)
E3x  GLISSANDO (0=off, 1=semitone steps)
E4x  VIBRATO WAVEFORM (0=sine, 1=ramp, 2=square)
E5x  SET FINETUNE (x = finetune value 0–F)
E6x  PATTERN LOOP (E60=set point, E6x=repeat x times)
E7x  TREMOLO WAVEFORM (0=sine, 1=ramp, 2=square)
E8x  SET PANNING (0=left … 8=center … F=right)
E9x  RETRIGGER (retrigger every x ticks)
```

### FX Chain Effects (mix-level inserts)
| ID | Name | Description | Parameters |
|----|------|-------------|------------|
| `reverb` | REVERB | Convolution reverb with synthetic IR | wet, dry, decay |
| `delay` | DELAY | Stereo delay with feedback | wet, dry, time, feedback |
| `filter` | FILTER | Biquad filter: LP / HP / BP | type, freq, Q |
| `compressor` | COMPRESSOR | Dynamics compressor with makeup gain | threshold, ratio, attack, release |
| `distortion` | DISTORTION | Waveshaper overdrive with tone filter | drive, tone |
| `chorus-flanger` | CHORUS / FLGR | Chorus and flanger with LFO modulation | rate, depth, feedback, mode |
| `bitcrusher` | BITCRUSHER | Bit depth and sample rate reducer | bits (2–16), sample rate |
| `stereo-width` | STEREO WIDTH | Stereo imaging control | width |

Bitcrusher runs as an **AudioWorklet** for real-time performance:
```javascript
new AudioWorkletNode(ctx, "nanotracker.bitcrusher", {
  parameterData: {
    bits: Math.round(s.bits ?? 8),
    sampleRate: s.sampleRate ?? 22050
  }
})
```

## Instrument / Synth Architecture

### Instrument Types
| Type | Description |
|------|-------------|
| `"sample"` | Classic sample-based playback via `AudioBufferSourceNode` with `playbackRate` pitch shifting (semitone calculation: `2^((key - rootKey)/12)`) |
| `"plugin"` | Plugin instruments (e.g., synthesizers) routed through plugin graph builder |
| `"workspace"` | Workspace instruments from external libraries |

### Available Synthesizer Types (in plugin system)
- **sampler** — basic sample playback with gain routing
- **FM** — frequency modulation synthesis via audio-rate oscillators
- **Granular** — granular synthesis with ping-pong and freeze modes
- **Oscillator** — audio-rate oscillator for FM within FX chains
- **Constant** — DC offset / modulation bias source

Oscillator waveform types: `sine`, `triangle`, `square`, `sawtooth`

## UI Layout

```
┌─────────────────────────────────────────────┐
│ Title bar (project name + theme)            │
├─────────────────────────────────────────────┤
│ Transport: ▶ ■ ⏺  |  BPM | Speed | Pos      │
├──────┬──────────────────────┬───────────────┤
│Order │  Pattern Editor      │  Sample List  │
│List  │  (up to 8 ch, 64 rows│  (31 samples, │
│      │   per pattern)       │   7 visible)  │
│      │  Tabs: GRID / FX / SEQ│              │
├──────┴──────────────────────┴───────────────┤
│ VU Meters (per channel + mute buttons)      │
└─────────────────────────────────────────────┘
```

Pattern editor has three tabs:
- **GRID** — classic tracker view
- **FX** — per-row effect automation
- **SEQ** — piano roll sequencer view

## Cable Physics

The tracker features animated cables (connections between visual elements) powered by a **dedicated Web Worker** (`/cable-physics-worker.js`):
- Worker computes physical cable paths via simulation
- Returns `tickResult` with SVG `d` path attributes per cable
- Cables are SVG `<path>` elements with animated midpoint labels
- Falls back to static display if Workers aren't available

This is a visual detail — the physics simulation creates satisfying, organic-looking connections between tracker elements that respond to layout changes.

## MIDI Integration

Full Web MIDI API support via `navigator.requestMIDIAccess({sysex: false})`:
- **MIDI input** — note-on/off, CC, external controller input
- **MIDI thru** — custom routing for hardware monitoring
- **MIDI output** — sending note events to external hardware
- **Hanging note detection** — tracks active notes to prevent stuck notes
- **Inbound by channel** — channel-based MIDI event routing
- MIDI parser module (`midiParser-DuZR7ayc.js`) handles raw MIDI message parsing

## Visualization

Built-in spectrum analyzer:
- `analyzerFftSize: 256` — FFT resolution
- `analyzerUpdateHz: 30` — display refresh rate
- Spectrum and waveform rendering on canvas
- `_drawSpectrum()` and `_drawWaveform()` methods
- `disableSpectrum: false` — can be disabled for performance

## Relevance to mod-writer

### Direct Takeaways
1. **MOD format edge cases** — nanoTracker handles untagged 15-sample SoundTracker files, arbitrary xCHN variants, and period table differences (amiga vs PC clones). Our mod-writer parser should handle these too.
2. **OfflineAudioContext rendering** — same approach we could use for high-quality mod-writer WAV export with dithering.
3. **Effect interpretation modes** — supports both ProTracker and NoiseTracker compatibility modes. Our mod-writer should match one or both.
4. **Sample header sizes** — OpenMPT 40-byte default vs file-claimed. Our parser should be aware of this.
5. **Delta decoding** — XM compression with delta encoding. Worth supporting.

### Architecture Inspiration
1. **Plugin system** — nanoTracker has a plugin instrument architecture with FM, granular, sampler synth types. This maps well to our zone-based synthesis approach.
2. **FX chain** — separate from pattern effects, a post-processing chain that runs on the mix bus. We could add something similar to mod-writer.
3. **Web Audio signal chain** — the 284 connect() calls show a sophisticated routing architecture. Our audio-renderer could learn from this.
4. **Retro mode** — bitcrushing, sample rate reduction, and lowpass filtering as a master effect. Very demoscene.

### Format Comparison
| Feature | mod-writer | nanoTracker |
|---------|-----------|-------------|
| Output format | `.mod` (Protracker) | `.mod` (read) + `.ftrk` (save) |
| FX support | Basic MOD effects (Cxx, Fxx) | Full 0-F + Exy extended effects |
| Rendering | Python-based | Web Audio OfflineAudioContext |
| Audio export | None (MOD only) | WAV/MP3/OGG with dither |
| Channels | 4 | Up to 8 (project supports 2/4/6/8/16/32) |
| Patterns | Basic | Different row counts per pattern |
| Instruments | Samples only | Samples + plugins (FM, granular) |

## Action Items

- [ ] Compare nanoTracker's MOD parser edge cases with mod-writer parser
- [ ] Consider adding offline rendering to mod-writer via Web Audio (or Python equivalent)
- [ ] Explore the .ftrk format spec for potential numogram-native extensions
- [ ] Build a cables.gl visualization bridge using the tracker's MIDI/WebAudio architecture as inspiration
- [ ] Consider adding dither to audio-renderer output (nanoTracker does it by default)
- [ ] Study the plugin synth architecture for zone-based synthesis mapping

## See Also

- [[mod-writer]] — Our MOD file generator
- [[audio-renderer]] — WAV rendering and analysis
- [[cables-gl-visual-programming]] — Visual programming platform (from InterestingSites)
- [[mod-writer-audio-renderer]] — WAV rendering, spectral analysis
- [[tracker-music-theory-mappings]] — Music theory ↔ numogram zone mappings
