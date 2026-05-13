---
title: "Hexagram → Demon Mapping"
created: 2026-05-13
last_updated: 2026-05-13
status: stub
tags: ["i-ching", "hexagram", "demon", "numogram", "casting", "pandemonium"]
related:
  - [[hexagram-zone-mapping]]
  - [[i-ching-connections]]
  - [[iching-numogram-casting]]
  - [[pandemonium]]
---

# Hexagram → Demon Mapping

> **STUB.** Pipeline for mapping single or two-hexagram I Ching readings to the 45-demon Pandemonium Matrix.

## Single Hexagram → 5 Carrier Demons

A single hexagram maps to a zone, which maps to its syzygy carrier:

```
Hexagram → zone → syzygy → carrier demon
```

| Carrier | Syzygy | Hexagrams assigned (DR method) |
|---------|--------|-------------------------------|
| Murrumur | 1↔8 | Zones 1 and 8 hexagrams |
| Oddubb | 2↔7 | Zones 2 and 7 hexagrams |
| Djynxx | 3↔6 | Zones 3 and 6 hexagrams |
| Katak | 4↔5 | Zones 4 and 5 hexagrams |
| Uttunul | 0↔9 | Zone 9 hexagrams only (Zone 0 has none via DR) |

Distribution: 14 hexagrams each for Katak, Djynxx, Oddubb, Murrumur. 7 for Uttunul (under DR method, Zone 0 is empty).

## Two Hexagrams → All 45 Demons

Traditional casting (reading + transformed hexagram) produces 64×64 = 4,096 possible readings. When mapped via the Pandemonium Matrix net-span lookup, **ALL 45 demons are reachable** from two-hexagram castings.

The net-span between the two hexagram zones determines the demon. Non-syzygy pairs walk **unmediated paths** — no carrier, traversed alone. See [[i-ching-connections#non-syzygy-paths]].

## Unmediated Paths

~69% of possible zone pairs are unmediated (no named carrier). These include:
- Lateral steps (net-span 1): adjacent zones, subtle shifts
- Wide gaps (net-span 2-4): significant but unnamed transitions

The querent walks these paths without a demon escort. See [[i-ching-connections]] for divination interpretation.

## See Also

- [[hexagram-zone-mapping]] — Full 64-hexagram reference table
- [[iching-numogram-casting]] — Complete casting pipeline skill
- [[pandemonium]] — 45-demon matrix reference
- [[tai-hsuan-ching-demons]] — Tetragram-to-demon pipeline (ternary system)
