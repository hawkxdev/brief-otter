# Public knowledge owners

The [project guide](../SKILL.md) explains cross-stage technical distinctions. This index selects the public source needed for a task; it does not copy that source's content or state. Paths are relative to this index.

| Need | Owner | Reading cue |
|---|---|---|
| Project introduction and current stage | [README](../../../../README.md) | Recover context when the project or requested scope is unclear |
| Working instructions and operation authority | [AGENTS.md](../../../../AGENTS.md) | Before edits, verification or external actions |
| History collection versus later recovery/monitoring | [Roadmap](../../../../docs/ROADMAP.md) | Decide which milestone owns the behavior; do not import later scope |
| Applicable requirements, phase and next decision | [Specification](../../../../docs/specs/001-local-candidates/spec.md), [feature record](../../../../docs/specs/001-local-candidates/tasks.md) | Bind a change to its actual contract and approval state |
| Model boundary, prompt, response schema and failure handling | [AI contract](../../../../docs/specs/001-local-candidates/ai-classification.md) | Change or evaluate the classifier without mixing provider and source behavior |
| Selection expectations and contrasting inputs | [Examples and rubric](../../../../docs/specs/001-local-candidates/rules.md), [English cases](../../../../docs/specs/001-local-candidates/spec.md#synthetic-selection-examples) | Review labels or change semantic checks; examples are not a lookup algorithm |
| No-AI versus real-model execution | [Test policy](../../../../docs/specs/001-local-candidates/tasks.md#accepted-test-execution-policy) | Select the run mode before testing; a command flag is not approval |

The classifier contract links its prompt/schema sources. README links contribution and sensitive-reporting routes; follow those owners for submissions rather than reproducing their instructions here.
