---
id: chore-0096
title: Give every skill step a completion criterion, and settle the length limit the overhaul set
type: chore
status: open
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
([`2026-11-overhaul-verification.md`](../docs/reviews/2026-11-overhaul-verification.md), findings F5
and F6) found two places where the overhaul did not meet its own yardstick, the
[`writing-for-agents.md`](../.agents/rules/writing-for-agents.md) checklist:

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

- [ ] Exit 0.
- [ ] Every step heading in the skills named above is followed, before the next heading, by a line
      starting "Done when".
- [ ] The length decision is recorded in the lens or in the four skills.

## Definition of done

- [ ] Acceptance command passes; `python scripts/build-adapters.py --marketplace` rerun if a shipped
      skill changed.
- [ ] Task file moved to `.tasks/done/` with `status: done` and links re-anchored; one dated line in
      `CHANGELOG.md`.
