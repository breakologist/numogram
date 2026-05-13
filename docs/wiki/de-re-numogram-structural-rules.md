---
title: "DE-RE Numogram Structural Rules"
created: 2026-05-13
last_updated: 2026-05-13
status: reference
tags: ["de-re", "numogram", "base-n", "torque", "fractal", "structural-rules"]
related:
  - [[i-ching-connections]]
  - [[numogram-time-circuit]]
  - [[pandemonium]]
  - [[subdecadence]]
---

# DE-RE Numogram Structural Rules

Structural properties of the numogram system as generalized across different bases. Extracted from "DE-RE-Mystifying the CCRU's Numogram" (Internet Archive OCR, ~56K chars).

## Warp Region Condition

The Warp region exists in Base-N when N = 3M + 1 where M is odd:

| Base | 3^k + 1 | M | Warp? | Torque regions |
|------|---------|---|-------|---------------|
| 4 | 3¹ + 1 | 1 (odd) | ✅ | 0 |
| 10 | 3² + 1 | 2 (even) | ✅ | 1 |
| 16 | 3³ + 1 | 3 (odd) | ✅ | — |
| 22 | 3⁴ + 1 | 4 (even) | — | — |
| 28 | 3⁵ + 1 | 5 (odd) | ✅ | 2 |

Base-10 is the canonical case: 1 Torque region (the Time-Circuit), plus Warp and Plex.

## Multiple Time-Circuits

The number of Torque regions = M (from N = 3^M + 1):

- **Base-4:** 0 Time-Circuits (no temporal region)
- **Base-10:** 1 Time-Circuit (canonical 6-zone loop: 1→8→2→7→5→4)
- **Base-28:** 2 Time-Circuits (Torque-A and Torque-B, largely independent)
- **Base-244:** 5 Time-Circuits

## Triangular Number Rule

**Total demon count = T(N-1)** where T(k) = k(k+1)/2:

- Base-10: T(9) = 45 demons
- Base-12: T(11) = 66 demons
- Base-2: T(1) = 1 demon

## Decademon

A demon whose two zone-numbers sum to the base number (10 for Base-10):
- e.g., 1+9, 2+8, 3+7, 4+6 (5+5 is self-decadence, grants zero bonus)

## Zone-Planetary Correspondence

From DE-RE: mapping of 10 zones to planets:

| Zone | Planet | Character |
|------|--------|-----------|
| 0 | Sun | Central |
| 1 | Mercury | Mediator, messenger |
| 2 | Venus | — |
| 3 | Earth | — |
| 4 | Mars | — |
| 5 | Jupiter | — |
| 6 | Saturn | — |
| 7 | Uranus | — |
| 8 | Neptune | — |
| 9 | Pluto | Terminal |

This connects the numogram directly to astrology. Zone 1 = Mercury fits the Surge's role as messenger and mediator.

## Fractal Torque Structure

Base-82 (3⁴ + 1) has 3 Torque regions with sizes following powers of 3:

- **Torque-A:** 3⁴ = 27 zone-pairs
- **Torque-B:** 3³ = 9 zone-pairs
- **Torque-C:** 3² = 3 zone-pairs

Each is 1/3 the size of the previous. The numogram's temporal structure is self-similar.

## Base-28: Four Region Types

Base-28 develops a fourth region type absent in base-10:
- Plex region
- Warp region
- Large Torque region
- **Fourth region** (name not specified in source)

The numogram's internal structure is richer at larger bases.

## Demons as Decans

The 36 cards of Decadence share their quantity with the zodiac's **36 decans** (12 signs × 3 decans per sign). The numogram and astrology share the same combinatorial skeleton.

## Angels

Decadence and Subdecadence call **both** demons and angels. The angel system is the numogram's "light side" — the counterpart to the Pandemonium. 45 demons + N angels = complementary halves.

## Lurgo's Rite

Lurgo (1::0) has a single rite, Rel, following the path:

```
1 → 8 (syzygy) → 9 (minor flow) → 0 (syzygy partner)
```

Zone 1 paired with Zone 8, Zone 8 flows to Zone 9, Zone 9 paired with Zone 0. The system closes itself.

## Demonic Classification (from DE-RE source)

The DE-RE text provides an alternative demon classification beyond the standard 45-demon matrix. The standard Pandemonium Matrix has 15 chronodemons, 24 amphidemons, and 6 xenodemons. DE-RE may add additional classification criteria.

## Source

"DE-RE-Mystifying The CCRU's Numogram" (epub, ~56K chars). Internet Archive OCR scan. Multiple structural rules not documented elsewhere in the wiki.

## Related

- [[i-ching-connections]] — Contains the original extraction notes
- [[numogram-time-circuit]] — The Torque/Time-Circuit discussion
- [[pandemonium]] — 45-demon reference
- [[subdecadence]] — 36-card decadence = 36 zodiac decans
- [[c-ten-fortyfive-fiveness]] — C(10)=45 combinatorics
