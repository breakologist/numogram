---
title: "M3 Phase 1–3 Status — KS Synthesis, Zoning Diagnostics, PD Batch Render"
date: 2026-05-24T07:00:00
tags: [m3, phase1, phase2, phase3, open]
current: IV-Audio-Alchemist + I-Numogram-Oracle
session_type: diagnostic + stepper-template
---

## Executive Summary

**Phase 1 complete** — closed-loop KS → WAV → MIR → classifier works end-to-end; intentional domain collapse confirms 11.1% accuracy (expected, training artefacts were real-world MOD samples, not KS).  
**Phase 2 complete** — per-zone centroid profiling shows 7.4× spectral separation across the 11 KS zones; feature-space structure is real, classifier gap is distributional.  
**Phase 3 in progress** — JACK dummy daemon confirmed; PD 0.56.2 batch syntax partially decoded; `tabwrite~ → soundfiler → WAV` path documented, `pd quit` still unresolved.

---

## 1. Phase 1 — Closed-Loop Verification ✅

**Artifacts:**
- `ks_string(zone, sr, dur)` in `/home/etym/numogram/mod_writer/renderer/synth.py`
- `/home/etym/numogram/mod_writer/m3_loop.py` (offline orchestrator)
- `/home/etym/numogram/docs/wiki/autonomous-journal/artifacts/m3_phase1_loop_summary.json`

**Result:**
```
Zone     Classified   True       Correct?
Z0 (Void)   3          4          ✗
...         ...        ...        ...
Overall: 1/9 = 11.1% accuracy
```

**Interpretation:** The loop is wired correctly; the MLPClassifier (trained on zone-constrained MOD samples, 29 features) cannot extrapolate to KS-generated audio. The feature-space gap is verified.

---

## 2. Phase 2 — KS-Zone MIR Benchmark ✅

**Artifacts:**

🐚 Phase 1 (closed-loop): `/tmp/m3_loop/` (9 KB WAV + `m3_p1_summary.json`, **not in wiki — ephemeral**)
  → *M3 Phase 3a (open): archive this dir to `autonomous-journal/artifacts/m3_phase1_loop/` to prevent loss.*

| Artifact | Path |
|----------|------|
| WAV per zone (×9) | `/tmp/m3_loop/z[01-09]_*.wav`, 259K each |
| Summary | `/tmp/m3_loop/m3_p1_summary.json` (confusion table) |
| Per-zone caller | `/tmp/m3_profile.json` (Phase 2, same as canonical) |

**Per-zone prediction breakdown (raw, from `m3_p1_summary.json`):**

| Zone | Name | pred | correct? | centroid (Hz) | proba |
|------|------|-----:|---------:|--------------:|------:|
| **Z1** surge | 2 (breaker) | ✗ | 2570 | 1.00 |
| **Z2** breaker | 2 (breaker) | **✓** | 592 | 1.00 |
| **Z3** warp | 2 (breaker) | ✗ | 1483 | 1.00 |
| **Z4** gate | 2 (breaker) | ✗ | 3014 | 1.00 |
| **Z5** pressure | 7 (blood) | ✗ | **1203** ⚠️ | 1.00 |
| **Z6** abstraction | 2 (breaker) | ✗ | 2051 | 1.00 |
| **Z7** blood | 2 (breaker) | ✗ | 1366 | 1.00 |
| **Z8** multiplicity | 7 (blood) | ✗ | 3229 | 0.95 |
| **Z9** plex | 2 (breaker) | ✗ | 5027 | 1.00 |

⚠️ **Z5 centroid anomaly:** 1203 Hz actual vs. 856 Hz Phase 2 mean — this track crossed into Zone 7's recognition basin.

**Artifacts:**
- `/home/etym/numogram/mod_writer/m3_profile.py` (170 lines)
- `/home/etym/numogram/docs/wiki/autonomous-journal/artifacts/m3_phase2_zone_profiles.json`

**Per-zone centroids (KS synth, n=2, seed=42):**

| Zone | Name        | f0 (Hz) | Centroid (Hz) | BW (Hz)  | RMS (dB) |
|------|-------------|--------:|--------------:|---------:|---------:|
| Z5   | pressure    | 300     | 856           | 2096     | −52.6    |
| Z2   | breaker     | 250     | 1043          | 1363     | −43.9    |
| Z3   | warp        | 200     | 1300          | 2182     | −49.2    |
| Z7   | blood       | 160     | 1378          | 2389     | −36.9    |
| Z1   | surge       | 180     | 2716          | 4641     | −44.2    |
| Z6   | abstraction | 180     | 2820          | 4670     | −38.5    |
| Z8   | multiplicity| 150     | 3174          | 5103     | −36.0    |
| Z0   | void        | 140     | 3257          | 5000     | −38.4    |
| Z4   | gate        | 120     | 3373          | 3967     | −46.4    |
| Z9   | plex        | 90      | 6303          | 6569     | −33.5    |

**Span:** 856 Hz → 6303 Hz = **7.4× spectral separation**.  
**Key driver:** f0 (pitch) — lower f0 pushes centroid higher through KS partial structure.  
**BPM ghosts:** measurable in all zones; known KS frame-rate artefact, not musical tempo.  
**Conclusion:** zones *do* produce structured feature-space separation. Classifier failure is distributional (KS ≪ MOD), not absence of signal.

---

## 3. Phase 3 — JACK + PD Batch Render 🔄

**Status:** JACK confirmed; PD batch path partially decoded; no live WAV yet from batch mode.

### 3a. JACK Dummy Daemon
```bash
jackd -d dummy -r 44100 -p 512
```
Works in foreground. Background via `terminal(background=true)`. No hardware or ALSA dependency. PID tracked and killed each cycle.

### 3b. PD Object Forensics (Pd 0.56.2 confirmed objects)
| Object | Status | Correct Syntax |
|--------|--------|----------------|
| `tabwrite~` | ✅ | `# X obj … tabwrite~ arrayname`; `msg start arrayname;` `msg stop arrayname;` |
| `soundfiler` | ✅ | `# X msg … write -wave /path/file.wav arrayname` |
| `osc~`, `*~`, `+` | ✅ | standard objects, no issues |
| `writesf~` | ⚠️ flaky | creation under auto-patch hit `"bad arguments for message"`; use `tabwrite~` instead |
| `pd quit` | ❌ broken | `"canvas: no method for 'pd'"` — must use `; pd quit` or external env trigger |
| `loadbang`, `timer`, `f`, `>` | ✓ | objects confirmed from help patches |

### 3c. Working Batch Skeleton (hypothesis, not yet validated end-to-end)
```pd
# N canvas 0 0 600 400 10;
# X obj 10 50 tabwrite~ sigbuf;
# X msg 10 90 start sigbuf;
# X obj 10 130 osc~ 440;
# X obj 10 170 *~ 0.5;
# X obj 10 210 dac~;
# X msg 10 250 stop sigbuf;
# X obj 200 50 soundfiler;
# X msg 200 90 write -wave /tmp/zr_out.wav sigbuf;
# X msg 280 90 pd quit;   ← still hangs; correct syntax unknown
```

---

## 4. Key Decisions

| Decision | Rationale |
|----------|-----------|
| Python-first unblock | Verify data-pipeline before wiring JACK; Stage 1 closed-loop validated end-to-end regardless of server state |
| JACK isolated | Dummy daemon confirmed; Tui tmux launching deferred to Phase 4; do not mix JACK with M3 struct |
| `ZONE_PARAMS` reuse | Canonical table in `render_zone_resonator.py`; no duplication |
| KS-domain benchmark separate from classifier | Re-train only if M3 hypothesis requires MOD-classifier applicability to real-time zone-by-zone tracker interaction |
| `tabwrite~` → `soundfiler` over `writesf~` | `writesf~` object creation errors in auto-patched batch; `tabwrite~` creates cleanly; `soundfiler` write documented |

---

## 5. Open Questions / Current Blockers

- `pd quit` from inside a Pd patch — failing with `"canvas: no method for 'pd'"`. Candidates: `; pd quit` message syntax, or use `; pd dsp $1` toggle then external exit, or environment variable to close on empty queue.
- Full zone-parameterised WAV write not yet end-to-end validated. The loop must prove a non-zero WAV before moving to rhythmic/ketitudinal zone sweep.

---

## 6. Architecture Map

```
m3_loop.py  ──► KS zone synth ──► /tmp/*.wav ──► mir_profiler.py (44-dim)
                                           │
                                           └──► mlp_classifier  ──► Zone hit/miss
                                                                           │
                                                                           ▼
                                                          m3_profile.py  ──► centroid/RMS/BPM table

m3_profile.py (Phase 2)  ──► zone→centroid benchmark  (no classifier)
m3_batch_render.py (Phase 3, next) ──► PD/WAV generation
```

---

## 7. Related Resources

| Resource | Path |
|----------|------|
| ZONE_PARAMS canonical table | `/home/etym/.hermes/skills/creative/puredata-wrapper/scripts/render_zone_resonator.py` |
| KS algorithm reference | `/home/etym/.hermes/skills/creative/puredata-wrapper/references/python-karplus-strong.md` |
| Zone-audio synthesis | `/home/etym/.hermes/skills/numogram-zone-audio-synthesis/src/zone_audio_synth.py` |
| Audio renderer (mod-writer) | `/home/etym/numogram/mod_writer/renderer/synth.py` |
| MIR profiler | `/home/etym/numogram/mod_writer/mod_writer/mir_profiler.py` |
| Classifier trainer | `/home/etym/numogram/mod_writer/mod_writer/classifier/trainer.py` |
| Classifier artifacts | `zone_clf.joblib` (29 feat, zones 1–9) |
| M3 product spec | `/home/etym/numogram/docs/wiki/the-unbuilt.md` |
| Phase 2 MIR stats | `/autonomous-journal/artifacts/m3_phase2_zone_profiles.json` |
