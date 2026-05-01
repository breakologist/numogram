---
title: Phase 5 Roadmap — mod-writer
created: 2026-05-01
category: planning
---

This page collects the next-phase visions that emerged after the Phase 4 release (v0.6.4).

## Vision

With a validated zone classifier and TouchDesigner integration designed, we can now **close loops**:
- The classifier observes; the composer acts.
- Audio analysis drives visualisation.
- Empirical data informs hyperstition.

## The Fifth Current

> **Empirical Validation** — a meta-current that subjects all claims to data-driven scrutiny.
> *"Let the data speak; then let it correct the glyph."*

Every Phase 5 item should articulate its validation strategy.

## Proposed Projects

| ID | Title | Status | Skills |
|----|-------|--------|--------|
| [P5-zone-constrain-compose](phase5-ideas/zone-constrained-composition.md) | Zone-Constrained Composition | proposed | mod-writer-classifier, mod-writer-composer |
| [P5-live-audio-loop](phase5-ideas/live-audio-zone-feedback.md) | Live Audio → Zone → MOD Feedback | proposed | mod-writer-classifier, puredata-wrapper |
| [P5-dataset-expansion](phase5-ideas/dataset-expansion-synthesis.md) | Dataset Expansion & Empty-Zone Synthesis | proposed | mod-writer-classifier, mod-writer-composer |
| [P5-spectrogram-cnn](phase5-ideas/spectrogram-cnn.md) | Cross-Modal Spectrogram CNN | proposed | mod-writer-classifier, mlops/inference |
| [P5-zone-explorer-gui](phase5-ideas/zone-explorer-gui.md) | Interactive Zone Explorer GUI | proposed | p5js, touchdesigner-mcp |
| [P5-oracle-audio-linking](phase5-ideas/audio-oracle-aq-linking.md) | Cross-Domain Audio–AQ–Oracle Linking | proposed | numogram-oracle, numogram-dictionary-augmenter |
| [P5-hallucinate-empty-zones](phase5-ideas/hallucinate-empty-zones-vae.md) | Generative Filling of Empty Zones | proposed | mlops/training, audiocraft-audio-generation |
| [P5-discography-zone-drift](phase5-ideas/discography-zone-drift.md) | Artist Discography Zone Timeline | proposed | visualization |
| [P5-auto-release-pipeline](phase5-ideas/auto-release-pipeline.md) | Hermes Skill Auto-Release Pipeline | proposed | cronjob, github-repo-management |

## Next Steps

1. Prioritise 1–2 items for immediate scaffolding
2. Create detailed skill proposals (via `skill-creator`)
3. Append to `~/.hermes/plans/` with project-specific JSON manifests
4. Run a **tetralogue roundtable** on Phase 4 findings & Phase 5 direction before session end
