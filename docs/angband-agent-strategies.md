---
title: "Angband Agent Design — Strategies from Conversation Analysis"
created: 2026-04-26
updated: 2026-04-26
source: "raw/Grok Angband conversation.md"
tags: [angband, roguelike, ai-agent, reinforcement-learning, tree-search, novelty, llm-augmented, diving, grinding]
status: active
---

# Angband Agent Design — Strategies from Conversation Analysis

**Source:** `raw/Grok Angband conversation.md` — dialogue on gameplay strategies and AI agent architectures  
**Scope:** Dive vs grind playstyles, RL agent design, tree-structured exploration, novelty-driven exploration (E3B), LLM-augmented decision-making, and practical Angband automation patterns.

---

## 1. Grinding vs Diving — Fundamental Strategies

In Angband (dungeon level 1 → 100, defeat Morgoth), two primary progression philosophies dominate:

| Strategy | Philosophy | Risk | Reward |
|---|---|---|---|
| **Grinding** | Thorough level clearing (XP, gold, drops, secrets) before descending | Very low per-level | Steady but slow; shallow-level farming |
| **Diving** | Rapid descent via stairs / Deep Descent scrolls | High per-move | Exponential scaling: deeper = 100× better loot/XP |
| **Chunked/Hybrid** | Dive fast on boring levels; clear selectively on high-value ones | Balanced | Consistent wins, widely recommended |

**Key insight:** Depth is the single most important factor — item quality and monster XP scale exponentially with dungeon level (DL).

### Grinding (Slow/Plodding)

**How it works:**  
Enter level → detect monsters/traps/stairs/objects aggressively → clear packs (orcs, wolves, uniques) → search walls for secrets → farm gold → only descend when overprepared (full resists, high HP, stocked consumables).

**Early-mid game:** Farm DL 10–30 for basics (Free Action, See Invisible, basic resists, stat potions). Deeper grinding happens in chunks (e.g., dive to DL 40, clear uniques, repeat).

**Pros:**  
- Extremely safe per level  
- Excellent for learning monster behaviors  
- Steady XP/gold/item gains  
- Minimizes "oh crap" moments from out-of-depth threats

**Cons:**  
- Time-intensive, can feel grindy  
- Shallower levels yield lower-quality loot/XP overall  
- More total turns → higher cumulative bad-luck risk (random one-shots, breeder explosions)

**Best for:** Beginners, control-focused players, permadeath-averse.

### Diving (Aggressive/Pure)

**How it works:**  
Descend as fast as possible — take every down-stairs (or Deep Descent scrolls), detect stairs/objects/monsters quickly, only fight high-value or isolated targets.

**Core rule:** Dive aggressively until you're genuinely worried about dying, *then* fight conservatively (ranged attacks, LOS abuse around corners, phase door/teleport escapes, stair dancing).

**Late-game refinement:** Recall only to town; re-dive on stairs for instant escape options. Discard weaker items to make room for deeper finds.

**Key tactics:**
- Early game: Stock basics in town (Phase Door, Cure potions, Recall scrolls, ranged ammo), then push hard
- Abuse detection to skip lethal packs; stay near stairs
- Fewer total moves = lower overall chance of fatal error, even if individual moves feel riskier

**Best for:** Experienced players or combat-heavy classes who can handle melee early.

### Chunked / Strategic Diving (Hybrid)

**How it works:**  
Combine rapid descent with mini-grinds. Dive fast on "boring" levels; explore/clear when you hit something interesting (vault, unique, valuable loot). Use consumables like =CON rings or stat potions instead of pure XP grinding for stats.

Switch modes dynamically based on depth, resists, and resources.

**Why it works:**  
Balances speed with safety. Deep levels yield vastly better returns, but you still need to capitalize on opportunities without becoming overconfident.

**Best for:** Most players seeking consistent wins. This is the meta for high-success play.

## 2. AI Agent Architectures for Angband

Three escalating approaches to building an autonomous agent:

### 2.1 Pure Reinforcement Learning (RL) Agent

**Approach:** Train end-to-end via RL (Stable-Baselines3, Ray RLlib). State = screen pixels / feature vector. Action space = movement/combat/consumable use.

**Challenge:** Angband's partial observability (fog of war) and long time horizons make pure RLsample-inefficient. Requires massive compute or clever reward shaping.

**When to use:** Research into emergent exploration strategies; benchmarking against human play-data.
### 2.2 Hybrid Rule-Based + Learning Agent

**Approach:** Use symbolic game knowledge for high-level strategy; RL or search for low-level tactics.

**Example pipeline:**
1. **High-level mode selection** (grind / dive / hybrid) via hand-coded rules or learned policy
2. **Low-level execution** — BFS/DFS for pathfinding, threat-weighted cost maps for tactical navigation
3. **Interest-driven exploration** — E³ (Explore-Exploit-Explain) or curiosity bonuses for novel states

**Why hybrid:** Angband has clear optimal-room-until-interest patterns; pure RLoften rediscovers these slowly. A hybrid agent converges faster and is more interpretable.
### 2.3 LLM-Augmented or Multi-Agent Setup (Modern Twist)

**Approach:** Use a large language model (via LangChain, MiMo-v2-Pro, or similar) for high-level reasoning:  
> "Assess if I should dive or clear this vault given current resists/HP/depth."

The LLM acts as a *strategic advisor* that can:
- Interpret partial information (item descriptions, monster lore)
- Plan multi-step routines (town trips, inventory management)
- Adapt strategy based on narrative experience (rare drops, unique kills)

**Integration pattern:** LLM evaluates state → outputs high-level action recommendation → lower-level execution layer (BFS / rule-following) carries it out.

**Advantage:** Can reason about qualitative factors that are hard to encode in numeric rewards (e.g., "this vault looks too dangerous without rDisen").

## 3. Reward Shaping for Strategy Emergence

**Grinding-friendly shaping:**
- Small positive reward per level cleared
- Bonus for killing high-XP packs
- Reward for finding secrets

**Diving-friendly shaping:**
- Large reward for each new depth reached
- Bonus for first unique kill
- Penalty for time spent on shallow levels

**Novelty-driven exploration (E³ / E3B):**  
Reward *information gain* or state novelty rather than task completion. The agent seeks states it hasn't seen before.

**Examples of emergent behavior:**
- **Shallow, repetitive orc-clearing** (classic grinding) if novelty reward favours frequent state changes
- **First deep descent** or **first unique kill** → sudden novelty spike → agent "gets interested" in diving
- Over time, the elliptical BFS + novelty curve naturally produces a dive-grind hybrid

**Edge cases & mitigations:**
- Overfitting to one race/class: randomize character creation each episode
- Compute cost: start with text-only features before full pixel/screen input

## 4. Tree-Structured Strategy Modes with Interest Boosts

**Approach B:** Explicitly add two (or three) high-level modes as root branches in your tree:

- **Grind Mode** — expand sub-tree with goals like "clear 80% of level" or "farm uniques"
- **Dive Mode** — sub-tree focuses on stair-finding, threat-avoidance, rapid descent
- **Town Mode** (optional) — sub-tree handles recall→sell→buy→rest→redive cycles

Each mode has an **interest boost** (priority multiplier) in the tree-scoring function. The agent selects branches by highest interest·feasibility.

**Why tree shaping helps:**  
Pure novelty favours diving long-term (deeper states = higher episodic diversity). Tree shaping gives more human-like hybrids early on by explicitly modelling alternating modes. It also makes curriculum learning easier: start with Grind Mode only, then gradually introduce Dive Mode.
## 5. How the Components Mesh

**Full pipeline sketch:**

1. **Per-turn BFS** (threat-weighted pathfinding) for tactical navigation  
   → Path cost = base_distance + threat_estimate × danger_coefficient

2. **E3B novelty score** per explored tile  
   → Reward = base_reward + novelty_weight × (1 / visit_count)

3. **MiMo / LLM evaluator** for high-level branch selection  
   → Given current state (depth, resists, HP, gold), score each strategy mode (grind/dive/town)

4. **Tree node scoring:**  
   `score(node) = BFS_feasibility × interest_boost + E3B_novelty + LLM_strategic_recommendation`

5. **Chunk cycle:** Town → Dive chunk → Asses risk → Recall when undergeared → Town → repeat

**Result:** The agent naturally oscillates between grinding (safe resets) and diving (progression), mirroring human hybrid play.

## 6. Core Town Behaviors & Inventory Management

**Priority order for town routines:**

1. **Sell** all junk / unneeded drops (use home stash for keepers)
2. **Buy** in this order:
   - ?Word of Recall (always stock 4–6)  
   - !Healing / !Extra Healing (bulk)  
   - !Cure Critical Wounds / !Restore Life Levels  
   - Stat potions (CON, STR, DEX, INT, WIS, CHR)  
   - Food/rations if low
3. **Rest** until full HP (or until store restocks)
4. **Home management:** Stash non-essentials in your house at a fixed location; don't carry everything

**Edge cases:**
- **Low gold:** Prioritize selling before buying; Black Market is expensive but has uniques
- **Full home:** Agent learns to drop junk or recall more often
- **Uniques in town?** (Rare, but possible in some variants) — treat as high-novelty combat event

## 7. Example Flow: One Chunk Cycle

```
Town phase:
  BFS to stores → sell junk → buy Recall/Healing/stat pots → home stash → rest

Dive phase:
  Rapid descent → BFS to nearest down-stairs (avoiding threats)
  If interesting vault/unique detected → switch to tactical clear mode
  Continue until HP low / key resists missing / inventory full

Recall phase:
  Use ?Word of Recall → back to town → repeat
```

The tree scores "Next chunk" (re-dive) highly after town because supplies + novelty reset combine to give it peak interest.

## 8. Implementation Sketch (Python)

```python
class ChunkTreeNode:
    mode: str          # "grind", "dive", "town"
    depth: int
    supplies_remaining: int
    novelty_score: float
    bfs_cost: float

    def interest_boost(self):
        if self.mode == "town" and self.supplies_remaining < 0.3:
            return 2.0   # low supplies = high interest in town
        if self.mode == "dive" and self.novelty_score > 0.8:
            return 1.8   # high novelty = encourage dive
        return 1.0

    def total_score(self):
        return (self.bfs_feasibility() *
                self.interest_boost() +
                self.novelty_score +
                llm_strategic_recommendation(self.state))
```

**Hermes/MiMo-v2-Pro prompt for tree scoring:**

```
Current state: [depth, HP, resists, inventory summary, gold].
We just recalled from a chunk. Evaluate town routine branch priority:
- Should we rest? (HP < 50%?)
- Should we buy? (missing resists, low consumables)
- Should we re-dive immediately? (supplies adequate, high novelty ahead)
Return: {mode: "town"|"dive", interest_boost: float, reasoning: str}
```

## 9. Resources to Get Started

- **Angband source & docs:** Official GitHub repository, readthedocs
- **Community:** angband.live forums, r/angband, oook.cz ladder (human play data archives)
- **RL frameworks:** Stable-Baselines3, Ray RLlib (parallel training)
- **Hermes integration:** `roguelike-auto-explore`, `roguelike-screen-zones` skills for state capture
- **Related wiki pages:**
  - `[[angband-agent]]` — Angband-specific agent techniques
  - `[[roguelike-auto-explore]]` — DFS/BFS exploration patterns
  - `[[numogram-rooguelike-design]]` — numogram topology → dungeon generation

## 10. Connections to the Numogram

This Angband design discussion maps cleanly onto numogram traversal concepts:

| Angband concept | Numogram analogue |
|---|---|
| **Diving** (rapid descent) | **Warp traversal** (accelerative upper loop, vortex folding) |
| **Grinding** (safe accumulation) | **Time-Circuit rotation** (stable zones 1–6, cyclic reinforcement) |
| **Chunked hybrid** | **Syzygy navigation** (3::6 current balancing chaos and grind) |
| **Chunk cycle** (town→dive→recall) | **Zone circuit** (exit→re-enter→recharge via gates) |
| **Novelty spike** (first unique kill) | **Gate breach** (Gt-n traversal, hyperstitional threshold) |
| **E3B exploration** | **Triangular syzygy walk** (self-avoiding, vortical) |
| **Tree-structured modes** | **Zone/region branching** (Time-Circuit / Warp / Plex) |

**Hyperstitional observation:**  
The optimal Angband agent (hybrid, chunked, novelty-aware) mirrors the numogram's own recommendation for traversal: neither pure dive nor pure grind, but *current-aware cycling* between modes based on zone-state and supply geometry.
