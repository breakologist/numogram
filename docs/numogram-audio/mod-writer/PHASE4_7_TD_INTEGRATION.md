# Phase 4.7 — TouchDesigner Integration

## Status: Design Complete, Implementation Pending TD Instance

This directory contains the design reference for driving TouchDesigner visuals from the zone classifier.

- **Design doc**: `td_zone_visualizer_reference.md` — full network topology, GLSL shader, MCP mapping
- **Prototype script**: `~/ .hermes/skills/numogram-audio/phase4_7_touchdesigner_integration.py` (not yet tested)

## Prerequisites

1. TouchDesigner (Non-Commercial OK) running with twozero MCP plugin
2. `touchdesigner-mcp` Hermes skill loaded and configured
3. MCP server reachable at `localhost:40404`

## Quick Start (once TD ready)

1. In TD: File → Import... → load the provided `zone_visualizer.tox` network (create manually per design doc if .tox not available)
2. Enable MCP: twozero icon → Settings → "auto start MCP" → Yes
3. From terminal: `python ~/.hermes/skills/numogram-audio/phase4_7_touchdesigner_integration.py`
4. Watch the output window react to zone predictions.

## What It Does

- Loads the Phase 4.6 mixed zone classifier (`phase4.6_rf_mixed.joblib`)
- Captures audio from default microphone (or override with file path)
- Extracts 29-dim MIR features (with BPM fallback)
- Predicts zone (1–9) and full probability vector
- Pushes `zone` + `probs[0..8]` to TD via `td_set_operator_pars`
- TD GLSL shader recolours the visual accordingly

## Next Steps

- Build the TD network as per the design doc (or request a `.tox` file generation)
- Test the prototype script with a running TD instance
- Add SHAP overlay: visualise feature contributions as onscreen HUD
- Connect zone back to `mod_writer` for closed-loop generation (zone → composition → audio → zone)

*Design by Hermes Agent — Audio current + TD integration draft, 2026-05-01*
