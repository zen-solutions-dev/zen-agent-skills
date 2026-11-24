---
id: feat-0091
title: Configure the skills per repository, and sharpen the align and plan skills
type: feat
status: open
priority: P1
parent: "ROADMAP 2026-11-24 Marjana overhaul"
depends_on: [chore-0099]
spec: docs/spec/zen-config.md
scenarios: [S-001, S-002, S-003, S-004, S-005, S-006, S-007, S-008, S-009, S-010, S-011, S-012, S-013, S-014, S-015, S-016, S-017, S-018, S-019, S-020, S-021, S-022, S-023, S-024, S-025, S-026, S-027, S-028, S-029, S-030]
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
  - docs/spec/
  - docs/
created: 2026-11-24
---

## Problem

Every skill rediscovers, on every run, where a repository keeps its tracker, glossary, specs and acceptance command, and adopters get no walkthrough that fits the kit to their environment ([sources delta](../docs/reviews/2026-11-24-sources-delta.md), "Install-time setup walkthrough"). The two scaffolds are model-invoked against `AGENTS.md`'s own rule and carry the longest shipped descriptions ([inventory `P2`](../docs/reviews/2026-11-24-marjana-inventory.md)). Nothing names whether a piece of work runs AFK or with a human in the loop.

## Scope

**In scope** ([plan, WS-B](../docs/reviews/2026-11-24-marjana-plan.md)):

- **`D2`, the setup file.** Write a spec, `docs/spec/zen-config.md`, with `spec-author` (this is a contract adopters will depend on): the path `docs/agents/zen.md`, the fenced `zen-config` block of `key: value` lines parseable by the Python standard library, the keys from the sources delta's design table, `config_version`, fallback when absent, and re-runs never overwriting a hand-edited value. Run `spec-quality` and `spec-plan-readiness` over it.
- A "configure the skills" step in `init-worktracking`: explore read-only, recommend, confirm one section at a time, skip what exploration settled, show the draft, write only on confirmation; add an `## Agent skills` pointer block to the target's `AGENTS.md`. The `validate.py` it installs parses the block and fails on an unknown key or a missing path. Labels the configuration names but the tracker lacks are printed as commands, never run.
- **First real run**: write this repository's own `docs/agents/zen.md` with that step.
- `zen`: hint at the setup step when a repository has no `docs/agents/zen.md`; hint at `orchestrate` and `research` as drafts (WS-C builds them).
- `P2`: `project-bootstrap` and `init-worktracking` become `invocation: user`, with descriptions cut to a third-person one-liner. A leaner seeded `AGENTS.md` template: no structure listing, no commands discoverable from a manifest.
- `mode: afk` or `hitl` as an optional task field: `.tasks/_TEMPLATE.md`, `.tasks/README.md` (add the missing `conformance:` row too), `.tasks/validate.py`, and the template copies under `init-worktracking/templates/`; `new-task` sets it from the door and the blast radius.
- `grill`: split "Still open" into deferred decisions and fog, add "Out of scope", open by asking for the problem and its why. `domain-language`: test a candidate name against real sentences in a table. `project-bootstrap`: print, never install, a pre-commit config that runs the acceptance command. `new-task` and `init-worktracking`: a quality-bar line (prototype, production or library); risky slices first. `new-task`: `chore-0074` (the documents a change falsifies are in scope).
- `GLOSSARY.md`: the terms this round settles (orchestrator, child session, integration branch, frontier, AFK, human-in-the-loop, one-way door, two-way door), kept with `domain-language`.
- `P10` and the slimming rules for every skill you own.

**Out of scope:** `orchestrate`, `research`, `autonomy.md`, `core.md` (WS-C); `install.py` (WS-E prints the pointer line).

## Risks and rollback

The `zen-config` path and format become a one-way door once adopters use them; the spec waits for the maintainer's approval in the final pull request, and nothing outside this repository reads the file before then.

## Acceptance criteria (mechanically verifiable)

    ZEN_CHECKS_SCOPE=full python3 scripts/run-checks.py

- [ ] `docs/spec/zen-config.md` exists with Given/When/Then scenarios, and `docs/agents/zen.md` parses with the shipped `validate.py`.
- [ ] `grep -n "invocation: user" .agents/skills/project-bootstrap/SKILL.md .agents/skills/init-worktracking/SKILL.md` finds both.
- [ ] `docs/reviews/2026-11-24-dogfood/ws-b.md` has a row for every skill this task owns.

## Definition of done

- [ ] Acceptance command passes locally.
- [ ] Notes for integration and the `CHANGELOG.md` line reported to the orchestrator.
- [ ] File moved to `.tasks/done/`, `status: done`.
