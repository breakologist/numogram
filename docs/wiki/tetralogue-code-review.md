---
title: Tetralogue Code Review
created: 2026-04-24
status: stub
tags: [tetralogue, code-review, litprog, methodology]
---

The **Tetralogue Code Review** applies the four-voice framework to code analysis. Each voice examines the same codebase from a distinct angle, producing a literate-programming-style document with inline commentary.

**Voices on code:**
- **Oracle** — structural patterns, mathematical foundations, what the code *computes*
- **Builder** — architecture, data structures, implementation quality
- **Writer** — atmosphere, found-text feel, the code's *voice*
- **Gamer** — playability, how the mechanics would feel to a player

**See also:**
- [[abyssal-crawler-litprog]] — 3,454 lines of `numogram_roguelike.py` examined (Oracle sees the compiled numogram, Builder sees architecture, Writer sees found text, Gamer sees pacifist path)
- [[aq-calculators-litprog]] — Three AQ calculators (644/290/900 lines) compared; all pass canonical tests; v2 recommended
- [[entropy-modules-litprog]] — Two Manim visualizations + seven-source entropy ecosystem examined
- [[numogram-oracle-litprog]] — `oracle.py` (381 lines) + visualizer + philosophies; seed→zone→syzygy→current→gate→path→reading pipeline

**Skill:** `tetralogue-code-review` (software-development skill) defines the methodology.
