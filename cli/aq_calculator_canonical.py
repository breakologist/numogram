#!/usr/bin/env python3
"""
AQ Calculator — Canonical Merged Version
Merged from aq_calculator.py (v1), aq_calculator_v2.py (v2), and aq_calculator_enhanced.py.
All AQ values verified against canonical cipher: A=10, B=11, ..., Z=35.

The math survived the machine that wrote it. Three versions, one cipher.
"""

import sys
import math
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, Tuple, List, Optional, Set

# ==================== AQ CIPHER ====================
# Canonical: A=10, B=11, ..., Z=35. Digits 0-9 = face value.
AQ_MAP = {str(i): i for i in range(10)}
AQ_MAP.update({chr(ord('A') + i): 10 + i for i in range(26)})
AQ_MAP.update({chr(ord('a') + i): 10 + i for i in range(26)})

def aq_value(text: str) -> int:
    """Calculate AQ value of a string. Digits = face value, A=10...Z=35."""
    total = 0
    for char in text:
        if char in AQ_MAP:
            total += AQ_MAP[char]
    return total

def digital_root(n: int) -> int:
    """Reduce to single digit via repeated summing. Returns 0 for input 0."""
    if n == 0:
        return 0
    return 1 + (n - 1) % 9

# ==================== NUMOGRAM ZONES ====================
ZONE_NAMES = {
    0: "Void", 1: "Surge", 2: "Hold", 3: "Warp", 4: "Sink",
    5: "Hinge", 6: "Vortex", 7: "Hold", 8: "Rise", 9: "Plex"
}

ZONE_REGIONS = {
    0: "plex", 1: "time_circuit", 2: "time_circuit", 3: "warp",
    4: "time_circuit", 5: "time_circuit", 6: "warp", 7: "time_circuit",
    8: "time_circuit", 9: "plex"
}

ZONE_FLAVOR = {
    0: "Plex — Abyssal Origin. The void before the first count.",
    1: "Time-Circuit — Initiating Spark. The first door.",
    2: "Time-Circuit — Renewed Drive. Oddubb's mirror.",
    3: "Warp — Chaotic Attractor (Djynxx). Primordial triangularity.",
    4: "Time-Circuit — Closure & Return. Katak's domain.",
    5: "Time-Circuit — Central Ruler. The hinge. Mercury.",
    6: "Warp — Upper Source / Vortical Recursion. CCRU=69→6.",
    7: "Time-Circuit — Heavy Sink Current. Blood and DNA.",
    8: "Time-Circuit — Receptive Pause. The mouth.",
    9: "Plex — Terminal Abyss (Uttunul). Cthelll. Iron core."
}

# ==================== SYZYGIES ====================
SYZYGIES = {
    frozenset({4, 5}): {"current": 1, "name": "Sink",  "demon": "Katak",   "region": "time_circuit"},
    frozenset({3, 6}): {"current": 3, "name": "Warp",  "demon": "Djynxx",  "region": "warp"},
    frozenset({2, 7}): {"current": 5, "name": "Hold",  "demon": "Oddubb",  "region": "time_circuit"},
    frozenset({1, 8}): {"current": 7, "name": "Rise",  "demon": "Murrumur","region": "time_circuit"},
    frozenset({0, 9}): {"current": 9, "name": "Plex",  "demon": "Uttunul", "region": "plex"},
}

def get_zone(aq: int) -> int:
    """Get numogram zone from AQ value."""
    return digital_root(aq)

def get_syzygy(zone: int) -> Optional[Dict]:
    """Get syzygy data for a zone's partner."""
    for pair, data in SYZYGIES.items():
        if zone in pair:
            partner = next(z for z in pair if z != zone)
            return {"zone": zone, "partner": partner, **data}
    return None

def get_current_name(zone: int) -> str:
    """Get the current name flowing through a zone."""
    syzygy = get_syzygy(zone)
    return syzygy["name"] if syzygy else "unknown"

# ==================== TRIANGULAR NUMBERS ====================
TRIANGULAR_NUMBERS = {i * (i + 1) // 2 for i in range(1, 100)}

def is_triangular(n: int) -> Tuple[bool, int]:
    """Check if n is triangular. Returns (is_triangular, T_index)."""
    if n < 1:
        return False, -1
    discriminant = 1 + 8 * n
    sqrt_disc = int(math.isqrt(discriminant))
    if sqrt_disc * sqrt_disc == discriminant:
        n_idx = (-1 + sqrt_disc) / 2
        if n_idx == int(n_idx):
            return True, int(n_idx)
    return False, -1

def is_gate_number(aq: int) -> Tuple[bool, str]:
    """Check if AQ value is a gate number (cumulation)."""
    tri, idx = is_triangular(aq)
    if tri:
        return True, f"Gt-{aq} = T({idx})"
    return False, ""

# ==================== GATES ====================
def cumulate(n: int) -> int:
    """Cumulation: C(n) = n*(n-1)/2"""
    return n * (n - 1) // 2

GATES = {}
for z in range(10):
    gt = cumulate(z)
    dr = digital_root(gt)
    GATES[z] = {"gate_value": gt, "target_zone": dr, "triangular": is_triangular(gt)[0]}

NAMED_GATES = {
    "Gt-06": (3, 6), "Gt-21": (6, 3),
    "Gt-36": (8, 9), "Gt-45": (9, 9),
}

# ==================== ANSI COLORS ====================
ANSI = {
    0: "\033[38;5;238m", 1: "\033[38;5;226m", 2: "\033[38;5;214m",
    3: "\033[38;5;201m", 4: "\033[38;5;51m",  5: "\033[38;5;46m",
    6: "\033[38;5;39m",  7: "\033[38;5;124m", 8: "\033[38;5;147m",
    9: "\033[38;5;93m",
}
ANSI_RESET = "\033[0m"
ANSI_BOLD = "\033[1m"
ANSI_DIM = "\033[2m"

def get_zone_color(zone: int) -> str:
    """Get ANSI color code for a zone."""
    return ANSI.get(zone, "")

def colorize(text: str, zone: int) -> str:
    """Apply zone color to text."""
    return f"{get_zone_color(zone)}{text}{ANSI_RESET}"

# ==================== JOURNAL ====================
JOURNAL_FILE = Path("aq_journal.jsonl")

def save_to_journal(text: str, aq: int, zone: int, syzygy: Optional[Dict] = None):
    """Append analysis to journal file (JSONL)."""
    entry = {
        "timestamp": datetime.now().isoformat(),
        "input": text,
        "aq": aq,
        "zone": zone,
        "digital_root": digital_root(aq),
        "triangular": is_triangular(aq)[0],
        "gate": is_gate_number(aq)[1] if is_gate_number(aq)[0] else None,
        "syzygy": syzygy,
    }
    with open(JOURNAL_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

# ==================== ANALYSIS ====================
def analyze(text: str, verbose: bool = True) -> Dict:
    """Full AQ analysis of a word or phrase."""
    aq = aq_value(text)
    zone = get_zone(aq)
    dr = digital_root(aq)
    tri, tri_idx = is_triangular(aq)
    gate, gate_name = is_gate_number(aq)
    syzygy = get_syzygy(zone)

    result = {
        "text": text,
        "aq": aq,
        "digital_root": dr,
        "zone": zone,
        "zone_name": ZONE_NAMES.get(zone, "unknown"),
        "region": ZONE_REGIONS.get(zone, "unknown"),
        "triangular": tri,
        "triangular_index": tri_idx if tri else None,
        "gate": gate_name if gate else None,
        "syzygy": syzygy,
    }

    if verbose:
        print(colorize(f"\n  {text}", zone))
        print(f"    AQ = {aq}  |  DR = {dr}  |  Zone {zone} ({ZONE_NAMES.get(zone, '?')})")
        print(f"    Region: {ZONE_REGIONS.get(zone, '?')}")
        if tri:
            print(f"    Triangular: T({tri_idx}) = {aq}")
        if gate:
            print(f"    Gate: {gate_name}")
        if syzygy:
            print(f"    Syzygy: {zone}::{syzygy['partner']} ({syzygy['name']}) → {syzygy['demon']}")
        print(f"    Flavor: {ZONE_FLAVOR.get(zone, '?')}")

    save_to_journal(text, aq, zone, syzygy)
    return result

def analyze_phrase(phrase: str) -> List[Dict]:
    """Analyze each word in a phrase separately."""
    words = re.findall(r'[A-Za-z0-9]+', phrase)
    results = []
    for word in words:
        result = analyze(word, verbose=True)
        results.append(result)

    # Also analyze the full phrase
    print(colorize("\n  [FULL PHRASE]", 5))
    full = analyze(phrase, verbose=True)
    results.append(full)
    return results

# ==================== INTERACTIVE ====================
def interactive():
    """Interactive AQ calculator. Type a word or phrase, get analysis."""
    print(colorize("\n  AQ Calculator — Canonical", 5))
    print("  Type a word or phrase. 'q' to quit.\n")

    while True:
        try:
            text = input(colorize("  ⊹ ", 5)).strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  ∿ The currents return to zero. ∿")
            break

        if text.lower() in ('q', 'quit', 'exit'):
            print("  ∿ The currents return to zero. ∿")
            break

        if not text:
            continue

        if ' ' in text:
            analyze_phrase(text)
        else:
            analyze(text)

# ==================== MAIN ====================
if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Command-line mode: analyze arguments
        for arg in sys.argv[1:]:
            if ' ' in arg:
                analyze_phrase(arg)
            else:
                analyze(arg)
    else:
        interactive()
