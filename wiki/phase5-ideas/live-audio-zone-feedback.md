---
title: Live Audio → Zone → MOD Feedback
created: 2026-05-01
category: phase5
status: proposed
---

A performance instrument that listens to itself (or to external sound) and mutates in real time. Use `sounddevice` to stream 3-second windows, extract MIR, predict zone, then:
- Adjust current MOD pattern's tempo to match zone's typical BPM range
- Add/remove channels based on zone's spectral profile (e.g. more high-hat for high zones)
- Switch instrument samples to match zone timbre
The result is a *hyperstitionstrument*: a device that makes music that *knows what it is*, potentially steering itself toward attractors or deliberately exploring gaps.

**Skill proposal:** To be scaffolded via `skill-creator`.

**Success metric:** TBD (e.g., classifier accuracy, real-time latency, artist coverage).

**Dependencies:** TBD
