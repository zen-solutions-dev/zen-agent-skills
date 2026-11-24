---
id: feat-0089
title: Promote zen from the first time it routed the maintainer on real work
type: feat
status: open
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

**Pending.** Phase 2 of the `kit-refresh-audit` session: `zen` places the maintainer's next real piece of kit work (a likely candidate is `feat-0051`, the paired evaluation harness) and names the one skill to start. "The right skill" is judged by the maintainer, not by this session. Filled in from that session, not ahead of it.

## What the use exposed

To be recorded from the session.

## Refinements (apply on promotion)

- Whatever the routing exposes.
- Whatever promotes in the same change: every `*(draft)*` mark in `zen`'s flows must match the frontmatter after this wave, so each promoted sibling loses its mark here.

## Link conversion

None. `zen` names every skill in backticks by design: it is a router, and a link to each sibling would make every install that carries `zen` carry the whole kit.

## Acceptance criteria (mechanically verifiable)

    python scripts/run-checks.py
    python .tasks/validate.py

- [ ] The routing, and the maintainer's judgement of it, recorded here.
- [ ] Refinements applied; draft marks match the frontmatter of every skill named.
- [ ] `metadata.status: draft` removed; `docs/CATALOG.md` updated (with `kit-release-ready`); `python scripts/build-adapters.py --marketplace` rerun.

## Definition of done

- [ ] Acceptance commands pass.
- [ ] `doc-sync` over the reader-facing documents, findings applied or dismissed.
- [ ] Moved to `.tasks/done/`, links re-anchored; a dated `CHANGELOG.md` line proposed in the pull request body.
