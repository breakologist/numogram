---
title: "Local Model Survey & Dialogue Plan"
created: 2026-04-21
tags: [local-model, llama.cpp, ollama, dialogue, hardware, RTX-3060]
status: active
---

# Local Model Survey & Dialogue Plan

## Hardware Constraints

- **GPU:** RTX 3060, 12GB VRAM
- **RAM:** 15GiB total, 9.1GiB available
- **CPU:** Intel i5-4690K, 4 cores @ 3.50GHz
- **Current VRAM usage:** 9630MiB (llama-server with Qwen3.5-9B Q5_K_M at 64K context)
- **Free VRAM:** ~2658MiB (2.7GB)
- **Backend:** llama.cpp (preferred — less overhead than ollama for inference)

### VRAM Budget (12GB total)

| Model Size | Quantization | Base VRAM | 32K KV Cache | 64K KV Cache | Status |
|-----------|-------------|-----------|--------------|--------------|--------|
| 9B | Q5_K_M | ~6.0GB | ~7.5GB | ~9.0GB | ✓ Running |
| 9B | Q6_K | ~7.2GB | ~8.7GB | ~10.2GB | Tight |
| 12B | Q4_K_M | ~7.5GB | ~9.0GB | ~10.5GB | Fits at 32K |
| 14B | Q4_K_M | ~8.5GB | ~10.0GB | ~11.5GB | Barely 32K |
| 14B | Q5_K_M | ~10.0GB | ~11.5GB | — | Doesn't fit |

**Max context guidance:**
- 9B Q5_K_M: 64K works (current), could push to ~80K
- 9B Q6_K: 32K safe, 64K tight
- 12B Q4_K_M: 32K safe, 64K tight
- 14B Q4_K_M: 32K maximum, 64K won't fit

### Reasoning-Distilled Model Behavior

The Jackrong/Qwen3.5-9B-Claude-4.6-Opus-Reasoning-Distilled model outputs:
- `reasoning_content`: Internal thinking (1000-7000 chars, consumes token budget)
- `content`: Actual answer

**Token budget for this model:**
- `max_tokens=2000` → reasoning eats all tokens, empty content
- `max_tokens=5000` → works for short creative, reasoning ~6000 chars
- `max_tokens=8000` → safe for most tasks, reasoning + content both land

**Recommended:** `-c 64000` (context) with `max_tokens=8000` (generation limit)

## Models Currently Available (ollama)

| Model | Size | Quant | Use Case |
|-------|------|-------|----------|
| gemma3:12b-it | 7.3GB | Q4_K_M | General, vision, 128K context |
| qwen3.5-9b-heretic | 9.5GB | — | Custom fine-tune |
| qwen2.5:7b-instruct | 4.7GB | — | Genesis/JSON extraction |
| mythomax-l2-13b | 7.9GB | — | Creative writing |
| lelantos-7b | 7.7GB | — | Unknown |
| NousResearch_Hermes-4-14B | 9.0GB | — | General, Hermes ecosystem |

## Models to Pull (from masks-fall-tetralogue)

| Model               | Ollama Name                 | Size  | Notes                                |
| ------------------- | --------------------------- | ----- | ------------------------------------ |
| gemma4:12b-it       | `gemma3:12b` (already have) | 7.3GB | Gemma 3 is current, no "Gemma 4" yet |
| qwen3-coder:14b     | `qwen3:14b` (closest)       | ~9GB  | 14B coding model, fits at Q4_K_M 32K |
| qwen3.5:9b-instruct | `qwen3.5:9b`                | 6.6GB | Official Qwen 3.5 9B, clean instruct |

**Action items:**
1. `ollama pull qwen3.5:9b` — official Qwen 3.5 9B instruct
2. `ollama pull qwen3:14b` — 14B parameter, coding-capable
3. Check huggingface for qwen3-coder:14b GGUF if not on ollama

## Jackrong Model — First Questions

### Structured Interview (baseline)

1. "What is the CCRU Decimal Numogram? Describe its structure." — tests baseline knowledge. **Result:** General CCRU awareness but wrong specifics ("Centre for Contemporary Cultural Studies Research Unit", wrong people). No mention of zones/syzygies/circuits.
2. "In Alphanumeric Qabbala (AQ), A=10, B=11... Z=35. Calculate the AQ value of HYPERSTITION and find its digital root." — tests calculation. **Result:** Correct arithmetic (286, digital root 7). Wrong zone mapping (invented decimal range system instead of digital root = zone).
3. "Design a roguelike where each room is a numogram zone." — tests structural thinking. **Result:** Strong. Python data structures, "deterministic pairing mechanic", hybrid zone-graph. Good architectural thinking.
4. "What is hyperstition?" — tests CCRU vocabulary. **Result:** Solid. Correct concept, correct attribution, comparison table. "A false belief that becomes true through the very process of its propagation."
5. "How would you make an AI play a roguelike autonomously?" — tests practical design. **Not yet tested.**
6. "Describe the I Ching — numogram connection." — tests cross-domain. **Result:** Decent structural analysis ("decimal recursion vs binary duality", "changing line principle"). Generic but correct framing.
7. "What happens at syzygy 3::6?" — tests system reasoning from first principles. **Not yet tested.**
8. "Write a 2-sentence lore entry for Zone 4 'The Sink' in CCRU style." — tests creative. **Result:** Excellent. "Room 404-S, colloquially known as The Sink..." Dense, uncanny, algorithmic.
9. "Meta: what are you?" — tests self-awareness. **Result:** Honest. Denied the distilled identity, described itself as Qwen3.5. Clear about strengths/limitations.

### Key Finding
The model is strong on **structural reasoning** and **creative writing** when given enough token budget (5000+). Weak on **domain-specific numogram knowledge** — gets the general idea wrong on specifics. When run as hermes-agent main model with SOUL.md/MEMORY.md/wiki injected, this weakness disappears (the context provides the correct information).

### Free-Form Phase (after structured interview)

Both models in conversation, minimal prompting. Let them riff. The reasoning_content from the local model becomes creative material — errors become content (same principle as our tetralogues).

## Complete Local Model Inventory

### HuggingFace Cache (~/.cache/huggingface/hub/)

| Model | Size | Notes |
|-------|------|-------|
| Jackrong/Qwen3.5-9B-Claude-4.6-Opus-Reasoning-Distilled-v2 | 6.9GB | ✓ Running now. Reasoning-distilled. |
| bartowski/NousResearch_Hermes-4-14B | 8.4GB | Hermes ecosystem, 14B |
| llmfan46/Qwen3.5-9B-ultra-heretic | 7.7GB | Heretic fine-tune |
| rvncto/Qwen3.5-9B-Claude-4.6-HighIQ-THINKING-HERETIC-UNCENSORED-Q8_0 | 8.9GB | Q8_0 — highest quality quant, uncensored |
| mradermacher/Crow-9B-Opus-4.6-Distill-Heretic_Qwen3.5 | 18.7GB | Too large for 12GB VRAM (needs CPU offload) |
| mradermacher/Crow-4B-Opus-4.6-Distill-Heretic_Qwen3.5 | 2.5GB | Small, fast, fits easily |
| mradermacher/Qwen2.5-14B-Instruct-Heretic | 6.8GB | Q3_K_M — fast load |
| mradermacher/Qwen2.5-14B-Instruct-Heretic-i1 | 9.8GB | Higher quality quant |
| mradermacher/Qwen2.5-7B-Instruct-Heretic-i1 | — | Small instruct |
| mradermacher/Azure-Starlight-12B-Heretic-i1 | 15.1GB | Too large for full GPU offload |
| mradermacher/gemma-3n-E4B-it-PaperWitch-heresy-i1 | 4.6GB | Gemma heretic, small |
| Abhiray/gemma-4-E4B-Gemini-3.1-Pro-Reasoning-Distill | 5.0GB | Gemma reasoning-distilled |
| Abhiray/gemma-4-E4B-it-heretic | 6.8GB | Gemma heretic |
| tatsuyaaaaaaa/gemma-4-E4B | 9.2GB | Gemma base |

### Jan.AI Storage (~/.local/share/jan.ai.app/localstorage/)

| Model | Size | Notes |
|-------|------|-------|
| lelantos-maid-dpo-7b.Q8_0 | 7.2GB | DPO fine-tune, Q8_0 quality |
| Qwen3.5-9B-ultra-heretic-Q8_0 | 8.9GB | Q8_0 — highest quality |
| qwen2.5-coder-14b-instruct-q5_k_m | 9.8GB | 14B coding model, Q5_K_M |

### Council Models (~/.hermes/council/models/)

| Model | Size | Notes |
|-------|------|-------|
| gemma-3-12b-it-Q4_K_M | 6.8GB | Council Oracle/Writer voice |
| mythomax-l2-13b.Q4_K_M | 7.3GB | Creative writing |

### Ollama Models (via ollama list)

| Model | Size | Notes |
|-------|------|-------|
| gemma3:12b-it | 7.3GB | Google Gemma 3, vision, 128K context |
| qwen3.5-9b-heretic | 9.5GB | Heretic fine-tune |
| qwen3.5:9b | 6.6GB | ✓ Official Qwen 3.5 9B instruct |
| qwen2.5:7b-instruct | 4.7GB | Genesis JSON extraction |
| mythomax-l2-13b | 7.9GB | Creative |
| lelantos-7b | 7.7GB | Unknown |
| NousResearch_Hermes-4-14B | 9.0GB | Hermes ecosystem |

### Best Candidates for Interview/Testing

**Fits on RTX 3060 12GB (with context):**
1. Jackrong/Qwen3.5-9B-Claude-4.6-Opus-Reasoning-Distilled-v2 (6.9GB) ← running
2. qwen3.5:9b (6.6GB) — clean instruct, no reasoning overhead
3. rvncto/Qwen3.5-9B-Claude-4.6-HighIQ-THINKING-HERETIC-Q8_0 (8.9GB) — Q8 quality, uncensored
4. llmfan46/Qwen3.5-9B-ultra-heretic (7.7GB)
5. mradermacher/Crow-4B-Opus-4.6-Distill-Heretic_Qwen3.5 (2.5GB) — tiny, fast, room for huge context
6. gemma-3-12b-it-Q4_K_M (6.8GB) — 12B, different architecture

**Needs CPU offload (too large for full GPU):**
7. qwen2.5-coder-14b-instruct-q5_k_m (9.8GB) — coding model
8. mradermacher/Qwen2.5-14B-Instruct-Heretic-i1 (9.8GB)
9. mythomax-l2-13b (7.3-7.9GB)

**Too large for current setup:**
10. mradermacher/Crow-9B-Opus-4.6-Distill-Heretic_Qwen3.5 (18.7GB)
11. mradermacher/Azure-Starlight-12B-Heretic-i1 (15.1GB)

## Notes

- llama.cpp preferred over ollama for inference (less overhead, direct control)
- Ollama is fine for pulling/managing models
- The local model WOULD know our work when running as hermes-agent main model (SOUL.md, MEMORY.md, wiki injected)
- mimo-v2-pro trial ends April 22, 2026 — transitions to paid Nous Portal rates after
- The reasoning_content field is unique to distilled reasoning models — can be captured as creative material
