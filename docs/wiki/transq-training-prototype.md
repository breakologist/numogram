---
title: Transq Training Loop — Prototype Project
created: 2026-05-17
tags:
  - Transq
  - Training
  - Prototype
  - Project
  - CBD
  - CBI
---

# Transq Training Loop — Prototype Project

**Status:** Early design & planning  
**Last Updated:** 2026-05-19

---

## Project Overview

This project aims to build a minimal but principled implementation of the **Transq Training Loop** — a training system that combines elements of **Cronkle Bisection Descent (CBD)** and **Coherence-Bound Induction (CBI)** inside the six-slot Machine formalism.

The goal is to create a training process that:
- Keeps the model in the **kernel regime** for as long as useful
- Navigates the loss landscape deliberately
- Expands capability without destroying verified structure
- Maintains clear visibility into uncertainty, precision, and coherence

This is an exploratory prototype focused on **interpretability and correctness first**, with performance improvements to follow.

---

## Current Phase

**Phase 0 – Design & Planning**

- High-level architecture defined
- Operator families outlined
- Initial Transq Training Loop sketch complete
- Project tracking page created

Next: Begin implementation of core components (Coherence Corridor + basic operators).

---

## Key Goals

### v0.1 Goals (Minimal Viable Prototype)

- Implement a working Coherence Corridor (at least Regression + Coherence gates)
- Support 2–3 operator types (one Coherence, one Exploration)
- Basic scheduler with dynamic weighting
- Clear logging of uncertainty, corridor status, and operator decisions
- Run on a small transformer using Hugging Face + PEFT (LoRA)

### Longer-term Goals

- Full set of operator families
- More sophisticated scheduler logic
- Better uncertainty / precision field approximations
- Integration with existing tools (e.g. heerich, Reality Autoencoder ideas)
- Evaluation on more complex tasks

---

## Open Tasks

| Priority | Task | Notes | Status |
|----------|------|-------|--------|
| High | Define Coherence Corridor gates | Regression + Coherence to start | Not started |
| High | Set up small transformer + LoRA baseline | Hugging Face + PEFT | Not started |
| Medium | Implement basic Scheduler | Scoring-based with dynamic weights | Not started |
| Medium | Create first 2–3 operators | One Coherence, one Exploration | Not started |
| Medium | Build logging & metrics system | Uncertainty, corridor health, operator choices | Not started |
| Low | Sketch Uncertainty / Precision field approximations | Initial lightweight version | Not started |
| Low | Create project README / usage notes | For future sessions | Not started |

---

## Decisions Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-05-17 | Use Hugging Face + PEFT (LoRA) for updates | Aligns with non-destructive / Coherence Operator philosophy; memory efficient on 12GB card |
| 2026-05-17 | Prioritise interpretability over raw performance in v0.1 | "Correct first, then speed" approach |
| 2026-05-17 | Start with small transformer (4–6 layers) | Good balance of capability and inspectability |
| 2026-05-17 | Keep tracking lightweight (wiki-based project page) | Low overhead suitable for exploratory work |

---

## Implementation Progress

**Last Updated:** 2026-05-19

### Current State

We have completed the initial design phase and begun sketching concrete components for the Transq Training Loop prototype.

### Completed Design Work

- **Operator Interface** (`operators/base.py`)
  - Abstract base class with `apply()`, `estimate_cost()`, and `estimate_risk()` methods.
  - `OperatorResult` dataclass for consistent return values.

- **Coherence Corridor** (`core/corridor.py`)
  - `CoherenceCorridor` class with staged verification.
  - Two gates implemented:
    - `RegressionGate` — prevents capability regression.
    - `CoherenceProbe` — basic check for representation stability.

- **Scheduler** (`core/scheduler.py`)
  - Simple scoring-based scheduler using linear weighted sum.
  - Dynamic weight adjustment based on corridor health and uncertainty.
  - Supports occasional exploration via epsilon-greedy.

- **Coherence Operator** (`operators/coherence.py`)
  - `LoRAUpdate` — non-destructive low-rank adaptation.
  - Supports adapter tracking, cost/risk estimation, and rollback via `disable()`.

- **Exploration Operators** (`operators/exploration.py`)
  - `TemperatureSpike` — temporary increase in sampling temperature with cooldown.
  - `RolloutBraiding` — injects fragments from previous rollouts into current episodes.
  - `InternalStatePerturbation` — adds controlled noise to hidden states during training.

- **Curriculum Operators** (`operators/curriculum.py`)
  - `AscensionMaze` — generator-solver adversarial curriculum using nested compositional challenges.
  - `ClusterReweighting` — dynamic sampling frequency across feature clusters.

- **Stabilization Operators** (`operators/stabilization.py`)
  - `InternalStateRewards` — auxiliary rewards for healthy internal dynamics.
  - `StochasticRollback` — controlled noise injection for recovery.
  - `ProprioceptiveMonitoring` — lightweight diagnostic monitoring of coherence signals.

### TransqMachine Integration

A central `TransqMachine` class has been sketched to act as the state holder and integration point. It provides clean accessors for uncertainty, precision, corridor health, and progress signals, and owns the logger. This makes it easy for the scheduler and training loop to interact with the underlying model (including PEFT adapters) in a structured way.

### Coherence Corridor Evaluation Strategy

We have begun considering how the Coherence Corridor would work with a real transformer, including:
- Using a small fixed regression set for the Regression Gate.
- Measuring representation similarity (e.g. CKA) or attention stability for the Coherence Probe.
- Keeping checks lightweight enough to run frequently in early prototypes.

---

## Resumption Notes (May 2026)

When resuming this project next month, here’s the recommended starting point:

1. **Re-read** the following pages in order:
   - `transq-training-prototype.md` (this page)
   - `transq-operators.md`
   - `foom-superbase-training.md`

2. **Current best understanding**:
   - The loop should combine CBD-style boundary awareness with CBI-style coherence gating.
   - The scheduler uses a linear weighted scoring system with dynamic bias.
   - We are leaning toward a small transformer + PEFT (LoRA) for the first implementation.
   - Interpretability and correctness are currently prioritised over speed.

3. **Suggested first actions on resumption**:
   - Review the current operator sketches (especially `LoRAUpdate`).
   - Decide on the exact scope for v0.1 (how many operators, how minimal the corridor should be).
   - Begin implementing the core files in `/home/etym/foom/` following the structure in this page.

4. **Open questions worth revisiting**:
   - How sophisticated should the Uncertainty and Precision fields be in v0.1?
   - Should we support multiple simultaneous biases in the scheduler, or keep it simple?
   - What is the minimum viable version of the Coherence Corridor for a real transformer?

---

## Status Snapshot

| Area | Status | Notes |
|------|--------|-------|
| Architecture & Design | Solid | High-level structure and operator families are well defined |
| Operator Sketches | Good coverage | All five families have at least one concrete example |
| Scheduler | Basic version ready | Linear scoring with dynamic bias works; more advanced models (Pareto, UCB) noted for later |
| Coherence Corridor | Conceptual + light sketch | Regression + Coherence gates defined; transformer evaluation approach outlined |
| Logging | Lightweight design ready | Structured logging approach sketched |
| Implementation | Not started | Only `operators/base.py` has been written so far |
| Integration with real models | Early thinking | PEFT/LoRA direction chosen; concrete wiring not yet detailed |

---

## Relevant Links

- [[transq-operators]] — Detailed operator family reference
- [[foom-superbase-training]] — Kernel regime and CBD/CBI theory
- [[foom-semiodynamics-deep-dive]] — Broader semiodynamic context
- [[session-threads-2026-05-16]] — Related ideas from recent sessions
- [[foom-love-nuke]] — Theoretical foundation for coherence
- [[foom-universal-truth-machine]] — Oracle as UTM framing

---

*This page serves as the main coordination point for the Transq Training Loop prototype.*