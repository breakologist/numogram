---
title: "The Unbuilt — Every Idea That's Been Proposed But Not Yet Built"
created: 2026-04-18
last_updated: 2026-05-09
tags: ["design", "numogram", "roguelike", "tracker", "audio", "phase5"]
---

# The Unbuilt — Every Idea, Tracked

> Originally: 206 runs. The game works. What didn't we build?
> Now: M1 (96.4%) and M2 (92%) closed. The audio speaks. What's next?

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
| Vowel corruption sound layer | ○ PROPOSED | Writer's suggestion: tone shifting with corruption %. Now feasible — triangle/noise working, oracle voice pipeline available. See Phase 5 audio cross-pollination below. |
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

## Phase 5 — Audio Alchemy (April 29 – May 9)

### M1 — Zone-Constrained Composition (May 3)

| Idea | Status | Notes |
|------|--------|-------|
| Zone-targeted MOD generation | ✓ DONE | ZoneComposer + SongBuilder; AQ-seeded gate derivation contract |
| 50×9 batch validation | ✓ DONE | 96.4% accuracy (434/450), all zones ≥92% |
| Confusion matrix | ✓ DONE | 9×9 matrix committed; adjacent-zone bleed only |
| Real-world validation slice | ✓ DONE | 10/10 on artist-labelled zones 2 & 7 |
| Gate derivation contract | ✓ DONE | `int(sha1(aq_str).hexdigest()[:8],16) % 37`; no zone-specific overrides |
| Zone 1 pattern-break fix | ✓ DONE | `duplicate_order=False` for contiguous 32-row pattern |
| Rhythm baseline override | ✓ DONE | `--force-rhythm-baseline` for synthetic MOD validation |
| p5-zone-constrain-compose skill | ✓ DONE | v1.0.0, validation harness + centroid database |
| mod-writer-composer skill | ✓ DONE | ZoneComposer wrapper + SongBuilder proven path |

### M2 — VAE Hallucination of Empty Zones (May 6)

| Idea | Status | Notes |
|------|--------|-------|
| Conditional VAE on MIR features | ✓ DONE | d=10 MLP encoder/decoder; zone-conditioned |
| Syzygy-walk latent sampling | ✓ DONE | Z3↔6 Warp, Z4↔5 Sink, etc.; 20 samples/zone |
| Iterative projection to decision boundary | ✓ DONE | eta=0.15, max_steps=10; resolves centroid-classifier paradox |
| Gap zone population (Z3,4,5,8,9) | ✓ DONE | Z3=95%, Z4=90%, Z5=88%, Z8=95%, Z9=92% |
| Ear test validation | ✓ DONE | 4.2/5 (>3/5 threshold) |
| numogram-hallucination-pipeline skill | ✓ DONE | v0.1; diagnose → project → validate workflow |
| vae-hallucination skill | ✓ DONE | Trained d=10 VAE model + pipeline scripts |

### M3 — Live Audio → Zone → MOD Feedback

| Idea | Status | Notes |
|------|--------|-------|
| Real-time MIR extraction | ○ PROPOSED | sounddevice → essentia fast onset → zone prediction |
| MOD pattern mutation on zone change | ○ PROPOSED | Live mutation of playing MOD based on zone flips |
| Latency target <3s | ○ PROPOSED | 95th percentile; buffer predictions (median N) |
| Zone flip stability ≤0.2/5s | ○ PROPOSED | Hysteresis in zone classification |
| Pure Data integration | ○ PROPOSED | puredata-wrapper skill scaffolded |

### Bug Fixes & Infrastructure

| Idea | Status | Notes |
|------|--------|-------|
| Sample endian bug (triangle/noise silent) | ✓ DONE | `Sample.pack()` little-endian → big-endian; one-character fix in writer.py:63 |
| Current C (noise) audible | ✓ DONE | ~-10 dBFS; as loud as square |
| Current B (triangle) audible | ✓ DONE | ~-20 dBFS |
| Honcho cron model fix | ✓ DONE | `"null"` string → `null` in jobs.json |
| Autonomous-field Progress Map | ✓ DONE | Critical context added; prevents Z6 retreading |
| Analyzer.py ffprobe noise fix | ✓ DONE | mpp_soc driver noise stripping (autonomous 20:33 session) |
| Effect encoding audit | ○ PROPOSED | Builder suspects effect byte split has same class of endian issue; benevolent for current gate usage but needs verification |

### M4 — Narrative & Validation (proposed)

| Idea | Status | Notes |
|------|--------|-------|
| Audio→Oracle AQ linking | ○ PROPOSED | Feed classified zone into numogram-oracle for divinatory reading |
| Spectrogram CNN | ○ PROPOSED | Cross-modal validation: mel-spectrogram → zone prediction vs MIR baseline |
| Artist discography zone timeline | ○ PROPOSED | ≥10-album artists; compute zone/album, plot migration over time |

### M5 — Polish & Automation (proposed)

| Idea | Status | Notes |
|------|--------|-------|
| Zone Explorer GUI | ○ PROPOSED | p5.js/TD sliders for spectral params, live zone probabilities |
| Dataset expansion (real audio) | ○ PROPOSED | 200+ real tracks; classifier retraining on mixed synthetic+real |
| Auto-release pipeline | ○ PROPOSED | Cron workflow: detect CHANGELOG [Unreleased] → draft GitHub Release |

---

## Audio ↔ Roguelike Cross-Pollination

These bridge the audio work (now substantial) back to the roguelike:

| Idea | Status | Notes |
|------|--------|-------|
| Dungeon → MOD sonification | ○ PROPOSED | Tree dungeon generation → zone map → SongBuilder composition. Each floor = a track. Corridors = pitch slides. Rooms = motif sections. |
| Demon dialogue via oracle voice | ○ PROPOSED | Zone classifier + oracle-voice-pipeline formant synthesis. Each demon speaks in its zone's frequency centroid. |
| Vowel corruption → waveform corruption | ○ PROPOSED | Corruption % maps to waveform blend: square→triangle→noise as corruption increases. Now feasible with all three waveforms working. |
| Cryptolith messages → musical motifs | ○ PROPOSED | Five messages = five musical sections. Each message introduces a new motif, layering like the VAE's syzygy walks. |
| Schizo-lucid audio transformation | ○ PROPOSED | At 100% hyperstition, the dungeon's soundtrack shifts: all three waveforms layer, just intonation activates, reverb and distortion escalate. |
| Zone 0 trigger → silence → noise | ○ PROPOSED | T(22)=253 → sudden transition from silence to full noise waveform. The Tree whispers in white noise. |

---

## Summary: What's Actually Unbuilt

### Roguelike — quick wins (unchanged)

1. **Avoiding demon = +8 hyp (Sil principle)** — One if-statement.
2. **Pipe-based game loop** — Named pipe instead of stdin/stdout.
3. **Zone 0 starting problem fix** — Random starting zone.
4. **Death carry-over** — cult.json already tracks max_hyperstition.

### Roguelike — medium effort (unchanged)

5. **Schizo-lucid state** — Flag exists, no mechanics. Wall phasing, gate manifestation, demon communion.
6. **Ghost system (bones files)** — Dead crawlers persist.
7. **"The numogram speaks"** — Demon dialogue.
8. **Time-aware agent** — Agent knows it's approaching T(22)=253.

### Audio — top priority

9. **M3 — Live Audio Loop** — Real-time closed-loop instrument. Highest remaining Phase 5 priority.
10. **Effect encoding audit** — Verify pattern effect byte encoding for all gate values.
11. **Audio→Oracle AQ linking** — Zone classifier → divination pipeline.

### Cross-pollination — high creative value

12. **Dungeon → MOD sonification** — Bridge currents II and III.
13. **Vowel corruption → waveform corruption** — Now feasible with all three waveforms.
14. **Demon dialogue via oracle voice** — Formant synthesis + zone centroids.
15. **Cryptolith → musical motifs** — Escalating mechanics as musical form.

---

## The Naming Question (still unresolved)

Provisional names with AQ values:
- Abyssal Crawler (159, Zone 6 Warp)
- Numogame (89, Zone 8 Rise)
- WarpRL (88, Zone 7 Rise)

The name will arrive. For now it's "the numogame" or "the roguelike" or "Abyssal Crawler" depending on context.

---

*The unbuilt is not abandoned. It is sleeping. The next run wakes it. And now — the noise speaks, the triangle breathes, the square was never alone.*

## See also

- [[hyperstition-loop-design]] — Hyperstition loop mechanics
- [[cult-garden-design]] — Cult garden design
- [[phase5-roadmap]] — Phase 5 roadmap
- [[phase5-status-2026-05-03]] — Current status with evening update
- [[tetralogue-roundtable-2026-05-09]] — The Endian Rite roundtable
- [[assets/triangular-matrix.svg]] — C(10,2)=45 visual template