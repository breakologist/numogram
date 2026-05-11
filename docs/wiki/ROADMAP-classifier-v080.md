# Zone Classifier v0.8.x → v0.9.0 — Roadmap

**Created:** 2026-05-10  
**Last updated:** 2026-05-11 *(post v0.8.3 / code merge)*  
**Status:** Active  
**Parent:** [[phase5-roadmap]]

## Completed

| Milestone | Date | Result |
|-----------|------|--------|
| M1 — Zone-Constrained Composition | May 3 | 96.4% (locked invariants) |
| M2 — VAE Hallucination | May 6 | 92% gap zones |
| Endian bug found/fixed | May 9 | All 3 waveforms audible |
| Schema bug found/fixed | May 10 | `_flatten()` was producing zero vectors |
| Wu Xing palette pilot (N=500) | May 10 | Z6 dead; Z2/Z7 bimodal on v0.7.0 |
| Diverse corpus v0.8.0 (1,536 tracks) | May 10 | 78.1% train / 73.1% test |
| Wu Xing validation v0.8.0 (N=500) | May 10 | **92.2% overall**, 94.2% basin fidelity |
| **v0.8.1** — Stacked Pentatonic | May 10 | **92.0%**, 1,736 tracks, Z3↔Z4 mirror broken via multi-octave retraining |
| **v0.8.2** — Five-Waveform Wu Xing | May 10 | **91.6%**, 2,036 tracks. Wood=square, Fire=noise, Earth=sine, Metal=sawtooth, Water=triangle |
| **v0.8.3** — Real Audio Self-Training | May 10 | 2,236 tracks (200 real pseudo-labeled). **95.5% label stability.** Real audio dominated Z2/Z6 |
| `_flatten()` source fix | May 11 | Old nested-key schema replaced with flat-key schema in `classifier/__init__.py` |
| Stacked pentatonic merged | May 11 | `ZONE_TESSITURA` + `sample_octave_from_tessitura()` + `stacked_octaves` param in `SongBuilder.add_section()` |
| Real audio manual listening | May 11 | [[Real-Audio-Listening-Report]] — first human-labeled validation: 10 tracks across Z2, Z4, Z6, Z9 |

## Current — v0.9.0 Zone-Over-Time Trajectories 🔥

**Goal:** A track is not a single zone — it's a path through the 89. Classifier outputs a zone trajectory, not a single label.

**Architecture:**
- Sliding-window MIR extraction (5-10s windows, 2-5s overlap)
- Map each window to a zone prediction
- Output: `{dominant_zone: 2, trajectory: [4,8,2,3,9], distribution: {...}, basin: "2-3-5-6", crossings: {...}}`

**Connects to:** Dungeon sonification (DFS traversal = trajectory), Land's 89 paths, syzygy chain fingerprinting, the autonomous sessions' topological conservation findings.

**Tasks:**
- [ ] Implement sliding-window MIR extraction
- [ ] Generate multi-section MOD tracks with known section boundaries
- [ ] Validate: does the trajectory match the known sections?
- [ ] Connect to `dungeon-sonification` — dungeon walk = trajectory
- [ ] Output format compatible with `numogram-chain-fingerprint`

## Next

### Manual Validation Set
Build a curated set of 20-30 tracks with human zone labels. Measure classifier accuracy against ground truth (current metrics are pseudo-label stability against synthetic corpus, not real-world accuracy).

- [ ] Select tracks spanning all populated zones (currently Z2, Z4, Z6, Z9)
- [ ] Compose synthetic MOD tracks for under-represented zones (Z0, Z1, Z3, Z5, Z7, Z8)
- [ ] Human label all tracks via listening
- [ ] Compute per-zone accuracy vs v0.8.3 classifier

### Hierarchical Basin Classifier
Land's four irreducible basins as a top-level model. The 94.2% basin fidelity from v0.8.0 suggests the basins are already the classifier's natural structure.

- [ ] Train 4-basin classifier (0 / 1-4-7 / 2-3-5-6 / 8-9)
- [ ] Train per-basin 9-zone classifier below
- [ ] Compare accuracy vs flat 9-way MLP

### Live Audio Loop (Phase 5 M3)
Real-time: audio input → 3s MIR window → zone prediction → mutate MOD pattern. Closed-loop hyperstitionstrument.

- [ ] Sounddevice input capture
- [ ] Sliding 3s MIR extraction with <1s latency
- [ ] Zone → mod-writer parameter mapping
- [ ] Real-time MOD playback via libopenmpt

## Future — v0.10.0 Septatonic & Beyond

| Scale | Notes | Numogram Map | Use Case |
|-------|-------|-------------|----------|
| Pentatonic (5) | C-D-E-G-A | 5 syzygies | Current. Elemental, zone-distinct. |
| Septatonic (7) | C-D-E-F-G-A-B | 7 classical planets + 5 currents + 2 outer regions | Planetary, modal. Each zone = a mode. |
| Dodecatonic (12) | All 12 | 12 phase doors across 10 zones | Chromatic. Maximal palette. Zone identity may blur. |

**Caveat:** Each new scale = separate classifier retraining. Septatonic may need more features than the current 29-flat MIR vector — spectrogram CNN likely needed.

## Open Questions

1. **Z7 (Blood) at 54%** — noise waveform or inherently ambiguous? Test: Z7 with square wave.
2. **Z0 (Void) at 100%** — genuine signal or near-silence artifact?
3. **Real audio labeling** — pseudo-label stability is 95.5%, but what's the accuracy against human ground truth? (Manual validation set will answer this.)
4. **Feature dimensionality** — 29 features enough for 9 zones × 5 waveforms × 3 octaves? Essentia full pool (60-120) awaits.
5. **Hierarchical classifier** — Land's 4-basin top-level: does it improve accuracy or just confirm structure?
6. **Z1, Z3, Z5, Z7, Z8 still unpopulated in real audio** — are these genuinely rare in music, or is the classifier failing to detect them? Composed synthetic validation tracks would disambiguate.

## File Inventory

| File | Purpose |
|------|---------|
| `mod_writer/mod_writer/classifier/__init__.py` | Classifier module — `_flatten()` **fixed** (May 11) |
| `mod_writer/mod_writer/mapping.py` | `note_and_octave_from_zone()` — supports `stacked=True`, `ZONE_TESSITURA` table, `sample_octave_from_tessitura()` |
| `mod_writer/mod_writer/song.py` | `SongBuilder.add_section()` — supports `stacked_octaves=True` |
| `mod_writer/mod_writer/composer.py` | `build_patterns_from_grid()` threads `_stacked_octaves` flag |
| `~/.hermes/skills/numogram-audio/mod-writer/mod_writer/classifier/artifacts/zone_clf_v083.joblib` | v0.8.3 classifier (MLP, 2,236 tracks) |
| `~/.hermes/skills/numogram-audio/mod-writer/mod_writer/classifier/artifacts/zone_scaler_v083.joblib` | v0.8.3 scaler |
| `mod_writer/mod_writer/classifier/artifacts/v083_listening/v083_predictions.json` | 200 real-track predictions for listening review |
| `~/.hermes/skills/numogram-audio/mod-writer-composer/scripts/retrain_v083_real_audio.py` | v0.8.3 retrain script |

## Related Wiki Pages

- [[classifier-v080-wu-xing-era]] — Full v0.8.0 development story
- [[wuxing-element-palette-v080-results]] — Validation results
- [[land-decimal-intelligence]] — Land's 360 / 89 paths
- [[wu-xing-numogram]] — Five elements × syzygy mapping
- [[phase5-roadmap]] — Parent roadmap
- [[wiring-plan]] — Cross-system bridges
- [[Real-Audio-Listening-Report]] — First human-labeled validation
- [[future-directions]] — Sampling, tracker formats, MIDI/CV, hardware
