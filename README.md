# BriefOtter

Find development projects and job vacancies in Telegram without reading every feed yourself.

BriefOtter is a personal monitoring tool being designed for people who follow multiple Telegram channels and chats for development work. The goal is a local list of relevant project requests and job vacancies, shown separately with original message links and reasons for selection.

**Status:** An offline foundation is implemented: package setup, command/configuration preflight, local response validation and isolated tests. Message collection, semantic model evaluation and HTML reporting are not implemented yet.

See the [product roadmap](docs/ROADMAP.md) for the planned milestones and first vertical slice.

The [first feature specification](docs/specs/001-local-candidates/spec.md) proposes the detailed behavior for one-source local collection and identifies decisions still needed before implementation.

## Planned workflow

1. Read messages from selected channels and chats.
2. Identify client project requests and job vacancies as separate opportunity categories; filter out service advertisements and resumes.
3. Apply the agreed selection criteria and show relevant candidates locally, with source links and selection reasons.

Unclear messages remain marked as uncertain. The first version keeps read-only collection and local reporting. The [accepted D5 technical basis](docs/adr/0001-local-collection-technical-basis.md) selects semantic AI classification and `glm-5.3-flash` as the first evaluation candidate; actual quality and operational access remain unverified. The [AI contract](docs/specs/001-local-candidates/ai-classification.md) specifies its response shape and limits. Outgoing Telegram actions remain excluded, and real message processing requires separate access/content-use approval.

## Planned verification

The [test execution policy](docs/specs/001-local-candidates/tasks.md#accepted-test-execution-policy) separates tests without AI requests from tests using a real model. The maintainer selects the scope before a run. The implemented tests are synthetic and block external requests and inherited credentials. Real-model cases are not implemented; requesting `--run-ai` fails preflight explicitly. Passing local response validation does not demonstrate model classification quality.

## Local setup

The project pins Python 3.14.10 and its dependencies in `.python-version`, `pyproject.toml` and `uv.lock`. The setup below needs an existing uv launcher, a bootstrap `python3` and package/download access. It installs the selected uv inside the project environment and does not replace the global launcher.

```bash
uv tool run --python python3 --from uv==0.13.7 uv python install 3.14.10
uv tool run --python python3 --from uv==0.13.7 uv sync --locked
source .venv/bin/activate
uv run --locked brief-otter --help
```

The offline foundation is verified on macOS. Linux remains an intended target with no executed platform check; Windows support is outside this first slice.

## Local checks

```bash
./scripts/check.sh
./scripts/check.sh --tests
```

The first command performs formatting/lint, type checks, an offline build, complete wheel/sdist inspection, installed-wheel import and source rebuild. It runs no pytest suite. The explicit `--tests` mode additionally runs the synthetic suite in the working tree and extracted source archive after the maintainer selects that mode. A missing required tool, failed check or empty required test collection makes the runner fail.

Build targets use explicit file lists in `pyproject.toml`. Add intended product/test inputs to those lists when changing the package; the verifier refuses unselected Python source rather than silently dropping it. Unlisted runtime data is kept out of both distribution formats, and required source/test/document bytes are compared against each actual archive.

For a focused run after the same run-mode decision, use `uv run --locked pytest tests/`. `--run-ai` returns an explicit unmet preflight until a later stage implements and separately admits real-model cases. No interactive approval prompt is embedded in pytest.

## Command capability

`brief-otter --help` and `brief-otter collect --help` exit 0 without loading private configuration or credentials. Invalid arguments/configuration or a missing runtime `--allow-ai` opt-in exit 2. With valid synthetic settings, `collect` exits 5 with `collection_not_implemented` before reading credential carriers, constructing a client or replacing any report. The runtime opt-in is distinct from pytest's model-test option and grants no access or spending permission.

Configuration is explicit TOML, validated from a private owner-only location outside the project boundary. Output and attempt-state destinations must have owner-only parents, remain outside that boundary and be distinct; validation resolves parent symlinks and rejects symlink destinations. Run configuration preflight from the project checkout or extracted source tree so its `pyproject.toml` boundary can be established. No `.env` discovery or login flow is implemented. Use synthetic settings for current development; account/session and real-source work retain their separate decisions.

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
