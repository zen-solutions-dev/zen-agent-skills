---
id: chore-0115
title: Plan the rollout of the kit into the maintainer's repositories, the Zen product app first
type: chore
status: open
priority: P2
parent: "Marjana round 2, Phase 3: plans only (docs/reviews/2026-11-25-marjana-r2-plan.md)"
depends_on: []
spec: ""
scenarios: []
external: ""
mode: hitl
touched_files:
  - docs/reviews/2026-11-25-plan-rollout-campaign.md
  - docs/reviews/README.md
created: 2026-11-25
---

## Problem

Phase 3 of the [round 2 handoff](../docs/reviews/2026-11-25-round-2-handoff.md) (section 6) asks for one short plan per wider goal, ending in the questions only the maintainer can answer, and says to stop and check in before building any of them. This quest is the plan for the rollout campaign: install and run the kit in each repository the maintainer keeps, the Zen product app first, as a `wayfinder` map. The round 2 plan reserves this quest for the rollout; the maintainer wants the kit's own setup squared away in their repositories, to show others how it is done. Only he can name the repositories.

## Scope

**In scope:** the plan [`docs/reviews/2026-11-25-plan-rollout-campaign.md`](../docs/reviews/2026-11-25-plan-rollout-campaign.md): goal, what exists to build on (with paths), the smallest first slice, risks and one-way doors, a rough size, and the questions for the maintainer, each standing on its own with the recommended option first. Its row in [`docs/reviews/README.md`](../docs/reviews/README.md).

**Out of scope:** Installing the kit in any repository, or naming repositories on the maintainer's behalf. Building any slice the plan proposes: that waits on the maintainer's answers and becomes its own quests.

## Acceptance criteria (mechanically verifiable)

    python scripts/run-checks.py

- [ ] The plan exists, is under about 120 lines, and ends in a "Questions for the maintainer" section.
- [ ] Every podcast claim in it cites a section of [the podcast extraction](../docs/reviews/2026-11-25-podcast-extraction.md).
- [ ] `docs/reviews/README.md` lists the plan.

## Definition of done

- [ ] Acceptance command passes locally.
- [ ] Conventions in AGENTS.md's conventions section followed.
- [ ] The maintainer has answered the plan's questions, and the answers are recorded in the plan or the decision record.
- [ ] File moved to `.quests/done/`, `status: done`; one dated line added to `CHANGELOG.md` referencing this quest id (by the integration owner, `feat-0109`).
