# Product Vision and Roadmap

BriefOtter aims to turn selected Telegram feeds into a useful local list of development project requests and job vacancies, shown separately with original message links and reasons for selection. See the [README](../README.md) for the product introduction.

## Current state

The offline foundation implements package setup, command/configuration preflight, local response validation and synthetic test isolation. Versions are pinned in the project manifests; README owns setup/check commands. A runnable collector, model evaluation and HTML reporting are not available, and Milestone 1 is not accepted by this foundation result.

The product direction and first vertical slice below are agreed, including both projects and vacancies. [D5 is accepted as the technical basis](adr/0001-local-collection-technical-basis.md), with its first AI evaluation candidate and local-report approach. Detailed requirement rows and individual expected labels retain their review state. Implementation and real-run permissions remain separate; feature packages own their criteria and plans.

## Milestones

| Milestone | User outcome | Evidence needed before progressing |
|---|---|---|
| **1. First useful results** | One local run reads an agreed source and produces separate selections of project requests and vacancies | The complete scenario works; contrasting selection examples, repeated delivery and unavailable-source behavior are checked; the maintainer assesses whether the result is useful |
| **2. Reliable repeated use** | Multiple agreed sources, saved processing positions and recovery after interruptions support repeated collection | Stop and resume cases are checked; incomplete results and uncovered periods are visible; repeated processing preserves message identity |
| **3. Continuous local monitoring** | New candidates appear without manually starting every collection; source health and errors are visible | Shutdown, restart and recovery are checked; update latency and the operating procedure are agreed |
| **4. Convenient daily review** | Configurable selection profiles and local viewed/hidden markers help review new candidates | Feedback identifies which improvements help the real workflow; unnecessary features are excluded |

Milestones build on the preceding evidence. A failed usefulness check returns the selection rules or first-slice scope for revision before expanding automation. Later details remain subject to what earlier use reveals.

Reproducible setup, safe configuration, focused checks and public documentation accompany every milestone. They are part of each delivery rather than deferred to a final documentation phase.

## First vertical slice

The recommended first result is a manually started collection from one agreed, accessible channel, followed by a local HTML table. This provides an early opportunity to evaluate selection usefulness before introducing continuous operation.

The end-to-end scenario is:

1. The user starts a local collection command. Its exact interface belongs to the feature package.
2. The collector reads an agreed range of messages from one selected channel.
3. The agreed classifier identifies client project requests and job vacancies as separate opportunity categories, distinguishes executor advertisements and resumes, and preserves uncertain messages. The accepted D5 basis selects semantic AI classification, with implementation and actual model qualification still pending.
4. A topic filter selects candidates within the agreed interests.
5. A local HTML table presents project requests and vacancies separately, with source, publication time, category, selection reason and original message link. Uncertain messages have their own section.
6. Processing the same message again does not create another copy. An inaccessible source or incomplete collection is reported visibly.

The slice includes the whole path from source to a reviewable result. It excludes continuous execution, server deployment, delivery notifications, CRM integration, a full web interface and complex grouping of cross-posts. The exact data retained and its lifetime must be agreed before live collection.

### Validation

Use contrasting synthetic examples: a relevant client request, an executor advertisement using the same technologies, a permanent vacancy, an unclear message and a repeated delivery. Check that the output preserves the original link and selection reason, retains uncertainty and exposes incomplete collection rather than presenting it as an empty result.

Apply the [accepted test execution policy](specs/001-local-candidates/tasks.md#accepted-test-execution-policy). Local tests check the collector, orchestration and report without model calls. Separately enabled model tests check classification on the agreed synthetic examples. A full run requires the maintainer's scope and spending approval; a marked test or command flag supplies no such authority by itself.

On an agreed evaluation set, compare correct findings, irrelevant selections and missed relevant opportunities, assessing projects and vacancies separately. Numerical accuracy targets are not set before baseline observations exist. Live-source verification follows explicit access and content-use decisions. A working demonstration does not by itself establish sustained usefulness, complete Telegram coverage or account safety.

### Alternative considered

Starting directly with a continuous monitor would provide automatic collection earlier, but would add connection recovery and operating concerns before selection usefulness has been established. The one-source local run is the chosen starting direction; continuous operation follows the reliability milestone.

## Constraints and open decisions

The initial direction keeps read-only collection, separate categories and local reporting. Semantic AI classification is the accepted technical approach; the selected candidate has not been evaluated. Outgoing Telegram actions remain excluded. Processing real Telegram content through a model requires a separate content-use/access decision. Credentials, session material and live archives remain outside the public repository.

Before live collection, resolve the first source and its access method, the account and protected session location, the initial reading range, permitted content use, retained data and retention policy. Before implementing the feature, agree its selection examples, detailed behavior and acceptance criteria. The first feature package must also state its edit, deletion and cross-post policies, including explicit exclusions.

Dates, resource forecasts, storage technology and detailed architecture require their own evidence and decisions. The roadmap does not assign a deadline, approve implementation or authorize publication of a release.

## Next step

Review the [first feature specification](specs/001-local-candidates/spec.md) for Milestone 1 and resolve the decisions that affect its scope. Its [feature record](specs/001-local-candidates/tasks.md) owns current preparation progress. Keep proposed choices distinct from accepted requirements. Implementation, live account access and release retain their respective maintainer decisions.
