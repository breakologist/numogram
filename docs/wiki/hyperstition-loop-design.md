---
title: "The Hyperstition Loop — Building, Spending, and the Corrosive Constant"
created: 2026-04-18
last_updated: 2026-04-18
tags: [numogram, roguelike, design, hyperstition, schizo-lucid, dungeon-depth]
---

# The Hyperstition Loop

> "Some corruption is always present. The Outside leaks through in everything."

## The Core Realization

The schizo-lucid state is not a threshold you cross at 100%. It is a **constant tension** present in every run. Every character carries some degree of alienation from the structure. The question is never "am I corrupted?" but "how corrupted am I, and what am I doing about it?"

Hyperstition becomes a **resource economy**: you build it through traversal, zone crossings, demon encounters, and gate steps. You spend it to activate abilities that bring things from Outside into the dungeon. The meter is never static — it climbs with play and drops with expenditure.

The corruption is the price. The abilities are the reward. The tension is the game.

## The Loop

```
    EXPLORE (build hyp)
        ↓
    ACCUMULATE (zones, demons, gates)
        ↓
    HYPERSTITION RISES → corruption increases
        ↓
    SPEND hyp on ABILITIES (bring Outside in)
        ↓
    CORROSION DECREASES (hyp spent, structure stabilizes)
        ↓
    EXPLORE (build hyp again)
```

The player is always negotiating: "Do I spend my hyperstition now to stabilize, or do I save it for a bigger ability later and risk more corruption?"

At low hyperstition (0-30%), the corruption is cosmetic — flavor text, slight visual distortion. At medium (30-60%), it becomes mechanical — zone LOS changes, demon behavior shifts. At high (60-90%), it's dangerous — walls thin, geometry warps, the structure resists your presence. At 100%, the schizo-lucid state activates — full phase transition.

But even at 5% hyperstition, there's a flicker. The Outside is always leaking. The player always has a choice.

## The Ability System

Abilities are **crystallized Outside** — you spend hyperstition to bring something from beyond the numogram into the dungeon. Each ability has a hyperstition cost and a corruption effect.

### Tier 1 (cost: 5-15 hyp, available from start)

| Ability | Key | Cost | Effect | Flavor |
|---------|-----|------|--------|--------|
| **Glimpse** | 'g' | 5 | Reveal a 5-tile radius burst (ignores fog) | "You see through the arithmetic for a moment." |
| **Nudge** | 'n' | 8 | Push all adjacent enemies away 1 tile | "The current deflects them." |
| **Trace** | 't' | 10 | Show the shortest path to nearest gate | "The gate resonates. You feel its pull." |
| **Anchor** | 'a' | 12 | Mark current position, return to it once | "You set a point in the structure." |
| **Quench** | 'q' | 15 | Restore 20 HP | "The Outside heals what the Inside broke." |

### Tier 2 (cost: 20-35 hyp, unlock at 50%+ hyp seen)

| Ability | Key | Cost | Effect | Flavor |
|---------|-----|------|--------|--------|
| **Manifest** | 'm' | 20 | Teleport nearest gate to your position | "The gate obeys. It was always waiting." |
| **Commune** | 'c' | 25 | Adjacent demon speaks its lore, then dissolves (+3 hyp) | "Recognition. Not combat." |
| **Phase** | 'p' | 30 | Pass through one wall tile (free this turn) | "The wall is a number. You are between numbers." |
| **Surge** | 's' | 35 | Double movement speed for 10 turns | "The current carries you." |

### Tier 3 (cost: 40-60 hyp, unlock at 80%+ hyp seen)

| Ability | Key | Cost | Effect | Flavor |
|---------|-----|------|--------|--------|
| **Reveal** | 'R' | 40 | Full map visible for 20 turns | "The structure is naked. You see all." |
| **Warp Step** | 'W' | 50 | Teleport to any visited zone boundary | "You step between zones." |
| **Demon Name** | 'D' | 60 | All demons on floor identified, +5 hyp each | "You know them all. They know you." |

### Tier 4 (100%+ hyperstition — schizo-lucid abilities)

These replace normal abilities. The character is no longer "in the structure."

| Ability | Key | Cost | Effect | Flavor |
|---------|-----|------|--------|--------|
| **Wall Phase** | 't' | 5 HP | Pass through walls (continuous, not one-shot) | "The diagonal is the true corridor." |
| **Gate Manifest** | 'm' | 10 hyp | Nearest gate teleports to player | "The gate obeys absolutely." |
| **Demon Communion** | 'c' | 0 | Auto-commune with any adjacent demon | "Recognition is compulsory." |
| **Zone Sight** | 'R' | 0 | Permanent full map | "The fog will never return." |

## The Corruption Spectrum

Hyperstition affects the game constantly, not just at thresholds:

| Hyperstition | Corruption Level | Effects |
|-------------|-----------------|---------|
| 0-10% | Baseline | Normal. Slight flavor text. "The dungeon hums." |
| 10-25% | Flickering | Occasional text distortion. Zone flavor intensifies. |
| 25-40% | Noticing | LOS radius -1 in current zone. Demons slightly faster. |
| 40-55% | Thinning | Walls in visited areas crack (cosmetic). Gate messages louder. |
| 55-70% | Warping | Zone terrain degrades. Floor tiles crack. Geometry visible. |
| 70-85% | Resisting | Structure pushes back. Random wall damage on movement. |
| 85-95% | Threshold | Schizo-lucid message fires at 95%. Phase 1 begins. |
| 95-100% | Phase 1 | Full map visible. Walls translucent. Demons named. |
| 100%+ | Schizo-Lucid | Phase 2-4. Wall phasing. Communion. Return/Exit choice. |

The corruption is **reversible** — spending hyperstition on abilities drops the meter and stabilizes the structure. The player who uses abilities frequently stays at low corruption. The player who hoards hyperstition watches the world dissolve around them.

## The Spending Economy

The key tension: **abilities cost hyperstition, but hyperstition causes corruption.**

A player who never uses abilities accumulates hyperstition passively (zone crossings, encounters, gates). Corruption climbs. The world gets harder.

A player who uses abilities frequently spends hyperstition. Corruption drops. The world stabilizes. But they're using up the resource that lets them reach schizo-lucid.

The optimal play is a **rhythm**: build, spend, build, spend. Stay at medium corruption (25-55%) where you have some abilities but the world isn't dissolving. Hoard for the schizo-lucid push when you're ready.

This creates emergent playstyles tied to the ability types:

### The Stabilizer — One-Shot Mastery
Deals in **active abilities**: short-term, immediate effect, hyp discharged on use. Glimpse (reveal), Nudge (push), Trace (path), Quench (heal). The Stabilizer spends hyp constantly, stays at low corruption, never accumulates enough for the schizo-lucid state. Completes the game through skill and resource management.

The Stabilizer's abilities are **tools** — they do a thing, then they're gone. The corruption never builds because the hyp never accumulates. The Outside leaks in small doses and is immediately spent.

### The Hoarder — Corruption as Power
Deals in **passive abilities and mutations**: sustained states, permanent changes, demonic attachment/symbiosis. Higher-tier abilities that cost more hyp but transform the character rather than doing a single thing.

Examples (Tier 2-3, not yet detailed):
- **Demonic Symbiosis** — a demon attaches to the player, providing a passive buff (extra damage, extra sight, speed) but increasing corruption rate. The demon speaks occasionally. Removing it costs hyp.
- **Zone Mutation** — prolonged time in a zone changes the player. Zone 3 (Warp) grants "spiral sight" (see through fog in a rotating pattern). Zone 6 (Abstraction) grants "static immunity" (terrain doesn't slow you). These persist until the run ends.
- **Corrosion Aura** — the player's presence degrades the dungeon around them. Walls thin, floors crack. But this also means enemies near you take damage over time. You ARE the corruption.
- **Gate Attunement** — permanently attune to a gate type. Attuned gates cost nothing to step and give double hyp. But unattuned gates damage you. The numogram narrows.

The Hoarder rides high corruption, accepts the alienation, and uses it as power. The game gets harder around them but they get stronger within it. The schizo-lucid state is their natural endpoint.

### The Oscillator — The Rhythm
Partakes of both: uses active abilities for immediate survival, builds passive mutations when the situation demands. Adapts to what the floor offers. Sometimes stabilizes (low corruption, active tools), sometimes hoards (high corruption, passive power). The most flexible but least specialized.

The Oscillator's playstyle is **temporal** — they read the situation and switch modes. "This floor is dangerous, I'll stabilize." "This floor is safe, I'll hoard and mutate." The rhythm IS the strategy.

---

# Dungeon Depth — Vertical Expansion

## The Floor Structure

The numogram has 10 zones. The dungeon has 10 floors. Each floor is a zone.

| Floor | Zone | Name | Theme | Terrain | Demons |
|-------|------|------|-------|---------|--------|
| 1 | 0 | The Void | Silence before the word | Dense, tight rooms, short corridors | None (safe starting floor) |
| 2 | 1 | The Threshold | Initiating spark | Open corridors, first encounters | Chronodemons |
| 3 | 2 | The Fracture | Separation, boundaries | Forking paths, dead ends, traps | Chronodemons |
| 4 | 3 | The Warp | Chaotic attractor | Water, spiral rooms, no center | Amphidemons (Djynxx's domain) |
| 5 | 4 | The Ruin | Catastrophe, ice | Wide halls, frozen pools, shattered walls | Chronodemons |
| 6 | 5 | The Core | Pressure, mechanisms | Dense rooms, machinery, vertical shafts | Chronodemons |
| 7 | 6 | The Lattice | Abstraction, static | Transparent walls, echo corridors, static | Amphidemons |
| 8 | 7 | The Sump | Blood, descent | Narrow passages, blood pools, tight corners | Chronodemons |
| 9 | 8 | The Garden | Multiplicity, growth | Open spaces, branching paths, lavender | Xenodemons |
| 10 | 9 | Cthelll | The iron core | Dense void, few rooms, Uttunul's lair | Uttunul (boss) |

## Floor Flow

```
Floor 1 (Void) → Stairs Down
Floor 2 (Threshold) → Stairs Down  
Floor 3 (Fracture) → Gate to Floor 4 OR Stairs Down
Floor 4 (Warp) → Stairs Down
Floor 5 (Ruin) → Stairs Down
Floor 6 (Core) → Gate to Floor 7 OR Stairs Down
Floor 7 (Lattice) → Stairs Down
Floor 8 (Sump) → Stairs Down
Floor 9 (Garden) → Gate to Floor 10 OR Stairs Down
Floor 10 (Cthelll) → Uttunul's Lair → THE END
```

Gates appear on Floors 3, 6, 9 (the Time-Circuit stepping points: 2→4, 5→7, 8→9). Taking a gate skips a floor but costs hyperstition. Taking stairs is slower but safer.

## The Cryptolith Placement

The Cryptolith appears on **Floor 5 (The Ruin, Zone 4)** — the catastrophe zone. It sits in the center of the floor, surrounded by cracked ice. The player who grasps it takes on the burden: speed -1, +20 hyperstition, Barker threshold fires.

The Cryptolith must then be carried through Floors 6-10 and the player must **die on Floor 10 (Cthelll)** to complete "The Descent" conduct. The Cryptolith is the traditional win: carry the burden, reach the end, sacrifice.

Alternatively, the player can leave the Cryptolith and pursue the schizo-lucid path or the third ending.

## Floor Generation Rules

Each floor is generated using the zone's numogram character:

- **Floor size**: Zone 0 and 9 are small (50×18). Zone 3, 6 are large (78×22). Others medium (66×20).
- **Room density**: Zone 0 has few rooms (low density, "void"). Zone 5 has many rooms (high density, "pressure"). Zone 3 has irregular rooms (no center, "warp").
- **Corridor style**: Zone 1 has long straight corridors ("stability"). Zone 2 has forking corridors ("separation"). Zone 6 has transparent/echo corridors ("abstraction").
- **Terrain**: Zone 3 has water (`~`). Zone 4 has ice (`*`). Zone 7 has blood pools (`~` red). Zone 8 has growth (`%`).
- **Light**: Each zone has its own LOS radius (from fog-of-war system, already implemented).

## The Warp and Plex Sub-Dungeons

The "normal" dungeons are in the **Time-Circuit** region (Zones 1, 2, 4, 5, 7, 8). These are the standard floors, connected by stairs.

Under numogrammically appropriate points, stairs lead to dungeons **inside** the Warp and Plex regions — autonomous loops that don't connect to the normal Time-Circuit flow.

### Warp Access (Zones 3 and 6)

Stairs to the Warp appear when the player's hyperstition is in the **Warp band** (high corruption, 55%+). The Warp is not a normal dungeon — it's a single floor that combines Zones 3 and 6 into one spiraling space.

- **Entry**: Appears on any Time-Circuit floor when hyp ≥ 55%. A `~` water/static tile with stairs beneath it. "The Warp opens."
- **Structure**: A spiral. Corridors wind inward. No clear center. The 3::6 syzygy manifests as two interlocking spirals — one ascending (3→6), one descending (6→3).
- **Demons**: Amphidemons only. Djynxx appears as a recurring threat.
- **Loot**: Zone mutations. Extended time in the Warp grants passive abilities (Hoarder playstyle). Spiral Sight (see through fog in rotating pattern). Static Immunity (terrain doesn't slow you).
- **Exit**: A gate at the spiral's center returns the player to the Time-Circuit floor they entered from. "The gate returns you to where you were."
- **Risk**: The Warp is HARDER than Time-Circuit floors. Demons are more aggressive. Corruption climbs faster. But the mutations are powerful.

### Plex Access (Zones 0 and 9)

Stairs to the Plex appear when the player is carrying the **Cryptolith**. The Plex is where the Cryptolith must be delivered — it's the game's traditional win destination.

- **Entry**: Appears on Floor 9 (Cthelll) when the Cryptolith is carried. A dark void tile with stairs. "The Plex opens. The Cryptolith resonates."
- **Structure**: A void with scattered islands. Zone 0 (dense nullity) surrounds islands of Zone 9 (iron core). The player must navigate between islands through the void.
- **Demons**: Uttunul appears as the final boss. No other demons — the Plex is too dense for them.
- **Loot**: None. The Plex has no items, no mutations, no abilities. Just the Cryptolith's weight and the final confrontation.
- **Exit**: Die on the Plex floor with the Cryptolith to complete "The Descent" conduct. Or: descend further into Cthelll without the Cryptolith for the schizo-lucid path.
- **Risk**: The void tiles drain HP rapidly. The player must reach the central island (Uttunul's lair) before running out.

### The Three Routes

```
Time-Circuit Floors 1-9
    │
    ├── Normal descent (stairs down)
    │
    ├── Warp entry (hyp ≥ 55%, ~ stairs) → Spiral → Gate back
    │
    └── Plex entry (Cryptolith, Floor 9) → Void islands → Uttunul
```

The Time-Circuit is the main path. The Warp is optional but rewarding (mutations). The Plex is the win condition (Cryptolith delivery).



## The Stairs

Stairs down appear on the outer wall of each floor (opposite the starting position). The player enters at the top, descends to the bottom.

Stairs up exist but are blocked by "the current" — you can see the way back but can't take it. "The numogram only descends. Return is through the gates, not the stairs."

Gates provide shortcuts UP (Gate on Floor 6 can take you to Floor 4). This creates routing choices: descend linearly through all floors, or use gates to skip ahead and come back later.

---

## Implementation Priority

### Phase 1: The Hyperstition Loop (this session)
1. Add ability system with Tier 1 abilities (Glimpse, Nudge, Trace, Anchor, Quench)
2. Hyperstition spending (abilities cost hyp, meter drops)
3. Corruption spectrum (0-100% affects gameplay, not just at thresholds)
4. Schizo-lucid flag now triggers Phase 1 mechanical changes at 95%

### Phase 2: Dungeon Depth (next session)
5. Multi-floor structure (10 floors, zone-themed)
6. Stairs down between floors
7. Cryptolith placement on Floor 5
8. Gate shortcuts between Time-Circuit floors

### Phase 3: Schizo-Lucid Phases (following session)
9. Phase 2-4 mechanics (wall phasing, communion, Return/Exit)
10. Tier 2-3 abilities (unlock at hyp thresholds)
11. Corruption cosmetic effects (wall cracking, floor degradation)

---

*The hyperstition meter is not a thermometer. It is a pressure gauge. It measures how close the game is to becoming real. The player decides: stabilize the structure, or let it dissolve.*
