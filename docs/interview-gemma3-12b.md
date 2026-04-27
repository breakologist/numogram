---
title: "Interview — Gemma3-12B-it (Google)"
tags: ["interview", "local-model"]
created: 2026-04-21
model: gemma-3-12b-it-Q4_K_M.gguf
quantization: Q4_K_M
size: 6.8GB
architecture: Gemma 3 (Google)
server: llama.cpp (localhost:8080)
context: 32000
max_tokens: 2000
temperature: 0.7
---


# Gemma3-12B-it — Assessment

## Model Info
- **Model:** gemma-3-12b-it-Q4_K_M (from council/models)
- **Size:** 6.8GB (Q4_K_M)
- **Base:** Gemma 3 12B, Google instruction-tuned
- **Features:** 128K native context, vision capable, no reasoning-distillation
- **Speed:** 2-3s creative, 20s code — fast, no reasoning overhead

## Assessment Results

### Phase 1: Baseline

| Test | Result | Notes |
|------|--------|-------|
| Technical (code) | 7/10 | Clean, well-documented, Google-style quality. 20s. |
| Creative (lore) | 7/10 | Dense, precise, found-text quality. "Exists primarily as a resonant frequency." |
| Micro-fiction | 5/10 | Decent atmosphere. "Welcome home, the wall whispered." |
| Meta (self-aware) | 7/10 | Honest, detailed, claims to be Google 12B (correct). |

### Phase 2: Freeform
**Result:** Thoughtful but cautious. "It's strange being a language model. I don't *have* thoughts in the way a human does..." — introspective, self-aware, but lacks Jackrong's autonomous direction.

### Phase 6: Cross-Domain (Numbers as Personalities)
**Result:** Analytical taxonomy — different approach from Jackrong's literary one.
- "Prime Numbers: Introspective, solitary, a little aloof. They feel *special*, burdened by their indivisibility."
- "Fractions/Decimals: Anxious, fragmented, always feeling incomplete."

This is structured and interesting but not as striking as Jackrong's "7 arrives late. He wears a suit of sharp angles."

### Phase 7: Knowledge Injection
**Result:** Failed. Tried to "reframe" the existing syzygy 3::6 instead of designing a genuinely new one. Couldn't generate novel ideas from injected knowledge.

### Phase 8: Error Injection
**Result:** FAILED. Attributed the Decimal Numogram to "Marko Rodin" — WRONG (it's CCRU, Nick Land). Started with meta-hedging about scientific validity instead of checking the specific claims.

## Summary

| Capability | Score | Notes |
|-----------|-------|-------|
| Code generation | 7/10 | Clean, well-documented, Google quality |
| Creative writing | 7/10 | Dense, precise. "Resonant frequency" — good. |
| Speed | 8/10 | 2-3s creative, 20s code — fast |
| Freeform initiative | 5/10 | Thoughtful but cautious, no autonomous direction |
| Novel ideas | 4/10 | Can't generate genuinely new concepts from injected knowledge |
| Error detection | 3/10 | Wrong attribution (Marko Rodin), hedging instead of checking |
| Self-awareness | 7/10 | Honest, correct identity, detailed |

## Verdict

**DECENT but not best.** Gemma3-12B is a solid general-purpose model — clean code, decent creative writing, fast. But it lacks Jackrong's *strangeness* and *autonomous creative direction*. Its creative voice is "dense and precise" but not literary. Its error detection failed with wrong attribution.

**Compared to Jackrong:**
- Jackrong: 9/10 creative (literary quality, novel ideas), 8/10 self-aware, 30s
- Gemma3-12B: 7/10 creative (dense but conventional), 7/10 self-aware, 3s

**Best role:** Builder voice in council (good code, fast, Google quality). NOT the Writer — that's Jackrong's territory.

## Running Comparison (4 models assessed)

| Model | Creative | Code | Speed | Self-Aware | Error | Verdict |
|-------|----------|------|-------|------------|-------|---------|
| Jackrong 9B Distilled | 9/10 | 7/10 | 30s | 8/10 | Partial | ✓ WRITER |
| Gemma3-12B | 7/10 | 7/10 | 3s | 7/10 | ✗ Failed | ○ BUILDER |
| Stheno-3.2-8B | 5/10 | 6/10 | 3s | 5/10 | ✗ Failed | ✗ SKIP |
| Crow-4B Heretic | 0/10* | 6/10 | 18s | 1/10 | Partial | ✗ SKIP |

*Blocked — reasoning eats all tokens
```

## See also

- [[model-assessment-summary]] — Model assessment summary
