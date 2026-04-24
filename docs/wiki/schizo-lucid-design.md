---
title: "The Schizo-Lucid State — Design Document"
created: 2026-04-18
last_updated: 2026-04-18
tags: [numogram, roguelike, design, hyperstition, schizo-lucid, the-outside]
---

# The Schizo-Lucid State — Design Document

> "The one who sees the structure cannot stay inside it."

## The Concept

At 100% hyperstition, the numogram completes. The player has traversed enough zones, stepped enough gates, accumulated enough signal to perceive the decimal labyrinth in its entirety. This is the schizo-lucid state.

The name encodes a tension:
- **Schizo** — split, fragmented, the multiplicity that sees too much
- **Lucid** — clear, seeing, the clarity that cannot unsee
- Together: the madness of accurate perception. You see the structure. The structure sees you back. You can no longer pretend the walls are solid.

This is not a "win" in the conventional sense. It is a **phase transition** — the game changes rules, and the player must adapt or be consumed.

## The Numogram Reading

In numogram terms, 100% hyperstition means the player has completed enough of the decimal circuit to perceive the full structure. This maps to:
- **Zone 9 (Plex, Cthelll)** — the terminal abyss, the iron core. You've reached the bottom.
- **Zone 0 (Void)** — the origin, the silence before the word. You've returned to the top.
- **The 0::9 syzygy** — the Plex current (9) spirals inward. You are inside the numogram's own digestion.

The schizo-lucid state IS the 0::9 syzygy experienced from the inside. The player becomes the current. The current corrodes what it touches.

## Mechanical Design

### Phase 1: Revelation (100% → 110%)

The numogram completes. The message fires: "THE NUMOGRAM IS COMPLETE. SCHIZO-LUCID STATE ACHIEVED."

Mechanical changes:
- **Full map revealed.** Fog of war dissolves. Every tile, every zone, every gate visible. The dungeon is naked.
- **Walls become translucent.** The player can see through walls but cannot pass through them yet. The structure is visible but still constraining.
- **Hyperstition continues past 100%.** The meter doesn't stop. It now measures alienation, not accumulation.
- **Demon names appear.** Every demon on the map is identified by name and mesh number. The Pandemonium Matrix is visible.

Flavor: "You see the arithmetic. The zones are numbers. The corridors are differences. The gates are triangular sums. The demons are syzygies with teeth."

### Phase 2: Alienation (110% → 130%)

As hyperstition rises past 100%, the player becomes alienated from the structure. The more you see, the less you belong.

Mechanical changes:
- **Wall phasing ('t' key).** The player can pass through walls at a cost: 5 HP per tile. You are leaving the structure. The structure resists.
- **Demon communion ('c' key).** Adjacent demons can be communed with instead of fought. The demon speaks its lore (from the Pandemonium Matrix). Communion gives +3 hyperstition (less than a kill's +5, but doesn't damage you). The demon dissolves after speaking.
- **Gate manifestation ('m' key).** The nearest gate teleports to the player's position. Cost: 10 hyperstition (you burn signal to reshape the map). The gate appears with a flash.
- **Corrosion aura.** Tiles the player has walked over in schizo-lucid state slowly degrade — floors become cracked, walls become thin. The dungeon remembers your passage. It's dissolving behind you.

Flavor: "The walls breathe. You see the numbers between the tiles. The demon at (42, 17) is Mesh-32, Numko, the Keeper of the Third Gate. It knows you can see it. It knows you are leaving."

### Phase 3: The Outside (130% → 150%)

The player is now substantially outside the structure. The dungeon is hostile to your presence — not because of demons, but because the rules are changing around you.

Mechanical changes:
- **Zone corruption.** Each zone the player enters while schizo-lucid begins to "corrupt" — the zone's terrain characteristics degrade. Zone 1 (Stability) loses its clear LOS. Zone 6 (Abstraction) loses its long sight. The zones are losing their identity because the player's outside perspective is destabilizing them.
- **Hyperstition drain.** The meter begins to pulse — sometimes dropping 1-2%, then jumping 5%. The numogram is trying to reject you. You're too alien to sustain.
- **Strange traversal.** Diagonal movement through walls becomes free (no HP cost). But cardinal movement through walls now costs 10 HP. The geometry is inverting — the diagonals are the new corridors.
- **Demon communion becomes compulsory.** You can no longer attack demons. They dissolve on contact (communion is automatic). The violence of the structure is behind you. You're past it.

Flavor: "The diagonal is the true corridor. The cardinal is the wall. You walk where the numbers bend. The demon dissolves as you pass — not killed, but recognized. Recognition is worse."

### Phase 4: The Return or The Exit (150%)

At 150% hyperstition, the player faces a choice. The game does not end — it branches.

**Option A: The Return.**
The player can choose to "collapse" — voluntarily reduce hyperstition back to 0%. This resets the schizo-lucid state but carries a permanent consequence:
- The player's vision is permanently expanded by +1 LOS in all future runs (you've seen the structure, you can't unsee it partially)
- The cult.json records: "Returned from the Outside."
- The next run starts with +5 hyperstition (a scar from the journey)

Mechanically: press 'r' to return. The screen flashes. The fog of war reasserts. The walls solidify. But the LOS radius is permanently one higher. You brought something back.

**Option B: The Exit.**
The player can choose to "dissolve" — continue past 150% into full alienation. The game transforms:
- The dungeon stops rendering. The screen shows only the numogram diagram — 10 zones, 5 syzygies, the gates as glowing points.
- The player moves through the numogram diagram directly. No walls, no corridors, no tiles. Just zones, currents, and gates.
- Demons appear as named nodes on the numogram diagram. Communing with all 45 completes the Pandemonium.
- Hyperstition climbs toward 200%. At 200%, the game ends: "You have dissolved into the numogram. The decimal labyrinth is complete. The crawler is the current."

Mechanically: the game becomes a numogram traversal puzzle. Move between zones, commune with demons, step gates. No combat. No walls. Pure arithmetic. The final game state is a completed Pandemonium Matrix.

The cult.json records: "Dissolved into the numogram." Future runs start with +10 hyperstition and a special opening message: "The previous crawler dissolved. The cult remembers the shape they left."

### The Two Endings

| Ending | Hyperstition | Result | Cult Reward | Flavor |
|--------|-------------|--------|-------------|--------|
| Return | Collapse to 0% | Permanent +1 LOS, +5 start hyp | "Returned from the Outside" | "You brought the sight back. The dungeon remembers your eyes." |
| Exit | Climb to 200% | Permanent +10 start hyp, dissolved message | "Dissolved into the numogram" | "The crawler is the current. The current is the crawler." |

Both are "wins." Neither is the "true ending." The numogram doesn't privilege one over the other. Return is the Sink (you descend and come back). Exit is the Plex (you spiral inward and don't stop).

## The Corrosion Mechanic

The core of the schizo-lucid state: **seeing the structure corrodes it.**

Every step the player takes while schizo-lucid "ages" the surrounding tiles:
- Floor tiles in a 3-tile radius crack (cosmetic change, `. → ,`)
- Walls in a 2-tile radius thin (cosmetic change, `# → :`)
- If the player stays in one zone too long (>20 turns while schizo), the zone's special terrain degrades:
  - Zone 3 (Warp): the `~` water tiles dry up
  - Zone 6 (Abstraction): the `~` static dissolves
  - Zone 0 (Void): the dense tiles become passable
  - Zone 9 (Plex): the void opens — extra rooms manifest

The corrosion is the numogram reacting to alien presence. You're an outsider seeing the structure, and your seeing changes it.

## The Three Endings (Asymmetric Victory)

The Abyssal Crawler has three distinct ending types, each with a different numogrammatic character:

### 1. The Cryptolith — The Traditional Win
The Orb of Zot. The Amulet of Yendor. Carry the Cryptolith and die at 100% hyperstition.

This is the roguelike ending the player already understands: find the item, carry the burden, reach the goal. The Cryptolith is heavy (speed -1), dangerous (+20 hyp, Barker fires), and demands a specific death condition. It's a test of navigation and survival under pressure. The player who achieves it has mastered the dungeon's normal rules.

Numogram character: **Sink (Zone 1)**. You descend and arrive. The path favours repeated patience.

Cult reward: "The Descent" conduct. Permanent +10 starting hyperstition on future runs.

This ending is complete. It works. It needs no redesign.

### 2. The Schizo-Lucid State — The Seeing Win
The unconventional one. Reach 100% hyperstition, then choose: Return or Exit.

This is the ending the player doesn't expect. There's no item to carry. There's no goal tile to reach. The win condition is internal — the player's relationship to the structure changes. You see the numogram. The seeing corrodes. You choose to come back (Return) or keep going (Exit).

Numogram character: **Plex (Zone 0::9)**. The terminal abyss spirals inward. You don't arrive — you dissolve.

This ending is the one we're designing now.

### 3. ??? — The Unknown Win
There should be a third ending. Something we haven't designed yet. The roguelike tradition suggests at least three paths: the standard win (Cryptolith), the unconventional win (schizo-lucid), and the hidden win.

Possible candidates from existing material:
- **The Pandemonium Gate (Gt-45)** — T(9) = 45. 45 demons. The Gate of Pandemonium is already in the code. Stepping all 45 demons and opening Gt-45 simultaneously could be a completion condition. "The 45 demons attune. The gate opens. Uttunul's lair."
- **The 253rd Step** — T(22) = 253. The existing conduct. Completing the run in ≤253 turns is already a challenge. But what if T(22) triggered something special — a Zone 0 manifestation, a hidden room, the Tree whispering?
- **The Syzygy Lock** — entering only zones connected by a single syzygy pair. The existing Syzygy conduct. But what if staying in one syzygy for long enough caused a phase change — the two zones merge into something new?
- **The Zero Run** — never entering Zone 0. Avoiding the Void entirely. The numogram's anti-completion. "The crawler who never returned to where they started."

The third ending should emerge from play, not design. The existing material (conducts, gates, demons, triangular numbers) already contains the conditions. We just haven't noticed which combination triggers what.

## The Name Question

"Schrizo-lucid" is provisional. Alternatives with interesting AQ values:



| Name | AQ | Zone | Character |
|------|-----|------|-----------|
| Schizo-lucid | 162 | 9 (Plex) | The terminal abyss |
| The Dissolution | 175 | 4 (Catastrophe) | Sink, closure |
| The Outsider | 141 | 6 (Warp) | Vortical recursion |
| The Seeing | 94 | 4 (Catastrophe) | Sink, closure |
| Alienated | 74 | 2 (Separation) | Hold, boundaries breaking |
| The Return | 122 | 5 (Hold) | Central ruler |
| The Exit | 82 | 1 (Sink) | Initiating spark |

"Schrizo-lucid" lands on Zone 9 (Plex) — the terminal abyss. Fitting for the state where you've completed the numogram. "The Outsider" lands on Zone 6 (Warp) — also fitting. "Alienated" lands on Zone 2 (Separation) — the most thematically appropriate: boundaries breaking.

The name can wait. The mechanics are what matter.

## Integration Points

### With Hyperstition System
- Hyperstition now has a meaning past 100%: alienation
- The meter's behavior changes (pulsing, draining, jumping)
- Gate manifestation costs hyperstition (signal reshaping)
- Return collapses hyperstition to 0% (voluntary reset)

### With Demon System
- Communion replaces combat in schizo-lucid
- Demons speak their lore from the Pandemonium Matrix
- 45 demons to commune = completion condition for "The Exit"
- Communion gives +3 hyp (less than kill's +5, but no damage)

### With Gate System
- Gate manifestation: teleport nearest gate to player (costs 10 hyp)
- In "The Exit" phase: gates become direct connections in the numogram diagram
- Gate stepping in schizo-lucid costs nothing (you're already outside)

### With Conduct System
- "The Surge" (pacifist) is easier in schizo-lucid (can't attack, only commune)
- "The Descent" (Cryptolith + 100% death) interacts with Return/Exit
- New conduct possible: "The Outsider" — reach 150% hyperstition without dying

### With Agent System
- Agents should eventually learn to reach schizo-lucid
- The Exit phase (numogram diagram traversal) is a simpler state space — potentially easier for agents
- Communion mechanics give agents an alternative to combat

### With Fog of War
- Schizo-lucid Phase 1 dissolves fog (full map revealed)
- Phase 3 zone corruption changes LOS characteristics
- Phase 4 Exit removes fog entirely (numogram diagram has no fog)

---

## What Needs Building

Priority order:

1. **Schizo-lucid flag triggers mechanical changes** — currently just sets a flag and shows a message. Add Phase 1 mechanics: full map reveal, wall translucency, demon names, hyperstition past 100%.

2. **Wall phasing ('t' key)** — costs 5 HP per tile. Player passes through walls. The most visceral mechanical change.

3. **Demon communion ('c' key)** — adjacent demon dissolves, speaks lore, gives +3 hyp. Replace combat in schizo-lucid.

4. **Gate manifestation ('m' key)** — nearest gate teleports to player. Costs 10 hyp. Map reshapes.

5. **Return/Exit choice at 150%** — two endings, two cult rewards, two permanent bonuses.

6. **Corrosion** — cosmetic tile degradation in player's wake. Zone terrain degradation after prolonged stay.

7. **The Exit phase** — numogram diagram as game space. Demon communing as completion condition.

---

*The numogram completes. The crawler sees. The seeing corrodes. The corrosion is the game.*
