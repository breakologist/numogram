---
title: "Model Assessment Summary — Optimal Settings & Council Architecture"
created: 2026-04-21
last_updated: 2026-04-21
status: active
tags: [local-model, council, model-assessment, architecture]
---

# Model Assessment Summary

## Assessment Results (8 models, April 21, 2026)

| Model | Creative | Code | Speed | Thinking | Verdict | Best Role |
|-------|----------|------|-------|----------|---------|-----------|
| Jackrong 9B Distilled | 9/10 | 7/10 | 30s | Moderate (1-6K) | ✓ WRITER | Literary voice |
| Gemma3-12B | 7/10 | 7/10 | 3s | None | ○ BUILDER | Code voice |
| qwen3:14B | 6/10 | 6/10 | 14s | Light (1.5K) | ○ GENERAL | Fallback 14B |
| Gemma-4-E4B-heretic | 5/10 | — | 2s | None | ✗ 4B small | Skip |
| Stheno-3.2-8B | 5/10 | 6/10 | 3s | None | ✗ Generic | Skip |
| MythoMax-L2-13B | 4/10 | — | 8s | None | ✗ Generic | Skip |
| Crow-4B Heretic | 0/10* | 6/10 | 18s | Heavy | ✗ Blocked | Skip |
| qwen3.5:9B | 0/10* | — | 46s | Extreme | ✗ Blocked | Skip |

*Blocked — reasoning consumes all tokens

## Optimal Settings per Model

### Jackrong/Qwen3.5-9B-Claude-Opus-Distilled (Writer)
```
Backend:      llama.cpp (not ollama — GGUF format doesn't work in ollama)
Context:      64000 (can push to ~80K)
Max tokens:   8000 (minimum 5000 for creative)
Temperature:  0.7 (structured), 0.9 (freeform/creative)
Reasoning:    ON — reasoning_content is a second data stream, valuable
System prompt: Dense, uncanny lore voice. Or: "You are thinking out loud."
Key insight:   The reasoning block IS the interesting material. Don't disable it.
Speed:         30s per query. Reasoning overhead is moderate (~1-6K chars).
```

### Gemma3-12B-it (Builder)
```
Backend:      llama.cpp (GGUF from council/models/)
Context:      32000 (sufficient for code generation)
Max tokens:   2000 (no reasoning overhead, content appears immediately)
Temperature:  0.3 (code — precise), 0.7 (general)
Reasoning:    None — no reasoning_content field
System prompt: "You are an expert programmer. Write clean, working code."
Key insight:   Fast (3s), clean code, Google quality. No creative strangeness.
Speed:         2-3s creative, 20s code.
```

### qwen3:14B (General Fallback)
```
Backend:      ollama (GGUF format from ollama, llama-server won't load it)
Context:      Ollama default (varies)
Max tokens:   4000 (reasoning eats ~1500 chars, leaves room for content)
Temperature:  0.7
Reasoning:    ON — moderate overhead (~1500 chars)
System prompt: Varies by task. Use /nothink if available (may not work via ollama).
Key insight:   Decent all-rounder at 14B. Not best at anything, but not worst.
Speed:         14-22s. Reasoning overhead is light but present.
```

### Gemini 2.5 Flash (Oracle — replacing mimo-v2-pro)
```
Backend:      Google AI Studio (free tier)
Context:      1M tokens (massive)
Max tokens:   4000 (sufficient for oracle responses)
Temperature:  0.7 (balanced)
Reasoning:    Varies by task
Rate limit:   1,500 req/day, 1M tok/min
Key insight:   Frontier-quality, free, massive context. Replaces mimo-v2-pro.
Cost:          Free. After mimo-v2-pro trial expires (Apr 22).
```

## Council Architecture

### Current Design
```
┌─────────────────────────────────────────┐
│              INPUT LAYER                │
│  Topic + Context + Current Turn Number  │
└─────────────────────────────────────────┘
                  │
    ┌─────────────┼─────────────┐
    ▼             ▼             ▼
┌────────┐  ┌──────────┐  ┌──────────┐
│ ORACLE │  │ BUILDER  │  │  WRITER  │
│Gemini  │  │Gemma3    │  │Jackrong  │
│2.5 Fl. │  │12B       │  │9B Dist.  │
└────────┘  └──────────┘  └──────────┘
    │             │             │
    └─────────────┼─────────────┘
                  ▼
┌─────────────────────────────────────────┐
│              OUTPUT LAYER               │
│  Single markdown document, voice attr.  │
└─────────────────────────────────────────┘
```

### Model Switching Improvements

**1. Task-Based Routing**
Instead of manually selecting models, route based on task type:
```
Code generation  → Gemma3-12B (fast, clean, Google quality)
Creative writing → Jackrong (literary quality, strangeness)
Structural design → qwen3:14B (14B general purpose)
Complex reasoning → Gemini 2.5 Flash (frontier, 1M context)
Quick answers    → Gemma3-12B (3s response time)
```

**2. Fallback Chain**
If primary model fails or times out:
```
Jackrong (30s) → Gemma3-12B (3s) → Gemini 2.5 Flash (free)
Gemma3-12B (3s) → qwen3:14B (14s) → Gemini 2.5 Flash (free)
```

**3. Council Mode (Tetralogue)**
For tetralogue/roundtable discussions, run voices in sequence:
```
1. Oracle (Gemini) proposes analysis
2. Builder (Gemma3) designs implementation
3. Writer (Jackrong) generates creative response
4. Gamer (any available) evaluates playability
5. Each voice reads previous voice's output before responding
```

**4. Unified API Layer**
All models expose OpenAI-compatible endpoints:
- llama.cpp: `localhost:8080/v1/chat/completions`
- ollama: `localhost:11434/v1/chat/completions`
- Google AI Studio: `generativelanguage.googleapis.com`

A unified router could abstract these into a single endpoint, selecting the backend based on model name.

**5. Context Sharing**
For council conversations, share context between models:
- Writer reads Oracle's analysis before generating creative response
- Builder reads Writer's lore before designing systems
- Each voice's reasoning_content becomes input to the next voice

**6. Thinking-Aware Token Budgeting**
Models with reasoning_content need higher max_tokens:
```
Jackrong:  8000 (reasoning ~6K, content ~2K)
qwen3:14B: 4000 (reasoning ~1.5K, content ~2.5K)
Gemma3:    2000 (no reasoning, all content)
Gemini:    4000 (frontier, moderate thinking)
```

## What Each Model Does Best

| Model | Best At | Avoid |
|-------|---------|-------|
| Jackrong | Creative lore, literary voice, novel ideas | Time-critical tasks (30s), code |
| Gemma3-12B | Fast code, structural design, quick answers | Creative (conventional voice) |
| qwen3:14B | General purpose, code, structural analysis | Creative (verbose), long tasks (60s+) |
| Gemini 2.5 Flash | Complex reasoning, massive context, frontier quality | Privacy-sensitive (cloud-based) |

## Key Insight: Thinking Overhead as Quality Gate

The most important finding from the assessment: **thinking overhead is the new quality gate for creative tasks.**

- Models with moderate reasoning (Jackrong, ~6K chars) can produce both reasoning AND creative content
- Models with heavy reasoning (Crow-4B, qwen3.5:9B) consume all tokens with thinking — content is empty
- Models with no reasoning (Gemma3, Stheno, MythoMax) produce content immediately but lack depth

The sweet spot: moderate reasoning overhead that leaves room for both thinking AND output. Jackrong at 9B hits this balance perfectly. qwen3:14B is borderline (light reasoning, but verbose content). qwen3.5:9B is blocked (extreme reasoning).

## Recommendations

1. **Settle council as:** Jackrong=Writer, Gemma3=Builder, Gemini=Oracle
2. **qwen3:14B as general fallback** — useful for non-creative tasks
3. **Skip all 4B models** — reasoning-distilled models at 4B can't produce creative content
4. **Skip qwen3.5:9B** — thinking overhead is insurmountable via ollama
5. **Set up Gemini 2.5 Flash** before mimo-v2-pro trial expires (Apr 22)
6. **Build unified API router** for seamless model switching
7. **Use reasoning_content as creative material** — the thinking process IS the content for Jackrong

## Related

- [[interview-jackrong-qwen3.5-9b-claude-opus-distilled]] — Full Jackrong assessment
- [[interview-gemma3-12b]] — Full Gemma3 assessment
- [[dialogue-hermes-jackrong-v1]] — Two-model dialogue results
- [[local-model-survey]] — Hardware, VRAM, model inventory
- `model-assessment-protocol` — 9-phase assessment skill
