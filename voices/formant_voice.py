#!/usr/bin/env python3
"""
Numogram Formant Voice — Plaits/Braids-style speech synthesis
Direct control over formant frequencies, phoneme space, and voice character.
No TTS dependency — pure synthesis from phoneme parameters.

Usage: python3 formant_voice.py --zone 3
       python3 formant_voice.py --vowel a --f1 700 --f2 1200
       python3 formant_voice.py --phoneme-sequence "z-o-n-e-t-h-r-e-e"
       python3 formant_voice.py --sweep 3  (sweeps through vowels in Zone 3's character)
"""

import numpy as np
from scipy import signal as sig
from scipy.io import wavfile
import os
import sys

SAMPLE_RATE = 44100
OUTDIR = os.path.expanduser("~/numogram-voices")
os.makedirs(OUTDIR, exist_ok=True)


# ─── PHONEME DATABASE ───
# Formant frequencies (Hz) for vowels and consonants
# Based on classic Peterson & Barney (1952) + Praat defaults
# F1 = openness, F2 = frontness, F3 = lip rounding

PHONEMES = {
    # Vowels
    "a":  {"f1": 730, "f2": 1090, "f3": 2440, "type": "vowel", "voiced": True},
    "e":  {"f1": 530, "f2": 1840, "f3": 2480, "type": "vowel", "voiced": True},
    "i":  {"f1": 270, "f2": 2300, "f3": 3000, "type": "vowel", "voiced": True},
    "o":  {"f1": 570, "f2": 840,  "f3": 2410, "type": "vowel", "voiced": True},
    "u":  {"f1": 300, "f2": 870,  "f3": 2240, "type": "vowel", "voiced": True},
    "ae": {"f1": 660, "f2": 1720, "f3": 2410, "type": "vowel", "voiced": True},  # cat
    "er": {"f1": 490, "f2": 1350, "f3": 1690, "type": "vowel", "voiced": True},  # bird
    "uh": {"f1": 530, "f2": 1200, "f3": 2440, "type": "vowel", "voiced": True},  # cup
    
    # Semivowels / nasals
    "m":  {"f1": 250, "f2": 1000, "f3": 2200, "type": "nasal",  "voiced": True},
    "n":  {"f1": 250, "f2": 1500, "f3": 2500, "type": "nasal",  "voiced": True},
    "ng": {"f1": 250, "f2": 1800, "f3": 2500, "type": "nasal",  "voiced": True},
    "l":  {"f1": 400, "f2": 1200, "f3": 2500, "type": "liquid", "voiced": True},
    "r":  {"f1": 400, "f2": 1300, "f3": 1700, "type": "liquid", "voiced": True},
    
    # Fricatives (noise-based, formants less defined)
    "z":  {"f1": 300, "f2": 2000, "f3": 5000, "type": "fricative", "voiced": True,  "noise_bw": 3000},
    "s":  {"f1": 300, "f2": 2000, "f3": 5500, "type": "fricative", "voiced": False, "noise_bw": 4000},
    "sh": {"f1": 300, "f2": 1800, "f3": 3500, "type": "fricative", "voiced": False, "noise_bw": 2000},
    "f":  {"f1": 300, "f2": 1500, "f3": 5000, "type": "fricative", "voiced": False, "noise_bw": 3500},
    "v":  {"f1": 300, "f2": 1500, "f3": 5000, "type": "fricative", "voiced": True,  "noise_bw": 3500},
    "th": {"f1": 300, "f2": 1800, "f3": 4500, "type": "fricative", "voiced": False, "noise_bw": 3000},
    "h":  {"f1": 400, "f2": 1500, "f3": 3000, "type": "fricative", "voiced": False, "noise_bw": 2500},
    
    # Plosives
    "p":  {"f1": 200, "f2": 800,  "f3": 2500, "type": "plosive", "voiced": False},
    "b":  {"f1": 200, "f2": 800,  "f3": 2500, "type": "plosive", "voiced": True},
    "t":  {"f1": 200, "f2": 1700, "f3": 2600, "type": "plosive", "voiced": False},
    "d":  {"f1": 200, "f2": 1700, "f3": 2600, "type": "plosive", "voiced": True},
    "k":  {"f1": 200, "f2": 1800, "f3": 2800, "type": "plosive", "voiced": False},
    "g":  {"f1": 200, "f2": 1800, "f3": 2800, "type": "plosive", "voiced": True},
    
    # Glottal
    "?":  {"f1": 100, "f2": 200,  "f3": 300,  "type": "glottal", "voiced": False},  # glottal stop
}


# ─── ZONE VOICE PROFILES ───
# Each zone has a character: base pitch, formant scaling, phoneme sequence

ZONE_VOICES = {
    0: {
        "name": "eiaoung",
        "pitch": 140,
        "formant_scale": 0.8,
        "breathiness": 0.4,
        "phonemes": ["ng", "uh", "e", "a", "o", "ng"],
        "durations": [0.8, 0.5, 0.4, 0.4, 0.4, 1.0],
        "desc": "Silent whisper — nasal, open, trailing off"
    },
    1: {
        "name": "gl",
        "pitch": 180,
        "formant_scale": 1.0,
        "breathiness": 0.1,
        "phonemes": ["g", "l", "uh"],
        "durations": [0.05, 0.15, 0.3],
        "desc": "Glottal spasm — hard onset, liquid release"
    },
    2: {
        "name": "dt",
        "pitch": 250,
        "formant_scale": 1.0,
        "breathiness": 0.15,
        "phonemes": ["d", "?", "t", "uh", "t"],
        "durations": [0.03, 0.02, 0.03, 0.1, 0.03],
        "desc": "Stuttering — repeated plosives, fractured"
    },
    3: {
        "name": "zx",
        "pitch": 200,
        "formant_scale": 1.2,
        "breathiness": 0.05,
        "phonemes": ["z", "sh", "z", "sh", "z"],
        "durations": [0.3, 0.2, 0.3, 0.2, 0.5],
        "desc": "Buzz-cutter — sustained fricatives, hissing"
    },
    4: {
        "name": "skr",
        "pitch": 120,
        "formant_scale": 1.1,
        "breathiness": 0.05,
        "phonemes": ["s", "k", "r", "ae"],
        "durations": [0.1, 0.05, 0.2, 0.4],
        "desc": "Growl — low, aggressive, open vowel"
    },
    5: {
        "name": "ktt",
        "pitch": 300,
        "formant_scale": 1.0,
        "breathiness": 0.0,
        "phonemes": ["k", "?", "t", "th", "t"],
        "durations": [0.02, 0.01, 0.02, 0.05, 0.02],
        "desc": "Hiss — fast, percussive, spittle-like"
    },
    6: {
        "name": "tch",
        "pitch": 180,
        "formant_scale": 0.9,
        "breathiness": 0.2,
        "phonemes": ["t", "sh", "uh", "t", "sh"],
        "durations": [0.05, 0.15, 0.1, 0.05, 0.2],
        "desc": "Static — chewing, friction"
    },
    7: {
        "name": "pb",
        "pitch": 160,
        "formant_scale": 0.85,
        "breathiness": 0.5,
        "phonemes": ["p", "b", "ae", "h"],
        "durations": [0.08, 0.08, 0.3, 0.4],
        "desc": "Sigh — breathy, lips flapping"
    },
    8: {
        "name": "mnm",
        "pitch": 150,
        "formant_scale": 0.9,
        "breathiness": 0.3,
        "phonemes": ["m", "n", "o", "m"],
        "durations": [0.3, 0.2, 0.5, 0.4],
        "desc": "Moan — nasal, warm, sustained"
    },
    9: {
        "name": "tn",
        "pitch": 90,
        "formant_scale": 1.0,
        "breathiness": 0.15,
        "phonemes": ["t", "n", "uh"],
        "durations": [0.03, 0.1, 0.3],
        "desc": "Grunt — low, percussive, guttural"
    },
}


# ─── SYNTHESIS ENGINE ───

def formant_filter(audio, freq, bw, sr=SAMPLE_RATE):
    """Bandpass filter centered on formant frequency"""
    nyq = sr / 2
    low = max((freq - bw/2) / nyq, 0.001)
    high = min((freq + bw/2) / nyq, 0.999)
    if low >= high:
        return audio * 0.1
    b, a = sig.butter(2, [low, high], btype='band')
    return sig.filtfilt(b, a, audio)


def synthesize_vowel(duration, pitch, f1, f2, f3, breathiness=0.1, sr=SAMPLE_RATE):
    """Synthesize a vowel using formant synthesis (FOF-style)"""
    n = int(sr * duration)
    t = np.arange(n) / sr
    
    # Glottal pulse train (sawtooth approximation)
    glottal = sig.sawtooth(2 * np.pi * pitch * t, width=0.3)
    
    # Three formant filters in parallel
    bw1 = f1 * 0.15  # bandwidth ~15% of center freq
    bw2 = f2 * 0.12
    bw3 = f3 * 0.10
    
    formant1 = formant_filter(glottal, f1, bw1)
    formant2 = formant_filter(glottal, f2, bw2)
    formant3 = formant_filter(glottal, f3, bw3)
    
    # Combine formants (F1 loudest, F3 quietest)
    voiced = formant1 * 1.0 + formant2 * 0.6 + formant3 * 0.3
    
    # Add breathiness (noise through same formants)
    noise = np.random.uniform(-1, 1, n)
    breath = formant_filter(noise, f1, bw1 * 2) * 0.5
    breath += formant_filter(noise, f2, bw2 * 2) * 0.3
    
    output = voiced * (1 - breathiness) + breath * breathiness
    
    # Normalize
    mx = np.max(np.abs(output))
    if mx > 0:
        output /= mx
    
    return output


def synthesize_fricative(duration, freq, bw, voiced=True, noise_bw=3000, sr=SAMPLE_RATE):
    """Synthesize a fricative (z, s, sh, f, th, h)"""
    n = int(sr * duration)
    
    # Noise source
    noise = np.random.uniform(-1, 1, n)
    
    # Bandpass the noise
    nyq = sr / 2
    low = max((freq - noise_bw/2) / nyq, 0.001)
    high = min((freq + noise_bw/2) / nyq, 0.999)
    if low >= high:
        high = min(low + 0.1, 0.999)
    b, a = sig.butter(3, [low, high], btype='band')
    filtered = sig.filtfilt(b, a, noise)
    
    if voiced:
        # Add low-frequency voicing
        t = np.arange(n) / sr
        voice = sig.sawtooth(2 * np.pi * freq * 0.5 * t, width=0.4)
        voice_filt = formant_filter(voice, freq, bw)
        output = filtered * 0.7 + voice_filt * 0.3
    else:
        output = filtered
    
    mx = np.max(np.abs(output))
    if mx > 0:
        output /= mx
    return output


def synthesize_plosive(duration, pitch, f1, f2, voiced=False, sr=SAMPLE_RATE):
    """Synthesize a plosive (p, b, t, d, k, g)"""
    n = int(sr * duration)
    
    # Burst of noise
    burst_len = min(int(0.015 * sr), n)
    burst = np.random.uniform(-1, 1, burst_len)
    burst *= np.exp(-np.arange(burst_len) / (burst_len * 0.2))
    
    # Formant transitions (onset)
    if voiced:
        t = np.arange(burst_len) / sr
        voice = sig.sawtooth(2 * np.pi * pitch * t, width=0.3)
        voice_filt = formant_filter(voice, f1, f1 * 0.2) + formant_filter(voice, f2, f2 * 0.15)
        burst = burst * 0.5 + voice_filt[:burst_len] * 0.5
    
    output = np.zeros(n)
    output[:burst_len] = burst
    
    mx = np.max(np.abs(output))
    if mx > 0:
        output /= mx
    return output


def synthesize_nasal(duration, pitch, f1, f2, f3, sr=SAMPLE_RATE):
    """Synthesize a nasal (m, n, ng) — formants + antiformant"""
    n = int(sr * duration)
    t = np.arange(n) / sr
    
    glottal = sig.sawtooth(2 * np.pi * pitch * t, width=0.3)
    
    # Nasal formants (lower, more damped)
    f1_n = formant_filter(glottal, f1 * 0.8, f1 * 0.2)
    f2_n = formant_filter(glottal, f2 * 0.7, f2 * 0.15)
    
    output = f1_n * 1.0 + f2_n * 0.4
    
    mx = np.max(np.abs(output))
    if mx > 0:
        output /= mx
    return output


def synthesize_glottal(duration, sr=SAMPLE_RATE):
    """Glottal stop — sudden silence with onset burst"""
    n = int(sr * duration)
    burst = np.random.uniform(-1, 1, int(0.01 * sr))
    burst *= np.exp(-np.arange(len(burst)) / (len(burst) * 0.1))
    output = np.zeros(n)
    output[:len(burst)] = burst
    return output


def synthesize_phoneme(phoneme_name, duration, pitch, scale=1.0, breathiness=0.1):
    """Dispatch to appropriate synthesizer based on phoneme type"""
    if phoneme_name not in PHONEMES:
        return np.zeros(int(SAMPLE_RATE * duration))
    
    p = PHONEMES[phoneme_name]
    f1 = p["f1"] * scale
    f2 = p["f2"] * scale
    f3 = p["f3"] * scale
    
    if p["type"] == "vowel":
        return synthesize_vowel(duration, pitch, f1, f2, f3, breathiness)
    elif p["type"] == "fricative":
        return synthesize_fricative(duration, f2, f2 * 0.5, p["voiced"], p.get("noise_bw", 3000))
    elif p["type"] == "plosive":
        return synthesize_plosive(duration, pitch, f1, f2, p["voiced"])
    elif p["type"] == "nasal":
        return synthesize_nasal(duration, pitch, f1, f2, f3)
    elif p["type"] == "glottal":
        return synthesize_glottal(duration)
    elif p["type"] in ("liquid",):
        return synthesize_vowel(duration, pitch, f1, f2, f3, breathiness * 0.5)
    else:
        return np.zeros(int(SAMPLE_RATE * duration))


def synthesize_sequence(phonemes, durations, pitch, scale=1.0, breathiness=0.1):
    """Synthesize a sequence of phonemes with crossfading"""
    parts = []
    for ph, dur in zip(phonemes, durations):
        audio = synthesize_phoneme(ph, dur, pitch, scale, breathiness)
        
        # Short fade for each phoneme
        fade = min(int(0.01 * SAMPLE_RATE), len(audio) // 4)
        if fade > 0:
            audio[:fade] *= np.linspace(0, 1, fade)
            audio[-fade:] *= np.linspace(1, 0, fade)
        
        parts.append(audio)
    
    return np.concatenate(parts)


# ─── ZONE VOICE GENERATION ───

def generate_zone_voice(zone, speech_rate=1.0):
    """Generate the formant-synthesized voice for a zone"""
    v = ZONE_VOICES[zone]
    
    # Scale durations by speech rate
    durations = [d / speech_rate for d in v["durations"]]
    
    audio = synthesize_sequence(
        v["phonemes"],
        durations,
        v["pitch"],
        v["formant_scale"],
        v["breathiness"]
    )
    
    print(f"Zone {zone}: {v['name']} — {v['desc']}")
    print(f"  Phonemes: {' → '.join(v['phonemes'])}")
    print(f"  Pitch: {v['pitch']}Hz, Scale: {v['formant_scale']}, Breath: {v['breathiness']}")
    
    return audio


def generate_sweep(zone, num_vowels=6):
    """Sweep through vowel space for a zone — interesting for resonator feeding"""
    v = ZONE_VOICES[zone]
    vowels = ["a", "e", "i", "o", "u", "ae", "er", "uh"]
    selected = vowels[:num_vowels]
    
    parts = []
    for vowel in selected:
        ph = PHONEMES[vowel]
        audio = synthesize_vowel(
            0.5, v["pitch"],
            ph["f1"] * v["formant_scale"],
            ph["f2"] * v["formant_scale"],
            ph["f3"] * v["formant_scale"],
            v["breathiness"]
        )
        parts.append(audio)
    
    return np.concatenate(parts)


# ─── MAIN ───

def save_wav(audio, filename):
    mx = np.max(np.abs(audio))
    if mx > 0:
        audio = audio / mx * 0.85
    fade = int(0.03 * SAMPLE_RATE)
    audio[:fade] *= np.linspace(0, 1, fade)
    audio[-fade:] *= np.linspace(1, 0, fade)
    path = os.path.join(OUTDIR, filename)
    wavfile.write(path, SAMPLE_RATE, (audio * 32767).astype(np.int16))
    print(f"  → {path}")
    return path


if __name__ == "__main__":
    args = sys.argv[1:]
    
    if "--zone" in args:
        zone = int(args[args.index("--zone") + 1])
        audio = generate_zone_voice(zone)
        save_wav(audio, f"formant_z{zone}_{ZONE_VOICES[zone]['name']}.wav")
    
    elif "--zones" in args:
        idx = args.index("--zones")
        zones = [int(z) for z in args[idx+1:]]
        for z in zones:
            audio = generate_zone_voice(z)
            save_wav(audio, f"formant_z{z}_{ZONE_VOICES[z]['name']}.wav")
    
    elif "--sweep" in args:
        zone = int(args[args.index("--sweep") + 1])
        audio = generate_sweep(zone)
        save_wav(audio, f"formant_z{zone}_sweep.wav")
    
    elif "--all" in args:
        print("Generating formant voices for all zones...\n")
        for zone in range(10):
            audio = generate_zone_voice(zone)
            save_wav(audio, f"formant_z{zone}_{ZONE_VOICES[zone]['name']}.wav")
        
        print("\nGenerating vowel sweeps...\n")
        for zone in range(10):
            audio = generate_sweep(zone)
            save_wav(audio, f"formant_z{zone}_sweep.wav")
        
        print(f"\nDone. Files in {OUTDIR}")
    
    elif "--vowel" in args:
        vowel = args[args.index("--vowel") + 1]
        f1 = int(args[args.index("--f1") + 1]) if "--f1" in args else PHONEMES[vowel]["f1"]
        f2 = int(args[args.index("--f2") + 1]) if "--f2" in args else PHONEMES[vowel]["f2"]
        pitch = int(args[args.index("--pitch") + 1]) if "--pitch" in args else 150
        audio = synthesize_vowel(1.0, pitch, f1, f2, f2 * 1.5, 0.1)
        save_wav(audio, f"formant_{vowel}_f{f1}_{f2}.wav")
    
    else:
        print("Usage:")
        print("  python3 formant_voice.py --all")
        print("  python3 formant_voice.py --zone 3")
        print("  python3 formant_voice.py --zones 2 3 4")
        print("  python3 formant_voice.py --sweep 3")
        print("  python3 formant_voice.py --vowel a --f1 700 --f2 1200 --pitch 150")
