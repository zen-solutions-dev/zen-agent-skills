# Dogfood record: the quest rename (2026-11-25)

Every skill and tool whose behaviour [`feat-0101`](../../../.quests/done/feat-0101-rename-tasks-to-quests.md) changed, run on this rename itself or on scratch repositories outside this checkout, per rule 8 of the [round 1 plan](../2026-11-24-marjana-plan.md) as kept by the [round 2 plan](../2026-11-25-marjana-r2-plan.md). Each row says what it ran on, the evidence, and the verdict. A skill not exercised says so and why.

The kit was installed with `python3 scripts/install.py --include-drafts` before the work. It placed at user scope (`~/.claude/skills`, `~/.agents/skills`); the installer has no project-scope option. `new-task`, `doc-sync` and `house-review` were among the placed skills, but none of the kit's skills was loaded in the session that did the work (the session-start hook said so), so each was followed by reading its `SKILL.md`.

Four scratch repositories, all under the session's scratchpad directory and never committed here:

- `old`: a git repository laid out as an adopter scaffolded before the rename: `.tasks/validate.py` (the shipped template), `.tasks/README.md`, an open `feat-0001` and a done `feat-0002`, and `docs/agents/zen.md` with `tracker: tasks`.
- `empty`: a git repository with only `.quests/validate.py`.
- `bad`: a `.quests/` holding a file with no frontmatter and one with a wrong id, a bad status, an unknown dependency and a missing `touched_files` path, beside `tracker: quest` (a typo for `quests`); and `bad2`, a validator in `.tasks/` beside `config_version: 2`.
- `kit`: a `git worktree` of this repository, first at `origin/zen/marjana-r2-2026-11-25` (before the rename), then at this branch's first commit `a2fab2b`, installing into a scratch home.

## Runs

| Skill or tool | Ran on | Evidence | Verdict |
|---|---|---|---|
| `new-quest` (was `new-task`) | Its first real run under the new name: this workstream's own quest, [`feat-0101`](../../../.quests/done/feat-0101-rename-tasks-to-quests.md). Steps 1 (tracker and next id), 3 (every `touched_files` path checked) and 5 and 6 followed; step 4's split was not put to a person, because the brief fixed the id and the scope. | Written from `.quests/_TEMPLATE.md`. `python3 .quests/validate.py --strict` then reported the one finding step 6 predicts: `ERROR .quests/.scaffold.json: id_high_water['feat'] is 95 but feat-0101 already exists`. Raising `feat` to 101 gave `Checked 261 quest files: 0 error(s), 0 warning(s).` | Works |
| `validate.py`, old names | `old`, then `old` after `git mv .tasks .quests` with `tracker: tasks` kept. | `python3 .tasks/validate.py --strict`: `Checked 2 quest files: 0 error(s), 0 warning(s).`, exit 0. After the move, `python3 .quests/validate.py --strict`: the same line, exit 0. | Works: S-043 |
| `validate.py`, degenerate input | `empty`. | `python3 .quests/validate.py --strict`: `Checked 0 quest files: 0 error(s), 0 warning(s).`, exit 0. An empty tracker is valid, as before the rename; the zero count is the only sign nothing was checked. | Works as designed; the silent zero is noted, not changed |
| `validate.py`, malformed input | `bad` and `bad2`. | Exit 1 with six errors, one per defect: `no YAML frontmatter block`; `invalid status: 'finished'`; `id 'feat-0009' does not match filename 'feat-0002-wrong.md'`; `depends_on unresolved: 'feat-0404' is not a known quest id`; `touched_files path does not exist: missing.py`; `tracker 'quest' is not one of ['github', 'gitlab', 'other', 'quests', 'tasks']`. With `config_version: 2` the one message ends `update .quests/validate.py from the kit` in `.quests/`, and `update .tasks/validate.py from the kit` in `bad2`'s `.tasks/`. | Works: S-007 as amended, S-008 as amended |
| `sitrep` | `old`, before and after the move. | `load_tasks()` on `old`: `[('feat-0002', '.tasks/done/feat-0002-done.md', True), ('feat-0001', '.tasks/feat-0001-old.md', False)]`, no notices. After `git mv .tasks .quests`, `build_board(since='HEAD~1')` gave `{'commits': 1, 'closed': [], 'updated': []}`: the move closed nothing. Without the rename guard the moved `done/` file would have read as closed (the mutation run below). | Works: S-041 |
| `install.py` | `kit`, the upgrade path an adopter takes: install before the rename, pull, check, install again. | Before: `--skills new-task --tools claude` placed `new-task` and its closure. After checking out `a2fab2b`, `--check` exited 2: `error claude new-task the kit no longer has a source at .../new-task`. `--skills new-task` then printed `'new-task' was renamed 'new-quest'; placing 'new-quest'.` and `retired claude new-task (...: renamed new-quest)`; the home held `domain-language grill new-quest spec-author spec-quality`, and `--check` gave `0 error(s)`, exit 0. The exit-2 `--check` led to one change: it now adds `The skill was renamed 'new-quest': an install run retires this one and places that.`, rerun in `kit` with that line printed. | Fixed, then works: S-030 |
| `doc-sync` | The reader-facing documents this change could have made stale, change scope this branch against `origin/zen/marjana-r2-2026-11-25`: `README.md`, `docs/CATALOG.md`, `docs/GETTING-STARTED.md`, `docs/INSTALL.md`, `docs/ARCHITECTURE.md`, `CONTRIBUTING.md`, `docs/ISSUE-LINKING.md`, `docs/agents/zen.md`, `docs/spec/README.md`, `.agents/hooks/README.md`. Grounding facts: `.tasks/` and `.agents/skills/new-task/` no longer exist here, and `ROADMAP.md`'s headings are Campaigns. | Applied: the tracker-item uses of "task" in `docs/GETTING-STARTED.md`, `docs/ISSUE-LINKING.md` and `docs/ARCHITECTURE.md`. Reported, not applied, because the brief keeps them for the orchestrator: `README.md` lines 110 and 176 ("task file"), `docs/CATALOG.md` lines 21, 22, 61 ("task files") and 36 ("Epic B"). `docs/CATALOG.md` line 111's "Epic B lenses" is a record of provenance and stays. Not audited: `docs/spec/` contracts beyond the three this change amended. | Works, scoped |
| `init-worktracking` | Not exercised. | Its text now treats a `.tasks/` holding `validate.py` as the scaffold under its old name and writes `tracker: quests` on a first run; no scaffold or configure run happened after the change. The validator it ships was exercised above. | Not exercised: no repository to scaffold in this session |
| `quest-tracker` | Not exercised. | Wording only: `sitrep reads quest files`, and one sentence in the authoring guide saying a tracker's `quests` entry is a run of steps on the page, not a quest file. | Not exercised: no behaviour changed |
| `house-review` | Not run by this session. | The orchestrator's landing review is the review of this branch. | Not exercised here |

## Mutation runs

Each alias test was shown to fail with its alias removed, then passed with it restored:

- `tests/test_zen_config.py`: `tasks` removed from the validator's tracker set: `FAILED (failures=2)`.
- `tests/test_sitrep_git.py`: the `moved_done` guard removed: `FAILED (failures=1)`; the `ls-files` pathspec narrowed to `.quests`: `FAILED (failures=1)`.
- `tests/test_install.py`: the retire loop given an empty table: `FAILED (failures=2)` in `RenamedSkillTests`.

## Review fix round, 2026-11-25

The orchestrator's independent verifier returned `fail` on `5e9e398`; these are the fixes, each with the run that shows it.

| Finding | Change | Evidence |
|---|---|---|
| F1, the shipped rename table was untested | `RealRenameTableTests` reads `RENAMED_SKILLS` unpatched: it maps `new-task` to a skill the kit has, and a real-kit `--skills new-task --dry-run` places `new-quest`. | With the table set to `{}`: `FAILED (failures=2)`. |
| F2, a run without `new-quest` retired `new-task` | `install()` retires an old name only when the same run placed its successor in that tool directory; otherwise it prints `kept`, says the new name was not placed and how to place it, and leaves the target and its record. `--check`'s hint now says "an install run that places 'new-quest' retires this one". | `test_a_run_that_does_not_place_the_successor_keeps_the_old_placement` keeps an edited copy and its record; with the guard removed it errors. |
| F3, the hook's `.tasks` marker was untested | `TrackerRootMarkerTests`: a tree with no `.git` or `AGENTS.md`, one level below a spare directory. | With `.tasks` dropped from the markers: `FAILED (failures=1)`. |
| F5, both directories merged silently | The validator (both copies) warns once when `.quests/` and `.tasks/` both exist, naming the `git mv` fix; `sitrep` adds a notice when files are tracked under both. A scratch repository `half` (one quest left in `.tasks/`, one moved) gave `WARN .quests/: both .quests/ and .tasks/ exist, and this run checks only .quests/; finish the move with git mv ...` from the validator and `notice: both .quests/ and .tasks/ are tracked: ...` from `sitrep`. | Removing the warning: `FAILED (failures=2)` per validator copy; removing the notice: `FAILED (failures=1)`. |
| F4, F7, F8 | Wording only: remaining Feature and Epic pointers in current documents, the rationale's incident prose restored with links repointed, and the `epic` type prefix explained in the glossary. | `ZEN_CHECKS_SCOPE=full python3 scripts/run-checks.py` exits 0 after the round. |
