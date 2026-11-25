---
id: chore-0099
title: Groundwork for the 2026-11-24 Marjana overhaul, research and plan
type: chore
status: done
priority: P1
parent: "ROADMAP 2026-11-24 Marjana overhaul"
depends_on: []
spec: ""
scenarios: []
touched_files:
  - docs/reviews/2026-11-24-sources-delta.md
  - docs/reviews/2026-11-24-marjana-inventory.md
  - docs/reviews/2026-11-24-marjana-plan.md
  - .tasks/.scaffold.json
created: 2026-11-24
---

## Problem

The maintainer asked for a full overhaul, the "Marjana" deep clean: learn what Matt Pocock's skills, aihero.dev, and his video teach that this kit has not adopted; clear the context bloat and drift that has accreted; bring every skill current, tested and dogfooded; and deliver it as one pull request. Nothing could be dispatched until the delta and the dust were mapped.

## Scope

**In scope:** two research child sessions, each producing one report, the [sources delta](../../docs/reviews/2026-11-24-sources-delta.md) and the [inventory](../../docs/reviews/2026-11-24-marjana-inventory.md); the [plan](../../docs/reviews/2026-11-24-marjana-plan.md) with the maintainer's four decisions; task ids `chore-0100` and `feat-0091` to `feat-0095` reserved.

**Out of scope:** any change to a skill, rule, script or reader document.

## Decisions

- **A premise that turned out false**: the video transcript was assumed fetchable. YouTube's bot check refused both the research session and the orchestrator; no workaround was attempted, and the 2026-11 overhaul's transcript-derived conclusions stand.

## Acceptance criteria (mechanically verifiable)

    python3 scripts/run-checks.py

- [x] The three reports exist under `docs/reviews/`.
- [x] Every workstream task file passes `python3 .tasks/validate.py --strict`.

## Definition of done

- [x] Acceptance command passes locally.
- [x] File moved to `.tasks/done/`, `status: done`; `CHANGELOG.md` line supplied to WS-A.
