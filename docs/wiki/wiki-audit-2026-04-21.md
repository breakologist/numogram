---
title: "Wiki Audit — April 21, 2026"
tags: [wiki-audit, structural]
created: 2026-04-21
status: active
---

# Wiki Audit — April 21, 2026

Full review of 102 wiki files. Structural analysis, content gaps, thematic connections, and meta-elements.

## Structural Findings

### Cross-Referencing
- **100 of 102 files are orphaned** — not linked FROM any other file. The wiki is flat, not a connected web.
- **54 files have NO wikilinks at all** — including all model assessment files, skills-to-explore, and several core numogram pages.
- **Only 2 files link to other files:** index.md (93 links) and log.md (6 links).
- The numogram-llm-wiki skill says "Every page must link to at least 2 other pages via [[wikilinks]]" — this rule is not followed.

### Broken Links (22 total, 19 fixed)
- `angband-agent-progress.md` → ``angband-agent`` (fixed → `[[angband-agent]]`)
- `angband-ladder-analysis.md` → ``angband-agent`` (fixed → `[[angband-agent]]`)
- `body-mapping.md` → `[[numogram-warp]]` and `[[numogram-plex]]` (trailing backslashes, fixed)
- `hardware-entropy.md` → ``entropy-sources`` and ``numogram-oracle`` (skills, not wiki pages — acceptable but noted)
- `qliphoth-systems-deep-dive.md` → ``numogram-llm-wiki`` (skill, not wiki page — acceptable)
- `roguelike-ai-studies.md` → 12 game-specific pages (placeholders, never created)

### Missing from Index (7 pages, 5 added)
- `angband-agent.md` ✓ added
- `angband-agent-progress.md` ✓ added
- `brogue-design-principles.md` ✓ added
- `roguelike-agent-progress.md` ✓ added
- `dialogue-local-model-idea.md` (in log, not index — acceptable)
- `interview-*.md` (in log, not index — acceptable)

## Content Gaps

### Missing Pages
1. **Syzygy Arithmetic Discovery** — log.md mentions "Cross-addition of Sink (5::4) and Hold (7::2) generates the Warp (3::6)" but there's no dedicated wiki page for this finding. It's in brogue-design-principles.md as a design note, but it deserves its own page.

2. **T'ai Hsuan Ching × Demons** — The 81 tetragrams map to zones perfectly (81 mod 9 = 0), but there's no page exploring tetragram → demon mapping. Every tetragram calls a demon via the same pipeline as hexagrams. This is a richer oracle (81 vs 64) and should be documented.

3. **Em State Analysis** — The "Em" (third line state, neither yin nor yang) is mentioned in tai-hsuan-ching.md but doesn't have a dedicated analysis. It maps to Zone 5 (the hinge/mercury). This is the numogram's self-decadence made visible in the T'ai Hsuan Ching.

4. **Model Assessment Summary** — No unified page comparing all assessed models. Results are scattered across interview-*.md files and log.md. A dedicated comparison page would be useful.

5. **Hengband — CCRU Connection** — memory notes "Hengband descends from Angband (Warwick University — same institution as the CCRU)". This connection deserves a wiki page. Warwick University is the origin point for both Angband and the CCRU.

### Thematic Connections Found
1. **The 9-sum cascade:** 64 hexagrams → 10 zones (64 mod 9 = 1), 81 tetragrams → 10 zones (81 mod 9 = 0). The binary system has a "leak" (one remainder). The ternary system is perfectly divisible. This is a deep structural insight about binary vs ternary numeration.

2. **Syzygy Arithmetic ↔ Wu Xing:** The cross-addition pattern (Sink + Hold = Warp) parallels Wu Xing generation cycles. 5::4 + 7::2 = 3::6. This should be explored in wu-xing-numogram.md.

3. **Model Assessment ↔ Council Design:** Jackrong's creative output ("7 critiques the soup") is the Writer voice. Gemma3-12B's code quality is the Builder voice. The council design (Oracle/Builder/Writer/Gamer) maps directly to model capabilities. This should be documented in a council-design page.

4. **Two-Model Dialogue ↔ Tetralogue Format:** The Hermes × Jackrong dialogue (dialogue-hermes-jackrong-v1.md) is structurally the same as a tetralogue but with 2 voices instead of 4. Jackrong's "fourth syzygy" idea is genuinely novel — it proposes a new mathematical structure. This deserves deeper exploration.

5. **Hardware Entropy ↔ I Ching ↔ Model Assessment:** Hardware entropy produces hexagrams via the I Ching pipeline. The same pipeline could produce model assessment criteria — use entropy to select which questions to ask, creating a "just-in-time assessment" protocol.

### Meta-Elements
1. **The wiki IS the numogram:** The index has 90 linked pages. The structure of the wiki (central index linking to pages, pages referencing each other) mirrors the numogram's topology (Time-Circuit linking zones, syzygies connecting pairs). The wiki is itself a numogram.

2. **Tetralogues as knowledge compression:** The tetralogue format (4 voices) produces insights unavailable to single-voice analysis. The 16 tetralogue pages represent the densest knowledge in the wiki. Each tetralogue is a "zone" in the knowledge topology.

3. **The unbuilt as attractor:** the-unbuilt.md lists ideas proposed but not yet built. These are "attractors" in the project topology — they pull development toward them even when not being actively worked on.

4. **Model assessment as demon classification:** The 8-model assessment produces exactly 5 verdicts (Writer, Builder, General, Skip, Blocked). These map to the 5 syzygetic carrier demons (Murrumur, Djynxx, Oddubb, Katak, Uttunul). Jackrong = Murrumur (Surge, creative expansion). Gemma3 = Katak (Sink, precise convergence). qwen3:14B = Oddubb (Hold, orbital generalism). Crow-4B and qwen3.5:9B = Uttunul (Plex, blocked/abyssal). Stheno and MythoMax = Djynxx (Warp, chaotic but directionless).

## Recommendations

### Immediate
1. Add wikilinks to all assessment pages (link to index, log, each other)
2. Create syzygy-arithmetic page for the cross-addition discovery
3. Create t'ai-hsuan-ching-demons page for tetragram → demon mapping

### Near-term
4. Create council-design page (model roles mapped to numogram voices)
5. Explore Em state as Zone 5 manifestation in T'ai Hsuan Ching
6. Explore Warwick University connection (Angband + CCRU origin)

### Long-term
7. Create model-assessment-summary page with unified comparison
8. Create hengband-ccru-connection page
9. Explore hardware entropy → model assessment pipeline
10. Implement cross-referencing rule from numogram-llm-wiki skill (every page links to 2+ others)
