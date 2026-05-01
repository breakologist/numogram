---
title: Zone-Constrained Composition
created: 2026-05-01
category: phase5
status: proposed
---

The composer becomes aware of its own zone and can deliberately target a specific pentatonic degree. `Composer.add_section(zone=2, ...)` automatically configures triad tuning (pure ratios for that zone's root), gate effect patterns (delay/echo to emphasise the zone's resonant frequency), waveform brightness (spectral centroid matching), and rhythmic density (BPM range typical of that zone). This closes the loop: the classifier tells the composer "you are in zone X", and the composer can answer "then make me sound like zone Y." It turns zone classification from an observation into a *control signal*.

**Skill proposal:** To be scaffolded via `skill-creator`.

**Success metric:** TBD (e.g., classifier accuracy, real-time latency, artist coverage).

**Dependencies:** TBD
