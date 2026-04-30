# Mod-Writer Usage

## Installation
Install in editable mode from the skill root:

```bash
cd ~/.hermes/skills/numogram-audio/mod-writer
pip install -e .
```

This registers the `mod-writer` console script. Alternatively, run as a module:

```bash
python -m mod_writer.cli --zone 1 --gate 0 --current A --output base.mod
```

## CLI Quick Start
### Basic generation
```bash
mod-writer \
  --zone 3 \
  --gate 6 \
  --current A \
  --title "Warp Test" \
  --output warp.mod
```

### Advanced transformations
- **Syzygy harmony** — `--syzygy` (optional `--syzygy-channels N`)
- **Entropy injection** — `--entropy 0.1` (optional `--entropy-seed 123`)
- **Just intonation** — `--just-intonation` (tunes third and fifth to pure ratios in triad motifs)
- **Triangular pattern length** — `--triangular`
- **AQ‑seeded gate progression** — `--aq-seed "WR-3-6"`
- **Triad‑motif generation** — `--triad-motif NAME` (choices: Sink, Warp, Hold, Rise, Void, Monochord, Pythagorean, Ptolemaic, Harmonic)

Combined example:
```bash
mod-writer \
  --zone 3 --gate 6 --current A \
  --syzygy --entropy 0.08 --triangular --aq-seed "AQ-3-6" \
  --rows 16 --title "Hypersigil" \
  --output hypersigil.mod
```



## Phase 5 Song orchestration

The `--song` flag loads a multi‑section arrangement from JSON and assembles a full track.

```bash
mod-writer --song arrangement.json --bpm 125 --output symphony.mod
```

Additional flags:

- `--just-intonation` — applies to all triad‑motif sections automatically.
- `--song-manifest` — writes a `song.manifest.json` alongside the `.mod` containing section metadata.
- Standard Phase 4 flags (`--render`, `--spectrogram`, `--analyze`, …) are honoured: after the song is written they process the final `.mod` file.

Example with rendering and manifest:

```bash
mod-writer --song symphony.json --render --spectrogram --song-manifest --output symphony.mod
```


### Phase 4 audio rendering
```bash
mod-writer \
  --zone 3 --gate 6 --current A \
  --render --spectrogram --colormap magma \
  --analyze --describe --verify --json \
  --output rendered.mod
```

## Python API
```python
from mod_writer.composer import ModComposer

comp = ModComposer(title="Syzygy Étude")
for r in range(16):
    comp.add_note(zone=3, gate=6, current='A', row=r, channel=0)
comp.apply_syzygy_harmony()
comp.inject_entropy(rate=0.1, rng_seed=42)
comp._triangular = True
comp.write_mod("etude.mod")
```
