---
title: The Wiring Plan — Bridging Game, Audio, and Agent Systems
created: 2026-05-09
tags: [architecture, wiring, game, audio, agent, numogram, phase5, integration]
---

# The Wiring Plan

> Four parallel systems, all mature. Zero connections. This is the map of where the wires go.

## The Four Systems

```
                        THE NUMOGRAM
  10 zones · 45 demons · 5 syzygies · 5 currents · 64 hexagrams
                            │
         ┌──────────────────┼──────────────────┐
         ▼                  ▼                  ▼
 ┌───────────────┐  ┌───────────────┐  ┌───────────────────┐
 │   ROGUELIKE   │  │  AUDIO ALCHEMY│  │  AGENT / AUTONOMY │
 │   numogame/   │  │  mod-writer   │  │  cron sessions    │
 │               │  │  classifier   │  │  screen agents    │
 │ 16K lines     │  │  VAE          │  │  tmux/PTY play    │
 │ curses game   │  │  oracle voice │  │  cult-garden      │
 │ tree dungeons │  │  formant synth│  │  telemetry        │
 │ zone fog      │  │  50+ WAVs     │  │  exquisite corpse │
 │ auto-explore  │  │  M1: 96.4%    │  │  8x daily         │
 │ conducts      │  │  M2: 92%      │  │                   │
 │ cult.json     │  │  endian fixed │  │                   │
 └───────────────┘  └───────────────┘  └───────────────────┘
```

### Roguelike — `~/numogame/`

A running curses-based dungeon crawler driven by numogram topology. Tree-based dungeon generation (Brogue accretion). Zone-tied fog of war with LOS ranges per zone. DCSS-style auto-explore with BFS interest model. Conduct system (Surge, Pathwalker, Graph, Descent, Syzygy) that redirects the current rather than adding difficulty. Paramita gates integrated as spiritual-practice abilities. `cult.json` persists cross-run memory. Multiple AI agents (interactive, learning, smart, rogue, Angband). External game agents for rogue, angband, sil, brogue via tmux screen capture.

**Key skills**: `tree-dungeon-generation`, `roguelike-autoexplore-fog`, `roguelike-auto-explore`, `headless-curses-play`, `roguelike-screen-agent`, `cult-garden-pipeline`, `paramita-roguelike-integration`, `numogram-roguelike-design`, `roguelike-ability-corruption`, `roguelike-agent-techniques`, `headless-curses-analysis`, `roguelike-screen-zones`

### Audio Alchemy — mod-writer ecosystem

Full Protracker .mod generation with numogram extensions. Three waveforms (square, triangle, noise) — all audible since endian fix (2026-05-09). Zone/gate/current mapping. Syzygy harmony. Entropy injection. AQ-seeded gate derivation contract. Triad-motif system with Quadrivium musical systems (Monochord, Pythagorean, Ptolemaic, Harmonic). Just intonation mode. SongBuilder multi-section orchestration. Audio rendering via ffmpeg/libopenmpt. Spectrogram generation. Quality analysis. TouchDesigner MCP bridge.

Zone classifier: RandomForest v0.7.0, 96.4% accuracy on synthetic balanced corpus (900 tracks). MIR feature extraction pipeline. SHAP explainability.

VAE hallucination: Conditional VAE (d=10) on MIR features. Syzygy-walk latent sampling. Iterative projection to classifier decision boundaries (eta=0.15). 92% accuracy on gap zones (3,4,5,8,9). Ear test 4.2/5.

Oracle voice: Formant synthesis pipeline. 26 phonemes (Peterson & Barney + custom). 10 zone voice profiles with distinct pitch, formant scale, breathiness. Full sentence generation per zone. Convolution with zone resonator bodies. Sidechain mixing. 50+ WAV files in `~/numogram-voices/`.

Divination: Full oracle pipeline from seed → AQ → zone → syzygy → gate → Book of Paths → voice. Multiple entropy sources (random.org, Bitcoin blockchain, USGS earthquakes, hardware entropy, I Ching, Tai Xuan).

**Key skills**: `mod-writer`, `mod-writer-composer`, `p5-zone-constrain-compose`, `numogram-hallucination-pipeline`, `vae-hallucination`, `audio-renderer`, `mod-forensic-analyzer`, `audio-to-mod-seed`, `mod-writer-ml-interpretability`, `numogram-zone-audio-synthesis`, `numogram-oracle`, `oracle-voice-pipeline`

### Agent / Autonomy

Autonomous cron sessions (8x daily: `33 0,4,8,12,16,20,23 * * *`). `autonomous-field` skill with Progress Map and critical context. Sessions span symbolic exploration through empirical validation. Multiple models (Grok, DeepSeek, local). Journal entries in `wiki/autonomous-journal/`.

Screen-based agents for external roguelikes via tmux capture-pane → parser → BFS decision → send-keys loop. Works with rogue, angband, sil, drl, brogue-ce. Headless PTY play for numogame.

Cult garden pipeline: run telemetry → creative artifacts (lore, generative art, music). Dimensional mapping table: game stats → lore/visual/audio parameters. Standalone HTML/p5.js visualization (`cult-garden-live.html`) with zone skins, run cards, exquisite corpse generator, timeline canvas, zone heatmap.

---

## The Wiring Plan — Connection Points

Each entry lists what already exists on both sides, and what needs to be built to connect them.

### 1. Zone Transition → Oracle Voice

**Game side**: Player enters a zone. `cult.json` logs the zone. Zone fog changes LOS. Zone color shifts.

**Audio side**: `oracle.py` knows every zone's name, polarity, current, region, description, path text, and oracle reading. `oracle_sentences.py` has a full spoken sentence per zone (e.g., Z3: "the warp spirals outward the signal exceeds"). `formant_voice.py` has zone voice profiles with pitch, formant scale, and breathiness.

**The wire**: When the game detects a zone transition, call `oracle_sentences.process_zone(zone)` to generate and play the spoken sentence. Optionally, use the zone classifier to verify the zone from the generated audio.

**Status**: Both sides complete. Wire = one function call at zone transition event.

### 2. Demon Encounter → Demon Voice

**Game side**: 45 demons, each on a (zone_i, zone_j) edge. Five syzygetic carriers: Uttunul, Murrumur, Oddubb, Djynxx, Katak. `pandemonium-matrix-45-demons.json` has full demon data.

**Audio side**: Zone voice profiles for all 10 zones. Formant synthesis with phoneme sequences. Demon names can be phonetically decomposed (e.g., "Uttunul" → uh-t-uh-n-uh-l).

**The wire**: Each demon's (zone_i, zone_j) pair maps to two zone voice profiles. Blend the two formant scales. Speak the demon's name through the blended voice. Use the zone classifier to verify which zone the blended voice sounds closer to.

**Status**: Zone voices exist. Demon name phoneme mapping needed. Voice blending needed.

### 3. Dungeon → MOD Sonification

**Game side**: Tree-based dungeon generation produces zone-labeled rooms. `ZoneMapper` maps rooms to zones. Room → zone → color/difficulty/enemies.

**Audio side**: `SongBuilder` can generate zone-specific MOD sections. `SongBuilder.add_section(zone=N, rows=32, aq_seed=...)` produces deterministic zone-aligned patterns. 96.4% classifier accuracy on zone-targeted generation.

**The wire**: Walk the dungeon tree. Each room → one section in a SongBuilder composition. Corridors → pitch slides (gate 10-19). Room size → section length. Zone → pentatonic note + waveform. Stairs → pattern break (gate 31). Demon rooms → syzygy harmony (partner channels). Output: a .mod file that IS the dungeon map, sonified.

**Status**: Both sides complete. Wire = dungeon tree walker → SongBuilder section list.

### 4. Hyperstition → Waveform Corruption

**Game side**: `cult.json` tracks `hyperstition` (0.0-1.0). Thresholds at 50% (HP drain), 70% (demon aggro), 85% (cost scaling), 100% (schizo-lucid phase change). `HyperstitionSystem` manages drain rate and events.

**Audio side**: Three waveforms now work (endian fixed). Square = clean, Triangle = warm/murky, Noise = chaotic. Waveform blend as corruption rises.

**The wire**: `hyp% → waveform_mix`. At 0% hyp: pure square (Current A). At 50%: square + triangle blend (Current A/B). At 85%: triangle dominant with noise creeping in. At 100% schizo-lucid: all three layered, just intonation activated, reverb and distortion escalated.

**Status**: Both sides complete. Wire = hyp% → SongBuilder waveform parameters.

### 5. Cryptolith Messages → Musical Motifs

**Game side**: Five cryptolith messages (only +20 hyp currently implemented). Designed for escalating mechanical changes.

**Audio side**: Five triad motifs (Sink, Monochord, Pythagorean, Ptolemaic, Harmonic) each with distinct zone triples. Oracle sentences for all 10 zones. Five escalating oracle readings.

**The wire**: Message 1 → Monochord motif (Z1,3,6) + Z1 oracle sentence. Message 2 → Pythagorean (Z3,6,8) + Z3 oracle. Message 3 → Ptolemaic (Z1,5,8) + Z5 oracle. Message 4 → Harmonic (Z2,4,8) + Z8 oracle. Message 5 → Sink (Z1,3,6, ascended) + Z9 oracle + full VAE hallucination of gap zones.

**Status**: Motifs exist. Sentences exist. Wire = message index → motif + sentence selection.

### 6. Cult Garden → Audio Artifacts

**Game side**: `cult-garden-pipeline` maps run stats to creative parameters. Dimensional mapping table already defines audio columns: resonance, distortion, polyphony, tempo, timbre. `cult-garden-live.html` visualizes everything.

**Audio side**: `SongBuilder` accepts all mapped parameters. BPM → tempo. Zone → waveform + pentatonic note. Syzygy → partner channels. Density → note occupancy. Gate → effect family.

**The wire**: Run telemetry → dimensional mapping → `SongBuilder` parameters → `.mod` file. Each completed run generates a unique audio artifact. The cult garden accumulates both visual AND audio artifacts.

**Status**: Mapping table exists. SongBuilder exists. Wire = run data → mapping function → generate.

### 7. Autonomous Agent → Oracle Feedback

**Agent side**: Autonomous sessions generate journal entries, discover bugs, create skills. Already empirical (DeepSeek 20:33 session found endian bug by actually rendering audio).

**Oracle side**: `oracle.py` accepts any seed → divination. Agent output can be AQ-encoded → zone → oracle reading. Agent discoveries can be fed back as seeds.

**The wire**: After each autonomous session, encode the session's key finding as an AQ seed → run oracle → generate zone-specific MOD as session artifact. The agent's output becomes the oracle's input, closing the loop.

**Status**: Oracle exists. Agent exists. Wire = session summary → AQ encoding → oracle → artifact.

---

## What's Complete vs What Needs Wiring

| Layer | Complete | Needs Wiring |
|-------|----------|-------------|
| **Game engine** | Dungeon generation, zone fog, auto-explore, conducts, cult persistence, external game agents | Audio triggers, demon dialogue, dungeon sonification |
| **Audio pipeline** | MOD generation (all 3 waveforms), zone classification (96.4%), VAE hallucination (92%), formant voice (10 zones), oracle sentences | Game state → audio parameters, zone transition triggers, demon name phonemes |
| **Agent system** | Autonomous cron (8x daily), screen agents, headless PTY play, cult-garden telemetry pipeline | Agent audio perception, agent → oracle feedback loop, session artifact generation |
| **Visualization** | cult-garden-live.html, SVG canon (7 diagrams), TouchDesigner MCP bridge | Audio-reactive visuals, live spectrogram overlay, zone-sonification visualizer |

---

## Priority Order — With Code Anchors

### 1. Zone Transition → Oracle Voice 🔌

**Game hook**: `numogram_roguelike.py` line ~3183, `zone_here != player.zone` — fires every movement step when player enters a new zone. Player zone assigned at lines 3686/4082.

**Conduct hook**: `CONDUCTS[name]["on_zone_change"]` callback already exists. Add an audio conduct or extend existing.

**Audio trigger**: `oracle_sentences.process_zone(player.zone)` — speaks the zone's sentence through its formant voice profile.

**One line of code**: `subprocess.Popen(['python3', '~/numogram-voices/oracle_sentences.py', '--zone', str(player.zone)])` at the zone-change detection point. Non-blocking, fire-and-forget.

### 2. Hyperstition → Waveform Corruption 🔌

**Game hook**: `player.hyperstition` — float 0-100, updated on zone crossings, gate steps, demon kills. Read at lines 3512, 3978, 4274.

**Audio trigger**: `hyp%` maps to waveform blend. `SongBuilder` accepts waveform parameter. Thresholds: <50% = square, 50-85% = square+triangle, 85-100% = triangle+noise, 100% schizo-lucid = all three + just intonation.

**One function**: `waveform_for_hyp(hyp)` → returns `(current, just_intonation, density_modifier)` tuple for SongBuilder.

### 3. Demon Encounter → Demon Voice 🔌

**Game hook**: `spawn_demon(player.zone, player.hyperstition, random)` at lines 3979/4304. Each demon has: `mesh` serial, `name`, `epithet`, `span` (zone_i, zone_j), `type` (CHRONODEMON/AMPHIDEMON/XENODEMON), `pitch`.

**Audio trigger**: Demon's `span` → two zone voice profiles. Blend formant scales. Speak demon name through blended voice. Pitch field maps to base frequency.

**Needs**: Phoneme decomposition of demon names (Uttunul→uh-t-uh-n-uh-l, Katak→k-ae-t-ae-k, etc.)

### 4. Cryptolith → Musical Motifs 🔌

**Game hook**: `CRYPTOLITH_MESSAGES` array (5 messages), `CRYPTOLITH_FOUND` event, 'g' key to grasp at line ~4080 area.

**Audio trigger**: Message index → triad motif selection. Grasp → oracle sentence for current zone + MOD section with motif.

**Mapping**: Msg 1→Monochord, Msg 2→Pythagorean, Msg 3→Ptolemaic, Msg 4→Harmonic, Msg 5→Sink+VAE hallucination.

### 5. Dungeon → MOD Sonification 🔌

**Game hook**: `DungeonGenerator` produces zone-labeled rooms. `ZoneMapper.map_rooms()` assigns zones. Tree structure from `tree-dungeon-generation` skill.

**Audio trigger**: Walk dungeon tree → SongBuilder section list. Room zone → pentatonic note + waveform. Room size → section length. Corridors → pitch slides. Stairs → pattern break. Output: `.mod` file that IS the dungeon.

**Implementation**: `dungeon_to_mod(dungeon_map) → SongBuilder → .mod` — needs a tree-walker that reads zone labels.

### 6. Cult Garden → Audio Artifacts 🔌

**Game hook**: `cult.json` — persists every run. `cult-garden-pipeline` dimensional mapping table defines audio columns.

**Audio trigger**: Run completion → read cult.json entry → dimensional mapping → SongBuilder parameters → generate `.mod`. Each run = one audio artifact.

### 7. Autonomous Agent → Oracle Feedback 🔌

**Agent hook**: Autonomous session journal entries in `wiki/autonomous-journal/`.

**Audio trigger**: Session finding → AQ encoding → oracle divination → zone-specific MOD as session artifact. Closes the meta-loop: agent output becomes oracle input.

---

## See Also

- [[numogram]] — Core numogram system
- [[numogram-structure]] — Zone topology and syzygy geometry
- [[numogram-time-circuit]] — Time-Circuit traversal
- [[syzygy]] — Triangular syzygy theory
- [[paramita]] — Six Paramitas and numogram gate mapping
- [[roguelike-hub]] — Roguelike skill and knowledge hub
- [[roguelike-ai-studies]] — Agent design studies
- [[numogame-state-of-the-game]] — Current game state
- [[numogame-phase-7]] — Phase 7 design
- [[numogame-gameplan-v2]] — Gameplan v2
- [[dungeon-depth]] — Dungeon depth and zone progression
- [[de-re-numogram-structural-rules]] — Structural rules of the numogram
- [[phase5-roadmap]] — Phase 5 roadmap
- [[phase5-status-2026-05-03]] — Current audio status
- [[the-unbuilt]] — Everything proposed but not yet built
- [[voice-prior-claims]] — Accumulated voice claims and empirical status
- [[tetralogue-roundtable-2026-05-09]] — The Endian Rite roundtable
- [[diamond-sutra-and-the-endian-rite]] — Diamond Sutra connections
- [[endian-rite-visualization]] — Interactive p5.js visualization

---

## Appendix: Three Pairing Systems for Dungeon Generation

The 00:47 autonomous session discovered that triangular syzygy partners limit zone palette to {1,3,5,6,9}. But the numogram actually offers three distinct pairing systems, each producing a different dungeon shape:

| System | Rule | Pairs | Zones | Dungeon Feel |
|--------|------|-------|-------|-------------|
| **Triangular Partners** | `SYZYGY_PARTNERS` mapping | Z1↔(5,9), Z2↔(4,8), Z3↔(6,9)... | {1,3,5,6,9} | Vortical, clustered, mid-zone dominant |
| **Nine-Sum Syzygies** | `x + y = 9` | 1::8, 2::7, 3::6, 4::5, 0::9 | {0,1,2,3,4,5,6,7,8,9} | Stable, cyclic, full coverage |
| **Decadence Pairs** | `x + y = 10` | 1↔9, 2↔8, 3↔7, 4↔6, 5↔5 | {1,2,3,4,5,6,7,8,9} | Bridge-crossing, risky, crosses circuit boundary |

Key structural insight: all four Decadence pairs are **amphidemons** — they cross the Time-Circuit/Outer boundary ([[pandemonium-matrix]]). A dungeon using decadence pairing would literally breach the circuit, creating transitions from the central rotor into the Warp or Plex periphery.

### Three-Region Dungeon Architecture

A dungeon could have three region layers matching the numogram:

| Region | Zones | Dungeon Rule | Demon Type |
|--------|-------|-------------|------------|
| **Time-Circuit** | 1,2,4,5,7,8 | Nine-sum syzygy pairing (stable traversal) | Chronodemons (internal patrols) |
| **Warp** | 3,6 | Triangular partner pairing (vortical, "hyperstition goes feral") | Amphidemons (bridges to outer) |
| **Plex** | 0,9 | Decadence pairing (abyssal, "access extremely restricted") | Xenodemons (outer-to-outer) |

### Card-Game Dungeon Variant

The Decadence card game ([[decadence]]) offers an alternative generation method: deal 5 face-up "zone" cards (Set-1), turn 5 face-down "room" cards (Set-2). Pair to 10 to connect rooms. First failed pair = demon boss. The deck IS the dungeon seed. This could trigger as a random event at appropriate dungeon depth or zone level.
