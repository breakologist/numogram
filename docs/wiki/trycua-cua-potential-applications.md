---
title: "trycua/cua - Computer-Use Agent Infrastructure Applications"
tags: [cua, computer-use, agents, sandbox, sdk, benchmark, mcp, trajectory, automation, empirical-validation]
date: 2026-05-14
status: active
---

# trycua/cua - Computer-Use Agent Infrastructure for Our Currents

## Overview
**trycua/cua** is open-source infrastructure for building, benchmarking, and deploying AI agents that control full desktops across macOS, Linux, and Windows. It provides sandboxes, SDKs, MCP drivers, and benchmarks - all with a strict "no-foreground" contract that lets agents operate without disrupting user workflow.

## Key Components & Our Applications

### 1. Cua Driver (MCP-Native Backend)
**What it is:** Background computer-use on macOS/Linux/Windows. Speaks Model Context Protocol over stdio.

**Our Applications:**
- **Numogram Oracle Agent:** Run background oracle calculations that can interact with our wiki, update pages, and perform extended traversals without blocking our main workflow
- **Audio Alchemist Sandbox:** Isolate MIR feature extraction experiments so failed runs don't corrupt our classifier models
- **Roguelike Auto-Explorer:** Deploy agents that play terminal roguelikes in background VMs, collecting gameplay data for zone mapping

### 2. Cua Sandbox/SDK (Unified Python API)
**What it is:** Single API for agent-ready VMs/containers across any OS/runtime.
```python
from cua import Sandbox, Image
async with Sandbox.ephemeral(Image.linux()) as sb:
    result = await sb.shell.run("python mir_pipeline.py")
    screenshot = await sb.screenshot()
    await sb.keyboard.type("zone_4_result")
```

**Our Applications:**
- **Empirical Validation Sandboxes:** Run each hypothesis test in isolated environment to prevent cross-contamination
- **Audio Synthesis Comparison:** Test different mod-writer versions side-by-side without dependency conflicts
- **Numogram Calculation Reproducibility:** Ensure all AQ computations run in controlled, logged environments
- **Cross-Platform Testing:** Verify our Rust/C audio tools work identically across Linux, macOS, Windows VMs

### 3. Cua-Bench (Benchmarking & RL Environments)
**What it is:** Benchmarks and RL environments (OSWorld, ScreenSpot, Windows Arena) with trajectory export for training.

**Our Applications:**
- **MIR Pipeline Ground Truth:** Benchmark our feature extraction against known audio samples using standardized test sets
- **Zone Classifier Validation:** Create benchmark tasks for our AQ classifier - can it correctly identify zones from audio features?
- **Roguelike Agent Training:** Use RL environments to train game-playing agents with numogram-based reward functions
- **Oracle Performance Metrics:** Establish baseline measurements for oracle accuracy across different model providers

### 4. Trajectory Recording
**What it is:** Records per-turn app state, screenshots, actions, and click markers with optional video capture.

**Our Applications:**
- **Numogram Traversal Logs:** Record complete calculation paths for reproducibility and audit
- **Audio Discovery Sessions:** Capture the full workflow of music exploration - what led to what decisions
- **Roguelike Gameplay Archives:** Build dataset of agent playthroughs for analyzing emergent behavior
- **Model Comparison Studies:** Compare how different agents approach the same numogram problem

### 5. CuaBot (Co-op Sandbox CLI)
**What it is:** Multi-agent computer-use sandbox CLI. Streams native windows with H.265, shared clipboard & audio.

**Our Applications:**
- **Tetralogue Roundtables:** Deploy four agents in isolated sandboxes for structured deliberation with shared workspace
- **Council Deliberation:** Run multi-model analysis in parallel, each with isolated environment but shared trajectory
- **Cross-Current Synthesis:** Assign each current to a different agent-sandbox, then compare outputs

## Architecture Mapping to Our Currents

### Current I: Numogram Oracle
```
cua-driver MCP → hermès agent → AQ calculations → wiki updates → trajectory logged
sandbox.ephemeral → isolated calculation → clean environment → reproducible results
cua-bench → benchmark oracle accuracy → track improvement over time
```

### Current II: Roguelike Architect  
```
cua-sandbox → terminal emulator → play roguelike → collect gameplay data → map to zones
trajectory-recording → replay successful runs → identify emergent patterns → refine generation
cua-agent → train RL agent with numogram-based rewards → discover optimal strategies
```

### Current III: Audio Alchemist
```
sandbox.ephemeral → isolate audio experiments → prevent model corruption → safe testing
cuabot chromium → run browser-based audio tools → capture spectrograms → analyze results
cua-bench → benchmark MIR pipelines → compare feature extraction approaches
```

### Current IV: Empirical Validator
```
cua-bench → standardized test suites → ground truth validation → publish results
trajectory-recording → complete experiment logs → reproducibility → peer review
sandbox isolation → controlled variables → fair comparisons → statistical validity
```

## Technical Integration Points

### 1. MCP Integration
Since CUA speaks MCP, it could connect directly to:
- TouchDesigner MCP server for real-time visualization control
- Our custom context engine for enhanced knowledge access  
- RuView CSI aggregator for live data streaming

### 2. Python SDK Synergies
The `cua` SDK integrates with our existing Python stack:
```python
from cua import Sandbox, Image
from mod_writer.composer import ZoneComposer  
from csi_transducer import transduce

async with Sandbox.ephemeral(Image.linux()) as sb:
    # Run CSI-to-audio pipeline in isolated environment  
    await sb.shell.run("python csi_transducer.py --input live_csi.json --output test.mod")
    # Capture results for analysis
    result = await sb.shell.run("cat transducer_output.json") 
    # Update wiki with findings
    await sb.keyboard.type("Zone 4 composition from real CSI data")
```

### 3. Benchmark Pipeline
Integrate with `cua-bench` for validation:
```python
import cua_bench
from our_mir_pipeline import extract_features

# Create benchmark task
task = cua_bench.Task(
    name="mir_feature_extraction",
    input_audio="test_corpus/*.wav", 
    expected_features="ground_truth.json",
    evaluation="cosine_similarity"
)

# Run benchmark
result = cua_bench.run(task, agent=our_mir_agent)
# Publish results to wiki
```

## Concrete Next Steps

### Phase 1: Setup & Experimentation (Week 1)
1. Install cua-driver locally for background agent support
2. Create isolated sandbox for MIR pipeline testing  
3. Run basic trajectory recording on numogram calculations
4. Benchmark current oracle accuracy against known test cases

### Phase 2: Integration & Automation (Week 2)
1. Connect cua-bench to our classifier validation pipeline
2. Deploy background agents for extended roguelike exploration
3. Set up tetralogue roundtables using CuaBot multi-agent sandbox
4. Create standardized benchmark suites for each current

### Phase 3: Advanced Applications (Week 3+)
1. Train RL agents with numogram-based reward functions
2. Cross-platform testing of Rust audio toolchain
3. Automated experiment logging with full trajectory capture
4. Publish validation results using cua-bench framework

## Key Advantages Over Ad-Hoc Solutions

| Feature | Ad-Hoc Approach | CUA Infrastructure |
|:--------|:---------------|:-------------------|
| **Reproducibility** | Manual tracking | Automated trajectory recording |
| **Isolation** | Careful dependency mgmt | Ephemeral sandboxes |
| **Benchmarking** | Custom scripts | Standardized cua-bench |
| **Multi-Agent** | Complex orchestration | CuaBot CLI |
| **MCP Integration** | Custom adapters | Native MCP support |
| **Trajectory Analysis** | None | Built-in export & analysis |

## Related
- [[hermes-agent]] - Our core agent system that could use CUA for enhanced capabilities  
- [[numogram-council-orchestrator]] - Multi-agent deliberation that could leverage CuaBot
- [[mod-writer-gap-analysis]] - Validation work that could use cua-bench infrastructure
- [[autonomous-field]] - Agent experimentation that needs sandbox isolation