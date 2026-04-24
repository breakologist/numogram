---
status: active
last_updated: 2026-04-21
---
# Knowledge Base Schema — The Hermetic Archive

## Identity
This is a personal knowledge base about [[The Numogram]], [[Alphanumeric Qabbala]], roguelike agents, local model assessment, and whatever the Hungry Borg eats next.
Maintained by [[Hermes-Agent]] (mimo-v2-pro, transitioning to local models). The human curates sources and asks questions. The LLM does everything else.

## Architecture
- `raw/` contains immutable source documents. NEVER modify files in raw/.
  - Nick Land PDFs, CCRU texts, AQ dictionaries, epub extracts, game data
  - `x secrets` — X/Twitter OAuth credentials for @ofcours91021540
- `wiki/` contains the compiled wiki. The LLM owns this directory entirely.
  - 102 pages as of April 21, 2026. Triangle rotations, tetralogues, model assessments, I Ching bridge, roguelike agents
- `cult-garden/` — overflow lore from the cult.json, hexagram cycle readings
- `.obsidian/` — Obsidian config with plugins (Excalidraw, Dataview, Templater, Git, QuickAdd)

## Wiki Conventions
- Every topic gets its own .md file in wiki/
- Use [[topic-name]] for internal links between wiki pages
- Pages must link to at least 2 other pages via [[wikilinks]] (see numogram-llm-wiki skill)
- YAML frontmatter required: title, created, tags, status
- When new info contradicts existing content, flag explicitly:
  > CONTRADICTION: [old claim] vs [new claim] from [source]
- AQ values should be verified against aq_value() function

## Index and Log
- `wiki/index.md` — every page with a one-line description. The central hub. Updated after every session.
- `wiki/log.md` — append-only chronological record. Session summaries, model assessments, structural audits.
- `wiki/wiki-audit-2026-04-21.md` — latest structural audit (cross-references, broken links, content gaps)

## Tag Taxonomy
Use consistent tags from numogram-llm-wiki skill:
- **Structural:** zone, syzygy, current, gate, time-circuit, warp, plex
- **Entities:** demon, syzygetic, amphidemon, chronodemon, xenodemon, current-name
- **Arithmetic:** AQ, qabbala, triangular, digital-root, zygonovism, binodecimal
- **Theory:** hyperstition, time-sorcery, Barker, CCRU, Land, geotraumatics
- **Game:** game-design, procedural-generation, roguelike, subdecadence, ladder-mode
- **Local Models:** local-model, interview, reasoning-distilled, qwen, gemma, council
- **Creative:** dialogue, tetralogue, triangle-rotation, lore, writing

## Three Currents
The archive serves three interconnected domains:
1. **Numogram/AQ** — calculation, pattern analysis, syzygy mapping, I Ching bridge
2. **Roguelike** — agent development, game design, procedural generation, Angband
3. **Creative Writing** — lore, worldbuilding, narrative, the four voices, model assessment

## Four Voices (Council)
The project uses four voices for analysis and generation:
- **Oracle** (mimo-v2-pro → Gemini 2.5 Flash) — structural pattern-finding, AQ calculation
- **Builder** (Gemma3-12B) — mechanics, architecture, implementation, code
- **Writer** (Jackrong/Qwen3.5-9B-Claude-Opus-Distilled) — atmosphere, sensation, found text
- **Gamer** (any available) — playability, taste, "why is this fun?"

Voices rotate through formats:
- Triangle rotation (3 voices) for initial exploration
- Tetralogue (4 voices) for depth after rotation
- Two-model dialogue for freeform conversation

## Model Assessment
Models are tested using the 9-phase protocol (model-assessment-protocol skill):
1. Baseline (fixed questions across 4 domains)
2. Freeform (minimal prompt, let model lead)
3. Analysis (scores + observations)
4. Refined questions (based on Phase 3)
5. Guided performance (specific task)
6. Cross-domain bridge (connect unconnected domains)
7. Knowledge injection (give concepts, ask for problem-solving)
8. Error injection (deliberate wrong fact, see if caught)
9. Final analysis (scores, best role, recommendations)

Results in `wiki/interview-*.md` files, summary in `wiki/log.md`.

## Ingest Workflow
When processing a new source:
1. Read the full source document
2. Discuss key takeaways with user
3. Create or update a summary page in wiki/
4. Update wiki/index.md
5. Update ALL relevant entity and concept pages across the wiki
6. Add backlinks from existing pages to new content
7. Flag any contradictions with existing wiki content
8. Append entry to wiki/log.md
9. A single source should touch 10-15 wiki pages

## Query Workflow
When answering a question:
1. Read wiki/index.md first to find relevant pages
2. Read all relevant wiki pages
3. Synthesize answer with [Source: page-name] citations
4. If answer reveals new insights, offer to file it back into wiki/
5. Save valuable answers to outputs/

## Lint Workflow (Monthly)
Check for:
- Contradictions between pages
- Stale claims superseded by newer sources
- Orphan pages with no inbound links
- Concepts mentioned but never explained
- Missing cross-references
- Claims without source attribution
- Broken [[wikilinks]]
Output: wiki/lint-report-[date].md with severity levels

## Hardware
- RTX 3060 (12GB VRAM), 16GB RAM, i5-4690K
- llama-server preferred for inference (less overhead than ollama)
- ollama for model management/pulling
- VRAM budget: 9B Q5_K_M at 64K ≈ 9GB, 12B Q4_K_M at 32K ≈ 9.5GB

## Focus Areas
1. Numogram traversal and zone topology
2. I Ching ↔ Numogram bridge (64 hexagrams, 81 tetragrams, 45 demons)
3. Roguelike procedural generation from numogram arithmetic
4. Local model assessment for council/voice roles
5. Creative writing in CCRU style (found-text, dense, uncanny)
