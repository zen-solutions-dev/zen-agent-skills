# Marjana inventory: context bloat, drift and dead weight (2026-11-24)

**Status:** report only. Nothing here is applied. It is the map the 2026-11-24 "Marjana" clean-up workstreams execute against; each proposal is approved and landed as its own change.

**Measured at:** `zen/marjana-2026-11-24` = `origin/main` `220282a` (2026-11-24). Every figure below came from a command run on that tree on that date, named beside it. Token figures are bytes divided by four, an approximation for English prose and Markdown.

**Coverage (`A6`).** Covered: always-loaded context here and in an adopter's default install, `AGENTS.md` section by section, `CHANGELOG.md` and `ROADMAP.md` and the gates that read them, the reader documents for stale claims, the 20 open tasks, the `R-001` to `R-008` retro proposals, all 29 skills, `docs/reviews/` and `docs/spec/`, and the four non-`main` remote branches. Not covered: `.tasks/done/` file by file (230 files, 2.2 MB, never loaded), `tests/` quality, `scripts/observatory/`, the GitHub ruleset (`R-002` needs repository settings this session cannot read), and real-use evidence outside this repository. Two parts were delegated to research agents and spot-checked, not re-derived line by line: the stale-claims sweep and the open-task triage (`A7`: verdicts produced by delegated agents in this session, reviewed by this session).

## Short version

- **This repository loads about 28.2 KB (about 7,000 tokens) into every session**, almost all of it `AGENTS.md` (27,822 bytes) through the `@AGENTS.md` import in `CLAUDE.md` (338 bytes). The committed `SessionStart` hook adds 834 bytes only when no kit skill is reachable. `.agents/rules/core.md` is not loaded here at all: nothing places it under `.claude/rules/` in this checkout.
- **About 60 percent of `AGENTS.md` is rationale, history, or a restatement of another file.** A rule-only `AGENTS.md` of about 10 to 11 KB keeps every rule an agent needs on every task. Saving: about 17 KB, about 4,300 tokens, every session.
- **An adopter's default install (`spine`) loads `core.md` (2,542 bytes) plus a 7,200-character skill listing** (7,947 reported, of which 747 belongs to the two user-invoked skills Claude Code hides). Two scaffolds, `project-bootstrap` (648 characters) and `init-worktracking` (588), are model-invoked against `AGENTS.md`'s own rule that a scaffold is `invocation: user`; flipping them takes 1,236 characters out of every adopter session.
- **The ledgers are 406 KB (`CHANGELOG.md`) and 106 KB (`ROADMAP.md`).** Neither is always loaded, but every agent that opens one to append a line pays for it. 362 KB of the changelog is the July and August task log. 21.8 KB of the roadmap is three finished hardening passes that name no open task. Per-month archives under `docs/history/` keep every gate green, because the `doc links` gate already globs `docs/**/*.md` and the `roadmap bookkeeping` gate reads only `ROADMAP.md`.
- **`ROADMAP.md`'s "Current state" is false today**: it says 10 drafts and 19 shipped (`ROADMAP.md:15`); the tree has 4 drafts and 25 shipped. Its overhaul subsections ("Drafts the overhaul added", "Links to convert on promotion", "Release readiness") describe work PR #109 and PR #113 finished. The bookkeeping gate cannot see a count.
- **Open tasks (20, not 21)**: 2 done but not closed (`chore-0098`, `chore-0077`), 1 obsolete (`chore-0059`), 4 do now, 13 later. `CHANGELOG.md` has no line for PR #113's six promotions or PR #110's `chore-0097`.
- **Retro proposals: 2 of 8 landed** (`R-006`, `R-008`). `R-001`, `R-003`, `R-004`, `R-005` and `R-007` are owed and unfiled; `R-002` is a GitHub setting this session cannot read.
- **Skill health**: five bodies exceed the 250-line checklist bound, five descriptions exceed 400 characters (four of them drafts), seven workflow skills have steps with no "Done when" line, and five skills never point at `core.md`. Only four skills have a dedicated test module.
- **Branches**: `zen/overhaul-ws1-align` is fully in `main` and safe to delete. `claude/2026-10-22-oversight-tasks` holds three never-merged task files (`feat-0073` to `feat-0075`) and `zen/eval-slice-71f3d5` holds a 94-file eval harness `feat-0051` says to mine first; both need a decision, not a delete. `developer` is the live integration branch and stays.
- **Baseline**: `python3 scripts/run-checks.py` passes 11 of 11 gates in 58.6 s wall time on this container.

### Measured numbers

| What | Loaded | Bytes | About tokens | Source |
|---|---|---|---|---|
| `CLAUDE.md` | every session, here | 338 | 85 | `wc -c` |
| `AGENTS.md` (imported) | every session, here | 27,822 | 6,960 | `wc -c` |
| `skill-reachability-reminder` output | session start, here, only when no kit skill is reachable | 834 | 210 | hook run on a `startup` payload, `wc -c` |
| `.agents/rules/core.md` | every session, adopter (placed in `~/.claude/rules/`) | 2,542 | 640 | `wc -c` |
| Skill listing, `spine` (default) | every session, adopter | 7,200 of 7,947 reported | 1,800 | `install.py --dry-run`; user-invoked share 747 from the same run |
| Skill listing, `core` | every session, adopter | 1,610 | 400 | same |
| Skill listing, `all` | every session, adopter | 7,941 of 9,527 reported | 1,985 | same, recomputed without the five user-invoked skills |
| `house-style.md`, `autonomy.md`, `review-quality.md`, `writing-for-agents.md` | on demand (`paths` frontmatter) | 2,436 / 9,398 / 16,500 / 8,375 | | `wc -c`, `head -3` |
| Skill bodies | on demand | 43 to 319 lines | | `wc -l` |
| `CHANGELOG.md` | on demand, but read by every closeout | 406,161 | 101,500 | `wc -c` |
| `ROADMAP.md` | on demand, but read by every closeout | 105,591 | 26,400 | `wc -c` |
| `run-checks.py` | | 11 of 11 gates, 58.6 s | | `time python3 scripts/run-checks.py` |

## Ranked proposals

Ranked by value over cost: always-loaded bytes first, then truth, then hygiene. "Door" says how reversible the action is.

### P1. Cut `AGENTS.md` to the rules, move the reasons out

- **What.** `AGENTS.md` is 27,822 bytes, 205 lines, imported into every session. Measured per section with `awk` over the headings:

  | Section | Bytes | Keep as rule | Move | Where it goes |
  |---|---|---|---|---|
  | Header and intro (lines 1 to 7) | about 980 | the "canonical file" sentence, the three-file map | the `.cursor`/Copilot pointer sentence | `README.md` already covers it |
  | 0. Reading protocol | 596 | all | | |
  | 1. What this repository is | 821 | one sentence | "Not every script distributes a skill" (line 23) | `docs/rationale/agents-md.md` already has "Why some scripts are not distribution scripts" |
  | 2. Layout | 4,305 | one short row per path | the `.agents/rules/` row (line 30, 1,067 bytes, restates `core.md` and each lens), the `scripts/` row (line 33, 943 bytes), the `docs/spec/` file-kind list (line 35) | `docs/ARCHITECTURE.md` ("Core components") and `docs/spec/README.md` |
  | 3. Altitude and lifecycle | 2,297 | the altitude table, the closeout checklist as a numbered list, "a spec is earned" in one line | line 58 (732 bytes, why the steps exist) and the deferral paragraph's argument | rationale already has the closeout section |
  | 4. Skill structure, invocation, two shapes, universal lens | 4,666 | the frontmatter rule, `invocation: user`, draft naming in backticks, the two shapes in two lines, "reference every universal lens" in one line | the history pointers (lines 88, 102), the explanation of why `review-quality` is topical (lines 96 to 98), the conventions-by-target paragraph (lines 104 to 113) | `writing-for-agents.md` already carries the invocation split; the target-conventions paragraph belongs in `house-style.md`, which every skill reads |
  | 5. Portability contract | 2,415 | the five bullets, one sentence each | the `house-review` incident and the `chore-0040` incident (lines 120, 121) | rationale |
  | 6. Conventions, preamble | 880 | house style pointer, Python stdlib, cross-platform | line 127, a word-for-word restatement of section 5's last bullet | delete |
  | Acceptance command | 2,563 | the command, exit codes, "docs-only runs docs gates", "necessary but not sufficient" in one line each | the gate enumeration (already in `run-checks.py`'s own summary), the `checks.yml` sentence, the "construct the empty input" paragraph's justification | rationale ("What the gates cannot see") |
  | The one committed hook | 2,140 | "`.claude/settings.json` registers one reminder hook; adding another, or a gate, is a new decision" | the rest, including the interpreter-fallback argument | already in `.claude/settings.json`'s 5 KB `_comment` and rationale ("Why the one hook registration is committed", "Why the hook interpreter is a fallback") |
  | No co-author trailer | 1,319 | the rule, the Copilot Autofix clause | the ruleset deadlock explanation | rationale ("Why commits carry no co-author trailer") |
  | Provenance | 4,441 | a three-line pointer: "material adapted from elsewhere carries a provenance block; the convention is in `CONTRIBUTING.md`" | the field table, placement rules, four rules, backfill note, why it stays out of CI | `CONTRIBUTING.md` (new "Provenance" section), whose reader is the person or agent folding material in; an agent whose task touches provenance is pointed there |
  | 7. Contribution bar | 397 | all | | |

- **Target outline** (about 10 to 11 KB, about 2,700 tokens):

  ```text
  # AGENTS.md                                     ~500  canonical, what this repo is, where rationale lives
  ## 0. Reading protocol                          ~600  unchanged
  ## 1. Layout                                   ~1,500  one short row per path, no history
  ## 2. Work lifecycle                           ~1,300  altitude table, closeout checklist, spec-is-earned
  ## 3. Skill structure                          ~1,800  frontmatter, invocation, drafts, two shapes, universal lenses
  ## 4. Portability contract                     ~1,300  five one-sentence bullets
  ## 5. Conventions                              ~2,600  house style, Python, cross-platform, acceptance command,
                                                         the one committed hook, no trailer, provenance pointer
  ## 6. Contribution bar                           ~400
  ```

- **Evidence.** Section sizes from `awk '/^##+ /{...} {b+=length($0)+1}' AGENTS.md`; destinations exist today (`grep -n '^#' docs/rationale/agents-md.md` lists all eleven rationale sections; `CONTRIBUTING.md` has no provenance section, `grep -n -i provenance CONTRIBUTING.md` finds none).
- **Action.** Rewrite `AGENTS.md` to the outline; append moved text to its named destination in the same change, so no rule or reason is lost; run `doc-sync` over `README.md`, `CONTRIBUTING.md` and `docs/ARCHITECTURE.md`, which cite section names. Also mirror the trimmed shape into `init-worktracking/templates/AGENTS.md.tmpl` only if that template has grown the same way (not measured here).
- **Door.** Two-way (a revert restores it).
- **Saved from always-loaded context.** About 17 KB, about 4,300 tokens, every session in this repository.

### P2. Make the two scaffolds user-invoked

- **What.** `AGENTS.md:71` says a scaffold declares `invocation: user`. `project-bootstrap` and `init-worktracking` are scaffolds and are model-invoked, so their descriptions (648 and 588 characters, the two longest shipped) sit in every adopter's skill listing, in all three profiles. `project-bootstrap`'s description is also imperative ("Bootstrap a new or bare repository"), not third person, against the `writing-for-agents.md` checklist.
- **Evidence.** `python3 scripts/install.py --dry-run --profile core` reports `core=1610`; both skills are in it. Neither `SKILL.md` has `invocation:` in its frontmatter.
- **Action.** Add `metadata.invocation: user` to both, cut each description to the person-facing one-liner the lens asks for, regenerate `.claude-plugin/` (the `plugin tree` gate requires it). Check first that no skill relies on reaching them unprompted: `project-bootstrap` hands off to `init-worktracking` by name, which still works for a user-invoked skill started by the person.
- **Door.** Two-way.
- **Saved.** 1,236 characters (about 310 tokens) from every adopter session in every profile; `core` drops from 1,610 to 374.

### P3. Correct `ROADMAP.md`'s "Current state" and retire the finished overhaul subsections

- **What.** `ROADMAP.md:15` says "29 skills, of which 19 ship and 10 are drafts" and lists six skills PR #113 promoted. `ROADMAP.md:13` says the release is "ahead of" PR 109, which merged (`ba58c54`). The "Drafts the overhaul added" table (lines 36 to 47) and "Links to convert on promotion" (lines 49 to 56) describe finished work: `spec-author` now links `../grill/SKILL.md` (`spec-author/SKILL.md:19`) and `../domain-language/SKILL.md` (`:114`), `test-author` links `../tdd/SKILL.md` (`:17`), `fix-batch` links it (`:131`). "Release readiness" ends "Still to record here once they merge" (line 67) over PRs that merged (#110, #113).
- **Why the gate missed it.** `check_roadmap()` in `scripts/run-checks.py` matches open-state phrases next to closed task ids. A count and a draft list name no task id, so it is outside the class the gate's own report says it covers ("evidence about bookkeeping and about nothing else").
- **Action.** Rewrite "Current state" from the tree, with its date; replace the overhaul section with three lines and a link to the overhaul plan; move the rest to the roadmap archive (P5). Consider deriving the counts instead of writing them: `install.py --dry-run` already prints the draft list, so "Current state" can point at that command rather than restate it. A cheap check is also possible: fail when `ROADMAP.md` names a skill as a draft that is not `status: draft`, the same shape as the existing gate.
- **Door.** Two-way.

### P4. Archive the changelog task log by month

- **What.** `CHANGELOG.md` is 406,161 bytes: 52 lines of release notes, then 391 `- [x] (YYYY-MM-DD)` task-log entries averaging 1.6 KB (the longest 5,083 bytes, against `AGENTS.md:54`'s "add one dated line"). By month: 2026-07 90 entries and 111 KB, 2026-08 130 and 251 KB, 2026-09 12 and 16 KB, 2026-10 3 and 5 KB, 2026-11 17 and 16 KB (`grep -E "^- \[x\] \(2026-MM" CHANGELOG.md | wc -c`).
- **Scheme.**
  - `CHANGELOG.md` keeps its title, intro, `## Releases`, `## Task log` with the current and previous month, and one new line under the intro: "Older entries: `docs/history/`", as a link once the directory exists. Target under 40 KB.
  - `docs/history/changelog-2026-07.md`, `-2026-08.md`, and so on, one per month, each with the same `## Task log` heading so `reconcile-worktrees`' union handling and `pr-describe`'s format inspection see a familiar shape. The "Seeded provenance" block moves with July.
  - `docs/history/README.md` indexes the files.
  - Every relative link in a moved entry is re-anchored two levels deeper (`.tasks/done/x.md` becomes `../../.tasks/done/x.md`), the same re-anchoring `AGENTS.md:54` already demands of a moved task file.
- **Gates.** `doc links` globs `*.md`, `.github/**/*.md` and `docs/**/*.md` (`scripts/run-checks.py`, the `doc links` gate), so archive files are checked and a missed re-anchor fails loudly. `backlog` (`.tasks/validate.py --strict`) does not read `CHANGELOG.md` (`grep -n CHANGELOG .tasks/validate.py` is empty). `roadmap bookkeeping` reads only `ROADMAP.md`. The tests that write a `CHANGELOG.md` (`tests/test_tasks_validate.py:632` onward) use a temporary fixture root, not the real file. No script or hook parses the live file (`grep -rln CHANGELOG scripts .agents/hooks` is empty).
- **Also.** Restate the closeout rule as "one dated line, at most about 300 characters, linking the task file for detail", since the task file already carries the narrative. Two templates seed the format into adopters (`init-worktracking/templates/CHANGELOG.md.tmpl`, `tasks-README.md.tmpl`); they need no change for the archive, only if the length rule is exported.
- **Door.** Two-way for the split (a concatenation restores it); the `git log` of the moved lines is preserved by `git log --follow` only per file, so `git blame` on an archived entry starts at the move. Acceptable for a ledger.
- **Saved.** Not always-loaded. Every closeout that opens `CHANGELOG.md` reads about 40 KB instead of 406 KB.

### P5. Archive the finished parts of `ROADMAP.md`

- **What.** By section: Forward plan 73.8 KB (Epic B 28.3 KB, Epic E 26.4 KB, Epic F 6.2 KB, Epic A 5.8 KB, Epic C 5.3 KB), the three hardening passes 21.8 KB, the overhaul 5.9 KB. Of the 20 open task ids, only eight are named in the roadmap, at lines 47, 65, 103 to 178; none in the hardening sections (lines 296 to 515), which the per-id `grep -n` confirms.
- **Scheme.** `docs/history/roadmap-2026.md` takes the three hardening sections verbatim, the overhaul section, and every forward-plan item that is struck through or marked shipped. `ROADMAP.md` keeps: Current state (P3), the open and held items of each epic, the declined lists, and Out of scope, plus a "Shipped and archived sections" list naming each moved heading, because 60-odd task `parent:` fields cite sections by heading text (`grep -h '^parent:'`, for example "ROADMAP Kit coherence hardening (2026-08-18 review pass)"), and a reader following one must still find it. Target 25 to 35 KB.
- **Gates.** `roadmap bookkeeping` reads only `ROADMAP.md`; moving closed ids out lowers its "task ids named" count and cannot add a finding. The archive is under `docs/**`, so `doc links` checks its links after re-anchoring. Interacts with open `feat-0050` (a controlled vocabulary for `parent`): do this first, or let `feat-0050` define the anchor form and do this after; not both at once.
- **Door.** Two-way.

### P6. Close the done-but-open tasks and refresh the false ones

See the open-task triage table. Closing is the `AGENTS.md:54` closeout (move to `.tasks/done/`, re-anchor, one changelog line). **Door:** two-way.

### P7. Correct the stale reader-facing claims

See the stale-claims table. The recurring shape is a count or a status written as prose beside the thing it counts, which `house-style.md` already forbids for table rows. **Door:** two-way.

### P8. File the owed retro proposals

`docs/reviews/2026-11-retro-pr-108.md` lists eight proposals, each waiting on the maintainer's approval by id.

| Id | Proposal | State | Evidence |
|---|---|---|---|
| `R-001` | hermetic home for the test gate | **owed** | `grep -n -E "USERPROFILE\|XDG_CONFIG_HOME\|decoy" scripts/run-checks.py` is empty. PR #110 (`cbb70e5`, `chore-0097`) fixed the two hook test modules themselves, which the proposal calls a separate fix; the guard for the next test file is not built |
| `R-002` | required checks bind `developer` too | **unverified** | a ruleset setting on GitHub; not readable from this session |
| `R-003` | check "Composed by" claims; derive the digest consumers | **owed** | `validate-skills.py` has no "Composed by" check; `tests/test_spec_digest.py:222` still has the literal `CONSUMERS` tuple |
| `R-004` | audit double-quoted phrases in matrix evidence | **owed** | `check-citations.py`'s quoted-phrase row dates from `a7fab15` (2026-08-28), before the proposal |
| `R-005` | "Done when" as a validator warning | **owed** | `grep -n -i "done when" scripts/validate-skills.py` is empty; the per-skill table below still finds seven workflow skills with steps and no criterion |
| `R-006` | re-read a restated step | **landed** | `.agents/rules/writing-for-agents.md:122`; recorded in `feat-0087` |
| `R-007` | undecodable-name test module | **owed** | no `tests/test_undecodable_names.py` |
| `R-008` | docs-only change runs docs gates and a secret scan | **landed** | `scripts/_change_scope.py`, `DOCS_GATES` in `run-checks.py`, PR #115; its task `chore-0098` is still open (P6) |

**Action.** Ask the maintainer to approve or dismiss `R-001`, `R-003`, `R-004`, `R-005` and `R-007` by id, and file each approved one with `new-task`. `R-005` overlaps P10. **Door:** two-way.

### P9. Settle the three stale branches

`git rev-list --left-right --count origin/main...origin/<b>` and `git cherry origin/main origin/<b>`:

| Branch | Only on the branch | Last commit | What it holds | Safe to delete |
|---|---|---|---|---|
| `developer` | 0 commits (main is 6 ahead) | 2026-11-23 | nothing `main` lacks | **keep**: it is the integration branch every pull request targets (`R-002`'s evidence) |
| `zen/overhaul-ws1-align` | 1 commit, `eedb615`, patch-equivalent in `main` (`git cherry` prints `-`) | 2026-11-23 | spec-author's grill fallback marker, already merged | **yes** |
| `claude/2026-10-22-oversight-tasks` | 2 commits, not in `main` (`+`) | 2026-10-22 | three task files never merged, `feat-0073` (list the tasks an agent can start now), `feat-0074` (a portfolio index above the season trackers), `feat-0075` (close out and lint session hand-over notes), plus a `.scaffold.json` counter bump and a two-line `ROADMAP.md` edit. `main` skips those ids (`feat-0072`, then `feat-0076`) | **not yet**: decide whether the three tasks are still wanted. If yes, cherry-pick them; if no, record the decline in `ROADMAP.md`. Then delete |
| `zen/eval-slice-71f3d5` | 1 commit, not in `main` | 2026-10-21 | a 94-file, 2,944-line pre-registered eval harness under `evals/rank9/` | **not yet**: `docs/reviews/2026-11-feat-0051-decisions.md` decision 5 says "mined, then closed", keeping its grader-isolation rule, decision rules and live-skill fixtures. `feat-0051` is open and nothing is mined (`evals/` does not exist on `main`). Tag it (`git tag archive/eval-slice-71f3d5 origin/zen/eval-slice-71f3d5`) so the branch can go without losing the fixtures |

**Door.** One-way for each delete (a deleted remote branch survives only in clones and reflogs). A tag first makes it two-way in practice.

### P10. Bring the skills under the `writing-for-agents.md` checklist

From the per-skill table: steps without "Done when" in `init-worktracking` (8 steps, 0 criteria), `project-bootstrap` (5, 0), `test-author` (5, 0), `reconcile-worktrees` (8, 2), `verifier-agent` (5, 4), and the drafts `agent-observatory` and `quest-tracker`; bodies over 250 lines in `doc-sync` (277), `fix-batch` (272), `house-review` (268), `quest-tracker` (283), `systematic-debugging` (319), each needing either a move to `references/` or the checklist's one-line justification; no pointer to `core.md` in `agent-observatory`, `init-worktracking`, `project-bootstrap`, `quest-tracker`, `sitrep`. The two oldest skill directories, `project-bootstrap` (last changed 2026-08-29) and `init-worktracking` (2026-10-20), are the only shipped skills the overhaul did not touch, and they carry most of the smells. **Door:** two-way.

### P11. Make the description budget report what Claude Code loads

`install.py`'s `profile_budgets()` sums every description, user-invoked included; the same run then prints the user-invoked share on a second line. The headline `Description budget: 7947` overstates what a session carries by 747 characters (`spine`) and 1,586 (`all`). Report the model-invoked total as the headline and the user-invoked total as the aside. Specified behaviour (`S-015` in `docs/spec/install.md` is cited beside the budget code), so this goes through the spec. **Door:** two-way.

### P12. Index `docs/reviews/` and `docs/spec/`; do not move them

- `docs/reviews/` holds nine reports (17 KB to 56 KB). All are dated, and all but the newest few are historical: the 2026-08-29 pre-publication review, the 2026-08-31 security review, the 2026-09-01 optimization review, the 2026-10 kit-refresh audit and the 2026-11 overhaul plan and verification are records of finished passes. Task files and changelog lines link into them, so moving them breaks links for no context saving: none is ever loaded unasked.
- `docs/spec/` holds 38 files (the largest conformance matrices run 42 KB to 59 KB). They are live contracts with live matrices that `matrix citations` audits (13 matrix files). `cloud-executable.s001-s016.verification.md` beside `cloud-executable.verification.md` is the one candidate for a merge or a "superseded" note.
- **Action.** Add a `docs/reviews/README.md` table: report, date, status (historical, live, or superseded by), and what it produced. **Door:** two-way.

### P13. Smaller items

- `CLAUDE.md`'s explanatory paragraph (about 280 bytes) is loaded every session to explain the import line under it; the same explanation is in `AGENTS.md:117`. Keep `@AGENTS.md` and one line. **Saved:** about 250 bytes. Two-way.
- `docs/CATALOG.md` Tier B still plans `adr` (line 83), while the shipped `domain-language` already writes an ADR when a decision is hard to reverse (line 43). Strike or merge it. Two-way.
- Personal-tier candidates: `quest-tracker` runs a shared claude.ai tracker page, which needs one harness's artifact runtime (`AGENTS.md:119`'s no-lock-in rule asks for it to be gated), and `agent-observatory` reads a local store of the maintainer's own sessions. Both are drafts and placed only on request, so they cost adopters nothing today; at promotion time, decide whether they are Tier A skills or the maintainer's own tooling that belongs beside `scripts/observatory/` and outside the shared kit. Two-way.

## Per-skill health

Columns: lines (`wc -l SKILL.md`), description characters (as `install.py` counts them), status and invocation (frontmatter `metadata`), dedicated tests (a `tests/test_<skill>*.py` module; "named in" counts test files that mention the skill at all, mostly `test_validate_skills.py` and `test_build_adapters.py` fixtures), spec (files under `docs/spec/` named for the skill), last changed (`git log -1 --format=%cs -- <dir>`), real-use evidence (a promotion or dogfood task in `.tasks/done/`, else the number of closed task files that name the skill), and smells against the `writing-for-agents.md` checklist. Step counts are headings matching `Step` or a number; "Done when" counts lines starting with it.

| Skill | Lines | Desc | Status | Invocation | Tests | Spec | Last changed | Real-use evidence | Smells |
|---|---|---|---|---|---|---|---|---|---|
| `agent-handoff` | 160 | 379 | shipped | model | named in 4 | none | 2026-11-23 | 12 closed tasks name it | none found |
| `agent-observatory` | 149 | 599 | draft | model | `test_observatory*.py` (4 modules, for the scripts) | contract, conformance, readiness | 2026-10-20 | maintainer-only store | desc over 400; 4 steps, 0 "Done when"; no `core.md` pointer; arguably maintainer tooling (P13) |
| `doc-author` | 52 | 390 | shipped | model | named in 6 | none | 2026-11-23 | 18 | none found |
| `doc-revise` | 43 | 369 | shipped | model | named in 4 | none | 2026-11-23 | 22 | none found |
| `doc-sync` | 277 | 375 | shipped | model | named in 13 | contract, conformance | 2026-11-23 | run at every closeout (`AGENTS.md:54`); 183 closed tasks name it | body over 250 with no one-line justification |
| `domain-language` | 129 | 356 | shipped | model | named in 3 | none | 2026-11-23 | promoted by `feat-0085`; `GLOSSARY.md` | none found |
| `fix-batch` | 272 | 380 | shipped | user | named in 17 | none | 2026-11-23 | 51 | body over 250; desc 380 though user-invoked (the lens asks for a one-line summary) |
| `grill` | 169 | 369 | shipped | model | named in 4 | none | 2026-11-23 | promoted by `feat-0084` | none found |
| `house-review` | 268 | 395 | shipped | model | named in 11 | contract, conformance, verification | 2026-11-23 | 34 | body over 250 |
| `human-handoff` | 57 | 364 | shipped | model | named in 2 | none | 2026-11-23 | 13 | none found |
| `improve-architecture` | 187 | 305 | shipped | user | named in 1 | none | 2026-11-23 | promoted by `feat-0088` | desc 305 though user-invoked |
| `init-worktracking` | 185 | 588 | shipped | model | named in 11 | none | 2026-10-20 | dogfooded by this repository | scaffold not user-invoked (P2); desc over 400; 8 steps, 0 "Done when"; no `core.md` pointer |
| `new-task` | 187 | 363 | shipped | model | named in 13 | none | 2026-11-24 | 45 | none found |
| `pr-describe` | 226 | 377 | shipped | model | named in 8 | none | 2026-11-23 | 37 | none found |
| `project-bootstrap` | 113 | 648 | shipped | model | named in 7 | none | 2026-08-29 | 23 | scaffold not user-invoked (P2); desc over 400 and imperative; 5 steps, 0 "Done when"; no `core.md` pointer |
| `quest-tracker` | 283 | 606 | draft | model | `test_quest_tracker.py` | none | 2026-10-21 | 2 | desc over 400; body over 250; 5 steps, 0 "Done when"; no `core.md` pointer; one harness's runtime (P13) |
| `reconcile-worktrees` | 168 | 369 | shipped | user | named in 3 | none | 2026-11-23 | 22 | 8 steps, 2 "Done when"; desc 369 though user-invoked |
| `retro` | 146 | 307 | shipped | user | named in 3 | none | 2026-11-23 | promoted by `feat-0087`; produced `R-001` to `R-008` | desc 307 though user-invoked |
| `sitrep` | 113 | 569 | draft | model | `test_sitrep_*.py` (4 modules) | contract, conformance, readiness | 2026-10-20 | 6 | desc over 400; no `core.md` pointer |
| `spec-author` | 171 | 375 | shipped | model | named in 5 | contract, conformance | 2026-11-23 | 34 | none found |
| `spec-conformance` | 72 | 369 | shipped | model | named in 12 | none (it writes the matrices) | 2026-11-23 | 42; 13 matrices in `docs/spec/` | none found |
| `spec-plan-readiness` | 121 | 391 | shipped | model | named in 9 | none | 2026-11-23 | 25; three readiness reports | none found |
| `spec-quality` | 103 | 362 | shipped | model | named in 6 | none | 2026-11-23 | 29 | none found |
| `systematic-debugging` | 319 | 363 | draft | model | `test_systematic_debugging.py` | contract, conformance, verification | 2026-11-23 | dogfooded in `feat-0062`; second run owed (`feat-0063`) | body over 250, the longest in the kit |
| `tdd` | 190 | 398 | shipped | model | named in 3 | none | 2026-11-23 | promoted by `feat-0086` | none found |
| `test-author` | 159 | 377 | shipped | model | named in 6 | contract, conformance | 2026-11-23 | 29 | 5 steps, 0 "Done when" |
| `test-quality` | 168 | 369 | shipped | model | named in 32 | none | 2026-11-23 | 29 | none found (a lens: headings are not steps) |
| `verifier-agent` | 214 | 347 | shipped | model | named in 6 | contract, conformance | 2026-11-23 | 41 | 5 steps, 4 "Done when" |
| `zen` | 163 | 230 | shipped | user | named in 37 (mostly the word, not the skill) | none | 2026-11-23 | promoted by `feat-0089` | none found |

Read the "named in" column with care: it is not coverage. Twenty-five skills have no dedicated test module, which is expected for prose skills whose mechanical layer `validate-skills.py` lints; the four with modules are the ones that ship scripts.

## Stale and false claims

Swept by a delegated agent over `README.md`, `docs/*.md`, `ROADMAP.md`, `.agents/hooks/README.md`, `.tasks/README.md`, `docs/spec/README.md` and `.claude-plugin/`; five rows re-checked by this session (`ROADMAP.md:15`, `ROADMAP.md:49` to `56`, `README.md:29`, `docs/INSTALL.md:45`, `.tasks/README.md`'s missing `conformance:` key against `spec-conformance-gate.py:35`). Severity: **false** (wrong now), **stale** (true when written, read as current), **incomplete** (a hand-kept list missing a member).

| Location | Claim | Evidence | Severity |
|---|---|---|---|
| `ROADMAP.md:13` | "Measured 2026-11-23 at `developer` `0305d5c`, ahead of the release that pull request 109 carries to `main`", in a section that "says only what is true now" (`:21`) | PR 109 merged as `ba58c54`; #110 to #116 followed; `main` is `220282a` | stale |
| `ROADMAP.md:15` | "29 skills, of which 19 ship and 10 are drafts", naming `domain-language`, `grill`, `improve-architecture`, `retro`, `tdd`, `zen` | 4 skills carry `status: draft`; PR #113 (`aa7e7e7`) promoted the six; `feat-0084` to `feat-0089` are in `.tasks/done/` | false |
| `ROADMAP.md:16` | "The shipped spine" lists 19 skills | omits the six promoted skills; the plugin tree holds 25 | stale |
| `ROADMAP.md:25` | "Integration branch `zen/overhaul-2026-11`." | not in `git branch -r`; merged by #98 (`6e48026`) | stale |
| `ROADMAP.md:31`, `:32` | budget "fell from 10,209 characters to 6,438"; "the default profile's budget is 6,827" | `install.py --dry-run` prints `spine=7947` | stale |
| `ROADMAP.md:34` to `47` | "Drafts the overhaul added, and what promotes each"; "Every one of these is a draft" | all six promoted | false |
| `ROADMAP.md:49` to `56` | "Links to convert on promotion" | `spec-author/SKILL.md:19` links `grill`, `:114` links `domain-language`; `test-author/SKILL.md:17` and `fix-batch/SKILL.md:131` link `tdd`. Still backticks: `grill/SKILL.md:134` to `domain-language`, and `house-review` and `retro` to each other (conditional item) | false (done) |
| `ROADMAP.md:63` to `67` | "Before pull request 109 carries the overhaul to `main` ... Still to record here once they merge: the sibling test-isolation fix and the draft-promotion reports" | #109, #110 (`chore-0097`) and #113 merged; none recorded | false |
| `ROADMAP.md:134`, `docs/CATALOG.md:83` | `adr` planned as a future skill | shipped `domain-language` writes ADRs (`CATALOG.md:43`, `domain-language/references/adr-format.md`) | stale |
| `README.md:29` | "To try them (see what's new)" for drafts | the linked section now describes promoted skills; only `systematic-debugging` among the four drafts is named | stale |
| `README.md:177` | the `scripts/` row lists the distribution tooling | omits `check-citations.py` and `scan-secrets.py` | incomplete |
| `README.md:180`, `docs/ARCHITECTURE.md:85` | `docs/spec/` report kinds | omit `.runbook.md` (`docs/spec/cloud-executable.runbook.md`) | incomplete |
| `docs/GETTING-STARTED.md:315` to `328` | "ask `zen`", "`retro` for ..." as everyday steps after "install the skills" | the default `spine` profile places neither (`install.py --dry-run` list); they need `--profile all` or the plugin, as the same guide says at `:216` | stale |
| `docs/INSTALL.md:45` | pin with `#v1.0.0` | the only tag is `v0.1.0` (`git tag`) | false (example does not resolve) |
| `docs/OBSERVATORY.md:342` | `discover_skills()` finds "the set this kit ships" | that set includes the four drafts, which do not ship | stale |
| `.tasks/README.md:33` to `48` | the frontmatter field table | omits `conformance:`, which `spec-conformance-gate.py:35` honours and `docs/INSTALL.md:209` tells users to set | incomplete |
| `CHANGELOG.md` | the ledger of finished work | no line for `feat-0084` to `feat-0089` (PR #113) or `chore-0097` (PR #110), though both task sets are in `.tasks/done/` | false (by omission) |

Clean, by the same sweep: `.claude-plugin/` (25 skills, no drafts), `CATALOG.md`'s status and invocation columns, `INSTALL.md`'s profile table (3, 20, 25), `docs/spec/README.md`'s scenario counts, `.agents/hooks/README.md`, `docs/ISSUE-LINKING.md`.

**Pattern.** PR #113 updated every reader document except `ROADMAP.md`; sentences that wait for an event ("before PR 109", "once they merge", "when promoted") outlive it; figures are re-measured and the prose quoting them is not. Every rotted status word is one `install.py` already reads mechanically from `metadata.status`, which is why P3 proposes a check rather than another pass.

## Open-task triage

Twenty open tasks (the brief's 21 counts one too many: `ls .tasks/*.md` holds 22 files, two of them `README.md` and `_TEMPLATE.md`). Triaged by a delegated agent; `chore-0077`'s supersession (`draft_refusals`, `build-adapters.py:578`) and `chore-0059`'s retirement (`feat-0090` line 42) were re-checked here. Every `depends_on` is in `.tasks/done/` except `feat-0071`'s, which is `feat-0070`.

| Task | Title | Verdict | Evidence | Next step |
|---|---|---|---|---|
| `chore-0098` | a docs-only change runs the docs gates and a secret scan | **done, not closed** | PR #115 (`34345e5`): `DOCS_GATES` at `run-checks.py:89`, `tests/test_change_scope.py`, `DocsScopeTests` at `tests/test_run_checks.py:590`; six CI cells green on `194cb8b`; file still `status: in_progress`, no changelog line | close it; its spec amendment (`S-021`, `S-022` in `cloud-executable.md`) still needs the author's re-approval |
| `chore-0077` | the draft axis stops at one of two distribution paths | **done, not closed** (superseded) | `feat-0079` built it: `draft_refusals` at `build-adapters.py:578`, `S-021` in `build-adapters.md`; `build-adapters.py --dry-run` withholds the four drafts | close as delivered by `feat-0079` |
| `chore-0059` | the third and fourth copies of the link helpers are unguarded | **obsolete** | `feat-0090` retires its identity test (`.tasks/feat-0090-*.md:42`); the four copies are still identical today | close inside the `feat-0090` change, as `feat-0090` says |
| `feat-0090` | one span-aware reader for links and profile edges | **do now** | duplicates live at `install.py:161`, `build-adapters.py:181`, `:219`, `:250`, `validate-skills.py:246`, `:277` | one to two hours; guard is identical `install.py --dry-run` output for every profile before and after |
| `chore-0074` | `new-task` does not put the documents a change falsifies in scope | **do now** | no such rule in `new-task/SKILL.md`; its premise "500 lines at the ceiling" is false (187 lines) | fix the premise, add the rule beside `touched_files` |
| `chore-0086` | the live watcher retries a persistent failure with no diagnosis | **do now** | `scripts/observatory/serve.py:2248` to `2253` still ends in `except Exception: pass` | maintainer tooling, two files |
| `feat-0052` | turn on telemetry capture before the bounds that need it | **do now** (low) | nothing names `CLAUDE_CODE_ENABLE_TELEMETRY`; `.gitignore` has no entry; criterion 4 already met by `chore-0076` | one document and one ignore line |
| `chore-0073` | four bookkeeping corrections the wave 16 agents left | **later** | items 1 and 4 done (`.tasks/README.md:38`, `house-style.md`); 2 and 3 remain (`tests/test_validate_skills.py:667`, `:707`; `validate-skills.conformance.md:140`) | strike items 1 and 4, then do the retag and re-derivation in one pass |
| `chore-0075` | the spec README carries derived arithmetic nothing recomputes | **later** | unblocked; a new checker; counts correct today only because they were fixed by hand on 2026-11-23; premise says "eleven specs", now 13 | build it in `check-citations.py` |
| `chore-0070` | adopt the published disclosure convention and decide its enforcement | **later** (human decision) | `MAX_BODY_LINES = 500` at `validate-skills.py:66` warns only; three references over 100 lines | the maintainer picks the enforcement level; touches `AGENTS.md`, so sequence after P1 |
| `chore-0080` | the diagnosis record has nowhere to put a defect found on the way | **later** (human decision) | spec has no `incidental` field; its motivating `serve.py` defect was fixed by `bug-0052` | put the field-or-sentence choice to the maintainer |
| `chore-0083` | no Codex session has ever exercised the Codex wiring | **later** (outside event) | needs real Codex sessions | wait |
| `chore-0084` | the hook registration path form must survive `cmd.exe` | **later** | `.claude/settings.json` uses the relative form, which works | low urgency |
| `feat-0042` | repeat and futility classification | **later** | dependencies done; leans on the draft `systematic-debugging`; "has not bitten yet" | hold until `feat-0063` |
| `feat-0050` | a controlled vocabulary and a consumer for `parent` | **later**, redesign | 59 distinct `parent` values (title says 41); newer tasks point `parent` at `docs/reviews/`, which its ROADMAP-only check would reject | rethink alongside P5's archive anchors |
| `feat-0051` | a paired evaluation harness from the closed-task corpus | **later** (large) | no `evals/`; `_change_scope.py:63` reserves it; decisions in `docs/reviews/2026-11-feat-0051-decisions.md`; title says "twenty skills" | first sub-task mines `zen/eval-slice-71f3d5` (P9) |
| `feat-0063` | a second independent run of `systematic-debugging` | **later** (outside event) | needs a session that did not write the skill, on a defect it did not choose | wait for a real defect |
| `feat-0065` | a scheduled sensor for the drift checks | **later** | only `checks.yml` under `.github/workflows/`; acceptance needs a scheduled run to have happened | later |
| `feat-0070` | render the board as text, page and document | **later** (large) | `sitrep.py` has no `--html` or `--since`; `sitrep.conformance.md:66`, `:71`, `:76` owe `S-028`, `S-033`, `S-038` to it | later |
| `feat-0071` | place the sitrep into Claude Code sessions | **later** (blocked on `feat-0070`) | `depends_on: [feat-0070]` | when built, it adds always-loaded context: give it a byte budget in its acceptance |

Totals: 2 done but not closed, 1 obsolete, 4 do now, 13 later. Task text now false, to refresh when each is next touched: `chore-0074` (500 lines), `chore-0075` (eleven specs), `chore-0077` (first draft, 21 skills), `feat-0050` (41 spellings), `feat-0051` (twenty skills), `chore-0073` (items 1 and 4 still in scope), `chore-0080` (its motivating defect is fixed).
