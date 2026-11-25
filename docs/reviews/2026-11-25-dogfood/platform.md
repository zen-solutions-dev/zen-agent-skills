# Dogfood record: platform and gates (2026-11-25)

What [`feat-0103`](../../../.quests/feat-0103-platform-and-gates-for-round-2.md) built, run on degenerate input and against its own tests with each feature removed, per the [round 2 plan](../2026-11-25-marjana-r2-plan.md). Every run below happened in this session; a run done by a delegated worker says so.

The kit was installed with `python3 scripts/install.py --include-drafts` before the work, and the kit's skills were then listed as reachable in the session. The quest file was written from `.quests/_TEMPLATE.md` and checked with `python3 .quests/validate.py --strict`, which is `new-quest`'s check; `new-quest`'s `SKILL.md` was not read step by step. Two parts were built by delegated workers in this session and checked here afterwards: the destructive-git gate and the release script. A third delegation, for the Codex sidecar, was refused by the environment's permission check (it asked to install a Codex CLI), and the work was done here without installing anything.

## Degenerate input

| Check | Input | What it said |
|---|---|---|
| N1, both tracker directories | This checkout with an ignored `.tasks/__pycache__/x.pyc` (`git status`: `!! .tasks/`) | New validator, `--strict`: `Checked 261 quest files: 0 error(s), 0 warning(s).` The committed copy before this change, same tree: `ERROR .quests/: both .quests/ and .tasks/ exist, ...` and `1 error(s)`. |
| Draft expiry (D1) | An empty `.agents/skills/` | `No skills found under .../.agents/skills.` |
| Draft expiry (D1) | One draft with no `metadata.drafted`, in a git repository with no commit adding it | `WARN  drafty/SKILL.md: a draft no file under docs/reviews/*dogfood* names, drafted unknown (no metadata.drafted, and git has no commit adding it); the 90-day expiry cannot be checked`, exit 0. |
| Draft expiry (D1) | The real kit | 0 warnings: all six drafts are named in a dogfood record. Dates read from git: `agent-observatory` and `systematic-debugging` 2026-08-29, `sitrep` 2026-09-11, `quest-tracker` 2026-10-20, `orchestrate` and `research` 2026-11-24. |
| Changelog lines (B4) | No file; an empty file; a file with no task-log lines | `CHANGELOG.md: absent, so 0 task-log lines were measured.`; ``CHANGELOG.md: no `## Task log` heading, so 0 task-log lines were measured.``; `Measured 0 task-log line(s)` (each pinned in `tests/test_run_checks_changelog.py`). The real file: `Measured 38 task-log line(s) in CHANGELOG.md: 0 new lines over the limit; 19 excepted, 0 stale exception(s).` |
| Skill listings (E9) | No `docs/CATALOG.md`; a repository with no skills | Fails: `docs/CATALOG.md: absent, so no skill could be found in it.` and `Checked 1 of 2 listing(s)`; the empty repository fails too, `against 0 skill(s)`. The real kit: `Checked 2 of 2 listing(s) against 31 skill(s): 0 finding(s) failing.` |
| Supporting-file list (B3) | A skills tree with a file the list lacks | The test names it: `([('house-review/references/rationale.md', 'markdown')], [])` when that line was deleted from the list. |
| Spec-digest readers (R-003 b) | A tree with a fifth reader, an unrelated skill, `spec-author` and a directory with no `SKILL.md` | Derives `['fifth']` only. The real kit derives `['new-quest', 'spec-plan-readiness', 'test-author', 'verifier-agent']`, the four the literal tuple held. |
| Release script (D5) | A directory with no `CHANGELOG.md`; an empty `CHANGELOG.md` | `Could not run: .../CHANGELOG.md: could not be read (No such file or directory).`, exit 2; `Refused: ... no '## Releases' heading, so there is no section to date.`, exit 1. The real repository, `--bump minor --dry-run --no-git`: `v0.2.0`, exit 0, nothing written, ending `git tag -a v0.2.0 ...` and `git push origin v0.2.0` printed, not run. |
| Destructive-git gate (D3) | Empty stdin | Printed nothing, exit 0. The worker also ran `{}` (nothing, exit 0). |
| Codex sidecar (E7) | A description of `""` | `short_description: ""`, pinned by a test; `validate-skills.py` fails such a skill before it ships. A real `--target codex` run into a scratch directory placed 25 shipped skills, and every sidecar parsed with PyYAML. |

## Mutation runs

Each feature was removed or weakened in place, the named tests run, and the file restored and compared byte for byte with its backup.

| Item | Mutation | Tests that failed |
|---|---|---|
| N1 | drop the guard that the other directory must hold a Markdown file | `test_an_old_directory_holding_only_ignored_bytecode_is_silent_under_strict`, and the copies-agree test |
| R2-10 validator | report the old names through `warn()`, which `--strict` promotes | `test_a_validator_run_from_the_old_directory_warns`, `test_tracker_tasks_warns_under_strict_without_failing`, and the copies-agree test |
| R2-10 sitrep | never raise `NOTICE_OLD_TRACKER` | `test_a_tasks_directory_is_read_as_the_tracker`, `test_both_tracker_names_at_once_raise_a_notice`, `test_s042_the_old_name_alone_says_when_the_alias_goes` |
| R2-10 install | drop `ALIAS_EXPIRY` from the warning | `test_the_old_name_warns_that_the_alias_expires` |
| B3 | delete one line from `tests/fixtures/supporting-files.txt` | `test_classification_of_the_real_shipped_supporting_files`, naming the file |
| R-003 b | narrow the reader pattern to "edited since" | `test_the_derived_consumers_include_every_known_reader`. A first attempt at this mutation did not apply (a quoting mistake in the edit) and its passing run is void. |
| R-003 a | do not call `check_composed_by()` | three `ComposedByTests` |
| R2-3 | drop the error for a relative link to a draft | `test_a_relative_link_to_a_draft_fails`, `test_a_relative_link_beside_the_guard_still_fails` |
| R2-3 | drop the unguarded-load warning | `test_an_unguarded_load_of_a_draft_warns`, `test_a_guard_missing_its_otherwise_clause_is_unguarded` |
| D1 | ignore `metadata.extended` (added after feat-0102's relay) | `test_an_extension_restarts_the_ninety_days`, `test_an_extension_without_a_date_is_reported` |
| R2-3 | drop the warning for a guard with no "; otherwise" clause (added after feat-0102's relay) | `test_a_guard_with_no_otherwise_clause_warns` |
| D1 | expire at 90 days inclusive | `test_exactly_ninety_days_is_not_over` |
| D1 | ignore the dogfood records | `test_a_dogfood_record_naming_it_silences_the_warning`, and two `GuardedLoadTests` whose fixtures rely on a record |
| B4 | ignore the exception list | `test_an_excepted_long_line_is_silent_and_counted` (a first attempt matched two places and did not apply; void) |
| B4 | never report a stale exception | `test_a_stale_exception_is_named_for_deletion` |
| B4 | loosen the limit by 100 | three tests |
| E9 | make `zen` name itself | `test_every_skill_named_in_both_passes_and_zen_need_not_name_itself`, `test_an_unnamed_draft_fails_unless_excepted_with_a_reason`, `test_the_real_kit_passes_and_the_gate_runs_on_documentation_changes` |
| E9 | count a bare substring as naming | `test_a_bare_word_does_not_count_as_naming` |
| E9 | drop the stale-exception check | `test_a_stale_exception_fails` |
| R-004 | drop the markup normalisation | `test_markup_in_the_source_does_not_decide_it` |
| R-004 | drop the code-span exclusion | first run: none failed, because the fixture's `""` could never match. The fixture was changed to a multi-word quote inside a code span; rerun: `test_a_quote_inside_a_code_span_is_not_a_double_quoted_citation` |
| R-004 | make a phrase that resolves nowhere fail | `test_a_stale_double_quoted_phrase_warns_without_failing` |
| R-004 | extract nothing | three `DoubleQuotedPhraseTests` |
| E7 | drop the invocation-to-policy mapping | `test_a_user_invoked_skill_turns_implicit_invocation_off`, `test_drafts_are_withheld_unless_asked_for` |
| E7 | drop the escaping | `test_hostile_characters_are_escaped_into_one_double_quoted_scalar` |
| E7 | drop the guard against writing into the kit's own sources | first run: none failed, since the only test was a dry run. A direct test was added; rerun: `test_emitting_a_skill_onto_its_own_source_writes_nothing` |
| D3 (worker) | stop skipping `git -C` and `-c` arguments | three evasion subtests |
| D3 (worker) | stop splitting on semicolon, ampersand and pipe | nine evasion subtests |
| D3 (worker) | drop the `--force-with-lease` exemption | one subtest |
| D5 (worker) | drop the "version must increase" refusal | three subtests |
| D5 (worker) | let a dry run write | two tests |

## The double-quoted phrase class, first run (R-004)

Measured before it was switched on, as `R-004` asked. 290 multi-word double-quoted phrases in Evidence cells; 52 resolved in no file their row names when matched as written, 24 once Markdown markup (backticks and asterisks) was removed on both sides. The 24 are reported as `WARN` lines and do not fail the gate. A search of the whole tree put each in one of two kinds: **attribution**, where the phrase is real but in a file the row does not name (`.agents/rules/review-quality.md` for seven `house-review` rows, `.agents/rules/autonomy.md`, a test file, a done quest), and **nowhere**, a paraphrase in quotation marks or a quote gone stale (the `zen-config` rows quoting skill bodies, `spec-author`, `verifier-agent`, `doc-sync`, `systematic-debugging`). None is in a matrix this quest owns, so none was disposed of here.

| Matrix | Row | Phrase |
|---|---|---|
| `agent-observatory.conformance.md` | `S-010`: cost reported as a dated estimate | no date recorded |
| `cloud-executable.conformance.md` | Unattended branch and pull request: `claude/` prefix, draft, | Landing: what you may do with the result |
| `doc-sync.conformance.md` | S-011 an approved correction is written | **Read `doc-revise` now and follow it** for the edit itself |
| `house-review.conformance.md` | S-008 a clean change is reported as clean | Say when it is clean |
| `house-review.conformance.md` | S-015 a quote found at a shifted line is re-anchored, not dr | The line number is deliberately not in it |
| `house-review.conformance.md` | S-019 the spec axis reports missing, unasked-for, and wrong  | Every spec finding quotes the contract line it rests on |
| `house-review.conformance.md` | S-020 with no contract, the spec axis says so and stops | the spec axis reports \ |
| `house-review.conformance.md` | S-020 with no contract, the spec axis says so and stops | it never reconstructs intent from the diff |
| `house-review.conformance.md` | S-021 the standards axis reads the repository's written stan | **The repository overrides the rubric.** |
| `house-review.conformance.md` | S-021 the standards axis reads the repository's written stan | **Cite the standard.** |
| `spec-author.conformance.md` | S-006 the spec goes where the repository already keeps specs | Find the repository's spec location before writing |
| `spec-author.conformance.md` | The interview follows `grill`, with an inline fallback | Fallback while `grill` is a draft |
| `systematic-debugging.conformance.md` | 3. A diagnosis that feeds `new-quest` directly | what a task file needs from `new-quest` and cannot otherwise obtain |
| `verifier-agent.conformance.md` | S-002 a declared command fails | record for each: the command as written, its exit status, and the excerpt of its output th |
| `zen-config.conformance.md` | S-007 a newer version fails with one named message | update .tasks/validate.py from the kit |
| `zen-config.conformance.md` | S-014 a reader without the fact discovers it and says so | Otherwise discover them, and say that you did |
| `zen-config.conformance.md` | S-016 a re-run keeps every value already present | change a key only when the person asks for it during the run |
| `zen-config.conformance.md` | S-021 a configured fact is used instead of discovered | use them and say so |
| `zen-config.conformance.md` | S-022 a reader does not rely on a block it cannot parse | use none of it, discover instead |
| `zen-config.conformance.md` | S-026 a re-run changes a key the person asks to change | change a key only when the person asks for it during the run |
| `zen-config.conformance.md` | S-031 a reader does not use a configured path that is missin | a configured path that does not exist is discovered instead too, and said |
| `zen-config.conformance.md` | S-039 a re-run over a broken file stops | when the block does not parse, write nothing and ask the person to repair it by hand |
| `zen-config.conformance.md` | Readers: a missing configured path is treated as absent | a configured path that does not exist is discovered instead too, and said |
| `zen-config.conformance.md` | D4, `domain-language` and `grill` keyed on the file, not the | A key the file does not set, or sets to a value outside its allowed set or a path that doe |

## Not verified

- **Codex and Copilot sessions.** No Codex CLI is installed here, and installing one was refused by the environment's permission check. `gh copilot` is present as a launcher and was not run, since it may download and needs an account. The Codex target's files are tested; no Codex or Copilot session has loaded them.
- **The destructive-git gate in a live Claude Code session.** Its behaviour is tested by feeding payloads to `main()`; it was not registered in any harness here, by design.
- **Windows and macOS.** Every run above is Linux, Python 3.13.

## Review fix round (2026-11-25)

An independent verifier returned `fail` on `0ef68e0`. The orchestrator relayed findings F1 to F7 and F9 (F8 was dismissed to `chore-0118`), and two maintainer decisions. Each fix was mutated in place, the named tests run, and the file restored by byte compare.

| Finding | Change | Mutation, and the tests that failed |
|---|---|---|
| F1 | `metadata.extended` restarts the 90 days; the exact case, drafted 2026-01-01 and extended `"2026-11-01: still in use"`, is silent | ignoring `extended`: `test_a_recent_extension_silences_an_old_draft`, `test_an_extension_restarts_the_ninety_days`, `test_an_extension_without_a_date_is_reported` |
| F2 | the guard line alone with no `; otherwise` warns | dropping that warning: `test_the_guard_line_alone_without_otherwise_warns`, `test_a_guard_with_no_otherwise_clause_warns` |
| F3 | the unguarded-load warning covers any case and "read `x` (now) and follow it"; the guarded form stays exempt | case-sensitive again: three subtests of `test_every_unguarded_phrasing_warns` (a first attempt did not apply and is void); second phrasing removed: two subtests of the same test |
| F4 | for a draft, the complete guarded sentence satisfies its "Composed by" claim | `test_a_guarded_load_satisfies_a_drafts_composed_by_claim` |
| F5 (worker) | the gate's lexer: per-line fallback, `bash -c --`, per-ref leases, `pwsh`/`cmd`/`env -S`/`submodule foreach`/`rebase --exec`/`find -exec`, xargs long options; limits listed in the docstring and the hooks README | line fallback: 2 tests; `--`: 2 subtests; named lease treated as bare: 5 subtests; `find`: 3; `rebase`: 3 |
| F6 | the gate's docstring no longer reads as wired anywhere; `install.py --with-hooks` prints the gate as a separate block, labelled as a gate | gate not separated: all three tests in `tests/test_install_gate_block.py` |
| F7 | a future date is invalid; a shallow clone reads "unknown (shallow clone)"; a record is any file under `docs/reviews/` with `dogfood` in its path, naming the skill as a whole word (AGENTS.md section 7, after feat-0102 landed) | future date accepted: `test_a_drafted_date_in_the_future_is_invalid`; shallow check removed: `test_a_shallow_clone_says_unknown_rather_than_dating_its_boundary`; path rule narrowed: `test_a_record_nested_deeper_under_reviews_counts` (the first fixture could not fail; rerun with a deeper one); word boundary removed: `test_a_longer_hyphenated_name_does_not_count` |
| F9 | the changelog heading is found in any case; stale exceptions are reported without it | case-sensitive: `test_the_heading_is_found_whatever_its_case`; no stale report: `test_without_the_heading_every_exception_is_reported_stale` (a first run's result did not match the mutation and is void) |
| VERSION | `VERSION` committed at `0.2.0`; `PLUGIN_BASE_VERSION` reads it | hard-coded again: `test_the_plugin_base_version_is_the_version_file` |

This checkout is a shallow clone (`git rev-parse --is-shallow-repository` prints `true`), so every draft here now dates as unknown unless it carries `metadata.drafted`; all six are named in a dogfood record, so none warns.
