# Contributing to BriefOtter

BriefOtter has an offline foundation; collection, model evaluation and reporting remain future work. Start with the [README](README.md) and the [project guide](.agents/skills/project-guide/SKILL.md). Use an issue to discuss a use case, clarify expected behavior or propose a focused change before substantial implementation.

## Useful reports

Explain the problem, the expected outcome and how the proposed change would help. For selection examples, provide a synthetic client request and a similar message that should not be selected. Do not post real private messages, account identifiers, credentials or session files. Report sensitive concerns through [SECURITY.md](SECURITY.md).

## Local checks

Follow README's locked setup for the offline foundation, then run `scripts/check.sh` for static/build/package qualification. Select the concrete test mode with the maintainer before adding `--tests` or invoking pytest. Current synthetic tests make no real-provider requests; `--run-ai` is an explicit unavailable preflight. For documentation changes, verify relative links, label intended versus implemented behavior accurately and run `git diff --check`. Inspect new files too: the default diff does not include untracked files.

Implementation proposals should identify focused behavior checks and preserve the default-on test boundary during imports, collection and child processes. Private configuration/session carriers and provider access are not contributor prerequisites for the offline foundation. Agree live-data verification separately. Source archives must retain required public source/tests/docs while excluding private context and generated runtime data; inspect actual wheel and sdist members independently.

## Pull requests

Keep changes focused and open a pull request targeting `main`. Link the relevant issue or agreed feature package, explain the resulting behavior and provide actual local verification results. State any unperformed check and its prerequisite. The maintainer reviews and performs the final merge; review timing and acceptance are not guaranteed.

Keep discussion respectful and specific. Questions and proposals use the repository issue tracker; no separate help channel or response-time commitment is offered at this stage.
