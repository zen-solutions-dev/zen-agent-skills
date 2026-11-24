---
id: feat-0091
title: Configure the skills per repository, and sharpen the align and plan skills
type: feat
status: done
priority: P1
parent: "ROADMAP 2026-11-24 Marjana overhaul"
depends_on: [chore-0099]
spec: docs/spec/zen-config.md
scenarios: [S-001, S-002, S-003, S-004, S-005, S-006, S-007, S-008, S-009, S-010, S-011, S-012, S-013, S-014, S-015, S-016, S-017, S-018, S-019, S-020, S-021, S-022, S-023, S-024, S-025, S-026, S-027, S-028, S-029, S-030, S-031, S-032, S-033, S-034, S-035, S-036, S-037, S-038, S-039, S-040, S-041, S-042]
mode: hitl
touched_files:
  - .agents/skills/init-worktracking/
  - .agents/skills/project-bootstrap/
  - .agents/skills/zen/
  - .agents/skills/grill/
  - .agents/skills/domain-language/
  - .agents/skills/spec-author/
  - .agents/skills/spec-quality/
  - .agents/skills/spec-plan-readiness/
  - .agents/skills/new-task/
  - .tasks/README.md
  - .tasks/_TEMPLATE.md
  - .tasks/validate.py
  - GLOSSARY.md
  - tests/test_zen_config.py
  - tests/test_validate_skills.py
  - .claude-plugin/
  - docs/spec/
  - docs/
created: 2026-11-24
---

## Problem

Every skill rediscovers, on every run, where a repository keeps its tracker, glossary, specs and acceptance command, and adopters get no walkthrough that fits the kit to their environment ([sources delta](../../docs/reviews/2026-11-24-sources-delta.md), "Install-time setup walkthrough"). The two scaffolds are model-invoked against `AGENTS.md`'s own rule and carry the longest shipped descriptions ([inventory `P2`](../../docs/reviews/2026-11-24-marjana-inventory.md)). Nothing names whether a piece of work runs AFK or with a human in the loop.

## Scope

**In scope** ([plan, WS-B](../../docs/reviews/2026-11-24-marjana-plan.md)):

- **`D2`, the setup file.** Write a spec, `docs/spec/zen-config.md`, with `spec-author` (this is a contract adopters will depend on): the path `docs/agents/zen.md`, the fenced `zen-config` block of `key: value` lines parseable by the Python standard library, the keys from the sources delta's design table, `config_version`, fallback when absent, and re-runs never overwriting a hand-edited value. Run `spec-quality` and `spec-plan-readiness` over it.
- A "configure the skills" step in `init-worktracking`: explore read-only, recommend, confirm one section at a time, skip what exploration settled, show the draft, write only on confirmation; add an `## Agent skills` pointer block to the target's `AGENTS.md`. The `validate.py` it installs parses the block and fails on an unknown key or a missing path. Labels the configuration names but the tracker lacks are printed as commands, never run.
- **First real run**: write this repository's own `docs/agents/zen.md` with that step.
- `zen`: hint at the setup step when a repository has no `docs/agents/zen.md`; hint at `orchestrate` and `research` as drafts (WS-C builds them).
- `P2`: `project-bootstrap` and `init-worktracking` become `invocation: user`, with descriptions cut to a third-person one-liner. A leaner seeded `AGENTS.md` template: no structure listing, no commands discoverable from a manifest.
- `mode: afk` or `hitl` as an optional task field: `.tasks/_TEMPLATE.md`, `.tasks/README.md` (add the missing `conformance:` row too), `.tasks/validate.py`, and the template copies under `init-worktracking/templates/`; `new-task` sets it from the door and the blast radius.
- `grill`: split "Still open" into deferred decisions and fog, add "Out of scope", open by asking for the problem and its why. `domain-language`: test a candidate name against real sentences in a table. `project-bootstrap`: print, never install, a pre-commit config that runs the acceptance command. `new-task` and `init-worktracking`: a quality-bar line (prototype, production or library); risky slices first. `new-task`: `chore-0074` (the documents a change falsifies are in scope).
- `GLOSSARY.md`: the terms this round settles (orchestrator, child session, integration branch, frontier, AFK, human-in-the-loop, one-way door, two-way door), kept with `domain-language`.
- `P10` and the slimming rules for every skill you own.

Only the `D2` items above trace to `docs/spec/zen-config.md`; the rest of the scope (`grill`, `domain-language`, `project-bootstrap`, the quality bar, `chore-0074`, `GLOSSARY.md`, `P2`, `P10`, the `zen` hints, the `mode` field) declares no spec and is checked by the dogfood record and the acceptance command.

**Out of scope:** `orchestrate`, `research`, `autonomy.md`, `core.md` (WS-C); `install.py` (WS-E prints the pointer line).

## Risks and rollback

The `zen-config` path and format become a one-way door once adopters use them; the spec waits for the maintainer's approval in the final pull request, and nothing outside this repository reads the file before then.

**Sequencing, by the plan rather than the readiness gate.** The plan has this one task write the spec and build against it in the same round, with approval at the final pull request (plan, "Rules for every workstream session" and decision `D2`). `spec-plan-readiness` therefore returns `blocked` on a draft spec, and that verdict stands until the maintainer approves; the build is offered for review, not landed as approved.

**Rollback.** Nothing here has reached an adopter: every surface ships only when the integration branch merges. Before that, reverting this branch's commits undoes all of it. After it, each surface reverts on its own: the `invocation: user` lines in two skills; the `zen-config` and `mode` checks, one block each in both validator copies (an absent `docs/agents/zen.md` and an empty `mode` were valid before and stay valid, so no adopter file is invalidated by a revert); the template changes, which affect only repositories scaffolded afterwards.

**Test strategy.** The validator scenarios (S-001 to S-013, S-019, S-020, S-027, S-028) are unit and filesystem tests in `tests/test_zen_config.py`, run against both validator copies. The conversational scenarios (S-014 to S-018, S-021 to S-026, S-029, S-030) are evidenced by recorded runs in the dogfood record and audited in `docs/spec/zen-config.conformance.md`; a scenario no run exercised is recorded as not exercised.

**The first real run** on this repository had no person present. The values exploration settled were written; the contested ones were written as recommended and routed to the maintainer, and the file says so. Against S-015 and S-025 that is a deviation, recorded in the conformance matrix rather than hidden.

## Acceptance criteria (mechanically verifiable)

    ZEN_CHECKS_SCOPE=full python3 scripts/run-checks.py

- [x] `docs/spec/zen-config.md` exists with Given/When/Then scenarios, and `docs/agents/zen.md` parses with the shipped `validate.py`.
- [x] `grep -n "invocation: user" .agents/skills/project-bootstrap/SKILL.md .agents/skills/init-worktracking/SKILL.md` finds both.
- [x] `docs/reviews/2026-11-24-dogfood/ws-b.md` has a row for every skill this task owns.
- [x] `python3 -m unittest tests.test_zen_config` passes, and `docs/spec/zen-config.conformance.md` exists.

## Definition of done

- [x] Acceptance command passes locally.
- [x] Notes for integration and the `CHANGELOG.md` line reported to the orchestrator.
- [x] File moved to `.tasks/done/`, `status: done`.
