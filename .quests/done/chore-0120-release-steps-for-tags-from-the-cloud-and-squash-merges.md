---
id: chore-0120
title: Add the release steps a cloud session and a squash merge need to docs/RELEASING.md
type: chore
status: done
priority: P2
parent: "ROADMAP Campaign G: rollout (docs/reviews/2026-11-25-rollout-first-adopter.md, findings 3 and 4)"
depends_on: []
spec: ""
scenarios: []
external: ""
mode: afk
touched_files:
  - docs/RELEASING.md
created: 2026-11-25
---

## Problem

The v0.2.0 release on 2026-11-25 (pull request #119, merged into `main` as `e694817`) hit two steps [`docs/RELEASING.md`](../../docs/RELEASING.md) does not name, recorded as findings 3 and 4 in [the first adopter run](../../docs/reviews/2026-11-25-rollout-first-adopter.md):

1. **A cloud session cannot push a tag.** Its git proxy refused the `v0.2.0` tag push with HTTP 403, so the maintainer pushed it. `RELEASING.md` already leaves tagging to the person, but does not say why a session cannot do it, nor that the commit to tag must be named by id when `main` takes squash merges (the squash commit is not the branch's head).
2. **A squash merge into `main` leaves `developer` behind.** After the release, `main` had to be merged back into `developer` (pull request #120) so the two trees agree again. No step says so.

## Scope

**In scope:** In `docs/RELEASING.md`'s steps: the tag command names the merged commit by its id (`git tag -a vX.Y.Z -m "Zen Agent Skills vX.Y.Z" <sha>`), and a note that a cloud session's push of a tag is refused (403, seen 2026-11-25), so the person runs it from their own checkout; and a final step that merges `main` back into `developer` on a branch, through a pull request the person merges, when the release was a squash merge.

**Out of scope:** Changing `scripts/release.py` or what it prints (if its printed tag line should carry the sha, record that as a seam in this quest's Decisions rather than building it). Changing branch protection or rulesets.

## Acceptance criteria (mechanically verifiable)

    ZEN_CHECKS_SCOPE=full python scripts/run-checks.py

- [ ] `docs/RELEASING.md` names the tagged commit by id, says a cloud session cannot push the tag, and has the merge-back step.

## Definition of done

- [ ] Acceptance command passes locally.
- [ ] Conventions in AGENTS.md's conventions section followed.

## Decisions

- **A seam left open deliberately:** `scripts/release.py`'s `next_steps()` still prints `git tag -a vX.Y.Z -m "..."` with no commit id, while step 5 of `docs/RELEASING.md` now names the commit by id. Its verifier (2026-11-26) classed this as the anticipated seam, not a defect; teaching the script to print the id is out of this quest's scope.
- **A premise that turned out false:** step 6 says "this was pull request #120" while #120 was still open at landing (2026-11-26). It reads true once the maintainer merges #120, which precedes this branch's own pull request.
