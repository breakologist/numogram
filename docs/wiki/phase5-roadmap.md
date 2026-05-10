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
> *\"Let the data speak; then let it correct the glyph.\"*

Every Phase 5 item should articulate its validation strategy.

## Proposed Projects

| ID | Title | Status | Skills |
|----|-------|--------|--------|
| [P5-zone-constrain-compose](phase5-ideas/zone-constrained-composition.md) | Zone-Constrained Composition | ✅ complete (96.4%, May 3) | mod-writer-classifier, mod-writer-composer |
| [P5-hallucinate-empty-zones](phase5-ideas/hallucinate-empty-zones.md) | VAE Hallucination of Empty Zones | ✅ complete (92%, May 6) | mlops/training, vae-hallucination, numogram-hallucination-pipeline |
| [P5-live-audio-loop](phase5-ideas/live-audio-zone-feedback.md) | Live Audio → Zone → MOD Feedback | 🔥 priority #1 | mod-writer-classifier, puredata-wrapper |
| [P5-audio-oracle-linking](phase5-ideas/audio-oracle-aq-linking.md) | Cross-Domain Audio–AQ–Oracle Linking | proposed | numogram-oracle, numogram-dictionary-augmenter |
| [P5-zone-explorer-gui](phase5-ideas/zone-explorer-gui.md) | Interactive Zone Explorer GUI | proposed | p5js, touchdesigner-mcp |
| [P5-dataset-expansion](phase5-ideas/dataset-expansion-synthesis.md) | Dataset Expansion & Empty-Zone Synthesis | proposed | mod-writer-classifier, mod-writer-composer |
| [P5-spectrogram-cnn](phase5-ideas/spectrogram-cnn.md) | Cross-Modal Spectrogram CNN | proposed | mod-writer-classifier, mlops/inference |
| [P5-discography-zone-drift](phase5-ideas/discography-zone-drift.md) | Artist Discography Zone Timeline | proposed | visualization |
| [P5-auto-release-pipeline](phase5-ideas/auto-release-pipeline.md) | Hermes Skill Auto-Release Pipeline | proposed | cronjob, github-repo-management |

## Completed Milestones

### M1 — Zone-Constrained Composition (May 3)
- **96.4%** overall accuracy (434/450 tracks, 50×9 zones)
- All zones ≥92% (Z4, Z6, Z8 at 100%)
- Real-world slice: 10/10 on artist-labelled zones 2 & 7
- Results: [[phase5-results/zone-constrain-compose-run-1]]

### M2 — VAE Hallucination of Empty Zones (May 6)
- **92%** target-zone accuracy across all five gap zones
- Z3=95%, Z4=90%, Z5=88%, Z8=95%, Z9=92%
- Ear test: 4.2/5 coherence
- Method: syzygy-walk latent sampling + iterative projection in scaled feature space
- Skills: `numogram-hallucination-pipeline`, `vae-hallucination`
- Results: [[phase5-results/phase5-m2-vae-hallucination]]

## Next Steps

1. ~~Prioritise 1–2 items for immediate scaffolding~~ — DONE (M1, M2)
2. ~~Create detailed skill proposals (via `skill-creator`)~~ — DONE (5 skills created)
3. **Current priority**: M3 — Live Audio → Zone → MOD Feedback (real-time closed-loop instrument)
4. M4 batch (oracle linking, spectrogram CNN, discography drift) can run in parallel
5. M5 (GUI, dataset, auto-release) — post-M3 polish pass

## See also

- [[zone_classifier_phase4.5_findings]] — Phase 4.5 validation results and classifier analysis
- [[phase5-validation-summary]] — Summary of Phase 5 validation runs
- [[tetralogue-phase4-review-phase5-direction]] — Tetralogue on Phase 4 review and Phase 5 direction
- [[mod-writer-validation]] — Mod-writer validation results
- [[zonecomposer-production]] — ZoneComposer production workflow
- [[mod-writer-gap-analysis]] — Analysis of gaps in MOD generation
- [[aq-augmentation-pipeline]] — AQ dictionary augmentation pipeline
- [[phase5-ideas]] — Directory of Phase 5 project ideas

---
*The Fifth Current demands empirical validation—let every claim be tested, every glyph corrected by data.*