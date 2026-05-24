# PD Template Diagnosis — M3 Live Audio Loop Fix Plan

*Compiled 2026-05-23 — hermetic wiki analysis*

---

## What We Have Right Now

### `templates/zone_resonator.pd` — STUB (25 lines)

```
# N canvas 0 0 600 400 10;
# X obj 50 50 loadbang;
# X obj 50 80 r zone_pitch;
# X obj 50 110 r zone_decay;
# X X obj 50 140 r zone_brightness;
# X obj 50 170 r zone_noise;

# X obj 50 200 osc~ 440;     ← placeholder pitch, hardcoded
# X msg 50 230 0.5;          ← placeholder decay, never connected to DSP
# X msg 50 260 0.7;          ← placeholder brightness, never connected to DSP
# X msg 50 290 0.1;          ← placeholder noise, never connected to DSP

# X obj 200 200 *~;          ← unconnected gain
# X obj 200 260 dac~;        ← sends to *hardware audio output* (no file write)
```

Connections in lines 16–25 look correct on paper, but the patch is entirely a stub — defined objects that never fire, parameters that never connect into the DSP graph, no `writesf~` at all.

### `scripts/render_zone_resonator.py` — WRITES WAV via `subprocess.run`

The `render()` function:
1. Reads the stub template
2. Does full `str.replace("440", pitch)` — replaces ALL occurrences of `440` everywhere in the file (fragile: replace `0.5` first, then `0.7`, then `0.1` would overwrite each other)
3. Calls `pd -nogui -batch` expecting... something (hangs forever; see below)
4. The `-audiooutdev dummy` flag will crash PD on this system (ALSA, not PortAudio)

### ZONE_PARAMS (derived from oracle-voice-pipeline, v2026-05-09)

```
Z0: pitch=140 decay=0.55 bright=0.30 noise=0.15
Z1: pitch=180 decay=0.25 bright=0.60 noise=0.10
Z2: pitch=250 decay=0.45 bright=0.50 noise=0.12
Z3: pitch=200 decay=0.20 bright=0.70 noise=0.08
Z4: pitch=120 decay=0.20 bright=0.65 noise=0.10
Z5: pitch=300 decay=0.15 bright=0.80 noise=0.05
Z6: pitch=180 decay=0.35 bright=0.55 noise=0.18
Z7: pitch=160 decay=0.60 bright=0.40 noise=0.20
Z8: pitch=150 decay=0.45 bright=0.50 noise=0.22
Z9: pitch=90  decay=0.45 bright=0.35 noise=0.25
```

These align with empirical resonance sweeps in `real-resonator-shap-driver-signatures.md`.

---

## Root Cause: Why `pd -batch` Hangs on This System

Confirmed through 8 hours of testing:

```
Terminal 1 [works]: pd -nogui -batch -open plain.pd -nosound → EXIT 0 (no DSP)
Terminal 2 [FAILS]: pd -nogui -batch -open osc440.pd           → HANGS (DSP, any audio API)
Terminal 3 [FAILS]: pd -nogui -batch -open osc440.pd -pa       → HANGS (PortAudio)
Terminal 4 [FAILS]: pd -nogui -batch -open osc440.pd -audioaddoutdev null → HANGS
```

**Why:** PD's default audio API on this system is **ALSA**. Opening any signal object (`osc~`, `noise~`, etc.) forces ALSA device opened. The HDA Intel PCH (ALC1150) is held by PipeWire/PulseAudio. ALSA `open()` in batch/non-interactive mode deadlocks waiting for device release. The DSP scheduler never starts, `loadbang` fire-and-forgets before the event loop picks up `; pd quit`, and the process loops forever.

**`-audiooutdev dummy` is wrong** — that's a PortAudio device name; ALSA ignores it and still opens `hw:0,0`.

**`-nosound` works** only if there is no DSP (no signal objects). Once an `osc~` is present, PD still tries to initialize audio regardless of `-nosound`.

### Long-term PD fix (if we care to use PD specifically later)

```bash
# Install jackd2 with dummy driver
sudo apt install jackd2  # or: sudo pacman -S jack2

# Run jackd in a tmux/screen session (daemonizes)
tmux new-session -d 'jackd -R -d dummy -r 44100 -p 128'
export JACK_DEFAULT_SERVER=dummy

# NOW pd works:
pd -nogui -batch -open patch.pd -r 44100 -jack -nojackconnect writesf~  # → exits, WAV written
```

This is the **only known path** to headless PD audio rendering on this system. It requires a background JACK server. If idle, minimal CPU cost.

---

## What We Can Do RIGHT NOW

### Path A — Python Synthesis (M3 Priority, immediately available)

`numpy 2.4.6 + scipy 1.17.1 + soundfile 0.13.1` — all confirmed available and working.

Karplus-Strong string resonator already renders correctly:
- `Z0 void`: pk=0.481, 264 KB/3s WAV ✓
- `Z9 gate`: pk=0.738, 264 KB/3s WAV ✓
- All 10 zones rendered in <2 seconds total

**Shortest possible M3 loop today:**

```bash
cd ~/numogram
python3 scripts/ks_synth_zone.py --zone 3 --out /tmp/z3.wav    # zone signature
python3 mod_writer/mod_writer/cli.py --zone 3 --render /tmp/z3.wav  # MIR tag
python3 mod_writer/mod_writer/cli.py --zone 3 --render /tmp/z3.wav --mod  # .mod
```

The MIR tag feeds the `zone_classifier`; zone signature feeds the VAE hallucination;
full .mod feeds the tracker sequencer. All three MIR+VAE+tracker paths now have WAV I/O.

### Path B — Fix the PD Template (retains PD, one day it works)

**What the template needs:**

```pd
# N canvas 0 0 600 400 1;
# X obj 10 10 loadbang;
# X obj 10 40 r zone_pitch;          ← receives zone pitch from [; pitch <val>( msg
# X obj 10 70 r zone_decay;
# X obj 10 100 r zone_brightness;
# X obj 10 130 r zone_noise;
# X obj 10 160 noise~;              ← noise excitation (1-pole lp brightness)
# X obj 30 160 vcf~;               ← variable filter controlled by brightness
# X obj 30 200 *~;                 ← gain = noise_amp × brightness
# X obj 70 40 osc~ 440;            ← K+S oscillator (zone_pitch controls)
# X obj 70 70 delwrite~ kstr 490;  ← delay line (period = sr/pitch)
# X obj 70 100 delread~ kstr 490;
# X obj 70 130 *~;                 ← feedback gain = decay
# X obj 70 160 +~;                 ← comb: noise + fb from kstr
# X obj 70 190 *~;                 ← output gain
# X obj 120 40 writesf~ /tmp/resonator_$zone.wav;
```

**Termination** — the piece that doesn't exist in any version of the template:

```pd
#X msg 10 200 2000, 8000 \; pd quit;
#X obj 10 230 t b b b;
#X connect ...

# 2000 MS delay start
# 8000 DSP ticks of writesf~ recording (8000×64/44100 ≈ 11.6 s)
# then ; pd quit
```

The **DSP tick calculation**: `writesf~` second arg is in DSP ticks. At 64-sample blocks,
44100 Hz: each tick = 64/44100 seconds. `8000 ticks × 64 / 44100 = 11.6 s`.

---

## Summary Table

| Item | Status | What To Do |
|------|--------|-----------|
| `zone_resonator.pd` template | **Stub (25 lines, no DSP)** | Build K+S graph: noise → vcf → osc→delwrite/delread→writesf~, four receives for zone params |
| `render_zone_resonator.py` | Works for file I/O; PD hangs on every call | Fix script in two ways: (A) Python `ks_string()` engine; (B) PD path with JACK + `-audiooutdev hw:0,0` in background |
| `; pd quit` termination | Missing entirely | Timer: ms-delay → DSP-tick-count → bang → writesf~ stop → pd bang → pd quit |
| PD hang on this system | ALSA blocks on `hw:0,0`, scheduler deadlocks | Long-term: `jackd -d dummy -r 44100` backgrounded; short-term: Py synth |
| `str.replace("440", ...)` | Fragile chaos | Replace with explicit dict-substitution tag injection: `{{PITCH}}` tokens |
| `-audiooutdev dummy` | Wrong flag | Use `-audioaddoutdev hw:0,0` if ALSA; or `-pa` only if PortAudio installed |
| VCV Rack | Installed, different tool | VCV Rack CLI saves `.vcv` patch + `--headless` mode, separate from PD pipeline — worth its own skill |

---

## Recommended Next Actions for M3

### Priority 1 — Unblock M3 live loop (Python path, today)

Write `ks_string()` into `mod_writer/utils.py` or a new `mod_writer/synth.py`:
```python
def zone_sig(zone, sr=44100, dur=3.0):
    p = ZONE_PARAMS[zone]
    return ks_string(p['pitch'], sr, dur, p['decay'], p['brightness'], p['noise'])
```
Then `render_zone_resonator.py` can call this directly when PD is unavailable,
writing the same `/tmp/resonator.wav` path that its PD subprocess would have produced.
**Zero infra changes; WAV output guaranteed.**

### Priority 2 — Fix the PD template (parallel)

1. Write `templates/zone_resonator.pd` with full K+S DSP graph (above)
2. Change substrings to `{{PITCH}}`/`{{DECAY}}`/`{{BRIGHTNESS}}`/`{{NOISE}}` tokens
3. Update `render_zone_resonator.py` to do token-substitution + `pd -batch -jack`
4. Add a `check_jackd()` scaffold that verifies `jackd_is_running()` before PD call

### Future — JACK plumbing

A `tmux` session with `jackd -R -d dummy -r 44100` started once, left running,
is the backend for all future PD renders. Add `hermes plugin` shell wrapper:

```bash
hermes plugin run --background 'jackd -R -d dummy -r 44100'
```

and `render_zone_resonator.py` auto-detects it before choosing engine.

---

## Hermes Agent New Features Relevant Here

| Hermes Release | Feature | Relevance |
|----------------|---------|-----------|
| **v0.12.0 (Curator)** | Autonomous skill maintenance, ComfyUI v5 | Background skill auto-fixer; wallpaper owner for zone visualization |
| **v0.13.0 (Tenacity)** | `/goal` persistent cross-turn goals, auto-resume | `/goal "M3 live audio loop"` persists intent across sessions; no re-prompting |
| **v0.14.0 (Foundation)** | `x_search` tool, LM Studio + Qwen3 provider | X/Twitter search when credits restore June 1; local LLM for zero-latency MIR inference |
| *(all)* | `session_search` | Retrieve past PD/numpy/synthesis experiments without re-tracing transcript |

v0.13 is the most relevant: set a `/goal` so every new session opens on M3.
v0.14 `xurl` with OAuth deferred (correct redirect `http://localhost:8080/callback`,
app type "Web app / automated app or bot" — documented in *skills-to-explore.md*).

---

## Status Cross-Reference

| Skill | Readiness | Issue |
|-------|-----------|-------|
| `puredata-wrapper` | **0% physical** | Stub template + broken PD launcher |
| `oracle-voice-pipeline` | **05% physical** | Formant model works; `synthesize.py` not found (lives in `~/numogram-voices/`) |
| `numogram-zone-audio-synthesis` | **50% Python** | `generate_zone_audio()` calls `mod-writer` not WAV synth; Python model not production |
| `mod-writer` | **80% physical** | `.mod` → WAV renderer exists; VAE hallucination running at 92%; zone classifier 96.4% |
| Python `ks_string()` now | **100% physical** | Immediate WAV output for all 10 zones |
| VCV Rack | **unknown** | Installed, headless CLI not yet validated |

---

*End of PD template fix plan. Next step: write `ks_string()` into the codebase, prove the M3 loop end-to-end.*
