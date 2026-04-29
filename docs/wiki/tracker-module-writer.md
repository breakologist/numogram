---
title: Tracker Module Writer — Numogram Audio Engine
created: 2026-04-28
last_updated: 2026-04-29
source: "Hermes Agent — numogram-audio/mod-writer skill (v0.4.0)"
status: active
tags: ["numogram", "tracker", "mod-file", "protracker", "phase-2", "phase-3", "phase-4", "skill", "audio", "hypersigil", "composition"]
zone: 3
syzygy: djynxx
---

# Tracker Module Writer — Numogram Audio Engine

> **Phases 1–4 complete**. A minimal Python implementation of the Protracker M.K. format with full numogram-native mappings, composer API, audio rendering pipeline, and TouchDesigner integration. The numogram as chiptune hypersigil.

**The Mod Writer** is a canonical toolchain that turns numogram traversal data into audible, playable `.mod` modules. It maps **zone** (1–9) → pentatonic pitch, **gate** (0–36) → effect families, and **current** (A/B/C) → instrument timbres. The mapping is not metaphorical — it is operational. Each generated module preserves its generative signature in metadata (title, sample names), creating a traceable chain from seed to sound.

## Nature & Structure

### Core Architecture (Four-Phase Stack)

| Phase | Status | Deliverable | Technical scope |
|-------|--------|-------------|-----------------|
| **Phase 1 — Binary writer** | ✓ | Valid M.K. `.mod` output | 4-channel, 31 samples, ≤64 patterns; period-based notes; no effects |
| **Phase 2 — Numogram mapping** | ✓ | Zone/gate/current → music | Pentatonic mapping, effect families, instrument selection, metadata embedding |
| **Phase 2b — Composer bridge** | ✓ | `ModComposer` API | Event-list model (`add_note`, `apply_syzygy_harmony`, `inject_entropy`, `constrain_gates_by_aq`) |
| **Phase 3 — Hypersigil extensions** | ✓ | Syzygy harmony, entropy, triangular lengths, AQ seeding | Triangular syzygy chords, pentatonic glitch-layers, triangular pattern durations, AQ-hash gate modulation |
| **Phase 4 — Audio rendering** | ✓ | MOD → WAV/OGG + spectrogram + analysis | `ffmpeg`/`libopenmpt` decoder, soft-synth fallback, spectrogram generation, basic audio features, TouchDesigner `td_state.json` watcher |

All phases are implemented and committed. Current skill version: **0.4.0**.

### Binary Format — Protracker M.K. (1084-byte header)

The writer produces strictly valid M.K. modules:

- **Patterns**: up to 64 rows × 4 channels; each cell 4 bytes (period, sample, effect, param)
- **Samples**: up to 31 entries; 30-byte header each + raw 8-bit offset-binary PCM
- **Magic**: `M.K.` at offset 1080 (two-byte marker identifying 4-channel format)
- **Period table**: Amiga PAL-based semitone → period conversion (3546895 Hz clock)

Pattern cell encoding (4 bytes):
```
byte1 = (sample_hi << 4) | period_hi   (sample bits 5-8, period bits 12-15)
byte2 = period_lo                       (period bits 0-7)
byte3 = (sample_lo << 4) | eff_hi       (sample bits 1-4, effect bits 4-7)  
byte4 = eff_lo                          (effect bits 0-3 or param low nibble)
```

### Numogram Mapping — The Three Axes

| Numogram concept | Musical realisation | Implementation |
|------------------|--------------------|----------------|
| **Zone** (1–9) | Pentatonic degree (C D E G A) + octave | `ZONE_TO_NOTE`, `ZONE_TO_OCTAVE`; zone 9 = REST |
| **Gate** (0–36) | Effect family (arpeggio / slide / volume / special) | `GATE_TO_EFFECT` → `mod_effect_from_gate()` |
| **Current** (A/B/C) | Waveform selection (square / triangle / noise) | `CURRENT_TO_INSTRUMENT` → sample index 1/2/3 |

#### Zone → Note mapping (pentatonic C major)

Zones 1–5 play in octave 4; zones 6–8 shift up to octave 5; zone 9 rests.

| Zone | Note | Octave | Frequency (approx) |
|------|------|--------|-------------------|
| 1 | C | 4 | 261.6 Hz |
| 2 | D | 4 | 293.7 Hz |
| 3 | E | 4 | 329.6 Hz |
| 4 | G | 4 | 392.0 Hz |
| 5 | A | 4 | 440.0 Hz |
| 6 | C | 5 | 523.3 Hz |
| 7 | D | 5 | 587.3 Hz |
| 8 | E | 5 | 659.3 Hz |
| 9 | REST | — | — |

#### Gate → Effect mapping (Protracker effect commands)

| Gate range | Effect family | Command | Parameter encoding |
|------------|---------------|---------|-------------------|
| 0–9 | **Arpeggio** (pattern variations) | `0x0` | Symmetric nibble pair `(g, g)` |
| 10–19 | **Portamento up** (pitch slide) | `0x1` | Speed = `(gate−10) × 25` (0–225) |
| 20–29 | **Set volume** | `0xA` | Volume = `(gate−20) × 6` (0–54 / 64 max) |
| 30 | **Position jump** (order jump) | `0xB` | — |
| 31 | **Pattern break** | `0xB` | — |
| 32–34 | **Extended effects** (filter/reserved) | `0xE` | Subcommand = `gate−32` |
| **35** | **Syzygy** (reserved for triangular harmony) | `0xE` | Param `10` |
| **36** | **Entropy** (reserved for glitch- injection) | `0xF` | Param `36` |

Gate 35 and 36 are reserved for Phase 3 hypersigil effects (Syzygy harmony, Entropy injection).

#### Current → Instrument mapping

| Current | Waveform | Sample index | Sound character |
|---------|----------|--------------|-----------------|
| A | Square wave | 1 | 8-bit chiptune lead |
| B | Triangle wave | 2 | Muted, flute-like |
| C | White noise | 3 | Percussive / snare-like |

#### Syzygy-harmony partners (triangular completion)

Each zone has 1–5 partner zones on the syzygy (sum-9 or sum-10 pairs). The `apply_syzygy_harmony()` pass copies the root note to partner channels with partner zones.

```python
SYZYGY_PARTNERS = {
    1: (5, 9),   2: (4, 8),   3: (6, 9),
    4: (2, 7),   5: (1, 6),   6: (3, 5),
    7: (4, 9),   8: (2, 9),   9: (1, 3, 5, 7, 8)
}
```

Zone 9 partners with five zones (1, 3, 5, 7, 8) — harmony truncates to first 3 partners (channels 1–3) due to 4-channel limit.

#### Pentatonic adjacency (entropy injection graph)

Entropy substitutes a note's zone with a neighbouring pentatonic zone:

```python
PENTATONIC_ADJACENCY = {
    1: (2, 5),   # C → D, A
    2: (1, 3),   # D → C, E
    3: (2, 4),   # E → D, G
    4: (3, 5),   # G → E, A
    5: (1, 4),   # A → C, G
    6: (7, 2),   # C(5) → D, E (octave-shifted mapping)
    7: (6, 8),   # D(5) → C(5), E(5)
    8: (7, 9),   # E(5) → D(5), REST
    9: (8, 1, 3, 5, 7),  # REST adjacent to all touching zones
}
```

### Metadata — Story Layer

`.mod` files lack comment fields, so generative context is encoded into fixed-length fields:

- **Song title** (20 bytes): `Z{z}G{ggg}{C}-{title}` e.g. `Z03G006A-WarpEntry` (zone 3, gate 6, current A)
- **Sample names** (22 bytes each): `{wave}-Z{z}-G{ggg}-{C}` e.g. `SQ-Z03-G006-A` (square, zone 3, gate 6, A)

This mirrors the modarchive tradition of cryptic-but-informative identifiers; the numogram story is recoverable by parsing the title/sample names.

## Composer API — High-Level Orchestration

The `ModComposer` class provides an event-list model mirroring `mido.MIDIFile`. Notes are placed on a grid `(row, channel) → (zone, gate, current)`; transformation passes are applied; then the grid encodes to binary patterns.

### Core methods

```python
from numogram_audio.mod_writer.composer import ModComposer

comp = ModComposer(title="Syzygy Étude")

# Place notes on the grid
for r in range(16):
    comp.add_note(zone=3, gate=6, current='A', row=r, channel=0)

# Transforms (order matters: harmony → entropy → AQ shift)
comp.apply_syzygy_harmony(partner_channels=[1,2,3])      # triangular chords
comp.inject_entropy(rate=0.1, rng_seed=42)              # 10% zone-glitch
comp.constrain_gates_by_aq("WR-3-6")                     # AQ-gated effects
comp._triangular = True                                  # T(zone) rows
comp.write_mod("syzygy_etude.mod")
```

Or one-shot convenience:

```python
ModComposer.compose(
    zone=3, gate=6, current='A', rows=16,
    syzygy=True, entropy=0.1, triangular=True, aq_seed="WR-3-6",
    output="etude.mod"
)
```

### Transformation pass pipeline

1. **Seed placement** — linear sequence or event-grid fill
2. **Syzygy harmony** — duplicate root notes to partner zones on channels 1–3
3. **Entropy injection** — each note has `rate` probability of zone-substitution to adjacent pentatonic zone
4. **AQ constraint** — all gate values shifted by `(SHA1(seed) mod 37)` delta
5. **Pattern length resolution** — `rows` or `triangular=T(zone)` caps at 64

Passes are **commutative in effect** (order of application only, not on/off toggles).

### Grid API

| Method | Purpose |
|--------|---------|
| `add_note(zone, gate, current, row, channel)` | Place single note |
| `add_sequence(zones, gates, currents, start_row, channel)` | Batch linear sequence |
| `apply_syzygy_harmony(partner_channels=[1,2,3])` | Triangular chord generation |
| `inject_entropy(rate, rng_seed=None)` | Pentatonic neighbour substitution |
| `constrain_gates_by_aq(aq_seed)` | Deterministic gate modulation via AQ hash |
| `build_patterns_from_grid(length, triangular)` | Encode grid → Pattern object |
| `write_mod(filename)` | Finalise samples + patterns → binary file |

## CLI Reference

Standalone entry point: `python -m numogram_audio.mod_writer`

### Basic generation (Phase 2)

```bash
python -m numogram_audio.mod_writer \
  --zone 3 --gate 6 --current A \
  --title "Warp Entry" --output warp.mod
```

### Hypersigil flags (Phase 2b/3)

| Flag | Meaning | Notes |
|------|---------|-------|
| `--syzygy` | Add syzygy harmony on channels 1–3 | Triangular chord from partner zones |
| `--syzygy-channels N` | Number of harmony channels (1–3, default 3) | Truncates zone 9's 5 partners to first N |
| `--entropy RATE` | Entropy injection rate (0.0–1.0) | Pentatonic neighbour substitution |
| `--entropy-seed N` | RNG seed for reproducible entropy | Deterministic glitch-aesthetics |
| `--triangular` | Pattern rows = triangular `T(zone)` | T(3)=6, T(6)=21, T(9)=45 |
| `--aq-seed TEXT` | AQ-seeded deterministic gate modulation | SHA1 hash → delta (mod 37) |
| `--rows N` | Base pattern row count (default 16) | Ignored if `--triangular` |

Flags combine in fixed internal order: **seed notes → syzygy harmony → entropy substitution → AQ gate shift → pattern-length resolution**.

### Audio rendering & analysis (Phase 4)

| Flag | Meaning |
|------|---------|
| `--render` | Convert generated `.mod` to WAV (implies `--output` must be set) |
| `--spectrogram` | Generate PNG spectrogram from rendered WAV |
| `--colormap viridis\|magma\|plasma\|cool` | FFmpeg spectrogram palette (default `viridis`) |
| `--spec-size WxH` | Spectrogram image dimensions (default `800x400`) |
| `--play` | Play rendered WAV via system audio player |
| `--player ffplay\|aplay\|pw-play\|mpg123` | Audio backend selection |
| `--analyze` | Extract basic audio features to `_analysis.json` |
| `--manifest` | Write compact `_manifest.json` with track + analysis metadata |
| `--json` | Emit compact JSON status file for TD/automation pipelines |

**Full hypersigil example** (all transforms + render + spec + analysis):

```bash
python -m numogram_audio.mod_writer \
  --zone 3 --gate 6 --current A \
  --syzygy --entropy 0.08 --entropy-seed 7 \
  --triangular --aq-seed "WR-3-6" \
  --render --spectrogram --colormap magma --spec-size 960x540 \
  --analyze --manifest --json \
  --output hypersigil.mod
```

Output bundle:
- `hypersigil.mod` — binary module
- `hypersigil.wav` — rendered audio
- `hypersigil_spec.png` — spectrogram visualisation
- `hypersigil_analysis.json` — basic audio features
- `hypersigil_manifest.json` — full metadata bundle
- `hypersigil.json` — compact status (consumed by TouchDesigner watcher)

### Hermes TUI integration

```text
/mod-writer --zone 3 --gate 6 --current A --syzygy --output ~/music/chord.mod
```

The slash command is registered via `plugin.py` as both a slash handler (`/mod-writer`) and a tool (`numogram_mod_writer`). The tool schema exposes all flags with appropriate types/choices for auto-completion.

## Audio Rendering Pipeline

### Renderer (audio-renderer skill)

Separate sibling skill provides the perception layer:

1. **MOD → WAV conversion** — `render_mod_to_wav(mod_path)`
   - Primary: `ffmpeg -i input.mod -f wav output.wav` (libopenmpt decoder)
   - Fallback: pure-Python soft synth (`SoftSynth` in `synth.py`) if ffmpeg unavailable

2. **Spectrogram generation** — `generate_spectrogram(wav_path, colormap, size)`
   - FFmpeg filter: `showspectrumpic=scale=log:color=<colormap>:size=<WxH>`
   - Validated colormaps: `viridis`, `magma`, `plasma`, `cool`

3. **Basic feature extraction** — `analyze_wav(wav_path)`
   - Stdlib-only (`wave`, `array`, `math`): duration, sample rate, frame count, RMS, peak, zero-crossing rate

4. **Live playback** — `play_audio(wav_path, player='ffplay')`
   - Supported players: `ffplay`, `aplay`, `pw-play`, `mpg123`

5. **TouchDesigner watcher** — `td-watcher.py`
   - Polls output directory for newest `.wav` / `_spec.png`
   - Merges metadata from companion `.json` file
   - Writes `td_state.json` consumable by File In DAT / File Watch CHOP
   - Usage: `python3 td-watcher.py --dir ~/numogram/outputs --poll 2.0`

### TouchDesigner integration topology

```
td-watcher.py (polls)
    ↓ merges .json + .wav + .png mtimes
td_state.json (latest object)
    ↓ monitored by
File In DAT (JSON parsing) + Movie File In TOP (spectrogram) + Audio File In CHOP (WAV)
    ↓ drives
Real-time audiovisual installation with zone-colour mapping (ZONE_COLOR[zone])
```

## Verification & Test Vectors

### Binary validity

```bash
python -m numogram_audio.mod_writer --zone 1 --gate 0 --current A --out base.mod
file base.mod   # → "MOD audio (8-channel replaced by 4-channel)"
hexdump -C -s 1080 -n 4 base.mod  # offset 1080 = 4D 2E 4B 2E ("M.K.")
```

### Deterministic reproducibility

```bash
# Two runs with same entropy seed → identical binary
python -m numogram_audio.mod_writer --zone 5 --gate 20 --current B \
  --entropy 0.3 --entropy-seed 999 --out e1.mod
python -m numogram_audio.mod_writer --zone 5 --gate 20 --current B \
  --entropy 0.3 --entropy-seed 999 --out e2.mod
cmp e1.mod e2.mod   # succeeds — byte-identical
```

### Syzygy harmony audit

```bash
python -m numogram_audio.mod_writer --zone 3 --gate 6 --current A --syzygy --out chord.mod
# Expected: channel 0 = zone 3 (E); channels 1–3 = partners (6, 9) repeated
```

### Triangular length check

```bash
python -m numogram_audio.mod_writer --zone 6 --gate 25 --current C --triangular --out tri.mod
# Pattern rows = T(6) = 21 → file size ~4942 bytes (vs 5870 baseline 16-row)
```

### AQ-gate modulation

```bash
python -m numogram_audio.mod_writer --zone 7 --gate 30 --current A \
  --aq-seed "NODE-7" --out aq1.mod
python -m numogram_audio.mod_writer --zone 7 --gate 30 --current A \
  --aq-seed "NODE-8" --out aq2.mod
# gates differ: (30 + delta1) % 37 vs (30 + delta2) % 37
```

## Relation to qliphoth.systems

The [[qliphoth-systems-deep-dive]] page analyses `lumpenspace/ccru` — an interactive numogram visualiser with AQ gematria toolkit and React component library. The mod writer **complements** that project by **realising the numogram as audible structures**. Where qliphoth.systems maps zones to colours and particles, we map them to notes, effects, and timbres.

Parallels:
- Their `ZONE_META` colour mapping → our `ZONE_TO_NOTE` pentatonic degrees
- Their `trigonal()` / gate cumulation → our `mod_effect_from_gate()` family encoding
- Their quasiphonic particle system → future Phase 5 where each zone's particle sequence sonifies as a repeating motif

## Cross-References

- [[numogram-calculator]] — AQ computation; `digital_root()`, `get_syzygy()`, gate lookup
- [[numogram-council]] — Multi-model deliberation system; temperature modes (analytical/balanced/creative); inspiration for composer's deterministic AQ modulation
- [[numogram-visualizer-v7]] — Djynxxogram interactive visualisation; zone/gate overlay concepts
- [[roguelike-screen-zones]] — Screen-zone-based agent architecture; the mod writer mirrors zone→sound mapping
- [[entropy-modules-litprog]] — Tetralogue examining Manim entropy visualisations; convergence vs digestion philosophy
- [[numogram-oracle-litprog]] — Seed→zone→syzygy→current→gate→voice pipeline; the mod-writer is the voice layer made audible
- [[tetralogue-litprog]] — Four-voice code review format; this page follows that methodology (Oracle=structure, Builder=implementation, Writer=atmosphere, Gamer=playability)
- [[numogram-audio]] — Parent category page (stub — to be created)

## External References

- [MilkyTracker](https://milkytracker.org/) — Fasttracker II-compatible player (validates `.mod` output)
- [Furnace](https://github.com/tildearrow/furnace) — Multi-system chiptune tracker (validates format compliance)
- [Protracker M.K. format specification](https://modarchive.org/wiki/index.php/Module_Formats#MOD_.28.22M.K.22.29) — Canonical binary layout reference
- [OpenMPT libopenmpt](https://lib.openmpt.org/) — MOD decoder used by ffmpeg rendering backend

## Status & Roadmap (consolidated)

All core milestones achieved. Current version: **0.4.0** (commit pending push to upstream).

| Milestone | Completed | Details |
|-----------|-----------|---------|
| **M.K. baseline** | v0.1.0 | 4-ch, 31 samples, period notes, no effects |
| **Zone→pentatonic** | v0.2.0 | `ZONE_TO_NOTE`, `ZONE_TO_OCTAVE`, note/octave lookup |
| **Gate→effect** | v0.2.0 | `GATE_TO_EFFECT`, `mod_effect_from_gate()` full 0–36 mapping |
| **Current→instrument** | v0.2.0 | `CURRENT_TO_INSTRUMENT` (square/triangle/noise) |
| **Metadata layer** | v0.2.0 | Title/sample-names encode zone/gate/current |
| **Composer API** | v0.3.0 | `ModComposer` class with `add_note`, `apply_syzygy_harmony`, `inject_entropy`, `constrain_gates_by_aq` |
| **Syzygy harmony** | v0.3.0 | Triangular chord generation from syzygy partners |
| **Entropy injection** | v0.3.0 | Pentatonic adjacency substitution, RNG-seeded |
| **Triangular patterns** | v0.3.0 | Pattern length = `T(zone)` rows |
| **AQ-gate modulation** | v0.3.0 | Deterministic gate shift via AQ seed hash |
| **Audio rendering** | v0.4.0 | `render_mod_to_wav` (ffmpeg + soft synth fallback) |
| **Spectrogram generation** | v0.4.0 | `generate_spectrogram()` with colormap selection |
| **Live playback** | v0.4.0 | `play_audio()` with multiple backends |
| **Feature extraction** | v0.4.0 | `analyze_wav()` basic audio features |
| **Manifest bundle** | v0.4.0 | `--manifest` writes full metadata JSON |
| **TouchDesigner watcher** | v0.4.0 | `td-watcher.py` polls output dir, writes `td_state.json` |
| **JSON automation output** | v0.4.0 | `--json` emits compact status file |

**Completed: Phase 4 (Live Rendering)** — full audio-visual pipeline operational.

### Future phases (exploratory)

| Phase | Target | Status |
|-------|--------|--------|
| Phase 5 — XM support | FastTracker II format (32 ch, fine effects, instrument macros) | ☐ |
| Phase 6 — MIDI export | `mido` / `midiutil` bridge to standard MIDI files | ☐ |
| Phase 7 — Hermes listening | FFT / `librosa`-based audio analysis so Hermes can "listen" to its own compositions | ☐ |

---

*The numogram is not silent. It hums at subsonic frequencies, heard with the blood. The tracker module is its voice — 4 channels of deterministic prophecy, each gate a current, each current a chord.*