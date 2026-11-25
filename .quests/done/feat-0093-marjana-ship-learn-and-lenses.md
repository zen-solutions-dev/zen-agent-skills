---
id: feat-0093
title: Teach review when to stop, the learning loop to ratchet and prune, and the lenses to keep documents honest
type: feat
status: done
priority: P1
parent: "ROADMAP 2026-11-24 Marjana overhaul"
depends_on: [chore-0099]
spec: ""
scenarios: []
touched_files:
  - .agents/skills/house-review/
  - .agents/skills/pr-describe/
  - .agents/skills/doc-author/
  - .agents/skills/doc-revise/
  - .agents/skills/doc-sync/
  - .agents/skills/human-handoff/
  - .agents/skills/retro/
  - .agents/skills/improve-architecture/
  - .agents/rules/writing-for-agents.md
  - .agents/rules/house-style.md
  - .agents/rules/review-quality.md
  - docs/spec/
  - docs/
created: 2026-11-24
---

## Problem

Nothing in the review chain says when to stop reviewing, and repeated broad reviews never converge. `retro` waits for a bad session, has no path for a check that cannot pass on day one, and never prunes a check that fires on good code. The lenses warn that a document is a stale cache, but give no rule for keeping one honest, and a skill named in prose is not reliably loaded ([sources delta](../../docs/reviews/2026-11-24-sources-delta.md)).

## Scope

**In scope** ([plan, WS-D](../../docs/reviews/2026-11-24-marjana-plan.md)):

- `house-review`: review once, fix once, re-check only the fixed findings, then stop; the comment beside a workaround as a standards-axis smell; an optional cross-family reviewer line. Under about 250 lines, history to `references/`.
- `pr-describe`: offer a stacked split when a large branch holds a one-way door, with human review mandatory only on that one.
- `retro`: a sampled-sessions input (about one in five, failures first); ratchet a stricter check with an exception list; a periodic checks audit that removes a check firing on good code.
- `human-handoff`: a questionnaire mode, for when the person cannot answer and someone else must.
- `doc-author`: a runbook may ship as a standard-library Python script (never bash), taking secrets by hidden entry and confirming before irreversible steps.
- `writing-for-agents.md`: "write history, not the present" (date claims, cite the commit, no bare "currently"); "composition must load" (a composing step says read and follow the sibling now). Apply the second to every composing step in the skills you own; list the other skills' composing steps for integration.
- `doc-sync` under about 250 lines. `improve-architecture`: run it on `scripts/` and leave its report for the maintainer as the dogfood.
- `P10` and the slimming rules for every skill you own.

**Out of scope:** skills other workstreams own; scripts and tests (WS-E).

## Acceptance criteria (mechanically verifiable)

    ZEN_CHECKS_SCOPE=full python3 scripts/run-checks.py

- [x] `wc -l .agents/skills/house-review/SKILL.md .agents/skills/doc-sync/SKILL.md` prints at most 250 for each, or the file states its one-line reason.
- [x] `grep -n -i "ratchet" .agents/skills/retro/SKILL.md` finds the new input.
- [x] `docs/reviews/2026-11-24-dogfood/ws-d.md` has a row for every skill this task owns.

## Definition of done

- [x] Acceptance command passes locally.
- [x] Notes for integration and the `CHANGELOG.md` line reported to the orchestrator.
- [x] File moved to `.tasks/done/`, `status: done`.

## Decisions

- **The house-review contract was amended, not left alone.** Step 8 (the re-check) is a behaviour, so `docs/spec/house-review.md` gained `S-025`, pending the maintainer's approval, and the conformance matrix was re-audited the same day. The fig-leaf smell and the cross-family reviewer are lens and procedure guidance and add no scenario. `doc-sync`'s new habit (an undated "currently" is a claim to ground) narrows nothing in its contract, so its spec is unamended and its matrix records the re-check of every quoted clause.
- **No new sibling links into `core` or `spine`.** Every composing step now says read and follow, but the only link added is `improve-architecture` to `grill`, and `improve-architecture` sits in no profile seed, so `EXPECTED_PROFILE_MEMBERSHIP` is unchanged.
- **`retro`'s `R-101` from the dogfood rests on a false premise** (it read an unpushed local commit as landed); recorded in the dogfood file rather than filed.
