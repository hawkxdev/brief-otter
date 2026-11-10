# D5: AI classification proposal

**Decision state:** Complete proposal for maintainer review, not an accepted model assignment or authorization to install dependencies, implement, read credentials or make requests. The maintainer assigns preparation of the model, response contract, failure handling and call limits. [spec.md](spec.md) owns requirements; [tasks.md](tasks.md) owns feature state and the accepted run-confirmation policy. [plan.md](plan.md) links collection/report integration to this document.

## Proposed choice and evidence

Use an AI classifier as the proposed first implementation, with deterministic application code handling identity, disposition, budgets and HTML. The preferred initial evaluation candidate is `glm-5.3-flash` through Z.ai's ordinary metered API at `https://api.z.ai/api/paas/v4/chat/completions`. Coding Plan is a different product and is not a substitute. Account eligibility, balance, a BriefOtter credential and this exact operation remain unverified; no credential value is read during preparation.

| Candidate | Evidence and fit | Disposition |
|---|---|---|
| Z.ai `glm-5.3-flash` | The official model page documents JSON output and a 1M context. The ordinary API and existing integration knowledge support a small stateless JSON client. Thinking is mandatory; use its supported `low` effort rather than an unsupported off setting. | Preferred candidate for the first bounded evaluation, not a quality winner. |
| Z.ai GLM-4.7-Flash family | The official price list lists a free API tier and the family documents JSON output. The exact serving ID/access needs verification before an optional run; free price does not establish equivalent Russian quality. | Secondary candidate only for another separately scoped evaluation; no automatic fallback. |
| Z.ai `glm-5.3` | The published token rates are higher; its coding/agent positioning does not establish better results for this short taxonomy. | No initial need to spend more without relevant evidence. |

The choice is an engineering starting hypothesis, not a measured ranking. No A/B, quality, latency or current access result is claimed. A future change of model, effort, prompt or provider needs a new identified evaluation; it is not a transparent fallback. Keep the prompt short rather than importing another application's pricing, eligibility or long-form analysis policy.

Sources inspected on 2026-11-10: [model and supported thinking](https://docs.z.ai/guides/vlm/glm-5.3-flash), [ordinary Chat Completion API](https://docs.z.ai/api-reference/llm/chat-completion), [reasoning parameters](https://docs.z.ai/guides/overview/concept-param), [JSON output](https://docs.z.ai/guides/capabilities/struct-output), [pricing](https://docs.z.ai/guides/overview/pricing), [Coding Plan scope](https://docs.z.ai/devpack/faq) and [API data-processing terms](https://docs.z.ai/legal-agreement/privacy-policy#data-processing-addendum-for-api-services). The API documentation identifies the ordinary endpoint; a model page showing a coding endpoint does not change this billing product. The provider's API privacy statement is not independently verified account-specific retention evidence or permission to process Telegram content. D3/D4 still govern real data.

## Data flow and client boundary

For each distinct normal message with available text: normalize its source identity/time locally, retain the text in memory, invoke one classifier request, validate the reply, compute disposition in ordinary code and render the approved report fields. Do not keyword-prefilter potentially useful text before classification. Service records and duplicate deliveries need no model call. Empty available text produces a local uncertain result without a call; do not download media or fetch links to fill it.

Use one `httpx.AsyncClient`, one outstanding request and a transport that can be replaced in local tests. Proposed direct dependencies are HTTPX 0.28.1 and Pydantic 2.14.3, from [HTTPX metadata](https://pypi.org/pypi/httpx/0.28.1/json) and [Pydantic metadata](https://pypi.org/pypi/pydantic/2.14.3/json). Lock transitive dependencies with uv in the future implementation. No OpenAI/Z.ai SDK, agent framework or automatic SDK retry is required. These versions and the target Python 3.14.10 are proposed, not installed or compatibility-tested here.

The client uses the exact approved HTTPS host/path with certificate verification, no redirects, no ambient proxy/credential discovery, and zero automatic application/transport retries. An alternate endpoint requires a new route decision, not a config fallback. Source input is serialized as the `text` value of one user message, with the [system prompt](classifier-prompt.md) supplied separately. Each call is independent: no tools, search, conversation history or source/account metadata is appended. Keep the correlation ID, message identity and expected labels outside the model input.

Proposed private settings are `ai.endpoint`/`ai.model` matching the admitted route, positive integer `ai.max_calls`, positive finite `ai.deadline_seconds`, positive decimal-string `ai.budget_usd` and absolute owner-only `ai.state_path` outside the checkout. Prompt/schema versions are derived from the packaged sources, not a hidden override. The proposed credential variable is only `BRIEF_OTTER_AI_API_KEY`; no project credential is created here and no existing application's key is assumed reusable. Model tests construct a source-independent evaluation profile and do not load production Telegram/source configuration. Their effective limits and journal location must match the approved run packet.

## Response contract

[classification.schema.json](classification.schema.json) is the normative local JSON shape. It is not submitted as unsupported provider `json_schema`; Z.ai's documented mode is `response_format={"type":"json_object"}`. A future Pydantic model uses strict validation and forbids extra fields, with conformance checks against this schema.

| Field | Allowed values and meaning |
|---|---|
| `intent` | Exactly one of `project_request`, `job_vacancy`, `executor_ad`, `resume`, `editorial`, `uncertain`, as defined in the system prompt and example rubric |
| `topic` | `match`, `no_match` or `uncertain`, independently of intent, against the accepted five-direction profile |
| `reason` | Nonblank English plain text of at most 240 Unicode characters, grounded in the input; no invented terms or chain of thought |

Parse exactly one JSON object after trimming surrounding whitespace. Reject duplicate keys, NaN/Infinity, extra/trailing objects, Markdown fences, missing keys, extra keys, invalid enums, wrong types and blank/overlong reasons. Do not extract a convenient JSON substring, repair a malformed reply by another paid call or parse `reasoning_content` as the answer. Local shape validation does not establish semantic correctness.

The application computes the final section using [the disposition table](rules.md#terminal-disposition-and-precedence); the model does not supply an action or URL. Preserve both dimensions even when one exclusion decides the final disposition. Evaluate intent and topic separately so a correct overall exclusion cannot hide a wrong component. Original links are constructed locally from validated source metadata, never generated by the model.

## Proposed request parameters and limits

| Parameter | Proposal | Boundary |
|---|---|---|
| Model and product | `glm-5.3-flash`, ordinary metered Z.ai API | No Coding Plan endpoint or silent model/provider switch |
| Thinking | `thinking.type=enabled`, `reasoning_effort=low`, cleared prior thinking | Do not send `disabled`, `none` or other unsupported effort values |
| Output | Nonstreaming, JSON-object mode, `max_tokens=4096`, temperature 1, top_p 0.95 | Reasoning remains enabled. Qualification checks completion accounting; cost admission conservatively reserves the published full 128K output ceiling instead of relying on the lower request value. Do not add reasoning usage twice |
| Input | At most 12000 source code points and 65536 serialized request UTF-8 bytes including prompt/envelope | Reject oversized input locally without truncating it into a misleading classification; these are byte/character limits, not claimed token counts |
| Response body | At most 1 MiB | Stop reading oversized responses; usage may then be unknown |
| Per-request deadline | 60 seconds, bounded by remaining phase deadline | An outer asyncio deadline covers all awaited phases, not only a socket read timeout; cleanup is bounded and cancellation is propagated |
| Concurrency and spacing | One outstanding request; at least one second between request starts | Application pacing, not a provider quota guarantee |
| Retries | Zero | Failure/retry/recovery consumes a separately approved physical call if later authorized |

One response must have the expected served model, one nonempty completion, `finish_reason=stop`, no tool call/refusal frame and a valid local result. The first scheduled evaluation case also checks this wire contract and accounting; no extra handshake request is added. A mismatch stops qualification. The current route cannot be called verified until that authorized sample succeeds.

## Failure and report semantics

| Condition | Result and continuation |
|---|---|
| Empty text | Local semantic uncertainty, no request; source text remains unavailable rather than downloaded |
| Oversized input or exhausted call/time/cost limit | No request; mark the item unclassified with a local reason and make the run partial |
| Invalid JSON/schema, truncation or empty completion | No trusted model classification; preserve the item in the uncertain section with a technical-error label |
| HTTP 401/403, insufficient balance, rate limit or provider/network failure | Stop the model phase without retry, login, provider switch or fallback; already obtained observations remain visible |
| Timeout, cancellation, interrupted sent attempt or absent/invalid usage | Stop further requests and retain the conservative reserved amount as unknown spend; no automatic replay/resume |
| Valid structure but wrong expected label | Evaluation failure, not a transport error. Record the disagreement and continue only within the approved evaluation scope |

For a provider failure, do not partially trust a valid-looking intent from an otherwise invalid object. Code supplies an uncertain technical result with a stable error code. Do not log credential headers, raw provider error text or chain-of-thought content. Render model reasons as escaped text. Inspect both HTTP status and the provider's `error.code`: the [official error contract](https://docs.z.ai/api-reference/api-code) distinguishes 429/1113 (balance or missing resource package), 429/1302 (rate limit) and 429/1305 (overload). Authentication/permission errors stop access; invalid model/parameters or code 1315 leave the product/route unqualified. Never infer an exact balance from a code. Unknown shapes/codes stay unknown; no provider suggestion to retry/contact support overrides this run's authority.

Track collection coverage and classification coverage separately. A complete history traversal plus unclassified/model-error items is an overall partial result, not a successful empty selection. Show valid model decisions, semantic uncertainties, technical failures and unattempted items separately. Every observed normal message still has one report disposition; a budget stop must not silently remove the remaining messages or call them irrelevant.

## Run budgets and spending admission

All values below are proposals awaiting the maintainer's concrete run approval. They authorize no request now. A published token-cost estimate is not an invoice, account balance or subscription entitlement.

| Run | Physical request cap | Token-cost admission cap | Phase time |
|---|---|---|---|
| First full semantic evaluation | 45, one pass over EX-01 through EX-15 and RU-01 through RU-30 after labels are accepted | 0.50 USD | 1800 seconds maximum |
| Later first source run | 100, at most one attempt per distinct eligible message | 1.00 USD | 900 seconds for classification, separately from the proposed 180-second source budget |

The full test run also includes no-AI tests; TECH-01 through TECH-15 do not add model calls. Repetitions, A/B candidates, repairs and retries are not included. A request for repetitions changes the physical count and needs its own scoped approval. Stop at whichever admitted limit is reached first; caps do not promise all cases/messages will finish.

The observed ordinary rates are 0.15 USD per million input tokens and 0.50 USD per million output tokens. Ignore cache discounts in admission estimates. With the explicit illustrative assumption of 2500 prompt tokens per case, 45 cases cost 0.039915 USD at 1024 output tokens each or 0.109035 USD at 4096 each. These are computed scenarios, not measured usage or forecasts of thinking length. The proposed 0.50 USD cap applies to token charges at frozen rates, excluding top-up fees/taxes. Recheck prices/product/limits before approving a real run.

Before sending, durably reserve the conservative whole-model charge: 1048576 input tokens at the uncached rate plus 131072 output tokens, giving 0.2228224 USD per admitted call. These allowances cover binary readings of the published 1M/128K ceilings; they are billing reserves, not actual payload size or an instruction to request that output. Reserving the full output ceiling avoids depending on an unqualified assumption about how the lower requested limit interacts with reasoning. Admit a call only when recorded estimated spend, outstanding reserves and the next reserve fit the approved cap. Replace a reserve with an estimate from validated aggregate usage; count completion tokens once and do not count a cached subset in addition to prompt tokens. Missing usage is not zero. A provider/accounting contract outside these bounds leaves qualification incomplete.

Evaluation evidence belongs in an owner-only private run journal identified by corpus, prompt, schema, route and parameter hashes. Record reservation before possible send, then known result/usage or unknown spend. On restart an unresolved sent attempt blocks further calls; do not replay it from a failed test. A source run needs only the latest private cost/attempt-state diagnostic, without message bodies, history cursors or an accumulating inbox. Keep this small non-message diagnostic separate from the replaceable HTML, with exclusive ownership and atomic writes. Its purpose is spending recovery, not a second financial ledger or message archive. The exact output locations remain explicit private configuration.

## Evaluation and implementation checks

The no-AI suite uses substituted replies and injected HTTP transports to cover all enum values/dispositions, strict schema failures, request bytes/parameters, no redirect/retry, deadline/cancellation, empty/oversized input, budget reservation/recovery and report reconciliation. Isolation checks must prove that imports, collection and unmarked tests cannot reach a real provider even when full mode is selected. Test fixtures contain no real API key or source content. The feature prompt/schema are the editable source of truth; future packaging derives runtime text/schema resources, verifies their hashes and excludes the surrounding development instructions.

The separately marked AI group runs the same actual prompt/schema and adapter on accepted semantic cases. Expected labels are not sent to the model. Compare intent/topic independently and inspect reason grounding rather than exact wording. A full pass requires every case in the approved full manifest, not only an admitted/completed prefix, to have an actual result and satisfy its agreed assertions. Skipped, unknown, budget-stopped or unrun cases do not establish a full pass. All 45 proposed labels need review before execution. They form a regression/screening set, not an independent market sample or unseen-quality proof; later validation needs separately held inputs, and one pass does not establish stability.

Stage 1 establishes version/import compatibility, the response model and the no-network test gate. Stage 2 implements this candidate adapter and classifier-independent result handling with local tests; code routes no-AI fixtures without invoking the live adapter. Stage 3 integrates bounded collection and these model-phase outcomes. Real-model tests and the later Telegram usefulness check remain separately approved runs. No runtime tests are executed by preparation of this document.

## Remaining decisions

The D5 design proposal is ready for review. Acceptance must name this candidate/contract or amend it; account access and spending are separate decisions. A BriefOtter-scoped ordinary-API credential, account/product eligibility and current operation access remain unverified. Real model calls need the accepted example labels, exact run packet and spending/credential approval. Collected Telegram content additionally requires D3/D4 resolution. No dependency install, paid call, source collection, commit or publication follows from this proposal alone.
