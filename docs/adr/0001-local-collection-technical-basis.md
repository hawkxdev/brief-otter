# First local collection technical basis

Status: Accepted as the D5 technical basis. Implementation, operational qualification and permission for real requests remain separate.

Decision date: 2026-11-10. Applicable design baseline: `3ac5013bbff5009440ea711b9ec8a12e957571d5`.

## Context

The first slice needs a bounded way to evaluate useful Telegram project requests and job vacancies before adding continuous monitoring. The maintainer accepts the six-point D5 summary with the linked technical plan and classifier contract as its basis. This decision does not establish that the detailed behavior has been implemented or tested.

## Decision

- Start with one manually launched run against one public broadcast channel on macOS/Linux.
- Use per-message semantic AI classification for intent, topic and reason; application code owns final disposition.
- Select `glm-5.3-flash` through the ordinary metered Z.ai API, with enabled thinking and `low` effort, as the first evaluation candidate.
- Process message content in memory and keep one replaceable local HTML report, without a message database or archive.
- Keep tests without AI requests separate from real-model tests, with the maintainer selecting the concrete run mode.
- Plan the first semantic evaluation for 45 synthetic cases and a maximum token-cost admission cap of 0.50 USD. Execution requires separate run approval.

## Owners and consequences

[The specification](../specs/001-local-candidates/spec.md) owns detailed requirements, [the plan](../specs/001-local-candidates/plan.md) owns integration and implementation stages, and [the AI contract](../specs/001-local-candidates/ai-classification.md) owns the candidate protocol, prompt/schema and failure limits. [The feature record](../specs/001-local-candidates/tasks.md) owns progress and next action.

The initial candidate is selected for evaluation, with no measured quality, access or runtime-compatibility claim. Individual expected labels still need review before they become the concrete evaluation manifest. This decision does not approve the entire proposed requirement table, install dependencies, assign implementation, authorize spending or grant Telegram/content access. D3/D4 retain their live-work prerequisites; commit and publication approval remain separate.
