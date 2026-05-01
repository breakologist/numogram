# TouchDesigner Zone Visualizer — Network Design

## Goal

Build a real-time audio-reactive visualisation that reflects the **predicted zone** (1–9) and **spectral profile** of incoming audio, driven by the numogram zone classifier via MCP.

## Architecture

```
[Audio In] → [Audio Spectrum CHOP] → [Math CHOP (gain)] → [CHOP to TOP] → [GLSL TOP]
                                                                     ↓
                                                              [Feedback TOP] ←
                                                                     ↓
                                                               [Output TOP]
```

## Top-Level OP Layout

| OP Path | Type | Purpose |
|---------|------|---------|
| `/project1/audio_in` | `audiofileinCHOP` | Load an audio file or use microphone input |
| `/project1/spectrum` | `audiospectrumCHOP` | FFT → 256 bins, TimeSlice=ON |
| `/project1/gain` | `mathCHOP` | Multiply spectrum by 10 (boost) |
| `/project1/spectrum_top` | `choptoTOP` | Convert CHOP → 1-channel texture (256×1) |
| `/project1/time_constant` | `constantTOP` (rgba32float) | Single-pixel texture carrying `absTime.seconds` |
| `/project1/shader` | `glslTOP` | Main visual: zone-coded colour + spectrum overlay |
| `/project1/feedback` | `feedbackTOP` | Trailing effect (optional) |
| `/project1/out` | `nullTOP` | Output node |
| `/project1/zone_controller` | `tableDAT` or `nullCHOP` | Holds zone number + probs (MCP writes here) |

## GLSL Shader Logic (inside `shader`)

Uniforms (from inputs):
- `uTime` (from `time_constant`): current time in seconds
- `uSpectrum` (from `spectrum_top`): 256×1 texture, red channel = power per bin
- `uZone` (from `zone_controller`): integer 1–9 (as float)
- `uProbs[9]` (from `zone_controller`): probability array

Zone colour palette (hyperstitional):
```glsl
vec3 zone_colors[9] = vec3[](
    vec3(0.2, 0.6, 0.3),   // Z1 — mid green (Sink)
    vec3(0.9, 0.7, 0.2),   // Z2 — gold (Hold)
    vec3(0.8, 0.2, 0.5),   // Z3 — magenta (Warp)
    vec3(0.1, 0.4, 0.7),   // Z4 — deep blue (Sink)
    vec3(0.6, 0.3, 0.6),   // Z5 — purple (Hold)
    vec3(0.9, 0.4, 0.1),   // Z6 — orange (Warp)
    vec3(0.95, 0.1, 0.1),  // Z7 — red (Rise)
    vec3(0.2, 0.8, 0.9),   // Z8 — cyan (Rise)
    vec3(0.1, 0.1, 0.1)    // Z9 — black (Plex, with entropic noise)
);
vec3 base_col = zone_colors[int(uZone)-1];
```

Visual composition:
1. **Background**: dark (0.05) with subtle noise/grain
2. **Spectrum overlay**: vertical bars across screen height, coloured by zone tint, amplitude from `uSpectrum`
3. **Zone indicator**: central glyph (could be a 3-bar gate pattern or a decimal digit)
4. **Probability strip**: horizontal bar chart of uProbs along bottom

### Vertex shader (default pass-through)

```glsl
// glslTOP default vertex shader
```

### Pixel shader (outline)

```glsl
uniform float uTime;
uniform sampler2D sTD2DInputs[2];  // 0 = time constant, 1 = spectrum
uniform float uZone;
uniform float uProbs[9];

void main() {
    vec2 uv = gl_FragCoord.xy / uResolution;
    float t = texture(sTD2DInputs[0], vec2(0.5)).r;
    float spec = texture(sTD2DInputs[1], vec2(uv.x, 0.25)).r;

    // Zone colour
    vec3 zone_col = ... from palette ...
    vec3 col = vec3(0.05);

    // Spectrum bars
    float bar = step(uv.y, spec * 0.8);
    col = mix(col, zone_col * 0.7, bar);

    // Zone glow pulse
    float pulse = 0.5 + 0.5 * sin(t * (2.0 + uZone));
    col += zone_col * pulse * 0.1;

    gl_FragColor = vec4(col, 1.0);
}
```

## MCP Parameter Mapping

Hermes → TD via `td_set_operator_pars`:

| Target OP | Parameter | Value source |
|-----------|-----------|--------------|
| `/project1/zone_controller` (tableDAT) | cell `zone`  | predicted zone integer |
| `/project1/zone_controller` | cells `prob_1` … `prob_9` | probability floats |
| `/project1/shader` | custom parameter `uZone` (float) | zone float |
| `/project1/shader` | custom parameter `uProbs[0]` … `uProbs[8]` | probability floats |

> **Implementation note**: The twozero MCP plugin auto-exposes custom parameters on GLSL TOP as `value0`, `value1`, …; we'll map `uZone` → `value0`, `uProbs[0]` → `value1`, etc., or directly set DAT cells and read them in GLSL via `op('zone_controller')[0,0]`.

Alternatively, use a `executeDAT` that listens for MCP updates and writes directly to the shader's `par.value0` etc.

## Step-by-Step Build (inside TouchDesigner)

1. **Create base network**: drag `twozero.tox` → it adds MCP ROP
2. **Audio chain**:
   - `audiofileinCHOP` → `audiospectrumCHOP` (FFT=512, Output Length=256, TimeSlice=ON)
   - `Math CHOP: gain = 10`
   - `CHOP to TOP`: Data Format = `r`, Layout = `rowscropped`
3. **Time constant**:
   - `constantTOP` (1×1, rgba32float). Set `value0 = absTime.seconds` via `expr = absTime.seconds`.
4. **GLSL TOP**:
   - Inputs: 0 = time constant, 1 = spectrum TOP
   - Paste vertex + pixel shader code (store in a textDAT for easy editing)
   - Add custom parameters: `value0` (zone, float), `value1`–`value9` (probs)
5. **Feedback** (optional): `feedbackTOP` → `blurTOP` → composite over shader
6. **Output**: `nullTOP` named `out`
7. **Controller DAT**: `tableDAT` named `zone_controller` with 10 rows (zone, prob_1…prob_9)
8. **MCP wiring**: Hermes script will call `td_set_operator_pars(path='/project1/zone_controller', parameters={'value0': zone, ...})`

## Hermes-Side Implementation

The `phase4_7_touchdesigner_integration.py` script will:
- Load the classifier (Phase 4.3 or 4.6 mixed)
- Capture audio (microphone or file) in short windows (2–4 s)
- Extract features with `MIRFeatureExtractor` (using BPM fallback)
- Predict zone + probabilities
- Call MCP tools: `td_set_operator_pars` to update shader uniforms

**Prerequisites**: TD running, twozero MCP listening on port 40404, `touchdesigner-mcp` skill loaded.

## Future Enhancements

- **SHAP visualisation**: overlay SHAP value bars per feature as a HUD element
- **Syzygy chains**: animate triangular syzygy connections between zones when probabilities shift smoothly
- **Numogram walk**: trace a glyph path through zones as the piece progresses
- **Audio generation**: feed zone back into `mod_writer` to generate a response module, render and loop

---

*Design doc by Hermes Agent — Audio current + TD integration, 2026-05-01*
