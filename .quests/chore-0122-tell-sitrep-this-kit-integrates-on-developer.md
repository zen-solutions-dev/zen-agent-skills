---
id: chore-0122
title: Tell sitrep that this kit integrates on developer, with a committed .sitrep.json
type: chore
status: open
priority: P2
parent: "ROADMAP Campaign G: rollout (docs/reviews/2026-11-25-rollout-first-adopter.md, finding 8)"
depends_on: []
spec: ""
scenarios: []
external: ""
mode: afk
touched_files:
  - .sitrep.json
created: 2026-11-25
---

## Problem

[`sitrep`](../.agents/skills/sitrep/SKILL.md) takes its integration branch from `.sitrep.json`'s `integration_branch` key, else the remote `origin`'s default branch, else `main` ([`docs/spec/sitrep.md`](../docs/spec/sitrep.md), the configuration table). This kit's default branch is `main`, but its work lands on `developer` (`base_branch` in [`docs/agents/zen.md`](../docs/agents/zen.md)). So the board measures "in flight" against `main`, and on a checkout without `main` it says `no integration branch` (finding 8 of [the first adopter run](../docs/reviews/2026-11-25-rollout-first-adopter.md)).

## Scope

**In scope:** A committed `.sitrep.json` at the repository root with `"integration_branch": "origin/developer"`, in the format the sitrep spec defines; run `python .agents/skills/sitrep/scripts/sitrep.py` before and after and quote both in the report.

**Out of scope:** Changing `sitrep.py` or its spec. Teaching sitrep to read `base_branch` from `zen-config` is `feat-0111`, which needs a spec amendment approved first.

## Acceptance criteria (mechanically verifiable)

    ZEN_CHECKS_SCOPE=full python scripts/run-checks.py

- [ ] `.sitrep.json` exists with `integration_branch: origin/developer`, and sitrep's in-flight list is measured against `origin/developer`, also in a fresh clone with no local `developer` (its output shows no `no integration branch` notice).

## Definition of done

- [ ] Acceptance command passes locally.
- [ ] Conventions in AGENTS.md's conventions section followed.

## Decisions

- **A premise that turned out false:** the first build wrote `developer`, as this quest then said. Its verifier (2026-11-26) found that a local branch name does not resolve in a fresh clone, where the board then shows nothing in flight, and that sitrep's own fallback already uses a remote-tracking ref (`origin/main`). The orchestrator changed the value to `origin/developer` (a two-way door; revert by editing one line).
