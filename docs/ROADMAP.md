# Product Vision and Roadmap

BriefOtter aims to turn selected Telegram feeds into a useful local list of freelance development requests, with original message links and reasons for selection. See the [README](../README.md) for the product introduction.

## Current state

The project is at the design stage. The public foundation is available, but there is no runnable collector. Python and Telethon are selected; runtime versions, dependency tooling, storage technology and detailed architecture remain decisions for the first feature package.

The product direction and first vertical slice below are agreed. All implementation milestones remain planned. Feature packages under `docs/specs/<NNN-feature>/` will own their detailed requirements, acceptance criteria and execution plans.

## Milestones

| Milestone | User outcome | Evidence needed before progressing |
|---|---|---|
| **1. First useful results** | One local run reads an agreed source and produces a local selection of candidate requests | The complete scenario works; contrasting selection examples, repeated delivery and unavailable-source behavior are checked; the maintainer assesses whether the result is useful |
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
3. Explicit rules distinguish client requests, executor advertisements, permanent job vacancies, resumes and uncertain messages.
4. A topic filter selects candidates within the agreed interests.
5. A local HTML table presents the source, publication time, category, selection reason and original message link. Uncertain messages are shown separately.
6. Processing the same message again does not create another copy. An inaccessible source or incomplete collection is reported visibly.

The slice includes the whole path from source to a reviewable result. It excludes continuous execution, server deployment, delivery notifications, CRM integration, a full web interface and complex grouping of cross-posts. The exact data retained and its lifetime must be agreed before live collection.

### Validation

Use contrasting synthetic examples: a relevant client request, an executor advertisement using the same technologies, a permanent vacancy, an unclear message and a repeated delivery. Check that the output preserves the original link and selection reason, retains uncertainty and exposes incomplete collection rather than presenting it as an empty result.

On an agreed evaluation set, compare correct findings, irrelevant selections and missed relevant requests. Numerical accuracy targets are not set before baseline observations exist. Live-source verification follows explicit access and content-use decisions. A working demonstration does not by itself establish sustained usefulness, complete Telegram coverage or account safety.

### Alternative considered

Starting directly with a continuous monitor would provide automatic collection earlier, but would add connection recovery and operating concerns before selection usefulness has been established. The one-source local run is the chosen starting direction; continuous operation follows the reliability milestone.

## Constraints and open decisions

The initial direction is read-only collection with rule-based filtering. Outgoing Telegram actions and language-model processing of collected content remain excluded. Account operations and changes to source membership require their own explicit assignment. Credentials, session material and live message archives remain outside the public repository; public examples are synthetic.

Before live collection, resolve the first source and its access method, the account and protected session location, the initial reading range, permitted content use, retained data and retention policy. Before implementing the feature, agree its selection examples, detailed behavior and acceptance criteria. The first feature package must also state its edit, deletion and cross-post policies, including explicit exclusions.

Dates, resource forecasts, storage technology and detailed architecture require their own evidence and decisions. The roadmap does not assign a deadline, approve implementation or authorize publication of a release.

## Next step

Prepare the first feature package for Milestone 1, linking this roadmap and resolving the decisions that affect its scope. Keep proposed choices distinct from accepted requirements. Implementation, live account access and release retain their respective maintainer decisions.
