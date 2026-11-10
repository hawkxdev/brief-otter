# Feature 001: Local candidates

## Feature state

**Scope:** [Single-source Local Collection](spec.md), with accepted first-run settings, storage, test policy and the [accepted D5 technical basis](../../adr/0001-local-collection-technical-basis.md). The detailed requirement table and individual expected labels retain their review state; the selected model candidate is not implemented or qualified.

**Phase:** `preparing`.

**Evidence:** The maintainer accepts D1/D2, D3 storage, the test policy and D5 as the six-point technical basis against published design baseline `3ac5013bbff5009440ea711b9ec8a12e957571d5`. [The ADR](../../adr/0001-local-collection-technical-basis.md) records the decision and its limits. The plan, AI contract and prompt/schema remain the design owners. No product implementation or collector runtime verification has started.

**Dependencies:** D5 now selects one public broadcast channel, macOS/Linux, semantic AI classification, the ordinary Z.ai candidate and one replaceable HTML report. Individual EX/RU labels and the remaining detailed requirement criteria need review before their dependent evaluation/implementation. Target-runtime compatibility and the selected route's current access/quality remain unverified. D3 permitted content use and D4 account/API/session/source authorization constrain live work, while offline preparation can continue.

**Next action:** Prepare the bounded Stage 1 implementation assignment from the accepted D5 basis and resolve the detailed criteria needed by that stage. Implementation is not assigned by design acceptance. The planned 45-case/0.50 USD model evaluation requires its reviewed manifest and separate run, spending and credential approval.

**Delivery:** The preceding design proposal is delivered through [PR 2](https://github.com/hawkxdev/brief-otter/pull/2) in `3ac5013bbff5009440ea711b9ec8a12e957571d5`. This documentation update records subsequent D5 acceptance and reconciles its decision states. A runnable collector, operational qualification and model evaluation remain undelivered. Future commits/publication and final merges retain their respective maintainer gates.

## Accepted test execution policy

The maintainer requires two separate test groups: tests without AI requests and tests making real AI requests. Before testing, ask whether to run only the no-AI group or the full set including AI requests. The ordinary/default choice excludes AI requests; a generic request to test is not approval for the full set. Reuse an explicit mode choice for that concrete run rather than asking again during it.

The no-AI group must use synthetic inputs and substituted provider replies, with real credential/environment loading disabled and external networking blocked. The AI group exercises the real classifier/prompt on agreed synthetic semantic cases through an explicit opt-in gate. Pagination, identity, rendering and injected failures remain local tests, not automatic additional model requests. Passing substituted replies proves local behavior, not model classification quality. Report passed, skipped/deselected and unexecuted groups separately.

Before a real-model run, present its selected provider/model, case/request count, spending limit and credential boundary for approval. Actual Telegram access keeps its separate source/account/content-use authorization. Neither a test flag nor this policy authorizes a model request, credential access or source collection now. Mode selection happens in conversation, not through an interactive pytest prompt. No tests are implemented or run by recording this policy. [plan.md](plan.md#test-groups-and-execution-mechanism) owns the selected marker/flag and isolation design; donor identity and access limits remain private.
