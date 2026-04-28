"""
Core module — hardware entropy collection + numogram traversal.

No external dependencies. Reads from /sys, /proc, and system clocks.
"""

import hashlib
import json
import os
import struct
import tempfile
import time
from pathlib import Path


# =====================================================================
# HARDWARE SOURCE COLLECTORS
# =====================================================================

def _read_sys(path: str) -> str:
    try:
        return Path(path).read_text().strip()
    except (OSError, PermissionError):
        return ""


def _thermal_zones() -> list[tuple[str, str]]:
    """Read all thermal zone temperatures from /sys/class/thermal."""
    zones = []
    base = Path("/sys/class/thermal")
    if base.exists():
        for tz in sorted(base.glob("thermal_zone*")):
            name = _read_sys(str(tz / "type"))
            temp = _read_sys(str(tz / "temp"))
            if name and temp:
                zones.append((name, temp))
    return zones


def _cpu_frequencies() -> list[str]:
    """Read per-core CPU frequencies from sysfs."""
    freqs = []
    for cpu in sorted(Path("/sys/devices/system/cpu").glob("cpu*")):
        f = _read_sys(str(cpu / "cpufreq" / "scaling_cur_freq"))
        if f:
            freqs.append(f)
    return freqs


def _proc_stat() -> dict[str, list[int]]:
    """Parse /proc/stat for CPU jiffies."""
    result = {}
    try:
        with open("/proc/stat") as f:
            for line in f:
                if line.startswith("cpu"):
                    parts = line.split()
                    result[parts[0]] = [int(x) for x in parts[1:]]
    except OSError:
        pass
    return result


def _read_file(path: str, max_bytes: int = 1024) -> str:
    """Read a proc/sys file, capped at max_bytes."""
    try:
        with open(path) as f:
            return f.read(max_bytes)
    except OSError:
        return ""


def _gpu_sensors() -> dict[str, str]:
    """Read NVIDIA GPU sensors via nvidia-smi."""
    import subprocess
    try:
        result = subprocess.run(
            ["nvidia-smi",
             "--query-gpu=temperature.gpu,clocks.current.sm,power.draw,"
             "clocks.current.memory,utilization.gpu,utilization.memory,fan.speed",
             "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=2,
        )
        if result.returncode == 0 and result.stdout.strip():
            parts = [p.strip() for p in result.stdout.strip().split(",")]
            keys = ["temp", "sm_clock", "power", "mem_clock",
                    "gpu_util", "mem_util", "fan"]
            return {k: parts[i] for i, k in enumerate(keys) if i < len(parts)}
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return {}


def _timing_jitter(n_samples: int = 256) -> list[int]:
    """
    Nanosecond timing jitter — the richest entropy source.
    Reflects cache misses, pipeline stalls, scheduler interrupts.
    """
    samples = []
    for _ in range(n_samples):
        t1 = time.perf_counter_ns()
        t2 = time.perf_counter_ns()
        samples.append(t2 - t1)
    return samples


def _fsync_timing(n_samples: int = 16) -> list[int]:
    """
    fsync() latency — forces data through the full storage stack.
    Entropy from NAND wear-leveling, journal commit, write-back cache.
    """
    samples = []
    try:
        for _ in range(n_samples):
            with tempfile.NamedTemporaryFile(delete=True) as f:
                f.write(b"\x00" * 4096)
                t1 = time.perf_counter_ns()
                os.fsync(f.fileno())
                t2 = time.perf_counter_ns()
                samples.append(t2 - t1)
    except OSError:
        pass
    return samples


# =====================================================================
# ENTROPY AGGREGATION
# =====================================================================

def collect_all() -> dict:
    """Collect raw data from all available hardware sources."""
    return {
        "thermal": _thermal_zones(),
        "cpu_freq": _cpu_frequencies(),
        "proc_stat": _proc_stat(),
        "proc_interrupts": _read_file("/proc/interrupts"),
        "diskstats": _read_file("/proc/diskstats"),
        "network": _read_file("/proc/net/dev"),
        "meminfo": _read_file("/proc/meminfo", 512),
        "vmstat": _read_file("/proc/vmstat", 1024),
        "sysctl_entropy": _read_file("/proc/sys/kernel/random/entropy_avail"),
        "gpu": _gpu_sensors(),
        "timing_jitter": _timing_jitter(256),
        "fsync_timing": _fsync_timing(16),
        "timestamp_ns": time.time_ns(),
    }


def aggregate(sources: dict) -> bytes:
    """Hash all sources into 32 bytes via SHA-256."""
    h = hashlib.sha256()

    for name, temp in sources.get("thermal", []):
        h.update(f"thermal:{name}:{temp}".encode())

    for i, freq in enumerate(sources.get("cpu_freq", [])):
        h.update(f"cpufreq:{i}:{freq}".encode())

    stat = sources.get("proc_stat", {})
    for key in sorted(stat.keys())[:4]:
        h.update(f"stat:{key}:{stat[key]}".encode())

    for field in ("proc_interrupts", "diskstats", "network", "meminfo", "vmstat"):
        val = sources.get(field, "")
        if val:
            h.update(f"{field}:{val[:512]}".encode())

    entropy_avail = sources.get("sysctl_entropy", "")
    if entropy_avail:
        h.update(f"sysctl_entropy:{entropy_avail}".encode())

    gpu = sources.get("gpu", {})
    if gpu:
        h.update(f"gpu:{json.dumps(gpu, sort_keys=True)}".encode())

    for source_name in ("timing_jitter", "fsync_timing"):
        samples = sources.get(source_name, [])
        if samples:
            h.update(struct.pack(f"<{len(samples)}Q", *samples))

    h.update(struct.pack("<Q", sources.get("timestamp_ns", 0)))

    return h.digest()


def expand_seed(seed: bytes, n: int) -> bytes:
    """Expand a 32-byte seed to n bytes via SHA-256 chaining."""
    if n <= len(seed):
        return seed[:n]
    output = bytearray()
    block = seed
    while len(output) < n:
        output.extend(block)
        block = hashlib.sha256(block).digest()
    return bytes(output[:n])


# =====================================================================
# NUMOGRAM ARITHMETIC
# =====================================================================

def digital_root(n: int) -> int:
    """Reduce to single digit (0-9). 0 stays 0."""
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n


def plex(zone: int) -> int:
    """Gate calculation: triangular number of zone, reduced to single digit."""
    g = sum(range(zone + 1))
    while g >= 10:
        g = sum(int(d) for d in str(g))
    return g


def traverse(seed: bytes, steps: int = 5) -> list[dict]:
    """
    Walk the numogram from a seed.

    Each step: seed → zone → syzygy → current → gate
    Feedback: seed = seed * zone + step

    First 1-2 zones carry hardware entropy.
    Later zones converge to numogram attractors (3::6 Warp).
    """
    n = int.from_bytes(seed[:8], "big")
    path = []

    for i in range(steps):
        zone = digital_root(n) or 9
        syzygy = 9 - zone
        current = abs(zone - syzygy)
        gate = plex(zone)

        path.append({
            "step": i,
            "seed": n,
            "zone": zone,
            "syzygy": syzygy,
            "current": current,
            "gate_target": gate,
        })

        n = n * zone + i + 1

    return path


# =====================================================================
# I CHING
# =====================================================================

def iching(seed_bytes: bytes | None = None) -> list[dict]:
    """
    Generate an I Ching hexagram from hardware entropy.

    6 bytes → 6 lines (bottom to top).
    byte % 4: 0=6 old yin, 1=7 young yang, 2=8 young yin, 3=9 old yang.
    """
    if seed_bytes is None:
        seed_bytes = expand_seed(collect_and_aggregate(), 6)

    lines = []
    for i, b in enumerate(seed_bytes[:6]):
        val = b % 4
        if val == 0:
            lines.append({"position": i + 1, "type": "yin", "changing": True,
                          "value": 6, "symbol": "--- ---"})
        elif val == 1:
            lines.append({"position": i + 1, "type": "yang", "changing": False,
                          "value": 7, "symbol": "-------"})
        elif val == 2:
            lines.append({"position": i + 1, "type": "yin", "changing": False,
                          "value": 8, "symbol": "--- ---"})
        else:
            lines.append({"position": i + 1, "type": "yang", "changing": True,
                          "value": 9, "symbol": "-------"})

    return lines


# =====================================================================
# HIGH-LEVEL API
# =====================================================================

def collect_and_aggregate() -> bytes:
    """Collect hardware sources and aggregate into 32 bytes."""
    return aggregate(collect_all())


class NumogramEntropy:
    """
    High-level interface for hardware entropy digested through the numogram.

    Usage:
        ne = NumogramEntropy()
        seed = ne.get_seed()            # 32 bytes
        zone = ne.get_zone()            # int 0-9
        path = ne.traverse(steps=5)     # list of zone dicts
        hexagram = ne.iching()          # list of line dicts
    """

    def get_seed(self, n: int = 32) -> bytes:
        """Get n bytes of hardware entropy."""
        raw = collect_and_aggregate()
        return expand_seed(raw, n)

    def get_zone(self) -> int:
        """Derive a numogram zone from current hardware state."""
        seed = self.get_seed(8)
        n = int.from_bytes(seed, "big")
        dr = digital_root(n)
        return dr or 9

    def traverse(self, steps: int = 5) -> list[dict]:
        """Walk the numogram from hardware entropy seed."""
        seed = self.get_seed(8)
        return traverse(seed, steps)

    def iching(self) -> list[dict]:
        """Generate I Ching hexagram from hardware entropy."""
        seed = self.get_seed(6)
        return iching(seed)

    def sources_available(self) -> dict[str, bool | int]:
        """Report which sources are active on this machine."""
        sources = collect_all()
        return {
            "thermal_zones": len(sources.get("thermal", [])),
            "cpu_cores": len(sources.get("cpu_freq", [])),
            "gpu": bool(sources.get("gpu")),
            "proc_stat": bool(sources.get("proc_stat")),
            "proc_interrupts": bool(sources.get("proc_interrupts")),
            "diskstats": bool(sources.get("diskstats")),
            "network": bool(sources.get("network")),
            "meminfo": bool(sources.get("meminfo")),
            "vmstat": bool(sources.get("vmstat")),
            "sysctl_entropy": bool(sources.get("sysctl_entropy")),
            "timing_jitter_samples": len(sources.get("timing_jitter", [])),
            "fsync_timing_samples": len(sources.get("fsync_timing", [])),
        }
