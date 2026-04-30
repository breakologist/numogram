# Mod-Writer Classifier — MIR to AQ Prediction

**Status:** Phase 4 in progress (v0.7.0). Experimental.

The classifier module learns a mapping from MIR audio features to AQ seed values
and — crucially — to *zone* (1–9). This is the "ears that hear the numogram":
feed it an audio file, get back predicted AQ/zone candidates.

## Architecture (Phase 4)

```
audio (WAV) → MIRFeatureExtractor → base 29-dim + optional Essentia pool (60–100+)
                                          ↓
                               StandardScaler (fit on train)
                                          ↓
               ┌──────────────────────────┴──────────────────────────┐
               │                       │                            │
         MLPRegressor           9‑class MLPClassifier        RandomForest
   (AQ regression, deprecated)   (zone prediction)         (baseline)
```

## Dataset

### Phase 3.1 — Baseline (100 samples, zone 1 only)
- 100 synthetic examples: AQ seeds 0–99, all generated in zone 1
- `SongBuilder(zone=1, aq_seed=seed)` → MOD → rendered WAV
- 29‑dim base features: band energy (6), timbre centroid/bandwidth/rolloff/dyn‑comp (4), rhythm (onset rate, BPM, confidence) (3), key one‑hot (12), scale one‑hot (3), duration (1)
- Cache: `artifacts/dataset.npz`

### Phase 4.1 — Balanced Multi‑Zone (900 samples, zones 1–9) — CURRENT
- **100 distinct AQ seeds per zone** → 900 total examples
- Seeds selected per zone via `_aq_candidates_for_zone()` to ensure each zone gets
  a diverse, non‑overlapping AQ set
- Each example labelled with both `aq` (0–99) **and** `zone` (1–9)
- Cache: `artifacts/dataset_balanced_900.npz`
- Zone‑balanced data is the single highest‑accuracy lever: expected zone accuracy
  jump from ~10% (chance) to **40–60%** on synthetic test

**Label ambiguity note:** Multiple AQ seeds map to identical gate transformations
(delta = SHA1(seed) % 37). Up to 37 distinct audio patterns exist for 100 seeds.

## Feature Set

### Base profile (always available)
29 dimensions: 6-band energy, 4 timbre descriptors, 3 rhythm, 12 key one‑hot,
3 scale one‑hot, duration.

### Essentia full‑pool (`use_all=True`) — Phase 4.2 in progress
When `essentia` is installed and `use_all=True` is passed to
`MIRFeatureExtractor.extract()`, an Essentia `MusicExtractor` is run with
`lowlevelStats=['mean','stdev']`, `rhythmStats=['mean']`, ` tonalStats=['mean']`.
Every scalar descriptor from the result pool is flattened and appended to the
feature vector. Expected dimension: **60–100+** depending on which pool fields
are scalar (vectors are skipped for now).

Advantage: a single flag unlocks 2000+ Essentia descriptors without hand‑crafting
each one.

## Training

### Phase 3.2 — Baseline regression (deprecated)
```bash
python run_phase3.py
```
- Split: 80/20 stratified by **derived** zone (digital root of AQ)
- Model: `sklearn.neural_network.MLPRegressor(hidden=(128,64))` (ReLU, 1000 epochs)
- Metrics (held‑out, zone‑1 only data):
  - MAE: ~25.6 AQ units
  - Acc@5: 10% (true AQ within ±5)
  - **ZoneAcc:** 10% (chance)

### Phase 4.3 — Zone classification (planned)
- New model: `MLPClassifier` (9‑class softmax)
- Training on balanced 900‑sample dataset
- Expected zone accuracy: **≥50%** on synthetic, **≥30%** on real‑audio set

### Phase 4.5 — Hyperparameter tuning
- Try `(256,128)` layers, dropout 0.2–0.5, early stopping
- Compare against `RandomForestClassifier`
- Curate 40‑track held‑out set balanced across zones if possible

## Usage

```bash
# Install classifier deps
pip install -e .[classifier]

# Phase 3: full pipeline on legacy single‑zone data
python run_phase3.py

# Phase 4.1: generate balanced multi‑zone dataset
python run_phase4_dataset.py
# Output: artifacts/dataset_balanced_900.npz

# Phase 4.3: train zone classifier (once implemented)
python -m mod_writer.classifier.trainer --data dataset_balanced_900.npz --zone-classifier
```

**Python API:**
```python
from mod_writer.classifier import predict, load_artifacts
scaler, model = load_artifacts()          # loads latest artifacts (auto‑detect)
result = predict(feature_vector)          # {'aq': 42.3, 'zone': 6, 'candidates': [...]}
```

## Real‑Audio Validation (Phase 3.3 — complete)

10‑track curated corpus (Kimberly Steele, Gregorian Chant, Nurse With Wound,
Current 93, death’s dynamic shroud):

| Track                                   | Pred AQ | Zone | BPM | Key |
|----------------------------------------|---------|------|-----|-----|
| Kimberly Steele – Orphic Hymn to Saturn | 50.9    | 6    | 0.0 |  ?  |
| Gregorian Chant Rosary                 | 57.8    | 4    |  ?  |  ?  |
| death's dynamic shroud – シェンムーONLINE #3 | 50.9  | 6    | 2.5 |  ?  |
| Current 93 – 01‑Lucifer Over London    | 50.8    | 6    | 0.5 |  ?  |
| Nurse With Wound – 03. Untitled        | 50.6    | 6    | -0.2|  ?  |
| Nurse With Wound – 02. Trippin' With The Birds | 50.6 | 6 | 1.1 | ? |
| Nurse With Wound – 01. Cold            | 50.8    | 6    | 0.3 |  ?  |

- **Zone distribution:** 9× Zone 6, 1× Zone 4
- **AQ range:** 50.6–57.8 (near training mean)
- CSV: `mod_writer/classifier/artifacts/real_audio_predictions.csv`

**Interpretation:** Classifier conservative; synthetic‑only training (zone‑1 only) insufficient.
Pipeline functional; dataset diversification (Phase 4.1) should resolve.

## Files

- `run_phase3.py` — Phase 3 orchestrator (legacy)
- `run_phase4_dataset.py` — Phase 4.1 balanced multi‑zone dataset builder
- `mod_writer/classifier/data_collector.py` — synthetic dataset builder (all phases)
- `mod_writer/classifier/mir_profiler.py` — MIR extraction, `use_all=True` Essentia pool
- `mod_writer/classifier/artifacts/` — scaler, model, datasets

## Roadmap

| Milestone                                   | Status          |
|--------------------------------------------|-----------------|
| Phase 3.3 — Real audio validation          | ✅ complete      |
| Phase 4.1 — Balanced multi‑zone dataset     | 🟡 in progress   |
| Phase 4.2 — Essentia full‑pool integration  | 🟡 in progress   |
| Phase 4.3 — Zone‑classifier training        | planned         |
| Phase 4.4 — Vocal presence detection        | optional        |
| Phase 4.5 — Validation suite + tuning       | planned         |
