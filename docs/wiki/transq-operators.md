---
title: Transq Operators — Reference
tags:
  - Transq
  - Training
  - CBD
  - CBI
  - Operators
  - Reference
  - Kernel-Regime
---

# Transq Operators — Reference

This page describes the operator families used inside the minimal **Transq Training Loop**. These operators allow the training process to balance exploration, coherence, and progress while treating the model as an active participant in its own development.

---

## Overview

The Transq Training Loop uses five families of operators:

- **Boundary Operators** — Navigate the structure of the loss landscape
- **Coherence Operators** — Expand capability without destroying verified structure
- **Exploration Operators** — Inject useful entropy and prevent premature convergence
- **Curriculum Operators** — Systematically expand the range of solvable tasks
- **Stabilization Operators** — Maintain or recover coherence under stress

Each operator interacts with the **uncertainty field** and **precision field** of the six-slot Machine, and must respect the **Coherence Corridor** (regression, reconstruction, and coherence gates).

---

## Boundary Operators

**Goal**: Help the training process understand and navigate the geometry of the loss landscape.

These operators are most closely aligned with **Cronkle Bisection Descent (CBD)**. They keep the model near meaningful interfaces (basin boundaries, ridges, separatrices) while representations are still forming.

### Key Operators

| Operator | Description | Best Used When |
|---------|-------------|----------------|
| **Basin Boundary Bisection** | Repeatedly narrow in on transitions between trajectories flowing to different basins | Early to mid training, when major structural choices are still open |
| **Saddle Probing** | Move toward regions of high curvature or index-1 critical points | Approaching performance plateaus |
| **Committor Estimation** | Estimate probability of ending in different basins under current noise | Deciding whether to commit to a basin |
| **Edge Tracking** | Maintain and periodically re-sample points near current basin boundaries | Long-running training with slowly changing landscapes |

### Interaction

- Strongly increase resolution in the **uncertainty field**.
- Avoid modifying high-precision regions unless necessary.
- Favored when the model is still in the kernel regime.

### Failure Modes

- Over-focusing on boundaries at the expense of progress.
- High computational cost in smooth or well-connected landscapes.

---

## Coherence Operators

**Goal**: Expand capability while protecting already-verified structure.

These operators form the practical core of **Coherence-Bound Induction (CBI)**. They treat training as a series of non-destructive edits.

### Key Operators

| Operator | Description | Corridor Strength |
|---------|-------------|-------------------|
| **Non-Destructive Adapter Update** | Apply changes via LoRA or similar adapters | Strong regression + reconstruction protection |
| **LoRA Tower Extension** | Stack new adapter layers for easy rollback and bisection | Excellent auditability |
| **Reconstruction-Preserving Edit** | Only accept updates that allow verified commitments to replay cleanly | Directly enforces reconstruction gate |
| **Coherence-Aware Regularization** | Add losses that penalize representation fragmentation | Supports coherence probe |

### Interaction

- Strongly respect the **precision field**.
- Preferred when corridor health is moderate or low.
- Enable safe, auditable expansion of the model.

### Failure Modes

- Patch pileup and loss of composability with too many stacked adapters.
- Overly conservative updates that slow progress.

---

## Exploration Operators

**Goal**: Increase exposure to novel structure and prevent stagnation.

These operators inject controlled entropy while attempting to stay within the coherence corridor.

### Key Operators

| Operator | Description | Notes |
|---------|-------------|-------|
| **Temperature Spiking** | Brief increases in sampling temperature followed by cooling | Controlled entropy injection |
| **Learned Sampling Policy** | Auxiliary head that predicts sampling parameters conditioned on internal state | Dynamic exploration modulation |
| **Rollout Braiding** | Inject fragments from previous rollouts into new ones | Creates topological mixing between episodes |
| **Internal State Perturbation** | Add noise to hidden states to encourage robustness | Prevents over-reliance on specific patterns |
| **Adversarial Prompt Injection** | Insert challenging prefixes then require recovery | Builds mode-switching resilience |

### Interaction

- Most effective when uncertainty is high but corridor health remains strong.
- Should be applied in lower-precision regions.

### Failure Modes

- Excessive noise leading to coherence collapse.
- Learned policies overfitting and losing transfer.

---

## Curriculum Operators

**Goal**: Systematically expand the range of solvable tasks while maintaining compositionality.

These operators control the *order and structure* of what the model learns.

### Key Operators

| Operator                            | Description                                                                   | Notes                                                |
| ----------------------------------- | ----------------------------------------------------------------------------- | ---------------------------------------------------- |
| **Ascension Maze**                  | Generator–solver adversarial curriculum using nested compositional challenges | Forces integration of multiple capabilities          |
| **Cluster-Based Reweighting**       | Dynamically adjust sampling frequency across feature clusters                 | Curriculum as a frequency spectrum over capabilities |
| **Frontier Expansion**              | Up-weight tasks the model is close to solving                                 | Focuses pressure on the current capability edge      |
| **Compression-Frontier Scheduling** | Prioritize data that is currently hard to compress but reachable              | Aligns with MDL pressure                             |

### Interaction

- Can steer the **uncertainty field** toward under-explored regions.
- Must not be allowed to degrade verified (high-precision) capabilities.

### Failure Modes

- Generator produces unsolvable or degenerate tasks.
- Stale curriculum that no longer matches the model’s current state.

---

## Stabilization Operators

**Goal**: Maintain or recover coherence, especially after stress or novelty injection.

These operators act as a counterbalance to more aggressive exploration and curriculum operators.

### Key Operators

| Operator | Description | Notes |
|---------|-------------|-------|
| **Internal State Rewards** | Reward desirable internal dynamics (attention entropy, hidden-state variance, productive SAE features) | Gives the model proprioception |
| **Proprioceptive Monitoring** | Track cheap internal signals as early warnings | Can trigger other stabilization operators |
| **Stochastic Rollback** | Inject controlled noise into recent edits to enable recovery | Useful after corridor violations |
| **Rollout Rehearsal** | Re-introduce fragments of older verified rollouts | Reinforces stable behaviors |
| **Checkpoint Gating + Soft Reset** | Frequent lightweight checkpoints with partial rollback | Default safety net during aggressive phases |

### Interaction

- Reduce unnecessary uncertainty caused by drift.
- Strongly protect high-precision regions.
- Strongly favored when corridor health drops.

### Failure Modes

- Over-stabilization leading to stagnation.
- Internal rewards being gamed without external improvement.

---

## Summary Table

| Family | Primary Focus | Risk Level | Main Alignment |
|--------|---------------|------------|----------------|
| **Boundary Operators** | Landscape navigation | Medium | CBD |
| **Coherence Operators** | Protect verified structure | Low–Medium | CBI |
| **Exploration Operators** | Entropy & novelty | Medium–High | General exploration |
| **Curriculum Operators** | Task ordering & composition | Medium | Long-term growth |
| **Stabilization Operators** | Recovery & maintenance | Low | Corridor health |

---

*These operator families together allow the Transq Training Loop to explore, expand, and stabilize in a principled way while remaining inside a coherence corridor.*