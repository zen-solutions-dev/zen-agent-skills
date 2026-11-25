---
id: feat-0095
title: Integrate the Marjana workstreams, verify independently, and open one pull request
type: feat
status: done
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

**In scope** ([plan, Integration](../../docs/reviews/2026-11-24-marjana-plan.md)): land each workstream after one fresh-context review and one fix round; apply every workstream's notes for integration to the reader documents; regenerate `.claude-plugin/`; combine the dogfood records; an independent verification by a session that wrote none of the work (`A7`); `retro` over this orchestration; `pr-describe` with the merge danger; one draft pull request into `main`; after it opens, `D3`.

**Out of scope:** new features beyond the workstreams' notes.

## Acceptance criteria (mechanically verifiable)

    ZEN_CHECKS_SCOPE=full python3 scripts/run-checks.py

- [x] A verification report under `docs/reviews/` with a `pass` verdict from a session that authored none of the work.
- [ ] One open pull request from `zen/marjana-2026-11-24` into `main`.

## Definition of done

- [x] Acceptance command passes locally.
- [x] File moved to `.tasks/done/`, `status: done`; its `CHANGELOG.md` line written.

## Decisions

- **A premise that turned out false**: the plan assumed every landing could be a fast-forward. Once the first workstream landed, the rest were behind the tip. The orchestrator merged WS-C and WS-B itself (`c0579ad`, `6162d00`), mechanical conflicts only, before rule `D1`'s fast-forward-only text had landed. It then sent WS-E back to merge the tip itself. The independent verification re-derived both merges and found them correct, and rated the breach major; retro `R-201` puts the rule to the maintainer.
- **A seam left open deliberately**: the maintainer's decision `D3` (delete `zen/overhaul-ws1-align`; tag and delete `zen/eval-slice-71f3d5`; delete `claude/2026-10-22-oversight-tasks` after the cherry-pick) is not carried out here, because the session proxy refuses branch deletion both through `git push --delete` and through the REST API (retro `R-207`). The commands are left for the maintainer.

## Resolution

Closed 2026-11-24. All five workstreams landed, each after one fresh-context review, one fix round and a focused re-check on the exact commit. [The independent verification](../../docs/reviews/2026-11-24-marjana-verification.md) returned `pass` on `6793cb6`, with nine findings; the minor ones are fixed on the close-out commit. [The retro](../../docs/reviews/2026-11-24-retro-marjana.md) records ten proposals for approval. The one draft pull request into `main` is the criterion still open here: it is opened from this commit, so it cannot be ticked inside it.

