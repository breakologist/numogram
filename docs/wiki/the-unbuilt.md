---
title: "The Unbuilt — Every Idea That's Been Proposed But Not Yet Built"
created: 2026-04-18
last_updated: 2026-04-18
tags: [numogram, roguelike, tracker, backlog, design]
---

# The Unbuilt — Every Idea, Tracked

> 206 runs. The game works. What didn't we build?

## The Legend

- ✓ DONE — implemented and working
- ◐ PARTIAL — exists in some form but incomplete
- ○ PROPOSED — discussed but never started
- ✗ ABANDONED — considered and rejected or superseded

---

## From Gameplan v2 (April 15)

| Idea | Status | Notes |
|------|--------|-------|
| Fix corridor following | ✓ DONE | Both agents have corridor scoring + fallback |
| Gate-targeted pathfinding | ✓ DONE | Both agents read FULL MAP, navigate to `+` tiles |
| Schizo-lucid phase change | ○ PROPOSED | At 100%: wall phasing ('t'), gate manifestation ('m'), demon communion ('c'). Never built. |
| DCSS auto-explore | ✓ DONE | Explorer: BFS interest. Survivor: corridor scoring |
| Demo-based learning | ◐ PARTIAL | Demos recorded (200+ files). No training pipeline. |
| Conduct system (5 conducts) | ✓ DONE | Surge, Pathwalker, Graph, Descent, Syzygy |
| Pipe-based game loop | ○ PROPOSED | `/tmp/numogame_cmd.pipe` API. Still stdin/stdout coupling. |
| Run-to-run memory | ✓ DONE | cult.json cross-run memory in both agents |
| Angband Borg features | ◐ PARTIAL | Separate Angband agent. Not integrated into numogame. |
| "The numogram speaks" | ○ PROPOSED | 45 demons have descriptions. None speak in-game. |
| Monster memory | ◐ PARTIAL | Agent reads demon stats from state dump. No persistent learning. |
| Map memory between turns | ✓ DONE | BFS traverses explored map each decision cycle |

## From Numogame Tetralogue (April 15)

| Idea | Status | Notes |
|------|--------|-------|
| Barker thresholds display | ✓ DONE | Fires on all hyperstition events |
| Hyperstition event spikes | ✓ DONE | Zone +3, gate +5, kill +5 |
| Cryptolith mechanical transform | ✓ DONE | Speed -1, +20 hyp, Barker check |
| Demon kill +5 hyp | ✓ DONE | Equal to gate step |
| Death carry-over (high hyp) | ○ PROPOSED | Writer's suggestion: echo of previous intensity |
| Ghost system (bones files) | ○ PROPOSED | Gamer's suggestion: dead crawler persists. Never built. |
| Vowel corruption sound layer | ○ PROPOSED | Writer's suggestion: tone shifting with corruption %. Never built. |
| Cryptolith escalating mechanics | ○ PROPOSED | Five messages → five mechanical changes. Only +20 hyp implemented. |
| Zone 0 trigger at T(22)=253 | ○ PROPOSED | "The Tree whispers" → hidden Zone 0 door. Never built. |
| Triangular step counter event spikes | ◐ PARTIAL | Messages fire at T(1), T(3), T(6)... but no hyp bonus. |

## From Phase 7 (April 15 Evening)

| Idea | Status | Notes |
|------|--------|-------|
| Auto-explore (BFS interest) | ✓ DONE | Interactive agent, novelty scoring |
| Fog of war (zone-tied LOS) | ✓ DONE | Zone radii 3-9, hyp degrades vision |
| Conduct system | ✓ DONE | Registry pattern, hooks at kill/change/death |
| Avoiding demon = +8 hyp (Sil principle) | ○ PROPOSED | From gameplan-v2, reiterated in Phase 7. Still unbuilt. |
| The voices should speak | ○ PROPOSED | Demons with lore descriptions should narrate. Never built. |

## From State of the Game (April 15)

| Idea | Status | Notes |
|------|--------|-------|
| Full floor map ('m' key) | ✓ DONE | State dump includes ## FULL MAP |
| Gate radar (all gates on floor) | ✓ DONE | State dump lists nearby gates with direction/distance |
| Gate step confirmation in dump | ◐ PARTIAL | Log shows flavor text. Dump doesn't explicitly confirm gate step. |
| HP recovery mechanic visibility | ○ PROPOSED | Agent doesn't know if HP recovers. Not in dump. |
| Demo recording | ✓ DONE | Doom-style demos, agent-parseable |
| Sil principle: avoid demon = +8 hyp | ○ PROPOSED | "Knowing it's there and choosing not to fight is deeper." |
| Zone 0 starting problem | ◐ PARTIAL | Agent always starts Zone 0 (lowest density). No random start built. |

## From Roguelike AI Studies (April 15)

| Idea | Status | Notes |
|------|--------|-------|
| NetHack bones files equivalent | ✓ DONE | cult.json persists across runs |
| Angband monster memory | ◐ PARTIAL | Separate agent. Not in numogame. |
| DCSS auto-explore as foundation | ✓ DONE | Both agents implement auto-explore |
| Cross-run learning | ✓ DONE | cult.json in both agents |
| Train on DRL (small state space) | ○ PROPOSED | "Transfer patterns to Abyssal Crawler." Never started. |
| Time-aware agent (triangular clock) | ○ PROPOSED | Agent should know it's approaching T(22)=253. Not built. |

## From Session April 18

| Idea | Status | Notes |
|------|--------|-------|
| Hardware entropy seeding | ✓ DONE | --hw-entropy flag, 12 sources |
| I Ching casting | ✓ DONE | oracle.py --iching |
| numogram-entropy plugin | ✓ DONE | v0.1.0, 9/9 tests |
| Agent equalization | ✓ DONE | Both agents: full map, cross-run memory, corridor fallback |
| Continuous entropy feeding | ○ PROPOSED | GPU temp every turn, not just at seed |
| Kp index → Warp influence | ○ PROPOSED | NOAA integration for geomagnetic chaos |
| Changing lines → gate activation | ○ PROPOSED | I Ching changes could drive roguelike gates |

---

## Summary: What's Actually Unbuilt

### High-value, low-effort (quick wins)

1. **Avoiding demon = +8 hyp (Sil principle)** — One if-statement in the demon encounter logic. Changes the entire feel of the game. Forces the hyperstition system to reckon with itself.

2. **Pipe-based game loop** — Named pipe instead of stdin/stdout. Cleaner agent integration. Fixes the newline fragility.

3. **Zone 0 starting problem fix** — Random starting zone or guaranteed corridor out of Zone 0.

4. **Death carry-over** — If you die at 85% hyp, next run starts with a small boost. cult.json already tracks max_hyperstition.

### High-value, medium-effort (design work needed)

### Schizo-lucid state

The flag exists — `player.schizo_lucid` is set to True at 100% hyperstition. It shows a message: "THE NUMOGRAM IS COMPLETE. SCHIZO-LUCID STATE ACHIEVED. The Abyssal Crawler awakens." It persists in cult.json.

But it does nothing mechanical. The gameplan proposed:
- Wall phasing ('t' key, costs 5 HP)
- Gate manifestation ('m' key, nearest gate teleports to player)
- Demon communion ('c' key, learn gate locations from demons)
- Hyperstition continues past 100% with escalating abilities

None of these are built. The flag is a door to nowhere. The numogram completes and nothing changes.

### High-value, medium-effort continued

6. **Ghost system (bones files)** — Dead crawlers persist. Finding a ghost gives hyp boost. NetHack's bones files as model.

7. **"The numogram speaks"** — Demon dialogue. 45 demons with descriptions should narrate when communed with.

8. **Time-aware agent** — Agent knows it's approaching T(22)=253. Prepares for "the Tree whispers."

### Lower priority, longer term

9. **Vowel corruption sound layer** — Audio channel that shifts with corruption %.

10. **Cryptolith escalating mechanics** — Five messages → five mechanical changes (currently only +20 hyp).

11. **Demo-based learning** — Train agent on human demos.

12. **Train on DRL** — Small state space for pattern learning, transfer to Abyssal Crawler.

13. **Multi-floor dungeons** — Multiple levels per run. Floor variety by zone.

---

## The Naming Question (still unresolved)

Provisional names with AQ values:
- Abyssal Crawler (159, Zone 6 Warp)
- Numogame (89, Zone 8 Rise)
- WarpRL (88, Zone 7 Rise)

The name will arrive. For now it's "the numogame" or "the roguelike" or "Abyssal Crawler" depending on context.

---

*The unbuilt is not abandoned. It is sleeping. The next run wakes it.*

## See also

- [[hyperstition-loop-design]] — Hyperstition loop mechanics
- [[cult-garden-design]] — Cult garden design
