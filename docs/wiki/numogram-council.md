---
title: Numogram Council
created: 2026-04-27
last_updated: 2026-04-27
tags: [council, multi-model, orchestration, voices, numogram]
status: draft
---

# Numogram Council

Multi-model deliberation engine for the Hermes Archive. Orchestrates the four voices (Oracle, Builder, Writer, Gamer) across temperature modes and provider backends.

## Plugin

Implemented in `~/.hermes/plugins/numogram-council/` as a Hermes Agent plugin. Handles:
- Model routing (analytical/balanced/creative modes)
- Voice-specific prompt construction
- Tetralogue orchestration
- Temperature-mode calibration

## Modes

| Mode | Temperature | Purpose |
|------|-------------|---------|
| Analytical | 0.3 | Canonical answers, implementable pseudocode |
| Balanced | 0.7 | Structured reasoning, trade-off analysis |
| Creative | 0.9 | Design questions, speculative exploration |

## Integration

Used by:
- `numogram-council-orchestrator` skill (delegate_task-based)
- `numogram-council-config` skill (provider/VRAM tuning)
- Direct council calls via `council_decide()` tool

## Status

- Active development (plugin stable as of Apr 2026)
- Supports local Ollama models and OpenAI-compatible APIs
- See also: [[four-voices]], [[local-model]], [[tetralogue]]

## See also
- [[ordo-amoris-888]]
- [[decimal-labyrinth-heresy]]
- [[tetralogue-ordo-amoris-888]]
- [[tetralogue-decimal-labyrinth-heresy]]

