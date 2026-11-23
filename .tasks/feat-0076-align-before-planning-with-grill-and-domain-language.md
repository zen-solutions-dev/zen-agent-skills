---
id: feat-0076
title: Align before planning, with a grill skill, a domain-language skill, and a spec front that interviews
type: feat
status: open
priority: P1
parent: "ROADMAP 2026-11 overhaul WS1 Align"
depends_on: [chore-0095]
spec: docs/spec/spec-author.md
scenarios: []
touched_files:
  - .agents/skills/
  - .agents/skills/spec-author/
  - .agents/skills/spec-quality/
  - .agents/skills/spec-plan-readiness/
  - .agents/skills/new-task/
  - docs/spec/spec-author.md
  - docs/spec/spec-author.conformance.md
  - CHANGELOG.md
created: 2026-11-23
---

## Problem

Nothing in the kit gets the agent aligned with the person before a contract is written.
[`spec-author`](../.agents/skills/spec-author/SKILL.md) step 1 is titled "Understand the intent, and
ask at most one question", so a spec is drafted from whatever the request happened to say. Matt
Pocock's most-used skill does the opposite: a structured interview that walks the decision tree
until nothing is silently assumed. In the podcast he calls the gap it closes the "communication
gap", and says it "is not going to go away if the model gets smarter".

The kit also has no shared language. No skill keeps a glossary of the project's terms or records
the decisions that are hard to reverse, so every session re-learns the jargon and repeats settled
arguments.

Read [`docs/reviews/2026-11-overhaul-plan.md`](../docs/reviews/2026-11-overhaul-plan.md) in full,
including its rules for every workstream session, before starting.

**New paths this task creates**, so `touched_files` lists their existing parent instead: `.agents/skills/grill/` and `.agents/skills/domain-language/`. Within `.agents/skills/`, this task owns only the skill directories named in its `touched_files` and those new ones.

## Scope

**In scope:**

1. **A new `grill` skill**, draft, model-invoked (people say "grill me"; `spec-author` composes it).
   Study `skills/productivity/grilling/SKILL.md` and `skills/productivity/grill-me/SKILL.md` in
   Matt's repository. Carry over the mechanism, in this kit's words:
   - the decision tree, worked in **rounds** over the **frontier** (every decision whose
     prerequisites are settled);
   - every question numbered, with a recommended answer, worded so "yes" accepts it;
   - **facts are the agent's job, decisions are the person's**: a fact the environment can answer
     goes to a fresh-context subagent (or a direct lookup), never to the person, and only the
     questions downstream of a running lookup wait for it;
   - done when the frontier is empty and the person confirms a shared understanding;
   - a dictated brain dump is valid input.
   Add what this kit needs: a short closing **decisions record** (each settled decision, and each
   term the session minted) that `spec-author` and `new-task` consume, and the autonomy pointer.
2. **A new `domain-language` skill**, draft, model-invoked. Study
   `skills/engineering/domain-modeling/SKILL.md`, `GLOSSARY-FORMAT.md` and `ADR-FORMAT.md`. It
   keeps the target repository's glossary (find an existing one first; create `GLOSSARY.md` only
   when the first term is settled) and its decision records (create `docs/adr/` only when the first
   one is earned). An ADR is earned only when a decision is hard to reverse, surprising without
   context, and a real trade-off: all three. A mismatch between the glossary and a name in the code
   is a finding to report, never a rename to perform (`A2`). It writes into the target repository,
   so it follows that repository's conventions (`AGENTS.md`, the shape section).
3. **`spec-author` interviews.** Replace step 1 with: read the glossary and the ADRs in the area,
   then compose `grill` (a relative link, because the composition must work) until the frontier is
   empty, scaled to the change. Terms the interview settles go through `domain-language`. Amend
   [`docs/spec/spec-author.md`](../docs/spec/spec-author.md) with a dated amendment note and bring
   its conformance matrix up to date.
4. **`new-task` sizes by context.** Study `skills/engineering/to-tickets/SKILL.md`. Add: each task
   fits one fresh context window (exploration plus implementation; when it would not, split it);
   prefer vertical tracer-bullet slices that are verifiable on their own; sequence a wide refactor
   as expand, migrate in batches, contract; word tasks in the glossary's terms. Keep everything that
   makes a task file executable today (honest `touched_files`, the acceptance command, verified
   claims).
5. **Slim all six skills** per the plan's slimming rules. `spec-plan-readiness` and `spec-quality`
   keep their verdict semantics; cut their length, not their bar.

**Out of scope:** publishing tasks to an issue tracker (the kit is local-first), a prototype skill,
and every file outside `touched_files` except one `CHANGELOG.md` line. Catalog, README and roadmap
notes go under "Notes for integration" in the pull request body.

## Implementation notes

- `grill` and `domain-language` each carry a provenance block for every upstream file they adapt.
- `grill` must work in a harness with no subagents: say what to do instead (look the fact up
  directly, before the round).
- Keep `spec-author`'s stop-for-approval behaviour exactly as it is. Grilling happens before the
  draft, not instead of the human approval after it.

## Acceptance criteria (mechanically verifiable)

    python scripts/run-checks.py

- [ ] Exit 0, with the command and the verbatim tail in the pull request body.
- [ ] `grill` and `domain-language` exist, carry `status: draft` under `metadata`, and have
      provenance blocks.
- [ ] `spec-author` no longer limits itself to one question, and links `grill`.
- [ ] Every `SKILL.md` this task owns is at most about 250 lines, with a description under about
      400 characters that leads with its trigger.

## Definition of done

- [ ] Acceptance command passes.
- [ ] The spec amendment and conformance update are in the same pull request, flagged for the
      maintainer's approval.
- [ ] Task file moved to `.tasks/done/` with `status: done` and links re-anchored; one dated line in
      `CHANGELOG.md`.
- [ ] Draft pull request into `zen/overhaul-2026-11`, with "Notes for integration".
