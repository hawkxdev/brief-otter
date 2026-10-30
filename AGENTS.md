# BriefOtter working instructions

Read [README.md](README.md) for the project stage and [.agents/skills/project-guide/SKILL.md](.agents/skills/project-guide/SKILL.md) for subject-specific concepts. Use the relevant approved feature package before implementation; repository setup does not approve the first product specification.

## Structure and ownership

Product sources belong in `src/`, checks in `tests/`, project utilities in `scripts/`, feature requirements and plans in `docs/specs/<NNN-feature>/`, and accepted architecture decisions in `docs/adr/`. Empty roles are populated when there is real content. Keep one Git root, a real `.agents/skills/` directory and this file as the shared instruction owner.

Requirements and acceptance criteria belong to the agreed feature package. Link its issue and PR when those objects exist; do not maintain competing requirement lists. Proposals remain proposals until the maintainer accepts them.

## Implementation and verification

Python and Telethon are selected. Runtime versions, dependency tooling and database choice must follow the first approved implementation specification rather than assumptions from another project. There is no application setup, test or build command at the current stage.

Run applicable checks locally. Do not add, enable or trigger GitHub Actions as part of routine work. For documentation edits, check links and factual claims, inspect new files as well as tracked changes, and run `git diff --check`. Define and execute focused behavior checks with the first implementation.

Use English for public documentation and technical instructions. Keep paragraphs on single lines. Preserve exact source literals when their spelling or language matters.

## Data and external actions

Do not commit credentials, session material, live message archives or personal correspondence. Use synthetic examples in issues, tests and documentation. Before real collection, resolve the approved sources, account, session location, content-use terms and retention policy with the maintainer.

The initial product direction excludes outgoing Telegram actions and language-model processing of collected messages. Do not log in, reuse another application's session, send messages, join sources or change production systems without the corresponding explicit assignment.

## Git and delivery

Create commits only after the maintainer explicitly approves the prepared result. The first commit message is exactly `chore: initialize project`. Publication also requires approval of the exact outgoing package.

Subsequent updates to `main` use pull requests; the human maintainer performs the final merge. Do not force push or delete branches. Written rules do not establish server enforcement: verify protection before reporting a public delivery complete.
