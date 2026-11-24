---
id: feat-0087
title: Promote retro from its first real run, over pull request 108
type: feat
status: done
priority: P1
parent: "ROADMAP 2026-11 overhaul: drafts the overhaul added"
depends_on: []
spec: ""
scenarios: []
touched_files:
  - .agents/skills/retro/SKILL.md
  - .agents/skills/house-review/SKILL.md
  - docs/reviews/2026-11-retro-pr-108.md
  - .claude-plugin/plugin/
created: 2026-11-23
---

## Problem

`retro` is a draft because nobody had run it on real work. The roadmap's promotion condition for it is: "it has run on a real session or pull request and an approved proposal has landed". Writing more prose about it does not move it.

## The real use

Run on 2026-11-23 by the `kit-refresh-audit` session over [zen-solutions-dev/zen-agent-skills#108](https://github.com/zen-solutions-dev/zen-agent-skills/pull/108), with [#98](https://github.com/zen-solutions-dev/zen-agent-skills/pull/98) read for recurrence. The report is [`2026-11-retro-pr-108.md`](../../docs/reviews/2026-11-retro-pr-108.md): eight proposals (`R-001` to `R-008`), eight dismissals, and a guardrail inventory. Step 1's check command failed locally on 30 tests that CI passes, which became `R-001`; a retro that trusted CI's green result would have missed it.

**Half met.** The run happened. "An approved proposal has landed" has not: no proposal is approved yet. This task stays open until the maintainer approves at least one id and it lands (applied by its own task, with the show-it-failing rule from step 5). Promoting before then would be the faked use the rule forbids.

## What the use exposed

1. **Neither pull request had a single review comment.** This kit reviews by independent verification (`A7`), so the friction lives in verification records, fix commits, and task Decisions, not in GitHub review threads. Step 2 names "review comments" and "session moments" only, and an agent following it literally would have found nothing to read.
2. **Step 1's guardrail list missed the merge rules.** The second most important finding (`R-002`, required checks bind `main` only, so `developer` merges with cells unrun) came from the repository ruleset, which step 1 does not name. Branch protection is a guardrail.
3. **"Run the check command once" is expensive and its failure is ambiguous.** Here it took over two minutes and failed for an environmental reason (the real home directory), not because of the pull request under review. The step does not say how to tell a pre-existing failure from one the change caused, or to compare with CI's result for the same commit.
4. **The output block has no rank field**, but step 4 ranks by severity. The report added `rank:` to each proposal to make the order checkable.
5. **The maintainer's always-loaded rules are a guardrail source too.** `R-008` came from a global rule (docs-only pull requests skip tests) that this repository's CI does not implement. Step 1 reads the repository's written standards but not the user-level ones the agent actually runs under.

## Refinements (apply on promotion)

- Step 2: name verification records, fix commits ("Address the verification of ..."), and task Decisions ("A premise that turned out false") as primary sources alongside review comments, and say to use whichever the repository actually reviews with.
- Step 1: add branch protection and rulesets (`gh api repos/<owner>/<repo>/rulesets` where available) to the guardrail list; add user-level instruction files the agent loads; and say to compare a local failure with CI's result on the same commit before ranking it.
- Step 4: add `rank:` to the output block.

## Link conversion (on promotion)

- `house-review` to `retro`: `house-review` line "standing comment; `retro` is where that conversion happens." becomes a relative link, **only if** the composition should become an install edge. It should not: `house-review` does not compose `retro`, it only points the reader at it, and the link would pull a user-invoked skill into every profile that carries `house-review`. Recommended: keep the backtick name. Decide with the maintainer.
- `retro` to `house-review`: `retro` step 3 names `house-review` as the reader of the standards file. `retro` does not run `house-review` either. Same recommendation: keep the backtick name.

## Promotion (2026-11-24, approved by the maintainer in writing)

The maintainer approved `R-006`, and it landed in this change: one checklist line in `writing-for-agents.md`, "A summary, verdict rule or opening promise that restates a step is re-read against that step whenever either is edited; prefer pointing at the step to restating it." It is a written standard, not a check, so step 5's failing-then-passing rule does not apply; what was confirmed first is that the lens had no such line. Its evidence, three self-contradicting skills (`verifier-agent`, `spec-author`, `retro`) across two pull requests, stays in the retro report, not in the lens. `R-001` to `R-005`, `R-007` and `R-008` are not approved yet and are not applied. All three refinements applied; `metadata.status: draft` removed. `house-review` and `retro` keep naming each other in backticks, as recommended: neither runs the other.

## Acceptance criteria (mechanically verifiable)

    python scripts/run-checks.py
    python .tasks/validate.py

- [x] The real run's report exists under `docs/reviews/`.
- [x] At least one `R-` id approved by the maintainer and landed, with its failing-then-passing evidence.
- [x] Refinements above applied to `retro/SKILL.md`.
- [x] `metadata.status: draft` removed; the `(draft)` mark removed from `zen`; `docs/CATALOG.md` row moved out of drafts (coordinated with `kit-release-ready`, which owns the docs).
- [x] `python scripts/build-adapters.py --marketplace` rerun so the plugin tree carries it.

## Definition of done

- [x] Acceptance commands pass.
- [x] `doc-sync` over the reader-facing documents, findings applied or dismissed.
- [ ] Moved to `.tasks/done/`, links re-anchored; a dated `CHANGELOG.md` line (proposed in the pull request body, since `kit-release-ready` owns the file).
