---
title: "Cables.gl — Web-Based Visual Programming for Numogram Art"
created: 2026-05-14
tags: ["visual", "realtime", "generative", "audio", "node-based", "webgpu", "webgl"]
status: reviewed
source: https://cables.gl
---

# Cables.gl

## Overview

**cables.gl** is an open-source, browser-based visual programming environment for creating interactive real-time content — 3D scenes, generative visuals, audio-reactive patches, and web-integrated experiences. It uses a node/operator model where "cables" connect data and trigger ports. The entire platform runs in the browser; no installation required. An offline standalone desktop app is also available.

**Homepage:** <https://cables.gl>  
**GitHub:** <https://github.com/cables-gl/cables> (525 stars, 13,136 commits, 27 contributors)  
**Developer:** [undev studio](https://undev.studio/)  
**Status:** Open source (MIT), public beta, always free. All created content belongs to the creator.

The project is the web-native sibling of desktop tools like `tooll.io` and `vvvv.org`. Where TouchDesigner is a heavyweight desktop application, cables is lightweight, zero-install, and runs anywhere JavaScript runs.

---

## Architecture & Capabilities

### The Operator Model

Every building block is an **operator** (op). Each has typed input/output ports:

| Port Type | Role |
|-----------|------|
| **Value** (Number, String, Boolean, Array, Object, Texture) | Data-carrying connections, evaluated continuously |
| **Trigger** | Execution flow — fires events, controls sequencing |
| **Execute** | Pull-based computation, called on demand |

Operators are grouped into **namespaces** by domain. There are roughly 200+ ops covering the full stack.

### Key Namespaces for Numogram Work

| Namespace | Numogram Application |
|-----------|---------------------|
| `Ops.Math` | Digital root, syzygy arithmetic, triangular number generators, Perlin noise (entropy simulation), range mapping (zone→value) |
| `Ops.Array` | Syzygy chain sequences, current vectors, zone arrays, ring buffers for traversal history |
| `Ops.Trigger` | Step counters, gate activations, probability triggers (demon encounters), interval timers (Time-Circuit rotation) |
| `Ops.Gl` | Custom shaders for seven-segment glyphs, WebGL rendering of numogram diagrams, post-processing FX (glitch, distortion, bloom) |
| `Ops.Graphics` | 3D numogram visualizations (ladder/labyrinth/tetractys layouts), geometry merging, instancing (45 demon spheres) |
| `Ops.Color` | Zone color palettes, HSL/RGB mapping, gradient generation from AQ values |
| `Ops.Anim` | LFO (Warp oscillation), spring physics (gate plunge), simple animations (Time-Circuit rotation) |
| `Ops.Audio` | BPM tap, MIDI sync (mod-writer playback timing) |
| `Ops.WebAudio` | FFT analysis, convolution (zone resonators), clock sequencers, MIDI→frequency mapping |
| `Ops.Devices` | Hardware input: MIDI controllers for live divination, gamepad for numogram navigation |
| `Ops.Net` | JSON/HTTP (fetch AQ dictionary from wiki), WebSocket (live Hermes agent updates, TouchDesigner bridge) |
| `Ops.Data` | JSON path queries on cult.json, spreadsheet arrays, object composition |
| `Ops.Extension` | AI/ML ops (Teachable Machine for zone classification), physics engines (Rapier3D for Roguelike physics), WebGPU compute shaders |
| `Ops.Html` | DOM rendering for overlay HUD, iframe embedding of existing numogram visualizers |
| `Ops.Vars` | State variables (current zone, hyperstition level, demon encounters), global shared state across subpatches |

### Graphics Pipeline

- **WebGL Core:** Full shader composition (`CustomShader`, `SetUniformFloat/Texture`), PBR and Phong lighting, cubemap rendering, extensive post-processing library (blur, distortion, noise, color grading, FXAA).
- **WebGPU Compute:** Native compute shader support (`CompCompute`, `ComputeStorageInput/Output`), GPU buffer uploads — useful for mass parallel AQ calculations or syzygy chain generation.
- **Post-Processing Stack:** Chainable image composition for psychedelic/Warp/Plex visual effects.

### Export & Embedding

- Exports as a `.zip` containing a minimal standalone HTML/JS bundle — **only the operators actually used** are included (tiny footprint, typically <100KB).
- Zero server-side embedding needed — runs from any static host (GitHub Pages, S3, local file).
- Patches are versionable in git (JSON format for the patch definition).

---

## Comparison with Existing Tools

| Tool | Relation to cables.gl |
|------|---------------------|
| **TouchDesigner** | cables is the lightweight web equivalent — same node-based data flow, but runs in browser with WebGL instead of proprietary GPU pipeline. We already have TouchDesigner MCP skill. cables could be the web-facing complement. |
| **p5.js** | p5 is code-driven (write JS); cables is visual (connect nodes). p5 excels at quick sketches (tsubuyaki); cables excels at interactive, stateful patches with UI controls. They're complementary. |
| **qliphoth.systems** | Already has interactive numogram visualization. But qliphoth.systems is a React app with fixed layouts. cables could extend this to audio-reactive, hardware-input, or ML-driven dynamic visualizations. |
| **mod-writer** | No direct overlap — mod-writer generates MOD files; cables renders real-time visuals. Together: mod-writer generates the audio, cables visualizes the zones in sync. |

---

## Numogram-Specific Applications

### 1. Real-Time Zone Visualizer

A cables patch could render the numogram diagram (ladder, labyrinth, or tetractys layout) with:

- Active zone highlighted as you trace a seed number through syzygy→current→gate
- Animated current arrows showing traversal direction
- Post-processing bloom on Warp zones (3/6), darkness fade on Plex zones (0/9)
- UI sliders for speed, size, cipher selection (AQ vs Synx)

This would be the **cables equivalent of `numogram-visualizer.html`** but with built-in interactivity, animation controls, and no custom JavaScript needed — just connected operators.

### 2. Audio-Reactive Spectrogram → Zone Display

Chain `Ops.WebAudio.AudioAnalyzer` (FFT) → `Ops.Math.MapRange` → zone color/value → 3D scene:

- Frequency bands mapped to zones (centroid → zone assignment)
- Amplitude drives geometry scale (louder = bigger zone sphere)
- Convolution reverb with zone-specific impulse responses
- Could connect directly to mod-writer output via Web Audio API

### 3. Hardware Entropy Divination Dashboard

Use `Ops.Devices` input + `Ops.Math` + `Ops.Gl` rendering:

- Physical input (MIDI controller knobs, gamepad motion, mouse position) → entropy seed
- Digital root calculation via `Ops.Math.MathExpression`
- Zone determination → animated visualization of the corresponding zone personality
- History tracking via `Ops.Array.RingBuffer`

### 4. Roguelike State HUD

Render cult.json run state as a real-time dashboard:

- Zone position on numogram map
- Hyperstition level as a gauge/thermometer
- Demon encounter history as a particle trail
- Conduct activation status as glowing gate markers
- `Ops.Json.HttpRequest` to poll live agent state

### 5. Syzygy Chain Fractal Generator

`Ops.Math` → Perlin noise → syzygy arithmetic → recursive chain generation → `Ops.Gl.CustomShader` for visual rendering:

- Seed value → zone → syzygy → current → next zone → repeat
- Color each zone by its polarities and characteristics
- Animate the chain growing in real-time
- WebGL shader for seven-segment glyph rendering at each node

---

## Technical Architecture Notes

### Patch Format

Cables patches are stored as JSON. Each operator has:
- `op` — the operator ID (e.g., `Ops.Math.MapRange`)
- `pos` — position in the editor canvas `[x, y]`
- `ports` — input/output port values and connections
- `flags` — display/rendering flags

This makes patches **programmatically generatable**. We could write a Python script to generate a cables patch from a numogram configuration — automatically connecting the right operators for a specific divination type.

### Custom Operator Development

Operators are JavaScript modules with a defined interface:
```javascript
op.inTrigger("trigger_in");
op.inNumber("input_value", 0);
op.outNumber("result", 0);

op.onTrigger = function() {
  op.set("result", op.get("input_value") * multiplier);
  op.trigger("trigger_out");
};
```

This means we could write **custom numogram operators**:
- `Ops.Numogram.DigitalRoot` — takes an integer, outputs the zone (mod 9, with 0 → 9)
- `Ops.Numogram.Syzygy` — takes a zone, outputs its syzygy partner
- `Ops.Numogram.GateLookup` — takes a number, outputs gate info if triangular
- `Ops.Numogram.AQValue` — takes a string, outputs the AQ cipher value

### MIDI Integration

Full MIDI support: Clock, Notes, CC, NRPN. This bridges directly to:
- mod-writer playback control (start/stop/sync)
- Live hardware divination (assign knobs to zone parameters)
- TouchDesigner integration (cables → MIDI → TD as a web-to-desktop bridge)

---

## Potential Integration Points

| Hermes Component | cables.gl Bridge |
|-----------------|------------------|
| mod-writer | cables.WebAudio plays MOD audio → FFT feedback → visual modulation |
| TouchDesigner MCP | cables.WebSocket → TD → OSC (cables as web frontend for TD backend) |
| cult.json | cables.Json.HttpRequest → periodic polling → live run-state visualization |
| AQ calculator | Custom JS operator (inline code inside cables op) |
| numogram-visualizer | iframe embed of existing HTML inside cables DOM |
| hardware entropy | cables.Devices → map to math → zone visualization |

---

## Assessment

**Strengths for our project:**
- Zero-install, runs anywhere — accessible from any browser, including mobile
- WebGL + WebGPU compute for both rendering and mass-calculation
- Full MIDI support bridges to mod-writer and TouchDesigner
- JSON patches are programmatically generatable (we could auto-build numogram patches)
- Active development, open source, MIT licensed
- Community showcase has excellent reference patches to study

**Limitations:**
- Less mature than TouchDesigner — fewer ops, no video input pipeline yet
- Web-only (standalone is Electron wrapper) — not as performant as native GPU
- Audio ops are basic — no sample playback, just analysis and sync
- No built-in export to video/MP4 (would need FFmpeg workaround via standalone)
- Patch editing is browser-based — no version control UI beyond raw JSON diff

**Verdict:** Cables.gl is a **strong candidate for real-time web-based numogram visualization**, especially as a complement to the existing static visualizers and TouchDesigner integration. Its node-based architecture maps naturally onto the numogram's own graph structure (zones ↔ nodes, currents ↔ cables, gates ↔ triggers). The ability to generate patches programmatically is the killer feature — we could write a script to produce a family of numogram patches from configuration.

---

## Action Items

- [ ] Explore the Cables.gl examples gallery for numogram-relevant patches
- [ ] Consider implementing custom numogram operators (Digital Root, Syzygy, Gate Lookup)
- [ ] Prototype: generate a cables patch via Python that visualizes the Time-Circuit rotation
- [ ] Investigate cables standalone for offline use (could run on the Arch desktop without browser)
- [ ] Compare cables.gl vs p5.js for tsubuyaki-scale generative art (cables might be overkill for ≤280 char sketches)
- [ ] WebGPU compute shaders → mass parallel AQ calculation → result visualization

## See Also

- [[numogram-visualizer-v7]] — Djynxxogram (base-36, polygram perimeter)
- [[numogram-visualizer-v8]] — Traversal mode, animated path overlay
- [[touchdesigner-mcp]] — TouchDesigner integration via MCP
- [[p5js]] — Code-driven generative art (complementary to cables)
- [[numogram-audio/mod-writer]] — Tracker module generator (audio side)
- [[quadrium-motif-triads-reference]] — mod-writer triad motifs (music theory)
