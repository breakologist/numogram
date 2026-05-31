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

### M2 — VAE Hallucination (May 6)
- 92% target accuracy on gap zones; all five empty zones now synthesizable.

## 2026-05-25 Empirical Findings (post-M1/M2)

- **Endian bug resolved** (actual fix date May 25, not May 9). Both `writer.py` copies updated; 9/9 ZoneComposer files now audible.
- **ZoneComposer spectral gap identified**: Single-section output is too thin vs. training corpus → classifier accuracy drops to 22.2% on real generated files.
- **Corpus centroid statistics** now available (global mean ~6924 Hz). `ZONE_DEFAULTS` require recalibration.
- M3 (live loop) remains blocked until composition density is increased to match corpus statistics.

These findings reinforce the Fifth Current: every autonomous session should escalate from symbolic to empirical verification as quickly as possible.