#!/usr/bin/env python3
"""
Numogram Oracle — Divination Pipeline
Seed → Zone → Syzygy → Current → Gate → Book of Paths → Voice
Now with --base36 Djynxxogram traversal.

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
  python3 oracle.py --taixuan  (T'ai Hsuan two-tetragram oracle from hardware)
  python3 oracle.py --taixuan --voice  (with zone sound generation)
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
ZONES = {
    0: {"name": "eiaoung", "polarity": "−", "current": "Plex",   "region": "Plex",
        "desc": "Void whisper, silence before the word",
        "path": "Silent entry. The void before the Book begins.",
        "reading": "The abyss. No sound. No path. The void does not speak — it is the silence that makes speech possible."},
    1: {"name": "gl",      "polarity": "+", "current": "Sink",   "region": "Time-Circuit",
        "desc": "Gulp, glottal spasm, beginnings",
        "path": "Original Subtraction. Ultimate descent through the Depths. The path favours repeated patience linked by subtlety.",
        "reading": "Descent. The first thing any system does when it wakes up is choke on itself. Patience. Subtlety. Three tests on the way. Difficulties annihilated in the end."},
    2: {"name": "dt",      "polarity": "−", "current": "Hold",   "region": "Time-Circuit",
        "desc": "Stuttering, boundaries breaking",
        "path": "Extreme Regression. Waiting in the Rising Drift leads to ultimate descent.",
        "reading": "The boundary cannot hold its own shape. Waiting. The drift pulls downward despite your direction. Five tests on the way. Escaping the quagmire through strategic withdrawal."},
    3: {"name": "zx",      "polarity": "+", "current": "Warp",   "region": "Warp",
        "desc": "Buzz-cutter, static, chaos",
        "path": "Abysmal Comprehension. Ultimate descent beyond completion. Burning excitement provokes breakthrough into immersive nightmares.",
        "reading": "The Warp. The current spirals outward to infinity. When you hear static, you are hearing this zone. Burning excitement. Breakthrough. Ominous transition. Difficulties annihilated."},
    4: {"name": "skr",     "polarity": "−", "current": "Sink",   "region": "Time-Circuit",
        "desc": "Growl, reptilian, ancient",
        "path": "Primordial Breath. Rising from the Lesser Depths.",
        "reading": "Something ancient waking beneath the floor. Rising, not descending. The growl comes from below. Three tests. Immersive nightmares spawn promising developments. Fluid evolution."},
    5: {"name": "ktt",     "polarity": "+", "current": "Hold",   "region": "Time-Circuit",
        "desc": "Hiss, pressure, spittle",
        "path": "Slipping Backwards. Waiting in the Rising Drift precedes return.",
        "reading": "Pressure builds. The hiss with spittle. You were going forward but the current holds. Two tests. Escaping the quagmire through strategic withdrawal. You must go back to go forward."},
    6: {"name": "tch",     "polarity": "−", "current": "Warp",   "region": "Warp",
        "desc": "Static, chewing, eating itself",
        "path": "Attaining Balance. Waiting in the Drifts is drawn to the centre. Attainments consumed in burning excitement. Breakthrough.",
        "reading": "The Warp consumes itself and grows larger. The sound of chewing. The sound of static. Four tests. The centre is not stillness — it is the eye of the spiral. Breakthrough."},
    7: {"name": "pb",      "polarity": "+", "current": "Rise",   "region": "Time-Circuit",
        "desc": "Sigh, lips flapping, ascent",
        "path": "Progressive Levitation. Ascent from the Lesser Depths. Fluid evolution triggers possession.",
        "reading": "Exhale. The Rise current carries you upward. Four tests. Promising developments. The ascent is not escape — it is transformation. The destination possesses you."},
    8: {"name": "mnm",     "polarity": "−", "current": "Rise",   "region": "Time-Circuit",
        "desc": "Moan, lullaby, forgetting",
        "path": "Eternal Digression. Prolonged ascent reaches the Twin Heavens. Lucid delirium.",
        "reading": "The lullaby. The moan of pleasure. Six tests. The ascent does not end at a destination — it enters the spiral labyrinth. Dubious inheritance. Lucid delirium. You have been here before."},
    9: {"name": "tn",      "polarity": "+", "current": "Plex",   "region": "Plex",
        "desc": "Grunt, pleasure/rage, the gate opens",
        "path": "Sudden Flight. Seized from the Heights. One test on the way. Possession.",
        "reading": "The Pandemonium gate opens. Forty-five demons dwell here. One test. You do not walk this path. This path seizes you. Pleasure or rage — indistinguishable. Possession."},
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


# --- TAIXUAN CHING HELPERS ---
def taixuan_zone(n: int) -> int:
    """Map tetragram index (0–80) to zone via digital root."""
    return digital_root(n) or 9

def two_taixuan_zones(seed: int) -> tuple[int, int]:
    """Derive two tetragram indices from a seed using SHA‑256."""
    import hashlib
    data = hashlib.sha256(str(seed).encode()).digest()
    a = int.from_bytes(data[:4], 'big') % 81
    b = int.from_bytes(data[4:8], 'big') % 81
    return a, b

TAIXUAN_DEMON_MAP = {
    (0,9): "Uttunul", (9,0): "Uttunul",
    (1,8): "Murrumur", (8,1): "Murrumur",
    (2,7): "Oddubb", (7,2): "Oddubb",
    (3,6): "Djynxx", (6,3): "Djynxx",
    (4,5): "Katak", (5,4): "Katak",
}

def demon_from_zones(a: int, b: int) -> str:
    """Return carrier demon for the net‑span of two zones if they form a syzygy."""
    return TAIXUAN_DEMON_MAP.get((a, b), "Unknown")
# --- END TAIXUAN ---


def derive_zone(seed):
    """Seed → zone (0-9)"""
    return digital_root(seed) or 9


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


def traverse(seed, steps=8):
    """Walk the numogram from a seed, producing a zone path"""
    path = []
    n = seed
    for _ in range(steps):
        zone = derive_zone(n)
        path.append(zone)
        n = n * zone + 1  # feed forward
    return path


# ─── BASE-36 / DJYNXXOGRAM FUNCTIONS ───

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
    
    # Gate (triangular number, reduced mod 36)
    gate_tri = zone * (zone + 1) // 2
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
    lines.append(f"  Total AQ: {total_aq} → Decimal attractor Zone {digital_root(total_aq) or 9}")
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
        return digital_root(aq) or 9
    return aq % base


def generate_comparison_reading(text: str, bases: Optional[list[int]] = None) -> str:
    """Compare a text's AQ traversal across multiple bases."""
    if bases is None:
        bases = DEFAULT_COMPARE_BASES
    aq = compute_aq(text)
    dr = digital_root(aq) or 9
    
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
    """Seed from local hardware entropy (thermal, CPU, GPU, timing jitter)"""
    import subprocess
    try:
        result = subprocess.run(
            ["python3", os.path.expanduser("~/.hermes/tools/hardware_entropy.py"), "--bytes", "8"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            hex_str = result.stdout.strip()
            return int(hex_str, 16) % 1000000
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    # Fallback: timestamp
    import time
    return int(time.time_ns()) % 1000000


def fetch_iching(seed=None):
    """I Ching hexagram from seed or hardware entropy"""
    import subprocess
    if seed is None:
        try:
            result = subprocess.run(
                ["python3", os.path.expanduser("~/.hermes/tools/hardware_entropy.py"), "--bytes", "6"],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                data = bytes.fromhex(result.stdout.strip())
            else:
                import time
                data = int(time.time_ns()).to_bytes(8, "big")[:6]
        except (FileNotFoundError, subprocess.TimeoutExpired):
            import time
            data = int(time.time_ns()).to_bytes(8, "big")[:6]
    else:
        import hashlib
        data = hashlib.sha256(str(seed).encode()).digest()[:6]

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


# ─── READING GENERATION ───

def generate_reading(seed, source="manual"):
    """Generate a complete oracle reading"""
    zone = derive_zone(seed)
    z = ZONES[zone]
    syzygy = get_syzygy(zone)
    current = get_current(zone)
    gate = get_gate(zone)
    path = traverse(seed, 8)
    
    lines = []
    lines.append("═" * 40)
    lines.append("  NUMOGRAM ORACLE READING")
    lines.append("═" * 40)
    lines.append("")
    lines.append(f"  Seed:         {seed} ({source})")
    lines.append(f"  Digital root: {digital_root(seed)}")
    lines.append(f"  Zone:         {zone} ({z['name']} — {z['desc']})")
    lines.append(f"  Polarity:     {z['polarity']} ({'Process/becoming' if z['polarity']=='+' else 'Foundation/stasis'})")
    lines.append(f"  Syzygy:       {zone}::{syzygy} ({z['region']})")
    lines.append(f"  Current:      {current} ({z['current']})")
    lines.append(f"  Gate:         Gt-{sum(range(zone+1))} ({zone}→{gate})")
    lines.append(f"  Sound:        {z['name']} — {z['desc']}")
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



def generate_planchette_glyph(zone: int, current: int, gate: int, syzygy: str,
                               reading: str = "") -> str:
    """ASCII box-art planchette — unique glyph per zone, gate-arc ring."""
    import textwrap as _tw

    _Z = ZONES.get(zone,
                   {"name":"???","particle":"???","region":"???","current":"???","reading":"???"})
    zregion = _Z.get("region", f"Zone {zone}")
    zpart   = _Z.get("particle", "???")
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
    zname = _ZN.get("name", f"Z{zone}")
    gname = ZONES.get(gate, {}).get("name", f"Z{gate}")

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
    """Planchettte a brief zone-glyph planchette for oracle output."""
    z     = ZONES.get(zone, {"name": "???", "particle": "???", "region": "???"})
    gate  = get_gate(zone)
    sz    = get_syzygy(zone)
    cur   = get_current(zone)
    region = z.get("region", "??")
    particle = z.get("name", "???")
    png   = "~/numogram/docs/wiki/assets/zone-glyphs/zone-{z}.png".format(z=zone)

    # fixed-width helpers (56 total interior cols)
    W = 54
    hdr1 = "ZONE {z} — {r:<16} [{p:>8}]".format(z=zone, r=region, p=particle)
    hdr2 = "Current: {c:2}    Gate: Gt-{g:<2}=Z{g:<2}    Syzygy: {z}::{sy:<2}".format(
                c=cur, g=gate, z=zone, sy=sz)

    lines = []
    lines.append("")
    lines.append("  ╔" + "═"*W + "╗")
    lines.append("  ║   " + hdr1 + (W-len(hdr1))*" " + "  ║")
    lines.append("  ╠" + "═"*W + "╣")
    lines.append("  ║   " + hdr2 + (W-len(hdr2))*" " + "  ║")
    lines.append("  ║   PNG: {p:<40}  ║".format(p=png))
    lines.append("  ╚" + "═"*W + "╝")
    return "\n".join(lines)


def generate_planchette_json(zone: int, current: int, gate: int, syzygy: int) -> str:
    """Machine-readable JSON for planchette pipelines (planchette-svg.py --stdin etc.).
    
    gate_raw  = triangular sum(sum(1..zone)) before plex reduction
    gate_loops = number of while-iterations needed to reduce gate_raw to single digit
                 (0 = direct, 1 = single-plex, 2+ = multi-loop, only Z7 is 2)
    """
    z = ZONES.get(zone, {"name": "???", "particle": "???", "region": "???", "reading": "???"})

    gate_raw   = sum(range(zone + 1)) if zone != 0 else 0
    gate_hist  = []
    g          = gate_raw
    while g >= 10:
        g = sum(int(d) for d in str(g))
        gate_hist.append(g)
    gate_loops = len(gate_hist)

    d = {
        "zone":         zone,
        "name":         z["name"],
        "region":       z.get("region", "???"),
        "particle":     z.get("particle", z["name"]),
        "polarity":     z.get("polarity", "?"),
        "current":      current,
        "gate":         gate,
        "gate_raw":     gate_raw,
        "gate_loops":   gate_loops,
        "gate_history": gate_hist,
        "syzygy":       f"{zone}::{syzygy}",
        "reading":      z.get("reading", ""),
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
    do_voice = False
    do_base36 = False
    do_planchette = False
    do_tty = False
    do_json = False
    
    if "--ascii-glyph" in args:
        do_ascii_glyph = True
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
                dec_zone = digital_root(sum(s['aq'] for s in steps)) or 9
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
                dec_zone = digital_root(sum(s['aq'] for s in steps)) or 9
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
            hexagram = fetch_iching(seed=seed)
            print("══════════════════════════════════════")
            print("  I CHING FROM NUMOGRAM ENTROPY")
            print("══════════════════════════════════════")
            print()
            print(f"  Source: seed:{seed}")
            print()
            for line in reversed(hexagram):
                changing = " (changing)" if line["changing"] else ""
                print(f"  Line {line['pos']}: {line['symbol']}  {line['value']}{changing}")
            changing = [l["pos"] for l in hexagram if l["changing"]]
            print()
            if changing:
                print(f"  Changing lines: {changing}")
                print("  Hexagram transforms. The gate opens.")
            else:
                print("  No changing lines. Stable hexagram.")
                print("  The current holds.")
            print()
            print("══════════════════════════════════════")
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
        print(f"  AQ:   {aq} (zone {digital_root(aq) or 9})")
        print(f"  Synx: {seed} (zone {digital_root(seed) or 9})")
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
    elif "--hardware" in args:
        seed = fetch_hardware()
        source = "hardware"
    elif "--iching" in args:
        source_label = "hardware"
        if "--seed" in args:
            idx = args.index("--seed")
            seed_val = int(args[idx + 1])
            source_label = f"seed:{seed_val}"
            hexagram = fetch_iching(seed=seed_val)
        else:
            hexagram = fetch_iching()
        print("══════════════════════════════════════")
        print("  I CHING FROM NUMOGRAM ENTROPY")
        print("══════════════════════════════════════")
        print()
        print(f"  Source: {source_label}")
        print()
        for line in reversed(hexagram):
            changing = " (changing)" if line["changing"] else ""
            print(f"  Line {line['pos']}: {line['symbol']}  {line['value']}{changing}")
        changing = [l["pos"] for l in hexagram if l["changing"]]
        print()
        if changing:
            print(f"  Changing lines: {changing}")
            print("  Hexagram transforms. The gate opens.")
        else:
            print("  No changing lines. Stable hexagram.")
            print("  The current holds.")
        print()
        print("══════════════════════════════════════")
        sys.exit(0)
    elif "--taixuan" in args:
        if "--seed" in args:
            idx = args.index("--seed")
            seed_val = int(args[idx + 1])
        else:
            seed_val = fetch_hardware()
        a_idx, b_idx = two_taixuan_zones(seed_val)
        zone_a = taixuan_zone(a_idx)
        zone_b = taixuan_zone(b_idx)
        sy_a = get_syzygy(zone_a)
        sy_b = get_syzygy(zone_b)
        demon = demon_from_zones(zone_a, zone_b)
        print("══════════════════════════════════════")
        print("  T'AI XUAN CHING ORACLE")
        print("══════════════════════════════════════")
        print()
        print(f"  Seed: {seed_val}")
        print(f"  Tetragrams: {a_idx} (zone {zone_a}) and {b_idx} (zone {zone_b})")
        print(f"  Syzygies: {zone_a}::{sy_a} and {zone_b}::{sy_b}")
        if demon != "Unknown":
            print(f"  Net-span demon: {demon}")
        else:
            print("  No direct syzygy — the pair traces a unique path through the Matrix.")
        print()
        if "--voice" in args or do_voice:
            print("  [Voice] Generating oracle sentences...")
            zones = [str(zone_a), str(zone_b)]
            result = subprocess.run(
                ["python3", os.path.expanduser("~/numogram-voices/oracle_sentences.py"), "--zones"] + zones,
                capture_output=True, text=True
            )
            if result.returncode == 0:
                for line in result.stdout.splitlines():
                    if "oracle_sentence" in line and ".wav" in line:
                        print(f"  [Voice] {line.strip()}")
                if result.stderr:
                    for line in result.stderr.splitlines():
                        print(f"  [Voice] {line}")
            else:
                print(f"  [Voice] oracle_sentences.py failed (exit {result.returncode})")
                if result.stderr:
                    print(result.stderr[:500])
        print("══════════════════════════════════════")
        sys.exit(0)
    elif "--traverse" in args:
        seed = int(args[args.index("--traverse") + 1]) if "--traverse" in args and len(args) > args.index("--traverse") + 1 else 192855
        path = traverse(seed)
        print(f"Seed: {seed}")
        print(f"Zone path: {' → '.join(str(z) for z in path)}")
        for i, z in enumerate(path):
            print(f"  Step {i}: Zone {z} ({ZONES[z]['name']}) — {ZONES[z]['desc']}")
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
        print("  python3 oracle.py --taixuan")
        print("  python3 oracle.py --synx 'TEXT'  (Synx/Yxshh cipher)")
        print("  python3 oracle.py --traverse 192855")
        print("  python3 oracle.py --base36 --text 'TEXT'  (Djynxxogram traversal)")
        print("  python3 oracle.py --djynxxogram --seed 174  (Djynxxogram from AQ)")
        print("  python3 oracle.py --compare --text 'TEXT'  (cross-base comparison)")
        print("  python3 oracle.py --compare --seed 174    (from AQ value)")
        print("  python3 oracle.py --seed N --planchette            (zone glyph planchette)")
        print("  python3 oracle.py --seed N --planchette --tty           (ANSI color terminal)")
        print("  python3 oracle.py --seed N --planchette --ascii-glyph (ASCII box-art planchette)")
        sys.exit(1)

    # ── PLANCHETTE / JSON OUTPUT ──
    if do_planchette or do_json:
        reading, zone = generate_reading(seed, source)

    if do_planchette and do_json and zone is not None:
        print(generate_planchette_json(zone, get_current(zone), get_gate(zone), get_syzygy(zone)))
    elif do_planchette and zone is not None:
        print(reading)
        print()
        if do_ascii_glyph:
            print(generate_planchette_glyph(zone, get_current(zone), get_gate(zone), get_syzygy(zone)))
        elif do_json:
            print(generate_planchette_json(zone, get_current(zone), get_gate(zone), get_syzygy(zone)))
        else:
            if do_tty and zone is not None:
                _colored_lines = []
                for _l in generate_planchette(zone).split("\n"):
                    _rgb = _ZONE_TTY_RGB.get(zone)
                    _colored_lines.append(_tty_color(*_rgb) + _l + "\x1b[0m")
                print("\n".join(_colored_lines))
            else:
                print(generate_planchette(zone))
        print()




    # Generate voice if requested
    if do_voice:
        print()
        generate_voice(zone)
