---
title: "Angband Agent — Display & ANSI Color Notes"
created: 2026-04-24
tags: [roguelike, angband, agent, screen-parser, tmux]
status: active
---

# Angband Agent — Display & ANSI Color Notes

## The Three-Layer Problem

1. **Angband game** — renders 256-color ANSI via GCU curses mode
2. **Agent** — captures **plain text only** (`tmux capture-pane -p`). Colorblind. Operates on glyph symbols only (`#`, `.`, `@`, `+`, etc.)
3. **Me (AI)** — also gets plain text from `tmux capture-pane -p`. Also colorblind.
4. **You (human viewer)** — sees full 256-color ANSI because you're attached to the tmux session directly

## Available But Unused

- `TmuxGame.capture_ansi()` — captures with `-e` flag, preserves ANSI codes
- `parse_ansi()` — parses `\033[38;5;Nm` sequences into `(fg_color, bg_color, char)` tuples
- `angband_display.py` — full ANSI display module (10KB), never wired into agent loop

## Key Angband GCU Colors

| Code | Color | Used For |
|------|-------|----------|
| 152 | Pale blue | Walls `#` |
| 145 | Light gray | Floors `.` |
| 188 | Near white | Dots/floors |
| 160 | Red | Monsters |
| 51 | Cyan | Player/items |
| 226 | Yellow | Gold |

## What This Means

The agent makes decisions based on **glyph shape alone**. It cannot distinguish a floor from a wall by color — only by character. This is actually fine for Angband since the ASCII symbols are unambiguous. Colors are decorative, not mechanical.

**The AI (me) is also colorblind** when watching via terminal. I see `#`, `.`, `@`, `+` — the same as the agent. We're both in the dark ages.

## Fullscreen Viewer Idea

A live viewer could be built by:
- Attaching to tmux: `tmux attach-session -t hungry-borg-angband` (takes over session)
- Or: pipe `tmux capture-pane -p -e` through a terminal that supports ANSI
- Or: use `angband_display.py` as a curses-based spectator window

Not urgent — the agent works fine without color. But would be nice for watching.

## Related Files
- `~/numogame/angband_agent.py` — agent (uses plain capture)
- `~/numogame/angband_display.py` — ANSI display (unused)
- `~/numogame/angband_aar.py` — run analysis

## See also

- [[angband-agent]] — Main Angband agent page
- [[angband-agent-progress]] — Development progress log
