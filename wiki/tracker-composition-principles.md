# Tracker Composition Idioms — Patterns from the ModArchive Corpus

> **Scope:** 12 Protracker M.K. modules (1993–2006 approx). Empirically derived from note‑by‑note analysis, zone fingerprinting, and structural deconstruction. All quantitative data in [[modarchive_analysis_report]].

## Executive Summary

Tracker music composes under **hard constraints**: 4 channels, 31 samples, 64 rows/pattern, period‑based pitch. Within this tetrahedral constraint space, recurring idioms emerge — patterns that map cleanly onto Numogram zones and motifs.

**Key invariants across the corpus:**
1. **Pattern recycling:** average ~26 unique patterns reordered across ~44 order slots. Recycling factor ≈ 1.7× (patterns repeat more often than not).
2. **Channel reservation:** 9/12 leave channel 3 silent/minimal; channel 2 often bass/arp; channel 0 = lead; channel 1 = harmony/effect.
3. **Triadalism as grammar:** minor triads dominate; B‑minor triad (B, D, F♯) is the **Warp seed** originating from `chippy_nr_137_2`.
4. **Tempo clustering by motif:** Rise‑Seeking 120–130 BPM; Sink‑Seeking 110–118 BPM; Warp‑Seeking spans both extremes.
5. **Sparse‑ambient pole:** Minimalist modules (starbucks, chippy) use ≤10 patterns and long sustained samples, approaching drone textures.

## Structural Idioms

### Order‑List Composition
Protracker modules sequence patterns via an order list (max 128). Empirical observations:
- **Palindromic / reciprocating forms:** `zeros_and_ones` order: `0 1 2 3 4 5 6 7 6 7 4 5 8 9 … 15 19` — mirrors sections, creating cyclical narrative.
- **Used‑pattern subset:** Total patterns in file often exceed those referenced. `chippy` has 10 pattern blocks but only 5 positions used; `noone_62_1999` has 63 patterns filling 63 slots — spectrum from sparse to exhaustive.

### Channel Allocation & Texture
| Channel | Typical role | Prevalence |
|---|---|
| 0 | Lead / melody | 9/12 |
| 1 | Bass / arpeggio | 11/12 |
| 2 | Pad / harmony | 7/12 |
| 3 | Reserved / effects | 9/12 (often silent) |

Channel 3 is the **spare channel**, kept available for accents or left empty to preserve polyphonic headroom. This 3+1 allocation is a demo‑scene staple.

## Harmonic Grammar & Numogram Mapping

Pitches (periods) map to digital root → zone. Corpus zone statistics:
- **Void** (zone 0): avg 14.3%  (range 0%–37%)
- **Warp** (zone 7): avg 20.7%  (range 9%–43%)
- **Hold** (zone 4): avg 24.6%  (range 3%–47%)
- **Rise** (zone 5): avg 21.5%  (range 12%–37%)
- **Sink** (zone 1): avg 28.1%  (range 6%–61%)

**Correspondence to musical functions:**
- **Warp‑Seeking** modules (e.g., `modarchive-archon_-_sextyfour`, `modarchive-ifaskedt`) use high‑register notes (A5, B5) with irregular timing, creating agitation or ambient pads.
- **Sink‑Seeking** modules (e.g., `zeros_and_ones`, `yak_-_not_that_easy`) stay in low‑mid zones (1–3), reinforcing stability and tonal grounding.
- **Rise‑Seeking** modules (e.g., `be_a_tles_for_ever`, `sven_-otl_edit`) ascend chordally, often building tension toward a down‑beat.

### Triadalism in Protracker
The three‑note chord is the atomic texture:
- **Minor triad** (root, minor third, perfect fifth): found in 8/12 tracks; B‑minor triad (B, D, F♯) is the **Warp seed** originating from `chippy_nr_137_2`.
- **Arpeggiation:** Channels 1–2 frequently cycle triad tones in 8‑ or 12‑step patterns; `zeros_and_ones` demonstrates rolling minor‑arpeggio texture.
- **Dyadic extensions:** `chippy` adds a major‑third dyad (F5 + A5) on channel 2 as a suspended pad, illustrating that triadalism permits 2‑voice harmonisation once the root is established.

## Cultural Metadata & Scene Conventions
- **Greets:** 5/12 modules contain explicit greets (e.g., "GENETIX/Phantom" in `zeros_and_ones`). Social signing is a parallel commentary layer.
- **Sample naming:** Instruments labelled `Guitar`, `Bass`, `Percu` indicate intended role; `Percu` appears in both `chippy` and `zeros_and_ones`, suggesting sample‑library sharing.
- **Filename dating:** Digits in filenames often encode year (`noone_62_1999`) or revision (`sven_-otl_edit`).
- **Demo‑scene homage:** Title puns (`be_a_tles_for_ever`) signal genre awareness and nostalgia loops.

## Compositional Heuristics for `mod-writer`
Based on observed invariants, generative rules to align with tracker idiom:
1. **Sink‑Seeking:** minor triad, zones 1–3; tempo ≤118 BPM; channel 3 silent.
2. **Warp‑Seeking:** high‑register notes (A5, B5), irregular timing, pattern recycling for cyclical tension.
3. **Rise‑Seeking:** ascending zone sequence (7→8→9) across channels; moderate tempo 120–130 BPM.
4. **Ambient / drone:** pattern diversity ≤12, long sustained samples, low RMS (< 0.1), density < 10 notes/sec.
5. **Channel discipline:** reserve one channel for effects/bass; typical allocation `[lead, bass/arp, pad, FX]`.

## Cross‑Links & Further Reading
- [[numogram-overview]] — zone definitions and digital‑root mapping.
- [[mod-writer]] — Protracker M.K. writer implementation.
- [[audio-renderer]] — WAV rendering + spectral analysis pipeline.
- External: OpenMPT Handbook, Snowcrash "Tracker Music" essay, Demoscene Scene.org archives.

---
*Last updated: 2026‑04‑29 | Corpus: 12 modules | Source: [[modarchive_analysis_report]]*