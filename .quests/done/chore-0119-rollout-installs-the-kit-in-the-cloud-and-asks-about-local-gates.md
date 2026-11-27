---
id: chore-0119
title: Say how a rollout installs the kit in an adopter's cloud environment, and asks early about local-only gates
type: chore
status: done
priority: P2
parent: "ROADMAP Campaign G: rollout (docs/reviews/2026-11-25-rollout-first-adopter.md, findings 1 and 5)"
depends_on: []
spec: ""
scenarios: []
external: ""
mode: afk
touched_files:
  - docs/INSTALL.md
  - docs/reviews/2026-11-25-plan-rollout-campaign.md
created: 2026-11-25
---

## Problem

The kit's first run in an adopter repository (the Zen product app, a private repository) on 2026-11-25 hit two gaps that no document warned about. Both are recorded in [the first adopter run](../../docs/reviews/2026-11-25-rollout-first-adopter.md), findings 1 and 5.

1. **The kit was not installed where the work ran.** A cloud session sees only what the repository commits or what its environment's setup script installs, so `init-worktracking` could not run there, and its output was written by hand from the templates.
2. **The adopter's own pre-PR gate needs a file that never leaves the maintainer's computer** (a git-ignored list), so no cloud session could open a pull request there. The child correctly refused to go around the gate, and the person opened the pull requests from their own checkout.

[`docs/INSTALL.md`](../../docs/INSTALL.md) says nothing about either, and step 1 of the rollout map's "Smallest first slice" in [`2026-11-25-plan-rollout-campaign.md`](../../docs/reviews/2026-11-25-plan-rollout-campaign.md) mentions the setup script only in passing.

## Scope

**In scope:**

- A short section in `docs/INSTALL.md` for installing into a repository that is worked in cloud sessions: a saved cloud environment per repository whose setup script runs the install (with `--include-drafts` or not, the adopter's choice), why (a cloud session sees only what is committed or installed by the setup script), and the check that the skills are there before work starts. Model it on this repository's own `zen-agent-skills` environment (round 2, `B5`, in [the round 2 plan](../../docs/reviews/2026-11-25-marjana-r2-plan.md)).
- In the same section, the early question: does the adopter's pre-PR check need files that exist only on the person's computer? If yes, plan from the start for the person (or a session on their computer) to open the pull requests, and for cloud children to push branches and hand over the bodies.
- Steps 1 and 3 of the rollout map's "Smallest first slice" point at that section in one line each.

**Out of scope:** Changing `scripts/install.py`. Naming any adopter repository, its owner, or anything about its users: the kit is public, so the adopter is "the Zen product app (a private repository)" at most. Creating any cloud environment.

## Acceptance criteria (mechanically verifiable)

    ZEN_CHECKS_SCOPE=full python scripts/run-checks.py

- [ ] `docs/INSTALL.md` has the section, and the rollout map's steps 1 and 3 link to it.
- [ ] No private repository name, owner or person's name appears in the diff (`git diff origin/zen/rollout-r3-2026-11-25 -- docs/` read by eye, and the secret scan passes).

## Definition of done

- [ ] Acceptance command passes locally.
- [ ] Conventions in AGENTS.md's conventions section followed.
