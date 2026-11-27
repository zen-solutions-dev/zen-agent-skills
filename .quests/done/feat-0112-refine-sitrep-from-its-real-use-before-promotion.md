---
id: feat-0112
title: Refine sitrep from its real use before promotion
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
  - .agents/skills/sitrep/SKILL.md
created: 2026-11-27
---

## Problem

The maintainer chose on 2026-11-27 to promote [`sitrep`](../../.agents/skills/sitrep/SKILL.md). Its real runs are in the dogfood records `docs/reviews/2026-11-24-dogfood/ws-e.md`, `docs/reviews/2026-11-25-dogfood/rollout.md` and `docs/reviews/2026-11-26-dogfood/rollout-r3.md`. They exposed three things its body does not yet say: the integration branch is best named as a remote-tracking ref in `.sitrep.json` (a local branch name does not resolve in a fresh clone, `chore-0122`); a stale local branch or leftover worktree inflates the in-flight list; and the board has no list of what can start now (`feat-0073` will add one).

## Scope

**In scope:** In `SKILL.md` only, as text the board's reader acts on: where the body describes the integration branch, say a repository may name it in `.sitrep.json`, and that a remote-tracking ref (for example `origin/developer`) also resolves in a fresh clone; one line in the report step on reading an inflated in-flight list (stale local branches and old worktrees count); one line that the board does not list ready work yet, naming `feat-0073` in backticks. Keep `status: draft` and the draft notice: the flip is `feat-0116`.

**Out of scope:** Changing `sitrep.py`, its spec or its tests (`feat-0111` and `feat-0073` own the behaviour). Removing the draft status. Any other file.

## Acceptance criteria (mechanically verifiable)

    ZEN_CHECKS_SCOPE=full python scripts/run-checks.py

- [ ] The three points are in `SKILL.md`, each consistent with `docs/spec/sitrep.md` as it stands.
- [ ] `python scripts/validate-skills.py` passes.

## Definition of done

- [ ] Acceptance command passes locally.
- [ ] Conventions in AGENTS.md's conventions section followed.
