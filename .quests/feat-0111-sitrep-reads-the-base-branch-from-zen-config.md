---
id: feat-0111
title: Have sitrep fall back to zen-config's base_branch for its integration branch
type: feat
status: open
priority: P2
parent: "ROADMAP Campaign G: rollout (docs/reviews/2026-11-25-rollout-first-adopter.md, finding 8)"
depends_on: []
spec: docs/spec/sitrep.md
scenarios: []
external: ""
mode: hitl
touched_files:
  - docs/spec/sitrep.md
  - docs/spec/sitrep.conformance.md
  - .agents/skills/sitrep/scripts/sitrep.py
  - .agents/skills/sitrep/SKILL.md
  - tests/
created: 2026-11-25
---

## Problem

`sitrep` chooses its integration branch from `.sitrep.json`, else `origin`'s default branch, else `main` ([`docs/spec/sitrep.md`](../docs/spec/sitrep.md), the configuration table). A repository configured for the kit already says where its work lands, in the `base_branch` key of `docs/agents/zen.md`'s `zen-config` block ([`docs/spec/zen-config.md`](../docs/spec/zen-config.md)). So every adopter whose base is not its default branch has to say the same thing twice. This kit is one (`chore-0122` adds its `.sitrep.json` meanwhile).

## Scope

**In scope:** An amendment to the sitrep spec: the order becomes `.sitrep.json`, then `zen-config`'s `base_branch`, then `origin`'s default branch, then `main`, with a scenario for each step it adds and the tier the figure earns. Then, once the maintainer approves the amended spec, the build, test first, and the conformance matrix updated.

**Out of scope:** Building before the amendment is approved. Any other sitrep change.

## Open question

Approve the amendment's order (`.sitrep.json` first, then `zen-config`), or should `zen-config` win over `.sitrep.json`? Recommended: `.sitrep.json` first, because it is sitrep's own file and the more specific one.

## Acceptance criteria (mechanically verifiable)

    ZEN_CHECKS_SCOPE=full python scripts/run-checks.py

- [ ] The spec carries the new order and scenarios, approved by the maintainer.
- [ ] The tests tagged with the new scenario ids pass.

## Definition of done

- [ ] Acceptance command passes locally.
- [ ] Conventions in AGENTS.md's conventions section followed.
