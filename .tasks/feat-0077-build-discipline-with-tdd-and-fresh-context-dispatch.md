---
id: feat-0077
title: Build discipline, with a tdd skill, fresh-context dispatch, and feedback-loop-first debugging
type: feat
status: open
priority: P1
parent: "ROADMAP 2026-11 overhaul WS2 Build"
depends_on: [chore-0095]
spec: ""
scenarios: []
touched_files:
  - .agents/skills/
  - .agents/skills/test-author/
  - .agents/skills/test-quality/
  - .agents/skills/fix-batch/
  - .agents/skills/reconcile-worktrees/
  - .agents/skills/verifier-agent/
  - .agents/skills/spec-conformance/
  - .agents/skills/systematic-debugging/
  - .agents/skills/agent-handoff/
  - docs/spec/test-author.md
  - docs/spec/test-author.conformance.md
  - docs/spec/verifier-agent.md
  - docs/spec/verifier-agent.conformance.md
  - docs/spec/systematic-debugging.md
  - docs/spec/systematic-debugging.conformance.md
  - tests/test_systematic_debugging.py
  - CHANGELOG.md
created: 2026-11-23
---

## Problem

The build half of the kit has the strongest evidence discipline anywhere comparable, and it is the
heaviest part to carry: [`fix-batch`](../.agents/skills/fix-batch/SKILL.md) is 452 lines with incident
history between its steps, and [`reconcile-worktrees`](../.agents/skills/reconcile-worktrees/SKILL.md)
is 265. It also lacks three things Matt Pocock's workflow treats as basic:

- **Test-first work.** [`test-author`](../.agents/skills/test-author/SKILL.md) writes tests after an
  implementation exists. Nothing drives a change from a failing test.
- **Context hygiene for dispatched agents.** Nothing tells a dispatched agent to start from a fresh
  context rather than a fork of the parent, or that it is a leaf. Nothing sizes work to one context
  window, or sets effort. In the podcast Matt runs medium effort "for pretty much everything" and
  raises it for verification, because high effort spends the context window on exploration early.
- **A feedback loop before a hypothesis.** [`systematic-debugging`](../.agents/skills/systematic-debugging/SKILL.md)
  starts hypothesising before it owns a command that goes red on the bug.

Read [`docs/reviews/2026-11-overhaul-plan.md`](../docs/reviews/2026-11-overhaul-plan.md) in full,
including its rules for every workstream session, before starting.

**New paths this task creates**, so `touched_files` lists their existing parent instead: `.agents/skills/tdd/`. Within `.agents/skills/`, this task owns only the skill directories named in its `touched_files` and those new ones.

## Scope

**In scope:**

1. **A new `tdd` skill**, draft, model-invoked. Study `skills/engineering/tdd/SKILL.md`, `tests.md`
   and `mocking.md` in Matt's repository. In this kit's words: agree the seam and the public
   interface with the person first; red, then green, one behaviour at a time; test through the
   narrow interface of a deep module, never its internals; mock only at system boundaries; a test
   that restates the implementation is a tautology and is rejected. It composes `test-quality` as
   its lens. State plainly how it differs from `test-author` (spec-derived and characterization
   tests, after the fact) so the two descriptions do not compete.
2. **`test-quality`**: add the tautological-test and deep-module heuristics. Resolve the validator's
   shape warning by deciding whether it is a lens (then give it `Intent`, `Workflow`, `Output`) or a
   workflow (then drop the lens declaration).
3. **`fix-batch`**: every dispatched agent starts with a fresh context and is told it is a leaf;
   medium effort by default, high for the verifier; a task too big for one fresh context is sent back
   to `new-task` to split. Move incident history into `references/incidents.md` (it exists). Keep
   the nine-field report and every evidence gate. Target at most about 250 lines.
4. **`verifier-agent`, `reconcile-worktrees`, `spec-conformance`**: slim per the plan's rules, and
   carry the fresh-context and effort guidance where they dispatch or are dispatched. Keep the
   `pass`, `fail`, `blocked` semantics and the worktree recovery lessons exactly.
5. **`systematic-debugging`**: add a phase before hypotheses: build a **red** command (one that
   reproduces the failure and fails on it) first; with no red command, no hypothesis phase. Study
   `skills/engineering/diagnosing-bugs/SKILL.md`. Keep the hypothesis budget and the three verdicts.
   It stays a draft; `feat-0063` governs its promotion. Amend its spec with a dated note.
6. **`agent-handoff`**: add the phase-boundary decision (continue, clear, hand off, subagent,
   compact) and the reason behind it: every move except continuing turns a primary source into a
   lossy secondary one. Add a "suggested skills" line to the handoff. Study
   `skills/engineering/ask-matt/PHASE-BOUNDARIES.md` and `skills/productivity/handoff/SKILL.md`.
7. **Break the link cycle** where you own the link: a sibling `SKILL.md` link stays only where the
   skill genuinely composes that sibling.

**Out of scope:** promoting `systematic-debugging`, changing the delegate report's fields, and every
file outside `touched_files` except one `CHANGELOG.md` line.

## Implementation notes

- `tdd` carries a provenance block for each upstream file it adapts.
- The fresh-context instruction must be harness-neutral: say what to do where a harness forks by
  default, without naming one harness's tool.
- When a contract under `docs/spec/` changes, amend it with a dated note and update its matrix.
- `python scripts/check-provenance.py` reported drift on 2026-11-23 for the upstreams of `systematic-debugging` (`obra/superpowers`) and `test-quality` (`moonray/repoprompt-workflows`). Read what changed upstream; fold in only what this task's scope already covers, and leave the recorded digests alone unless you reconcile the difference (`AGENTS.md`, provenance).

## Acceptance criteria (mechanically verifiable)

    python scripts/run-checks.py

- [ ] Exit 0, with the command and the verbatim tail in the pull request body.
- [ ] `tdd` exists with `status: draft` under `metadata` and a provenance block.
- [ ] `validate-skills.py` reports no shape warning for `test-quality`.
- [ ] `fix-batch` is at most about 250 lines and still names all nine report fields.

## Definition of done

- [ ] Acceptance command passes.
- [ ] Spec amendments flagged for the maintainer's approval in the pull request.
- [ ] Task file moved to `.tasks/done/` with `status: done` and links re-anchored; one dated line in
      `CHANGELOG.md`.
- [ ] Draft pull request into `zen/overhaul-2026-11`, with "Notes for integration".
