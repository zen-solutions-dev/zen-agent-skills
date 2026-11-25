# Dogfood: round 2 rules and lenses (`feat-0102`)

Recorded 2026-11-25 by the Wave 1 "Rules and lenses" child of Marjana round 2, on branch
`zen/marjana-r2-rules`, cut from `zen/marjana-r2-2026-11-25` at `7496499`. One section per changed
lens: what was run, on what, and what it said. Every run below happened in this session; where a
lens change was not exercised by a run, its section says so.

## `autonomy.md` `A8`: the mechanical merge

**Run.** The new definition applied to the two merge commits the 2026-11-24 orchestrator made,
which retro proposal `R-201` is about. For each, `git merge-tree --write-tree --name-only <tip>
<child>` lists the conflicted paths, and `git diff --stat <merge-tree result> <merge commit>` shows
what the resolution changed.

| Merge | Child commit | Conflicted paths (`git merge-tree`) | Generated? | Verdict under the new rule |
|---|---|---|---|---|
| `c0579ad` (WS-C, `feat-0092`) | `9b9c311` | `.claude-plugin/plugin/.claude-plugin/plugin.json`, `ROADMAP.md`, `docs/reviews/2026-11-24-marjana-plan.md` | the first only | Not mechanical: two hand-written files conflicted |
| `6162d00` (WS-B, `feat-0091`) | `e9775bf` | the same three, plus `tests/test_validate_skills.py` | the first only | Not mechanical: three hand-written files conflicted |

The resolution diff touched exactly the conflicted paths in both cases (3 files, then 4), which is
the property round 1's verifier found; the new rule adds the second condition, that every such path
be generated and rebuilt by its command. **Both merges would have gone back to their children.** The
rule is narrower than the practice that prompted it, on purpose: a `ROADMAP.md` or a plan conflict
needs a choice of order or wording. Recorded in `docs/rationale/autonomy-citations.md`.

**Run.** The same check on this branch before its own merge of the integration tip:
`git merge-tree --write-tree --name-only HEAD origin/zen/marjana-r2-2026-11-25`, recorded under
"The merge into this branch" below.

## `autonomy.md` `A8` and `zen-config`: the self-merge opt-in

**Run.** The reader rule of S-044 and S-045 applied by hand to this repository's own
`docs/agents/zen.md`, whose `merge_policy` reads "an orchestrator merges verified work it did not
author into a zen/ integration branch; a person merges into developer and main". Its first word is
`an`, not `self-merge-sampled`, so sampled self-merge is **off** here, as intended: this round did not
opt the kit's own repository in. No repository has the value set, so no positive case has run.

## `review-quality.md`: the smell baseline and the security axis

**Run.** The baseline applied to the code half of commit `7496499` (feat-0101's fix round), read
with `git show 7496499 -- scripts/ .quests/validate.py .agents/skills/sitrep/scripts/sitrep.py`.
What it labels:

| Smell | Where | Label | Severity |
|---|---|---|---|
| Duplicated code | `both_tracker_dirs()` added in `.quests/validate.py` and, identically, in `.agents/skills/init-worktracking/templates/validate.py` | **Suppressed**: the repository keeps the two copies byte-identical on purpose (`zen-config.conformance.md`, the code surface paragraph), a standard that endorses the pattern | none |
| Shotgun surgery | One idea, "both tracker directories exist", added to `validate.py`, its template copy and `sitrep.py`'s `load_tasks()` with a second message constant `NOTICE_BOTH_TRACKERS` | Judgement call: the next wording change touches three files. Fix: none needed while the two readers have different outputs (a warning and a board notice); worth naming if a third reader appears | minor |
| Long function | `install()` in `scripts/install.py`, lines 717 to 993 on this branch, grown by the `placed_here` set and a nine-line `kept` branch | Judgement call: the change makes a 277-line function longer; the retire loop is a candidate to extract with its own tests | minor |
| Mysterious name | `placed_here` | Not labelled: the name says what the set holds | none |

No other smell in the table fires on this diff. The lens's rule "report a smell only where the
diff adds it or makes it worse" did real work: `install()`'s length predates the commit, and only
the growth is this change's finding.

**Security axis, run as the optional pass** (the commit is a two-way door: no persisted data, no
public surface renamed). Inspected: the new deletion guard in `install()` (`_rm(retired)` now runs
only when the successor was placed; `old` and `new` come from the constant `RENAMED_SKILLS`, not from
input, so no path is built from input); `both_tracker_dirs()` (reads two fixed names under the
repository root); the `sitrep.py` notice (a constant). No input crosses a trust boundary, no secret,
no command built from data. **No finding**, with that inspected list.

## `deep-modules.md`: the lens moved out of `improve-architecture`

**Run.** The deletion test and "tests stand where callers stand" applied to
`scripts/_change_scope.py` (164 lines), read on this branch.

- **Interface.** Its one caller, `scripts/run-checks.py`, uses `_change_scope.decide()` and the
  constant `DOCS`, nothing else.
- **Deletion test.** Without the module, `run-checks.py` would carry the base-branch resolution
  (`LOCAL_BASES`, `changed_paths()`), the `git diff --name-status` parsing and the documentation
  classification: about 110 lines of logic for one call. The complexity would land on the caller, so
  the module **earns its place**: deep, a two-name interface over the implementation.
- **Tests stand where callers stand.** Of the module's references in `tests/test_change_scope.py`,
  9 call `decide()` and 9 reach behind it (`classify` 3, `is_documentation` 4,
  `parse_name_status` 2). The lens counts internal seams used by the module's own tests as fine, so
  this is not a finding; it is the place the lens's two principles pull apart, and a reviewer should
  expect the question.
- **Dependency category.** git, a local process, reached through an injected `runner`: a
  **local stand-in** in the lens's terms, and the tests use the seam as intended.

## `writing-for-agents.md`: the guarded load, and effort levels

**Run.** The guarded form applied to a real shipped line. `tdd` (shipped) says at its trigger list:
"If the cause is still unknown, find it with `systematic-debugging` first, which ends on a red
command". `systematic-debugging` is a draft, so this is the mention rule 9 of the coverage map
describes. In the guarded form it would read:

> If `systematic-debugging` is installed, read and follow it now; otherwise localise the cause by
> hand until one command fails red for it, and use that command as the first test.

The sentence starts with the fixed prefix, the fallback starts with `; otherwise`, and the name is in
backticks with no link. Not applied: `tdd` belongs to a Wave 2 child (`feat-0107`), so it is handed
on as a note rather than edited here.

**Effort levels: not exercised.** This leaf dispatched no subagent, so the C5 line had no dispatch to
govern. The brief that started this session asked for medium effort for building, which matches it.

## `house-style.md`: a code-shaped sketch in a PR summary

**Run.** The summary of this branch, written as the rule allows, for the integration pull request:

```text
.agents/rules/
  autonomy.md      A8: + mechanical merge (no conflict | generated-only, regenerated)
                       + opt-in sampled self-merge, via merge_policy
  core.md          A8 line, 40 lines (budget 40)
  review-quality   + smell baseline (13 names, Fowler) + security axis on one-way doors
  writing-for-agents + guarded load-by-name + effort levels
  house-style      + code-shaped sketches in PR summaries
  deep-modules.md  <- improve-architecture/references/vocabulary.md
docs/spec/zen-config.md   + S-044..S-046 (self-merge-sampled), re-approval needed
AGENTS.md, CONTRIBUTING.md  bar gates promotion; drafts expire at 90 days; shareability
```

Eleven lines, a shallow file tree, no hunk: the rule's boundary held without effort. The one
judgement it took was keeping the arrows inside a text block rather than drawing a graph, which the
rule sends to Mermaid.

## The merge into this branch

Filled in after the merge of `origin/zen/marjana-r2-2026-11-25`, below.
