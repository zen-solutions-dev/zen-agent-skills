---
id: feat-0095
title: Integrate the Marjana workstreams, verify independently, and open one pull request
type: feat
status: open
priority: P1
parent: "ROADMAP 2026-11-24 Marjana overhaul"
depends_on: [chore-0100, feat-0091, feat-0092, feat-0093, feat-0094]
spec: ""
scenarios: []
touched_files:
  - .agents/skills/
  - .claude-plugin/
  - README.md
  - docs/CATALOG.md
  - docs/GETTING-STARTED.md
  - ROADMAP.md
  - CHANGELOG.md
  - docs/reviews/
created: 2026-11-24
---

## Problem

Five workstreams change the kit in parallel. Their reader-facing notes, the new drafts' place in the catalog, and the marketplace tree have to come together on one branch, be verified by someone who wrote none of it, and reach the maintainer as one pull request into `main`.

## Scope

**In scope** ([plan, Integration](../docs/reviews/2026-11-24-marjana-plan.md)): land each workstream after one fresh-context review and one fix round; apply every workstream's notes for integration to the reader documents; regenerate `.claude-plugin/`; combine the dogfood records; an independent verification by a session that wrote none of the work (`A7`); `retro` over this orchestration; `pr-describe` with the merge danger; one draft pull request into `main`; after it opens, `D3`.

**Out of scope:** new features beyond the workstreams' notes.

## Acceptance criteria (mechanically verifiable)

    ZEN_CHECKS_SCOPE=full python3 scripts/run-checks.py

- [ ] A verification report under `docs/reviews/` with a `pass` verdict from a session that authored none of the work.
- [ ] One open pull request from `zen/marjana-2026-11-24` into `main`.

## Definition of done

- [ ] Acceptance command passes locally.
- [ ] File moved to `.tasks/done/`, `status: done`; its `CHANGELOG.md` line written.
