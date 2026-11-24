---
id: feat-0094
title: Gates for the drift this round found, a truthful budget, and the owed retro checks
type: feat
status: done
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

The drift this round found was all mechanical, and no gate saw it: a roadmap naming promoted skills as drafts ([inventory `P3`](../../docs/reviews/2026-11-24-marjana-inventory.md)), workflow steps without a "Done when" (`R-005`), and a description budget headline that counts characters Claude Code never loads (`P11`). Three retro checks are owed (`R-001`, `R-005`, `R-007`), and adopters are never told to configure the skills per repository.

## Scope

**In scope** ([plan, WS-E](../../docs/reviews/2026-11-24-marjana-plan.md)), each change test-first with `tdd`:

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

- [x] A test shows each new check failing on a constructed bad input and passing on the tree.
- [x] `python3 scripts/install.py --dry-run` prints a headline that excludes user-invoked skills.
- [x] `docs/reviews/2026-11-24-dogfood/ws-e.md` records the `tdd` red-green evidence for each change and a row for each status draft.

## Definition of done

- [x] Acceptance command passes locally.
- [x] Notes for integration and the `CHANGELOG.md` line reported to the orchestrator.
- [x] File moved to `.tasks/done/`, `status: done`.

## Decisions

- **`R-005` reads `chore-0096`'s own definitions.** A step is a `###` heading inside `## Procedure`, or
  a `## Step N` or `### Step N` heading. A criterion is a line starting "Done when", outside a fence.
  A declared lens is exempt. It is a warning, one line per skill, and is specified as `S-028` in
  `validate-skills.md`. Numbered-list procedures (`sitrep`, `zen`) are invisible to it, as they were
  to `chore-0096`'s script. `sitrep`'s list items were given criteria by reading.
- **`P3` reads `## Current state` only, per sentence.** That is the one section that claims to state
  the present. A sentence using "draft" makes a draft claim about every skill it names in backticks;
  otherwise a sentence using "ship" makes a shipped claim. When any draft list exists, the lists
  together must name every draft. A digit beside "skills", "ship" or "drafts" is compared only in a
  claim sentence. The first version read whole blocks, and WS-A's true rewrite showed that was
  wrong. The check lands with `ROADMAP_STATUS_EXCEPTIONS`: eight dated keys for the base's stale
  claims, each printed as excepted and reported for deletion once it stops firing (plan principle
  9). A missing section is reported as "not judged", and a test pins that this repository's
  roadmap has one.
- **`P11` changes `profile_budgets()` itself to model-invoked totals,** so the headline and every
  per-profile figure agree. The user-invoked share is an aside on every run that places one,
  whatever the tool: Claude Code keeps those descriptions out of context, and OpenCode loads them.
  Amended `S-014`; matrix row re-audited.
- **`R-001` is a `hermetic_home` flag on `Gate`,** set only on the test suite gate. `HOME`,
  `USERPROFILE` and `XDG_CONFIG_HOME` point at a scratch directory seeded with three decoys, which is
  removed afterwards. Every other gate keeps the caller's environment, because the install gates
  already take `--home`.
- **`R-007` was written by a delegated leaf agent and reviewed here.** It found two real defects in
  `build-adapters.py`, both fixed under `systematic-debugging`: `plugin_version()` encoded paths as
  strict UTF-8, and `--marketplace --check` printed a surrogate to a strict stream. Fixing the
  first exposed the second.
- **`feat-0090` and `chore-0059` are closed here;** see their own Decisions. The `R-005` test pins a
  real-tree supporting-file count, now 16 with `quest-tracker/references/why-claims.md`. That is a
  literal other workstreams will also move.
- **Not done (optional scope):** the destructive-git gate hook, and the Codex sidecar for
  `invocation: user` skills. Neither was started. Both stay owed, recorded in Notes for integration.
- **Spec amendments, each pending the maintainer's approval:** `validate-skills.md` (`S-028`) and
  `install.md` (`S-014`), each with a dated note naming this task, and matrix rows updated in both.
  The S-022 row of `validate-skills.conformance.md` was re-derived after `feat-0090` moved its
  evidence.

## Evidence

See [`ws-e.md`](../../docs/reviews/2026-11-24-dogfood/ws-e.md) for each change's red and green runs
and each skill's dogfood row.
