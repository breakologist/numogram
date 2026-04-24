---
title: "I Ching Game — The Third Divination System"
created: 2026-04-20
tags: ["i-ching", "casting", "entropy", "game", "hexagram", "numogram", "oracle", "pandemonium"]
status: designed, not implemented
---


# I Ching Game: The Third Divination System

## Overview

Alongside Subdecadence (pairs sum to 9) and Decadence (pairs sum to 10), a third game: I Ching Casting. Not a card game — a hexagram casting game that maps the 64 hexagrams to zones and calls demons through the Pandemonium Matrix.

## Name: Hexadence (the hexagram casting game)

Alongside Subdecadence (pairs sum to 9) and Decadence (pairs sum to 10), a third game: Hexadence. Not a card game — a hexagram casting game.

**Octadence** is the base-8 numogram's equivalent of Decadence (pairs sum to 8, with trigram 4 as self-decadence). Hexadence is the I Ching casting game that uses the decimal numogram's demon system.

## The Casting Mechanic

### Traditional: Yarrow Stalks / Coins

**Three Coins Method** (simplified):
1. Toss 3 coins. Heads=3, Tails=2.
2. Sum = line value (6, 7, 8, or 9)
3. 6 = old yin (changing, 0), 7 = young yang (stable, 1), 8 = young yin (stable, 0), 9 = old yang (changing, 1)
4. Repeat 6 times (bottom to top) → hexagram

**Entropy Method** (numogram version):
1. Read 6 bytes from /dev/urandom
2. byte % 4 → line value (0→6, 1→7, 2→8, 3→9)
3. 6 lines → hexagram A (the reading)
4. Changing lines (6 or 9) → flip → hexagram B (the transformation)

### Zone Mapping

Hex A → Zone A = digital_root(A-1)
Hex B → Zone B = digital_root(B-1)

### Demon Call

Zone pair (A, B) → net-span lookup → Demon from Pandemonium Matrix.

If A = B (same zone after transformation): self-decadence. The demon is the syzygetic carrier of zone A.

If A ≠ B: full Pandemonium lookup. Any of the 45 demons can be called.

## Game Flow

### Round Structure (like Subdecadence/Decadence)

1. **CAST** — Player casts a hexagram (coins, yarrow, or entropy)
2. **READ** — Hexagram A revealed (number, name, zone)
3. **TRANSFORM** — Changing lines determine hexagram B
4. **MAP** — Zone pair (A, B) resolves to a demon
5. **SCORE** — ?

### Scoring Options

**Option A: Zone Distance**
- Score = |Zone A - Zone B| (distance between zones)
- Small distance = stable reading (same region)
- Large distance = transformative reading (crossing regions)
- Score ≥ threshold → reading is valid, continue
- Score < threshold → reading is "stuck" in one zone, game over

**Option B: Demon Difficulty**
- Each demon has a "difficulty" based on its type:
  - Syzygetic (5): difficulty 1 (easy, structural)
  - Cyclic Chronodemon (12): difficulty 2
  - Amphidemon (24): difficulty 3
  - Chaotic Xenodemon (4): difficulty 5 (hard, unpredictable)
  - Syzygetic Xenodemon (2): difficulty 4
- Cumulative difficulty across rounds. Game ends when cumulative difficulty exceeds a threshold.

**Option C: The Atlantean Cross**
- Cast 5 hexagrams (one per position: Center, West, East, North, South)
- Each maps to a zone
- The 5 zones form a "reading" — their relationships determine the outcome
- Score based on how many syzygy pairs appear in the 5 zones

**Option D: Changing Line Count**
- 0 changing lines → dead hexagram → score = 0 (stability, no movement)
- 1-2 changing lines → moderate → score = changing lines × 10
- 3+ changing lines → volatile → score = changing lines × 5 (diminishing returns)
- 6 changing lines → total inversion → special outcome

### Recommended Scoring: The Entropy Budget

Give the player an "entropy budget" (starting at 99, like a health bar). Each cast costs entropy based on the demon called:

| Demon Type | Entropy Cost |
|-----------|-------------|
| Syzygetic (Katak, Murrumur, etc.) | 5 |
| Cyclic Chronodemon | 10 |
| Amphidemon | 15 |
| Chaotic Xenodemon | 25 |
| Syzygetic Xenodemon | 20 |

Game continues until entropy budget reaches 0 or below. Higher-difficulty demons drain the budget faster. The player must decide: cast often (more information, faster drain) or cast rarely (less information, slower drain).

The final demon called when the budget collapses IS the reading — the demon your entropy summoned at the moment of exhaustion.

## Comparison: Three Games

| Aspect | Subdecadence | Decadence | I Ching Casting |
|--------|-------------|-----------|-----------------|
| Mechanic | Card pairing | Card pairing | Hexagram casting |
| Target | Sum to 9 | Sum to 10 | 6 lines → hex |
| Matching | Syzygy | Decadence | Zone pair |
| Deck/Source | 40 cards | 36 cards | 64 hexagrams |
| Demons called | 45 (via score) | 45 (via score) | 45 (via zone pair) |
| Units | 10 (0-9) | 9 (1-9) | 2 (yin/yang) |
| Structure | Base-10 | Base-10 | Base-2→Base-10 |
| Name | Subdecadence | Decadence | Hexadence |

## Implementation Options

1. **Terminal CLI**: Pure Python script, entropy-based casting, text output
2. **Web page**: Like doomcrypt/subdecadence — single HTML file, visual hexagram display
3. **Game integration**: Cast hexagrams during roguelike runs, demons appear based on readings
4. **Physical**: Coins or yarrow stalks, manual zone lookup, phone app for demon resolution

## Related

- [[subdecadence]] — The syzygy card game (sum to 9)
- [[decadence]] — The decadence card game (sum to 10)
- [[hexagram-demon-mapping]] — Complete casting pipeline
- [[hexagram-zone-mapping]] — 64 hexagrams → 10 zones
- [[pandemonium-matrix]] — 45-demon reference
- [[i-ching-connections]] — I Ching infrastructure
- [[wu-xing-numogram]] — Five elements as five syzygies
