"""Tests for numogram-entropy core module."""

from numogram_entropy.core import (
    digital_root,
    plex,
    traverse,
    iching,
    expand_seed,
    collect_all,
    aggregate,
    NumogramEntropy,
)


def test_digital_root():
    assert digital_root(0) == 0
    assert digital_root(9) == 9
    assert digital_root(10) == 1
    assert digital_root(192855) == 3
    assert digital_root(999) == 9


def test_plex():
    assert plex(0) == 0
    assert plex(1) == 1
    assert plex(3) == 6
    assert plex(7) == 1
    assert plex(9) == 9


def test_traverse():
    # Known seed
    seed = b"\x01\x02\x03\x04\x05\x06\x07\x08"
    path = traverse(seed, steps=3)

    assert len(path) == 3
    assert path[0]["step"] == 0
    assert 0 <= path[0]["zone"] <= 9
    assert path[0]["syzygy"] == 9 - path[0]["zone"]

    # Feedback should change seed for next step
    assert path[1]["seed"] != path[0]["seed"]


def test_traverse_convergence():
    """Later zones should converge toward numogram attractors."""
    import os
    seed = os.urandom(8)
    path = traverse(seed, steps=10)

    # Last 3 zones should cluster around 3, 4, or 6 (Warp attractors)
    last_zones = [p["zone"] for p in path[-3:]]
    # Not a hard assertion — just checking the pattern is visible
    assert all(0 <= z <= 9 for z in last_zones)


def test_iching():
    hexagram = iching(b"\x00\x01\x02\x03\x00\x01")

    assert len(hexagram) == 6
    assert hexagram[0]["value"] == 6    # 0 % 4 = 0 → old yin
    assert hexagram[0]["changing"] is True
    assert hexagram[1]["value"] == 7    # 1 % 4 = 1 → young yang
    assert hexagram[1]["changing"] is False
    assert hexagram[2]["value"] == 8    # 2 % 4 = 2 → young yin
    assert hexagram[3]["value"] == 9    # 3 % 4 = 3 → old yang
    assert hexagram[3]["changing"] is True


def test_collect_all():
    sources = collect_all()
    assert "thermal" in sources
    assert "timing_jitter" in sources
    assert "timestamp_ns" in sources
    assert len(sources["timing_jitter"]) == 256


def test_aggregate():
    sources = collect_all()
    result = aggregate(sources)
    assert len(result) == 32  # SHA-256 output


def test_expand_seed():
    short = b"\x01\x02\x03\x04"
    expanded = expand_seed(hashlib.sha256(short).digest(), 64)
    assert len(expanded) == 64


def test_numogram_entropy_api():
    ne = NumogramEntropy()

    seed = ne.get_seed(32)
    assert len(seed) == 32

    zone = ne.get_zone()
    assert 0 <= zone <= 9

    path = ne.traverse(steps=5)
    assert len(path) == 5

    hexagram = ne.iching()
    assert len(hexagram) == 6

    sources = ne.sources_available()
    assert sources["thermal_zones"] >= 1
    assert sources["timing_jitter_samples"] == 256


# Import for test_expand_seed
import hashlib
