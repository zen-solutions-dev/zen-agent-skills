---
id: feat-0094
title: Gates for the drift this round found, a truthful budget, and the owed retro checks
type: feat
status: open
priority: P1
parent: "ROADMAP 2026-11-24 Marjana overhaul"
depends_on: [chore-0099]
spec: ""
scenarios: []
touched_files:
  - scripts/
  - tests/
  - .github/workflows/
  - .agents/hooks/
  - .agents/skills/sitrep/
  - .agents/skills/quest-tracker/
  - .agents/skills/agent-observatory/
  - docs/spec/
  - .tasks/done/feat-0090-one-span-aware-reader-for-links-and-profile-edges.md
  - .tasks/done/chore-0059-the-third-and-fourth-copies-of-the-link-helpers-are-unguarded.md
created: 2026-11-24
---

## Problem

The drift this round found was all mechanical, and no gate saw it: a roadmap naming promoted skills as drafts ([inventory `P3`](../docs/reviews/2026-11-24-marjana-inventory.md)), workflow steps without a "Done when" (`R-005`), and a description budget headline that counts characters Claude Code never loads (`P11`). Three retro checks are owed (`R-001`, `R-005`, `R-007`), and adopters are never told to configure the skills per repository.

## Scope

**In scope** ([plan, WS-E](../docs/reviews/2026-11-24-marjana-plan.md)), each change test-first with `tdd`:

- `R-005`: `validate-skills.py` warns when a workflow-shaped skill has a step with no "Done when" line; a declared lens is exempt.
- `P3`: the `roadmap bookkeeping` gate fails when `ROADMAP.md` names a skill as a draft whose frontmatter is not `status: draft`, or the reverse.
- `P11`: `install.py`'s budget headline is the model-invoked total; the user-invoked share is the aside. Amend `docs/spec/install.md` with a dated note.
- `R-001`: the test gate runs with a hermetic home (`HOME`, `USERPROFILE`, `XDG_CONFIG_HOME` pointed at a scratch directory). `R-007`: `tests/test_undecodable_names.py`.
- `install.py` prints, after an install, one line: in each repository, run `init-worktracking` once to configure the skills (WS-B builds that step).
- `feat-0090`, closing `chore-0059` inside it, as `feat-0090` says.
- Health fixes for the three status drafts: descriptions under about 400 characters, a `core.md` pointer, a "Done when" on every step.
- Optional, if time allows: an opt-in destructive-git gate in `.agents/hooks/` (`reset --hard`, `clean -f`, `branch -D`, `checkout .`; never `push`); the Codex sidecar for `invocation: user` skills, after checking Codex's current format.

**Out of scope:** skill bodies other than the three status drafts; `R-003` and `R-004` stay owed.

## Risks and rollback

Touches several modules; a new gate can block unrelated work if it misfires, so each gate lands with a test proving it can fail and a test proving it passes on the current tree. Rollback is one revert.

## Acceptance criteria (mechanically verifiable)

    ZEN_CHECKS_SCOPE=full python3 scripts/run-checks.py

- [ ] A test shows each new check failing on a constructed bad input and passing on the tree.
- [ ] `python3 scripts/install.py --dry-run` prints a headline that excludes user-invoked skills.
- [ ] `docs/reviews/2026-11-24-dogfood/ws-e.md` records the `tdd` red-green evidence for each change and a row for each status draft.

## Definition of done

- [ ] Acceptance command passes locally.
- [ ] Notes for integration and the `CHANGELOG.md` line reported to the orchestrator.
- [ ] File moved to `.tasks/done/`, `status: done`.
