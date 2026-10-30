---
name: project-guide
description: 'BriefOtter public project knowledge. WHEN: understand BriefOtter, design source monitoring, distinguish client requests, изучи/изучай BriefOtter, разбери/разбирай отбор сообщений. WHEN NOT: account authorization, private project coordination or unrelated Telegram applications.'
allowed-tools: [Read, Grep, Glob, Bash]
---

# BriefOtter Project Guide

## Degrees of Freedom: MEDIUM

## Role

Explain the monitoring concepts that future BriefOtter changes must distinguish. The README owns the introduction, AGENTS.md owns work rules and an approved feature package owns its requirements. This guide describes design concepts, not a running monitor.

## Knowledge entry

Read [references/kb-index.md](references/kb-index.md) for the accessible project owners. Use the current task and relevant owners directly; no private notes or personal tooling are prerequisites for this guide.

## Source access and updates

A source is a selected channel or chat with an agreed access method. Resolving its name, reading a historical message and receiving its next new-message event are different observations. A successful lookup is not evidence of continuing update delivery. Do not treat inaccessible history as an empty source.

Python and Telethon are the selected foundation. Source membership, update delivery and recovery behavior still need source-specific verification before collection is accepted. A user session has account authority; a read-only application boundary must be enforced by the application rather than assumed from the credential.

## Selection and identity

A candidate is a message worth the owner's attention, not an accepted job or a client commitment. Message intent and technical topic are separate: an advertisement offering Python services can contain the same keywords as a client requesting Python development. Job vacancies, resumes, advertisements and uncertain messages must not silently become freelance requests.

The proposed processing identity combines source identity and message identity. Delivery of the same message again, an edit to that message and a cross-post in another source are different cases. A timestamp alone is insufficient to identify them. The first feature specification must choose edit, deletion and cross-post policies explicitly.

## Recovery and evaluation

The proposed collector separates receiving current updates from recovering an interruption. Fetching a fixed recent window does not by itself establish complete recovery. A future acceptance case should cover restart behavior, message identity, unavailable sources and visible incomplete results.

Evaluate filtering with contrasting synthetic examples: a relevant client request, an executor advertisement with the same stack, a permanent role, an unclear request and a duplicate delivery. Preserve the selection reason and unknown fields rather than inventing a budget or hiding uncertainty. Output format, retention and recovery cursors remain specification decisions.

## Upkeep

Keep this guide aligned with accepted feature documents and actual behavior. Move a new detailed contract to its appropriate public owner and link it through the knowledge index. Report unresolved decisions to the maintainer instead of presenting them as implemented behavior.

## Harness enhancements

Use available file-reading and search tools, or read the declared files directly. Report unavailable task inputs rather than assuming access to an account or private context.
