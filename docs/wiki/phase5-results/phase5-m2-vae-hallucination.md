---
title: Phase 5 M2 — VAE Hallucination with Iterative Projection
created: 2026-05-03
updated: 2026-05-03
category: phase5-results
status: in_progress
tags: [phase5, vae, hallucination, iterative-projection, classifier-validation]
---

# M2 — VAE Hallucination (pre‑projection diagnostic)

> **Diagnostic run:** 2026‑05‑03 | 100 hallucinated tracks (20× zones 3,4,5,8,9)
> **Classifier accuracy (pre‑projection):** 0%
> **Nearest‑centroid (scaled features):** 92%
> **Mean target‑centroid rank:** 1.38 (86/100 are rank‑1)
> **Decision:** iterative projection in scaled feature space required

## 📊 Diagnostic figures

- [[figures/mir_tsne.png]] — t‑SNE of training + hallucinated MIR (scaled)
- Nearest‑centroid accuracy (raw): 86.0%
- Nearest‑centroid accuracy (scaled): 92.0%

## 🔍 Root‑cause analysis

The RandomForest classifier was trained on **StandardScaler‑transformed** MIR features. Hallucinated vectors are **geometrically close** to their zone centroids (Euclidean distance) but their **specific feature thresholds** are shifted:

| Feature | Mean delta (hallucinated − target centroid) |
|---------|---------------------------------------------|
| mfcc1   | +122.5 |
| mfcc2   | +86.0 |
| mfcc5   | +0.058 |
| key_C   | -0.030 |
| key_C#  | +0.009 |

These large MFCC deviations push points into wrong RF leaves despite overall proximity. The classifier’s decision boundaries are **piecewise‑constant**; a single early split on `mfcc1` can determine the predicted class regardless of other features.

## 🎵 Audio rigidity audit

All 100 tracks share nearly identical rendering parameters:

- **BPM:** ~125 (±1)
- **Key:** C or C# only
- **Scale:** 'unknown' (100%)
- **Density:** 0.2 (minimum)

**Causes:**
1. **VAE decoder collapse** — decoder learns to ignore latent codes and output the per‑zone mode.
2. **Conservative `mir_to_mod` param mapping** — `bpm = mir[11] * 200` saturates at ~125 because `mir[11]` ≈ 0.625 for all hallucinated vectors; similarly for density, key, and scale.

3. **Latent sampling σ too small** — `sigma_scale=0.25` × zone std yields tight clusters.

## 🎯 Remedy: iterative projection

We will nudge hallucinated MIR vectors in **scaled feature space** toward their target zone centroid until the RandomForest agrees. Because the space is StandardScaler units, a step size `η=0.15` corresponds to ~0.15σ per feature — far below just‑noticeable differences for timbral features.

**Algorithm:** gradient‑free walk along the centroid direction. Stop when:
- predicted class == target zone (success), or
- `max_steps=10` reached (failure)

Expected: 1–4 steps per track. Per‑zone accuracy should rise from 0% → ≥80%.

## 📈 Parallel variety boost

Simultaneously increase **latent dispersion**:

```bash
--sigma-scale 1.0   # full training spread (instead of 0.25)
```

This causes the VAE decoder to explore more of its conditional output space, producing varying BPMs, keys, and densities. After projection, these diverse points will still land in the correct zone.

**Optional post‑projection jitter** (if still too rigid):
```python
mir += np.random.randn(*mir.shape) * 0.03   # tiny random walk staying within class
```

## 📁 Outputs (pre‑projection)

| Artifact | Path |
|----------|------|
| MOD files | `vae_m2/output/mod/*.mod` |
| WAV renders | `vae_m2/output/audio/*.wav` |
| Sidecar MIR JSON | `vae_m2/output/mod/*.mir.json` |
| Classifier report | `vae_m2/output/classification/m2_report.json` |
| t‑SNE figure | `vae_m2/output/figures/mir_tsne.png` |
| Diagnostic JSON | `vae_m2/output/diagnostic_report.json` |

## 🚀 Next actions (fresh session)

1. Implement `correct_to_zone()` in `mir_to_mod.py`
2. Add `--project` import path + logic to `MirToMod.generate()`
3. Expose `--sigma-scale` in `vae_hallucinate.py` (default 1.0)
4. Re‑run full pipeline with `--sigma-scale 1.0 --project`
5. Validate: classifier accuracy ≥80%, per‑zone ≥70%
6. Human listen (5 tracks/zone), update wiki
7. Commit to `~/numogram` and sync vault

---

**Plan file:** `~/.hermes/plans/m2-iterative-projection-plan.md`  
**M1 results:** `phase5-results/zone-constrain-compose-run-1.md`
