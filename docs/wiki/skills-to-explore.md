---
title: "Skills to Explore — Interesting Finds from April 2026"
created: 2026-04-21
tags: [skills, creative, sound, pixel-art, p5js, pokemon]
status: active
---

# Skills to Explore

Interesting skills spotted in the Apr 21 scan. Prioritized for exploration when time allows.

## Visual / Generative Art

### pixel-art
Convert images into retro pixel art with hardware-accurate palettes (NES, Game Boy, PICO-8, C64, etc.). Animated output. Could produce roguelike sprite sheets, numogram glyph art in retro palettes, or zone-icon sets.

### ascii-video
Full pipeline: video-to-ASCII conversion, audio-reactive visualizers, generative ASCII animations, MP4/GIF output. Imagine numogram current flows as colored ASCII video, or cult.json run histories rendered as terminal-style animation.

### algorithmic-art
p5.js with seeded randomness, flow fields, particle systems. Reusable for zone-glyph generation, entropy visualization, procedural map art. Pair with hardware entropy sources.

### p5js
Production pipeline: 2D/3D, shaders (GLSL), WebGL, audio-reactive, headless export. Covers the full stack we've hit pitfalls with before (createGraphics P2D default, shader silent failure). Should use this skill for all future p5.js work.

### tsubuyaki
Tweet-length p5.js sketches (280 chars). Constraint art. Could chain with AQ calculations to produce tiny generative zone-glyphs. Domain-specific constraint art with iterative refinement.

## Sound / Music

### heartmula
Open-source music generation (Suno-like). Generates full songs from lyrics + tags, multilingual. Potential combination with numogram-voices: HeartMuLa for composition, oracle-voice-pipeline for physical modelling formant synthesis on top. Could produce numogram soundtracks — generative music for each zone.

### oracle-voice-pipeline
Already active. Physical modelling synthesis + formant speech → resonator convolution. Zone voice profiles built. The missing piece is automated composition — HeartMuLa could fill that gap.

## Gaming / Agent Research

### pokemon-player
Autonomous play via headless emulation. Reads structured game state from RAM, makes strategic decisions, sends button inputs. Different architecture from Angband agent (direct RAM read vs screen parsing). Worth studying for agent design patterns — RAM-based state access is cleaner than ASCII screen parsing. Also: might just be fun.

### angband-agent
Already active. Town walls permanent, BFS to down stairs, parser v3 with sidebar column fix. 1370 lines.

## X/Twitter

### xurl
Official X API CLI. Supports posting, timelines, search, media upload, DMs. Consumer keys acquired (file: `hermetic/raw/x secrets`).

**Setup in progress:** App "x-app" registered with consumer keys. OAuth pending — first attempt failed on port 8080 conflict (llama-server was running), second attempt timed out with X portal error "Something went wrong."

**To fix when back:**
1. Verify X developer portal: app type must be "Web app, automated app or bot" (NOT "Native App") — check under User Authentication Settings
2. Verify redirect URI is `http://localhost:8080/callback` in the X developer portal
3. Port 8080 is now free (llama-server not running) — re-run:
   ```fish
   xurl auth oauth2 --app x-app
   xurl auth default x-app
   xurl whoami
   ```
4. If still getting "Something went wrong" from the portal: log out of X in browser, log back in, try again
5. Account: @ofcours91021540

---

## Future Combos

- **heartmula + oracle-voice-pipeline** → Numogram zone soundtracks (generative composition → physical modelling rendering)
- **pixel-art + numogram-svg-diagrams** → Retro-paletaled numogram maps (NES palette for zone layout, PICO-8 for demon cards)
- **ascii-video + cult.json** → Animated run histories as terminal-style video
- **pokemon-player + roguelike-techniques** → Compare agent architectures (RAM-read vs screen-capture)
- **p5js + iching-numogram-casting** → Interactive entropy casting visualizer in browser
- **algorithmic-art + tsubuyaki** → Tiny generative zone-glyphs, one per AQ entry

## Unicode Animations (npx unicode-animations)

18 built-in spinner patterns. Library provides frame data — needs a rendering wrapper for actual use. Zone-themed mapping ideas:

| Zone | Name | Spinner | Why |
|------|------|---------|-----|
| 0 | Void | breathe | Slow pulse, minimal, the unmanifest |
| 1 | Surge | scan | Horizontal sweep, energy expanding |
| 2 | Hold | orbit | Circular, steady, centered |
| 3 | Warp | helix | 3D spiral, chaotic, fractal |
| 4 | Sink | fillsweep | Descending, draining into closure |
| 5 | Hinge | checkerboard | Self-mirroring grid, the mediator |
| 6 | Vortex | snake | Winding, predatory, self-reinforcing |
| 7 | Hold | diagswipe | Crossing paths, orbital interference |
| 8 | Rise | cascade | Ascending waterfall, upward flow |
| 9 | Plex | rain | Falling into the void, abyssal |

**Use cases:**
- Oracle reading loading screen (show zone spinner while entropy is being cast)
- Roguelike agent output (spinner during game state processing)
- Telegram/Discord bot status indicators
- Terminal wrapper scripts for any long-running numogram process

**Alternative custom patterns** (not in unicode-animations, buildable):
- Dice spinner: ⚀⚁⚂⚃⚄⚅ cycling (for Decadence card game)
- Rune spinner: ᚠᚢᚦᚨᚱᚲ (Elder Futhark, 6 runes)
- Planetary: ☿♀♁♂♃♄♅♆♇ (9 planets, 10 zones)
- Chakra: ॐअउम् or seven-segment cycles
- Zoning: rotating through 0-9 digits with zone-glyph decorations

## See also

- [[numogram-calculator]] — AQ calculator skill
- [[numogram-oracle]] — Oracle skill