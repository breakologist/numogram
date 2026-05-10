# Zone Classifier v0.8.x — Roadmap

**Created:** 2026-05-10  
**Status:** Active  
**Parent:** [[phase5-roadmap]]

## Completed

| Milestone | Date | Result |
|-----------|------|--------|
| M1 — Zone-Constrained Composition | May 3 | 96.4% (locked invariants only) |
| M2 — VAE Hallucination | May 6 | 92% gap zones |
| Endian bug found/fixed | May 9 | All 3 waveforms audible |
| Schema bug found/fixed | May 10 | `_flatten()` was producing zero vectors |
| Wu Xing palette pilot (N=500) | May 10 | Z6 dead; Z2/Z7 bimodal on v0.7.0 |
| Diverse corpus v0.8.0 (1536 tracks) | May 10 | 78.1% train / 73.1% test |
| Wu Xing validation v0.8.0 (N=500) | May 10 | **92.2% overall**, 94.2% basin fidelity |

## Current (v0.8.1 — Stacked Pentatonic)

**Goal:** Expand each zone's note palette from 1 octave to 3 octaves with zone-specific tessitura (octave distribution weights).

**Why:** Single-octave pentatonic is tight — 5 notes × 2 octaves = 10 slots for 9 zones. Multi-octave gives each zone vertical range, enabling richer melodies and zone-over-time trajectories without sacrificing zone identity. The dungeon walk through zones becomes a walk through pitch space.

**Blocked by:** `SongBuilder.add_section()` uses internal `note_and_octave_from_zone()` in `mapping.py` which maps to a single octave. Multi-octave generation needs either:
- A new `SongBuilder` parameter for octave override
- Direct MOD construction with variable periods
- A wrapper that post-processes the pattern grid with octave shifts

**Tasks:**
- [ ] Add `octave` parameter to `SongBuilder.add_section()`
- [ ] Implement zone tessitura sampling in `mapping.py` or composer layer
- [ ] Generate small test set (10 tracks/zone, 3 octaves)
- [ ] Evaluate on v0.8.0 classifier → does it still work?
- [ ] If accuracy drops >15%: retrain with multi-octave tracks → v0.8.1
- [ ] If accuracy holds: no retraining needed, multi-octave is "free"

**Retraining policy:** No separate classifier. Extend the 1536-track corpus with multi-octave variants. Same MLP architecture, same 29 features. The classifier learns that Z1 = "C-ness across octaves" not "C4 specifically."

## Next (v0.8.2 — Real Audio)

**Goal:** Integrate real music from `/run/media/etym/Extreme SSD/music` (240 artist dirs) as training data.

**Strategy:** Pseudo-labeling. Use v0.8.0/8.1 classifier to assign zone labels to real tracks. Train on the combined synthetic+real corpus. This teaches the classifier natural timbres, real rhythms, and genre diversity while preserving the zone structure learned from synthetic data.

**Tasks:**
- [ ] Survey music collection for genre/era diversity
- [ ] Sample ~200 tracks across genres
- [ ] Extract MIR features with corrected `flatten_new()`
- [ ] Pseudo-label with current classifier
- [ ] Retrain on synthetic + real → v0.8.2
- [ ] Manual listening check: do zone assignments feel right?

## Later (v0.9.0 — Zone-Over-Time Trajectories)

**Goal:** A track is not a single zone — it's a path through the 89. Classifier outputs a zone trajectory, not a single label.

**Architecture:**
- Sliding-window MIR extraction (5-10s windows, 2-5s overlap)
- Map each window to a zone prediction
- Output: `{dominant_zone: 2, trajectory: [4,8,2,3,9], distribution: {...}, basin: "2-3-5-6"}`

**Connects to:** Dungeon sonification (DFS traversal = trajectory), Land's 89 paths, syzygy chain fingerprinting.

**Tasks:**
- [ ] Implement sliding-window MIR extraction
- [ ] Generate multi-section MOD tracks with known section boundaries
- [ ] Validate: does the trajectory match the known sections?
- [ ] Connect to `dungeon-sonification` — dungeon walk = trajectory

## Future (v0.10.0 — Septatonic & Beyond)

**Goal:** Expand from pentatonic (5) → septatonic (7) → dodecatonic (12) as optional generation modes, mapping to planetary and chromatic systems.

**Scale architecture:**

| Scale | Notes | Numogram Map | Use Case |
|-------|-------|-------------|----------|
| Pentatonic (5) | C-D-E-G-A | 5 syzygies | Current. Elemental, zone-distinct. |
| Septatonic (7) | C-D-E-F-G-A-B | 7 classical planets + 5 currents + 2 outer regions | Planetary, modal. Each zone = a mode. |
| Dodecatonic (12) | All 12 | 12 phase doors across 10 zones | Chromatic. Maximal palette. Zone identity may blur. |

**Caveat:** Each new scale is a separate classifier retraining. The septatonic in particular may require more features (chroma, mode detection) than the current 29-flat MIR vector. A spectrogram CNN might be the right approach for chromatic classification.

## Open Questions

1. **Z7 (Blood) at 54%** — is noise waveform the cause, or is Z7 inherently ambiguous? Test: Z7 with square wave → does accuracy recover?
2. **Z0 (Void) at 100%** — is this genuine or an artifact of the near-silent generation? Test with varied Void parameters.
3. **Real audio labeling** — is pseudo-labeling sufficient, or do we need manual zone assignment for a validation set?
4. **Feature dimensionality** — are 29 features enough for 9 zones × 3 waveforms × 3 octaves? When do we need the Essentia full pool (60-120 features)?
5. **Hierarchical classifier** — would Land's 4-basin top-level improve accuracy, or is the flat 9-way MLP sufficient?

## File Inventory

| File | Purpose |
|------|---------|
| `mod-writer-composer/scripts/wuxing_element_palette.py` | Wu Xing generation + validation |
| `mod-writer-composer/scripts/diverse_corpus_generator.py` | Diverse training corpus generator |
| `mod-writer-composer/scripts/stacked_pentatonic_experiment.py` | Multi-octave experiment |
| `mod-writer/mod_writer/classifier/__init__.py` | Classifier module (`_flatten` needs fix) |
| `mod-writer/mod_writer/classifier/artifacts/zone_clf_v080.joblib` | v0.8.0 classifier |
| `mod-writer/mod_writer/mapping.py` | `note_and_octave_from_zone()` — needs octave param |
| `/tmp/diverse_corpus_v080/` | Training artifacts |
| `/tmp/wuxing_palette/` | Validation artifacts |

## Related Wiki Pages

- [[classifier-v080-wu-xing-era]] — Full development story
- [[wuxing-element-palette-v080-results]] — Validation results
- [[land-decimal-intelligence]] — Land's 360 / 89 paths
- [[wu-xing-numogram]] — Five elements × syzygy mapping
- [[phase5-roadmap]] — Parent roadmap
- [[wiring-plan]] — Cross-system bridges
