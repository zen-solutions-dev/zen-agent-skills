---
id: feat-0102
title: Write round 2's rule and lens changes, from mechanical orchestrator merges to the smell baseline
type: feat
status: in_progress
priority: P1
parent: "Marjana round 2, Wave 1: Rules and lenses (docs/reviews/2026-11-25-marjana-r2-plan.md)"
depends_on: [feat-0101]
spec: "docs/spec/zen-config.md"
scenarios: [S-044, S-045, S-046]
external: ""
mode: "hitl"
touched_files:
  - .agents/rules/autonomy.md
  - .agents/rules/core.md
  - .agents/rules/house-style.md
  - .agents/rules/review-quality.md
  - .agents/rules/writing-for-agents.md
  - .agents/rules/deep-modules.md
  - .agents/skills/improve-architecture/SKILL.md
  - .agents/skills/improve-architecture/references/report.md
  - .quests/.scaffold.json
  - docs/reviews/2026-11-24-improve-architecture-scripts.md
  - docs/reviews/2026-11-architecture-review.md
  - AGENTS.md
  - CONTRIBUTING.md
  - docs/rationale/agents-md.md
  - docs/rationale/autonomy-citations.md
  - docs/spec/zen-config.md
  - docs/spec/zen-config.conformance.md
  - docs/reviews/2026-11-25-dogfood/rules.md
  - tests/test_validate_skills.py
  - .claude-plugin/
created: 2026-11-25
---

## Problem

The maintainer's decisions of 2026-11-25 ([decision sheet](../docs/reviews/2026-11-25-marjana-decisions.md), [round 2 plan](../docs/reviews/2026-11-25-marjana-r2-plan.md)) approve ten changes to the kit's rules and lenses that no file carries yet: A8 with B1 (mechanical-only orchestrator merges), C1 (opt-in sampled self-merge), D1 (the contribution bar gates promotion; drafts expire), D2 (shareability is the only scope filter), D4 (code-shaped sketches in PR summaries), C3 (the security axis on one-way doors), C5 (effort levels), E4's deep-module lens, E8 (a smell baseline) and R2-3 (guarded load-by-name of a draft).

## Scope

**In scope:** the rule text for each item in `.agents/rules/`, `AGENTS.md` sections 4, 5 and 7, `CONTRIBUTING.md`; the reasons in `docs/rationale/`; C1's `merge_policy` value as a dated amendment of `docs/spec/zen-config.md` with scenarios and conformance rows; moving `improve-architecture/references/vocabulary.md` to `.agents/rules/deep-modules.md` and repointing that one link; the regenerated marketplace; the one test that counts shipped supporting files.

**Out of scope:** `scripts/` and the validator's teaching of the draft-expiry and guarded-load forms (`feat-0103`); `house-review`'s use of the security axis and smells (`feat-0108`); `orchestrate`'s use of the merge rules (`feat-0107`); `CHANGELOG.md`, `ROADMAP.md`, `README.md`, `docs/CATALOG.md` (integration, `feat-0109`).

## Decisions

- **Rejected: the retro's wider option (b) for `R-201`**, which also allowed conflicts in ledger lines and planning documents. The maintainer chose "mechanical-only"; a ledger conflict needs a choice of order, which is judgement, so only generated files qualify.
- **Rejected: a validator change for C1's token.** `merge_policy` stays free text (S-027); a reader that cannot parse the token treats it as off, so a typo fails safe.
- **Seam left open:** the extension key for an expiring draft is `metadata.extended` (`extended: "YYYY-MM-DD: reason"`, quoted), named here so `feat-0103` can read it; if that child chose otherwise, integration reconciles.

## Risks and rollback

Touches more than one module and amends an approved contract. Every change is prose plus one file move; reverting the branch's commits undoes it. Items 1 and 2 widen what an unattended agent may do, so their text is a check-in gate before landing.

## Acceptance criteria (mechanically verifiable)

    ZEN_CHECKS_SCOPE=full python3 scripts/run-checks.py

- [ ] Each of the ten items has rule text in the files named above.
- [ ] `.agents/rules/deep-modules.md` exists, `vocabulary.md` does not, and `improve-architecture` links the new path.
- [ ] `zen-config.md` carries a dated amendment naming `feat-0102`, scenarios S-044 to S-046, and the conformance file rows for them.
- [ ] Dogfood record `docs/reviews/2026-11-25-dogfood/rules.md` records a real use of each changed lens.

## Definition of done

- [ ] Acceptance command passes locally.
- [ ] `doc-sync` run over the reader-facing documents (integration owns the ledgers).
- [ ] Left in `.quests/` for the orchestrator to move (decision B2).
