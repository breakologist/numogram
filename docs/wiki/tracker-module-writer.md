---
title: Tracker Module Writer
tags: ["numogram", "tracker", "mod-file", "protracker", "phase-2", "skill"]
zone: 3
syzygy: djynxx
created: 2026-04-28
last_updated: 2026-04-28
source: "Hermes Agent — numogram-audio/mod-writer skill"
status: draft
---

# Tracker Module Writer

> **Phase 2** deliverable: valid `.mod` generation with numogram-native mappings, registered as a Hermes skill.

## Overview

The **Mod Writer** is a minimal Python implementation of the Protracker M.K. (4-channel, 31-sample) module format. It writes binary `.mod` files that play in MilkyTracker, Furnace, and any compatible player.

**Why custom?** No maintained Python library writes `.mod` reliably; GUI trackers lack CLI generation; and we need to embed numogram semantics directly in the music data layer.

**Phase 1** (baseline) produced valid binary output with one hard-coded square wave sample and no effects.

**Phase 2** (current) integrates the full Alphanumeric Qabbala mapping:

| Numogram Layer | Mapping | Realised in |
|---|---|---|
| **Zone** (1–9) | Pentatonic scale degree (C D E G A) | Note pitch + octave |
| **Gate** (0–36) | Effect family (arpeggio, slide, volume, special) | Protracker effect command & parameter |
| **Current** (A/B/C) | Instrument selection (square/triangle/noise) | Sample index |

Additionally, **metadata** (song title, sample names) encodes the originating zone/gate/current to preserve the numogram "story layer" that modarchive hosts treasure.

## Design

### Format — Protracker M.K. (1084-byte header)

- **Patterns**: 64 rows × 4 channels; each cell 4 bytes (period, sample, effect, param)
- **Samples**: up to 31; 30-byte header + raw 8-bit offset-binary PCM
- **Magic**: `M.K.` at offset 1080
- **Period table**: Amiga PAL-based semitone → period lookup

Beyond the spec, we use:
- Effect command `0x0` (Arpeggio) for gates 0–9, parameter encodes symmetric offsets
- Effect command `0x1` (Porta up) for gates 10–19, parameter as speed
- Effect command `0xA` (Set volume) for gates 20–29
- Effect commands `0xB` (Position jump / Pattern break) for gate 30/31
- Extended commands `0xE` / `0xF` for Syzygy/Entropy gates 35/36

This mapping is **naïve Phase 2** — audible quality is secondary to structural fidelity. Future phases will add harmonies, portamento curves, and proper arpeggio patterns.

### Metadata — Information Layer

Since `.mod` lacks comment fields, we encode numogram context into:
- **Song title** (20 bytes): `ZzZgggC-Title` where `zz`=zone, `ggg`=gate (zero-padded), `C`=current
- **Sample names** (22 bytes each): `SQ-Z3-G15-A` (square, zone, gate, current)

This mirrors the modarchive tradition of cryptic filenames that tell the module's story.

## Usage

### From Hermes TUI

```
/mod-writer --zone 3 --gate 6 --current A --title "Warp Entry" --output warp.mod
```

### Standalone CLI

```bash
python -m numogram_audio.mod_writer \
  --zone 5 \
  --gate 12 \
  --current B \
  --title "Hold Tapestry" \
  --output hold.mod
```

### From Python

```python
from numogram_audio.mod_writer import ModWriter, Pattern, Sample
from numogram_audio.mod_writer.mapping import note_and_octave_from_zone, mod_effect_from_gate, CURRENT_TO_INSTRUMENT
from numogram_audio.mod_writer.utils import generate_square_wave

writer = ModWriter(title="Z4G20A-Test")

# samples …
# pattern with effect …
writer.write("output.mod")
```

**Verification**:
```bash
milkytracker output.mod   # GUI player
furnace output.mod        # multi-format tracker
```

## Relation to qliphoth.systems

The [[qliphoth-systems-deep-dive]] page analyses `lumpenspace/ccru` — an interactive numogram visualiser with AQ gematria toolkit and React component library. Our mod writer complements that project by **realising the numogram as audible structures**. Where qliphoth.systems maps zones to colours and particles, we map them to notes, effects, and timbres.

Notable parallels:
- Both define `ZONE_TO_NOTE` / `ZONE_META` → our ZONE_TO_NOTE maps to **pentatonic degrees**, their version maps to planetary colours
- Their `trigonal()` / gate cumulation inspires our `mod_effect_from_gate` family encoding
- Their quasiphonic particle system suggests a future **phase 3+** where each zone's particle sequence is sonified as a repeating arpeggio motif

## Status & Roadmap

| Phase | Status | Description |
|---|---|---|
| Phase 1 — Core writer | ✓ | M.K. binary output (4 ch, 31 samples, 64 patterns) |
| Phase 2 — Numogram mapping | ✓ | Zone→pentatonic, Gate→effect, Current→instrument, metadata |
| Phase 2b — Composer Bridge | ✓ | `ModComposer` API (midiutil‑style), high‑level orchestration |
| Phase 3 — Hypersigil extensions | ✓ | Syzygy harmony, Entropy injection, Triangular lengths, AQ‑seeded gates |
| Phase 4 — Live rendering | ☐ | MOD → WAV streaming, spectrogram analysis |
| Phase 5 — XM support | ☐ | FastTracker II format (32 ch, fine effects) |
| Phase 6 — MIDI export | ☐ | `mido` / `midiutil` bridge |
| Phase 7 — Audio analysis | ☐ | Hermes listening via FFT / `librosa` |

All core features (Phases 1‑3) are implemented and committed
(hermes‑agent `94bdde4b`, skill version **0.3.0**). See `SKILL.md` for the
complete reference.

---

## Advanced Features (CLI flags)

| Flag | Meaning | Example |
|---|---|---|
| `--syzygy` | Add partner‑zone harmony on channels 1‑3 | `--syzygy` |
| `--syzygy-channels N` | How many harmony channels (1‑3, default 3) | `--syzygy-channels 2` |
| `--entropy RATE` | Pentatonic zone substitution rate (0‑1) | `--entropy 0.15` |
| `--entropy-seed N` | RNG seed for reproducible entropy | `--entropy-seed 42` |
| `--triangular` | Pattern rows = triangular `T(zone)` | `--triangular` |
| `--aq-seed TEXT` | AQ‑seeded deterministic gate modulation | `--aq-seed CHAOS-3-6` |
| `--rows N` | Base pattern row count (ignored if `--triangular`) | `--rows 32` |

Flags combine arbitrarily; internal order:
seed notes → syzygy harmony → entropy substitution → AQ gate shift → pattern-length.

---

## Composer API (Python)

The `ModComposer` class provides an event‑list model similar to `mido.MIDIFile`.

```python
from numogram_audio.mod_writer.composer import ModComposer

comp = ModComposer(title="Syzygy Étude")
for r in range(16):
    comp.add_note(zone=3, gate=6, current='A', row=r, channel=0)

comp.apply_syzygy_harmony()                     # partner notes on ch1‑3
comp.inject_entropy(rate=0.1, rng_seed=7)      # 10% zone glitches
comp.constrain_gates_by_aq("WR-3-6")           # AQ‑modulated effects
comp._triangular = True                         # T(3)=6 rows
comp.write_mod("etude.mod")
```

Or one‑shot convenience:

```python
ModComposer.compose(
    zone=3, gate=6, current='A', rows=16,
    syzygy=True, entropy=0.1, triangular=True, aq_seed="WR-3-6",
    output="etude.mod"
)
```

This **composer layer** is the MIDI bridge: a clean, AI‑friendly interface that
abstracts binary packing while retaining full numogram semantics. Future Phase
6 may add `write_midi()` using `mido` to emit actual `.mid` files.

---

## Files

```
numogram-audio/
  mod-writer/
    __init__.py   # package constants, version
    writer.py     # binary packer (ModWriter, Pattern, Sample, period table)
    utils.py      # waveform generators (square, triangle, noise)
    mapping.py    # numogram → music mappings + Phase 2 conversion helpers
    cli.py        # argparse standalone entry point with metadata injection
    plugin.py     # Hermes skill registration (slash command + tool)
    SKILL.md      # skill descriptor (triggers, phases, usage)
```

## See Also

- [[numogram-visualizer-v7]] — Djynxxogram interactive visualisation (36-zone AQ layout)
- [[numogram-council]] — multi-model deliberation system (our design inspiration)
- [[roguelike-screen-zones]] — screen-zone based roguelike agent architecture
- **External**: [MilkyTracker](https://milkytracker.org/) — Fasttracker II clone; [Furnace](https://github.com/tildearrow/furnace) — multi-system chiptune tracker
