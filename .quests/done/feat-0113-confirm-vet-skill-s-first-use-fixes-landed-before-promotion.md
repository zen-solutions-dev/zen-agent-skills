---
id: feat-0113
title: Confirm vet-skill's first-use fixes landed before promotion
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
  - .agents/skills/vet-skill/SKILL.md
created: 2026-11-27
---

## Problem

The maintainer chose on 2026-11-27 to promote [`vet-skill`](../../.agents/skills/vet-skill/SKILL.md). Its one real run, vetting an outside author's `wayfinder` skill, is in `docs/reviews/2026-11-25-dogfood/ship.md` (the `vet-skill` section): the subagent listed thirteen gaps, and commit `cad9c99` names the fixes (scope over files loaded from outside the skill directory, a hooks-off clone with enough history, clash checks in every install location and in run-time names, shared input others edit, no remote images, a severity for known harness keys, a dependency-to-vet-first verdict, pinned copy-and-digest install steps, whose verdict it is).

## Scope

**In scope:** Check each fix the record and `cad9c99` name against the body at this commit, and fix in `SKILL.md` any that did not land or reads ambiguously. Report every one as landed, fixed here, or not applicable, with the line. Keep `status: draft`: the flip is `feat-0116`.

**Out of scope:** New vetting checks beyond the record. Running a new vetting. Any other file.

## Decisions

- **A premise that turned out false:** the quest expected some of the first vetting's fixes might be missing. Its builder (2026-11-27) found all thirteen in the body at `7b918ac`, each with its line, and made no commit; with no commit there was nothing for a separate verifier to check, so the orchestrator spot-checked three of the thirteen against the file (the hooks-off clone, no remote images, the dependency-to-vet-first verdict).

## Acceptance criteria (mechanically verifiable)

    ZEN_CHECKS_SCOPE=full python scripts/run-checks.py

- [ ] Every fix the record names is reported as landed, fixed here, or not applicable, with the line.
- [ ] `python scripts/validate-skills.py` passes.

## Definition of done

- [ ] Acceptance command passes locally.
- [ ] Conventions in AGENTS.md's conventions section followed.
