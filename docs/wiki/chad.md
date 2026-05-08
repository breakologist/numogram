---
title: Chad - Local Coding Engine with Verifier Loop
tags:
  - AI
  - Agents
  - Coding Assistant
  - Verifier
  - Local AI
  - Open Source
---

# Chad - Local Coding Engine with Verifier Loop

[Chad](https://usechad.dev/) is a local coding engine that doesn't lie about progress. It features a verifier loop, discovery layer, and plain-English receipts to provide transparent, reliable code generation. Unlike cloud-based coding assistants, Chad runs locally and emphasizes verifiable progress.

## Key Features

- **Verifier Loop**: Every step gets checked before moving to the next one, ensuring actual progress rather than illusory completions.
- **Discovery Before Code**: Like a contractor, Chad asks questions before quoting the job, clarifying requirements upfront.
- **Design Summary Checkpoint**: Repeats back what you asked for to catch misunderstandings early.
- **Receipt with Every Project**: Provides a detailed receipt showing exactly what was done.
- **Self-Bug Fixes**: Shows fixes before they go live, requiring your approval.
- **Confidence Calibration**: Tells you upfront how good it is at your kind of project.
- **Local Execution**: Runs entirely locally on your machine, ensuring privacy and control.

## How It Works

Chad operates in three stages:

1. **Discovery**: Asks questions to understand the project scope and requirements.
2. **Plan**: Creates a detailed plan with milestones and checkpoints.
3. **Build, Verify, Write Receipt**: Executes the plan step-by-step, verifying each step before proceeding, and provides a final receipt.

## Why It's Different

Unlike many coding assistants that generate code in a single shot and hope for the best, Chad:
- Breaks problems into manageable steps
- Verifies each step before proceeding
- Provides transparency throughout the process
- Runs locally without cloud dependencies
- Doesn't make false claims about progress

## Relevance to Hermes Agent

Chad represents an alternative approach to AI-assisted development that emphasizes verification and transparency. For Hermes Agent users, Chad could serve as:
- A local coding companion for building and testing skills
- A verification layer for agent-generated code
- A model for how agents should communicate progress honestly

The "verifier loop" concept is particularly relevant to Hermes Agent's skill-based architecture, where each skill could incorporate similar verification mechanisms.

## Technical Details

Chad is built with:
- Local language models (supports various open-source models)
- Custom verification logic
- Plain-text receipts for auditability
- Modular architecture for extensibility

It can be installed via `go install` or from source, and runs on Linux, macOS, and Windows.

## External Links

- [Chad Official Website](https://usechad.dev/)
- [Chad GitHub Repository](https://github.com/chadlain/chad)
- [Cook-off Benchmarks](https://usechad.dev/cook-off) - comparisons with other coding engines

## See Also

- [Interesting Sites#Chad](Interesting%20Sites.md#chad)
- [EvoSkill](evoskill.md) - another skill-learning framework
- [Hermes Agent Skills](Hermes%20Agent.md#skills)