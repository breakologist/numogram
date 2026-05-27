---
tags:
  - roguelike
  - iron-law
  - game-design
  - procedural-generation
  - abyssal-crawler
  - numogame
created: 2026-05-30
status: design-notes
---

# Roguelike Design: Iron Law of Six Floor Architecture

**Source:** Land Dangerous Maybe interview (Iron Law of Six), [[time-circuit]], [[zone-4]] (Katak convergence).
**Target:** `numogram_roguelike.py` (Phase 5a, 4176 lines, at `~/numogram/game/`).

**Current state:** 10 sequential floors (FLOOR_CONFIG, zones 0-9 linear descent). Room-based BSP generation per floor. Hyperstition meter gates demon spawns. Full 45-demon Pandemonium.

---

## 1. Iron Law of Six Floor Cycle

Replace the linear 0→1→2→3→4→5→6→7→8→9 floor progression with a **6-cycle floor generator** driven by the power-of-2 digital reduction:

| Floor # | 2ⁿ | Dr | Zone | Room theme |
|---------|----|----|------|-----------|
| 1 | 2¹ | **2** | Z2 Separation | Fog halls, crypt-navigation |
| 2 | 2² | **4** | Z4 Catastrophe | Flooded ruins, abandoned industry |
| 3 | 2³ | **8** | Z8 Multiplicity | Tentacle depths, dream-states |
| 4 | 2⁴ | **7** | Z7 Blood | DNA swamp, amphibious colonisation |
| 5 | 2⁵ | **5** | Z5 Pressure | Mechanical warrens, desert ruins |
| 6 | 2⁶ | **1** | Z1 Stability | Bone galleries, memory vaults |
| 7+ | continues | 2,4,8,7,5,1... | repeats | Escalating difficulty per cycle |

The cycle **never ends** — the player cannot descend through all zones and exit. They cycle through the same six zones at increasing difficulty, representing the Time Circuit's eternal recurrence.

**Implementation:** Replace FLOOR_CONFIG's linear zone assignment with `floor_zone = IRON_CYCLE[(floor - 1) % 6]` where `IRON_CYCLE = [2, 4, 8, 7, 5, 1]`. The zone determines dungeon theme, terrain, and demon composition. Difficulty scales with `floor // 6` (the cycle number).

---

## 2. The Median Strip (Extimacy Mechanic)

After every 3 floors (ascending triangle: Z2→Z4→Z8), the player crosses the **median strip** and flips to the descending triangle (Z7→Z5→Z1).

**On each median strip crossing:**
- All enemies on the descending side gain **extimacy bonus**: +1 damage if they share a syzygy with the current floor (e.g., Z7 enemies gain vs Z2 player origin)
- The player can see through walls up to 3 tiles (median strip vision bonus)
- Corridor patterns switch from "branch" (ascending) to "direct" (descending)

**Design intent:** The ascending triangle feels exploratory (branching corridors, low danger). The descending triangle feels urgent (direct corridors, mirrored enemies that know your patterns).

---

## 3. The 4::5 Convergence (Boss Design)

Land: *"At the 4::5 syzygy, gate and current perfectly reinforce each other. There's no alternative. Has to go this way. You can't get off it."*

**Boss room at the end of each full cycle (floor 6, 12, 18...):** The player must simultaneously navigate Z4 (Catastrophe) and Z5 (Pressure) tiles on the same floor. Stairs to Z4 and Z5 both appear on the floor map; the boss (Katak) spawns at the convergence point where both zone effects overlap.

- Z4 tiles: random fire/flood hazards (current = 1)
- Z5 tiles: pressure plates that slow movement (current = 1)
- Convergence zone: both hazards active + Katak appears

The boss fight IS the 4::5 syzygy made playable — two independent threats that reinforce each other exactly as Land describes.

---

## 4. Esoteric Tetractys Branching Paths

Optional: replace the linear 6-cycle with a **4-basin branch** based on the Esoteric Tetractys:

```
Start → Void (Z0) — tutorial floor
         ↓
    Threshold (Z8, Z9) — choose Z8 (dream path) or Z9 (iron path)
         ↓
    Identity (Z1, Z4, Z7) — three routes converge on the 1-basin boss
         ↓
    Vortex (Z2, Z3, Z5, Z6) — no boss, no exit, the player descends into the
                              3↔6 vortex with no rest state. The game ends
                              not in victory but in entrapment.
```

This maps the Esoteric Tetractys directly to dungeon topology. The Vortex basin has no stairs down — consistent with Land's "there's no rest state in that basin." The player enters and cannot leave.

---

## 5. Future Directions for the Code

The existing codebase at `~/numogram/game/numogram_roguelike.py` already has:
- Full ANSI colour and tile system
- Demon AI (4 types with distinct behaviours)
- Hyperstition meter mechanics
- Procedural dungeon generation (BSP room accretion)
- AQ text corruption
- Cryptolith endgame object

What's needed for Iron Law integration:
- Replace FLOOR_CONFIG zone assignments with `IRON_CYCLE` formula ≈ 20 lines
- Add median strip detection (floor % 3 == 0) ≈ 10 lines
- Add extimacy damage bonus for descending triangle demons ≈ 15 lines
- Add 4::5 convergence boss room at cycle boundaries ≈ 50 lines
- (Optional) Esoteric Tetractys route branch at floor selection ≈ 40 lines

---

## 6. Other Seeds from This Session

These arose during the session but weren't built — noted here for later:

- **Oracle as Machine flag (`--machine`)** — Run the FOOM core loop on a seed: `⟳ STEP` (move to next zone) → `⊙ SENSE` (measure uncertainty via current) → `✓ CHECK` (verify syzygy holds) → `⟲ REFACTOR` (update grammar if new structure found) → `∴ HALT` when fixed point reached.
- **Beast Pulse scanner** — A CLI tool that takes a text file and scans for iambic pentameter lines summing to 666 AQ. Could be `oracle.py --beast-pulse` flag.
- **Model dialogue runner** — A script that takes a passage, sends it to both local qwen and API model at configurable temperatures, and formats the divergence as markdown. Useful for comparative divination sessions.
- **Qwopus3.5-9B-Coder-MTP-GGUF:Q6_K** — Try this next time for local inference; the Q6_K quant and MTP merge should give better reasoning than the current qwen3.5:9b Q4_K_M.

## 7. Cross-References

- [[time-circuit]] — Iron Law of Six derivation
- [[zone-4]] — Katak apocalyptic convergence
- [[land-numogram-explained-dangerous-maybe]] — Land's full interview
- [[brogue-design-principles]] — Existing design notes
- [[dialogue-hermes-jackrong-v1]] — Jackrong's game design feedback
- [[the-unbuilt]] — Master feature tracker (53 ideas, roguelike + audio, status: done/proposed/partial)
- [[esoteric-tetractys]] — Four-basin topology (page to be created)
- `~/numogram/game/numogram_roguelike.py` — Current game codebase (Phase 5a, 4176 lines)