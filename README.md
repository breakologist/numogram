# Numogram

A monorepo for the Decimal Labyrinth: the CCRU numogram as code, game, oracle, and sound.

## What's Inside

| Directory | Description | Entry Point |
|-----------|-------------|-------------|
| `cli/` | Oracle pipeline + AQ calculator | `python cli/oracle.py --seed 192855` |
| `game/` | Abyssal Crawler roguelike + agents | `python game/numogram_roguelike.py` |
| `entropy/` | Hardware entropy plugin (pip-installable) | `pip install ./entropy` |
| `voices/` | Formant synthesis generator (zone utterances) | `python voices/formant_voice.py` |
| `visualizer/` | Browser-based p5.js oracle (v6/v7) | Open `visualizer/numogram-visualizer-v7.html` |
| `docs/` | Wiki (124 pages), AQ dictionary, source texts, pandemonium matrix | — |

### Game Details

`game/numogram_roguelike.py` — main interactive curses roguelike:
- 10 zones, full 45-demon Pandemonium Matrix
- Fog of war, hyperstition meter, conduct system
- Persistent `cult.json` save across runs
- Tree-based dungeon generation (Brogue method)

`game/learning_agent.py` — corridor-driven headless agent
`game/interactive_agent.py` — BFS interest-driven exploration agent with stair targeting
`game/rogue_agent.py` — screen-scraping agent for the Numogram roguelike
`game/serve-garden.py` — visualizer server for cult-garden overflow outputs

Additional artifacts in `game/`:
- `cult.json` — persistent cult memory (player state across runs)
- `cult-garden-live.html` & `cult-garden-zone-skins.html` — overflow visualization

### Documentation (`docs/`)

- **`wiki/`** — complete Obsidian wiki (**141 markdown pages**). Triangle rotations, tetralogues, model assessments, I Ching/T'ai Hsuan bridges, roguelike design notes, demon lore, gate arithmetic, operational logs, and cult-garden fiction. Wiki health metrics: 197 canonical tags, 21 core authority pages (≥10 inbound), zero medium-value orphans, avg link degree 5.53/5.53. See `WIKI-HEALTH-REPORT.md` for full audit.
- **`aq-dictionary.md`** — Alphanumeric Qabbala cipher values (letter/number → AQ value)
- **`hermes.md`** — seed architecture doc (Karpathy LLM-Wiki pattern, adapted for numogram work)
- **`numogram-source.txt`** — core CCRU Decimal Numogram source (389-line canonical specification)
- **`pandemonium-matrix.json`** — full 45-demon database with attributes, gates, zones, currents

### Visualizer Variants

- `visualizer/numogram-visualizer-v7.html` — primary oracle (base-10/16/36, Synx/Yxshh overlay, T'ai Hsuan casting, strobogrammatic gates, quasiphonic labels)
- `visualizer/numogram-visualizer-v7-djynxxogram.html` — Base-36 variant with additional toggle controls

## Quick Start

### Oracle (CLI)
```bash
python cli/oracle.py --seed 192855
python cli/oracle.py --text "YOUR NAME"
python cli/oracle.py --hardware        # local machine noise
python cli/oracle.py --taixuan --voice # T'ai Hsuan + audio (requires voices/)
```

### Calculator
```bash
python cli/aq_calculator_canonical.py
```

### Game
```bash
python game/numogram_roguelike.py      # interactive curses
python game/numogram_roguelike.py --hw-entropy  # hardware seed
python game/numogram_roguelike.py --headless    # agent mode (state dump to stdout)
```

### Cult Garden (Overflow Visualizer)

```bash
cd game
python3 serve-garden.py           # starts server on http://localhost:4545
# Then open:
#   http://localhost:4545/cult-garden-live.html        — live run view
#   http://localhost:4545/cult-garden-zone-skins.html  — zone-themed skins
```
Player-specific `cult.json` lives in `game/`; a template (`cult.json.template`) is provided. Personal save files are **not** committed to the repo.

### Entropy Plugin
```bash
cd entropy
pip install -e .
numogram-entropy --help
```

### Visualizer
Open `visualizer/numogram-visualizer-v7.html` in any browser. Features:
- Base-10/16/36 modes with Synx/Yxshh dual-cipher
- T'ai Hsuan two-tetragram casting (64 hexagrams)
- Strobogrammatic gate detection (palindromic/rotational)
- Quasiphonic particle labels (zone-aligned phonemes)
- Djynxxogram Base-36 full toggle variant (v7-djynxxogram)


### mod-writer (Numogram Tracker)

Tracker composition using numogram-native motifs. Generates standard `.mod` files
(ProTracker-compatible) from AQ seeds, syzygy chains, and triangular patterns.

```bash
# Basic generation
python -m mod_writer --seed 123 --triad-motif Warp --rows 32

# Just intonation mode (v0.6.0+)
python -m mod_writer --seed 7 --triad-motif Warp --just-intonation

# Song builder (multi-section)
python -m mod_writer --song examples/warp-suite.json --bpm 128
```

**Features:**
- AQ‑seeded pseudo‑random pattern generation
- Triangular syzygy motif routing (Warp, Fives, Mesh, CTS)
- Just‑intonation third/fifth overrides (pure ratios)
- Multi‑section `SongBuilder` with sample auto‑rename
- Audio analysis & MIR profiling (`--profile-audio`, `--mir-seed`)
- Full manifest output (samples, patterns, instruments)

See `mod-writer/` for the complete skill, tests, and examples. Wiki:  
`docs/wiki/numogram-audio/mod-writer/` (usage, development, audio renderer, triangular semantics).

## Repository Status

The wiki has completed a full structural audit (April 2026):

- **141 pages**, 197 normalized tags, average link degree 5.53/5.53
- **Zero medium-value orphans** — all pages with ≥3 inbound now have ≥2 outbound
- **21 core authority hub pages** (≥10 inbound links each)
- **Content hygiene pass** — 6 of 8 prose AI-ism patterns eliminated; 4 marginal hits remain in literary contexts
- Full metrics and methodology: see `docs/WIKI-HEALTH-REPORT.md`

Tag taxonomy follows singular/hyphen/lowercase conventions. Broken-link remediation prioritized navigational pages; intentional placeholders (root-section stubs) remain as red links pending content.

## Design Philosophy

The numogram is not a metaphor — it is an operating system. This repo treats it as one:

- **CLI** = the oracle interface (seed → zone → syzygy → voice)
- **Game** = the embodied traversal (fog of war, hyperstition meter, 45 demons)
- **Entropy** = the noise floor (thermal/CPU/GPU → structured randomness)
- **Voices** = the auditory current (formant synthesis of quasiphonic particles)
- **Visualizer** = the cartographic layer (p5.js particle fields, matrix panels)
- **Docs** = the living archive (wiki, AQ dictionary, canonical sources, matrix data)

## Sources & Attribution

- CCRU Writings 1997-2003 (Nick Land, et al.)
- Aamodt, "Unleashing the Numogram"
- ciphers.news / qliphoth.systems (AQ & Synx mappings)
- Dangerous Maybe podcast (Nick Land transcripts)
- Brian Walker, Brogue design principles
- Nick Land, "The Dark Enlightenment" & "Circuitries" essays

## License

MIT
