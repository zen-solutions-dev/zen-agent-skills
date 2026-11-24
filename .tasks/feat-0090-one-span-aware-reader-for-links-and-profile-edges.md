---
id: feat-0090
title: One span-aware reader for skill links and profile edges, shared by the validator, installer and adapter builder
type: feat
status: open
priority: P2
parent: "docs/reviews/2026-11-architecture-review.md candidate 2"
depends_on: []
spec: ""
scenarios: []
touched_files:
  - scripts/_skillmeta.py
  - scripts/validate-skills.py
  - scripts/install.py
  - scripts/build-adapters.py
  - tests/test_validate_skills.py
  - tests/test_install.py
  - tests/test_build_adapters.py
created: 2026-11-24
---

## Problem

Three scripts decide what counts as a link in a `SKILL.md`, and they disagree. [`validate-skills.py`](../scripts/validate-skills.py) skips links inside code spans and fenced blocks (`code_span_ranges`, `fenced_block_ranges`, `_link_targets`). [`install.py`](../scripts/install.py) (`SIBLING_REF_RE`, `sibling_refs`) and [`build-adapters.py`](../scripts/build-adapters.py) (`SIBLING_LINK_RE`, `draft_refusals`) scan the raw text. So a sibling link shown as an example inside a fenced block becomes an install edge, and a draft refusal, that the validator never checks. AGENTS.md calls that edge load-bearing: it decides which skills an install places.

Reproduced on 2026-11-23: a scratch skill whose only link is `[grill](../grill/SKILL.md)` inside a fenced block gives `install.sibling_refs: {'grill'}` and `validator _link_targets: []`. No shipped skill triggers it today.

Found by the first real run of `improve-architecture` ([`2026-11-architecture-review.md`](../docs/reviews/2026-11-architecture-review.md), candidate 2, its top recommendation), and chosen by the maintainer on 2026-11-24 as the candidate to act on.

## Scope

**In scope:** one span-aware reader, `link_targets(text)` and `sibling_edges(text)`, in the shared module the three scripts already import ([`_skillmeta.py`](../scripts/_skillmeta.py), or a sibling module beside it), used by all three. `install.py` keeps one `closure` instead of the copy inside `resolve_profile`. The span helpers' duplicate copies in `build-adapters.py` go.

**Out of scope:**

- `.tasks/validate.py` and its `init-worktracking` template copy: they ship to adopters and stay copied, held together by the existing AST test.
- Unifying frontmatter parsing (the review's candidate 1). It can land in the same shared module afterwards, as its own task.
- Any change to which skills a profile places today: the dry-run placements must be identical before and after.

## Implementation notes

Write the fenced-example case first, as a failing test at `sibling_edges`, then move the callers. This retires `chore-0059`'s proposed identity test for copies 3 and 4 of the link helpers; close or amend that task in the same change and say which.

## Risks and rollback

It touches more than one module, and the installer's profile resolution is the edge every install depends on. The guard is that `python scripts/install.py --dry-run` for `core`, `spine` and `all` places exactly the same skills before and after; record both. Reverting the one commit restores the three copies.

## Acceptance criteria (mechanically verifiable)

    python scripts/run-checks.py

- [ ] A test at `sibling_edges` shows a fenced example link is not an edge, failing before the change and passing after.
- [ ] `install.py`, `build-adapters.py` and `validate-skills.py` all call the shared reader; `grep -n "SIBLING_REF_RE\|SIBLING_LINK_RE\|def code_span_ranges\|def fenced_block_ranges" scripts/*.py` finds each definition once.
- [ ] Profile placements for `core`, `spine` and `all` are identical before and after.
- [ ] Existing tests pass.

## Definition of done

- [ ] Acceptance command passes locally.
- [ ] Conventions in AGENTS.md's conventions section followed.
- [ ] `doc-sync` run over the reader-facing documents and its findings applied or dismissed with a reason.
- [ ] File moved to `.tasks/done/`, `status: done`; one dated line added to `CHANGELOG.md` referencing this task id.
