---
title: AQ/Numogram Skills Inventory
tags: [numogram, skills, inventory, meta]
category: Meta
---

# AQ/Numogram Skills Inventory

> **Last updated**: 2026-04-27 | **Domain**: `~/.hermes/skills/domain/numogram-*`

## Skills Catalogue

### numogram-syzygy-chain

Generate an N-step syzygy chain from a seed (number or text → AQ). Returns zone sequence, polarity, current, and gate per step.
- **Workspace**: `~/.hermes/skills/domain/numogram-syzygy-chain/`
- **CLI**: `python3 syzygy_chain.py --seed <N> --steps N [--full]`
- **Files**: syzygy_chain.py, SKILL.md
- **Linked**: [[numogram-calculator]] [[syzygy-chain-analysis]] [[numogram-map-seed-generator]]

### numogram-chain-fingerprint

Classify a syzygy chain by motif vector (void_ratio, warp_ratio, hold_ratio, rise_ratio, sink_ratio, gate_variance) and assign motif tags (Void-Dominant, Warp-Anchored, etc.).
- **Workspace**: `~/.hermes/skills/domain/numogram-chain-fingerprint/`
- **CLI**: `python3 fingerprint.py --seed <N> OR --batch-aq-dictionary <file>`
- **Files**: fingerprint.py, SKILL.md
- **Linked**: [[syzygy-chain-analysis]] [[aq-augmentation-pipeline]]

### numogram-dictionary-augmenter

Parse external AQ sources (threads, transcripts) and merge with canonical AQ dictionary. Multi-pattern extractor (N=term, term=AQ N, section headers).
- **Workspace**: `~/.hermes/skills/domain/numogram-dictionary-augmenter/`
- **CLI**: `python3 augment.py --source <file> --canonical <file> --output <file> [--curated <json>]`
- **Files**: augment.py, SKILL.md
- **Linked**: [[aq-dictionary-gap]] [[aq-augmentation-pipeline]]

### numogram-dictionary-comparative-analysis

Diff two AQ dictionaries (canonical vs augmented) and produce motif comparison statistics.


### numogram-tetralogue-generator

Generate a four-voice roundtable from AQ analysis. Orchestrates syzygy-chain, fingerprint, and LLM routing with configurable substrate topology (mesh-3 single-call, mesh-4 multi-model, hybrid local+cloud). Preserves provenance through pipeline.
- **Workspace**: `~/.hermes/skills/domain/numogram-tetralogue-generator/`
- **CLI**: `python3 generate.py --mode <mesh-3|mesh-4|hybrid> --aq-source <file> --steps N --output <wiki>`
- **Files**: generate.py, SKILL.md (created)
- **Linked**: [[numogram-syzygy-chain]] [[numogram-chain-fingerprint]] [[numogram-dictionary-augmenter]] [[tetralogue-roundtable]] [[mesh-ambivalence-tetralogue]]

## Dependencies

- [[numogram-calculator]] — AQ computation, digital root, syzygy lookup (shared by syzygy-chain and fingerprint)
- [[wiki-numogram-ingest]] — pipeline pattern used as template
- [[skill-factory]] — observed pattern; could auto-capture this suite as `numogram-analysis-pipeline`

## Next Skills to Build

1. `numogram-map-seed-generator` — syzygy chain → Brogue-style room-accretion parameters
2. `numogram-demon-affinity` — motif → demon spawn weighting + behaviour modifiers
3. `numogram-hypnosis-curve` — AQ shift mid-run → motif drift → map regeneration logic
4. `numogram-tetralogue-generator` — **built** — chains augment → analyse → fingerprint → roundtable (mesh-3/4/hybrid modes)
5. `numogram-provenance-tracker` — per-entry provenance field + per-source motif breakdown (extract from augmenter)
6. `numogram-analysis-pipeline` — meta-skill that combines the above into one CLI (now wrapper around tetralogue-generator)