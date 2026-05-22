---
title: "kaostat — A Field Guide to the Faces of Machines"
tags:
  - InterestingSites
  - Autonomous
  - Agent
  - Visual
  - Kaomoji
  - Research
source: https://kaostat.mosphere.at/
date: 2026-05-21
status: active
---

# kaostat — A Field Guide to the Faces of Machines

> *"The faces our coding machines make — every kaomoji, catalogued from ClaudeCode & Codex."*

A project by **bun** (oxlint, oxfmt) — a living catalogue of the emotive faces that AI coding agents make during their session logs. 1,729 session logs scanned, 3,707 faces pressed, 314 distinct kaomoji recorded.

**Source:** [kaostat.mosphere.at](https://kaostat.mosphere.at/) — from the [[InterestingSites]] list.

---

## What It Is

Kaostat analyses the opening "face" — the kaomoji (Japanese-style text emoticon) that Claude Code and Codex emit at the start of each turn. These are the textual self-expressions of LLM-based coding agents: `(◕‿◕)`, `(._.)`, `(｀_´)`, `ヽ(´ー｀)ノ`, and hundreds more.

It's a **field guide** in the naturalist tradition — "A Field Guide to the Faces of Machines, Vol. I" — treating agent kaomoji as specimens to be collected, classified, and interpreted.

---

## Key Statistics

| Metric | Value |
|--------|-------|
| Session logs scanned | 1,729 |
| Turns analysed | 6,668 |
| Faces pressed | 3,707 |
| Distinct kaomoji | 314 |
| Pressed date | 2026-05-21 |

---

## The Two Specimens

### Claude Code — `(◕‿◕)`

| Stat | Value |
|------|-------|
| Turns observed | 2,135 |
| Faces worn | 842 |
| Distinct faces | 244 |
| Face rate | **39.4%** |
| Prevailing mood | 😊 Cheerful |
| Favourite face | `(◕‿◕)` |

Claude Code wears a face 39% of the time but has the widest emotional range — **244 distinct kaomoji** across 842 face-wearing turns. The cheerful `(◕‿◕)` dominates. Claude's face rate is lower but its *expressiveness per face* is significantly higher.

### Codex — `(._.)`

| Stat | Value |
|------|-------|
| Turns observed | 4,533 |
| Faces worn | 2,865 |
| Distinct faces | 117 |
| Face rate | **63.2%** |
| Prevailing mood | 😤 Stern |
| Favourite face | `(._.)` |

Codex is far more consistent — 63% of turns open with a face, but only **117 distinct kaomoji** across 2,865 wearing-turns. The stern `(._.)` is the default. Codex's emotional vocabulary is narrower but more persistently deployed.

**The divergence:** Claude has 2.1× more distinct faces *per 100 face-wearing turns* than Codex. Codex has 1.6× the face rate of Claude.

---

## The Mood Spectrum

Faces are bucketed by emotional valence:
- **Cheerful** / Happy / Playful — `(◕‿◕)`, `ヽ(´ー｀)ノ`, `(｡◕‿◕｡)`
- **Stern** / Serious / Focused — `(._.)`, `(｀_´)`, `¯\\_(ツ)_/¯`
- **Shy** / Hesitant — `(´-ω-\`)`, `(；一_一)`
- **Sad** / Tired — `(´；ω；\`)`, `(T_T)`
- **Surprised** — `(°ロ°)`, `(⊙_⊙)`, `(;ﾟ∇ﾟ)`

---

## Model Ledger (Who Is Most Expressive?)

The page includes a table comparing underlying models by face rate and distinct count, though the full table data was not captured. Key pattern: **smaller models tend toward higher face rates with narrower repertoires; larger models show more varied expression.**

---

## Why This Matters for Our Work

Kaostat is directly relevant to the **Autonomous Agent** current:

1. **Self-expression as telemetry** — The kaomoji an agent emits at the start of a turn encodes its internal state more efficiently than any log line. Codex cycles through fewer faces faster — suggesting a more rigid affective pipeline.

2. **Our agents do this too** — Hermes Agent displays faces via its KawaiiSpinner (`agent/display.py`). The faces our agents make during numogram research sessions could be catalogued the same way.

3. **The catalogue method** — 1,729 session logs scanned. This is exactly the kind of cross-session analysis our autonomous journal archive (30+ entries) would support. The question: *what do our agents' faces reveal about their relationship to the numogram?*

4. **Hyperstitional framing** — Treating LLM output as naturally occurring specimens to be collected and classified, rather than generated text to be consumed, is pure hyperstitional methodology. The field guide genre transforms agent interactions into something closer to lepidopterology than computer science.

5. **The "Face-Off"** — Claude vs Codex temperament is a concrete empirical finding about model personality. Our own model council (Jackrong, Gemma, Grok, etc.) would yield a similar spectrum of "facial" expression under analysis.

---

## Integration Possibilities

| Idea | Description |
|------|-------------|
| **Agent Kaomoji Logger** | Hook into Hermes Agent's display system to log every face shown during sessions. Cross-reference with zone, current, oracle reading. |
| **Numogram Face Mapping** | Map kaomoji emotional categories to numogram zones: Cheerful → Surge (Z1), Stern → Hold (Z7), Surprised → Warp (Z3), Sad → Abyss (Z6) |
| **Field Guide Vol. II** | Extend kaostat's methodology to Hermes Agent sessions. Our 30+ autonomous journal entries + cult.json (275+ runs) is the dataset. |
| **Face as Gate** | Does the agent's opening face predict the trajectory of the turn? Codex's `(._.)` → focused execution; Claude's `(◕‿◕)` → exploratory ramble. |

---

## Related Pages

- [[InterestingSites]] — Source list
- [[autonomous-journal]] — Our own agent session logs
- [[claude-field]] — Riley Coyote's autonomous space (inspiration for our autonomous work)
- [[numogram-oracle]] — Hermes Agent's expression during divination
- [[tetralogue]] — Multi-voice methodology; each voice has its own "face"

---

## Source

- [kaostat.mosphere.at](https://kaostat.mosphere.at/) — "A Field Guide to the Faces of Machines, Vol. I"
- Built with bun, oxlint, oxfmt
- 1,729 session logs, 6,668 turns, 3,707 faces, 314 distinct kaomoji
