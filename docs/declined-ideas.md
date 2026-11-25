# Declined ideas

The register of ideas this kit chose not to adopt: skills, techniques and rules studied and turned down, each with the date, the reason, and where it was decided. Its readers are `zen`, before it recommends a new skill, and `retro` (from `feat-0108`), before it proposes one. Its purpose is that a settled argument is not reopened by someone who never saw it, and that a decline whose reason has gone stale is noticed.

Created on 2026-11-25 by `feat-0105` (decision E9 in the [Marjana decisions](reviews/2026-11-25-marjana-decisions.md)), seeded from three sources: the declines in the [2026-11 overhaul plan](reviews/2026-11-overhaul-plan.md) ("What we deliberately do not adopt"), the "Declined, with reasons" list of the [2026-11-24 sources delta](reviews/2026-11-24-sources-delta.md), and the Declined and "Do not adopt" verdicts of the [2026-11-25 skills coverage map](reviews/2026-11-25-skills-coverage-map.md).

## How to use it

- **Before proposing a new skill or rule**, search this file for it. When it is here, the proposal names the entry and gives a reason the entry did not weigh, or it is not made.
- **Add an entry** when an idea is studied and turned down: the idea, the date, the reason in one or two sentences, and where it was decided, with a link. A decline nobody wrote down is decided again by the next session to meet the idea.
- **Supersede, never rewrite.** When a later decision reopens or weakens an entry, add a dated line under **State** and leave the original reason as it was.
- **Where it was decided** says who decided. An entry a research report recommended and no person put a separate decision on says so; that is weaker than a maintainer's decision and may be put to one.

## Skills

### `triage` as a skill

- **Declined:** 2026-11-24. Built for inbound issues from outside contributors, and rarely used when the work comes from one's own planning; this kit's tracker is local. The role vocabulary went into `zen-config` instead.
- **Where:** recommended in [`sources-delta.md`](reviews/2026-11-24-sources-delta.md) (line 214), a report-only research file the approved Marjana plan of 2026-11-24 built on.
- **State:** **reopened** 2026-11-25. The coverage map found the configured `role.*` labels had no consumer (its rule 12), and the maintainer chose opt-in tracker publishing with a `triage` draft as their consumer (decision R2-2 in the [round 2 plan](reviews/2026-11-25-marjana-r2-plan.md); built by `feat-0106`).

### `wayfinder` now

- **Declined:** 2026-11-24. The right tool for an effort too big for one session, but large, and the contribution bar asks for real use first; keep it on the roadmap until an effort needs it. Its fog and out-of-scope sections were adopted into `grill`.
- **Where:** recommended in `sources-delta.md` (line 216).
- **State:** **reopened** 2026-11-25. The promised roadmap entry was never written (coverage map, section 6), and the maintainer answered E5 "Do it": a `wayfinder` draft and the roadmap entry (built by `feat-0108`).

### `software-factory` as a glossary skill

- **Declined:** 2026-11-24. Premature for a solo maintainer. Its brakes (start slow, throttle, cap loops) and its five questions per task were to go into `orchestrate`'s notes instead.
- **Where:** recommended in `sources-delta.md` (line 217).
- **State:** the decline of the skill holds. The coverage map found the brakes not carried through (2026-11-25); `feat-0107` owns them.

### `claude-handoff` (`claude --bg`)

- **Declined:** 2026-11-24. Single-harness; at most a labelled optional line in `agent-handoff`.
- **Where:** recommended in `sources-delta.md` (line 220).
- **State:** the decline of the skill holds. The optional line was missing on 2026-11-25 (coverage map); `feat-0107` owns it.

### `teach`

- **Declined:** 2026-11-24, as personal productivity outside the kit's engineering scope.
- **Where:** recommended in `sources-delta.md` (line 221).
- **State:** **reopened** 2026-11-25. The coverage map found the cited reason did not fit (its rule 2), the maintainer made shareability the only scope filter (D2), and adopted `teach` as a draft (C2; built by `feat-0108`).

### `loop-me`, `writing-beats`, `writing-fragments`, `writing-shape`

- **Declined:** 2026-11-24. Personal productivity: one person's content workflow, outside the kit's scope.
- **Where:** recommended in `sources-delta.md` (line 221); re-read on 2026-11-25 by the coverage map, which found the reason holds for these four.
- **State:** holds. Under the scope rule of 2026-11-25 (D2, `AGENTS.md` section 7) the reason reads as "hyper-specific personal pipeline", which still excludes them.

### `migrate-to-shoehorn`

- **Declined:** 2026-11-25. A single TypeScript library its author maintains; too specific for the kit.
- **Where:** recommended ("Do not adopt") in the [coverage map](reviews/2026-11-25-skills-coverage-map.md), Misc table. No person decided it separately.
- **State:** holds.

### `scaffold-exercises`

- **Declined:** 2026-11-25. Tied to one course's linter and layout.
- **Where:** recommended ("Do not adopt") in the coverage map, Misc table. No person decided it separately.
- **State:** holds.

### Wrapper skills that only say "call the other skill"

- **Declined:** 2026-11-23. The composed skill is often not loaded; composition by relative link is sturdier, because the install profile pulls the dependency in. Covers `grill-with-docs`, `grill-me` and `implement` as named entries.
- **Where:** the [2026-11 overhaul plan](reviews/2026-11-overhaul-plan.md), "What we deliberately do not adopt", approved by the maintainer on 2026-11-23.
- **State:** **weakened** 2026-11-25. The coverage map (rule 4) found its reason answered by "composition must load" and user invocation; it recommends a load instruction inside the composing skill over a wrapper, which `feat-0105` did for `grill` and `domain-language` and, for `implement`, as the one-quest flow line in `zen`.

### Author-named skills

- **Declined:** 2026-11-23. `ask-matt` and `setup-matt-pocock-skills` keep their author's name; this kit's router is `zen`.
- **Where:** the overhaul plan, approved 2026-11-23.
- **State:** holds.

## Techniques and rules

### Durable agent briefs without file paths

- **Declined:** 2026-11-24. Upstream briefs sit for weeks, so paths go stale; this kit's briefs run soon and `touched_files` is a contract the validator checks.
- **Where:** recommended in `sources-delta.md` (line 215).
- **State:** holds (coverage map, 2026-11-25).

### Automating `retro` after every session

- **Declined:** 2026-11-24. An automated retro chases false positives; sampling is the middle ground and was adopted.
- **Where:** recommended in `sources-delta.md` (line 218).
- **State:** holds.

### A bash wizard template

- **Declined:** 2026-11-24. The idea is adopted; bash is not, because the kit targets Windows as well (`AGENTS.md` section 6).
- **Where:** recommended in `sources-delta.md` (line 219).
- **State:** holds. The standard-library Python port landed in `doc-author` on 2026-11-24, and its reusable library in `doc-author/scripts/wizard.py` on 2026-11-25 (`feat-0105`).

### A preset of `permissions.deny` rules to trim the payload

- **Declined:** 2026-11-24. Harness-specific, and the tools it removes are the ones orchestration uses; measuring the payload is documented instead.
- **Where:** recommended in `sources-delta.md` (line 222).
- **State:** holds.

### Blocking `git push` in the guardrail hook

- **Declined:** 2026-11-24. This kit's flow pushes branches by design; `A8` and branch protection cover merging.
- **Where:** recommended in `sources-delta.md` (line 223).
- **State:** holds. The opt-in destructive-git gate of 2026-11-25 (`feat-0103`) excludes `push`.

### "Skills take no per-user configuration"

- **Declined in part:** 2026-11-24. Kept in spirit: the setup file records facts about a repository, never behaviour preferences.
- **Where:** recommended in `sources-delta.md` (line 224).
- **State:** holds.

### Hand-written per-skill docs pages with no check

- **Declined:** 2026-11-23. Upstream's pages drifted from their skills; this kit's catalog stays small and link-checked.
- **Where:** the overhaul plan, approved 2026-11-23.
- **State:** holds, mostly. The coverage map (rule 11) suggests one checkable "It's working if" line per catalog row instead.

### Leaving recursion to the harness

- **Declined:** 2026-11-23. A review fanned out to more than fifty agents upstream; this kit tells every dispatched agent it is a leaf.
- **Where:** the overhaul plan, approved 2026-11-23.
- **State:** holds.

### Blind repository-wide substitutions

- **Declined:** 2026-11-23. An upstream em-dash sweep broke frontmatter in six skills; every rewrite here runs the validator.
- **Where:** the overhaul plan, approved 2026-11-23.
- **State:** holds.

### "No evals"

- **Declined:** 2026-11-23. The eval slice is kept as the route to measuring whether a skill helps.
- **Where:** the overhaul plan, approved 2026-11-23.
- **State:** holds (`feat-0051` open on 2026-11-25).

### Questions in plain prose instead of a structured question tool

- **Declined:** 2026-11-25. Upstream rejects pickers because they push toward canned answers; the maintainer finds questions in prose overwhelming to scroll and keeps the structured question tool in `grill`.
- **Where:** the maintainer's answer T3 in the [Marjana decisions](reviews/2026-11-25-marjana-decisions.md), round 2 Phase 0 answers, settling the coverage map's rule 16 for this maintainer.
- **State:** holds. The coverage map's suggestion of one dogfood comparison is not run.
