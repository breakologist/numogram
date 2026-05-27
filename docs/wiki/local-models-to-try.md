# Local Models to Try

Shortlist of Qwen3.5-derived GGUF quants for local testing on RTX 3060 (12GB VRAM). All are 9B-class with various distillation sources (DeepSeek V4 Flash, Claude Opus, custom finetunes).

## Current Stable Model

| Model | Status | Notes |
|-------|--------|-------|
| `qwopus3.5:9b-q6k` (via llama-server :8081) | Tested | Jackrong Qwopus3.5-9B-Coder-MTP, Q6_K. Needs rebuilt llama-server (b9351+). |
| `Qwen3.5-9B-DeepSeek-V4-Flash-MTP-Q5_K_M` (via llama-server :8081) | Tested | Jackrong DeepSeek Flash distill, Q5_K_M, ~6.2GB. Same MTP requirement. |
| `armand0e-Qwen3.5-9B-Opus-Agent:Q4_K_M` (via ollama blob or llama-server) | Tested | armand0e Opus Agent distill. Needs llama-server — ollama 0.24 too old. |

## Test Results — Qwopus3.5-9B-Coder-MTP (Q6_K, 7.6GB)

Tested 2026-05-26 on llama-server port 8081. Structured assessment across 5 dimensions:

| Dimension | Score | Notes |
|-----------|-------|-------|
| **Code generation** | 9/10 | Clean dict-based syzygy, correct AQ calculation + digital root. Ran first time. |
| **Creative writing** | 8/10 | Genuinely good found-text quality. Concrete, sensory, effective short sentences. Gate descriptions had actual strangeness ("numbers on the lintel weep", "the reflection blinks independently"). |
| **Logic / reasoning** | 7/10 | Solved mislabeled boxes cleanly. Missed numogram domain-specific error (5::5 isn't a syzygy) but caught all logical structure flaws. |
| **System design** | 7/10 | Competent 4-module layered architecture. Correctly separates semantic analysis from serialization. |
| **Creative constraint** | 4/10 | Needs 5000+ max_tokens because reasoning block eats budget. Syllable counts off on haiku. Short-constraint creative fights the thinking layer. |

### Key Strengths
- **Reasoning + code output is genuinely useful.** 3815-4582 char reasoning blocks are structured decomposition, not boilerplate.
- **Creative voice above local-model average.** Opus distillation lineage shows through.
- **Good abstraction sense in system design.** Correctly separates concerns.

### Key Weaknesses
- **Reasoning tax is real.** Every task burns 1500-4500 chars of reasoning before producing content. Counterproductive for short-form creative (haiku, one-liners).
- **Domain knowledge gaps.** Doesn't know Numogram-specific terms without context injection (expected).
- **MTP architecture requires llama-server.** Can't use through ollama. Run on port 8081 with:
  ```bash
  ~/llama.cpp/build/bin/llama-server -m /path/to/Qwopus3.5-9B-Coder-MTP-Q6_K.gguf -ngl 99 -c 8192 --port 8081
  ```

### Recommendation
Use as a **code + reasoning** model for local work. Strong for Python scripts, algorithm design, constrained generation with grammar. The reasoning layer makes it slower for simple/creative tasks but the output quality is higher than base Qwen3.5:9b.

### Benchmarks (Q6_K on RTX 3060 12GB)
- **Prompt processing:** 103.87 tok/s (9.63 ms/tok)
- **Token generation:** 38.22 tok/s (26.17 ms/tok)
- **Total:** 1213 tokens in 31.3s (28-token prompt, 1185-token response)

## Models to Try

### Jackrong/Qwen3.5-9B-DeepSeek-V4-Flash-MTP-GGUF

**HF:** https://huggingface.co/Jackrong/Qwen3.5-9B-DeepSeek-V4-Flash-MTP-GGUF

Distilled from DeepSeek V4 Flash (MTP = multi-token prediction variant). Likely strong on reasoning and code. The DeepSeek lineage tends toward structured analytical output — could slot into the Oracle/Council role for numogram arithmetic tasks.

Try: AQ calculations, syzygy chain analysis, constrained generation with `outlines` grammar.

### Test Results — DeepSeek V4 Flash Distill (Q5_K_M, ~6.2GB)

Tested 2026-05-26 on llama-server :8081.

| Dimension | Score | Notes |
|-----------|-------|-------|
| **Code generation** | 9/10 | Correct dict-based syzygy + AQ digital root. Clean code. |
| **Creative writing** | 7/10 | Abstract/metaphysical register. Good lines ("the ticking is not mechanical") but less concrete sensory detail than Qwopus. |
| **Logic / reasoning** | 7/10 | Solved mislabeled boxes correctly. Heavy reasoning tax (10698 chars for 312 chars answer). |
| **System design** | 7/10 | 5-component design with AST pipeline, Instrument Resolver. More detailed than Qwopus. |

### Key Observations
- **Heavy reasoning tax** — 10561 chars on creative, 10698 on logic. Needs 15K+ max_tokens.
- **Abstract register** — metaphysical pronouncements over concrete sensory detail. More Z6 (Warp) than Z3 (Rise).
- **Code quality similar to Qwopus** — both produce correct implementations from same family.
- **Faster than Qwopus** — 47.60 tok/s vs 38.22 tok/s (24% faster), likely due to smaller Q5_K_M quant.

### armand0e/Qwen3.5-9B-Opus-Agent-GGUF

**HF:** https://huggingface.co/armand0e/Qwen3.5-9B-Opus-Agent-GGUF

Distilled from Claude Opus via the Opus Agent finetuning pipeline. Likely the strongest candidate for **creative/literary voice** — the Jackrong models (which were distilled from Claude 4.6 Opus) already showed notably better literary strangeness than generic local models. This is a different training lineage (Opus Agent), could offer a different creative texture.

Try: lore writing, tetralogue participation, oracle-mode prose.

### Test Results — Armand0e Opus Agent (Q4_K_M, ~5.3GB)

Tested 2026-05-26 on llama-server :8081.

| Dimension | Score | Notes |
|-----------|-------|-------|
| **Code generation** | 3/10 | Failed: used `i % 7` instead of syzygy pairs summing to 9. Used ASCII sum instead of AQ cipher. Did not understand domain-specific terms even with context. |
| **Creative writing** | 6/10 | Decent found-text quality but more generic than both Jackrong models. "Black hole of absolute silence" is a cliché. |
| **Reasoning tax** | ❌ Extreme | 29360 chars of reasoning consumed 15000 token budget with zero content output. Needed 32000 max_tokens to see any output, and even the reasoning at temp=0.1 was 1870 chars. |

### Key Observations
- **Highest reasoning tax of all three** — the Opus Agent finetuning encourages extremely verbose reasoning that overwhelms output generation on a 9B model.
- **Weaker domain comprehension** than Jackrong models — didn't understand syzygy or AQ concepts even with explicit instructions.
- **Creative similar to DeepSeek Flash** in abstraction level, but less concrete than Qwopus.
- **Needs max_tokens >= 32000** for any measurable output. Not practical for interactive use.
- **Fastest inference of the three** — 265 tok/s prompt processing (small Q4_K_M quant at 5.3GB). Speed doesn't compensate for quality.

### Creative Writing Comparison (Gt-6)

| Model | Entry | Character |
|-------|-------|-----------|
| **Qwopus** | "A hexagonal aperture sealed in wet concrete. It hums at sixty cycles per second, a frequency that loosens the teeth in your jaw. The numbers on the lintel weep when you step across the threshold." | Concrete, sensory, physical — Z3 (Rise) |
| **DeepSeek Flash** | "Gt-6 does not rotate; it absorbs the rotation. The air tastes of copper and old paper. The ticking is not mechanical." | Abstract, metaphysical — Z6 (Warp) |
| **Armand0e** | "Gate Six manifests at the intersection of silent frequencies. Coordinates resolve into static noise that tastes like copper. The observer is not permitted to exit." | Generic uncanny — lowest density |

### Jackrong/Qwopus3.5-9B-Coder-MTP-GGUF

**HF:** https://huggingface.co/Jackrong/Qwopus3.5-9B-Coder-MTP-GGUF

Already loaded previously as Q6_K via Ollama — tested ~7.6 GB with vision encoder. Jackrong's Qwopus series blends Qwen3.5 base with Opus-style creative voice, and MTP gives it a code-favoured skew. Previously loaded against the Q6_K variant; has been flagged for full structured testing but hasn't gotten one yet. The Q5_K_M variant may be a better fit for 12GB VRAM with 32K+ context.

Try: code generation, system design, roguelike procedural generation scripts.

## VRAM Budget (RTX 3060 12GB)

| Quant | Base VRAM | 32K Context | 64K Context | Fit? |
|-------|-----------|-------------|-------------|------|
| Q5_K_M | ~6.0 GB | ~7.5 GB | ~9.0 GB | ✅ Safe |
| Q6_K | ~7.2 GB | ~8.7 GB | ~10.2 GB | ✅ Tight |
| Q8_0 | ~9.5 GB | ~11.0 GB | — | ❌ No headroom |

For most use cases: **Q5_K_M** offers the best quality/VRAM trade-off for 9B models on 12GB. Q6_K works if you don't need long context.

## Three-Model Comparison (2026-05-26)

### Overall Ranking

1. **🥇 Qwopus3.5-9B-Coder-MTP (Q6_K)** — Best balance across all dimensions. Strongest creative voice, best code, manageable reasoning tax. ★ Best for lore writing + code generation.
2. **🥈 DeepSeek V4 Flash Distill (Q5_K_M)** — Similar code quality to Qwopus, more abstract creative register, heavier reasoning tax. ★ Best for structured analysis + system design.
3. **🥉 Armand0e Opus Agent (Q4_K_M)** — Higher reasoning tax with weaker output. Domain comprehension gaps. Use only with very high token budgets. ★ Not recommended for interactive use.

### Key Takeaways

- All three are Qwen3.5-9B reasoning-distilled models from different source models (Qwopus/Claude Opus, DeepSeek V4 Flash, Claude Opus Agent).
- All three **require llama-server b9351+** — none work on ollama 0.24.0 due to Qwen3.5-next architecture.
- The **Jackrong models** (Qwopus, DeepSeek Flash) are consistently stronger than the armand0e Opus Agent across all dimensions tested.
- **Reasoning tax varies significantly**: Qwopus (~4K chars) < DeepSeek Flash (~10K chars) < Armand0e (~29K chars) for comparable tasks.
- For most local work, **Qwopus is the best first choice** — best creative/concrete ratio, lowest reasoning overhead, correct code first time.

When testing, use the [[local-model-testing]] skill protocol:

1. **Structured interview** — 6 dimensions (code, creative, logic, meta, system design, constraint)
2. **Two-model dialogue** — pit against a cloud model (e.g. DeepSeek V4 Flash via Nous) for conversation
3. **Free-form** — minimal prompting to see default creative tendencies
4. **Captured reasoning** — for reasoning-distilled models, capture `reasoning_content` as separate artifact

## Launching Qwopus

Qwopus requires llama-server b9351+ (rebuilt 2026-05-26 from HEAD). The model is cached at `~/.cache/huggingface/hub/`.

### Exact launch command

```bash
~/llama.cpp/build/bin/llama-server \
  -m ~/.cache/huggingface/hub/models--Jackrong--Qwopus3.5-9B-Coder-MTP-GGUF/snapshots/e2fd321c5ad49d75c122ccf1091c872c2b6c5ce8/Qwopus3.5-9B-Coder-MTP-Q6_K.gguf \
  -ngl 99 \
  -c 8192 \
  --port 8081 \
  --host 127.0.0.1
```

### Parameters explained

| Flag | Value | Why |
|------|-------|-----|
| `-ngl` | `99` | Offload all layers to GPU (RTX 3060 12GB, model is 7.6GB — fits comfortably) |
| `-c` | `8192` | Context window. The model supports 262K native but 8K is realistic for 12GB. Bump to 16384 if you don't need other apps' VRAM. |
| `--port` | `8081` | Avoids ollama's port 11434 and any other services. |
| `--host` | `127.0.0.1` | Local only — no network exposure. |

### Checking it loaded

```bash
tail -5 /tmp/llama-server-qwopus.log
# Should show: "server is listening on http://127.0.0.1:8081"
```

### Using the API

OpenAI-compatible endpoint on `http://127.0.0.1:8081/v1/chat/completions`:

```bash
curl -s http://127.0.0.1:8081/v1/chat/completions \
  -d '{
    "model": "qwopus",
    "messages": [{"role": "user", "content": "hello"}],
    "temperature": 0.7,
    "max_tokens": 3000
  }'
```

Note: this is a reasoning-distilled model. It outputs `reasoning_content` before the actual response. Set `max_tokens >= 5000` for anything non-trivial — the reasoning block eats the first ~4K chars.

### Logging

The launch command in this session used:
```bash
~/llama.cpp/build/bin/llama-server [flags] 2>&1 | tee /tmp/llama-server-qwopus.log
```

This captures server logs to a file while keeping them visible in the terminal. Check the log for timing info, error messages, and checkpoint status.

## Ollama Import

```bash
# For any of the above GGUF files downloaded locally:
ollama create my-model-name -f Modelfile
# Where Modelfile contains:
# FROM /path/to/downloaded.gguf
# PARAMETER num_ctx 32768
```

Or use `llama-server` directly for more control over context size and offload layers:

```bash
llama-server -m /path/to/model.gguf -ngl 99 -c 32768 --port 8081
```

---

See also: [[local-model-testing]] (skill), [[aq-calculator-design]] (designed during 9B local model session)