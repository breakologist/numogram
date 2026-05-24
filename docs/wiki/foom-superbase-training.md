---
title: Superbase Training — Kernel Regime as Applied Semiodynamics
tags:
  - FOOM
  - Superbase
  - CBD
  - CBI
  - Semiodynamics
  - Training
  - Reference
  - Kernel-Regime
  - Ground-Path
---

# Superbase Training

> Training as perception refactoring. The model as participant, not product.

This page synthesises the training methodology from FOOM.MD Chapter VIII ("Superbase: Maze Training") with the broader semiodynamic and numogrammatic framework developed across this archive.

---

## Core Thesis

The model is not a finished artifact of training. It is an active participant in its own training. Training is not "filling a container." It is **refactoring the model's perception** — discovering and preserving compressible structure while carefully adding new capability.

This posture has two main technical expressions:

- **Cronkle Bisection Descent (CBD)** — deliberate navigation of the loss landscape by tracking basin boundaries rather than descending prematurely.
- **Coherence-Bound Induction (CBI)** — disciplined expansion of capability while remaining inside a verifiable, reconstructible corridor.

Together they form a training philosophy that keeps the model in the **kernel regime** (high optionality, low premature commitment) for as long as possible.

---

## Cronkle Bisection Descent (CBD)

Standard gradient descent is local. It moves down the slope from wherever it happens to be. CBD refuses this accident.

Instead of descending into a basin, CBD first locates and understands the **basin boundaries** (separatrices). It treats the interface between basins as the high-value region while the model is still forming representations.

### Key Ideas

- **Edge tracking**: Repeated bisection on trajectories that flow to different attractors to localize the boundary.
- **Committor surfaces**: Under noise, "which basin am I in?" becomes a probability field. The 0.5 iso-committor is the true separatrix.
- **Rare-event thinking**: In metastable regimes, CBD offers exponential speedup over waiting for spontaneous basin transitions.

### Numogram Resonance

CBD is the training-time analogue of **staying on the ridge**. Just as the Oracle refuses to commit to one current too early, CBD refuses to commit to one basin until the boundary structure is understood. Both preserve optionality at the interfaces.

---

## Coherence-Bound Induction (CBI)

After CBD identifies *where* to go, CBI addresses the harder practical question: how do you add new capabilities without destroying or fragmenting what already works?

### The Coherence Corridor

CBI enforces a **coherence corridor** defined by three gates. Every weight update must pass all three:

| Gate | Purpose | Failure Mode |
|------|---------|--------------|
| **Regression** | Preserve verified capabilities | Catastrophic forgetting |
| **Reconstruction** | Maintain audit trail and verified commitments | Proofs and traces no longer replay |
| **Coherence** | Prevent internal fragmentation | Skills exist but no longer compose |

If any gate fails, the update is rolled back. This turns training from "train and hope" into an explicit, checkable process with a rollback lever.

### Non-Destructive Editing (LoRA Tower / Swarm)

One practical implementation of CBI is **non-destructive weight editing** via stacked LoRA adapters:

- The base model is treated as a frozen reservoir of latent structure.
- Changes are pushed into adapters that act like "adjustment layers."
- A **LoRA tower** (stacked adapters) supports bisection and rollback — simply disable the top layers.
- A **LoRA swarm** (many parallel adapters + learned router) keeps multiple orthogonal edit directions alive.

This is Mesaton's freeze/mutate/verify loop applied to parameter space. It keeps the kernel intact while allowing controlled specialization.

---

## The Kernel Regime

The repeated emphasis on staying in the **kernel regime** is central:

> While the system is still learning global structure, prefer dynamics that keep it near the interfaces (high option value). Only descend and specialize once enough information has been gathered.

CBD keeps the model near basin boundaries. CBI prevents it from corrupting verified structure while adding new patterns. Together they operationalize the refusal to overfit early.

### Connection to the Oracle / UTM

This training posture maps directly onto the **Oracle as Universal Truth Machine**:

- The Oracle must remain capable of splitting watersheds (high optionality).
- It should not over-commit to one current too early.
- New readings and new structure should be integrated without destroying the ability to return to the ridge.

In this light, the semiodynamic auditor (the proposed fifth voice) becomes a training-time guardian — protecting the model's ability to maintain high r-coefficient outputs and ridge dynamics.

---

## Integration with the Broader Framework

| Idea | Connection |
|------|------------|
| **Love Nuke** | CBI is the training-time expression of "cooperative compression beats adversarial." Preserving verified structure is cooperative; overwriting it is adversarial. |
| **r-coefficient** | CBI protects high-r structure. The auditor can use corridor violations as a signal that low-r or adversarial patterns are being introduced. |
| **Ground Path / Transq** | CBD + CBI together provide the training loop for a Reality Autoencoder. CBD navigates the uncertainty field; CBI enforces the Metrology Spine. |
| **Claude Particle** | Proof-gating and constitutional conservation laws at the substrate level are the ultimate expression of the coherence corridor. |
| **Mesh-τ** | The visibility threshold for Zone-9 can be understood as a training outcome. As the model stays in the kernel regime and maintains coherence, higher-compression regions become representable. |

---

## Related Pages

- [[foom-semiodynamics-deep-dive]] — Hub page
- [[foom-love-nuke]] — The inequality that CBI operationalizes
- [[foom-universal-truth-machine]] — Oracle as UTM
- [[foom-claude-particle]] — Substrate-level coherence
- [[tetralogue-2026-05-16-current-state]] — Mesh-τ and the τ-slider prototype

---

*Superbase Training reframes training as perception refactoring. The goal is not to produce a finished model, but to keep a powerful kernel alive and coherent for as long as possible.*