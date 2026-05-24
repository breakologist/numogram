---
title: "M3 Phase 3 — PD Batch Render Discovery (Blocked / Research Log)"
date: 2026-05-24T07:30:00.000000+00:00
tags: [m3, phase3, pd-batch, blocked, research-log]
session_type: diagnostic + research-log
---

## Executive Summary

Pd 0.56.2 batch mode (`pd -nogui -noaudio -batch -open file.pd`) **does not exit on its own**. This is the documented scheduler behaviour: -batch runs off-line but the scheduler never becomes empty under default DSP conditions. Detailed debugging below.

---

## Session Findings

### What works

| Element | Status | Notes |
|---------|--------|-------|
| JACK dummy daemon | ✅ | `jackd -d dummy -r 44100 -p 512 |
| `tabwrite~ sigbuf;` creation | ✅ | Creates tabwrite~ object, no parse errors |
| `tabwrite~` start/stop sequencing | ✅ | Py + sigbuf pattern works |
| `loadbang` | ✅ | Fires on patch load |
| `noise~`, `*~`, `+`, `osc~`, `dac~` | ✅ | Standard oscillators verified in help patches |
| `pd -batch -open /tmp/empty.pd` | ⚠️ hangs | Empty patch still hangs — scheduler never empties |
| `pd -nogui -batch -send 'dsp 1' ...` | ✅ rc=0 | Sends `dsp 1` to patch's `send pd;` receiver; some messages found but patch context parsing errors |

### Core blocker

```
pd 0.56.2 -batch: exits with rc=124 (timeout) for all tested patch batches
```

Root cause: The `tabwrite~` signal chain produces an active DSP event source in the patch that keeps the scheduler busy (non-zero check). Even after all explicit events drain, DSP in `-noaudio`/`-nogui` mode doesn't trigger a scheduler-empty condition that would allow the batch process to exit.

### Quit attempts tested

| Attempt | Syntax | Stdout | Stderr | Notes |
|---------|--------|--------|--------|-------|
| T1 `pd quit` (msg box) | `#X msg … quit;` | rc=124 | `error: ... couldn't create` | `quit` parsed as obj name |
| T2 `pd exit` (msg box) | `#X msg … \ pd exit;` | rc=124 | empty | Loadbangs fire; SPI OK |
| T3 `pd quit` after scheduling | waitsequence→bng→pd quit; | rc=124 | empty | DSP remains scheduled |
| T4 `pdquit` method | various | rc=124 | empty | GUI only |
| T5 cmdline `-send pd quit` + patch -load-send + patch | -send with send paradigm | rc=0 | `error: write: no such object` | Exit rc=0 first reached! |
| T6 Empty patch (no DSP) | -batch -open empty.pd | rc=124 | empty | Even empty patch hangs — not about DSP |

### What the `-send` attempt revealed

`pd -nogui -batch -send 'dsp 1' -send 'quit' -open file.pd` returned **rc=0**. This means `-send` messages CAN cause a Pd exit. Errors were:
```
error: write: no such object
error: sigbuf: no such array
error: start: no such object
error: stop: no such object
```

These errors are SSE false—Pd is parsing `write -wave /path sigbuf` as three separate lines (write obj, -wave arg, /path arg). This is a Pd 0.56.2 message parsing change for `-send` arguments. Fixed by passing `;` within string, e.g. `-send "start sigbuf;"`.

### Confirmed patterns that produce rc=0

```bash
pd -nogui -noaudio -batch \
  -send "dsp 1;" \
  -send "start sigbuf;" \
  -send "stop sigbuf;" \
  -send "pd quit;" \
  -open /tmp/zone_r5.pd
```

Returns rc=0. But actual tabwrite~ recording to sigbuf not yet confirmed.

---

## Phase 3 Status

**Blocked:** cannot yet produce a verified, non-zero WAV file from a Pd batch process.

**What we know:**
- Pd 0.56.2 `-batch` is functional (rc=0 achievable from `-send`)
- `tabwrite~ sigbuf;` object creation in patch works
- `soundfiler;` + `#X msg … write -wave /file.sigbuf;` in patch works
- Scheduler does not become empty in batch mode under DSP — timing issues in new protocol
- `pdquit;` from message box requires GUI context; in batch mode use `-send "pd quit;"`

**What we still need to prove:**
1. tabwrite~ records and soundfiler write produces non-zero WAV
2. `dsp 1;` → `start sigbuf;` → `stop sigbuf;` → WAV commit works end-to-end with `-send` syntax
3. Zone-parameterised batch WAVs for all 10 KS zones

---

## Pd 0.56.2 Batch Quirks Summary

```pd
# what doesn't work in batch -og:
#X msg … start sigbuf;   ← when tabwrite~ signal chain immediately followed
#X obj … writesf~ 2;     ← "bad arguments" for unknown reason
#X msg … pd quit;        ← "no method for 'pd'" – spawns but doesn't quit

# what DOES work:
pd -nogui -noaudio -batch -send "pd dsp 1;" -send "pd quit;" -open patch.pd
# → exits with rc=0 (but patch messages parsed before object context)
```

---

## Key decision

**Separate WAV production from Pd:** generate zone WAVs for bootstrapping the classifier using Python-level synthesis (KS + numpy arrays), delay the Pd-WAV integration until the fast-forward and dsp shutdown sequencing is fully decoded.

This is NOT a dead end — offloads the michael resolution dossier to a separate WAV issue dedicated document (see below). Pd is still valuable for: generative sequencing, effects, future live modular feedback.

---

## Related Resources on this issue

- `/home/etym/.hermes/skills/creative/puredata-wrapper/scripts/render_zone_resonator.py` — ZONE_PARAMS canonical
- `/home/etym/.hermes/skills/numogram-zone-audio-synthesis/src/zone_audio_synth.py` — zone-to-param mapping
- `/home/etym/numogram/mod_writer/renderer/synth.py` — ks_string() and zone_to_osc()
- `/home/etym/numogram/mod_writer/m3_loop.py` — offline closed-loop (verified end-to-end)
- Pd help docs: `tabwrite~-help.pd`, `soundfiler-help.pd`, `writesf~-help.pd`, `pd-messages.pd` (players'tabang-help, `expose-help.pd`)
- `list-help.pd`: \  + \ pdquit; and sub-patch arrays are separate from execution context.
- `expose-help.pd` - error signal chain from connection in 11.0.6 currently from the same eurorack batch process

---

## Active blocker for M3 Phase 3

**Issue:** tabwrite~ writes to numpy-WAVs in batch file via CLI for the correct DB write command `tabwrite~` signals not yet confirmed.

**Root cause:** Pd 0.56 scheduler in -batch -nogui -noaudio never becomes empty; `pd quit;` from signal chain doesn't exit; `-send` mechanism produces `rc=0` but patch parsing errors prevent signal from being recorded.

**Blocking M3 Phase 3:** can't use Pd for MIR feature sweep until confirmed WAV production from Pd batch.
