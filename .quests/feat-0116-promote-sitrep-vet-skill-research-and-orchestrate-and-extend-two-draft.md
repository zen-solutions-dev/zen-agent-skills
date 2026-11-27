---
id: feat-0116
title: Promote sitrep, vet-skill, research and orchestrate, and extend two drafts
type: feat
status: open
priority: P2
parent: "ROADMAP Campaign G: rollout (docs/reviews/2026-11-27-promotions-plan.md)"
depends_on: [feat-0112, feat-0113, feat-0114, feat-0115]
spec: ""
scenarios: []
external: ""
mode: afk
touched_files:
  - .agents/skills/sitrep/SKILL.md
  - .agents/skills/vet-skill/SKILL.md
  - .agents/skills/research/SKILL.md
  - .agents/skills/orchestrate/SKILL.md
  - .agents/skills/agent-observatory/SKILL.md
  - .agents/skills/quest-tracker/SKILL.md
  - .agents/skills/zen/SKILL.md
  - docs/CATALOG.md
  - scripts/install.py
  - .claude-plugin/
created: 2026-11-27
---

## Problem

The maintainer chose on 2026-11-27 to promote `sitrep`, `vet-skill`, `research` and `orchestrate` (each refined from its real use first, `feat-0112` to `feat-0115`), and to extend `agent-observatory` and `quest-tracker` by 60 days, because their core actions have not run on real work (renaming or messaging a session; publishing a tracker page). The last promotion, `feat-0084` to `feat-0089` (commit `aa1d721`), is the precedent.

## Scope

**In scope:** For the four: remove `status: draft` and `drafted` under `metadata`, and each body's draft notice; where a shipped skill composes one of them and names it in backticks or the guarded load form, make it a relative link (AGENTS.md section 5), and where it only names it, leave the backticks; list each in `zen` and `docs/CATALOG.md` as the precedent did; choose each one's install profile following the precedent and `docs/spec/install.md`, and say why in this quest's Decisions; update any profile table the precedent updated (README, getting started, INSTALL); regenerate the marketplace with `python scripts/build-adapters.py --marketplace`. For the two: add `extended: "2026-11-27: <the step still owed>"` under `metadata`.

**Out of scope:** Further refinements to any skill (`feat-0112` to `feat-0115` own those). `CHANGELOG.md` and `ROADMAP.md` (the orchestrator's). Promoting any other draft.

## Acceptance criteria (mechanically verifiable)

    ZEN_CHECKS_SCOPE=full python scripts/run-checks.py

- [ ] The four skills carry no `status: draft`, appear in `zen` and `docs/CATALOG.md`, and `python scripts/install.py --dry-run` places each in its chosen profile.
- [ ] The two drafts carry `extended` with a dated reason, and `python scripts/validate-skills.py` reports no expiry warning for them.
- [ ] The marketplace gate is green.

## Definition of done

- [ ] Acceptance command passes locally.
- [ ] Conventions in AGENTS.md's conventions section followed.
