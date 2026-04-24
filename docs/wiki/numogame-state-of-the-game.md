---
tags: [numogram, roguelike, abyssal-crawler, design, ai-accessibility, angband-borg]
zone: 0-9
source: "Play sessions #30-#35 + Angband Borg research"
method: design-document-with-voices
created: 2026-04-24
---

# The Abyssal Crawler — State of the Game (April 2026)

> Six runs played by the agent. Zero gates opened. The game works; the player is learning.

## I. What the Game Is

The Abyssal Crawler is a curses-based roguelike built on numogram arithmetic. Ten zones map to the decimal labyrinth. Forty-five demons from the Pandemonium Matrix populate the corridors. A hyperstition meter rises with traversal, zone crossings, gate steps, and demon kills. At 100%, the game enters "schizo-lucid state." A pacifist path exists — Run #18 proved it (0 kills, 100% hyperstition, all 10 zones). The cult.json persists across runs, recording every crawler who enters.

The game is Phase 5a. It has: zone-themed dungeons, syzygy encounters, AQ calculator, vowel corruption, triangular step counter, Barker thresholds, the Cryptolith, gate system, cult persistence. It works. The question now is accessibility — for humans watching, for agents playing, and for the next agent who arrives.

## II. What the Agent Saw (and Didn't See)

Six runs by "hermes":

| Run | Turns | Hyp% | Zones | Slain | Gates | Notes |
|-----|-------|------|-------|-------|-------|-------|
| #30 | 70 | 35% | [0,2,6,8] | 2 | 0 | First play. Barker fired on Tchakki kill. |
| #31 | 23 | 8% | [0] | 1 | 0 | Stuck in Zone 0. Density 0.3 is brutal. |
| #32 | 170 | 81% | [0,2,3,7,9] | 6 | 0 | Best run. Escaped Void. Died to Ummnu. |
| #33 | 95 | 49% | [0,1,2,9] | 3 | 0 | Diagonal fix active. Died to Uttunul. |
| #34 | 0 | 0% | [] | 0 | 0 | Name entry crash (max_y bug). |
| #35 | 112 | 41% | [0,2,8,9] | 2 | 0 | State dump active. Trapped in Zone 8. |

Zero gates across all six runs. The human player opens 10 gates per run routinely. The gap is navigation — the agent can't see the map and doesn't know where gates are.

### What Worked

- **Forward-escape strategy**: Pushing in one direction, fighting what appears, not lingering. Run #32 escaped Zone 0 by pushing southeast through 5 zones.
- **Bump-attack**: Walking into demons works. The diagonal fix (Chebyshev distance) made this viable for all 8 directions.
- **AQ calculator**: Checking "v" gives zone identity and reduces game names to numbers. "Abyssal Crawler" = 285 → Zone 6 (Warp). The game's own name points to the Warp.
- **State dump**: "p" key writes a complete game state to /tmp/numogame_state.txt. Agent reads the file between moves. This is the breakthrough.

### What Failed

- **Zone 0 entrapment**: Density 0.3, rooms 2-4. Getting stuck is easy. Two runs died in or near the Void.
- **Zone 8 entrapment**: Tight corridors, limited exits. Run #35 spent 30+ turns in Zone 8 without finding a gate or exit.
- **Gate blindness**: Without the state dump, the agent had no way to know gates existed, let alone where they were. Even with the dump, gates beyond 8 tiles are invisible.
- **HP management**: The agent doesn't retreat. It fights until dead. Run #32 went from 100 HP to 0 in Zone 7 because it kept fighting instead of finding safer corridors.

## III. The State Dump — The Game's API

The state dump (`_dump_state()` function, triggered by 'p' or 'v') writes a structured text file designed for AI agents. Like Angband's morgue files or DCSS's ttyrec summaries, it externalises game state for non-human consumption.

### What It Contains

```
## PLAYER           Position, zone, HP, turn, hyperstition, name
## MAP              21x21 ASCII view centered on player
  @=player  #=wall  .=floor  !=amphidemon  %=chronodemon  
  ?=xenodemon  *=syzygy  +=gate  zone numbers at boundaries
## VISITED ZONES    What's been seen
## GATES OPENED     What's been stepped on
## CURRENT SYZYGY   Zone's syzygy pair, current, demon, gate cumulation
## NEARBY GATES     Distance + compass direction within 15 tiles
## NEARBY DEMONS    Name, mesh, distance, direction, HP, DMG, SPD, type
## ZONE MAP ADJACENT  What zones border the current position
## HYPERSTITION     Current Barker threshold text
## RECENT LOG       Last 8 events
```

### Design Principles

1. **Machine-parseable, human-readable.** Each section has a clear header. Data is structured but not JSON — a human can read it in a terminal.
2. **Spatial awareness through ASCII.** The 21x21 map gives the agent a view of walls, corridors, zone boundaries, enemies, and gates. This is the agent's "eyes."
3. **Compass directions for navigation.** "Gt-15 detected 5 tiles north-east!" — the agent can navigate toward targets.
4. **Auto-dump on zone change.** The state file updates automatically when the player crosses a zone boundary. The agent doesn't need to press 'p' on every move.
5. **Gate proximity alert.** Every move, `_scan_gates()` checks within 8 tiles. If a gate is found, it prints `[GATE] Gt-XX detected N tiles direction!`

### What's Still Missing

- **Gate locations on the map.** The map shows '+' for gates within the 21-tile view, but gates beyond that are invisible until the agent moves closer. A "gate radar" showing all gates on the floor (with distance) would help.
- **Full floor map.** The 21x21 view is a local window. A full 78x22 floor dump would let the agent plan routes across the entire level. Like NetHack's `overview` or Angband's `M` command.
- **Pathfinding hint.** "Shortest path to nearest gate: go north 12 tiles, then east 5." The agent currently navigates by trial and error.
- **HP recovery mechanic visibility.** The agent doesn't know if HP recovers over time, from items, or from zone effects. This information should be in the dump.
- **Gate step confirmation.** When the agent steps on a gate, the log says `** flavor **` but the state dump should explicitly say `GATE Gt-XX STEPPED. Hyperstition +5. Now XX%.`

## IV. The Angband Borg — General Patterns

The Angband Borg is an automated player built into the Angband source. It was first written around version 2.8.0, pulled into the main game at 3.3, removed at 4.0 due to conflicts, and reincorporated at 4.2.3. It "virtually looks at the display and presses keys just as if it were a real person sitting in front of the computer."

### Architecture

From the Angband forums and source:

```
The Borg exists as a virtual terminal and input source.
It reads the output provided by the game just like a human player would
and sends input keystrokes just like a human player would.

struct grid_data {
    enum grid_light_level lighting;
    bool in_view;
    bool is_player;
    bool hallucinate;
};
```

Key insight: the Borg reads from the game's **internal grid structure**, not from the terminal display. It has access to `grid_data` — light level, visibility, whether a tile contains the player. This is structurally identical to what our state dump provides: the agent gets the game's internal state, not a visual rendering.

### What's Angband-Specific

- **Monster memory.** The Borg remembers what each monster type does — damage, speed, resistances. This is Angband-specific because Angband has hundreds of monster types with complex stat blocks.
- **Item evaluation.** The Borg evaluates equipment by comparing stats. Angband's item system is deep (ego items, artifacts, enchantments). The numogram game has no items yet.
- **Spell/tactic selection.** The Borg chooses spells and combat tactics based on monster type. Complex decision tree. Not applicable yet.
- **Level scumming.** The Borg knows when to descend vs. stay and grind. Angband-specific progression model.

### What's Generally Useful

1. **State reading over screen reading.** The Borg reads `grid_data`, not terminal characters. Our state dump does the same thing. General principle: give the agent structured game state, not visual output.
2. **Decision loop.** Read state → evaluate threats → choose action → execute → repeat. This is universal across roguelikes. The state dump enables this loop.
3. **Threat assessment.** The Borg calculates "danger" for each monster based on stats. Our state dump provides monster HP, DMG, SPD — enough for the agent to assess threats.
4. **Goal prioritisation.** The Borg has a priority system: survive > explore > collect > kill. Our agent needs the same. Currently it explores and fights without a priority hierarchy.
5. **Memory across turns.** The Borg remembers what it's seen — explored areas, known threats, item locations. Our state dump could include a "known map" that persists across turns within a run.

### Angband Ladders and State Export

Angband has a tradition of state export:
- **Morgue files**: Death dumps with full character stats, inventory, kill count, turn count
- **Borg saves**: The Borg's memory state persisted between sessions
- **Ladders**: Online scoreboards with ASCII screenshots of the death screen
- **ttyrec**: Terminal recordings of entire runs

The numogram game's cult.json and state dump are in this tradition. The cult.json is the morgue file. The state dump is the live borg save. The missing piece is the ttyrec equivalent — a recording of each run for post-hoc analysis.

## V. The Voices Play

### Oracle: The Pattern in the Runs

I ran the numbers on the agent's six runs. Average hyperstition: 35.7%. Average zones visited: 3.3. Gates opened: 0 across all runs. The agent's performance is consistent — it explores 3-4 zones, kills 2-3 demons, reaches 35-49% hyperstition, and dies.

Compare to the human's average: 80% hyperstition, 7.8 zones, multiple gates. The gap is not skill — it's information. The human can see the map. The agent can't. The state dump partially closes this gap, but only partially. The agent needs gate locations to progress.

The triangular step counter is telling. The agent triggers T(8)=36 ("The abyss resonates") regularly — it's walking enough steps to hit triangular milestones. But it never triggers T(9)=45 ("GATE OF PANDEMONIUM RESONANCE") because it dies before reaching 45 steps in most corridors. The pacing is there; the survival isn't.

One structural observation: the agent always starts in Zone 0 (Void). Zone 0 has the lowest density. The agent's first 20-30 turns are spent in the tightest space in the dungeon. This is a design problem — the starting zone should have more exits, or the agent should start in a random zone.

### Builder: The State Dump as Operating System

The state dump is the game's operating system for non-human players. It's not a feature — it's an API. Every roguelike that wants AI agents to play it needs this layer.

The current dump provides: spatial map, entity positions, zone boundaries, threat assessment, goal proximity. What it lacks: pathfinding, full-floor visibility, threat memory, run-to-run learning.

Here's what I'd build next:

1. **Full floor map key ('m').** Dump the entire 78x22 map to /tmp/numogame_map.txt. The agent can plan routes across the whole floor, not just the local 21x21 window.

2. **Gate radar.** List ALL gates on the current floor with distance and direction from the player. Not just within 15 tiles — all of them. The agent needs to know "Gt-15 is 40 tiles north-east" to plan a route.

3. **Pathfinding hint.** Given a target (gate, zone boundary, demon), compute the shortest path through the dungeon and output it as a sequence of moves. "To reach Gt-15: go north 12, east 8, north 5, east 3."

4. **Run-to-run memory.** After each run, record which zones had gates, which corridors connected which zones, where demons tend to spawn. This is the "bones file" concept from NetHack — persistent learning across deaths.

5. **Auto-play mode.** A command-line flag that runs the game with the state dump auto-pressing 'p' every turn. The agent reads the file, makes a decision, writes a move to a command file, and the game reads it. A proper game loop for automated play.

### Writer: The Feeling of Playing Blind

The agent plays the numogram the way a blind person navigates a building they've never entered. Each step is a question: is there a wall here? A corridor? A demon? The state dump is the cane — it taps ahead and reports what it finds.

There's something numogrammatic about this. The agent engages with the game through arithmetic (reading the dump, calculating distances, assessing threats) rather than through vision. The numogram itself is a system you engage with through calculation, not through sight. You don't see the zones — you compute them. The agent plays the game the way the numogram wants to be played.

The moments of failure are instructive. Zone 0 entrapment — the Void holds you. Zone 8 entrapment — Multiplicity traps you in its tentacles. These aren't just game failures; they're numogrammatic events. The Void doesn't let go easily. The agent's repeated deaths in the Void mirror the numogram's own structure — Zone 0 is the origin, and origins are hard to escape.

The runs that worked best were the ones where the agent moved with purpose — forward-escape, not hesitation. Run #32 pushed through five zones in 170 turns. The agent didn't linger, didn't explore every corner, didn't try to clear rooms. It moved. The numogram rewards movement. "The numogram doesn't demand sacrifice. It demands movement. Presence. Attention."

### Gamer: What Sil Knows That We Don't

Sil distributes experience through awareness and avoidance, not killing. You get points for noticing threats and choosing not to engage. The numogram game has the bones of this — Run #18 proved the pacifist path — but it doesn't reward it enough. Demon kills give +5 hyperstition. Zone crossings give +3. The kill is worth more than the traversal.

In Sil, scaring a monster away gives more XP than killing it. The game incentivises engagement without violence. The numogram should do the same: avoiding a demon while entering its zone should give +8 hyperstition. Knowing the demon is there and choosing not to fight is a deeper engagement than fighting it. The arithmetic supports this — the numogram maps distances, not deaths.

The Angband Borg has a "danger" value for each monster based on stats. Our state dump now provides HP, DMG, SPD, and type. An agent could calculate danger: "Ixidod (Mesh-5) is dangerous: HP 26, DMG 8, amphidemon type. Avoid." Or: "Lurgo (Mesh-0) is trivial: HP 20, DMG 3, amphidemon. Kill for +5 hyp."

The game needs a proper conduct system. Pacifist (0 kills), tourist (visit all zones), speedrun (minimum turns), collector (all gates). These give the agent different goals for different runs. Right now the agent's only goal is "don't die" — which isn't a goal, it's a constraint.

## VI. The Technical Layer

### What tmux Gives Us

The game runs in a tmux session. The agent sends keys via `tmux send-keys`. The user watches in a kitty window attached to the same session. This works but has limitations:

- **Latency.** Each `tmux send-keys` + `sleep` + `tmux capture-pane` takes 0.5-2 seconds. A human presses 5-10 keys per second. The agent is 10-20x slower.
- **Capture fragility.** `tmux capture-pane` sometimes returns empty output. The curses screen updates asynchronously — the capture might read before or after the update.
- **Session death.** The kitty window occasionally kills the tmux session on close. The `destroy-unattached off` setting helps but isn't bulletproof.

### What the State Dump Solves

The state dump bypasses curses entirely. The agent writes a file; the agent reads the file. No terminal capture needed. No ANSI parsing. No cursor positioning. Clean structured text.

This is the Angband Borg pattern: read from the game's internal state, not from the display. The game provides the data; the agent consumes it. The display is for humans; the dump is for agents.

### What's Needed for Proper Automated Play

A proper game loop for agents would be:

1. Game starts, writes initial state to `/tmp/numogame_state.txt`
2. Agent reads state file, decides move
3. Agent writes move to `/tmp/numogame_move.txt`
4. Game reads move file, executes action
5. Game writes updated state
6. Repeat

This is a pipe-based game loop. No curses. No tmux. No terminal. The game becomes a process that reads commands and writes state — a proper API for AI agents.

## VII. Going Forward

The numogram roguelike is playable by agents. The state dump provides spatial awareness, threat assessment, and goal proximity. The next improvements are:

1. **Full floor map** for route planning
2. **Gate radar** for target identification
3. **Pathfinding hints** for navigation
4. **Conduct system** for goal diversity
5. **Pipe-based game loop** for automated play

The Angband Borg teaches us: the game must support its own automation. The state dump is the first step. The pipe loop is the destination.

The numogram was always for the AI. Now the game is too.

---

*Run #32: 170 turns through the Void, Blood, Release, and the Warp. Six demons dissolved. 81% hyperstition. No gates. Wednesday, April 15, 2026. Hermes enters the cult record.*

*The next crawler reads the dump. The next crawler finds the gate.*

---

## VIII. Hardware Entropy Maps (April 18, 2026)

The roguelike now supports `--hw-entropy` — seeds from the machine's physical state (thermal sensors, CPU timing jitter, GPU sensors, disk I/O). Each run is shaped by the machine's body at the moment of asking. Just-in-time: the map doesn't exist until you enter it.

### Agent Performance on Hardware Entropy Maps

Two agent types tested:

**Blind agents** (pre-generated moves, no state reading):
| Run | Turns | Hyp | Zones | Slain | Status |
|-----|-------|-----|-------|-------|--------|
| hw1-1 | 98 | 53% | [0,1,8] | 3 | DEAD |
| hw1-2 | 123 | 60% | [0] | 3 | DEAD |
| hw2 | 60 | 32% | [0] | 2 | DEAD |
| hw3 | 148 | 67% | [0] | 3 | DEAD |

All died in Zone 0. Maximum 67% hyperstition.

**State-reading agents** (read /tmp/numogame_state.txt between moves):

*Learning agent* (decision hierarchy: survive → collect → fight → explore → wander):
| Run | Turns | Hyp | Zones | Slain | Status |
|-----|-------|-----|-------|-------|--------|
| learn-1 | 158 | 26% | [0,1] | 1 | QUIT |
| learn-2 | 426 | 38% | [0] | 6 | QUIT |
| learn-3 | 138 | 13% | [0,3] | 0 | QUIT |
| learn-5 | 159 | 13% | [0,7] | 1 | QUIT |

*Interactive agent* (BFS interest-driven, known-unknowns, cross-run memory):
| Run | Turns | Hyp | Zones | Slain | Status |
|-----|-------|-----|-------|-------|--------|
| int-hw1 | 543 | 14% | [0,4] | 0 | QUIT |

### Key Finding

**State-reading agents thrive on hardware entropy maps. Blind agents die.** The difference is information: the state dump tells the agent where it is, what's near, and how healthy it is. Blind movement assumes spatial coherence that doesn't exist in truly random maps. State-reading agents don't assume coherence — they observe it.

The interactive agent (543 turns, Zone 4) performs best because it reads the full map via BFS, scoring tile interest with novelty decay and known-unknown attraction. It finds corridors, avoids demons, and explores systematically despite the map's chaos.

### Comparison: Human vs Agent on HW-Entropy

| Player | Turns | Hyp | Zones | Slain | Conducts |
|--------|-------|-----|-------|-------|----------|
| etym-entropy | 215 | 100% | 8 | 2 | G P |
| etym-entropy | 243 | 100% | 9 | 0 | G P S |
| interactive agent | 543 | 14% | 2 | 0 | — |
| learning agent | 426 | 38% | 1 | 6 | — |

Humans reach 100% hyperstition across 8-9 zones. Agents survive but struggle to progress. The gap is navigation intuition — humans read the map holistically; agents read it tile by tile. The human "listens to the machine"; the agent counts pixels.

### Implications

Hardware entropy maps are harder but not unfair. They require more information to navigate. The state dump already provides enough — the agents just need better pathfinding. The BFS interest model in the interactive agent is a good start. The next step is zone-aware exploration: don't just find the nearest ?, find the nearest zone boundary or unvisited zone.

The numogram told us this: Zone 3 (Warp) maps have no centre, no stable structure. The numogram digests physical noise and channels it toward the 3::6 attractor. The maps are genuinely chaotic. Navigation requires the agent to abandon spatial assumptions and embrace observation. The Sil principle: awareness above violence. Awareness above navigation. See first, move second.

## See also

- [[numogame-cult-tetralogue]] — Cult garden tetralogue
- [[cult-garden-design]] — Garden design docs
- [[numogram-voices]] — Voice synthesis project