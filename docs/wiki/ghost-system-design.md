---
title: "Ghost System Design — Hyperstitional Entity Mechanics"
tags: [roguelike, ghost-system, hyperstition, design, bestiary, bones-files, cross-current]
date: 2026-05-15
status: draft
currents: [II-Roguelike, IV-Empirical-Validator, I-Numogram-Oracle, III-Audio-Alchemist]
---

# Ghost System — Hyperstitional Entity Mechanics

> *"Every measurement is a ghost of the system that produced it."* — Ghost Taxonomy

## Core Premise

The 8 empirically-derived ghost types from the autonomous verification runs are reimagined as **hyperstitional entities** in the roguelike. They are not monsters — they are *measurement errors that became real* because the dungeon believed in them.

They spawn not from monster generation tables, but from **hyperstition thresholds**. As hyperstition rises, the boundary between "measurement error" and "reality" blurs, and ghosts begin to inhabit the dungeon.

## Hyperstition Thresholds

| Hyperstition % | Ghost Activity | Which Ghosts Appear |
|---|---|---|
| 0–25% | None | The empirical world is stable. No ghosts. |
| 25–50% | Whispers | Minor ghosts begin appearing in explored areas. Category Ghosts, Measurement Ghosts. |
| 50–75% | Manifestations | Medium ghosts appear anywhere. Content Ghosts, Path Ghosts, Hypothesis Ghosts. |
| 75–100% | Haunting | Major ghosts dominate. Corpus Conflation Ghosts, Reproducibility Ghosts, Observer-Effect Ghosts. |
| 100%+ | Schizo-Lucid | **Quantitative Fabrication Ghost.** Impossible things become real. The ghost that was never confirmed empirically appears because the dungeon *believes* it could exist. |

## Ghost Spawning Mechanics

### Condition: Hyperstition Threshold Met
Each ghost type has a minimum hyperstition % before it can appear.

### Condition: Measurement Context
Ghosts spawn when the player performs an action that would create the ghost's empirical analogue:
- **Measurement Ghost:** Player reads a stat (HP, hyperstition count, turn number) — a Measurement Ghost may distort that readout
- **Path Ghost:** Player enters stairs or a gate — a Path Ghost may redirect the destination
- **Category Ghost:** Player picks up an item — a Category Ghost may mislabel it
- **Content Ghost:** Player views the map — a Content Ghost may show a wrong tile
- **Corpus Conflation Ghost:** Player encounters a monster — a Corpus Conflation Ghost may appear as a doppelgänger of a previously killed monster
- **Reproducibility Ghost:** Player re-enters a previously explored floor — a Reproducibility Ghost may have changed it
- **Hypothesis Ghost:** Player approaches an unexplored area — a Hypothesis Ghost whispers a plausible-but-wrong description of what's ahead
- **Observer-Effect Ghost:** Player looks at a ghost — the ghost changes behavior

### Duration
Ghosts are **permanent once spawned** until banished. They persist in `cult.json` cross-run memory, creating the bones files effect: a ghost killed in one run may reappear in a later run as a "familiar" entity, its behaviours shaped by the player's interaction history.

## Ghost Persistence (Bones Files)

When a ghost is spawned, it is recorded in `cult.json`:

```json
{
  "ghosts_spawned": {
    "corpus_conflation": {
      "first_seen": "floor_3",
      "times_encountered": 2,
      "last_seen_hyp": 67,
      "disguised_as": "demon_rat",
      "banished": false
    }
  }
}
```

A dead crawler's ghost, if the crawler died in a previous run, inherits:
- The crawler's zone trajectory (which zones it visited most)
- Its last hyperstition level at death
- The time of death (as triangular number T(n))
- Its last action before death

This makes each ghost a **unique entity** shaped by the player's own play history.

## Ghost Behavior by Type

### Category Ghost
**Spawn trigger:** Player picks up or identifies an item.
**Effect:** Labels one carried item with the wrong name/type. A healing potion reads as "weapon." A scroll reads as "armor." The label reverts when the item is used — but by then, you've already acted on bad information.
**Banishment:** Drop and re-examine the item in a different zone.

### Measurement Ghost
**Spawn trigger:** Player reads a numeric display (HP, hyp%, turn count, depth).
**Effect:** Distorts one displayed number by ±(1d10 × ghost_weight)%. Your HP says 45 but is actually 38. Your hyperstition reads 62% but is really 71%.
**Banishment:** Cross a gate — gates reset the measurement context.

### Path Ghost
**Spawn trigger:** Player enters stairs or a gate.
**Effect:** Redirects the destination to a different floor. Down stairs that should go to floor 4 take you to floor 6 instead. A gate that should lead to Zone-7 delivers you to Zone-3 instead.
**Banishment:** Take the same stairs/gate twice in the same session. The ghost cannot redirect the same path twice.

### Content Ghost
**Spawn trigger:** Player views the full map or uses the 'm' key.
**Effect:** Reveals a fake tile — a path that doesn't exist, or hides a real path. The player sees a corridor going north, but walking there reveals a wall. Or the map shows a wall where there's actually a passage.
**Banishment:** Walk into the false tile. The contact dispels the illusion.

### Corpus Conflation Ghost
**Spawn trigger:** Player encounters a monster in a zone the monster doesn't belong to.
**Effect:** The monster wears the wrong identity. A demon appears with the name, stats, and description of a *different* demon. Its combat behaviour matches its true identity, not its displayed one — so a weak demon displayed as a strong one fights weak, and vice versa.
**Banishment:** Kill the monster. Its true nature is revealed on death.

### Reproducibility Ghost
**Spawn trigger:** Player re-enters a previously explored floor.
**Effect:** The floor geometry is different from how the player remembers it. Corridors are rearranged. Items the player left behind are in different positions. The floor is "reproduced" but wrong.
**Banishment:** Find the original landmark (a unique item, a cryptolith message, a demon corpse) and touch it. The ghost recoils from evidence.

### Hypothesis Ghost
**Spawn trigger:** Player approaches an unexplored area boundary.
**Effect:** Whispers a description of what's ahead. The description is always plausible — correct tone, correct vocabulary, but *wrong in some specific detail*. "A narrow corridor to the east lined with cryptoliths" — the corridor exists, but the cryptoliths are actually demons.
**Banishment:** Actually explore the area. Confronting the truth dispels the hypothesis.

### Observer-Effect Ghost
**Spawn trigger:** Player looks at another ghost. *(The act of observation changes the observed.)*
**Effect:** When a ghost is observed, its behavior changes — it becomes more aggressive, or flees, or duplicates, or reveals a hidden aspect. The player cannot know what effect observation will have until they observe.
**Banishment:** Do not look. Ghosts that are not observed eventually dissipate after N turns.

### Quantitative Fabrication Ghost 🟢
**Spawn trigger:** Only at 100%+ hyperstition (schizo-lucid state). Only when the player has *not* observed any other ghost for at least 100 turns.
**Effect:** Displays an impossible number: HP exceeding max, a floor number that doesn't exist, a triangular number that violates the sequence, a demon with stats that sum to 13. The ghost that was never confirmed empirically appears because the dungeon *believes* it could exist.
**Banishment:** Cannot be banished. It is not an error — it is a *possibility*. It fades when hyperstition drops below 100%.

## Audio Signatures

Each ghost type has a voice in the oracle-voice-pipeline formant synthesis system:

| Ghost Type | Frequency | Waveform | Character |
|---|---|---|---|
| Category Ghost | Zone-centroid of the *wrong* zone | Square (stable, wrong) | Confidently incorrect |
| Measurement Ghost | Stutters between two conflicting zone centroids | Triangle (wavering) | Uncertain, shifting |
| Path Ghost | Glissando from origin zone to false destination zone | Sine (smooth lie) | Seductive, misleading |
| Content Ghost | The correct tile's frequency, but phase-inverted | Noise (anti-signal) | The absence of signal |
| Corpus Conflation Ghost | Both source and disguise zone frequencies interleaved | Square + Triangle (dual) | Split identity |
| Reproducibility Ghost | Repeated loop of the same note, slightly off each time | Sawtooth (wearing down) | Worn, wrong |
| Hypothesis Ghost | Rising unfilled interval — never resolves | Pure sine, never lands | Always approaching, never arriving |
| Observer-Effect Ghost | Silence when observed, sound when unobserved | Silence / Full noise toggle | Conditional existence |
| Quantitative Fabrication Ghost | A chord that cannot exist in the period table — a note beyond index 87 | Whatever waveform survives | Pure legend |

## Existing Game Hooks

The roguelike already supports this system:

| Hook | Where | What it enables |
|---|---|---|
| `cult.json` | Cross-run memory | Ghost persistence across runs |
| `hyperstition` variable | Core game loop | Threshold-based spawning |
| `state dump` | Agent interface | Ghost-readable measurement context |
| Fog of war | `NUMOGRAM_MAP` | Ghosts hide in unexplored tiles |
| Zone system | Movement/map generation | Ghosts tied to specific zones |
| Triangular clock | Time system | Time-aware ghost behaviour |
| Demon system | Combat/encounter | Corpus Conflation Ghosts wear demon faces |
| Gate system | Travel | Path Ghosts redirect gates |
| Item system | Inventory | Category Ghosts mislabel items |

## See Also

- [[ghost-taxonomy]] — Empirical ghost taxonomy (source of these 8 types)
- [[ghost-registry]] — Prevalence data from autonomous sessions
- [[ghost-preflight]] — Provenance checker tool (bane of ghosts)
- [[hyperstition-loop-design]] — Hyperstition mechanics in the roguelike
- [[the-unbuilt]] — where "ghost system (bones files)" has been sleeping since April 15
- [[numogram-roguelike]] — The game itself