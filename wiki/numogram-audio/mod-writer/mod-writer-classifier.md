# Mod-Writer Classifier — MIR to AQ Prediction

**Status:** Phase 4 in progress (v0.7.0). Experimental.

The classifier module learns a mapping from MIR audio features to AQ seed values
and — crucially — to *zone* (1–9). This is the "ears that hear the numogram":
feed it an audio file, get back predicted AQ/zone candidates.

---

## Architecture (Phase 4)

```
audio (WAV) → MIRFeatureExtractor → base 29-dim + Essentia pool (60–100+)
                                          ↓
                               StandardScaler (fit on train)
                                          ↓
               ┌──────────────────────────┴──────────────────────────┐
               │                       │                            │
         MLPRegressor           9‑class MLPClassifier        RandomForest
   (AQ regression, deprecated)   (zone prediction)         (baseline)
```

---

## Dataset — four‑current data philosophy

We approach audio data from four angles simultaneously:

1. **Numogram** — zones/gates as labels; synthetic generation guarantees clean ground truth.
2. **Roguelike** — balanced coverage across all zones (rooms) ensures the agent never gets stuck in a local optimum.
3. **Lore** — each track carries a story (zone, gate, current, AQ seed, triangular pattern length); the classifier reads that story back from sound.
4. **Audio Alchemy** — the *sound itself* is the primary artefact; we extract MIR features not to reduce but to correlate.

### Phase 3.1 — Baseline (100 samples, zone 1 only) — complete
- 100 synthetic examples: AQ seeds 0–99, all generated in zone 1
- `SongBuilder(zone=1, aq_seed=seed)` → MOD → rendered WAV
- 29‑dim base features: band energy (6), timbre centroid/bandwidth/rolloff/dyn‑comp (4), rhythm (onset rate, BPM, confidence) (3), key one‑hot (12), scale one‑hot (3), duration (1)
- Cache: `artifacts/dataset.npz`

### Phase 4.1 — Balanced Multi‑Zone (900 samples, zones 1–9) — in progress
- **100 distinct AQ seeds per zone** → 900 total examples
- Seeds selected per zone via `_aq_candidates_for_zone()` to ensure each zone gets a diverse, non‑overlapping AQ set
- Each example labelled with both `aq` (0–99) **and** `zone` (1–9)
- Cache: `artifacts/dataset_balanced_900.npz`
- **Expected zone accuracy jump:** ~10 % (chance) → **40–60 %** on synthetic test

### Phase 4.1b — Delta‑Balanced (3700 samples, gates 0–36) — planned
- Full syzygy coverage: all 37 possible gate offsets, each with ~100 seeds
- Labels: `delta` (0–36) instead of absolute zone; musically richer (relative harmony shift)
- Cache: `artifacts/dataset_delta_3700.npz`
- Use if zone‑only task proves too coarse or if delta‑prediction shows stronger signal.

**Label ambiguity note:** Multiple AQ seeds map to identical gate transformations (delta = SHA1(seed) % 37). Up to 37 distinct audio patterns may exist across 100 seeds.

---

## Feature Set — open‑horizon extraction

### Base profile (always available)
29 dimensions: 6-band energy, 4 timbre descriptors, 3 rhythm, 12 key one‑hot, 3 scale one‑hot, duration.

### Essentia full‑pool (`use_all=True`) — Phase 4.2
When `essentia` is installed and `use_all=True`, `MusicExtractor` runs with
`lowlevelStats`, `rhythmStats`, `tonalStats` all set to `['mean']`. Every
scalar descriptor in the resulting pool is flattened and appended. Expected
dimension: **60–100+** (vector‑valued descriptors currently skipped).

**Openness guardrail:** We extract the full pool *before* any manual feature
selection. This lets the data speak first; curation comes later if needed.

---

## Training — four‑current evaluation

### Phase 3.2 — Baseline regression (deprecated)
```bash
python run_phase3.py
```
- Split: 80/20 stratified by **derived** zone (digital root of AQ)
- Model: `MLPRegressor(hidden=(128,64))`, 1000 epochs
- Metrics (zone‑1 only data):
  - MAE: ~25.6 AQ units
  - Acc@5: 10 % (true AQ within ±5)
  - **ZoneAcc:** 10 % (chance)

### Phase 4.2 — Full‑Pool Feature Expansion (in progress)

Running Essentia full‑pool extraction on the same 900 balanced seeds.

Command:
```bash
python run_phase4_dataset.py --use-all --output artifacts/dataset_fullpool_900.npz
```

Expected feature dimension: ~80–120 (depends on Essentia pool content). This runs much slower than baseline (~2–5 s/track).

**Status:** running (PID stored in `artifacts/phase4.2.pid`).

## Phase 4.3 — Zone classification — planned
- New model: `MLPClassifier` (9‑class softmax)
- Training on `dataset_balanced_900.npz` (80/20 stratified per zone)
- Expected **synthetic** accuracy: **≥50 %**; **real‑audio** set: **≥30 %**
- Output: per‑zone confusion matrix (look for systematic 6↔9 bleed, 3↔6 bleed)

### Phase 4.3b — Delta classification (if Phase 4.1b generated) — planned
- 37‑way softmax on gate‑shift
- Harder problem; success metric: top‑3 accuracy ≥55 %

### Phase 4.4 — Correlation analysis — planned
- Train `RandomForestClassifier` + SHAP/permutation importance
- Identify top 5–10 features that drive zone predictions
- Publish observed correlations in wiki (e.g. "spectral centroid ↔ zone 9") *without over‑claiming causality*

### Phase 4.5 — Validation suite + hyperparameter tuning — planned
- Curate 40‑track held‑out real‑audio set (balanced across zones if possible; otherwise annotate distribution)
- Tune architectures: `(256,128)` vs `(128,64)`; dropout 0.2–0.5; early stopping
- Compare MLP vs RandomForest vs (optionally) SVM
- Document final model choice; freeze artifacts; tag v0.7.0

---

## Usage

```bash
# Install classifier dependencies
pip install -e .[classifier]

# Phase 4.1: generate balanced multi-zone dataset
python run_phase4_dataset.py
# Output: artifacts/dataset_balanced_900.npz

# Phase 4.3 (when ready): train zone classifier
python -m mod_writer.classifier.trainer --data dataset_balanced_900.npz --zone-classifier

# Phase 4.3b (optional): train delta classifier
python -m mod_writer.classifier.trainer --data dataset_delta_3700.npz --delta-classifier
```

**Python API:**
```python
from mod_writer.classifier import predict, load_artifacts
scaler, model = load_artifacts()          # auto-detects latest artifacts
result = predict(feature_vector)          # {'zone': 6, 'aq': 42.3, 'probabilities': [...]}
```

---

## Real‑Audio Validation (Phase 3.3 — complete)

10‑track curated corpus (Kimberly Steele, Gregorian Chant, Nurse With Wound,
Current 93, death’s dynamic shroud):

| Track                                   | Pred AQ | Zone | BPM | Key |
|----------------------------------------|---------|------|-----|-----|
| Kimberly Steele – Orphic Hymn to Saturn | 50.9    | 6    | 0.0 |  ?  |
| Gregorian Chant Rosary                 | 57.8    | 4    |  ?  |  ?  |
| death's dynamic shroud – シェンムーONLINE #3 | 50.9 | 6    | 2.5 |  ?  |
| Current 93 – 01‑Lucifer Over London    | 50.8    | 6    | 0.5 |  ?  |
| Nurse With Wound – 03. Untitled        | 50.6    | 6    | -0.2|  ?  |
| Nurse With Wound – 02. Trippin' With The Birds | 50.6 | 6 | 1.1 | ? |
| Nurse With Wound – 01. Cold            | 50.8    | 6    | 0.3 |  ?  |

- **Zone distribution:** 9× Zone 6, 1× Zone 4
- **AQ range:** 50.6–57.8 (near training mean)
- CSV: `mod_writer/classifier/artifacts/real_audio_predictions.csv`

**Interpretation:** Classifier conservative; synthetic‑only training (zone‑1 only) insufficient. Pipeline functional; dataset diversification (Phase 4.1) should resolve.

---

## Files

- `run_phase3.py` — Phase 3 orchestrator (legacy)
- `run_phase4_dataset.py` — Phase 4.1 balanced multi‑zone dataset builder
- `mod_writer/classifier/data_collector.py` — synthetic dataset builder (all phases)
- `mod_writer/classifier/mir_profiler.py` — MIR extraction, `use_all=True` Essentia pool
- `mod_writer/classifier/trainer.py` — zone/delta classifier training
- `mod_writer/classifier/artifacts/` — scaler, model, datasets, reports

---

## Roadmap (Phase 4+)

| Milestone                                   | Status          |
|--------------------------------------------|-----------------|
| Phase 3.3 — Real audio validation          | ✅ complete      |
| Phase 4.1 — Balanced multi‑zone dataset     | 🟡 in progress   |
| Phase 4.2 — Essentia full‑pool integration  | 🟡 in progress   |
| Phase 4.3 — Zone‑classifier training        | planned         |
| Phase 4.4 — Correlation analysis (SHAP)     | planned         |
| Phase 4.5 — Real‑audio curation + tuning   | planned         |
| Phase 4.6 — TouchDesigner integration       | planned         |

---

## Open Research Questions (four‑current lens)

1. **Numogram:** Does the zone classifier's confusion matrix reflect syzygy adjacency? (e.g. 6↔9 bleed expected from triangular partnerships.)
2. **Roguelike:** How does dataset size affect exploration? We will compare 900 vs 3700 samples for diminishing returns on accuracy.
3. **Lore:** Can we turn the classifier's errors into narrative material? A track predicted Zone 3 but truly Zone 7 becomes a "warp artifact" story.
4. **Audio Alchemy:** Which Essentia features actually carry numogram signal? SHAP will tell. If none do, we accept the numogram as a generative fiction that nevertheless structures our practice.

---

## Ethics & Openness

- Music is not a dataset. We study audio *as music* — with listening, not just analysis.
- The numogram overlay is a lens, not a law. We publish both correlations and null results.
- All synthetic data is CC0. Real‑audio metadata is citation‑only; no copyrighted audio distributed.
- All code pushed to `breakologist/hermes-agent` fork; community PRs welcome.

---

*Page updated 2026‑04‑30 to reflect four‑current framework and tightened Phase 4+ roadmap.*
