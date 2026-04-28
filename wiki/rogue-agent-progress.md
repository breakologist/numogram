---
tags: ["agent", "corridor", "interest-model", "roguelike", "screen-parser", "threshold", "tmux"]
created: 2026-04-15
source: "Rogue agent development — 8 versions, 8 commits, crossing thresholds"
---


# The Hungry Borg in Rogue — Crossing Thresholds

> Eight versions of the Rogue agent. Each crosses a threshold the previous couldn't. The architecture is proven: TmuxGame → Screen parser → Agent decision → send-keys. What's game-specific is how thresholds work. Doors are verbs. Corridors are entities. The room dies when explored.

## Version History

### v1-v3: Stuck in Rooms
The agent explored 37-78 floors in the starting room. Found doors on walls. Couldn't walk through them. The BFS found nearest unvisited tiles — always inside the room. Never targeted the distant door.

**Lesson:** The BFS picks the nearest interesting tile, not the most interesting. Distance dominates interest.

### v4-v5: Goal-First Architecture
Rewrote the decision hierarchy. Pick a goal (stairs > doors > unexplored). Then pathfind to it. BFS is for navigation, not goal selection.

**Problem:** Goals were doors. Doors are wall tiles. BFS can't pathfind through walls. Agent walked toward doors but couldn't step onto them.

### v6: The Threshold Fix
"When standing on a door, don't pick a new goal. Keep walking."
The agent reached a door tile at T:0. Next turn, picked a different goal and ran away. The fix: when `(px,py) in doors`, keep walking in the same direction. Don't change goals.

**Breakthrough:** Agent walked through a door into a corridor. 16 floors → 17 floors + 1 corridor.

### v7: Context-Dependent Interest
Interest scores change based on agent context:
- **In a room:** doors score +10 (exits), corridors +8
- **In a corridor:** endpoints score +10 (room entrances), doors +2
- **Empty room:** tiles decay to -2.0 (the room dies)
- **Low HP:** items score +15 (survival instinct)

Key principle: "Empty rooms die. Exits live."

### v8: Corridor Entities
Corridors treated as entities, not just tiles:
```
corridor = {
    tiles: set of (x,y) positions,
    endpoints: where corridor meets room/door,
    length: number of tiles
}
```
When in a corridor, walk toward unvisited endpoints. Endpoints are bridges to undiscovered rooms. The corridor entity concept generalizes — every roguelike has corridors with endpoints.

### v9 (current): Smart Movement and Stuck Recovery
- **Cardinal vs diagonal:** cardinal in corridors/near walls, diagonal in open rooms
- **Running (Shift+dir):** passes through doors naturally, covers corridors fast
- **Stuck recovery:** random walk after 1 turn stuck (rest excluded from stuck counter)
- **Wall fix:** checks both `known_walls` AND current screen walls

## The Three Thresholds

From Tetralogue VII:

1. **Door threshold:** Walk THROUGH doors, not ONTO. "The door is not a place. The door is a verb."
2. **Screen threshold:** Can't see beyond 80×24. Corridors off-screen are invisible. Need accumulated memory.
3. **Interest threshold:** Doors should dominate interest. They're the only way out of any room.

## Interest Model (transplanted from Abyssal Crawler)

```
_tile_interest(x, y, screen):
    walls: -999
    
    unvisited:
        base: 8.0 (mystery)
        stairs: +20.0
        doors (in room): +10.0
        corridors (from room): +8.0
        items (low HP): +15.0
        items (normal): +6.0
    
    visited:
        base: -2.0 - visits × 0.5 (room dies)
        stairs: +15.0 (survives)
        doors: +8.0 (survives)
        corridors: +6.0 (survives)
        endpoints: +10.0 (bridges to new territory)
        items: +5.0
```

The agent is a heat engine. Visited tiles are cold. Unvisited tiles are hot. Doors are thermal bridges. The agent flows from cold to hot.

## Architecture

```
tmux session (Rogue process)
  → tmux capture-pane (read screen as ASCII)
    → Screen parser (player, monsters, items, doors, corridors, status)
      → Agent decision (goal-first, then BFS pathfind)
        → tmux send-keys (vi movement, running)
          → repeat
```

The TmuxGame class works with any terminal roguelike. The Screen parser is game-specific (symbol table, status regex). The Agent architecture is universal.

## Connection to Game-Agent-Techniques

From `[[game-agent-techniques]]`:

- **Dijkstra maps:** Our BFS with interest scoring IS a Dijkstra map with custom costs. Instead of uniform distance, the cost is interest. "Shortest path to most interesting tile."
- **Interest scoring:** Our model is a simplified E3B + visit decay. We track visit counts and decay with familiarity. Domain-specific bonuses (doors, stairs, items) replace learned rewards.
- **State representation:** Our screen parser provides structured data (paradigm 2). The opportunity is adding LLM reasoning (paradigm 3) — feed the state dump to a local LLM with game rules in the system prompt.

## Current Status (April 15, 2026)
@sz
@sb- **Explores:** 30-49 floors per run
@sb- **Finds:** corridors (2-3), doors (2-3)
@sz- **Navigates:** through doors into corridors
@sz- **Stuck:** at walls after running into them (oscillation)
@sz- **Never found:** stairs, items (too rare in early levels)



## Next Thresholds

1. **Wall bounce detection:** Stop running before hitting walls. Detect when position doesn't change.
2. **Corridor endpoint targeting:** Follow corridors to their rooms, not just nearest unvisited tile.
3. **Stair finding:** Stairs are the ultimate goal. Prioritize once most of the level is explored.
4. **Item management:** Use potions when low HP. Equip better weapons/armor.

---

*The door is not a place. The door is a verb. The agent speaks in nouns. It needs to learn verbs.*
— The Writer, `[[threshold-problem-tetralogue]]`
