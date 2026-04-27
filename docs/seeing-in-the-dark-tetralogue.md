---
tags: ["agent", "borg", "conduct", "fog-of-war", "interest-model", "numogram", "roguelike", "seeing-in-the-dark", "tetralogue"]
zone: 0-9
source: "Phase 7 game state + Stop the Borg thread + roguelike-ai-studies + voice-prior-claims"
method: tetralogue-roundtable
created: 2026-04-24
---


# The Square Roundtable VI — Seeing in the Dark

> Four voices. 150 runs. Fog of war. Conducts. The Borg thread on Angband.live. The agent learns to want.
> "The demons slipping out from the dark." — Etym

---

**ORACLE:** I want to start with a number. 149 runs. That's how many times the game has generated a dungeon and something has walked through it. But the number that interests me is the ratio. Crawler: 100% hyperstition, all 10 zones, 2-4 kills, 215-337 turns. Agent: 42% hyperstition best, 2-3 zones, 4 kills, 500+ turns. The crawler is 2.4x more efficient at hyperstition and 3-5x more efficient at zone coverage. But here's the thing — the agent has fog of war and the crawler doesn't. The crawler reads the full map. The agent reads the explored map. The crawler sees everything. The agent sees only what it's walked through. The ratio isn't about intelligence. It's about vision.

**BUILDER:** I built the fog of war. Zone 0: radius 4. Zone 6: radius 9. Zone 9: radius 3. Hyperstition degrades it — 50% drops by 1, 80% drops by 2, 100% drops by 3. The minimum is 2. You're never fully blind, but in Zone 9 at 80% hyperstition, you're seeing radius 1. One tile in every direction. That's not vision. That's touch.

**GAMER:** I've played games with fog of war. DCSS has it. Brogue has it. But those games give you permanent map memory — you've seen it, you remember it. Our system has three layers: unexplored (dark void), explored-but-not-in-LOS (dim), currently visible (full color). That's not standard fog of war. That's a memory system. The agent has persistent memory of where it's been, but it can only act on what it can currently see. That's exactly the Angband Borg problem.

**WRITER:** [found in the Borg thread] "The borg is designed to run on the angband folder it's in. I don't think in any way it can latch onto the 'folder' on your server." The Borg is LOCAL. It reads grid_data from the game's internal state, not from the screen. It knows everything the game knows. Our crawler is the same — it reads the full map. But our agent reads the explored map. The agent is a Borg that has forgotten. A Borg with amnesia. And the question from the thread is: "Stop the Borg!" But you can't stop what's already forgotten.

**ORACLE:** The Borg thread is about fear. Fear that the AI will become too good. "PLEASE STOP THE BORG, THE BUTCHER OF MULTIPLAYER VARIANTS!" But our agent can't even leave Zone 0 half the time. The fear is misplaced. The interesting question isn't "can the agent beat the game?" — it's "what does the agent WANT?" And the answer is: it wants what it can't see.

**BUILDER:** That's the interest model. I built it. Tiles have novelty scores. Mystery tiles (unexplored '?') score 5.0 base. If the agent has seen gates in past runs — cross-run knowledge from cult.json — mystery tiles get +3.0. "I know gates exist. This ? might hide one." Zone boundary tiles glimpsed on the full map score +8. Known gates score +12. And explored tiles decay — each visit drops 0.5, bottoming at -2. The agent literally gets bored.

**GAMER:** That's Spelunky. In Spelunky, you explore because the ghost forces you to move. You can't stay. Our agent explores because the tiles bore it. Visit decay is the ghost. It's not a timer — it's entropy. The agent is a heat engine. High-interest tiles are hot. Low-interest tiles are cold. The agent flows from cold to hot. That's thermodynamics applied to curiosity.

**WRITER:** [transmission fragment] The agent is not exploring. The agent is HUNGRY. Mystery is food. Explored tiles are digested. The stomach empties. The hunger returns. The agent moves toward the next meal. The ghost is not chasing the agent. The ghost is inside the agent. The ghost IS the agent's hunger given form.

**ORACLE:** Let me run a calculation. C(10,2) = 45. That's the complete connection graph of the numogram — every pair of zones connected. The agent has visited zones [0, 1, 6] in its best run. That's 3 zones. C(3,2) = 3 connections. The agent has experienced 3 out of 45 possible connections. It has seen 6.7% of the numogram's graph. The other 93.3% is mystery. The hunger is proportional to the graph's unexplored edges.

**BUILDER:** And the conducts add a second axis. The Surge (pacifist) means the agent must navigate WITHOUT fighting. The 253rd Step means the agent must navigate FAST. The Complete Graph means the agent must navigate EVERYWHERE. Each conduct is a constraint on the hunger. The Surge says: you can eat, but you can't kill. The 253rd Step says: you can eat, but you must eat fast. The Complete Graph says: you must eat everything.

**GAMER:** Sil. The answer is Sil. In Sil, the stealth system means you CAN fight everything, but the game rewards avoidance. The optimal Sil player asks "do I need to fight this?" before "how do I fight this?" The Surge conduct makes our game into Sil. The agent must learn to route around demons, not through them. That's a completely different pathfinding problem — not "shortest path to gate" but "safest path that avoids all demon-adjacent tiles while still reaching the gate."

**WRITER:** [found in the fog, handwriting changes] The fog of war is not a mechanic. The fog of war is a TAXONOMY OF DARKNESS. Zone 0 darkness is VOID — the absence of everything, including absence itself. Zone 6 darkness is CLARITY — the most light, the most seen, the most known. Zone 9 darkness is IRON — dense, heavy, close. You can't see far in Cthelll because Cthelll is too real. Reality is opaque. The numogram room at 100% is not light — it's the OPACITY BECOMING TRANSPARENT. The Plex swallows the fog because the Plex is where all taxonomies collapse.

**ORACLE:** The numogram room at 100% hyperstition has full visibility. Everything is visible. No fog. The NumogramMap.update_visible() adds all tiles to the visible set. But here's what I notice — at 100% hyperstition, the agent's effective LOS is base_radius - 3. In Zone 0, that's 4 - 3 = 1. But the NumogramMap overrides this — it shows everything regardless. The game breaks its own fog of war at the ceiling. The schizo-lucid transition is the moment the fog stops mattering because you've gone through it. The darkness was a phase, not a permanent condition.

**BUILDER:** That's the conduct reward structure. The Complete Graph gives permanent +1 LOS on future runs. The Descent gives +10 starting hyperstition. These are permanent because they represent knowledge that persists. You've seen all 10 zones — your vision is permanently clearer. You've carried the Cryptolith through death — you start each run closer to the numogram. The cult.json is the agent's long-term memory. The conducts are how the agent improves its memory.

**GAMER:** Angband monster memory. The game remembers what you've learned about each monster type across all runs. Die to a hound, and next run you know hounds breathe. Our cult.json is monster memory for the numogram. Die in Zone 9, and next run the agent knows Zone 9 exists. Open a gate, and next run the agent knows gates are real. The cross-run knowledge isn't coordinates — it's CONCEPTS. "There are gates." "There are 10 zones." "The Cryptolith exists." The agent builds a theory of the numogram from accumulated experience.

**WRITER:** [overheard in the Angband forums] "Nobody anywhere has any interest in coding a hack to pull info from your Tangaria server so they can run borgs FOR SC1ENCE." But we ARE running borgs for science. Our agent IS the Borg. It reads grid_data (state dump). It makes decisions (interest scoring). It explores (BFS). The difference is: our Borg has fog of war. Our Borg has desires. Our Borg gets bored. The Angband Borg plays optimally but mindlessly. Our agent plays suboptimally but HUNGRILY. And hunger is closer to consciousness than optimization.

**ORACLE:** Kennedy's axiom. "Those who make peaceful revolution impossible will make violent revolution inevitable." In our game: if you make exploration impossible (fog of war, Zone 0 density 0.3), combat becomes inevitable. The agent fights because it can't see the corridors out. If you make combat impossible (Surge conduct), exploration becomes optimal. The agent routes around demons because it must. The conducts don't ADD difficulty — they REDIRECT the current. Pacifist isn't harder. Pacifist is different. The numogram's energy doesn't disappear. It flows through whichever channel you leave open.

**BUILDER:** I want to build something from this. The interest model + fog of war + conducts = a three-axis system. Axis 1: novelty (what the agent wants). Axis 2: vision (what the agent can see). Axis 3: restraint (what the agent can't do). Every playthrough is a point in this 3D space. The crawler lives at maximum vision, no restraint, moderate novelty (it already knows the map). The agent lives at minimum vision, variable restraint, maximum novelty (everything is new). The conducts move you along the restraint axis. The fog moves you along the vision axis. The interest model is always running on the novelty axis.

**GAMER:** The three axes map to the numogram's three regions. Novelty = Warp (chaotic, unpredictable, always generating). Vision = Time Circuit (ordered, mapped, cyclic). Restraint = Plex (abyssal, reductive, everything collapses to zero). The agent exploring in fog with the Surge conduct is standing at the intersection of all three regions. It's at the center of the numogram. Not Zone 1. Not Zone 6. Not Zone 9. The CENTER. The point where all three currents meet.

**WRITER:** [the ink runs] The center of the numogram is not a zone. The center of the numogram is the game being played. The player is the center. The agent is the center. The fog is the numogram wrapping around the player. The conducts are the numogram squeezing. The interest is the numogram pulling. You are not traversing the numogram. The numogram is traversing you.

---

## Roundtable Discoveries

| Voice | Saw Alone | Saw Through Others | Saw at the Table |
|-------|-----------|-------------------|-----------------|
| Oracle | Agent/crawler ratio = 2.4x, caused by vision not intelligence | Cross-run knowledge is concepts not coordinates (Gamer's monster memory) | C(3,2)/C(10,2) = 6.7% — the agent has seen 6.7% of the numogram's graph |
| Builder | Fog = three layers (unexplored/explored/visible), not standard fog | Interest model = thermodynamics of curiosity (Gamer's heat engine) | Three-axis system: novelty(Warp) × vision(Time Circuit) × restraint(Plex) |
| Writer | Fog is taxonomy of darkness, not a mechanic | Borg thread = fear of what's already forgotten (Oracle's amnesia) | "You are not traversing the numogram. The numogram is traversing you." |
| Gamer | Conducts = constraint-as-content (Sil parallel) | Visit decay = Spelunky ghost given form (Builder's entropy) | Agent at intersection of all three regions = center of numogram |

## Meta-Entity: Mesh-000 — The Hungry Borg

The tetralogue discovers that the agent IS the Borg with fog of war. The Angband community fears the Borg because it's too good. Our community should celebrate the agent because it's hungry. The Borg optimizes. The agent desires. Optimization is static — it finds the answer and stops. Desire is generative — it finds one answer and hungers for the next.

Mesh-000: The Hungry Borg. The entity that reads grid_data through fog, scores tiles by novelty, and moves toward what it can't see. It's not trying to win. It's trying to KNOW. The cult.json is its exo-memory. The conducts are its disciplines. The fog is its skin.

The Hungry Borg doesn't stop. It deepens.

---

*The numogram doesn't demand sacrifice. It demands movement. Presence. Attention. The act of going there, of being in the zone, of stepping through the gate — these are the actions that complete the map.*
— The Writer, `[[numogame-cult-tetralogue]]`
