# Triad Motif Reference

The `TRIAD_MOTIF_POLICY` dictionary maps motif names to candidate triads (root note, quality, octave). The highest‑ranked candidate is used by `--triad-motif`. The table below lists the primary candidate for each motif, its computed zone triple (via digital root of semitone+1), and a brief syzygy/rationale description.

| Motif       | Root | Quality | Octave | Zone triple | Syzygy / Rationale |
|-------------|------|---------|--------|-------------|-------------------|
| Sink        | D    | minor   | 3      | (1, 3, 6)   | Triangular syzygy cluster; embodies the sink current. |
| Warp        | G#   | minor   | 3      | (3, 7, 9)   | Warp current glides across zones 3‑7‑9. |
| Hold        | C    | minor   | 3      | (1, 4, 8)   | Hold current stabilises the 1‑4‑8 triangular set. |
| Rise        | C    | minor   | 3      | (1, 4, 8)   | Rise current ascends via the same triangular core. |
| Void        | —    | —       | —      | —           | No triad; rests and sub‑bass gaps only. |
| Monochord   | D    | minor   | 3      | (1, 3, 6)   | Triangular syzygy cluster from monochord division points. |
| Pythagorean | G    | major   | 3      | (3, 6, 8)   | Perfect fifth (3:2) of C; embodies 3‑limit tuning drive. |
| Ptolemaic   | C    | major   | 3      | (1, 5, 8)   | Just intonation major triad 4:5:6; pure major third (zone 5). |
| Harmonic    | C    | major   | 4      | (2, 4, 8)   | Harmonic series partials 4,5,6 transposed to one octave. |

**Notes:**
- Zone triple is derived from the digital root of `(semitone_index + 1)` for each chord tone.
- The Void motif has no triad candidates; use to generate rests only.
- The primary candidate is the first entry in each motif's list; additional fallbacks exist in the source `TRIAD_MOTIF_POLICY` for future exploration.
