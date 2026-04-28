"""
numogram-entropy — Hardware entropy digested through numogram traversal.

Physical noise (thermal, timing, GPU, I/O) → numogram zone path → structured entropy.

Standalone usage:
    from numogram_entropy import NumogramEntropy
    ne = NumogramEntropy()
    seed = ne.get_seed()          # 32 bytes of hardware entropy
    zone = ne.get_zone()          # Numogram zone from hardware noise
    path = ne.traverse(steps=5)   # Zone path through the numogram
    hexagram = ne.iching()        # I Ching hexagram from hardware entropy

qr-sampler integration:
    export QR_ENTROPY_SOURCE_TYPE=numogram
"""

from .source import NumogramEntropySource
from .core import NumogramEntropy

__version__ = "0.1.0"
__all__ = ["NumogramEntropySource", "NumogramEntropy"]
