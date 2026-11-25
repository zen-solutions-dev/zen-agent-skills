---
id: feat-0108
title: Sharpen the ship-and-learn skills and draft teach, vet-skill, prototype, wayfinder and wait-what
type: feat
status: in_progress
priority: P1
parent: "Marjana round 2, Wave 2: Ship and learn (docs/reviews/2026-11-25-marjana-r2-plan.md)"
depends_on: []
spec: "docs/spec/house-review.md"
scenarios: [S-026, S-027]
external: ""
mode: "hitl"
touched_files:
  - .agents/skills/pr-describe/SKILL.md
  - .agents/skills/house-review/SKILL.md
  - .agents/skills/retro/SKILL.md
  - docs/spec/house-review.md
  - docs/spec/house-review.conformance.md
  - scripts/run-checks.py
  - tests/fixtures/supporting-files.txt
  - docs/reviews/2026-11-25-dogfood/ship.md
  - .agents/rules/review-quality.md
  - .agents/rules/deep-modules.md
  - .agents/rules/writing-for-agents.md
  - .agents/rules/house-style.md
  - docs/reviews/2026-11-24-retro-marjana.md
  - docs/reviews/2026-11-25-marjana-decisions.md
  - docs/reviews/2026-11-25-skills-coverage-map.md
created: 2026-11-25
---

## Problem

Five items from the maintainer's decisions of 2026-11-25
([`2026-11-25-marjana-decisions.md`](../docs/reviews/2026-11-25-marjana-decisions.md)) fall to the
skills that ship and learn from work:

- **E8.** [`pr-describe`](../.agents/skills/pr-describe/SKILL.md) asks for a Summary of "one to three
  sentences", and the coverage map's `pr` row found the smallest-visual summary missing. D4 allowed
  code-shaped sketches in `house-style.md` (`feat-0102`), and nothing tells the skill to use the
  glossary's terms.
- **B9.** [`house-review`](../.agents/skills/house-review/SKILL.md)'s spec axis reads the contract's
  requirements and not its guards. `R-209` in
  [`2026-11-24-retro-marjana.md`](../docs/reviews/2026-11-24-retro-marjana.md) counts three of five
  landing reviews where a change contradicted its own contract's guard.
- **C3.** `review-quality.md` gained a security axis and a smell baseline in `feat-0102`, and
  `deep-modules.md` became a lens; `house-review` loads none of them at the step that uses them. The
  approved contract [`docs/spec/house-review.md`](../docs/spec/house-review.md) has no scenario for
  either the guards or the security axis.
- **E4, E9.** [`retro`](../.agents/skills/retro/SKILL.md) reads `writing-for-agents.md` only when
  it writes a proposal, not while it classifies a no-op or misplaced instruction, and it reads no
  register of declined ideas, so it can re-propose what the maintainer already declined.
- **C2, C4, E5, `wait-what`.** No skill teaches a concept to the person, vets another author's skill
  before install, prototypes to answer a design question, maps a foggy multi-session effort, or
  re-pitches a message that did not land.

## Scope

**In scope:**

- `pr-describe`: the Summary as the smallest visual that explains the change, with a new
  `.agents/skills/pr-describe/references/visuals.md` holding the shapes; the glossary's terms in the
  body.
- `house-review`: the spec axis quotes and checks every guard of the contract (B9); the security
  axis, required on a one-way door and optional otherwise, the smell baseline, and an optional load
  of `deep-modules.md` (C3); a `## Security` output section.
- `docs/spec/house-review.md`: a dated amendment adding S-026 (guards) and S-027 (security axis),
  Proposed Surface rows, flagged for the maintainer's re-approval; `house-review.conformance.md`
  rows for both.
- `retro`: read `writing-for-agents.md` at classification (E4) and `docs/declined-ideas.md` where it
  exists (E9).
- New drafts, each with `status: draft` and `drafted: "2026-11-25"`:
  `.agents/skills/teach/SKILL.md`, `.agents/skills/vet-skill/SKILL.md`,
  `.agents/skills/prototype/SKILL.md` (with `references/logic.md` and `references/ui.md`),
  `.agents/skills/wayfinder/SKILL.md` (with `references/map-format.md`),
  `.agents/skills/wait-what/SKILL.md`.
- The five drafts in `UNLISTED_DRAFT_EXCEPTIONS` in `scripts/run-checks.py`, and each new supporting
  file in `tests/fixtures/supporting-files.txt`.
- One dogfood run per changed or new skill, recorded in `docs/reviews/2026-11-25-dogfood/ship.md`.

**Out of scope:** `zen`, `docs/CATALOG.md`, `CHANGELOG.md`, `ROADMAP.md`, `README.md`, `GLOSSARY.md`
and `.claude-plugin/` (the integration quest `feat-0109` owns them; their lines go under Notes for
integration); `review-quality.md` and `deep-modules.md` text (`feat-0102` owns the lenses); creating
`docs/declined-ideas.md` (`feat-0105`); moving this file to `done/` (B2).

## Decisions

- **`prototype` is model-invoked**, unlike the other four drafts: `grill` and `wayfinder` compose it
  by name when a question cannot be settled in talk, and a user-invoked skill is not reachable that
  way.
- **`wayfinder` keeps its map local**, as a markdown file beside the tracker, not as a GitHub issue:
  tracker publishing is `feat-0106`'s opt-in draft, and a map that needs it would depend on an
  unbuilt draft.
- **The smell baseline adds no scenario.** It is lens guidance that changes what a standards finding
  may name, not an obligation a reader could check apart from S-021; the security axis is an
  obligation (required on a one-way door) and gets S-027.

## Risks and rollback

The change touches more than one module (three shipped skills, an approved spec, a gate's exception
list). Each part reverts on its own: the drafts are new directories that install only with
`--include-drafts`; the `house-review` and spec edits revert together in one commit; the exception
entries revert with the drafts. Nothing persisted or published changes.

## Acceptance criteria (mechanically verifiable)

    ZEN_CHECKS_SCOPE=full python3 scripts/run-checks.py

- [ ] The command exits 0 after `origin/zen/marjana-r2-2026-11-25` is merged in.
- [ ] `python3 scripts/validate-skills.py --include-drafts` names each of the five drafts and reports
      0 errors.
- [ ] `docs/spec/house-review.md` carries S-026 and S-027 and a dated `feat-0108` amendment flagged
      for re-approval; `house-review.conformance.md` has a row for each.
- [ ] `docs/reviews/2026-11-25-dogfood/ship.md` has one entry per changed or new skill: what it ran
      on, the evidence, the verdict and what changed, or "not exercised" with the reason.

## Definition of done

- [ ] Acceptance command passes locally.
- [ ] Conventions in AGENTS.md's conventions section followed.
- [ ] `doc-sync` run over the reader-facing documents and its findings applied or dismissed with a
      reason.
- [ ] Left in `.quests/` for the orchestrator to move at close (B2); the CHANGELOG line is passed
      under Notes for integration.
