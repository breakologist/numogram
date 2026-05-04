# Tracker Motif‑Triad Reference — mod‑writer Design Notes

> **Scope:** Concrete recommendations for the `mod-writer` skill: which triads and register choices maximize alignment with each zone motif. Derived from digital‑root zone mapping (same as [[tracker-music-theory-mappings]]). Motif target zones per `compute_fingerprint`: Warp {7,8,9}, Rise {7,8}, Hold {4,5}, Sink {1,2,3,6}, Void {0}.

## How to use

For each desired motif, pick a triad‑quality‑octave combination from the top of the corresponding table below. The score is the count of triad zones that fall inside the motif's target range. Because a single triad occupies at most 2 target zones (except Sink which can be 3), additional notes or non‑triadic fills are recommended to reach >=30% motif ratio observed in the corpus.

## Top triad candidates per motif

### Sink
| Root (±oct) | Quality | Zones | Overlap |
|---|---|---|---|
| D‑minor @ o3 | minor | 1, 3, 6 | 3 |
| B‑minor @ o3 | minor | 1, 3, 6 | 3 |
| G#‑minor @ o4 | minor | 1, 3, 6 | 3 |
| F‑minor @ o5 | minor | 1, 3, 6 | 3 |
| D‑minor @ o6 | minor | 1, 3, 6 | 3 |

### Warp
| Root (±oct) | Quality | Zones | Overlap |
|---|---|---|---|
| G#‑minor @ o3 | minor | 3, 7, 9 | 2 |
| G#‑major @ o3 | major | 4, 7, 9 | 2 |
| F‑minor @ o4 | minor | 3, 7, 9 | 2 |
| F‑major @ o4 | major | 4, 7, 9 | 2 |
| D‑minor @ o5 | minor | 3, 7, 9 | 2 |

### Hold
| Root (±oct) | Quality | Zones | Overlap |
|---|---|---|---|
| C‑minor @ o3 | minor | 1, 4, 8 | 1 |
| C‑major @ o3 | major | 1, 5, 8 | 1 |
| C#‑minor @ o3 | minor | 2, 5, 9 | 1 |
| D#‑minor @ o3 | minor | 2, 4, 7 | 1 |
| D#‑major @ o3 | major | 2, 4, 8 | 1 |

### Rise
| Root (±oct) | Quality | Zones | Overlap |
|---|---|---|---|
| C‑minor @ o3 | minor | 1, 4, 8 | 1 |
| C‑major @ o3 | major | 1, 5, 8 | 1 |
| D‑major @ o3 | major | 1, 3, 7 | 1 |
| D#‑minor @ o3 | minor | 2, 4, 7 | 1 |
| D#‑major @ o3 | major | 2, 4, 8 | 1 |

### Void
| Root (±oct) | Quality | Zones | Overlap |
|---|---|---|---|
| C‑minor @ o3 | minor | 1, 4, 8 | 0 |
| C‑major @ o3 | major | 1, 5, 8 | 0 |
| C#‑minor @ o3 | minor | 2, 5, 9 | 0 |
| C#‑major @ o3 | major | 2, 6, 9 | 0 |
| D‑minor @ o3 | minor | 1, 3, 6 | 0 |

## Extended discussion

* **Sink** offers perfect matches (overlap = 3) via D‑minor / B‑minor at octave 3, and G#‑minor at octave 4. These triads alone can achieve pure Sink texture if the rest of the arrangement stays within Sink zones. Use low registers and avoid high arpeggios.

* **Warp** never reaches all three target zones from a triad alone; best you get is two (e.g., G#‑minor @o3 zones [3,7,9]). To push Warp‑ratio >20%, layer in pentatonic runs that hit zone 8 (e.g., high‑register A‑notes) or use portamento sweeps that traverse zones 7→8→9.

* **Hold** is sparse across triads; best overlap is 1 (C‑minor @o3 includes zone 4). Hold‑heavy pieces (e.g., Brogue‑inspired generators) should use fourth‑chord structures rather than triads.

* **Rise** requires zones 7 or 8. The highest‑scoring triads already include zone 7 or 8, but never both. Complement with suspended 4th/2nd extensions.

* **Void** cannot be touched directly by triadic notes; Void‑dominant tracks (e.g., `retrograde`) employ sustained rests, very low note density, and occasional C‑2 sub‑bass. Triad‑based construction works against Void.


## Implementation note for `mod-writer`

Add a constraint system:

```python

TRIAD_MOTIF_POLICY = {

  "Sink":  [("D","minor",3), ("B","minor",3), ("G#","minor",4)],

  "Warp":  [("G#","minor",3), ("F","minor",4), ("D","minor",5), ("G#","major",3)],

  "Hold":  [("C","minor",3), ("C","major",3), ("C#","minor",3)],

  "Rise":  [("C","minor",3), ("D","major",3), ("D#","major",3), ("E","major",4)],

  "Void":  []  # triad avoided

}

```

When generating a pattern, pick a base triad from the chosen motif's list and enforce its root/quality within a ±1 octave tolerance. Complement with gate‑notes that round out the motif ratio.


---

*Created: 2026‑04‑29 | Data: digital‑root mapping over octaves 3–7 | See also: [[tracker-music-theory-mappings]], [[modwriter-orchestration]], [[tracker-composition-principles]]*


## ✅ Validation status (2026‑04‑29)

All five motifs now produce the correct zone triple when rendered:

| Motif       | Expected zones | Observed zones | Status |
|-------------|----------------|----------------|--------|
| Sink        | [1, 3, 6]      | [1, 3, 6]      | ✅ |
| Monochord   | [1, 3, 6]      | [1, 3, 6]      | ✅ |
| Pythagorean | [3, 6, 8]      | [3, 6, 8]      | ✅ |
| Ptolemaic   | [1, 5, 8]      | [1, 5, 8]      | ✅ |
| Harmonic    | [2, 4, 8]      | [2, 4, 8]      | ✅ |

**Octave‑boundary bug fixed** — `apply_triad_motif` previously used the candidate octave for all chord tones, causing the fifth (and sometimes third) to be placed one octave too low when the interval crossed an octave boundary (e.g., Pythagorean G‑major: G3–B3–D4; D was incorrectly rendered as D3). The fix computes absolute semitone indices and derives individual octaves per chord tone.

**Dry‑run validation**: use the new `--validate-motif NAME` CLI flag to perform an in‑memory zone check without writing a `.mod` file. Exit code 0 on pass, 1 on failure; JSON report printed to stdout.


