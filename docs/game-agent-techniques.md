---
tags: ["llm", "ai-agent", "exploration", "game", "roguelike", "technique"]
created: 2026-04-15
source: "Research on AI agents playing games — emulator-based RL, LLM game agents, heuristic borgs, curiosity-driven exploration"
---


# Game-Playing AI Agents — Techniques and Landscape

> Hub for researching how AI agents play games. Covers emulator-based RL, LLM game agents, heuristic borgs, and curiosity-driven exploration. Companion to [[roguelike-ai-studies]] (design patterns) — this page covers the *how*, that page covers the *what*.

## The Interface Determines Everything

Every game-playing agent faces the same fundamental question: **what does the agent see?** The interface between game and agent determines what's possible. Three paradigms:

### 1. Pixel-Based (Vision)
- Agent sees: raw frame buffer (screenshots, pixel arrays)
- Decision method: CNN/encoder → RL policy, or vision LLM → reasoning
- Projects: PyBoy-RL, Stable-Retro, Claude/Gemini Plays Pokemon
- Strengths: universal (any game), no game-specific parsing
- Weaknesses: high-dimensional, slow, requires massive training

### 2. Structured Data (State)
- Agent sees: parsed game state (glyphs, stats, inventory, messages)
- Decision method: heuristic rules, or structured RL on tensor representations
- Projects: Angband Borg (grid_data), NLE (glyphs + stats + messages), **our agents** (state dump)
- Strengths: fast, interpretable, low-dimensional
- Weaknesses: requires game-specific parser, fragile to state format changes

### 3. Text-Based (Language)
- Agent sees: natural language description of game state
- Decision method: LLM reasoning (zero-shot or few-shot)
- Projects: GPT/Claude/Gemini Plays Pokemon (screenshot → vision LLM → text action), NLE + LLM (2024 paper)
- Strengths: generalizable, can reason about novel situations, no training required
- Weaknesses: slow (API calls), expensive, context window limits, hallucination

**Our current approach** is Structured Data (paradigm 2). The state dump parses the ASCII map into tiles, zones, gates, demons, HP, hyperstition. The interest model scores tiles by novelty. BFS finds the most interesting reachable target. This is closest to the Angband Borg.

**The opportunity** is adding Text-Based (paradigm 3). The state dump is already text. Feed it to a local LLM (Hermes-4-14B, qwen2.5) with the game rules in the system prompt. The LLM reasons about what to do. The interest model becomes the LLM's "curiosity" — it doesn't need to be hand-coded.

---

## The Landscape

### Emulator-Based RL

| Project | Platform | Games | Interface | Notes |
|---------|----------|-------|-----------|-------|
| **stable-retro** (Farama Foundation) | NES, SNES, Genesis, Game Boy, more | Hundreds | Frame buffer + RAM | Fork of OpenAI gym-retro. Standard toolkit for retro game RL. |
| **PyBoy-RL** | Game Boy | Mario, Kirby | Frame buffer | Clean Python emulator with RL hooks. |
| **PySNES** | SNES | Any SNES game | Frame buffer | Designed for AI training, Python interface. |
| **Serpent.AI** | Any | Any | Frame buffer + plugins | "Use any video game as a deep learning sandbox." |
| **Nintendo-NES-Ai-Agent** | NES | Any NES game | Frame buffer | Complete setup + training + visualization. |

**Key insight:** These all use pixel input. Massive training data, slow convergence. Works for simple games (Atari), struggles with complex ones (RPGs, roguelikes).

### LLM Game Agents (the 2024-2025 wave)

| Project | Game | Model | Interface | Result |
|---------|------|-------|-----------|--------|
| **Claude Plays Pokemon** | Pokemon Red | Claude (Anthropic) | Screenshots → vision | Streamed on Twitch. Made progress but struggled with navigation. |
| **Gemini Plays Pokemon** | Pokemon Red | Gemini (Google) | Screenshots → vision | Similar approach. Also on Twitch. |
| **GPT Plays Pokemon FireRed** | Pokemon FireRed | GPT-4/OpenAI | Screenshots → vision | GitHub: Clad3815. Live web dashboard. Autonomous real-time play. |
| **NLE + LLMs** (arxiv 2024) | NetHack | GPT-4, Claude | NLE structured obs → text | Zero-shot. Promising generalization but far from heuristic agents. |
| **BALROG benchmark** (UCL, 2024) | NetHack, Baba, others | LLM/VLM | Varies | Benchmark for vision+reasoning+planning agents on roguelikes. |
| **Multi-agent Pokemon** (arxiv 2025) | Pokemon Red | Multi-LLM | Screenshots + goals | One agent generates goals, another optimizes battles. |

**Key insight:** The Pokemon agents are "vision LLM → reasoning → action." They work because Pokemon is relatively simple (turn-based, small map, few choices per turn). Roguelikes are harder — more choices, more consequences, partial observability.

**The arxiv paper finding:** NetHack LLM agents (2024) show that LLMs can reason about novel situations (unseen monsters, unknown items) better than trained RL agents. But they're slower and more expensive. The hybrid approach — LLM for planning, heuristic for execution — might be optimal.

### Heuristic Bors (No ML)

| Project | Game | Interface | Decision Method | Notes |
|---------|------|-----------|-----------------|-------|
| **Angband Borg** | Angband | grid_data (internal state) | Heuristic rules + priority tree | The OG. Plays for score. "Stop the Borg" thread = too good for multiplayer. |
| **NetHack bots** | NetHack | Various | Heuristic rules | Community-built, many variants. Some quite good. |
| **DCSS auto-explore** | DCSS | Game internals | Flood-fill (Dijkstra map) | Built into the game. Gold standard for roguelike exploration. |
| **Our agents** | Abyssal Crawler | State dump (parsed ASCII) | Interest BFS + priority rules | Novelty scoring, cross-run memory, fog of war. |

**Key insight:** Heuristic borgs are still competitive with ML agents for complex roguelikes. The Angband Borg hasn't been beaten by any RL agent. Structure beats pixels for grid-based games.

---

## Core Techniques

### 1. Dijkstra Maps (Flood-Fill Distance Maps)

The foundation of roguelike AI navigation. Compute distances from every tile to a goal set. Use for:
- **Auto-explore:** goal set = unexplored tiles. Walk toward nearest.
- **Threat avoidance:** goal set = dangerous tiles (monsters, traps). Walk away from.
- **Item retrieval:** goal set = items. Walk toward nearest.
- **Exit finding:** goal set = stairs/gates. Walk toward nearest.

**Implementation:** BFS from all goal tiles simultaneously. Each pass adds +1 distance to neighbors. Result: distance map where each tile knows how far it is from the nearest goal.

**Our usage:** `find_most_interesting_target()` is a Dijkstra map with a custom cost function. Instead of uniform distance, the cost is interest (novelty). Shortest path to most interesting tile. This is the numogrammatic twist on the standard technique.

**Source:** Josh Ge (Grid Sage Games) popularized Dijkstra maps for roguelikes. The technique predates AI — it's used for monster pathfinding too.

### 2. Interest/Novelty Scoring (Curiosity-Driven Exploration)

Instead of "go to nearest unexplored tile," score tiles by how interesting they are. Factors:
- **Visit decay:** tiles you've walked over lose interest. Each visit drops score by some amount. Eventually a tile is boring.
- **Type bonuses:** gates > zone markers > floors > corridors > walls.
- **Cross-run knowledge:** "I know gates exist from past runs (cult.json). This ? might hide one."
- **Known-unknowns:** tiles glimpsed on the full map (gate positions, zone boundaries) but not yet explored.
- **Demon kill sites:** "the blood remembers."

**This is our key innovation over the Angband Borg.** The Borg optimizes for survival and score. Our agent optimizes for *understanding*. The agent wants to know what's behind the door more than it wants to survive. That's closer to how a human plays.

**Academic parallels:**
- **ICM (Intrinsic Curiosity Module):** Pathak et al. 2017. Agent gets reward for states its world model can't predict. Prediction error = curiosity.
- **RND (Random Network Distillation):** Burda et al. 2018. Agent gets reward for states a random network finds surprising. Novelty = curiosity.
- **E3B (Elliptical Episodic Bonuses):** Henaff et al. 2022. Inverse state visitation counts as exploration bonus. Efficient in hard-exploration environments.
- **NovelD:** Zhang et al. 2021. Scales intrinsic reward by visitation count. Prevents the agent from re-visiting the same "interesting" state.
- **MOTIF (2024, ICLR):** Learns intrinsic rewards from LLM preferences. Uses Llama 2 to judge whether a state is interesting.

**Our interest model is a simplified version of E3B + visit decay.** We track visit counts per tile and decay interest with familiarity. We add domain-specific bonuses (gates, zone boundaries, demon kills) that an RL agent would need to learn from experience.

### 3. State Representation (What to See)

The agent can't see everything. What it sees determines what it can do.

| Representation | What's Visible | Agent Capability |
|----------------|---------------|-----------------|
| Full map | Everything | Optimal routing, no exploration needed |
| Explored map | Tiles ever visited | Auto-explore meaningful, fog of war matters |
| Visible map (LOS) | Current line of sight only | Must plan with incomplete info, most realistic |
| Local map (21×21) | Surrounding area | Purely reactive, no long-term planning |
| Text description | Natural language summary | LLM reasoning, most general |

**Our state dump provides four layers:** full map (backward compat), explored map (`?` for unexplored), visible map (LOS-filtered), and local map (21×21 around player). The agent reads the explored map by default. This is the right abstraction — the agent has memory (explored tiles) but limited vision (only current LOS).

**The fog of war makes auto-explore meaningful.** Without fog, the agent just reads the full map and pathfinds optimally. With fog, the agent must *discover* the map through movement. Exploration becomes an intrinsic goal, not just a means to an end.

### 4. Cross-Run Memory (Meta-Learning)

The agent learns across runs, not just within them.

| Project | Cross-Run Memory | What Persists |
|---------|-----------------|---------------|
| Angband Borg | Monster memory | What it learned about each monster type |
| NetHack | Bones files | Dead player's ghost + inventory in future runs |
| Our agents | cult.json | zones_ever_visited, gates_ever_opened, max_hyperstition |

**Our approach:** The agent reads cult.json at init. It doesn't remember coordinates — it remembers *concepts*. "Gates exist." "There are 10 zones." "The Cryptolith exists." This creates motivation without specific knowledge. "I know there's a gate somewhere. I will explore until I find one."

**The key distinction:** cross-run memory should be **semantic** (what exists) not **episodic** (where things were). Specific coordinates change every run. Concepts persist.

### 5. Conduct Systems (Constraints as Content)

Self-imposed challenges that transform the game:
- **NetHack conducts:** pacifist, atheist, foodless, weaponless, illiterate
- **DRL Angel challenges:** Berserk (melee only), Pacifism (no weapons), Darkness (6-tile vision), 100 (100 floors)
- **Our conducts:** Surge (zero kills), 253rd Step (≤253 turns), Complete Graph (all 10 zones), Descent (Cryptolith + 100% death), Syzygy (single current)

**Agent relevance:** Each conduct transforms the decision hierarchy. Pacifist removes the "fight" branch. Speedrun prioritizes stairs over exploration. Complete Graph forces full map coverage. The agent must adapt its priority tree to the active conduct.

### 6. LLM as Decision Engine

Feed game state as text to an LLM, get back an action. No training required.

**Architecture:**
```
Game → State Dump (text) → LLM (system prompt + rules + state) → Action → Game
```

**Advantages:**
- Zero-shot: works on any game without training
- Reasoning: can handle novel situations (unseen enemies, unknown items)
- Explainable: the LLM can explain WHY it chose an action

**Disadvantages:**
- Slow: API calls add latency (seconds per turn)
- Expensive: token costs for long state descriptions
- Context window: can't hold full game history
- Hallucination: LLM might "see" things that aren't there

**Our opportunity:** The state dump is already text. The game rules are documented. A local LLM (Hermes-4-14B, qwen2.5) could receive the state dump + game rules + cult.json memory and reason about the next action. The interest model could be replaced by LLM curiosity — "what would be most interesting to explore next?"

**Hybrid approach (recommended):** LLM for high-level planning ("should I go to Zone 6 or pursue the gate?"), heuristic for low-level execution ("walk toward the most interesting tile"). The LLM sets goals, the interest BFS executes them.

---

## The Roguelike Agent Spectrum

| Level | Technique | Example | Our Agents |
|-------|-----------|---------|------------|
| 0 | Random walk | Random keypresses | ❌ Left this behind |
| 1 | Corridor following | "Go down longest corridor" | ✅ `corridor_direction()` (v1) |
| 2 | BFS auto-explore | "Find nearest unexplored tile" | ✅ BFS with blacklist (v2-3) |
| 3 | Interest-driven explore | "Find most interesting tile" | ✅ `tile_interest()` + visit decay (v4) |
| 4 | Fog-aware explore | "Explore with limited vision" | ✅ Explored map only (v5) |
| 5 | Conduct-aware explore | "Explore within constraints" | ✅ Conduct system hooks (v5+) |
| 6 | LLM-planned explore | "LLM sets goals, BFS executes" | 🔜 Next step |
| 7 | RL-trained explore | "Neural net learns from experience" | 📋 Future |
| 8 | Multi-agent explore | "Agents cooperate/compete" | 📋 Far future |

We're at level 5. The next step (level 6) is adding LLM planning on top of the heuristic execution. This is the hybrid approach the NLE paper suggests.

---

## Links

- [[roguelike-ai-studies]] — Design patterns mapped to numogram zones
- [[numogame-phase-7]] — Technical summary of fog of war, conducts, agent iterations
- [[seeing-in-the-dark-tetralogue]] — Four voices discuss the agent's hunger, fog of war, conducts
- [[numogame-state-of-the-game]] — Earlier design document + Angband Borg analysis
- `interactive_agent.py` — Current agent (interest BFS + cross-run memory)
- `rogue_agent.py` — Rogue (classic) agent (tmux-based, BFS + interest scoring)
- `learning_agent.py` — Batch runner with state parser and decision engine

## Key Papers

- NLE: "The NetHack Learning Environment" (Kuttler et al., 2020) — Meta FAIR. The academic benchmark.
- BALROG: "Benchmarking Agent LLM and VLM Reasoning on Games" (UCL, 2024) — LLM/VLM benchmarks on roguelikes.
- "Playing NetHack with LLMs" (2024) — Zero-shot LLM agents on NLE. Promising but behind heuristic agents.
- MOTIF: "Intrinsic Motivation from Artificial Intelligence Feedback" (ICLR 2024) — Learns curiosity from LLM preferences.
- ICM: "Curiosity-driven Exploration by Self-supervised Prediction" (Pathak et al., 2017) — Prediction error as curiosity.
- E3B: "Exploration via Elliptical Episodic Bonuses" (Henaff et al., 2022) — Inverse visitation counts.
