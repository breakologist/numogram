---
title: I Ching Dictionary
created: 2026-05-06
last_updated: 2026-05-06
source: raw/I Ching Dictionary.epub (binary; structured mappings from iching-numogram-casting skill)
status: stub-reviewed
tags: [i-ching, yi-jing, hexagram, numogram, wu-xing, syzygy, divination]
---

# I Ching Dictionary — Hexagram-Zone Lattice

**Source**: raw/I Ching Dictionary.epub (219KB EPUB; extraction pending calibre/pandoc). Canonical mappings via [[iching-numogram-casting]]: 64 hexagrams → digital root (N-1 mod 9) → Zone.

## Hexagram → Zone Mapping
`(hex_number - 1) mod 9`; 0=Zone-0.

| Hex # | Name (King Wen) | Digital Root | Zone | Syzygy Carrier |
|-------|-----------------|--------------|------|---------------|
| 1 | Qian (Creative) | 0 | [[numogram#zone-0|Z0]] | Uttunul (36) |
| 2 | Kun (Receptive) | 1 | [[numogram#zone-1|Z1]] | Murrumur (29) |
| 3 | Tun (Difficulty) | 2 | [[numogram#zone-2|Z2]] | Oddubb (23) |
| ... | ... | ... | ... | ... (full 64 elided; Z1-9: 7 each, Z0:1) |
| 64 | Weiji (Before Completion) | 0 | [[numogram#zone-0|Z0]] | Uttunul (36) |

**King Wen Spiral**: Ascends zones 0→1→9 cycle (Z0 once; 1-9 repeat).

## Changing Lines Hypercube
192 edges (6/line ×64); **all cross zones** (powers-of-2 shift root).

## Wu Xing ↔ Syzygy
| Element | Syzygy | Gate |
|---------|--------|------|
| Water | 4::5 | Pressure |
| Wood | 1::8 | Multiplicity |
| Fire | 2::7 | Blood |
| Metal | 3::6 | Abstraction |
| Earth | 0::9 | Plex |

Generation: Pentagon; Control: Pentagram.

## Casting Pipeline
Hardware entropy → 6 lines → hexagram → Zone → Demon (45 via pair).

## See Also
- [[iching-numogram-casting]] — Full pipeline
- [[numogram]] — Zone topology
- [[pandemonium-matrix]] — 45 demons
- [[wu-xing]] — Elemental currents
- [[numogram-oracle]] — Divination

*Stub from raw/I Ching Dictionary.epub. Gaps: Full hexagram dict (terms/interpretations); PDF ingest.*
