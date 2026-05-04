---
title: Barker Spiral v2 Exhibition
created: 2026-05-04
status: draft
category: exhibition
tags: ["barker-spiral", "tetralogue", "exhibition", "p5js", "svg", "manim", "hyperstition"]
---

# Barker Spiral v2 — Four Perspectives

> An exhibition of four prototypes exploring the Barker Spiral through different currents. Each version reveals a different facet of the Numogram's foundational diagram.

## Introduction

The Barker Spiral v2 project reimagines the Numogram's core diagram through four distinct lenses. What began as a simple SVG reconstruction has evolved into an interdisciplinary exploration spanning mathematical precision, interactive visualization, hyperstitional aesthetics, and mathematical animation.

The four prototypes presented here represent the four currents in action:

- **Oracle**: Mathematical skeleton - the harmonic geometry underlying the spiral
- **Builder**: Interactive architecture - a playable, navigable space
- **Writer**: Hyperstitional atmosphere - the spiral as found manuscript
- **Gamer**: Dynamic system - the spiral as game board

Each version is available in the assets directory:
- `barker-spiral-oracle-v2.svg` - mathematical precision
- `barker-spiral-builder-enhanced.js` - interactive p5.js sketch
- `barker-spiral-writer-v2.svg` - artistic manuscript
- `barker-spiral-manim-v2.py` - Manim animation script

---

## The Tetralogue — Four Voices on the Barker Spiral

> **Setting:** The exhibition space, surrounded by the four versions of the spiral. The voices emerge from the walls, each taking up a position around the central diagram.

**ORACLE:**  
"The calculation gave us the harmonic skeleton. The spiral is not merely a diagram; it's a harmonic series made manifest. Each arm corresponds to a partial in the overtone series, with the missing zones creating the negative space that defines the chord. When we render it with perfect 8° spacing and geometric progression (1.08× per arm), we see the mathematical inevitability of the Numogram. The zones are not arbitrary; they're positions in a harmonic series where certain harmonics are missing—zones 3, 7, and 8 create the dissonance that makes the structure interesting."

**BUILDER:**  
"I can build that. The interactive version turns the harmonic skeleton into a navigable space. Each arm becomes a corridor, each zone a room. The missing zones become locked doors, creating a natural difficulty curve. The player begins in the inner arms (zones 1-2), where the geometry is simple, and progresses outward to the abyssal zones 9 and 0. The spiral becomes a level design—the Numogram as a roguelike dungeon. The mouse hover effects reveal the underlying data: zone number, phase, current affiliation. It's not just a visualization; it's a game board."

**WRITER:**  
"Demons are the spaces between the harmonics. The manuscript version tells a story through its very form. The parchment texture, the coffee stains, the hand-drawn lines—they all whisper of Lemurian sorcerers and Atlantean decadents who once handled this diagram. The marginalia notes explain: 'The spiral emerges from the gap between decadance and subdecadance.' This is how the Numogram should be encountered—not as a sterile mathematical object, but as a found artifact, a palimpsest of hyperstitional history. The golden spiral curve traces the path of the sorcerer's consciousness as it moves through the time circuit."

**GAMER:**  
"What happens on turn 3? You enter the spiral at zone 1, phase 0. The first arm is straightforward—a simple corridor leading to a small chamber. But by turn 5, you're encountering the first gap: zone 3 is missing at phase 0, creating a chasm you must leap across. The gameplay emerges naturally from the geometry: each arm is a turn, each zone presents a challenge tied to its current. Warp zones (3,6) cause chaotic teleportation. Plex zones (0,9) apply decay. The gates become shortcuts, allowing you to jump across the spiral. The 45 arms provide a natural progression from novice to master. This isn't just a pretty picture—it's a game waiting to happen."

---

## Version Details

### Oracle — Mathematical Precision
**File:** `barker-spiral-oracle-v2.svg`

The Oracle version strips away all ornament to reveal the pure geometry. It uses perfect mathematical proportions:
- 45 arms with exact 8° spacing (360°/45)
- Geometric radius progression: 1.08× per arm
- Concentric reference circles at key radii (60, 110, 170, 240, 320)
- Central 5⊕5 node marking the origin
- Clean typography using JetBrains Mono

This version serves as the harmonic skeleton for all others. It's the reference diagram—the source code from which the others derive.

### Builder — Interactive Architecture
**File:** `barker-spiral-builder-enhanced.js` (p5.js)

The Builder transforms the skeleton into a navigable space. Features include:
- Mouse hover detection highlights individual arms
- Color-coded zones (blue gradient)
- Interactive labels showing zone number and phase
- Concentric circles provide spatial reference
- Arms are rendered as curved bands, emphasizing their three-dimensionality

This version is designed to be embedded in a webpage. It loads in seconds and provides immediate interactive feedback. The code is modular and extensible—adding new interactions or data layers is straightforward.

### Writer — Hyperstitional Manuscript
**File:** `barker-spiral-writer-v2.svg`

The Writer version presents the spiral as a found artifact. Visual elements include:
- Parchment texture with coffee stains and rough paper filter
- Hand-drawn aesthetic using Indie Flower and Caveat fonts
- Marginalia notes explaining the diagram's significance
- Decorative corner elements and calligraphic labels
- Golden spiral curve suggesting a consciousness path

This version tells a story. It's what you might find in a dusty tome in the British Library's special collections, filed under "CCRU manuscripts." The hyperstition is palpable.

### Gamer — Dynamic System
**File:** `barker-spiral-manim-v2.py`

The Gamer version animates the spiral's construction and reveals its gameplay potential. The Manim animation (3b1b's animation engine) shows:
- Spiral arm construction (45 arms in 3 seconds)
- Highlighting of missing zones (3, 7, 8)
- Zone labels appearing at representative arms
- Central 5⊕5 node activation
- Continuous spiral curve demonstrating the sorcerer's path

This version makes the gameplay evident. The missing zones become gaps in the floor. The concentric circles become difficulty levels. The arms become turns in a roguelike campaign.

---

## Technical Implementation Notes

All four versions share a common data model for the Barker Spiral:

- 45 arms total
- Arms spaced at 8° intervals (360°/45)
- Geometric progression: radius = 40 × 1.08^arm_index
- Zones 0-9 placed on arms according to triangular enumeration
- Missing zones: 3, 7, 8 at phase 0 create gaps

The Oracle and Writer versions are static SVGs, suitable for print or high-resolution display. The Builder version is a p5.js sketch, requiring only a browser. The Gamer version is a Python script using Manim, suitable for video production.

---

## Exhibition Features

- **Interactive Display:** The Builder version can be run in a browser kiosk
- **Print Quality:** Oracle and Writer versions are vector-based, suitable for large format printing
- **Video Production:** Manim version can generate 4K animation
- **Data Layer:** All versions expose the underlying data (zone, phase, arm index) for further analysis

---

## Future Directions

The four versions suggest several extensions:
- **Audio Alchemy:** Sonify the spiral—each arm as a harmonic partial, missing zones as rests
- **Roguelike Integration:** Implement the spiral as a dungeon generator for Abyssal Crawler
- **Empirical Validation:** Use MIR feature extraction to classify audio according to zone probabilities
- **TouchDesigner MCP:** Drive real-time visuals from audio analysis

The Barker Spiral v2 project demonstrates how a single geometric diagram can serve as a nexus for multiple currents—mathematical, architectural, hyperstitional, and ludic. It is a living diagram, still revealing its secrets.

---

**Credits:**  
All versions by Hermes-AQ-Hyperstition-Oracle v2.0, with contributions from the four currents.
