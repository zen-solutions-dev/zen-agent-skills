---
id: feat-0101
title: Rename the work-tracking vocabulary from tasks to quests, keeping the old names as aliases
type: feat
status: in_progress
priority: P1
parent: "Marjana round 2, Wave 0: the quest rename (docs/reviews/2026-11-25-marjana-r2-plan.md, decisions R2-4 to R2-7)"
depends_on: []
spec: ""
scenarios: []
external: ""
mode: "hitl"
touched_files:
  - AGENTS.md
  - GLOSSARY.md
  - ROADMAP.md
  - docs/agents/zen.md
  - docs/spec/zen-config.md
  - docs/spec/zen-config.conformance.md
  - docs/spec/sitrep.md
  - docs/spec/sitrep.conformance.md
  - docs/spec/install.md
  - docs/spec/install.conformance.md
  - .quests/validate.py
  - .quests/README.md
  - .quests/_TEMPLATE.md
  - .quests/.scaffold.json
  - .agents/skills/new-quest/SKILL.md
  - .agents/skills/init-worktracking/SKILL.md
  - .agents/skills/init-worktracking/templates/validate.py
  - .agents/skills/init-worktracking/templates/quests-README.md.tmpl
  - .agents/skills/quest-tracker/SKILL.md
  - .agents/skills/sitrep/SKILL.md
  - .agents/skills/sitrep/scripts/sitrep.py
  - .agents/hooks/spec-conformance-gate.py
  - scripts/install.py
  - scripts/run-checks.py
  - tests/test_quests_validate.py
  - tests/test_zen_config.py
  - tests/test_sitrep_git.py
  - tests/test_install.py
created: 2026-11-25
---

## Problem

The kit names its unit of work a task, its tracker directory `.tasks/`, the skill that writes one
`new-task`, and the `zen-config` tracker value `tasks`. The maintainer decided on 2026-11-25 (R2-4
to R2-7 in [the round 2 plan](../docs/reviews/2026-11-25-marjana-r2-plan.md)) to rename the whole
vocabulary to quests, first and alone, so every later workstream writes quests: Campaign (was Epic),
Quest chain (was Feature), Quest (was Task), and a Side quest for a quest in no chain. An adopter's
repository configured with the old names must keep working.

## Scope

**In scope:** `git mv .tasks .quests` and `new-task` to `new-quest`; the tracker value `quests`;
every skill, rule, script, test, template and current document that names them; the old names
accepted as aliases by the validator (`tracker: tasks`, a validator in `.tasks/`), by `sitrep`
(`.tasks/` read beside `.quests/`), by `install.py` (`--skills new-task`, and retiring a recorded
`new-task` placement), by the conformance-gate hook's root markers, and in the wording of every skill
that reads the tracker; Campaign and Quest chain in `ROADMAP.md` and `AGENTS.md` section 3; the
hierarchy and the five rarity colours defined in `GLOSSARY.md`; dated amendments to the `zen-config`,
`sitrep` and `install` specs with their conformance rows; the regenerated `.claude-plugin/`. New
file: the dogfood record `docs/reviews/2026-11-25-dogfood/quests.md`.

**Out of scope:** renaming ids or their kind prefixes; rewriting the prose of historical records
(`docs/history/`, `docs/reviews/`, `CHANGELOG.md` lines, `.quests/done/`), where only links the move
broke are fixed; applying rarity to `research` (Wave 2); redesigning `quest-tracker` or `sitrep`;
`CHANGELOG.md`, `README.md` and `docs/CATALOG.md` beyond path fixes (the orchestrator's, `feat-0109`).

## Decisions

- **Rejected: a stub `new-task` skill that forwards to `new-quest`.** It would ship a second skill,
  spend description budget, and appear in every profile. The alias lives in `install.py` instead, and
  `new-quest`'s description names its old name so a request phrased the old way still finds it.
- **Rejected: one alias sentence in `core.md`.** `core.md` holds the autonomy rules and loads in every
  session; each skill that reads the tracker says it once instead, next to the path it names.
- **Seam left open: `quest-tracker`'s own `quests` key** means a run of steps on a tracker page, not a
  quest file. Renaming it would be a redesign and a data-format change, so it stays, with one
  sentence in the authoring guide; the collision is a question for the maintainer.
- **Seam left open: the rarity colours share their five names with `sitrep`'s evidence tiers**, which
  rank how a figure was derived. The glossary says they are different scales; whether to merge or
  rename one is the maintainer's question.

## Risks and rollback

It touches every module and changes a persisted path and a configuration value adopters configure
against. The aliases are the mitigation: an adopter's `.tasks/` and `tracker: tasks` keep validating
and keep being read. Rollback is reverting the branch's commits; the move is `git mv`, so history
follows either way.

## Acceptance criteria (mechanically verifiable)

    ZEN_CHECKS_SCOPE=full python3 scripts/run-checks.py

- [ ] `python3 .quests/validate.py --strict` exits 0.
- [ ] `tests/test_zen_config.py` S-043, the `OldTrackerNameTests` in `tests/test_sitrep_git.py` and
      `RenamedSkillTests` in `tests/test_install.py` pass, and each fails when its alias is removed.
- [ ] A scratch repository outside this checkout with `.tasks/` and `tracker: tasks` validates and is
      read by `sitrep`; an empty and a malformed `.quests/` give the messages recorded in the dogfood
      record.

## Definition of done

- [ ] Acceptance command(s) pass locally.
- [ ] Conventions in AGENTS.md's conventions section followed.
- [ ] `doc-sync` run over the reader-facing documents and its findings applied or dismissed with a reason.
- [ ] Left in `.quests/` for the orchestrator to close (decision B2); the `CHANGELOG.md` line is passed under Notes for integration.
