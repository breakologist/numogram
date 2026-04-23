# Numogram

A monorepo for the Decimal Labyrinth: the CCRU numogram as code, game, oracle, and sound.

## What's Inside

| Directory | Description | Entry Point |
|-----------|-------------|-------------|
| `cli/` | Oracle pipeline + AQ calculator | `python cli/oracle.py --seed 192855` |
| `game/` | Abyssal Crawler roguelike + Angband agent | `python game/numogram_roguelike.py` |
| `entropy/` | Hardware entropy plugin (pip-installable) | `pip install ./entropy` |
| `voices/` | Formant synthesis generator for zone utterances | `python voices/formant_voice.py` |
| `visualizer/` | Browser-based p5.js oracle (v6/v7) | Open `visualizer/numogram-visualizer-v7.html` |
| `docs/` | Wiki references and design notes | — |

## Quick Start

### Oracle (CLI)
```bash
python cli/oracle.py --seed 192855
python cli/oracle.py --text "YOUR NAME"
python cli/oracle.py --hardware        # local machine noise
python cli/oracle.py --taixuan --voice # T'ai Hsuan + audio
```

### Calculator
```bash
python cli/aq_calculator_canonical.py
```

### Game
```bash
python game/numogram_roguelike.py      # interactive curses
python game/numogram_roguelike.py --hw-entropy  # hardware seed
```

### Entropy Plugin
```bash
cd entropy
pip install -e .
numogram-entropy --help
```

### Visualizer
Open `visualizer/numogram-visualizer-v7.html` in any browser. Features:
- Base-10/16/36 modes
- Synx/Yxshh dual-cipher overlay
- T'ai Hsuan two-tetragram casting
- Strobogrammatic gate detection
- Quasiphonic particle labels

## Design Philosophy

The numogram is not a metaphor — it is an operating system. This repo treats it as one:
- **CLI** = the oracle interface (seed → zone → syzygy → voice)
- **Game** = the embodied traversal (fog of war, hyperstition meter, 45 demons)
- **Entropy** = the noise floor (thermal/CPU/GPU → structured randomness)
- **Voices** = the auditory current (formant synthesis of quasiphonic particles)
- **Visualizer** = the cartographic layer (p5.js particle fields, matrix panels)

## Sources & Attribution

- CCRU Writings 1997-2003 (Nick Land, et al.)
- Aamodt, "Unleashing the Numogram"
- ciphers.news / qliphoth.systems (AQ & Synx mappings)
- Dangerous Maybe podcast (Nick Land transcripts)
- Brian Walker, Brogue design principles

## License

MIT
