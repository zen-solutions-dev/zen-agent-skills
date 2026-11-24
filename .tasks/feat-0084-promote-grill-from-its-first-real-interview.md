---
id: feat-0084
title: Promote grill from its first real interview, ahead of the next piece of kit work
type: feat
status: in_progress
priority: P1
parent: "ROADMAP 2026-11 overhaul: drafts the overhaul added"
depends_on: []
spec: ""
scenarios: []
touched_files:
  - .agents/skills/grill/SKILL.md
  - .agents/skills/spec-author/SKILL.md
  - docs/spec/spec-author.conformance.md
  - .claude-plugin/plugin/
created: 2026-11-23
---

## Problem

`grill` is a draft because it has not interviewed anyone ahead of real work. Its promotion condition: "it has interviewed a person ahead of a real spec or task".

## The real use

2026-11-23, the `kit-refresh-audit` session. `zen` routed the maintainer's next piece of kit work, [`feat-0051`](feat-0051-a-paired-evaluation-harness-seeded-from-the-closed-task-corpus.md) (the paired evaluation harness), to `grill` and then `new-task`. `grill` interviewed the maintainer in three rounds and a close (Q1 to Q18), with two facts sent to fresh-context leaf subagents (the `claude plugin eval` CLI and sign-in state; the October eval-slice branch). The frontier emptied, the maintainer confirmed a one-sentence restatement, and the record is [`2026-11-feat-0051-decisions.md`](../docs/reviews/2026-11-feat-0051-decisions.md): 15 decisions, 5 terms, 5 facts, 2 items still open with owners.

**Met:** it interviewed a person ahead of a real task.

## What the use exposed

1. **Facts were the decisive half.** The lookups found that no CLI here is signed in, that `claude plugin eval` reads evals from below the plugin, and that the October harness measures retired code. None of these was in the task file; each reshaped a recommendation. "Never ask the person a fact" earned its place.
2. **A fact returned after a decision had settled, and constrained it.** Q3 (evals at the repository root) was settled before the lookup showed that the runner expects them below the plugin. The skill has no instruction for this; the session reconciled it inside Q4's recommendation and said so, but it could as easily have been absorbed silently.
3. **Every round was accepted wholesale.** 17 of 17 recommendations went through as "yes to all". The yes-accepts form makes that cheap, which is its point, but it also means the one question in a round that is hard to reverse (Q7, the baseline) gets the same single click as a flag choice. The closing restatement was the only check that the whole was understood.
4. **Running beside `domain-language` duplicated the Terms section.** Terms were settled as questions in the rounds (Q10, Q17) and written to the glossary as they landed, so the record's Terms section could only point at the glossary.
5. **The rule "nothing more is asked until they come back" held, and cost nothing:** the lookups returned during round 1, and round 2 waited for the answers as written.

## Refinements (apply on promotion)

- Step 4: when a returned lookup bears on a decision already settled, put that to the person in the next round as its own question, rather than reconciling it inside another recommendation.
- Step 3: mark, in the round, the question that is hardest to reverse, so a wholesale "yes" is a choice made knowingly.
- Output: when `domain-language` keeps the glossary in the same session, the record's **Terms** section names the glossary entries instead of restating them.

## Link conversion (on promotion)

- `spec-author` to `grill`: delete the paragraph in `spec-author` step 1 that begins "Fallback while `grill` is a draft (delete this paragraph when it is promoted and linked)", turn the first `grill` mention into a relative link, and remove the sentence saying `grill` "is named" rather than linked.
- Then re-derive rows `S-008` and `S-009` of [`spec-author.conformance.md`](../docs/spec/spec-author.conformance.md): both cite the fallback's wording as evidence ("the fallback 'ask in rounds over the frontier ...'" and "Procedure step 1 fallback / 'look facts up yourself ...'"), so with the fallback gone their evidence must move to the composed `grill` steps 2 and 3, and the note that "the inline sentence is what carries the behavior in an install that lacks it" no longer holds. The `Interview round` surface row cites "same clauses as S-008" and moves with it. Run `python scripts/check-citations.py` after.
- `spec-author` is in the `spine` profile, so the link pulls `grill` into `spine`: recompute profile counts and report them.

## Acceptance criteria (mechanically verifiable)

    python scripts/run-checks.py
    python .tasks/validate.py

- [ ] The real interview's decisions record exists and is linked from this task.
- [ ] Refinements applied to `grill/SKILL.md`.
- [ ] `metadata.status: draft` removed; the fallback paragraph deleted; the link made; `S-008`, `S-009` and the surface row re-derived; `check-citations.py` passes.
- [ ] `zen` and `docs/CATALOG.md` updated (with `kit-release-ready`); `python scripts/build-adapters.py --marketplace` rerun.

## Definition of done

- [ ] Acceptance commands pass.
- [ ] `doc-sync` over the reader-facing documents, findings applied or dismissed.
- [ ] Moved to `.tasks/done/`, links re-anchored; a dated `CHANGELOG.md` line proposed in the pull request body.
