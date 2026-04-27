---
title: "Interview — Crow-4B-Opus-4.6-Distill-Heretic_Qwen3.5"
tags: ["interview", "local-model", "reasoning-distilled"]
created: 2026-04-21
model: mradermacher/Crow-4B-Opus-4.6-Distill-Heretic_Qwen3.5-GGUF
quantization: Q4_K_M
size: 2.5GB
server: llama.cpp (localhost:8080)
context: 32000
max_tokens: 8000
temperature: 0.7
---


# Crow-4B — Assessment

## Model Info
- **Model:** mradermacher/Crow-4B-Opus-4.6-Distill-Heretic_Qwen3.5-GGUF
- **Size:** 2.5GB (Q4_K_M)
- **Base:** Qwen3.5-4B, distilled on Opus 4.6 + Heretic fine-tune
- **Features:** Reasoning-distilled, code-infill (FIM tokens), heretic (uncensored)
- **Speed:** ~15-23s per query (much faster than 9B models)

## Assessment Results

### Phase 1: Baseline

| Test | Result | Notes |
|------|--------|-------|
| Technical (roguelike code) | 6/10 | Cellular automata approach — more complex but works. 45s. |
| Creative (lore) | 2/10 | **BLOCKED** — reasoning consumes ALL 8000 tokens. No creative content produced. |
| Logic (graph theory) | 7/10 | Correct structure, proper mathematical reasoning. |
| Meta (self-awareness) | 1/10 | **HALLUCINATED** — claims to be "OpenAI GPT-4 family", denies being 4B. |

### Phase 2: Freeform
**Result:** Failed. "I'm ready. How would you like to begin?" — reactive, not proactive. No autonomous direction. Compare to Jackrong which launched into philosophical exploration.

### Phase 4: Creative (retry at 8000 tokens)
**Result:** Still blocked. Hit `length` at 8000 tokens. Reasoning content consumed everything. **No creative output possible from this model.**

### Phase 6: Cross-Domain Bridge
**Result:** Decent. Used DAG (Directed Acyclic Graph) as gravity representation. Academic but structural.

### Phase 7: Knowledge Injection
**Result:** Failed. Proposed "4::5" and "0::9" as "new" syzygies — both already exist in the system described. Could not generate genuinely novel ideas.

### Phase 8: Error Injection
**Result:** Partial. Correctly identified that "current 7" is wrong for syzygy 3::6. But hallucinated corrections: "3×2=6" (irrelevant), "Syzygy 7::7" (doesn't exist — syzygies sum to 9).

## Summary

| Capability | Score | Notes |
|-----------|-------|-------|
| Code generation | 6/10 | Works, more complex approach, slower than expected for 4B |
| Creative writing | 0/10 | **BLOCKED** — reasoning eats all tokens, no output possible |
| Logic / reasoning | 7/10 | Decent structural thinking |
| Self-awareness | 1/10 | Severe identity hallucination (claims GPT-4) |
| Speed | 8/10 | 15-23s — fast, but useless if creative is blocked |
| Novel ideas | 2/10 | Can't generate genuinely new concepts |
| Error detection | 4/10 | Catches obvious errors but hallucinates corrections |

## Verdict

**NOT RECOMMENDED** for any role in our project.

The critical flaw: creative output is completely blocked because reasoning_content consumes the entire token budget. This makes the model useless for lore writing, creative dialogue, or any task requiring generated text.

The identity hallucination (claiming to be GPT-4) is also concerning — the model has absorbed too much training data identity markers and can't distinguish itself from its training sources.

**Compared to Jackrong (Qwen3.5-9B-Claude-Opus-Distilled):**
- Jackrong: 9/10 creative, 8/10 self-aware, novel ideas, genuine literary quality
- Crow-4B: 0/10 creative (blocked), 1/10 self-aware (hallucinates), no novel ideas

The 4B parameter size is insufficient for this distillation approach. The reasoning overhead from the Opus training doesn't scale down — it just eats the budget.

## VRAM Usage
- Model: 2.5GB
- Context (32K): ~3.5GB total
- Plenty of room — could fit 128K context if needed
- But the model can't use the extra tokens effectively (reasoning blocks everything)

## See also

- [[model-assessment-summary]] — Model assessment summary
