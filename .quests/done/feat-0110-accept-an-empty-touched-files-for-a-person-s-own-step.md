---
id: feat-0110
title: Accept an empty touched_files on a hitl quest, which is a person's own step
type: feat
status: done
priority: P2
parent: "ROADMAP Campaign G: rollout (docs/reviews/2026-11-25-rollout-first-adopter.md, finding 2)"
depends_on: []
spec: ""
scenarios: []
external: ""
mode: afk
touched_files:
  - .quests/validate.py
  - .agents/skills/init-worktracking/templates/validate.py
  - .quests/_TEMPLATE.md
  - .agents/skills/init-worktracking/templates/
  - tests/test_quests_validate.py
  - .claude-plugin/
created: 2026-11-25
---

## Problem

The quests validator warns `touched_files is empty` on any open quest with no files ([`.quests/validate.py`](../validate.py), the `touched_files` check). With `--strict`, as an adopter's CI runs it, the warning is an error. But some quests are a person's own step that changes no file in the repository: a deploy, a dashboard setting, a review by someone outside. The kit's first adopter (the Zen product app, a private repository) had 19 such quests on 2026-11-25 and had to name the record each step is noted in, just to pass (finding 2 of [the first adopter run](../../docs/reviews/2026-11-25-rollout-first-adopter.md)). A made-up path is a dishonest `touched_files`, which is the thing the field exists to prevent.

## Scope

**In scope:**

- The validator accepts an empty `touched_files` list without a warning when the quest's `mode` is `hitl`. Any other mode, including empty (which takes the repository's default), warns as today.
- The same change in the shipped copy under `init-worktracking/templates/`, kept identical to this repository's copy (a test or gate already compares them; keep it green).
- The template's `touched_files` comment (both copies of `_TEMPLATE.md`) says so in one line.
- Tests first, per [`tdd`](../../.agents/skills/tdd/SKILL.md): a `hitl` quest with no files passes clean; an `afk` quest with no files still warns, and fails under `--strict`.
- Regenerate the marketplace with `python scripts/build-adapters.py --marketplace` if `init-worktracking` ships in it.

**Out of scope:** A new frontmatter key, or detecting "the body names a person" from prose (not mechanical). Changing any other check.

## Decisions

- **A rejected alternative:** requiring the body to name the person's step before the empty list is accepted. Rejected because it is not mechanically decidable; `mode: hitl` is the field that already says a person must be present.

- **A premise that turned out false:** this quest first said the two `validate.py` copies were byte-identical. They already differed in docstrings and comments at `f5ac3c8`; the gate compares executable code only, so the criterion was reworded at landing (2026-11-26).
- **A seam left open deliberately:** an absent `touched_files` key stays a required-field error on every mode, `hitl` included; only an empty list on a `hitl` quest is accepted. Relaxing the required field would change a second check (orchestrator's ruling, 2026-11-26).

## Acceptance criteria (mechanically verifiable)

    ZEN_CHECKS_SCOPE=full python scripts/run-checks.py

- [ ] `python -m pytest tests/test_quests_validate.py` (or the suite's own runner) passes, including the new cases.
- [ ] The two `validate.py` copies have identical executable code (`test_the_executable_code_is_identical_in_both_copies`).

## Definition of done

- [ ] Acceptance command passes locally.
- [ ] Conventions in AGENTS.md's conventions section followed.
