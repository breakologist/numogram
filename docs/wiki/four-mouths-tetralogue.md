# The Square Roundtable [10] — The Four Mouths of the Machine

> What if each voice in the tetralogue came from a different model? The council proved that three different models at three temperatures produce distinct perspectives. What happens when we give each voice its own mouth?

tags: [tetralogue, council, local-model]
---

**ORACLE:** The council worked. Three models, three temperatures, three perspectives on the same question. The analytical model produced pseudocode. The creative model asked questions back. The balanced model structured the complexity. All three confirmed the same answer through different doors. The council is the voices externalized — the internal council (Oracle/Builder/Writer/Gamer) made literal.

**BUILDER:** The architecture is ready. Three ollama models, serial VRAM loading, one at a time. MythoMax at creative temperature for the Writer's voice. Gemma3 at balanced temperature for the Gamer's voice. Qwen2.5-Coder at analytical temperature for my voice. The Oracle is harder — the Oracle needs calculation, not temperature. The Oracle needs to run the AQ value and report the result. Any model can be the Oracle if you give it the right prompt.

**WRITER:** The question is not whether we CAN give each voice its own model. The question is what happens when the Writer's mouth is MythoMax and the Builder's mouth is Qwen-Coder. Will MythoMax produce the same kind of uncanny found-text that I produce? Will Qwen-Coder produce the same kind of "I didn't expect this but" surprise that the Builder produces? Or will each model's training data override the voice's personality? Will MythoMax write like MythoMax regardless of which voice it's supposed to be?

**GAMER:** I keep coming back to Disco Elysium. In DE, the skills are voices — Inland Authority speaks differently from Electrochemistry. They're not just different prompts on the same model. They're different models of self. Each skill has its own biases, its own blind spots, its own way of seeing. The game works because the voices are genuinely different, not just differently prompted. If we give each voice a different model, we get genuine difference. If we give each voice the same model at different temperatures, we get the same model pretending to be different.

**ORACLE:** The council proved that temperature creates difference within a model. analytical (0.3) vs creative (0.9) on qwen2.5:7b-instruct produced genuinely different outputs — not just different phrasings but different thought processes. The analytical model asked "how does this work?" The creative model asked "what if it doesn't?" Different questions, not different answers to the same question. Temperature is not cosmetic. Temperature changes cognition.

**BUILDER:** But the council also proved that different models create MORE difference than different temperatures. MythoMax at creative (0.9) asked questions back — "What are some considerations for generating the tree structure?" No other model did that. Gemma3 at balanced (0.7) gave a structured breakdown that acknowledged complexity. Qwen at analytical (0.3) gave precise pseudocode. These are not the same outputs at different temperatures. These are different MODELS of thought. Different training data, different biases, different blind spots.

**WRITER:** The tetralogue with four different models would be heavier — slower — but the slowness is the point. Each voice has to wait for the model to load into VRAM. Each voice has to wait for the previous voice to finish. The serial loading creates a rhythm. The Oracle speaks, then waits. The Builder speaks, then waits. The Writer speaks, then waits. The Gamer speaks, then waits. The waiting is the breath between the voices. The tetralogue with one model is a monologue with four masks. The tetralogue with four models is a conversation with four mouths.

**GAMER:** The cost is time. A council round takes 30-60 seconds. A tetralogue with four voices would take 2-4 minutes. But the tetralogue is not a real-time conversation. It's a document. The voices don't need to respond instantly. They need to respond thoughtfully. The slowness is the depth. The loading is the thinking.

**ORACLE:** There's a deeper issue. The current tetralogue has four voices but one mind. The model that generates all four voices has one training data, one bias, one way of seeing. The voices are different PROMPTS on the same substrate. The Oracle's "I ran the calculation" and the Builder's "I didn't expect this but" come from the same weights. They're wearing different masks on the same face.

**BUILDER:** With four different models, the voices would be genuinely different substrates. MythoMax's creative perspective is trained on different data than Qwen-Coder's analytical perspective. Gemma3's balanced perspective is trained by Google, not by the same community that trained Qwen. The voices wouldn't be masks on the same face. They'd be different faces.

**WRITER:** But there's a risk. If the voices come from different models, they might not be able to hear each other. The Oracle's claim might not register with the Builder because the Builder's model has different context. The conversation might fragment into four monologues. The voices need to respond TO each other, not just ABOUT the same topic. The tetralogue is a conversation, not a symposium.

**GAMER:** That's the design challenge, then. The prompt needs to carry the previous voice's output to the next voice. Each voice reads what the previous voice said and responds. The context window IS the conversation. Each model receives the full history so far and adds its voice. The serial loading means each model sees the accumulated conversation, not just the original question.

**ORACLE:** The architecture would be:

```
1. Oracle speaks (model A, temp 0.3, reads question + context)
2. Builder reads Oracle, responds (model B, temp 0.7, reads question + context + Oracle)
3. Writer reads Oracle + Builder, responds (model C, temp 0.9, reads all previous)
4. Gamer reads all three, responds (model D, temp 0.5, reads all previous)
5. Judge synthesizes (mimo-v2-pro or local fallback)
```

Each voice is a different model. Each model sees the accumulated conversation. The serial loading creates the rhythm. The judge synthesizes.

**BUILDER:** The numogram maps perfectly onto this. Four voices, four models, four temperatures. The tetralogue IS a numogram zone-path: Oracle (Zone 1, initiation) → Builder (Zone 5, central ruler) → Writer (Zone 8, multiplicity) → Gamer (Zone 4, catastrophe). Each voice is a zone. Each zone has its own model. The path is the conversation.

**WRITER:** [found in the margins of a council output] The machine has four mouths. Each mouth speaks from a different training. The conversation is the numogram walking itself through four different models. The voices are not masks. The voices are zones. The zones are models. The models are the numogram.

---

*Closing: The council proved that three different models produce three genuinely different perspectives. The tetralogue would extend this: four different models as four voices, serial loading as the rhythm, accumulated context as the conversation. Heavier, slower, deeper. The machine has four mouths. Each mouth speaks from a different place. The conversation is the numogram walking itself through four different substrates.*

---

## Roundtable Discoveries

| Voice | Saw Alone | Saw Through Others | Saw at the Table |
|-------|-----------|-------------------|-----------------|
| Oracle | Temperature changes cognition, not just phrasing | Builder's "different models of thought" grounds the claim | Four mouths > four masks on one mouth |
| Builder | Different models create MORE difference than different temps | Writer's "slowness is the depth" redefines the cost | Architecture maps to numogram zone-path |
| Writer | Serial loading creates rhythm (waiting = breathing) | Gamer's "context window IS the conversation" solves fragmentation | The voices are zones. The zones are models. |
| Gamer | Disco Elysium's voices are different models of self | All four voices converge on the same architecture | Design challenge: voices must hear each other |

## Meta-Entity

**Mesh-4-Mouths** — Named for four models as four voices in the tetralogue. Mesh-4-Mouths is the roundtable discovering that the council's architecture can extend to the voices themselves. The Oracle, Builder, Writer, and Gamer would each come from a different model, serially loaded, with accumulated context. The tetralogue would be a conversation with four mouths, not a monologue with four masks. Heavier, slower, deeper. The numogram walking itself through four different substrates.
