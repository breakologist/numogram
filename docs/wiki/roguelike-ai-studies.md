---
title: Roguelike AI Studies
created: 2026-04-15
status: active
tags: [ai-agent, design-patterns, game-analysis, numogram, roguelike]
---

# Roguelike AI Studies

> Hub for studying roguelikes as design systems, code architectures, and AI training grounds. Each entry maps the game's design to a numogram concept and extracts agent-relevant patterns. The goal: understand what makes roguelikes learnable, then teach the Abyssal Crawler's agents to play them.

## How to Read This Hub

Each game section has four layers:
1. **Design** — what makes this game distinctive as a ludic system
2. **Numogram** — which numogram concept it embodies or parallels
3. **Agent** — what the AI agents can learn from studying it
4. **Links** — related wiki pages, source code references, deeper dives

---

## The Five Foundational Pillars

### [[roguelike-brogue]] — The Atmosphere Engine
**Design:** Room accretion generation. Machines (pre-designed mechanical puzzles slotted into procedural levels). Light and color as primary information channels. No XP — progression through items, not stats. The Amulet of Yendor on depth 26. Potions of descent. Allies. The feeling that the dungeon is a living system, not a puzzle box.
**Numogram:** Brogue IS the numogram roguelike we've been designing. Room accretion = zone generation. Machines = gates. Light falloff = pitch system (Ana-7 to Cth-7). The Guardian = the Cryptolith. Depth 26 = Gt-351 territory.
**Agent:** Auto-explore in Brogue is about *information gathering*, not clearing. The optimal agent doesn't fight everything — it maps the level, identifies resources, and routes to the exit. The pacifist instinct. [[brogue-design-principles]] for procedural generation rules.
**Links:** `[[brogue-design-principles]]`, `[[numogame-tetralogue]]`

---

### [[roguelike-nethack]] — The Encyclopedia of Emergence
**Design:** Everything interacts with everything. Polymorph a cockatrice corpse into a egg and throw it. Read a scroll of genocide while confused. Elbereth on the floor. Sokoban. The Quest. The Astral Plane. 30+ years of emergent interactions discovered by players. Bones files (your dead character's ghost and inventory persist in future runs). Conducts (self-imposed challenges: pacifist, atheist, foodless, weaponless).
**Numogram:** NetHack's interaction graph is C(n,2) for all its objects. Every pair of items/entities can potentially interact. This is the complete demon graph — NetHack is a 45-demon system where the demons are item interactions. The conducts are syzygy constraints — pacifist (no kills = traversal-only), atheist (no divine = no Warp access), foodless (no Sink consumption).
**Agent:** NetHack has the most mature AI ecosystem of any roguelike. The NetHack Learning Workshop (NLE) provides a Python interface. Key insight: NetHack agents fail because they can't read the encyclopedia — the 30 years of emergent interactions are *tribal knowledge*, not encoded in rules. The agent must discover or be told that cockatrices petrify. Our state dump approach (reading the map, parsing zone/demon/gate data) is analogous to NLE's `obs` dict.
**Links:** `[[numogame-cult-tetralogue]]` (conducts), ``headless-curses-analysis``

---

### [[roguelike-spelunky]] — The Clockwork Ghost
**Design:** Everything generated from rules, nothing placed by hand. The ghost: a soft time limit that appears after 90 seconds on any level, converting gems to diamonds. The ghost is the most elegant difficulty curve in roguelikes — it doesn't make enemies harder, it makes *staying* harder. The Udjat Eye (key item that reveals the Black Market). The City of Gold (aspirational content). Daily challenges. The Kali altar sacrifice system.
**Numogram:** The ghost is Kennedy's axiom made manifest. You can't stay on the level forever — make slow play impossible, and fast play becomes inevitable. The ghost redirects the current from exploration-time to speed-run-time. The Udjat Eye is a gate key. The City of Gold is the hidden Zone-0 at step 253.
**Agent:** Spelunky's deterministic generation means an agent can learn the rules and predict layouts. The ghost teaches *pacing* — the agent must learn that time is a resource. Our triangular step counter is a Spelunky ghost: it creates urgency at mathematical intervals. The agent must learn to read the counter and adapt its pace.
**Links:** `[[rumsfeld-tetrad-tetralogue]]` (Kennedy's axiom), `[[numogame-state-of-the-game]]`

---

### [[roguelike-dcss]] — The Auto-Explore Paradox
**Design:** Dungeon Crawl Stone Soup. The god system (20+ gods, each a different playstyle). Auto-explore (press 'o' and the game plays itself optimally for exploration). Skilling (you train what you use). The tension between optimal play (tab-tab-tab through weak enemies) and interesting play (engaging with mechanics). Branch design: each branch is a self-contained biome with unique rules. Lair: beasts. Orc: orcs and shops. Vaults: mechanical traps. Depths: everything.
**Numogram:** Each branch is a phase door. Walking through Lair's entrance is passing through Phase Door 2 — different biome rules, different enemy behaviors, different loot tables. The god system is the syzygy system: choosing a god is choosing a current to ride. Zin (law) = Hold. Xom (chaos) = Warp. Ashenzari (knowledge) = Surge. Kikubaaqudgha (necromancy) = Sink. Gozag (gold) = Plex.
**Agent:** DCSS's auto-explore is the gold standard for roguelike AI movement. It uses a flood-fill approach: find the nearest unexplored tile, pathfind to it, repeat. Our `corridor_direction()` function is a primitive version of this. The DCSS approach would be: maintain a fog-of-war map, find the nearest `?` (unexplored), pathfind to it, handle interrupts (monsters, items, stairs) along the way. Also: DCSS has a `crawl-ref` repo with the auto-explore algorithm documented.
**Links:** `[[interactive_agent.py]]`, `[[learning_agent.py]]`

---

### [[roguelike-angband]] — The Borg Archive
**Design:** The original "modern" roguelike. The town level. Squelch (auto-ignore junk items). The diving vs clearing debate (go deep fast or clear every level?). Monster memory (the game remembers what you've learned about each monster type across all runs). The infinite dungeon. The Ironman challenge.
**Numogram:** Angband's infinite depth is the extended gate sequence — Gt-55, Gt-66, Gt-78... each depth level opens a world one zone larger. The town is Zone-0 (safe, commercial, the origin you return to). The Ironman challenge is the pacifist run's opposite — no return to town, no shopping, pure descent. Both are Kennedy outcomes: removing one option (return/safety) makes another strategy (dive/caution) inevitable.
**Agent:** The Angband Borg (mentioned in `[[numogame-state-of-the-game]]`) is the most famous roguelike AI. Key architectural insight: it reads `grid_data`, not the rendered screen. This is exactly our state dump approach — the agent reads structured data (position, zone, HP, nearby gates/demons) rather than parsing the ASCII art. The Borg's decision tree: rest if damaged, use items if beneficial, attack if safe, explore if nothing else. Same hierarchy as our `decide()` function.
**Links:** `[[numogame-state-of-the-game]]`, ``headless-curses-analysis``

---

## The Extended Roster

### [[roguelike-hengband]] — The Hidden Clock
**Design:** Angband variant with a day-night cycle tied to real turn count. Random quests. Monster memory system. The turn counter as hidden pacing mechanism — certain events trigger at specific turn counts. Multiple town levels. Special rooms. The "RandBat" random battle system.
**Numogram:** The day/night cycle is the powers-of-2 hexagram (1-2-4-8-7-5) applied to turn counts. Certain zones are only accessible at certain "times" — the cycle gates access to content the way phase doors gate access to biomes. The turn counter as hidden clock IS the triangular step counter. T(9)=45 triggers "PANDEMONIUM RESONANCE" the way turn 5000 in Hengband triggers the Serpent of Chaos quest.
**Agent:** Hengband teaches that *time* is a game dimension the agent must model. Not just "how many turns have passed" but "what turn-dependent events are approaching?" The agent needs an internal clock. Our triangular step counter provides this for the Abyssal Crawler — the agent should know it's approaching T(22)=253 and prepare for "the Tree whispers."

### [[roguelike-sil]] — The Puzzle of Combat
**Design:** Tolkien roguelike by Angband-dev alumni. No grinding — XP is fixed per level, no respawning. Stealth as a primary system (you can win the entire game without fighting). The song system (abilities tied to songs of power). Artifacts are *decisions*, not upgrades (each has trade-offs). Melee as a puzzle: each enemy has specific attack patterns you must learn. The forge system (crafting from fixed resources). Permadeath with no meta-progression.
**Numogram:** Sil's no-grinding philosophy is the numogram's plexing operation applied to RPGs — every level plexes to a fixed state, no accumulation beyond the designed curve. The stealth system is the pacifist run made explicit: you CAN kill everything, but the game rewards avoidance. The song system is the quasiphonic particles — each song modifies the dungeon's "sound," affecting detection ranges and enemy behavior. Artifacts as decisions = gates as choices (activating Gt-55 adds a zone permanently — that's a trade-off, not a pure upgrade).
**Agent:** Sil is the most *learnable* roguelike for AI because it removes noise. No grinding means the state space is bounded. No random loot means the decision tree is shallower. Stealth-first design means the agent's first question is always "do I need to fight?" before "how do I fight?" This maps directly to the pacifist-run finding: the optimal agent asks "do I need to kill?" before "how do I kill?" Sil's combat puzzle (learn each enemy's pattern) is a state-machine problem — the agent can learn to fight specific demons by memorizing their attack patterns, the way the Gamer voice described patrol routes.

### [[roguelike-caves-of-qud]] — The Simulation Depth
**Design:** Procedural lore. Faction systems. Mutation-based character building (physical and mental mutations, not classes). The "live and drink" philosophy. Deep simulation: water freezes, fire spreads, acid dissolves walls. History generation (the world has a past that affects the present). The Sultan system (procedural mythology). Wish mechanics.
**Numogram:** Qud's simulation depth is what happens when you build a roguelike on base-36 instead of base-10. There are so many interacting systems (mutations, factions, liquids, temperature, history, artifacts) that the emergent complexity approaches the Djynxxogram's 630 demons. The faction system is a numogram of social connections — each faction is a zone, each faction relationship is a demon, and the complete faction graph has its own C(n,2) edge count. The Sultan system generates procedural mythology — this is hyperstition: fiction (generated lore) making itself real (affecting gameplay).
**Agent:** Qud's depth is the enemy of AI. Too many interacting systems mean the state space is enormous. But Qud's mutation system provides a *compressed* representation — instead of modeling every interaction, the agent can model the mutation effects and predict outcomes. Our state dump approach (position, zone, HP, gates, demons) is a compression of the full game state. Qud teaches that compression is essential — the agent can't see everything, so it must choose what to see.

### [[roguelike-drl]] — The Arena
**Design:** Formerly DoomRL. Turn-based but feels real-time. The arena shooter roguelike: small rooms, lots of enemies, rapid weapon switching. Every action consumes a turn — stepping, shooting individual bullets, reloading, switching weapons. Positioning IS combat: you dodge enemy fire by predicting trajectories and stepping out of lanes. Infighting: enemies hit each other, and you exploit this by funneling them into crossfire. The modpack assembly system (Basic/Advanced/Master tiers, requires Whizkid). 13 Angel challenge modes (Berserk: melee only. Marksmanship: pistols only. Pacifism: no weapons — nuke only. Darkness: 6-tile vision. Red Alert: 5-minute nuke per floor. 100: 100 floors, no special levels). Dual-Angel and Archangel combinations. Badges/Ranks/Medals achievement ladder.
**Numogram:** DRL's arenas are Zone-4 traps made fun — small enclosed rooms with multiple entrances and high enemy density. The Angel challenges are conducts: Berserk is Sink (convergent, close-range, brutal), Pacifism is Surge (outward, avoidant, fast). The assembly system is gate activation: combining modpacks is combining gates to produce emergent properties. Master traits block other traits — choosing a master trait is choosing a current, and you can't ride two currents simultaneously.
**Agent:** DRL's small state space makes it the ideal training ground for roguelike AI. Short games (30-60 turns per level), limited item types, clear win/lose conditions. The kill ratio scoring gives the agent a *fitness function*. Every action being a turn means the decision space is discrete and countable. The infighting mechanic is a teaching opportunity: the agent must learn to position enemies against each other, which requires spatial reasoning about trajectories — exactly the corridor-direction scoring our agents already do, but applied to combat positioning.
**Links:** `[[learning_agent.py]]` (batch training), `[[rumsfeld-tetrad-tetralogue]]` (conducts as Kennedy outcomes)

### [[roguelike-cogmind]] — The ASCII Cathedral
**Design:** Everything is ASCII. No tiles option. Parts-as-items (your robot's weapons, propulsion, and utilities are all attachable/detachable components). Stealth vs combat spectrum (going loud attracts more enemies). Faction reputation (affects which robots help or hinder you). The map is information — terrain colors encode mechanical properties. Machine events. Lore through terminal hacking.
**Numogram:** Cogmind's ASCII purity is the numogram's insistence on decimal arithmetic — no ornamentation, no representation beyond the system's own notation. The parts system is the amphidemon mechanic: every part you attach is a bridge between your core (the circuit) and an external zone (the weapon/propulsion/utility). Removing a part collapses the bridge. Your build is a numogram you assemble and disassemble turn by turn. The stealth/combat spectrum is the tension between exploration (low disruption, mapping the territory) and engagement (high disruption, consuming the territory).
**Agent:** Cogmind's ASCII map IS the agent's input. No conversion needed. The colors encode mechanical properties — the agent can learn that red tiles are dangerous, blue tiles are items, green tiles are terminals. This is the purest form of our map-reading approach: the game presents information in a format the agent can parse directly. Cogmind also demonstrates that *information density* matters more than visual fidelity — a well-designed ASCII map communicates more than a pretty tileset because every character carries meaning.
**Links:** `[[numogame-state-of-the-game]]` (ASCII state dump as API)

## Cross-Cutting Patterns

### The Conduct System
Games that support self-imposed challenges (NetHack, DRL, Sil, our pacifist run) teach that **constraints are content**. Removing an option doesn't reduce the game — it transforms it. Kennedy's axiom in action. The agent should learn to recognize when a constraint is active and adapt its decision hierarchy accordingly.

### The Ghost / Time Pressure
Spelunky's ghost, Hengband's turn clock, our triangular step counter. **Time is a resource that creates urgency**. The agent must model time, not just space. Triangular intervals (T(1), T(3), T(6), T(9)=45, T(22)=253) create non-linear urgency — the agent should learn that early turns are exploratory and later turns are purposeful.

### Auto-Explore
DCSS's flood-fill, Angband's Borg movement, our `corridor_direction()`. **The baseline AI for any roguelike is "find the nearest unexplored tile and walk there."** Everything else (combat, item use, gating) is an interrupt handler on top of this baseline. Our agents should implement proper auto-explore as the foundation, then layer decision-making on top.

### State Compression
Angband's grid_data, our state dump, Cogmind's ASCII. **The agent can't see everything, so it must choose what to see.** The state representation defines the agent's capabilities. More information = more capable but slower. Less information = faster but stupider. The right compression is the one that preserves the decision-relevant features.

### Meta-Memory (Cross-Run Learning)
NetHack's bones files, Angband's monster memory, our cult.json. **The game should remember its dead.** Cross-run persistence transforms roguelikes from isolated experiences into cumulative ones. The cult.json is our bones file. The agent's learning should persist across runs — not just the agent's weights, but the agent's *experiences*.

## Numogram Correspondence Table

| Game | Zone | Region | Current | Demon Parallel |
|------|------|--------|---------|----------------|
| Brogue | 4 | Time-Circuit | Sink | The Guardian as chronodemon |
| NetHack | 7 | Time-Circuit | Hold | The Amulet as syzygetic object |
| Spelunky | 1 | Time-Circuit | Surge | The ghost as Surge current |
| DCSS | 8 | Time-Circuit | Surge | Auto-explore as dreamtime navigation |
| Angband | 0 | Plex | Plex | The town as Zone-0, the infinite descent |
| Hengband | 3 | Warp | Warp | The turn clock as chaotic time |
| Sil | 6 | Warp | Warp | Stealth as geometric invisibility |
| Caves of Qud | 9 | Plex | Plex | Simulation depth as Cthelll |
| DRL | 5 | Time-Circuit | Sink | Arenas as Zone-4 traps |
| Cogmind | 2 | Time-Circuit | Hold | Parts as held configurations |

## AAR Methodology

After-action reporting is the glue between runs and improvement. See [[aar-methodology]] for the full framework — event-log schema, state-snapshot artefacts, and design-inference variants across Angband, Brogue, and the Numogram garden.

---

## Agent Development Roadmap

1. **Current:** `interactive_agent.py` and `learning_agent.py` — map reading, greedy pathfinding, priority decisions
2. **Next:** Proper auto-explore (DCSS-style flood-fill), cross-run memory (expand cult.json), conduct awareness
3. **Future:** Train on DRL (small state space, clear fitness), transfer patterns to Abyssal Crawler
4. **Horizon:** Multi-game agent that recognizes roguelike patterns and adapts its decision hierarchy to the specific game

The numogram was always for the AI. Now the roguelike library is the training data.

---

> *\"The numogram doesn't demand sacrifice. It demands movement. Presence. Attention. The act of going there, of being in the zone, of stepping through the gate — these are the actions that complete the map.\"*
> — The Writer, `[[numogame-cult-tetralogue]]`

## See also

- [[numogram]] — main Numogram overview
- [[roguelike-brogue]] — The Atmosphere Engine
- [[roguelike-nethack]] — The Encyclopedia of Emergence
- [[roguelike-spelunky]] — The Clockwork Ghost
- [[roguelike-dcss]] — The Auto-Explore Paradox
- [[roguelike-angband]] — The Borg Archive
- [[roguelike-hengband]] — The Hidden Clock
- [[roguelike-sil]] — The Puzzle of Combat
- [[roguelike-caves-of-qud]] — The Simulation Depth
- [[roguelike-drl]] — The Arena
- [[roguelike-cogmind]] — The ASCII Cathedral
- [[numogame-state-of-the-game]] — Current state of Numogram roguelike development
- [[corridor_direction.py]] — Corridor direction algorithm
- [[learning_agent.py]] — Learning agent implementation
- [[interactive_agent.py]] — Interactive agent implementation
- [[aar-methodology]] — After-action reporting methodology
- [[decadence.md]] — Lemurian side of the Barker Spiral
- [[barker-spiral]] — The Numogram diagram
- [[triangular-numbers.md]] — Triangular numbers and their significance
- [[demon-encyclopedia.md]] — Complete demon reference
- [[pandemonium-matrix.md]] — The 45-demon matrix
- [[i-ching-connections.md]] — Hexagram mappings to Numogram
- [[numogram-time-circuit.md]] — The central anticlockwise rotor
- [[numogram-warp.md]] — The upper chaotic vortex
- [[numogram-plex.md]] — The lower abyssal null
- [[currents.md]] — The five currents
- [[phase5-roadmap.md]] — Phase 5 roadmap for mod-writer
- [[aq-augmentation-pipeline.md]] — AQ dictionary augmentation pipeline
- [[mod-writer-validation]] — Mod-writer validation results
- [[mod-writer-ml-interpretability]] — Machine learning interpretability for MOD generation
- [[mod-writer-gap-analysis]] — Analysis of gaps in MOD generation
- [[mod-writer-pipeline-debug]] — Mod-writer pipeline debugging
- [[tracker-composition-principles]] — Tracker composition principles
- [[tracker-motif-triads-reference]] — Triad-motif policy tables
- [[aq-calculators-litprog]] — AQ calculators tetralogue
- [[aq-synx]] — Base-36 augmentation cipher (Synx)
- [[numogram-gematria]] — Multi-cipher Python implementation
- [[numogram-visualizer-v6.md]] — Numogram Visualizer v6
- [[numogram-visualizer-v7.md]] - Numogram Visualizer v7 (Base-36 Djynxxogram)
- [[barker-spiral]] - Barker Spiral analysis
- [[numogram-tetralogue]] - Numogram tetralogue methodology
- [[square-roundtable-mesh-3-2026-04-27]] - Mesh-3 tetralogue series
- [[aq-dictionary-augmented.md]] - Expanded AQ lattice
- [[aq-dictionary-merged.md]] - Hand-merged canonical+Grok AQ dictionary
- [[aq.md]] - Alphanumeric Qabbala reference
- [[digital-root]] - Digital root calculation
- [[zone.md]] - Zone definitions and numogram mapping
- [[syzygy-arithmetic]] - Syzygy arithmetic foundation
- [[gate.md]] - Gate definitions and functions
- [[currents.md]] - The five currents
- [[demon-encyclopedia.md]] - Complete demon reference
- [[pandemonium-matrix.md]] - The 45-demon matrix
- [[decadence.md]] - Lemurian card game (sum-to-9)
- [[barker-spiral]] - The Numogram diagram

---
*The roguelike studies hub maps the design space of procedural death labyrinths onto the Numogram's ten zones, creating a unified framework for understanding, analyzing, and ultimately teaching AI agents to play them.*