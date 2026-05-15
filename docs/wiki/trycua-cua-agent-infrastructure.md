---
title: "trycua/cua — Computer-Use Agent Infrastructure"
tags: [cua, computer-use, agents, sandbox, mcp, trajectory, background-control, cua-bench, cua-driver, automation, empirical-validation, roguelike, audio]
date: 2026-05-15
status: active
source: https://github.com/trycua/cua
---

# trycua/cua — Computer-Use Agent Infrastructure

## ⚡ Current Installation Status (2026-05-15)

| Component | Status | Notes |
|-----------|--------|-------|
| **cua CLI** (v0.1.8) | ✅ Installed | `~/.cua/bin/cua` — cloud sandbox management |
| **cua Python SDK** | ❌ Blocked | Requires Python `<3.14`; system has 3.14.4 |
| **Docker** | ✅ Available | Used as local sandbox equivalent |
| **CuaBot** | ❌ Not installed | Optional, needs Node.js |
| **cua-bench** | ❌ Not installed | Needs `uv` + separate checkout |

The Python SDK (`cua-sandbox`, `cua-agent`) pins `requires-python = ">=3.11,<3.14"` and will not install on Python 3.14. A Hermes skill (`cua-setup`) documents the current state and provides Docker-based sandbox templates as a stopgap. Track https://github.com/trycua/cua for when Python 3.14 support lands.

See [[cua-setup]] for the Hermes skill with install details and Docker sandbox templates.

Open-source infrastructure for building, benchmarking, and deploying AI agents that control full desktops across macOS, Linux, and Windows. Provides unified sandboxes, SDKs, MCP drivers, and RL environments to train and evaluate computer-use agents **without disrupting foreground user workflows**.

## Architecture & Core Components

| Component | Purpose | Our Relevance |
|-----------|---------|---------------|
| **cua-driver** (Swift + Rust port) | Background computer-use on macOS/Linux/Windows via SkyLight/private AX SPIs. MCP/CLI backend for any agent. | Background agent orchestration: run numogram calculations, mod-writer experiments, or roguelike gameplay without stealing focus |
| **cua-sandbox SDK** (`pip install cua`) | Unified Python API for agent-ready VMs/containers across Docker, QEMU, Lume, Android Emulator, Hyper-V | Isolated experiment sandboxes for audio synthesis, classifier training, CSI pipeline testing |
| **cua-bench** | Benchmarks & RL environments (OSWorld, ScreenSpot, Windows Arena). Exports trajectories for training | Empirical validation framework: standardized test suites for MIR pipeline, oracle accuracy, zone classifier |
| **cua-mcp** | MCP-native driver over stdio. Drop-in backend for coding assistants | Could connect to our TouchDesigner MCP, context engine, or RuView CSI aggregator |
| **Trajectory Recording** | Per-turn app state, screenshots, actions, click markers. Optional video capture with zoom-on-click | Complete experiment logs, reproducibility, peer review workflow |
| **CuaBot** | Co-op sandbox CLI. Streams native windows with H.265, shared clipboard & audio | Multi-agent tetralogue roundtables: four isolated sandboxes sharing a workspace |

## Background Control: The Deep Technical Win

The cua-driver's approach to **background computer-use** is remarkable — it solves a fundamental OS constraint (one cursor, one keyboard, one focused window) through reverse engineering:

| Technique | What it does | Why it matters |
|-----------|-------------|----------------|
| **Focus Without Raising** | Uses `SLPSPostEventRecordTo` (SkyLight) to flip app active state without `SLPSSetFrontProcessWithOptions` | Agent can drive apps without stealing focus or triggering Space-switching |
| **Bypassing HID** | `SLEventPostToPid` (undocumented) posts events via auth-signed SkyLight channel, bypassing `IOHIDPostEvent` | Chrome/renderer accept events because they carry a "WindowServer trust envelope" marker |
| **Chromium User-Activation Gate** | Send decoy `LeftMouseDown`/`Up` at `(-1, -1)` to tick the activation gate without triggering any target | Synthetic clicks in Chromium become "trusted gestures" |
| **Electron AX Trees** | Private `_AXObserverAddNotificationAndCheckRemote` keeps AX trees live through occlusion/hidden states | Accessibility trees update even when windows are hidden — full UI state accessible in background |

The technical depth here is **empirical systems engineering**: reverse-engineer undocumented APIs, probe with `lldb`, diff against system tools (yabai), and iteratively test. This is the kind of work that produces durable knowledge about how systems actually behave, not how their docs say they should.

## Capture Modes

| Mode | Output | Best For | Permission Required |
|------|--------|----------|---------------------|
| `ax` | Simplified AX tree (Markdown outline) | System/AppKit/SwiftUI apps | No Screen Recording needed |
| `vision` | PNG screenshot | Vision-first VLMs | Screen Recording |
| `som` **(default)** | AX tree + screenshot + clickable element mapping | General use | Screen Recording |

The `som` (Set-Of-Mark) mode overlays numbered markers on interactive elements — exactly the same pattern our `browser_snapshot` tool uses with `@e1`, `@e2` ref IDs. This is a **universal UI addressing pattern**: every GUI system needs element-indexed clicks to be agent-comprehensible.

## Sandbox SDK — Unified Abstraction

```python
from cua import Sandbox, Image

async with Sandbox.ephemeral(Image.linux()) as sb:   # or .macos(), .windows(), .android()
    result = await sb.shell.run("python csi_transducer.py")
    screenshot = await sb.screenshot()
    await sb.mouse.click(100, 200)
    await sb.keyboard.type("Hello from Cua!")
    await sb.mobile.gesture((100, 500), (100, 200))  # multi-touch gestures
```

Single API, any runtime. The `ephemeral()` context manager creates a throwaway VM/container, runs the task, captures output, and destroys it — perfect for reproducible experiments.

## Applications for Our Currents

### Current I: Numogram / AQ
- **Background Oracle Agent:** Run cua-driver to execute extended numogram traversals while user continues working. Agent reads wiki pages, calculates syzygy chains, updates findings — all without stealing the active window.
- **Isolated Reproducibility:** Each AQ calculation runs in a sandbox with logged inputs, outputs, and intermediate state. No more "what was the seed?" — every result has a trajectory.
- **Cross-Platform Verification:** Run the same numogram-calculator across Linux, macOS, Windows sandboxes to verify floating-point consistency.

### Current II: Roguelike Architecture
- **Headless Roguelike Agent in Sandbox:** Deploy agents that play terminal roguelikes in isolated VMs. Cua captures screenshots → agent decides → Cua executes keystrokes → trajectory logs everything. Perfect for automated cult-garden telemetry and gameplay analysis.
- **RL Training Loop:** Use cua-bench as the reward signal environment. Agent plays → cua-bench scores → agent updates strategy → replay. The standard RL cycle, but for dungeon-crawling agents.
- **Multi-Instance Parallel Play:** Spawn N sandbox instances, each running a different agent with different strategies (Brogue accretion, DCSS interest-driven, random walker). Compare emergent behaviors across strategies.

### Current III: Audio Alchemy
- **MIR Pipeline Isolation:** Run feature extraction in ephemeral sandboxes. If a bad model corrupts the pipeline, the sandbox is already gone — no damage to the main environment.
- **Mod-Writer Version Testing:** Deploy sandboxes running mod-writer v0.8.0 vs v0.8.3 with identical inputs. Compare outputs side by side with screenshots and trajectory recordings.
- **Cross-Platform Audio Toolchain:** Verify that our Rust audio rendering crate produces identical WAV output across Linux, macOS, and Windows sandboxes.

### Current IV: Empirical Validator
- **cua-bench Integration:** Standardized benchmark suites for each current. MIR feature extraction accuracy, zone classifier precision, oracle reading quality — all measured against ground truth test sets.
- **Trajectory-as-Evidence:** Every experiment has a complete trajectory: inputs → intermediate states → final output → screenshots → video. This is **publication-ready evidence** — peer review can replay exactly what happened.
- **Reproducibility by Design:** Ephemeral sandboxes mean every experiment starts from a known state. No "it works on my machine" — the sandbox IS the machine definition.

## MCP Integration Potential

Cua's MCP-native architecture means it could connect to:

| Target | Integration | Use Case |
|--------|-------------|----------|
| **TouchDesigner MCP** | cua-driver MCP → TouchDesigner MCP bridge | Background agent controls TOPs/CHOPs via the existing TouchDesigner MCP protocol |
| **Context Engine** | cua sandbox → context engine → enhanced knowledge access | Agent running in sandbox has access to our full wiki and memory |
| **RuView CSI Aggregator** | UDP port 5005 → cua sandbox → transducer pipeline | Live CSI data flows into isolated sandbox for processing |
| **Hermes Agent** | cua MCP stdio → hermès tool invocation | Background agent can call our tools (web_search, terminal, file) through MCP |

## Technical Architecture Mapping

```
┌─────────────────────────────────────────────────────────────┐
│                        Host Machine                         │
│                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │ Foreground    │    │ cua-driver   │    │ cua-mcp      │  │
│  │ (user work)   │    │ (background  │◄──►│ (stdio       │  │
│  │               │    │  control)    │    │  protocol)   │  │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘  │
│         │                   │                   │           │
│         │            ┌──────▼───────┐    ┌──────▼───────┐  │
│         │            │ Sandbox A    │    │ Sandbox B    │  │
│         │            │ (MIR exp)    │    │ (Roguelike)  │  │
│         │            │              │    │              │  │
│         │            └──────┬───────┘    └──────┬───────┘  │
│         │                   │                   │           │
│  ┌──────▼───────┐    ┌──────▼───────┐    ┌──────▼───────┐  │
│  │ Active App   │◄───►│ Sandbox C    │    │ cua-bench    │  │
│  │ (browser)    │    │ (Oracle)     │    │ (RL env)     │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

Foreground user workflow is completely unaffected. All agent activity happens in background sandboxes with separate input streams, invisible windows, and independent state.

## Comparison with Alternatives

| System | Pros | Cons | vs cua |
|--------|------|------|--------|
| **Playwright/Puppeteer** | Web automation, headless browsers | Browser-only, can't control desktop | cua covers full desktop including native apps |
| **pyautogui** | Simple desktop automation | Blocks foreground, no isolation | cua provides background control + isolation |
| **Anthropic CUA** | Integrated with Claude | Proprietary, $2000/month | cua is open-source, permissive license |
| **OpenAI CUA** | Built into GPT-4o | Closed ecosystem, no transparency | cua releases full source + benchmarks |
| **AutoHotKey** | Mature Windows automation | Windows-only, foreground-only | cua is cross-platform + background |
| **AppleScript** | Native macOS control | macOS-only, limited scope | cua uses private APIs SkyLight for broader control |

Cua's unique value: **open-source background control + unified sandbox + benchmark framework + trajectory recording**. No other system offers all four.

## Known Limitations

| Limitation | Impact | Workaround |
|------------|--------|------------|
| Chromium right-clicks coerced to left-clicks | Context menus in web apps don't work | Use AX-based right-clicks for AX-addressable targets |
| Canvas/game apps lack AX trees | Blender GHOST, Unity, games can't use element-indexed clicks | Fall back to `vision` mode + pixel coordinates |
| macOS private APIs | SkyLight/AX SPIs are undocumented and may break | cua-driver Swift/Rust port includes parity tests for resilience |
| Screen Recording permission | Required for `vision` and `som` modes | `ax` mode works without it but reduced functionality |

## Concrete Integration Opportunities

### 1. Background Numogram Oracle

```python
# Run oracle calculations without disturbing foreground
async with Sandbox.ephemeral(Image.linux()) as oracle:
    await oracle.shell.run("python numogram_calculator.py --seed 'hyperstition'")
    result = await oracle.shell.run("cat results.json")
    screenshot = await oracle.screenshot()  # Capture the output
    # Update wiki with findings (via trajectory recording)
```

### 2. Rogueike Agent Training Loop

```
cua-bench environment ← defines reward function (rooms explored, deaths, items found)
    ↓
Agent (DQN, PPO, or our interest-driven heuristic)
    ↓
cua sandbox ← terminal emulator running the roguelike
    ↓
Agent takes action (keypress/mouse) → sandbox executes → game state updates
    ↓
cua-bench scores → agent updates policy → repeat
    ↓
Trajectory exported → analyze emergent behavior → refine zone mapping
```

### 3. MIR Pipeline Cross-Validation

```python
# Run identical MIR processing in three different sandbox images
for img in [Image.linux(), Image.macos(), Image.windows()]:
    async with Sandbox.ephemeral(img) as sb:
        await sb.shell.run("pip install librosa essentia")
        await sb.file.upload("test_audio.wav")
        result = await sb.shell.run("python extract_features.py test_audio.wav")
        screenshots.append(await sb.screenshot())

# Compare results across platforms → verify deterministic behavior
```

## Empirical Validation Questions

| Question | Test Method |
|----------|-------------|
| Can cua-bench provide standardized test sets for MIR feature extraction? | Load known audio corpus → run feature extraction → compare to ground truth |
| Does trajectory recording capture enough state for full experiment replay? | Record session → replay in fresh sandbox → verify identical output |
| Can background cua-driver reliably control terminal applications? | Run tmux + ncurses roguelike → execute agent actions → verify game responds |
| Do sandbox snapshots preserve environment state for reproducibility? | Create snapshot → destroy sandbox → recreate from snapshot → verify identical behavior |

## Related

- [[hermes-agent]] — Core agent system; cua is a potential extension for background control
- [[autonomous-field]] — Agent experimentation that needs sandbox isolation
- [[numogram-council-orchestrator]] — Multi-agent deliberation could leverage CuaBot
- [[mod-writer-gap-analysis]] — Validation work that could use cua-bench infrastructure
- [[ruview-wifi-csi-transducer]] — CSI pipeline testing in isolated sandboxes
- [[roguelike-auto-explore]] — Automated gameplay that could use cua sandbox + terminal control
- [[InterestingSites]] — Source link list where cua was originally noted
