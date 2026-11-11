# Local candidates: technical plan

**Decision state:** D5 is accepted as the technical basis under [the ADR](../../adr/0001-local-collection-technical-basis.md). The maintainer assigns the bounded Stage 1 offline foundation and selects no-AI verification. The first real-model evaluation candidate remains ordinary-API `glm-5.3-flash` with enabled/low thinking; its access, quality, individual labels and concrete run approval remain separate.

**Requirements:** [spec.md](spec.md), LC-01 through LC-10 and decisions D1 through D5. [tasks.md](tasks.md) alone owns feature progress and the [accepted test execution policy](tasks.md#accepted-test-execution-policy). [rules.md](rules.md) owns expected synthetic labels and a reference rule interpretation. [ai-classification.md](ai-classification.md) owns the selected initial model candidate, protocol, failure handling and spending admission; its prompt/schema are linked there. [README](../../../README.md) identifies the implemented offline commands; collection and real-model commands below retain their later-stage boundaries.

## Outcome and boundaries

One manual run reads the accessible history of one configured channel for the accepted seven-day interval and replaces one private local HTML report. Projects, vacancies and uncertain items remain separate. The report explains coverage, selection reasons and failures. The accepted technical basis uses AI classification with ordinary code computing disposition. No database, persistent history cursor, message archive, background listener or delivery bot is introduced. The earlier rules-only mechanism remains a reference. Collection/rendering stay independent of the model adapter, and real-model evaluation uses separately approved synthetic inputs. A latest cost/attempt-state diagnostic contains no message bodies and serves only spending recovery.

The initial adapter is limited to one public broadcast channel on macOS/Linux under the accepted D5 basis. It accepts a public channel username and validates the peer kind, rather than accepting a user, group, invite link or source list. Private-channel and Windows support are outside this first implementation. The real pilot identity stays outside public documents and fixtures.

## Architectural choices

| Choice | Proposal and reason | Alternative and limit |
|---|---|---|
| Runtime and dependencies | Pinned baseline: CPython 3.14.10, Telethon 1.45.0, HTTPX 0.28.1, Pydantic 2.14.3, uv, `pyproject.toml`, `.python-version` and `uv.lock`. Planned collection/report code otherwise uses the standard library. No model SDK or agent framework is needed. | Stage 1 qualifies imports, CLI preflight and package builds on macOS. Linux, collection and provider compatibility remain unexecuted. |
| Execution and data | One asyncio lifecycle, sequential history requests, an in-memory run model and one replaceable HTML report. | SQLite and recovery cursors serve repeated monitoring, outside this slice. A Telethon authorization carrier is separate from message storage. |
| Source adapter | Use Telethon's raw `messages.GetHistoryRequest` through a narrow page interface. Keep page progress and termination decisions in the collector. | `iter_messages()` is convenient, but its inspected early-stop paths hide distinctions required by LC-08. Do not copy Telethon internals or implement another MTProto transport. |
| Selection | Per-message AI classifier, with `glm-5.3-flash` on ordinary Z.ai API as the first evaluation candidate. Validate the three-field response locally, then compute disposition from the rubric. | Candidate quality and current access are unverified. No automatic provider/model fallback or implementation of the older rules-only algorithm. |
| Report publication | Reserve the output with an exclusive local lock, replace the old report with an unfinished-run marker before networking, then atomically replace it with the terminal report. | Keeping an old successful report silently after a new failure violates LC-08. An archive or timestamped history violates D3. |

The accepted architectural basis is recorded in [the ADR](../../adr/0001-local-collection-technical-basis.md). This plan owns its detailed integration choices and staged implementation checks; the ADR does not duplicate those contracts or claim runtime verification.

## Proposed command and configuration

The intended real collection/classification command is `uv run --locked brief-otter collect --allow-ai --config <private-config.toml>` under separately approved Telegram/content/model scope. Missing `--allow-ai` fails preflight rather than silently enabling a model or falling back to rules. This runtime flag is separate from pytest's `--run-ai`, and neither grants authorization. Help and invalid input make no external calls. Future authorized setup uses the approved interpreter and `uv sync --locked`; dependency upgrades are explicit. Private source/AI configuration stays outside the checkout.

| Input | Contract |
|---|---|
| `source.username` | Exactly one public username, with optional leading `@`; reject URLs with a message path, invite links, lists and empty values. Resolve once per run and validate the peer kind. |
| `source.expected_id` | Optional stable channel ID from separately approved source setup. If supplied, require equality after resolution; a mismatch stops collection. |
| `report.path` | Explicit absolute path ending in `.html`, outside the checkout, in an existing owner-only directory. Reject a symlink destination and unsafe permissions. Do not derive it from a source name. |
| Selection configuration | Explicit model/endpoint/profile and the prompt/schema hashes from ai-classification.md, with run call/time/cost caps. No model/provider fallback, ambient route discovery or implicit AI enabling. |
| Credentials | `BRIEF_OTTER_API_ID`, `BRIEF_OTTER_API_HASH`, `BRIEF_OTTER_SESSION` and proposed `BRIEF_OTTER_AI_API_KEY` arrive only through their separately approved carriers. No key/session is created or borrowed by this plan; no credential CLI arguments or implicit `.env` loading. |

Source configuration and report paths must be checked after resolving parent symlinks against the checkout boundary. If that boundary or ownership cannot be established, fail preflight. Credentials are never echoed, interpolated into errors or included in a report. A missing credential is an explicit preflight failure, not a request for a phone number. An empty or malformed session must not create a new authorization key. The carrier and provisioning procedure remain D4 decisions, not work assigned by this plan.

### Proposed collection budgets

| Setting | Default | Meaning |
|---|---|---|
| `collection.max_messages` | 5000 | Maximum raw history records received, including duplicates, service and unavailable records. Request no more than the remaining allowance. |
| `collection.page_size` | 100 | Maximum records requested in one history page; also constrained by the remaining allowance. |
| `collection.max_pages` | 50 | Maximum history RPCs, including an empty terminal page. This is not a bound on Telethon's connection/authentication protocol traffic. |
| `collection.page_interval_seconds` | 3 | Minimum interval between history request starts; one request at a time. |
| `collection.max_seconds` | 180 | Monotonic deadline for connection, access checks and collection after local preflight. |
| `collection.request_timeout_seconds` | 15 | Bound each awaited access/history operation by this value and the remaining global deadline. |
| `report.excerpt_characters` | 400 | Unicode code points retained from each displayed message; include a visible truncation marker when needed. |

These are proposed collection budgets, not Telegram quotas, model-call budgets or account-safety guarantees. Validate positive finite values, integer counts, page size no greater than 100 and sensible relationships before connecting. The interval remains the accepted seven days; a cap never silently shortens the requested interval or becomes successful completion. Classification uses available text before report excerpt truncation. The AI contract defines provider deadlines, retries and spending admission; the concrete real-model run needs its own approval.

## History and completeness

1. Freeze an aware UTC `end` at run start, including its subsecond precision. Set `start = end - seven days`; membership is `start <= publication_time < end`. Show both exact UTC bounds and their `Europe/Minsk` rendering. Use publication time, not edit or forwarded-original time.
2. Start history reading with `offset_id=0` and an exclusive `offset_date` at the first whole UTC second strictly after `end`. This avoids dropping a message in the same whole second as a subsecond run start. Local interval filtering remains authoritative.
3. On subsequent pages use the smallest positive message ID observed as the exclusive `offset_id`, with `offset_date` unset/zero. Keep `add_offset`, `min_id`, `max_id` and `hash` at zero. Do not use search, filters, comments, scheduled messages or global history.
4. Validate page records against the resolved source and expected descending history order. A short nonempty page is not exhaustion. Deduplicate by `(source_id, message_id)` and continue if the page advances even when its first record repeats. Never infer a missing message from an ID gap.
5. Completion requires reaching a dated record strictly before `start`, or receiving an empty normal history page before a budget/error stop. Process all boundary-equal records. A page with no usable progress, invalid ordering, unsupported response constructor or unavailable records that prevent establishing coverage is partial, not complete. Do not use the API's lifetime total count as the interval denominator.
6. A repeated identity with identical content has one disposition. Conflicting content under one identity during a run retains one entry, marks the run partial and explains the conflict; it is not silently treated as a stable snapshot. Later manual runs always start fresh and use their newly available versions.

The collector interface returns raw page records and an explicit completion/stop reason. `MessageService` records have their own excluded disposition; a regular message without usable text is uncertain, not a downloaded attachment. `MessageEmpty` or an undated record is counted as unavailable; if its interval membership cannot be established, the run remains partial. Unavailable bodies are not reconstructed or archived.

The result distinguishes requested bounds, obtained dated bounds, raw records, duplicates, out-of-window records, unavailable records and distinct analysed messages. Within the interval, distinct analysed messages equal the sum of selected projects, selected vacancies, uncertain messages and mutually exclusive exclusion dispositions. Do not include an unavailable undated record in a denominator whose interval membership is unknown.

## Access, errors and report replacement

Create the client inside the active loop, using the approved nonempty StringSession only. Proposed explicit options are `receive_updates=False`, `catch_up=False`, `request_retries=0`, `connection_retries=0`, `auto_reconnect=False`, `flood_sleep_threshold=0` and `raise_last_call_error=True`. Use `connect()` and an authorization check, never `start()` or an async context manager that starts login. Always disconnect under a bounded cleanup path. These options constrain application/library retries; they do not promise one network packet per operation or change Telegram permissions.

On FloodWait, report the supplied duration and stop the run without sleeping/retrying in a loop or scheduling a new run. Revoked, duplicated, banned or frozen authorization is terminal. A timeout, network error or schema mismatch is visible. Do not use the source failure to join, change account, fetch another source, enumerate dialogs, retrieve sender profiles, acknowledge history, download media or issue outgoing social actions.

| Terminal outcome | Exit | Artifact meaning |
|---|---|---|
| `complete` | 0 | Accessible traversal has a completion proof; empty sections are legitimate and explicit. |
| Invalid command/configuration | 2 | No collection; if a safe output cannot be established, no current report is returned and the diagnostic identifies any existing report as a previous run. |
| `partial` | 3 | A budget, interruption or coverage anomaly stops traversal; preserve observed candidates and the exact stop reason, even with zero candidates. |
| `source_unavailable` | 4 | The configured channel is absent, inaccessible or mismatched; report the access failure rather than an empty completed interval. |
| `failed` | 5 | Authorization, connection, unexpected processing or output failure prevents a valid result. Never print a successful report path for a failed write. |

After output preflight, acquire a nonblocking POSIX advisory lock on an empty reserved lock file in the report directory. A competing run exits before replacing anything. The target platform is the owner's macOS, with Linux as a planned second POSIX target; Windows is not claimed. Under the lock, atomically replace the old report with a small `unfinished` marker carrying this run's ID, start time and requested interval before any network work. A hard interruption leaves that explicit unfinished marker, not the old success. A cooperative interrupt writes a partial or failed result as appropriate and exits nonzero.

Build the terminal report from the in-memory model, write an owner-only temporary file in the same directory, flush and atomically replace the destination. Retain only the latest final report. The empty lock file contains no message content; a reserved pending HTML file exists only during replacement and is removed on handled failure or reclaimed under the lock on the next run. Document this crash residue, without deleting unrelated files. A write/permission failure may leave the previous artifact or unfinished marker; stderr states that no new terminal report was published. Do not claim otherwise.

Escape message text, captions, source labels and reasons as plain text. Construct original-message links from the validated resolved channel username and positive message ID; do not embed URLs extracted from message bodies. Permit only the constructed HTTPS `t.me` destination. No script, embedded remote resource, form or automatic external request is present. Sort each section by descending publication time, then message ID. Labels and reason descriptions are English initially; excerpts keep their source language. Include the run ID, classifier kind and selection-profile version; an AI evaluation also records the actual model and prompt version. Do not include credentials or full message bodies.

## Planned file roles

| Path | Responsibility |
|---|---|
| `pyproject.toml`, `uv.lock`, `.python-version` | Entry point, runtime/dependency contract and reproducible setup |
| `src/brief_otter/cli.py`, `config.py` | Command lifecycle and fail-fast configuration |
| `src/brief_otter/domain.py` | Message identity, decisions, page observations and run outcomes |
| `src/brief_otter/selection.py`, `classification.py`, `ai_client.py` | Per-message orchestration, strict result/disposition model and injected HTTP provider boundary |
| `src/brief_otter/report.py` | Safe rendering, output lock and atomic replacement |
| `src/brief_otter/telegram.py`, `collect.py` | Narrow source adapter and bounded traversal |
| `tests/`, `tests/conftest.py` | Synthetic fixtures, local checks, marked AI cases and test isolation; no real source identity |
| `scripts/check.sh` | Implemented local static/build/distribution checks with explicit test mode; no Actions |

Stage 1 implements the manifests, CLI/configuration, domain/local response validation, synthetic tests and quality scripts. Selection orchestration, provider transport, report rendering and Telegram traversal remain future work. Introduce no web framework, ORM, template engine, bot library or background service. Development dependencies and exact quality-tool pins are resolved in Stage 1 under the project's quality standards. Prompt/schema source stays in this feature package; future packaging derives runtime resources from it and verifies hashes rather than creating a competing editable prompt.

## Test groups and execution mechanism

The normative run/approval rule is owned once at [tasks.md](tasks.md#accepted-test-execution-policy). Groups are classified by actual AI requests, not duration or whether the input mentions AI. A fake model reply belongs to the no-AI group. Real-model cases exercise the actual classifier/prompt and check agreed intent/topic labels and response structure; free-form explanations are not exact-string oracles.

The selected technical pattern is a registered `ai` pytest marker and opt-in `--run-ai` flag. Proposed ordinary command: `uv run --locked pytest tests/`. Proposed full command: `uv run --locked pytest tests/ --run-ai`. Ordinary mode visibly skips AI cases and blocks external requests. Full mode keeps ordinary tests isolated while admitting only the selected AI cases and approved provider scope. A missing route, credential or approved limit in requested AI mode is an explicit unmet preflight, not a green full run with silently skipped model checks. The ordinary command is implemented for synthetic local checks. `--run-ai` is registered but currently fails explicitly before collection because real-model admission and semantic cases belong to Stage 2; no provider evaluation has run.

Ask the maintainer in conversation before invoking pytest; do not put `input()` or another interactive approval inside the runner. The flag enforces the chosen mode but supplies no authorization. Keep imports and collection network-free even with the flag. Read real credentials only in the explicitly admitted model fixture from the approved carrier; never load another application's environment or log values. Bound physical calls, including retries, before a real run.

Use injected provider transports for local replies and errors. Adapt the inspected isolation mechanism to this project's libraries and fields rather than copying a whole application conftest or globally disabling every guard in full mode. Verify blocking with an attempted request, import/collection and subprocess canaries, plus positive controls for ordinary async/local operations. A real-provider test without both the mode gate and case marker must not reach a provider.

EX-01 through EX-15 and RU-01 through RU-30 are proposed semantic expectations for review. TECH-01 through TECH-15 check identity, pagination, failures and rendering locally; they are not automatically extra model calls. Substituted replies prove handling, not model quality. Report run/pass/fail/skip counts and unexecuted boundaries separately. Synthetic evaluation does not authorize sending collected Telegram messages to a model.

The mechanism follows [pytest option-based selection](https://docs.pytest.org/en/stable/example/simple.html#control-skipping-of-tests-according-to-command-line-option) and [test isolation techniques](https://docs.pytest.org/en/stable/how-to/monkeypatch.html#global-patch-example-preventing-requests-from-remote-operations). Marker/flag names and the maintainer's per-run question are project choices, not universal pytest requirements. Donor identity, pinned files and borrowing scope remain private; this document contains no private donor source.

## Stages

Execution and feature phase remain at [tasks.md](tasks.md). The stage scopes and exit criteria below distinguish the implemented offline foundation from later work; they are not evidence of complete Milestone 1 acceptance.

<!-- === Stage 1: Reproducible offline boundary === -->
### Stage 1: Reproducible offline boundary

Dependencies: the accepted D5 technical basis and the assigned S1-01 through S1-09 offline scope. The maintainer selects tests without AI requests for this implementation. No Telegram account or provider credential is needed; real-model evaluation keeps its separate bounded-run approval.

#### Implementation scope

The maintainer assigns this bounded contract for local implementation. Keep this section as the scope/criteria owner; tasks.md links it rather than repeating the checklist. Stage 1 code and synthetic verification do not assign later collection, provider or report work.

The result is an installable local Python package whose command can explain its usage, reject invalid configuration and stop explicitly before unimplemented collection, with local tests unable to contact an external service. Use the runtime/dependency baseline in Architectural choices; dependency setup is implemented with a project-local interpreter/tool environment and a complete lock. Keep development/build tool versions pinned in the manifests. An incompatibility must be reported with its exact package/version evidence before changing the selected runtime or silently falling back.

| Planned paths | Stage 1 responsibility |
|---|---|
| `pyproject.toml`, `.python-version`, `uv.lock` | One reproducible project, declared build backend, entry point and locked runtime/development dependencies |
| `src/brief_otter/__init__.py`, `__main__.py`, `cli.py` | Import-safe package and command lifecycle; no source or model client construction |
| `src/brief_otter/config.py` | Pure validation of explicit settings and fail-fast command preflight, with injected synthetic settings in tests |
| `src/brief_otter/domain.py`, `classification.py` | Used identity/outcome/count types and strict local three-field response validation; no semantic classification or provider adapter |
| `tests/conftest.py`, focused tests | Early credential/network isolation, option/marker registration and distinguishing offline checks |
| `scripts/check.sh` | Explicit local quality entry with failure propagation and separately selected test execution |
| `README.md`, `AGENTS.md`, affected project guide references | Actual implemented setup/check commands and the Stage 1 capability limit, without private configuration or source identity |

Do not introduce database/storage infrastructure, history traversal, the HTTP model adapter, real-provider fixtures, report rendering/replacement, a server, background work, GitHub Actions or another execution service. They are outside this stage. Add only interfaces and types used by the Stage 1 command or its checks; no empty future subsystem or simulated successful collection.

#### Acceptance criteria

| ID | Required outcome and distinguishing evidence |
|---|---|
| S1-01 | Setup selects the declared Python baseline and produces a consistent lock. Package imports, selected library imports, entry-point help and a built wheel work in an isolated local check. Declared versions alone do not pass compatibility. Prove the owner's macOS target; name Linux checks not performed rather than claiming cross-platform verification. |
| S1-02 | Help exits 0 without reading configuration or credentials or making a network request. Unknown arguments, missing/invalid configuration and a missing runtime AI opt-in exit 2. A fully synthetic valid invocation reaches an explicit unimplemented-collection diagnostic and exits 5 before credential-carrier loading, client construction or output replacement; it never reports a completed run. |
| S1-03 | Validation distinguishes missing, valid, invalid and boundary settings under this plan: one public username, positive finite budgets, page/count relationships, admitted endpoint/model and safe output/attempt-state paths. Absolute-path containment checks resolve parent symlinks, reject an unsafe or symlink destination and preserve unrelated files. Pure validation does not establish account/source access. |
| S1-04 | A synthetic secret marker is absent from settings representations, validation errors, captured command output and traceback diagnostics. Imports/help/collection do not load `.env`, production Telegram/source configuration, another application's environment or a real secret carrier. No real credential value is needed to verify this boundary. |
| S1-05 | Identity distinguishes equal versus different `(source_id, message_id)` pairs. Used count/outcome types reject invalid states and preserve the nonoverlapping categories from this plan. Strict response validation matches classification.schema.json, including extra/missing fields, types/enums, blank/overlong reasons, duplicate JSON keys, nonfinite literals and trailing content. These are local shape checks, not model-quality tests. |
| S1-06 | A default-on test boundary blocks attempted socket/DNS/HTTP and command-based external requests before any request process/send occurs, including import/collection and test-owned subprocess canaries. It strips inherited credential inputs and disables implicit environment-file discovery early enough for collection. Positive controls preserve ordinary local subprocesses, file I/O and asyncio/socket-pair operation. |
| S1-07 | Register `ai` and `--run-ai` without enabling networking or credential discovery for unmarked tests. Selecting the flag alone leaves imports/collection and ordinary tests isolated. The actual provider fixture and semantic group belong to Stage 2. Requesting full mode before an eligible model group/admission fixture exists returns an explicit nonzero preflight failure without loading credentials. An empty model group cannot establish a passed full evaluation. No real request is needed or permitted for Stage 1 checks. |
| S1-08 | The quality entry runs Ruff formatting check/lint, mypy and the declared package build, and fails on a missing required tool or failed check. Python style uses a 79-character line limit and single-quote formatting; type exceptions need inspected evidence and narrow scope. Tests are an explicit runner mode following the maintainer's conversation choice. When the required Stage 1 tests are selected, zero collected tests is failure, not a successful scaffold exception. |
| S1-09 | README and project instructions name only commands actually implemented and checked, show the absence of a collector/provider runtime, and preserve the no-AI/full-run approval policy. Report exact Python/tool versions, commands, exit codes, test counts and unperformed platform/runtime checks on the result revision. |

The implemented runner default performs static/build checks only. An explicit `--tests` mode adds the default no-AI suite after the maintainer selects that mode in conversation. Future real-model mode remains governed by tasks.md and `--run-ai`; it is not enabled by this stage. Missing SDK typing is not an automatic global mypy exception: inspect built-in and separately supplied typing for the selected release before a scoped override.

#### Verification and delivery boundary

README owns the implemented project-local bootstrap and locked setup commands. `scripts/check.sh` qualifies static checks and actual wheel/sdist contents with offline build/rebuild and installed-wheel import. Explicit `--tests` additionally checks the working tree and extracted source. Dependency setup may download declared packages; it does not approve inference, Telegram access, a global tool upgrade or credential operations.

For isolation guards, retain the original blocked attempt and a contrasting local-operation control. Show that removing the relevant guard makes its intended canary fail; a globally broken event loop or an always-failing test is not evidence of correct isolation. All such tests are synthetic and require the maintainer's chosen test mode before execution.

The current local lead implements this coherent offline boundary directly, without another agent or cloud execution. Return a scoped PR and current-head evidence under the project's commit/publication gates, with merge separately approved. D3/D4 and the individual semantic label review do not block offline setup preparation; they still block their dependent live/model evaluation work.

Exit: evidence for S1-01 through S1-09 on the actual implementation revision, covering the offline parts of LC-01/LC-09/LC-10 and response shape. This does not accept collector behavior, semantic quality, source coverage or a complete Milestone 1 result.

<!-- === Stage 2: Classification contract and local report === -->
### Stage 2: Classification contract and local report

Dependency: Stage 1's accepted interfaces.

1. Reuse Stage 1's local response types, then implement the accepted AI transport/orchestration contract, final disposition and candidate provider adapter from ai-classification.md. The earlier rule interpretation is not an implementation instruction.
2. Add all agreed English and Russian examples as synthetic evaluation data, including contrast pairs and unsupported text.
3. Implement report rendering, exclusive output ownership, unfinished marker and atomic terminal replacement.
4. Verify local handling with substituted replies, reconciliation, HTML/link safety, duplicates and replacement failures. Extend Stage 1's isolation with explicitly admitted provider fixtures and separately marked semantic cases before requesting a real-model run.

Exit: local handling aspects of LC-02 through LC-07 and report aspects of LC-08/LC-10 have no-AI evidence. Actual model classification quality remains unverified until the separately approved semantic group runs and is assessed. Expected labels are independent of implementation and subject to review; no Telegram-source accuracy is claimed.

<!-- === Stage 3: Bounded source traversal === -->
### Stage 3: Bounded source traversal

Dependency: Stage 2's accepted domain/report contracts. Fake source responses do not require a Telegram account.

1. Implement the narrow Telethon adapter and explicit retry/access boundary.
2. Implement page progress, exact interval filtering, budgets, anomaly detection and run finalization.
3. Verify the command end to end against a page fake that can fail, repeat, return short pages or expose unavailable records; spy on the adapter's permitted calls.
4. Run current-head local checks for every acceptance row below and review the result under the selected project route.

Exit: all local integration criteria have evidence on an identifiable revision, with real-model semantics clearly separated. A passed approved model group is required before model classification is qualified; only then request the separately gated source/content usefulness check. Neither gate permits login or real collection by itself.

<!-- === Stage 4: Maintainer usefulness decision === -->
### Stage 4: Maintainer usefulness decision

Dependencies: explicit live-work assignment, D3 content-use decision, D4 account/API/session/source authorization and accepted offline result. Source setup and account creation remain separately scoped operations.

1. Prepare the exact bounded live protocol and verify that the approved account, source, carrier, paths and collection budget match it, without exposing secrets.
2. Perform only the authorized one-source run; retain the latest private report and record actual access/completeness evidence.
3. Have the maintainer assess correct, irrelevant and missed findings in the agreed sample, with projects and vacancies evaluated separately; record absent categories as not evaluated.

Exit: a supported usefulness decision or exact remaining limitations. A vacancy-oriented sample does not establish live project-request quality. No second source, automatic resumption, deployment or publication follows from this stage.

## Acceptance mapping

| Requirement | Required distinguishing evidence |
|---|---|
| LC-01 | UTC/Minsk bounds, subsecond upper guard, inclusive lower/exclusive upper boundary and invalid interval/configuration |
| LC-02 | Caption, empty text and external-link-only cases; no external fetch, OCR, media download or sender enrichment |
| LC-03 | Local decision handling with substituted replies; separate real-model semantic cases for agreed labels, negation and mixed/uncertain evidence |
| LC-04 | All five directions, non-Python examples, explicit mismatch and uncertain topic; an attributable rule change |
| LC-05 | Three sections, required display fields, explicit emptiness, stable order and count reconciliation |
| LC-06 | Repeated identity once, distinct IDs with equal text retained and repeatable local processing of identical inputs/replies; model stability reported separately |
| LC-07 | Changed current text on a new run, missing message without a deletion claim and separate cross-post identities |
| LC-08 | Proven empty interval versus inaccessible source; short page, duplicate page, no progress, cap, timeout, interrupt and old-report replacement failure |
| LC-09 | Invalid/revoked authorization and FloodWait stop without login, join, source/account switch or outgoing action; opt-in live evidence separately |
| LC-10 | HTML/link injection, unsafe paths/permissions, no external page resources, no secret/source leakage in public fixtures and no message archive |

## Evidence behind the proposal

On 2026-11-10, [PyPI Telethon 1.45.0](https://pypi.org/project/Telethon/1.45.0/) and the [Python 3.14.10 release](https://www.python.org/downloads/release/python-31410/) identify the proposed versions. [uv locking documentation](https://docs.astral.sh/uv/concepts/projects/sync/) supports explicit locked setup/run commands. The earlier preparation environment used Python 3.14.6 and uv 0.9.3. Stage 1 installs the selected Python 3.14.10 and project-local uv 0.13.7, with local selected-library import checks. This qualifies the offline foundation on macOS, not provider access, Linux execution or Telegram history.

The inspected [Telethon wheel](https://files.pythonhosted.org/packages/92/ac/241c09e6905215f225d8088438ceb1f32cc4b4865f3f49068cb402debfd7/telethon-1.45.0-py3-none-any.whl) has SHA-256 `339e24c83aedc9f12cbe389264627edc49779e4289c535aa90aafc4ce62f7972`, verified against PyPI metadata. Selected symbols are `telethon/client/messages.py::_MessagesIter._load_next_chunk/_message_in_range`, `telethon/client/users.py::_call`, `telethon/helpers.py::retry_range` and `telethon/requestiter.py::RequestIter`. This is selected source inspection, not a review of the entire dependency.

An isolated execution of the inspected page-loading/range methods with synthetic objects confirms that a page `[9, 8]` after previous ID 9 ends without yielding 8, whereas `[8, 7]` yields both values. This supports exposing raw page progress instead of treating iterator termination alone as completeness. Standard-library probes also confirm the subsecond offset distinction, the four interval boundary cases and replacing a previous file with an unfinished marker using `os.replace`. These are bounded design probes, not a running collector, live access, filtering accuracy, full crash testing or proof of account safety.

Primary contracts: [messages.getHistory](https://core.telegram.org/method/messages.getHistory), [Telethon raw API](https://docs.telethon.dev/en/stable/concepts/full-api.html), [client options](https://docs.telethon.dev/en/stable/modules/client.html) and [session security](https://docs.telethon.dev/en/stable/concepts/sessions.html). Telegram's [API terms](https://core.telegram.org/api/terms) and [content terms](https://telegram.org/tos/content-licensing) are read for the design boundary; applicability of the intended use, including API sections 1.4 and 3.3, remains part of D3/D4. Reading these pages does not grant collection rights or approve an account.

## Readiness and review boundary

The D5 technical basis is accepted and the assigned offline foundation is implemented locally. Local verification covers imports, preflight, pure response shape and test/build boundaries on macOS. It does not establish model access/quality, semantic label acceptance, Linux execution or Telegram coverage. Stage 2 and later implementation need their own assignments; real-model tests and source/content work keep their concrete run and D3/D4 gates.

Local checks and focused guard probes are author verification, not independent review or full feature acceptance. Review the Stage 1 result before continuing to Stage 2. Commit and publication require approval of the exact changed package.
