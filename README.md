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

- **`wiki/`** — complete Obsidian wiki (124 markdown pages). Triangle rotations, tetralogues, model assessments, I Ching/T'ai Hsuan bridges, roguelike design notes, demon lore, gate arithmetic, and operational logs.
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
