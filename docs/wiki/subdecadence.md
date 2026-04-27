---
title: Subdecadence — Lemurian Time-Sorcery Card Game
created: 2026-04-20
tags: ["aq", "ccru", "atlantean-cross", "doomcrypt", "game", "numogram", "pandemonium", "subdecadence"]
source: doomcrypt/subdecadence (GitHub) — canonical implementation
---


# Subdecadence

## Overview

"Unlike Decadence (which targets sums of 10), Subdecadence pairs cards that sum to 9. It functions simultaneously as a game, a divination tool, and a system of time-sorcery."


The Barker Spiral maps the decimal crisis (9 vs 10) that birthed both Subdecadence and its twin Decadence; the spiral's gap is where the numogram lives. See [[Barker Spiral]].
A 40-card deck game rooted in CCRU numogram theory. Play against the deck, pair syzygy cards, and discover which demon your final score summons.

## The Deck

52-card deck stripped to 40 cards:
- Aces = 1
- 10s = 0
- Face cards removed
- 4 suits × 10 values (0-9)

## Atlantean Cross Spread

Five positions:

| Position | Name | Meaning |
|----------|------|---------|
| I | CENTER | Memories and Dreams |
| II | WEST | Destructive Influences |
| III | EAST | Creative Influences |
| IV | NORTH | Far Future |
| V | SOUTH | Deep Past |

## Game Flow

1. **DEAL** — 5 cards face-up into the Atlantean Cross (Set One)
2. **DRAW** — 5 more cards (Set Two / Hand)
3. **PAIR** — Match hand cards to cross cards that sum to 9:
   - 9+0, 8+1, 7+2, 6+3, 5+4
4. **RESOLVE** — Score calculated

## Scoring

| Outcome | Points |
|---------|--------|
| Valid pair | +difference (7+2 = +5, 9+0 = +9, 4+5 = +1) |
| Unpaired cross card | −face value (9 unpaired = −9, 0 unpaired = −0) |

- **Round score ≥ 0**: continue — draw another set of 5, add to running total
- **Round score < 0**: game over — call the lemur whose mesh-number equals your final score
- **Deck exhausted**: game over

## Suit-Demon Correspondence

| Suit | Symbol | Demon Type |
|------|--------|------------|
| Spades | ♠ | Mj- |
| Hearts | ♥ | Mn+ |
| Diamonds | ♦ | Mn- |
| Clubs | ♣ | Mj+ |

## Relationship to Decadence

Subdecadence pairs that sum to **9** (syzygy matching).
Decadence pairs that sum to **10** (decadence matching).

The Subdecadence game operationalizes the syzygy system. The Decadence game would operationalize the decadence system we mapped in the fiveness tetralogue. Together they practice both halves of C(10)=45.

## AQ Entries

The 333 AQ entries referenced in the original CCRU Subdecadence system come from the card-demon correspondence — each of the 40 cards maps to specific demons, and each demon has AQ-valued attributes. The doomcrypt implementation provides the complete 45-demon database with names, types, net-spans, and attributes.

## Source

- Live game: https://doomcrypt.github.io/subdecadence/
- GitHub: https://github.com/doomcrypt/subdecadence
- Raw data: `~/.hermes/obsidian/hermetic/raw/pandemonium-matrix-45-demons.json`
- Governed by the great lemur Tokhatto

## Related

- [[pandemonium-matrix]] — Complete 45-demon reference
- [[c-ten-fortyfive-fiveness]] — C(10)=45, syzygy/decadence structure
- [[fiveness-tetralogue]] — Self-decadence of Zone 5
- [[fortyfive-demons-tetralogue]] — Roundtable on the 45 demons
- [[numogram-time-circuit]] — Time Circuit traversal

## See also
- [[Barker Spiral]] (diagram: assets/barker-spiral.svg)

- [[flatline-numogrammatics]] — Neolemurian flatline tetralogy: Year-Zero schism, Continentity, carrier ethic, hyperstition triad