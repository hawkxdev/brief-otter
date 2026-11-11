# Feature 001: Local candidates

## Feature state

**Scope:** [Single-source Local Collection](spec.md), with accepted first-run settings, storage, test policy and the [accepted D5 technical basis](../../adr/0001-local-collection-technical-basis.md). The detailed requirement table and individual expected labels retain their review state; the selected model candidate is not implemented or qualified.

**Phase:** `in_progress`.

**Evidence:** D5 acceptance is delivered through PR 3. The maintainer then assigns the prepared S1-01 through S1-09 contract for direct local implementation and explicitly selects tests without AI requests. The offline package, command/configuration preflight, local response types, test boundary and build/quality scripts are implemented. Current result verification and delivery retain separate evidence; no collection or real-model evaluation has started.

**Dependencies:** The scoped offline result targets Python 3.14.10 with project-local uv 0.13.7 and locked dependencies. macOS qualification is local; Linux has no executed platform check. Individual EX/RU labels, model access/quality and D3/D4 constrain later semantic/live work, not this offline foundation. No source account or real credential is used by the current synthetic checks.

**Next action:** Review the bounded Stage 1 result against S1-01 through S1-09 and approve its exact Git delivery when ready. The rest of feature 001 remains unimplemented; Stage 2 needs a separate assignment. Reuse the maintainer's selected no-AI mode for this concrete implementation verification; a real-model run still needs its manifest and spending/credential approval.

**Delivery:** The accepted design baseline is PR 3 at `77ef04789a43d61410c48c63599faaff00c58f83`, after PR 2. Stage 1 adds the offline foundation; report generation, collection and real-model evaluation remain undelivered. Its implementation uses the project's scoped PR route, with commit/publication and final merge retaining their respective maintainer gates.

## Accepted test execution policy

The maintainer requires two separate test groups: tests without AI requests and tests making real AI requests. Before testing, ask whether to run only the no-AI group or the full set including AI requests. The ordinary/default choice excludes AI requests; a generic request to test is not approval for the full set. Reuse an explicit mode choice for that concrete run rather than asking again during it.

The no-AI group must use synthetic inputs and substituted provider replies, with real credential/environment loading disabled and external networking blocked. The AI group exercises the real classifier/prompt on agreed synthetic semantic cases through an explicit opt-in gate. Pagination, identity, rendering and injected failures remain local tests, not automatic additional model requests. Passing substituted replies proves local behavior, not model classification quality. Report passed, skipped/deselected and unexecuted groups separately.

Before a real-model run, present its selected provider/model, case/request count, spending limit and credential boundary for approval. Actual Telegram access keeps its separate source/account/content-use authorization. Neither a test flag nor this policy authorizes a model request, credential access or source collection now. Mode selection happens in conversation, not through an interactive pytest prompt. Recording this policy alone never authorizes a test run; the implemented synthetic group is selected separately from real-model work. [plan.md](plan.md#test-groups-and-execution-mechanism) owns the selected marker/flag and isolation design; donor identity and access limits remain private.
