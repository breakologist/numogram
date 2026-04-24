---
title: Session Log — Hardware Entropy & Numogram Entropy Plugin
created: 2026-04-18
last_updated: 2026-04-18
tags: ["entropy", "i-ching", "session-log"]
---


# Session Log — 2026-04-18

## Hardware Entropy Investigation

Investigated qr-sampler (Entropic-Science/qr-sampler) — a framework for replacing PRNG with external entropy sources in LLM token sampling. Key concepts absorbed:

- **Just-in-time entropy**: quantum measurement happens AFTER logits are computed, never before. The reading doesn't exist until you ask for it.
- **Signal amplification**: 20,480 bytes → single float u ∈ (0,1). A 0.1% per-byte bias becomes detectable after aggregation.
- **Entropy-dependent temperature**: model's own uncertainty calibrates sampling randomness.
- **OpenEntropy**: 63 hardware sources, but blocked on Python 3.14 (PyO3 maxes at 3.13).

Built local alternative: `~/.hermes/tools/hardware_entropy.py` — reads 12 sources directly from /sys and /proc without compiled dependencies.

## Sources Built (12)

| Source | Interface | Notes |
|--------|-----------|-------|
| Thermal (3) | /sys/class/thermal | acpitz + x86_pkg_temp |
| CPU freq (4) | /sys/devices/system/cpu | Per-core clock jitter |
| GPU | nvidia-smi | Temp, clock, power, util, fan |
| /proc/stat | /proc/stat | CPU jiffies |
| /proc/interrupts | /proc/interrupts | IRQ counters |
| /proc/diskstats | /proc/diskstats | Block I/O counters |
| /proc/net/dev | /proc/net/dev | Packet counters |
| /proc/meminfo | /proc/meminfo | Memory pressure |
| /proc/vmstat | /proc/vmstat | VM subsystem counters |
| Kernel entropy | /proc/sys/kernel/random | entropy_avail |
| Timing jitter | perf_counter_ns() × 256 | 60-860ns range |
| fsync timing | os.fsync() × 16 | Storage stack noise |

## Numogram Traversal Discovery

Hardware entropy → numogram traversal produces zone paths. Key finding:
- **First 1-2 zones diverge** (true entropy from hardware state)
- **Later zones converge** toward numogram attractors (3::6 Warp)
- The numogram digests chaos and channels it toward structure

## I Ching Integration

Six bytes → six lines. byte % 4 maps to:
- 0 → 6 (old yin, changing)
- 1 → 7 (young yang, stable)
- 2 → 8 (young yin, stable)
- 3 → 9 (old yang, changing)

Changing lines = gates. Stable lines = zones.

## numogram-entropy Plugin

Built at `~/numogram-entropy/` (v0.1.0):
- 12 hardware sources, SHA-256 aggregation
- Numogram traversal built-in
- I Ching hexagram generation
- qr-sampler EntropySource ABC (registers via entry point)
- CLI: `~/numogram-entropy/.venv/bin/numogram-entropy`
- 9/9 tests pass

## Roguelike Integration

`--hw-entropy` flag added to `numogram_roguelike.py` (both curses and headless modes).

### Agent Runs (hw-entropy)
| Run | Player | Turns | Hyp | Zones | Slain |
|-----|--------|-------|-----|-------|-------|
| #181 | agent-hw1 | 98 | 53% | [0,1,8] | 3 |
| #182 | agent-hw1 | 123 | 60% | [0] | 3 |
| #183 | agent-hw2 | 60 | 32% | [0] | 2 |
| #184 | agent-hw3 | 148 | 67% | [0] | 3 |
| #185 | agent-hw4 | 100 | 46% | [0] | 2 |

Agent consistently dies in Zone 0 on hw-entropy maps. Maps are genuinely different from PRNG-seeded runs.

### Human Runs (hw-entropy)
| Run | Player | Turns | Hyp | Zones | Slain | Conducts |
|-----|--------|-------|-----|-------|-------|----------|
| #172 | etym-entropy | 215 | 100% | 8 | 2 | G P |
| #174 | etym-entropy | 243 | 100% | 9 | 0 | G P S |

Run #174: triple conduct (Graph + Pathwalker + Surge). 100% hyp, 9 zones, zero kills.

## Updated Files
- `~/numogram-roguelike.py` — hardware entropy seeding
- `~/.hermes/skills/numogram-oracle/oracle.py` — --hardware and --iching flags
- `~/.hermes/skills/numogram-oracle/SKILL.md` — entropy sources table expanded
- `~/.hermes/skills/entropy-sources.md` — source #11 added
- `~/.hermes/tools/hardware_entropy.py` — 12 sources
- `~/.hermes/tools/numogram_traverse.py` — numogram traversal from HW noise
- `~/numogram-entropy/` — pip-installable plugin

## Open Questions
- qr-sampler consciousness framing: "infrastructure for studying whether conscious intent can influence quantum-random processes"
- Hardware entropy maps are harder for the agent — is this structural (different layouts) or statistical (unlucky seeds)?
- QRNG device (Crypta Labs QCicada, ~£200+) would connect via qr-sampler's gRPC protocol
- Python 3.14 blocks OpenEntropy; wait for PyO3 upstream or install python313 from AUR

## Next Steps
- Tetralogue: four voices discuss the entropy sources
- I Ching ↔ numogram zone mapping (hexagram numbers → zone topology)
- Entropy-dependent roguelike generation (Kp index → Warp influence on map)
