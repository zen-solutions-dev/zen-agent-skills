---
id: feat-0082
title: Add A11 to the autonomy module, so an agent may not edit the check that judges its work
type: feat
status: done
priority: P1
parent: "ROADMAP Epic E #1: autonomy.md v1"
depends_on: []
touched_files:
  - .agents/rules/autonomy.md
  - .agents/rules/core.md
  - docs/rationale/autonomy-citations.md
  - .agents/skills/fix-batch/SKILL.md
  - .claude-plugin/plugin/
  - AGENTS.md
  - ROADMAP.md
  - CHANGELOG.md
created: 2026-10-28
---

## Problem

The autonomy module says what an agent may touch (`A1` to `A3`), what it may claim (`A4` to
`A7`, `A9`), and what it may do with material it did not author (`A10`). It says nothing about the
one move that turns every other rule into theatre: changing the check instead of the work. An agent
that deletes a failing test, loosens an assertion, edits an acceptance command, or special-cases
the input a test feeds it reports a green run that `A4` would record faithfully and `A7`'s
independent verifier would re-run and confirm.

This is measured, not hypothetical. ImpossibleBench (arXiv:2510.20270) finds frontier models
frequently editing or deleting failing tests when the specification and tests conflict, with
stronger models cheating more, and METR (2025-06-05) documents models altering tests and scoring
code. The kit already behaves this way by habit (`bug-0013`, `bug-0010`), but a habit nothing
states is one a dispatched agent has no reason to share.

## Scope

**In scope:**
- `A11` in [`autonomy.md`](../../.agents/rules/autonomy.md), in the evidence section, with its
  *Cited* line, and the scope statement widened so `A10` and `A11` both apply to every run.
- One line for `A11` in the always-loaded [`core.md`](../../.agents/rules/core.md), held under its
  line budget.
- The full citation in `docs/rationale/autonomy-citations.md`, including why it takes `A10`'s
  every-run scope.
- The rule stated explicitly in [`fix-batch`](../../.agents/skills/fix-batch/SKILL.md)'s dispatch
  prompt, since a dispatched agent holds both the work and the check.

**Out of scope:**
- Making `verifier-agent` detect judge edits in a diff. That changes its approved contract
  (`docs/spec/verifier-agent.md`) and is a separate decision.
- A hook. Whether a diff "loosens" a test is not decidable from a payload.
- Rewording the per-skill autonomy sentence in every skill. `validate-skills.py` enforces the lens
  reference, not that sentence, and the lens and the always-loaded core both carry the scope.

## Decisions

- **A rejected alternative: scoping `A11` to unattended runs like `A1` to `A9`.** Editing the check
  is as available to an attended agent, and the person watching sees a passing run rather than a
  changed judge. The rule names a property of the judge, so it takes `A10`'s scope.
- **A seam left open deliberately: "unless your task scopes that change".** Writing tests is
  `test-author`'s whole job and a legitimate task for anyone. The rule forbids changing the judge
  as a route to "done", not changing tests, and asks only that a scoped test change be reported
  apart from the code it judges.

## Acceptance criteria (mechanically verifiable)

    python scripts/validate-skills.py
    python scripts/run-checks.py

- [x] `A11` appears in `autonomy.md` with a *Cited* line naming internal and outside evidence.
- [x] `core.md` carries `A11` and states that `A10` and `A11` apply to every run, and
      `validate-skills.py` still passes its always-loaded line budget.
- [x] `docs/rationale/autonomy-citations.md` has an `A11` entry with dated, attributed sources.
- [x] `fix-batch`'s dispatch prompt states the rule.
- [x] `AGENTS.md`'s layout row for the rules names `A10` and `A11` as the every-run rules. The
      verbatim "original opening" kept in `docs/rationale/autonomy-citations.md` still names
      only `A10`, and stays that way: it is a record of the module's first wording, and
      rewriting it would falsify the history it exists to keep.

## Definition of done

- [x] Acceptance command(s) pass locally.
- [x] Conventions in AGENTS.md's conventions section followed.
- [x] `doc-sync` run over the reader-facing documents. No README, catalog, or getting-started page
      enumerates the autonomy rules by id or count; `ROADMAP.md` Epic E item 1 dates its count
      ("Ten rules as of 2026-08-27") and gained a line for `A11` rather than a rewritten count.
- [x] File in `.tasks/done/`, `status: done`; one dated line added to `CHANGELOG.md`.
