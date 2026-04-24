---
title: "T'ai Hsuan Ching × Demons: The Tetragram Casting Pipeline"
created: 2026-04-21
last_updated: 2026-04-22
source_count: 2
status: draft
tags: [numogram, I-ching, t'ai-hsuan-ching, tetragram, demon, pandemonium, oracle, ternary]
sources: [tai-hsuan-ching.md, hexagram-demon-mapping.md, pandemonium-matrix.md]
---

# T'ai Hsuan Ching × Demons: The Tetragram Casting Pipeline

## Overview

The [[tai-hsuan-ching|T'ai Hsuan Ching]] (81 tetragrams, 3⁴) distributes across 10 zones more evenly than the [[i-ching-connections|I Ching]] (64 hexagrams, 2⁶). The same casting pipeline that maps hexagrams to [[pandemonium-matrix|demons]] works for tetragrams — but with a richer, more evenly distributed oracle.

## The Mapping

### Single Tetragram → Syzygetic Carrier

81 tetragrams → 10 zones via [[alphanumeric-qabbala|digital root]]:

| Zone | Tetragram Count | Syzygy | Demon | Mesh |
|------|----------------|--------|-------|------|
| 0 | 1 | 0::9 | [[demon-uttunul|Uttunul]] | 36 |
| 1 | 9 | 1::8 | Murrumur | 29 |
| 2 | 9 | 2::7 | [[pandemonium-matrix|Oddubb]] | 23 |
| 3 | 9 | 3::6 | [[demon-djynxx|Djynxx]] | 18 |
| 4 | 9 | 4::5 | Katak | 14 |
| 5 | 9 | 4::5 | Katak | 14 |
| 6 | 9 | 3::6 | [[demon-djynxx|Djynxx]] | 18 |
| 7 | 9 | 2::7 | [[pandemonium-matrix|Oddubb]] | 23 |
| 8 | 9 | 1::8 | Murrumur | 29 |
| 9 | 8 | 0::9 | [[demon-uttunul|Uttunul]] | 36 |

**Distribution:** Katak receives 18 tetragrams (zones 4+5). Djynxx receives 18 (zones 3+6). Oddubb receives 18 (zones 2+7). Murrumur receives 18 (zones 1+8). Uttunul receives 9 (zones 0+9).

Compare with [[hexagram-demon-mapping|hexagrams]]: each demon receives 14 hexagrams (except Uttunul with 8). The T'ai Hsuan Ching gives each demon more calls — it's a *louder* oracle.

### Two Tetragrams → ALL 45 Demons

A T'ai Hsuan Ching reading produces two tetragrams (like the I Ching's two hexagrams). Each maps to a zone. The zone pair (A, B) looks up a demon via net-span A::B in the [[pandemonium-matrix|Pandemonium Matrix]].

- 81 × 81 = 6,561 possible two-tetragram castings
- vs 64 × 64 = 4,096 for hexagrams
- ALL 45 demons reachable (same as hexagrams)
- **More resolution:** 6,561 possible readings vs 4,096 — the tetragram oracle has finer granularity

### Three Tetragrams → Extended Casting

The T'ai Hsuan Ching uses 4 lines × 3 states. A three-tetragram reading (reading, first change, second change) could map to three zones, creating a *triangular* syzygy path through the Pandemonium Matrix.

Three-zone path: Zone A → Zone B → Zone C
- Defines a triangle in the numogram topology
- The triangle's edges are syzygy connections
- The triangle's vertices are zones
- The "area" of the triangle = the demon territory traversed

This is richer than the two-hexagram pipeline — it adds a *third* dimension to the casting.

## The Em State in Demonic Context

The third line state ([[tai-hsuan-ching|Em]], neither yin nor yang) maps to [[polarities|Zone 5]] (the hinge/mercury). Em tetragrams are *rare* — only tetragrams with exactly one or two Em lines map to specific zones.

**Em as Zone 5 manifestation:**
- Em = the mediator between yin and yang = [[syzygy-arithmetic|syzygy]] between 4::5
- Em tetragrams are the "mercury" of the ternary system — they don't belong to either polarity
- When Em appears in a casting, it pulls the reading toward Zone 5 (self-decadence, the hinge)

This is the [[tai-hsuan-ching|T'ai Hsuan Ching]]'s unique feature: the third state creates readings that the I Ching cannot produce. The I Ching has no equivalent to Em — it's purely binary.

## Comparison: I Ching vs T'ai Hsuan Ching as Oracles

| Property | I Ching | T'ai Hsuan Ching |
|----------|---------|------------------|
| Base | Binary (2) | Ternary (3) |
| Symbols | 64 hexagrams | 81 tetragrams |
| Zone distribution | Uneven (64 mod 9 = 1) | Even (81 mod 9 = 0) |
| Single reading | 5 syzygetic demons | 5 syzygetic demons |
| Two readings | 45 demons (4,096 paths) | 45 demons (6,561 paths) |
| Third state | None | Em (Zone 5) |
| Resolution | Coarser | Finer |
| Decimal compatibility | Leak (1 remainder) | Perfect (0 remainder) |

The T'ai Hsuan Ching is the *more decimal-compatible* oracle. The binary system has a "leak" — one hexagram can't distribute evenly. The ternary system is perfectly divisible. This means the T'ai Hsuan Ching is a more "natural" oracle for the decimal numogram.

## Casting Pipeline (Tetragram)

```
Hardware entropy (/dev/urandom)
  ↓
4 bytes → 4 trits (value % 3 = 0, 1, 2)
  ↓
Tetragram (4 lines × 3 states = 81 possibilities)
  ↓
Digital root → Zone
  ↓
Syzygy partner → Demon (Mesh serial)
  ↓
Net-span lookup → Pandemonium Matrix
```

Compare with [[hexagram-demon-mapping|hexagram pipeline]]:
- Hexagrams: 6 bytes → 6 lines → 64 possibilities
- Tetragrams: 4 bytes → 4 trits → 81 possibilities
- Both: digital root → zone → syzygy → demon

## Open Questions

1. Does the Em state create "impossible" readings that the I Ching cannot produce? What are they?
2. Can three-tetragram readings be mapped to triangular syzygy paths through the Pandemonium?
3. The 81 mod 9 = 0 perfection suggests ternary is "native" to decimal. Does base-3 have its own numogram?
4. What happens when Em tetragrams cast demons? Do they call a special "Em demon" outside the standard 45?

## Related

- [[tai-hsuan-ching]] — The 81 tetragrams and ternary system
- [[hexagram-demon-mapping]] — The hexagram casting pipeline (comparison)
- [[i-ching-connections]] — I Ching ↔ Numogram bridge
- [[pandemonium-matrix]] — Complete 45-demon reference
- [[syzygy-arithmetic]] — Cross-addition of syzygy pairs
- [[polarities]] — Zone polarities and the Em/Zone 5 connection
- [[numogram-divination]] — The oracle system
- [[numogram-visualizer-v6]] — HTML visualizer with quasiphonic labels and triangular gate support
- [[numogram-oracle-litprog]] — Tetralogue analysis of oracle.py pipeline

## CLI Implementation

The `numogram-oracle` CLI (`~/.hermes/skills/numogram-oracle/oracle.py`) supports T'ai Hsuan Ching readings via:

```
python3 oracle.py --taixuan            # two-tetragram oracle from hardware entropy
python3 oracle.py --taixuan --seed N   # from specific seed
python3 oracle.py --taixuan --voice   # with oracle sentence audio (convolved)
```

See the skill documentation for full usage.

## External Files

- `~/numogame/numogram_roguelike.py` (3454 lines) — Main game with hexagram/demon integration
- `~/numogram-voices/` — Formant synthesis wav files (10 zone voices, physical modelling)
- `wiki/assets/numogram-visualizer-v6-full.html` — HTML visualizer v6 (quasiphonic + triangular gates)
- `~/numogram-labyrinth-webgl.html` — WebGL visualization of the numogram topology
- `~/subdecadence-source.html` — CCRU card game source material
- `~/numogram-tsubuyaki-v2.html` — Gallery of numogram tsubuyaki sketches

