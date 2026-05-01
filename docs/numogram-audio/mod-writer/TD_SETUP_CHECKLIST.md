# TouchDesigner MCP Integration — Setup Checklist

**Last updated:** 2026-05-01  
**Status:** Design complete; live test pending

## Prerequisites

1. TouchDesigner installed (2023.10000+ recommended)
2. twozero MCP plugin — install via `pip install twozero-td-mcp` or from
   <https://github.com/twozero/td-mcp>
3. MCP server running (the plugin exposes an MCP endpoint that Hermes talks to)
4. Hermes skill `touchdesigner-mcp` available and loaded

## Step-by-Step

### 1. Install the twozero MCP plugin in TouchDesigner
```bash
# Option A: pip (if plugin published)
pip install twozero-td-mcp

# Option B: manual
git clone https://github.com/twozero/td-mcp.git
# Follow repo instructions for building/installing the .tox plugin
```

In TouchDesigner:
- View → Palettes → Install... → select `twozero.tox`
- Confirm it appears in the Palette

### 2. Enable MCP server on port 40404

In the TD network:
- Drag `twozero MCP` operator (Palette → twozero)
- Set its **Port** parameter to `40404` (default)
- Set **Auto Start** = `On`
- Press `Start`; status should go green

### 3. Load the zone visualiser network

Build (or download) from `td_zone_visualizer_reference.md`:

```
/project1/
  audio_in       → Audio Spectrum TOP
  zone_controller → Script CHOP
  zone_color     → constant TOP (GLSL)
  zone_visual    → GLSL TOP (renders to output)
  Table DAT      → zone name + hex colours
```
See design doc for full OP parameter tables.

### 4. Verify MCP connectivity from Hermes
```bash
# Check MCP tools are visible
hermes tools | grep td_
# Expected: td_create_operator, td_set_operator_pars, td_execute_python, ...

# If tools missing:
- Ensure touchdesigner-mcp skill is in ~/.hermes/plugins/enabled/
- Restart gateway: hermes gateway restart
- Restart TUI: hermes --tui
```

### 5. Run the prototype script
```bash
cd ~/.hermes
python phase4_7_touchdesigner_integration.py
```

Expected output:
```
[+] Loaded mixed RF model (909 samples, 97.78%)
[+] Extracted features from test track: zone=2, probs=[...]
[+] Pushed to TD: zone=2, probabilities=...
```

The `zone_controller` Script CHOP should update its custom parameters:
  - `zone` (int 1–9)
  - `prob_1` … `prob_9` (float)

The GLSL visualiser should recolour accordingly.

### 6. Debugging Tips

| Symptom | Check |
|---------|-------|
| `td_set_operator_pars` fails | Is MCP server running? `curl http://localhost:40404/health` |
| Parameters not updating | OP name/path correct? Use `td_get_operator_info` to inspect |
| No colour change | GLSL shader compiled? Check TD latency; look at `zone_visual` TOP error |
| Script CHOP errors | Python script syntax; `print()` appear in TD textport |

### 7. Known Limitations

- MCP currently only sets *parameters*; for complex logic use `td_execute_python`
- Prototype uses a single test WAV; expand to live audio stream later
- Zone probabilities are floats; the shader expects 0–1 normalised

---

Once live test passes, commit the prototype & design doc to
`mod-writer/examples/phase4_touchdesigner/` (already done) and update
this runbook with any corrections.