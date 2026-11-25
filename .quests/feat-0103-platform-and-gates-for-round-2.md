---
id: feat-0103
title: Build the round 2 platform and gate changes the maintainer approved on 2026-11-25
type: feat
status: in_progress
priority: P1
parent: "Marjana round 2, Wave 1: Platform and gates (docs/reviews/2026-11-25-marjana-r2-plan.md)"
depends_on: []
spec: ""
scenarios: []
external: ""
mode: "hitl"
touched_files:
  - scripts/validate-skills.py
  - scripts/run-checks.py
  - scripts/check-citations.py
  - scripts/build-adapters.py
  - scripts/install.py
  - scripts/release.py
  - .quests/validate.py
  - .quests/.scaffold.json
  - .agents/skills/init-worktracking/templates/validate.py
  - .agents/skills/sitrep/scripts/sitrep.py
  - .agents/hooks/destructive-git-gate.py
  - .agents/hooks/README.md
  - .github/ISSUE_TEMPLATE/bug_report.yml
  - .github/ISSUE_TEMPLATE/skill_behavior.yml
  - docs/INSTALL.md
  - docs/RELEASING.md
  - docs/spec/validate-skills.md
  - docs/spec/validate-skills.conformance.md
  - docs/spec/build-adapters.md
  - docs/spec/build-adapters.conformance.md
  - docs/spec/install.md
  - docs/spec/install.conformance.md
  - docs/spec/sitrep.md
  - docs/spec/sitrep.conformance.md
  - docs/spec/cloud-executable.conformance.md
  - docs/reviews/2026-11-25-dogfood/platform.md
  - tests/fixtures/supporting-files.txt
  - tests/test_validate_skills.py
  - tests/test_validate_skills_composition.py
  - tests/test_run_checks.py
  - tests/test_run_checks_changelog.py
  - tests/test_run_checks_listings.py
  - tests/test_check_citations.py
  - tests/test_spec_digest.py
  - tests/test_build_adapters_codex.py
  - tests/test_hooks.py
  - tests/test_hooks_destructive_git.py
  - tests/test_install.py
  - tests/test_quests_validate.py
  - tests/test_sitrep_git.py
  - tests/test_issue_templates.py
  - tests/test_release.py
created: 2026-11-25
---

## Problem

The 2026-11-25 decisions ([decisions record](../docs/reviews/2026-11-25-marjana-decisions.md), [round 2 plan](../docs/reviews/2026-11-25-marjana-r2-plan.md)) approved eleven platform and gate items that need code rather than prose: B3 (`R-203`, a per-file list instead of one shared count), B4 (`R-204`, a changelog line warning as a ratchet), B11 (`R-003` composed-by check, `R-004` quoted-phrase audit), D3 (an opt-in destructive-git gate), D5 (a release script), E7 (the Codex `agents/openai.yaml` sidecar), E9 (zen and catalog completeness, a name-clash install note, issue templates), R2-3 (guarded load-by-name for drafts), D1's draft expiry warning, R2-10 (warnings on the old tracker names) and N1 (the both-directories warning firing on a stray `.tasks/__pycache__/`).

## Scope

**In scope:** the eleven items above, in the owned paths of the plan's Platform and gates row, each with tests that fail when the feature is removed, and amendments to the specs they change.

**Out of scope:** any `SKILL.md`, `.agents/rules/`, `AGENTS.md`, `CONTRIBUTING.md`, `docs/spec/zen-config*.md`, and the integrator's files (`CHANGELOG.md`, `ROADMAP.md`, `README.md`, `docs/CATALOG.md`). No tag is cut or pushed.

## Decisions

- **The old-name warnings are not promoted by `--strict`** in `.quests/validate.py`: the alias is a promise that an adopter's tree keeps working until the second tagged release, and a strict CI failing on the day the kit updates would break it early.
- **The destructive-git gate is in no committed wiring**, `.codex/hooks.json` and the opencode adapter included, since a session here runs those without anyone choosing them. `tests/test_hooks.py` asserts its absence there (`OPT_IN_HOOKS`) instead of exempting it silently; `install.py` still prints its registration.
- **The double-quoted phrase class (`R-004`) is report-only.** Measured first, as `R-004` asked: 290 phrases, 24 resolving in no file their row names, all in matrices this quest does not own. They are listed as `WARN` lines and do not fail the gate until someone disposes of them by hand.
- **The changelog limit is 330 raw characters, as `R-204` proposed**, against AGENTS.md's "about 300"; exceptions are keyed by the line's digest, so editing an excepted line makes it new.
- **No sidecar is written into this repository's own `.agents/skills/`**: Codex reads it directly, and a generated file among sources is the hand copy `build-adapters.py` exists to prevent.
- **A premise that turned out false:** `validate-skills.py` had no shipped-to-draft link check at all; the relative-link refusal lived only in `install.py` and `build-adapters.py`. R2-3's "a relative link to a draft still fails" is now true of the validator too.

## Risks and rollback

Touches several modules and the gate set (two new gates, `changelog lines` and `skill listings`, both in `DOCS_GATES`). Each item is independent; revert per file. The new validator warnings (draft expiry, unguarded load) never fail a run; the new errors (composed-by, a link to a draft) pass on the tree as it stands.

## Acceptance criteria (mechanically verifiable)

    ZEN_CHECKS_SCOPE=full python3 scripts/run-checks.py

- [ ] Every new check was run on an empty or degenerate input and each new test fails with its feature removed, recorded in [the dogfood record](../docs/reviews/2026-11-25-dogfood/platform.md).
- [ ] Approved specs changed carry a dated amendment naming `feat-0103`, flagged for re-approval.

## Definition of done

- [ ] Acceptance command passes.
- [ ] Left in `.quests/` for the orchestrator to close (B2).
