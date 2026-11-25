---
id: feat-0106
title: Publish the local tracker to GitHub issues one way, opt-in, and add a triage draft for the role labels
type: feat
status: in_progress
priority: P1
parent: "Marjana round 2, Wave 2: Tracker publishing (docs/reviews/2026-11-25-marjana-r2-plan.md)"
depends_on: []
spec: "docs/spec/zen-config.md"
scenarios: [S-047, S-048, S-049, S-050, S-051, S-052, S-053, S-054, S-055, S-056, S-057, S-058, S-059]
external: ""
mode: "hitl"
touched_files:
  - .agents/skills/new-quest/SKILL.md
  - .agents/skills/new-quest/references/publishing.md
  - .agents/skills/new-quest/scripts/publish.py
  - .agents/skills/triage/SKILL.md
  - docs/spec/zen-config.md
  - docs/spec/zen-config.conformance.md
  - .quests/validate.py
  - .agents/skills/init-worktracking/templates/validate.py
  - tests/test_publish.py
  - tests/fixtures/supporting-files.txt
  - scripts/run-checks.py
  - .agents/hooks/skill-reachability-reminder.py
  - docs/reviews/2026-11-25-dogfood/publish.md
  - .quests/.scaffold.json
created: 2026-11-25
---

## Problem

Coverage map rule 12 ([`2026-11-25-skills-coverage-map.md`](../docs/reviews/2026-11-25-skills-coverage-map.md), section 4) found the kit inconsistent: [`zen-config`](../docs/spec/zen-config.md) accepts `tracker: github` and five `role.*` labels, `init-worktracking` asks for them, and no skill reads a `role.*` key or publishes to a tracker. The maintainer decided R2-2 in the [round 2 plan](../docs/reviews/2026-11-25-marjana-r2-plan.md): opt-in publishing, as a draft. `.quests/` stays the source of truth and mirrors one way out, specs as issues, quests as sub-issues, `depends_on` as native blocking, and a `triage` draft consumes the role labels.

The shape of a published issue is a one-way door. It was proposed at a check-in gate before any build and approved by the maintainer on 2026-11-25, relayed by the orchestrator, with every recommended answer (Q1 to Q5). The approved text is in [`publishing.md`](../.agents/skills/new-quest/references/publishing.md).

## Scope

**In scope:**

- [`publish.py`](../.agents/skills/new-quest/scripts/publish.py), stdlib only: dry run by default, `--offline`, `--apply` through `gh api` only, idempotent by a hidden marker, one way, never deleting.
- [`publishing.md`](../.agents/skills/new-quest/references/publishing.md), the procedure and the approved shape, and step 8 of [`new-quest`](../.agents/skills/new-quest/SKILL.md), which loads it only when the setup file opts in.
- The `publish` and `publish_repo` keys and the quest field `private` in both copies of `validate.py`.
- The `zen-config` amendment (S-047 to S-059, dated, flagged for re-approval) and its conformance rows.
- The draft [`triage`](../.agents/skills/triage/SKILL.md), user-invoked, report-first.
- [`test_publish.py`](../tests/test_publish.py), against a fake `gh`; the dogfood record.

**Out of scope:** `zen`'s and `docs/CATALOG.md`'s lines for `triage` (the integration's, passed under Notes), the `private` field's line in `.quests/_TEMPLATE.md` and `_TEMPLATE.md.tmpl` (not owned), Campaign and Quest chain issues, GitLab, a live apply against a real repository, and the approved `tracker-links` contract, which stays unchanged.

## Implementation notes

Test seam, one for the plan: the script's command line, `main()`, with the `gh` runner injected. The fake answers the REST calls in memory and records them, so every assertion is on resulting issue state or on the calls made, never on internals. It misses the real API's behaviour, which only a live apply would show.

## Decisions

- **Rejected: the publisher seeding `role.*` labels from `mode`.** Two writers of one label fight; the publisher owns `zen:` labels and `triage` and people own `role.*` (Q1).
- **Rejected: a parser of `docs/agents/zen.md` inside the publisher.** It imports the repository's own `validate.py` instead, so it never accepts a file the validator rejects, and an old validator turns publishing off rather than guessing.
- **A seam left open:** the REST endpoint shapes are as GitHub documents them, unobserved here; the fake encodes that reading, so a wrong reading would pass the tests and fail a live apply.

## Risks and rollback

The rule fires: the change spans several modules and defines a persisted format, the issue shape, which adopters' repositories will hold. Rollback before any adopter publishes is reverting the commits. After, the shape can only change by amending the contract and teaching the publisher to read `v1` markers. Publishing is off by default, so a repository that does not opt in is unaffected.

## Acceptance criteria

- [x] `python3 -m unittest tests.test_publish` passes, without network.
- [x] `python3 .quests/validate.py --strict` exits 0.
- [x] The dry run over this repository's tracker, in a scratch clone that opts in, is recorded in the dogfood file.
- [ ] The maintainer re-approves the `zen-config` amendment in the round 2 pull request.

```bash
ZEN_CHECKS_SCOPE=full python3 scripts/run-checks.py
```

## Definition of done

- [ ] Acceptance criteria above are met.
- [ ] `CHANGELOG.md` updated (by the integration, `feat-0109`).
- [ ] This file moved to `.quests/done/` with `status: done` (by the orchestrator, B2).
