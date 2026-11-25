---
id: feat-0080
title: Integrate the 2026-11 overhaul, with a zen router, reader docs, profiles, and verification
type: feat
status: done
priority: P1
parent: "ROADMAP 2026-11 overhaul Phase 2"
depends_on: [feat-0076, feat-0077, feat-0078, feat-0079]
spec: ""
scenarios: []
touched_files:
  - .agents/skills/
  - .agents/hooks/skill-reachability-reminder.py
  - scripts/install.py
  - scripts/check-provenance.py
  - tests/
  - README.md
  - AGENTS.md
  - ROADMAP.md
  - docs/CATALOG.md
  - docs/GETTING-STARTED.md
  - docs/ARCHITECTURE.md
  - docs/OBSERVATORY.md
  - docs/spec/install.conformance.md
  - docs/spec/README.md
  - docs/INSTALL.md
  - docs/rationale/agents-md.md
  - scripts/build-adapters.py
  - scripts/validate-skills.py
  - .claude-plugin/
  - .tasks/chore-0070-adopt-the-published-disclosure-convention-and-decide-its-enforcement-level.md
  - .tasks/chore-0096-give-every-step-a-completion-criterion-and-settle-the-length-limit.md
  - docs/reviews/2026-11-overhaul-verification.md
  - CHANGELOG.md
created: 2026-11-23
---

## Problem

The four workstream tasks each change part of the kit and leave notes for the reader-facing
documents rather than editing them, so the documents and the install profiles describe the kit as it
was. Nothing yet tells a person or an agent which of the skills to reach for, and the skill
`review-depth` was folded into `house-review` but still exists.

**New paths this task creates**, so `touched_files` lists their existing parent instead: `.agents/skills/zen/`. Within `.agents/skills/`, this task owns only the skill directories named in its `touched_files` and those new ones.

## Scope

**In scope:**

1. **A `zen` router skill**, `invocation: user` under `metadata`: names every skill, when to reach
   for it, and the flows they form (align, plan, build, verify, ship, learn), including the light
   paths from the README's "Choosing a path". It hints and never fires. Study
   `skills/engineering/ask-matt/SKILL.md` for the shape.
2. **Delete `review-depth`**, with every test, hook entry, installer reference and document that
   names it.
3. **Recompute the install profiles** now that the link cycle is broken, and keep the profile
   comment in `install.py` true.
4. **Reader documents**: `README.md` with the quick start first; `docs/CATALOG.md`,
   `docs/GETTING-STARTED.md`, `docs/ARCHITECTURE.md` and `ROADMAP.md` updated from every workstream's
   "Notes for integration"; `AGENTS.md` updated for the invocation convention and the new lens.
5. **Verification by an agent that wrote none of it** (`A7`): `run-checks.py`, an install cycle into
   a scratch home with `--include-drafts`, and a read of every new skill against the
   `writing-for-agents.md` checklist.

**Out of scope:** promoting any draft.

## Decisions

- **Split in two.** Part A (the `zen` router and the reader documents) ran in a child session (PR #104)
  while `feat-0079` was still open, because it touched none of that task's paths; part B (deleting
  `review-depth`, the profile seeds, the Windows fixes) ran after it, because it did.
- **`spine` seeds `doc-author` explicitly.** It used to arrive only through a neighbour's link; once
  every neighbour was named in backticks it dropped out of the default, which nobody had chosen.
- **The provenance repository tests compare against an independent tally**, not a literal, so a
  fold-in no longer needs the test edited (`chore-0095`); the `review-depth` real-file guard moved to
  `house-review`, where the depth wording now lives.
- **Two Windows-only failures in `feat-0079`'s code** were fixed here: `plugin_version()` sorted with
  `Path` ordering, which is case-insensitive on Windows, and a test recorded a target under the
  unresolved 8.3 temporary home.
- **Verification failed on two narrow grounds, both fixed here**: `fix-batch` regained its pointer to
  the `test-quality` lens (F1), and the budget figures below are now reported (F2). F4 (two passages
  too close to upstream) and F7 to F14 were fixed as well. **F5 and F6 are deferred to `chore-0096`**
  rather than rushed: a completion criterion written to clear a finding is worse than none.

**Default profile description budget**, measured with `install.py --dry-run`: **10,209 characters
over 18 skills before, 6,827 over 17 after**, of which 6,080 is model-facing in Claude Code, because
`fix-batch` and `reconcile-worktrees` are now user-invoked.

## Acceptance criteria (mechanically verifiable)

    python scripts/run-checks.py

- [x] Exit 0, with the command and the verbatim tail in the pull request body.
- [x] No file in the repository outside `.tasks/done/`, `CHANGELOG.md` and `docs/reviews/` names
      `review-depth` as a current skill.
- [x] The default profile's description characters are reported before and after.

## Definition of done

- [x] Acceptance command passes, and the independent verification is recorded.
- [x] Task file moved to `.tasks/done/`; one dated line in `CHANGELOG.md`.
- [x] One pull request from `zen/overhaul-2026-11` into `developer` for the maintainer to review.
