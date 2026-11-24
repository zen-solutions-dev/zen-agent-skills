---
id: chore-0100
title: Cut always-loaded context to the rules, archive the ledgers, and make the documents true
type: chore
status: open
priority: P1
parent: "ROADMAP 2026-11-24 Marjana overhaul"
depends_on: [chore-0099]
spec: ""
scenarios: []
touched_files:
  - AGENTS.md
  - CLAUDE.md
  - docs/rationale/
  - CONTRIBUTING.md
  - docs/ARCHITECTURE.md
  - ROADMAP.md
  - CHANGELOG.md
  - docs/
  - README.md
  - docs/CATALOG.md
  - docs/GETTING-STARTED.md
  - docs/INSTALL.md
  - docs/OBSERVATORY.md
  - .claude/settings.json
  - .tasks/chore-0098-a-docs-only-change-runs-the-docs-gates-and-a-secret-scan.md
  - .tasks/chore-0077-the-draft-axis-stops-at-one-of-two-distribution-paths.md
created: 2026-11-24
---

## Problem

Every session in this repository loads about 28 KB of `AGENTS.md`, about 60 percent of it rationale, history or restatement ([inventory `P1`](../docs/reviews/2026-11-24-marjana-inventory.md)). `CHANGELOG.md` (406 KB) and `ROADMAP.md` (106 KB) are paid for by every closeout that opens them (`P4`, `P5`). `ROADMAP.md`'s "Current state" is false today (`P3`), two tasks are done but open (`P6`), and seventeen reader-facing claims are stale or false (`P7`).

## Scope

**In scope** ([plan, WS-A](../docs/reviews/2026-11-24-marjana-plan.md)):

- `P1`: rewrite `AGENTS.md` to the rules, at most 10 KB, every moved block landing at its named destination in the same change, so no rule or reason is lost. The test from [the sources delta](../docs/reviews/2026-11-24-sources-delta.md) "Context hygiene" applies: keep only what is undiscoverable and globally relevant. `P13`: `CLAUDE.md` keeps `@AGENTS.md` and one line.
- `P3`: rewrite "Current state" from the tree, dated; retire the finished overhaul subsections; add a short "2026-11-24 Marjana overhaul" section naming this round's tasks.
- `P4`, `P5`: per-month archives under `docs/history/` with a `README.md` index; re-anchor every moved link; keep every section heading a task `parent:` cites findable. Restate the closeout rule as one dated line of at most about 300 characters, linking the task file.
- Add the missing `CHANGELOG.md` lines for PR #110 (`chore-0097`) and PR #113 (`feat-0084` to `feat-0089`), and the line for `chore-0099`.
- `P6`: close `chore-0098` and `chore-0077` (superseded by `feat-0079`).
- `D3`: cherry-pick the three task files `feat-0073`, `feat-0074` and `feat-0075` from `origin/claude/2026-10-22-oversight-tasks` into `.tasks/`, with a roadmap line each. Do not delete the branch; the orchestrator does that after the pull request is opened.
- `P7` and `P12`: correct every row of the stale-claims table in files you own; add `docs/reviews/README.md`.
- Trim `.claude/settings.json`'s `_comment` to a pointer at the rationale, moving the history there.
- An optional, labelled Claude Code section in `docs/INSTALL.md` on measuring and trimming the hidden system-prompt payload, with no preset (sources delta, "Measure, then trim").

**Out of scope:** any skill, rule lens, script or test; `.tasks/README.md`, `_TEMPLATE.md` and `validate.py` (WS-B owns them).

## Risks and rollback

Touches more than one module and moves ledger history across files. A missed re-anchor fails the `doc links` gate loudly. Rollback is one revert of this branch's merge; the archive split is restored by concatenation.

## Acceptance criteria (mechanically verifiable)

    ZEN_CHECKS_SCOPE=full python3 scripts/run-checks.py

- [ ] `wc -c AGENTS.md` prints at most 10240.
- [ ] `wc -c CHANGELOG.md` prints under 40960, and every archived entry exists verbatim under `docs/history/`.
- [ ] `grep -n "10 are drafts" ROADMAP.md` finds nothing.
- [ ] `docs/reviews/2026-11-24-dogfood/ws-a.md` records each kit skill used on this work.

## Definition of done

- [ ] Acceptance command passes locally.
- [ ] `doc-sync` run over the reader-facing documents, findings applied or dismissed with a reason.
- [ ] File moved to `.tasks/done/`, `status: done`; its `CHANGELOG.md` line written.
