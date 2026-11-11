---
name: project-guide
description: 'BriefOtter public project knowledge. WHEN: understand BriefOtter, design source monitoring, distinguish client requests, изучи/изучай BriefOtter, разбери/разбирай отбор сообщений. WHEN NOT: account authorization, private project coordination or unrelated Telegram applications.'
allowed-tools: [Read, Grep, Glob, Bash]
---

# BriefOtter Project Guide

## Degrees of Freedom: MEDIUM

## Role and entry

Help a contributor locate the correct BriefOtter contract and reason about its technical boundaries. Read [references/kb-index.md](references/kb-index.md) for the owner needed by the current task; exact requirements, work rules and progress stay there.

## Technical distinctions

Source lookup, history reading and future update delivery are different capabilities. Evidence for one does not qualify another. Match the observation to the applicable milestone instead of inferring continuous monitoring from a successful lookup or history run.

The designed pipeline has separate collection, classification and report-publication failure boundaries. A malformed model reply calls for inspecting the classifier contract, not expanding the Telegram scan. Complete source traversal proves neither a valid classification nor a successfully replaced report. Identify the failing stage before changing another stage's behavior.

## Implemented boundary mechanics

The CLI parses help before resolving a project boundary or loading settings. Configuration validation checks canonical private destinations without creating a client or replacing output. A local preflight failure therefore does not establish an account or provider failure. Response parsing rejects duplicate JSON keys before typed field validation; once a parser has discarded duplicate keys, ordinary dictionary validation cannot recover that evidence.

The test boundary starts before collection and is reinstalled for admitted Python children through sitecustomize. A function-scoped fixture alone misses module imports and child startup. Process arguments are bound to the real Popen signature before executable, shell and environment checks, so positional arguments follow the same policy as keywords. Child modes that suppress the bootstrap are rejected, while Unix socket-pair controls keep local asyncio operation usable.

## Upkeep

Add concrete module interactions, verified pitfalls and reproducible checks when implementation supplies evidence. Keep feature criteria, example labels, run policies and status at their indexed owners. Report unverified behavior instead of filling this guide with assumptions or copying those records.

## Harness enhancements

Read the indexed public files directly when native skill loading is unavailable. Report an unavailable owner; this guide requires no private notes, accounts or personal tooling.
