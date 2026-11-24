---
id: feat-0085
title: Promote domain-language from the first glossary it kept through a real grilling
type: feat
status: open
priority: P1
parent: "ROADMAP 2026-11 overhaul: drafts the overhaul added"
depends_on: []
spec: ""
scenarios: []
touched_files:
  - .agents/skills/domain-language/SKILL.md
  - .agents/skills/grill/SKILL.md
  - .agents/skills/spec-author/SKILL.md
  - .claude-plugin/plugin/
created: 2026-11-23
---

## Problem

`domain-language` is a draft because it has not kept a real glossary. Its promotion condition: "it has kept a real glossary through a grilling session".

## The real use

**Pending.** Phase 2 of the `kit-refresh-audit` session: `domain-language` runs alongside the `grill` interview (`feat-0084`), settling each term as it lands and writing it to the glossary. This kit has no glossary yet, so the run also decides where one lives. Filled in from that session, not ahead of it.

## What the use exposed

To be recorded from the session.

## Refinements (apply on promotion)

To be recorded from the session.

## Link conversion (on promotion)

- `grill` to `domain-language`: `grill`'s Output section, "Each term in **Terms** is a candidate for the project glossary, which `domain-language` keeps." Make it a link only if `grill` composes it (hands its terms over as a step). If `grill` only points at it, keep the backtick name. Both are drafts today; if `grill` is promoted and `domain-language` is not, the link is illegal.
- `spec-author` to `domain-language`: step 1, "they go to `domain-language` after the spec is written (step 5)", and step 5, "`domain-language` on them as its own step". Step 5 runs it, so the link is a real composition and an install edge into `spine`; recompute profile counts.

## Acceptance criteria (mechanically verifiable)

    python scripts/run-checks.py
    python .tasks/validate.py

- [ ] The real glossary exists in this repository, written by the run, and is linked from this task.
- [ ] Refinements applied to `domain-language/SKILL.md`.
- [ ] `metadata.status: draft` removed; links converted as decided; `zen` and `docs/CATALOG.md` updated (with `kit-release-ready`); `python scripts/build-adapters.py --marketplace` rerun.

## Definition of done

- [ ] Acceptance commands pass.
- [ ] `doc-sync` over the reader-facing documents, findings applied or dismissed.
- [ ] Moved to `.tasks/done/`, links re-anchored; a dated `CHANGELOG.md` line proposed in the pull request body.
