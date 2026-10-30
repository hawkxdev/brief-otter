# Contributing to BriefOtter

BriefOtter is at the design stage. Start with the [README](README.md) and the [project guide](.agents/skills/project-guide/SKILL.md). Use an issue to discuss a use case, clarify expected behavior or propose a focused change before substantial implementation.

## Useful reports

Explain the problem, the expected outcome and how the proposed change would help. For selection examples, provide a synthetic client request and a similar message that should not be selected. Do not post real private messages, account identifiers, credentials or session files. Report sensitive concerns through [SECURITY.md](SECURITY.md).

## Local checks

There are no application dependencies or runtime commands yet. For documentation changes, verify relative links, check that behavior is labelled as intended or implemented accurately, and run `git diff --check` from the repository root. Inspect newly added files too: the default diff does not include untracked files.

Implementation proposals should identify the required local setup and focused checks. Do not assume access to a maintainer's Telegram account, private sources or paid services. Agree any live-data verification separately and use synthetic fixtures for ordinary automated checks.

## Pull requests

Keep changes focused and open a pull request targeting `main`. Link the relevant issue or agreed feature package, explain the resulting behavior and provide actual local verification results. State any unperformed check and its prerequisite. The maintainer reviews and performs the final merge; review timing and acceptance are not guaranteed.

Keep discussion respectful and specific. Questions and proposals use the repository issue tracker; no separate help channel or response-time commitment is offered at this stage.
