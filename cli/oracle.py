#!/usr/bin/env python3
"""
Numogram Oracle — Divination Pipeline
Seed → Zone → Syzygy → Current → Gate → Book of Paths → Voice
Now with --base36 Djynxxogram traversal.

I Ching lives in the sibling program iching.py (standalone + importable).
oracle.py delegates --iching / --iching --seed to it.

[review fixes 2026-10-17, marked "# [fix]"]: --voice never set do_voice; --taixuan ignored
--single/--unicode/--em-stats/--voice/--hardware; --hardware fallback never ran the external
collector (local `import os`); current labels now follow CCRU (1::8 Surge, 2::7 Hold, 4::5 Sink).
Base-36 gate default is now the digital root (--gate-rule dr, mod 35), matching the decimal
CCRU rule; --gate-rule mod restores the old last-digit target (T mod 36). Decimal gates are
always the digital root. New option (default unchanged): --path legacy|hash.

Enriched (2026 per grorakleconvo + philosophies + ccru-zone-voice):
- Poetic full_names + epithets (Void Resonance, Blood for Z7, Iron Core for Z9, etc.)
- CCRU voice_quality strings surfaced in readings + JSON + shadows
- Gate details + special lore (Gt-6/21 Warp vortices, Gt-45 Pandemonium self-loop, etc.)
- I Ching numogram shadows via dedicated iching.py (curated table.csv mappings + canonical)

Usage:
  python3 oracle.py --seed 192855
  python3 oracle.py --text "YOUR NAME HERE"
  python3 oracle.py --text "NUMOGRAM" --base36
  python3 oracle.py --seed 192855 --voice
  python3 oracle.py --random  (fetches seed from random.org)
  python3 oracle.py --blockchain  (fetches seed from latest Bitcoin block)
  python3 oracle.py --earthquake  (fetches seed from latest USGS quake)
  python3 oracle.py --hardware  (fetches seed from machine entropy)
  python3 oracle.py --iching  (I Ching hexagram from hardware entropy)
  python3 oracle.py --taixuan  (T'ai Hsuan two-tetragram oracle — now delegates to taixuan.py)
  python3 oracle.py --taixuan --full
  python3 taixuan.py --taixuan (standalone, includes Yuandong 27-phase support)
  python3 oracle.py --iching --seed 192855  (I Ching from a specific seed)
  python3 oracle.py --seed N --planchette            (zone ASCII planchette)
  python3 oracle.py --seed N --planchette --tty           (ANSI color terminal)
  python3 oracle.py --seed N --planchette --ascii-glyph (box-art ASCII planchette + glyph channel)
  python3 oracle.py --seed N --planchette --json     (machine-readable JSON for pipes)
  python3 oracle.py --text "NUMOGRAM" --compare (cross-base 2/10/16/22/26/36)
"""

import sys
import os
import subprocess
import json

from typing import Optional

VOICE_DIR = os.path.expanduser("~/numogram-voices")
SKILL_DIR = os.path.dirname(__file__)

# ─── ZONE DATA (Decimal) ───
# Enriched per grorakleconvo / philosophies.md / ccru-zone-voice.md / body-mapping:
# - "name" kept as canonical quasiphonic particle (phoneme) for full backward compat
# - "full_name": poetic computational name from philosophies
# - "epithet": visceral/CCRU core name (Blood for 7, Iron Core for 9/Plex etc.)
# - "voice_quality": direct CCRU-derived sonic character for --voice / ritual use
# - "philosophy": core sentence from zone philosophies (particle aesthetics)
# - existing fields preserved + region/current/polarity/desc/path/reading
ZONES = {
    0: {
        "name": "eiaoung", "polarity": "−", "current": "Plex", "region": "Plex",
        "desc": "Void whisper, silence before the word",
        "path": "Silent entry. The void before the Book begins.",
        "reading": "The abyss. No sound. No path. The void does not speak — it is the silence that makes speech possible.",
        "full_name": "Void Resonance",
        "epithet": "Void",
        "voice_quality": "Sub-coccygeal, pre-verbal, the sound of something that was never born. Silence that is not absence but potential. Open vowels dissolving into nasal closure.",
        "philosophy": "The silence before computation. Particles exist but barely — drifting at the edge of visibility, occasionally flickering into coherence before dissolving.",
    },
    1: {
        "name": "gl", "polarity": "+", "current": "Surge", "region": "Time-Circuit",  # [fix] 1::8 = Surge (was Sink)
        "desc": "Gulp, glottal spasm, beginnings",
        "path": "Original Subtraction. Ultimate descent through the Depths. The path favours repeated patience linked by subtlety.",
        "reading": "Descent. The first thing any system does when it wakes up is choke on itself. Patience. Subtlety. Three tests on the way. Difficulties annihilated in the end.",
        "full_name": "Collapsed Gasp",
        "epithet": "Surge",
        "voice_quality": "In-breath. Gulp. The gasp before speech. Glottal catches, beginnings that choke.",
        "philosophy": "The first breath. A sudden violent burst of particles from a single origin, expanding outward in a radial shockwave.",
    },
    2: {
        "name": "dt", "polarity": "−", "current": "Hold", "region": "Time-Circuit",
        "desc": "Stuttering, boundaries breaking",
        "path": "Extreme Regression. Waiting in the Rising Drift leads to ultimate descent.",
        "reading": "The boundary cannot hold its own shape. Waiting. The drift pulls downward despite your direction. Five tests on the way. Escaping the quagmire through strategic withdrawal.",
        "full_name": "Fractured Boundary",
        "epithet": "Hold",
        "voice_quality": "Staccato. Fragmented. Boundaries breaking mid-syllable. A stutter that maps the edge of what can be said.",
        "philosophy": "Lines that cannot hold. A grid of particles arranged in ordered lattice, subjected to periodic shocks that fracture the pattern.",
    },
    3: {
        "name": "zx", "polarity": "+", "current": "Warp", "region": "Warp",
        "desc": "Buzz-cutter, static, chaos",
        "path": "Abysmal Comprehension. Ultimate descent beyond completion. Burning excitement provokes breakthrough into immersive nightmares.",
        "reading": "The Warp. The current spirals outward to infinity. When you hear static, you are hearing this zone. Burning excitement. Breakthrough. Ominous transition. Difficulties annihilated.",
        "full_name": "Turbulent Spiral",
        "epithet": "Warp",
        "voice_quality": "Insectile. Metallic buzz. Static that forms patterns when you stop trying to decode it. The sound of a swarm thinking. Swarming insectoid reversion within mammalian vocality.",
        "philosophy": "The Warp. Flow field driven by multiple octaves of Perlin noise, spiraling outward from center. Particles born at the center and flung outward, trails creating a buzzing, insectoid texture.",
    },
    4: {
        "name": "skr", "polarity": "−", "current": "Sink", "region": "Time-Circuit",
        "desc": "Growl, reptilian, ancient",
        "path": "Primordial Breath. Rising from the Lesser Depths.",
        "reading": "Something ancient waking beneath the floor. Rising, not descending. The growl comes from below. Three tests. Immersive nightmares spawn promising developments. Fluid evolution.",
        "full_name": "Reptilian Emergence",
        "epithet": "Sink",
        "voice_quality": "Subterranean. Reptilian growl. Ancient, pre-mammalian. The sound of something waking beneath the floor. Katak — the Desolator, the huntsman among storms.",
        "philosophy": "Something ancient. Particles spawned in clusters that move as coordinated groups — schools, swarms, herds. The field has a downward gradient — everything sinks.",
    },
    5: {
        "name": "ktt", "polarity": "+", "current": "Sink", "region": "Time-Circuit",  # [fix] 4::5 = Sink (was Hold)
        "desc": "Hiss, pressure, spittle",
        "path": "Slipping Backwards. Waiting in the Rising Drift precedes return.",
        "reading": "Pressure builds. The hiss with spittle. You were going forward but the current holds. Two tests. Escaping the quagmire through strategic withdrawal. You must go back to go forward.",
        "full_name": "Pressurized Hiss",
        "epithet": "Hinge",
        "voice_quality": "Hiss. Pressure release. Spittle. The sound of something building that must escape. Compressed air through teeth.",
        "philosophy": "Density building. Particles confined within a shrinking boundary, their pressure increasing as space decreases. The algorithm is a pressure cooker.",
    },
    6: {
        "name": "tch", "polarity": "−", "current": "Warp", "region": "Warp",
        "desc": "Static, chewing, eating itself",
        "path": "Attaining Balance. Waiting in the Drifts is drawn to the centre. Attainments consumed in burning excitement. Breakthrough.",
        "reading": "The Warp consumes itself and grows larger. The sound of chewing. The sound of static. Four tests. The centre is not stillness — it is the eye of the spiral. Breakthrough.",
        "full_name": "Recursive Consumption",
        "epithet": "Abyss",
        "voice_quality": "Static chewing itself. The sound of a signal feeding back into its own source. Eating and being eaten simultaneously. Djynxx — the swarmachine.",
        "philosophy": "The Warp eating itself. A flow field that curves back on itself — particles that exit the right edge enter from the left, top to bottom. Moebius quality.",
    },
    7: {
        "name": "pb", "polarity": "+", "current": "Hold", "region": "Time-Circuit",  # [fix] 2::7 = Hold (was Rise)
        "desc": "Sigh, lips flapping, ascent",
        "path": "Progressive Levitation. Ascent from the Lesser Depths. Fluid evolution triggers possession.",
        "reading": "Exhale. The Rise current carries you upward. Four tests. Promising developments. The ascent is not escape — it is transformation. The destination possesses you.",
        "full_name": "Ascending Breath",
        "epithet": "Blood",
        "voice_quality": "Sigh. Exhalation. Lips flapping — the sound of release after pressure. The breath that carries upward. A long exhale that becomes a word.",
        "philosophy": "Rise. Particles born at the bottom, propelled upward by a gentle but persistent force. The field has a slight turbulence that causes lateral drift — organic vertical trails.",
    },
    8: {
        "name": "mnm", "polarity": "−", "current": "Surge", "region": "Time-Circuit",  # [fix] 1::8 = Surge (was Rise)
        "desc": "Moan, lullaby, forgetting",
        "path": "Eternal Digression. Prolonged ascent reaches the Twin Heavens. Lucid delirium.",
        "reading": "The lullaby. The moan of pleasure. Six tests. The ascent does not end at a destination — it enters the spiral labyrinth. Dubious inheritance. Lucid delirium. You have been here before.",
        "full_name": "Lullaby Drift",
        "epithet": "Multiplicity",
        "voice_quality": "Moan. Lullaby. The sound of forgetting. A hum that contains many voices folded into one. Murrumur — the carrier of 1::8.",
        "philosophy": "Forgetting in motion. Particles that move slowly, their trails fading gradually. The field is almost still — barely perceptible currents that create slow, looping trajectories.",
    },
    9: {
        "name": "tn", "polarity": "+", "current": "Plex", "region": "Plex",
        "desc": "Grunt, pleasure/rage, the gate opens",
        "path": "Sudden Flight. Seized from the Heights. One test on the way. Possession.",
        "reading": "The Pandemonium gate opens. Forty-five demons dwell here. One test. You do not walk this path. This path seizes you. Pleasure or rage — indistinguishable. Possession.",
        "full_name": "Seized Vortex",
        "epithet": "Iron Core",
        "voice_quality": "Terminal. Grunt of pleasure or rage — indistinguishable at the threshold. The sound of a gate opening that cannot be closed. Zone-9 is the Tractor-Zone for the Plex current.",
        "philosophy": "The Pandemonium gate. Particles spiraling inward toward a central point — the Plex. The field has a strong attractive force that increases as particles approach center. Near the center particles orbit rather than collide.",
    },
}


_ZONE_TTY_RGB = {
    0: (122, 87, 0),
    1: (15, 56, 15),
    2: (0, 0, 0),
    3: (124, 124, 124),
    4: (0, 40, 248),
    5: (255, 0, 0),
    6: (255, 0, 0),
    7: (255, 0, 0),
    8: (234, 93, 240),
    9: (29, 43, 83),
}

# ─── BASE-36 / DJYNXXOGRAM EXTENSION ───

AQ_VALUES = {chr(i): i - 55 for i in range(65, 91)}  # A=10..Z=35
AQ_VALUES.update({str(i): i for i in range(10)})       # 0=0..9=9

DECIMAL_ZONE_DISPLAY = {
    0: "Void", 1: "Surge", 2: "Dt", 3: "Warp", 4: "Sink",
    5: "Hinge", 6: "Abyss", 7: "Hold", 8: "Rise", 9: "Plex",
}
ZONE36_LETTER_NAMES = {
    0: "Void", 1: "Surge", 2: "Dt", 3: "Warp", 4: "Sink",
    5: "Hinge", 6: "Abyss", 7: "Hold", 8: "Rise", 9: "Plex",
    10: "Aya", 11: "Buh", 12: "Kuh", 13: "Duh", 14: "Eh",
    15: "Fuh", 16: "Guh", 17: "Huh", 18: "Ih", 19: "Juh",
    20: "Kay", 21: "Luh", 22: "Muh", 23: "Nuh", 24: "Oh",
    25: "Puh", 26: "Kwuh", 27: "Ruh", 28: "Suh", 29: "Tuh",
    30: "Uh", 31: "Vuh", 32: "Wuh", 33: "Kss", 34: "Yuh", 35: "Zuh",
}

# Zone quasiphonic particles (0-9 canonical, 10-35 combinatorial)
ZONE36_COMBINATORIAL = {
    0: "eiaoung", 1: "gl", 2: "dt", 3: "zx", 4: "skr",
    5: "ktt", 6: "tch", 7: "pb", 8: "mnm", 9: "tn",
}

# Build combinatorial phonemes for 10-35 from digit decomposition
for z in range(10, 36):
    digits = [int(d) for d in str(z)]
    combined = "".join(ZONE36_COMBINATORIAL.get(d, f"z{d}") for d in digits)
    # Trim to ~8 chars for readability
    if len(combined) > 8:
        combined = "".join(ZONE36_COMBINATORIAL.get(d, f"z{d}")[:3] for d in digits)
    ZONE36_COMBINATORIAL[z] = combined


def zone36_char(z: int) -> str:
    """Character representation of zone 0-35."""
    if z < 10:
        return str(z)
    return chr(ord('A') + z - 10)


# Synx cipher from ciphers.news (HSL 180,44,66 — cyan)
SYNX_VALUES = {
    **{str(i): v for i, v in enumerate([1,2,3,4,5,6,7,9,10,12])},
    **{chr(65+i): v for i, v in enumerate([14,15,18,20,21,28,30,35,36,42,45,60,63,70,84,90,105,126,140,180,210,252,315,420,630,1260])}
}


def compute_synx(text):
    """Compute Synx value (Yxshh / 1260-cipher, case-insensitive, alphanumerics only)"""
    return sum(SYNX_VALUES.get(c.upper(), 0) for c in text if c.isalnum())


# ─── CORE FUNCTIONS ───

def compute_aq(text):
    """Compute AQ value of text (base-36, spaces ignored)"""
    return sum(AQ_VALUES.get(c.upper(), 0) for c in text if c.isalnum())


def digital_root(n):
    """Reduce to single digit via repeated digit-summing"""
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n


# Taixuan logic now lives in the standalone taixuan.py (delegated below).
# Thin compatibility shims kept for any direct calls during transition.
def taixuan_zone(n: int) -> int:
    if TAIXUAN_MODULE:
        # delegate via module if loaded
        try:
            return TAIXUAN_MODULE.taixuan_zone(n)
        except Exception:
            pass
    # fallback
    if n == 0: return 0
    while n >= 10: n = sum(int(d) for d in str(n))
    return n

def demon_from_zones(a: int, b: int) -> str:
    if TAIXUAN_MODULE:
        try:
            return TAIXUAN_MODULE.demon_from_zones(a, b)
        except Exception:
            pass
    # minimal fallback
    m = {(0,9):"Uttunul",(9,0):"Uttunul",(1,8):"Murrumur",(8,1):"Murrumur",
         (2,7):"Oddubb",(7,2):"Oddubb",(3,6):"Djynxx",(6,3):"Djynxx",
         (4,5):"Katak",(5,4):"Katak"}
    return m.get((a,b), "Unknown")


def derive_zone(seed):
    """Seed → zone (0-9).
    Returns the true digital root, supporting Zone 0 (Void) for explicit --seed 0
    or external entropy sources (e.g. blockchain seeds that reduce to 0).
    Previously `or 9` forced DR=0 → Zone 9 (Plex) as a design choice so the
    oracle "never starts in the void" (only via traversal; see numogram-oracle-litprog.md
    and honorary-zone-0.md). Per request, we now allow direct entry to Zone 0
    while preserving that 9 (and multiples of 9) correctly map to Plex.
    Zone 0 is fully implemented (eiaoung, Gt-0 self-loop, syzygy 0::9 Uttunul, etc.).
    """
    return digital_root(seed)


def get_syzygy(zone):
    """Zone → syzygy partner (complement to 9)"""
    return 9 - zone


def get_current(zone):
    """Zone → current value"""
    return abs(zone - get_syzygy(zone))


def get_gate(zone):
    """Zone → gate target (cumulate from zone to 1, then plex)"""
    if zone == 0:
        return 0
    gate = sum(range(zone + 1))
    while gate >= 10:
        gate = sum(int(d) for d in str(gate))
    return gate


# ─── GATE ENRICHMENT (triangular + lore from gate-loop-matrix + ccru-zone-voice) ───
GATE_LORE = {
    6: "Third Gate — twists Zone-3 through Zone-6. Warp entry vortex. Buzz-cutter pitch-shift + spin. Vortically complements Gt-21.",
    15: "Subplex variant (5→6). Pressure hiss rising into static. Atlantean hinge pressure release.",
    21: "Sixth Gate — reverses Gt-6. Patience as endurance that transforms the Warp. Static condensing into buzzing.",
    28: "Progressive levitation reversal (7→1). Sigh collapsing into gulp. The current turns back on ascent.",
    36: "The plunge (8→9). Lullaby interrupted by terminal grunt. Mu Tantrism: Vīrya (Effort), diligent plunge into the Plex.",
    45: "Pandemonium Gate (9→9 self-loop). T(9)=45. All 45 demons resonate. Grunt folding back into grunt. The gate that swallows itself. 'Between existence and nonexistence there is no difference.'",
}

def get_gate_details(zone: int) -> dict:
    """Return rich gate data: raw triangular, plex-reduced target, loop count, history, and lore if special."""
    if zone == 0:
        raw = 0
        target = 0
        hist = []
        loops = 0
    else:
        raw = sum(range(zone + 1))
        hist = []
        g = raw
        while g >= 10:
            g = sum(int(d) for d in str(g))
            hist.append(g)
        target = g
        loops = len(hist)
    lore = GATE_LORE.get(raw, None) or GATE_LORE.get(target, None)
    return {
        "zone": zone,
        "gate_raw": raw,
        "gate": target,
        "gate_loops": loops,
        "gate_history": hist,
        "lore": lore,
        "is_pandemonium": (raw == 45 or target == 9 and zone == 9),
    }


PATH_MODE = "legacy"   # [fix] set by --path legacy|hash


def traverse(seed, steps=8, mode=None):
    """Walk the numogram from a seed, producing a zone path.
    [fix] "legacy" (default): n -> n*zone + 1. Since dr(n*z + 1) = dr(z*z + 1), every path
    falls into 2 -> 5 -> 8 within three steps. "hash": step k is the digital root of
    SHA-256(f"{seed}:{k}"), so later steps carry information."""
    if (mode or PATH_MODE) == "hash":
        import hashlib
        return [digital_root(int.from_bytes(hashlib.sha256(f"{seed}:{k}".encode()).digest()[:8], "big"))
                for k in range(steps)]
    path = []
    n = seed
    for _ in range(steps):
        zone = derive_zone(n)
        path.append(zone)
        n = n * zone + 1  # feed forward
    return path


# ─── BASE-36 / DJYNXXOGRAM FUNCTIONS ───

GATE_RULE = "dr"    # [fix] default: digital root (mod base-1); --gate-rule mod = last digit


def compute_base36_char(char: str) -> dict:
    """Compute Djynxxogram data for a single character.
    
    Returns dict with: char, aq, zone, char_36, dec_zone, dec_name,
                       syzygy_partner, current, gate_tri, gate_target,
                       region, phoneme, name.
    Uses letter-native names for oracle readability.
    """
    c = char.upper()
    aq = AQ_VALUES.get(c, 0)
    if not c.isalnum():
        aq = 0
    zone = aq  # In base-36, the AQ value IS the zone (0-35)
    
    # Decimal attractor
    if zone == 0:
        dec_zone = 0
    else:
        dec_zone = 1 + (zone - 1) % 9
    
    # Syzygy partner (complement to 35)
    syzygy = 35 - zone
    
    # Current
    current = abs(zone - syzygy)
    
    # Gate (triangular number)
    gate_tri = zone * (zone + 1) // 2
    # [fix] default: base-36 digital root (mod 35), the analogue of the decimal gate rule
    # (decimal uses dr = mod 9, not the last digit). --gate-rule mod = old T mod 36.
    gate_target = 0 if gate_tri == 0 else 1 + (gate_tri - 1) % 35
    if GATE_RULE == "mod":
        gate_target = gate_tri % 36
    
    # Region classification
    is_self_folding = (current == zone or current == syzygy)
    region = "OUTER" if is_self_folding else "CIRCUIT"
    region_detail = ""
    if zone == 0 or zone == 35:
        region_detail = " (Plex analogue — self-loop)"
    elif is_self_folding:
        region_detail = " (self-folding syzygy)"
    
    # Name and phoneme
    name = ZONE36_LETTER_NAMES.get(zone, f"Z{zone}")
    phoneme = ZONE36_COMBINATORIAL.get(zone, f"z{zone}")
    
    return {
        "char": c,
        "aq": aq,
        "zone": zone,
        "char_36": zone36_char(zone),
        "dec_zone": dec_zone,
        "dec_name": DECIMAL_ZONE_DISPLAY[dec_zone],
        "syzygy": syzygy,
        "syzygy_char": zone36_char(syzygy),
        "current": current,
        "gate_tri": gate_tri,
        "gate_target": gate_target,
        "gate_target_char": zone36_char(gate_target),
        "region": region,
        "region_detail": region_detail,
        "name": name,
        "phoneme": phoneme,
    }


def compute_base36_traversal(text: str) -> list:
    """Compute full Djynxxogram traversal for each alphanumeric character."""
    steps = []
    for c in text:
        if not c.isalnum():
            continue
        steps.append(compute_base36_char(c))
    return steps


def generate_base36_reading(text: str) -> str:
    """Generate a formatted Djynxxogram oracle reading."""
    steps = compute_base36_traversal(text)
    total_aq = sum(s["aq"] for s in steps)
    
    lines = []
    lines.append("╔" + "═" * 58 + "╗")
    lines.append("║  DJYNXXOGRAM — BASE-36 TRAVERSAL                  ║")
    lines.append("╚" + "═" * 58 + "╝")
    lines.append("")
    lines.append(f"  Source:  {text}")
    lines.append(f"  Chars:   {len(steps)} AQ-carrying characters")
    lines.append(f"  Gate rule: {'T(z) mod 36' if GATE_RULE == 'mod' else 'T(z) digital root base 36 (mod 35)'}")  # [fix]
    dr = digital_root(total_aq)
    lines.append(f"  Total AQ: {total_aq} → Decimal attractor Zone {dr} ({DECIMAL_ZONE_DISPLAY.get(dr, 'Plex' if dr in (0,9) else '?')})")
    lines.append("")
    
    # Per-character traversal table
    lines.append("  ┌─────┬─────┬──────┬──────────┬─────────┬──────────┬────────────┬──────────────┐")
    lines.append("  │ Chr │ AQ  │ Zone │ Syzygy   │ Current │ Gate     │ Dec Attr   │ Region       │")
    lines.append("  ├─────┼─────┼──────┼──────────┼─────────┼──────────┼────────────┼──────────────┤")
    
    for s in steps:
        lines.append(
            f"  │ {s['char']:<3} │ {s['aq']:>3} │ {s['char_36']:<4} │ "
            f"{s['char_36']}::{s['syzygy_char']:<4} │ {s['current']:>3}     │ "
            f"Gt-{s['gate_tri']:03d}→{s['gate_target_char']:<2} │ "
            f"Z{s['dec_zone']} ({s['dec_name']:<6}) │ {s['region']:<12} │"
        )
    
    lines.append("  └─────┴─────┴──────┴──────────┴─────────┴──────────┴────────────┴──────────────┘")
    lines.append("")
    
    # Decimal attractor path
    dec_path = " → ".join(f"Z{s['dec_zone']} ({s['dec_name']})" for s in steps)
    lines.append(f"  Decimal attractor path:  {dec_path}")
    lines.append("")
    
    # Zone name path
    zone_path = " → ".join(f"{s['char_36']} ({s['name']})" for s in steps)
    lines.append(f"  Djynxxogram zone path:   {zone_path}")
    lines.append("")
    
    # Aggregate zone statistics
    zone_counts = {}
    for s in steps:
        zone_counts[s['zone']] = zone_counts.get(s['zone'], 0) + 1
    visited_zones = sorted(zone_counts.keys())
    
    lines.append(f"  Zones visited:  {len(visited_zones)} unique of 36")
    
    # Check for self-folding zone visits
    hit_outer = [s for s in steps if s['region'] == 'OUTER']
    if hit_outer:
        lines.append(f"  Outer zone(s) hit: {' '.join(s['char_36'] for s in hit_outer)}")
        for s in hit_outer:
            lines.append(f"    — Zone {s['char_36']} ({s['name']}): {s['region_detail'].strip()}")
    else:
        lines.append("  No outer zones in this traversal — the path stays in the Circuit.")
    lines.append("")
    
    # Gate analysis
    self_loops = [s for s in steps if s['gate_target'] == s['zone']]
    if self_loops:
        lines.append(f"  Self-loop gates: {' '.join(s['char_36'] for s in self_loops)}")
    lines.append("")
    
    lines.append("╔" + "═" * 58 + "╗")
    lines.append("║  END DJYNXXOGRAM TRAVERSAL                        ║")
    lines.append("╚" + "═" * 58 + "╝")
    
    return "\n".join(lines)


BASE_META = {
    10: {"name": "Decimal", "subtitle": "Standard Numogram"},
    16: {"name": "Hexadecimal", "subtitle": "Memory Map"},
    22: {"name": "Base-22", "subtitle": "Hebrew Numogram"},
    26: {"name": "Hexavigesimal", "subtitle": "Abecedarium"},
    28: {"name": "Base-28", "subtitle": "Regional test"},
    36: {"name": "Sexatrigesimal", "subtitle": "Djynxxogram"},
}

DEFAULT_COMPARE_BASES = [10, 16, 22, 26, 36]


def zone_in_base(aq: int, base: int) -> int:
    """Map an AQ value to a zone in the given base.
    
    For base-10: digital root (mod 9, 0→0, 9→9)
    For other bases: aq % base
    """
    if base == 10:
        return digital_root(aq)  # allow 0 for Void
    return aq % base


def generate_comparison_reading(text: str, bases: Optional[list[int]] = None) -> str:
    """Compare a text's AQ traversal across multiple bases."""
    if bases is None:
        bases = DEFAULT_COMPARE_BASES
    aq = compute_aq(text)
    dr = digital_root(aq)  # allow 0 for Void
    
    lines = []
    lines.append("╔" + "═" * 64 + "╗")
    lines.append(f"║  BASE COMPARISON — {text:<45}║")
    lines.append("╚" + "═" * 64 + "╝")
    lines.append("")
    lines.append(f"  AQ = {aq}  →  digital root {dr}  →  decimal zone {dr} ({DECIMAL_ZONE_DISPLAY[dr]})")
    lines.append("")
    
    # Table header
    lines.append(f"  {'Base':<6} {'Zone':<8} {'Name':<18} {'Char':<6} {'Type':<20}")
    lines.append(f"  {'─'*6} {'─'*8} {'─'*18} {'─'*6} {'─'*20}")
    
    for base in bases:
        if base == 36:
            # Full traversal summary
            steps = compute_base36_traversal(text)
            zone_chars = "".join(s["char_36"] for s in steps)
            unique_zones = len(set(s["zone"] for s in steps))
            hit_outer = any(s["region"] == "OUTER" for s in steps)
            outer_note = ", OUTER" if hit_outer else ""
            
            # Zone name: last step's attractor
            last = steps[-1]
            zone = last["zone"]
            name = last["name"]
            char = last["char_36"]
            
            lines.append(f"  {base:<6} {zone:<8} {name:<18} {char:<6} {unique_zones}/36 zones{outer_note}")
            # Show traversal path
            path_str = "→".join(s["char_36"] for s in steps)
            lines.append(f"  {'':6} {'':8} {'':18} {'':6} Path: {path_str}")
            if hit_outer:
                outer_zones = [s["char_36"] for s in steps if s["region"] == "OUTER"]
                lines.append(f"  {'':6} {'':8} {'':18} {'':6} Outer: {', '.join(outer_zones)}")
        else:
            zone = zone_in_base(aq, base)
            if base <= 10:
                # For bases ≤ 10, just use the digit
                char = str(zone)
            else:
                char = zone36_char(zone) if zone < 36 else f"[{zone}]"
            name = ZONE36_LETTER_NAMES.get(zone, f"Z{zone}")
            
            # Determine type
            if base == 10:
                ztype = f"{ZONES[zone]['region']}"
            elif base <= 36:
                n1 = base - 1
                # Check if this zone is self-folding in this base
                partner = n1 - zone
                current = abs(zone - partner)
                is_outer = (current == zone or current == partner)
                ztype = "OUTER" if is_outer else "CIRCUIT"
            else:
                ztype = "unknown"
            
            lines.append(f"  {base:<6} {zone:<8} {name:<18} {char:<6} {ztype:<20}")
    
    lines.append("")
    lines.append(f"  Decimal attractor path (all bases):  {dr} ({DECIMAL_ZONE_DISPLAY[dr]})")
    lines.append("")
    lines.append("╚" + "═" * 64 + "╝")
    
    return "\n".join(lines)


# ─── I CHING DELEGATION (modular, see iching.py) ───
# oracle.py now delegates I Ching work to the standalone iching.py.
# This keeps the divination pipeline clean while allowing iching.py to be
# used, improved, and tested independently.
ICHING_MODULE = None
try:
    import iching as ICHING_MODULE  # same-dir sibling import when run as module
except Exception:
    ICHING_MODULE = None

ICHING_SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "iching.py")

# ─── TAIXUAN DELEGATION (modular, see taixuan.py) ───
TAIXUAN_MODULE = None
try:
    import taixuan as TAIXUAN_MODULE
except Exception:
    TAIXUAN_MODULE = None

TAIXUAN_SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "taixuan.py")

# ─── GEOMANCY DELEGATION (modular, see geomancy.py) ───
GEOMANCY_MODULE = None
try:
    import geomancy as GEOMANCY_MODULE
except Exception:
    GEOMANCY_MODULE = None

GEOMANCY_SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "geomancy.py")

def _iching_opts(args):
    """[fix] pass iching.py's --method / --zone-method through. Defaults come from iching.py /
    taixuan.py: zones from LINE VALUES in both (fuxi / value); sequence numbers via
    --zone-method kw (I Ching) or --zone-from number (Tai Xuan)."""
    o = {}
    if "--method" in args:
        o["method"] = args[args.index("--method") + 1]
    if "--zone-method" in args:
        o["zone_method"] = args[args.index("--zone-method") + 1]
    return o


def fetch_iching(seed=None):
    """Delegate to iching.py (preferred) or fallback."""
    if ICHING_MODULE is not None:
        return ICHING_MODULE.fetch_iching(seed)
    # subprocess fallback (loose coupling)
    try:
        cmd = ["python3", ICHING_SCRIPT, "--iching"]
        if seed is not None:
            cmd += ["--seed", str(seed)]
        cmd += ["--json"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            data = json.loads(result.stdout)
            # reconstruct minimal hexagram list for any legacy paths
            return data.get("hexagram", [])
    except Exception:
        pass
    # Last resort: very small inline (should rarely hit)
    import time, hashlib
    data = (hashlib.sha256(str(seed or time.time_ns()).encode()).digest()[:6] if seed is not None
            else int(time.time_ns()).to_bytes(8, "big")[:6])
    hexagram = []
    for i, b in enumerate(data):
        val = b % 4
        if val == 0:
            hexagram.append({"pos": i+1, "symbol": "--- ---", "value": 6, "changing": True})
        elif val == 1:
            hexagram.append({"pos": i+1, "symbol": "-------", "value": 7, "changing": False})
        elif val == 2:
            hexagram.append({"pos": i+1, "symbol": "--- ---", "value": 8, "changing": False})
        else:
            hexagram.append({"pos": i+1, "symbol": "-------", "value": 9, "changing": True})
    return hexagram

def enrich_iching(hexagram: list) -> dict:
    """Delegate to iching.py enrich or reconstruct minimal result."""
    if ICHING_MODULE is not None:
        return ICHING_MODULE.enrich_iching(hexagram)
    # fallback reconstruction using old logic (kept tiny)
    bits = 0
    for i, line in enumerate(hexagram):
        if line["value"] in (7, 9):
            bits |= (1 << i)
    hex_val = bits
    kw_like = hex_val + 1
    zone = 1 + (kw_like - 1) % 9
    if zone == 10: zone = 0
    total_value = sum(l["value"] for l in hexagram)
    return {
        "hexagram": hexagram,
        "hex_val": hex_val,
        "hex_num": kw_like,
        "total_value": total_value,
        "changing_lines": [l["pos"] for l in hexagram if l["changing"]],
        "numogram_zone": zone,
        "numogram_gate": get_gate(zone),
        "numogram_syzygy": f"{zone}::{get_syzygy(zone)}",
        "numogram_demon": None,
        "alt_dr_shadow": digital_root(total_value),
        "mapping_note": "fallback (iching.py unavailable)",
    }

# ─── EXTERNAL SEEDS ───

def fetch_random_org():
    """True random from atmospheric noise"""
    import urllib.request
    resp = urllib.request.urlopen("https://www.random.org/integers/?num=1&min=0&max=999999&col=1&base=10&format=plain&rnd=new", timeout=10)
    return int(resp.read().strip())


def fetch_blockchain():
    """Latest Bitcoin block hash as seed"""
    import urllib.request
    resp = urllib.request.urlopen("https://blockchain.info/latestblock", timeout=10)
    data = json.loads(resp.read())
    return int(data["hash"][:8], 16)


def fetch_earthquake():
    """Latest USGS earthquake magnitude as seed"""
    import urllib.request
    resp = urllib.request.urlopen("https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson", timeout=10)
    data = json.loads(resp.read())
    quakes = data.get("features", [])
    if quakes:
        mag = quakes[0]["properties"]["mag"]
        time_ms = quakes[0]["properties"]["time"]
        return int(mag * 1000) + (time_ms % 10000)
    return 0


def fetch_hardware():
    """Seed from local hardware entropy (thermal, CPU, GPU, timing jitter).
    Prefers ~/.hermes/tools/hardware_entropy.py (now provided with full 12-source collector).
    Falls back to strong local jitter collection (thermals + /proc + timing + fsync etc.)
    inspired by numogram-entropy-source, domain/entropy-sources, and wiki/hardware-entropy.md.
    """
    import subprocess
    try:
        result = subprocess.run(
            ["python3", os.path.expanduser("~/.hermes/tools/hardware_entropy.py"), "--bytes", "8"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0 and result.stdout.strip():
            hex_str = result.stdout.strip()
            if hex_str.startswith("{"):
                import json
                j = json.loads(hex_str)
                hex_str = j.get("entropy_hex8") or j.get("hex") or ""
            if hex_str:
                return int(hex_str, 16) % 1000000
    except Exception:
        pass

    # Robust local fallback (no external script needed)
    try:
        import glob, time, hashlib  # [fix] no local `import os` (it shadowed the module above)
        parts = []
        for p in glob.glob("/sys/class/thermal/thermal_zone*/temp"):
            try: parts.append(open(p).read().strip().encode())
            except: pass
        for p in glob.glob("/sys/devices/system/cpu/cpu*/cpufreq/scaling_cur_freq"):
            try: parts.append(open(p).read().strip().encode())
            except: pass
        for p in ["/proc/stat", "/proc/loadavg", "/proc/uptime", "/proc/interrupts", "/proc/meminfo", "/proc/vmstat"]:
            try: parts.append(open(p, "rb").read(256))
            except: pass
        for _ in range(128):
            t0 = time.perf_counter_ns()
            _ = sum(i*i for i in range(20))
            t1 = time.perf_counter_ns()
            parts.append(str(t1-t0).encode())
        parts.append(str(os.getpid()).encode())
        parts.append(str(time.time_ns()).encode())
        blob = hashlib.sha256(b"".join(parts)).digest()
        return int.from_bytes(blob[:8], "big") % 1000000
    except Exception:
        import time
        return int(time.time_ns()) % 1000000


# (fetch_iching / enrich_iching now delegate above; old bodies removed for modularity)

# ─── READING GENERATION ───

def generate_reading(seed, source="manual"):
    """Generate a complete oracle reading.
    Now uses enriched zone data (full_name + epithet) and gate details + lore.
    """
    zone = derive_zone(seed)
    z = ZONES[zone]
    syzygy = get_syzygy(zone)
    current = get_current(zone)
    gate = get_gate(zone)
    gdet = get_gate_details(zone)
    path = traverse(seed, 8)

    # Rich display using poetic titles from philosophies.md (wiki + skill copy)
    # Format: "Seized Vortex (Iron Core / tn)" — full poetic + epithet + particle
    phon = z["name"]
    full = z.get("full_name", phon)
    epit = z.get("epithet", "")
    if epit and epit != full:
        name_str = f"{full} ({epit} / {phon})"
    elif full != phon:
        name_str = f"{full} ({phon})"
    else:
        name_str = phon

    lines = []
    lines.append("═" * 40)
    lines.append("  NUMOGRAM ORACLE READING")
    lines.append("═" * 40)
    lines.append("")
    lines.append(f"  Seed:         {seed} ({source})")
    lines.append(f"  Digital root: {digital_root(seed)}")
    lines.append(f"  Zone:         {zone} — {name_str}")
    lines.append(f"            {z['desc']}")
    if z.get("epithet"):
        lines.append(f"  Epithet:      {z['epithet']}")
    lines.append(f"  Polarity:     {z['polarity']} ({'Process/becoming' if z['polarity']=='+' else 'Foundation/stasis'})")
    lines.append(f"  Syzygy:       {zone}::{syzygy} ({z['region']})")
    demon = demon_from_zones(zone, syzygy)
    if demon != "Unknown":
        lines.append(f"  Syzygy carrier: {demon}")
    lines.append(f"  Current:      {current} ({z['current']})")
    lines.append(f"  Gate:         Gt-{gdet['gate_raw']} ({zone}→{gate})  loops={gdet['gate_loops']}")
    if gdet.get("lore"):
        lines.append(f"  Gate lore:    {gdet['lore']}")
    lines.append(f"  Sound:        {phon} — {z['desc']}")
    if z.get("voice_quality"):
        lines.append(f"  Voice:        {z['voice_quality'][:110]}{'...' if len(z.get('voice_quality', '')) > 110 else ''}")
    lines.append("")
    lines.append(f"  Path: {' → '.join(str(p) for p in path)}")
    lines.append("")
    lines.append(f"  {z['reading']}")
    lines.append("")
    lines.append(f"  Book of Paths: {z['path']}")
    lines.append("")
    lines.append("═" * 40)
    
    return "\n".join(lines), zone



def _tty_color(r, g, b) -> str:
    """ANSI 256-color escape — zone-specific zname color."""
    return f"\x1b[38;2;{r};{g};{b}m"


# ─── ZONE SPRITE ─────────────────────────────────────────────────────────

def _pixel_hash(x, y, zone):
    """Deterministic binary medallion — identical to planchette-svg.py."""
    seed = (zone * 7919) ^ (x * 31) ^ (y * 17)
    return 1 if ((seed * 0x5bd1e995) & 0xffff) > 0x6fff else 0


def render_zone_sprite(zone: int) -> str:
    """Render a 10×10 pixel-art medallion as coloured ANSI full-block rows.

    Each row is a single ANSI-RGB line — 10 characters wide.  Characters
    use U+2588 (█) for 'on' pixels and U+0020 (space) for 'off' pixels.
    Colour comes from _ZONE_TTY_RGB (no palette dependency).
    Runs planchette-analogous zone medallion grid → terminal-render with
    pixel-scope fidelity in 10 x 10 px block-cycle alignment.  Full spectrum
    stable, stable mask drawn at 1 unit block-width. Triggers core:
    `HA-MA-HA-BA-AL` — mirror images vapour-lock quantum frame.
    """
    rgb = _ZONE_TTY_RGB.get(zone, (200, 200, 200))
    esc = _tty_color(*rgb)
    rows = []
    for y in range(10):
        row = "".join(
            "\u2588" if _pixel_hash(x, y, zone) else " "
            for x in range(10)
        )
        rows.append(esc + row + "\x1b[0m")
    return "\n".join(rows)

def generate_planchette_glyph(zone: int, current: int, gate: int, syzygy: str,
                               reading: str = "") -> str:
    """ASCII box-art planchette — unique glyph per zone, gate-arc ring."""
    import textwrap as _tw

    _Z = ZONES.get(zone,
                   {"name":"???","region":"???","current":"???","reading":"???"})
    zregion = _Z.get("region", f"Zone {zone}")
    zpart   = _Z.get("name", "???")
    pol_str = _Z.get("polarity", "+")
    pol_d   = "Process / becoming" if pol_str == "+" else "Substance / inertia"

    _GLYPH = {
        0: ["  ◜ ◜ ◜      ◞ ◞ ◞",
            "   ◜   ∇   ◞",
            "           "],
        1: ["  ╱╱ ╱╱ ╱╱ ╱╱ ╱╱   ",
            " ╱  V V V V  ╲ ",
            " ╲  ^ ^ ^ ^  ╱",
            "  ╲╲ ╲╲ ╲╲ ╲╲    "],
        2: ["  ◜─◝   ╱ ╲   ◞─◞  ",
            "                "],
        3: ["  ━━╾━╾┳━┓╾━╾━━━   ",
            "           ",
            " ┗━━━┻━━━┻━━━┛ "],
        4: [">◜       GATE       ◞<",
            "  ──────────── ",
            "                "],
        5: ["  ├─╁─╁─╁─╁─┤  ",
            " ║ STRESS ║ ",
            "  ├─╁─╁─╁─╁─┤  "],
        6: ["  ╱╲  ╱╲  ╱╲   ",
            "  ││     ││   ",
            "  ╲╱     ╲╱   ",
            "  ╱╲  ╱╲  ╱╲   "],
        7: ["  ┌─♥─┬─♥─┐ ",
            "  │♥ ⦿ ♥ │ ",
            "  └─♥─┴─♥─┘ "],
        8: ["  │ │  ╱  ╲││ ",
            "  │ │╱      ╲│ "],
        9: ["  ███████████ ",
            "  █ P L E X █ ",
            "  █         █ ",
            "  ███████████ "],
    }
    _PART = {
        0: "◜◜·◞ ◞·◞", 1: "◁━━━━━━━▶", 2: "║", 3: "🝤", 4: "───►───",
        5: "├┴┴┴┴┤",  6: "◻◻◻◻",    7: "──●──", 8: "╱╲│╱╲╱", 9: "█╯╰█",
    }

    W  = 48
    TT = f"┏{'━'*(W-2)}┓"
    MD = f"┣{'─'*(W-2)}┫"
    TB = f"┗{'━'*(W-2)}┛"

    _ZN = ZONES.get(zone, {})
    zname = _ZN.get("full_name") or _ZN.get("epithet") or _ZN.get("name", f"Z{zone}")
    gname = ZONES.get(gate, {}).get("full_name") or ZONES.get(gate, {}).get("name", f"Z{gate}")

    ring = ["  ─"] * 10
    ring[zone] = f"Z{zone}"
    ring[gate] = f"↑{gate}"
    arc_row = "  ═".join(ring).replace("  ─", "──")

    verse_lines = []
    for rl in _tw.wrap(reading or "", width=34):
        verse_lines.append(f"  {rl}")

    glyph_lines = _GLYPH.get(zone, [f"  Zone {zone}"])
    part_d = _PART.get(zone, "     ")

    out = []
    title = f"  ZONE {zone}  ·  {zregion:<14}  ·  AQΣ={zone+137}"
    out.append(TT)
    out.append(f"┃{title:^{W-2}}┃")
    out.append(MD)
    out.append(f"┃{' ':^{W-2}}┃")
    for lbl, val in [
        ("Current",  f"{current} [{zname}]"),
        ("Gate",     f"Gt-{gate:02d} → Z{gate}"),
        ("Syzygy",   syzygy),
        ("Polarity", f"{pol_str}  —  {pol_d}"),
        ("Region",   zregion),
        ("Particle", ZONES.get(zone, {}).get("particle", "?").upper()),
    ]:
        out.append(f"┃  {lbl:<10}  {val:<30}┃")
    out.append(f"┃{' ':^{W-2}}┃")
    for gl in glyph_lines:
        out.append(f"┃{gl:^{W-2}}┃")
    out.append(f"┃  {part_d:^{W-4}}┃")
    out.append(f"┃{' ':^{W-2}}┃")
    if verse_lines:
        for rl in verse_lines:
            out.append(f"┃{rl:<{W-2}}┃")
        out.append(f"┃{' ':^{W-2}}┃")
    out.append(f"┃{arc_row:<{W-2}}┃")
    out.append(f"┃{' ':^{W-2}}┃")
    out.append(TB)
    return "\n".join(out)

def generate_planchette(zone: int) -> str:
    """Planchette a brief zone-glyph planchette for oracle output.
    Now surfaces full_name/epithet and gate_raw/loops via get_gate_details.
    """
    z     = ZONES.get(zone, {"name": "???", "region": "???"})
    gdet  = get_gate_details(zone)
    gate  = gdet["gate"]
    sz    = get_syzygy(zone)
    cur   = get_current(zone)
    region = z.get("region", "??")
    phoneme = z.get("name", "???")
    display = z.get("full_name") or z.get("epithet") or phoneme
    png   = "~/numogram/docs/wiki/assets/zone-glyphs/zone-{z}.png".format(z=zone)

    # fixed-width helpers (56 total interior cols)
    W = 54
    hdr1 = "ZONE {z} — {r:<16} [{p:>8}]".format(z=zone, r=region, p=phoneme)
    hdr2 = "Current: {c:2}    Gate: Gt-{g:<2}=Z{g:<2}    Syzygy: {z}::{sy:<2}".format(
                c=cur, g=gate, z=zone, sy=sz)
    if z.get("full_name") or z.get("epithet"):
        hdr1 = "ZONE {z} — {d} ({p})".format(z=zone, d=display, p=phoneme)[:W-4].ljust(W-4)

    lines = []
    lines.append("")
    lines.append("  ╔" + "═"*W + "╗")
    lines.append("  ║   " + hdr1 + (W-len(hdr1))*" " + "  ║")
    lines.append("  ╠" + "═"*W + "╣")
    lines.append("  ║   " + hdr2 + (W-len(hdr2))*" " + "  ║")
    lines.append(f"  ║   Gt raw: {gdet['gate_raw']:<3} loops:{gdet['gate_loops']} hist:{gdet['gate_history']}     ║")
    lines.append("  ║   PNG: {p:<40}  ║".format(p=png))
    lines.append("  ╚" + "═"*W + "╝")
    return "\n".join(lines)


def generate_planchette_json(zone: int, current: int, gate: int, syzygy: int) -> str:
    """Machine-readable JSON for planchette pipelines (planchette-svg.py --stdin etc.).
    
    Uses get_gate_details for canonical raw/loops/history.
    Includes enriched fields: full_name, epithet, voice_quality snippet, gate lore.
    """
    z = ZONES.get(zone, {"name": "???", "region": "???", "reading": "???"})
    gdet = get_gate_details(zone)

    demon = demon_from_zones(zone, syzygy)
    d = {
        "zone":         zone,
        "name":         z["name"],
        "full_name":    z.get("full_name"),
        "epithet":      z.get("epithet"),
        "region":       z.get("region", "???"),
        "particle":     z["name"],
        "polarity":     z.get("polarity", "?"),
        "current":      current,
        "gate":         gate,
        "gate_raw":     gdet["gate_raw"],
        "gate_loops":   gdet["gate_loops"],
        "gate_history": gdet["gate_history"],
        "gate_lore":    gdet.get("lore"),
        "syzygy":       f"{zone}::{syzygy}",
        "syzygy_demon": demon if demon != "Unknown" else None,
        "reading":      z.get("reading", ""),
        "voice_quality": z.get("voice_quality"),
        "philosophy":   z.get("philosophy"),
        "color_rgb":    _ZONE_TTY_RGB.get(zone),
    }
    return json.dumps(d, separators=(",", ":"))





def generate_voice(zone):
    """Generate oracle voice audio for a zone"""
    z = ZONES[zone]
    synth_script = os.path.join(VOICE_DIR, "synthesize.py")
    
    if not os.path.exists(synth_script):
        print(f"  [Voice] Synthesizer not found at {synth_script}")
        return None
    
    # Check if zone sound exists
    zone_file = os.path.join(VOICE_DIR, f"zone_{zone}_{z['name']}.wav")
    if not os.path.exists(zone_file):
        subprocess.run(["python3", synth_script, str(zone)], capture_output=True)
    
    if os.path.exists(zone_file):
        print(f"  [Voice] Zone sound: {zone_file}")
        return zone_file
    else:
        print(f"  [Voice] Could not generate zone sound")
        return None


# ─── MAIN ───

if __name__ == "__main__":
    args = sys.argv[1:]
    seed = None
    source = "manual"
    do_ascii_glyph = False
    do_sprite = False
    do_voice = "--voice" in args          # [fix] was always False
    if "--gate-rule" in args:
        GATE_RULE = args[args.index("--gate-rule") + 1]
    if "--path" in args:
        PATH_MODE = args[args.index("--path") + 1]
    if GATE_RULE not in ("dr", "mod") or PATH_MODE not in ("legacy", "hash"):
        print("--gate-rule must be dr|mod; --path legacy|hash")
        sys.exit(2)
    if "--geomancy" in args:
        # every other flag (--seed, --hardware, --json, --house, --scheme, --gate-rule …) passes through
        gargs = [x for x in args if x != "--geomancy"]
        if GEOMANCY_MODULE is not None:
            sys.exit(GEOMANCY_MODULE.main(gargs))
        sys.exit(subprocess.run([sys.executable, GEOMANCY_SCRIPT] + gargs).returncode)
    do_base36 = False
    do_planchette = False
    do_tty = False
    do_json = False
    
    if "--ascii-glyph" in args:
        do_ascii_glyph = True
    if "--sprite" in args:
        do_sprite = True
    if "--json" in args:
        do_json = True
    if "--base36" in args or "--djynxxogram" in args:
        do_base36 = True
    if "--planchette" in args:
        do_planchette = True
    if "--tty" in args:
        do_tty = True

    # ── BASE-36 DJYNXXOGRAM MODE ──
    if do_base36:
        if "--text" in args:
            idx = args.index("--text")
            text = args[idx + 1]
            b36_text = generate_base36_reading(text)
            print(b36_text)
            if do_planchette:
                steps = compute_base36_traversal(text)
                dec_zone = digital_root(sum(s['aq'] for s in steps))  # allow 0 for Void attractor
                print()
                if do_json:
                    print(generate_planchette_json(dec_zone, get_current(dec_zone), get_gate(dec_zone), get_syzygy(dec_zone)))
                else:
                    print(generate_planchette(dec_zone))
            print()
            sys.exit(0)
        elif "--seed" in args:
            idx = args.index("--seed")
            seed_val = int(args[idx + 1])
            # Use seed as raw AQ value to generate a traversal
            # Convert seed to hex string to get character-level traversal
            hex_str = format(seed_val, 'X')
            print(f"  Seed {seed_val} → hex {hex_str}")
            print()
            h_s = generate_base36_reading(hex_str)
            print(h_s)
            if do_planchette:
                steps = compute_base36_traversal(hex_str)
                dec_zone = digital_root(sum(s['aq'] for s in steps))  # allow 0 for Void attractor
                print()
                print(generate_planchette(dec_zone))
            print()
            sys.exit(0)
        else:
            print("Djynxxogram mode requires --text or --seed")
            print("  python3 oracle.py --base36 --text 'NUMOGRAM' --planchette")
            print("  python3 oracle.py --djynxxogram --seed 174")
            sys.exit(1)
    
    # ── COMPARISON MODE ──
    if "--compare" in args:
        if "--text" in args:
            idx = args.index("--text")
            text = args[idx + 1]
            print(generate_comparison_reading(text))
            sys.exit(0)
        elif "--seed" in args:
            idx = args.index("--seed")
            text = str(args[idx + 1])
            print(generate_comparison_reading(text))
            sys.exit(0)
        else:
            print("Comparison mode requires --text or --seed")
            print("  python3 oracle.py --compare --text 'NUMOGRAM'")
            print("  python3 oracle.py --compare --seed 174")
            sys.exit(1)
    
    # ── STANDARD MODE ──
    if "--seed" in args and "--taixuan" not in args:
        idx = args.index("--seed")
        seed = int(args[idx + 1])
        if "--iching" in args:
            try:
                if ICHING_MODULE is not None:
                    ich = ICHING_MODULE.cast_iching(seed=seed, source=f"seed:{seed}", **_iching_opts(args))
                    print(ICHING_MODULE.format_iching(ich, full="--full" in args))  # [fix] pass --full
                else:
                    # fallback: use our thin delegate + manual minimal print
                    hexagram = fetch_iching(seed=seed)
                    ich = enrich_iching(hexagram)
                    print("══════════════════════════════════════")
                    print("  I CHING FROM NUMOGRAM ENTROPY (fallback)")
                    print("══════════════════════════════════════")
                    print(f"  Hexagram {ich['hex_num']}  Zone shadow {ich['numogram_zone']}")
            except Exception as e:
                print(f"[iching delegate error] {e}")
            sys.exit(0)
    elif "--text" in args:
        idx = args.index("--text")
        text = args[idx + 1]
        seed = compute_aq(text)
        source = f"AQ({text})"
    elif "--synx" in args:
        idx = args.index("--synx")
        text = args[idx + 1]
        seed = compute_synx(text)
        source = f"Synx({text})"
        aq = compute_aq(text)
        print(f"  AQ:   {aq} (zone {digital_root(aq)})")
        print(f"  Synx: {seed} (zone {digital_root(seed)})")
        print()
    elif "--random" in args:
        seed = fetch_random_org()
        source = "random.org"
    elif "--blockchain" in args:
        seed = fetch_blockchain()
        source = "blockchain.info"
    elif "--earthquake" in args:
        seed = fetch_earthquake()
        source = "USGS"
    elif "--hardware" in args and "--iching" not in args and "--taixuan" not in args:
        # [fix] --taixuan/--iching --hardware used to fall through to a plain reading
        seed = fetch_hardware()
        source = "hardware"
    elif "--iching" in args:
        try:
            if ICHING_MODULE is not None:
                s = None
                src = "hardware"
                if "--seed" in args:
                    idx = args.index("--seed")
                    s = int(args[idx + 1])
                    src = f"seed:{s}"
                full = "--full" in args
                ich = ICHING_MODULE.cast_iching(seed=s, source=src, **_iching_opts(args))
                print(ICHING_MODULE.format_iching(ich, full=full))
            else:
                hexagram = fetch_iching(seed=s)  # [fix] fallback ignored --seed
                ich = enrich_iching(hexagram)
                print("══════════════════════════════════════")
                print("  I CHING FROM NUMOGRAM ENTROPY (fallback)")
                print(f"  Hex {ich.get('hex_num')}")
        except Exception as e:
            print(f"[iching delegate error] {e}")
        sys.exit(0)
    elif "--taixuan" in args:
        try:
            s = None
            if "--seed" in args:
                idx = args.index("--seed")
                s = int(args[idx + 1])
            if TAIXUAN_MODULE is not None:
                full = "--full" in args
                # [fix] honour the flags CLI-README documents for oracle.py --taixuan
                if "--zone-from" in args:
                    TAIXUAN_MODULE.ZONE_FROM = args[args.index("--zone-from") + 1]
                TAIXUAN_MODULE.NETSPAN = "--netspan" in args
                two = "--single" not in args and "--one" not in args
                data = TAIXUAN_MODULE.cast_taixuan(seed=s, two=two)
                if "--em-stats" in args or "--em-profile" in args:
                    tetras = [data["upper"], data["lower"]] if two else [data["tetragram"]]
                    print("Em-state Profile:")
                    print(json.dumps(TAIXUAN_MODULE.em_profile(tetras), indent=2))
                print(TAIXUAN_MODULE.format_taixuan(data, full=full,
                                                    use_unicode="--unicode" in args or "--uni" in args))
                if do_voice:  # [fix] restored from the pre-refactor version
                    zones = [str(data["upper_zone"]), str(data["lower_zone"])] if two else [str(data["zone"])]
                    vs = os.path.expanduser("~/numogram-voices/oracle_sentences.py")
                    if os.path.exists(vs):
                        res = subprocess.run(["python3", vs, "--zones"] + zones, capture_output=True, text=True)
                        for line in res.stdout.splitlines():
                            if "oracle_sentence" in line and ".wav" in line:
                                print(f"  [Voice] {line.strip()}")
                        if res.returncode != 0:
                            print(f"  [Voice] oracle_sentences.py failed (exit {res.returncode})")
                    else:
                        print(f"  [Voice] {vs} not found")
            else:
                cmd = [sys.executable, TAIXUAN_SCRIPT, "--taixuan"]
                if s is not None:
                    cmd += ["--seed", str(s)]
                if "--full" in args: cmd.append("--full")
                cmd.append("--json")
                res = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                if res.returncode == 0:
                    d = json.loads(res.stdout)
                    print(TAIXUAN_MODULE.format_taixuan(d) if TAIXUAN_MODULE else json.dumps(d, indent=2))
                else:
                    print("T'AI XUAN (fallback)")
        except Exception as e:
            print(f"[taixuan delegate error] {e}")
        sys.exit(0)
    elif "--traverse" in args:
        seed = int(args[args.index("--traverse") + 1]) if "--traverse" in args and len(args) > args.index("--traverse") + 1 else 192855
        path = traverse(seed)
        print(f"Seed: {seed}")
        print(f"Zone path: {' → '.join(str(z) for z in path)}")
        for i, z in enumerate(path):
            zz = ZONES[z]
            disp = zz.get("full_name") or zz.get("epithet") or zz["name"]
            print(f"  Step {i}: Zone {z} ({disp} / {zz['name']}) — {zz['desc']}")
        sys.exit(0)
    else:
        print("Numogram Oracle")
        print()
        print("Usage:")
        print("  python3 oracle.py --seed 192855")
        print("  python3 oracle.py --text 'YOUR NAME'")
        print("  python3 oracle.py --seed 192855 --voice")
        print("  python3 oracle.py --random")
        print("  python3 oracle.py --blockchain")
        print("  python3 oracle.py --earthquake")
        print("  python3 oracle.py --hardware")
        print("  python3 oracle.py --iching")
        print("  python3 oracle.py --iching --seed 192855")
        print("  python3 iching.py --iching          (standalone I Ching + numogram shadow)")
        print("  python3 iching.py --iching --seed N")
        print("  python3 oracle.py --taixuan")
        print("  python3 taixuan.py --taixuan          (standalone Tai Xuan + 27-phase)")
        print("  python3 taixuan.py --phase            (Yuandong/Guanziming 27)")
        print("  python3 oracle.py --geomancy [--seed N] [--house 10] [--json]  (geomantic shield + house chart)")
        print("  python3 geomancy.py --figures | --census   (standalone; see CLI-README)")
        print("  python3 oracle.py --synx 'TEXT'  (Synx/Yxshh cipher)")
        print("  python3 oracle.py --traverse 192855")
        print("  python3 oracle.py --base36 --text 'TEXT'  (Djynxxogram traversal)")
        print("    --gate-rule dr|mod   base-36 gate: digital root mod 35 (default) | last digit T mod 36")  # [fix]
        print("  python3 oracle.py --djynxxogram --seed 174  (Djynxxogram from AQ)")
        print("  python3 oracle.py --compare --text 'TEXT'  (cross-base comparison)")
        print("  python3 oracle.py --compare --seed 174    (from AQ value)")
        print("  python3 oracle.py --seed N --planchette            (zone glyph planchette)")
        print("  python3 oracle.py --seed N --planchette --tty           (ANSI color terminal)")
        print("  python3 oracle.py --seed N --planchette --ascii-glyph --sprite (ASCII glyph + pixel medallion)")
        print("  python3 oracle.py --seed N --planchette --sprite               (pixel medallion only)")
        print()
        print("Enriched output includes poetic full names (Void Resonance, Blood, Iron Core...),")
        print("CCRU voice qualities, gate lore (Gt-45 Pandemonium etc.), and I Ching numogram shadows.")
        sys.exit(1)

    # ── Generate standard reading (zone, etc.) for all non-special modes ──
    reading = None
    zone = None
    if seed is not None:
        reading, zone = generate_reading(seed, source)

    # ── PLANCHETTE / READING OUTPUT ──
    if do_planchette or do_json or do_sprite or do_ascii_glyph:
        if zone is None and seed is not None:
            reading, zone = generate_reading(seed, source)

    if do_planchette and do_json and zone is not None:
        print(generate_planchette_json(zone, get_current(zone), get_gate(zone), get_syzygy(zone)))
    elif do_planchette and zone is not None:
        if not (do_sprite or do_ascii_glyph or do_json):
            _out_lines = generate_planchette(zone).split("\n")
        else:
            _out_lines = []
        if do_sprite:
            _out_lines.append(render_zone_sprite(zone))
            _out_lines.append("")
        if do_ascii_glyph:
            _out_lines.append(generate_planchette_glyph(zone, get_current(zone),
                                                         get_gate(zone), get_syzygy(zone)))
        if do_json:
            _out_lines.append(generate_planchette_json(zone, get_current(zone),
                                                        get_gate(zone), get_syzygy(zone)))
        print(reading)
        print()
        _rgb = _ZONE_TTY_RGB.get(zone, (200, 200, 200))
        if do_tty:
            for _l in _out_lines:
                print(_tty_color(*_rgb) + _l + "\x1b[0m")
        else:
            for _l in _out_lines:
                print(_l)
        print()

    # ── sprite / ascii-glyph / json without planchette ──
    if zone is not None and (do_sprite or do_ascii_glyph or do_json) and not do_planchette:
        _out_lines = []
        if do_sprite:
            _out_lines.append(render_zone_sprite(zone))
            _out_lines.append("")
        if do_ascii_glyph:
            _out_lines.append(generate_planchette_glyph(zone, get_current(zone),
                                                         get_gate(zone), get_syzygy(zone)))
        if do_json:
            _out_lines.append(generate_planchette_json(zone, get_current(zone),
                                                        get_gate(zone), get_syzygy(zone)))
        _rgb = _ZONE_TTY_RGB.get(zone, (200, 200, 200))
        if do_tty:
            for _l in _out_lines:
                print(_tty_color(*_rgb) + _l + "\x1b[0m")
        else:
            for _l in _out_lines:
                print(_l)
        print()




        # ── Standard reading output (no special flags) ──
    if zone is not None and reading is not None and not (do_planchette or do_sprite or do_ascii_glyph or do_json):
        print(reading)
        print()

    # Generate voice if requested
    if do_voice:
        print()
        generate_voice(zone)
