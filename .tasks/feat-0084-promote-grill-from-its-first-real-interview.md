---
id: feat-0084
title: Promote grill from its first real interview, ahead of the next piece of kit work
type: feat
status: open
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

**Pending.** Phase 2 of the `kit-refresh-audit` session: after `zen` routes the maintainer's next real piece of kit work, `grill` interviews them about it, one round at a time, each question with a recommended answer. The decisions record is saved beside the work it feeds. This section is filled in from that session, with what the interview exposed, and is not written ahead of it.

## What the use exposed

To be recorded from the interview.

## Refinements (apply on promotion)

To be recorded from the interview.

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
