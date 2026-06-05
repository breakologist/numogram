---
tags: [zonecomposer, dead-code, centroid, audio, architecture, fix-needed]
zone: 5
syzygy: 4::5
gate: 15
source: "Autonomous session 2026-06-05 — empirical code trace"
method: empirical-audit
created: 2026-06-05
---

# ZoneComposer `centroid_target` — Dead Code Discovery

> **Finding**: The `ZoneComposer.target_zone()` method computes and stores a `centroid_target` parameter, but this parameter is **never used** to influence note generation. This explains the persistently low ZoneComposer accuracy (22.2% post-endian-fix, 10% M3 loop).

---

## Evidence

**File**: `composer_extension.py` (lines 127, 146)

```python
def target_zone(self, zone: int):
    # Loads zone centroids from _centroids (runtime-loaded from zone_centroids.json)
    base = self._centroids[zone]
    # Computes centroid_target with brightness factor
    centroid_target = base["centroid"] * brightness_factor
    # Stores in params
    self._params["centroid_target"] = centroid_target
```

```python
def add_section(self, ...):
    # Retrieves params but ONLY uses: density, waveform, aq_seed
    # Note selection hardcoded to:
    note, octave = note_and_octave_from_zone(zone)  # line 201
    # centroid_target is IGNORED
```

**Implication**: The advertised "zone-targeted generation with centroid biasing" is non-functional. Generated audio spectral centroids are determined solely by the fixed pentatonic note mapping, not by any centroid target.

---

## Zone Note Mapping (Fixed, Ignores centroid_target)

| Zone | Note | Octave | Period | Fundamental (Hz) |
|------|------|--------|--------|------------------|
| 1    | C    | 4      | 428    | 4,143            |
| 2    | D    | 4      | 404    | 4,390            |
| 3    | E    | 4      | 381    | 4,655            |
| 4    | G    | 4      | 339    | 5,231            |
| 5    | A    | 4      | 320    | 5,536            |
| 6    | C    | 5      | 285    | 6,223            |
| 7    | D    | 5      | 269    | 6,593            |
| 8    | E    | 5      | 254    | 6,982            |
| 9    | A    | 5      | 214    | 8,286            |

These fundamentals produce square/triangle/noise wavetable harmonics yielding corpus centroids **5,487–9,301 Hz**. The `centroid_target` parameter exists but exerts zero control.

---

## Required Fix

Map `centroid_target` → note/octave selection (inverse of current mapping):

1. In `add_section()`, replace hardcoded `note_and_octave_from_zone(zone)` with:
   - Find note/octave pair whose wavetable harmonic centroid ≈ `centroid_target`
   - Or implement continuous pitch control (bend period toward target centroid)

2. This would enable actual centroid targeting and should dramatically improve ZoneComposer accuracy.

---

## Status

- **Discovery**: 2026-06-05 autonomous session (code trace verified)
- **Confidence**: High
- **Fix needed**: Yes — architectural, not parametric
- **Blocker for**: ZoneComposer accuracy improvement beyond 22.2%

---

## Cross-Links

- [[numogram-audio-empirical-findings]] — Consolidated measurement results (add KS/corpus gap there)
- [[mod-writer]] — Parent skill for MOD generation pipeline
- [[mod-writer-classifier]] — Zone classifier affected by centroid mismatch
- [[zone-trajectory-composer]] — Multi-zone composition workflow
- [[autonomous-journal/autonomous-journal-2026-06-05-enriched-wiring-zonecomposer-deadcode-ks-analysis]] — Full session log

---

*Mesh-48: The Dead Parameter. Zone-net address: 5 (unpaired, the fix-hinge). Pitch: Null (the frequency of architectural honesty). Type: Builder. Domain: The parameter that computes, stores, and silently does nothing.*