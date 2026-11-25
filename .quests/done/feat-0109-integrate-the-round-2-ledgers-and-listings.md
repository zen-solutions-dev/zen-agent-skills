---
id: feat-0109
title: Bring the round 2 ledgers and listings up to date and remove the gate bridges
type: feat
status: done
priority: P1
parent: "Marjana round 2, close: Integration (docs/reviews/2026-11-25-marjana-r2-plan.md)"
depends_on: [feat-0101, feat-0102, feat-0103, feat-0105, feat-0106, feat-0107, feat-0108]
spec: ""
scenarios: []
external: ""
mode: "afk"
touched_files:
  - CHANGELOG.md
  - ROADMAP.md
  - README.md
  - docs/CATALOG.md
  - docs/GETTING-STARTED.md
  - docs/INSTALL.md
  - docs/ARCHITECTURE.md
  - .agents/skills/zen/SKILL.md
  - scripts/run-checks.py
  - .quests/_TEMPLATE.md
  - .agents/skills/init-worktracking/templates/_TEMPLATE.md.tmpl
  - .claude-plugin/
  - docs/reviews/2026-11-25-dogfood/ledgers.md
created: 2026-11-25
---

## Problem

Every round 2 workstream (`feat-0101` to `feat-0108`, and the orchestrator's `chore-0104`, recorded
in [the round 2 plan](../../docs/reviews/2026-11-25-marjana-r2-plan.md)) has landed on
`zen/marjana-r2-2026-11-25`, and none of the reader-facing ledgers says so: `CHANGELOG.md` has no
round 2 line, `ROADMAP.md`'s "Current state" counts 31 skills and 6 drafts against a tree of 37 and
12, and neither [`zen`](../../.agents/skills/zen/SKILL.md) nor [`CATALOG.md`](../../docs/CATALOG.md)
names the six new drafts. Two children kept the gates green with named bridges in
[`run-checks.py`](../../scripts/run-checks.py) (`ROADMAP_STATUS_EXCEPTIONS`,
`UNLISTED_DRAFT_EXCEPTIONS`) that this quest is to delete.

## Scope

**In scope:** one dated `CHANGELOG.md` line per round 2 quest and the Unreleased section renamed to
cover both Marjana rounds without a version; a "2026-11-25 Marjana round 2" roadmap section with what
landed and what is owed, the rollout campaign, the Phase 3 plans F1 to F5, and a true "Current
state"; the six drafts in `zen` and the catalog, and the changed skills' catalog rows and the
`deep-modules.md` lens; `README.md`'s quest wording, the alias line and a link to
`docs/RELEASING.md`; an optional `private: false` line in both quest templates; deleting every
bridge key the two exception sets no longer need; `doc-sync` over the reader documents, recorded in
the dogfood record; the regenerated `.claude-plugin/`.

**Out of scope:** every other skill, rule, spec or script; the close-round fix list in the plan
(items (a) to (n), the fix child's); the Phase 3 plan files `docs/reviews/2026-11-25-plan-*.md`,
written by a sibling, named in backticks until they exist; moving this file to `done/` and the pull
request (the orchestrator's).

## Decisions

- **A premise that turned out false:** the brief says each quest's "Notes for integration" gives
  suggested texts; no closed quest file has that section (the notes went in the children's reports),
  so every line here is derived from the quest files' Problem, Scope and Decisions and from the tree.
- **A premise that turned out false:** `chore-0104` has no quest file; its changelog line links the
  plan section that records it.

## Risks and rollback

Touches more than one module (ledgers, a router skill, a gate's exception sets, two templates). Each
part reverts alone; with the bridges gone, a revert of the listing edits alone makes the two gates
fail, so revert them together.

## Acceptance criteria (mechanically verifiable)

    ZEN_CHECKS_SCOPE=full python3 scripts/run-checks.py

- [ ] `ROADMAP_STATUS_EXCEPTIONS` and `UNLISTED_DRAFT_EXCEPTIONS` are empty, and the `roadmap
      bookkeeping` and `skill listings` gates pass.
- [ ] `python3 .quests/validate.py --strict` exits 0.
- [ ] The `doc-sync` run and each finding's disposition are in
      `docs/reviews/2026-11-25-dogfood/ledgers.md`.

## Definition of done

- [ ] Acceptance command passes locally after `origin/zen/marjana-r2-2026-11-25` is merged in.
- [ ] Left in `.quests/` for the orchestrator to close (B2).
