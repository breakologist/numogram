---
title: "Aider — AI Coding Agent & Possible Integration"
created: 2026-04-21
last_updated: 2026-04-21
status: draft
tags: ["agent", "code", "local-model", "roguelike", "tool"]
sources: [aider.chat, web research April 2026]
---


# Aider — AI Coding Agent & Possible Integration

## What Is Aider?

[Aider](https://aider.chat) is an open-source AI coding agent that works directly with your codebase via the terminal. It can:
- Edit existing files in-place (not just generate new code)
- Run git commands to track changes
- Execute code and read error output
- Work with multiple files simultaneously
- Support local models via ollama, llama.cpp, vLLM, LiteLLM

Key difference from chat-based coding: Aider operates on your actual files. It doesn't just suggest code — it *changes* code and commits the changes.

## How It Works

```
$ aider src/numogram_roguelike.py
> Add a new Zone 5 ability: "Mercury's Hinge" — teleport to the last syzygy partner visited
```

Aider reads the file, understands the codebase structure, makes the edit, and can commit the change. It's like having a pair programmer who actually touches the keyboard.

## Local Model Support

Aider supports local models via:
- **ollama** — `aider --model ollama/qwen2.5:7b-instruct`
- **llama.cpp** — `aider --model openai/Qwen3.5-9B-Q5_K_M` (via OpenAI-compatible API)
- **vLLM** — `aider --model openai/model-name` (local vLLM server)

For our RTX 3060 setup:
```
# Via ollama
aider --model ollama/qwen2.5:7b-instruct ~/numogame/numogram_roguelike.py

# Via llama-server (port 8080)
aider --model openai/Qwen3.5-9B-Q5_K_M --api-base http://localhost:8080/v1 ~/numogame/numogram_roguelike.py
```

## Qwen2.5 Models for Coding

| Model | Size | Quant | Best For | VRAM Fit |
|-------|------|-------|----------|----------|
| qwen2.5:7b-instruct | 4.7GB | Q4_K_M | General coding, fast | ✓ Plenty of room |
| qwen2.5-coder-7b-instruct | ~5GB | Q4_K_M | Code-specific fine-tune | ✓ Plenty of room |
| qwen2.5-coder-14b-instruct | 9.8GB | Q5_K_M | Best coding quality | ⚠ Needs CPU offload |
| qwen2.5:32b | ~18GB | Q4_K_M | Best overall coding | ✗ Too large |

**Recommendation:** `qwen2.5-coder-7b-instruct` if available on ollama, or `qwen2.5:7b-instruct` (already installed). The 14B coder is the best quality but needs CPU offload (9.8GB model + VRAM overhead > 12GB). Still testable but slower.

For comparison, Gemma3-12B scored 7/10 for code in our assessment. Qwen2.5-Coder-14B would likely score higher for code but lower for creative writing.

## Possible Uses with the Roguelike

### 1. Feature Implementation
Aider could implement new abilities, room types, or demon mechanics directly in `numogram_roguelike.py`. Example:
```
aider ~/numogame/numogram_roguelike.py
> Add a "Bleed" event: when hyperstition exceeds 75%, the current zone bleeds into adjacent zones, creating hybrid rooms
```

### 2. Bug Fixing
Aider can read error output and fix bugs:
```
aider ~/numogame/numogram_roguelike.py
> The player can walk through walls in Zone 0 when hyperstition is above 90%. Fix this.
```

### 3. Refactoring
Aider can clean up and refactor code:
```
aider ~/numogame/numogram_roguelike.py
> Refactor the demon combat system into a separate class. Keep the same behavior.
```

### 4. Test Generation
Aider can write tests for existing functionality:
```
aider ~/numogame/numogram_roguelike.py
> Write pytest tests for the syzygy_event() function and the cult.json persistence
```

### 5. Documentation
Aider can generate docstrings and README updates:
```
aider ~/numogame/numogram_roguelike.py
> Add docstrings to all public methods. Follow Google style.
```

## Comparison: Aider vs Hermes Agent

| Feature | Aider | Hermes Agent |
|---------|-------|-------------|
| File editing | ✓ In-place, git-aware | ✗ Suggests, doesn't edit |
| Code execution | ✓ Runs code, reads output | ✗ Can run via execute_code but not integrated |
| Multi-file | ✓ Reads multiple files simultaneously | ✗ One file at a time via read_file |
| Git integration | ✓ Automatic commits | ✗ Manual git operations |
| Local models | ✓ ollama, llama.cpp, vLLM | ✓ ollama, llama.cpp |
| Context window | Model's native (32K-128K) | Limited by conversation |
| Domain knowledge | Generic (no wiki/memory) | Numogram wiki, MEMORY.md, SOUL.md |
| Creative writing | Weak (code-focused) | Strong (Jackrong, tetralogue) |
| Roguelike design | Can implement | Can design + implement |
| Cost | Free (local models) | Free (local models) |

### Hybrid Approach

The best approach might be:
1. **Hermes Agent** designs the system (tetralogue, oracle analysis, numogram mapping)
2. **Aider** implements the design (code changes, git commits, testing)
3. **Hermes Agent** reviews the implementation (code review, numogram verification)

This is a Builder/Aider split: the Builder (Gemma3-12B) designs through Hermes, the Aider (Qwen2.5-Coder) implements through Aider.

## Open Questions

1. Can Aider use our numogram wiki as context? (Probably not directly — it works with code files, not markdown)
2. Would Qwen2.5-Coder-14B score higher than Gemma3-12B for code? (Needs testing)
3. Can Aider integrate with our council? (It could be the "Builder" layer, with Hermes as the "Oracle" layer)
4. Does Aider support multi-model routing? (Use one model for code, another for creative)

## Related

- [[model-assessment-summary]] — Model comparison and council architecture
- [[brogue-design-principles]] — Roguelike design principles
- [[numogame-state-of-the-game]] — Current state of the Abyssal Crawler
- [[hermes-agent-guide]] — Hermes Agent capabilities
