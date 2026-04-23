"""
qr-sampler EntropySource adapter.

Implements the EntropySource ABC so numogram-entropy can plug into
qr-sampler's token sampling pipeline via entry point auto-discovery.

When qr-sampler is not installed, this module is inert (import succeeds,
registration is skipped gracefully).
"""

from .core import collect_and_aggregate, expand_seed, traverse


class NumogramEntropySource:
    """
    qr-sampler EntropySource: hardware entropy → numogram traversal.

    The numogram acts as a digestive organ — it ingests raw physical noise
    and outputs structured zone-numbers. First zones carry hardware entropy,
    later zones converge to numogram attractors (3::6 Warp).

    Config via environment variables:
        NUMOGRAM_TRAVERSE_STEPS  — number of traversal steps (default: 3)
        NUMOGRAM_RAW_PREFIX      — prepend raw bytes before zone path (default: true)
    """

    def __init__(self, config=None):
        import os
        self._traverse_steps = int(os.environ.get("NUMOGRAM_TRAVERSE_STEPS", "3"))
        self._raw_prefix = os.environ.get("NUMOGRAM_RAW_PREFIX", "true").lower() == "true"

    @property
    def name(self) -> str:
        return "numogram"

    @property
    def is_available(self) -> bool:
        # Always available — reads /proc and /sys which exist on Linux
        return True

    def get_random_bytes(self, n: int) -> bytes:
        """
        Get entropy bytes, digested through numogram traversal.

        If raw_prefix is true:
            [raw_bytes] + [zone_path_bytes]
        Otherwise:
            [zone_path_bytes] only
        """
        raw = collect_and_aggregate()

        # Run through numogram
        path = traverse(raw[:8], steps=self._traverse_steps)
        zone_bytes = bytes(p["zone"] for p in path)

        if self._raw_prefix:
            # Interleave: raw bytes provide base entropy,
            # zone bytes provide numogram structure
            combined = bytearray()
            raw_expanded = expand_seed(raw, n)
            for i in range(n):
                if i < len(zone_bytes):
                    # XOR zone structure into first bytes
                    combined.append(raw_expanded[i] ^ zone_bytes[i % len(zone_bytes)])
                else:
                    combined.append(raw_expanded[i])
            return bytes(combined)
        else:
            # Pure zone path, repeated to fill n bytes
            expanded = bytearray()
            while len(expanded) < n:
                expanded.extend(zone_bytes)
            return bytes(expanded[:n])

    def close(self) -> None:
        pass

    def health_check(self) -> dict:
        """Diagnostic check."""
        from .core import collect_all
        sources = collect_all()
        return {
            "source": "numogram",
            "healthy": True,
            "traverse_steps": self._traverse_steps,
            "raw_prefix": self._raw_prefix,
            "thermal_zones": len(sources.get("thermal", [])),
            "timing_samples": len(sources.get("timing_jitter", [])),
            "gpu_available": bool(sources.get("gpu")),
        }


# Attempt registration with qr-sampler if installed
try:
    from qr_sampler.entropy.registry import register_entropy_source
    register_entropy_source("numogram")(NumogramEntropySource)
except ImportError:
    pass
