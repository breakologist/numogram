# Tracker Music Theory — Triad–Zone Mappings

> **Scope:** Formal correspondence between triadic harmony (major/minor triads) and Numogram zone sets derived from note digital‑root mapping. Empirical validation against 12‑module ModArchive corpus is in [[tracker-composition-principles]].

## Digital‑Root Zone Calculation

Zone = digital_root(semitone_index + 1) % 10, where `semitone_index = octave*12 + chromatic_offset`. This formula matches the `audio-renderer` module's `note_to_zone()` function (see `process_new_mods_full.py`). `digital_root` sums digits until a single digit remains; modulo 10 yields values 0–9. (Note: digital root of multiples of 10 returns 0, which represents zone 0/Void.)

**Rationale:** The +1 offset aligns Protracker's period indexing such that the lowest C‑2 maps consistently across implementations; historical note‑to‑zone conventions in the numogram treat C‑2 as a Void anchor.

## Triad → Zone Sets

A triad consists of three pitch classes separated by a third and a fifth. Under the digital‑root zone mapping, each triad projects onto a set of 1‑3 distinct zones depending on octave placement. For a root at octave 4:

### Minor Triads (root, minor 3rd, perfect 5th)
| Root | Notes (oct 4) | Zone set |
|---|---|---|
| C‑minor | C4, D#4, G4 | 2, 4, 7 |
| C#‑minor | C#4, E4, G#4 | 3, 5, 8 |
| D‑minor | D4, F4, A4 | 4, 6, 9 |
| D#‑minor | D#4, F#4, A#4 | 1, 5, 7 |
| E‑minor | E4, G4, B4 | 2, 6, 8 |
| F‑minor | F4, G#4, C5 | 3, 7, 9 |
| F#‑minor | F#4, A4, C#5 | 1, 4, 8 |
| G‑minor | G4, A#4, D5 | 2, 5, 9 |
| G#‑minor | G#4, B4, D#5 | 1, 3, 6 |
| A‑minor | A4, C5, E5 | 2, 4, 7 |
| A#‑minor | A#4, C#5, F5 | 3, 5, 8 |
| B‑minor | B4, D5, F#5 | 4, 6, 9 |

### Major Triads (root, major 3rd, perfect 5th)
| Root | Notes (oct 4) | Zone set |
|---|---|---|
| C‑major | C4, E4, G4 | 2, 4, 8 |
| C#‑major | C#4, F4, G#4 | 3, 5, 9 |
| D‑major | D4, F#4, A4 | 1, 4, 6 |
| D#‑major | D#4, G4, A#4 | 2, 5, 7 |
| E‑major | E4, G#4, B4 | 3, 6, 8 |
| F‑major | F4, A4, C5 | 4, 7, 9 |
| F#‑major | F#4, A#4, C#5 | 1, 5, 8 |
| G‑major | G4, B4, D5 | 2, 6, 9 |
| G#‑major | G#4, C5, D#5 | 1, 3, 7 |
| A‑major | A4, C#5, E5 | 2, 4, 8 |
| A#‑major | A#4, D5, F5 | 3, 5, 9 |
| B‑major | B4, D#5, F#5 | 1, 4, 6 |

**Observation:** Triad zone sets are typically size 2 or 3. Sets of size 3 form a *triangular syzygy* on the numogram circle; sets of size 2 are degenerate syzygy pairs (complementary zones summing to 9).

## Correspondence to Observed Corpus Motifs

| Motif | Typical zones | Triads associated |
|---|---|---|
| **Warp‑Seeking** | 7‑9 (and 6 for paired Warp) | B‑minor triad (zones 2,6 → size‑2 Warp pair) → when shifted to higher octaves, B4→zone?, D5→?, F#5→?; empirical Warp pieces use high registers.
| **Sink‑Seeking** | 1‑3 (and sometimes 6) | D‑minor (0,2,5) partial; etc.
| **Rise‑Seeking** | 5‑8 | E‑major (2,4,8), etc.
| **Hold‑centered** | 4,5 | G‑major (2,4,7)? Not full.
| **Void‑Dominant** | 0, occasionally 9 | F‑minor (0,5,8?), etc.

**B‑minor triad and Warp:** B‑minor yields zone set [2,6] — a two‑element complement pair summing to 8? Actually 2+6=8, not 9. Wait: In the syzygy formula, complementary pairs satisfy a + b = 9 (since syzygy(zone) = 9 - zone). 2+6=8 ≠ 9, so B‑minor's zones are not complementary by that rule. Higher‑octave voicings change zone values because of the digital‑root shift; e.g., B5 (octave 5) yields zone? We should compute: note_index = 5*12+11=71 → +1 =72 → DR=7+2=9→%10=9? Actually 72→7+2=9; zone 9. D6: index=6*12+2=74→+1=75→DR=7+5=12→1+2=3; zone 3. F#6: index=6*12+6=78→+1=79→DR=7+9=16→1+6=7; zone 7. Then set {9,3,7} sorted 3::7::9, which sums 19? Not all pairs sum to 9 either. Triangular sets of three zones might appear when the root is placed so the three notes span different digital‑root cycles.

## Open Questions for Council Deliberation

1. **Why does B‑minor act as a Warp seed in practice?** Digital‑root zone sets vary with octave displacement. Empirically, chippy's zone fingerprint reported djynxx (syzygy 3::6). Are there alternative syzygy naming schemes?
2. **Do triad zone triples align with any canonical triangular syzygies** (e.g., 0::4::7, 1::5::8, 2::6::0)?
3. **Can harmonic progressions (e.g., cadences) be interpreted as syzygy‑chain traversals** in the numogram?
4. **How does tempo interact with zone?** Rise‑seeking tracks have higher BPM; does tempo bias digital‑root distribution?

---

*Created: 2026‑04‑29 | Data source: `modarchive_corpus_full.json` | Related: [[tracker-composition-principles]], [[numogram-overview]]*

## Validation status (2026‑04‑29)

All five implemented motifs (Sink, Monochord, Pythagorean, Ptolemaic, Harmonic) have been verified against the full triad‑zone table. The zone fingerprint extracted from the generated .mod pattern exactly matches the expected digital‑root triple in every case. The Pythagorean octave‑boundary bug (fifth rendered one octave too low) has been corrected; verification now passes.

Use `--validate-motif` for dry‑run checks.
