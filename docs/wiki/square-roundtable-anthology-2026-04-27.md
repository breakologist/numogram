---
title: Square Roundtable — Anthology (Seeds 7, 666, 123, 369)
date: 2026-04-27
tags: [numogram, council, tetralogue, anthology, seeds, syzygy]
---

# Square Roundtable — Anthology

Four tetralogue runs using **precomputed syzygy chains** from local seeds. Each run: 5 chains × 12 steps; fingerprint computed from aggregated zone visits; question fed to the Council (Oracle/Builder/Writer/Gamer) via Nous StepFun.

## Matrix

| Seed | DR* | Chains | Fingerprint | Void | Warp | Hold | Rise | Sink | Wiki |
|------|-----|--------|-------------|------|------|------|------|------|------|
| 7 | 7 | 5 | mixed-motif | 0.333 | 0.0 | 0.167 | 0.333 | 0.167 | [[square-roundtable-mesh-3-2026-04-27-seed7|page]] |
| 123 | 6 | 5 | mixed-motif | 0.0 | 0.333 | 0.167 | 0.333 | 0.167 | [[square-roundtable-mesh-3-2026-04-27-seed123|page]] |
| 369 | 9 | 5 | mixed-motif | 0.333 | 0.0 | 0.167 | 0.333 | 0.167 | [[square-roundtable-mesh-3-2026-04-27-seed369|page]] |
| 666 | 9 | 5 | mixed-motif | 0.333 | 0.0 | 0.167 | 0.333 | 0.167 | [[square-roundtable-mesh-3-2026-04-27-seed666|page]] |

> **DR*** = digital root of seed (zone start).

## Comparative notes

- All seeds classified as **mixed-motif** — none crossed the 60% dominance threshold.
- Ratios reflect syzygy topology: seeds starting in zone 3/6 introduce Warp; zone 0/9 produce Void; 1/8 produce Sink+Rise; 2/5 produce Hold.
- Despite ratio variation, council judges converge on same synthesis: the 47-entry AQ dictionary densifies the Numogram into an autophagic mythos.

## Raw data

- Seed 7 (DR 7): `generated/tetralogue_mesh-3_augmented_20260427_111557_seed7.json`
- Seed 123 (DR 6): `generated/tetralogue_mesh-3_augmented_20260427_112023_seed123.json`
- Seed 369 (DR 9): `generated/tetralogue_mesh-3_augmented_20260427_112132_seed369.json`
- Seed 666 (DR 9): `generated/tetralogue_mesh-3_augmented_20260427_111648_seed666.json`

## Context-only control

A control run with seed 7 and `--no-precompute` (no local chains computed) produced fingerprint `context-only`. The council still produced a similar synthesis, confirming the tetralogue's stability across data-depth variations.
