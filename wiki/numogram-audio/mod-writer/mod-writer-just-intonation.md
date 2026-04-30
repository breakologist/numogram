# Just Intonation Mode

## Overview

When generating triad motifs, the default tuning uses **equal temperament**: each semitone is a fixed ratio (2^(1/12)). With the `--just-intonation` flag, the third and fifth chord tones are tuned to **simple just ratios**:

| Chord quality | Third ratio | Fifth ratio |
|---------------|------------|------------|
| Major         | 5/4        | 3/2        |
| Minor         | 6/5        | 3/2        |

The root retains its equal-tempered period. The third and fifth periods are computed as:

```
period_override = round(root_period / ratio)
```

This yields purer harmonic intervals in the rendered audio, at the cost of slightly detuning the chord from equal temperament.

## Why it matters

Just intonation produces beatless thirds and fifths — the harmonic series made audible. In the context of numogram‑aligned composition, this lets a triad motif embody a more "natural" syzygy resonance while still mapping its zones.

## Usage

```bash
mod-writer --triad-motif Ptolemaic --just-intonation --rows 64 --output ptolemaic-just.mod
```

The flag applies globally:

- In **advanced mode** (`--triad-motif`) it affects the generated triad.
- In **song mode** (`--song`) it propagates to every section automatically.

## Technical notes

- Period overrides are clamped to ≥ 1. If the computed value rounds to 0, it is set to 1 (lowest playable period).
- The mapping from note name + octave to period comes from the standard MOD period table (Amiga PAL clock). Just ratios adjust that period directly, bypassing the lookup.
- This feature lives entirely in `composer.py`; no changes to the binary writer are required.


