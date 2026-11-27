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

## Decisions

- **Profiles: no seed changes; all four land in `all` only.** The precedent (`aa1d721`) changed no `PROFILE_SEEDS` entry: a promoted skill reached `spine` only through a link from a spine skill (`grill`, `domain-language`, `tdd`), and the three a person starts by name went to `all`. Here no spine skill composes any of the four, so the same rule places them in `all`: `orchestrate` and `vet-skill` are user-invoked, like `zen`, `retro` and `improve-architecture`; `sitrep` and `research` are model-invoked but are not steps of the contract-driven delivery loop `spine` is defined as in `docs/spec/install.md`, and seeding them would spend default-install description budget on every adopter. `core` and `spine` are unchanged (3 and 20); `all` grows from 25 to 29. `scripts/install.py` needs no edit.
- **Links: none added.** The only shipped skill that composes one of the four is `orchestrate`, and its load of `research` was already a relative link. `fix-batch` and `autonomy.md` only name `orchestrate`, `sitrep` and `research` name each other's rarity ladder, and `zen` names every skill in backticks by design, so all keep backticks. The guarded loads of `research` in `teach` and `wayfinder` stay guarded: both are still drafts, and the guarded form remains whole for them.
- **Draft notices.** `sitrep` loses its "This skill is a draft" sentence and keeps the built-in-stages statement as history; `orchestrate` keeps its pointer to `references/first-run.md`; `research`'s Evidence section now says "This skill is written from", not "This draft"; `vet-skill` carried no body notice.
- **Extensions.** `agent-observatory` and `quest-tracker` carry `extended: "2026-11-27: ..."` naming the step still owed. The plan says 60 days; the validator and AGENTS.md section 7 count 90 from the extension date, so the value records the date and the reason, not a length.

## Acceptance criteria (mechanically verifiable)

    ZEN_CHECKS_SCOPE=full python scripts/run-checks.py

- [ ] The four skills carry no `status: draft`, appear in `zen` and `docs/CATALOG.md`, and `python scripts/install.py --dry-run` places each in its chosen profile.
- [ ] The two drafts carry `extended` with a dated reason, and `python scripts/validate-skills.py` reports no expiry warning for them.
- [ ] The marketplace gate is green.

## Definition of done

- [ ] Acceptance command passes locally.
- [ ] Conventions in AGENTS.md's conventions section followed.
