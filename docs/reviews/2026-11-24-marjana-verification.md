# 2026-11-24 Marjana overhaul: independent verification

Verification of the integration branch `zen/marjana-2026-11-24` at `6793cb64c0dc26f2650a4ae2855ab3fe01ce99d1` against `origin/main` at `220282ad97e07d95295214e9deb6f0cbfac001bb`, for [`feat-0095`](../../.tasks/done/feat-0095-marjana-integrate-verify-and-ship.md) (rule `A7`). Written by following [`verifier-agent`](../../.agents/skills/verifier-agent/SKILL.md). The contract for the round is the [Marjana plan](2026-11-24-marjana-plan.md). Report only: nothing else in the tree was changed.

The branch had not moved: `git rev-parse origin/zen/marjana-2026-11-24` printed `6793cb64c0dc26f2650a4ae2855ab3fe01ce99d1`. Every check below ran on a checkout of that commit, on Linux, Python 3.13.18, one of the six CI cells.

## Verdict

```text
verdict: pass
blocking_reasons: []
conformance:
  audited: not assessed against an approved spec. The round's one new contract,
    docs/spec/zen-config.md, is status draft and spec_digest.py prints
    "not-approved"; it is pending the maintainer's approval in this pull request,
    by the plan's design. Six approved specs carry amendments marked "pending the
    maintainer's approval" (house-review, install, spec-author, validate-skills,
    verifier-agent, test-author's matrix). All 13 approved specs read "unbound",
    as they did on origin/main.
  unreconciled: []
criteria: 19 of 19 met (below)
findings: 9 (1 major, 3 minor, 5 nit or information), none blocking
verified_by: a fresh Claude Code cloud session, session_017QLseo9RRiLNfhUuEoH8Ye,
  model claude-opus-5-5, high effort, which authored none of the work.
  It was dispatched and briefed by the orchestrator, session_017QLseomNtJvsnYxQu8HkHp,
  so it is independent for the five workstreams' commits and NOT independent for
  the orchestrator's own commits (see "The orchestrator's own commits").
  Commit verified: 6793cb64c0dc26f2650a4ae2855ab3fe01ce99d1.
```

Note on `verified_by`: none of the 57 commits in `origin/main..6793cb6` carries this session's id in its `Claude-Session` trailer (`git log --format='%(trailers:key=Claude-Session,valueonly)'` lists eight other sessions, and four commits carry none).

**Scope of the pass.** It says the tree at `6793cb6` meets every acceptance criterion the five workstream tasks and `chore-0099` declare, that the acceptance command and every declared command succeed, and that an adopter can install the kit and run the new configure step end to end. It does not approve the `zen-config` contract or the six spec amendments (the maintainer's call), and it does not cure finding F1, a process deviation the maintainer has to rule on.

## Check 1: acceptance

```bash
ZEN_CHECKS_SCOPE=full python3 scripts/run-checks.py
```

Exit status 0. Tail, verbatim:

```text
ok          roadmap bookkeeping
            Checked ROADMAP.md: 54 task ids named, 44 in .tasks/done/, 10 in .tasks/, 0 unresolved; 149 blocks read, 0 carrying an open-state claim over a closed id; 1 header rule, 0 tripped; 34 skill status claim(s) in Current state read against 31 SKILL.md file(s), 0 wrong, 0 excepted, 0 stale exception(s). Not judged: the restated-contract class (a roadmap claim restating a spec's own bar, which needs reading that contract), quoted commands and their written-down output, and a hedged phrase in a block that also carries a completion marker. 2 of the 3 shapes chore-0066 mapped are covered, so a pass here is evidence about bookkeeping and about nothing else.
ok          secret scan
            Scanned 556 file(s) for 9 credential shape(s), skipped 0 binary or oversized; 0 finding(s). Fixed-prefix shapes only: a credential with no published prefix is not detected.

11 passed, 0 failed, 0 could not run.
Ran on Linux, Python 3.13.18. CI runs 3 operating systems x 2 Python versions, so this is one of six cells: passing here is necessary but not sufficient.
```

The test gate reported `OK (skipped=2)`; both skips are Windows-only branches (`process identity is established from procStart, which is verified only on Windows`; `the presence fallback is a Windows-path branch`). `ROADMAP_STATUS_EXCEPTIONS` is `frozenset()` at `scripts/run-checks.py:285`, so the eight dated exceptions `feat-0094` landed with have all been retired.

## Check 2: every workstream task's acceptance criteria

Each criterion checked mechanically on `6793cb6`.

| Task | Criterion | Status | Evidence |
|---|---|---|---|
| `chore-0099` | The three reports exist under `docs/reviews/` | met | `ls docs/reviews/`: `2026-11-24-marjana-inventory.md`, `2026-11-24-marjana-plan.md`, `2026-11-24-sources-delta.md` |
| `chore-0099` | Every workstream task file passes `validate.py --strict` | met | `python3 .tasks/validate.py --strict`: `Checked 260 task files: 0 error(s), 0 warning(s).` |
| `chore-0100` | `wc -c AGENTS.md` at most 10240 | met | `9206 AGENTS.md` (origin/main: 27822) |
| `chore-0100` | `CHANGELOG.md` under 40960, every archived entry verbatim under `docs/history/` | met | `31860 CHANGELOG.md`. A script joined every bullet of `origin/main:CHANGELOG.md` with its continuation lines (267 entries), normalised link targets (the archive re-anchors them by its stated rule), and searched `CHANGELOG.md` plus `docs/history/*.md`: 265 found verbatim. The 2 not found are the "Still to record" placeholders (`The test-isolation fix ...: one bullet here`, `The draft-promotion reports ...: one bullet here`), which were promises, now kept: `CHANGELOG.md:49` and the `#110` and `#113` task-log lines at `CHANGELOG.md:87-99` |
| `chore-0100` | `grep -n "10 are drafts" ROADMAP.md` finds nothing | met | grep exit 1, no output |
| `chore-0100` | `ws-a.md` records each kit skill used | met | rows for `doc-sync`, `doc-revise`, `new-task` (not exercised, with reason) |
| `feat-0091` | `zen-config.md` with Given/When/Then; `docs/agents/zen.md` parses | met | 42 scenarios `S-001` to `S-042`, each Given/When/Then; the `backlog` gate runs `.tasks/validate.py`, which checks `docs/agents/zen.md` whenever it exists: 0 errors |
| `feat-0091` | `invocation: user` in both scaffolds | met | `project-bootstrap/SKILL.md:8` and `init-worktracking/SKILL.md:8`: `  invocation: user` |
| `feat-0091` | `ws-b.md` has a row per owned skill | met | script: each of the nine owned skills named in a row, none missing |
| `feat-0091` | `python3 -m unittest tests.test_zen_config` passes; conformance matrix exists | met | `Ran 51 tests in 0.105s` / `OK`; `docs/spec/zen-config.conformance.md` exists |
| `feat-0092` | `orchestrate` and `research` exist with `status: draft` | met | `orchestrate/SKILL.md:10` and `research/SKILL.md:10`: `  status: draft` |
| `feat-0092` | `grep -n "integration branch"` finds `D1` in both lenses | met | `autonomy.md:147-169` and `core.md:33` (quoted in check 5) |
| `feat-0092` | `ws-c.md` has a row per owned skill | met | script: all eleven named |
| `feat-0093` | `house-review` and `doc-sync` at most 250 lines | met | `250 .agents/skills/house-review/SKILL.md`, `250 .agents/skills/doc-sync/SKILL.md` |
| `feat-0093` | `grep -n -i ratchet retro/SKILL.md` finds the new input | met | `retro/SKILL.md:99`: `| **Ratchet** | Would the right check fail on files that exist today ...` |
| `feat-0093` | `ws-d.md` has a row per owned skill | met | script: all eight named |
| `feat-0094` | A test shows each new check failing on bad input and passing on the tree | met | `tests.test_run_checks.RoadmapDraftStatusTests`: `Ran 16 tests` / `OK`; `tests.test_validate_skills.TestStepsEndOnDoneWhen`: `Ran 9 tests` / `OK`; both suites build bad inputs (read, and the red runs reproduced in check 8) |
| `feat-0094` | `install.py --dry-run` prints a headline excluding user-invoked skills | met | `[dry-run] Description budget: 5965 characters for this profile, what Claude Code loads: model-invoked only (core=376, spine=5965, all=6699).` then `878 character(s) more belong to 4 user-invoked skill(s) ...` |
| `feat-0094` | `ws-e.md` records `tdd` red-green per change and a row per status draft | met | red and green columns for `R-005`, `P3` (two cycles), `P11`, `R-001`, `feat-0090`, `chore-0059`; rows for `sitrep`, `quest-tracker`, `agent-observatory` |

`feat-0095` is still open and is not judged here; this report is its first criterion's input.

## Check 3: install cycle into a scratch home

Every run used `--home` under this session's scratch directory; the real home was never touched.

| Selection | Install | Placed | Rendered `disable-model-invocation: true` | `--check` | Uninstall |
|---|---|---|---|---|---|
| default (`spine`) | exit 0 | 20 of 31 | `fix-batch init-worktracking project-bootstrap reconcile-worktrees`, exactly the four placed skills whose source has `invocation: user` | `4 current, 0 diverged, 17 linked, 0 revised upstream, 0 unknown, 0 error(s).` exit 0 | `Uninstalled 21 target(s).` exit 0, 0 files left |
| `--include-drafts` | exit 0 | 28 of 31 | `fix-batch init-worktracking orchestrate project-bootstrap reconcile-worktrees retro`, the six placed user-invoked skills | `6 current, 0 diverged, 23 linked, ...` exit 0 | `Uninstalled 29 target(s).` exit 0, 0 left |
| `--skills orchestrate --include-drafts` | exit 0 | 19 (closure) | `fix-batch orchestrate reconcile-worktrees retro` | `4 current, 0 diverged, 16 linked, ...` exit 0 | `Uninstalled 20 target(s).` exit 0, 0 left |

Budget headline and closing lines, default profile, verbatim:

```text
Done: profile 'spine', 20 of 31 skill(s) x 1 tool(s), plus the rules module.
Description budget: 5965 characters for this profile, what Claude Code loads: model-invoked only (core=376, spine=5965, all=6699).
878 character(s) more belong to 4 user-invoked skill(s) (fix-batch, init-worktracking, project-bootstrap, reconcile-worktrees): Claude Code keeps them out of context, so start one by name, as /<name>; OpenCode loads them.
In each repository, run `init-worktracking` once to configure the skills (docs/agents/zen.md).
```

With `--skills orchestrate --include-drafts`, where `init-worktracking` is not placed, the pointer changes correctly to: ``Each repository is configured once by `init-worktracking`, and `init-worktracking` is not in this selection: add it with `--skills init-worktracking`.``

```bash
python3 scripts/build-adapters.py --marketplace --check
```

Exit 0: `The committed marketplace is current: 25 skill(s) in .claude-plugin/plugin/, and .claude-plugin/marketplace.json.` 25 is the shipped count (31 less 6 drafts).

## Check 4: end-to-end adopter run, outside the repository

A scratch git repository (`tinycalc`: `pyproject.toml`, `src/tinycalc/__init__.py`, one unittest, a README; no remote, branch `main`), worked by reading `init-worktracking/SKILL.md` at `6793cb6` and following it step by step. **I stood in for the person and accepted every recommendation.**

- Step 1: a git repository; none of the five targets present; no tracker found.
- Step 2: recommended **lite** (small, one contributor) and **production** (the code carries a test). Accepted.
- Steps 3 and 4: wrote `AGENTS.md`, `.tasks/README.md`, `.tasks/_TEMPLATE.md`, `.tasks/validate.py` (verbatim), `.tasks/done/.gitkeep`, `CLAUDE.md`, applying `references/tier-stripping.md`. `grep -rn "ROADMAP\|CHANGELOG\|{{"` over the four files: empty.
- Step 6, configure: `tracker` settled (`.tasks/` exists). Documents: recommended `glossary: none`, `adr_dir: none`, `spec_dir: none`, `standards: AGENTS.md`. How work lands: `acceptance: python -m unittest discover -s tests`, `base_branch: main` (no `origin/HEAD`, the one local branch), `integration_prefix: none`, `merge_policy: a person merges every change into main`. Agent work: `default_mode: hitl` (the step's own recommendation); `session_logs` and `memory` left out as unknown. All accepted. Wrote `docs/agents/zen.md` from `zen.md.tmpl`, appended the pointer block: `grep -c "^## Agent skills" AGENTS.md` printed `1`. Labels: `tasks` tracker, so none printed, as the step says.
- Step 7: manifest written; `git check-ignore` found none of the targets ignored.

```text
$ python3 .tasks/validate.py --strict
Checked 0 task files: 0 error(s), 0 warning(s).
strict exit=0
$ python3 .tasks/validate.py --links "*.md" "docs/**/*.md" ".tasks/*.md"
checked 6 documents, 0 broken link(s)
```

Degenerate inputs from `docs/spec/zen-config.md`, each restored afterwards. Every one exited 1 with one error:

| Input | `validate.py --strict` said |
|---|---|
| S-041, closing fence removed | `ERROR docs/agents/zen.md: the zen-config block is never closed: add its closing fence` |
| S-042, `glossary: docs/../GLOSSARY.md`, file present | `glossary 'docs/../GLOSSARY.md' is not a normalised path: write it without '.', '..' or empty segments` |
| S-042, `glossary: ./docs//x.md` | the same message for the empty segment |
| unknown key `favourite_colour: blue` | `unknown key 'favourite_colour'` |
| `tracker: none` | `tracker 'none' is not one of ['github', 'gitlab', 'other', 'tasks']` |
| `config_version` removed | `config_version is required` |
| empty file; prose with no block | `found 0 zen-config blocks; exactly one is required` |
| block twice | `found 2 zen-config blocks; exactly one is required` |
| `config_version: 2` | `config_version is 2, and this validator reads versions up to 1: update .tasks/validate.py from the kit` |
| `config_version: 01` | `config_version '01' must be a positive whole number` |
| `default_mode: HITL` | `default_mode 'HITL' is not one of ['afk', 'hitl']` |
| `spec_dir: /etc`; `spec_dir: docs\spec` | `... must be a forward-slash path inside the repository` |
| `spec_dir: docs/missing`; `spec_dir: DOCS` (on-disk `docs`) | `... does not exist (letter case included)` |
| a task with `mode: auto` | `ERROR .tasks/feat-0001-add-subtraction.md: mode 'auto' is not one of ['afk', 'hitl']` |

After restoring: exit 0.

## Check 5: rule `D1`

`core.md:32-36`, verbatim:

> **A8.** Push to a branch of your own and open a draft pull request. Never merge your own work. One exception: an orchestrator may fast-forward an integration branch to work it did not author, once an agent that is neither its author nor the orchestrator, nor dispatched or briefed by the author, passed that exact commit (`A7`). Only a person merges into the base branch (`developer`, `main`).

`autonomy.md:147-171` carries the full exception: four guards (not its own work, with dictation defined; verified by someone else on the exact commit, latest verdict, no unanswered `fail`; a fast-forward onto the integration branch only, a merge commit or conflict resolution going back to the child; a person merges into the base branch), and a paragraph saying the orchestrator's own commits on the integration branch are not landed under the exception.

The plan's `D1`: "Only work it did not author, only after someone else verified it (`A7`), only into an integration branch. A person always merges into `developer` or `main`." **The text is no wider than `D1`.** Each of `D1`'s three conditions and its base-branch clause is present; the text adds restrictions `D1` did not state (fast-forward only, exact commit, verifier not dispatched or briefed by the author, dictation counts as authorship). It grants nothing `D1` withholds. The tree does not live up to its guard 3, though: see F1.

## Check 6: coherence

- **`zen` names all 31 skills.** A script read every `SKILL.md` frontmatter (31 skills, 6 drafts, 8 user-invoked) and searched `zen/SKILL.md` for each name in backticks: none missing. Each of the six drafts is named on a line carrying `*(draft)*`; no shipped skill is marked a draft.
- **`docs/CATALOG.md` against frontmatter**, by script over every `| \`name\` | status | invocation |` row: 31 skills, 31 rows matched, 0 mismatches, no duplicate rows, no shipped or draft row naming a missing skill.
- **`ROADMAP.md` "Current state"** is true at `6793cb6`: 31 skills, 25 shipped and 6 drafts with the names right; four lenses plus `core.md` (`ls .agents/rules/`); seven hooks (`ls .agents/hooks/*.py | wc -l` printed 7); `A1` to `A11` (`grep -oE "\*\*A[0-9]+\."`); `spine` places 20; 13 specs at `status: approved` (frontmatter of every spec; the fourteenth, `zen-config`, is `draft`). Its "Measured ... at `6162d00` merged with WS-E's branch" is dated and correct for that date.
- **README "What's new"**, every number: `AGENTS.md` "about 28 KB to about 9 KB" (27,822 to 9,206 bytes, true); "the two scaffolds no longer spend an adopter's description budget" (both render user-invoked, check 3, true); "counts only what Claude Code loads" (true); the two gates exist and are tested (true). One overstatement: F4.
- **Sizes**: `AGENTS.md` 9,206 bytes (at most 10,240); `CHANGELOG.md` 31,860 bytes (under 40,960).

## Check 7: provenance

```bash
python3 scripts/check-provenance.py
```

Exit 1: `45 up to date, 3 drifted, 0 unlocatable, 0 error(s).` The three drifts:

```text
.agents/hooks/delegation-reminder.py:41  DRIFT: https://raw.githubusercontent.com/moonray/repoprompt-workflows/main/.agents/hooks/delegation-reminder.py
.agents/rules/review-quality.md:258  DRIFT: https://raw.githubusercontent.com/moonray/repoprompt-workflows/main/.agents/skills/review-quality/SKILL.md
.agents/rules/review-quality.md:267  DRIFT: https://raw.githubusercontent.com/moonray/repoprompt-workflows/main/.agents/workflows/Deep-Review.md
```

None is introduced by this branch: each recorded digest (`92ea2a78...`, `5cf5a6e5...`, `77437e6e...`) is present byte-for-byte in `origin/main` (`git grep` found all three there). Upstream moved. Every provenance block this round added (`orchestrate`, `research`, `retro`, `human-handoff`, `house-review`, `grill`, and the rest) reads `up to date`. See F5.

## Check 8: dogfood records

Ten rows sampled across four records (`ws-b`, `ws-c`, `ws-d`, `ws-e`), each checked against the tree or history:

| Record, row | Claim | Found |
|---|---|---|
| `ws-c`, `orchestrate` | commits `c37c7db`, `9acb338`, `6cafcee`, `5fd8e6f`; deadlock rule in Step 3 (`ff7c441`) | all five exist; `orchestrate/SKILL.md:116-117`: "**An empty frontier while unlanded children remain is a deadlock**" |
| `ws-c`, `verifier-agent` | F2 closed in `autonomy.md` by `897e6e0` | `897e6e0` "tighten D1 per independent verification (F1-F8)" changes `autonomy.md`, `core.md` |
| `ws-c`, `research` | first runs are child commits `24e255e`, `d835f3f` | both exist, each with a different session trailer from the orchestrator's |
| `ws-c`, `tdd` | Step 3 now has the interface-only stub, and a test passing on arrival is kept only after breaking the code | `tdd/SKILL.md:85` "interface-only stub"; `:90` "after breaking the code on purpose and seeing the test fail" |
| `ws-b`, `project-bootstrap` | Step 2 now asks for the acceptance command | Step 2: "when step 1 found none, the acceptance command: offer the stack's usual test command as the recommendation" |
| `ws-b`, `new-task` | `mode: auto` gives `mode 'auto' is not one of ['afk', 'hitl']` | reproduced in the scratch adopter (check 4), the same message |
| `ws-d`, `doc-author` | now says never run it against the real service, and describes the dry walk | `doc-author/SKILL.md:41` "never run it against the real service"; `:49` the dry walk |
| `ws-d`, `improve-architecture` | 48 commits on a shallow clone, 81 on a full one | this clone was shallow: `git log 4b41861 -- scripts/` gave 46; after `git fetch --unshallow`, 81; the report says 81 at line 30 |
| `ws-e`, `chore-0059` | mutating `FENCE_RE`'s `{0,3}` to `{0,4}` fails a test | reproduced in a scratch worktree of `6793cb6`: `FAIL: test_the_shared_copy_is_identical_to_the_original ... (name='FENCE_RE')`, `FAILED (failures=1, skipped=2)`; worktree removed |
| `ws-e`, `P3` | `RoadmapDraftStatusTests` green | `Ran 16 tests` / `OK` (the record says 13 at its second cycle; the verifier fix round `44f885c` added tests after it, consistent) |

Every sampled row's evidence was found. One claim in `orchestrator.md` is false at this commit: F2.

## Check 9: commit trailers

```bash
git log --format=%B origin/main..6793cb6 | grep -ci co-authored
```

Printed `0`.

## Check 10: the orchestrator's own commits

**Reviewed by a verifier the orchestrator dispatched, so not independent under `A8`'s exception.** The maintainer's review is the independent check for these.

Found by `git log --grep=session_017QLseomNtJvsnYxQu8HkHp origin/main..6793cb6`: the six the brief named, plus `9598355`.

| Commit | What it does | Review |
|---|---|---|
| `9598355` | `chore-0099`: the plan, the four decisions, the five workstream task files | Not in the brief's list; authored by the orchestrator session. Documentary; the plan is the round's contract. No defect found. See F3 |
| `c0579ad` | Merge landing WS-C at `9b9c311` | A merge commit, not a fast-forward (F1). I re-ran `git merge-tree --write-tree c0579ad^1 c0579ad^2`: conflicts in exactly `plugin.json`, `ROADMAP.md` and the plan. `git diff <auto-merge-tree> c0579ad` touches only those three files, and each resolution keeps both sides' intent (WS-C and WS-D both shown shipped, links to `.tasks/done/`, a fresh plugin version hash). Correct |
| `6162d00` | Merge landing WS-B at `e9775bf` | Same method: conflicts in `plugin.json`, `ROADMAP.md`, the plan and `tests/test_validate_skills.py`; the resolution sets the supporting-file count to `{"markdown": 19, "template": 10, "other": 9}`, both sides' additions, which the test gate confirms. Correct |
| `536c35a` | README "What's new", CATALOG rows, dogfood index and the orchestrator's record | Claims checked in check 6; CATALOG matches frontmatter. F2 and F4 are in this commit |
| `2763c36` | Reviewer nits applied to `orchestrate`, `research`, `fix-batch`, `spec-author`, the `zen-config` key table; D1 citation; `chore-0074` closed; changelog lines | Edits are wording and citations, no behaviour change; the `zen-config` edit points `session_logs` at the Paths section's outside spellings, consistent with S-012. The `changelog-2026-08.md` edit re-anchors one link for the `chore-0074` move, which the archive's rule allows. Applying reviewer fixes itself makes these edits the orchestrator's own (guard 1); they are listed as its own, so covered, but F2 follows. Two lines left long (F7) |
| `3d40f25` | WS-E in the dogfood index; setup step and `orchestrate` in `GETTING-STARTED.md` | No defect |
| `6793cb6` | Regenerates the plugin tree for `2763c36`'s `fix-batch` and `spec-author` edits | `build-adapters.py --marketplace --check` is current. Between `2763c36` and `6793cb6` the plugin tree was stale; at the verified head it is not |

Also on the integration line: `2940be0`, a merge of `zen/marjana-research-sources` with **no** `Claude-Session` trailer, so its author cannot be named from history. It predates `D1` (the plan is its child). Its tree equals the automatic merge of its parents (`088e9afc...` both ways), so it adds nothing beyond `24e255e` and `d835f3f`. And `24e255e`, the inventory research child's commit, sits directly on the integration line rather than on a child branch.

WS-A's fix commit `92d4697`, which `orchestrator.md` says only the orchestrator re-checked: it is child work, not the orchestrator's, so this verification, by an agent neither its author nor the orchestrator and not briefed by WS-A, is an independent check of it under guard 2.

## Findings, ranked

**F1. Major (process). Two workstreams landed by orchestrator merge commits, which the shipped rule forbids.**
Where: `c0579ad`, `6162d00`; rule at `.agents/rules/autonomy.md:161-164` and `.agents/rules/core.md:33`; `orchestrate/SKILL.md:146-150`.
Evidence: `autonomy.md:161`: "3. **A fast-forward onto the integration branch only.** ... A landing that needs a merge commit or a conflict resolution goes back to the child." `git log --format='%h %p'` shows `c0579ad` with parents `dcf8c92 9b9c311` and `6162d00` with parents `c0579ad e9775bf`, each resolving conflicts. The verified child commits `9b9c311` and `e9775bf` are not the commits that landed; the merged trees were verified by nobody until this report, and this report is not independent for them. The orchestrator disclosed both, in `orchestrator.md` ("Rule `D1` guard 3 ... was written by a child while this session was already landing") and in each commit message.
I found the resolutions mechanical and correct (check 10), and the tree at `6793cb6` passes every check.
Suggested fix: the maintainer decides. Either accept the two merges as disclosed orchestrator work and keep them in the pull request body's unverified list, or answer the question the orchestrator raised: amend guard 3 to allow a mechanical-only orchestrator merge with a defined test for "mechanical", or keep it and have `orchestrate` say what to do when landing order makes a fast-forward impossible.

**F2. Minor. The orchestrator's dogfood record says it wrote no skill text; at this commit it has.**
Where: `docs/reviews/2026-11-24-dogfood/orchestrator.md:3`.
Evidence: "It wrote no skill text." Commit `2763c36`, authored by the orchestrator session after this line was written (`536c35a`), changes `.agents/skills/orchestrate/SKILL.md` (27 lines), `research/SKILL.md`, `fix-batch/SKILL.md`, `spec-author/SKILL.md` and `docs/spec/zen-config.md`.
Suggested fix: say it applied the reviewers' wording fixes to those four skills and the spec itself in `2763c36`, and that they are its own work under guard 1.

**F3. Minor. The orchestrator's commit list omits `9598355`, and `2940be0` is unattributed.**
Where: the verification brief's list; whatever list the pull request body carries.
Evidence: `git log --grep=session_017QLseomNtJvsnYxQu8HkHp` returns `9598355` besides the six named. `2940be0` has no `Claude-Session` trailer (check 10).
Suggested fix: add `9598355` to the pull request's own-commits list, and say who made `2940be0` if the session knows.

**F4. Minor. README overstates the dogfood coverage.**
Where: `README.md:53`.
Evidence: "Every skill this round touched was run on the round's own work". `ws-c.md` records `systematic-debugging` (touched by WS-C's `P10`) as "not exercised" and `test-author` as "not exercised (routed away correctly)"; `ws-a.md` records `new-task` as not exercised. The dogfood index itself says it correctly: "or on a realistic scratch target ... A skill that was not exercised is recorded as such".
Suggested fix: "Every skill this round touched was run on the round's own work or a scratch target, or recorded as not exercised, in the dogfood records."

**F5. Information, pre-existing. Three provenance blocks have drifted upstream.**
Where: `.agents/hooks/delegation-reminder.py:41`, `.agents/rules/review-quality.md:258`, `:267`.
Evidence: check 7; the recorded digests are identical on `origin/main`.
Suggested fix: not this pull request's; a separate task to review the moonray upstream changes and re-record.

**F6. Information. Contracts awaiting the maintainer.**
Where: `docs/spec/zen-config.md` (`status: draft`, `spec_digest.py`: `not-approved`); amendment notes in `house-review.md`, `install.md`, `spec-author.md`, `validate-skills.md`, `verifier-agent.md`.
Evidence: each amendment says "pending the maintainer's approval". `zen-config.md`'s own header says the second `spec-quality` run returned `needs_revision` and its fixes were not re-checked by design.
Suggested fix: approve, or not, in the pull request review. The `zen-config` path and block format are the round's one-way door (`D2`).

**F7. Nit. Two lines in `orchestrate` left unwrapped by a commit that says "rewrapped".**
Where: `.agents/skills/orchestrate/SKILL.md:113` (141 characters) and `:149` (163 characters), from `2763c36`; the file otherwise wraps near 100.
Suggested fix: rewrap; no gate enforces it.

**F8. Nit. Two validator messages could be clearer.**
Where: `.agents/skills/init-worktracking/templates/validate.py:746`, `:779`.
Evidence: `config_version '01' must be a positive whole number`, where `01` reads as one; the rule broken is "no leading zero". A backslash path is echoed through `!r` as `'docs\\spec'`, doubling the backslash the person typed. Also, a clean run prints only `Checked 0 task files: ...`, so the person cannot tell that `docs/agents/zen.md` was checked at all.
Suggested fix: name the leading zero; print the value without `repr`; mention the setup file in the summary line when it exists.

**F9. Nit. The `zen.md` template leaves a trailing blank line.**
Where: `.agents/skills/init-worktracking/templates/zen.md.tmpl`, last line `{{TRACKER_NOTES}}`.
Evidence: for any tracker but `other` the placeholder is empty, so the written file ends with two newlines (seen in the adopter run).
Suggested fix: strip trailing whitespace when the notes are empty.

## Coverage (`A6`)

**Checked:** the acceptance command at full scope; all 19 acceptance criteria of `chore-0099`, `chore-0100` and `feat-0091` to `feat-0094`; three install, check and uninstall cycles plus the marketplace check; one full adopter run of `init-worktracking` steps 1 to 7 at lite tier and 17 degenerate inputs; the `D1` text against the decision; `zen`, CATALOG and ROADMAP against frontmatter by script; every number in README "What's new"; provenance with network; ten dogfood rows, two of them reproduced by running code; the trailer grep; every orchestrator commit, with both merge resolutions re-derived from `git merge-tree`; the verbatim survival of every archived changelog entry.

**Not checked:**

- The other five CI cells (Windows, macOS, the second Python). Only Linux and Python 3.13.18 ran here.
- Conformance matrices row by row. The `matrix citations` gate passed; I did not re-derive any matrix.
- The adopter run at `standard` or `team` tier, the `github`, `gitlab` or `other` tracker paths, a re-run of the configure step (S-016, S-034, S-039), or `project-bootstrap` end to end. WS-B's record claims some of these; I did not reproduce them.
- Whether a model, as opposed to me reading the text, follows the new skills: `orchestrate` and `research` are drafts with one run each.
- The behaviour of the hooks under a real harness session, and the Codex sidecar and destructive-git gate (optional in `feat-0094`; I did not check whether they were built).
- The dogfood rows I did not sample, including every row of `ws-a.md` and `orchestrator.md` beyond F2.
- The quality of the reader documents' prose beyond their factual claims; that is `house-review`'s, not this report's.
- `D3` (branch deletions and the cherry-pick), which happens after the pull request opens.
