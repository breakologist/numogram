---
title: "Angband Agent Progress Log"
created: 2026-04-24
tags: ["agent", "angband", "development", "progress", "roguelike"]
status: active
---


# Angband Agent Progress Log

*Last updated: 2026-04-17 (v3 — sidebar fix verified)*

## Session Summary (April 17)

### What's Working
- ✅ **Sustained exploration**: 310+ floors on L1 without dying, M:0 (no sidebar contamination)
- ✅ **Food tracking**: `Fed:89→85` over 800 turns, fallback eat every 2000 turns
- ✅ **No oscillation**: BFS tie-breaking (30% randomization) kills oscillation
- ✅ **Strong novelty decay**: visited floors lose interest fast (`-2 - (v-1)*2.0`)
- ✅ **Reroll logic**: tiny rooms search 15 turns, then go up
- ✅ **Level regen**: resets visited, vcount, recent_positions on depth change
- ✅ **Secret door discovery**: search command revealed hidden door (Run 31)
- ✅ **Ladder data**: 500 listings scraped, equipment patterns analyzed
- ✅ **Wiki**: angband-ladder-analysis.md with equipment by level tier
- ✅ **Zone-aware parser**: sidebar contamination FIXED (user correction)
- ✅ **C command validation**: backstop for screen parser inflation

### What's Broken

#### Monster Parser (FIXED — verified)
~~The screen parser's `ch.isalpha()` catches sidebar text (`STR`, `INT`, `DEX`, etc.) as monsters.~~
- **User correction**: sidebar is on the LEFT, columns 0-12 (race, class, stats, HP, etc.)
- **Root cause**: parser had NO column restriction on monster detection — `x < 66` was on the STORES check, not monsters
- **Fix applied**: `x >= 13 and 1 <= y < 22` — only parse monsters in map area (rows 1-21, columns 13-79)
- **Added**: uppercase monster detection (was missing entirely — only lowercase was caught)
- **C command backstop**: `_scan_nearby_monsters()` called every 5 turns when screen count > 3. Converts direction/distance to approximate positions.
- **Verification**: 34 false positives → M:0 on runs without monsters. No sidebar contamination in 310+ floor exploration.

#### The Borg Approach (for reference)
The built-in Angband Borg is compiled INTO the game. It reads:
- `cave` array (tile features)
- `monster` list (positions, HP, types)
- `object` list (items, equipment)
- `player` struct (stats, inventory)

No screen parsing. No sidebar contamination. Our terminal-parsing approach will always be fundamentally limited.

#### Items Not Found
- 0 items in 3500-turn run despite 136 floors explored
- Items might be behind doors or hidden
- Or the room genuinely had no items

#### No `>` Stairs
- 136 floors explored, no `>` stairs found
- Stairs might be behind secret doors
- Or the level generation didn't place stairs in the explored area

### Equipment Analysis (from Ladder)

| Tier | Avg Items | Top Slots | Notes |
|---|---|---|---|
| L1-3 | 3 | Torch, Weapon, Body | Starting gear only |
| L4-8 | 6 | Torch, Body, Cloak, Ring | Filling slots |
| L9-15 | 7.1 | Body(86%), Shield(71%), Boots(71%), Cloak(57%) | All slots filling |
| L40+ winners | 12 | Ring(187%), Ranged(100%), Cloak(100%) | Fully equipped |

### Diving vs Grinding (Ladder Data)
- 0% speedrun (<1.0 ratio turns/depth)
- 21% cautious (3-10 ratio)
- 79% grind-heavy (>10 ratio)
- Fastest winner: 14,713 turns (Hobbit Mage)
- Median winner: 85,596 turns
- Agent's approach (dive, fight weak, reroll bad floors) matches aggressive divers

### Death Causes (Early Game)
- Town: dogs, drunks, Grip, Fang
- L1-5: poison, trap doors, soldiers, Kobold archers
- L5-15: orcs (Grishnákh), mages, stegocentipedes, starvation

## Code Changes This Session

1. **Fight more**: weak monsters at 25% HP (was 35%), walk toward within 5 tiles
2. **Equip on pickup**: `w` command for all equipment (removed duplicate `W`)
3. **Reroll**: tiny rooms search 15 turns first, then go up
4. **Novelty decay**: `-2 - (v-1)*2.0` (was `-2 - v*0.5`)
5. **BFS tie-breaking**: 30% randomization on equal-score tiles
6. **Level regen**: resets visited, vcount, recent_positions
7. **Fed parsing**: `Fed\s+(\d+)` regex, fallback eat every 2000 turns
8. **No wall digging**: removed from escape + oscillation handlers
9. **Perimeter search**: walk walls, search at each position when all explored
10. **Stairs**: walk toward directionally when BFS fails (no save-and-quit)
11. **Secret doors**: filter from item pickup messages
12. **Monster parser**: zone-aware fix — `x >= 13, y <= 20` excludes sidebar + status
13. **Uppercase monsters**: added detection (was missing — only lowercase caught)

## Next Steps
1. ~~Fix monster parser~~ ✅ Done — zone-aware, sidebar excluded
2. Test with real gameplay — does agent fight DL1 monsters correctly now?
3. Verify item pickup — are items spawning but not detected?
4. Test secret door passage — agent finds them but does it walk through?
5. Add `E` command testing when Fed drops below 50%
6. Consider Angband cheat options for structured data
7. ~~Screen zone awareness~~ — could generalize to other roguelikes (see below)

## Screen Zone Recognition (Cross-Roguelike Pattern)
Every terminal roguelike has scrolling map + fixed UI panels:
- **Angband**: left sidebar cols 0-12, map cols 13-79, status rows 21-28
- **DCSS**: right panel, map left, messages bottom
- **Brogue**: bottom panel with border ╔═══
- **NetHack**: message top, sidebar right

Generic approach: define UI zones, exclude from map parsing. The sidebar boundary is always detectable — either fixed columns, visual separators, or repetitive text patterns.

## Data Files
- `~/.hermes/angband_ladder_listings.json` — 500 ladder entries
- `~/.hermes/angband_ladder_dumps.json` — 30 detailed dumps
- `~/.hermes/angband_early_deaths.json` — 12 early death dumps
- `~/.hermes/angband_ladder_data.json` — analysis summary
- `~/numogame/scrape_angband_ladder.py` — scraper script
- `~/numogame/angband_agent.py` — agent code (~1385 lines)

## Session Notes (April 17 — Late Session)
- **Sidebar fix verified**: M:0 across 310+ floor exploration. No phantom monsters.
- **C command backstop**: `_scan_nearby_monsters()` called every 5 turns when screen count > 3. Converts direction/distance to approximate (x,y) positions.
- **Row boundary**: `1 <= y < 22` for monster detection. Row 0 = status bar. Rows 22+ = Fed/Speed/Level overlap.
- **Upper rows also need exclusion**: Status text "D:L1 F:141 M:19" rendered at rows 19-22 when map extends. The M:19 in status bar was being parsed as 19 uppercase monster characters.
- **No real monster encounters yet**: Agent rerolls tiny rooms efficiently (15 turns search + reroll). DL1 levels explored 310 floors without encountering monsters — either rooms are empty or monsters are in unexplored corridors.
- **Food system confirmed**: Fed 89→85 over 800 turns. Fallback eat every 2000 turns working.

## Next Session Priorities
1. Run longer test (4000+ turns) to observe real monster encounters
2. Verify C command integration works when monsters are present
3. Test item pickup — are items spawning behind doors?
4. Secret door passage — agent finds them but needs more testing
5. Consider Angband cheat options (wizard mode) for structured data access

## Related
- [[angband-ladder-analysis]] — full ladder analysis wiki
- [[angband-symbols]] — symbol reference
- [[angband-agent]] — agent techniques and pitfalls
- [[hermes-agent-meta-analysis]] — usage optimization recommendations

## DL1 Pocket Fix (April 18)

### The Problem
Agent getting stuck on DL1 (first dungeon level). Two distinct failure modes:

1. **Staircase phantom**: Sidebar displays "Up staircase" at the player's current position. The sidebar parser overwrites the actual `<` character found by the map parser with the player's position. Agent then tries to go up stairs that aren't there — `cmd.go` triggers and fails with "I see no up staircase here."

2. **Pocket rooms**: Agent enters a small room with no visible exits and no treasure. Oscillates between tiles. BFS explores in local radius; stairs at the far end of the map never reached without explicit targeting.

### Fixes Applied

**Staircase detection**:
- Map parser finds `<` at its actual position — this takes priority
- Sidebar "Up staircase" text is used as fallback ONLY when map parser didn't find `<`
- Logic: `if map_parser_found_stairs: use map position; elif sidebar_found: use sidebar position`

**Town detection**:
- `_is_town` must match `'L1'` (not just `'Town'`) — Angband labels the first dungeon level as "D:L1" in status bar, not "Town"
- Without this fix, agent treats DL1 as dungeon and tries to fight town NPCs

**Pocket room handling**:
- Detect pocket rooms (small enclosed space, no doors, stuck >= 5 turns)
- If stuck in pocket: go up stairs → return to town → find down stairs → re-enter (generates new level)
- Requires DIALOG_PATTERNS entry for direction prompts ("Which direction?" → send direction key)

**Oscillation detector**:
- Tightened to 8/3 threshold (8 revisits of same 3 tiles = oscillation confirmed)
- Previously too loose, agent would oscillate 20+ turns before triggering

### Open Question: True Pocket or DFS Flaw?

**Hypothesis A — True pockets**: Angband generates some rooms that are genuinely enclosed with no doors or hidden doors. The DFS explores the room, finds nothing, and has no exit. These are real pockets in the map topology.

**Hypothesis B — DFS flaw**: The DFS/BFS explores in a local radius and may miss exits that are:
- Hidden doors (require search command `s`)
- At the edge of the agent's exploration radius
- Behind already-explored tiles that the agent considers "done"

**Evidence for A**: Agent has hit rooms where searching (s) revealed no hidden doors, and the room was genuinely sealed. The up→town→re-enter workaround generates a new level, suggesting the pocket was a map generation artifact.

**Evidence for B**: Agent's BFS explores in a local radius (typically 20-30 tiles). Stairs at the far end of the map never get reached without explicit long-range targeting. The agent may be giving up on rooms that DO have exits but at distances beyond BFS reach.

**Resolution needed**: Log all pocket rooms — record room size, number of wall tiles searched, and whether a hidden door existed (verifiable via wizard mode or by walking walls after the fact). If pockets consistently have hidden doors the agent missed → DFS flaw. If they're genuinely sealed → true pocket.

**Related**: The stair targeting system was added to address this — explicit BFS scoring for stair positions, long-range direction toward stairs when BFS fails, corridor fallback when completely stuck. But the core question remains: are pockets real or perceived?

