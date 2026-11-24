---
id: feat-0085
title: Promote domain-language from the first glossary it kept through a real grilling
type: feat
status: in_progress
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

2026-11-23, the `kit-refresh-audit` session, alongside the `grill` interview on `feat-0051` (`feat-0084`). Step 1 found no glossary and no ADR directory. The first terms settled in the interview (Q10: **Grader**, **Discriminating**) created [`GLOSSARY.md`](../GLOSSARY.md) at the repository root; Q17 added **Case**, **Arm** and **Baseline**. Each term was put to the maintainer with its _Avoid_ list and written as it landed. Step 4 judged the baseline decision (Q7) to pass all three tests and offered it as a record (Q18); the maintainer placed it in the rewritten `feat-0051`'s Decisions. One glossary-versus-text mismatch was reported, not edited: `feat-0051` says "non-discriminating assertions", which the glossary lists under _Avoid_. The code has no evaluation code yet, so the grep of `scripts/` and `tests/` for "grader" and "assertion" in this sense found none.

**Met:** it kept a real glossary through a grilling session.

## What the use exposed

1. **Step 1 does not recognise this repository's decision-record convention.** It lists `docs/adr/`, `docs/decisions/` and `adr/`, but this kit, like any repository scaffolded by `init-worktracking`, records decisions in each task's Decisions section and in `docs/rationale/`. Step 4 then nearly created a `docs/adr/` the repository does not use; Q18 had to ask.
2. **The mismatch was in a planning document, not the code.** Step 2's "check the code" found nothing, because the conflicting word lived in a task file. Task files and specs are where a term is used before any code exists.
3. **The glossary's location was consented to by silence.** It was offered in passing in round 1 ("unless you'd rather it lived somewhere else") and never asked as a question. Creating a new root file deserves a question.
4. **Nothing points at the new glossary.** The reading protocol in `AGENTS.md` does not name it, so the next session will not read it unless it happens to look. A glossary nobody loads does not do its job.

## Refinements (apply on promotion)

- Step 1: recognise a task-file Decisions section and a rationale directory as a decision-record convention, and use it in step 4 when that is what the repository does.
- Step 2: grep task files and specs as well as code, and report a mismatch there the same way.
- Step 3: when no glossary exists, ask where it should live before creating it.
- Step 5: when a glossary is created, offer a one-line pointer to it from the agent-instructions file (an offer, since that file is the person's), and report it. For this kit: a proposed line in `AGENTS.md`'s reading protocol, which is not this task's file to edit.

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
