---
title: Interlocking Triangles
category: structure
tags: [numogram, pentagram, chord, hexagram, geometry]
source: chord-pentagram-v2.svg, powers-of-2-circular.svg
---

# Interlocking Triangles

Two triangles interlock to form the hexagram that underpins the CCRU's
pentagram structure in the `chord-pentagram-v2.svg` diagram.

## Diagrams

`chord-pentagram-v2.svg`

```
  Z2                  Z4
   ♪─────────║◈║───────║
  Z1 ♪ ~ ║◈║*test◈*║◈ ║ ♪  Z5   ← inner valley zone (Z3 center)
  Z9 ♪ ~ ║*║◈*◈◈*║* ║ ♪  Z7
   ♪───────║*║◈*◈◈*║*║───────║
           Z0▓L  Z8     Z6    ← outer star-points (zones 1, 5, 9)
```

`powers-of-2-circular.svg` renders the same geometry differently:

```
       ▲ 1-2-4          ▽ 8-7-5
   cyan triangle         amber triangle
   (TC-set apex)         (multiplicity base)
```

## Structure

- Triangle 1 (forward/triangle): vertices at Z1 (alpha), Z2 (beta), Z9 (gamma-pivot),
  vertex contour property `[vertex_z1, gyr_2_1x, att_universal_z9]`
- Triangle 2 (inverse/bowtie): vertices at Z5, Z8, Z7 — `[att_universal_z7,
  gyr_4_1x, axion_z5]`
- The two triangles meet at Z4 (centroid, TC-set node) which is the
  pentagram's "sixth step/node"

## Numogram Properties

The backing topology of this pentagram means that:
- five points (vertices) correspond to the five outer-layer zones
- five points (valleys) correspond to the inner-layer zones
- the hexagram dual with power-of-2 diagram is a separate mapping but
  shares the same anhydrous coordinate alignment

## See

- [[intermorphology-plan]]
- [[demon-chronicles]]
- [[tc-≡-2²]]
