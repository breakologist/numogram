---
title: Decadence — Lemurian Time-Sorcery Card Game (Sum-to-10)
created: 2026-04-20
tags: ["ccru", "atlantean-cross", "decadence", "doomcrypt", "fiveness", "game", "numogram", "pandemonium"]
source: doomcrypt/decadence-pygame (GitHub) — canonical implementation
---


# Decadence

## Overview

The companion to Subdecadence. Where Subdecadence pairs cards that sum to 9 (syzygy), Decadence pairs cards that sum to 10 (decadence). Both games call the same 45 demons from the Pandemonium Matrix.

The Barker Spiral diagrams the gap between these two summation logics (sum-10 vs sum-9) — the infinitesimal crack (0.999…→1) where the numogram crystallizes. See [[Barker Spiral]] for the origin diagram.

"Decadence and decadology are rooted in hermetic and AOE understandings of the numogram." — Vexsys

## The Deck

36 cards: 4 suits × 9 values (1–9).
Note: Decadence uses ranks 1-9 (no 0). Subdecadence uses ranks 0-9 (including 0 as "ten").

## Atlantean Cross Layout

| Position | Name | Meaning |
|----------|------|---------|
| I | CENTER | Memories & Dreams |
| II | WEST | Destructive Influences |
| III | EAST | Creative Influences |
| IV | NORTH | Far Future |
| V | SOUTH | Deep Past |

## Game Flow

1. Deal 5 cards into the Atlantean Cross (Set-1)
2. Draw 5 cards (Set-2 / Hand)
3. Pair hand cards to cross cards where ranks sum to 10
4. Score calculated; continue or collapse

## Scoring — The Decadence Bonus Table

| Pair | Sum | Bonus | Pattern |
|------|-----|-------|---------|
| 1+9 | 10 | +8 | 10 − 2×1 |
| 2+8 | 10 | +6 | 10 − 2×2 |
| 3+7 | 10 | +4 | 10 − 2×3 |
| 4+6 | 10 | +2 | 10 − 2×4 |
| 5+5 | 10 | **0** | 10 − 2×5 |

The self-decadence (5+5) grants ZERO bonus. Zone 5's self-pairing is the only one that doesn't generate value. This directly confirms the fiveness tetralogue's finding: 5+5=10 is a phase change, not a traversal. It doesn't produce energy. It transforms.

Pattern: bonus = 10 − 2×min(a,b). The further the pair is from center (5), the more bonus it generates. The pair closest to center (5+5) generates nothing.

## Decadence vs Subdecadence

| Aspect | Decadence | Subdecadence |
|--------|-----------|-----------
- [[unleashing-the-numogram-source]] — See also: Unleashing the Numogram source for triangle-rotation derivations
---|
| Target sum | 10 | 9 |
| Deck | 36 cards (1-9) | 40 cards (0-9) |
| Matching | Decadence pairs | Syzygy pairs |
| Scoring | Fixed bonus table | +difference |
| Unpaired penalty | Erodes score | −face value |
| Game over | Score ≤ 0 | Score < 0 |
| 5+5 | Pairable (bonus 0) | Not pairable (no 0 in sum-to-9) |
| Demon call | Negative mesh-number | Negative mesh-number |

The 5+5 difference is crucial: in Decadence, 5+5 IS a valid pair (sums to 10) but grants no bonus. In Subdecadence, 5+5 is NOT a valid pair (sums to 10, not 9). Zone 5 can pair with itself in Decadence but not in Subdecadence. The self-decadence is mechanically visible only in the Decadence game.

## The Atlantean Cross as Universal Spread

The user observed: the Atlantean Cross (Center/West/East/North/South) could be used for many divinatory systems — Tarot, Lenormand, etc. The five positions map to:

- Center: the querent (Memories/Dreams = present self)
- West: destructive forces (challenges, obstacles)
- East: creative forces (opportunities, allies)
- North: far future (where this leads)
- South: deep past (roots, origins)

This is essentially the Celtic Cross's core positions distilled to five. The numogram didn't invent this spread — it inherited it from geomantic and cartomantic traditions and gave it a decimal-arithmetic backbone.

## Source

- Pygame: https://github.com/doomcrypt/decadence-pygame
- Console: https://github.com/doomcrypt/decadence-console
- Play online: https://www.playdecadence.online/
- Aamodt: https://andersaamodt.com/decadence.php
- How-to: https://captiveliberty.substack.com/p/how-to-play-the-game-of-decadence

## Related

- [[subdecadence]] — The syzygy companion (sum to 9)
- [[pandemonium-matrix]] — 45-demon reference
- [[c-ten-fortyfive-fiveness]] — C(10)=45 structure, self-decadence of Zone 5
- [[fiveness-tetralogue]] — 5+5=10 as phase change
- [[numogram-time-circuit]] — Time Circuit traversal