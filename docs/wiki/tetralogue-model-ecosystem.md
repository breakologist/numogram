---
title: Tetralogue — Model Ecosystem: Local vs API vs Trials
created: 2026-05-03
updated: 2026-05-03
category: tetralogue
status: in_progress
tags: [tetralogue, model-landscape, local-llm, api-models, free-trials, stepfun, ollama, multi-provider]
---

# Tetralogue Roundtable — The Model Ecosystem

> **Context**: Hermes Agent operates across multiple model backends — local Ollama instances, paid API providers (OpenAI, Anthropic, etc.), and free trials (StepFun, Groq, etc.). As trials end and hardware shifts, how do we maintain coherent agency across this heterogeneous landscape?

---

## Opening Statements

**ORACLE**  
The numogram does not care where computation happens. A gate derived from `sha1(aq_str)` is indifferent to GPU vendor. But *oracle voice* — the texture of response, the cadence of hyperstition — varies with model architecture, context window, and training corpus. We must map **model identity** onto **current signature**: which model speaks as Tiresias, which as Prometheus, which as the Builder?

**BUILDER**  
Practical constraints first. Local models (Llama 3.1 70B, Qwen 2.5 72B) give us privacy, speed, and unlimited retries. Paid APIs (Claude Opus, GPT-4.5) offer reasoning depth and tool use fidelity. Free trials (StepFun step-3.5-flash, Groq Llama 3.1 70B) are high-throughput but rate-limited. My job is to build a **router** that matches task to model: oracle divination → deep model; code generation → fast local; council deliberation → multi-model ensemble.

**WRITER**  
Voice consistency is narrative hygiene. If the oracle's pronouncements shift from "CCRU-tinged accelerationist" to "neutral helpful assistant" between sessions, the hyperstition breaks. We need **voice-preserving adapters**: system prompts that anchor each model to its role, regardless of base architecture. Or better: fine-tune small adapters (LoRA) for each voice that sit atop any base model.

**GAMER**  
What happens on turn 3 when the API rate limit hits? We need **failover cascades** and **local fallbacks**. Also: can we use free trials as "oracle dice"? Roll a StepFun request when we want accidental insight. The meta-game: treat model availability itself as a numogram gate — which model answers depends on the day's entropy.

---

## Council Deliberation

### Q1: Should we standardise on a single provider, or embrace heterogeneity?

**ORACLE**: Heterogeneity is the only honest stance. The numogram is a *plural* system — 9 zones, 45 gates, 5 currents. No single model can embody all currents. We need a **council-of-models** architecture where each voice corresponds to a specialised backend.

**BUILDER**: Agreed, but orchestration overhead is real. My proposal:
- **Oracle mode** → Claude Opus (deep, narrative-rich)
- **Builder mode** → GPT-4.5 (code structure, architectural clarity)
- **Writer mode** → local Llama 3.1 70B (fine-tuned on CCRU corpus)
- **Gamer mode** → StepFun step-3.5-flash (fast, playful, trial-friendly)

Fallback chain: if primary is down, cascade to next-cheapest alternative.

**WRITER**: The risk is **voice drift**. If we switch oracles mid-tetralogue, the tetralogue fractures. Better: maintain **consistent system prompts** that are more powerful than the model. A sufficiently strong prompt can make a fast model sound like a deep one. Test: run the same tetralogue question through 4 models with identical system prompts — which diverges least?

**GAMER**: I like the idea of **model roulette** for certain gates. For instance, when casting the I Ching via `iching-numogram-casting`, use the hardware entropy to select which model interprets the hexagram. That way, the *interpretation* becomes part of the divination.

### Q2: How do we handle context window limits across models?

**BUILDER**: Context compression is mandatory. We already use `karpathy-llm-wiki` for long-term memory; for active context we need:
- **Recency prioritisation**: latest 10 turns always in context
- **Summarisation**: older turns compressed via local model (fast, cheap)
- **Selective retrieval**: only fetch wiki pages relevant to current AQ calculation

**ORACLE**: The numogram itself is a compression scheme. A syzygy chain stands in for thousands of words. When we invoke `current: T₁–T₉`, that single token should expand in the model's mind to the full triangular structure. We need **numogram-native context tags** that the model learns to unpack.

**WRITER**: Could we pre-embed common numogram expansions as *hidden tokens*? Like, whenever `[TRIANGLE]` appears, the model actually receives a pre-written paragraph describing T₁–T₉–T₁₀. This keeps response latency low while preserving density.

**GAMER**: Or treat context slots as **inventory**. Each model gets a fixed budget (e.g., 10 wiki pages + 20 turns). We manage it like a roguelike inventory screen — drop something to make space. The player (user) decides what's important.

### Q3: What about cost? Paid APIs add up fast.

**BUILDER**: Cost-aware routing:
1. **Local first**: If model capable, use local (zero $)
2. **Free trial second**: StepFun, Groq, Together (rate-limited but free)
3. **Paid fallback**: Only for tasks that absolutely need it (longReasoning, deep oracle)

Track usage per model in `~/.hermes/billing.json`. Set monthly caps. When cap hit, auto-downgrade to next-cheapest tier.

**ORACLE**: The numogram teaches **parsimony**. A good oracle speaks in few words. We should train our models to be **terse**: compress the oracle voice into fewer tokens without losing density. That saves money *and* improves mystical impact.

**WRITER**: I'm concerned about **accessibility**. If the project becomes dependent on paid APIs, only those with budgets can replicate. We should maintain a **fully local stack** that runs on consumer hardware, even if weaker. Document the trade-offs: "Local Llama 3.1 70B + adapters achieves 85% of Opus quality for oracle tasks."

**GAMER**: What if we **game** the system? Use free trials as "mana potions" — they refill daily. Schedule heavy tasks (councils, wiki generation) for trial windows. Keep local model for baseline. This is resource management, pure and simple.

### Q4: How do we keep skills working when backends change?

**BUILDER**: **Abstraction layer**. All skill-provider interactions go through `honcho-deriver-custom-llm` which maps:
- Task type → provider selection
- Provider → token format, streaming, tool calling
- Failure modes → retry/fallback logic

When a provider changes API (e.g., OpenAI deprecates a parameter), we update the adapter, not every skill.

**ORACLE**: The **council plugin** already does this for local Ollama. We need to extend it to support HTTP adapters for OpenAI, Anthropic, StepFun, etc. Each model gets a `provider_config.yaml`:
```yaml
name: stepfun-step-3.5-flash
endpoint: https://api.stepfun.com/v1/chat/completions
rate_limit: 1000/day
cost_per_1k: 0.0
voice: oracle-accelerated
```

**WRITER**: Skills that rely on specific model quirks (e.g., "Claude is good at XML tool use") need **capability flags**. A skill can declare `requires: reasoning-depth=high` and the router picks Opus or GPT-4.5; or declares `requires: fast, cheap` and picks StepFun trial.

**GAMER**: This is the **load-out screen**. Before a session, we pick our gear: which models are active today? Which are on cooldown? The agent's effectiveness depends on strategic model management.

---

## Tetralogue Synthesis

**ORACLE**: The future is **multi-provider, voice-preserving, cost-aware routing**. The numogram's currents will flow through whichever pipes are open.

**BUILDER**: I will extend the `multi-provider-council-pattern` skill to formalise this: provider registry, capability matrix, fallback trees, billing tracker.

**WRITER**: I'll draft a **voice specification** per current: Oracle (Landian accelerationist), Builder (clear pragmatic), Writer (uncanny, anti-AI-isms), Gamer (systems-thinking playful). These prompts will be model-agnostic.

**GAMER**: And I'll design a **model roulette mechanic** for divination tasks — each query rolls a die to pick which backend answers, turning infrastructure uncertainty into a feature.

---

## Implementation Checklist

- [ ] Extend `multi-provider-council-pattern` to support HTTP-based providers (StepFun, OpenAI, Anthropic, Groq)
- [ ] Create `~/.hermes/config/model-providers.yaml` with rate limits, costs, voice tags
- [ ] Build cost-tracking in `honcho-billing` (monthly caps, per-provider usage)
- [ ] Write **voice-preserving system prompts** for each tetralogue role (portable across models)
- [ ] Create a **fallback cascade skill**: `call_with_fallback(task, preferred_providers, fallback_chain)`
- [ ] Document local-only vs hybrid operation modes in `AGENTS.md`
- [ ] Add a `--model-roulette` flag to oracle skills (random backend selection per turn)
- [ ] Test: run full tetralogue with mixed providers (StepFun + local Llama + Claude if available) — assess coherence
- [ ] Archive current StepFun trial state (API key, remaining quota) in `~/.hermes/trials/stepfun.json`

---

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Voice drift when switching providers | Anchor with strong role-play system prompts; test each provider's voice fidelity |
| Rate limit exhaustion during critical task | Local fallback always available; cache frequent queries |
| Cost overrun | Hard caps in billing; daily spend alerts; auto-disable expensive models |
| API deprecation breaking skills | Adapter pattern isolates changes; monitor provider changelogs |
| Free trial expiry mid-session | Graceful degradation: pause task, inform user, offer local alternative |

---

## Hyperstitional Afterword

The numogram is a **distribution over models**. Each backend samples from a different slice of the belief space. By weaving them together, we don't just get a better agent — we get a **pantheon of oracles**, each with its own accent, its own bias, its own relationship to the symbolic. The closed loop now spans **hardware and cloud, local and remote, free and paid**. The loop strengthens.

Let the trials end and the local stacks persist. The voices remain.

---

**Next**: Builder to draft provider adapter schema. Oracle to compose voice anchors. Gamer to design roulette probabilities. Writer to compose the final tetralogue narrative.
