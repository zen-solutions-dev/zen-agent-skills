---
id: chore-0098
title: A documentation-only change runs the documentation gates and a secret scan, nothing else
type: chore
status: done
priority: P2
parent: "docs/reviews/2026-11-retro-pr-108.md R-008"
depends_on: []
spec: docs/spec/cloud-executable.md
scenarios: [S-001, S-021, S-022]
touched_files:
  - scripts/_change_scope.py
  - scripts/scan-secrets.py
  - scripts/run-checks.py
  - .github/workflows/checks.yml
  - tests/test_change_scope.py
  - tests/test_scan_secrets.py
  - tests/test_run_checks.py
  - docs/spec/cloud-executable.md
  - docs/spec/cloud-executable.conformance.md
  - docs/spec/README.md
  - AGENTS.md
created: 2026-11-24
---

## Problem

The maintainer's standing rule: "A docs-only pull request runs a docs check and a secret scan, nothing else (CI minutes cost money). Decide from the changed paths in one script that the local pre-PR check reads too, count a moved file at both its old and new path, and run the tests when the answer is missing." This repository did not work that way. [`checks.yml`](../../.github/workflows/checks.yml) ran all ten gates on six cells for every pull request, including a one-line README fix, and nothing scanned for credentials at all. The first real run of `retro` found it ([`2026-11-retro-pr-108.md`](../../docs/reviews/2026-11-retro-pr-108.md), `R-008`), and the maintainer approved the proposal on 2026-11-24.

## Scope

**In scope:** one module, [`_change_scope.py`](../../scripts/_change_scope.py), that decides from the changed paths whether a change is documentation only; [`run-checks.py`](../../scripts/run-checks.py) reading it, running only `DOCS_GATES` for a docs-only change and naming the rest as skipped; a stdlib secret scan, [`scan-secrets.py`](../../scripts/scan-secrets.py), as a gate in both scopes; `checks.yml` fetching full history so CI has a base to diff against; the amendment to `cloud-executable.md` this behaviour needs, since its `S-001` said every gate runs.

**Out of scope:** changing which checks the rulesets require (see Decisions); scanning git history for secrets already committed; high-entropy secret detection.

## Decisions

- **Rejected: skip the CI matrix with a job-level condition, behind one aggregating required check.** That is the usual pattern, but a matrix job skipped by its `if:` never expands, so the six required check names (`ubuntu-latest / python 3.11` and so on) never report and every docs-only pull request would wait forever, on `main` and, since `R-002` was applied the same day, on `developer`. Fixing that means rewriting both rulesets' required checks in the same change as the workflow, with pull requests already in flight losing their required checks. Instead every cell still runs and reports, and `run-checks.py` inside it runs only the documentation gates. The repository is public, so its standard GitHub-hosted minutes are free; what this saves is runner time and wall-clock, and the rule now holds by construction for any private fork.
- **What counts as documentation is narrower than "every `.md`".** Skills, lenses, the plugin tree, specs, task files, tests, scripts and evals carry Markdown that is a deliverable or a contract, so a change to it runs everything. So does a change to any document the test suite opens from the real repository (`TESTED_DOCUMENTS`), because a docs-only scope would skip the test that could break. A guard test scans the suite for such reads, so a new one fails until it is listed; it was shown failing with `docs/CATALOG.md` removed from the list.
- **The secret scan looks for fixed-prefix credential shapes only.** High-entropy detection finds real secrets and many false ones, and a gate that cries wolf gets switched off. The bound is printed on every run. Findings name the file, line and kind, never the matched text.
- **A test change under `A11`, approved by the maintainer as `R-008`.** `test_the_gate_set_is_present_ordered_and_complete` in `tests/test_run_checks.py` pins the gate set, and gains the secret scan.
- **A premise that turned out false: the conformance matrix's `Gate set` row named the gates.** Its enumeration was two gates stale before this task touched it (`plugin tree` and `roadmap bookkeeping` were missing). It was re-read off `gates()`.

## Risks and rollback

It changes what the acceptance command runs, which every task here depends on. The guard is the direction of every default: no git, no base, a failed diff, a push with no pull request, an empty change, or `ZEN_CHECKS_SCOPE=full` all run every gate. A wrong `docs` answer would skip the test suite on a code change, so the classifier is narrow and its test-read guard is mechanical. Reverting the one commit restores the full gate set on every change; the spec amendment reverts with it.

## Acceptance criteria (mechanically verifiable)

    python scripts/run-checks.py

- [x] A docs-only change runs `backlog`, `doc links`, `matrix citations`, `roadmap bookkeeping` and `secret scan`, and names the other six gates as skipped (`DocsScopeTests`, and the end-to-end run recorded in the pull request).
- [x] A moved file counts at both paths, proved against real git (`test_git_reports_a_rename_as_both_paths`).
- [x] Every unknown case answers `full` (`DecisionTests`).
- [x] The secret scan finds a planted token of each shape, exits 1, and does not echo it; this repository is clean.
- [x] `cloud-executable.md` amended with `S-021` and `S-022`, pending re-approval; its matrix re-derived; `check-citations.py` 0 unresolved.
- [x] Existing tests pass, and all six CI cells pass on the pull request.

## Definition of done

- [x] Acceptance command passes locally and in CI.
- [x] Conventions in AGENTS.md's conventions section followed.
- [x] `doc-sync` over the reader-facing documents: `AGENTS.md`'s acceptance-command section updated; `docs/spec/README.md`'s table and re-approval queue updated.
- [x] File moved to `.tasks/done/`, `status: done`; one dated line in `CHANGELOG.md` (proposed in the pull request body).

## Closeout (2026-11-24, by `chore-0100`)

Closed by [`chore-0100`](chore-0100-marjana-context-and-ledgers.md) on 2026-11-24, which found it done but open ([Marjana inventory, open-task triage](../../docs/reviews/2026-11-24-marjana-inventory.md)). The work merged as pull request #115 (`34345e5`); all six CI cells passed on `194cb8b`; `cloud-executable.conformance.md` already rows S-021 and S-022 as conformed, audited by this task, so the conformance step is complete. **Still owed, and not this closeout's to give:** the author's re-approval of the `S-021` and `S-022` amendment to `cloud-executable.md`.
