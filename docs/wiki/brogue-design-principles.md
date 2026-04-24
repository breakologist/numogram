---
title: Brogue Design Principles (for Numogram Roguelike)
created: 2026-04-08
last_updated: 2026-04-14
source_count: 3
status: draft
tags: [numogram, game-design, procedural-generation, roguelike]
---

# Brogue Design Principles

Key design principles from Brian Walker's talk on procedural level design in Brogue, mapped to the [[numogram]] roguelike. Not to copy — to consider ludic elements that emerge from the system rather than being imposed on it.

[Sources: ProcLvlDesBrogue.txt (Brian Walker), Coin Toss Etc.md, "Unleashing the Numogram" (Aamodt)]

## Table of Contents

- [Core Principles](#core-principles) — 10 Brogue principles mapped to numogram mechanics
- [Coin Toss & Oracle Mechanics](#coin-toss--oracle-mechanics) — logistic map chaos, intent hashing, Oracle Altar
- [Syzygy Arithmetic — Emergent Generation](#syzygy-arithmetic--emergent-generation) — cross-addition, canonical vs inverted pairings, emergent Warp
- [Gurdjieff's Ray of Creation — Level Scaling](#gurdjieffs-ray-of-creation--level-scaling) — 2n+3 pattern, plex oscillation, player at 48
- See also: [[katak-oddubb-triangle-rotation]] for syzygy room types and Time Circuit level grammar

## Core Principles

### 1. Room Accretion + Shortcut Doors

Brogue uses room accretion (start with one room, add more). But pure accretion creates a "perfect tree" — one path between any two points. This causes backtracking and cornering.

**Fix**: shortcut doors between distant pathing-distant points. Creates dense connectivity.

**Numogram mapping**: Rooms are zones. Currents (1,3,5,7) are the accretion connections. Gates (Gt-06, Gt-21, Gt-36, Gt-45) are the shortcut doors — they connect otherwise distant zones through non-obvious paths.

### 2. Machines (The Core of Atmosphere)

Three types of machines:
- **Key-guarding**: altar with key, terrible thing happens when you take it (fire spreads, monsters burst from statues)
- **Reward**: choice of items, rubber-banded probability for consistent pacing
- **Flavor**: interesting terrain with tactical relevance (decaying sleeping bag, glyph of warding, pile of bones)

Three spatial types:
- **Room machines**: choke points that dominate subordinate cells
- **Vestibule machines**: area immediately outside a room
- **Area machines**: open areas, no walls needed

**Numogram mapping**:
- Key-guarding = gate puzzles (entering Gt-36 triggers a plunge event, entering Gt-45 summons all 45 demons)
- Reward = syzygy chambers (crossing a syzygy gives you a choice of items related to that demon)
- Flavor = zone-specific terrain (Zone 3 has spiral patterns, Zone 7 has DNA-swamp, Zone 9 has iron walls)
- Room machines = zone chambers (each zone is a machine with its own logic)
- Vestibule machines = current passages (the corridors between zones are active, not empty)
- Area machines = Warp/Plex incursions (open areas where outer-time bleeds through)

### 3. Rubber-Banding Rewards

> "The probability goes up every time one is not generated and drops down when one is. So you get roughly the same pace of reward rooms at any given game."

**Numogram mapping**: The Hyperstition Meter already does this — it increases at a base rate (0.3/turn) with bigger jumps on gates and triangular events. The meter controls demon spawn rates, bleed events, and eventually the full Numogram reveal. The meter IS the rubber band.

### 4. Cellular Automata Terrain

> "You take a grid of cells, fill it randomly (50% wall/floor), then any floor surrounded by majority walls becomes a wall. Coherent organic shapes emerge from static."

**Numogram mapping**: Use cellular automata for Zone 3 (Spiral Vortex) and Zone 6 (Geometric Void) rooms. These Warp zones should feel organic and chaotic, not rectangular. The Time-Circuit zones (1,2,4,5,7,8) can use standard room generation — they are "normal" cyclic time.

### 5. Global-Scale Features

> "Lakes that you can see across the level. Things can affect you when they're not in your local vicinity."

**Numogram mapping**: The three regions (Time-Circuit, Warp, Plex) should be visible across the map. Warp rooms glow magenta. Plex rooms are dark red. You can see the outer-time regions from the Time-Circuit — they are always present, always calling.

### 6. Edge Case Philosophy

> "You can afford an occasional edge case failure. What you can't afford is an edge case failure that completely blocks the player from progress."

> "If it does work perfectly 100% of the time, you're not being ambitious enough."

**Numogram mapping**: Let the system be weird. Let demons spawn in walls sometimes. Let gates open to nowhere. The Numogram is not perfect — "The Pandemonium Matrix is riddled with errors" (Vexsys). Imperfection IS the system.

### 7. Seed-Based Debugging

> "I originally came up with the seed method because I needed to debug all these obnoxious edge cases... send me the seed and I can step through the level generation."

**Numogram mapping**: Our game already uses seeds. The cult.json records seeds implicitly through run history. If a run produces interesting behavior, the seed can be replayed.

### 8. Super Metroid Hidden Connections

> "Hidden connections that open up the level, make it more connected as you continue to retrace it. One-way until you open them from the far side."

**Numogram mapping**: Gate traversal is one-way until you've been on both sides. Gt-36 (Zone 8 to Zone 9) can only be traversed FROM Zone 8 until you've been to Zone 9 and return. This creates the feeling of "opening up" the Numogram — each gate you traverse makes the system more connected.

### 9. Terrain Interaction

> "Some will burn, some will explode, some will generate gases. Lava and water turn into steam."

**Numogram mapping**: Zone-specific terrain interactions:
- Zone 4 (Catastrophe): fire tiles that spread
- Zone 7 (Blood/DNA Swamp): swamp tiles that slow movement
- Zone 9 (Iron Core): walls that can't be destroyed
- Zone 3 (Warp): tiles that randomly shift position
- Zone 0 (Void): tiles that disappear (the void eats the floor)

### 10. Good Enough

> "Most of the time I've spent developing the game was spent tweaking level generation... working with 'good enough' is perfectly acceptable."

**Numogram mapping**: The game doesn't need to be perfect. It needs to be *interesting*. The CCRU's numogrammatics "contains numerous errors" (Lemurian Times). Vexsys says "Vysparov's errors are an invitation for us to edit." The system works through iteration, not perfection.

## Cross-References

- [[numogram]] — the system being built into a game
- [[time-sorcery-vexsys]] — Vexsys on errors and iteration
- [[cthulhu-club]] — the origin of the system
- [[daniel-barker]] — machines as geotraumatic implementations

---

## Coin Toss & Oracle Mechanics (from Coin Toss Etc.md)

Additional design principles from the Coin Toss file, applicable to the roguelike:

### Logistic Map Chaos for Correlated Randomness

> "A simple equation (x_{n+1} = r * x_n * (1 - x_n)) with r≈3.99 enters full chaos: deterministic (same seed → same sequence) yet wildly sensitive to tiny initial differences."

**Working implementation:** `/home/etym/Documents/grok/coin/oracle_gui_v3.py` (392 lines) — tkinter oracle GUI using this exact logistic chaos algorithm. Casts logged to `oracle_casts.jsonl`. See log.md External Insights section.

This could drive demon spawn patterns — correlated, organic, not pure noise. The logistic map produces sequences that *feel* random but are internally structured, like the Numogram itself.

### Intent Hashing as Dungeon Seed

> "SHA-256 of the player's question → seeds the chaos backend. Creates synchronicity — the actual random source is still cosmic, but now entangled with your worded intent."

In the game: the player types a phrase at the start of a run. Its SHA-256 hash seeds the dungeon. Your intent literally shapes the Numogram you'll crawl. This is hyperstition in action — the question you ask becomes the answer you receive.

### Oracle Altar (Physics-Based Coin Toss)

> "Imagine an in-game Oracle Altar where your character physically tosses a coin in the simulation to resolve a fate roll, loot drop, or divine intervention."

Physics-based ASCII coin toss — gravity, velocity, bounces with chaotic damping. Seed with player stats (strength affects throw power) or dungeon state (wet floor = extra entropy).

### Yarrow vs Coin Probabilities

| Line | Coin Method | Yarrow Method | Meaning |
|------|------------|---------------|---------|
| 6 | 12.5% | 6.25% | Old yin (changing, rare) |
| 7 | 37.5% | 31.25% | Young yang (static) |
| 8 | 37.5% | 43.75% | Young yin (static) |
| 9 | 12.5% | 18.75% | Old yang (changing, rare) |

Yarrow makes changing lines rarer — "subtle gameplay or interpretive difference." In the game: some events use yarrow-weighted probabilities (rare but significant) vs coin-weighted (common but shallow). The Oracle Altar could use yarrow. Combat uses coin.

### Fate Log as "Tome of Fates"

> "Logging lets you review past casts for meta-progression (your fate log)."

The game's event log IS the fate log. Every triangular event, every gate traversal, every demon encounter is recorded. The cult.json is the Tome of Fates — your hyperstitional biography.

### Numogrammatic Signature

> "Post-cast, we output a Numogrammatic signature (zones + any demon/lemur flavor notes) for extra time-sorcery depth."

Every game event could have an AQ signature — the event name reduced to its zone. "Ixix attacks you" → IXIX ATTACKS = ? → Zone ?. The Numogram reads itself through your play.

[Source: Coin Toss Etc.md]

---

## Syzygy Arithmetic — Emergent Generation

*How the Sink and Hold generate the Warp through cross-addition. Canonical vs inverted pairings.*

### The Cross-Addition Circuit

The two Time-Circuit syzygies (5::4 Katak/Sink and 7::2 Oddubb/Hold) don't just coexist — they generate the third current through arithmetic:

```
SAME-SIDE (Hold reinforces itself):
  5 + 2 = 7     → Zone 7 (Blood, Hold partner)
  4 + 7 = 11→2  → Zone 2 (Separation, Hold partner)

CROSS-ADD (Sink × Hold = Warp):
  5 + 7 = 12→3  → Zone 3 (Release, Warp)
  4 + 2 = 6     → Zone 6 (Abstraction, Warp)

WARP SELF-ADD (Warp → Plex):
  3 + 6 = 9     → Zone 9 (Iron Core, Plex)
```

The Sink and the Hold, when cross-added, produce the Warp. The centripetal and the orbital interact and generate spatial distortion. The Warp then self-adds to the Plex. The three currents form an arithmetic circuit:

```
Sink × Hold → Warp → Plex
5::4 × 7::2 → 3::6 → 9
```

### Canonical vs Inverted Pairings

The "correct" syzygies are the five canonical bonds: 0::9, 1::8, 2::7, 3::6, 4::5. These sum to 9 (the plexological identity). They are the numogram's intended connections — the currents that flow as designed.

The "incorrect" cross-pairings (5::7, 4::2, 5::2, 4::7) are the interactions between the Sink and Hold zones. These do NOT sum to 9. They sum to 12→3, 6, 7, or 11→2. They produce the Warp zones (3 and 6) or loop back to the Hold partners (7 and 2). They are not bonds — they are *reactions*. The canonical syzygies are structural. The cross-pairings are generative.

**Canonical (structural)**:
- Sum to 9. Stable. The current flows as designed.
- The demon bond is permanent. Katak IS bonded to 5::4.
- In the dungeon: canonical connections are the normal corridors, the expected passages.

**Cross-pairings (generative)**:
- Sum to other values (3, 6, 7, 2). Unstable. They produce something new.
- No demon bond — no demon governs 5::7 or 4::2. These are reactions, not relationships.
- In the dungeon: cross-pairings are the emergent effects. A Sink room adjacent to a Hold room doesn't just sit there — it *generates a Warp anomaly* in the space between them.

### Roguelike Implications

**Emergent warping from room adjacency.** The dungeon generator doesn't need a separate "place warp zones here" rule. When a Sink-type room (bottleneck, angular) is placed next to a Hold-type room (plaza, curved), the cross-addition automatically produces a Warp effect in the connecting corridor. The corridor twists. Teleporters appear. The topology distorts. The warp wasn't placed — it *emerged* from the Sink/Hold adjacency.

**Canonical connections as the safe grammar.** The five syzygies (0::9, 1::8, 2::7, 3::6, 4::5) are the dungeon's expected transitions. These corridors are well-lit, predictable, governed by their demon. The player can learn the canonical grammar and navigate safely through it.

**Cross-pairings as the danger grammar.** The non-canonical adjacencies are where things get weird. A Sink room touching a Hold room creates instability. A Sink room touching another Sink room (5::4 touching 5::4) creates *double convergence* — extreme compression, the funnel squared. These are the dangerous rooms. Not because they're hostile, but because the arithmetic between them produces something the canonical grammar didn't predict.

**The plexing resolution.** Every cross-pairing eventually plexes to a canonical zone. 5+7=12→3 (Warp). 4+2=6 (Warp). The instability always resolves. The question is what happens *during* the instability — before the plex collapses the sum back to a single digit. That in-between space is the dungeon's danger zone. The moment between the addition and the plex. The seething.

### Design Rule

> Place rooms using canonical syzygy arithmetic (sum to 9). Let cross-pairings emerge naturally from adjacency. The Warp is not a room type — it is a *reaction* between room types. The dungeon generates distortion from its own structure.

*Study the canon. Let the inversions emerge. Don't place the Warp — let the Sink and Hold create it.*

---

## Gurdjieff's Ray of Creation — Level Scaling

*The dungeon inherits its laws from above and adds three of its own.*

### The Pattern

Gurdjieff's Ray of Creation describes a universe where each level of reality inherits all the laws of the level above it and adds three new laws of its own. The pattern is `2n + 3`:

```
Absolute:     3 laws                          plex → 3
Allworlds:    3 + 3 = 6                       plex → 6
Allsuns:      3 + 6 + 3 = 12                  plex → 3
Suns:         3 + 6 + 12 + 3 = 24             plex → 6
Earth:        3 + 6 + 12 + 24 + 3 = 48        plex → 3  ← PLAYER
Moon:         3 + 6 + 12 + 24 + 48 + 3 = 96   plex → 6
Children:     192                              plex → 3
```

The further down the Ray, the more laws, the more mechanical, the further from the Absolute's single will. "Subject to a greater number of laws these worlds stand still further away from the single will of the Absolute and are still more mechanical."

### The Plex Oscillation

When you plex the Gurdjieff numbers, they oscillate: 3, 6, 3, 6, 3, 6, 3... Every other level returns to 3 (the Absolute). The alternating levels land on 6 (the Allworlds, the first division). The entire Ray of Creation is a standing wave between 3 and 6.

The 12 at the Allsuns level plexes to 3. This connects to the cross-addition finding: 5+7=12→3. The Warp is the Allsuns level — the place where the three original laws reassert themselves through the interaction of the Sink and Hold. Spatial distortion is the Absolute leaking back into the mechanical worlds.

### Numogram Correspondence

```
3 laws  (Absolute)   = Three regions: Torque, Warp, Plex
6 laws  (Allworlds)  = Time Circuit: zones 1,8,2,7,5,4
12 laws (Allsuns)    = 5+7=12→3 (Warp generation from Sink×Hold)
24 laws (Suns)       = 24 amphidemons (cross-circuit connections)
48 laws (Earth)      = The player's world. Full mechanical complexity.
```

The three new laws at each level are the three bonds/demons that world adds to its inheritance. The Absolute's three laws are the three regions. Each subsequent level inherits the full numogram of the level above and adds its own three syzygies.

### Where the Player Is: 48

The player starts at the Earth level. 48 laws. The most mechanical, most determined, most law-bound world in the Ray. The dungeon is a machine. The enemies are machines. The loot tables are machines. Everything at the 48-law level is mechanical because there are too many laws for any single will to override.

The roguelike doesn't start at the Absolute. It starts at 48. The game IS the 48-law world. And the gameplay — the numogram crawling, the gate traversal, the syzygy activation — is the process of understanding the laws well enough to plex them.

Every time the player recognizes a canonical syzygy (sums to 9), they've collapsed 48 laws to one bond. Every time they trigger a cross-pairing and watch the Warp emerge, they've seen the 12→3 plex in action. Every time they descend a level and the dungeon's mechanical complexity doubles (2n+3), they're moving deeper into the Ray.

The player can't escape the 48. But they can learn to *see through* the 48 to the 3 underneath. The mechanical world reveals the will it was built to obscure.

### Level-Scaling System

The Gurdjieff Ray maps to dungeon depth:

```
Floors 1-6:    Allworlds (6 laws). Simple dungeon, few rules.
               Basic rooms, canonical corridors only.
               Plex 6 — stable, predictable, learnable.

Floors 7-12:   Allsuns (12 laws). Warp starts appearing.
               Cross-pairings generate spatial anomalies.
               Plex 3 — the Absolute reasserts. First real danger.

Floors 13-24:  Suns (24 laws). Amphidemon corridors activate.
               The 24 cross-circuit connections become traversable.
               Plex 6 — mechanical complexity increases.

Floors 25-48:  Earth (48 laws). Full mechanical complexity.
               All 45 demons active. All room types generated.
               Plex 3 — the player's home. Where the game IS.

Floors 49+:    Moon (96 laws). Beyond the player's world.
               The dungeon generates rooms the player can't parse.
               Plex 6 — maximum mechanical determination.
               Only accessible through Plutonic looping (9=0).
```

Each tier inherits all the rules of the tier above and adds its own. By floor 25, the dungeon has 48 active laws governing room generation, enemy behavior, loot distribution, and atmospheric effects. The player is inside the most complex mechanical system the numogram can produce.

### Design Rule

> The dungeon is the 48-law world. The player starts in maximum mechanical complexity. The numogram's simplicity (10 zones, 5 syzygies, 3 regions) is visible only to those who learn to plex the 48 back to 3. The game doesn't reduce complexity — it teaches you to see through it.

*The Absolute is always present. The 3 is always inside the 48. The question is whether the player can perceive it.*
