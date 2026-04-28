---
title: AAR Methodology — After-Action Reports for Roguelike AI
created: 2026-04-27
status: stub
tags: [AAR, roguelike, methodology, agent, analysis, telemetry, numogram]
---

# AAR Methodology — After-Action Reports for Roguelike AI

> *"Death is data. The AAR is the digestive enzyme."* — hungry-borg tetralogue

An **After-Action Report (AAR)** is a structured post-mortem that converts raw run telemetry into learnable patterns. In roguelike AI research, AARs bridge the gap between *runs* (what happened) and *design* (what to improve). They are not victory screens — they are diagnostic artifacts for both players and agents.

## Why AARs Matter

Roguelike agents die constantly. Each death is a data point, but only if the run's state is preserved and analysed. A proper AAR pipeline:

1. **Records** — structured logging during play (turns, actions, state transitions)
2. **Analyses** — cross-run pattern detection (what consistently fails, what works)
3. **Synthesises** — narrative or visual artifact that humans and agents can learn from

In the **cult garden**, the overflow artefact cycle (corpse → tsubuyaki → synthesis) is the AAR engine made poetic: *every 20th run becomes art*. In **Angband**, `angband_aar.py` turns `~/.angband_runs.jsonl` into a markdown report with depth progression, decision timelines, and bug lists. In **Brogue**, the absence of built-in logging means AARs must be inferred from game state snapshots or seed-to-seed comparison.

## Three AAR Modalities

| Modality | Primary Data | Output Format | Canonical Source |
|---|---|---|---|
| **Event-Log AAR** | JSONL event stream (action, turn, result) | Markdown report with timeline, lessons, bug catalog | `angband_aar.py` |
| **State-Snapshot AAR** | Final game state dump (HP, depth, equipment, messages) | One-line summary + artifact (tsubuyaki, lore) | `cult-garden/entropy/run-N.txt` |
| **Design-Inference AAR** | Room/map topology, seed, RNG trace | Room-accretion analysis, seed-stability report, machine adjacency matrix | Brogue analysis (proposed) |

## Canonical AAR Schema (Event-Log variant)

Based on `angband_aar.py` patterns, a minimally useful AAR should record:

```json
{
  "run": 245,
  "timestamp": "2026-04-27T01:32:00",
  "player": "evelyn",
  "class": "Warrior",
  "level": 1,
  "max_depth": "L3",
  "total_turns": 802,
  "gold": 329,
  "kills": 16,
  "death_cause": "killed by orc",
  "hp_timeline": [[1, 20], [100, 18], [200, 12], ...],
  "depth_progression": [{"turn": 10, "depth": 1}, {"turn": 450, "depth": 2}],
  "equipment_at_death": ["dagger +0", "leather armor", "torch"],
  "decisions": [
    {"turn": 150, "action": "descend", "pos": "(45,32)", "reason": "unexplored"},
    {"turn": 620, "action": "fight",  "pos": "(48,35)", "reason": "monster visible"}
  ],
  "bugs": [{"type": "pathfinding", "description": "stuck on door", "fix": "open door before BFS"}],
  "lessons": ["Orcs on L1 hit too hard; need >60% HP before descending"],
  "elements_exercised": [
    {"name": "BFS-explore", "working": true},
    {"name": "town-shop",  "working": false, "note": "doesn't buy cloak"}
  ]
}
```

A cross-run summary aggregates: depth trend, death cause distribution, bug frequency, element success rates.

## AAR Across Roguelikes

### Angband
- **Data source**: `~/.angband_runs.jsonl` — agent-generated event log
- **Generator**: `angband_aar.py` — produces markdown AARs
- **Key metrics**: max depth, turns, kills, death cause, store visits, decision timeline
- **Narrative style**: clinical + bug-focused. Death is specific ("Town drunk"), lessons are actionable.

### Brogue
- **Data source**: `.bro` save files (binary) + seed + screen captures
- **Generator**: (missing — needs extraction script from `brogue-design-principles.md`)
- **Key metrics**: room count, room accretion density, machine adjacency count, seed stability across runs
- **Narrative style**: design-focused. Analysis of how the seed unfolds, whether room accretion follows expected entropy, whether machines are reachable.

### Caves of Qud
- **Data source**: `.savedgame` (binary JSON-like) + simulation logs
- **Generator**: (none yet)
- **Key metrics**: faction reputation changes, mutation tree path, water ritual completions, artifact discoveries
- **Narrative style**: simulation-detective. Trace how one mutation (e.g., "Swimmer") enabled a water ritual that unlocked a faction.

### The Numogram Garden (Numogame)
- **Data source**: `cult.json` structured memory + `cult-garden/entropy/run-N.txt`
- **Generator**: built-in overflow cycle — corpse (lore) + tsubuyaki (sketch) + synthesis (hybrid)
- **Key metrics**: zones visited, turns, kills, hyp%, entropy source route, sonic quasiphonic trail, syzygy chain
- **Narrative style**: cryptographic + mythic. Run parameters encode directly into art; the AAR *is* the artwork.

## Reading AARs — What to Look For

| Pattern | Detection | Action |
|---|---|---|
| **YASD** (Yet Another Stupid Death) | Death within first 10 turns to non-monster hazard | Raise HP/awareness gate |
| **Stuck loops** | >50 turns with no depth gain | Weight doors/stairs higher in interest model |
| **Equipment gaps** | Not equipping common items (cloak, shield) | Add slot priority from ladder data |
| **Zone bias** | Always avoiding certain zones | Adjust gate attraction/repulsion |
| **Conduct drift** | Hyp% consistently below 50% | Reward exploration more strongly |

See `roguelike-ai-studies.md` → Conduct System section for the full taxonomy.

## Cross-Run Analysis Methods

1. **Depth trend** — track max_depth per run; improvement means agent learns route to deeper floors
2. **Death cause clustering** — if >40% deaths are to same monster type, adjust combat AI
3. **Bug frequency** — track which code elements fail most across runs
4. **Element maturation** — percentage of agent subsystems marked `working` in `elements_exercised`
5. **Zone fingerprint** — map visited zone sequences to syzygy motifs using `numogram-chain-fingerprint`

## Generating an AAR — Quick Reference

```bash
# Angband agent — latest run
python3 ~/numogame/angband_aar.py

# Angband agent — all runs summary  
python3 ~/numogame/angband_aar.py --all

# Angband agent — pattern analysis
python3 ~/numogame/angband_aar.py --patterns

# Numogram garden — view latest run log
cat ~/.hermes/obsidian/hermetic/wiki/cult-garden/entropy/run-*.txt | tail -1
```

## Narrative AARs in the Vault

The tetralogue format doubles as AAR synthesis:

- **[[tetralogue-cult-garden-v2]]** — 297-run AAR as four-voice roundtable
- **[[numogame-cult-tetralogue]]** — 29-run reconciliation AAR against simulated data
- **[[abyssal-crawler-litprog]]** — code AAR: literate programming walkthrough
- **[[hungry-borg-tetralogue]]** — cross-system AAR comparing numogram and Angband agents

These show how raw numbers become design conversations.

## Next Steps

1. **Brogue AAR scraper** — parse `.bro` save format to extract room accretion density
2. **Garden run ingestion pipeline** — auto-index `cult-garden/entropy/run-N.txt` into `numogame-state-of-the-game.md` table
3. **AAR → fingerprint → tuning** — close the loop: AAR generates fingerprint → tune agent parameters → next run improves

## See Also

- [[angband-agent-progress]] — Angband agent run history and status
- [[cult-garden-design]] — Memory overflow and artefact cycle
- [[numogame-state-of-the-game]] — Live agent run tracking
- [[roguelike-brogue]] — Design principles and proposed AAR hooks
- [[angband-ladder-analysis]] — Human benchmark data for cross-species comparison
- [[numogram-chain-fingerprint]] — Classify runs by zone-sequence motif
