---
id: feat-0107
title: Fold the round 2 orchestrate-and-build decisions into the skills that dispatch, land and debug
type: feat
status: in_progress
priority: P1
parent: "Marjana round 2, Wave 2: Orchestrate and build (docs/reviews/2026-11-25-marjana-r2-plan.md)"
depends_on: []
spec: docs/spec/systematic-debugging.md
scenarios: [S-016, S-017, S-018, S-019, S-020]
external: ""
mode: "afk"
touched_files:
  - .agents/skills/orchestrate/SKILL.md
  - .agents/skills/orchestrate/references/claude-code.md
  - .agents/skills/orchestrate/references/first-run.md
  - .agents/skills/reconcile-worktrees/SKILL.md
  - .agents/skills/fix-batch/SKILL.md
  - .agents/skills/agent-handoff/SKILL.md
  - .agents/skills/systematic-debugging/SKILL.md
  - .agents/skills/research/SKILL.md
  - .agents/skills/tdd/SKILL.md
  - .agents/skills/sitrep/SKILL.md
  - .agents/rules/autonomy.md
  - docs/agents/zen.md
  - docs/spec/systematic-debugging.md
  - docs/spec/systematic-debugging.conformance.md
  - docs/spec/zen-config.md
  - GLOSSARY.md
  - tests/test_systematic_debugging.py
  - tests/fixtures/supporting-files.txt
  - docs/reviews/2026-11-24-retro-marjana.md
  - docs/reviews/2026-11-25-marjana-decisions.md
  - .quests/.scaffold.json
created: 2026-11-25
---

## Problem

The maintainer approved, on 2026-11-25, a set of changes to the skills that plan, dispatch, land and
debug work ([decisions](../docs/reviews/2026-11-25-marjana-decisions.md) `B1`, `B2`, `B6` to `B8`,
`E2`, `E3`, `E6`, `E9`; round 2 plan decisions `R2-6` and `R2-9`; the
[plan](../docs/reviews/2026-11-25-marjana-r2-plan.md)'s Wave 2 row for this id). As of `d906b20`
none of them is in the skills: [`orchestrate`](../.agents/skills/orchestrate/SKILL.md) has no memory
location, lint or recurring-job offer, and lands by fast-forward only although
[`autonomy.md`](../.agents/rules/autonomy.md) `A8` now allows a mechanical merge;
[`systematic-debugging`](../.agents/skills/systematic-debugging/SKILL.md) lacks redaction, ranked
hypotheses and four ladder rungs; [`research`](../.agents/skills/research/SKILL.md) marks no rarity,
and [`sitrep`](../.agents/skills/sitrep/SKILL.md)'s tiers were documented as a separate scale.

## Scope

**In scope:** the ten items of the orchestrator's brief for this quest: `orchestrate` memory (key
set in `docs/agents/zen.md`, entries under `docs/agents/memory/`, new
`.agents/skills/orchestrate/references/memory.md`), lint, recurring-job offer, exploration child;
`A8`'s mechanical merge in `orchestrate` Step 5 and `reconcile-worktrees`; the merge-conflict rule;
`R-202`, `R-206`, `R-207`, `R-208`; `tdd` in build briefs; a proposed landing order in `fix-batch`;
`software-factory`'s brakes and five questions in `orchestrate`; `systematic-debugging`'s missing
rungs with the spec amendment `S-017` to `S-020` and the new
`.agents/skills/systematic-debugging/scripts/hitl_loop.py`; the one rarity ladder in `research`,
`sitrep/SKILL.md` and `GLOSSARY.md`; `tdd`'s guarded load; `fix-batch`'s `spec_digest` run; the
`claude --bg` section in `agent-handoff`; the re-pitch rule; a round 2 section in
`orchestrate/references/first-run.md`; the dogfood record
`docs/reviews/2026-11-25-dogfood/orchestrate.md`.

**Out of scope:** `zen`, `docs/CATALOG.md`, `CHANGELOG.md`, `ROADMAP.md`, `README.md` (lines passed
to integration); `sitrep`'s script; promoting `research` or `systematic-debugging`; amending
`docs/spec/zen-config.md` (read only, for the `memory` key's type).

## Decisions

- **A premise that turned out false**: the brief set `memory: docs/agents/memory/`, a directory. The
  approved `zen-config` contract defines `memory` as a file (its key table and `S-004`), and the
  validator rejects a directory there. The key names the index, `docs/agents/memory/README.md`;
  the directory and the index are as the brief asked.
- **A rejected alternative**: a person-in-the-loop command as a new red-command kind with its own
  record field. Rejected for one narrow exception in `S-016` read with `S-019`, recorded in
  `reproduction`, so the record's field set stays exact.
- **A premise that turned out false**: the scaffold's shared counter was meant to stay untouched,
  but `.quests/validate.py` errors while `id_high_water['feat']` (103) is below an existing id. It
  is raised to 109, the highest id the round 2 plan reserves, so siblings who raise it the same way
  write an identical line.
- **A seam left open deliberately**: the re-pitch rule names no `wait-what` skill, because that
  draft is being written in parallel (`feat-0108`); a guarded load can be added once it lands.

## Risks and rollback

Touches several skills and amends an approved spec. Each file's change is independent text; revert
the branch's commits to undo it whole. The `systematic-debugging` amendment is pending the
maintainer's re-approval and changes no verdict, field or input.

## Acceptance criteria (mechanically verifiable)

    ZEN_CHECKS_SCOPE=full python3 scripts/run-checks.py

- [x] `tests/test_systematic_debugging.py` carries one test per new scenario `S-017` to `S-020` and
  runs the human-in-the-loop script.
- [x] `python scripts/validate-skills.py` reports no error and no warning.
- [x] `python .quests/validate.py` accepts `memory: docs/agents/memory/README.md`.

## Definition of done

- [ ] Acceptance command(s) pass locally.
- [ ] Conventions in AGENTS.md's conventions section followed.
- [ ] `doc-sync` run over the reader-facing documents and its findings applied or dismissed with a reason.
- [ ] File moved to `.quests/done/`, `status: done`; one dated line added to `CHANGELOG.md` referencing this quest id (the orchestrator, at close).
