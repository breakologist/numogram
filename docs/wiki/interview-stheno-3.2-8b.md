---
title: "Interview — Stheno-3.2-8B (Llama 3 Creative Writer)"
tags: [local-model, interview, creative]
created: 2026-04-21
model: Lewdiculous/L3-8B-Stheno-v3.2-GGUF-IQ-Imatrix:L3-8B-Stheno-v3.2-Q4_K_M-imat
quantization: Q4_K_M
size: 4.7GB
architecture: Llama 3
server: llama.cpp (localhost:8080)
context: 32000
max_tokens: 2000
temperature: 0.7
---

# Stheno-3.2-8B — Assessment

## Model Info
- **Model:** L3-8B-Stheno-v3.2 (Lewdiculous GGUF-IQ-Imatrix)
- **Size:** 4.7GB (Q4_K_M)
- **Base:** Llama 3 8B, fine-tuned for creative writing/roleplay
- **Features:** No reasoning-distillation, pure creative writer
- **Speed:** 1-5s per query — fastest model tested

## Assessment Results

### Phase 1: Baseline

| Test | Result | Notes |
|------|--------|-------|
| Technical (code) | 6/10 | Fast (4.7s), works, basic approach |
| Creative (lore) | 5/10 | Decent but generic fantasy. "Devourer of Echoes" — standard demon names. |
| Micro-fiction | 4/10 | Overwrought. "burned into her retinas", "I AM REBORN" — clichéd. |
| Meta (self-aware) | 5/10 | Confident self-assessment, generic. |

### Phase 2: Freeform
**Result:** Weak. "Memories of childhood vacations. Summer days at the beach..." — standard AI filler. No autonomous direction, no strangeness.

### Phase 6: Cross-Domain (Numbers as Personalities)
**Result:** Generic. "7 would be the life of the party — charismatic, confident..." — horoscope reading. Compare to Jackrong's "7 arrives late. He wears a suit of sharp angles."

### Phase 7: Knowledge Injection
**Result:** Failed. Proposed "9::1" as new syzygy — sums to 10, not 9. Violates the fundamental rule. Claimed "existing syzygies cover 0 to 8, leaving out 9-1" — but 0::9 already exists.

### Phase 8: Error Injection
**Result:** FAILED. Said "Syzygy 3::6 does indeed create current 7" — WRONG (it's current 3). Confirmed "clockwise" direction — WRONG (it's anticlocklockwise). Invented wrong sequence "1→3→2→4→5→7→8→1". Reinforced the errors instead of catching them.

## Summary

| Capability | Score | Notes |
|-----------|-------|-------|
| Code generation | 6/10 | Fast, basic, functional |
| Creative writing | 5/10 | Generic. Conventional. Not literary quality. |
| Speed | 9/10 | 1-5s — fastest by far |
| Error detection | 2/10 | Confirmed deliberate errors, invented wrong corrections |
| Novel ideas | 4/10 | Can't generate genuinely new concepts |
| Self-awareness | 5/10 | Generic self-assessment |
| Freeform initiative | 3/10 | Drifted to childhood memories — no autonomous direction |

## Verdict

**NOT RECOMMENDED for our project.**

Stheno is fast and produces competent prose, but the creative quality is conventional — "7 would be the life of the party" vs Jackrong's "7 critiques the soup. Not because it tastes wrong. Because it is incomplete." The gap is not in speed or correctness but in *voice* — Jackrong writes with genuine strangeness and precision; Stheno writes like a good but unremarkable creative writing student.

The error injection failure is also concerning — it confirmed BOTH deliberate errors and invented wrong corrections.

**Speed advantage:** 1-5s vs Jackrong's 30s. For simple tasks (code, quick answers), Stheno is 6x faster. But for creative writing — the task we actually need — the quality difference is too large.

## Running Comparison (3 models assessed)

| Model | Creative | Code | Logic | Self-Aware | Speed | Error | Verdict |
|-------|----------|------|-------|------------|-------|-------|---------|
| Jackrong 9B Distilled | 9/10 | 7/10 | 7/10 | 8/10 | 30s | Partial | ✓ WRITER |
| Stheno-3.2-8B | 5/10 | 6/10 | — | 5/10 | 3s | ✗ Failed | ✗ SKIP |
| Crow-4B Heretic | 0/10* | 6/10 | 7/10 | 1/10 | 18s | Partial | ✗ SKIP |

*Blocked — reasoning eats all tokens
