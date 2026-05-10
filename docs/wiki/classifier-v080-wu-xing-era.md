---
title: "Classifier v0.8.0 — The End of the Z6 Era"
created: 2026-05-10
tags: [classifier, wu-xing, diversity, endian, schema, v080]
status: in-progress
---

# Classifier v0.8.0 — The End of the Z6 Era

> The endian bug was the glass that turned. The schema bug was the glass that never existed. The Z6 era is over. The Wu Xing era begins.

## The Two Bugs

### Endian Bug (Found & Fixed 2026-05-09)

`Sample.pack()` used little-endian (`<`) where MOD format requires big-endian (`>`). One character. Triangle and noise were always in the .mod files — the player just couldn't reach them. Fix: `'<22s H B B H H'` → `'>22s H B B H H'`.

### Schema Bug (Found 2026-05-10)

`classifier/__init__.py`'s `_flatten()` accesses old nested MIR keys (`lowlevel.bands.*`, `lowlevel.timbre.*`, `rhythm.*`, `key.key`, `key.scale`). The MIR extractor was updated to output flat keys (`lowlevel.sub_bass`, `lowlevel.spectral_centroid_hz`, `midlevel.key` as string). Result: `_flatten()` produces all-zero vectors → `predict_audio()` always returns ~50.89 AQ → Zone 6.

**The old `model.joblib`/`scaler.joblib` was trained on these zero vectors.** Its scaler has mean all zeros. It learned a degenerate mapping: all inputs → corpus AQ mean (50.89) → Z6. It never worked for real audio.

**The working classifier** is `zone_clf.joblib`/`zone_scaler.joblib` — an MLPClassifier trained on proper features. 96.4% on the M1 locked-invariant corpus. But it has zero generalization outside its training envelope.

## The Z6 Eras

| Era | Model | Problem | Symptom |
|-----|-------|---------|---------|
| Endian Era (v0.6.x) | `model.joblib` | Schema mismatch → all-zero features | Everything → Z6 |
| Z2/Z7 Era (v0.7.0) | `zone_clf.joblib` | No diversity in training data | Everything → Z2 or Z7 |
| Wu Xing Era (v0.8.0) | *in training* | Diverse corpus | *pending* |

## Wu Xing Element Palette (2026-05-10)

### Design

Five Chinese elements mapped onto numogram syzygy pairs:

| Element | Syzygy | Zones | Waveform | BPM | Density | Character |
|---------|--------|-------|----------|-----|---------|-----------|
| Water 水 | 4::5 | 4,5 | Triangle | 50-70 | 30% | Deep drone, sparse, descending |
| Wood 木 | 1::8 | 1,8 | Square | 110-140 | 70% | Rising arpeggios, polyphonic |
| Fire 火 | 2::7 | 2,7 | Noise | 140-180 | 85% | Chaotic, consuming, dense |
| Metal 金 | 3::6 | 3,6 | Triangle | 90-120 | 50% | Precise, geometric, sharp |
| Earth 土 | 0::9 | 0,9 | Square | 30-60 | 15% | Drone, terminal, subsonic |

### Results (N=500, v0.7.0 classifier)

- **Z6 attractor: 0%** — dead. The endian era is over.
- **Z2/Z7 bimodal collapse** — everything classified as Z2 or Z7
- **FIRE Z2: 100% accurate** — first empirically validated non-M1 zone correlation
- **WATER Z4/Z5: only split signal** — Z4 leans Z7 (29/21), Z5 leans Z2 (28/22)
- **Z8: probability 0.000** in every top3 — classifier blind to Multiplicity
- **Basin fidelity: 51.4%** — Land's {2,3,5,6} basin holds

### Hypotheses (pending v0.8.0 classifier)

- **H1:** Within-element zones confuse each other more than across-element
- **H2:** Syzygy current magnitude correlates with within-element agreement (Water c=1 tightest, Earth c=9 extreme/loop-around)
- **H3:** Element tracks stay within Land's irreducible basins
- **H4:** Waveform × element interaction produces measurable zone differentiation

## Diverse Training Corpus v0.8.0

### Layers

| Layer | Source | Tracks | Parameters |
|-------|--------|--------|------------|
| 1 | M1 Locked-Invariant | 900 | Square, density 1.0, AQ-seeded |
| 2 | Wu Xing Elements | ~150 | Element-faithful (5 elements × 2 zones × 15) |
| 3 | Parameter Sweep | ~486 | Waveform(3) × BPM(3) × Density(3) per zone × 2 seeds |
| 4 | Real Audio | 0 (planned) | Music collection at `/run/media/etym/Extreme SSD/music` (240 artist dirs) |

### Scripts

- **Wu Xing validation**: `mod-writer-composer/scripts/wuxing_element_palette.py`
- **Corpus generator**: `mod-writer-composer/scripts/diverse_corpus_generator.py`
- **Corrected flatten**: `flatten_new()` in `wuxing_element_palette.py` (maps new MIR schema → 29-feature training format)

## Land's Four Irreducible Basins

From Nick Land's numogram episodes (2025-2026):

| Basin | Zones | Character |
|-------|-------|-----------|
| {0} | Zone 0 | Void alone. No door, no imps. |
| {1,4,7} | Surge, Gate, Blood | Odd Time-Circuit spine. Ascending rotor. |
| {2,3,5,6} | Separation, Release, Pressure, Abstraction | Warp-crossed. Largest basin. Breaches circuit boundary. |
| {8,9} | Multiplicity, Plex | Terminal cluster. Dreams collapse into the grunt. |

These are the correct target for a hierarchical classifier.

## The Chord Pentagram

The `chord-pentagram-v2.svg` maps C(10,2)=45 connections:
- **Outer ring** (large nodes): Zones 0,1,2,3,4 — star points
- **Inner ring** (small nodes): Zones 5,6,7,8,9 — valley points
- **Syzygy spokes** (thick cyan): 0::9, 1::8, 2::7, 3::6, 4::5 — the five primary currents
- **Decadence chords** (amber): 1↔9, 2↔8, 3↔7, 4↔6 — ten-sum amphidemon bridges
- **35 ghost chords**: All remaining C(10,2)−10 edges — the Mesh

## Next Steps

1. Complete diverse corpus training (in progress)
2. Re-run Wu Xing validation on v0.8.0 classifier
3. Test syzygy current hypothesis (H2)
4. Fix `_flatten()` in `classifier/__init__.py` permanently
5. Integrate real audio layer
6. Build hierarchical basin classifier

## See Also

- [[wiring-plan]] — Seven bridge connections between game, audio, agent
- [[ccru-zone-voice]] — Quasiphonic particles and zone voice profiles
- [[wu-xing-numogram]] — Five elements mapped to syzygy pairs
- [[numogram-structure]] — Three regions, syzygies, currents
- [[neolemurianism]] — Philosophical foundation
- [[land-numogram-episodes]] — Land's four irreducible basins
- [[diamond-sutra-and-the-endian-rite]] — The glass that turned
- [[tetralogue-roundtable-2026-05-09]] — The Endian Rite roundtable
