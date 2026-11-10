# Feature 001: Local candidates

## Feature state

**Scope:** [Single-source Local Collection](spec.md), accepted first-run settings, storage and test policy within the proposed Milestone 1 contract. The complete [AI classification proposal](ai-classification.md) is ready for review; no model route is accepted or implemented yet.

**Phase:** `preparing`.

**Evidence:** The maintainer approves the first-run proposal in D1/D2 and the D3 policy of one latest local HTML report with short excerpts and links, replaced by the next run or removed manually, without a separate full-message archive. The maintainer assigns D5 and Russian-example preparation. The resulting [technical proposal](plan.md) and [rules/examples](rules.md) are prepared for review, including requirement mapping and bounded design probes. The preceding public baseline is `f51ab4c21a4c0e4f4b5ee87adcf8612325494699`. No product implementation or collector runtime verification has started.

**Dependencies:** [Decisions D1 through D5](spec.md#decisions-and-open-questions) distinguish accepted settings from open details. The maintainer must accept or amend the prepared plan/rules and the remaining detailed contract before implementation is assigned. The plan explicitly proposes public-channel-only access and POSIX operation for the first implementation; these limits require review rather than implicit scope narrowing. D3 permitted content use and D4 account/API/session/source authorization remain prerequisites for live work. Target-runtime compatibility is not executed. The missing account does not block offline preparation or later separately assigned synthetic implementation.

**Next action:** Review D5's preferred candidate, three-field response, prompt, limits and expected labels. Accept or amend that baseline before assigning implementation. The first model evaluation remains proposed at 45 physical calls/0.50 USD, with no launch authority. The testing architecture/reuse strategy are accepted; model access/quality and D3/D4 prerequisites remain unverified.

**Delivery:** Local documentation only. No issue or PR is created for this package. Commit and publication require approval of the prepared result; final merge remains with the human maintainer.

## Accepted test execution policy

The maintainer requires two separate test groups: tests without AI requests and tests making real AI requests. Before testing, ask whether to run only the no-AI group or the full set including AI requests. The ordinary/default choice excludes AI requests; a generic request to test is not approval for the full set. Reuse an explicit mode choice for that concrete run rather than asking again during it.

The no-AI group must use synthetic inputs and substituted provider replies, with real credential/environment loading disabled and external networking blocked. The AI group exercises the real classifier/prompt on agreed synthetic semantic cases through an explicit opt-in gate. Pagination, identity, rendering and injected failures remain local tests, not automatic additional model requests. Passing substituted replies proves local behavior, not model classification quality. Report passed, skipped/deselected and unexecuted groups separately.

Before a real-model run, present its selected provider/model, case/request count, spending limit and credential boundary for approval. Actual Telegram access keeps its separate source/account/content-use authorization. Neither a test flag nor this policy authorizes a model request, credential access or source collection now. Mode selection happens in conversation, not through an interactive pytest prompt. No tests are implemented or run by recording this policy. [plan.md](plan.md#test-groups-and-execution-mechanism) owns the selected marker/flag and isolation design; donor identity and access limits remain private.
