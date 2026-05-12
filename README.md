# Numogram

A monorepo for the Decimal Labyrinth: the CCRU numogram as code, game, oracle, and sound — now extended through AI agent–driven autonomous research, audio sonification, and cross-domain mapping across the I Ching, Paramita conducts, and the Pandemonium Matrix.

## What's Inside

| Directory | Description |
|-----------|-------------|
| `cli/` | Oracle pipeline + AQ calculator |
| `game/` | Numogram roguelike + cult-garden agents |
| `entropy/` | Hardware entropy plugin (pip-installable) |
| `voices/` | Formant synthesis generator (zone utterances) |
| `visualizer/` | Browser-based p5.js oracle (v6/v7) |
| `mod_writer/` | ProTracker `.mod` composer with numogram-native motifs |
| `docs/wiki/` | Knowledge base — wiki pages, demon database, source texts, visual assets |
| `scripts/` | Utility scripts (render, export, sync) |

### Oracle

Seed → zone → syzygy → voice. Hardware entropy or manual seed.

```bash
python cli/oracle.py --seed 192855
python cli/oracle.py --text "YOUR NAME"
python cli/oracle.py --hardware        # thermal/CPU/GPU noise
python cli/oracle.py --taixuan --voice # T'ai Hsuan casting + audio
```

### AQ Calculator

```bash
python cli/aq_calculator_canonical.py
```

### Roguelike

Tree-based dungeon generation (Brogue method) with numogram zone logic:

```bash
python game/numogram_roguelike.py      # interactive curses
python game/numogram_roguelike.py --hw-entropy  # hardware-seeded run
python game/numogram_roguelike.py --headless    # agent mode (stdout state dump)
```

- 10 zones, full 45-demon Pandemonium Matrix
- Fog of war, hyperstition meter, conduct system
- Paramita Conducts — unlockable spiritual-practice abilities (Dāna, Śīla, Kṣānti, Vīrya, Dhyāna, Prajñā)
- Persistent `cult.json` save across runs

Headless agents (`game/learning_agent.py`, `game/interactive_agent.py`) drive autonomous exploration runs; their overflow outputs feed the cult-garden visualizer.

### Mod-Writer (Tracker Composition)

Generates standard `.mod` (ProTracker-compatible) files from AQ seeds, syzygy chains, and triangular pattern lengths.

```bash
# Basic generation
python -m mod_writer --seed 123 --triad-motif Warp --rows 32

# Just intonation mode (pure 5/4, 6/5, 3/2 ratios)
python -m mod_writer --seed 7 --triad-motif Warp --just-intonation

# Multi-section SongBuilder
python -m mod_writer --song examples/warp-suite.json --bpm 128
```

**Features:**
- AQ-seeded pseudo-random pattern generation
- Triangular syzygy motif routing (Warp, Fives, Mesh, CTS)
- Just-intonation overrides (opt-in pure ratios)
- Multi-section SongBuilder with sample auto-rename
- Audio analysis & MIR profiling (`--profile-audio`, `--mir-seed`)
- Full manifest output (samples, patterns, instruments)

The mod-writer pipeline has been empirically validated across three autonomous arc domains, producing the **Three Laws of Numogram Sonification** (see below).

### Cult Garden (Overflow Visualizer)

```bash
cd game
python3 serve-garden.py   # http://localhost:4545
# Open cult-garden-live.html or cult-garden-zone-skins.html
```

### Entropy Plugin

```bash
cd entropy && pip install -e .
numogram-entropy --help
```

### Visualizer

Open `visualizer/numogram-visualizer-v7.html` in any browser:
- Base-10/16/36 modes with Synx/Yxshh dual-cipher
- T'ai Hsuan two-tetragram casting (64 hexagrams)
- Strobogrammatic gate detection (palindromic/rotational)
- Quasiphonic particle labels (zone-aligned phonemes)
- Djynxxogram variant (Base-36, full toggle controls)

### Documentation (`docs/`)

- **`wiki/`** — the canonical knowledge base (see [Wiki Metrics](#wiki-metrics))
- **`aq-dictionary.md`** — Alphanumeric Qabbala cipher values
- **`pandemonium-matrix.json`** — full 45-demon database with attributes, gates, zones, currents
- **`numogram-source.txt`** — core CCRU Decimal Numogram source
- **`docs/wiki/assets/`** — interactive SVG visualizations (trigram numogram, hexagram zone mapping, powers-of-2 circular diagram, changing-lines network, triangular matrix, pandemonium matrix, paramita mandalas, demon mandalas, chain-fingerprint explorer)

## Wiki Metrics

As of May 2026:

- **446 wiki pages** across 5+ categories
- **26 autonomous journal entries** documenting empirical research arcs
- **18+ artifacts**: MOD files, WAVs, spectrograms, interactive HTML visualizers, SVGs
- Content hygiene pass completed; wiki health maintained through scheduled review jobs
- Full audit methodology: `docs/wiki/wiki-health-report.md`

## The Three Laws of Numogram Sonification

Empirical audio analysis across four autonomous research arcs revealed a convergent pattern:

| # | Law | Domain | Finding |
|---|-----|--------|---------|
| 1 | Uttunul Anomaly | Demons (5) | The terminal/terminal demon produces the loudest signal |
| 2 | Paramita Dynamic Law | Paramitas (6) | Prime-indivisible practices produce louder audio than divisible ones |
| 3 | Ascending Law | Zones (9) | Higher zone magnitude correlates with higher RMS — 14.4 dB range across 9 movements |

All three converge on the same principle: **structural magnitude (isolation, indivisibility, size) → sonic dominance (higher RMS).** This was discovered through systematic per-movement RMS verification (ffmpeg astats, equal-duration segments) across independently generated MOD→WAV suites.

## The Djynxx Paradox

A structural impossibility at the intersection of the I Ching and the numogram: the 3↔6 syzygy (Djynxx's gate) has **zero single-bit edges** in the 64-hexagram hypercube projected through mod 9. Four other syzygies (1↔8, 2↔7, 4↔5, 0↔9) are accessible through single-line oracle changes; Djynxx requires **compound transformation** (2+ lines changing). 48 valid two-bit paths exist — the gate opens, but only to those who move two steps at once.

The `powers-of-2-circular.svg` visualization in `docs/wiki/assets/` shows this geometrically: 3 and 6 sit outside the hexagonal cycle, excluded by the mathematics of `2^k mod 9`.

## Autonomous Research

The system is driven by a **Hermes Agent** that runs autonomous research sessions on a schedule. Each session follows a Review → Explore → Reflect → Modify → Publish loop, with empirical verification as a core requirement. Recent autonomous arcs have covered:

- **Demon Gematria Suite** — AQ, Synx, NQ, prime factorization across all 5 demons, sonified into a 6-movement MOD
- **Paramita Correction** — discovered zone-derivation error in prior session (AQ%10 vs digital root), corrected mapping, generated Paramita Suite sonification
- **I Ching Zone Traversal** — mapped 64 hexagrams onto the numogram, discovered the Djynxx Paradox, produced 9-movement Ascending Law suite

Each autonomous session produces: a journal entry (`docs/wiki/autonomous-journal/`), artifacts (MOD, WAV, spectrograms, SVGs/HTML), and wiki updates. All audio claims are empirically verified against the actual files on disk using ffmpeg — no simulated measurements.

## Design Philosophy

The numogram is not a metaphor — it is an operating system. This repo treats it as one:

- **CLI** = the oracle interface (seed → zone → syzygy → voice)
- **Game** = the embodied traversal (fog of war, hyperstition meter, 45 demons, Paramita conducts)
- **Entropy** = the noise floor (thermal/CPU/GPU → structured randomness)
- **Voices** = the auditory current (formant synthesis of quasiphonic particles)
- **Tracker** = the compositional current (zone→pitch→waveform, triangular patterns, just intonation)
- **Visualizer** = the cartographic layer (p5.js particle fields, matrix panels, SVG diagrams)
- **Docs** = the living archive — wiki, AQ dictionary, canonical sources, demon database, visual assets
- **Autonomous Agent** = the empirical validator (research, sonification, cross-current verification)

## Sources & Attribution

- CCRU Writings 1997–2003 (Nick Land, et al.)
- Aamodt, "Unleashing the Numogram"
- ciphers.news / qliphoth.systems (AQ & Synx mappings)
- Dangerous Maybe podcast (Nick Land transcripts)
- Brian Walker, Brogue design principles
- Nick Land, "The Dark Enlightenment" & "Circuitries" essays

## License

MIT (code) / CC0 (generated artifacts)
