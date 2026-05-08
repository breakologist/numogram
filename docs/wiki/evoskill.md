---
title: EvoSkill - Automatic Skill Discovery from Failed Trajectories
tags:
  - AI
  - Agents
  - Skill Learning
  - Open Source
  - Reinforcement Learning
---

# EvoSkill - Automatic Skill Discovery from Failed Trajectories

[EvoSkill](https://github.com/sentient-agi/EvoSkill) is an open-source framework that automatically discovers and synthesizes reusable agent skills from failed trajectories to improve coding agent performance. It addresses a key challenge in developing autonomous AI agents: how to learn effectively from mistakes.

## Key Concepts

- **Failed Trajectory Analysis**: EvoSkill analyzes failed attempts to complete tasks to identify what went wrong and how to improve.
- **Skill Synthesis**: It automatically creates reusable skills from these analyses that can be applied to future tasks.
- **Iterative Improvement**: The framework enables agents to build a repertoire of skills over time, becoming more capable with experience.
- **Open Source**: Available on GitHub for integration into various agentic systems.

## How It Works

1. **Task Execution**: An agent attempts to complete a task, which may fail.
2. **Trajectory Analysis**: EvoSkill analyzes the failure trajectory to identify specific breakdown points.
3. **Skill Extraction**: It extracts reusable patterns from the analysis that can serve as skills.
4. **Skill Library**: These skills are added to a library that the agent can draw upon for future tasks.
5. **Performance Improvement**: With each failure, the agent's skill library grows, leading to better performance on similar tasks.

## Relevance to Hermes Agent

EvoSkill directly complements Hermes Agent's skill-based architecture. While Hermes Agent allows for manual skill creation and management, EvoSkill provides an automated way to discover and synthesize skills from experience. This could be integrated to create a hybrid system where:
- Manual skills provide explicit knowledge and best practices
- EvoSkill-derived skills capture implicit patterns from trial and error

The framework aligns well with the numogram community's interest in AI autonomy and emergent behavior.

## Technical Implementation

EvoSkill is implemented in Python and designed to be modular. It can work with various foundation models and agent frameworks. The project includes:
- Trajectory analysis tools
- Skill extraction algorithms
- Skill library management
- Integration utilities for common agent frameworks

## External Links

- [EvoSkill GitHub Repository](https://github.com/sentient-agi/EvoSkill)
- [Project Documentation](https://github.com/sentient-agi/EvoSkill#readme)

## See Also

- [Interesting Sites#EvoSkill](Interesting%20Sites.md#evoskill)
- [Hermes Agent Skills](Hermes%20Agent.md#skills)
- [Chad](chad.md) (another coding engine with verifier loop)