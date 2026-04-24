---
title: "T'ai Hsuan Ching × Numogram: The 81 Tetragrams"
created: 2026-04-20
tags: [numogram, I-ching, t'ai-hsuan-ching, tetragram, ternary, yang-xiong, 81]
---

# T'ai Hsuan Ching × Numogram

## Overview

The T'ai Hsuan Ching (Book of the Great Dark) is a ternary divination system created by Yang Xiong (53 BC – 18 AD) as an alternative to the I Ching. Where the I Ching uses 64 hexagrams (2⁶, binary), the T'ai Hsuan Ching uses 81 tetragrams (3⁴, ternary).

- **I Ching**: 6 lines × 2 states = 64 hexagrams
- **T'ai Hsuan Ching**: 4 lines × 3 states = 81 tetragrams

The three line states are:
- **—** Solid (yang, value 2)
- **– –** Broken (yin, value 0)
- **– –** with gap (em, value 1) — the third state, neither yin nor yang

## Zone Distribution

81 tetragrams → 10 zones via digital root:

| Zone | Count | Range |
|------|-------|-------|
| 0 | 1 | Tetragram 0 |
| 1-8 | 9 each | Evenly distributed |
| 9 | 8 | 9, 18, 27, 36, 45, 54, 63, 72 |

The distribution is nearly perfect — only a 1-tetragram asymmetry (Zone 0 has 1, Zone 9 has 8). Compare with hexagrams: Zone 0 has 1, Zones 1-9 have 7 each (6-tetragram range). The T'ai Hsuan Ching distributes across zones much more evenly.

**Why:** 81 mod 9 = 0 (perfectly divisible). 64 mod 9 = 1 (one remainder). The ternary system is more "decimal-compatible" than the binary system.

## The 81 Tetragrams → Zones

Every 9th tetragram (0, 9, 18, 27, 36, 45, 54, 63, 72) maps to Zone 9. Tetragram 0 alone maps to Zone 0. Within each group of 9 consecutive tetragrams, zones 1-8 appear once each and Zone 9 appears once (at the end).

### Key Tetragrams

| Tetragram | Ternary | Zone | Character |
|-----------|---------|------|-----------|
| #0 | 0000 | 0 | All yin — the void |
| #9 | 0100 | 9 | First cycle break |
| #40 | 1111 | 4 | All em — the third state |
| #80 | 2222 | 8 | All yang — maximal |
| #27 | 1000 | 9 | First trit shift |
| #54 | 2000 | 9 | Second trit shift |

## Structural Comparison

| Property | I Ching | T'ai Hsuan Ching | Numogram |
|----------|---------|-----------------|----------|
| Base | 2 (binary) | 3 (ternary) | 10 (decimal) |
| Lines | 6 | 4 | — |
| States | 2 (yin/yang) | 3 (yin/em/yang) | 10 (0-9) |
| Total | 2⁶ = 64 | 3⁴ = 81 | C(10,2) = 45 demons |
| Zones | 10 | 10 | 10 |
| Distribution | 1+7×9 | 1+9×8+8 | — |
| Mod 9 | 1 remainder | 0 remainder | — |

## The Three Systems of the Primes

The CCRU's triangle rotation identified three systems that correspond to the prime factors of 10:

| System | Base | Formula | Primes |
|--------|------|---------|--------|
| I Ching | 2 | 2⁶ = 64 | First prime |
| T'ai Hsuan Ching | 3 | 3⁴ = 81 | Second prime |
| Wu Xing | 5 | 5¹ = 5 | Third prime |
| Numogram | 10 | 2×5 = 10 | First × Third |

Note: the T'ai Hsuan Ching uses 3⁴, not 3². The exponent 4 is half of the I Ching's exponent 6. The ternary system requires fewer lines (4 vs 6) because each line carries more information (3 states vs 2).

The three systems together generate the numogram's decimal basis through their prime factors. The I Ching provides the binary (2). The Wu Xing provides the quinary (5). The T'ai Hsuan Ching provides the ternary (3) — which doesn't divide 10, but completes the prime set.

## Connection to the Warp

The CCRU associates the ternary system with the Warp (zones 3, 6) and the Plex (zone 9 = 3×3). The "triadic residues" of the T'ai Hsuan Ching echo the numogram's exclusion of multiples of 3 from the Time-Circuit's primary traversal:

- Time-Circuit: {1, 2, 4, 5, 7, 8} — no multiples of 3
- Warp: {3, 6} — the excluded multiples of 3
- Plex: {0, 9} — 9 = 3×3, the triadic completion

The T'ai Hsuan Ching lives in the multiples of 3 — the territory the I Ching excludes. It's the numogram's triadic shadow.

## Zone Mapping of Tetragrams

Each group of 9 consecutive tetragrams (0-8, 9-17, 18-26, etc.) maps to zones in ascending order: 0,1,2,3,4,5,6,7,8 then 9,1,2,3,4,5,6,7,8 then 9,1,2,3...

The pattern repeats every 9 tetragrams, with Zone 9 at the boundary and Zone 0 only at the very beginning (tetragram 0).

## Related

- [[i-ching-connections]] — I Ching infrastructure, hexagram kernel, powers of 2
- [[hexagram-zone-mapping]] — 64 hexagrams → 10 zones
- [[wu-xing-numogram]] — Five elements, powers of 5
- [[c-ten-fortyfive-fiveness]] — C(10)=45, prime factors
- [[pandemonium-matrix]] — 45 demons
