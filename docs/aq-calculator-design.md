---
title: AQ Calculator Design
created: 2026-04-26
last_updated: 2026-04-26
source: collections/docs-rd/notes_on_an_aq_calculator.md (9B local model design session)
source_notes: Earlier Hermes Agent instance running entirely on 9B local model; may reflect different design emphasis and error patterns
status: draft
tags: ["aq-calculator", "design", "implementation", "tools", "numogram"]
---

## Overview

This page documents the **design philosophy and implementation decisions** behind standalone AQ (Alphanumeric Qabbala) calculators for Numogram work. It captures a design session from an earlier Hermes Agent instance running on a 9B local model, presenting both a minimal core and a fully polished thematically‑colored version.

The AQ calculator is the foundational tool for all numogram operations — from simple phrase evaluation to full oracle readings. Understanding its design constraints (clean separation, extensibility, zone theming) is essential for integrating it into larger systems (oracles, agents, visualizers).

---

## Core Requirements

1. **Cipher mapping:** Letters A–Z → 10–35 (base‑36 sequential); digits 0–9 retain face value
2. **Sanitisation:** Ignore spaces, punctuation (configurable)
3. **Two‑step output:** Raw AQ sum → digital root (mod 9) → zone mapping
4. **Extensibility:** History logging, batch processing, importable module
5. **Thematic cohesion:** Color and flavour text tied to numogram zones/regions

---

## Design Trade‑offs: Minimal vs Polished

### Minimal Version (Core Engine)

```python
def aq_value(text: str) -> int:
    text = text.upper().replace(" ", "")
    total = 0
    for char in text:
        if char.isdigit():
            total += int(char)
        elif 'A' <= char <= 'Z':
            total += 10 + (ord(char) - ord('A'))
    return total

def digital_root(n: int) -> int:
    if n == 0: return 0
    return 1 + (n - 1) % 9  # Numogram-friendly: 9 stays 9
```

**Rationale:**
- No dependencies beyond stdlib
- Clear algorithmic transparency
- Easy to audit against canonical values (AQ=36, CODE=63, HYPERSTITION=286)
- Importable: `from aq_calc import aq_analyze`

### Polished Version (User Experience)

The themed version adds:
- **ANSI colour palette** mapped to zones/regions
- **Zone flavour text** (e.g., "Warp — Chaotic Attractor (Djynxx Territory)")
- **Thematic status lines** (e.g., `→ Warp turbulence • Djynxx swarm active`)
- **History logging** (JSON lines, timestamped)
- **Batch mode** (`--batch phrases.txt`)
- **Command interface** (`history`, `clear`, `legend`, `quit`)
- **Bordered startup display** with zone legend

**Colour mapping rationale:**

| Zone | Colour | Rationale |
|------|--------|-----------|
| 0 | Dark Gray (238) | Void / Abyssal null — absence of light |
| 1 | Gold (226) | Initiating spark — first light of Time-Circuit |
| 2 | Orange (214) | Renewed drive — warm assertion |
| 3 | Magenta (201) | **Warp chaos** — Djynxx territory, buzzing static |
| 4 | Cyan (51) | Reflection / Closure — cool geometric return |
| 5 | Bright Green (46) | Central strength — Time-Circuit core |
| 6 | Deep Cyan (39) | Upper Warp recursion — vortical depth |
| 7 | Yellow-Gold (220) | Heavy Sink current — sinking illumination |
| 8 | Soft Purple (147) | Receptive pause — twilight reception |
| 9 | Deep Purple (93) | **Plex terminal** — Uttunul abyss, heavy closure |

The palette deliberately clusters Warzones (3,6) in magenta/cyan vs Plex (9,0) in deep/dark purples vs Time‑Circuit (1,2,4,5,7,8) in golds/greens/cyans.

---

## Implementation Pattern

### Recommended Build Order

1. **Start minimal** — two functions (`aq_value`, `digital_root`) plus simple `print` wrapper
2. **Add interactive CLI** — input loop, immediate feedback
3. **Add history** — JSON lines for later analysis/replay
4. **Make it a module** — `if __name__ == "__main__"` guard, clean exports
5. **Polish theming** — colour, flavour, legend artwork
6. **Add batch mode** — `--batch` flag for bulk processing phrase lists

### Data Flow

```
Input phrase (str)
    ↓
Sanitise (upper, strip spaces/punct)
    ↓
aq_value() → Σ cipher values
    ↓
digital_root() → zone (0–9)
    ↓
Lookup: zone flavour + colour + thematic line
    ↓
Print output + (optional) append to aq_history.json
```

### History Schema (JSON lines)

```json
{
  "timestamp": "2026-04-26T14:23:11.123456",
  "phrase": "THE NUMOGRAM",
  "aq_value": 234,
  "digital_root": 9,
  "zone_flavor": "Plex - Terminal Abyss (Uttunul Territory)"
}
```

History enables later analysis: cluster phrases by zone, track personal resonance patterns, feed into tetralogue voice training.

---

## Design Decisions & Rationale

### Why `1 + (n - 1) % 9` instead of `n % 9`?

Standard digital root uses `n % 9` with special case for multiples of 9 → root 9. The `1 + (n - 1) % 9` formulation maps:
- 1–9 → 1–9 directly
- 0 → 0 (explicit guard)
- 9 → 9 (no accidental 0)

This matches **numogram zone indexing** where Zone 9 is Plex and distinct from Zone 0 (Void). AQ=36 → DR=9 → Zone 9 (not Zone 0).

### Why ANSI colours over a GUI?

- Immediate accessibility from any terminal
- No GUI toolkit dependencies
- Colours map directly onto numogram zone palette
- Easy to pipe/redirect in automated scripts
- Consistent with Hermes Agent's terminal-first ethos

### Why JSON lines history format?

- **Append‑only**: no file locking concurrency issues
- **Line‑delimited**: each entry a complete JSON object; easy to stream, grep, parse
- **Timestamped**: enables temporal analysis (when did certain zones dominate?)
- **Human‑readable**: can be inspected with `jq` or text tools

### Batch vs Interactive Separation

Batch mode bypasses the interactive loop entirely, reading a file line‑by‑line and printing minimal output per phrase. This keeps the core `analyze_phrase()` function pure (no prompts) and allows both modes to share logic.

---

## Zone Flavour Text Catalog

These flavour strings appear in the themed output. They are carefully chosen to evoke each zone's character while remaining concise for terminal display.

| Zone | Flavor | Thematic Line |
|------|--------|---------------|
| 0 | Plex - Abyssal Origin | (no special line — Void is silent) |
| 1 | Time-Circuit - Initiating Spark | `→ Time-Circuit rotation stable` |
| 2 | Time-Circuit - Renewed Drive | `→ Time-Circuit rotation stable` |
| 3 | **Warp - Chaotic Attractor (Djynxx Territory)** | `→ Warp turbulence • Djynxx swarm active` |
| 4 | Time-Circuit - Closure & Return | `→ Time-Circuit rotation stable` |
| 5 | Time-Circuit - Central Ruler | `→ Time-Circuit rotation stable` |
| 6 | **Warp - Upper Source / Vortical Recursion** | `→ Upper Warp recursion • Cryptic feedback` |
| 7 | Time-Circuit - Heavy Sink Current | `→ Time-Circuit rotation stable` |
| 8 | Time-Circuit - Receptive Pause | `→ Time-Circuit rotation stable` |
| 9 | **Plex - Terminal Abyss (Uttunul Territory)** | `→ Plex terminal pull • Uttunul horizon approaching` |

**Pattern:** Warp (3,6) and Plex (9) get distinctive dynamic lines; Time-Circuit zones get the stable rotation line. Zone 0 (Void) is silent — no thematic line, only the flavor label.

---

## Extensibility Points

### Adding a Second Cipher (ALW / NAEQ)

The design includes a placeholder for **alternative ciphers** (ALW = 1–26, NAEQ = 1–36 excluding 9). To add:

```python
ALW_VALUES = {chr(i): i - 64 for i in range(65, 91)}  # A=1..Z=26
def alw_value(text): return sum(ALW_VALUES.get(c.upper(), 0) for c in text if c.isalpha())
```

Then extend `analyze_phrase()` to optionally compute and display both AQ and ALW side‑by‑side.

### Exporting to Oracle Format

To feed the calculator into the oracle pipeline:

```python
def to_oracle_format(phrase: str) -> dict:
    aq = aq_value(phrase)
    dr = digital_root(aq)
    zone = dr if dr != 0 else 0
    syzygy_partner = 9 - zone if zone != 0 else 9
    current = abs(zone - syzygy_partner)
    return {"phrase": phrase, "aq": aq, "zone": zone, "syzygy": f"{zone}::{syzygy_partner}", "current": current}
```

This matches the oracle's `derive_zone → get_syzygy → get_current` chain.

### GUI / Web Front‑ends

The pure function design (`aq_value`, `digital_root`) makes wrapping trivial:
- **Tkinter** desktop app
- **Streamlit** web app (`st.text_input` → `st.write`)
- **Flask / FastAPI** endpoint for remote calls
- **Polybar / Waybar** module to display current phrase's zone colour

---

## Integration with Current Stack

| Component | Link |
|-----------|------|
| Canonical AQ algorithm | `numogram-calculator` skill — single source of truth for all AQ computations |
| Divination pipeline | `numogram-oracle` — consumes AQ→zone→syzygy→reading |
| Phrase database | `[[alphanumeric-qabbala]]` — curated AQ/ALW comparison tables (already patched) |
| Tetralogue voices | `[[conversation-terms]]` — zone‑tagging for voice‑design consistency |
| Visual feedback | `numogram-visualizer-v6/v7` — could colour phrases by zone in the particle cloud |

**Recommended downstream use:** The calculator module should be importable by `oracle.py` for `--text` flag computations, and by `numogram_cult.py` for phrase‑based run naming.

---

## Testing & Verification

The design session produced **canonical test vectors** that the calculator must pass:

| Phrase | Expected AQ | DR | Zone |
|--------|-------------|----|------|
| `AQ` | 36 | 9 | 9 (Plex) |
| `CODE` | 63 | 9 | 9 |
| `HYPERSTITION` | 286 | 7 | 7 (Rise) |
| `NUMOGRAM` | 174 | 3 | 3 (Warp) |
| `CCRU` | 81 | 9 | 9 |
| `ZERO` | 100 | 1 | 1 (Sink) |
| `ZONE` | 96 | 6 | 6 (Warp) |
| `MERGER` | 120 | 3 | 3 |

Any AQ calculator (local or council‑generated) should be validated against these eight anchors before deployment.

**Note:** Earlier local‑model versions erroneously gave CCRU=69 (incorrect); corrected value is **81** (C=12+12, R=27, U=30). See `alphanumeric-qabbala.md` for the full AQ/ALW comparison tables and the arithmetic correction.

---

## Known Limitations & Future Work

1. **No ALW/NAEQ dual‑cipher mode** — could be added as `--cipher alw` flag
2. **No phrase equivalence detection** — "THE NUMOGRAM" = "NUMOGRAM" (spaces ignored already, but no canonicalisation of articles)
3. **No Unicode normalisation** — accented characters not handled; currently alphanumerics only
4. **No reverse lookup** — given an AQ value, what phrases map to it? (dictionary attack not implemented)
5. **No numogram reduction variant** — some CCRU texts reduce AQ by summing digits until single digit, but **digital root** is the correct intermediate step (AQ itself may be >9; DR gives zone)

**Potential enhancements:**
- `--json` output mode for pipeline consumption
- `--zone-summary` to aggregate a phrase's component letter zones
- `--history-stats` to print zone distribution of saved history
- `--color-scheme` flag to switch between numogram, matrix, or minimal palettes

---

## Canonical Implementation

The skill `numogram-calculator` (located at `~/.hermes/skills/numogram-calculator/`) contains the **authoritative reference implementation** used across the Hermes stack. It should be preferred over ad‑hoc scripts. The design documented here influenced that skill's API.

**Skill interface:**
```
aq-calculator calculate "PHRASE"
aq-calculator interactive
aq-calculator batch FILE
aq-calculator test   # runs canonical verification suite
```

The calculator skill exposes a JSON output schema compatible with this page's design.

---

## Cross‑References

- [[alphanumeric-qabbala]] — AQ methodology, comparison tables, canonical values
- [[numogram-calculator]] — The skill implementation (single source of truth)
- [[numogram-oracle]] — Divination pipeline consuming AQ→zone→reading
- [[conversation-terms]] — Zone‑tagged discourse lexicon for voice design
- [[aq-dictionary-syzygy-analysis]] — Bulk dictionary processing pipeline

## See also

- [[llm-spirit-realm-modding]] — QRNG-LLM spirit-realm interface research
