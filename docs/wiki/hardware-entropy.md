---
title: Hardware Entropy Sources
created: 2026-04-18
last_updated: 2026-04-18
source_count: 3
status: active
tags: [numogram, entropy, hardware]
---

# Hardware Entropy Sources

Local entropy harvesting from physical machine state — thermal sensors, CPU timing jitter, GPU sensors, VM subsystem, storage stack. No network, no API keys, no root.

Built as an alternative to OpenEntropy (amenti-labs/openentropy) which requires Python ≤3.13 for its Rust/PyO3 bindings. Our implementation reads the same underlying kernel interfaces directly.

## Tools

- `~/.hermes/tools/hardware_entropy.py` — sampler with 12 sources, numogram zone derivation
- `~/.hermes/tools/numogram_traverse.py` — numogram traversal from hardware entropy seed

## Sources (12 on this machine)

| # | Source | Interface | What it captures |
|---|--------|-----------|-----------------|
| 1 | Thermal zones (3) | /sys/class/thermal/thermal_zone*/temp | CPU/chipset temperature in millidegrees |
| 2 | CPU frequencies (4) | /sys/devices/system/cpu/cpu*/cpufreq/scaling_cur_freq | Per-core clock speed jitter |
| 3 | GPU sensors | nvidia-smi | Temperature, SM clock, power draw, utilization, fan |
| 4 | /proc/stat | /proc/stat | CPU jiffies (user, nice, system, idle, iowait) |
| 5 | /proc/interrupts | /proc/interrupts | Interrupt counters per IRQ per CPU |
| 6 | Disk I/O | /proc/diskstats | Block device read/write counters |
| 7 | Network | /proc/net/dev | Packet/byte/error counters per interface |
| 8 | Memory | /proc/meminfo | Free/available/buffered/cached memory |
| 9 | Timing jitter | time.perf_counter_ns() | 256 nanosecond samples (60-860ns range) |
| 10 | VM subsystem | /proc/vmstat | Page faults, swaps, reclaim counters |
| 11 | Kernel entropy | /proc/sys/kernel/random/entropy_avail | Available entropy in kernel pool |
| 12 | fsync timing | os.fsync() + perf_counter_ns | Storage stack latency (NAND, journal, cache) |

## Comparison with OpenEntropy (63 sources)

OpenEntropy has 63 sources across 13 categories. Breakdown of what we have vs what we're missing:

### We have equivalents for:
- **Timing (3/7):** clock_jitter (our timing_jitter_sample), dram_row_buffer (vmstat covers some), page_fault_timing (fsync covers storage path)
- **Scheduling (1/6):** /proc/stat captures scheduler counters; we lack sleep_jitter, thread_lifecycle, pe_core_arithmetic
- **System (3/6):** /proc/stat, /proc/vmstat, sysctl_entropy match sysctl_deltas, vmstat_deltas, process_table
- **Network (1/3):** /proc/net/dev counters; we lack DNS/TCP timing, WiFi RSSI
- **IO (2/6):** /proc/diskstats + fsync_timing; we lack NVMe passthrough, raw device reads
- **Microarch (0/16):** None — speculative_execution, dvfs_race, tlb_shootdown etc. require low-level CPU timing
- **Thermal (1/4):** /sys/class/thermal; we lack PLL-specific sources (audio, display, PCIe)
- **Sensor (0/3):** No audio/camera/bluetooth (need hardware)
- **GPU (1/2):** nvidia-smi (better than gpu_divergence for our setup)
- **IPC (0/4):** macOS-only (Mach, kqueue, keychain)
- **Quantum (0/1):** No QRNG device

### What we're missing that matters:
- **NVMe passthrough** (source #58) — closest to NAND hardware, needs ioctl
- **DRAM row buffer timing** (source #13) — 32MB buffer, cache hierarchy noise
- **Branch predictor state** (source #15) — data-dependent timing
- **P/E core migration** (source #35) — highest entropy rate (6.35 bits/byte)

### What we're missing that doesn't matter:
- 30+ macOS-only sources (IOKit, Mach IPC, Apple Silicon specific)
- Audio/camera/bluetooth sensors (need external hardware)
- USB QRNG (need £200+ device)

### Bottom line for our use case:
12 sources is sufficient for numogram seeding. The marginal gain from adding NVMe passthrough or DRAM timing is low — we're already getting unique seeds every run. The numogram's own attractors (3::6 Warp) provide more structural entropy than hardware noise does after the first 2 traversal steps.

## Roguelike Integration

The roguelike now supports `--hw-entropy` flag:

```bash
# Normal mode (PRNG seed)
python3 ~/numogame/numogram_roguelike.py --headless

# Hardware entropy mode
python3 ~/numogame/numogram_roguelike.py --headless --hw-entropy
```

When active:
- Seed is derived from 8 bytes of hardware entropy
- Numogram zone is calculated from the seed
- Game log shows: "Hardware entropy seed: 438294 | Zone 7 (syzygy 2)"
- Each run is seeded by the physical state of this machine at that moment

## Usage Patterns

### Get a numogram zone from hardware noise
```bash
python3 ~/.hermes/tools/hardware_entropy.py --zone
```

### Stream zones for oracle readings
```bash
python3 ~/.hermes/tools/hardware_entropy.py --stream 10 --interval 0.5
```

### Numogram traversal (zone path from hardware seed)
```bash
python3 ~/.hermes/tools/numogram_traverse.py --steps 8
```

### I Ching hexagram from hardware entropy
```bash
# Future: map 6 bytes to 6 lines (yin/yang changing)
python3 ~/.hermes/tools/hardware_entropy.py --bytes 6 | python3 -c "
import sys
data = bytes.fromhex(sys.stdin.read().strip())
for i, b in enumerate(data):
    line = '--- ---' if b % 2 == 0 else '-------'  # yin/yang
    changing = ' x' if b % 8 >= 6 else ''
    print(f'Line {i+1}: {line}{changing}')
"
```

## OpenEntropy Install Status

Blocked on Python 3.14 (PyO3 maxes at 3.13). Options:
- Wait for PyO3 upstream 3.14 support
- Install python313 from AUR (heavy compile)
- **Use our direct approach** (already working, reads same kernel interfaces)

See also: `entropy-sources`, [[numogram-divination]], `numogram-oracle`
