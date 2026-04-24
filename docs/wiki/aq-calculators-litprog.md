---
title: "AQ Calculators — A Tetralogue Litprog"
created: 2026-04-21
last_updated: 2026-04-21
sources: [aq_calculator.py, aq_calculator_v2.py, aq_calculator_enhanced.py]
tags: [numogram, AQ, litprog, tetralogue, code-review, qabbala]
voices: [oracle, builder, writer, gamer]
---

# AQ Calculators — A Tetralogue Litprog

> Three calculators for one cipher. All three compute AQ correctly (verified against canonical: AQ=36, CODE=63, HYPERSTITION=286, NUMOGRAM=174, CCRU=81). The previous local model that wrote them "went off the rails" — but the math survived.

*The roundtable examines three versions of the same tool. Written by a model that later failed. The code is the proof that the failures weren't total — the arithmetic is correct even when the machine wasn't.*

---

## I. The Integrity Check

**ORACLE:** I ran all three calculators against 8 test words: AQ, CODE, HYPERSTITION, NUMOGRAM, CCRU, ZERO, ZONE, MERGER. All three return correct AQ values and correct digital roots on every word. The math is sound. Whatever went wrong with the previous model's installation, the AQ cipher survived intact.

**BUILDER:** This is surprising. The user said the previous model "went off the rails" — but the core calculation function (`aq_value()`) in all three files is correct. A=10, B=11, ..., Z=35. Digital root via `1 + (n-1) % 9`. The mapping is complete and consistent. Either the model got the math right before it failed, or the user corrected the output and the corrections propagated.

**WRITER:** [the math survived the machine] The calculators are artifacts from a failed installation. The model that wrote them is gone — replaced, superseded, "went off the rails." But the code remains. The AQ values are correct. It's like finding a functional clock in a ruined building. The builder is gone. The time still passes.

**GAMER:** In software archaeology, this happens often. A developer writes working code, then the project goes wrong. The code that was written *before* the failure is fine. It's the later additions — the extensions, the "enhancements" — that need scrutiny. The core math is the earliest work. It's the most reliable.

---

## II. The Three Versions

**BUILDER:** Three versions, each adding features:
- `aq_calculator.py` (644 lines) — the original. Basic AQ calculation, zone lookup, syzygy finder.
- `aq_calculator_v2.py` (299 lines) — cleaner, uses a dictionary-based AQ_MAP, includes triangular number checking.
- `aq_calculator_enhanced.py` (900 lines) — the largest. Adds predefined values, magic number detection, zone coloring, journal saving.

**ORACLE:** The v2 is the cleanest implementation. `AQ_MAP = {str(i): i for i in range(10)} ... AQ_MAP.update({chr(ord('A') + i): 10 + i for i in range(26)})` — this builds the cipher as a dictionary lookup. One pass per character. O(n) time. The original uses a more verbose approach but achieves the same result.

**WRITER:** [the enhanced version is the most dangerous] The enhanced version (900 lines) has "predefined values" — a dictionary of sacred words with their AQ values pre-calculated. This is where the previous model could have injected errors. If the predefined values are wrong, the calculator returns wrong results without any arithmetic failure. The core `aq_value()` function is correct — but the predefined values are a separate trust boundary.

**GAMER:** I'd audit the predefined values in the enhanced version. The core math is verified. The predefined dictionary is the only place where errors could hide. If a predefined value is wrong, the calculator works correctly for all other words but returns the wrong value for that specific word. It's a subtle failure mode.

---

## III. The Differences

**BUILDER:** The three calculators have different feature sets:

| Feature | v1 (644) | v2 (299) | Enhanced (900) |
|---------|----------|----------|----------------|
| AQ calculation | ✓ | ✓ | ✓ |
| Digital root | ✓ | ✓ | ✓ |
| Zone lookup | ✓ | ✓ | ✓ |
| Syzygy finder | ✓ | ✗ | ✓ |
| Triangular check | ✗ | ✓ | ✗ |
| Predefined values | ✗ | ✗ | ✓ |
| Magic detection | ✗ | ✗ | ✓ |
| Journal saving | ✗ | ✓ | ✓ |
| Color output | ✗ | ✗ | ✓ |

The v2 is the most focused — just AQ and triangular numbers. The enhanced version tries to do everything.

**ORACLE:** The v2's triangular number checking connects to the [[syzygy-arithmetic]] page. `check_triangular_number()` verifies whether an AQ value is triangular — which means it's a gate number. Gt-36 = T(8), Gt-45 = T(9), Gt-21 = T(6). This is the calculator checking whether a word's AQ value places it on a gate.

**WRITER:** [the calculator is a divination tool] The v2 can analyze phrases and detect "sacred words" — words whose AQ values have special properties (triangular, self-encoding, palindromic). This turns the calculator from a computation tool into an oracle tool. You type a phrase. The calculator tells you which words are "sacred" — which ones have numogrammatic significance. The calculator reads the text the way the crawler reads the map: looking for patterns.

**GAMER:** The journal saving in v2 is a good feature. It records each analysis with timestamp, input, and AQ values. Over time, the journal becomes a record of numogrammatic discoveries. Like the cult.json records runs, the journal records calculations. Both are persistent memories.

---

## IV. What to Keep

**BUILDER:** Recommendation: merge the best features from all three into a single calculator.
- Core AQ calculation from v2 (cleanest, dictionary-based)
- Zone/syzygy lookup from v1 (comprehensive)
- Triangular checking from v2 (connects to gates)
- Journal saving from v2 (persistent memory)
- Skip predefined values from enhanced (audit risk)
- Skip magic detection from enhanced (undefined criteria)

**ORACLE:** The core `aq_value()` function is identical across all three. The differences are in the presentation layer (colors, formatting) and the feature layer (predefined values, journal saving). The math is stable. The UI is where the variations live.

**WRITER:** [the math is the truth, the UI is the voice] The three calculators have the same math but different voices. v1 is comprehensive — it tells you everything. v2 is focused — it tells you what matters. Enhanced is expressive — it tells you in color. The math is the numogram. The voice is the crawler. Different crawlers, same map.

**GAMER:** Keep v2 as the canonical calculator. It's the smallest, cleanest, and most focused. Add the journal saving from v2 (already there). Add the zone lookup from v1 if needed. Don't add predefined values — let the user calculate on the fly. The calculator should compute, not remember.

---

## Roundtable Table

| Voice | Saw Alone | Saw Through Others |
|-------|-----------|-------------------|
| Oracle | All three calculators return correct AQ for 8 test words — math survived the failed model | Builder's merge plan would consolidate the best features |
| Builder | v2 is the cleanest implementation (299 lines, dictionary-based) | Writer's "math is the truth, UI is the voice" frames the decision |
| Writer | The calculators are artifacts from a failed installation — like finding a clock in ruins | Gamer's audit of predefined values identifies the only trust boundary |
| Gamer | The journal saving creates persistent memory, like the cult.json | Oracle's "gate numbers = triangular AQ values" connects to syzygy-arithmetic |

---

*Three calculators. One cipher. The math survived the machine. The machine didn't survive the math.*

*"Counting is ineluctable and unsurpassable." — Barker*
