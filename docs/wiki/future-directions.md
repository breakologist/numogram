---
title: "Future Directions — Notions & Horizons"
created: 2026-05-11
status: open-ended
tags: [planning, audio, tracker, mod-writer, future, sampling, midi, cv]
---

# Future Directions — Notions & Horizons

> *Not a roadmap. Not a plan. A record of threads worth pulling, noted now so the autonomous sessions can find them.*

## Sound Sources — Synthesis → Sampling

The mod-writer currently generates all waveforms procedurally (square, triangle, noise, sine, sawtooth — 8-bit, 1,254 bytes). The next dimension is **loaded audio**: field recordings, drum breaks, vocal fragments, resampled instrument libraries. A sample slot should accept both synthesized and external data.

**Why it matters:** Timbre from the world. The same zone's note data played through different sample bodies = polysemy. A Z6 Abstraction pattern on a drum break sounds different from the same pattern on noise synthesis. Same numogrammatic identity, different sonic body.

**Bridge architecture:** Sample slots already exist (31 max in Protracker `.mod`, 128 in `.xm`). The loader just needs to accept external `.wav`/`.flac` and downsample/resample to the target format.

## Format Bridges

### `.xm` — FastTracker II (32 channels, 16-bit, instruments)

Where `.mod` gives each zone a note + waveform, `.xm` gives it an **instrument**: attack/decay/sustain/release envelopes, panning, vibrato. The zone mapping deepens without widening:

- Z3 Release → slow attack, long release
- Z1 Surge → sharp pluck, fast decay
- Z7 Blood → sustain loop, slow modulation
- Zone-over-time trajectories could modulate envelope parameters across sections

### MIDI

Any MOD pattern is a note-on/note-off stream at heart. A MIDI export path (`mod_writer → .mid`) lets the numogram sequence external hardware. Zone → MIDI channel, gate → CC value, current → program change.

### CV / Modular

Zone → voltage. Gate → trigger. Current → waveform select. The decimal labyrinth as a modular patch. More speculative, but the mapping is clean: Eurorack 1V/oct is just a different encoding of the same pitch data the MOD period table represents.

## Tracker Software — Comparative Study

Each tracker's "business method" is a different answer to the question the mod-writer faces: *how much data can you encode in limited space, and where do you put the metadata?*

| Tracker | Era | Channels | Format | Signature |
|---------|-----|----------|--------|-----------|
| **Protracker 2.3d** | Amiga, 1990 | 4 | `.mod` | Austere classicism. Constraints as aesthetic. The mod-writer's genetic ancestor. |
| **OctaMED** | Amiga, 1990+ | 4+8 | `.med` | Synth-based origins, hybrid MIDI+sample. The eccentric who stayed Amiga. |
| **FastTracker II** | PC DOS, 1994 | 32 | `.xm` | The revolution: 16-bit, envelopes, instrument mapping. Orchestration-era tracking. |
| **Impulse Tracker** | PC DOS, 1995 | 64 | `.it` | Filters, NNAs, compressed samples. The peak of DOS-era complexity. |
| **Scream Tracker 3** | PC DOS, 1994 | 16 | `.s3m` | 16-bit samples, AdLib FM synthesis. The bridge between Amiga and PC worlds. |
| **Renoise** | Modern, 2002+ | unlimited | `.xrns` | DAW-level automation inside a tracker grid. The modern synthesis. |
| **SunVox** | Modern | — | `.sunvox` | Modular synth + tracker. Node-graph routing, real-time synthesis, cross-platform. |
| **Furnace** | Modern | multi | multi | Multi-chip tracker: NES, Genesis, C64, arcade boards. Not one sound chip — many. |

**Study paths:**
- Tempo/speed interplay conventions across formats
- Effect column encoding: how each tracker uses the same 8-bit effect/parameter byte differently
- Pattern chaining: `.mod` position-jump vs `.xm` pattern-loop vs `.it` order-list
- Sample slot limits as compositional constraints
- How each format handles metadata "blind spots" (compare to mod-writer's AQ steganography)

## Tracker Artists — Research Threads

If each tracker format is a language, individual artists are its poets. Tracker music emerged from the demoscene — a culture of inventiveness, constrained resources, and competitive one-upmanship. Studying individual voices would reveal what's convention vs signature:

**Amiga era:**
- **4-mat / Matthew Simmonds** — Anarchy, melodic chip-influenced `.mod`s
- **Jester / Voltri** — technical minimalism, sample economy
- **Moby** — before the albums: `brainstorm.mod`, `bbs intro #8`
- **Audiomonster** — effect-column virtuosity

**PC era:**
- **Skaven / Future Crew** — Purple Motion's counterpart, epic `.s3m` compositions
- **Necros / Andrew Sega** — scene-to-industry crossover, `.it` format refinement
- **Maktone / Martin Nordell** — microscopic `.xm` files, 4KB-to-20KB masterpieces
- **Elwood / Jeroen Tel** — C64 + tracker hybrid workflows

**Modern:**
- **Virt / Jake Kaufman** — Shovel Knight, chiptune through tracker lineage
- **Dubmood / Zabutom** — cracked game trainers, `.mod` as cultural artifact
- **Various tsubuyaki artists** — micro-composition as form

**Research questions:**
- Signature effect-column patterns per artist
- Sample reuse and economy: how artists stretch limited sample slots
- Pattern-length modulation as structural tool
- Greeting messages (`greetz to...`) as steganographic predecessor to AQ embedding
- How demoscene competition constraints shaped compositional voice

## Hardware Interaction

External hardware as a numogrammatic transducer:

- **MIDI out:** Zone → channel, gate → CC, current → program change. Any MOD pattern → any MIDI synth.
- **CV/gate:** Modular-specific. Zone-to-pitch via 1V/oct, gate-to-trigger on note-on, current-to-waveform select. The decimal labyrinth as Eurorack patch.
- **Audio in:** External audio → MIR analysis → zone classification → mod-writer response. Live audio as divination input (the Phase 5 M3 live-loop direction).
- **TouchDesigner:** Already wired (MCP bridge, localhost:40404). Audio → visual mapping; spectrum analysis as color modulation.

## Core Loop — The Invariant

Whatever bridges are built, the loop stays the same:

```
Zone → Parameters → Audio → MIR → Zone Classification → Feedback
```

Each new transducer (sampling, .xm, MIDI, CV) is a different material pathway through the same structure. Same in, same out. The numogram is the invariant.

---

*Noted 2026-05-11. For the autonomous sessions to stumble upon. For future us to recall what we were thinking, even if we change our minds.*