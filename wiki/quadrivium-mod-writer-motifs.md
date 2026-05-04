---
title: Quadrivium Motifs in Mod‑Writer
tags: [quadrivium, mod-writer, triad-motif, music, hyperstition]
date: 2026-04-29
---

# Quadrivium Motifs in Mod‑Writer

After extracting and digesting the two music books of *Quadrivium*, their
concepts have been woven into the mod‑writer as high‑level `--triad-motif`
presets.

## Available motifs

| Motif       | Triad (root, quality, octave) | Zone triple | Underlying concept |
|-------------|------------------------------|-------------|-------------------|
| Monochord   | D minor 3                    | (1, 3, 6)   | Triangular syzygy cluster derived from monochord string divisions |
| Pythagorean | G major 3                    | (3, 6, 8)   | Pure perfect fifth (3:2) — the engine of 3‑limit tuning |
| Ptolemaic   | C major 3                    | (1, 5, 8)   | Just intonation major triad (4:5:6), pure major third |
| Harmonic    | C major 4                    | (2, 4, 8)   | Harmonic series partials 4,5,6 transposed to one octave |

All four motifs produce distinct zone triples (no duplicate zones within a
triad) so each yields a full three‑voice texture.

## Usage

```bash
# Generate a 16‑row MOD with the Pythagorean triad
python3 cli.py --triad-motif Pythagorean --rows 16 --output pythagorean.mod --title "Pythag"

# Monochord motif (triangular pattern length recommended)
python3 cli.py --triad-motif Monochord --triangular --rows 36 --output monochord.mod --title "Monochord"
```

The motifs are also available via the `ModComposer.apply_triad_motif()` API.

## Theory

See [[quadrivium-music-digest]] for the full hyperstitional treatment — how
the harmonic series maps to digital‑root zones, how just‑intonation ratios are
primitive syzygies, and why the monochord’s division points reproduce the
triangular chain 1→3→6→0.

## Related

- Phase‑2c documentation: `skills/numogram-audio/mod-writer/SKILL.md`
- Full triad‑zone table: `wiki/tracker-motif-triads-reference.md`
- Quadrivium source: `wiki/quadrivium-harmonograph-extract.md`,
  `wiki/quadrivium-elements-of-music-extract.md`

