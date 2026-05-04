# M2 Plan — VAE Hallucination with Iterative Projection
**Created**: 2026-05-03 (post-diagnostic)  
**Status**: ready-to-implement  
**Session handoff**: fresh session required to avoid context-stuffing; this file is the canonical source of truth

---

## 📋 Problem statement

| Metric | Target | Pre-fix | Post-fix goal |
|--------|--------|---------|---------------|
| Classifier accuracy | ≥80% | 0% | ≥80% |
| Audio variety | BPM spread, key variety, scale diversity | BPM ~125, key C/C#, scale 'unknown', density 0.2 | BPM variance ≥30, keys across circle, mixed scales, density variance |
| Human-listen score | ≥3/5 per zone | Not yet collected | ≥3/5 |

**Root causes**:
1. Hallucinated MIR vectors lie near centroids (92% nearest-centroid) but fall on wrong side of non-linear RF decision boundaries due to specific feature threshold violations (MFCC1/2 extremely shifted).
2. VAE decoder collapses to per-zone mode; `sigma_scale=0.25` + conservative MIR→parameter mapping yields uniform audio.

---

## 🛠️ Implementation steps (fresh-session checklist)

### Step 1 — Add iterative projection to `mir_to_mod.py`

**File**: `~/.hermes/skills/numogram-audio/mod-writer-composer/scripts/vae_m2/mir_to_mod.py`

**Functions to add**:

```python
def correct_to_zone(
    mir_scaled: np.ndarray,
    target_zone: int,
    scaler: StandardScaler,
    centroids_scaled: dict[int, np.ndarray],
    clf: RandomForestClassifier,
    eta: float = 0.15,
    max_steps: int = 10,
    tol: float = 0.01,          # stop when prediction flips and deltas shrink
    verbose: bool = False
) -> tuple[np.ndarray, dict]:
    """
    Iteratively nudge a scaled MIR vector toward its target zone centroid
    until the RandomForest classifier agrees, or max_steps is reached.

    Works in *scaled* feature space (StandardScaler units), because classifier
    was trained on scaled data. Small steps in scaled space correspond to
    perceptually tiny audio changes (<< JND for most timbral features).

    Returns:
        corrected_mir_scaled (1D array)
        trail: {'steps': int, 'flipped': bool, 'final_pred': int, 'deltas': [...]}
    """
    original_pred = clf.predict(mir_scaled.reshape(1,-1))[0]
    if original_pred == target_zone:
        return mir_scaled, {'steps': 0, 'flipped': False, 'final_pred': target_zone, 'deltas': []}

    mir_curr = mir_scaled.copy()
    centroid = centroids_scaled[target_zone]
    direction = centroid - mir_curr        # unit vector toward centroid
    step_norm = np.linalg.norm(direction)
    if step_norm < 1e-6:
        return mir_curr, {'steps': 0, 'flipped': False, 'final_pred': original_pred, 'deltas': []}
    direction = direction / step_norm

    trail = {'steps': 0, 'flipped': False, 'final_pred': original_pred, 'deltas': []}
    for step in range(max_steps):
        # Proposed move
        candidate = mir_curr + eta * direction
        pred = clf.predict(candidate.reshape(1,-1))[0]

        trail['steps'] += 1
        trail['deltas'].append(float(np.linalg.norm(candidate - mir_scaled)))

        if pred == target_zone:
            trail['flipped'] = True
            trail['final_pred'] = target_zone
            return candidate, trail

        # Not there yet — move a bit more aggressively next time (momentum)
        # But never overshoot centroid
        dist_to_cent = np.linalg.norm(centroid - candidate)
        if dist_to_cent < tol * step_norm:
            break  # close enough; stop to avoid jitter

        mir_curr = candidate

    trail['final_pred'] = clf.predict(mir_curr.reshape(1,-1))[0]
    return mir_curr, trail
```

**Integration point**: Inside `MirToMod.generate()` right after:

```python
# MIR physical already computed from latent decode
# -------------------------------------------------
if project:
    X_scaled = scaler.transform(mir_physical.reshape(1,-1))
    corrected, proj_trail = correct_to_zone(
        X_scaled[0],
        target_zone=self.target_zone,
        scaler=self.scaler,
        centroids_scaled=self.centroids_scaled,
        clf=self.classifier,
        eta=0.15,
        max_steps=10,
        verbose=False
    )
    # Flip back to physical space for downstream param mapping
    mir_physical = scaler.inverse_transform(corrected.reshape(1,-1))[0]
    metadata['projection'] = proj_trail
else:
    metadata['projection'] = None
```

**Sidecar update**: `mir.json` must now include:

```json
{
  "zone": 5,
  "aq": "...",
  "projection": {
    "steps": 3,
    "flipped": true,
    "final_pred": 5,
    "deltas": [0.42, 0.78, 1.13]
  }
}
```

---

### Step 2 — Increase latent dispersion

**Files**:
- `vae_sample.py`: `latent_zone_sample(zone, sigma_scale=1.0)`
- `vae_hallucinate.py`: add `--sigma-scale` arg (default 1.0)

In `latent_zone_sample()`:

```python
def latent_zone_sample(zone: int, vae, device, sigma_scale: float = 1.0) -> np.ndarray:
    # current: sigma = 0.25 * zone_std
    # new:      sigma = sigma_scale * zone_std
    # with sigma_scale=1.0 we get full training spread
```

In `vae_hallucinate.py` argparse:

```python
parser.add_argument('--sigma-scale', type=float, default=1.0,
                    help='Scale factor for latent sampling dispersion (default: 1.0 = full training std)')
```

---

### Step 3 — Re-run full pipeline

**Command**:

```bash
cd ~/.hermes/skills/numogram-audio/mod-writer-composer/scripts/vae_m2/
python vae_hallucinate.py \
  --latent-dim 10 \
  --empty-zones 3,4,5,8,9 \
  --samples-per-zone 20 \
  --mode zone \
  --sigma-scale 1.0 \
  --project
```

**Expected outputs**:
- `output/mod/*.mod` + `*.mir.json` (with projection metadata)
- `output/audio/*.wav`
- `output/classification/m2_report.json` with ≥80% accuracy
- `output/figures/mir_tsne_projected.png` (update t-SNE plot to colour-code projected points)

---

### Step 4 — Validation checklist

- [ ] Classifier accuracy ≥80% (aggregate across all 100 tracks)
- [ ] Per-zone accuracy ≥70% (allow weaker zones but not below 70%)
- [ ] Human listen: pick 5 tracks per zone (prioritize low BPM variance if needed) → score 1–5 on "zone recognizability" and "listening interest"
- [ ] Audio variety metrics:
  - BPM std ≥30
  - Key variety: at least 4 different keys per zone
  - Scale distribution: ≥30% non-'unknown'
- [ ] t-SNE shows hallucinated tracks shifted toward centroids without collapsing to single points
- [ ] All artifacts committed to `~/numogram/docs/data/phase5/validation/m2-run-1/`
- [ ] Wiki page created: `phase5-m2-vae-hallucination.md`

---

## 🔄 Fallback plan (if Step 1–3 fail)

**Failure mode A**: Projection does not increase accuracy above 60% after 10 steps.

- Train `vae_d16.pt` (d=16 latent) — more capacity to preserve zone cues
- Retry with `--sigma-scale 0.5` (moderate spread)

**Failure mode B**: Accuracy reaches 80% but audio remains too rigid.

- Add **feature-level jitter** after projection: `mir += np.random.randn(*mir.shape) * 0.03`
- Modify `mir_to_mod` param mapping to use *full* MIR range (not just near-zero):
  - `bpm = 80 + mir[11] * 120`  # instead of `mir[11] * 200`
  - `density = 0.1 + mir[10] * 1.8`  # ensure 0.1–1.9 range
- Inject **entropy-sourced noise** for each track (`entropy_hex` from `numogram-entropy-source`)

**Failure mode C**: Generator utterly ignores zone conditioning.

- Switch to **Conditional VAE** (CVAE) with zone label as auxiliary input
- Requires architecture change: encoder/decoder accept concatenated one-hot zone

---

## 📁 File inventory (canonical)

| Purpose | Path |
|---------|------|
| VAE trainer (d=10) | `vae_train.py` |
| Latent sampler | `vae_sample.py` |
| MIR→MOD inverter | `mir_to_mod.py` |
| Orchestrator | `vae_hallucinate.py` |
| Diagnostic script | `diagnostic_mir_centroids.py` |
| Pre-fix outputs | `output/` (mod, audio, classification, figures) |
| Post-fix outputs | `output_projected/`  ← new directory |
| Training artifacts (scaler, clf) | `~/.hermes/skills/numogram-audio/mod-writer/mod_writer/classifier/artifacts/` |
| Training MIR dataset | `dataset_balanced_900.npz` |
| Zone centroids (computed) | not saved yet — recompute on-the-fly in mir_to_mod for now |

---

## ⚙️ Git & wiki workflow

After successful run:

```bash
cd ~/numogram
cp -r ~/.hermes/skills/numogram-audio/mod-writer-composer/scripts/vae_m2/output_projected \
      docs/data/phase5/m2-hallucination/
git add docs/data/phase5/m2-hallucination/
git commit -m "Phase5 M2: VAE hallucination + iterative projection (sigma-scale=1.0, --project)
- 100 tracks (20× zones 3,4,5,8,9)
- Classifier accuracy: XX.X%
- Per-zone breakdown: {...}
- Variety: BPM μ=..., σ=..., key distribution: {...}
- t-SNE updated with projected points"
git push
```

Sync wiki:
```bash
# Copy summary to obsidian vault
cp ~/numogram/docs/wiki/phase5-m2-vae-hallucination.md \
   ~/.hermes/obsidian/hermetic/wiki/
# Commit vault separately
cd ~/.hermes/obsidian/hermetic
git add wiki/phase5-m2-vae-hallucination.md
git commit -m "M2 hallucination results (post-projection)"
git push
```

---

**Handoff complete** — when returning, load this file, implement Steps 1–4 in `mir_to_mod.py` and `vae_hallucinate.py`, then run the pipeline.
