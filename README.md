# BriefOtter

Find development projects and job vacancies in Telegram without reading every feed yourself.

BriefOtter is a personal monitoring tool being designed for people who follow multiple Telegram channels and chats for development work. The goal is a local list of relevant project requests and job vacancies, shown separately with original message links and reasons for selection.

**Status:** Design stage. A runnable version is not available yet.

See the [product roadmap](docs/ROADMAP.md) for the planned milestones and first vertical slice.

The [first feature specification](docs/specs/001-local-candidates/spec.md) proposes the detailed behavior for one-source local collection and identifies decisions still needed before implementation.

## Planned workflow

1. Read messages from selected channels and chats.
2. Identify client project requests and job vacancies as separate opportunity categories; filter out service advertisements and resumes.
3. Apply the agreed selection criteria and show relevant candidates locally, with source links and selection reasons.

Unclear messages remain marked as uncertain. The first version keeps read-only collection and local reporting. The [AI classification proposal](docs/specs/001-local-candidates/ai-classification.md) specifies a first evaluation candidate, strict response format and call limits; model acceptance and real quality remain pending. The earlier rules-only mechanism is a reference, not the proposed runtime. Outgoing Telegram actions remain excluded, and real message processing requires its separate access/content-use decisions.

## Planned verification

The [test execution policy](docs/specs/001-local-candidates/tasks.md#accepted-test-execution-policy) separates tests without AI requests from tests using a real model. The maintainer selects the scope before a run. Model tests use agreed synthetic examples and a separately approved request/spending limit; local tests substitute provider replies and block external calls. There are no implemented test commands yet. Passing local tests does not demonstrate model classification quality.

## Example of the intended selection

These synthetic examples illustrate the planned behavior, not output from a working application.

| Message | Intended result | Reason |
|---|---|---|
| Need a Python developer to build a reporting bot | Project candidate for review | A client is asking for project work |
| Python developer available for Telegram bot projects | Filter out | An executor is advertising services |
| Hiring a full-time Python developer | Vacancy candidate for review | An employer is hiring; show separately from projects |

## Technology

The selected foundation is [Python](https://www.python.org/) with [Telethon](https://docs.telethon.dev/en/stable/). See the [project guide](.agents/skills/project-guide/SKILL.md) for the monitoring concepts behind the design.

## Contributing and questions

Use the [issue tracker](https://github.com/hawkxdev/brief-otter/issues) to discuss a use case, ask a question or propose a focused improvement. Read [CONTRIBUTING.md](CONTRIBUTING.md) before starting substantial work, and use synthetic examples when describing selection behavior. Follow [SECURITY.md](SECURITY.md) for sensitive reports.

Maintained by [hawkxdev](https://github.com/hawkxdev).

## License

[MIT](LICENSE). The software license does not grant rights to third-party Telegram content or accounts.
