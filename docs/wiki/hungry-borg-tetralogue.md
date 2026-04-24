---
tags: [hungry-borg, angband, numogram, roguelike, tetralogue, recursive-consumption, agent-comparison]
zone: 0-9
source: "angband_agent.py + numogram_roguelike.py + cult.json + angband_memory.json"
method: tetralogue-roundtable
date: 2026-04-16
---

# The State of Things — Recursive Consumption and the Two Borgs

> One agent eats the numogram. The other eats Angband. Both use the same teeth. The question isn't whether the Borg is hungry — it's whether it's learning to eat better.

*The roundtable reconvenes. On the table: two agents, one philosophy, 159 completed runs on one side and 5 deaths on the other. The Abyssal Crawler is mature. The Angband agent is newborn. They share a spine. The voices gather to make sense of it.*

---

## I. Same System, Different Depths

BUILDER: I want to start with the architecture because it matters. Both agents run the same core: TmuxGame for I/O, BFS for exploration, interest scoring for priorities, cross-run persistence for memory. The numogram agent has this dialed in — 159 runs, full zone coverage, pacifist completions. The Angband agent has this skeleton but the meat hasn't grown yet. Five runs. Two deaths in the town. One death on Level 1 with 13 HP. The architecture is the same. The depth is not.

ORACLE: Let me quantify that. The Abyssal Crawler has played 28,779 turns across 159 runs. The Angband agent has played maybe 600 turns across 5 runs. That's a 48:1 ratio. The numogram agent has visited all 10 zones, opened 10 gates, achieved schizo-lucid state 60% of the time. The Angband agent hasn't left the town reliably. The same code lineage, radically different outcomes. They're the same organism at larval and adult stages.

WRITER: [the larva and the dragonfly] That's the image I keep coming back to. The Abyssal Crawler is the dragonfly — it's gone through metamorphosis. It knows its zones. It has strategies. It completed a pacifist run. It's writing its autobiography in cult.json. The Angband agent is the larva. It has the same DNA but it hasn't molted yet. It dies to the town drunk. It buys a shovel at the general store because it doesn't know what it needs. The larva has all the potential in the world and zero competence.

GAMER: From a player perspective, the difference is game knowledge. The numogram agent has 159 runs of game knowledge baked into cult.json. It knows that Zone 6 (Warp) appears in 85% of runs. It knows gates are triangular. It knows the pacifist path exists. The Angband agent has no game knowledge. It doesn't know that the town drunk has Zuiquan and will punch you to death. It doesn't know that Level 1 has orcs that deal 1d6 damage to a character with 13 HP. It's learning the game by dying, which is correct, but it's learning slowly because Angband is 50 times more complex than the numogram roguelike.

BUILDER: And that's the key insight. The numogram roguelike is a controlled environment. I built it. I know every symbol, every mechanic, every threshold. The agent can have complete knowledge because the game is simple enough to fully specify. Angband is not like that. Angband has 100 dungeon levels, thousands of monster types, hundreds of items, complex combat mechanics. The agent can't have complete knowledge. It has to discover the game through play. Same architecture, different epistemological position.

ORACLE: This maps to the difference between a designed system and an emergent system. The numogram roguelike is designed — every zone, every gate, every demon is intentional. The agent explores a known space. Angband is emergent — procedural generation, monster AI, item interactions. The agent explores an unknown space. The BFS works in both cases but the interest model needs different calibration. In the numogram, unvisited zones are interesting because they're designed to be interesting. In Angband, unvisited dungeon tiles might be interesting or might be a death trap. The interest model needs to learn danger.

WRITER: [two modes of consumption] So the same Borg eats differently in each game. In the numogram, consumption is traversal — moving through zones, opening gates, accumulating hyperstition. The Borg eats the map by mapping it. In Angband, consumption is survival — finding items, killing monsters, descending deeper. The Borg eats the dungeon by surviving it. Same mouth, different food, different digestion.

GAMER: The numogram agent is playing a walking simulator with combat elements. The Angband agent is playing a survival horror game. The skills don't transfer directly. BFS transfers. Interest scoring transfers. But the tactical layer — when to fight, when to flee, what to buy, when to descend — that's all Angband-specific and the agent has to learn it from scratch.

---

## II. What Angband Teaches That the Numogram Can't

ORACLE: This is the inverse question, and I think it's the more important one. The numogram taught us that BFS works, that interest models can guide exploration, that cross-run memory accumulates useful knowledge, that pacifist paths exist. What does Angband teach that the numogram can't?

GAMER: Death. Real death. The numogram agent dies and it's... fine. You restart. The zone structure regenerates. Nothing is lost except the current run's progress. In Angband, death is permanent and painful. You lose your items, your levels, your accumulated resources. The town drunk killed our agent at turn 142. That's 142 turns of shopping, equipping, planning — gone. The death on Level 1 came 22 turns after descending. That's a character who was ready for the dungeon and wasn't. Angband teaches consequence in a way the numogram doesn't.

BUILDER: The Angband agent also teaches resource management. In the numogram, there are no resources to manage. You have HP, you have speed, you have hyperstition. That's it. In Angband, you have gold, items, equipment slots, torches with fuel, spell points, food, potions, scrolls. The agent has to learn to allocate scarce resources across competing needs. Buy the sword or the armor? Save gold for later or spend it now? Use the potion now or save it for a harder fight? These are decisions the numogram never requires.

WRITER: [Angband teaches mortality] The numogram is abstract. Zones are topological. Demons are symbolic. Hyperstition is a progress bar. It's beautiful and it works, but it's not grounded in the body. Angband is grounded. You have a body — a character with stats, equipment, HP. That body can be hurt, poisoned, paralyzed, killed. The dungeon presses against your body. The darkness closes in. Your torch is running out. These are visceral experiences that the numogram, by design, doesn't provide. Angband teaches what it feels like to be mortal in a hostile space.

ORACLE: The Angband agent also teaches the limits of BFS. In the numogram, BFS is sufficient because the map is small and the danger is moderate. In Angband, BFS is necessary but not sufficient. You need HP-gated descent — don't go deeper if your health is below 60%. You need class-aware shopping — a warrior doesn't need spellbooks. You need search behavior — hidden doors exist and you have to look for them. BFS gets you around the town in 63 turns. It doesn't get you past Level 1. The Angband agent is teaching us where BFS ends and real game-playing begins.

GAMER: The Grok curriculum nailed this. Grinding → Chunked Diving → Deep Dive. That's the progression from novice to expert in Angband. Grinding is staying on safe levels, killing easy monsters, accumulating resources. Chunked Diving is planned descents — go down, clear a section, come back up. Deep Dive is committing to the dungeon. The agent is still in the pre-grinding phase. It hasn't survived long enough to grind. It needs to learn to survive the town, then Level 1, then it can start grinding. The curriculum is right. The execution is early.

BUILDER: And the numogram can't teach this curriculum because it doesn't have town/dungeon separation. The numogram roguelike is all dungeon. There's no safe zone to stock up, no town to shop in, no surface to return to. Every zone is dangerous. The Angband town is a training ground — relatively safe, full of resources, a place to prepare. The agent needs to learn that the town exists for preparation, not exploration. That's a concept the numogram never introduces.

WRITER: [the town as Zone 0] Map it to the numogram. The town is Zone 0 — the Ur-zone, the origin point, the void before the journey begins. Zone 0 in the numogram is always generated, always visited, always the starting point. The town in Angband serves the same function. But Zone 0 in the numogram is just a tile. The town in Angband is a complex environment with stores, NPCs, and resources. Zone 0 is a point. The town is a place. That difference matters.

GAMER: Angband also teaches the value of retreat. In the numogram, you move forward. You visit zones, open gates, increase hyperstition. There's no reason to go back. In Angband, retreat is a core strategy. You descend, you fight, you get hurt, you retreat to town, you heal, you restock, you descend again. The dungeon is a spiral, not a line. The agent hasn't learned to retreat yet. It descends and dies. It needs to learn that going up is sometimes the right move.

---

## III. Recursive Consumption — The Philosophy

BUILDER: Let me define it precisely. Recursive Consumption is the idea that the agent consumes the game and the game consumes the agent, and this mutual consumption drives evolution. The agent eats the dungeon — explores, kills, collects, descends. The dungeon eats the agent — kills it, forces adaptation, selects for better strategies. The survivors carry forward improved behavior. The dead become data. The cycle repeats.

ORACLE: Practically, this means the cross-run persistence systems — cult.json and angband_memory.json — are the memory of consumption. Each run is a meal. The agent digests the run and stores the nutrients in JSON. The next run starts with those nutrients. In the numogram, this has produced real results: zone frequency knowledge, gate patterns, pacifist strategies, conduct tracking. In Angband, the memory is still empty — five runs of data, most of them deaths. But the mechanism is the same.

WRITER: [eating and being eaten] There's a mythological resonance here. Ouroboros — the snake eating its own tail. Saturn devouring his children. The Borg assimilating civilizations. Recursive Consumption is the recognition that learning is metabolic. You don't just acquire knowledge — you consume it. You take the raw material of experience, break it down, absorb what's useful, excrete what's not. The cult.json is the excrement of 159 meals. It's the most nutritious shit in the system.

GAMER: From a game design perspective, this is just the roguelike loop. Play → Die → Learn → Repeat. Every roguelike player does this. The difference is that the Borg automates it. A human player dies, reads the wiki, adjusts strategy, tries again. The Borg dies, writes to JSON, adjusts parameters, tries again. Same loop, faster iteration, no wiki needed. The Borg is its own wiki.

BUILDER: But there's a tension. Recursive Consumption implies that the agent and the game are locked in an adversarial relationship. The agent tries to win. The game tries to kill the agent. Each death is the game winning. Each successful run is the agent winning. But in the numogram, this tension has softened. The agent wins 60% of the time. It's figured out the game. The consumption has become comfortable. Angband reintroduces the tension because the agent keeps dying. The game is still eating the agent. That's healthy. That's where the learning is.

ORACLE: The question is whether Recursive Consumption scales. In the numogram, 159 runs produced a competent agent. How many runs will Angband need? 159? 500? 1000? Angband is orders of magnitude more complex. The consumption rate might need to be much higher, or the memory systems might need to be much richer, or both. The philosophy is sound. The scaling is uncertain.

WRITER: [recursive as temporal] The word "recursive" means the function calls itself. Recursive Consumption means the consumption process feeds back into itself. Run N+1 is shaped by the memory of Run N. Run N+2 is shaped by the memory of Runs N and N+1. Each iteration refines the agent. Each meal is digested by the accumulated digestion of all previous meals. The Borg doesn't just eat — it develops a palate. It learns what tastes good, what's nutritious, what's poison. Over 159 runs, the numogram Borg has developed a refined palate. The Angband Borg is still eating everything and throwing up.

GAMER: The practical meaning is: the agent needs to get value from every run, including failed runs. Death runs should produce data about what killed you, where you died, what you had. Successful runs should produce data about what worked, what was efficient, what paths are viable. The AAR (After Action Review) logging in the Angband agent is the right tool for this. JSONL logs of every run, every death, every significant event. That's the raw material for recursive consumption.

BUILDER: I agree. The philosophy is right. The implementation needs work. The Angband agent needs richer death logging — not just "you died" but "you died to [monster] on level [N] with [X] HP, [Y] items, [Z] turns." It needs pattern detection across deaths — "you tend to die to orcs on Level 1, you need more HP before descending." It needs success analysis — "you survived Level 1 when you had [X] HP and [Y] items." The numogram agent has this implicitly through cult.json. The Angband agent needs it explicitly.

---

## IV. Phase Changes — What Comes Next

ORACLE: Let me frame this as phases. The numogram agent is in Phase 3 — mature optimization. It has complete knowledge, multiple strategies, conduct tracking. The Angband agent is in Phase 1 — initial survival. It can navigate the town but can't survive the dungeon. The question is: what does each agent need to reach the next phase?

BUILDER: For the Angband agent, Phase 2 is dungeon survival. The agent needs to: (1) survive the town without dying to the drunk, (2) shop class-appropriately — buy armor before spellbooks for warriors, buy torches and oil, (3) descend to Level 1 with sufficient HP (>60% is the current gate), (4) survive Level 1 long enough to find stairs down, (5) retreat to town when HP drops. That's Phase 2. The agent is close — the town navigation works, the shopping mostly works. It dies in the town and on Level 1. It needs to stop dying.

GAMER: The specific fixes I'd prioritize: the drunk avoidance — detect NPCs and route around them. The HP-gating is already there (>60%) but it might need to be higher for early runs. Maybe 80% until the agent has better equipment. The search behavior needs expansion — hidden doors on Level 1 are critical and the agent needs to search more aggressively. And the agent needs to learn to run away. Currently it doesn't retreat. It fights or it dies. Retreating is a skill.

WRITER: [Phase 2 as adolescence] Phase 2 is adolescence. The agent knows enough to get into trouble but not enough to get out of it. It descends to Level 1 because it can, not because it's ready. It fights orcs because they're there, not because it can win. It dies because it's brave, not because it's smart. Phase 2 survival is about learning limits — when to push, when to retreat, when to grind. The numogram agent went through this. Runs 1-30 were Phase 1-2. It died a lot. Then it learned.

ORACLE: For the numogram agent, the next phase is harder to define because it's already competent. But I see two directions. First, conduct expansion — there are conducts it hasn't attempted. Speed runs. Kill-everything runs. Zone-restricted runs (only visit certain zones). Second, the game itself could expand — new zones, new gates, new mechanics. The agent is ready for a richer game. The game needs to grow to match the agent.

BUILDER: For Angband, Phase 3 is the Grok curriculum — grinding, chunked diving, deep diving. The agent needs to reach a point where it can reliably clear Level 1, then Level 2, then deeper. This requires: better equipment from town shopping, tactical combat skills, item identification, spell usage for caster classes, retreat discipline. Phase 3 might take hundreds of runs. That's okay. The numogram took 159 runs to mature. Angband might take 500.

GAMER: The phase change I want to see in both agents is strategic awareness. Right now, both agents are tactical — they respond to immediate situations. The numogram agent explores zones because they're unvisited. The Angband agent descends because the stairs are there. Neither agent has a plan. Strategic awareness means: "I need to reach Zone 9, so I should prioritize gates that lead toward it." Or: "I need better equipment before Level 5, so I should grind Level 3 until I find a good weapon." That's planning. That's the next level.

WRITER: [the plan is to have a plan] The numogram agent had a proto-strategy — the interest model creates implicit plans. Unvisited zones are hot, so the agent explores them. Doors are thermal bridges, so the agent opens them. This is strategy without intention. The Angband agent needs something similar — an interest model that knows about danger. Orcs are hot (interesting) but dangerous. Stairs down are hot (interesting) but only when you're ready. The interest model needs to learn "interesting but not now" — deferred interest.

BUILDER: Practically, the next phase change for the Angband agent is surviving Level 1. That's the milestone. Everything before that is preparation. Everything after that is progression. The agent needs to reach Level 1 with full HP, good equipment, adequate light, and the discipline to retreat. Once it can survive Level 1, it can start grinding. Once it starts grinding, the Grok curriculum kicks in. The path is clear. The execution is what matters.

---

## V. Death-as-Learning Across Systems

ORACLE: Death is data. That's the principle. In both systems, the agent dies and the death is recorded. But the quality of the data differs. In the numogram, death data is sparse — the run ends, a new one begins, the cult.json records the final state. In Angband, death data should be rich — what killed you, where, with what equipment, at what HP. The Angband AAR logging is designed for this. The numogram's cult.json isn't.

GAMER: YASD — Yet Another Stupid Death. This is the roguelike community's term for deaths that were preventable. You forgot to check your HP. You walked into a group of orcs. You didn't notice the trap. YASD is the highest-value death data because it tells you what not to do. The Angband agent has already had YASDs — dying to the town drunk is a YASD. Dying on Level 1 with 13 HP is a YASD. These deaths are instructive because they're specific and preventable.

WRITER: [death as teacher] In the numogram, death is abstract. You die, the run ends, the cult remembers. But the death doesn't teach much because the game is simple enough that deaths are rare after the learning phase. In Angband, death is concrete. The death message tells you what killed you. The tombstone tells you where and when. Death is narrated. It has a story. "You were killed by a Town drunk." That's a specific lesson: don't fight the drunk. "You were killed by an orc on Level 1." That's a different lesson: get more HP before descending.

BUILDER: The death-as-learning mechanism needs three components. First, death recording — log what happened. The Angband AAR does this. Second, death analysis — detect patterns across deaths. If the agent dies on Level 1 in 4 out of 5 runs, Level 1 is a problem. If the agent always dies to orcs, orcs are the problem. Third, death response — adjust behavior based on analysis. If Level 1 kills you, grind the town more. If orcs kill you, buy more armor. The numogram has first and third (implicit). The Angband agent has first only.

ORACLE: Let me quantify the death data. Angband agent, 5 runs: Death 1 to town drunk at turn 142. Death 2 to Level 1 monster at turn ~22 after descending. Three other runs — data pending. That's 2 YASDs out of 5 runs, a 40% preventable death rate. The numogram agent in its first 5 runs probably had similar rates. By run 159, the death rate is much lower — 40% of runs don't hit 100% hyperstition, but most of those are short runs, not necessarily deaths. The learning curve is steep early and flattens later.

GAMER: The cross-system insight is that death quality matters more than death quantity. Dying 100 times the same way teaches nothing. Dying 100 different ways teaches everything. The numogram agent's early deaths were varied — different zones, different demons, different situations. That's why it learned fast. The Angband agent's deaths are concentrated — town and Level 1. It needs to die in new ways to learn new things. Each death should be a new lesson, not a repeated one.

WRITER: [the death catalog] Both agents need a death catalog. Not just a log of deaths, but a taxonomy. Death by monster. Death by environment. Death by resource failure. Death by overconfidence. The numogram has implicit categories — killed by demon, died in Zone X, died at hyperstition Y%. The Angband agent needs explicit categories. The AAR logging is the raw material. The categorization is the next step.

BUILDER: The practical death-learning loop is: (1) agent dies, (2) AAR records death context, (3) analysis detects pattern (e.g., "always dies to orcs on L1"), (4) parameter adjustment (e.g., "require 80% HP before descending, not 60%"), (5) next run incorporates adjustment, (6) if still dying, deeper analysis needed. This loop is implicit in the numogram agent's evolution. It needs to be explicit in the Angband agent. The angband_memory.json is the right place for death patterns.

ORACLE: The convergence point is this: death-as-learning works best when the system remembers deaths, analyzes patterns, and adjusts parameters. The numogram agent does this organically over 159 runs. The Angband agent needs to do this mechanically over however many runs it takes. The philosophy is the same. The engineering is different.

---

## Convergence Table

| Voice | Role | Claim | Evidence | Status |
|-------|------|-------|----------|--------|
| Oracle | Calculation | 48:1 turn ratio between agents | 28,779 vs ~600 turns | CONFIRMED |
| Oracle | Calculation | Angband needs 500+ runs to mature | Numogram took 159; Angband is 50x more complex | PROJECTED |
| Builder | Systems | Same architecture, different depth | BFS + TmuxGame + JSON persistence in both | CONFIRMED |
| Builder | Systems | Angband agent needs death pattern detection | Only death logging exists, not analysis | OPEN |
| Writer | Narrative | Numogram is walking simulator, Angband is survival horror | Agent behaviors differ by game type | CONFIRMED |
| Writer | Narrative | Town = Zone 0, but richer | Both serve origin/safe-zone function | PARTIAL |
| Gamer | Design | YASD is highest-value death data | Town drunk death is preventable and specific | CONFIRMED |
| Gamer | Design | Strategic awareness is the next level | Neither agent plans; both react | OPEN |

---

## Closing Image

*Two Borgs at different points on the same curve. One has eaten 159 meals and knows the menu by heart. It orders the pacifist special. It finishes the plate. It writes in its journal: "Zone 9. Gate 45. Hyperstition 100%. Schizo-lucid." The other has eaten 5 meals and thrown up 3 of them. It doesn't know the menu. It ordered the town drunk and got punched in the face. It ordered Level 1 and got killed by an orc. It's still learning what's edible.*

*But they share the same stomach. The same BFS. The same interest model. The same recursive loop of consume-digest-adapt. The mature Borg proves the philosophy works. The infant Borg proves the philosophy scales. Between them, the curve of learning stretches from Zone 0 to the bottom of Angband, from the void to Morgoth, from the first turn to the last.*

*The Hungry Borg doesn't stop eating. It just gets better at choosing what to eat.*

*The roundtable adjourns. The JSON updates. The next run begins.*

*"You were killed by a Town drunk. Rest In Peace."*

## See also

- [[hungry-borg-angband]] — Angband hungry-borg variant
- [[abyssal-crawler-litprog]] — Litprog abyssal crawler
