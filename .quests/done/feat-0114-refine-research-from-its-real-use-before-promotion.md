---
id: feat-0114
title: Refine research from its real use before promotion
type: feat
status: done
priority: P2
parent: "ROADMAP Campaign G: rollout (docs/reviews/2026-11-27-promotions-plan.md)"
depends_on: []
spec: ""
scenarios: []
external: ""
mode: afk
touched_files:
  - .agents/skills/research/SKILL.md
created: 2026-11-27
---

## Problem

The maintainer chose on 2026-11-27 to promote [`research`](../../.agents/skills/research/SKILL.md), together with `orchestrate`, which links it. Its real runs: round 1's two research questions (`docs/reviews/2026-11-24-sources-delta.md`, and the dogfood rows in `docs/reviews/2026-11-24-dogfood/orchestrator.md` and `ws-c.md`) and round 2's citation sourcing (`docs/reviews/2026-11-25-dogfood/orchestrate.md`). The lessons they record are the reach probe, the never-reconstruct rule, the asker's spot-check, and proxies or bot checks that refuse a host until a restart.

## Scope

**In scope:** Check each lesson those records name against the body and its references, and fold in any that did not land, in the kit's own words. Report each as landed, fixed here, or not applicable, with the line. Keep `status: draft`: the flip is `feat-0116`.

**Out of scope:** A new research procedure. Fetching any source. Any file outside the skill's directory.

## Acceptance criteria (mechanically verifiable)

    ZEN_CHECKS_SCOPE=full python scripts/run-checks.py

- [ ] Every lesson the records name is reported as landed, fixed here, or not applicable, with the line.
- [ ] `python scripts/validate-skills.py` passes.

## Definition of done

- [ ] Acceptance command passes locally.
- [ ] Conventions in AGENTS.md's conventions section followed.
