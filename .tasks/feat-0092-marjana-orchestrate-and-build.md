---
id: feat-0092
title: Add an orchestrator and a research skill, and bring the build and verify skills current
type: feat
status: open
priority: P1
parent: "ROADMAP 2026-11-24 Marjana overhaul"
depends_on: [chore-0099]
spec: ""
scenarios: []
touched_files:
  - .agents/skills/
  - .agents/skills/fix-batch/
  - .agents/skills/reconcile-worktrees/
  - .agents/skills/verifier-agent/
  - .agents/skills/spec-conformance/
  - .agents/skills/agent-handoff/
  - .agents/skills/tdd/
  - .agents/skills/test-author/
  - .agents/skills/test-quality/
  - .agents/skills/systematic-debugging/
  - .agents/rules/autonomy.md
  - .agents/rules/core.md
  - docs/spec/
  - docs/
created: 2026-11-24
---

## Problem

The maintainer works through one orchestrating session per project or day: child sessions research and build on their own branches, everything lands on one integration branch, and one pull request reaches the person. The kit has the parts (`fix-batch`, `verifier-agent`, `reconcile-worktrees`, `agent-handoff`, `pr-describe`) but no skill that runs the day, and `A8` has no rule for an orchestrator merging other agents' verified work ([sources delta](../docs/reviews/2026-11-24-sources-delta.md), "Orchestrator pattern").

## Scope

**In scope** ([plan, WS-C](../docs/reviews/2026-11-24-marjana-plan.md)):

- **`D1`** in `autonomy.md` and mirrored in `core.md` (inside its line budget): an orchestrator may merge into an integration branch only work it did not author and that someone else verified (`A7`); only a person merges into `developer` or `main`.
- **`orchestrate`**, a new draft, `invocation: user`: the sources delta's seven steps, each with a "Done when"; frontier waves computed from merges into the integration branch; children merge the integration tip before reporting; relay as outcome first, then decisions; `afk` or `hitl` per child, with `hitl` work kept in the orchestrator's own conversation; a rework cap; one review, one fix, then stop; dated, commit-cited memory ("write history, not the present"); offer environment changes after friction and route them to `retro`; sample about one child in five for `retro`. Child stays transport-neutral; a labelled optional section covers Claude Code cloud sessions (`create_session`, `send_message`, `list_events`). It composes `agent-handoff`, `verifier-agent`, `reconcile-worktrees` and `pr-describe` by link. **This session is its first real run**: the orchestrator's account of it is in the plan and in its reports to you.
- **`research`**, a new draft: a fresh agent investigates one question against primary sources, bound by `A10`, and writes one cited markdown file where the repository keeps such notes, saying what it could not reach. Its first real runs are the two reports under `docs/reviews/2026-11-24-*`.
- `reconcile-worktrees` lands on an integration branch as well as the main checkout. `agent-handoff`: the compact-right-after-a-document cue, and a durability line for briefs in a temporary directory. `verifier-agent`: an optional "different model family where the harness allows" line. `fix-batch`: point at `orchestrate` for dependent work.
- `P10` and the slimming rules for every skill you own; `systematic-debugging` and `fix-batch` under about 250 lines or with a one-line reason.

**Out of scope:** `house-review`, `pr-describe`, `retro` (WS-D); `zen` (WS-B hints at the new drafts); scripts and tests (WS-E).

## Risks and rollback

`D1` widens what an unattended agent may do, which is the one-way door here; it is approved and must be worded with every guard. Rollback is one revert.

## Acceptance criteria (mechanically verifiable)

    ZEN_CHECKS_SCOPE=full python3 scripts/run-checks.py

- [ ] `.agents/skills/orchestrate/SKILL.md` and `.agents/skills/research/SKILL.md` exist with `status: draft`.
- [ ] `grep -n "integration branch" .agents/rules/autonomy.md .agents/rules/core.md` finds the `D1` text in both.
- [ ] `docs/reviews/2026-11-24-dogfood/ws-c.md` has a row for every skill this task owns.

## Definition of done

- [ ] Acceptance command passes locally.
- [ ] Notes for integration and the `CHANGELOG.md` line reported to the orchestrator.
- [ ] File moved to `.tasks/done/`, `status: done`.
