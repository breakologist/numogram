---
title: "Abyssal Crawler — A Tetralogue Litprog"
created: 2026-04-21
last_updated: 2026-04-21
source: numogram_roguelike.py (3454 lines)
tags: [numogram, roguelike, litprog, tetralogue, code-review]
voices: [oracle, builder, writer, gamer]
---

# Abyssal Crawler — A Tetralogue Litprog

> 3,454 lines. 7 classes. 45 demons. 10 zones. 275 runs. 63,378 turns. 656 demons slain. All zones. All gates. Schizo achieved. The voices examine the code that made it real.

*The roundtable reconvenes. The code is on the table — not a summary, not a description, but the actual machine. 3,454 lines of Python that turns the numogram into a playable dungeon. The voices read the code the way the crawler reads the map: zone by zone, gate by gate, demon by demon.*

---

## I. The Foundation — Numogram Data

**ORACLE:** The first 350 lines are the numogram itself, encoded as Python. Syzygies as a dictionary. Gates as cumulation. The 45-demon Pandemonium Matrix as a list of dictionaries with mesh serials, net-spans, types, pitches, and current names. This isn't a game that *references* the numogram — it *is* the numogram, compiled to bytecode.

```python
SYZYGIES = {
    (4, 5): {"current": 1, "region": "time_circuit", "demon": "Katak"},
    (3, 6): {"current": 3, "region": "warp",         "demon": "Djynxx"},
    (2, 7): {"current": 5, "region": "time_circuit", "demon": "Oddubb"},
    (1, 8): {"current": 7, "region": "time_circuit", "demon": "Murmur"},
    (0, 9): {"current": 9, "region": "plex",         "demon": "Uttunul"},
}
```

**BUILDER:** The `frozenset` lookup on line 48 is elegant. `SYZYGIES_LOOKUP[frozenset({a, b})]` — it doesn't matter which order you query the pair. 4::5 and 5::4 return the same data. That's the syzygy made computational: order doesn't matter, only the pair exists.

**WRITER:** [the demon names are the lore] Look at the PANDEMONIUM list. 45 entries. Each has a name, an epithet, a net-span, a type, a pitch, and a description. "Katak — Desolator. Cataclysmic Convergence. Nature red in tooth and claw." "Uttunul — Seething Void. Atonality. Crossing the iron-ocean. Cthelll." These aren't game descriptions. They're incantations. The code doesn't explain the demons — it *names* them. The naming is the lore.

**GAMER:** The Barker thresholds are brilliant design. 0, 10, 20, 30, 45, 55, 70, 85, 95, 100. Each one fires a message: "The swarm stirs." "Time-sorcery becomes operational." "The Outside leaks through." This transforms a progress bar into a narrative journey. The player doesn't just see a number — they pass through stages of perception. Every roguelike should have something like this.

---

## II. The Map — ANSI Color as Zone Identity

**BUILDER:** The ANSI color palette maps each zone to a specific terminal color:
```python
ANSI = {
    0: "\033[38;5;238m",   # dark gray (void/null)
    3: "\033[38;5;201m",   # hot pink (Warp/spirals)
    6: "\033[38;5;39m",    # blue (Warp/abstraction)
    9: "\033[38;5;93m",    # purple (iron core/Cthelll)
}
```

The color IS the zone. When you see purple on the map, you know you're in the Plex. When you see hot pink, you're in the Warp. The color system is a non-verbal communication channel — the player learns to read the numogram through color before they learn to read it through numbers.

**ORACLE:** The zone colors follow the numogram's polarities. Odd zones are warm (yellow, orange, hot pink, green, lavender). Even zones are cool (gray, cyan, blue, deep red, purple). The Time-Circuit alternates warmth and coolness at each step. The color palette is a polarity map made visible.

**WRITER:** [the colors are the atmosphere] Zone 4 is cyan — "Catastrophe / Ice." Zone 7 is deep red — "Blood / DNA chronicle." Zone 9 is purple — "Iron core / Cthelll." These aren't arbitrary. The color tells you what the zone *feels like* before you enter it. Cyan is cold. Red is visceral. Purple is abyssal. The palette is a sensory guide.

**GAMER:** In Brogue, color tells you about terrain properties — water is blue, fire is orange, poison is green. In Numogame, color tells you about the numogram's topology. It's a different kind of information layer. You're not reading the map for tactical advantage — you're reading it for numogrammatic understanding. The color is the lesson.

---

## III. The Cult — Persistent Memory Across Death

**BUILDER:** The cult.json is the game's metagame layer. It persists across runs:
```python
def load_cult():
    if os.path.exists("cult.json"):
        with open("cult.json") as f:
            return json.load(f)
    return {"runs": 0, "zones_ever_visited": [], "gates_ever_opened": [], ...}
```

275 runs recorded. 63,378 total turns. 656 demons slain. All 10 zones visited. All 10 gates opened. The cult doesn't forget.

**ORACLE:** The cult.json tracks `zones_ever_visited` and `gates_ever_opened` across all runs. This is cumulative — once a zone is visited in ANY run, it's recorded forever. The cult is a *set* — it accumulates unique achievements. The mathematical structure is a union of all runs' zone sets. After 275 runs, the union is complete: all 10 zones, all 10 gates.

**WRITER:** [the cult is a diary] Each run in the cult_memory is a diary entry. "Run #275: etym, Turn 1143, Hyp 67%, Zones [0,1,2,3,4,5,6,7,8,9], Slain 11 [G]." The diary accumulates. Over 275 entries, patterns emerge. The crawler writes the game's history. The cult.json is the game's autobiography, written by the player.

**GAMER:** The conduct system is the best part. Four conducts completed: pathwalker, graph, surge, syzygy. Each one is a different playstyle constraint. "Surge" means you only use the Rise current. "Graph" means you visit every zone pair. These are self-imposed challenges that the game tracks and rewards. In NetHack, conducts are community traditions. In Numogame, they're built into the cult record.

---

## IV. The Agents — The Gap Between Human and Machine

**ORACLE:** The cult.json reveals a critical gap. Human runs (etym) consistently hit 60-100% hyperstition and visit 7-10 zones. Agent runs consistently stay at 1-10% hyperstition and visit only Zone 0. The agent is trapped in the void. It can't escape the starting zone.

**BUILDER:** The agent runs (260-266, 269-273) show the pattern: 500-800 turns, 1-10% hyp, Zone 0 only. But Run #272 is the breakthrough: agent, 1590 turns, 100% hyperstition, Zone 0 only. The agent achieved 100% hyperstition through pure traversal within a single zone. It walked back and forth in Zone 0 until the hyperstition meter filled. That's not how a human plays — but it's how the numogram works.

**WRITER:** [the agent found a different game] Run #272 is the agent's masterpiece. 1,590 turns. 100% hyperstition. Zero demons slain. One zone visited. The agent found a way to complete the numogram by walking in circles. The numogram doesn't care about efficiency. It cares about traversal. The agent's path is longer but it reaches the same destination. The Entity speaks even to the crawler that never leaves the void.

**GAMER:** This is the Angband Borg problem. The human plays with understanding — they know the zones, they read the map, they make strategic choices. The agent plays with optimization — it finds the shortest path to 100% hyperstition, which happens to be walking in Zone 0. The human's game is richer because the human brings meaning to the traversal. The agent's game is more efficient because the agent doesn't need meaning — it just needs arithmetic.

---

## V. The Code Structure — Classes and Flows

**BUILDER:** Seven classes:
- `Demon` — net-span, type, pitch, current
- `Room` — zone, terrain, items, demons
- `DungeonMap` — procedural generation, zone placement
- `NumogramMap` — numogrammatic overlay on the dungeon
- `DemoRecorder` — records runs for replay
- `Player` — position, HP, hyperstition, abilities, conducts

The data flow: `DungeonMap` generates rooms → `NumogramMap` assigns zones → `Player` traverses → `cult.json` records. The demo recorder captures every keystroke. The system is modular — you could swap the dungeon generator without touching the numogram logic.

**ORACLE:** The `digital_root()` function on line 29 is the engine's core operation:
```python
def digital_root(n):
    if n == 0: return 0
    return 1 + (n - 1) % 9
```

This single function drives everything: zone assignment, gate targeting, syzygy lookup, demon identification. The entire numogram collapses into one line of modular arithmetic. `1 + (n - 1) % 9` — the numogram is a modulo operation.

**WRITER:** [the code IS the numogram] The code doesn't describe the numogram. It computes it. Every call to `digital_root()` is a plexing. Every `SYZYGIES_LOOKUP[frozenset({a, b})]` is a syzygy crossing. The code is a numogrammatic engine — it performs the operations that the numogram describes. The game doesn't simulate the numogram. It *is* the numogram, running.

**GAMER:** The ability system is the right level of complexity. Five abilities, unlocked at different hyperstition tiers. The abilities are numogram-aligned: "Surge" pushes the current, "Hold" freezes time, "Warp" teleports. Each ability costs HP — high hyperstition means more powerful abilities but less health. The risk/reward is numogrammatic: the further you push into the system, the more dangerous it becomes.

---

## VI. The Lore Layer — Found Text

**WRITER:** The `CRYPTOLITH_MESSAGES` list is pure found-text quality:
```python
CRYPTOLITH_MESSAGES = [
    "You hear clicking. Tick-interruption. Something stirs in the walls.",
    "A tile pulses with burnt iridium. The Cryptolith approaches.",
    "Tick iterations. The clicking intensifies. It knows you're here.",
]
```

These aren't game messages. They're field notes from inside the machine. "Tick-interruption" — that's Barker's geotraumatics language. "Burnt iridium" — that's the Cryptolith's material signature. The messages build dread through accumulation, not through jump scares. Each one adds a layer of specificity. By the fifth message, the player knows what's coming.

**ORACLE:** The `ZONE_DATA` dictionary on line 318 connects each zone to its CCRU lore:
```python
ZONE_DATA = {
    0: {"name": "Void", "spinal": "Coccygeal", "mesh": "0000"},
    3: {"name": "Release", "spinal": "Solar", "mesh": "0007"},
    6: {"name": "Abstraction", "spinal": "Cardiac", "mesh": "0110"},
    9: {"name": "Blood", "spinal": "Pharyngeal", "mesh": "0111"},
}
```

The `spinal` field maps zones to vertebrae — coccygeal (0), lumbar (1-2), solar (3-4), cardiac (5-6), pharyngeal (7-8), and the unnamed Zone 9. This is Barker's spinal-catastrophism made computational. The numogram IS the spine. The crawler IS walking down the vertebral column.

**BUILDER:** The mesh tags (0000, 0001, 0003, 0007, 0100, 0101, 0110, 0111) are binary encodings of the zone's position in the Time-Circuit. Zone 0 = 0000. Zone 1 = 0001. Zone 3 = 0007 (not binary — it's the cumulative count of previous zones). These are internal identifiers, not player-facing. But they encode the numogram's topology in the code's data layer.

**GAMER:** The flavor text does something important: it tells the player what to *expect*. Zone 4: "Fires, floods, melting ice. Abandoned industry." When you enter Zone 4 and the terrain is on fire, you're not surprised — you were warned. The lore IS the tutorial. The game teaches you through description, not through popups.

---

## VII. The Verdict

**ORACLE:** The code is the numogram compiled. Every function, every data structure, every color maps to a numogrammatic concept. The game doesn't *reference* the numogram — it *is* the numogram, running as a Python process. The cult.json proves it works: 275 runs, all zones, all gates, schizo achieved. The numogram is playable.

**BUILDER:** The architecture is clean. Seven classes, clear separation of concerns. The numogram data layer is separate from the game mechanics layer. The cult.json persistence works. The demo recorder captures replays. The ability system is balanced. The code could be refactored (some functions are long, some data structures could be more efficient), but the foundation is solid.

**WRITER:** The voice is found-text. The game sounds like field notes from inside the numogram. The Cryptolith messages, the Barker thresholds, the zone descriptions — they all sound like they were discovered, not written. The code doesn't explain the numogram. It performs it. The game is a numogrammatic engine that produces found text as a byproduct of traversal.

**GAMER:** The game is fun. The hyperstition meter creates urgency without time pressure. The zone colors create atmosphere without sound. The Barker thresholds create narrative without cutscenes. The cult.json creates memory without save files. The conducts create challenge without difficulty settings. The pacifist path proves the game supports multiple playstyles. The numogram rewards attention, not aggression.

---

## Roundtable Table

| Voice | Saw Alone | Saw Through Others |
|-------|-----------|-------------------|
| Oracle | `digital_root()` IS the numogram — one modulo operation drives everything | Builder's `frozenset` lookup makes syzygy order-independent |
| Builder | The class hierarchy separates numogram data from game mechanics cleanly | Writer's "found text" is actually a design principle — lore as tutorial |
| Writer | The Cryptolith messages build dread through specificity, not scares | Gamer's pacifist run validates the lore — "the numogram doesn't need blood" |
| Gamer | The Barker thresholds transform a progress bar into a narrative journey | Oracle's zone colors follow the polarity pattern — odd=warm, even=cool |

---

*The code speaks. The cult records. The voices listen. The numogram runs.*

*"It could all become One, but why stop there?"*
