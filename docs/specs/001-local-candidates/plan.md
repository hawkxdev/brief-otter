# Local candidates: technical proposal

**Decision state:** Complete D5 proposal for review, including the [AI classifier contract](ai-classification.md). The maintainer accepts the test execution policy and scoped reuse of an existing isolation mechanism. The preferred model is an evaluation candidate, not an accepted route or measured winner. No implementation, provider call or live Telegram access is authorized here.

**Requirements:** [spec.md](spec.md), LC-01 through LC-10 and decisions D1 through D5. [tasks.md](tasks.md) alone owns feature progress and the [accepted test execution policy](tasks.md#accepted-test-execution-policy). [rules.md](rules.md) owns expected synthetic labels and a reference rule interpretation. [ai-classification.md](ai-classification.md) owns the proposed model, protocol, failure handling and spending admission; its prompt/schema are linked there. No application or test command described below exists yet.

## Outcome and boundaries

One manual run reads the accessible history of one configured channel for the accepted seven-day interval and replaces one private local HTML report. Projects, vacancies and uncertain items remain separate. The report explains coverage, selection reasons and failures. The proposed implementation uses AI classification with ordinary code computing disposition. No database, persistent history cursor, message archive, background listener or delivery bot is introduced. The earlier rules-only mechanism remains a reference. Collection/rendering stay independent of the model adapter, and real-model evaluation uses separately approved synthetic inputs. A latest cost/attempt-state diagnostic contains no message bodies and serves only spending recovery.

The selected pilot is public. The proposed initial adapter accepts one public channel username and validates that it resolves to a broadcast channel, rather than a user, group, invite link or a list. Private-channel support is not claimed by this proposal. This explicit access restriction needs review with the detailed contract; the real pilot identity stays outside public documents and fixtures.

## Architectural choices

| Choice | Proposal and reason | Alternative and limit |
|---|---|---|
| Runtime and dependencies | Proposed baseline: CPython 3.14.10, Telethon 1.45.0, HTTPX 0.28.1, Pydantic 2.14.3, uv, `pyproject.toml`, `.python-version` and `uv.lock`. Collection/report code otherwise uses the standard library. No model SDK or agent framework is needed. | Dependency/version compatibility is not executed; Stage 1 establishes it before product work depends on it. |
| Execution and data | One asyncio lifecycle, sequential history requests, an in-memory run model and one replaceable HTML report. | SQLite and recovery cursors serve repeated monitoring, outside this slice. A Telethon authorization carrier is separate from message storage. |
| Source adapter | Use Telethon's raw `messages.GetHistoryRequest` through a narrow page interface. Keep page progress and termination decisions in the collector. | `iter_messages()` is convenient, but its inspected early-stop paths hide distinctions required by LC-08. Do not copy Telethon internals or implement another MTProto transport. |
| Selection | Proposed one-message AI classifier, with `glm-5.3-flash` on ordinary Z.ai API as the first evaluation candidate. Validate the three-field response locally, then compute disposition from the rubric. | Candidate quality and current access are unverified. No automatic provider/model fallback or implementation of the older rules-only algorithm. |
| Report publication | Reserve the output with an exclusive local lock, replace the old report with an unfinished-run marker before networking, then atomically replace it with the terminal report. | Keeping an old successful report silently after a new failure violates LC-08. An archive or timestamped history violates D3. |

These are proposed decisions, not ADRs recording accepted architecture. Only this plan owns the technical choices; it links requirements instead of replacing them.

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

These are proposed collection budgets, not Telegram quotas, model-call budgets or account-safety guarantees. Validate positive finite values, integer counts, page size no greater than 100 and sensible relationships before connecting. The interval remains the accepted seven days; a cap never silently shortens the requested interval or becomes successful completion. Classification uses available text before report excerpt truncation. Provider deadlines, retries and spending limits must be designed separately before a real-model run.

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
| `scripts/check.sh` | Future local verification entry, using the selected project standards; no Actions |

These paths are proposed, not files already created. Introduce no web framework, ORM, template engine, bot library or background service. Development dependencies and exact quality-tool pins are resolved in Stage 1 under the project's quality standards. Prompt/schema source stays in this feature package; future packaging derives runtime resources from it and verifies hashes rather than creating a competing editable prompt.

## Test groups and execution mechanism

The normative run/approval rule is owned once at [tasks.md](tasks.md#accepted-test-execution-policy). Groups are classified by actual AI requests, not duration or whether the input mentions AI. A fake model reply belongs to the no-AI group. Real-model cases exercise the actual classifier/prompt and check agreed intent/topic labels and response structure; free-form explanations are not exact-string oracles.

The selected technical pattern is a registered `ai` pytest marker and opt-in `--run-ai` flag. Proposed ordinary command: `uv run --locked pytest tests/`. Proposed full command: `uv run --locked pytest tests/ --run-ai`. Ordinary mode visibly skips AI cases and blocks external requests. Full mode keeps ordinary tests isolated while admitting only the selected AI cases and approved provider scope. A missing route, credential or approved limit in requested AI mode is an explicit unmet preflight, not a green full run with silently skipped model checks. These commands are not implemented or executed.

Ask the maintainer in conversation before invoking pytest; do not put `input()` or another interactive approval inside the runner. The flag enforces the chosen mode but supplies no authorization. Keep imports and collection network-free even with the flag. Read real credentials only in the explicitly admitted model fixture from the approved carrier; never load another application's environment or log values. Bound physical calls, including retries, before a real run.

Use injected provider transports for local replies and errors. Adapt the inspected isolation mechanism to this project's libraries and fields rather than copying a whole application conftest or globally disabling every guard in full mode. Verify blocking with an attempted request, import/collection and subprocess canaries, plus positive controls for ordinary async/local operations. A real-provider test without both the mode gate and case marker must not reach a provider.

EX-01 through EX-15 and RU-01 through RU-30 are proposed semantic expectations for review. TECH-01 through TECH-15 check identity, pagination, failures and rendering locally; they are not automatically extra model calls. Substituted replies prove handling, not model quality. Report run/pass/fail/skip counts and unexecuted boundaries separately. Synthetic evaluation does not authorize sending collected Telegram messages to a model.

The mechanism follows [pytest option-based selection](https://docs.pytest.org/en/stable/example/simple.html#control-skipping-of-tests-according-to-command-line-option) and [test isolation techniques](https://docs.pytest.org/en/stable/how-to/monkeypatch.html#global-patch-example-preventing-requests-from-remote-operations). Marker/flag names and the maintainer's per-run question are project choices, not universal pytest requirements. Donor identity, pinned files and borrowing scope remain private; this document contains no private donor source.

## Stages

Execution and phase remain at [tasks.md](tasks.md). Each stage below describes future work and its exit evidence, not a checked implementation checklist.

<!-- === Stage 1: Reproducible offline boundary === -->
### Stage 1: Reproducible offline boundary

Dependencies: approval of the revised classifier/requirement/plan baseline and a separate implementation assignment. Local work needs no Telegram account. A real-model evaluation requires its own approved route and bounded run.

1. Establish the proposed interpreter, package entry point, complete lock and local quality-tool configuration; prove import/startup compatibility on the target version.
2. Define domain outcomes, identities and nonoverlapping counting fields.
3. Implement configuration validation and command preflight; reject invalid secrets/paths without reading or printing credential values in tests.
4. Verify help, invalid input, boundary/permission checks and offline execution; document actual setup/check commands.

Exit: reproducible local setup, no implicit login/network on preflight, and focused checks for LC-01/LC-09/LC-10. No collector behavior is accepted here.

<!-- === Stage 2: Classification contract and local report === -->
### Stage 2: Classification contract and local report

Dependency: Stage 1's accepted interfaces.

1. Implement the accepted AI contract, typed disposition model and candidate provider adapter from ai-classification.md. The earlier rule interpretation is not an implementation instruction.
2. Add all agreed English and Russian examples as synthetic evaluation data, including contrast pairs and unsupported text.
3. Implement report rendering, exclusive output ownership, unfinished marker and atomic terminal replacement.
4. Verify local handling with substituted replies, reconciliation, HTML/link safety, duplicates and replacement failures. Implement separately marked real-model semantic cases and the isolation gates before requesting a real-model run.

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

On 2026-11-10, [PyPI Telethon 1.45.0](https://pypi.org/project/Telethon/1.45.0/) and the [Python 3.14.10 release](https://www.python.org/downloads/release/python-31410/) identify the proposed versions. [uv locking documentation](https://docs.astral.sh/uv/concepts/projects/sync/) supports explicit locked setup/run commands. The project has no installed Telethon environment; the local observation is Python 3.14.6 and uv 0.9.3, not a completed compatibility test.

The inspected [Telethon wheel](https://files.pythonhosted.org/packages/92/ac/241c09e6905215f225d8088438ceb1f32cc4b4865f3f49068cb402debfd7/telethon-1.45.0-py3-none-any.whl) has SHA-256 `339e24c83aedc9f12cbe389264627edc49779e4289c535aa90aafc4ce62f7972`, verified against PyPI metadata. Selected symbols are `telethon/client/messages.py::_MessagesIter._load_next_chunk/_message_in_range`, `telethon/client/users.py::_call`, `telethon/helpers.py::retry_range` and `telethon/requestiter.py::RequestIter`. This is selected source inspection, not a review of the entire dependency.

An isolated execution of the inspected page-loading/range methods with synthetic objects confirms that a page `[9, 8]` after previous ID 9 ends without yielding 8, whereas `[8, 7]` yields both values. This supports exposing raw page progress instead of treating iterator termination alone as completeness. Standard-library probes also confirm the subsecond offset distinction, the four interval boundary cases and replacing a previous file with an unfinished marker using `os.replace`. These are bounded design probes, not a running collector, live access, filtering accuracy, full crash testing or proof of account safety.

Primary contracts: [messages.getHistory](https://core.telegram.org/method/messages.getHistory), [Telethon raw API](https://docs.telethon.dev/en/stable/concepts/full-api.html), [client options](https://docs.telethon.dev/en/stable/modules/client.html) and [session security](https://docs.telethon.dev/en/stable/concepts/sessions.html). Telegram's [API terms](https://core.telegram.org/api/terms) and [content terms](https://telegram.org/tos/content-licensing) are read for the design boundary; applicability of the intended use, including API sections 1.4 and 3.3, remains part of D3/D4. Reading these pages does not grant collection rights or approve an account.

## Readiness and review boundary

The D5 proposal now specifies the candidate model, prompt/schema, failure handling and call/spend limits at ai-classification.md. Those choices await review; account/operation access, dependency compatibility and real quality are unverified. Implementation requires acceptance of the baseline and an assignment. Model tests require an approved concrete run; Telegram/model-content work additionally requires D3/D4. No provider spend, deployment or external commitment is approved here.

The author checks document coherence and requirement mapping, not an unimplemented classifier. This is self-check, not independent review or maintainer acceptance. Next, review the complete D5 candidate and expected labels before assigning implementation. Commit and publication require approval of the exact outgoing package.
