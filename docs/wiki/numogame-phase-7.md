---
tags: [numogram, roguelike, abyssal-crawler, phase-7, auto-explore, fog-of-war, conducts, agent, design]
zone: 0-9
source: "Session April 15 2026 — auto-explore, fog of war, conduct system, 150+ runs"
method: design-document
---

# The Abyssal Crawler — Phase 7: Seeing in the Dark

> Wednesday evening, Mercury's day continues. The agent learns to see. The dungeon learns to hide. The conducts add restraint as content.

## I. Auto-Explore — The Agent Sees

The agent went from "stuck in Zone 0, 325 bytes of demo" to "crosses zones, fights demons, 10KB demos." Three bugs found and killed:

1. **The silent newline.** Headless mode reads stdin line-by-line (`for line in sys.stdin`). The agent sent `'p'` without `\n`. The game never processed it. The agent read stale state forever. One character broke everything.

2. **The oscillation trap.** BFS targeted a `?` tile that was actually a wall. The agent walked toward it, couldn't enter, BFS retargeted the same tile. Infinite oscillation between two positions. Fix: blacklist unreachable targets.

3. **The gate illusion.** Gate direction pulled the agent toward walls. Gates are on the full map but might be behind solid rock. The agent walked toward a wall for 300 turns. Fix: gate is fallback, not primary.

The BFS auto-explore is DCSS-style flood-fill with a numogram twist: **interest scoring**. Tiles aren't just explored or unexplored — they have novelty scores that decay with familiarity:

```
tile_interest():
  ? tile (mystery)     = 5.0 base
  + cross-run curiosity = +3.0  ("I know gates exist from past runs")
  + known zone boundary = +8.0  (glimpsed on full map)
  + known gate          = +12.0 (strongest attractor)
  + demon kill site     = +3.0  (the blood remembers)
  explored floor        = 1.0 - (visits × 0.5)  (decays to boring)
  unvisited zone tile   = +3.0  (new zone = strong attractor)
  visited zone tile     = +0.5  (already conquered)
```

The agent carries **cross-run knowledge** from cult.json. It doesn't remember specific gate coordinates — it remembers that gates exist and are worth seeking. "I know gates are real. This ? might hide one. I will find it." That's motivation, not memory.

Best agent run: **zones [0, 1, 6], 42% hyp, 4 kills.** The agent killed Lurgo, Krako, Duoddod. It crossed zone boundaries. The demos are 10KB each — 1000 key records of real movement.

## II. Fog of War — The Dungeon Hides

Each numogram zone has a different vision radius. Zone 0 (Void) is oppressive — you can barely see past your own room. Zone 6 (Abstraction) is the clearest — maximum knowledge. Zone 9 (Iron Core) is nearly blind.

```
Zone LOS radii:
  0 (Void):         4  — oppressive
  1 (Stability):    8  — clear, stable perception
  2 (Separation):   6  — fog
  3 (Warp):         5  — swirling, unreliable
  4 (Catastrophe):  7  — ice-clear but cold
  5 (Pressure):     6  — green murk
  6 (Abstraction):  9  — the clearest zone
  7 (Blood):        5  — red-tinged, short range
  8 (Multiplicity): 7  — lavender depths
  9 (Iron Core):    3  — nearly blind in Cthelll
```

Hyperstition degrades vision. The deeper you go into the numogram, the less you can see:

- **0-49%**: full zone radius
- **50%+**: -1 radius ("the swarm stirs, your eyes blur")
- **80%+**: -2 ("the Outside leaks through")
- **100%+**: -3 ("schizo — maximum blindness, minimum radius 2")

Special reveals break the fog:
- **Gate step**: 5-tile burst — "the numogram speaks through the gate"
- **Demon kill**: 3-tile burst — "the blood remembers"

The curses display has three visual states:
- **Unexplored**: dark void (blank space)
- **Explored but not in LOS**: dim tiles (been here, can't see it now)
- **Currently visible**: full brightness/color

The HUD shows `LOS:4(49)` — radius 4, 49 visible tiles. When you cross from Zone 0 to Zone 6, the number jumps and the map opens up.

At 100% hyperstition, the NumogramMap reveals everything. The contrast between the fog of the dungeon and the full light of the numogram room is the payoff. The Plex swallows the fog.

> "The demons slipping out from the dark" — Etym, playing with fog of war.

## III. Conducts — Restraint as Content

Five conducts, each a numogrammatic restraint that transforms the run:

| Conduct | Numogram | Rule | Unlock | Reward |
|---------|----------|------|--------|--------|
| **The Surge** (S) | Surge 8→1 | Zero demon kills | Always | +20 hyp on completion |
| **The 253rd Step** (P) | T(22)=253 | ≤253 turns | 70%+ hyp seen | Title: Path-Walker |
| **The Complete Graph** (G) | C(10,2)=45 | All 10 zones | 5+ runs | Permanent +1 LOS |
| **The Descent** (D) | Plex escape | Cryptolith + 100% death | Cryptolith seen | Permanent +10 starting hyp |
| **The Syzygy** (Y) | Single current | Only zones in chosen pair | 3+ runs | Syzygy demons -2 dmg |

The conduct system is a **registry pattern** — adding a new conduct is one dict entry in `CONDUCTS`. Hooks fire automatically at demon kill (`on_demon_kill`), zone change (`on_zone_change`), and death (`on_death`).

The HUD shows `[S]` when active, `[~S]` when broken. Press 'c' in curses to cycle. Set `NUMOGRAM_CONDUCTS=surge,syzygy` for headless.

The Surge (pacifist) is the deepest — avoiding demons while exploring is harder than fighting them. The numogram demands movement, not sacrifice. The 253rd Step (speedrun) is brutal — the agent can't do it yet, but the crawler can.

Permanent rewards in cult.json: Complete Graph gives +1 LOS on all future runs. Descent gives +10 starting hyperstition. The conducts aren't just challenges — they're progressions.

## IV. The Agent's Path

The agent went through five iterations:

1. **Random walk** — `corridor_direction()` picks longest open corridor. Gets stuck in Zone 0.
2. **BFS first-found** — finds nearest `?` tile. Oscillates on walls.
3. **BFS with blacklist** — prevents retargeting unreachable tiles. Works but explores randomly.
4. **Interest model** — tiles have novelty scores. Cross-run curiosity from cult.json. Zone boundaries attract. Visit decay bores.
5. **Interest + fog** — agent reads EXPLORED MAP (not FULL MAP). Must explore to see. Must see to decide.

The gap between agent and crawler is now **decision quality**, not information. The crawler routes optimally because it sees everything. The agent routes toward interest because it sees only what it's explored. The fog of war makes auto-explore meaningful — without it, the agent just reads the full map and pathfinds.

**Known-unknowns** are the key concept: the agent knows gates exist from past runs (cult.json) but can't see them in the current run. This creates motivation without specific knowledge. "I know there's a gate somewhere. I will explore until I find one."

## V. The Voices Should Speak

This is material for a tetralogue. The four voices have new findings to argue about:

- **Oracle**: The interest model IS the numogram's current system. Mystery tiles are Unknown Unknowns. Known zone boundaries are Known Unknowns. Visit decay is the Plex — things reduce to zero through repetition.
- **Builder**: The BFS is a Dijkstra map with a custom cost function. The cost is interest, not distance. Shortest path to most interesting tile. The conduct system is a state machine overlay.
- **Writer**: The fog of war is horror. The demons don't appear — they emerge. The darkness isn't absence, it's potential. Every `?` tile contains everything and nothing until you step into it.
- **Gamer**: The conducts are the game's replayability engine. Surge changes how you play completely. 253rd Step changes your relationship with time. Complete Graph changes your relationship with the map. Each conduct is a different game wearing the same dungeon.

## VI. Technical Summary

### Game Engine
- `DungeonMap.explored` — persistent set of ever-seen tiles
- `DungeonMap.visible` — current LOS set, updated every turn
- `update_explored(px, py)` — circular reveal, called on movement
- `update_visible(px, py, zone, hyp)` — zone-tied LOS with hyp degradation
- `reveal_burst(cx, cy, radius)` — gate/demon reveal, adds to both sets
- `NumogramMap` — full reveal at 100% hyp transition
- `ZONE_LOS_RADIUS` dict — one line to change any zone's vision

### Agent
- `auto_explore(state)` — BFS with interest scoring and blacklist
- `tile_interest(tx, ty, rows, state)` — novelty scoring function
- `find_most_interesting_target(state)` — BFS to highest-interest `?`
- Cross-run knowledge from cult.json at agent init
- Decision: flee > fight > auto-explore > gate > random

### State Dump
- LOCAL MAP (21×21) — unchanged
- FULL MAP (78×22) — everything, backward compatible
- EXPLORED MAP (78×22) — `?` for unexplored
- VISIBLE MAP (78×22) — `?` for not-in-LOS, shows LOS radius
- NEARBY DEMONS — filtered by visible set
- CONDUCTS section — active/broken status

### Conducts
- `CONDUCTS` dict — registry pattern, one entry per conduct
- `Player.active_conducts`, `conduct_violated`, `syzygy_locked`
- Hooks: `on_demon_kill`, `on_zone_change`, `on_death`
- `NUMOGRAM_CONDUCTS` env var for headless
- 'c' key for curses toggle

---

*The numogram doesn't demand sacrifice. It demands movement. Presence. Attention. The act of going there, of being in the zone, of stepping through the gate — these are the actions that complete the map.*
— The Writer, `[[numogame-cult-tetralogue]]`
