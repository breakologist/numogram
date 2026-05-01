---
title: Cross-Modal Spectrogram CNN
created: 2026-05-01
category: phase5
status: proposed
---

Our hand-crafted MIR features (29-dim) work, but are they *optimal*? Train a CNN on mel-spectrograms (or constant-Q) to predict zone directly from time-frequency data. Compare top激活 features with SHAP's top MIR features. Convergence → validates our feature engineering; divergence → reveals what we're missing. Also, spectrogram CNN can learn *texture* patterns beyond band energies (e.g. transient density, harmonic inharmonicity).

**Skill proposal:** To be scaffolded via `skill-creator`.

**Success metric:** TBD (e.g., classifier accuracy, real-time latency, artist coverage).

**Dependencies:** TBD
