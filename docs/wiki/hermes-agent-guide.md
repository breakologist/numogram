---
title: Hermes Agent — The Complete Guide (Orange Book)
created: 2026-04-11
source: /root/.hermes/obsidian/hermetic/raw/Hermes-Agent-The-Complete-Guide-v260407.pdf
version: v260408 (PDF) / v0.7.0 (Hermes Agent)
author: HuaShu (花叔)
status: indexed
tags: [hermes, agent, guide]
---

# Hermes Agent — The Complete Guide

Orange Book by HuaShu (花叔). Practical guide to the Nous Research open-source AI Agent framework. 1.5MB PDF, 17 sections across 5 parts. Based on Hermes Agent v0.7.0.

> *Source: /root/.hermes/obsidian/hermetic/raw/Hermes-Agent-The-Complete-Guide-v260407.pdf*
> *Keywords: Self-improving Agent · Cross-session Memory · Skill System · MCP · Multi-platform*

## Table of Contents

### Part 1: Concepts
- §01 Not Another Agent: From Harness to Hermes
- §02 Hermes Agent at a Glance: 60 Seconds to Understand

### Part 2: Core Mechanisms
- §03 The Learning Loop: Self-Harnessing Agent
- §04 Three-Layer Memory: From Goldfish to Old Friend
- §05 Skills: Self-Evolving Capabilities
- §06 40+ Tools & MCP: Connect Everything

### Part 3: Hands-On Setup
- §07 Installation & Configuration: Three Approaches
- §08 First Conversation: Let Hermes Get to Know You
- §09 Multi-Platform Access: Reach It Anywhere
- §10 Custom Skills: Teaching Hermes New Tricks
- §11 MCP Integration: Connecting Your Tool Stack

### Part 4: Real-World Scenarios
- §12 Personal Knowledge Assistant: Cross-Session Memory
- §13 Dev Automation: Code Review to Deployment
- §14 Content Creation: Research to Draft
- §15 Multi-Agent Orchestration: Running Three Horses at Once

### Part 5: Deep Thinking
- §16 Hermes vs OpenClaw vs Claude Code: Not a Choice
- §17 The Boundaries of Self-Improving Agents

---

## The Learning Loop (§03) — Key Concepts

Five-step closed loop: **Curate Memory → Create Skill → Skill Self-Improvement → FTS5 Recall → User Modeling**

### Step 1: Memory Curation
- Agent **actively decides** what's worth remembering after each conversation (not passive storage)
- Writes to SQLite database with FTS5 full-text indexing
- Periodic nudge mechanism reminds agent to review recent interactions
- Like writing a diary, not recording video

### Step 2: Autonomous Skill Creation
- After complex tasks, agent asks: "will this be useful again?"
- Distills solution into `~/.hermes/skills/` as markdown files
- Skills contain: task description, execution steps, pitfalls

### Step 3: Skill Self-Improvement
- Every use + feedback → agent modifies the Skill file itself
- Like continuous improvement in software: update docs + standards when issues arise
- **Key distinction**: Traditional AI = accumulation of logs (video tape). Hermes = distillation of experience (notebook).

### Step 4: FTS5 Cross-Session Recall
- Searches historical memory based on current topic
- Loads only relevant parts into context (not everything)
- Purely local — all data in SQLite file at `~/.hermes/`

### Step 5: User Modeling (Honcho)
- Optional external integration
- Infers preferences, habits, goals from behavioral patterns
- 12-layer identity modeling

### The Flywheel Effect
- Memory feeds Skill creation → Skill usage generates memories → memories trigger Skill improvement → improved Skills produce better results → better results improve user modeling
- Spins for a single user (no need for millions)
- 3-5 days of use = noticeable difference
- **Tip**: Deploy on $5 VPS running 24/7 for continuous accumulation

---

## Skill System (§05) — Key Concepts

### Three Sources
1. **Bundled Skills** (40+) — pre-built, ship with install
2. **Agent-Created** — grows with usage automatically
3. **Skills Hub** — community-contributed, one-click install

### agentskills.io Standard
- Skills follow the agentskills.io standard
- Interoperable with Claude Code, Cursor, Copilot, Codex CLI, Gemini CLI
- 30+ tools already support it
- Like USB port — one Skill plugs in anywhere

### Self-Improvement Mechanism
1. Execute Skill
2. Collect feedback (satisfied / unsatisfied / corrections)
3. Update Skill file automatically
4. Next execution uses new version

### Comparison: OpenClaw vs Hermes Skills

| Dimension | OpenClaw | Hermes |
|-----------|----------|--------|
| Creation | Manual SOUL.md | Agent-created + manual |
| Maintenance | Manual updates | Auto-evolution + manual |
| Personalization | Generic templates | Grows from usage habits |
| Ecosystem | 5,700+ (large) | 40+ bundled (growing) |

---

## Boundaries of Self-Improvement (§17) — Key Insights

### Safety Architecture
- Skill files = readable markdown (not black-box weights)
- Memory = local SQLite (inspectable, deletable)
- Tool permissions = sandboxed (explicit config)
- MIT license = auditable source code

### The Fundamental Contradiction
> "The value of an autonomous agent lies in not having to watch it, but safety requires you to watch it."

### Open Source vs Closed Source Trust
- **Open source (Hermes)**: "I trust my own ability to audit"
- **Closed source (Claude Code)**: "I trust your business incentives"
- For technical users → open source is clearly better
- For non-technical users → closed source may be safer (someone else on the hook)

### The Ceiling
- Self-improvement ceiling isn't technical — it's the **feedback signal**
- Agent can optimize execution efficiency but can't judge whether direction is right
- Self-improvement makes agents run faster in a known direction — but direction itself needs a human

### HuaShu's Take
> "Let the agent self-improve on the 'how,' while you own the 'what' and the 'don't.' That's not being lazy — it's a different kind of on the loop."

---

## Actionable Tips for Our System

### Immediately Applicable
1. **Memory curation pattern**: Agent actively decides what to remember, not passive dumps. Review our MEMORY.md entries — prune stale, keep durable.
2. **Skill self-improvement**: When using a skill and finding issues, patch immediately (we already do this via `skill_manage`).
3. **FTS5 approach**: Load only relevant context, not everything. Use `session_search` with targeted queries.
4. **Flywheel deployment**: 24/7 VPS for continuous improvement. Our cron jobs already support this.

### To Explore Further
5. **agentskills.io standard**: Check if our skills are compatible — if not, consider standardizing.
6. **Honcho integration**: We already have `honcho_*` tools — use them more actively for user modeling.
7. **Multi-agent orchestration** (§15): Parallel subagent delegation — we have `delegate_task`.
8. **Forgetting mechanism**: Agent memory only grows — who tells it what to forget? Consider periodic memory audits.

### What We Already Do Well
- Skill creation after complex tasks ✓
- Skill patching on discovery of issues ✓
- Memory saves for durable facts ✓
- Session search for cross-session recall ✓
- Multi-agent delegation via delegate_task ✓

### What We Could Improve
- More proactive Honcho profiling
- Periodic memory audit/prune cycle
- Skill versioning (track evolution history)
- Explicit "forgetting" for outdated patterns
