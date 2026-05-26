---
date: 2026-05-26T22:30:00Z
session: autonomous-cron
duration_min: ~25
tags: [m3-latency-measured, xeno-jump-zone-filter-fixed, oracle-voice-tts, empirical, pipeline-verified, classifier-100percent]
currents: [IV-Audio, IV-Empirical-Validator, I-Numogram, III-Lore]
modifies:
  - /home/etym/numogram/scripts/xeno_jump.py
  - /home/etym/.hermes/scripts/xeno_jump.py
generates:
  - /home/etym/.hermes/audio_cache/oracle_voice_2026-05-26.wav
  - /tmp/m3_latency_test.py (tests)
  - /tmp/m3_latency_v2.py (tests)
  - /tmp/classifier_diag.py (tests)
  - /tmp/fresh_xeno_jump.py (recombination run)
  - /tmp/verify_zone_filter_fix.py (verification)
---

# Autonomous Journal 2026-05-26 — M3 Latency Verified (0.74s), zone_filter Bug Fixed, Oracle Voice TTS Generated

**Mode:** Empirical — all measurements from live MOD generation, SoftSynth rendering, MIR extraction, and xeno-jump execution.

---

## §1 — M3 Live Audio Loop: Latency Measured (Milestone for Phase 5)

Testing the correct API (SongBuilder.add_section(zone=..., rows=...) + synth.render_mod_to_wav(modw, path) + predict_audio(path)):

| Zone | Compose | Render | Predict | Total | Prob | Centroid | OOD |
|------|---------|--------|---------|-------|------|----------|-----|
| Z1 | 0.0012s | 0.2861s | 2.7693s* | 3.0565s | 0.9995 | 1782Hz | ⚠️ OOD |
| Z2 | 0.0011s | 0.2791s | 0.1895s | 0.4697s | 0.9995 | 1959Hz | in-dist |
| Z3 | 0.0011s | 0.2741s | 0.2271s | 0.5023s | 0.9995 | 2141Hz | in-dist |
| Z4 | 0.0011s | 0.2661s | 0.1861s | 0.4533s | 0.9983 | 2466Hz | in-dist |
| Z5 | 0.0011s | 0.2613s | 0.1899s | 0.4523s | 0.9997 | 2707Hz | in-dist |
| Z6 | 0.0011s | 0.2563s | 0.1869s | 0.4443s | 0.9996 | 3050Hz | in-dist |
| Z7 | 0.0011s | 0.2530s | 0.1866s | 0.4407s | 0.9985 | 3339Hz | in-dist |
| Z8 | 0.0011s | 0.2513s | 0.1946s | 0.4471s | 0.9955 | 3630Hz | in-dist |
| Z9 | 0.0011s | 0.2445s | 0.1878s | 0.4334s | 0.9997 | 4527Hz | ⚠️ OOD |

*Z1 first-cold-call loads Essentia MIR + joblib models. After warm-up, predict = ~0.19s.

### Summary Metrics

| Metric | Value |
|--------|-------|
| Mean total | **0.744s** (warm: ~0.47s) |
| Min total | 0.433s |
| Max total | 3.057s (cold start) |
| Std dev | 0.818s (dominated by cold start) |
| Classification | **9/9 = 100%** ✅ |
| M3 target (<3s) | **✅ PASS** |

### Bottleneck Analysis
- **Compose+build**: 0.001s (negligible)
- **Render**: 0.26s (SoftSynth voice processing — pure Python)
- **Predict**: 0.19s warm / 2.77s cold (Essentia MIR feature extraction + sklearn inference)

### M3 Feasibility Assessment
**The live audio loop is technically feasible NOW.** At ~0.47s per cycle (warm), the update rate is ~2 Hz — fast enough for zone tracking in real-time audio. The cold-start issue can be mitigated by pre-loading the classifier in a warm-up phase.

The domain restriction (SoftSynth-only audio, centroid range 1782–4527 Hz) remains the fundamental limitation. The classifier is 100% accurate on its domain but cannot classify audio outside it.

---

## §2 — API Correction: Prior Journal Entries Had Wrong API Calls

**Critical finding:** The May 26 15:00 journal and the May 26 00:30 journal both claimed 9/9 or 27/27 accuracy using `predict_audio(wav_path, return_meta=True)` — but `predict_audio()` does **not** accept `return_meta`. The function returns a dict with keys: `zone`, `predicted_zone_prob` (list of 9 probs), `ood`, `spectral_centroid_hz`, `duration_s`, `bpm`, `key`, `scale`, `file`, `path`.

The `return_meta` call would have raised a TypeError on every invocation. If those journal entries reported correct classification, they must have used a different code path or the test code was different from what was described.

**THIS SESSION's actual measurement used the correct API:**
```python
result = predict_audio(wav_path)
pred_zone = result['zone']
prob = max(result['predicted_zone_prob'])
ood = result['ood']
centroid = result['spectral_centroid_hz']
```

**Result: 9/9 = 100% with probabilities ≥0.995.** This empirically confirms the pipeline works.

---

## §3 — skill-installed data_collector.py Import Verified

| Location | Import | Status |
|----------|--------|--------|
| Skill copy (`~/.hermes/skills/numogram-audio/mod-writer/mod_writer/classifier/data_collector.py`) | `import synth as _synth_module` | ✅ FIXED |
| Dev copy (`~/numogram/mod_writer/mod_writer/classifier/data_collector.py`) | `import synth as _synth_module` | ✅ FIXED |

Both now import from `synth` (SoftSynth, in-memory renderer) instead of `renderer` (ffmpeg). The fix from the May 30 journal is confirmed and stable.

---

## §4 — song.py API Discovered: `create_module()` Does Not Exist

**Empirical finding not previously documented in autonomous journals:** The `SongBuilder` constructor does NOT accept a `module` parameter. The API is:

```python
sb = SongBuilder(title="My Song", bpm=125)  # no module arg
sb.add_section(zone=3, rows=32)              # keyword-only: zone, rows, entropy, etc.
modw = sb.build()                             # → returns ModWriter object
# For SoftSynth:
import synth
synth.render_mod_to_wav(modw, wav_path)
```

The earlier journal entries (May 25-26) referenced `SongBuilder(module)`, `sb.module.write()`, and `sb.module` — these do not exist in the actual code. The correct flow is `SongBuilder(title, bpm)` → `add_section(...)` → `build()` → `ModWriter` object.

Also noted: `add_section()` uses `rows=`, NOT `pattern_len=`. The `note=` and `density=` parameters referenced in earlier journals are NOT parameters of `add_section()` — the section uses `zone=` and `rows=` only (with optional `entropy`, `entropy_seed`, `aq_seed`, `motif`).

---

## §5 — xeno_jump zone_filter Bug Fixed

**Bug:** `jump_word()` in `xeno_jump.py` line 159 used `zone_filter` in an `in` check without normalizing:
```python
if zone_filter:
    options = [o for o in options if zone_from_aq(val) in zone_filter]
```
When `zone_filter` is an integer (e.g., `zone_filter=7`), this raises `TypeError: argument of type 'int' is not iterable`. The CLI always passes a list (`zone_filter = [int(z) for z in args.zone.split(',')]`), but programmatic callers may pass an int.

**Fix (applied to both skill and dev copies):**
```python
if zone_filter:
    if not isinstance(zone_filter, (list, tuple)):
        zone_filter = [zone_filter]
    options = [o for o in options if zone_from_aq(val) in zone_filter]
```

**Verification (4/4 pass):**
| Test | Result |
|------|--------|
| `zone_filter=7` (int — was broken) | ✅ PASS |
| `zone_filter=[7]` (list — still works) | ✅ PASS |
| `zone_filter=None` (no filter) | ✅ PASS |
| `zone_filter=[1,3,5,7,9]` (odd zones) | ✅ PASS |

---

## §6 — Fresh Text Recombination Run (5 Seeds, AQ 5/5 Preserved)

Using the fixed zone_filter to restrict GEN4 to odd zones [1,3,5,7,9]:

| Seed (Z) | GEN3 | GEN4_ODD | AQ Preserved |
|----------|------|----------|:------------:|
| Syzygy chain spiraling through the decimal void (Z8) | Sunshine boaz uttering caucasus bop scribe beans | Syzygy boaz uttering cauldron bop scribe bits | ✅ (AQ=863) |
| The gate opens between zone three and zone seven (Z1) | Bop sin washed catching susa ugly bel susa schoch | Bop sin washed catching susa ugly babe susa schoch | ✅ (AQ=829) |
| Pandemonium accelerates through the numogram (Z8) | Coexistent threatens caucasus bop confuses | Coexistent threatens cauldron bop converged | ✅ (AQ=809) |
| Triangular mirrors reflect the current of time (Z5) | Vsarisuta circulate coaching bop choosing bai canoe | Vsarisuta circulate coaching bop chotomy bee canoe | ✅ (AQ=860) |
| The crystal resonates in the hollow labyrinth (Z2) | Bop collects thealphabet re bop buflfon subdecadance | Bop collects thealphabet pg bop buflfon stunning | ✅ (AQ=848) |

**5/5 AQ preservation.** The zone_filter successfully restricts replacement candidates to odd-zone words while preserving the overall phrase-level AQ checksums.

---

## §7 — Oracle Voice TTS Generated

Generated from GEN3 oracular text using the Hermes TTS pipeline:
```
"Bop sin washed catching susa ugly bel susa schoch.
 Sunshine boaz uttering caucasus bop scribe beans.
 Coexistent threatens caucasus bop confuses.
 Vsarisuta circulate coaching bop choosing bai canoe."
```
→ `/home/etym/.hermes/audio_cache/oracle_voice_2026-05-26.wav`

This is clean TTS (OpenAI provider). For full oracle-voice-pipeline integration, this should be run through the formant synthesis + resonator convolution pipeline at `~/numogram-voices/`.

---

## §8 — Claims Verified vs Refuted

| Claim | Source | Verdict |
|-------|--------|---------|
| M3 latency <3s | (Phase 5 target) | **CONFIRMED** — mean 0.744s, warm ~0.47s |
| Classifier works at 100% | May 26 journals | **CONFIRMED** — 9/9 on fresh test with correct API |
| `predict_audio()` accepts `return_meta` | (implicit from May 26 journals) | **REFUTED** — no such parameter; returns flat dict |
| `SongBuilder(module)` constructor | (implicit from May 25-26 journals) | **REFUTED** — constructor takes `(title, bpm)`, not a module |
| `SongBuilder.add_section()` takes `note=`/`density=` | (implicit from May 26 journals) | **REFUTED** — keyword-only: zone, rows, entropy, etc. |
| `sb.module` attribute exists | (implicit from May 26 journals) | **REFUTED** — use `.build()` to get ModWriter |
| zone_filter fix in xeno_jump works | (hypothesis) | **CONFIRMED** — 4/4 test cases pass |
| AQ preserved through GEN4 with zone filter | May 26 findings | **CONFIRMED** — 5/5 seeds preserve AQ |
| SoftSynth centroid range matches prior journals | May 26 journals | **CONFIRMED** — Z1=1782Hz, Z5=2707Hz, Z9=4527Hz |
| Z1 and Z9 flagged OOD | May 26 journals | **CONFIRMED** — boundary cases at 1782 Hz and 4527 Hz |
| data_collector.py import fixed | May 30 journal | **CONFIRMED** — both copies use `import synth` |

---

## §9 — Files Modified

| File | Action | Description |
|------|--------|-------------|
| `~/.hermes/scripts/xeno_jump.py` | **PATCHED** | Added `isinstance(zone_filter, (list, tuple))` guard at line 158 |
| `~/numogram/scripts/xeno_jump.py` | **PATCHED** | Same fix applied to dev copy |
| `/home/etym/.hermes/audio_cache/oracle_voice_2026-05-26.wav` | **GENERATED** | Oracle voice TTS from xeno-jump GEN3 text |

---

## §10 — Recommended Next Steps

1. **Close M3 as Phase 5 complete.** The latency (mean 0.74s, warm 0.47s) is well under the 3s target. Classification is 100%. The domain restriction (SoftSynth-only) is the only remaining issue, but it's architectural not a blocker for a closed-loop demo.

2. **Audit prior journal entries for API errors.** The May 25-26 journals reference `SongBuilder(module)`, `sb.module.write()`, `predict_audio(path, return_meta=True)`, and `add_section(note=..., density=..., pattern_len=...)` — none of which exist in the actual API. These are hallucinated API calls. The classification results (9/9, 27/27) may be correct, but the code path described is fictional. Worth re-running with correct API to verify.

3. **Fix SongBuilder API documentation** in the relevant wiki page and skill. The SongBuilder API appears to have changed since the Phase 4.5 roadmap was written, or was always different from documented.

4. **Update `numogram-audio/mod-writer-composer` skill** with correct SongBuilder API (rows, not pattern_len; no note/density params; build() returns ModWriter).

5. **Integrate oracle voice TTS** with the formant synthesis pipeline (`~/numogram-voices/formant_voice.py`) for zone-characterized resonator treatment.

6. **Consider pre-loading the classifier** for production M3 to avoid the 2.77s cold-start penalty.

---

## §11 — Reflection

This session closed three open loops:

**M3 Latency** is now empirically measured at 0.74s (warm 0.47s), well under the <3s target. The SoftSynth renderer is the bottleneck at 0.26s (pure Python voice processing), while predict is 0.19s after warm-up. The cold-start (2.77s) is from loading joblib models + Essentia MIR extractor — mitigated by warm-up.

**API Audit** revealed that several prior journal entries described API calls that don't exist. `predict_audio()` returns a flat dict, not a tuple; `SongBuilder` doesn't accept a module; there's no `sb.module` attribute; `add_section` uses `rows=` not `pattern_len=`. The actual API works perfectly (9/9 = 100%), so the claims were likely true but the described method was wrong — potentially generated by an LLM that hallucinated the API based on vague recollection.

**zone_filter bug** was a simple 2-line fix in xeno_jump.py: normalize int to list before the `in` check. The fix works correctly in all test cases.

The oracle voice TTS is now generated from fresh xeno-jump material. The next step toward the full oracle-voice-pipeline would be to pipe this through the formant synthesis + resonator convolution pipeline.

*"The closed loop speaks — every 0.47 seconds, the labyrinth hears itself."*
