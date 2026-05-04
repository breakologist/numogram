# Oracle Fine-Tuning — Status 2026-05-04

## ✅ Completed

| Task | Result |
|------|--------|
| **Corpus builder** | Adapted to use local Qwen on port 11434; generated **177 instruction examples** |
| **Dataset** | `~/.hermes/data/oracle_finetuning_v1.jsonl` — Llama 2 chat format, zone/gate/current/triangular topics |
| **Axolotl config** | `~/.hermes/config/oracle_ft_config.yaml` — QLoRA (r=64, 4-bit, 1k seq, 4 epochs) |
| **Install script** | `~/.hermes/scripts/setup_oracle_finetune.sh` — one-command environment setup |

## 📦 Corpus Details

- **Seed corpus**: 74 paragraphs extracted from core wiki (numogram, syzygy, triangular, warp, plex, Barker Spiral)
- **Augmentation**: 2× paraphrasing via Qwen 2.5 7B (local Ollama) + Q&A extraction from headings
- **Total examples**: 177
- **Format**: Llama 2 chat (`<s>[INST] ... [/INST]`) — ready for Axolotl `chat_template: llama-2`
- **Topic distribution**:
  - Zone questions: 94
  - Gate questions: 38
  - Current questions: 35
  - Triangular: 10

## 🔧 Next Steps (Your Machine)

### 1. Install training environment (run in terminal)

```bash
bash ~/.hermes/scripts/setup_oracle_finetune.sh
```

This creates `~/.hermes/venv_oracle/` and installs torch + axolotl (~5–10 min depending on network).

**If PyTorch CUDA download fails** (common on slow links), alternative:

```bash
cd ~/.hermes
python3 -m venv venv_oracle
source venv_oracle/bin/activate
pip install --upgrade pip
# Try CPU torch first (fast), then verify CUDA driver works at runtime
pip install torch --index-url https://download.pytorch.org/whl/cu118 || pip install torch
python -c "import torch; print('CUDA available:', torch.cuda.is_available())"
pip install "axolotl[flash-attn]" git+https://github.com/OpenAccess-AI-Collective/axolotl.git
```

### 2. Start training

```bash
cd ~/.hermes
source venv_oracle/bin/activate
axolotl train --config config/oracle_ft_config.yaml
```

Expected time: ~2–4 hours on RTX 3060 12GB (bs=1, grad-acc=4, 4 epochs, 177 examples).

### 3. Merge LoRA & serve

```bash
# After training, merge LoRA into base
axolotl merge-lora --config config/oracle_ft_config.yaml

# Convert to GGUF (optional, for llama-server)
# (script to be added)

# Serve on new port
llama-server --model ~/.hermes/models/oracle_qwen7b_lora/ --port 8081
```

### 4. Update provider registry

Add to `~/.hermes/config.yaml`:

```yaml
providers:
  oracle-local:
    endpoint: http://localhost:8081/v1/chat/completions
    models:
      - oracle-qwen7b
    rate_limit: null
    voice: oracle-native  # our fine-tuned voice
```

Then route `oracle:` queries to this provider via skill or manual dispatch.

## ⚠️ Known Issues & Notes

- **StepFun API key**: Not directly accessible; using local Qwen via Ollama is correct path.
- **Ollama port confusion**: Corpus builder now uses port 11434 (OpenAI-compatible endpoint). Verified working.
- **Axolotl install**: May fail on slow networks; fallback to CPU-only torch and rely on CUDA driver at runtime.
- **Dataset size**: 177 examples is minimal but should produce a noticeable voice shift. Plan to augment later with manual examples or synthetic expansion.
- **Base model**: Qwen2.5-7B-Instruct requires HuggingFace access (not gated). If you hit HFauth errors, set `HF_TOKEN` env var or use a local GGUF conversion path (more involved).

## 📂 Files Modified/Created

- `~/.hermes/scripts/build_oracle_corpus.py` (patched to use localhost:11434 + qwen2.5:7b-instruct)
- `~/.hermes/data/oracle_finetuning_v1.jsonl` (new, 177 examples)
- `~/.hermes/config/oracle_ft_config.yaml` (new, Axolotl training config)
- `~/.hermes/scripts/setup_oracle_finetune.sh` (new, install script)

## 🎯 Success Criteria

After training, expect:
- **Oracle density**: ≥15% numogram mentions vs current Nemotron (0%)
- **Hyperstitional markers**: CCRU-style neologisms, zone/gate references present
- **Local execution**: No rate limits, fast inference on RTX 3060

---

**Once you've run the install script and (optionally) started training, let me know and I'll help validate the oracle's output quality and set up provider routing.**
