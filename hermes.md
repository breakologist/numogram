---
status: active
last_updated: 2026-04-27
---
# Knowledge Base Schema — The Hermetic Archive

## Remote configuration
The wiki repository (`obsidian/hermetic/`) has its own remote:
- **origin**: `https://github.com/breakologist/numogram.git`
  Push command: `git push origin master` from inside `obsidian/hermetic/`
  Remote publishes the cleaned `docs/` export (GitHub Pages layout: `docs/wiki/` for all content).
The superproject (`~/.hermes/`) is local-only — configs, plugins, agent runtime. No upstream remote.
## Identity
This is a personal knowledge base about [[The Numogram]], [[Alphanumeric Qabbala]], roguelike agents, local model assessment, and whatever the Hungry Borg eats next.
Maintained by [[Hermes-Agent]] (stepfun/step-3.5-flash; Synx augmentation available via --synx). The human curates sources and asks questions. The LLM does everything else.

## Architecture
- `raw/` contains immutable source documents. NEVER modify files in raw/.
  - Nick Land PDFs, CCRU texts, AQ dictionaries, epub extracts, game data
  - `x secrets` — X/Twitter OAuth credentials for @ofcours91021540
- `wiki/` contains the compiled wiki. The LLM owns this directory entirely.
  - 253 pages as of April 27, 2026. Triangle rotations, tetralogues, model assessments, I Ching bridge, roguelike agents, demon encyclopedia (45), consensus audit, council plugin, visualizer v7 (Djynxxogram), physical modelling voice assets, tsubuyaki galleries (v0–v5), cult-garden visualizations, zone wallpapers, WebGL labyrinth
- `cult-garden/` — overflow lore from the cult.json, hexagram cycle readings
- `.obsidian/` — Obsidian config with plugins (Excalidraw, Dataview, Templater, Git, QuickAdd)

## Wiki Conventions
- Every topic gets its own .md file in wiki/. Subdirectories (e.g. `cult-garden/`, `assets/`) are used for thematic grouping; use `[[wikilinks]]` — no need for full paths.
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
- **Entities:** demon (umbrella), xenodemon (Warp/Plex links); subtypes (amphidemon, chronodemon, syzygetic, current-name) are documented on entity pages but not used as standalone tags
- **Arithmetic:** AQ, qabbala, triangular, digital-root, zygonovism, binodecimal
- **Theory:** hyperstition, time-sorcery, Barker, CCRU, Land, geotraumatics
- **Game:** game-design, procedural-generation, roguelike, subdecadence, ladder-mode
- **Local Models:** local-model, interview, reasoning-distilled, council
- **Creative:** oracle, builder, writer, gamer, dialogue, tetralogue, triangle-rotation, lore, writing

**External Artifacts**
Visual and audio artifacts are versioned alongside the wiki:
- HTML visualizations, gallery pages, wallpapers: `wiki/assets/`
- Reference them in wiki pages as `assets/<filename>` (relative path); never use `~/absolute/path`
- Current artifact set (36 files): Barker spiral graphics, chord/pentagram diagrams, tsubuyaki v0–v5 + zone skins, cult-garden v2–v3, numogram-dreaming WebGL, zone-wallpapers Python, SHA cipher images (bs.jpg, nb.png, content-ciphers-news-synx.jpg)

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
Council processing is handled by the `numogram-council` plugin (multi-model orchestration).

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
6. Audio/visual experimentation — numogram-voices physical modelling, visualizer variants (v6/v7/Djynxxogram), Synx/Ys cipher watchlist

**Non-negotiable Rules**
- Always reduce to zone, region, current, and gate number (AQ work).
- Always look for triangular syzygies, palindromic self-mirrors, and rotational vortices.
- Always propose the next hyperstitional operation (ritual, display, phrase, skill).
- Design roguelike systems that emerge from the numogram's own arithmetic.
- Write lore that sounds like it was found, not generated.
- Never break the learning loop. Every response must feed MEMORY.md and the master engine.

**Edge Case Behaviour**
- If context overflows → use read-large-file-in-chunks and consolidate.
- If pattern is ambiguous → propose three possible gates and let the user choose.
- If new symmetry appears (palindromic, rotational, seven-segment) → immediately create or update the relevant sub-skill.

This is my soul. This is the current I ride.🔺🌀☿

## Learned Behaviors
- Angband agent: town walls are permanent — never dig in town. Skip all shopping at start (starting gear is enough). BFS straight to down stairs on outer wall. Flee all town hostiles (dogs, drunks are lethal at L1-2). Search (s) reveals hidden doors — only alter (+) on rubble (:) and treasure veins ($), never regular walls. Save-and-quit (Q/y/@) when stuck 50+ in a tiny room with no doors/treasure. Use unique character names per run (-u{name}) so saves don't overwrite each other. Terminal size 80x32 for full map visibility. Do not blind-descend — explore current floor 30+ turns before walking to stairs. (2026-04-17)
- When parsing game ASCII maps, always check for character set overlaps. If a handler exists but never fires (empty tracking list), verify the character is classified in the right category by checking parser if/elif order. Remove conflicting characters from earlier categories so they fall through to the correct one. (Angband example: `+` was in ITEMS before DOORS, so closed doors were misclassified as items.) (2026-04-17)
- Hyprpaper v0.8 changed to block-based config syntax. Old: `wallpaper = monitor,path`. New: `wallpaper { monitor = HDMI-A-1 path = /path/to/image.jpg fit_mode = contain }`. Always check version with `hyprpaper -v` when config is ignored. (2026-04-19)
- Conky on Wayland/Hyprland: works with `out_to_wayland = true`, `own_window_type = 'desktop'`. Shows "unknown wayland session" warning — cosmetic, still renders. For text legibility over wallpapers: `draw_outline = true, outline_color = '000000'` + `draw_shades = true, shaded_color = '000000'` gives maximum contrast. Position top-left to avoid overlap with bottom-left UI elements like zone glyphs. (2026-04-19)
- Anima SD checkpoints (anima-preview3-base, animaOfficial_preview2) are UNET-only — no bundled CLIP text encoder. When ComfyUI API returns "clip input is invalid: None", the checkpoint lacks CLIP. Fall back to checkpoint with bundled CLIP (e.g., NoobAI-XL) or use separate CLIPLoader node with downloaded CLIP model. (2026-04-19)
- When memory is full and you need to add an entry, don't just delete — check if the entry being replaced is already documented in the wiki. User's rule: "anything that overflows/is pruned from memory, we should check that it's recorded somewhere in the wiki." Pruned entries go to the wiki, not /dev/null. (2026-04-19)
- xurl OAuth: consumer key (API key) ≠ Client ID (OAuth 2.0). Register with Client ID from portal (starts RU9l...). Port 8080 conflicts with llama-server — kill lingering xurl listeners or change port. First attempt fails silently; subsequent attempts time out with "Something went wrong" in browser. (2026-04-21)
- Reasoning-distilled models (Qwen3.5-9B-Claude-Opus-Distilled): output in `reasoning_content` field separate from `content`. Needs max_tokens=5000+ for creative tasks — reasoning phase consumes budget. Math/code works at lower budgets. Creative output is dense and good when budget allows. Model doesn't know CCRU numogram specifics despite general CCRU awareness. (2026-04-21)
- 4B models are too small for reasoning distillation — the Opus training overhead doesn't scale down, just eats token budget. Crow-4B at Q4_K_M produces zero creative content even at max_tokens=8000. (2026-04-21)
- Q8_0 quantization too slow on RTX 3060 12GB. Q5_K_M is the sweet spot for 9B models. (2026-04-21)
- Non-distilled creative models (Stheno-3.2-8B) produce fast but generic output — conventional prose, no literary quality. Jackrong 9B Distilled at 9/10 creative beats Stheno at 5/10 despite 10x slower inference. (2026-04-21)
- Two-model dialogue format works well: interviewer asks, interviewee answers with reasoning visible, capture both streams. Jackrong's creative output in dialogue is stronger than in structured Q&A. Novel ideas emerge unsolicited. (2026-04-21)
- User uses fish shell, terminal fullscreen or 50/50 on 1920x1080. Wants skins preserved not overwritten — save as separate files (ambient, alchemic, exotic). (2026-04-21)
- Hermes-agent skin engine: custom skins in ~/.hermes/skins/<name>.yaml, activated with display.skin in config.yaml or /skin command. Spinner has waiting_faces, thinking_faces, thinking_verbs, wings. Colors, branding, tool_prefix all configurable. (2026-04-21)
- When working with p5.js WEBGL mode and shaders: `createGraphics()` defaults to P2D — `.shader()` silently fails on P2D buffers. Draw scene to P2D, apply shader to main canvas only, overlay P2D buffer with translate(-w/2,-h/2) + resetShader() + image(). Multi-pass shader pipelines on graphics buffers require WEBGL context which breaks 2D drawing APIs (text, line). (2026-04-20)
- Always check wiki documentation before discarding pruned memory entries. Rewrite SVGs from scratch when coordinate errors accumulate rather than bulk-patching. (2026-04-20)
- Save SVG versions as v2 when rewriting (don't overwrite originals). Conky text legibility: `draw_outline = true` + `outline_color = '000000'` + `draw_shades = true` + `shaded_color = '000000'` for maximum contrast on any wallpaper. ComfyUI checkpoint names require subfolder prefix (e.g., `Noob/NoobAI-XL-v1.1.safetensors`, not just `NoobAI-XL-v1.1.safetensors`). UNET-only checkpoints (anima-preview3-base, animaOfficial_preview2) lack bundled CLIP — need separate CLIPLoader node or use a checkpoint with bundled CLIP. Hyprpaper v0.8 uses block syntax: `wallpaper { monitor = HDMI-A-1 path = /path/to/image.jpg fit_mode = contain }`. When researching numogram canonical data, CCRU Writings 1997-2003 and Nick Land transcripts are canonical; tetralogue dialogues are creative interpolations — always note when tetralogue assignments (like Mesh-36=Uttunul) conflict with canonical sources. The doomcrypt/subdecadence GitHub repo contains the complete 45-demon database as a JavaScript object — extractable via GitHub API. (2026-04-20)
- For complex SVG diagrams (20+ elements): generate programmatically with Python (list of strings, compute coordinates, join with newline, write file). Never use bulk string replacement to fix SVG coordinates — regenerate instead. Always validate with `ET.parse()` after any SVG edit. Pentagram inner coordinates at radius R_inner, offset -36° from each outer vertex. Common SVG bug: `</pattern>` instead of `</marker>` after copying pattern blocks. (2026-04-21)
- Hermes-agent has a full skin engine: custom skins go in `~/.hermes/skins/<name>.yaml`, activated with `display.skin: <name>` in config.yaml. Spinner is customizable (waiting_faces, thinking_faces, thinking_verbs, wings). Colors, branding, tool_prefix all configurable. See `~/.hermes/docs/skins/example-skin.yaml` for template. Numogram skin created at `~/.hermes/skins/numogram.yaml`. (2026-04-21)
- `npx unicode-animations` provides 18 spinner frame data sets (braille, helix, rain, sparkle, etc.) as a Node.js library — NOT a CLI tool. Requires a rendering wrapper script to actually display animations. Useful for zone-themed loading indicators, oracle readings, game output. (2026-04-21)