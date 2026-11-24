---
id: chore-0095
title: Lay the groundwork for the 2026-11 overhaul before any workstream is dispatched
type: chore
status: done
priority: P1
parent: "ROADMAP 2026-11 overhaul Phase 0"
depends_on: []
touched_files:
  - docs/reviews/2026-11-overhaul-plan.md
  - .agents/rules/writing-for-agents.md
  - .agents/skills/doc-author/SKILL.md
  - .agents/skills/doc-revise/SKILL.md
  - .tasks/feat-0076-align-before-planning-with-grill-and-domain-language.md
  - .tasks/feat-0077-build-discipline-with-tdd-and-fresh-context-dispatch.md
  - .tasks/feat-0078-close-the-loop-with-retro-two-axis-review-and-merge-danger.md
  - .tasks/feat-0079-distribution-that-updates-itself-and-installs-what-you-ask.md
  - .tasks/feat-0080-integrate-the-overhaul-with-a-router-docs-and-verification.md
  - .tasks/.scaffold.json
  - tests/test_check_provenance.py
  - README.md
  - docs/INSTALL.md
  - docs/GETTING-STARTED.md
  - .github/PULL_REQUEST_TEMPLATE.md
  - .github/ISSUE_TEMPLATE/config.yml
  - CHANGELOG.md
created: 2026-11-23
---

## Problem

Four workstreams are about to rewrite skills in parallel sessions. Without a shared yardstick each
would slim and rewrite to its own taste; without reserved ids two sessions would mint the same task
id; and the reader documents still point at the repository's old owner.

## Scope

**In scope:** the [overhaul plan](../../docs/reviews/2026-11-overhaul-plan.md); the
[`writing-for-agents.md`](../../.agents/rules/writing-for-agents.md) lens with provenance, composed by
`doc-author` and `doc-revise`; the five task files `feat-0076` to `feat-0080` with their ids
reserved in `.tasks/.scaffold.json`; repository URLs moved from `hams-ollo` to `zen-solutions-dev`
in the reader documents and GitHub templates.

**Out of scope:** every skill rewrite, which belongs to the workstreams.

## Decisions

- **Rejected: a top-level `disable-model-invocation` key in skill sources.** claude.ai and the
  Skills API reject any frontmatter key outside their six (`https://code.claude.com/docs/en/skills.md`,
  checked 2026-11-23). A skill declares `invocation: user` under `metadata` instead, and the Claude
  Code distribution paths render the key (`feat-0079`).
- **Ids `feat-0073` to `feat-0075` are skipped**: they are reserved on the unmerged
  `claude/2026-10-22-oversight-tasks` branch.

## Acceptance criteria (mechanically verifiable)

    python scripts/run-checks.py

- [x] Exit 0 on the integration branch before any workstream is dispatched.
