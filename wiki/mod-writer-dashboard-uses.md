# mod-writer × Dashboard — Practical Uses

> How the existing `example-dashboard` plugin system could enhance the mod-writer project

---

## Current State

- **Plugin system**: Hermes Agent supports dashboard plugins mounted at `/api/plugins/<name>/` with frontend bundles in `plugins/<name>/dashboard/dist/`.
- **Example plugin**: `example-dashboard` provides a minimal manifest, API route (`/hello`), and a React-ish frontend bundle.
- **Configuration**: `config.yaml` has `dashboard.theme: default`; no mod-writer-specific tab yet.
- **Mod-writer assets**: Phase 4 pipeline (dataset generator, trainer, MIR profiler) all run as CLI/Skill scripts; no live UI.

---

## Three Practical Dashboard Applications

### 1. Live Zone Predictor (microphone → Essentia → zone panel)

**What**: Real-time microphone feed → Essentia `MusicExtractor` (low-latency mode) → 29-feature vector → trained zone classifier → zone probabilities displayed as a gauge/hud.

**Use case**:  
- Performance / VJ rig: musicians play into mic, zone prediction drives visuals (TouchDesigner) or mod parameters.  
- Debugging: verify that real audio maps to expected zones; discover gaps in the classifier.

**Dashboard UI spec**:
- Zone 0–9 probability bars (horizontal bar chart)
- Current dominant zone highlighted with zone colour & glyph
- Audio waveform / spectrogram mini-view
- Start/Stop microphone button (uses browser `getUserMedia`)
- Confidence threshold slider (ignore predictions below X%)

**Implementation path**:
1. Create a new skill `mod-writer-dashboard` (fork of `example-dashboard`).
2. Backend: FastAPI route `/predict` that receives audio buffer (base64 or raw WAV) and returns zone probabilities via the `trainer.py` model (`zone_clf.joblib`).
3. Frontend: WebRTC audio capture → chunks → POST → live-update HUD.
4. Optionally cache the latest Essentia feature vector for inspection.

**Why dashboard not CLI**: Real-time feedback needs low-latency WebSocket (MCP can also do this, but dashboard is browser-native and can use Web Audio). Dashboard also allows VJ-friendly large-UI elements.

---

### 2. Dataset Generator Progress & Quality Monitor

**What**: Dashboard view of ongoing Phase 4 dataset generation — samples produced per zone, feature-distribution histograms, ETA.

**Use case**:
- While the 3700-sample balanced set is generating (takes hours), watch progress from a browser tab instead of `tail -f log`.
- Spot imbalance early (e.g., Zone 3 only 80 samples while others at 100) and adjust seeds.
- See feature distribution drift between phases (Phase 4.1 baseline 29-dim vs Phase 4.2 full-pool 80–120-dim).

**Dashboard UI spec**:
- Progress bar: `X / N` samples, per-zone breakdown (small bar chart)
- Latest N MIR feature values as a sparkline / histogram (e.g., `spectral_centroid_mean` across all samples)
- Current phase indicator (4.1 / 4.2 / 4.3-train etc.)
- Log tail (last 50 lines) in a scrollable pane

**Implementation path**:
1. Extend `data_collector.py` to emit periodic JSON progress blobs to a shared location (`~/.hermes/mod-writer/progress.json`).
2. Backend route `/progress` reads that file and returns it.
3. Frontend polls every 2s and updates bar charts (use lightweight chart library or CSS bars).

**Benefit**: No need to switch to terminal; keeps the hyperstitional workflow in one visual plane.

---

### 3. MIR Feature Inspector + Zone Probability Explorer

**What**: Upload an arbitrary audio file → Essentia extracts full feature vector → live zone probabilities computed → user can tweak individual features and see how zone shifts.

**Use case**:
- **Correlation research** (Phase 4.4): see which features most affect zone classification.
- **Compositional guidance**: composers can test a WIP mod and see how its MIR profile aligns with zone aesthetics.
- **Debugging the classifier**: find blind spots where feature X alone sends everything to Zone 5.

**Dashboard UI spec**:
- File drop zone (accepts WAV/MP3/OGG)
- After analysis: display feature grid (sliders reflecting each extracted feature's value relative to training distribution)
- Live zone probability bar chart that updates as sliders move
- "Reset to actual" button to restore audio-derived values
- "Export feature vector" as JSON

**Implementation path**:
1. Backend: `/analyze` endpoint runs `MusicExtractor` on uploaded file, returns feature dict + zone probabilities.
2. Frontend: builds sliders dynamically from feature names (grouped by category: timbral, rhythm, tonal).
3. Slider changes POST updated feature vector to `/predict-features` to get new probabilities (no re-extraction needed).

**Why not a CLI tool**: Interactive exploration requires rapid slider movement; doing this in a shell is painful. Dashboard is natural for what-if analysis.

---

## How to Build the mod-writer Dashboard Plugin

Follow the `example-dashboard` pattern:

```
~/.hermes/skills/creative/mod-writer-dashboard/
├── SKILL.md              # skill definition
├── dashboard/
│   ├── manifest.json     # name: "mod-writer", tab: "ModWriter", slots: ["main:bottom"] or ["sessions:top"]
│   ├── plugin_api.py     # FastAPI routes: /hello, /progress, /predict, /analyze
│   └── dist/index.js     # React/Vanilla JS frontend bundle (compiled from src/)
└── README.md
```

**Hooks to implement**:
- `/api/plugins/mod-writer/hello` — ping
- `/api/plugins/mod-writer/progress` — read `mod_writer/classifier/artifacts/generation_progress.json`
- `/api/plugins/mod-writer/predict` — accepts feature vector JSON, returns zone probs via `trainer.py` inference function
- `/api/plugins/mod-writer/analyze` — accepts audio file, runs Essentia extractor (use existing `mir_profiler.py`), returns features + predict

**Frontend state**: Keep bundle small; use vanilla JS + Chart.js (already in Hermes frontend deps) for bar charts.

---

## Auxiliary Models Note

Currently `config.yaml` has an `auxiliary` block but no models wired. Dashboard uses could later include:

- **LLM lyric→zone tagger**: Send lyric text to local LLM with zone definitions, get zone profile overlay.
- **Diffusion zone-art generator**: Stable Diffusion with ControlNet conditioned on zone palette; output directly in dashboard.
- **Whisper transcription**: live transcript → AQ → zone prediction during voice note recording.

These would be separate MCP servers or REST microservices, not core mod-writer.

---

## Next Steps

- [ ] Fork `example-dashboard` → `mod-writer-dashboard` inside `~/.hermes/skills/creative/`
- [ ] Implement `/progress` route (poll `phase4.2.pid` and artifact growth)
- [ ] Build a simple "Phase 4 monitor" page in vanilla JS (bar chart + log tail)
- [ ] Register tab in manifest (`"tab": {"path":"/mod-writer","position":"after:sessions"}`)
- [ ] Add to `AGENTS.md` skills table once functional

Until then, the three use-cases above provide a clear design target for when dashboard work begins in Phase 4.6+.
