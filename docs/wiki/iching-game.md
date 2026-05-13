---
title: "Hexadence — The I Ching Card Game"
created: 2026-05-13
last_updated: 2026-05-13
status: stub
tags: ["i-ching", "game", "divination", "hexagram", "hexadence"]
related:
  - [[i-ching-connections]]
  - [[hexagram-zone-mapping]]
  - [[subdecadence]]
  - [[decadence]]
---

# Hexadence

> **STUB.** Third divination system: hexagram casting with entropy budget and demon difficulty scoring.

## Concept

An I Ching-inspired divination game extending the Subdecadence/Decadence card game framework into the 64-hexagram space:

- **Deck:** 64 hexagram cards (or digital equivalent)
- **Entropy source:** Hardware entropy for casting (see [[i-ching-connections#hardware-entropy-casting]])
- **Spread:** Hexagram → zone → demon scoring
- **Difficulty:** Based on hexagram's zone position (higher zones = higher entropy requirements)
- **Changing lines:** Track which lines change → zone transition → demon net-span

## Relationship to existing games

| Game | Cards | Pairing | Demons |
|------|-------|---------|--------|
| Subdecadence | 40 | Sum-to-9 (syzygy) | 45 demons |
| Decadence | 36 | Sum-to-10 | 36 demon-cards |
| Hexadence | 64 | Changing-line transformation | All 45 demons reachable |

## TODO

- [ ] Define deck structure and card faces
- [ ] Specify entropy budget mechanics
- [ ] Implement demon difficulty scoring
- [ ] Design spread layout (analog of Atlantean Cross for 64 cards)
- [ ] Write oracle.py integration

## See Also

- [[subdecadence]] — CCRU card game
- [[decadence]] — Sum-to-10 pairing game
- [[i-ching-connections#hardware-entropy-casting]] — Casting from physical noise
- [[iching-numogram-casting]] — Skill: casting pipeline
