---
title: Hermes Skill Auto-Release Pipeline
created: 2026-05-01
category: phase5
status: proposed
---

Cron job that:
1. Scans skill SKILL.md versions vs GitHub releases
2. Detects new commits with updated CHANGELOG [Unreleased] sections
3. Generates release notes from commit messages + CHANGELOG
4. Creates GitHub Release draft via `gh` CLI
5. Commits/pushes updated wiki pages (if docs changed)
We did this manually for v0.6.4 — next time, let the robot do it.

**Skill proposal:** To be scaffolded via `skill-creator`.

**Success metric:** TBD (e.g., classifier accuracy, real-time latency, artist coverage).

**Dependencies:** TBD
