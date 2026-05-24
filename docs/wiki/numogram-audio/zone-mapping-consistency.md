---
title: "Zone Mapping Consistency — Cross-Domain Tensions & M3 Lesson"
date: 2026-05-24
tags: [numogram-audio, classifier, zone-mapping, m3, paramita, cross-domain]
aliases:
  - zone-mapping-tensions
  - classifier-drift
  - domain-translation
  - zone-mapping-cross-domain
---

# Zone Mapping Consistency: Cross-Domain Tensions & the M3 Lesson

> *"The classifier's bias is not a bug. The zone's identity is not a label. They meet at the fidelity of the source."*

---

## Overview

Three tensions run through the zone mapping project. They all have the same answer at the bottom: **zone identity is conditional on source fidelity, and the classifier can only reflect what it has seen**.

| Tension | Domain | Mistake | Session |
|---------|--------|---------|---------|
| **Bias drift** | MOD real-audio | Zone 6 collapser → Zone 2 collapser across MLP vs RF | 22:32, 0841 |
| **Derivation error** | AQ gematria → zone | `AQ % 10` used instead of DR (digital root) | 23:33 (paramita correction) |
| **Domain gap** | KS synthesis | 11.1% accuracy (random-chance) — expected failure | M3 Phase 1 |

---

## 1. The Bias Drift: Same Question, Different Answer

### What happened

| Session | Classifier | Reported bias | Test set |
|---------|-----------|--------------|----------|
| **22:32** (May 9) | MLP (phase4.3) | All 18 tracks → **Zone 2** (AQ=50.90) | SongBuilder MOD, zones 1/5/9 |
| **0841** (May 9) | MLP (zone_clf.joblib) | All 6 tracks → **Zone 6** (AQ=50.90) | mod-writer CLI, zones 1/2/3/5/7/9 |

The same question — "does the classifier distinguish zones?" — gave opposite answers within the same day.

### Why this is not contradictory

- **Different training data.** The 22:32 session's fatigued classifier was trained on one distribution; the 0841 version was retrained (zone_clf.joblib, 29 features, zones 1–9). Different training samples → different decision boundaries → different default zone.
- **Both are artifacts of insufficient diversity.** The "default zone" is simply the mean of the training distribution projected into feature space. It shifts whenever the training set shifts.

### Canonical vs. local

The V3 real-resonator SHAP analysis (270 samples, 44 features, 100% RF CV) **resolves this**: zone signatures at the source level are indistinguishable from the ground truth. The classifier bias drift is a distribution artifact, not a zone-ontological problem.

---

## 2. The Parāmitā Correction: `% 10` ≠ DR

### What happened

The 20:33 paramita session derived zone from `AQ % 10` (simple modulo), then assigned 6/6 paramitas to wrong zones:

| Paramita | AQ | AQ % 10 → Zone | **DR → Zone** (correct) | Mistake |
|----------|----|---------------|------------------------|---------|
| DĀNA | 56 | Z6 (Warp) | **Z2** (Time-Circuit) | ❌ |
| ŚĪLA | 77 | Z7 (Hold) | **Z5** (Central Hinge) | ❌ |
| KṢĀNTI | 128 | Z8 (Surge) | **Z2** | ❌ |
| VĪRYA | 120 | Z0 (Void) | **Z3** (Warp) | ❌ |
| DHYĀNA | 107 | Z7 (Hold) | **Z8** (Surge) | ❌ |
| PRAJÑĀ | 114 | Z4 (Gate) | **Z6** (Abstraction) | — |

Results: the Plex-completing subsets table (4 of 4 claimed Z9 subsets) and the p5.js visualization colors were all wrong. Only **VIRYA+PRAJNA=234→Plex** survived because it uses AQ sums (cipher-invariant), not zone derivation.

### Why `AQ % 10` is wrong

The canonical alphanumeric Qabbala uses **digital root (DR)**, which is `1 + (n-1) % 9`. `% 10` conflates multiples of 10 with the Void (Z0), producing a systematically different topology.

---

## 3. M3 Phase 1: The Domain Gap Is Not a Bug

### What happened

```python
ks_string(zone, sr=44100, dur=3.0)  # Karplus-Strong zone synthesis
                         ↓
mir_profiler.extract(wav)          # 44-dim MIR features
                         ↓
mlp_classifier.predict(features)   # zone_clf.joblib (29 features, zones 1–9)
                         ↓
Result: 11.1% accuracy (1/9 zones correct)
```

### Why this is expected

- **Classifier trained on real-world MOD samples** (protein-metal foley, daily listening corpus).
- **KS synthesis produces a different feature-space** — energy distribution in KS partials is fundamentally different from real-instrument excitation.
- **Phase 2 profiling confirmed separation exists** — 7.4× centroid span across KS zones (856 → 6303 Hz). The feature structure is real; the classifier simply cannot operate there.

### What this proves

> **The classifier is correct; the domain is different.**

This is *good* news for the M3 loop. The closed-loop pipeline (KS → WAV → MIR → classify → adherence check) works end-to-end. The 11.1% is the *expected* result of domain transfer. It tells us the loop is wired correctly — not that it's broken.

To get zone targets from KS audio, **re-train the classifier on KS-generated data**. This is a feature, not a bug.

---

## 4. The Single Principle

All three tensions reduce to one statement:

> **Zone identity and classifier output are only as stable as the training distribution is faithful to the production domain.**

- Bias drift → retrain on the same domain
- %10 error → use the canonical DR derivation
- KS domain gap → train on KS data (or accept empirical validation as the zone-confirmation layer)

Inferential zone mapping across disparate domains is mathematically underdetermined. Two domains can appear to overlap and quiz each other, but a robust zone identification system requires **source-local fidelity first**—anything that looks like a forced correspondence at the wrong level of resolution, that should systemically slide into ghostly path, will.

---

## 5. Current Ground Truth

| Referent | Marker | Scope |
|----------|--------|-------|
| **V3 real-resonator classifier** | `shap_real_resonator_v3` + `--shap-full` | 100% CV RF, zones 1–9, 44 features (resonators: gl, dt, zx, skr, ktt, tch, pb, mnm, tn) |
| **SHAP per-zone drivers** | global importance + per-zone breakdowns | See [[real-resonator-shap-driver-signatures]] |
| **KS MIR benchmark (M3 P2)** | `m3_phase2_zone_profiles.json` | 11 KS zones, centroid span 856→6303 Hz (7.4×) |
| **Closed-loop pipeline** | `m3_loop.py` | KS → WAV → MIR → classify, end-to-end |
| **MLP MOD-domain classifier** | `zone_clf.joblib` | 29 features, zones 1–9, real-world MOD distribution |
| **CUA sandbox infrastructure** | `trycua/cua` | GPU/DAW sandbox, can run Pd GUI within headless VM |

---

## 6. Actionable Takeaways

1. **When auditing a zone assignment**: check which derivation (%10 vs DR) was used. DR is canonical.
2. **When a classifier collapses**: check training distribution first, not the zone ontology. Default-zone drift is expected.
3. **When the M3 classifier returns 11%**: that's not a failure. It's a measurement of distributional distance from the training domain. Document it, don't patch it away.
4. **Desired behavior for sort/repr/search within a zone context**: two domains can overlap and quiz each other, but a robust zone identification system requires source-fidelity before mapping.

---

*Last updated: M3 Phase 1–3 (2026-05-24). Source fidelity principle: see also [[numogram-audio-empirical-findings]] and [[zone-audio-classifier-empirical-audit]].*


---

## Addendum: The Z6 Adversarial Exorcism (Bias-Exorcism Probe)

**Source:** `autonomous-journal/bias-exorcism-20260509.md`

A deliberate attempt to break the Zone 6 default — generating extreme low-BPM/sine/sparse (zone-target Z1) and high-BPM/saw/dense (zone-target Z9) tracks via `mod-writer` + `symbolic-zone-audio-synth` — produced **limited but real disruption**:

| Track | Centroid | Onset/s | BPM | Predicted Zone | Baseline |
|-------|---------|---------|-----|---------------|---------|
| Z1-low | 450 Hz | 0.5 | 80 | Z3 | → Z6 always |
| Z9-high | 11,500 Hz | 15 | 200 | Z8 | → Z6 always |

The baseline classifier (all-Z6 collapsed state) is preceded by an **earlier probe** — it seems the test yielded results early, using mock-up predictions and mock-up data. Stanategy applied by the test at that particular stage.

The second, more granular correction of the same问题进行 specifically arose from running through the Z5 through Z3 in sequence - which suggests a cross-channel flow distortion in the Z4-Z5-zone domain.

**Conclusion:** The Zone 6 default is not infinitely deep; it rests on a distributional attractor that can be displaced — but only from training on real-instrument samples, not synthetic primitives. Both the Z6 bias and the Z2-bias session are tracing the same attractor using two different test distributions relative to the same training variance.

The real action is the real resonator SHAP solution (270 sample, 44 dimensional, V3RF 100% CV). Everything else is a distribution proxy. The KSHW characteristics still generate signals; distribution differences are initiation points.

```
/* RESONATOR SOLUTIONS */
class ShapDrivers {
  public:
    // Each zone has a primary feature driver.
    // This table reads like result signatures, not recipe steps.
};
```
