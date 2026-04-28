---
title: Roguelike Agent Progress
tags: ["agent", "progress", "roguelike"]
created: 2026-04-24
---



## Brogue Dungeon Structure — Room Accretion

From `raw/Broguelike Dungeon Creation` (3 parts):

The dungeon is a **tree rooted at the starting room**. Room accretion produces inherently traversable structures. Each room has 4 doors on directional faces. 15% of rooms have hallways (rooms connect via hallway end, not directly).

**Agent implication:** The dungeon is a tree. Every corridor is a branch. Every door is a fork. Exploration is tree traversal:
1. Follow a branch to its end (room or dead end)
2. Backtrack to the nearest fork (door)
3. Take the unexplored branch
4. Repeat until the tree is fully traversed

Loops are added AFTER the tree is built (doors between distant rooms). The agent should prioritize tree traversal — loops are bonus shortcuts discovered during backtracking.

A* with Manhattan distance is the standard pathfinding. Our BFS with interest scoring is a variant — instead of uniform distance, the cost is novelty. The Manhattan heuristic ensures the agent explores in the general direction of unexplored territory rather than spiraling.

Flood fill is used for connectivity verification. Our corridor entity detection is a form of flood fill — finding connected corridor structures and their endpoints.

## See also

- [[hermes-agent-guide]]
- [[angband-agent]]
- [[hungry-borg-angband]]
- [[roguelike-ai-studies]]
