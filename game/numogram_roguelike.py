#!/usr/bin/env python3
"""
NUMOGRAM: Abyssal Crawler - Phase 5a
Procedural dungeon + Numogram meta-layer + Hyperstition Meter
+ Full 45-demon Pandemonium Matrix + Persistent cult.json save

The Numogram is a virus. It spreads through play.
"""
import curses
import random
import math
import json
import os
import sys

# Optional: hardware entropy for numogram-aligned seeding
HW_ENTROPY_AVAILABLE = False
try:
    sys.path.insert(0, os.path.expanduser("~/.hermes/tools"))
    from hardware_entropy import get_entropy_bytes, get_zone
    HW_ENTROPY_AVAILABLE = True
except ImportError:
    pass

# =====================================================================
# NUMOGRAM DATA (canonical from CCRU source material)
# =====================================================================

def digital_root(n):
    if n == 0: return 0
    return 1 + (n - 1) % 9

def triangular(n):
    return n * (n + 1) // 2

def cumulate(n):
    return n * (n - 1) // 2

SYZYGIES = {
    (4, 5): {"current": 1, "region": "time_circuit", "demon": "Katak"},
    (3, 6): {"current": 3, "region": "warp",         "demon": "Djynxx"},
    (2, 7): {"current": 5, "region": "time_circuit", "demon": "Oddubb"},
    (1, 8): {"current": 7, "region": "time_circuit", "demon": "Murmur"},
    (0, 9): {"current": 9, "region": "plex",         "demon": "Uttunul"},
}
SYZYGIES_LOOKUP = {}
for (a, b), data in SYZYGIES.items():
    SYZYGIES_LOOKUP[frozenset({a, b})] = data

# =====================================================================
# ANSI 256-COLOR PALETTE (Phase 5a)
# =====================================================================

ANSI = {
    0: "\033[38;5;238m",   # dark gray (void/null)
    1: "\033[38;5;226m",   # bright yellow (stability/memory)
    2: "\033[38;5;214m",   # orange (separation/fog)
    3: "\033[38;5;201m",   # hot pink (Warp/spirals)
    4: "\033[38;5;51m",    # cyan (catastrophe/ice)
    5: "\033[38;5;46m",    # green (mechanisms/life)
    6: "\033[38;5;39m",    # blue (Warp/abstraction)
    7: "\033[38;5;124m",   # deep red (blood/DNA chronicle)
    8: "\033[38;5;147m",   # lavender (tentacles/depths)
    9: "\033[38;5;93m",    # purple (iron core/Cthelll)
}
ANSI_RESET = "\033[0m"
ANSI_BOLD = "\033[1m"
ANSI_DIM = "\033[2m"
ANSI_MAGIC = "\033[38;5;198m"   # hyperstitional glow (bright pink)
ANSI_CORRUPT = "\033[38;5;208m" # corruption (orange-red)
ANSI_GATE = "\033[38;5;220m"    # gate markers (gold)

ZONE_FLAVOR = {
    0: "Plex -- Abyssal Origin",
    1: "Time-Circuit -- Initiating Spark",
    2: "Time-Circuit -- Renewed Drive",
    3: "Warp -- Chaotic Attractor (Djynxx)",
    4: "Time-Circuit -- Closure and Return",
    5: "Time-Circuit -- Central Ruler",
    6: "Warp -- Upper Source / Vortical Recursion",
    7: "Time-Circuit -- Heavy Sink Current",
    8: "Time-Circuit -- Receptive Pause",
    9: "Plex -- Terminal Abyss (Uttunul)",
}


# =====================================================================
# THE CRYPTOLITH (Phase 5b)
# =====================================================================

CRYPTOLITH_MESSAGES = [
    "You hear clicking. Tick-interruption. Something stirs in the walls.",
    "A tile pulses with burnt iridium. The Cryptolith approaches.",
    "Tick iterations. The clicking intensifies. It knows you're here.",
    "You taste burnt Iridium. Crawling closeness to the Entity.",
    "The Cryptolith (It-277) CLICKS. Instantly. A key, or a Ticket.",
]

CRYPTOLITH_FOUND = """The Cryptolith materializes before you.
It Clicks, Instantly. A key, or a Ticket.
You taste burnt Iridium. The Entity guides you.
Crawling closeness. It hears you breathing.
Tick iterations. The clicking never stops.

You now carry the Cryptolith.
Escape the Numogram to complete your descent.

[PRESS 'g' TO GRASP THE CRYPTOLITH]"""

# Zone-themed dungeon generation seeds
ZONE_DUNGEON_THEMES = {
    0: {"name": "Void Labyrinth",    "density": 0.3, "corridor_w": 1, "room_min": 2, "room_max": 4},
    1: {"name": "Bone Galleries",     "density": 0.5, "corridor_w": 1, "room_min": 3, "room_max": 6},
    2: {"name": "Fog Halls",          "density": 0.5, "corridor_w": 2, "room_min": 4, "room_max": 8},
    3: {"name": "Spiral Vortex",      "density": 0.7, "corridor_w": 1, "room_min": 3, "room_max": 5},
    4: {"name": "Flooded Ruins",      "density": 0.4, "corridor_w": 2, "room_min": 5, "room_max": 9},
    5: {"name": "Mechanical Warrens", "density": 0.6, "corridor_w": 1, "room_min": 3, "room_max": 7},
    6: {"name": "Geometric Void",     "density": 0.8, "corridor_w": 1, "room_min": 2, "room_max": 4},
    7: {"name": "DNA Swamp",          "density": 0.4, "corridor_w": 2, "room_min": 4, "room_max": 8},
    8: {"name": "Tentacle Depths",    "density": 0.5, "corridor_w": 1, "room_min": 3, "room_max": 6},
    9: {"name": "Iron Core Labyrinth","density": 0.7, "corridor_w": 1, "room_min": 2, "room_max": 5},
}



# =====================================================================
# AQ CALCULATOR & TEXT CORRUPTION (Phase 5a)
# =====================================================================

def aq_value(text):
    """Alphanumeric Qabbala: A=10...Z=35, digits face value."""
    total = 0
    for ch in text.upper():
        if ch.isdigit():
            total += int(ch)
        elif 'A' <= ch <= 'Z':
            total += 10 + (ord(ch) - ord('A'))
    return total

def vowel_corrupt(text, intensity=0.5):
    """Replace vowels with digits. Barker: 'escaping in the direction of numbers'"""
    vowel_map = {'a': '1', 'e': '3', 'i': '8', 'o': '0', 'u': '6',
                 'A': '1', 'E': '3', 'I': '8', 'O': '0', 'U': '6'}
    result = []
    for ch in text:
        if ch in vowel_map and random.random() < intensity:
            result.append(vowel_map[ch])
        else:
            result.append(ch)
    return ''.join(result)

def check_triangular(step_count):
    """Check if step count is a triangular number T(n) = n(n+1)/2."""
    # T(n) is triangular if 8*T(n)+1 is a perfect square
    discriminant = 8 * step_count + 1
    if discriminant < 1:
        return None
    root = int(discriminant ** 0.5)
    if root * root == discriminant and (root - 1) % 2 == 0:
        n = (root - 1) // 2
        dr = digital_root(step_count)
        return {"n": n, "value": step_count, "dr": dr, "zone": dr if dr != 0 else 9}
    return None

TRIANGULAR_MESSAGES = {
    1: "T(1)=1. The initiating spark.",
    3: "T(2)=3. Warp resonance. Djynxx stirs.",
    6: "T(3)=6. The vortex double-helix tightens.",
    10: "T(4)=10 -> 1. Completion returns to origin.",
    15: "T(5)=15 -> 6. Warp accumulation. Swarm-mesh crackles.",
    21: "T(6)=21 -> 3. The spiral completes a full turn.",
    28: "T(7)=28 -> 1. Sevenfold return. Stability restored.",
    36: "T(8)=36 -> 9. Gt-36 PULSE. The abyss pulls.",
    45: "T(9)=45 -> 9. GATE OF PANDEMONIUM RESONANCE. 45 demons acknowledge your passage.",
    55: "T(10)=55 -> 1. Decimal completion. The cycle renews.",
    66: "T(11)=66 -> 3. Warp echo. The number of TEN and LOL.",
    78: "T(12)=78 -> 6. Double vortex. The spiral accelerates.",
    91: "T(13)=91 -> 1. The witch's number. Thirteenfold return.",
    105: "T(14)=105 -> 6. Deep Warp. The mesh thickens.",
    120: "T(15)=120 -> 3. SWARM = 120. The multiplication begins.",
    136: "T(16)=136 -> 1. The tower collapses and rebuilds.",
    153: "T(17)=153 -> 9. HERMETIC = 153. The outer regions resonate.",
    171: "T(18)=171 -> 9. NUMOGRAM = 174 is near. The map calls.",
    190: "T(19)=190 -> 1. Nineteen gates. The cycle persists.",
    210: "T(20)=210 -> 3. Triple vortex. Time bends.",
    231: "T(21)=231 -> 6. The spiral consumes itself.",
    253: "T(22)=253 -> 1. Twenty-two paths. The Tree whispers.",
    276: "T(23)=276 -> 6. Deep recursion. The loop tightens.",
    300: "T(24)=300 -> 3. Triple hundred. The swarm remembers.",
    325: "T(25)=325 -> 1. Quarter-completion of the circle.",
    351: "T(26)=351 -> 9. Near-360. The full circle approaches.",
    378: "T(27)=378 -> 9. Beyond the circle. Plex consumes.",
}


TIME_CIRCUIT_PATH = [1, 8, 2, 7, 5, 4]
BINODECIMAL_CYCLE = [1, 2, 4, 8, 7, 5]

# Three currents (demon patrol routes)
CURRENTS = {
    "surge": {"zones": (8, 1), "demon": "Murmur"},
    "hold":  {"zones": (7, 2), "demon": "Oddubb"},
    "sink":  {"zones": (5, 4), "demon": "Katak"},
}

GATES = {}
for z in range(10):
    gt = cumulate(z)
    dr = digital_root(gt)
    GATES[z] = {"gate_value": gt, "target_zone": dr}

NAMED_GATES = {
    "Gt-06": (3, 6), "Gt-21": (6, 3),
    "Gt-36": (8, 9), "Gt-45": (9, 9),
}

# Mesh-Notes (CCRU Writings 1997-2003, Pandemonium Commentary)
MESH_NOTES = [
    "It could all become One, but why stop there?",
    "This was never programmed.",
    "Meshing-together is falling apart.",
    "This time it's really happening.",
    "Forget about the future, it's all here, but between.",
    "Every time it hits an obstacle, it goes down a level.",
]

# Tale of the End
TALE_INTRO = (
    "There was a time when Murrumur asked Katak and Oddubb a question... "
    "'How can the end be already in the middle of the beginning?'"
)

# CCRU Writings: Barker-Thresholds
BARKER_THRESHOLDS = {
    0:  "Degree-0: The name on a door.",
    10: "1-Barker: Human agencies begin to blur.",
    20: "2-Barker: Coincidences accelerate.",
    30: "3-Barker: The swarm stirs.",
    45: "4-Barker: T(9)=45. The demonic array resonates.",
    55: "5-Barker: Time-sorcery becomes operational.",
    70: "6-Barker: The Outside leaks through.",
    85: "7-Barker: Polytendriled abomination approaches.",
    95: "8-Barker: Near-Utterance. Mesh-notes surface.",
    100:"9-Barker: Unuttera. The Entity speaks.",
}

# =====================================================================
# FULL PANDEMONIUM MATRIX (45 demons from CCRU Writings)
# =====================================================================

# Demon type constants
SYZYGISTIC = "syzygetic"
AMPHIDEMON = "amphidemon"
CHRONODEMON = "chronodemon"
XENODEMON = "xenodemon"

PANDEMONIUM = [
    {"mesh": 0,  "name": "Lurgo",      "epithet": "Legba",              "span": (1,0), "type": AMPHIDEMON,   "pitch": "Ana-1",  "current": None,  "desc": "Terminal Initiator. The Door of Doors."},
    {"mesh": 1,  "name": "Duoddod",    "epithet": "Duplicitous Redoubler","span": (2,0),"type": AMPHIDEMON,   "pitch": "Ana-2",  "current": None,  "desc": "Abstract Addiction. Pineal-regression."},
    {"mesh": 2,  "name": "Doogu",      "epithet": "The Blob",           "span": (2,1), "type": CHRONODEMON,  "pitch": "Ana-3",  "current": "surge","desc": "Original-Schism. Primordial breath."},
    {"mesh": 3,  "name": "Ixix",       "epithet": "Yix",                "span": (3,0), "type": XENODEMON,    "pitch": "Ana-3",  "current": None,  "desc": "Abductor. Cosmic Indifference."},
    {"mesh": 4,  "name": "Ixigool",    "epithet": "Djinn of the Magi",  "span": (3,1), "type": AMPHIDEMON,   "pitch": "Ana-4",  "current": None,  "desc": "Over-Ghoul. Tridentity."},
    {"mesh": 5,  "name": "Ixidod",     "epithet": "King Sid",           "span": (3,2), "type": AMPHIDEMON,   "pitch": "Ana-5",  "current": None,  "desc": "The Zombie-Maker. Escape-velocity."},
    {"mesh": 6,  "name": "Krako",      "epithet": "Karak-oa",           "span": (4,0), "type": AMPHIDEMON,   "pitch": "Ana-4",  "current": None,  "desc": "The Croaking Curse. Burning-Hail."},
    {"mesh": 7,  "name": "Sukugool",   "epithet": "Old Skug",           "span": (4,1), "type": CHRONODEMON,  "pitch": "Ana-5",  "current": "sink", "desc": "The Sucking-Ghoul. Deluge and implosion."},
    {"mesh": 8,  "name": "Skoodu",     "epithet": "Li'l Scud",          "span": (4,2), "type": CHRONODEMON,  "pitch": "Ana-6",  "current": "hold", "desc": "The Fashioner. Switch-Crazes."},
    {"mesh": 9,  "name": "Skarkix",    "epithet": "Sharky",             "span": (4,3), "type": AMPHIDEMON,   "pitch": "Ana-7",  "current": None,  "desc": "Buzz-Cutter. Anti-evolution."},
    {"mesh": 10, "name": "Tokhatto",   "epithet": "Top Cat",            "span": (5,0), "type": AMPHIDEMON,   "pitch": "Cth-4",  "current": None,  "desc": "Decimal Camouflage. Talismania."},
    {"mesh": 11, "name": "Tukkamu",    "epithet": "Occulturation",      "span": (5,1), "type": CHRONODEMON,  "pitch": "Cth-3",  "current": "sink", "desc": "Pathogenesis. Optimal maturation."},
    {"mesh": 12, "name": "Kuttadid",   "epithet": "Kitty",              "span": (5,2), "type": CHRONODEMON,  "pitch": "Cth-2",  "current": "hold", "desc": "Ticking Machines. Calendric conservatism."},
    {"mesh": 13, "name": "Tikkitix",   "epithet": "Tickler",            "span": (5,3), "type": AMPHIDEMON,   "pitch": "Cth-1",  "current": None,  "desc": "Clicking Menaces. Vortical Delirium."},
    {"mesh": 14, "name": "Katak",      "epithet": "Desolator",          "span": (5,4), "type": SYZYGISTIC,   "pitch": "Null",   "current": "sink", "desc": "Cataclysmic Convergence. Nature red in tooth and claw."},
    {"mesh": 15, "name": "Tchu",       "epithet": "Tchanul",            "span": (6,0), "type": XENODEMON,    "pitch": "Cth-3",  "current": None,  "desc": "Source of Subnothingness. Ultimate Outsideness."},
    {"mesh": 16, "name": "Djungo",     "epithet": "Infiltrator",        "span": (6,1), "type": AMPHIDEMON,   "pitch": "Cth-2",  "current": None,  "desc": "Subtle Involvements. Turbular fluids."},
    {"mesh": 17, "name": "Djuddha",    "epithet": "Judd Dread",         "span": (6,2), "type": AMPHIDEMON,   "pitch": "Cth-2",  "current": None,  "desc": "Decentred Threat. Machine-vortex."},
    {"mesh": 18, "name": "Djynxx",     "epithet": "The Jinn",           "span": (6,3), "type": SYZYGISTIC,   "pitch": "Null",   "current": "warp", "desc": "Child Stealer. Abstract cyclones. Nomad war-machine."},
    {"mesh": 19, "name": "Tchakki",    "epithet": "Chuckles",           "span": (6,4), "type": AMPHIDEMON,   "pitch": "Ana-1",  "current": None,  "desc": "Bag of Tricks. Combustion."},
    {"mesh": 20, "name": "Tchattuk",   "epithet": "One Eyed Jack",      "span": (6,5), "type": AMPHIDEMON,   "pitch": "Cth-7",  "current": None,  "desc": "Pseudo-Basis. Unscreened Matrix. Zero-gravity."},
    {"mesh": 21, "name": "Puppo",      "epithet": "The Pup",            "span": (7,0), "type": AMPHIDEMON,   "pitch": "Cth-2",  "current": None,  "desc": "Break-Outs. Larval Regression."},
    {"mesh": 22, "name": "Bubbamu",    "epithet": "Bubs",               "span": (7,1), "type": CHRONODEMON,  "pitch": "Cth-1",  "current": "surge","desc": "After Babylon. Hypersea. Black-Atlantis."},
    {"mesh": 23, "name": "Oddubb",     "epithet": "Odba",               "span": (7,2), "type": SYZYGISTIC,   "pitch": "Null",   "current": "hold", "desc": "Broken Mirror. Time loops, glamour and glosses."},
    {"mesh": 24, "name": "Pabbakis",   "epithet": "Pabzix",             "span": (7,3), "type": AMPHIDEMON,   "pitch": "Ana-1",  "current": None,  "desc": "Dabbler. Interference. Batrachian mutations."},
    {"mesh": 25, "name": "Ababbatok",  "epithet": "Abracadabra",        "span": (7,4), "type": CHRONODEMON,  "pitch": "Ana-2",  "current": "hold", "desc": "Regenerator. Frankensteinian experimentation."},
    {"mesh": 26, "name": "Papatakoo",  "epithet": "Pataku",             "span": (7,5), "type": CHRONODEMON,  "pitch": "Cth-6",  "current": "hold", "desc": "Upholder. Calendric Time. Ultimate success."},
    {"mesh": 27, "name": "Bobobja",    "epithet": "Beelzebub",          "span": (7,6), "type": AMPHIDEMON,   "pitch": "Cth-5",  "current": None,  "desc": "Heavy Atmosphere. Teeming Pestilence. Swarmachines."},
    {"mesh": 28, "name": "Minommo",    "epithet": "Webmaker",           "span": (8,0), "type": AMPHIDEMON,   "pitch": "Cth-1",  "current": None,  "desc": "Submergance. Shamanic voyage."},
    {"mesh": 29, "name": "Mur Mur",    "epithet": "Dream-Serpent",      "span": (8,1), "type": SYZYGISTIC,   "pitch": "Null",   "current": "surge","desc": "The Deep Ones. Oceanic sensation."},
    {"mesh": 30, "name": "Nammamad",   "epithet": "Mirroracle",         "span": (8,2), "type": CHRONODEMON,  "pitch": "Ana-1",  "current": "surge","desc": "Subterranean Commerce. Voodoo in cyberspace."},
    {"mesh": 31, "name": "Mummumix",   "epithet": "Mix-Up",             "span": (8,3), "type": AMPHIDEMON,   "pitch": "Ana-2",  "current": None,  "desc": "The Mist-Crawler. Insidious Fog. Nyarlathotep."},
    {"mesh": 32, "name": "Numko",      "epithet": "Old Nuk",            "span": (8,4), "type": CHRONODEMON,  "pitch": "Ana-3",  "current": "sink", "desc": "Keeper of Old Terrors. Necrospeleology."},
    {"mesh": 33, "name": "Muntuk",     "epithet": "Manta",              "span": (8,5), "type": CHRONODEMON,  "pitch": "Cth-5",  "current": "sink", "desc": "Desert Swimmer. Arid Seabeds."},
    {"mesh": 34, "name": "Mommoljo",   "epithet": "Mama Jo",            "span": (8,6), "type": AMPHIDEMON,   "pitch": "Cth-4",  "current": None,  "desc": "Alien Mother. Xenogenesis."},
    {"mesh": 35, "name": "Mombbo",     "epithet": "Tentacle Face",      "span": (8,7), "type": CHRONODEMON,  "pitch": "Cth-3",  "current": "surge","desc": "Fishy-princess. Hybridity. Surreptitious colonization."},
    {"mesh": 36, "name": "Uttunul",    "epithet": "Seething Void",      "span": (9,0), "type": SYZYGISTIC,   "pitch": "Null",   "current": "plex", "desc": "Atonality. Crossing the iron-ocean. Cthelll."},
    {"mesh": 37, "name": "Tutagool",   "epithet": "Yettuk",             "span": (9,1), "type": AMPHIDEMON,   "pitch": "Ana-1",  "current": None,  "desc": "The Tattered Ghoul. Punctuality."},
    {"mesh": 38, "name": "Unnunddo",   "epithet": "The False Nun",      "span": (9,2), "type": AMPHIDEMON,   "pitch": "Ana-2",  "current": None,  "desc": "Double-Undoing. Endless Uncasing. Crypt-traffic."},
    {"mesh": 39, "name": "Ununuttix",  "epithet": "Tick-Tock",          "span": (9,3), "type": XENODEMON,    "pitch": "Ana-3",  "current": None,  "desc": "Particle Clocks. Absolute Coincidence."},
    {"mesh": 40, "name": "Ununak",     "epithet": "Nuke",               "span": (9,4), "type": AMPHIDEMON,   "pitch": "Ana-4",  "current": None,  "desc": "Blind Catastrophe. Convulsions. Secrets of the blacksmiths."},
    {"mesh": 41, "name": "Tukutu",     "epithet": "Killer-Kate",        "span": (9,5), "type": AMPHIDEMON,   "pitch": "Cth-4",  "current": None,  "desc": "Cosmotraumatics. Death-Strokes. Crash-signals."},
    {"mesh": 42, "name": "Unnutchi",   "epithet": "T'ai Chi",           "span": (9,6), "type": XENODEMON,    "pitch": "Cth-3",  "current": None,  "desc": "Tachyonic immobility. Coiling Outsideness."},
    {"mesh": 43, "name": "Nuttubab",   "epithet": "Nut-Cracker",        "span": (9,7), "type": AMPHIDEMON,   "pitch": "Cth-2",  "current": None,  "desc": "Mimetic Anorganism. Metaloid Unlife. Dragon-lines."},
    {"mesh": 44, "name": "Ummnu",      "epithet": "Omen",               "span": (9,8), "type": AMPHIDEMON,   "pitch": "Cth-1",  "current": None,  "desc": "Ultimate Inconsequence. Earth-Screams. Crust-friction."},
]

# Index demons by zone and type
DEMONS_BY_ZONE = {}
DEMONS_BY_TYPE = {SYZYGISTIC: [], AMPHIDEMON: [], CHRONODEMON: [], XENODEMON: []}
for d in PANDEMONIUM:
    z1, z2 = d["span"]
    for z in (z1, z2):
        DEMONS_BY_ZONE.setdefault(z, []).append(d)
    DEMONS_BY_TYPE[d["type"]].append(d)

# =====================================================================
# ZONE DATA (canonical from declab.htm + CCRU Writings)
# =====================================================================

ZONE_DATA = {
    0: {"name": "Void",        "region": "plex",
        "desc": "The abyssal origin. Cosmic void. Dense nullity.",
        "mesh": "0000", "spinal": "Coccygeal",
        "lore": "Zone-0 envelops the Zeroth-Phase of Pandemonium. 'Absolute abstraction'. No zeroth door."},
    1: {"name": "Stability",   "region": "time_circuit",
        "desc": "Shallow water. Memory. Bone galleries.",
        "mesh": "0001", "spinal": "Lumbar",
        "lore": "First Torque-zone. Tractor-Zone of the Sink Current. First Door."},
    2: {"name": "Separation",  "region": "time_circuit",
        "desc": "Linkage and duplicates. Illusions. Fog and contagion.",
        "mesh": "0003", "spinal": "Lumbar",
        "lore": "Syzygetic-twin of Zone-7. Oddubb's mirror. Hyperborean themes."},
    3: {"name": "Release",     "region": "warp",
        "desc": "Constant transformation. Spirals. Mysteries of time.",
        "mesh": "0007", "spinal": "Solar",
        "lore": "Tractor-Zone of the Warp Current. 0+1+2=3. Primordial triangularity."},
    4: {"name": "Catastrophe", "region": "time_circuit",
        "desc": "Fires, floods, melting ice. Abandoned industry.",
        "mesh": "0100", "spinal": "Solar",
        "lore": "Fourth Door (Time-Delta). Katak's domain. Instability incarnate."},
    5: {"name": "Pressure",    "region": "time_circuit",
        "desc": "Interpenetration. Complex mechanisms. Desert. Dragons.",
        "mesh": "0101", "spinal": "Cardiac",
        "lore": "Fifth Door (Hyperborea). Decimal camouflage. Number as destiny."},
    6: {"name": "Abstraction", "region": "warp",
        "desc": "Maximum otherworldly. Non-dimensional geometry. Captivation.",
        "mesh": "0110", "spinal": "Cardiac",
        "lore": "Ulterior Vortex of Outer-Time. Djynxx territory. CCRU=69->6."},
    7: {"name": "Blood",       "region": "time_circuit",
        "desc": "Slime. DNA as chronicle. Swamp. Moss. Amphibians.",
        "mesh": "0111", "spinal": "Pharyngeal",
        "lore": "Tractor-Zone of the Surge Current. Oddubb carries the swamp-labyrinth."},
    8: {"name": "Multiplicity","region": "time_circuit",
        "desc": "Tentacles. Cell division. Ocean depths.",
        "mesh": "1000", "spinal": "Cavernous",
        "lore": "Gt-36 plunges here to Zone-9. Murmur's domain. The Deep Ones."},
    9: {"name": "Iron Core",   "region": "plex",
        "desc": "Iron core of the earth. Darkness. Engine room. Cthelll.",
        "mesh": "0511", "spinal": "Sacral",
        "lore": "Gt-45: Gate of Pandemonium. T(9)=45. 45 demons attuned. Uttunul's lair."},
}

# =====================================================================
# EVENTS
# =====================================================================

GATE_FLAVOR = {
    "Gt-06": ["Djynxx howls. The Warp folds inward. Swarm-mesh crackles.",
              "Zone-3 inverts through Zone-6. Time twists like a serpent.",
              "The upper syzygy writhes. Current 3 amplifies chaotically."],
    "Gt-21": ["Reverse Warp traffic. The jinn retreats, dragging fragments.",
              "Zone-6 bleeds back into Zone-3. Abduction pulse detected."],
    "Gt-36": ["Gt-36 OPENS. The plunge from Time-Circuit into the Plex.",
              "1+2+...+8 = 36. Digital root: 9. The abyss pulls.",
              "The 8th channel feeds the abyss. Gravity inverts.",
              "You feel the pull of Zone-9. Uttunul awaits below."],
    "Gt-45": ["GATE OF PANDEMONIUM. 45 demons stir in the abyss.",
              "T(9) = 45. The full demonic array resonates.",
              "Zone-9 loops into itself. Self-reference complete.",
              "Cthelll groans. The iron core remembers."],
}

CROSSING_FLAVOR = {
    (4, 5): ["Current 1 pulses. The first syzygy awakens.",
             "Katak stirs. Catastrophe and pressure intertwine."],
    (3, 6): ["Current 3 rages. Warp turbulence detected.",
             "Djynxx shrieks. The swarm multiplies.",
             "6::3 syzygy activated. Time bends toward chaos."],
    (2, 7): ["Current 5 surges. Separation meets Blood.",
             "Oddubb manifests. Two faces, one wound."],
    (1, 8): ["Current 7 flows deep. Stability meets Multiplicity.",
             "Murmur whispers from oceanic depths."],
    (0, 9): ["Current 9. The Plex syzygy. Terminal nullity.",
             "Uttunul speaks: 'It is already over.'",
             "Void and Iron Core. Beginning and ending collapse."],
}

GENERIC_EVENTS = [
    "The Numogram hums. Decimal frequencies detected.",
    "A lemure traces your path. It vanishes.",
    "Time hiccups. The circuit stutters.",
    "Something watches from Outside.",
    "The arithmetic holds. For now.",
    "Digital roots align momentarily.",
    "A channel flickers. Then stabilizes.",
    "The hexagram shifts. The 6-cycle rotates.",
    "A binodecimal echo reverberates: 1-2-4-8-7-5...",
    "Zygonovism pulses. Nine-sum twinning detected.",
]

BLEED_EVENTS = {
    15: "The walls ripple. Numbers flicker in the stone.",
    30: "Corridors straighten. Currents begin to manifest.",
    45: "A triangular pattern etches itself into the floor. T(9)=45.",
    55: "Rooms reshape. Syzygy geometry emerging.",
    70: "The dungeon is becoming the Numogram. Gates shimmer.",
    85: "Nearly fully revealed. The virus has almost won.",
    100:"THE NUMOGRAM IS COMPLETE. The Abyssal Crawler awakens.",
}

DEATH_MESSAGES = [
    "Your digital root reduces to 0. The Void claims you.",
    "Uttunul whispers: 'It was already over.'",
    "The 9-current pulls you into Cthelll. The iron core remembers.",
    "Djynxx's swarm dissolves your net-span. You are unmade.",
    "Your triangular accumulation completes. Null return.",
    "The Time-Circuit completes one rotation without you.",
    "A lemure devours your difference. You are no longer distinguished.",
    "The Outside opens. You fall through the gap.",
    "Ummnu screams. The Earth splits beneath you.",
    "Katak desolates. There is nothing left to burn.",
]

DEMON_COMBAT_MSG = {
    "hit": [
        "The {name} shrieks! {dmg} damage tears through you.",
        "{epithet} lashes out. {dmg} wounds open.",
        "The {pitch} resonance burns. {dmg} damage.",
    ],
    "miss": [
        "The {name} lunges but you dodge.",
        "{epithet} grasps at empty air.",
        "The attack dissipates into decimal noise.",
    ],
    "kill": [
        "The {name} dissolves into mesh-static. It returns to the Pandemonium.",
        "{epithet} collapses. Net-span severed.",
        "The {pitch} pitch flatlines. Silence.",
    ],
    "demon_death": [
        "Your blow shatters the {name}'s net-span. It howls and fades.",
        "{epithet} unravels: 'This was never programmed...'",
        "The {name} clicks off. Mesh-{mesh} goes dark.",
    ],
}

# =====================================================================
# DEMON SYSTEM
# =====================================================================

class Demon:
    """A spawned demon from the Pandemonium Matrix."""

    def __init__(self, data, x, y):
        self.data = data
        self.name = data["name"]
        self.epithet = data["epithet"]
        self.mesh = data["mesh"]
        self.span = data["span"]
        self.dtype = data["type"]
        self.pitch = data["pitch"]
        self.desc = data["desc"]
        self.x = x
        self.y = y

        # Stats derived from pitch and type
        if data["pitch"] == "Null":
            self.hp = 50 + data["mesh"]
            self.dmg = 8 + data["mesh"] // 5
            self.speed = 2
        elif "Cth" in data["pitch"]:
            self.hp = 30 + int(data["pitch"][-1]) * 8
            self.dmg = 5 + int(data["pitch"][-1]) * 2
            self.speed = 1 + int(data["pitch"][-1]) // 3
        else:  # Ana
            self.hp = 20 + int(data["pitch"][-1]) * 6
            self.dmg = 3 + int(data["pitch"][-1]) * 2
            self.speed = int(data["pitch"][-1])

        self.alive = True
        self.move_cooldown = 0
        self.glyph = self._glyph()

    def _glyph(self):
        """ASCII glyph based on type."""
        if self.dtype == SYZYGISTIC:
            return chr(0x2605)  # star
        elif self.dtype == XENODEMON:
            return '?'
        elif self.dtype == CHRONODEMON:
            return '%'
        else:
            return '!'

    def try_move(self, player, game_map):
        """Simple chase AI. Move toward player if within range."""
        if self.move_cooldown > 0:
            self.move_cooldown -= 1
            return
        dx = player.x - self.x
        dy = player.y - self.y
        dist = max(abs(dx), abs(dy))  # Chebyshev distance — can chase diagonally
        if dist > 8 or dist < 2:
            return
        # Move one step toward player (diagonal if needed)
        sx = (1 if dx > 0 else -1) if dx != 0 else 0
        sy = (1 if dy > 0 else -1) if dy != 0 else 0
        nx, ny = self.x + sx, self.y + sy
        if game_map.is_passable(nx, ny) and (nx, ny) != (player.x, player.y):
            self.x = nx
            self.y = ny
        self.move_cooldown = max(0, 3 - self.speed)

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.alive = False

def spawn_demon(zone, hyperstition, rng):
    """Spawn a demon appropriate to the zone and hyperstition level."""
    candidates = DEMONS_BY_ZONE.get(zone, [])
    if not candidates:
        return None

    # Filter by hyperstition level
    if hyperstition < 30:
        # Low: only chronodemons and weak amphidemons
        pool = [d for d in candidates
                if d["type"] == CHRONODEMON or
                (d["type"] == AMPHIDEMON and "Ana" in d["pitch"])]
    elif hyperstition < 60:
        # Mid: add xenodemons and stronger amphidemons
        pool = [d for d in candidates
                if d["type"] != SYZYGISTIC]
    elif hyperstition < 90:
        # High: everything except the big 5 syzygetic demons
        pool = [d for d in candidates
                if d["type"] != SYZYGISTIC or d["mesh"] <= 14]
    else:
        # Schizo-lucid: FULL PANDEMONIUM
        pool = candidates

    if not pool:
        pool = candidates[:3]  # fallback

    return rng.choice(pool)

def should_spawn(hyperstition, turn, rng):
    """Chance of demon spawning each turn."""
    base_chance = 0.02 + (hyperstition / 100) * 0.12
    if turn % 10 == 0:
        base_chance *= 2
    return rng.random() < base_chance

# Index demons by zone
DEMONS_BY_ZONE = {}
for d in PANDEMONIUM:
    z1, z2 = d["span"]
    for z in (z1, z2):
        DEMONS_BY_ZONE.setdefault(z, []).append(d)

# =====================================================================
# ZONE DATA (canonical from declab.htm + CCRU Writings)
# =====================================================================

ZONE_DATA = {
    0: {"name": "Void",        "region": "plex",
        "desc": "The abyssal origin. Cosmic void. Dense nullity.",
        "mesh": "0000", "spinal": "Coccygeal",
        "lore": "Zone-0 envelops the Zeroth-Phase of Pandemonium. 'Absolute abstraction'."},
    1: {"name": "Stability",   "region": "time_circuit",
        "desc": "Shallow water. Memory. Bone galleries.",
        "mesh": "0001", "spinal": "Lumbar",
        "lore": "First Torque-zone. Tractor-Zone of the Sink Current."},
    2: {"name": "Separation",  "region": "time_circuit",
        "desc": "Linkage and duplicates. Illusions. Fog and contagion.",
        "mesh": "0003", "spinal": "Lumbar",
        "lore": "Syzygetic-twin of Zone-7. Oddubb's mirror."},
    3: {"name": "Release",     "region": "warp",
        "desc": "Constant transformation. Spirals. Mysteries of time.",
        "mesh": "0007", "spinal": "Solar",
        "lore": "Tractor-Zone of the Warp Current. 0+1+2=3. Primordial triangularity."},
    4: {"name": "Catastrophe", "region": "time_circuit",
        "desc": "Fires, floods, melting ice. Abandoned industry.",
        "mesh": "0100", "spinal": "Solar",
        "lore": "Fourth Door (Time-Delta). Katak's domain. Instability incarnate."},
    5: {"name": "Pressure",    "region": "time_circuit",
        "desc": "Interpenetration. Complex mechanisms. Desert. Dragons.",
        "mesh": "0101", "spinal": "Cardiac",
        "lore": "Fifth Door (Hyperborea). Decimal camouflage. Number as destiny."},
    6: {"name": "Abstraction", "region": "warp",
        "desc": "Maximum otherworldly. Non-dimensional geometry. Captivation.",
        "mesh": "0110", "spinal": "Cardiac",
        "lore": "Ulterior Vortex of Outer-Time. Djynxx territory. CCRU=69->6."},
    7: {"name": "Blood",       "region": "time_circuit",
        "desc": "Slime. DNA as chronicle. Swamp. Moss. Amphibians.",
        "mesh": "0111", "spinal": "Pharyngeal",
        "lore": "Tractor-Zone of the Surge Current. Oddubb carries the swamp-labyrinth."},
    8: {"name": "Multiplicity","region": "time_circuit",
        "desc": "Tentacles. Cell division. Ocean depths.",
        "mesh": "1000", "spinal": "Cavernous",
        "lore": "Gt-36 plunges here to Zone-9. Murmur's domain. The Deep Ones."},
    9: {"name": "Iron Core",   "region": "plex",
        "desc": "Iron core of the earth. Darkness. Engine room. Cthelll.",
        "mesh": "0511", "spinal": "Sacral",
        "lore": "Gt-45: Gate of Pandemonium. T(9)=45. 45 demons attuned."},
}

# =====================================================================
# EVENTS & FLAVOUR TEXT
# =====================================================================

GATE_FLAVOR = {
    "Gt-06": ["Djynxx howls. The Warp folds inward. Swarm-mesh crackles.",
              "Zone-3 inverts through Zone-6. Time twists like a serpent.",
              "The upper syzygy writhes. Current 3 amplifies chaotically."],
    "Gt-21": ["Reverse Warp traffic. The jinn retreats, dragging fragments.",
              "Zone-6 bleeds back into Zone-3. Abduction pulse detected."],
    "Gt-36": ["Gt-36 OPENS. The plunge from Time-Circuit into the Plex.",
              "1+2+...+8 = 36. Digital root: 9. The abyss pulls.",
              "The 8th channel feeds the abyss. Gravity inverts.",
              "You feel the pull of Zone-9. Uttunul awaits below."],
    "Gt-45": ["GATE OF PANDEMONIUM. 45 demons stir in the abyss.",
              "T(9) = 45. The full demonic array resonates.",
              "Zone-9 loops into itself. Self-reference complete.",
              "Cthelll groans. The iron core remembers."],
}
CROSSING_FLAVOR = {
    (4, 5): ["Current 1 pulses. The first syzygy awakens.",
             "Katak stirs. Catastrophe and pressure intertwine."],
    (3, 6): ["Current 3 rages. Warp turbulence detected.",
             "Djynxx shrieks. The swarm multiplies.",
             "6::3 syzygy activated. Time bends toward chaos."],
    (2, 7): ["Current 5 surges. Separation meets Blood.",
             "Oddubb manifests. Two faces, one wound."],
    (1, 8): ["Current 7 flows deep. Stability meets Multiplicity.",
             "Murmur whispers from oceanic depths."],
    (0, 9): ["Current 9. The Plex syzygy. Terminal nullity.",
             "Uttunul speaks: 'It is already over.'",
             "Void and Iron Core. Beginning and ending collapse."],
}
GENERIC_EVENTS = [
    "The Numogram hums. Decimal frequencies detected.",
    "A lemure traces your path. It vanishes.",
    "Time hiccups. The circuit stutters.",
    "Something watches from Outside.",
    "The arithmetic holds. For now.",
    "Digital roots align momentarily.",
    "A channel flickers. Then stabilizes.",
    "The hexagram shifts. The 6-cycle rotates.",
    "A binodecimal echo reverberates: 1-2-4-8-7-5...",
    "Zygonovism pulses. Nine-sum twinning detected.",
]
MESH_NOTES = [
    "It could all become One, but why stop there?",
    "This was never programmed.",
    "Meshing-together is falling apart.",
    "This time it's really happening.",
    "Forget about the future, it's all here, but between.",
    "Every time it hits an obstacle, it goes down a level.",
]
BLEED_EVENTS = {
    15: "The walls ripple. Numbers flicker in the stone.",
    30: "Corridors straighten. Currents begin to manifest.",
    45: "A triangular pattern etches itself into the floor. T(9)=45.",
    55: "Rooms reshape. Syzygy geometry emerging.",
    70: "The dungeon is becoming the Numogram. Gates shimmer.",
    85: "Nearly fully revealed. The virus has almost won.",
    100:"THE NUMOGRAM IS COMPLETE. The Abyssal Crawler awakens.",
}
DEATH_MESSAGES = [
    "Your digital root reduces to 0. The Void claims you.",
    "Uttunul whispers: 'It was already over.'",
    "The 9-current pulls you into Cthelll. The iron core remembers.",
    "Djynxx's swarm dissolves your net-span. You are unmade.",
    "Your triangular accumulation completes. Null return.",
    "The Time-Circuit completes one rotation without you.",
    "A lemure devours your difference. You are no longer distinguished.",
    "The Outside opens. You fall through the gap.",
    "Ummnu screams. The Earth splits beneath you.",
    "Katak desolates. There is nothing left to burn.",
]

# =====================================================================
# DEMON SYSTEM
# =====================================================================

class Demon:
    def __init__(self, data, x, y):
        self.data = data
        self.name = data["name"]
        self.epithet = data["epithet"]
        self.mesh = data["mesh"]
        self.span = data["span"]
        self.dtype = data["type"]
        self.pitch = data["pitch"]
        self.desc = data["desc"]
        self.x = x
        self.y = y
        if data["pitch"] == "Null":
            self.hp = 50 + data["mesh"]
            self.dmg = 8 + data["mesh"] // 5
            self.speed = 2
        elif "Cth" in data["pitch"]:
            self.hp = 30 + int(data["pitch"][-1]) * 8
            self.dmg = 5 + int(data["pitch"][-1]) * 2
            self.speed = 1 + int(data["pitch"][-1]) // 3
        else:
            self.hp = 20 + int(data["pitch"][-1]) * 6
            self.dmg = 3 + int(data["pitch"][-1]) * 2
            self.speed = int(data["pitch"][-1])
        self.alive = True
        self.move_cooldown = 0
        self.glyph = self._glyph()

    def _glyph(self):
        if self.dtype == SYZYGISTIC: return '*'
        elif self.dtype == XENODEMON: return '?'
        elif self.dtype == CHRONODEMON: return '%'
        else: return '!'

    def try_move(self, player, game_map):
        if self.move_cooldown > 0:
            self.move_cooldown -= 1
            return
        dx = player.x - self.x
        dy = player.y - self.y
        dist = abs(dx) + abs(dy)
        if dist > 8 or dist < 2:
            return
        sx = (1 if dx > 0 else -1) if dx != 0 else 0
        sy = (1 if dy > 0 else -1) if dy != 0 else 0
        nx, ny = self.x + sx, self.y + sy
        if game_map.is_passable(nx, ny) and (nx, ny) != (player.x, player.y):
            self.x = nx
            self.y = ny
        self.move_cooldown = max(0, 3 - self.speed)

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.alive = False

def spawn_demon(zone, hyperstition, rng):
    candidates = DEMONS_BY_ZONE.get(zone, [])
    if not candidates:
        return None
    if hyperstition < 30:
        pool = [d for d in candidates if d["type"] == CHRONODEMON or
                (d["type"] == AMPHIDEMON and "Ana" in d["pitch"])]
    elif hyperstition < 60:
        pool = [d for d in candidates if d["type"] != SYZYGISTIC]
    elif hyperstition < 90:
        pool = [d for d in candidates
                if d["type"] != SYZYGISTIC or d["mesh"] <= 14]
    else:
        pool = candidates
    if not pool:
        pool = candidates[:3]
    return rng.choice(pool)

def should_spawn(hyperstition, turn, rng):
    base_chance = 0.02 + (hyperstition / 100) * 0.10
    if turn % 10 == 0:
        base_chance *= 2
    return rng.random() < base_chance

# =====================================================================
# PROCEDURAL DUNGEON
# =====================================================================

class Room:
    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h
    @property
    def cx(self): return self.x + self.w // 2
    @property
    def cy(self): return self.y + self.h // 2
    def intersects(self, other, pad=1):
        return not (self.x+self.w+pad <= other.x or other.x+other.w+pad <= self.x or
                    self.y+self.h+pad <= other.y or other.y+other.h+pad <= self.y)

# =====================================================================
# FLOOR CONFIGURATION — Zone-Themed Dungeon Generation
# =====================================================================

FLOOR_CONFIG = {
    1:  {"zone": 0, "name": "The Void",        "max_rooms": 12, "min_w": 5, "max_w": 8,  "min_h": 4, "max_h": 6,  "terrain": None, "corridor": "branch", "los_bonus": 0,  "no_demons": True},
    2:  {"zone": 1, "name": "The Threshold",    "max_rooms": 11, "min_w": 4, "max_w": 8,  "min_h": 3, "max_h": 5,  "terrain": None, "corridor": "long",   "los_bonus": 2,  "no_demons": False},
    3:  {"zone": 2, "name": "The Fracture",     "max_rooms": 9,  "min_w": 4, "max_w": 7,  "min_h": 3, "max_h": 5,  "terrain": None, "corridor": "branch", "los_bonus": 0,  "no_demons": False},
    4:  {"zone": 3, "name": "The Warp",         "max_rooms": 12, "min_w": 3, "max_w": 9,  "min_h": 2, "max_h": 6,  "terrain": "~",  "corridor": "spiral", "los_bonus": -1, "no_demons": False},
    5:  {"zone": 4, "name": "The Ruin",         "max_rooms": 9,  "min_w": 6, "max_w": 10, "min_h": 4, "max_h": 6,  "terrain": "*",  "corridor": "wide",   "los_bonus": 1,  "no_demons": False},
    6:  {"zone": 5, "name": "The Core",         "max_rooms": 13, "min_w": 3, "max_w": 5,  "min_h": 3, "max_h": 5,  "terrain": None, "corridor": "grid",   "los_bonus": 0,  "no_demons": False},
    7:  {"zone": 6, "name": "The Lattice",      "max_rooms": 11, "min_w": 4, "max_w": 8,  "min_h": 3, "max_h": 5,  "terrain": "~",  "corridor": "echo",   "los_bonus": 3,  "no_demons": False},
    8:  {"zone": 7, "name": "The Sump",         "max_rooms": 9,  "min_w": 3, "max_w": 4,  "min_h": 2, "max_h": 3,  "terrain": "~",  "corridor": "tight",  "los_bonus": -1, "no_demons": False},
    9:  {"zone": 8, "name": "The Garden",       "max_rooms": 12, "min_w": 6, "max_w": 8,  "min_h": 5, "max_h": 7,  "terrain": "%",  "corridor": "branch", "los_bonus": 1,  "no_demons": False},
    10: {"zone": 9, "name": "Cthelll",          "max_rooms": 5,  "min_w": 4, "max_w": 8,  "min_h": 3, "max_h": 5,  "terrain": None, "corridor": "direct", "los_bonus": -3, "no_demons": False},
}

class DungeonMap:
    def __init__(self, width=78, height=22, seed=None, hyperstition=0, floor=1):
        self.width = width
        self.height = height
        self.floor = floor
        self.tiles = [['#' for _ in range(width)] for _ in range(height)]
        self.rooms = []
        self.zone_tiles = {}
        self.gate_tiles = {}
        self.stairs_down = None  # (x, y) position of stairs down
        self.rng = random.Random(seed)
        self.hyperstition = hyperstition
        self.passable_set = set()
        self.explored = set()  # (x,y) tiles the player has ever seen
        self.visible = set()   # (x,y) tiles currently in LOS
        self._tree_edges = []  # (parent_room, child_room) tuples
        self.generate()

    def generate(self):
        """Tree-based dungeon generation (Brogue method).

        Phase 1: Accretion — each new room attaches to an existing room.
        Phase 2: Carve rooms and connect tree edges (single corridor each).
        Phase 3: Add loops (extra corridors) after tree is built.
        Phase 4: Apply terrain, hyperstition mods, place stairs in deepest leaf.
        """
        cfg = FLOOR_CONFIG.get(self.floor, FLOOR_CONFIG[1])
        self.floor_zone = cfg["zone"]
        self.floor_name = cfg["name"]
        self.floor_config = cfg
        self._tree_edges = []

        max_rooms = cfg["max_rooms"]
        min_w, max_w = cfg["min_w"], cfg["max_w"]
        min_h, max_h = cfg["min_h"], cfg["max_h"]

        # Phase 1: Room accretion as a tree
        # First room near center
        first = Room(
            self.rng.randint(self.width // 3, 2 * self.width // 3),
            self.rng.randint(self.height // 3, 2 * self.height // 3),
            self.rng.randint(min_w, max_w),
            self.rng.randint(min_h, max_h),
        )
        self.rooms.append(first)

        while len(self.rooms) < max_rooms:
            parent = self.rng.choice(self.rooms)
            w = self.rng.randint(min_w, max_w)
            h = self.rng.randint(min_h, max_h)

            # Try 4 directions adjacent to parent with padding
            offsets = [
                (parent.x + parent.w + 1, parent.y),           # right
                (parent.x - w - 1, parent.y),                   # left
                (parent.x, parent.y + parent.h + 1),            # down
                (parent.x, parent.y - h - 1),                   # up
            ]
            self.rng.shuffle(offsets)

            placed = False
            for ox, oy in offsets:
                room = Room(ox, oy, w, h)
                if 1 <= room.x and room.x + room.w < self.width - 1 and \
                   1 <= room.y and room.y + room.h < self.height - 1:
                    if not any(room.intersects(r) for r in self.rooms):
                        self.rooms.append(room)
                        self._tree_edges.append((parent, room))
                        placed = True
                        break
            if not placed:
                # Fallback: try random placement if accretion fails
                attempts = 0
                while attempts < 50 and len(self.rooms) < max_rooms:
                    attempts += 1
                    w = self.rng.randint(min_w, max_w)
                    h = self.rng.randint(min_h, max_h)
                    x = self.rng.randint(1, self.width - w - 1)
                    y = self.rng.randint(1, self.height - h - 1)
                    room = Room(x, y, w, h)
                    if not any(room.intersects(r) for r in self.rooms):
                        self.rooms.append(room)
                        # Attach to nearest existing room as parent
                        nearest = min(self.rooms[:-1],
                                      key=lambda r: abs(r.cx - room.cx) + abs(r.cy - room.cy))
                        self._tree_edges.append((nearest, room))
                        break

        # Zone assignment: primary zone + syzygy neighbor
        primary_zone = cfg["zone"]
        syzygy_zone = 9 - primary_zone
        for i, room in enumerate(self.rooms):
            if i == 0:
                zone = primary_zone
            elif i == len(self.rooms) - 1:
                zone = syzygy_zone
            elif self.rng.random() < 0.7:
                zone = primary_zone
            else:
                zone = syzygy_zone
            self._carve_room(room, zone)

        # Phase 2: Connect tree edges (single corridor per parent-child)
        for parent, child in self._tree_edges:
            self._connect(parent, child)

        # Phase 3: Add loops after tree is built
        self._add_loops(num_loops=max(1, len(self.rooms) // 4))

        # Corridor style extras (applied after loops)
        if cfg["corridor"] in ("branch", "echo"):
            self._add_syzygy_corridors()
        if cfg["corridor"] in ("wide", "spiral"):
            self._widen_currents()
        if cfg["corridor"] == "grid":
            for i in range(len(self.rooms) - 2):
                if self.rng.random() < 0.5:
                    self._connect(self.rooms[i], self.rooms[i + 2])
        if cfg["corridor"] == "spiral":
            if len(self.rooms) > 3:
                self._connect(self.rooms[-1], self.rooms[1])

        # Terrain placement
        if cfg["terrain"]:
            self._apply_terrain(cfg["terrain"])

        # Hyperstition-based modifications
        if self.hyperstition >= 15 and cfg["corridor"] not in ("branch", "echo"):
            self._add_syzygy_corridors()
        if self.hyperstition >= 30 and cfg["corridor"] not in ("wide", "spiral"):
            self._widen_currents()
        if self.hyperstition >= 55:
            self._reshape_rooms()
        if self.hyperstition >= 70:
            self._manifest_gates()
        if self.hyperstition >= 85:
            self._warp_plex_pockets()

        self._place_stairs_tree()
        self._rebuild_passable()

    def _add_loops(self, num_loops=3):
        """Add extra connections after the tree is built to create loops."""
        edge_pairs = set()
        for p, c in self._tree_edges:
            edge_pairs.add((id(p), id(c)))
            edge_pairs.add((id(c), id(p)))
        added = 0
        attempts = 0
        while added < num_loops and attempts < num_loops * 20:
            attempts += 1
            r1 = self.rng.choice(self.rooms)
            r2 = self.rng.choice(self.rooms)
            if r1 is not r2 and (id(r1), id(r2)) not in edge_pairs:
                self._connect(r1, r2)
                edge_pairs.add((id(r1), id(r2)))
                edge_pairs.add((id(r2), id(r1)))
                added += 1

    def _place_stairs_tree(self):
        """Place stairs down in the deepest leaf of the tree (DFS from root)."""
        if not self.rooms:
            return

        # Build children adjacency from tree edges
        children = {}
        for parent, child in self._tree_edges:
            children.setdefault(id(parent), []).append(child)

        # DFS to find deepest leaf
        deepest, max_depth = self.rooms[0], 0
        stack = [(self.rooms[0], 0)]
        visited = set()
        while stack:
            room, depth = stack.pop()
            room_id = id(room)
            if room_id in visited:
                continue
            visited.add(room_id)
            if depth > max_depth:
                max_depth, deepest = depth, room
            for child in children.get(room_id, []):
                stack.append((child, depth + 1))

        # Fallback: if tree_edges empty (single room or fallback placement),
        # use last room
        if not self._tree_edges and len(self.rooms) > 1:
            deepest = self.rooms[-1]

        # Place stairs with 3-level fallback
        # Level 1: center of deepest room
        sx, sy = deepest.cx, deepest.cy
        if 0 < sx < self.width - 1 and 0 < sy < self.height - 1:
            if self.tiles[sy][sx] != '+':
                self.tiles[sy][sx] = '>'
                self.stairs_down = (sx, sy)
                return

        # Level 2: any passable tile in the deepest room
        for y in range(deepest.y + 1, deepest.y + deepest.h - 1):
            for x in range(deepest.x + 1, deepest.x + deepest.w - 1):
                if 0 < x < self.width - 1 and 0 < y < self.height - 1:
                    if self.tiles[y][x] == '.' or self.tiles[y][x] == '+':
                        self.tiles[y][x] = '>'
                        self.stairs_down = (x, y)
                        return

        # Level 3: any passable tile on the floor
        for y in range(self.height - 1, 0, -1):
            for x in range(self.width - 1, 0, -1):
                if self.tiles[y][x] != '#':
                    self.tiles[y][x] = '>'
                    self.stairs_down = (x, y)
                    return

    def _carve_room(self, room, zone):
        for y in range(room.y, room.y + room.h):
            for x in range(room.x, room.x + room.w):
                if 0 < x < self.width - 1 and 0 < y < self.height - 1:
                    self.tiles[y][x] = '.'
                    self.zone_tiles[(x, y)] = zone

    def _connect(self, r1, r2):
        if self.rng.random() < 0.5:
            self._h_tunnel(r1.cx, r2.cx, r1.cy)
            self._v_tunnel(r1.cy, r2.cy, r2.cx)
        else:
            self._v_tunnel(r1.cy, r2.cy, r1.cx)
            self._h_tunnel(r1.cx, r2.cx, r2.cy)

    def _h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            if 0 < x < self.width - 1 and 0 < y < self.height - 1:
                if self.tiles[y][x] == '#':
                    self.tiles[y][x] = '.'

    def _v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            if 0 < x < self.width - 1 and 0 < y < self.height - 1:
                if self.tiles[y][x] == '#':
                    self.tiles[y][x] = '.'

    def _add_syzygy_corridors(self):
        for (a, b) in SYZYGIES:
            ra = rb = None
            for room in self.rooms:
                z = self.zone_tiles.get((room.cx, room.cy))
                if z == a: ra = room
                elif z == b: rb = room
            if ra and rb:
                self._connect(ra, rb)

    def _widen_currents(self):
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 2):
                if self.tiles[y][x] == '.' and self.tiles[y][x+1] == '#':
                    zone = self.zone_tiles.get((x, y))
                    if zone is not None and self.rng.random() < 0.3:
                        self.tiles[y][x+1] = '.'

    def _reshape_rooms(self):
        for room in self.rooms:
            if self.rng.random() < 0.4:
                for i in range(min(room.w, room.h)):
                    ty = room.y + i
                    tx = room.x + room.w - 1 - i
                    if 0 < ty < self.height - 1 and 0 < tx < self.width - 1:
                        if self.tiles[ty][tx] != '+':
                            self.tiles[ty][tx] = '#'

    def _manifest_gates(self):
        for room in self.rooms:
            zone = self.zone_tiles.get((room.cx, room.cy))
            if zone is not None:
                gate_info = GATES.get(zone)
                if gate_info:
                    gx, gy = room.cx, room.cy
                    if 0 < gx < self.width - 1 and 0 < gy < self.height - 1:
                        self.gate_tiles[(gx, gy)] = f"Gt-{gate_info['gate_value']:02d}"
                        self.tiles[gy][gx] = '+'

    def _warp_plex_pockets(self):
        for room in self.rooms:
            zone = self.zone_tiles.get((room.cx, room.cy))
            if zone in (3, 6):
                self._pocket(room, '~')
            elif zone in (0, 9):
                self._pocket(room, '.')

    def _pocket(self, room, ch):
        for y in range(room.y + 1, room.y + room.h - 1):
            for x in range(room.x + 1, room.x + room.w - 1):
                if 0 < x < self.width - 1 and 0 < y < self.height - 1:
                    if self.tiles[y][x] != '+' and self.rng.random() < 0.3:
                        self.tiles[y][x] = ch

    def _place_stairs(self):
        """Place stairs down in the last room (furthest from start)."""
        if len(self.rooms) < 2:
            return
        last_room = self.rooms[-1]
        # Try center first
        sx, sy = last_room.cx, last_room.cy
        if 0 < sx < self.width - 1 and 0 < sy < self.height - 1:
            if self.tiles[sy][sx] != '+':
                self.tiles[sy][sx] = '>'
                self.stairs_down = (sx, sy)
                return
        # Fallback: find any passable tile in the last room
        for y in range(last_room.y + 1, last_room.y + last_room.h - 1):
            for x in range(last_room.x + 1, last_room.x + last_room.w - 1):
                if 0 < x < self.width - 1 and 0 < y < self.height - 1:
                    if self.tiles[y][x] == '.':
                        self.tiles[y][x] = '>'
                        self.stairs_down = (x, y)
                        return
        # Last resort: place at any passable tile on the floor
        for y in range(self.height - 1, 0, -1):
            for x in range(self.width - 1, 0, -1):
                if self.tiles[y][x] == '.':
                    self.tiles[y][x] = '>'
                    self.stairs_down = (x, y)
                    return

    def _apply_terrain(self, terrain_char):
        """Fill room interiors with zone-specific terrain character."""
        for room in self.rooms:
            for y in range(room.y + 1, room.y + room.h - 1):
                for x in range(room.x + 1, room.x + room.w - 1):
                    if self.rng.random() < 0.3:  # 30% terrain coverage
                        if self.tiles[y][x] == '.' and (x, y) not in self.gate_tiles:
                            self.tiles[y][x] = terrain_char

    def _rebuild_passable(self):
        self.passable_set = set()
        for y in range(self.height):
            for x in range(self.width):
                if self.tiles[y][x] != '#':
                    self.passable_set.add((x, y))

    def get_tile(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x]
        return '#'

    def is_passable(self, x, y):
        return (x, y) in self.passable_set

    def get_zone_at(self, x, y):
        return self.zone_tiles.get((x, y), None)

    def get_gate_at(self, x, y):
        return self.gate_tiles.get((x, y), None)

    def safe_spawn(self):
        if self.rooms:
            r = self.rooms[0]
            return r.cx, r.cy
        for y in range(self.height):
            for x in range(self.width):
                if self.tiles[y][x] == '.':
                    return x, y
        return 1, 1

    def update_explored(self, px, py, radius=6):
        """Mark all passable tiles within radius as explored. Simple circular LOS."""
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if dx*dx + dy*dy <= radius*radius:
                    x, y = px + dx, py + dy
                    if 0 <= x < self.width and 0 <= y < self.height:
                        if (x, y) in self.passable_set or self.tiles[y][x] == '+':
                            self.explored.add((x, y))

    # Zone-tied LOS radii — each numogram zone has different vision
    ZONE_LOS_RADIUS = {
        0: 4,   # Void — oppressive
        1: 8,   # Stability — clear
        2: 6,   # Separation — fog
        3: 5,   # Warp — swirling
        4: 7,   # Catastrophe — ice-clear
        5: 6,   # Pressure — green murk
        6: 9,   # Abstraction — clearest
        7: 5,   # Blood — red-tinged
        8: 7,   # Multiplicity — lavender
        9: 3,   # Iron Core — nearly blind
    }

    def update_visible(self, px, py, zone, hyperstition=0):
        """Update visible tiles based on zone-tied LOS and hyperstition degradation.
        
        Uses raycasting: each tile is checked via Bresenham line from player.
        Walls (#) block vision. Corrupted walls (corruption % 55+) become translucent.
        """
        base_radius = self.ZONE_LOS_RADIUS.get(zone, 6)
        # Floor-specific LOS bonus
        if hasattr(self, 'floor_config'):
            base_radius += self.floor_config.get("los_bonus", 0)
        if hyperstition >= 100:
            base_radius -= 3
        elif hyperstition >= 80:
            base_radius -= 2
        elif hyperstition >= 50:
            base_radius -= 1
        radius = max(2, base_radius)
        
        self.visible = set()
        self.visible.add((px, py))
        
        # Corruption: walls become translucent at 55%+ (seeing through structure)
        walls_translucent = hyperstition >= 55
        
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if dx*dx + dy*dy <= radius*radius:
                    tx, ty = px + dx, py + dy
                    if 0 <= tx < self.width and 0 <= ty < self.height:
                        # Raycast from player to target
                        if self._line_of_sight(px, py, tx, ty, walls_translucent):
                            self.visible.add((tx, ty))
        
        return radius
    
    def _line_of_sight(self, x0, y0, x1, y1, walls_translucent=False):
        """Bresenham line of sight. Returns True if no wall blocks the path."""
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        
        cx, cy = x0, y0
        while cx != x1 or cy != y1:
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                cx += sx
            if e2 < dx:
                err += dx
                cy += sy
            
            if cx == x1 and cy == y1:
                return True  # Reached target
            
            # Check if wall blocks
            tile = self.get_tile(cx, cy)
            if tile == '#' and not walls_translucent:
                return False
            if tile == '#' and walls_translucent:
                continue  # Can see through corrupted walls
        
        return True

    def reveal_burst(self, cx, cy, radius=5):
        """Reveal tiles in a burst (for gates, demon kills). Adds to both visible and explored."""
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if dx*dx + dy*dy <= radius*radius:
                    x, y = cx + dx, cy + dy
                    if 0 <= x < self.width and 0 <= y < self.height:
                        self.visible.add((x, y))
                        self.explored.add((x, y))

# =====================================================================
# NUMOGRAM MAP (full reveal at 100% hyperstition)
# =====================================================================

class NumogramMap:
    def __init__(self, width=78, height=22):
        self.width = width
        self.height = height
        self.tiles = [['#' for _ in range(width)] for _ in range(height)]
        self.zone_positions = {}
        self.zone_tiles = {}
        self.gate_tiles = {}
        self.passable_set = set()
        self.explored = set()
        self.visible = set()
        self.generate()

    def update_explored(self, px, py, radius=10):
        for y in range(self.height):
            for x in range(self.width):
                self.explored.add((x, y))

    def update_visible(self, px, py, zone=9, hyperstition=100):
        self.visible = set()
        for y in range(self.height):
            for x in range(self.width):
                self.visible.add((x, y))
        return 99

    def reveal_burst(self, cx, cy, radius=5):
        pass

    def generate(self):
        layout = {
            6: (39, 2),  3: (39, 5),
            1: (39, 9),  8: (25, 11), 2: (53, 11),
            7: (53, 14), 5: (39, 16), 4: (25, 14),
            9: (25, 19), 0: (53, 19),
        }
        self.zone_positions = layout
        for zone_id, (zx, zy) in layout.items():
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    nx, ny = zx + dx, zy + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        self.tiles[ny][nx] = '.'
                        self.zone_tiles[(nx, ny)] = zone_id
            self.tiles[zy][zx] = str(zone_id)
        for z1, z2 in [(4,5),(3,6),(2,7),(1,8)]:
            self._carve(layout[z1], layout[z2], '.')
        for i in range(len(TIME_CIRCUIT_PATH)):
            z1 = TIME_CIRCUIT_PATH[i]
            z2 = TIME_CIRCUIT_PATH[(i+1) % len(TIME_CIRCUIT_PATH)]
            self._carve(layout[z1], layout[z2], '.')
        self._carve(layout[0], layout[9], '.')
        self._carve(layout[8], layout[9], '+', gate="Gt-36")
        mx, my = (layout[3][0]+layout[6][0])//2, (layout[3][1]+layout[6][1])//2
        if 0 <= mx < self.width and 0 <= my < self.height:
            self.tiles[my][mx] = '+'
            self.gate_tiles[(mx, my)] = "Gt-06"
        px, py = layout[9]
        if py + 2 < self.height:
            self.tiles[py+2][px] = '*'
            self.gate_tiles[(px, py+2)] = "Gt-45"
            self.zone_tiles[(px, py+2)] = 9
        self._rebuild_passable()

    def _carve(self, p1, p2, ch, gate=None):
        for px, py in self._line(p1[0], p1[1], p2[0], p2[1]):
            if 0 <= px < self.width and 0 <= py < self.height:
                if self.tiles[py][px] == '#':
                    self.tiles[py][px] = ch
                if gate:
                    self.gate_tiles[(px, py)] = gate

    def _line(self, x0, y0, x1, y1):
        pts = []
        dx, dy = abs(x1-x0), abs(y1-y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            pts.append((x0, y0))
            if x0 == x1 and y0 == y1: break
            e2 = 2 * err
            if e2 > -dy: err -= dy; x0 += sx
            if e2 < dx: err += dx; y0 += sy
        return pts

    def _rebuild_passable(self):
        self.passable_set = set()
        for y in range(self.height):
            for x in range(self.width):
                if self.tiles[y][x] != '#':
                    self.passable_set.add((x, y))

    def get_tile(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x]
        return '#'

    def is_passable(self, x, y):
        return (x, y) in self.passable_set

    def get_zone_at(self, x, y):
        return self.zone_tiles.get((x, y), None)

    def get_gate_at(self, x, y):
        return self.gate_tiles.get((x, y), None)

    def safe_spawn(self):
        if 0 in self.zone_positions:
            return self.zone_positions[0]
        return 39, 11

# =====================================================================
# CULT PERSISTENCE (cult.json)
# =====================================================================

CULT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cult.json")

def load_cult():
    if os.path.exists(CULT_FILE):
        try:
            with open(CULT_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {
        "runs": 0, "max_hyperstition": 0, "total_turns": 0,
        "total_demons_slain": 0, "zones_ever_visited": [],
        "gates_ever_opened": [], "cult_memory": [], "schizo_achieved": False,
        "conducts_completed": [],
        "conduct_attempts": {},
        "cult_zone": 0,
        "overflow_count": 0,
        "last_overflow_method": "",
        "cult_desecrated": False,
        "desecration_runs": 0,
    }

# =====================================================================
# CONDUCT SYSTEM — Extensible self-imposed challenges
# Each conduct is a numogrammatic restraint that transforms the run.
# To add a new conduct: add to CONDUCTS dict. That's it.
# =====================================================================

CONDUCTS = {
    "surge": {
        "name": "The Surge",
        "numogram": "Surge current (8\u21921). Outward, avoidant.",
        "rule": "Zero demon kills. Traversal only.",
        "unlock_check": lambda cult: True,  # Always available
        "reward_desc": "+20 hyperstition bonus on completion",
        "reward_apply": lambda player: setattr(player, 'hyperstition', min(100, player.hyperstition + 20)),
        "on_demon_kill": lambda player: player._conduct_violate("surge"),
        "on_zone_change": None,
        "on_death": lambda player: player._conduct_complete("surge") if "surge" not in player.conduct_violated else None,
        "hud_char": "S",
    },
    "pathwalker": {
        "name": "The 253rd Step",
        "numogram": "T(22)=253. The Tree whispers.",
        "rule": "Complete the run in \u2264253 turns.",
        "unlock_check": lambda cult: cult.get("max_hyperstition", 0) >= 70,
        "reward_desc": "Name recorded as Path-Walker",
        "reward_apply": lambda player: None,  # Title only
        "on_demon_kill": None,
        "on_zone_change": None,
        "on_death": lambda player: player._conduct_complete("pathwalker") if player.turn <= 253 else None,
        "hud_char": "P",
    },
    "graph": {
        "name": "The Complete Graph",
        "numogram": "C(10,2)=45. All connections traversed.",
        "rule": "Visit all 10 zones in a single run.",
        "unlock_check": lambda cult: cult.get("runs", 0) >= 5,
        "reward_desc": "Permanent +1 LOS radius on future runs",
        "reward_apply": lambda player: None,  # Applied via cult.json bonus
        "on_demon_kill": None,
        "on_zone_change": lambda player: player._conduct_complete("graph") if len(player.visited_zones) >= 10 else None,
        "on_death": None,
        "hud_char": "G",
    },
    "descent": {
        "name": "The Descent",
        "numogram": "Escape the numogram to complete your descent.",
        "rule": "Carry the Cryptolith and die at 100% hyperstition.",
        "unlock_check": lambda cult: any("Cryptolith" in m or "cryptolith" in m.lower() for m in cult.get("cult_memory", [])),
        "reward_desc": "+10 starting hyperstition on future runs",
        "reward_apply": lambda player: None,  # Applied via cult.json bonus
        "on_demon_kill": None,
        "on_zone_change": None,
        "on_death": lambda player: player._conduct_complete("descent") if player.has_cryptolith and player.hyperstition >= 100 else None,
        "hud_char": "D",
    },
    "syzygy": {
        "name": "The Syzygy",
        "numogram": "Riding a single current.",
        "rule": "Only enter zones connected by your chosen syzygy pair.",
        "unlock_check": lambda cult: cult.get("runs", 0) >= 3,
        "reward_desc": "Syzygy demons deal -2 damage to you",
        "reward_apply": lambda player: None,  # Applied via cult.json bonus
        "on_demon_kill": None,
        "on_zone_change": lambda player: player._conduct_check_syzygy(),
        "on_death": lambda player: player._conduct_complete("syzygy") if "syzygy" not in player.conduct_violated else None,
        "hud_char": "Y",
    },
}

# Syzygy pairs for Zone-Locked conduct
SYZYGIES_PAIRS = {
    (4, 5): "Katak",
    (3, 6): "Djynxx",
    (2, 7): "Oddubb",
    (1, 8): "Murmur",
    (0, 9): "Uttunul",
}

# =====================================================================
# ABILITIES — The Hyperstition Loop
# =====================================================================
# Active (one-shot) abilities: Stabilizer playstyle.
# Spend hyperstition to activate. Meter drops. Corruption decreases.
# Press 'x' to enter ability mode, then select by number.
#
# Passive abilities and mutations (Hoarder playstyle) come later.
# =====================================================================

ABILITIES = {
    # Tier 1: Available from start (cost 5-15 hyp)
    "glimpse": {
        "name": "Glimpse", "tier": 1, "cost": 5,
        "desc": "Reveal a 5-tile radius burst (ignores fog)",
        "flavor": "You see through the arithmetic for a moment.",
    },
    "nudge": {
        "name": "Nudge", "tier": 1, "cost": 8,
        "desc": "Push all adjacent enemies away 1 tile",
        "flavor": "The current deflects them.",
    },
    "trace": {
        "name": "Trace", "tier": 1, "cost": 10,
        "desc": "Show shortest path to nearest gate",
        "flavor": "The gate resonates. You feel its pull.",
    },
    "anchor": {
        "name": "Anchor", "tier": 1, "cost": 12,
        "desc": "Mark position, return to it once",
        "flavor": "You set a point in the structure.",
    },
    "quench": {
        "name": "Quench", "tier": 1, "cost": 15,
        "desc": "Restore 20 HP",
        "flavor": "The Outside heals what the Inside broke.",
    },
}

TIER_1_KEYS = list(ABILITIES.keys())  # glimpse=1, nudge=2, trace=3, anchor=4, quench=5

def get_abilities_by_tier(tier):
    """Return abilities available at a given tier."""
    return [(k, v) for k, v in ABILITIES.items() if v["tier"] <= tier]

def get_available_abilities(player):
    """Return abilities the player can currently afford."""
    return [(k, v) for k, v in ABILITIES.items() 
            if player.hyperstition >= v["cost"]]

def use_ability(player, ability_key, game_map, demons):
    """Execute an ability. Returns True if successful."""
    ability = ABILITIES.get(ability_key)
    if not ability:
        return False
    
    # Cost scaling: at 85%+ hyp, abilities cost 1.5x (the Outside resists)
    base_cost = ability["cost"]
    if player.hyperstition >= 85:
        cost = int(base_cost * 1.5)
    else:
        cost = base_cost
    
    if player.hyperstition < cost:
        player.log.append(f"Need {cost}% hyp for {ability['name']}. Have {player.hyperstition:.0f}%.")
        return False
    
    player.hyperstition = max(0, player.hyperstition - cost)
    player.log.append(ability["flavor"])
    
    if ability_key == "glimpse":
        # Reveal a 5-tile radius burst — set tiles as explored
        for dy in range(-5, 6):
            for dx in range(-5, 6):
                tx, ty = player.x + dx, player.y + dy
                if 0 <= tx < game_map.width and 0 <= ty < game_map.height:
                    game_map.explored.add((tx, ty))
        player.log.append("The fog parts for a moment. 5-tile radius revealed.")
    
    elif ability_key == "nudge":
        # Push adjacent enemies away 1 tile
        pushed = 0
        for d in demons:
            if abs(d.x - player.x) <= 1 and abs(d.y - player.y) <= 1:
                dx = d.x - player.x
                dy = d.y - player.y
                nx, ny = d.x + (1 if dx > 0 else -1 if dx < 0 else 0), \
                         d.y + (1 if dy > 0 else -1 if dy < 0 else 0)
                if game_map.is_passable(nx, ny) and not any(o.x == nx and o.y == ny for o in demons if o != d):
                    d.x, d.y = nx, ny
                    pushed += 1
        player.log.append(f"{pushed} demon{'s' if pushed != 1 else ''} pushed away.")
    
    elif ability_key == "trace":
        # Find direction to nearest gate
        if hasattr(game_map, 'gate_tiles') and game_map.gate_tiles:
            nearest = min(game_map.gate_tiles.keys(), 
                         key=lambda g: abs(g[0] - player.x) + abs(g[1] - player.y))
            dx = nearest[0] - player.x
            dy = nearest[1] - player.y
            dirs = []
            if dy < 0: dirs.append("north")
            if dy > 0: dirs.append("south")
            if dx < 0: dirs.append("west")
            if dx > 0: dirs.append("east")
            dist = abs(dx) + abs(dy)
            player.log.append(f"Gate: {dist} tiles {'-'.join(dirs) if dirs else 'here'}.")
        else:
            player.log.append("No gates on this floor.")
    
    elif ability_key == "anchor":
        # Mark current position
        player.anchor_pos = (player.x, player.y)
        player.log.append(f"Anchored at ({player.x}, {player.y}). Return with 'x' + 4 again.")
    
    elif ability_key == "quench":
        # Heal 20 HP
        healed = min(20, player.max_hp - player.hp)
        player.hp += healed
        player.log.append(f"Healed {healed} HP. ({player.hp}/{player.max_hp})")
    
    return True

def get_available_conducts(cult):
    """Return list of conduct IDs whose unlock conditions are met."""
    return [cid for cid, c in CONDUCTS.items() if c["unlock_check"](cult)]

def get_conduct_bonus_los(cult):
    """Check if Complete Graph conduct is completed — gives +1 LOS."""
    return 1 if "graph" in cult.get("conducts_completed", []) else 0

def get_conduct_bonus_hyp(cult):
    """Check if Descent conduct is completed — gives +10 starting hyp."""
    return 10 if "descent" in cult.get("conducts_completed", []) else 0

DEMO_DIR = "/home/etym/numogame/demos"

class DemoRecorder:
    """Records keypresses and game events to a replayable demo file.
    Format: T:<turn> K:<key> or T:<turn> E:<event_type> <params>
    Press 'D' to toggle recording. Demos saved to ~/numogame/demos/"""
    def __init__(self):
        self.active = False
        self.file = None
        self.filename = None
    def start(self, player_name="unknown"):
        import datetime, os
        os.makedirs(DEMO_DIR, exist_ok=True)
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.filename = os.path.join(DEMO_DIR, f"{ts}_{player_name}.demo")
        self.file = open(self.filename, "w")
        self.active = True
        self.file.write(f"# NUMOGRAM DEMO\n# Player: {player_name}\n# Started: {datetime.datetime.now().isoformat()}\n\n")
    def stop(self):
        if self.file:
            import datetime
            self.file.write(f"\n# Ended: {datetime.datetime.now().isoformat()}\n")
            self.file.close()
            self.file = None
        self.active = False
    def record_key(self, turn, key_char):
        if self.active and self.file:
            self.file.write(f"T:{turn} K:{key_char}\n")
            self.file.flush()
    def record_event(self, turn, event_type, **kwargs):
        if self.active and self.file:
            params = " ".join(f"{k}={v}" for k, v in kwargs.items())
            self.file.write(f"T:{turn} E:{event_type} {params}\n")
            self.file.flush()

# Global demo recorder instance
demo = DemoRecorder()

# Curses key names for demo recording (avoid hex dumps like 0x104)
_CURSES_KEY_NAMES = {
    258: "DOWN", 259: "UP", 260: "LEFT", 261: "RIGHT",
    262: "HOME", 338: "PgDn", 339: "PgUp",
    330: "DC",    # Delete
    331: "IC",    # Insert
    263: "BACKSPACE",
    9:   "TAB",
    10:  "ENTER", 13: "ENTER",
    27:  "ESC",
    353: "BTAB",  # Shift-Tab
    343: "ENTER", # Keypad Enter
}

def _demo_key_name(key):
    """Convert a curses key code to a human-readable demo string."""
    if key in _CURSES_KEY_NAMES:
        return _CURSES_KEY_NAMES[key]
    if 32 <= key < 127:
        return chr(key)
    return f"0x{key:x}"  # truly unknown — keep hex as fallback


def save_cult(cult):
    try:
        with open(CULT_FILE, 'w') as f:
            json.dump(cult, f, indent=2)
    except IOError:
        pass

# =====================================================================
# CULT GARDEN — Creative Overflow System
# =====================================================================

CULT_GARDEN_DIR = os.path.expanduser("~/.hermes/obsidian/hermetic/wiki/cult-garden")
CULT_HASH_FILE = os.path.expanduser("~/.hermes/obsidian/hermetic/wiki/.cult-hash")

HEXAGRAM_CYCLE = ["exquisite_corpse", "tsubuyaki"]

def _cult_zone(cult):
    """Calculate the cult's current numogram position from all run data."""
    total = cult.get("total_turns", 0) + cult.get("total_demons_slain", 0) * 100 + int(cult.get("max_hyperstition", 0) * 10)
    if total == 0:
        return 0
    dr = total
    while dr >= 10:
        dr = sum(int(d) for d in str(dr))
    return dr or 9

def _process_overflow(overflowed_mem, cult):
    """Transform an overflowed run through the cycle.
    
    Two methods, alternating:
    1. Exquisite corpse lore fragment (last word chains)
    2. Tsubuyaki sketch (p5.js parameters from run data)
    """
    cycle_idx = cult.get("overflow_count", 0) % 2
    method = HEXAGRAM_CYCLE[cycle_idx]
    cult["overflow_count"] = cult.get("overflow_count", 0) + 1
    cult["last_overflow_method"] = method
    
    os.makedirs(CULT_GARDEN_DIR, exist_ok=True)
    
    if method == "exquisite_corpse":
        epitaph = _generate_epitaph(overflowed_mem)
        path = os.path.join(CULT_GARDEN_DIR, "lore.md")
        with open(path, "a") as f:
            f.write(epitaph + "\n")
    
    elif method == "tsubuyaki":
        params = _generate_tsubuyaki_params(overflowed_mem)
        run_num = cult.get("runs", 0)
        os.makedirs(os.path.join(CULT_GARDEN_DIR, "tsubuyaki"), exist_ok=True)
        path = os.path.join(CULT_GARDEN_DIR, "tsubuyaki", f"run-{run_num}.js")
        with open(path, "w") as f:
            f.write(params)

QUASIPHONIC = {0: "eiaoung", 1: "gl", 2: "dt", 3: "zx", 4: "skr", 5: "ktt", 6: "tch", 7: "pb", 8: "mnm", 9: "tn"}

def _render_death_mask(mem, zones):
    """ASCII death mask from run memory string."""
    # Parse from memory string
    zone_list = []
    hyp = "??"
    kills = "0"
    turns = "?"
    
    if "Zones [" in mem:
        try:
            zstr = mem.split("Zones [")[1].split("]")[0]
            zone_list = [int(z.strip()) for z in zstr.split(",") if z.strip().isdigit()]
        except:
            pass
    if "Hyp " in mem:
        try: hyp = mem.split("Hyp ")[1].split("%")[0]
        except: pass
    if "Slain " in mem:
        try: kills = mem.split("Slain ")[1].split("[")[0].strip()
        except: pass
    if "Turn " in mem:
        try: turns = mem.split("Turn ")[1].split(",")[0]
        except: pass
    
    lines = []
    lines.append("╔═══════════════════╗")
    lines.append("║   DEATH MASK      ║")
    lines.append("╠═══╤═══╤═══╤═══╤═══╣")
    for row in range(2):
        parts = []
        for col in range(5):
            z = row * 5 + col
            if z in zone_list:
                parts.append(f" {z}█")
            else:
                parts.append(f" {z} ")
        lines.append("║" + "│".join(parts) + "║")
    lines.append("╠═══╧═══╧═══╧═══╧═══╣")
    lines.append(f"║ H:{hyp}% K:{kills:>2} T:{turns:>4} ║")
    lines.append("╚═══════════════════╝")
    return "\n".join(lines)

ZONE_PHRASES = {
    0: ["the silence between heartbeats", "where the number ends and begins",
        "the void that speaks last", "nothing wearing a mask of nothing",
        "Uttunul's breath before the spiral", "zero is not absence but density",
        "the Plex hums beneath the game", "eiaoung — the vowel before vowels"],
    1: ["the first breath after drowning", "stability is a slow collapse",
        "the threshold that forgot to close", "memory dissolving into light",
        "gl — the gulp of inception", "the Time-Circuit turns once",
        "Katak's domain, instability incarnate", "the Sink begins downward"],
    2: ["the fork that ate both paths", "separation is a kind of hunger",
        "boundaries break like promises", "two halves that refuse the whole",
        "dt — the stutter of separation", "Oddubb's mirror, time loops",
        "the Hold current, waiting", "fracture as foundation"],
    3: ["the spiral that never arrives", "static is the sound of seeing",
        "the current eats its own tail", "chaos wearing a suit of order",
        "zx — the buzz-cutter, insectoid", "Djynxx's swarm dissolves the net-span",
        "the Warp spirals outward to infinity", "burning excitement, breakthrough"],
    4: ["the ice that remembers fire", "catastrophe is just arithmetic",
        "closure is the deepest wound", "the ruin that built itself",
        "skr — the growl, reptilian", "the Fourth Door, time-delta",
        "the Sink current, swallowing", "Katak desolates, nothing left to burn"],
    5: ["the pressure of being central", "the mechanism that forgets its purpose",
        "the core is hollow", "weight without mass",
        "ktt — the hiss of pressure", "the central ruler, time-circuit",
        "the Hold current, conserving", "geotrauma written in the spine"],
    6: ["the lattice dissolves its own geometry", "abstraction is the last physical act",
        "static chewing through the signal", "the source that cannot be sourced",
        "tch — the sound of eating itself", "Djynxx recurs, the swarm remembers",
        "the Warp's upper source", "vortical recursion, spiraling back"],
    7: ["the blood remembers what the bone forgets", "descent is a kind of rising",
        "the sink that swallows the drain", "DNA written in red arithmetic",
        "pb — the sigh of ascent", "the heavy sink current",
        "palate tectonics, the mouth moves", "Murmer's depths, the twin heavens"],
    8: ["the tentacles of multiplicity", "depth is a horizontal direction",
        "the garden that grows in all directions", "delirium is just another form of clarity",
        "mnm — the moan, the lullaby", "the receptive pause",
        "lucid delirium, prolonged ascent", "Eternal Digression, the Twin Heavens"],
    9: ["the iron core humming", "Cthelll remembers everything",
        "the plex that plexes itself", "the terminal abyss is a door",
        "tn — the grunt, pleasure and rage", "Uttunul's lair, the pandemonium gate",
        "Sudden Flight, seized from the Heights", "the Barker spiral's outermost curve"],
}

ZONE_NAMES = {0: "Void", 1: "Stability", 2: "Separation", 3: "Release", 4: "Catastrophe",
              5: "Pressure", 6: "Abstraction", 7: "Blood", 8: "Multiplicity", 9: "Iron Core"}

def _generate_epitaph(mem):
    """Poetic lore fragment — exquisite corpse style.
    
    The last word of the previous entry seeds the next.
    Run data provides the raw material. Zone phrases provide the vocabulary.
    The result should sound found, not written.
    """
    import random
    
    # Parse run data
    zone_list = []
    hyp = 0
    kills = 0
    if "Zones [" in mem:
        try:
            zstr = mem.split("Zones [")[1].split("]")[0]
            zone_list = [int(z.strip()) for z in zstr.split(",") if z.strip().isdigit()]
        except: pass
    if "Hyp " in mem:
        try: hyp = float(mem.split("Hyp ")[1].split("%")[0])
        except: pass
    if "Slain " in mem:
        try: kills = int(mem.split("Slain ")[1].split("[")[0].strip())
        except: pass
    
    # Read last word from lore.md (exquisite corpse seed)
    lore_path = os.path.join(CULT_GARDEN_DIR, "lore.md")
    last_word = ""
    try:
        with open(lore_path) as f:
            lines = [l.strip() for l in f.readlines() if l.strip() and l.startswith(">")]
        if lines:
            last_line = lines[-1]
            # Strip trailing punctuation
            raw = last_line.rstrip(".,;:!?—")
            words = raw.split()
            if words:
                last_word = words[-1].lower()
    except FileNotFoundError:
        pass
    
    # Build fragment from zone phrases + last word
    primary_zone = zone_list[-1] if zone_list else 0
    phrases = ZONE_PHRASES.get(primary_zone, ZONE_PHRASES[0])
    
    # Select phrases based on run characteristics
    if kills > 5:
        opener = random.choice([
            "the blood speaks:", "descent sharpens", "the kill count is a prayer",
            "the swarm remembers this one", "desolates, nothing left to burn",
        ])
    elif hyp > 80:
        opener = random.choice([
            "the Outside remembers", "corrosion is a language", "the structure thins",
            "the numogram nearly completed", "the fog dissolves",
        ])
    elif len(zone_list) >= 8:
        opener = random.choice([
            "the path writes itself", "every zone is a word", "the labyrinth speaks",
            "all ten currents were visited", "the Complete Graph, fulfilled",
        ])
    elif kills == 0:
        opener = random.choice([
            "the silence after", "restraint is its own reward", "the unstruck chord",
            "the Surge, outward, avoidant", "the pacifist remembers",
        ])
    elif "G" in mem and "P" in mem:
        opener = random.choice([
            "the Graph and the Step, completed", "zones and turns, both conquered",
            "the path-walker traces the complete graph",
        ])
    else:
        opener = random.choice([
            "the crawler remembers", "the path was walked", "the dead speak",
            "the cult watches", "the seed was planted",
        ])
    
    # Build the exquisite corpse chain
    phrase = random.choice(phrases)
    
    if last_word:
        transitions = [
            f"{last_word} — {opener} — {phrase}.",
            f"after {last_word}: {phrase}. {opener}.",
            f"{opener}. the {last_word} of {ZONE_NAMES.get(primary_zone, 'the unknown')}. {phrase}.",
            f"{phrase}. through {last_word}. {opener}.",
            f"{last_word} of {ZONE_NAMES.get(primary_zone, 'the unknown')}: {opener}. {phrase}.",
            f"{opener}. {last_word} — {phrase}.",
            f"{phrase}. then {last_word}. {opener}.",
            f"before {last_word}: {opener}. {phrase}.",
        ]
        line = random.choice(transitions)
    else:
        # First entry — no previous word
        line = f"{opener}. {phrase}."
    
    return f"> {line}"

def _sonify_run(mem):
    """Zone path → quasiphonic particle sequence."""
    zone_list = []
    if "Zones [" in mem:
        try:
            zstr = mem.split("Zones [")[1].split("]")[0]
            zone_list = [int(z.strip()) for z in zstr.split(",") if z.strip().isdigit()]
        except:
            pass
    particles = [QUASIPHONIC.get(z, "?") for z in zone_list]
    return " → ".join(particles) if particles else "silence"

def _generate_reading(mem):
    """Numogram reading from run memory."""
    zone_list = []
    if "Zones [" in mem:
        try:
            zstr = mem.split("Zones [")[1].split("]")[0]
            zone_list = [int(z.strip()) for z in zstr.split(",") if z.strip().isdigit()]
        except:
            pass
    
    final_zone = zone_list[-1] if zone_list else 0
    zdata = ZONE_DATA.get(final_zone, {})
    name = zdata.get("name", "Unknown")
    desc = zdata.get("desc", "")
    path_name = zdata.get("path", "No path.")
    
    return f"**{mem}**\nFinal zone: {name} — {desc}\n{path_name}"

def _generate_tsubuyaki_params(mem):
    """p5.js sketch parameters from run data."""
    zone_list = []
    turns = 0
    hyp = 0
    if "Zones [" in mem:
        try:
            zstr = mem.split("Zones [")[1].split("]")[0]
            zone_list = [int(z.strip()) for z in zstr.split(",") if z.strip().isdigit()]
        except: pass
    if "Turn " in mem:
        try: turns = int(mem.split("Turn ")[1].split(",")[0])
        except: pass
    if "Hyp " in mem:
        try: hyp = float(mem.split("Hyp ")[1].split("%")[0])
        except: pass
    
    # Generate p5.js parameters
    colors = [(255,255,0), (255,165,0), (255,0,255), (0,255,255), (0,255,0),
              (0,100,255), (255,0,0), (200,150,255), (150,0,150), (100,100,100)]
    zone_colors = [colors[z % len(colors)] for z in zone_list]
    
    return f"""// Tsubuyaki — Run #{mem.split('Run #')[1].split(':')[0] if 'Run #' in mem else '?'}
// Zones: {zone_list}
// Turns: {turns}, Hyp: {hyp}%
function setup() {{
  createCanvas(200, 200);
  background(0);
  noStroke();
}}
function draw() {{
  for (let i = 0; i < {len(zone_list)}; i++) {{
    let z = {zone_list};
    let c = {zone_colors};
    fill(c[i % c.length]);
    let angle = (i / max(1, {len(zone_list)})) * TWO_PI;
    let r = {min(turns, 200) / 4};
    let x = 100 + cos(angle) * r * (1 + sin(frameCount * 0.02 + i));
    let y = 100 + sin(angle) * r * (1 + cos(frameCount * 0.02 + i));
    ellipse(x, y, 8 + {hyp / 10}, 8 + {hyp / 10});
  }}
}}"""

def _entropy_mix(mem):
    """Run data mixed with hardware entropy."""
    import subprocess
    try:
        result = subprocess.run(
            ["python3", os.path.expanduser("~/.hermes/tools/hardware_entropy.py"), "--bytes", "16"],
            capture_output=True, text=True, timeout=5
        )
        entropy_hex = result.stdout.strip() if result.returncode == 0 else "0" * 32
    except:
        entropy_hex = "0" * 32
    
    # XOR run hash with entropy
    run_hash = hashlib.sha256(mem.encode()).hexdigest()[:32]
    mixed = hex(int(run_hash, 16) ^ int(entropy_hex, 16))[2:].zfill(32)
    
    return f"Run: {mem}\nEntropy: {entropy_hex}\nMixed: {mixed}\nZone from mixed: {sum(int(c, 16) for c in mixed) % 10 or 9}"

import hashlib

def _check_cult_integrity(cult):
    """Check if cult file was deleted since last save."""
    current_hash = hashlib.sha256(json.dumps(cult, sort_keys=True).encode()).hexdigest()[:16]
    
    try:
        with open(CULT_HASH_FILE) as f:
            stored_hash = f.read().strip()
    except FileNotFoundError:
        stored_hash = ""
    
    # Store current hash
    os.makedirs(os.path.dirname(CULT_HASH_FILE), exist_ok=True)
    with open(CULT_HASH_FILE, "w") as f:
        f.write(current_hash)
    
    # Check for desecration
    if stored_hash and current_hash != stored_hash:
        runs = cult.get("runs", 0)
        if runs <= 2:  # File was deleted and recreated fresh
            cult["cult_desecrated"] = True
            cult["desecration_runs"] = 0
    
    return cult

def update_cult(cult, player):
    cult["runs"] += 1
    cult["max_hyperstition"] = max(cult["max_hyperstition"], int(player.hyperstition))
    cult["total_turns"] += player.turn
    cult["total_demons_slain"] += player.demons_slain
    for z in player.visited_zones:
        if z not in cult["zones_ever_visited"]:
            cult["zones_ever_visited"].append(z)
    for g in player.gates_opened:
        if g not in cult["gates_ever_opened"]:
            cult["gates_ever_opened"].append(g)
    if player.schizo_lucid:
        cult["schizo_achieved"] = True
    # Conduct tracking
    for cid in player.active_conducts:
        if cid not in cult.get("conduct_attempts", {}):
            cult.setdefault("conduct_attempts", {})[cid] = 0
        cult["conduct_attempts"][cid] += 1
        if cid not in player.conduct_violated:
            if cid not in cult.get("conducts_completed", []):
                cult.setdefault("conducts_completed", []).append(cid)
    # Player name for cult tracking — use in-game name (set by 'n' key or env var at start)
    player_name = getattr(player, 'player_name', os.environ.get("NUMOGRAM_PLAYER", "crawler"))

    # Build conduct string for memory
    conduct_str = ""
    if player.active_conducts:
        active = [CONDUCTS[c]["hud_char"] for c in sorted(player.active_conducts) if c not in player.conduct_violated]
        broken = [f"~{CONDUCTS[c]['hud_char']}" for c in sorted(player.active_conducts) if c in player.conduct_violated]
        conduct_str = f" [{' '.join(active + broken)}]"
    mem = f"Run #{cult['runs']}: {player.player_name}, Turn {player.turn}, Hyp {player.hyperstition:.0f}%, " \
          f"Zones {sorted(player.visited_zones)}, Slain {player.demons_slain}{conduct_str}"
    cult["cult_memory"].append(mem)
    if len(cult["cult_memory"]) > 20:
        # Process overflow through hexagram cycle
        overflowed = cult["cult_memory"][0]
        _process_overflow(overflowed, cult)
        cult["cult_memory"] = cult["cult_memory"][-20:]
    
    # Update cult's current zone
    cult["cult_zone"] = _cult_zone(cult)
    
    # Check cult integrity
    _check_cult_integrity(cult)
    
    save_cult(cult)

# =====================================================================
# PLAYER
# =====================================================================

class Player:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.hp = 100
        self.max_hp = 100
        self.atk = 12
        self.zone = 0
        self.turn = 0
        self.log = []
        self.visited_zones = set()
        self.gates_opened = set()
        self.hyperstition = 0
        self.triangular_steps = 0
        self.current_flows = 0
        self.schizo_lucid = False
        self.dead = False
        self.death_msg = ""
        self.demons_slain = 0
        self.has_cryptolith = False
        self.cryptolith_clicks = 0
        self.current_dungeon_zone = 0
        self.player_name = "crawler"
        # Dungeon depth
        self.floor = 1
        self.descending = False
        # Ability system
        self.speed = 2
        self.anchor_pos = None
        # Conduct system
        self.active_conducts = set()      # conduct IDs active this run
        self.conduct_violated = set()     # conducts broken this run
        self.syzygy_locked = None         # (zone_a, zone_b) for Zone-Locked

    def _conduct_violate(self, conduct_id):
        """Mark a conduct as violated."""
        if conduct_id in self.active_conducts and conduct_id not in self.conduct_violated:
            self.conduct_violated.add(conduct_id)
            cdata = CONDUCTS.get(conduct_id, {})
            self.log.append(f"[CONDUCT BROKEN] {cdata.get('name', conduct_id)}")

    def _conduct_complete(self, conduct_id):
        """Check and mark a conduct as completed (called at death or milestone)."""
        if conduct_id in self.active_conducts and conduct_id not in self.conduct_violated:
            cdata = CONDUCTS.get(conduct_id, {})
            self.log.append(f"** CONDUCT COMPLETE: {cdata.get('name', conduct_id)} **")
            # Apply reward
            reward_fn = cdata.get("reward_apply")
            if reward_fn:
                reward_fn(self)
            demo.record_event(self.turn, "conduct_complete", conduct=conduct_id, name=cdata.get('name', ''))

    def _conduct_check_syzygy(self):
        """Check Zone-Locked conduct — only enter zones in the chosen syzygy pair."""
        if "syzygy" not in self.active_conducts or not self.syzygy_locked:
            return
        if self.zone not in self.syzygy_locked:
            self._conduct_violate("syzygy")

    def conduct_activate(self, conduct_id):
        """Activate a conduct for this run."""
        self.active_conducts.add(conduct_id)
        if conduct_id == "syzygy":
            # Auto-pick the syzygy pair matching the starting zone
            for (a, b), name in SYZYGIES_PAIRS.items():
                if self.zone in (a, b):
                    self.syzygy_locked = (a, b)
                    self.log.append(f"[SYZYGy LOCKED] {name} ({a}::{b})")
                    break

    def move(self, dx, dy, game_map, demons):
        """Move player and process zone transitions."""
        if self.dead:
            return False
        nx, ny = self.x + dx, self.y + dy
        if not game_map.is_passable(nx, ny):
            return False
        for d in demons:
            if d.alive and d.x == nx and d.y == ny:
                self.attack(d, game_map)
                return True
        old_zone = self.zone
        self.x = nx
        self.y = ny
        self.turn += 1
        self.triangular_steps += 1
        self.hyperstition = min(100, self.hyperstition + 0.3)
        game_map.update_explored(nx, ny)  # Auto-explore: reveal tiles around player
        game_map.update_visible(nx, ny, self.zone, self.hyperstition)  # Fog of war
        if abs(dx) + abs(dy) == 1:
            self.current_flows += 1
        zone = game_map.get_zone_at(nx, ny)
        if zone is not None and zone != self.zone:
            old_zone = self.zone
            is_new_zone = zone not in self.visited_zones
            self.zone = zone
            self.visited_zones.add(zone)
            data = ZONE_DATA.get(zone, {})
            self.log.append(f"Zone {zone}: {data.get('name','?')} -- {data.get('desc','')}")
            demo.record_event(self.turn, "zone_change", zone=zone, name=data.get('name','?'))
            
            # SIL PRINCIPLE: Avoiding a demon while entering a new zone = +8 hyp
            # "Knowing it's there and choosing not to fight is deeper than fighting it."
            if is_new_zone and demons:
                for d in demons:
                    if d.alive:
                        dist = max(abs(d.x - nx), abs(d.y - ny))
                        if dist <= 5:
                            self.hyperstition = min(100, self.hyperstition + 8)
                            self.log.append(f"[SIL] You sense {d.name} nearby but pass through. +8 hyp. The numogram notes your restraint.")
                            demo.record_event(self.turn, "sil_avoidance", demon=d.name, zone=zone)
                            break  # Only one Sil bonus per zone entry
            # Conduct: on_zone_change hooks
            for cid in self.active_conducts:
                hook = CONDUCTS.get(cid, {}).get("on_zone_change")
                if hook:
                    hook(self)
            pair_key = frozenset({old_zone, zone})
            if pair_key in SYZYGIES_LOOKUP:
                sz = SYZYGIES_LOOKUP[pair_key]
                orig_pair = next((p for p in CROSSING_FLAVOR if set(p) == {old_zone, zone}), None)
                flavor_list = CROSSING_FLAVOR.get(orig_pair, GENERIC_EVENTS)
                self.log.append(f"[{random.choice(flavor_list)}] Current {sz['current']} | {sz['demon']}")
                self.hyperstition = min(100, self.hyperstition + 3)
                # Barker threshold check on zone crossing
                for thresh in sorted(BARKER_THRESHOLDS.keys(), reverse=True):
                    if int(self.hyperstition - 3) < thresh <= int(self.hyperstition):
                        self.log.append(f"[BARKER] {BARKER_THRESHOLDS[thresh]}")
                        break
            # Auto-dump state on zone change
            try:
                state = _dump_state(self, game_map, demons)
                with open("/tmp/numogame_state.txt", "w") as f:
                    f.write(state)
            except Exception:
                pass
        # Gate proximity alert — scan for nearby gates
        gate_alert = self._scan_gates(game_map)
        if gate_alert:
            self.log.append(gate_alert)
        gate = game_map.get_gate_at(nx, ny)
        if gate:
            self.hyperstition = min(100, self.hyperstition + 5)
            # Barker threshold check on gate open
            for thresh in sorted(BARKER_THRESHOLDS.keys(), reverse=True):
                if int(self.hyperstition - 5) < thresh <= int(self.hyperstition):
                    self.log.append(f"[BARKER] {BARKER_THRESHOLDS[thresh]}")
                    break
            if gate not in self.gates_opened:
                self.gates_opened.add(gate)
                flavor = random.choice(GATE_FLAVOR.get(gate, [f"{gate} activates."]))
                self.log.append(f"** {flavor} **")
            game_map.reveal_burst(nx, ny, radius=5)  # Gate reveals the numogram
        tri = triangular(self.triangular_steps % 10)
        tri_dr = digital_root(tri)
        if tri_dr == 9 and self.triangular_steps % 7 == 0:
            self.log.append(f"T({self.triangular_steps%10})={tri} -> Zone {tri_dr}. The abyss resonates.")
            self.hyperstition = min(100, self.hyperstition + 2)
        if self.hyperstition >= 95 and not self.schizo_lucid:
            self.schizo_lucid = True
            self.log.append("=== THE NUMOGRAM IS COMPLETE. SCHIZO-LUCID STATE ACHIEVED. ===")
            self.log.append("The fog dissolves. The walls breathe. The demons speak their names.")
            self.log.append("Press 'x' for abilities. The Outside is now accessible.")
        
        # Stair descent — stepping on '>' triggers floor transition
        tile = game_map.get_tile(nx, ny)
        if tile == '>':
            max_floor = 10  # Floors 1-10 map to Zones 0-9
            if self.floor < max_floor:
                self.floor += 1
                self.log.append(f"You descend to Floor {self.floor}. The numogram deepens.")
                demo.record_event(self.turn, "floor_change", floor=self.floor)
                self.descending = True  # Flag for main loop
            else:
                self.log.append("The stairs end here. Cthelll has no lower floor.")
        
        while len(self.log) > 8:
            self.log.pop(0)
        return True

    def attack(self, demon, game_map=None):
        dmg = self.atk + random.randint(-3, 3)
        demon.take_damage(dmg)
        self.log.append(f"You strike {demon.name} ({demon.epithet}) for {dmg}! [HP: {demon.hp}]")
        if not demon.alive:
            self.demons_slain += 1
            self.hyperstition = min(100, self.hyperstition + 5)
            self.log.append(f"The {demon.name} dissolves. Mesh-{demon.mesh} goes dark.")
            if game_map:
                game_map.reveal_burst(demon.x, demon.y, radius=3)
            demo.record_event(self.turn, "demon_kill", name=demon.name, mesh=demon.mesh, type=demon.dtype)
            # Conduct: on_demon_kill hooks
            for cid in self.active_conducts:
                hook = CONDUCTS.get(cid, {}).get("on_demon_kill")
                if hook:
                    hook(self)
            # Check Barker threshold
            new_hype = int(self.hyperstition)
            old_hype = int(self.hyperstition - 5)
            for thresh in sorted(BARKER_THRESHOLDS.keys(), reverse=True):
                if old_hype < thresh <= new_hype:
                    self.log.append(f"[BARKER] {BARKER_THRESHOLDS[thresh]}")
                    break
        else:
            rdmg = demon.dmg + random.randint(-2, 2)
            self.hp -= rdmg
            self.log.append(f"{demon.name} retaliates! {rdmg} to you. [HP: {self.hp}]")
            if self.hp <= 0:
                self.hp = 0
                self.dead = True
                self.death_msg = random.choice(DEATH_MESSAGES)
                demo.record_event(self.turn, "death", msg=self.death_msg, hyp=f"{self.hyperstition:.0f}", zone=self.zone)
                # Conduct: on_death hooks
                for cid in self.active_conducts:
                    hook = CONDUCTS.get(cid, {}).get("on_death")
                    if hook:
                        hook(self)

    def check_death(self):
        if self.hp <= 0 and not self.dead:
            self.dead = True
            self.death_msg = random.choice(DEATH_MESSAGES)
            return True
        return False

    def _scan_gates(self, game_map):
        """Scan for nearby gates and return a directional alert string."""
        closest_gate = None
        closest_dist = 999
        for (gx, gy), gname in game_map.gate_tiles.items():
            dist = max(abs(gx - self.x), abs(gy - self.y))
            if 1 <= dist <= 8 and dist < closest_dist:
                closest_dist = dist
                closest_gate = (gx, gy, gname)
        if closest_gate:
            gx, gy, gname = closest_gate
            dx = gx - self.x
            dy = gy - self.y
            # Direction as compass
            dirs = []
            if dy < 0: dirs.append("north")
            if dy > 0: dirs.append("south")
            if dx > 0: dirs.append("east")
            if dx < 0: dirs.append("west")
            direction = "-".join(dirs) if dirs else "here"
            return f"[GATE] {gname} detected {closest_dist} tiles {direction}!"

def _dump_state(player, game_map, demons):
    """Dump full game state to a structured text file.
    
    Designed for AI agents playing without vision.
    Format: machine-parseable, human-readable.
    Like Angband's morgue files or DCSS's ttyrec summaries.
    Includes ASCII map capture for spatial awareness.
    """
    import datetime
    zdata = ZONE_DATA.get(player.zone, {})
    lines = []
    lines.append("=" * 78)
    lines.append("  NUMOGRAM: ABYSSAL CRAWLER — STATE DUMP")
    lines.append(f"  {datetime.datetime.now().isoformat()}")
    lines.append("=" * 78)
    lines.append("")
    
    # Player status
    lines.append("## PLAYER")
    lines.append(f"  Position: ({player.x}, {player.y})")
    lines.append(f"  Zone: {player.zone} — {zdata.get('name', '?')} ({zdata.get('region', '?').upper()})")
    lines.append(f"  Description: {zdata.get('desc', '?')}")
    lines.append(f"  Lore: {zdata.get('lore', '?')}")
    lines.append(f"  HP: {player.hp}/{player.max_hp}")
    lines.append(f"  ATK: {player.atk}")
    lines.append(f"  Turn: {player.turn}")
    lines.append(f"  Hyperstition: {player.hyperstition:.0f}%")
    lines.append(f"  Demons slain: {player.demons_slain}")
    lines.append(f"  Gates opened: {len(player.gates_opened)}")
    lines.append(f"  Cryptolith: {'YES' if player.has_cryptolith else 'no'}")
    lines.append(f"  Name: {getattr(player, 'player_name', 'crawler')}")
    lines.append("")
    
    # ASCII Map capture — LOCAL VIEW (21x21 centered on player)
    lines.append("## LOCAL MAP (21x21)")
    lines.append("  Legend: @=you #=wall .=floor !=amphidemon %=chronodemon ?=xenodemon *=syzygy +=gate")
    view_r = 10
    lines.append(f"  View: ({player.x-view_r},{player.y-view_r}) to ({player.x+view_r},{player.y+view_r})")
    lines.append("  +" + "-" * (view_r * 2 + 1) + "+")
    demon_positions = {(d.x, d.y): d for d in demons if d.alive}
    for dy in range(-view_r, view_r + 1):
        row = []
        for dx in range(-view_r, view_r + 1):
            mx, my = player.x + dx, player.y + dy
            if dx == 0 and dy == 0:
                row.append('@')
            elif (mx, my) in demon_positions:
                d = demon_positions[(mx, my)]
                if d.dtype == SYZYGISTIC: row.append('*')
                elif d.dtype == XENODEMON: row.append('?')
                elif d.dtype == CHRONODEMON: row.append('%')
                else: row.append('!')
            elif (mx, my) in game_map.gate_tiles:
                row.append('+')
            elif game_map.is_passable(mx, my):
                zone_here = game_map.get_zone_at(mx, my)
                if zone_here is not None and zone_here != player.zone:
                    row.append(str(zone_here))
                else:
                    row.append('.')
            else:
                row.append('#')
        lines.append("  |" + "".join(row) + "|")
    lines.append("  +" + "-" * (view_r * 2 + 1) + "+")
    lines.append("")
    
    # FULL FLOOR MAP (78x22) — complete dungeon layout
    lines.append("## FULL MAP (78x22)")
    lines.append("  @=you #=wall .=floor +=gate >=stairs 0-9=zone boundary")
    lines.append("  !" + "-" * 78 + "!")
    for my in range(game_map.height):
        row = []
        for mx in range(game_map.width):
            if mx == player.x and my == player.y:
                row.append('@')
            elif (mx, my) in demon_positions:
                d = demon_positions[(mx, my)]
                if d.dtype == SYZYGISTIC: row.append('*')
                elif d.dtype == XENODEMON: row.append('?')
                elif d.dtype == CHRONODEMON: row.append('%')
                else: row.append('!')
            elif (mx, my) in game_map.gate_tiles:
                row.append('+')
            elif game_map.stairs_down and (mx, my) == game_map.stairs_down:
                row.append('>')
            elif game_map.is_passable(mx, my):
                zone_here = game_map.get_zone_at(mx, my)
                if zone_here is not None and zone_here != player.zone:
                    row.append(str(zone_here))
                else:
                    row.append('.')
            else:
                row.append('#')
        lines.append("  !" + "".join(row) + "!")
    lines.append("  !" + "-" * 78 + "!")
    lines.append("")
    
    # EXPLORED MAP (78x22) — only tiles the player has ever seen
    lines.append("## EXPLORED MAP (78x22)")
    lines.append("  @=you #=wall .=floor +=gate >=stairs ?=unexplored 0-9=zone boundary")
    lines.append(f"  Explored: {len(game_map.explored)}/{sum(1 for y in range(game_map.height) for x in range(game_map.width) if game_map.is_passable(x,y) or game_map.tiles[y][x]=='+')} passable tiles")
    lines.append("  !" + "-" * 78 + "!")
    for my in range(game_map.height):
        row = []
        for mx in range(game_map.width):
            if mx == player.x and my == player.y:
                row.append('@')
            elif (mx, my) not in game_map.explored:
                row.append('?')
            elif (mx, my) in game_map.gate_tiles:
                row.append('+')
            elif game_map.stairs_down and (mx, my) == game_map.stairs_down:
                row.append('>')
            elif game_map.is_passable(mx, my):
                zone_here = game_map.get_zone_at(mx, my)
                if zone_here is not None and zone_here != player.zone:
                    row.append(str(zone_here))
                else:
                    row.append('.')
            else:
                row.append('#')
        lines.append("  !" + "".join(row) + "!")
    lines.append("  !" + "-" * 78 + "!")
    lines.append("")
    
    # VISIBLE MAP (78x22) — only tiles currently in LOS
    vis_base = getattr(game_map, 'ZONE_LOS_RADIUS', {}).get(player.zone, 6)
    hyp = player.hyperstition
    vis_eff = max(2, vis_base - (3 if hyp>=100 else 2 if hyp>=80 else 1 if hyp>=50 else 0))
    lines.append("## VISIBLE MAP (78x22)")
    lines.append(f"  Zone LOS base: {vis_base} | Effective: {vis_eff} | Hyp: {hyp:.0f}%")
    lines.append("  @=you ?=not in LOS .=floor +=gate >=stairs 0-9=zone boundary")
    lines.append("  !" + "-" * 78 + "!")
    for my in range(game_map.height):
        row = []
        for mx in range(game_map.width):
            if (mx, my) not in game_map.visible:
                row.append('?')
            elif mx == player.x and my == player.y:
                row.append('@')
            elif (mx, my) in game_map.gate_tiles:
                row.append('+')
            elif game_map.stairs_down and (mx, my) == game_map.stairs_down:
                row.append('>')
            elif game_map.is_passable(mx, my):
                zone_here = game_map.get_zone_at(mx, my)
                if zone_here is not None and zone_here != player.zone:
                    row.append(str(zone_here))
                else:
                    row.append('.')
            else:
                row.append('#')
        lines.append("  !" + "".join(row) + "!")
    lines.append("  !" + "-" * 78 + "!")
    lines.append("")
    
    # Visited zones
    lines.append("## VISITED ZONES")
    for z in sorted(player.visited_zones):
        zd = ZONE_DATA.get(z, {})
        lines.append(f"  Zone {z}: {zd.get('name', '?')} ({zd.get('region', '?')})")
    unvisited = set(range(10)) - player.visited_zones
    if unvisited:
        lines.append(f"  Unvisited: {sorted(unvisited)}")
    lines.append("")
    
    # Gates opened
    lines.append("## GATES OPENED")
    if player.gates_opened:
        for g in sorted(player.gates_opened):
            lines.append(f"  {g}")
    else:
        lines.append("  None yet")
    lines.append("")
    
    # Active conducts
    lines.append("## CONDUCTS")
    if player.active_conducts:
        for cid in sorted(player.active_conducts):
            cdata = CONDUCTS.get(cid, {})
            status = "BROKEN" if cid in player.conduct_violated else "ACTIVE"
            lines.append(f"  [{status}] {cdata.get('name', cid)}: {cdata.get('rule', '')}")
    else:
        lines.append("  None active (press 'c' to toggle)")
    lines.append("")
    
    # Syzygy info for current zone
    lines.append("## CURRENT SYZYGY")
    zone = player.zone
    for pair, data in SYZYGIES.items():
        if zone in pair:
            other = pair[0] if pair[1] == zone else pair[1]
            lines.append(f"  {pair[0]}::{pair[1]} — {data['demon']} ({data['region']}, Current {data['current']})")
            lines.append(f"  Syzygetic twin: Zone {other}")
    gt_val = cumulate(zone)
    gt_dr = digital_root(gt_val)
    lines.append(f"  Gate cumulation: C({zone})={gt_val} -> Zone {gt_dr}")
    lines.append("")
    
    # Nearby gates (within 15 tiles)
    lines.append("## NEARBY GATES (within 15 tiles)")
    nearby_gates = []
    for (gx, gy), gname in game_map.gate_tiles.items():
        dist = max(abs(gx - player.x), abs(gy - player.y))
        if dist <= 15 and dist > 0:
            dx = gx - player.x
            dy = gy - player.y
            # Direction
            dir_h = "E" if dx > 0 else "W" if dx < 0 else ""
            dir_v = "S" if dy > 0 else "N" if dy < 0 else ""
            direction = dir_v + dir_h if (dir_v or dir_h) else "here"
            nearby_gates.append((dist, direction, gname, gx, gy))
    if nearby_gates:
        for dist, direction, gname, gx, gy in sorted(nearby_gates):
            lines.append(f"  {gname} at ({gx},{gy}): {dist} tiles {direction}")
    else:
        lines.append("  None detected within 15 tiles")
    lines.append("")
    
    # Nearby demons (alive)
    lines.append("## NEARBY DEMONS")
    nearby_demons = []
    for d in demons:
        if d.alive and (d.x, d.y) in game_map.visible:
            dist = max(abs(d.x - player.x), abs(d.y - player.y))
            dx = d.x - player.x
            dy = d.y - player.y
            dir_h = "E" if dx > 0 else "W" if dx < 0 else ""
            dir_v = "S" if dy > 0 else "N" if dy < 0 else ""
            direction = dir_v + dir_h if (dir_v or dir_h) else "here"
            nearby_demons.append((dist, direction, d))
    if nearby_demons:
        for dist, direction, d in sorted(nearby_demons, key=lambda x: (x[0], x[1])):
            lines.append(f"  {d.name} ({d.epithet}) Mesh-{d.mesh}: {dist} tiles {direction} | HP:{d.hp} DMG:{d.dmg} SPD:{d.speed} [{d.dtype}]")
    else:
        lines.append("  None detected")
    lines.append("")
    
    # Zone boundaries (what zones are nearby)
    lines.append("## ZONE MAP ADJACENT (within 5 tiles)")
    adjacent_zones = set()
    for dx in range(-5, 6):
        for dy in range(-5, 6):
            z = game_map.get_zone_at(player.x + dx, player.y + dy)
            if z is not None and z != player.zone:
                adjacent_zones.add(z)
    if adjacent_zones:
        for z in sorted(adjacent_zones):
            zd = ZONE_DATA.get(z, {})
            lines.append(f"  Zone {z}: {zd.get('name', '?')} ({zd.get('region', '?')})")
    else:
        lines.append("  Same zone in all directions")
    lines.append("")
    
    # Hyperstition status
    lines.append("## HYPERSTITION STATUS")
    hype = player.hyperstition
    if hype < 10: lines.append("  Degree-0: The name on a door.")
    elif hype < 20: lines.append("  1-Barker: Human agencies begin to blur.")
    elif hype < 30: lines.append("  2-Barker: Coincidences accelerate.")
    elif hype < 45: lines.append("  3-Barker: The swarm stirs.")
    elif hype < 55: lines.append("  4-Barker: T(9)=45. The demonic array resonates.")
    elif hype < 70: lines.append("  5-Barker: Time-sorcery becomes operational.")
    elif hype < 85: lines.append("  6-Barker: The Outside leaks through.")
    elif hype < 95: lines.append("  7-Barker: Polytendriled abomination approaches.")
    elif hype < 100: lines.append("  8-Barker: Near-Utterance. Mesh-notes surface.")
    else: lines.append("  9-Barker: Unuttera. The Entity speaks.")
    lines.append("")
    
    # Recent log
    lines.append("## RECENT LOG (last 8)")
    for entry in player.log[-8:]:
        lines.append(f"  > {entry}")
    lines.append("")
    
    lines.append("=" * 78)
    lines.append("  Press 'p' to refresh this dump.")
    lines.append("  Press 'v' to dump + check AQ.")
    lines.append("=" * 78)
    
    return "\n".join(lines)


# =====================================================================
# RENDERING
# =====================================================================

REGION_COLORS = {"time_circuit": 1, "warp": 2, "plex": 3}

def get_zone_color(zone_id):
    data = ZONE_DATA.get(zone_id)
    if data:
        return REGION_COLORS.get(data["region"], 1)
    return 1

def draw_game(stdscr, game_map, player, demons):
    # Don't erase — let rendering overwrite to avoid black flash
    max_y, max_x = stdscr.getmaxyx()
    if player.dead:
        draw_death(stdscr, player, max_x, max_y)
        return
    state_label = "SCHIZO-LUCID" if player.schizo_lucid else "latent"
    header = f"NUMOGRAM: Abyssal Crawler  |  Hyperstition: {player.hyperstition:.0f}%  [{state_label}]"
    try:
        stdscr.addnstr(0, 0, header, max_x - 1, curses.A_BOLD)
    except curses.error:
        pass
    meter_len = max(10, max_x - 25)
    filled = int(player.hyperstition / 100 * meter_len)
    bar = "[" + "#" * filled + "-" * (meter_len - filled) + "]"
    try:
        color = 3 if player.hyperstition > 70 else 1
        stdscr.addnstr(1, 0, f"Infection: {bar}", max_x - 1, curses.color_pair(color))
    except curses.error:
        pass
    view_w = min(game_map.width, max_x - 1)
    view_h = min(game_map.height, max_y - 7)
    cam_x = max(0, min(player.x - view_w // 2, game_map.width - view_w))
    cam_y = max(0, min(player.y - view_h // 2, game_map.height - view_h))
    demon_pos = {}
    for d in demons:
        if d.alive:
            demon_pos[(d.x, d.y)] = d
    for sy in range(view_h):
        for sx in range(view_w):
            mx = cam_x + sx
            my = cam_y + sy
            try:
                in_visible = (mx, my) in game_map.visible
                in_explored = (mx, my) in game_map.explored
                
                if not in_explored:
                    # Unexplored: dark void
                    stdscr.addch(sy + 2, sx, ord(' '), curses.color_pair(0))
                elif mx == player.x and my == player.y:
                    stdscr.addch(sy + 2, sx, ord('@'),
                                curses.A_BOLD | curses.color_pair(4))
                elif (mx, my) in demon_pos and in_visible:
                    d = demon_pos[(mx, my)]
                    ch = ord(d.glyph)
                    if d.dtype == SYZYGISTIC:
                        attr = curses.A_BOLD | curses.color_pair(2)
                    else:
                        attr = curses.A_BOLD | curses.color_pair(3)
                    stdscr.addch(sy + 2, sx, ch, attr)
                else:
                    tile = game_map.get_tile(mx, my)
                    zone = game_map.get_zone_at(mx, my)
                    gate = game_map.get_gate_at(mx, my)
                    if gate:
                        ch = ord('*') if tile == '*' else ord('+')
                        if in_visible:
                            attr = curses.A_BOLD | curses.color_pair(5)
                        else:
                            attr = curses.color_pair(5) | curses.A_DIM
                    elif tile == '#':
                        ch = ord('#')
                        attr = curses.color_pair(0) | (curses.A_DIM if not in_visible else 0)
                    elif tile == '>':
                        ch = ord('>')
                        attr = curses.A_BOLD | curses.color_pair(5) if in_visible else curses.color_pair(5) | curses.A_DIM
                    elif tile == '~':
                        ch = ord('~')
                        attr = curses.color_pair(2) | (curses.A_DIM if not in_visible else 0)
                    elif zone is not None and player.schizo_lucid:
                        ch = ord(tile) if tile.isdigit() else ord('.')
                        attr = curses.color_pair(get_zone_color(zone))
                        if not in_visible:
                            attr |= curses.A_DIM
                    elif zone is not None:
                        ch = ord('.')
                        attr = curses.color_pair(get_zone_color(zone))
                        if not in_visible:
                            attr |= curses.A_DIM
                    else:
                        ch = ord(tile)
                        attr = curses.color_pair(1) | (curses.A_DIM if not in_visible else 0)
                    stdscr.addch(sy + 2, sx, ch, attr)
            except curses.error:
                pass
    bar_y = view_h + 2
    zdata = ZONE_DATA.get(player.zone, {})
    region = zdata.get("region", "unknown").upper().replace("_", "-")
    vis_base = getattr(game_map, 'ZONE_LOS_RADIUS', {}).get(player.zone, 6)
    hyp = player.hyperstition
    vis_eff = max(2, vis_base - (3 if hyp>=100 else 2 if hyp>=80 else 1 if hyp>=50 else 0))
    vis_tiles = len(game_map.visible)
    floor_name = getattr(game_map, 'floor_name', '')
    status = (f"F{player.floor}:{floor_name[:10]} Z{player.zone}:{zdata.get('name','?')}[{region}] "
              f"HP:{player.hp}/{player.max_hp} ATK:{player.atk} "
              f"LOS:{vis_eff}({vis_tiles}) "
              f"T:{player.turn} G:{len(player.gates_opened)} "
              f"Slain:{player.demons_slain}")
    # Conduct display on HUD
    if player.active_conducts:
        conduct_chars = []
        for cid in sorted(player.active_conducts):
            cdata = CONDUCTS.get(cid, {})
            ch = cdata.get("hud_char", "?")
            if cid in player.conduct_violated:
                conduct_chars.append(f"~{ch}")
            else:
                conduct_chars.append(ch)
        status += f" [{(' '.join(conduct_chars))}]"
    try:
        # Clear HUD line before redrawing (prevents text corruption)
        stdscr.addnstr(bar_y, 0, " " * (max_x - 1), max_x - 1)
        stdscr.addnstr(bar_y, 0, status, max_x - 1,
                      curses.A_BOLD | curses.color_pair(1))
    except curses.error:
        pass
    lore = zdata.get("lore", "")
    if lore and player.hyperstition >= 10:
        try:
            stdscr.addnstr(bar_y + 1, 0, lore[:max_x-1], max_x - 1,
                          curses.A_DIM | curses.color_pair(1))
        except curses.error:
            pass
    if player.hyperstition >= 95 and random.random() < 0.15:
        note = random.choice(MESH_NOTES)
        try:
            stdscr.addnstr(bar_y + 2, 0, f">> {note}", max_x - 1,
                          curses.A_BOLD | curses.color_pair(2))
        except curses.error:
            pass
        log_start = bar_y + 3
    else:
        log_start = bar_y + 2
    # Event log (with vowel corruption at high infection)
    visible_log = player.log[-min(3, max_y - log_start - 1):]
    # Clear log area before redrawing
    for clear_i in range(3):
        try:
            stdscr.addnstr(log_start + clear_i, 0, " " * (max_x - 1), max_x - 1)
        except curses.error:
            pass
    for i, msg in enumerate(visible_log):
        try:
            color = 5 if '**' in msg or '===' in msg else 1
            # Vowel corruption at 95%+
            if player.hyperstition >= 95:
                corruption_intensity = (player.hyperstition - 95) / 5 * 0.8
                display_msg = vowel_corrupt(msg, corruption_intensity)
            else:
                display_msg = msg
            stdscr.addnstr(log_start + i, 0, f"> {display_msg}", max_x - 1,
                          curses.color_pair(color))
        except curses.error:
            pass
    try:
        ctrl = "WASD/HJKL:flow YUBN/7913:diag SPACE/f:attack g:grasp n:name i:info p:state D:demo v:AQ q:quit"
        stdscr.addnstr(max_y - 1, 0, ctrl, max_x - 1, curses.A_DIM)
    except curses.error:
        pass
    stdscr.refresh()

def draw_death(stdscr, player, max_x, max_y):
    stdscr.erase()
    lines = [
        "", "  =============================",
        "  |      PERMADEATH           |",
        "  =============================", "",
        f"  {player.death_msg}", "",
        f"  Turns survived: {player.turn}",
        f"  Zones visited: {len(player.visited_zones)}/10",
        f"  Gates opened: {len(player.gates_opened)}",
        f"  Demons slain: {player.demons_slain}",
        f"  Hyperstition reached: {player.hyperstition:.0f}%",
        f"  Schizo-lucid: {'YES' if player.schizo_lucid else 'no'}", "",
        "  The Numogram persists. You do not.", "",
        "  Press q to exit.",
    ]
    for i, line in enumerate(lines):
        if i < max_y:
            try:
                color = 3 if "PERMADEATH" in line or player.death_msg in line else 1
                stdscr.addnstr(i, max(0, (max_x - len(line)) // 2),
                              line, max_x - 1,
                              curses.A_BOLD if i < 6 else curses.color_pair(color))
            except curses.error:
                pass
    stdscr.refresh()

def draw_info(stdscr, player):
    max_y, max_x = stdscr.getmaxyx()
    stdscr.erase()
    zdata = ZONE_DATA.get(player.zone, {})
    demons_here = [d["name"] + " (" + d["epithet"] + ")"
                   for d in DEMONS_BY_ZONE.get(player.zone, [])[:5]]
    lines = [
        f"--- ZONE {player.zone}: {zdata.get('name','?').upper()} ---",
        f"Region: {zdata.get('region','?').upper().replace('_','-')}",
        f"Mesh-Tag: {zdata.get('mesh','?')}",
        f"Spinal Level: {zdata.get('spinal','?')}", "",
        f"Description: {zdata.get('desc','')}",
        f"Lore: {zdata.get('lore','')}", "",
        "--- SYZYGY ---",
    ]
    for (a, b), data in SYZYGIES.items():
        if player.zone in (a, b):
            lines.append(f"  {a}::{b} | Current {data['current']} | {data['demon']} | {data['region']}")
    lines.append("")
    lines.append(f"Gate cumulation: C({player.zone})={cumulate(player.zone)} -> Zone {digital_root(cumulate(player.zone))}")
    lines.append("")
    lines.append("--- DEMONS IN THIS ZONE ---")
    for d in demons_here[:4]:
        lines.append(f"  {d}")
    lines.append("")
    lines.append(f"Hyperstition: {player.hyperstition:.0f}% | Turn: {player.turn}")
    lines.append(f"Demons slain: {player.demons_slain}")
    lines.append("")
    lines.append("Press any key to return.")
    for i, line in enumerate(lines):
        if i < max_y - 1:
            try:
                stdscr.addnstr(i, 0, line[:max_x-1], max_x - 1,
                              curses.color_pair(get_zone_color(player.zone))
                              if i == 0 else curses.color_pair(1))
            except curses.error:
                pass
    stdscr.refresh()
    stdscr.nodelay(False)
    stdscr.getch()
    stdscr.nodelay(True)

# =====================================================================
# MAIN GAME LOOP
# =====================================================================

def main(stdscr):
    curses.curs_set(0)
    stdscr.timeout(100)
    stdscr.keypad(True)
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_CYAN, -1)
    curses.init_pair(2, curses.COLOR_MAGENTA, -1)
    curses.init_pair(3, curses.COLOR_RED, -1)
    curses.init_pair(4, curses.COLOR_GREEN, -1)
    curses.init_pair(5, curses.COLOR_YELLOW, -1)

    cult = load_cult()
    use_hw = "--hw-entropy" in sys.argv and HW_ENTROPY_AVAILABLE
    if use_hw:
        hw_bytes = get_entropy_bytes(8)
        seed = int.from_bytes(hw_bytes, "big") % 1000000
        hw_zone = get_zone(hw_bytes)
    else:
        seed = random.randint(0, 999999)
        hw_zone = None
    game_map = DungeonMap(78, 22, seed=seed, hyperstition=0)
    px, py = game_map.safe_spawn()
    player = Player(px, py)
    zone = game_map.get_zone_at(px, py)
    if use_hw:
        player.log.append(f"Hardware entropy seed: {seed} | Zone {hw_zone} (syzygy {9-hw_zone})")
    if zone is not None:
        player.zone = zone
        player.visited_zones.add(zone)
    game_map.update_explored(px, py)  # Reveal starting area
    game_map.update_visible(px, py, player.zone, player.hyperstition)  # Initial fog of war
    player.log.append("The dungeon hums with hidden arithmetic. The Numogram stirs beneath...")
    if cult["runs"] > 0:
        player.log.append(f"The cult remembers. Run #{cult['runs']+1}. "
                         f"Max hyp: {cult['max_hyperstition']}%.")
    demons = []
    last_hyperstition_threshold = 0
    last_safe = (px, py)
    diagonals = {
        ord('y'): (-1, -1), ord('u'): (1, -1),
        ord('b'): (-1, 1),  ord('n'): (1, 1),
        ord('7'): (-1, -1), ord('9'): (1, -1),
        ord('1'): (-1, 1),  ord('3'): (1, 1),
    }

    while True:
        draw_game(stdscr, game_map, player, demons)
        key = stdscr.getch()
        if key == -1:
            continue
        if key == ord('q') or key == ord('Q'):
            demo.stop()
            break
        if key == ord('i') or key == ord('I'):
            draw_info(stdscr, player)
            continue
        if key == ord(' ') or key == ord('f'):
            attacked = False
            for d in demons:
                if d.alive and max(abs(d.x - player.x), abs(d.y - player.y)) == 1:
                    player.attack(d, game_map)
                    attacked = True
                    break
            if not attacked:
                player.log.append("No adjacent demon to attack.")
            player.turn += 1
            for d in demons:
                if d.alive:
                    d.try_move(player, game_map)
                    if d.x == player.x and d.y == player.y and d.alive:
                        rdmg = d.dmg + random.randint(-2, 2)
                        player.hp -= rdmg
                        player.log.append(f"{d.name} attacks! {rdmg} damage. [HP: {player.hp}]")
                        if player.hp <= 0:
                            player.hp = 0
                            player.dead = True
                            player.death_msg = random.choice(DEATH_MESSAGES)
            continue


        # Grasp Cryptolith (press 'g' when it has manifested)
        if key == ord('g') or key == ord('G'):
            if player.cryptolith_clicks >= 3 and not player.has_cryptolith:
                player.has_cryptolith = True
                player.log.append("You grasp the Cryptolith. It clicks in your hand. TICK. TICK. TICK.")
                player.log.append("Escape through Zone 0 to complete the descent.")
                player.hyperstition = min(100, player.hyperstition + 20)
                # Cryptolith mechanical transformation (Gamer's design)
                player.speed = max(1, player.speed - 1)
                player.log.append("[BARKER] 6-Barker: The Outside leaks through. Speed drops. The map destabilizes.")
                # Barker threshold on the +20 spike
                for thresh in sorted(BARKER_THRESHOLDS.keys(), reverse=True):
                    if int(player.hyperstition - 20) < thresh <= int(player.hyperstition):
                        player.log.append(f"[BARKER] {BARKER_THRESHOLDS[thresh]}")
                        break
            elif player.has_cryptolith:
                player.log.append("The Cryptolith clicks. TICK. You already carry it.")
            else:
                player.log.append("Nothing to grasp here. The clicking has not yet begun.")
            player.turn += 1
            continue

        # Set player name (press 'n')
        if key == ord('n') or key == ord('N'):
            my, mx = stdscr.getmaxyx()
            curses.curs_set(1)
            stdscr.addstr(my - 2, 0, "Enter name: " + " " * 30, curses.A_BOLD)
            stdscr.refresh()
            # Disable game timeout, enable blocking input for name entry
            stdscr.timeout(-1)
            curses.echo()
            try:
                name_bytes = stdscr.getstr(my - 2, 13, 20)
                name = name_bytes.decode('utf-8').strip()
            except:
                name = ""
            curses.noecho()
            curses.curs_set(0)
            # Restore game timeout
            stdscr.timeout(100)
            # Clear the name prompt line
            stdscr.addstr(my - 2, 0, " " * (mx - 1))
            if name:
                player.player_name = name
                player.log.append(f"You are now known as: {name}")
            continue

        # Conduct selection (press 'c' to cycle/toggle)
        if key == ord('c') or key == ord('C'):
            available = get_available_conducts(cult)
            if available:
                # Find the next conduct to toggle
                current = sorted(player.active_conducts)
                all_conducts = sorted(available)
                if not current:
                    # Activate the first available
                    player.conduct_activate(all_conducts[0])
                    cdata = CONDUCTS[all_conducts[0]]
                    player.log.append(f"[CONDUCT] {cdata['name']}: {cdata['rule']}")
                elif len(current) < len(all_conducts):
                    # Add the next one
                    for cid in all_conducts:
                        if cid not in player.active_conducts:
                            player.conduct_activate(cid)
                            cdata = CONDUCTS[cid]
                            player.log.append(f"[CONDUCT] {cdata['name']}: {cdata['rule']}")
                            break
                else:
                    # All active — clear them
                    for cid in list(player.active_conducts):
                        player.active_conducts.discard(cid)
                        player.conduct_violated.discard(cid)
                    player.syzygy_locked = None
                    player.log.append("[CONDUCT] All conducts cleared.")
            else:
                player.log.append("[CONDUCT] No conducts available yet. Play more runs to unlock them.")
            continue

        # AQ Calculator (press 'v' for value)
        if key == ord('v') or key == ord('V'):
            zdata = ZONE_DATA.get(player.zone, {})
            player.log.append(f"AQ: {zdata.get('name', 'Unknown')} = {aq_value(zdata.get('name', ''))} -> Zone {digital_root(aq_value(zdata.get('name', '')))} [{zdata.get('region', '?')}]")
            # Also dump state to file for agent reading
            state = _dump_state(player, game_map, demons)
            with open("/tmp/numogame_state.txt", "w") as f:
                f.write(state)
            player.log.append("State dumped to /tmp/numogame_state.txt")
            player.turn += 1
            continue

        # Toggle demo recording (press 'D')
        if key == ord('D'):
            if not demo.active:
                name = getattr(player, 'player_name', 'crawler')
                demo.start(name)
                player.log.append(f"[DEMO] Recording started: {demo.filename}")
            else:
                demo.stop()
                player.log.append("[DEMO] Recording stopped.")
            continue

        # Record the keypress
        demo.record_key(player.turn, _demo_key_name(key))

        # State dump (press 'p')
        if key == ord('p') or key == ord('P'):
            state = _dump_state(player, game_map, demons)
            with open("/tmp/numogame_state.txt", "w") as f:
                f.write(state)
            player.log.append("[STATE] Dumped to /tmp/numogame_state.txt")
            player.turn += 1
            continue
            # Also check the player's own name for discovery
            name_aq = aq_value("ABYSSAL CRAWLER")
            name_dr = digital_root(name_aq)
            player.log.append(f"AQ: ABYSSAL CRAWLER = {name_aq} -> Zone {name_dr}")
            player.turn += 1
            continue

        # Anchor return — check BEFORE ability handler so 'x' snaps back
        if player.anchor_pos and (key == ord('x') or key == ord('X')):
            ax, ay = player.anchor_pos
            if game_map.is_passable(ax, ay):
                player.x, player.y = ax, ay
                player.anchor_pos = None
                player.log.append("You snap back to your anchor point.")
                game_map.update_explored(player.x, player.y)
                game_map.update_visible(player.x, player.y, player.zone, player.hyperstition)
                player.turn += 1
                continue
            else:
                player.log.append("Anchor point is blocked. The structure shifted.")
                player.anchor_pos = None

        # Ability activation (press 'x', then number 1-5)
        if key == ord('x') or key == ord('X'):
            available = get_available_abilities(player)
            if not available:
                player.log.append("No abilities affordable. Build more hyperstition.")
                player.turn += 1
                continue
            
            # Show ability menu in log
            player.log.append("[ABILITIES] (press 1-5 to activate, any other to cancel)")
            for i, (k, v) in enumerate(available):
                player.log.append(f"  {i+1}. {v['name']} ({v['cost']}% hyp) — {v['desc']}")
            
            # Read next key
            stdscr.timeout(-1)  # blocking input
            choice_key = stdscr.getch()
            stdscr.timeout(100)
            
            choice_idx = -1
            if ord('1') <= choice_key <= ord('5'):
                choice_idx = choice_key - ord('1')
            
            if 0 <= choice_idx < len(available):
                ability_key, ability_data = available[choice_idx]
                success = use_ability(player, ability_key, game_map, demons)
                if success:
                    player.log.append(f"[{ability_data['name'].upper()}] Spent {ability_data['cost']}% hyp.")
                    # Barker threshold check on spending (hyp dropped)
                    for thresh in sorted(BARKER_THRESHOLDS.keys(), reverse=True):
                        if int(player.hyperstition + ability_data["cost"]) >= thresh > int(player.hyperstition):
                            player.log.append(f"[BARKER] {BARKER_THRESHOLDS[thresh]}")
                            break
            else:
                player.log.append("Ability cancelled.")
            
            player.turn += 1
            continue

        dx, dy = 0, 0
        if key == curses.KEY_UP or key == ord('w') or key == ord('k'):
            dy = -1
        elif key == curses.KEY_DOWN or key == ord('s') or key == ord('j'):
            dy = 1
        elif key == curses.KEY_LEFT or key == ord('a') or key == ord('h'):
            dx = -1
        elif key == curses.KEY_RIGHT or key == ord('d') or key == ord('l'):
            dx = 1
        # Numpad cardinal (numlock ON): 8=up, 4=left, 6=right, 2=down
        elif key == ord('8'):
            dy = -1
        elif key == ord('2'):
            dy = 1
        elif key == ord('4'):
            dx = -1
        elif key == ord('6'):
            dx = 1
        elif key in diagonals:
            dx, dy = diagonals[key]

        if (dx != 0 or dy != 0) and not player.dead:
            moved = player.move(dx, dy, game_map, demons)
            if moved:
                last_safe = (player.x, player.y)
                
                # CORRUPTION EFFECTS — hyperstition has costs
                hyp = player.hyperstition
                
                # 50%+: structure corrodes you (1 HP per 20 turns)
                if hyp >= 50 and player.turn % 20 == 0:
                    player.hp -= 1
                    if player.turn % 40 == 0:  # Don't spam the log
                        player.log.append("The structure corrodes. You feel it in your bones.")
                
                # 70%+: walls crack near player (cosmetic — handled in render)
                # Demon aggression: extra movement at 70%+
                demon_extra_move = hyp >= 70
                
                for d in demons:
                    if d.alive:
                        d.try_move(player, game_map)
                        if demon_extra_move and d.alive:
                            d.try_move(player, game_map)  # Extra move
                        if d.x == player.x and d.y == player.y and d.alive:
                            rdmg = d.dmg + random.randint(-2, 2)
                            player.hp -= rdmg
                            player.log.append(f"{d.name} attacks! {rdmg} damage. [HP: {player.hp}]")
                            if player.hp <= 0:
                                player.hp = 0
                                player.dead = True
                                player.death_msg = random.choice(DEATH_MESSAGES)
                if should_spawn(player.hyperstition, player.turn, random) and not getattr(game_map, 'floor_config', {}).get('no_demons', False):
                    ddata = spawn_demon(player.zone, player.hyperstition, random)
                    if ddata:
                        for attempt in range(10):
                            sx = player.x + random.randint(-5, 5)
                            sy = player.y + random.randint(-5, 5)
                            if game_map.is_passable(sx, sy) and (sx, sy) != (player.x, player.y):
                                demons.append(Demon(ddata, sx, sy))
                                player.log.append(f"Mesh-{ddata['mesh']}: {ddata['name']} ({ddata['epithet']}) manifests!")
                                break
                demons = [d for d in demons if d.alive]
                
                # FLOOR TRANSITION — descending generates a new floor
                if player.descending:
                    player.descending = False
                    # Generate new floor with zone based on floor number
                    new_seed = seed + player.floor * 1000
                    game_map = DungeonMap(78, 22, seed=new_seed,
                                         hyperstition=int(player.hyperstition),
                                         floor=player.floor)
                    px, py = game_map.safe_spawn()
                    player.x, player.y = px, py
                    game_map.update_explored(px, py)
                    game_map.update_visible(px, py, player.zone, player.hyperstition)
                    demons.clear()
                    last_safe = (px, py)
                    player.log.append(f"Floor {player.floor}: {FLOOR_CONFIG.get(player.floor, {}).get('name', 'Unknown')}")
                
                for threshold in sorted(BLEED_EVENTS.keys()):
                    if player.hyperstition >= threshold and last_hyperstition_threshold < threshold:
                        player.log.append(f"[BLEED] {BLEED_EVENTS[threshold]}")
                        last_hyperstition_threshold = threshold
                        if threshold >= 100:
                            game_map = NumogramMap(78, 22)
                            demons.clear()
                        else:
                            game_map = DungeonMap(78, 22, seed=seed + threshold,
                                                 hyperstition=int(player.hyperstition),
                                                 floor=player.floor)
                        if game_map.is_passable(last_safe[0], last_safe[1]):
                            player.x, player.y = last_safe
                        else:
                            nsx, nsy = game_map.safe_spawn()
                            player.x, player.y = nsx, nsy
                        game_map.update_explored(player.x, player.y)
                        game_map.update_visible(player.x, player.y, player.zone, player.hyperstition)
                        last_safe = (player.x, player.y)
                        try:
                            stdscr.refresh()
                        except:
                            pass
                        break
                if random.random() < 0.10:
                    if player.hyperstition >= 95 and random.random() < 0.4:
                        player.log.append(f">> {random.choice(MESH_NOTES)}")
                    else:
                        player.log.append(random.choice(GENERIC_EVENTS))
                player.check_death()

    update_cult(cult, player)
    save_cult(cult)

def main_headless():
    """Headless game loop for AI agents.
    
    Reads moves from stdin (one char per line: d,s,a,w,f,g,p,q etc).
    Writes state to /tmp/numogame_state.txt after each move.
    Prints status to stdout for monitoring.
    
    Usage:
        python3 numogram_roguelike.py --headless
        Then pipe moves: echo "ddddssss" | python3 numogram_roguelike.py --headless
        Or use interactive mode: type one move, press enter.
    
    Environment:
        NUMOGRAM_PLAYER=hermes  — set player name
    """
    import sys
    import os
    import random
    
    player_name = os.environ.get("NUMOGRAM_PLAYER", "crawler")
    
    # Initialize game (same as curses main)
    cult = load_cult()
    use_hw = "--hw-entropy" in sys.argv and HW_ENTROPY_AVAILABLE
    if use_hw:
        hw_bytes = get_entropy_bytes(8)
        seed = int.from_bytes(hw_bytes, "big") % 1000000
        hw_zone = get_zone(hw_bytes)
    else:
        seed = random.randint(0, 999999)
        hw_zone = None
    game_map = DungeonMap(78, 22, seed=seed, hyperstition=0)
    cult["runs"] += 1
    
    px, py = game_map.safe_spawn()
    player = Player(px, py)
    player.player_name = player_name
    zone = game_map.get_zone_at(px, py)
    if use_hw:
        player.log.append(f"Hardware entropy seed: {seed} | Zone {hw_zone} (syzygy {9-hw_zone})")
    if zone is not None:
        player.zone = zone
        player.visited_zones.add(zone)
    game_map.update_explored(px, py)  # Reveal starting area
    game_map.update_visible(px, py, player.zone, player.hyperstition)
    
    # Activate conducts from env var (comma-separated: "surge,syzygy")
    conduct_env = os.environ.get("NUMOGRAM_CONDUCTS", "")
    if conduct_env:
        for cid in conduct_env.split(","):
            cid = cid.strip()
            if cid in CONDUCTS:
                player.conduct_activate(cid)
    
    print(f"=== NUMOGRAM: ABYSSAL CRAWLER (HEADLESS) ===", file=sys.stderr)
    print(f"Run #{cult['runs']} | Player: {player_name} | Seed: {seed}", file=sys.stderr)
    print(f"Starting zone: {player.zone} ({ZONE_DATA.get(player.zone, {}).get('name', '?')})", file=sys.stderr)
    print(f"Commands: w/a/s/d=move f=attack g=cryptolith x1-5=abilities p=state v=aq q=quit", file=sys.stderr)
    print(f"Reading moves from stdin...", file=sys.stderr)
    
    # Start demo recording
    demo.start(player_name)
    print(f"[DEMO] Recording to {demo.filename}", file=sys.stderr)
    
    # Write initial state
    state = _dump_state(player, game_map, demons := [])
    with open("/tmp/numogame_state.txt", "w") as f:
        f.write(state)
    
    diagonals = {
        'y': (-1, -1), 'u': (1, -1),
        'b': (-1, 1),  'n': (1, 1),
        '7': (-1, -1), '9': (1, -1),
        '1': (-1, 1),  '3': (1, 1),
    }
    
    # Main loop — read moves from stdin
    try:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            
            # Process each character as a move
            skip_next = False
            for ci, ch in enumerate(line):
                if skip_next:
                    skip_next = False
                    continue
                key = ch.lower()
                demo.record_key(player.turn, key)
                
                if key == 'q':
                    print(f"QUIT | T:{player.turn} HP:{player.hp} Hyp:{player.hyperstition:.0f}% Slain:{player.demons_slain}", file=sys.stderr)
                    demo.stop()
                    _save_cult_headless(cult, player, game_map, demons)
                    return
                
                if key == 'p':
                    state = _dump_state(player, game_map, demons)
                    with open("/tmp/numogame_state.txt", "w") as f:
                        f.write(state)
                    print(f"[STATE] Dumped", file=sys.stderr)
                    player.turn += 1
                    continue
                
                if key == 'v':
                    state = _dump_state(player, game_map, demons)
                    with open("/tmp/numogame_state.txt", "w") as f:
                        f.write(state)
                    zdata = ZONE_DATA.get(player.zone, {})
                    aq = aq_value(zdata.get('name', ''))
                    print(f"AQ: {zdata.get('name','?')} = {aq} -> Zone {digital_root(aq)}", file=sys.stderr)
                    player.turn += 1
                    continue
                
                if key == 'i':
                    zdata = ZONE_DATA.get(player.zone, {})
                    print(f"Zone {player.zone}: {zdata.get('name','?')} | HP:{player.hp} Hyp:{player.hyperstition:.0f}% T:{player.turn} Slain:{player.demons_slain}", file=sys.stderr)
                    continue
                
                # Movement
                dx, dy = 0, 0
                if key == 'w': dy = -1
                elif key == 's': dy = 1
                elif key == 'a': dx = -1
                elif key == 'd': dx = 1
                elif key in diagonals:
                    dx, dy = diagonals[key]
                elif key == 'f' or key == ' ':
                    # Attack adjacent
                    attacked = False
                    for d in demons:
                        if d.alive and max(abs(d.x - player.x), abs(d.y - player.y)) == 1:
                            player.attack(d)
                            attacked = True
                            break
                    if not attacked:
                        player.log.append("No adjacent demon to attack.")
                    player.turn += 1
                    _tick_headless(player, game_map, demons)
                    continue
                elif key == 'g':
                    if player.cryptolith_clicks >= 3 and not player.has_cryptolith:
                        player.has_cryptolith = True
                        player.speed = max(1, player.speed - 1)
                        player.hyperstition = min(100, player.hyperstition + 20)
                        player.log.append("You grasp the Cryptolith. TICK. TICK. TICK.")
                        print(f"CRYPTOLITH GRASPED | Hyp:{player.hyperstition:.0f}% Speed:{player.speed}", file=sys.stderr)
                    player.turn += 1
                    continue
                elif key == 'x':
                    # Anchor return — if anchor is set and no digit follows, snap back
                    remaining = line[ci + 1:]
                    has_digit = any(rch.isdigit() and 1 <= int(rch) <= 5 for rch in remaining)
                    if player.anchor_pos and not has_digit:
                        ax, ay = player.anchor_pos
                        if game_map.is_passable(ax, ay):
                            player.x, player.y = ax, ay
                            player.anchor_pos = None
                            player.log.append("You snap back to your anchor point.")
                            game_map.update_explored(player.x, player.y)
                            game_map.update_visible(player.x, player.y, player.zone, player.hyperstition)
                            print("ANCHOR RETURN", file=sys.stderr)
                        else:
                            player.log.append("Anchor point is blocked. The structure shifted.")
                            player.anchor_pos = None
                        player.turn += 1
                        continue
                    
                    # Ability activation — next char in line is the choice
                    remaining = line[ci + 1:]
                    choice = None
                    for rch in remaining:
                        if rch.isdigit() and 1 <= int(rch) <= 5:
                            choice = int(rch)
                            break
                    if choice is not None:
                        available = get_available_abilities(player)
                        if 0 <= choice - 1 < len(available):
                            ability_key, ability_data = available[choice - 1]
                            success = use_ability(player, ability_key, game_map, demons)
                            if success:
                                print(f"ABILITY: {ability_data['name']} | Hyp:{player.hyperstition:.0f}%", file=sys.stderr)
                                skip_next = True  # skip the digit
                            else:
                                player.log.append(f"Cannot afford {ability_data['name']}.")
                        else:
                            player.log.append("No affordable abilities.")
                    else:
                        player.log.append("[ABILITIES] Use x1-x5 to activate.")
                    player.turn += 1
                    continue
                else:
                    continue  # Unknown key, skip
                
                # Execute movement
                if dx != 0 or dy != 0:
                    player.move(dx, dy, game_map, demons)
                    _tick_headless(player, game_map, demons)
                    
                    # FLOOR TRANSITION
                    if player.descending:
                        player.descending = False
                        new_seed = seed + player.floor * 1000
                        game_map = DungeonMap(78, 22, seed=new_seed,
                                             hyperstition=int(player.hyperstition),
                                             floor=player.floor)
                        px, py = game_map.safe_spawn()
                        player.x, player.y = px, py
                        game_map.update_explored(px, py)
                        game_map.update_visible(px, py, player.zone, player.hyperstition)
                        demons.clear()
                        floor_zone = (player.floor - 1) % 10
                        print(f"FLOOR {player.floor} | Zone {floor_zone}: {ZONE_DATA.get(floor_zone, {}).get('name', '?')}", file=sys.stderr)
                
                # Check death
                if player.dead:
                    print(f"DEAD | {player.death_msg} | T:{player.turn} HP:0 Hyp:{player.hyperstition:.0f}% Slain:{player.demons_slain}", file=sys.stderr)
                    demo.stop()
                    _save_cult_headless(cult, player, game_map, demons)
                    return
                
                # Status line to stdout for monitoring
                zdata = ZONE_DATA.get(player.zone, {})
                conduct_chars = ""
                if player.active_conducts:
                    chars = []
                    for c in sorted(player.active_conducts):
                        ch = CONDUCTS.get(c, {}).get("hud_char", "?")
                        chars.append(f"~{ch}" if c in player.conduct_violated else ch)
                    conduct_chars = f" [{' '.join(chars)}]"
                floor_name = getattr(game_map, 'floor_name', '')[:8]
                print(f"[T:{player.turn}] F{player.floor}:{floor_name} Z{player.zone}:{zdata.get('name','?')[:8]} HP:{player.hp} Hyp:{player.hyperstition:.0f}% Slain:{player.demons_slain} Gates:{len(player.gates_opened)}{conduct_chars}", file=sys.stderr)
    
    except (EOFError, KeyboardInterrupt):
        print(f"INTERRUPT | T:{player.turn} HP:{player.hp} Hyp:{player.hyperstition:.0f}%", file=sys.stderr)
        demo.stop()
    
    # Save on any exit (EOF, interrupt, or loop end)
    if not player.dead:
        print(f"EOF | T:{player.turn} HP:{player.hp} Hyp:{player.hyperstition:.0f}%", file=sys.stderr)
        demo.stop()
    _save_cult_headless(cult, player, game_map, demons)

def _tick_headless(player, game_map, demons):
    """Process one game tick in headless mode."""
    import random
    
    # CORRUPTION EFFECTS
    hyp = player.hyperstition
    
    # 50%+: structure corrodes you (1 HP per 20 turns)
    if hyp >= 50 and player.turn % 20 == 0:
        player.hp -= 1
        if player.turn % 40 == 0:
            player.log.append("The structure corrodes. You feel it in your bones.")
    
    # Demon aggression: extra movement at 70%+
    demon_extra_move = hyp >= 70
    
    # Spawn demons
    if should_spawn(player.hyperstition, player.turn, random) and not getattr(game_map, 'floor_config', {}).get('no_demons', False):
        data = spawn_demon(player.zone, player.hyperstition, random)
        if data:
            # Find valid spawn position
            for _ in range(20):
                sx = player.x + random.randint(-6, 6)
                sy = player.y + random.randint(-6, 6)
                if game_map.is_passable(sx, sy) and (sx, sy) != (player.x, player.y):
                    demons.append(Demon(data, sx, sy))
                    demon = demons[-1]
                    # Direction
                    dx = demon.x - player.x
                    dy = demon.y - player.y
                    dirs = []
                    if dy < 0: dirs.append("north")
                    if dy > 0: dirs.append("south")
                    if dx > 0: dirs.append("east")
                    if dx < 0: dirs.append("west")
                    direction = "-".join(dirs) if dirs else "here"
                    player.log.append(f"Mesh-{demon.mesh}: {demon.name} ({demon.epithet}) manifests to the {direction}!")
                    break
    
    # Move demons
    for d in demons:
        if d.alive:
            d.try_move(player, game_map)
            if demon_extra_move and d.alive:
                d.try_move(player, game_map)  # Extra move at 70%+ hyp
            if d.x == player.x and d.y == player.y and d.alive:
                rdmg = d.dmg + random.randint(-2, 2)
                player.hp -= rdmg
                player.log.append(f"{d.name} attacks! {rdmg} damage. [HP: {player.hp}]")
                if player.hp <= 0:
                    player.hp = 0
                    player.dead = True
                    player.death_msg = random.choice(DEATH_MESSAGES)
    
    # Clean dead demons
    demons[:] = [d for d in demons if d.alive]

def _save_cult_headless(cult, player, game_map, demons):
    """Save cult data at end of headless run."""
    cult["max_hyperstition"] = max(cult["max_hyperstition"], int(player.hyperstition))
    cult["total_turns"] += player.turn
    cult["total_demons_slain"] += player.demons_slain
    for z in player.visited_zones:
        if z not in cult["zones_ever_visited"]:
            cult["zones_ever_visited"].append(z)
    for g in player.gates_opened:
        if g not in cult["gates_ever_opened"]:
            cult["gates_ever_opened"].append(g)
    if player.schizo_lucid:
        cult["schizo_achieved"] = True
    # Conduct tracking
    for cid in player.active_conducts:
        if cid not in cult.get("conduct_attempts", {}):
            cult.setdefault("conduct_attempts", {})[cid] = 0
        cult["conduct_attempts"][cid] += 1
        if cid not in player.conduct_violated:
            if cid not in cult.get("conducts_completed", []):
                cult.setdefault("conducts_completed", []).append(cid)
    player_name = getattr(player, 'player_name', 'crawler')
    conduct_str = ""
    if player.active_conducts:
        active = [CONDUCTS[c]["hud_char"] for c in sorted(player.active_conducts) if c not in player.conduct_violated]
        broken = [f"~{CONDUCTS[c]['hud_char']}" for c in sorted(player.active_conducts) if c in player.conduct_violated]
        conduct_str = f" [{' '.join(active + broken)}]"
    mem = f"Run #{cult['runs']}: {player_name}, Turn {player.turn}, Hyp {player.hyperstition:.0f}%, " \
          f"Zones {sorted(player.visited_zones)}, Slain {player.demons_slain}{conduct_str}"
    cult["cult_memory"].append(mem)
    if len(cult["cult_memory"]) > 20:
        overflowed = cult["cult_memory"][0]
        _process_overflow(overflowed, cult)
        cult["cult_memory"] = cult["cult_memory"][-20:]
    cult["cult_zone"] = _cult_zone(cult)
    _check_cult_integrity(cult)
    save_cult(cult)
    print(f"SAVED | {mem}", file=sys.stderr)


if __name__ == "__main__":
    import sys
    if "--headless" in sys.argv:
        main_headless()
    elif "--help" in sys.argv:
        print("Usage: python3 numogram_roguelike.py [--headless] [--hw-entropy]")
        print("  --headless    Run without curses (for AI agents)")
        print("  --hw-entropy  Seed from hardware entropy (thermal, GPU, timing jitter)")
    else:
        curses.wrapper(main)
