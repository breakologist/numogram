# The Hungry Borg — Angband Agent

*Recursive Consumption: The Borg eats the dungeon, and the dungeon eats the Borg.*

## Status
- **Phase:** Phase 1 — Grinding (shallow dungeon exploration)
- **Town:** Complete — all 8 stores visited in 63 turns via BFS
- **Dungeon:** L1 reached multiple times, tiny room problem, died twice
- **Goal:** Survive L1, find hidden doors, reach L2
- **Code:** `~/numogame/angband_agent.py` (~520 lines)
- **Runs:** 5+ logged to `~/.angband_runs.jsonl`

## Architecture
```
TmuxGame (angband -mgcu -n -uborg)
  → tmux capture-pane (read screen as ASCII)
    → AngbandScreen parser (player, floors, walls, stairs, stores, doors, items, status)
      → AngbandAgent (BFS + interest model + DFS commitment)
        → tmux send-keys (numpad 2/4/6/8)
```

## Key Discoveries
1. **Vi keys broken** — Angband curses mode needs numpad (2/4/6/8), not h/j/k/l
2. **`-more-` prompt** (lowercase, single dash) blocks all input — space to dismiss
3. **Character creation** needs `'y'` key, not Enter
4. **`>` stairs priority** — always descend when visible
5. **Store visit loop** — use `visited_stores` by number, mark adjacent (within 1 tile)
6. **Search for hidden doors** — `s` key, proactive in tiny rooms (<20 floors)
7. **HP-gated descent** — only descend at >60% HP (town drunks are lethal)
8. **Progressive turn budget** — 200 + (visit-1) × 75 per level

## Town Behavior
- BFS navigates all 8 stores, routes around visited ones
- Class-aware shopping: Warriors skip spellbooks, buy torches/oil/healing/recall
- `visited_stores` by store number prevents re-entry loops
- Stores reset on town return (fresh stock)
- Light sources: Torches (2g), Lanterns (35g), Flask of oil (3g)

## Dungeon Behavior
- BFS exploration with interest scoring (doors +15, stairs +25, items +10)
- Stuck recovery: 70% search, 30% random walk
- Proactive search: 50% search rate when room <20 floors
- Doors (`+`/`'`) are walkable and high-interest
- Status-bar stair detection as fallback for tiny rooms
- Progressive turn budget: 200→275→350→... per level visit

## Deaths
| Run | Location | Cause | Lesson |
|-----|----------|-------|--------|
| #1 | Town (~turn 142) | Hostile NPC (town drunk with Zuiquan) | Avoid hostiles in town |
| #2 | L1 (turn 197) | Descended with 13 HP | HP-gate descent at >60% |

## Grok's Advice (chunked diving)
- Town is the strategic anchor — visit all stores, buy supplies, then dive
- Depth > everything — deeper kills level you faster, better loot
- Dive until worried, then fight conservatively
- Word of Recall scrolls for safe retreat (future)
- Curriculum: Phase 1 (grind L1) → Phase 2 (chunked diving L2-10) → Phase 3 (deep dive)

## Next Steps
1. Survive L1 — descend at full HP, search tiny rooms for hidden doors
2. Reach L2 — find `>` on L1, descend deeper
3. Try Dwarf race — STR/CON bonus, infravision (see in dark)
4. Selling in town — items found in dungeon → sell to stores
5. Word of Recall — buy scrolls, use for safe retreat
6. Cross-run learning — save death causes, max depth, strategies

## Links
- [Roguelike AI Studies](roguelike-ai-studies.md)
- [Brogue Design Principles](brogue-design-principles.md)
- [Grok Angband Conversation](../raw/Grok Angband conversation.md)
- [AQ Dictionary](../raw/AQ Dictionary.md)

---
*"The dungeon is a tree, and death is a leaf." — The Hungry Borg's first proverb*
*"YASD maketh the Man, and the Borg too." — Etym*
