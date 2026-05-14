---
title: "RuView — WiFi CSI → Audio Transducer"
tags: [wifi, csi, sensing, audio, MIR, transducer, edge, ESP32, RuView, research-stub, hardware-inventory]
date: 2026-05-14
status: active
---

# RuView — WiFi CSI as Audio Transducer

> **[ruvnet/RuView](https://github.com/ruvnet/RuView)** · 54.3k stars · WiFi Spatial Intelligence Platform
> *Turns commodity WiFi signals into real-time spatial intelligence, vital sign monitoring, and presence detection — all without cameras.*

## Overview

RuView captures **Channel State Information (CSI)** from ESP32-S3 nodes running in promiscuous WiFi mode. Each node streams per-subcarrier I/Q data (56 subcarriers per channel × 3 channels = 168 virtual subcarriers) over UDP. The signal pipeline produces real-time pose estimation (17 COCO keypoints), breathing detection (6–30 BPM), heart rate (40–120 BPM), through-wall presence sensing, and room fingerprinting.

## Why This Matters for the Numogram Currents

WiFi sensing is **the numogram as physical infrastructure**:

- **Invisible forces** (2.4 GHz radio waves) → **mathematical transform** (FFT/I/Q decomposition) → **spatial intelligence** (room model, body pose, vital signs)
- The 56-subcarrier grid is already a time-frequency surface — structurally identical to the spectrograms our MIR pipeline consumes
- Multipath scattering through a room is procedural generation by physics: the environment maps itself
- The project publishes honest failure metrics (PCK@20 ≈ 2.5% for camera-free pose) — empirical rigor embedded in speculative sensing

## Hardware Architecture

| Component | Role | Cost | Notes |
|-----------|------|------|-------|
| ESP32-S3 | CSI capture node (promiscuous WiFi) | $8-15 | Dual-core Xtensa LX7, 240 MHz, 8 MB flash + PSRAM |
| ESP32 mesh (3-6 nodes) | Multistatic sensing coverage | ~$54 | Each node streams raw I/Q over UDP |
| Cognitum Seed | Persistent vector store + kNN + WASM edge | ~$140 | Recommended full system |
| Intel 5300 / Atheros AR9580 | Research-grade CSI (3×3 MIMO) | $50-100 | Higher fidelity, discontinued, PCIe required |
| Any WiFi laptop | RSSI-only (no CSI) | $0 | Coarse presence/motion only |

### Known Limitations

- ESP32-C3 and original ESP32 **not supported** (single-core insufficient for CSI DSP)
- Heart rate detection unreliable on ESP32; requires research NIC for good results
- Single-node spatial resolution is minimal; 2+ nodes required for triangulation
- Camera-free pose accuracy: PCK@20 ≈ 2.5% (target 35%+ via camera-supervised training)

## Signal Pipeline

```
WiFi router (2.4 GHz) → radio waves pass through room
    ↓
Body/environment scatters multipath
    ↓
ESP32 mesh captures CSI on channels 1/6/11 (TDM protocol)
    ↓
Multi-Band Fusion: 3 channels × 56 subcarriers = 168 virtual subcarriers/link
    ↓
Feature extraction: Hampel filter, SpotFi, Fresnel zones, BVP, spectrogram
    ↓
RuVector (AI backbone): attention, graph algorithms, compression, field model
    ↓
Neural Network → 17 body keypoints + vital signs + room model
```

### Wire Protocol (ADR-018)

| Magic | Type | Rate | Size |
|-------|------|------|------|
| `0xC5110001` | CSI Frame | ~20 Hz | Variable (I/Q per subcarrier/antenna) |
| `0xC5110002` | Vitals Packet | 1 Hz | 32 bytes |
| `0xC5110004` | WASM Output | Event-driven | Variable |

CSI Frame header (20 bytes): `Magic(4) | NodeID(1) | Antennas(1) | Subcarriers(2) | FreqMHz(4) | SeqNum(4) | RSSI(1) | Noise(1) | Reserved(2)` + I/Q pairs

### Firmware Processing Tiers

| Tier | Status | Features |
|------|--------|----------|
| 0 | Stable | Raw CSI passthrough, ~20 Hz, ~5 KB/s |
| 1 | Stable | Phase unwrapping, Welford stats, Top-K subcarrier selection, Delta compression |
| 2 | Stable | Biquad IIR vitals filters, adaptive presence calibration, fall detection, multi-person clustering |
| 3 | Alpha | WASM programmable sensing (hot-swappable Rust modules) |

## CSI → Audio Transducer: The Concept

**Core idea:** Treat the 56 (or 168) subcarrier amplitudes as frequency bins in an audio frame. Map CSI amplitude → gain, phase → filter modulation, Doppler → pitch shift. The room becomes an instrument, sensed entirely through radio waves.

### Signal Mapping

| CSI Source | Audio Destination | Rationale |
|------------|-------------------|-----------|
| Subcarrier amplitude (56 bins) | Spectral envelope / gain per bin | Direct structural match: both are frequency-domain vectors |
| Phase variance | Filter resonance / FM index | Phase changes encode motion → timbre modulation |
| Doppler energy | Pitch shift / vibrato depth | Doppler directly measures velocity → frequency modulation |
| Breathing band (0.1-0.5 Hz) | LFO rate (6-30 BPM matches slow LFO range) | Breathing IS a slow oscillation; trivially maps to audio LFO |
| Heart rate (0.8-2.0 Hz) | Syncopation / rhythmic gating | Heart range maps to tremolo/beat modulation |
| Motion energy | Reverb wet / noise floor | More scatter = more "room" |
| Presence boolean | Voice on/off | Gate / mute trigger |
| Room fingerprint | Impulse response / reverb character | Stable multipath profile = room acoustics |

### Implementation Sketch

```
UDP port 5005 (ESP32 CSI stream)
    ↓
Parse ADR-018 binary frame → extract amplitude[56], phase[56]
    ↓
Apply per-subcarrier Hann smoothing → audio spectrogram frame
    ↓
IFFT → time-domain audio sample block
    ↓
Post-process: bandpass breathing/heart as LFOs, motion as reverb
    ↓
Output: MOD pattern (mod-writer) OR live WASM output
    ↓
Audio alchemy: zone mapping → AQ seeds → tracker composition
```

### Connection to mod-writer

The MIR pipeline already extracts spectral features from audio and maps them to seeds. CSI is simply **spectral features without the audio** — we can feed it directly into the seed pipeline, or use it as an alternative input modality for composition.

| Current Pipeline | CSI-Extended Pipeline |
|------------------|----------------------|
| WAV file → MIR features → zone seed → MOD | CSI stream → audio mapping → MIR features → zone seed → MOD |
| Audio source required | No audio source; room is the instrument |
| Post-hoc analysis | Real-time sensing → real-time composition |

## Edge Intelligence (WASM Modules)

65 implemented modules (609 tests passing), compiled to `wasm32-unknown-unknown`, runnable on ESP32-S3 via WASM3:

- Medical: Sleep apnea, cardiac arrhythmia, gait analysis, seizure detection
- Security: Perimeter breach, weapon detection, tailgating, loitering
- Smart building: HVAC presence, lighting zones, elevator counting
- Retail: Queue length, dwell heatmap, table turnover
- Industrial: Forklift proximity, confined space monitoring
- Each module: 5-30 KB, <10ms execution, OTA-updatable

## Alternative Hardware

Current microcontroller inventory:

| Device | Specs | CSI Capable? | RuView Role |
|--------|-------|--------------|-------------|
| **ESP32-S3** | Dual-core Xtensa LX7, 240 MHz | ✅ | Primary CSI node (ruvnet firmware) |
| **Raspberry Pi 4** | BCM2711, ARM Cortex-A72, 4×1.5 GHz | ✅ (via USB Intel 5300 NIC) | Research-grade CSI host, aggregator, ML inference |
| **Raspberry Pi Zero 2 W** | BCM2710A1, ARM Cortex-A53, 4×1 GHz | ❌ (no PCIe/CSI NIC) | Lightweight aggregator, data logger, MQTT bridge |
| **Teensy 4.1** | NXP i.MX RT1062, ARM Cortex-M7, 600 MHz | ❌ (WiFi + CSI not supported) | Audio DSP co-processor, mod-writer edge renderer, sensor bridge |

### Pi 4 Opportunity

The Pi 4 with a USB-connected Intel 5300 or Atheros AR9580 NIC can run research-grade CSI capture — higher fidelity than ESP32. The Pi 4 also has enough compute to run the full RuView aggregator + ML pipeline locally.

### Teensy 4.1 Role

The Teensy's strength is **real-time audio DSP** at low latency (600 MHz Cortex-M7). It can't capture CSI, but it can:
- Receive CSI-derived audio mappings over serial/USB from the Pi 4
- Run a mod-writer-like pattern renderer natively
- Generate audio output via I2S DAC
- Act as the "voice" of the WiFi-sensed room

### Pi Zero 2 W Role

Two Zero 2s can act as:
- Aggregator endpoints for separate ESP32 mesh clusters
- MQTT brokers routing CSI data to the main Pi 4
- Edge loggers writing raw frames to SD for later analysis

## Empirical Validation Questions

1. **Does CSI amplitude correlate with audio spectral features in any room?** Compare CSI-derived spectra to simultaneously recorded audio (mic in same room).
2. **Can CSI detect rhythmic events?** Stomp/clap/breath exercises with known tempo → does CSI-derived signal recover BPM?
3. **What is the effective frequency resolution?** 56 subcarriers over 20 MHz → ~357 kHz bin spacing vs. audio's 10-100 Hz. Resolution question matters.
4. **Does the multipath "room fingerprint" change measurably when objects/people move?** Baseline-empty-room vs. occupied CSI → cosine similarity of amplitude vectors.

## Telemetry → Audio Transducer

A prototype transducer was built at `/numogram/mod-writer/csi_transducer/csi_transducer.py`.

Three output paths:
- **Path A (additive synthesis):** CSI subcarrier amplitudes → spectral envelope → oscillator bank → WAV. The room-as-instrument: multipath changes modulate timbre in real-time.
- **Path B (MIR features):** CSI amplitude spectrum → spectral centroid/rolloff/flatness/MFCC → mod-writer seed score → AQ → tracker composition.
- **Path C (vital bands):** Breathing (0.1-0.5 Hz) and heart rate (0.8-2.0 Hz) band power from CSI temporal FFT → LFO/modulation parameters.

### Empirical results (Synthetic CSI, 100 Hz, 200 frames, 3 antennas, 56 subcarriers)

| Feature | Value | Interpretation |
|---------|-------|----------------|
| Spectrogram shape | (65, 56) | 65 Doppler bins × 56 subcarriers (window=128) |
| Audio output | 441,000 samples @ 44,100 Hz | 10 seconds of synthesised audio |
| Breathing detected | 0.50 Hz (30 BPM) | Upper edge of breathing band — synthetic signal has high-frequency breathing component |
| Heartbeat detected | 1.00 Hz (60 BPM) | Clean recovery from synthetic signal's 60 BPM heart component |
| Breathing power | 0.0246 | Breathing band contributes ~2.5% of total spectral power |
| Heartbeat power | 0.8958 | Heartbeat dominates (expected: synthetic signal was heart-driven) |
| Motion energy | 0.0009 | Low variance in synthetic signal (clean sinusoids) |
| Presence score | 1.0 | Vital band energy high enough to flag presence |
| Spectral centroid | 21.25 → **Zone 4** | Centroid maps to subcarrier 21 (of 56), digital root = 4 |
| Spectral rolloff | 45.00 | 85% of energy below subcarrier 45 — energy concentrated in mid-frequency subcarriers |
| Spectral flatness | 0.8413 | High flatness = broad spectrum, not tonally focused (expected for multi-frequency synthetic) |
| MFCC[0:5] | [-57.0, 11.5, 18.3, 3.9, -8.5] | First MFCC (energy) negative (log of small values), subsequent show spectral shape |
| Transduction time | 1.526s (200 frames) | ~7.6 ms/frame — real-time capable at 100 Hz |

**Validation status:** Synthetic data pipeline works end-to-end. The transducer correctly recovers the known vital sign frequencies from the reference signal. The centroid→Zone mapping produces Zone 4, which is interesting (syzygy 4::5, current 1 — the Gate of the Labyrinth). Next step: test with real ESP32 CSI data and cross-validate against simultaneous audio recording.

## Hardware Inventory

Current microcontroller/radio inventory for CSI/audio pipeline:

| Device | Role in CSI→Audio Pipeline | Cost to Deploy |
|--------|---------------------------|----------------|
| **ESP32-S3** | Primary CSI node (need to acquire) | $8-15 |
| **Raspberry Pi 4** | Research-grade CSI (via USB Intel 5300 NIC); aggregator; full pipeline host; ML inference on CSI spectrograms | Already owned |
| **Raspberry Pi Zero 2 W** (×2) | Aggregator endpoints; MQTT brokers; edge loggers; separate mesh cluster monitors | Already owned |
| **Teensy 4.1** | Audio DSP co-processor: receives CSI-derived parameters over serial/USB, runs additive synthesis natively, outputs via I2S DAC | Already owned |

**Deployment topology:** Pi 4 with Intel 5300 NIC captures high-fidelity CSI → runs transducer pipeline → sends MIR features to mod-writer (composition) AND modulation parameters to Teensy 4.1 (real-time audio output). Zero 2W units monitor separate rooms/ESP32 clusters and aggregate data to Pi 4.

## Related

- [[numogram-audio-empirical-findings]] — existing audio/AQ empirical research
- [[numogram-time-circuit]] — time as sensing domain
- [RuVector](https://github.com/ruvnet/ruvector/) — AI backbone for RuView
- [Cognitum Seed](https://cognitum.one/) — embedded edge intelligence hardware
