# BriefOtter

Find freelance development requests in Telegram without reading every feed yourself.

BriefOtter is a personal monitoring tool being designed for freelancers who follow multiple Telegram channels and chats. The goal is a local list of relevant client requests, each with its original message link and a reason for selection.

**Status:** Design stage. A runnable version is not available yet.

## Planned workflow

1. Read messages from selected channels and chats.
2. Distinguish client requests from service advertisements, resumes and permanent job vacancies.
3. Apply explicit filtering rules and show relevant candidates locally, with source links and selection reasons.

Unclear messages remain marked as uncertain. The first version is intended for read-only collection and rule-based filtering, without posting to Telegram or sending message content to language models.

## Example of the intended selection

These synthetic examples illustrate the planned behavior, not output from a working application.

| Message | Intended result | Reason |
|---|---|---|
| Need a Python developer to build a reporting bot | Candidate for review | A client is asking for project work |
| Python developer available for Telegram bot projects | Filter out | An executor is advertising services |
| Hiring a full-time Python developer | Classify separately | A permanent role is distinct from a freelance project |

## Technology

The selected foundation is [Python](https://www.python.org/) with [Telethon](https://docs.telethon.dev/en/stable/). See the [project guide](.agents/skills/project-guide/SKILL.md) for the monitoring concepts behind the design.

## Contributing and questions

Use the [issue tracker](https://github.com/hawkxdev/brief-otter/issues) to discuss a use case, ask a question or propose a focused improvement. Read [CONTRIBUTING.md](CONTRIBUTING.md) before starting substantial work, and use synthetic examples when describing selection behavior. Follow [SECURITY.md](SECURITY.md) for sensitive reports.

Maintained by [hawkxdev](https://github.com/hawkxdev).

## License

[MIT](LICENSE). The software license does not grant rights to third-party Telegram content or accounts.
