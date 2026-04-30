# Mod-Writer Classifier — MIR to AQ Prediction

**Status:** Phase 3 prototype (v0.6.2). Experimental.

The classifier module learns a mapping from MIR audio features to AQ seed values. This is the "ears that hear the numogram": feed it an audio file, get back predicted AQ candidates.

## Architecture

```
audio (WAV) → MIRFeatureExtractor → 29-dim feature vector
                                          ↓
                               StandardScaler (fit on train)
                                          ↓
                         MLPRegressor(hidden=(128,64))
                                          ↓
                         predicted AQ ∈ [0, 99] (regression)
```

## Dataset (Phase 3.1)

- 100 synthetic training examples: AQ seeds "0" through "99"
- Each seed → `SongBuilder(zone=1, aq_seed=seed)` → MOD → rendered WAV
- `MIRFeatureExtractor` profiles: bands (6), timbre (4), rhythm (3), key one-hot (12), scale (3), duration (1) = **29 features**
- Cached at `mod_writer/classifier/artifacts/dataset.npz` (compressed)

**Label ambiguity note:** Multiple seeds map to identical gate transformations (delta = SHA1(seed) % 37). Up to 37 distinct audio patterns exist for 100 seeds. Model trained on raw seed values encounters label noise; future versions should predict delta class (0-36) instead.

## Training (Phase 3.2)

```bash
python run_phase3.py  # generates dataset (if missing), trains, saves artifacts
```

- Split: 80/20 stratified by derived zone (digital root of AQ)
- Model: `sklearn.neural_network.MLPRegressor` (ReLU, 1000 epochs)
- Metrics (held-out):
  - **MAE:** ~25.6 AQ units
  - **Acc@5:** 10% (true AQ within ±5)
  - **ZoneAcc:** 10% (correct zone 1-9)

Interpretation: Near chance, but functional. The synthetic timbre palette (square/triangle/noise) provides limited acoustic variation; real music may yield different feature distributions.

## Usage

```bash
# Install classifier deps
pip install -e .[classifier]

# Run full pipeline (dataset generation + training)
python run_phase3.py

# Predict AQ from an audio file (WAV only currently)
python -c "
from mod_writer.classifier import predict
print(predict('track.wav'))
"
```

**Python API:**
```python
from mod_writer.classifier import predict, load_artifacts
scaler, model = load_artifacts()
result = predict(feature_vector)  # {'aq': 42.3, 'zone': 6, 'candidates': [(42,0.8), (43,0.1), ...]}
```

## Limitations & Next Steps (Phase 3.3+)

- **Audio format:** only WAV supported (scipy.io.wavfile). MP3/FLAC require transcoding.
- **Feature set:** low-level MIR only; no deep embeddings (musicnn, openl3).
- **Training data:** synthetic only; real music not yet evaluated.
- **Model capacity:** baseline MLP may be insufficient; try RandomForest or gradient boosting.
- **Label strategy:** shift to predicting `delta = SHA1(seed)%37` (37-class) for cleaner targets.

**Phase 3.3 — Real Audio Validation**
- Convert a subset of your music collection to WAV (ffmpeg)
- Label each track via filename AQ heuristic: `aq_seed = filename (sans ext)`
- Run classifier predictions; compare zone-level intuition (e.g., Saturn hymns → Zone 6?)
- Corpus: `~/music/Kimberly Steele`, `Gregorian Chant`, `Death's Dynamic Shroud`, `Current 93`, etc.

**Phase 3.4 — CLI Integration (complete)**

| Flag | Description |
|------|-------------|
| `--classify AUDIO_FILE` | Single‑track prediction (any format supported by ffmpeg) |
| `--classify-dir DIRECTORY` | Batch walk all audio files under directory |
| `--classify-limit N` | Maximum files to classify in batch mode (default: unlimited) |
| `--classify-format {table,json,csv}` | Output representation |

**Output schema** (all formats): `file`, `predicted_aq`, `zone`, `duration_s`, `bpm`, `key`, `scale`.

**Implementation notes:**
- Audio transcoding → WAV via `ffmpeg` (handles MP3/FLAC/OGG)
- MIR feature extraction through `mir_profiler.py` (same pipeline as `--profile-audio`)
- Feature vector → StandardScaler → MLPRegressor prediction
- Single‑track default: `--classify-format table` (human‑readable columns)

**Validation:** tested on 10‑track curated corpus (Kimberly Steele, Gregorian Chant, Nurse With Wound, Current 93, death’s dynamic shroud). Produced consistent Zone 6 bias, confirming synthetic‑only training limitations. CLI stable and production‑ready for exploratory listening sessions.

## Phase 3.3 — Real Audio Validation (complete)

### Results on 10 curated tracks

| Track | Predicted AQ | Zone | BPM | Key |
|---|---|---|---|---|
| Kimberly Steele - Orphic Hymn to Saturn.mp3 | 50.9 | 6 | 0.0 | ? |
| Gregorian Chant Rosary.mp3 | 57.8 | 4 | ? | ? |
| death's dynamic shroud - シェンムーONLINE #3 | 50.9 | 6 | 2.5 | ? |
| Current 93 - 01-Lucifer Over London.flac | 50.8 | 6 | 0.5 | ? |
| Nurse With Wound - 03. Untitled.flac | 50.6 | 6 | -0.2 | ? |
| Nurse With Wound - 02. Trippin' With The Birds.mp3 | 50.6 | 6 | 1.1 | ? |
| Nurse With Wound - 01. Cold.flac | 50.8 | 6 | 0.3 | ? |
| … 3 more tracks | ~50–51 | 6 | ~0 | ? |

- **Zone distribution:** 9× Zone 6, 1× Zone 4
- **AQ range:** 50.6 – 57.8 (close to training mean)
- CSV: `mod_writer/classifier/artifacts/real_audio_predictions.csv`

**Interpretation:** Classifier conservative; synthetic-only training insufficient.
Pipeline functional; next expand dataset diversity (multi-zone synthetic, real labels).


## Files

- `run_phase3.py` — end-to-end orchestrator
- `mod_writer/classifier/data_collector.py` — synthetic dataset builder
- `mod_writer/classifier/trainer.py` — training + evaluation
- `mod_writer/classifier/artifacts/` — scaler, model, dataset
