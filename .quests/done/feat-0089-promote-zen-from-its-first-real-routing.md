---
id: feat-0089
title: Promote zen from the first time it routed the maintainer on real work
type: feat
status: done
priority: P1
parent: "ROADMAP 2026-11 overhaul: drafts the overhaul added"
depends_on: []
spec: ""
scenarios: []
touched_files:
  - .agents/skills/zen/SKILL.md
  - .claude-plugin/plugin/
created: 2026-11-23
---

## Problem

`zen` is a draft because it has not routed anyone on real work. Its promotion condition: "it has routed a person to the right skill on real work".

## The real use

2026-11-23, the `kit-refresh-audit` session. `zen` placed the maintainer's next piece of kit work, [`feat-0051`](../feat-0051-a-paired-evaluation-harness-seeded-from-the-closed-task-corpus.md), at the plan stage: an open task with no spec and four decisions only the maintainer could make. Before recommending it read the `SKILL.md` of each skill it named (`grill`, `spec-author`, `new-task`), and it found two facts the task file did not carry: `claude plugin eval` now exists, and an unmerged October branch already held a never-run harness for the same work. It recommended `grill` on its own, then `new-task`, rather than `spec-author`. The maintainer accepted the route ("Yes, grill it"), and the interview it led to is recorded in `feat-0084`.

**Met:** it routed a person to the right skill on real work, judged by that person.

## What the use exposed

1. **The light paths had no route for what this work was.** Path 1 sends anything with decisions to `spec-author`; path 2 to a task file with no interview. `feat-0051` had decisions only the maintainer could make but no behaviour anyone else had to agree, so the honest route, `grill` then `new-task`, was off the map, and the reply had to argue for it.
2. **The decisive signal was an unmerged branch for the same work.** Step 1's "an open branch" covers it in principle, but the branch was a separate worktree, not the current one; `git worktree list` and `git branch -a` found it, not the current checkout.

## Refinements (apply on promotion)

- The light paths: a path between 1 and 2, "Are there decisions only a person can make, but no behaviour anyone else must agree? `grill`, then `new-task`." Path 1 keeps `spec-author` for behaviour that must be agreed.
- Step 1: look for other worktrees and unmerged branches that touch the same work (`git worktree list`, `git branch -a`), not only the current checkout.
- Every `*(draft)*` mark in `zen`'s flows matches the frontmatter after this wave, so each sibling promoted in the same change loses its mark here.

## Link conversion

None. `zen` names every skill in backticks by design: it is a router, and a link to each sibling would make every install that carries `zen` carry the whole kit.

## Promotion (2026-11-24, approved by the maintainer in writing)

Both refinements applied (the new light path 2, and looking beyond the current checkout in step 1); `metadata.status: draft` removed; the `*(draft)*` marks removed from the five siblings promoted in the same change, so every mark left matches a draft.

## Acceptance criteria (mechanically verifiable)

    python scripts/run-checks.py
    python .tasks/validate.py

- [x] The routing, and the maintainer's judgement of it, recorded here.
- [x] Refinements applied; draft marks match the frontmatter of every skill named.
- [x] `metadata.status: draft` removed; `docs/CATALOG.md` updated (with `kit-release-ready`); `python scripts/build-adapters.py --marketplace` rerun.

## Definition of done

- [x] Acceptance commands pass.
- [x] `doc-sync` over the reader-facing documents, findings applied or dismissed.
- [ ] Moved to `.tasks/done/`, links re-anchored; a dated `CHANGELOG.md` line proposed in the pull request body.
