"""
Zone‑constrained composition extension for mod‑writer.

This module provides the ZoneComposer wrapper and utility functions to
bias ModComposer generation toward a specific numogram zone (1‑9).
It loads per‑zone centroid statistics from the synthetic 900‑track
corpus and applies probabilistic adjustments to note/octave, waveform
selection, gate families, and BPM ranges.

Installation: import and wrap your ModComposer instance:
    from hermes.skills.numogram_audio.mod_writer_composer.composer_extension import ZoneComposer
    base = ModComposer()
    zc = ZoneComposer(base)
    zc.target_zone(zone=2, brightness="warm")
    zc.add_section(length=32, channel=0)

Alternatively, call patch_mod_composer() to inject .target_zone() and
.add_section() directly onto ModComposer (monkey‑patch).
"""

from __future__ import annotations
from typing import Dict, Tuple, Optional, List
import json
import os
import random

# ── Zone centroid storage ────────────────────────────────────────────────────

CENTROID_PATH = os.path.expanduser('~/numogram/mod_writer_artifacts/zone_centroids.json')

# Fallback defaults — gentle hand‑tuned approximations if centroid file missing.
# Keys are int zone (1‑9). centroid in Hz, bpm as (min, max), density ∈[0,1],
# waveform preference: "square", "triangle", "noise", or "adaptive".
ZONE_DEFAULTS = {
    1: {"centroid": 400,  "bpm": (90, 110),  "density": 0.25, "waveform": "square"},
    2: {"centroid": 1350, "bpm": (110, 140), "density": 0.30, "waveform": "triangle"},
    3: {"centroid": 2200, "bpm": (140, 170), "density": 0.35, "waveform": "square"},
    4: {"centroid": 3200, "bpm": (100, 130), "density": 0.40, "waveform": "triangle"},
    5: {"centroid": 4100, "bpm": (80, 110),  "density": 0.20, "waveform": "square"},
    6: {"centroid": 5000, "bpm": (160, 190), "density": 0.45, "waveform": "triangle"},
    7: {"centroid": 5900, "bpm": (130, 160), "density": 0.35, "waveform": "noise"},
    8: {"centroid": 6800, "bpm": (170, 200), "density": 0.50, "waveform": "square"},
    9: {"centroid": 7500, "bpm": (90, 120),  "density": 0.25, "waveform": "triangle"},
}

# Gate family buckets (gate value ranges)
GATE_FAMILY_RANGES = {
    "arpeggio": range(0, 5),          # gates 0‑4 (arity pattern indices)
    "slide":    range(10, 20),        # porta‑up speed
    "volume":   range(20, 30),        # volume level 0‑9
    "syzygy":   [30, 31, 32, 33, 34, 35, 36],  # special / symbolic
    "other":   list(range(5, 10)) + list(range(19, 20)) + list(range(29, 30)),  # leftovers
}

WAVEFORM_TO_CURRENT = {
    "square":   'A',   # ModWriter sample index 1 (square)
    "triangle": 'B',   # sample index 2 (triangle)
    "noise":    'C',   # sample index 3 (noise)
    "adaptive": None,  # resolved per-zone default below
}

# Zone → preferred waveform when adaptive (mirrors note brightness intuition)
ZONE_WAVEFORM_DEFAULT = {
    1: 'square', 2: 'triangle', 3: 'square', 4: 'triangle',
    5: 'square', 6: 'triangle', 7: 'noise', 8: 'square', 9: 'triangle',
}


def _load_centroids() -> Dict[int, Dict]:
    """Load pre‑computed zone statistics; fall back to ZONE_DEFAULTS."""
    if os.path.exists(CENTROID_PATH):
        try:
            with open(CENTROID_PATH) as f:
                data = json.load(f)
            # Ensure keys are ints
            return {int(k): v for k, v in data.items()}
        except Exception:
            pass
    return ZONE_DEFAULTS


class ZoneComposer:
    """
    Wrapper around ModComposer that adds zone‑targeted generation.
    All zone‑biasing happens here; the wrapped composer is untouched.
    """

    def __init__(self, composer):
        self.composer = composer
        self._zone_target: Optional[int] = None
        self._params: Dict = {}
        self._centroids = _load_centroids()

    # ── Public API ────────────────────────────────────────────────────────────

    def target_zone(
        self,
        zone: int,
        brightness: Optional[str] = None,
        density: Optional[float] = None,
        gate_bias: Optional[str] = None,
        bpm_range: Optional[Tuple[int, int]] = None,
        waveform: Optional[str] = None,
        aq_seed: Optional[str] = None,
        duplicate_order: bool = True,
    ) -> None:
        """Set zone‑target parameters for subsequent section generation.

        Args:
            aq_seed: When provided, gate selection for sections will be derived
                     deterministically from this AQ string (SHA1‑mod‑37), matching
                     the Phase 4 synthetic corpus generation strategy. If None,
                     gates are sampled uniformly at random per section.
            duplicate_order: If True (default), when the module is written the
                     pattern order list will contain the pattern index twice,
                     mirroring the original SongBuilder bug that doubled the
                     effective track length (corpus tracks were 2× pattern rows).
                     This aligns duration and BPM features with the corpus.
        """
        if zone not in range(1, 10):
            raise ValueError("zone must be 1‑9")

        base = self._centroids.get(zone, ZONE_DEFAULTS[zone]).copy()

        # Resolve brightness → centroid multiplier
        factor = {"dark": 0.7, "warm": 1.0, "bright": 1.5}.get(brightness, 1.0)
        centroid_target = base["centroid"] * factor

        # Gate bias — map to weighting dict
        gate_weights = self._gate_distribution(
            bias=gate_bias or "none",
            length_estimate=64,   # placeholder; actual length known in add_section
        )

        # Waveform resolution
        if waveform == "adaptive":
            waveform = ZONE_WAVEFORM_DEFAULT.get(zone, "square")

        self._zone_target = zone
        # Align with Phase 4 synthetic corpus generation defaults:
        # - square waveform (current='A')
        # - full density (every row gets a note)
        # - single gate per section (handled in add_section)
        self._params = {
            "zone": zone,
            "centroid_target": centroid_target,
            "bpm_range": bpm_range or base.get("bpm", (80, 160)),
            "density": 1.0,  # dataset tracks are continuous, no rests
            "waveform": waveform or "square",  # dataset used square wave (current A)
            "gate_bias": gate_bias or "none",  # retained for API but unused in single-gate mode
            "gate_weights": gate_weights,       # retained but unused
            "aq_seed": aq_seed,                 # optional seed for deterministic gate selection
        }
        # Zone 1 requires contiguous patterns; other zones may duplicate
        if zone == 1:
            self._duplicate_order = False
        else:
            self._duplicate_order = duplicate_order

    def add_section(self, length: int, channel: int = 0, **overrides) -> None:
        """
        Generate `length` rows of notes on `channel` using current zone
        parameters. Overrides temporarily replace target_zone settings.

        Gate strategy:
          * If an aq_seed was supplied to target_zone(), the gate value is
            derived deterministically from that AQ (SHA1 mod 37), matching the
            Phase 4 corpus where each track had one fixed gate tied to its AQ.
          * Otherwise a single gate is sampled uniformly from 0‑36 for this
            section (corpus‑aligned behaviour for creative use without a seed).
        """
        if self._zone_target is None:
            raise RuntimeError("Call .target_zone() before .add_section()")

        zone = self._zone_target
        params = {**self._params, **overrides}

        density = params["density"]
        waveform = params["waveform"]
        aq_seed = params.get("aq_seed")

        # Resolve current (channel instrument) from waveform
        current_char = WAVEFORM_TO_CURRENT.get(waveform, 'A')

        # Determine single gate for the whole section
        if aq_seed is not None:
            gate = self._gate_from_aq(aq_seed)
        else:
            gate = random.randint(0, 36)

        # For each row, probabilistically add a note
        for row in range(length):
            if random.random() > density:
                continue  # rest

            # Zone → note mapping from mod‑writer's mapping module
            try:
                from hermes.skills.numogram_audio.mod_writer.mapping import note_and_octave_from_zone
            except ImportError:
                from mod_writer.mapping import note_and_octave_from_zone
            note, octave = note_and_octave_from_zone(zone)

            # Add note to wrapped composer
            self.composer.add_note(
                zone=zone,
                gate=gate,
                current=current_char,
                row=row,
                channel=channel,
            )

    def _gate_from_aq(self, aq_str: str) -> int:
        """Derive a deterministic gate integer (0‑36) from an AQ string.

        Mirrors ``ModComposer.constrain_gates_by_aq``: compute SHA1, take
        the first 8 hex digits as an integer, then modulo 37. This matches
        the Phase 4 corpus generation exactly (gate = AQ mod 37; no overrides).
        """
        import hashlib
        h = hashlib.sha1(aq_str.encode()).hexdigest()
        return int(h[:8], 16) % 37

    def _gate_distribution(self, bias: str, length_estimate: int) -> Dict[int, int]:
        """
        Produce a gate → count dict that totals ~ length_estimate * density.
        For now: simple uniform across all gate values (0‑36), no bias.
        Phase 5 expansion will inflate one family based on bias.
        """
        total_gates = max(1, int(length_estimate * 0.5))
        # Uniform across all 37 gates
        per_gate = total_gates // 37
        remainder = total_gates % 37
        distrib = {g: per_gate for g in range(37)}
        for g in range(remainder):
            distrib[g] += 1
        return distrib

    def _weighted_gate_choice(self, weights: Dict[int, int]) -> int:
        """Sample a gate integer (0‑36) from the provided weight dict."""
        total = sum(weights.values())
        if total == 0:
            return random.randint(0, 36)
        r = random.uniform(0, total)
        cum = 0.0
        for gate, w in weights.items():
            cum += w
            if r <= cum:
                return gate
        return 36  # fallback

# ── Monkey‑patch convenience ─────────────────────────────────────────────────


def patch_mod_composer():
    """
    Inject .target_zone(), .add_section() and patched .write_mod() onto ModComposer.
    The patched write_mod() duplicates the pattern order when _duplicate_order is True,
    matching the corpus generation's double‑length tracks.
    Safe to call multiple times (idempotent).
    """
    try:
        from hermes.skills.numogram_audio.mod_writer.composer import ModComposer
    except ImportError:
        from mod_writer.composer import ModComposer
    if hasattr(ModComposer, "_zone_patched") and ModComposer._zone_patched:
        return

    def target_zone(self, *args, **kwargs):
        wrapper = ZoneComposer(self)
        wrapper.target_zone(*args, **kwargs)
        self._zone_composer = wrapper

    def add_section(self, *args, **kwargs):
        if not hasattr(self, "_zone_composer") or self._zone_composer is None:
            raise RuntimeError("Call .target_zone() before .add_section()")
        self._zone_composer.add_section(*args, **kwargs)

    def write_mod(self, filename: str):
        # Replicate original ModComposer.write_mod but with optional order duplication.
        self._ensure_samples()
        length = self._compute_max_row()
        if length == 0:
            raise ValueError("composer is empty — add_note() before write_mod()")
        triangular = getattr(self, '_triangular', False)
        pat = self.build_patterns_from_grid(length=length, triangular=triangular)
        self.writer.add_pattern(pat)
        # Duplicate the order if ZoneComposer requested it (corpus had double entries)
        if hasattr(self, "_zone_composer") and getattr(self._zone_composer, "_duplicate_order", False):
            if self.writer.orders:
                self.writer.orders.append(self.writer.orders[-1])
        self.writer.write(filename)
        return filename

    ModComposer.target_zone = target_zone  # type: ignore
    ModComposer.add_section  = add_section   # type: ignore
    ModComposer.write_mod    = write_mod     # type: ignore
    ModComposer._zone_patched = True
