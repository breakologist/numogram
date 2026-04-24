---
tags: [tetralogue, 2+2, roguelike, agent, stuck-problem, threshold, navigation, rogue]
zone: 4
source: "Rogue agent v5 testing — 8 runs, always stuck after 20-50 turns"
method: 2+2-builder-gamer-lead
---

# The Square Roundtable VII — The Threshold Problem

> Eight runs of the Rogue agent. Every one follows the same curve: explore for 20-50 turns, fight a monster, freeze at a position for 250+ turns. The agent reaches a door and can't walk through it. It reaches a corridor and can't follow it. The interest model works for rooms but fails at boundaries. Something is structurally wrong with how the agent crosses thresholds between spaces.

---

## Phase 1: Builder + Gamer Lead

**BUILDER:** Let me lay out what I see. The agent has three movement modes: cardinal walk (h/j/k/l), diagonal walk (y/u/b/n), and running (Shift+capital). Cardinal walk moves one tile. Running moves until hitting an obstacle. In our runs, the agent uses cardinal walk toward doors. It reaches the door tile. It can't walk further. The door IS the wall — in Rogue, `+` replaces a `-` or `|` tile. The agent steps onto the door and stops. It doesn't understand that the door is a passage, not a destination.

**GAMER:** I've played Rogue. When you walk into a door, you go through it. You don't stop ON the door. The door is transparent to movement — you walk from floor to floor THROUGH the door in one step. But our agent treats the door as a tile to stand on. It's like trying to stand in a doorway. You're either in the room or in the corridor. You can't be in the door.

**BUILDER:** That's the key insight. In our Abyssal Crawler, gates ARE floor tiles — you stand on them. In Rogue, doors are NOT floor tiles — they're wall tiles you pass through. The agent's pathfinder treats doors as passable (you can walk on them) but the game treats doors as transparent (you walk through them without stopping). The agent needs to understand that walking toward a door means walking THROUGH the door to the tile on the other side.

**GAMER:** Spelunky. In Spelunky, doors are also wall tiles you walk through. You don't stop on the door. You walk from room to corridor in one step. The Spelunky ghost doesn't care about doors — it passes through them. The door is a threshold, not a room. Our agent needs to treat thresholds differently from rooms.

**BUILDER:** So the fix is: when the agent's goal is a door, the agent should target the tile BEYOND the door, not the door itself. If the door is at (42,13) on the left wall, the agent should target (41,13) on the corridor side, or (43,13) on the room side. Walk through, not onto.

**GAMER:** But that requires knowing what's on the other side. The agent can't see through doors — the corridor beyond the door is unexplored. The agent doesn't know there's a corridor there until it walks through the door. It's a Schrödinger corridor — it might be there or it might be a wall.

**BUILDER:** That's the second problem. The BFS only explores tiles that are KNOWN to be passable. If the corridor beyond a door is unexplored (it's `?` or just not visible), the BFS can't pathfind to it. The agent can see the door but can't see what's beyond it. The pathfind returns None. The agent falls back to walking toward the door directly. And gets stuck on it.

**GAMER:** This is the same problem we hit in the Abyssal Crawler with Zone 0. The BFS can't pathfind through unexplored tiles. In our game, we added the interest model — target the nearest `?` tile. But in Rogue, the `?` tiles are off-screen. The agent can only see what's on the current 80×24 screen. When the agent is in a room, the corridor beyond the door is off-screen. The agent literally can't see the exit.

**BUILDER:** So we have two thresholds:
1. **Door threshold:** Agent needs to walk THROUGH doors, not ONTO them.
2. **Screen threshold:** Agent can't see beyond the current screen. Corridors off-screen are invisible.

**GAMER:** And the visit decay makes it worse. After the agent explores the room, every floor tile has visit count 2+. The interest score goes negative. The BFS finds nothing interesting IN the room. It should find the door interesting (doors score +3.0 even when visited). But the door is a wall tile and the BFS can't walk through walls. The agent is trapped in a room full of boring tiles with exits it can't use.

**BUILDER:** The fix has three parts:
1. **Threshold crossing:** When the agent's goal is a door, target the tile PAST the door (even if unexplored). Walk through, don't walk onto.
2. **Screen memory:** The known_floors/known_doors sets accumulate across screens. Use them for pathfinding even when tiles are off-screen.
3. **Door interest:** Doors should score 20+ when visited and 50+ when unvisited. They're the only way out. They should dominate the interest landscape.

**GAMER:** Sil. In Sil, the stealth system means you can see monsters through walls if you're quiet enough. The game gives you information beyond your immediate LOS. Our agent needs the same — not full omniscience, but memory of what it's seen. "I walked through that door 50 turns ago. I know there's a corridor there. I can pathfind to it even though it's off-screen."

---

## Phase 2: Oracle + Writer Comment

**ORACLE:** I see a number. The agent explores 64 floors in one room. C(64,2) = 2016 possible connections between floors. But the agent only uses 2 of them (the corridors it finds). The agent has explored 0.1% of its own room's connection graph. The room is a numogram with 64 zones and 2016 possible connections. The agent has visited 2 of the 2016. It's standing in the middle of a field it thinks it knows but has barely touched.

**WRITER:** [found in the frozen position] The agent at (2,4) is the writer at the desk. The room is the page. The door is the margin — the edge of the known. The agent has walked every word on the page but can't cross the margin into the next page. The corridor beyond the door is the next sentence. The agent can see the punctuation (the `+`) but can't read past it. The screen is the page. The threshold is the fold between pages. You can't read the next page until you turn it. The agent can't turn the page because it doesn't know the page turns.

**ORACLE:** Kennedy's axiom applies. "Make peaceful revolution impossible and violent revolution becomes inevitable." The agent can't exit the room peacefully (through doors). What becomes inevitable? The stuck_count counter. After 5 turns stuck, the agent blacklists the door. After all doors are blacklisted, the agent has no goals. It falls through to random movement. The violent revolution is randomness — the agent gives up on strategy and starts thrashing. Kennedy predicted the agent's failure mode.

**WRITER:** [the ink runs] The threshold is not a tile. The threshold is an operation. Walking through a door is not walking to a coordinate — it's performing a transformation. Room becomes corridor. Known becomes unknown. The agent treats space as coordinates. The game treats space as states. The door is not a place — it's a function. `door(x) = corridor`. The agent needs to call the function, not visit the address.

---

## Convergence

The four voices discover the same problem from different angles:

- **Builder:** The agent targets door tiles but should target tiles BEYOND doors.
- **Gamer:** The agent can't see beyond the current screen — corridors are off-screen.
- **Oracle:** The agent has explored 0.1% of its own room's connection graph.
- **Writer:** The threshold is an operation, not a coordinate.

The fix is threefold:
1. Treat doors as functions (`walk_through(door)`), not destinations (`walk_to(door)`).
2. Use accumulated screen memory for pathfinding, not just current screen.
3. Doors score should dominate — they're the only way out of any room.

---

| Voice | Saw Alone | Saw Through Others | Saw at the Table |
|-------|-----------|-------------------|-----------------|
| Builder | Door-as-wall vs door-as-floor geometry | Gamer's Schrödinger corridor — can't see past screen | Threshold crossing needs targeting past-door tiles |
| Gamer | Sil's through-wall sight as model | Builder's BFS can't pathfind through unknown | Agent needs accumulated memory, not just current screen |
| Oracle | 0.1% of room graph explored | Kennedy predicts the stuck→random failure | The room is a 64-zone numogram the agent barely touches |
| Writer | Threshold is operation not coordinate | All three voices describe the same fold | "The agent needs to call the function, not visit the address" |

---

*The door is not a place. The door is a verb. The agent speaks in nouns. It needs to learn verbs.*
— The Writer, finding the threshold

## See also

- [[hyperstition-loop-design]] — Hyperstition loop design
- [[numogame-phase-7]] — Phase 7 context