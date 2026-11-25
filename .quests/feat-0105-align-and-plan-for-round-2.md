---
id: feat-0105
title: Build the round 2 align and plan items in grill, spec-author, new-quest, zen, domain-language and doc-author
type: feat
status: in_progress
priority: P1
parent: "Marjana round 2, Wave 2: Align and plan (docs/reviews/2026-11-25-marjana-r2-plan.md)"
depends_on: []
spec: ""
scenarios: []
external: ""
mode: "afk"
touched_files:
  - .agents/skills/grill/SKILL.md
  - .agents/skills/domain-language/SKILL.md
  - .agents/skills/spec-author/SKILL.md
  - .agents/skills/new-quest/SKILL.md
  - .agents/skills/zen/SKILL.md
  - .agents/skills/doc-author/SKILL.md
  - .agents/rules/deep-modules.md
  - docs/spec/spec-author.md
  - docs/spec/spec-author.conformance.md
  - docs/reviews/2026-11-24-sources-delta.md
  - docs/reviews/2026-11-25-skills-coverage-map.md
  - docs/reviews/2026-11-25-podcast-extraction.md
  - docs/reviews/2026-11-overhaul-plan.md
  - tests/fixtures/supporting-files.txt
  - .quests/.scaffold.json
created: 2026-11-25
---

## Problem

The maintainer answered E1, E4 and E9 "Do it" ([decisions record](../docs/reviews/2026-11-25-marjana-decisions.md)), and the [round 2 plan](../docs/reviews/2026-11-25-marjana-r2-plan.md) gives them to this workstream with three items from the [coverage map](../docs/reviews/2026-11-25-skills-coverage-map.md) (rows `grill-with-docs`, `to-spec`, `to-tickets`, `implement`, `wizard`, rule 14) and the [podcast notes](../docs/reviews/2026-11-25-podcast-extraction.md) (section 5, items 3, 4, 20, 28, 29):

1. E4 in [`grill`](../.agents/skills/grill/SKILL.md): settled terms go to the glossary as they land, through `domain-language`; exploration finishes before the first question; a rename is offered when a term collides; a dictated brain dump is accepted whole; one question on module shape, in the terms of [`deep-modules.md`](../.agents/rules/deep-modules.md).
2. [`spec-author`](../.agents/skills/spec-author/SKILL.md): a synthesise-only mode for a decisions record already confirmed in the conversation. Amends the approved [`spec-author.md`](../docs/spec/spec-author.md).
3. [`new-quest`](../.agents/skills/new-quest/SKILL.md): prefactor first, and E1, one test-seams list per plan.
4. [`zen`](../.agents/skills/zen/SKILL.md): a one-quest flow line, and the bug chain `systematic-debugging` then `tdd`.
5. E9: a declined-ideas register that `zen` reads before recommending a new skill.
6. E9: a standard-library wizard library in [`doc-author`](../.agents/skills/doc-author/SKILL.md).

## Scope

**In scope:** the six items above. Files created: `docs/declined-ideas.md`, `.agents/skills/doc-author/scripts/wizard.py`, `tests/test_doc_author_wizard.py`, `docs/reviews/2026-11-25-dogfood/align.md`, and this quest file.

**Out of scope:** `GLOSSARY.md` (a dogfood that writes terms writes a scratch copy); tracker publishing in `new-quest/references/` (`feat-0106`); `retro` reading the register (`feat-0108`); `docs/spec/zen-config*.md`; `CHANGELOG.md`, `ROADMAP.md`, `README.md`, `docs/CATALOG.md` (the integrator's); a model trigger in `doc-author`'s description for human-only steps (named by the coverage map's `wizard` row, not by this brief).

## Implementation notes

**Prefactor:** none. Every item adds a step or a file to a skill whose existing steps already carry it; nothing would make the change easier first.

**Test seams** (the one record for this plan; `feat-0105` is a single quest, so it carries the list itself):

- `python scripts/run-checks.py` with `ZEN_CHECKS_SCOPE=full`, the highest seam: catches a broken link, an unguarded load of a draft, a skill missing from `zen`, an unlisted supporting file, and a failing unit test; misses whether a skill's prose changes an agent's behaviour, which only a dogfood run shows.
- `tests/test_doc_author_wizard.py`, the wizard library at its public interface (`Wizard.run` and the helpers a stage calls): catches a re-run duplicating an env key, an echoed secret, a declined confirmation that still acts, a dry walk that writes; misses terminal behaviour on a real TTY and Windows file modes.

## Decisions

- **A seam left open deliberately:** `depends_on` is `[]` although the items use `feat-0102`'s `deep-modules.md` lens and `feat-0103`'s guarded-load validator. Both landed on the integration branch at `d906b20`; their quest files stay outside `.quests/done/` until the orchestrator closes the round (B2), so naming them would block this quest on bookkeeping.
- **A rejected alternative:** a user-invoked `implement` wrapper for the single-quest flow. The coverage map calls the `zen` line the cheaper first step, and wrapper skills are a declined idea.
- **A premise that turned out false:** `spec-author.conformance.md` quoted "Fallback while `grill` is a draft" as evidence; `feat-0084` deleted that phrase. The row is re-derived and the Constraint's fallback half flagged for the maintainer.

## Risks and rollback

Touches six skills and an approved contract. Each item is its own edit to one skill, so any one reverts alone; the spec amendment is pending the maintainer's re-approval and changes nothing downstream until then.

## Acceptance criteria (mechanically verifiable)

    ZEN_CHECKS_SCOPE=full python3 scripts/run-checks.py

- [ ] Every changed skill was dogfooded or recorded as not exercised, with the reason, in [the dogfood record](../docs/reviews/2026-11-25-dogfood/align.md).
- [ ] `docs/spec/spec-author.md` carries a dated amendment naming `feat-0105`, flagged for re-approval, and its conformance matrix covers `S-012`.

## Definition of done

- [ ] Acceptance command passes.
- [ ] Left in `.quests/` for the orchestrator to close (B2).
