---
id: feat-0088
title: Promote improve-architecture from its first real run, over the kit's own tooling
type: feat
status: done
priority: P1
parent: "ROADMAP 2026-11 overhaul: drafts the overhaul added"
depends_on: []
spec: ""
scenarios: []
touched_files:
  - .agents/skills/improve-architecture/SKILL.md
  - .agents/skills/improve-architecture/references/report.md
  - docs/reviews/2026-11-architecture-review.md
  - .claude-plugin/plugin/
created: 2026-11-23
---

## Problem

`improve-architecture` is a draft because nobody had run it on real work. Its promotion condition: "it has produced a report a person acted on".

## The real use

Run on 2026-11-23 by the `kit-refresh-audit` session on this kit. Step 1's hot-spot command chose the tooling cluster (`validate-skills.py`, `install.py`, `build-adapters.py`, `observatory/serve.py`, `docs/spec/README.md`); step 2's walk ran in one fresh-context leaf subagent; step 3 wrote the offline HTML report to the temporary directory. The durable record is [`2026-11-architecture-review.md`](../../docs/reviews/2026-11-architecture-review.md): four candidates, the top one a latent defect reproduced in this session (the installer treats a sibling link inside a fenced example as a profile edge; the validator does not).

**Half met.** The report exists. "A person acted on" it has not happened: the maintainer has not yet picked, or rejected, a candidate. This task stays open until they do, and the pick becomes a task (step 6).

## What the use exposed

1. **The report has nowhere durable to live.** Step 3 writes to the temporary directory "so nothing lands in the repository", but the promotion rule, and any later "did anyone act on this", needs the report to survive the session. This run had to write a second, Markdown record under `docs/reviews/` by hand.
2. **Ledgers swamp the hot-spot list.** The top of step 1's output was `CHANGELOG.md` (68) and `ROADMAP.md` (23), which change by design. The step does not say to exclude ledgers, generated trees (`.claude-plugin/plugin/`, 79 file changes) or id manifests (`.tasks/.scaffold.json`, 21); the walk had to dismiss each by reasoning.
3. **The dependency categories are only in `vocabulary.md`.** Step 3 asks for "its dependency category" without naming the four. The brief written for the walk used the wrong names, and the subagent had to correct them from the reference.
4. **A walked claim needs checking before it reaches the report.** The skill dispatches a subagent for step 2 but has no step to verify what it returns. This run reproduced the top candidate's defect and re-quoted the code comments itself; one quote in the first draft was cut mid-sentence and had to be fixed.
5. **Step 4 cannot start in the same sitting** when the person is not there, and the skill says nothing about leaving the report for later.

## Refinements (apply on promotion)

- Step 3: write the HTML to the temporary directory as now, and also offer (not require) a Markdown record at the repository's review location, so a person can act on it later. Say which the person chose.
- Step 1: exclude ledgers, generated trees and manifests from the ranking, and say so in the scope line.
- Step 3: name the four dependency categories inline, or point at the table in `vocabulary.md` by name.
- Step 2: add to its "Done when" that every load-bearing claim from a subagent's walk (a defect, a quoted comment) was checked in the main session, and the report says which were.

## Link conversion

None. No shipped skill links `improve-architecture`, and it links no draft.

## Promotion (2026-11-24, approved by the maintainer in writing)

The maintainer acted on the report: they picked candidate 2, the top recommendation, and it became [`feat-0090`](../feat-0090-one-span-aware-reader-for-links-and-profile-edges.md). All four refinements applied; `metadata.status: draft` removed.

## Acceptance criteria (mechanically verifiable)

    python scripts/run-checks.py
    python .tasks/validate.py

- [x] The real run's report exists, offline HTML plus the durable record under `docs/reviews/`.
- [x] The maintainer picked a candidate (it became a task) or rejected each with a reason.
- [x] Refinements above applied.
- [x] `metadata.status: draft` removed; `zen` and `docs/CATALOG.md` updated (with `kit-release-ready`).
- [x] `python scripts/build-adapters.py --marketplace` rerun.

## Definition of done

- [x] Acceptance commands pass.
- [x] `doc-sync` over the reader-facing documents, findings applied or dismissed.
- [ ] Moved to `.tasks/done/`, links re-anchored; a dated `CHANGELOG.md` line proposed in the pull request body.
