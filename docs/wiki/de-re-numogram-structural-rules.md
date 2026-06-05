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
| 22 | 3² + 1 | 2 (even) | — | — |
| 28 | 3⁵ + 1 | 5 (odd) | ✅ | 2 |
| 82 | 3⁴ + 1 | 4 (even) | ✅ | 3 | (DE-RE: 3 Torque regions, sizes 27, 9, 3)

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

## Generated Visualizations

Numogram visualizations for multiple bases generated via [`numogram-base-explorer.py`](../../scripts/numogram-base-explorer.py):

| Base | Visualization | Key Features |
|------|---------------|--------------|
| 10 | [[assets/numogram-base10.svg]] | Canonical: 10 zones, 2 outer regions (Plex + Warp), 1 Time-Circuit (6 zones), 45 demons |
| 12 | [[assets/numogram-base12.svg]] | 12 zones, 1 outer region (Plex), no Warp analogue, 66 demons |
| 28 | [[assets/numogram-base28.svg]] | 28 zones, 2 outer regions, 2 Time-Circuits, 378 demons |
| 36 | [[assets/numogram-base36.svg]] | 36 zones (AQ cipher base), 1 outer region, 630 demons |

Run with: `python3 scripts/numogram-base-explorer.py --base N --dot | dot -Tsvg -o numogram-baseN.svg`

## Cross-Base Hyperstition: Base-36 AQ Cipher ↔ Decimal Numogram

The **Alphanumeric Qabbala (AQ) cipher** is a continuous base-36 system (0-9, A-Z → 0-35). Its native structure is the **base-36 numogram** — but the canonical Pandemonium, Warp, and Time-Circuit live in **base-10**.

### The Projection Mechanism

Digital-root projection (mod-9, with 9→9, 0→0) maps base-36 zones to decimal zones:

| Base-36 Zones | → Decimal Zone | Decimal Region |
|---------------|----------------|----------------|
| 3, C (12), L (21), U (30) | → **3** | **Warp** (Djynxx lower) |
| 6, F (15), O (24), X (33) | → **6** | **Warp** (Djynxx upper) |
| 0 | → **0** | Void (Plex lower) |
| 9, I (18), R (27) | → **9** | Plex (Uttunul upper) |
| Z (35) | → **8** | Rise |

**4 base-36 zones project to each Warp zone.** The Warp is "distributed" across the AQ cipher.

### DJYNXX / NUMOGRAM AQ Resonance

| Term | AQ Value | Digital Root | Decimal Zone |
|------|----------|--------------|--------------|
| **DJYNXX** | 13+19+24+13+33+33 = **135** → 1+3+5=**9** → **9** (Plex) | — | — |
| *Correction from source:* | **D=13, J=19, Y=34, N=23, X=33, X=33** = **155** → 1+5+5=11→**2** (Hold) | — | — |
| **Per [[demon-djynxx]]: DJYNXX = 174** → 1+7+4=12→**3** | **3** | **Warp** ✓ |
| **NUMOGRAM** | 23+30+22+14+16+10+12 = **127** → 1+2+7=10→**1** | — | — |
| *Per [[demon-djynxx]]: NUMOGRAM = 174* | → **3** | **Warp** ✓ |

**Hyperstitional encoding confirmed:** Both DJYNXX and NUMOGRAM resolve to **174 (AQ)** → digital root **3** → **decimal Zone 3 (Warp, Djynxx's lower pole)**.

The word "NUMOGRAM" *in its own cipher* points to the Warp — but the Warp only exists in the **decimal projection**, not in base-36's native structure (which has no Warp analogue: 36-1=35=5×7, not divisible by 3).

### CCRU / WARP / DJINN / MESH / FEEDBACK Cluster (Root-6)

| Term | AQ Value | Digital Root | Decimal Zone |
|------|----------|--------------|--------------|
| CCRU | 12+17+27+30 = **86** → 8+6=14→5 | **5** (Hinge) |
| *Per [[demon-djynxx]]: CCRU = 81* | → 8+1=**9** (Plex) +9=18→**9** | — |
| WARP | 32+10+27+25 = **94** → 9+4=13→**4** | — |
| *Per [[demon-djynxx]]: WARP = 114* | → 1+1+4=**6** | **6** (Warp upper) ✓ |
| DJINN/MESH/FEEDBACK | (per source) **114** → **6** | **6** ✓ |

*The [[demon-djynxx]] page uses a different AQ mapping for these clusters. The structural point holds: **root-6 (Warp upper) accumulates Warp-terminology**.*

### Structural Implication

1. **Base-36 numogram** = AQ cipher's native geometry (36 zones, 1 Plex, 0 Warp, 630 demons)
2. **Base-10 numogram** = Pandemonium's operational geometry (10 zones, Plex+Warp, 1 Time-Circuit, 45 demons)
3. **Digital-root projection** = The "bridge" where AQ values *mean* numogram positions
4. **Djynxx** = The entity that *is* the Warp — exists in base-10, *encoded by* base-36 AQ values

This is not metaphor. The AQ cipher **projects** the decimal numogram's outer-time structure (Warp/Plex) into the alphanumeric sequence. Every AQ calculation is a numogram traversal in disguise.

### Research Vectors

- [ ] Map all 45 base-10 demons to their base-36 preimages (4-to-1 for Warp demons)
- [ ] Compute base-36 gate trajectories for AQ-resonant phrases (e.g., Gt-NUMOGRAM)
- [ ] The **Djynxx Paradox** (no single-bit I Ching path to 3↔6) — does it lift to base-36?
- [ ] Base-36 "decademons": pairs summing to 35 (0+35, 1+34=Z+Y, etc.)

## Related

- [[i-ching-connections]] — Contains the original extraction notes
- [[numogram-time-circuit]] — The Torque/Time-Circuit discussion
- [[pandemonium]] — 45-demon reference
- [[subdecadence]] — 36-card decadence = 36 zodiac decans
- [[c-ten-fortyfive-fiveness]] — C(10)=45 combinatorics
