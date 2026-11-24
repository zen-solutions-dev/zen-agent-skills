---
id: chore-0096
title: Give every skill step a completion criterion, and settle the length limit the overhaul set
type: chore
status: done
priority: P2
parent: "ROADMAP 2026-11 overhaul follow-up"
depends_on: [feat-0080]
touched_files:
  - .agents/skills/
  - .agents/rules/writing-for-agents.md
created: 2026-11-23
---

## Problem

The independent verification of the 2026-11 overhaul
([`2026-11-overhaul-verification.md`](../../docs/reviews/2026-11-overhaul-verification.md), findings F5
and F6) found two places where the overhaul did not meet its own yardstick, the
[`writing-for-agents.md`](../../.agents/rules/writing-for-agents.md) checklist:

- **F5: steps without a completion criterion.** The checklist says every step ends on a clear,
  demanding "Done when". Steps without one were found in `grill`, `domain-language`, `tdd`, `retro`,
  `improve-architecture`, `zen`, `fix-batch` (steps 4, 5 and 7), `house-review` (3, 5 and 7),
  `pr-describe` (1, 3 and 4), `doc-sync` (every step), `systematic-debugging` (3 and 5 to 8),
  `agent-handoff` (4), `spec-author` (4 and 5) and `new-task` (5 and 7).
- **F6: length.** `systematic-debugging` (300), `doc-sync` (257), `house-review` (256) and
  `fix-batch` (251) are over the plan's "about 250 lines", and the median is about 156 against a
  target of about 120. `quest-tracker` (283) predates the overhaul.

Both were deferred rather than rushed at integration time: adding a criterion is a behaviour change
in each step, and a criterion written to clear a finding is worse than none.

## Scope

**In scope:** a "Done when" on every step named above, each one checkable and demanding, starting
with the drafts so they meet the bar before promotion; then either move the next tier of reference
material in the four long skills behind `references/`, or amend the lens's checklist to state the
limit the kit actually holds, with the reason.

**Out of scope:** any change to what a step does.

## Acceptance criteria (mechanically verifiable)

    python scripts/run-checks.py

- [x] Exit 0.
- [x] Every step heading in the skills named above is followed, before the next heading, by a line
      starting "Done when".
- [x] The length decision is recorded in the lens or in the four skills.

## Definition of done

- [x] Acceptance command passes; `python scripts/build-adapters.py --marketplace` rerun if a shipped
      skill changed.
- [x] Task file moved to `.tasks/done/` with `status: done` and links re-anchored; one dated line in
      `CHANGELOG.md`.

## Decisions

- **The step heading set, and what counts as a criterion.** The mechanical check treats every `###`
  heading, plus `## Step N` headings (the shape `agent-handoff` uses), as a step whose span runs to
  the next heading of the same or a higher level, so a `####` subsection belongs to its step
  (`pr-describe` step 2). A criterion is a line that *starts* with "Done when", outside a code
  fence. Where a criterion already existed mid-paragraph (`grill`, `retro`, `fix-batch` step 1,
  `house-review` step 1, `improve-architecture`, `agent-handoff` step 1, `spec-author` step 3,
  `new-task` steps 2 to 4 and 6) it was moved onto its own line, unchanged in wording, except where
  noted below. Measured with the final check: 76 step headings, 47 without such a line at
  `6e48026`, and 0 after. The lens's checklist line now says the criterion
  sits on a line of its own beginning "Done when", so the check this task ran is the convention.
- **Steps that gained a new criterion, rather than a reflowed one: 36.** `grill` 4; `domain-language`
  5; `tdd` 7; `retro` 3 and 5; `improve-architecture` 4 and 5; `zen` 3; `fix-batch` 4, 5 and 7;
  `house-review` 3, 5, 6 and 7; `pr-describe` 1 to 4; `doc-sync` 0 to 5; `systematic-debugging` 3
  and 5 to 8; `agent-handoff` 4; `spec-author` 4 and 5; `new-task` 5, 6 (replacing the criterion
  that sat on its sub-item 2) and 7. Sharpened rather than added: `grill` step 1 (the report called
  it weak; it now also requires the request's glossary terms to be in hand) and `new-task` step 4
  (the split confirmed *and* every task given a parent, which the step already does).
- **`grill` step 4's loop got its exit stated.** "Then go back to step 3" gained "unless the new
  frontier is empty: then go to step 5". That is step 5's existing entry condition written where the
  loop is, not a behaviour change; the report's finding was precisely that the loop had no stop
  condition on the page.
- **`zen` has no step headings; the finding still applied.** Its procedure is a numbered list under
  "How to answer", where items 1, 2 and 4 already end on "Done when". Item 3 gained one in the same
  inline form. The heading check cannot see list items, so this one was checked by reading.
- **Rejected: a criterion that changes what a step does.** None was needed: every criterion states
  the end condition of work the step already describes. Where a step has an exit that skips the
  work (`improve-architecture` step 5 is optional; `systematic-debugging` steps 6 and 7 apply only
  when their condition holds; `pr-describe` step 1 may stop on an empty changeset), the criterion
  names that exit as done rather than forcing the work.
- **Length: the limit is amended in the lens, and the four skills each say so in one line.** Line
  counts at `6e48026`, then after this task: `systematic-debugging` 300 to 319, `doc-sync` 257 to
  277, `house-review` 257 to 268, `fix-batch` 252 to 264. Every criterion added lines, and only two
  pieces of reference material were honestly movable: `house-review`'s "Running this in Claude
  Code" section went to `house-review/references/claude-code.md` (the shape `fix-batch` already
  uses), and one rationale sentence in `doc-sync` step 5 went to `references/notes.md`. What is left
  over 250 in each is steps, gates and the output or record contract. The checklist line in
  `writing-for-agents.md` now states the limit the kit holds: about 250, exceeded only for procedure
  every run needs or the provenance footer, said in one line in the skill.
- **Rejected: moving `systematic-debugging`'s red-command construction ladder and tightening
  paragraph to `references/`.** It was tried and reverted. `tests/test_systematic_debugging.py`
  pins both to step 2 as red-command obligations (`feat-0077`'s mutations), so they are procedure,
  not reference, and moving them to meet a number is the move the amended checklist line now names.
  Also left inline on purpose: `fix-batch`'s wrong-base recovery and the nine-field report,
  `house-review`'s depth tables and evidence gate, `doc-sync`'s classification table and output
  rules, and every provenance footer (the placement `AGENTS.md` requires).
- **Citations and counts brought up to date.** `house-review.conformance.md` row `S-011` now cites
  `references/claude-code.md`; `scripts/check-citations.py` stays at 0 unresolved. The supporting-file
  count asserted in `tests/test_validate_skills.py` rose from 14 markdown files to 15 for the new
  reference, with the reason in its comment. The median target of about 120 lines was not pursued:
  it is a property of 29 skills, not of this task's four.
