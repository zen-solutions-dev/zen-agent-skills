---
id: feat-0078
title: Close the loop, with retro, two-axis review, merge danger, and an improve-architecture draft
type: feat
status: done
priority: P1
parent: "ROADMAP 2026-11 overhaul WS3 Ship and learn"
depends_on: [chore-0095]
spec: docs/spec/house-review.md
scenarios: []
touched_files:
  - .agents/skills/
  - .agents/skills/house-review/
  - .agents/skills/pr-describe/
  - .agents/skills/doc-author/
  - .agents/skills/doc-revise/
  - .agents/skills/doc-sync/
  - .agents/skills/human-handoff/
  - .agents/rules/review-quality.md
  - docs/spec/house-review.md
  - docs/spec/house-review.conformance.md
  - docs/spec/doc-sync.md
  - docs/spec/doc-sync.conformance.md
  - docs/spec/tracker-links.md
  - docs/spec/tracker-links.conformance.md
  - CHANGELOG.md
created: 2026-11-23
---

## Problem

Nothing in the kit learns. When a review comment or a correction repeats, no skill turns it into
something that stops it repeating. Matt Pocock's loop ends with a retro whose question is "how can I
improve my environment so I never have to write this comment again?", and whose answer is
**always choose determinism**: a mechanical mistake becomes a check (type, lint rule, test, hook,
CI), and only a genuine judgement call becomes a written standard, which review reads and
implementation does not.

Review and shipping have the same gap from the other side:

- [`house-review`](../../.agents/skills/house-review/SKILL.md) applies one rubric. It does not separately
  ask whether the change did what its contract asked, no more and no less, and it never reads the
  target repository's own written standards. Picking its depth takes a whole second skill,
  `review-depth`, at 380 lines.
- [`pr-describe`](../../.agents/skills/pr-describe/SKILL.md) gets closing keywords right but never tells
  the human how hard to look: whether the change is a one-way or two-way door, and how wide its blast
  radius is.
- Nothing finds where a codebase has become hard for an agent to work in. In the podcast Matt runs an
  architecture review on a schedule because "poorly organized code bases are harder to explore".

Read [`docs/reviews/2026-11-overhaul-plan.md`](../../docs/reviews/2026-11-overhaul-plan.md) in full,
including its rules for every workstream session, before starting.

**New paths this task creates**, so `touched_files` lists their existing parent instead: `.agents/skills/retro/` and `.agents/skills/improve-architecture/`. Within `.agents/skills/`, this task owns only the skill directories named in its `touched_files` and those new ones.

## Scope

**In scope:**

1. **A new `retro` skill**, draft, `invocation: user` under `metadata`. Study
   `skills/engineering/retro/SKILL.md`. It reads the primary sources (the session, the pull request,
   its review comments, or the last N pull requests) and proposes environment improvements ranked by
   severity: navigation pointers, automated checks, written standards, always-loaded instructions
   that belong elsewhere, expensive tool use, no-op instructions, missing information access. It reads
   the repository's existing check command first, so an unwired or broken check is the finding rather
   than a reinvention, and a repository with no guardrail at all is itself a finding. It reports and
   proposes; it applies a change only on approval. It composes the
   [`writing-for-agents.md`](../../.agents/rules/writing-for-agents.md) lens.
2. **A new `improve-architecture` skill**, draft, `invocation: user` under `metadata`. Study
   `skills/engineering/improve-codebase-architecture/` and `skills/engineering/codebase-design/`. It
   scopes to hot spots from recent history, uses the deep-module vocabulary (depth, seam, locality,
   the deletion test), may design an interface twice in parallel fresh-context subagents, and writes a
   report that works offline (no CDN). Its candidates feed `spec-author` or `new-task`.
3. **`house-review` on two axes.** A **spec axis** (over or under the contract or task) and a
   **standards axis** (the target repository's written standards, for example `CODING_STANDARDS.md`
   or `CONTRIBUTING.md`, plus the rubric in `review-quality.md`), run as independent passes, each
   through the existing evidence gate, with no reranking across axes. Fold what `review-depth` decides
   into a short depth section of `house-review` and remove `house-review`'s link to it. Leave the
   `review-depth` directory in place: tests, a hook and the installer name it, so the integration
   task (`feat-0080`) deletes it with them. Amend
   [`docs/spec/house-review.md`](../../docs/spec/house-review.md) with a dated note and update its
   matrix. Study `skills/engineering/code-review/SKILL.md`.
4. **`pr-describe` states the merge danger**: the evidence (a command and its output, or a
   screenshot), one-way or two-way door, and blast radius, ending in how hard a human should look.
   Study `skills/engineering/pr/SKILL.md`. Keep the closing-keyword behaviour and its contract
   exactly.
5. **Slim `doc-author`, `doc-revise`, `doc-sync` and `human-handoff`** per the plan's rules. Keep
   `doc-sync`'s dry-run default and its classification of what may be corrected.

**Out of scope:** merging `doc-author` into `doc-revise`, deleting any skill directory (including
`review-depth`), and every file outside `touched_files` except one `CHANGELOG.md` line. References to
`review-depth` in `README.md`, `docs/CATALOG.md`, `docs/ARCHITECTURE.md`, `docs/OBSERVATORY.md`,
`ROADMAP.md` and `docs/spec/install.conformance.md` go under "Notes for integration".

## Implementation notes

- `retro` and `improve-architecture` each carry a provenance block for every upstream file they
  adapt.
- The two review axes must work in a harness with no subagents: say what to do instead (run them in
  sequence, and finish the first axis's findings before reading for the second).
- `review-quality.md` is a topical lens; add the standards-axis guidance there rather than in the
  skill body.
- `python scripts/check-provenance.py` reported drift on 2026-11-23 for both upstreams of `review-quality.md` (`moonray/repoprompt-workflows`). Read what changed upstream; fold in only what this task's scope already covers, and leave the recorded digests alone unless you reconcile the difference (`AGENTS.md`, provenance).

## Decisions

- **Rejected: keeping `review-depth`'s output block and its full rationale inside `house-review`.**
  The selection rule, the signal table, the three knobs and the fallback are in Step 2; the incidents
  and measurements that justify each rule moved to `house-review/references/rationale.md`. Keeping
  them inline would have put the skill near 400 lines against a target of about 250.
- **Premise that turned out false: the task's owned paths were enough to keep the acceptance
  command green.** Three files outside `touched_files` pin facts this task had to change, and each
  got the minimum edit, flagged for integration: `tests/test_install.py`
  (`EXPECTED_PROFILE_MEMBERSHIP`: `spine` loses `review-depth`, because `house-review` no longer
  links it, and `doc-author`, because `doc-sync` and `doc-revise` now name it in backticks as the
  neighbour it is); `.agents/hooks/skill-reachability-reminder.py` (`KIT_SKILL_NAMES` gains `retro`
  and `improve-architecture`, which the hook's own test demands in the same commit); and
  `tests/test_validate_skills.py` (the supporting-file count rises from 3 to 7 markdown files).
- **Seam left open: `spine` no longer places `doc-author`.** That follows from the slimming rule (a
  neighbour is named, not linked). If the default install should still carry it, add it to the
  `spine` seed in `install.py` during integration rather than restoring a link that is not a
  composition.
- **Seam left open: the `moonray/repoprompt-workflows` drift on `review-quality.md` is read, not
  reconciled.** Upstream now carries an `inspected`-scope proof and a keep-valid-siblings rule; both
  were in this task's scope and were folded in, in this kit's words. Its other additions (a
  revalidation gate for `fixed`, futility classification, frozen-baseline re-anchoring) are outside
  this task. The snapshot originally adapted from is gone, so the difference cannot be fully
  reconciled and the recorded digests were left alone.
- **Rejected: a smell baseline (Fowler's code smells) on the standards axis.** Matt's `code-review`
  carries one; the lens's readability category already covers the same ground, and a second list
  would be a second source of truth for one meaning.
- **Rejected: `improve-architecture`'s report loading Tailwind and Mermaid from a CDN**, as the
  upstream does. The task requires a report that works offline, so diagrams are inline SVG or HTML
  and a Mermaid block, if any, is text.

## Acceptance criteria (mechanically verifiable)

    python scripts/run-checks.py

- [x] Exit 0, with the command and the verbatim tail in the pull request body.
- [x] `retro` and `improve-architecture` exist with `status: draft` and `invocation: user` under
      `metadata`, and provenance blocks.
- [x] No skill links to `review-depth`, and `house-review` carries the depth decision itself.
- [x] `pr-describe` produces a merge-danger section.

## Definition of done

- [x] Acceptance command passes.
- [x] Spec amendments flagged for the maintainer's approval in the pull request.
- [x] Task file moved to `.tasks/done/` with `status: done` and links re-anchored; one dated line in
      `CHANGELOG.md`.
- [x] Draft pull request into `zen/overhaul-2026-11`, with "Notes for integration".
