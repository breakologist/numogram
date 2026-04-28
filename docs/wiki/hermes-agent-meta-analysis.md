---
title: "Hermes Agent — Usage Meta-Analysis"
created: 2026-04-24
tags: ["analysis", "hermes-agent", "local-model", "meta"]
status: active
---


# Hermes Agent — Usage Meta-Analysis

*Created: 2026-04-17*

## Current Usage Pattern

We're using Hermes Agent primarily as an **interactive coding + research companion** — running commands, editing files, searching the web, managing skills and memory. The Angband agent work is the primary development project, with numogram/roguelike design as the creative layer.

### What's Working Well

1. **Sequential iteration with tight feedback loops.** Run agent → observe → fix → rerun. The sidebar correction is a perfect example: user knowledge of actual Angband gameplay caught a parser assumption the model couldn't detect from code alone.

2. **Skills as procedural memory.** Every non-trivial workflow gets captured: angband-agent, roguelike-screen-zones, roguelike-agent-techniques. This compounds across sessions — the agent loads the skill and skips the learning curve.

3. **Wiki as archival layer.** Progress logs, ladder analysis, symbol references — all preserved before context gets compacted.

4. **Memory consolidation.** Stable facts (tool quirks, user preferences, project locations) persist across sessions. The user doesn't have to re-explain Docker networking or SearXNG configuration.

5. **Triangle rotation / tetralogue as creative method.** Three/four voice analysis produces insights unavailable to single-voice reasoning. Applied to numogram research, roguelike design, and lore building.

### What Could Be Done Differently

1. **Background processes for long runs.** Running `timeout 300 python3 angband_agent.py` in foreground blocks the session. Could use `background=true` with `notify_on_complete` to work on other things while the agent plays.

2. **Parallel delegation for research.** When investigating a topic (e.g., Angband Borg architecture), `delegate_parallel` could run 3 searches simultaneously and return all results at once.

3. **Cached delegates for repeated queries.** "Check run data" and "latest AAR" are recurring queries that don't change frequently. `cached_delegate` answers at zero cost from cache.

4. **Model council for design decisions.** "Should the agent fight or flee at 25% HP?" — `council_decide` (3 free models voting, judge synthesizing) gives better answers than single-model reasoning.

## Underutilized Features

### High Impact

1. **Goals system (`evey_goals`).** Multi-session projects (Angband agent, numogram-voices, roguelike design) have no formal goal tracking. Goals enable proactive continuation across sessions without re-explaining context.

2. **Cron jobs for automation.** The Angband agent could run autonomously via cron — 3 runs per night, results delivered to Telegram in the morning. No manual intervention needed.

3. **Background processes.** Long-running tasks (agent runs, scraping, compilation) should use `background=true` to keep the session responsive.

### Medium Impact

4. **Autonomous planning (`autonomous_plan`).** Multi-step tasks with tool/model recommendations and cost estimates. Currently using manual planning.

5. **Session checkpoints (`session_checkpoint`).** Protect against context loss during long development sessions. Not currently used.

6. **`apply_learnings` before delegations.** Check past learnings for relevant lessons before starting a task. Avoids repeating mistakes.

### Low Impact (But Easy Wins)

7. **`validate_output` after delegations.** Check subagent results for hallucination signals before trusting them.

8. **`reflect_on_output` for important summaries.** Self-critique draft responses before sending.

9. **`codebase_inspection` skill.** Structural overview of codebases (functions, complexity, dependencies) instead of manual grep.

## Automation Candidates

These tasks could be fully automated via cron:

| Task | Schedule | Delivery |
|---|---|---|
| Angband agent nightly runs (3 runs) | 2am daily | Telegram morning report |
| Memory consolidation | 3am daily ✅ (updated) | Local |
| Wiki backup to git | 4am daily | Local |
| Cost check + budget alert | 9am daily | Telegram |
| Numogram-voices audio generation | Weekly | Local |

## Session-by-Session Pattern

```
Session start
├── Check status (bridge, MQTT, costs, goals)
├── Load relevant skills
├── Resume work from memory/wiki
├── Interactive development loop
│   ├── Run → observe → fix → rerun
│   ├── Update skills from learnings
│   └── Update wiki from findings
└── Session end
    ├── Commit code changes
    ├── Update wiki
    ├── Consolidate memory
    └── Save skills
```

## Recommendations

1. **Set up cron for Angband agent runs.** 3 runs per night at 2am, results delivered to Telegram. This removes the 300-second blocking issue entirely.

2. **Use goals for multi-session tracking.** Add "Angband agent v3 refinement" as an active goal with clear milestones.

3. **Switch to background processes for agent runs.** When testing interactively, use `background=true` to maintain session responsiveness.

4. **Use council_decide for design choices.** Any decision with trade-offs (fight thresholds, interest scoring, exploration strategy) benefits from multi-model consensus.

5. **Add session checkpoints before long runs.** Protect against context loss during 300+ second agent runs.

## Related
- [[angband-agent-progress]] — agent development log
- [[angband-ladder-analysis]] — human play patterns
- [[angband-symbols]] — symbol reference
- [[roguelike-ai-studies]] — AI agent approaches across 10 roguelikes
