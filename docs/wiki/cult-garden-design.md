---
title: "The Cult Garden — Creative Overflow System"
created: 2026-04-18
last_updated: 2026-04-24
tags: [numogram, roguelike, design, cult, creative, entropy, conduct, mega-artifact]
---

# The Cult Garden

> "The cult file is a digestive organ. It consumes runs and excretes art."

## The Problem

The cult.json has a 20-slot memory buffer (`cult_memory`). When it overflows, old runs are discarded. 228 runs logged. The first 208 are gone — they fell into the abyss.

## The Solution

When a run overflows the buffer, it doesn't disappear. It transforms. The overflowed run becomes creative material — processed through one of six methods in a hexagram cycle rotation.

## The Cycle (Three Methods)

Three methods, cycling with each overflow:

| Step | Method | Output |
|------|--------|--------|
| 1 | Exquisite corpse | lore.md — cryptographic stat-to-language fragments |
| 2 | Tsubuyaki | tsubuyaki/run-{n}.js — data-driven geometry primitives |
| 3 | Synthesis | tsubuyaki/synthesis-{n}.js + lore.md — cross-run hybrid artifact |

The cycle expanded from 2 to 3 methods in Cult Garden v2 (2026-04-23). Synthesis triggers every 3rd overflow, merging the last 5 runs into a single hybrid tsubuyaki and collective corpse line.

## Synthesis Breaker Conduct (v3)

A new conduct: **Synthesis Breaker** (`hud_char: Œ`).

- The cult predicts your next run based on its last 5 memories: primary zone chain, average kills, average hyp, predicted zones.
- If you take the Breaker conduct, you must **break the prediction**.
- Complete the conduct by violating at least one prediction axis (different primary zone, kills off by >50%, hyp off by >30%, or visiting an unpredicted zone).
- Fail by matching all predictions too closely — "The cult anticipated every move."
- Unlock requirement: complete at least 3 other conducts.

This closes the loop: the cult's memory becomes a constraint on future play.

## Mega-Artifacts (v3)

Every 9 runs, the digital root cycle completes (1→2→3→4→5→6→7→8→9→**reset**). At this threshold, all accumulated memory crystallizes into a **mega-artifact**:

- Aggregates: total kills, total turns, zones touched, average/max hyp, conducts witnessed
- Generates a quasiphonic chant from run totals
- Records the longest zone traversal chain
- Saved to `cult-garden/mega-artifact-cycle-{n}.md`
- Also appended to `cult-garden/mega-artifacts.md` (the master chronicle)

The mega-artifact is the cult's diary. Each cycle is a chapter. The garden grows not just in depth but in scale.

## Zone Skins (v3)

The live garden visualization (`cult-garden-live.html`) supports 10 zone-specific skins:

| Zone | Skin | Atmosphere |
|------|------|------------|
| 0 | Void | Stars appear on hover, slow fade, minimal UI |
| 1 | Stability | Gold grid lines, structured layout, steady monospace pulse |
| 2 | Separation | Forked typography, halting animations, orange wound palette |
| 3 | Release | Magenta vortex swirl, chaotic particles, swarm behavior |
| 4 | Catastrophe | Cyan wave background, shatter effects, violent surging tempo |
| 5 | Pressure | Green ring motif, squeezed typography, tight spacing |
| 6 | Abstraction | Blue dodecagon geometry, cool distant colors, minimal text |
| 7 | Blood | Red pulse, vein-like connecting lines, heartbeat rhythm |
| 8 | Multiplicity | Purple swarm, echo/duplicate elements, layered opacity |
| 9 | Iron Core | Purple-black iron, singularity gravity, decaying orbits |

Showcase page: `~/cult-garden-zone-skins.html` — click through all 10 skins with live data.

The skin selector reads `cult_zone` from `cult.json` and auto-applies the matching theme.

## Cult→Game Feedback (Implemented v3)

The cult's zone now actively influences gameplay:

| Trigger | Effect | Log Message |
|---------|--------|-------------|
| Enter zone matching cult_zone | +5 hyp | `[CULT] The {zone}th current resonates with the garden.` |
| Gate connecting to cult_zone | +3 hyp | `[CULT] Gt-XX opens toward Zone-{zone}. The garden pulls.` |
| Attack demon in cult_zone | +2 damage | `[CULT] The garden remembers {name}. Its mesh frays.` |
| Cult zone on death | Death message references cult zone | (flavor text) |

The cult is no longer passive archival. It is a second player — watching, remembering, occasionally helping, occasionally predicting.

### Cryptographic Exquisite Corpse (v2)

Run stats encode directly into linguistic parameters:

- **hyp%** → word length distribution (high hyp = gerund forms, ongoing action)
- **kills** → violence register:
  - 0 kills = abstract/drift verbs (float, linger, dissolve)
  - 1–5 kills = touch verbs (trace, mark, graze)
  - 6–10 kills = break verbs (cut, burn, crush)
  - 10+ kills = sever verbs (rend, tear, gash, bleed)
- **zones.length** → syntactic complexity:
  - ≤2 zones = short clause
  - ≤5 zones = compound sentence
  - ≤8 zones = complex sentence with mood deepening
  - 9–10 zones = nested phrase with tempo/mood annotation
- **turns** → fragment length and connector selection
- **cult_zone** → color bias (vocabulary + emotional register):
  - Zone 7 (Blood) = pulse/vein/blood vocabulary, pulsing tempo, urgent mood
  - Zone 3 (Release) = vortex/swarm/spiral vocabulary, chaotic tempo
  - Zone 0 (Void) = silence/null/Uttunul vocabulary, slow tempo

The last word of the previous lore.md entry seeds the next via last-word chaining.

### Data-Driven Tsubuyaki (v2)

Run stats select geometry primitives and visual parameters:

- **zones.length** → primitive family:
  - 1 zone = point grid
  - 2 zones = connecting line
  - 3 zones = triangle
  - 5 zones = ring/wave
  - 7 zones = ellipse/pulse
  - 9 zones = network graph
  - 10 zones = dodecagon/complete structure
- **hyp%** → alpha/saturation/glow (0–255)
- **kills** → noise amplitude / chaos factor (0–10)
- **turns** → motion speed
- **primary_zone** → base color and shape seed
- **cult_zone** → background tint (Zone 7 = blood-red bg, Zone 0 = black, etc.)

### Cross-Run Synthesis (v2)

Every 3rd overflow triggers synthesis:

1. Averages stats from last 5 runs
2. Generates hybrid tsubuyaki (`synthesis-{n}.js`) representing collective trajectory
3. Generates collective corpse line naming all 5 runs with zone-noun chains

Example: `> Synthesis of runs #290, #291, #292, #293, #294: core -> grid -> pulse -> wave -> core. the cult remembers collectively.`

## Structured Memory (v2)

`cult_memory` now stores structured dicts instead of strings:

```python
{
  'run': 294,
  'player': 'agent',
  'turns': 430,
  'hyp': 100.0,
  'zones': [0, 1, 8, 9],
  'kills': 2,
  'conducts': []
}
```

Legacy string-format entries are auto-migrated on load via `_mem_parse_string()`. `_mem_format()` converts dicts back to display strings when needed.

## The Cycle (Two Methods) — Deprecated

Two methods, alternating with each overflow:

| Step | Method | Output |
|------|--------|--------|
| 1 | Exquisite corpse | lore.md — last-word chained poetic fragments |
| 2 | Tsubuyaki | tsubuyaki/{run}.js — p5.js sketch parameters |

## The Cult's Current Zone

The cult itself has a numogram position. Calculated from all runs:

```python
# Sum all run stats ever recorded
total_turns = sum of all turns
total_kills = sum of all kills
total_hyp = sum of all max hyp values
combined = total_turns + total_kills * 100 + int(total_hyp * 10)

# Digital root
cult_zone = digital_root(combined) or 9
```

Stored in cult.json as `cult_zone`. Updated every time a run completes.

The cult's zone changes as the cult grows. Early cult (few runs) might be in Zone 1 (initiation). A violent cult (many kills) shifts toward Zone 3 (Warp). A patient cult (long runs, few kills) drifts toward Zone 5 (Hold).

## The Run Glyph

On the game over screen, render a single glyph representing the run:

```
    ╔═══╗
    ║ 7 ║  ← Zone (digital root of seed)
    ╠═╦═╣
    ║█║ ║  ← Hyp bar (filled = high hyp)
    ╠═╩═╣
    ║ ×3║  ← Kill count
    ╚═══╝
```

The glyph is small, distinctive, and numogrammatic. Each run gets a unique glyph. The glyph could also appear in the cult memory entries.

## File Tracking — The Cult Watches

The cult.json file is sacred. If the player deletes it, the game should notice:

1. **On game start**: Check if cult.json exists. If it was deleted since last run, set a `cult_desecrated` flag.
2. **First run after deletion**: The game starts normally but with a modified opening:
   - "The cult remembers nothing. The dead are unnamed. The numogram weeps."
   - All runs start with -10 hyperstition (the cult's resentment)
   - Demons are 20% more aggressive for the first 3 runs
   - The Cryptolith does not appear for 5 runs (the dead refuse to give it)
3. **After 5 runs**: The cult forgives. Normal behavior resumes.
4. **Cult memory**: "The player desecrated the cult. The dead were unnamed. The cult forgave after 5 runs."

Implementation: store a hash of the cult file in a separate sentinel file (`~/.hermes/obsidian/hermetic/wiki/.cult-hash`). On game start, compare current hash to sentinel. If they don't match and cult.json is new (fewer than 2 runs), desecration detected.

## Influence on Game State

The cult's zone can influence game state at certain points:

- **On entering a new zone**: if `cult_zone` matches the entered zone, +5 hyp bonus. "The cult resonates with this place."
- **On demon spawn**: if demon's home zone matches `cult_zone`, the demon is slightly weaker. "The cult's presence weakens it."
- **On gate step**: if the gate connects to `cult_zone`, +3 hyp bonus. "The cult's gate. The dead remember."
- **On death**: if `cult_zone` is in the player's visited zones, the death message references the cult's zone. "The cult at Zone 4 watches you fall."

## Implementation Priority

1. **Cult overflow rotation** — when cult_memory exceeds 20, process the overflowed entry
2. **Cult's current zone** — calculate and store in cult.json
3. **Run glyph** — render on game over screen
4. **File tracking** — detect deletion, apply repercussions
5. **Game state influence** — cult zone affects gameplay at specific points

---

*The cult file is not a save file. It is a temple. The runs are offerings. The overflow is the ritual.*

## See also

- [[cult-garden-tetralogue]] — Design tetralogue (Oracle/Builder/Writer/Gamer)
- [[seeds-in-the-machine-tetralogue]] — Cult garden installation narrative
- [[hyperstition-loop-design]] — Hyperstition threshold and propagation
- [[numogame-cult-tetralogue]] — Game implementation tetralogue
- [[cult.json.template|Cult JSON template]]
