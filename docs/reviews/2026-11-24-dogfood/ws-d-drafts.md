# WS-D drafts for the orchestrator, 2026-11-24

Three drafts the WS-D dogfood runs produced for the orchestrator to finalise, written on 2026-11-24
against `zen/marjana-2026-11-24` at `9598355`, before any workstream had landed. Every claim about
a workstream's output below is the plan's intent, not a verified result; the orchestrator replaces
each with what actually landed. The record of the runs themselves is [`ws-d.md`](ws-d.md).

## 1. Pull request body (`pr-describe`)

Changeset, as `pr-describe` Step 1 resolved it on 2026-11-24: `origin/HEAD` is unset, so the
default branch fell back to `origin/main`; merge-base `220282a`. At `9598355` the integration
branch adds 978 lines over 11 files (the two research reports, the plan and five task files); the
five workstreams will add the rest. The repository's template, `.github/PULL_REQUEST_TEMPLATE.md`,
is followed, with Merge danger added after its last section.

```markdown
## Summary

The 2026-11-24 "Marjana" overhaul: a deep clean of the kit's always-loaded context, ledgers and
skills, bringing every skill current with what Matt Pocock's skills and aihero.dev teach, and
proving each on real work. Five workstreams landed on one integration branch; this is the one pull
request the plan promised.

## Context

The plan (`docs/reviews/2026-11-24-marjana-plan.md`) rests on two reports of the same date, the
sources delta and the Marjana inventory. The maintainer decided four one-way-door questions
(D1 to D4); every other decision is a two-way door, reversible by one revert.

## What changed

- **Context and ledgers (WS-A, `chore-0100`)**: <rule-only `AGENTS.md`, one-line `CLAUDE.md`,
  monthly archives under `docs/history/`, the reviews index; replace with what landed>
- **Setup and align (WS-B, `feat-0091`)**: <the `zen-config` spec and `docs/agents/zen.md`, both
  scaffolds user-invoked, the `mode: afk | hitl` task field, `grill` fog and out-of-scope>
- **Orchestrate and build (WS-C, `feat-0092`)**: <draft `orchestrate` and `research`, D1 in
  `autonomy.md` and `core.md`, integration-branch landing in `reconcile-worktrees`>
- **Ship, learn and lenses (WS-D, `feat-0093`)**: review runs once, fixes once, re-checks only the
  fixed findings, then stops (`house-review` Step 8, `review-quality` rule 8); a comment beside a
  workaround is a standards-axis smell; `retro` takes a sampled-sessions input, ratchets a stricter
  check in with an exception list, and audits checks for pruning; `pr-describe` offers a stacked
  split; `human-handoff` writes questionnaires; a runbook may ship as a standard-library script;
  `writing-for-agents.md` adds "write history, not the present" and "composition must load".
- **Platform and gates (WS-E, `feat-0094`)**: <the "Done when" validator warning, the roadmap
  draft-status check, the hermetic test home; replace with what landed>

## How this was verified

- [ ] `python scripts/run-checks.py` exited 0 <paste the tail; say which of the six CI cells ran>

Every skill a workstream owns was run on real work and recorded under
`docs/reviews/2026-11-24-dogfood/`, one file per workstream, each with its verdict. An independent
verification by a session that wrote none of it is at <path> (`A7`).

## Follow-ups / out of scope

- `R-003` and `R-004` stay owed, recorded not built.
- The three status drafts (`sitrep`, `quest-tracker`, `agent-observatory`) stay drafts.
- Spec amendments awaiting the maintainer's approval: `house-review` `S-025`, <others>.

## Merge danger

**Door:** one-way. D2 fixes the path and block format of `docs/agents/zen.md`, which every adopter's
repository will hold once they run the setup step; D1 widens what an unattended orchestrator may do.
Everything else reverts cleanly.
**Blast radius:** every adopter who installs after this merge: the shipped skills, the lenses and the
`init-worktracking` templates.
**Look:** scrutinise `docs/spec/zen-config.md` and the `autonomy.md` and `core.md` change; read the
skills; skim the ledgers and archives.
```

### Stack offer

Due: the Door is one-way and the branch will run far past 600 changed lines and five directories.
Offered, not performed; splitting rewrites the branch, which is the maintainer's call.

| Part | Takes | Door | Look |
|---|---|---|---|
| 1. Ledgers and context | WS-A's files | two-way | merge on evidence |
| 2. Lenses, review and learning | WS-D's files | two-way | merge on evidence |
| 3. Gates and platform | WS-E's files | two-way | merge on evidence |
| 4. Orchestrate and build, with D1 | WS-C's files | one-way (`autonomy.md`, `core.md`) | human review |
| 5. Setup, with D2 | WS-B's files and `docs/agents/zen.md` | one-way (the `zen-config` format) | human review |

Cost: parts 4 and 5 each read rules the others edit (`core.md`, the task template), so they may not
pass their checks alone; the plan already merges every workstream's tip into the integration
branch, so the cheaper split is two pull requests, parts 1 to 3 then parts 4 and 5, rather than five.

## 2. The maintainer's end-of-day update (`human-handoff`, partner register, message form)

```text
Marjana, 2026-11-24, end of day. <orchestrator: replace each bracket with what landed>

Where it stands: the plan is approved and five workstreams ran in parallel. <n> of 5 have landed on
zen/marjana-2026-11-24; one draft pull request into main is <open at #NNN | not yet open>.

Done today: the two research reports and the plan (your four decisions are in it as D1 to D4).
WS-D landed: review now stops after one fix round, retro ratchets and prunes, and the lenses carry
"write history, not the present" and "composition must load".

Needs you, in priority order:
1. Approve or reject the spec amendments marked pending (house-review S-025 among them). Nothing is
   blocked on them, but they are contracts and only you can approve one.
2. Decide whether to split the pull request in two (the stack offer in the body); one review on the
   two one-way doors is the point of it.
3. R-002, the ruleset that leaves developer's merges unchecked: a script that walks you through it
   in two minutes is drafted, not committed, if you want it.

Next: the orchestrator verifies, opens the pull request, then does D3 (the stale branches).
```

## 3. Questionnaire for the maintainer (`human-handoff`, questionnaire mode)

Run because the orchestrator cannot answer these and only the maintainer can. The send: the
recipient is the maintainer, who owns every contract and every merge into `main`; what WS-D needs
back is a decision on each item below.

```markdown
# Decisions WS-D cannot make for itself

**Purpose:** three contract and process decisions from the WS-D workstream that only you can take.
**From:** WS-D, via the orchestrator. **To:** the maintainer. **How your answers will be used:** each
becomes an approval line in the spec or a task filed with `new-task`.

## Context

WS-D taught review when to stop and taught `retro` to ratchet and prune. One contract changed:
`docs/spec/house-review.md` gained `S-025`, the re-check after one fix round.

## How to answer

Any time before the pull request merges, a few minutes in all. "Not sure" is a useful answer.

## Contracts

### Do you approve `house-review` `S-025` as written?

_Why this matters: until you do, the conformance matrix audits the skill against an unapproved
scenario._

>

## Process

### Should `retro` run on a schedule, on a sample of sessions, here?

_Why this matters: the sampled input exists now, but nothing runs it unless someone starts it._

>

### Do you want the R-002 ruleset script committed beside a runbook, or kept out of the repository?

>

## Anything else?

Anything we did not ask that we should know?

>
```
