---
title: install conformance
spec: docs/spec/install.md
audited: 2026-07-27
re_audited:
  - 2026-07-28 (bug-0003)
  - 2026-07-29 (bug-0009)
  - 2026-08-05 (bug-0010)
  - 2026-08-05 (feat-0036)
  - 2026-11-23 (feat-0079)
  - 2026-11-23 (chore-0033)
  - 2026-11-24 (feat-0094, partial: S-014 only)
---

# install conformance matrix

Spec-vs-implementation audit of [`scripts/install.py`](../../scripts/install.py) against
[`install.md`](install.md). Evidence is by code location; this audit is independent of test
pass/fail.

Produced by `feat-0029`, completing the kit's contract coverage: every distribution script now has an
approved contract and a matrix.

**Not re-audited after `bug-0018` amended the contract on 2026-08-07 with S-016 through S-018, Goal
10, and the `--replace-adopted` flag.** That amendment is **pending the author's re-approval**, which
is stated in the spec's header and repeated here for the reason
[`build-adapters.conformance.md`](build-adapters.conformance.md) states it: so this matrix is not
read as auditing the contract in full. When that amendment landed, the rows below covered S-001
through S-015 and the surface as it stood before it: three scenarios and one flag were unaudited, and
the coverage arithmetic was 15 of 18 scenarios. Those three scenarios, the flag, and the `Adopted
material` element the same amendment added are still unaudited, and the matrix for them is still owed
at that task's closeout. Later passes added rows for other scenarios, so the current arithmetic is in
the coverage proof below rather than here.

**One clause of S-016 was audited on 2026-08-30 by `bug-0056`, and it was found diverged.** The rest
of S-016 through S-018 remains unaudited and this is not a claim otherwise. That scenario says the
adopted and edited cases are told apart "by whether the installed file still matches the digest
recorded when it was placed, **which is the same line `--check` draws between `diverged` and
`revised`**". `--check` did not draw that line. Its adopted branch compared the recorded baseline
against the source and never opened the installed file, so it could not tell an edited lens from an
untouched one, and both answered `revised` at exit 0. The session-start currency reminder excludes
`revised` from what it reports, on the ground that firing on a file the adopter was invited to own is
crying wolf, so an untouched lens that had simply gone stale was silent in both places at once.
Measured on the author's machine that day: `autonomy.md`, carrying this kit's only rule about
material an agent did not author, sat two days behind in both installed homes with its installed
digest byte-identical to the recorded baseline.

**The contract was right and the code was wrong**, which is the direction `AGENTS.md` says a
disagreement resolves in, and the reason nothing caught it is that this clause sat inside the
unaudited range. `bug-0056` brought `--check` into line with the sentence rather than amending it.
That clause is now **conformed**: `_check_entry()` in `scripts/install.py` digests the installed tree
in the adopted branch, which it already did for `bug-0022`'s missing-file check, and splits on
whether the files the kit revised still match their baseline. Proven by
`test_a_kit_revision_to_a_lens_the_adopter_never_touched_is_reported`,
`test_a_kit_revision_to_a_lens_the_adopter_edited_stays_revised_and_exit_zero`, and
`test_the_revised_message_says_which_files_are_the_adopters_and_which_are_not`. The hook mirrors it,
proven by `test_an_untouched_lens_the_kit_revised_is_reported`,
`test_an_edited_lens_the_kit_revised_stays_silent`, and
`test_the_hook_and_install_py_give_the_same_verdict_for_the_same_state`, which asserts the two give
one answer for one entry rather than only sharing a vocabulary.

**Re-audited 2026-11-23 by `feat-0079` for the five scenarios it added, S-019 through S-023, and
the surface elements they brought.** The amendment carrying them is pending the maintainer's
approval, so these rows audit code against wording that is written and not yet approved, the same
standing `feat-0036` recorded for S-015. S-016 through S-018 remain outside this matrix as stated
above; this task did not audit them and does not claim to.

**Re-audited 2026-11-23 by `chore-0033` for the six scenarios it added, S-024 through S-029, and the
surface it amended: `--check`, `--with-hooks`, the new `Hooks module` element, and the `Record`,
`Exit code`, and `Output` rows.** That amendment is **pending the author's re-approval**, stated in the
spec's header and repeated here so these rows are not read as auditing approved wording. It moved the
contract and no code: every row below cites code that existed before the scenario did. S-016 through
S-018 were not audited by this pass either, apart from what S-027 restates of the one S-016 clause
`bug-0056` audited, and this pass does not claim them.

## Matrix

| Section | Item | Status | Evidence | Note |
|---|---|---|---|---|
| Scenarios | S-001 each requested tool receives every skill | Conformed | `install()` / the `for tool in tools` loop over `discover_skills()`, with `TOOL_SUBPATHS[tool]` | only requested tools are iterated, so an unrequested one receives nothing |
| Scenarios | S-002 the rules module lands where references resolve | Conformed | `install()` / `rules_target = base.parent / "rules"` | `base` is `<home>/<tool>/skills`, so the parent sibling is exactly what `../../rules/<file>` resolves to from an installed skill; confirmed by execution |
| Scenarios | S-003 a re-run recognises the tool's own targets | Conformed | `_place()` / the `is_managed(target, manifest)` branch returning `updated` or `relinked`, and the symlink branch comparing `points_to == src.resolve()`, over the record `install()` / `home = home.expanduser().resolve()` now writes | symlink mode recognises its own links without the manifest, as the constraint states. Re-audited by `bug-0010`, which found the recognition sound but the record it reads unreliable: `install()` recorded each target as `home` was spelled, so a caller passing a relative home wrote relative strings, and `is_managed()` compares them exactly. Measured 2026-07-29, a re-install under the absolute spelling of the same directory exited 1 with a CONFLICT per target, against the tool's own work. "The same arguments" in S-003 names a directory, not a spelling, so this was a divergence and not a contract gap; the spec is unamended |
| Scenarios | S-004 an unmanaged target is refused | Conformed | `_place()` / both `return "CONFLICT"` paths, with `install()` counting them and returning 1 while the loop continues | the loop continues past a conflict, so free targets are still placed |
| Scenarios | S-005 a lost record makes previous copies unmanaged | Conformed | `load_manifest()` returning empty entries, feeding `is_managed()` | confirmed by execution: deleting the manifest and re-running yields exit 1 with a conflict per previously-copied target |
| Scenarios | S-006 a preview run writes nothing | Conformed | `_place()` / the `if not dry` guards, and `save_manifest()` / `if dry: return` | neither targets nor the record are created |
| Scenarios | S-007 reversing removes what was placed beneath the given home | Conformed | `uninstall()` / `mine = [... if _beneath(e["target"], home)]`, the loop calling `_rm`, then `save_manifest(others, dry)` | amended and re-audited by `bug-0003`. The pre-fix code ignored `home` entirely and emptied the whole record. Re-audited by `bug-0009`, which found the scoping check honouring `home` but comparing it as spelled, so an unresolved home matched no entry and reversal removed nothing while exiting zero. "The same home" in S-007 names a directory, not a spelling, so this was a divergence and not a contract gap; the spec is unamended. Re-audited again by `bug-0010`, which found the residual case that normalisation cannot reach: a relative recorded target has no fixed meaning to normalise toward, since `Path.resolve()` reads it against the current directory of whoever reads the record. Measured 2026-07-29, reversing a relative home from a different directory classed all four entries as owned, found none of them on disk, reported each `gone`, and then emptied the record while the directories remained: created, no longer recorded, and permanently unmanaged. Fixed at the recording end, in `install()`, so `_beneath()` is unchanged |
| Scenarios | S-012 reversing one home leaves another intact | Conformed | `_beneath()` / `(t.parent.resolve() / t.name).is_relative_to(home.resolve())`, and `uninstall()` retaining `others` in the record | confirmed by execution against two throwaway homes and by a test proven to fail against the pre-fix code. Re-anchored by `bug-0009`, which replaced the bare `Path(target).is_relative_to(home)` this row previously quoted. The target's final component is deliberately left unresolved: in symlink mode every recorded target is a link back to its source in this checkout, so resolving it would place it beneath no home at all |
| Scenarios | S-008 reversing with nothing recorded is not an error | Conformed | `uninstall()` / the `if not manifest["entries"]` early return 0 | prints the nothing-recorded line |
| Scenarios | S-009 an unrecognised tool is rejected before anything is placed | Conformed | `main()` / the `bad` check returning 2 before `install()` is called | the check precedes any placement, so a valid tool in the same list does not save it |
| Scenarios | S-010 the default mode suits the platform | Conformed | `main()` / `default="copy" if os.name == "nt" else "symlink"` | |
| Scenarios | S-011 a refused link reports what to do instead | Conformed | `_link()` / the `except (OSError, NotImplementedError)` raising `SystemExit` with guidance | names Developer Mode and `--mode copy`; confirmed by execution |
| Scenarios | S-013 a profile places a closed subset and reports expansion | Conformed | `resolve_profile()` / the closure loop over `sibling_refs()`, `install()` / the expansion notice, and `main()` / the `profile not in PROFILE_SEEDS` check returning 2 | the closure is computed from each body's `../<name>/SKILL.md` references rather than listed, so a skill that gains a reference cannot leave a profile shipping a dangling one. Confirmed by execution, measured 2026-07-28: `core` resolves to 3 with no expansion, `spine` to 17 having added 4 (`doc-author`, `doc-revise`, `spec-quality`, `test-quality`), `all` to 19, and every profile has zero references to a skill it does not place. An unrecognised profile exits 2 before placement, matching S-009's shape. Dated for the same reason as S-014 below: the totals move whenever a skill is added, and an undated count reads as a claim about now rather than as the record it is. **Re-measured 2026-08-05 (`feat-0036`)**: `core` resolves to 3 with no expansion, `spine` to 18 having added 5 (`doc-author`, `doc-revise`, `review-depth`, `spec-quality`, `test-quality`), `all` to 20. The 2026-07-28 figures above are kept rather than overwritten, because they are the record of what was true then. The movement is `feat-0035` blessing `review-depth`, not `feat-0036`: `house-review` is a `spine` seed and references `review-depth`, so the closure now pulls it in, and the same figures resolve identically against the pre-`feat-0036` `install.py`, measured by running it. Closure itself is unchanged; it now runs over the shipped set (S-015) rather than over everything discovered |
| Scenarios | S-014 the run reports its description budget | Conformed | `profile_budgets()`, `description_of()`, and `install()` / the `Description budget:` print | reports the installed profile's total and every profile's, as counts. Confirmed by execution, re-measured 2026-07-29 with `--dry-run --home ./.tmp/zen-home`: `core=2298`, `spine=12489`, `all=14273`. Dated because the total moves whenever a `description` is edited: `all` was `14262` when first recorded, and the edits in `bug-0007`, `bug-0008`, and `chore-0022` moved it. `description_of()` strips a block-scalar indicator, without which the four skills using one would each inflate the figure by three. **Re-measured 2026-08-05 (`feat-0036`)** with the same command: `core=2298`, `spine=13398`, `all=15182`. The 2026-07-29 figures above are kept as the record of that date rather than overwritten. `core` is unmoved; `spine` and `all` moved because `feat-0035` blessed `review-depth`, adding a twentieth description and pulling it into `spine` through `house-review`. The identical figures resolve against the pre-`feat-0036` `install.py`, measured by running it, so none of this movement is this task's. What `feat-0036` does change is the input: the budget is now computed over the shipped set, so a draft's description is excluded from every profile's total, since no run can incur it **Re-audited 2026-11-24 (`feat-0094`)** against the amended scenario: `model_invoked_budget()` feeds `profile_budgets()` and the selection branch, so the headline and every per-profile figure exclude a skill `is_user_invoked()` reports, and the aside line names the user-invoked share. The closing `init-worktracking` pointer is printed by `install()` only, so `check()` and `uninstall()` never reach it. Measured with `--dry-run --home ./.tmp/x` on 2026-11-24: `core=1610`, `spine=7200`, `all=7941`, against `spine=7947` and `all=9527` before the change, the difference being the 747 and 1,586 characters of user-invoked descriptions. Covered by `BudgetHeadlineTests` and `SetupPointerTests` in `tests/test_install.py`, both written first and run red against the pre-change `install.py` |
| Scenarios | S-015 a skill marked a draft is placed by no profile | Conformed | `status_of()`, `partition_drafts()`, and `install()` / `shipped, drafts = partition_drafts(all_skills)` feeding `resolve_profile(profile, shipped)`, the held-back notice, `profile_budgets(shipped)`, and `draft_conflicts()` returning 2 before anything is placed | added by `feat-0036`. The partition runs *before* the profile is resolved, so the S-013 closure computes over the shipped set rather than around it. Absence of a marker means shipped, and so does any unrecognised value, so a typo over-delivers (the visible defect) rather than silently withholding a skill (the invisible one). `status_of()` reads only the frontmatter's `metadata:` block, never the body, because `validate-skills.py`'s `DRAFT_STATUS_RE` matches `status: draft` anywhere in a file and several skills discuss draft status in prose. The summary's denominator stays `len(all_skills)`, so a held-back draft is reported as discovered but not placed. Confirmed by execution against a fixture tree, and against the real tree, which has no draft today and still reports `20 of 20`. The marker is carried by the skill and not by a list here, per the constraint the amendment added |
| Proposed Surface | Invocation and its six flags | Conformed | `main()` / the `argparse` definitions | `--tools`, `--profile`, `--mode`, `--home`, `--dry-run`, `--uninstall` |
| Proposed Surface | Draft marker | Conformed | `metadata_fields`, `DRAFT_STATUS`, and `status_of()` | added by `feat-0036`; since `feat-0079` the reader is `metadata_fields` in `scripts/_skillmeta.py`, shared with `build-adapters.py` and `validate-skills.py`, and `status_of()` delegates to it with the same unrecognised-reads-as-shipped rule. The nested block form (`metadata:` then an indented `status:`) is the only legal spelling and the reason is external, not preference: `ALLOWED_FRONTMATTER_KEYS` in `validate-skills.py` rejects a bare top-level `status:`, and its `check_frontmatter_is_parseable` rejects the flow form `metadata: {status: draft}`. Both were confirmed by running that validator against fixture skills |
| Scenarios | S-019 an existing rules directory is merged into, file by file | Conformed | `install()` / the `merging` test, `_place_merged()`, `uninstall()` / the `"merged"` branch calling `_unmerge()`, and `_check_entry()` / the `"merged"` filter on `current` | added by `feat-0079`. A clashing file counts toward the run's conflicts and is named per file; an identical one is kept and not recorded; an entry is recorded only when something was placed. Covered by `RulesDirectoryMergeTests`, eight tests, each confirmed to fail with the merge disabled |
| Scenarios | S-020 a same-named symlink pointing elsewhere is a conflict | Conformed | `_place()` / the symlink branch calling `_recorded_link()` | added by `feat-0079`. Relinking requires both the record naming the target and the link resolving to the recorded source. Covered by `ForeignSymlinkTests`, which runs only where symlinks can be made |
| Scenarios | S-021 drafts are placed when asked for, and named | Conformed | `select_skills()` / the `include_drafts` branches, and `install()` / the `placed_drafts` notice and the `(draft)` mark on each line | added by `feat-0079`. Covered by `IncludeDraftsTests`, including a dry run of the real tree that asserts every draft the frontmatter marks is listed |
| Scenarios | S-022 a named set of skills is placed with its closure | Conformed | `select_skills()` / the `only` branch over `closure()`, and `main()` / the `--skills` parsing refusing a combined `--profile` | added by `feat-0079`. Covered by `NamedSkillsTests` |
| Scenarios | S-023 a user-invoked skill reaches Claude Code rendered | Conformed | `renders_for()`, `rendered_skill_md()`, `expected_digests()`, `install()` / `placed_mode = "copy" if render else mode`, and `_check_entry()` / the rendered-copy branches | added by `feat-0079`. Covered by `InvocationRenderingTests` over every combination of `status` and `invocation` |
| Scenarios | S-024 `--check` reports a current install as current, and writes nothing | Conformed | `check()` / `scoped = [e for e in manifest["entries"] if _beneath(e["target"], home)]` and the closing `return 1 if counts["diverged"] else 0`; `_check_entry()` / the `if target.is_symlink():` branch returning `linked`, and the derived branch returning `ok` when `_compare()` finds nothing | added by `chore-0033`. `check()` calls no writer at all, neither `save_manifest()` nor a file write, which is what makes "writes nothing" hold in every branch rather than in the tested ones. Confirmed by execution 2026-11-23: a fresh copy install of `core` for `claude` reported four `ok` lines at exit 0, a symlink install reported two `linked` lines at exit 0, and the record's SHA-256 was identical before and after a check |
| Scenarios | S-025 a derived target that no longer matches is named with both digests, at exit 1 | Conformed | `_check_entry()` / `problems = _compare(digest_tree(target), current)` returning `diverged` with `DIVERGED from the source`, the `if not (target.exists() or target.is_symlink()):` branch for a removed target, and the rendered-copy line `current["SKILL.md"] = hashlib.sha256(rendered_skill_md(source)).hexdigest()`; `_compare()` / `{left_label} {found[:12]}, {right_label} {digest[:12]}` | added by `chore-0033`. The hooks entry is not in `ADOPTED_ENTRY_NAMES`, so it takes this derived path, which is why S-025 names it beside a skill. Confirmed by execution 2026-11-23: appending a line to an installed `pr-describe/SKILL.md` reported `SKILL.md: installed cff607eae73c, source f87ad20bb5a2` at exit 1, with the other three entries `ok` |
| Scenarios | S-026 a check that cannot answer says so at exit 2, outranking a divergence | Conformed | `_check_entry()` / the `if not recorded:` branch, whose message differs by `ADOPTED_ENTRY_NAMES`, and the `if not source.is_dir():` branch returning `error`; `check()` / the `if not scoped:` early `return 2` and `if counts["error"] or counts["unknown"]:` tested before the diverged count; `_main()` / `if args.check and args.uninstall:` | added by `chore-0033`. Confirmed by execution 2026-11-23: stripping every entry's digests reported four `unknown` lines, the rules line naming `--replace-adopted`, at exit 2; pointing one entry's `source` at a missing directory reported `error` at exit 2; a home with nothing recorded printed "nothing can be checked" at exit 2; `--check --uninstall` exited 2 and left all three installed skills on disk. The nothing-recorded case is exit 2 and not 0 on purpose, per the comment on that branch |
| Scenarios | S-027 `--check` faults an adopted file only when the kit moved and the file is untouched | Conformed | `_check_entry()` / the `if entry.get("name") in ADOPTED_ENTRY_NAMES:` branch: `moved = _compare(recorded, current, "recorded", "source now")`, the `missing` list returning `diverged`, `if not moved:` returning `ok`, then `changed`, `theirs`, and `if changed and not theirs:` returning `diverged`, with `revised` otherwise; `check()` counting `revised` toward neither non-zero exit | added by `chore-0033`, and it agrees with `build-adapters.md` `S-010` and `S-014` and with the S-016 clause `bug-0056` audited, which is the same code. The task's implementation notes, written 2026-08-06, said the kit's copy moving under an adopted file is reported exit-neutrally in every case; `bug-0056` narrowed that on 2026-08-30 to the case where the file is the adopter's, and the scenario states the code as it now is. Confirmed by execution 2026-11-23, staging the kit's move by rewriting the recorded baseline rather than editing `.agents/rules/`: an edited lens with the kit unmoved was `ok` at exit 0; edited with the baseline differing from both was `revised` at exit 0; untouched with the baseline equal to the installed file and the source differing was `diverged` at exit 1 |
| Scenarios | S-028 `--with-hooks` places the hooks module and activates nothing | Conformed | `install()` / `hooks = discover_hooks() if with_hooks else []`, the `if with_hooks and hooks and tool in HOOK_SUBPATHS:` block placing through `_place()` and recording `"name": "hooks"` with `digest_tree(HOOKS_DIR)`, and the `for placed_tool, placed_target in placed_hooks:` loop printing `claude_registration()` or `opencode_activation_note()`; `HOOK_SUBPATHS` | added by `chore-0033`. Nothing in `scripts/install.py` writes a settings file: its only writes are the record, the rendered `SKILL.md`, and the placement helpers. Confirmed by execution 2026-11-23 against a home holding a `.claude/settings.json`: both tools received the module, the run printed the `INACTIVE` note with the registration block for Claude Code and the `INERT` note for OpenCode, the settings file's SHA-256 was unchanged, and a following `--check` reported both hooks entries `ok` |
| Scenarios | S-029 a record that parses but is the wrong shape stops every command at exit 2 | Conformed | `load_manifest()` / `_validate_manifest(data)` after `json.loads`, with `except json.JSONDecodeError:` returning an empty record; `_validate_manifest()` and `_OPTIONAL_ENTRY_TYPES`; `report_unreadable_manifest()`; `install()`, `uninstall()`, and `check()` each catching `ManifestError` from `load_manifest()` and returning its result | added by `chore-0033`, carrying `bug-0024`'s behaviour into the contract. In `install()` the record is loaded before the placement loop and before any `mkdir`, so a refusal leaves no directory behind. Confirmed by execution 2026-11-23 with an entry lacking `target`: `--check`, a real `--uninstall`, a real install, and a real install with `--with-hooks` each exited 2 naming `entry 1 ('house-review')`, the record's SHA-256 was unchanged after all four, the fresh home was never created, and the home under `--uninstall` kept its three skills. A `digests` given as a list also exited 2; bytes that do not parse gave `Nothing recorded as installed.` at exit 0 under `--uninstall` |
| Scenarios | S-030 a renamed skill's old name is an alias | Conformed | `RENAMED_SKILLS`; `_main()` maps `--skills` names through it and warns, naming `ALIAS_EXPIRY` and the new spelling (`feat-0103`, `test_the_old_name_warns_that_the_alias_expires`, which fails with the expiry removed); `install()` / the `for old, new in RENAMED_SKILLS.items()` loop removes only a target the record names | `RenamedSkillTests` in `tests/test_install.py`: the old name places the new skill; a recorded copy and a recorded symlink are retired and leave the record; a run that does not place `new-quest` keeps an edited `new-task` and its record (`test_a_run_that_does_not_place_the_successor_keeps_the_old_placement`, `placed_here` in `install()`); the shipped table itself, unpatched, maps `new-task` to an existing skill and a real-kit `--skills new-task --dry-run` places `new-quest` (`RealRenameTableTests`; emptying the table fails both); an unrecorded directory is left alone; `--check` names the rename (`check()`'s missing-source branch, `test_check_names_the_rename_for_a_placement_under_the_old_name`). Removing the retire loop fails two of these tests (mutation run 2026-11-25). **Added 2026-11-25 by the implementer (`feat-0101`), not re-audited** |
| Proposed Surface | `--skills`, `--include-drafts`, Invocation marker, Merged rules module | Conformed | `_main()` / the two `add_argument` calls, `is_user_invoked()`, and `_place_merged()` | added by `feat-0079` |
| Proposed Surface | `--check` and `--with-hooks`, and the Invocation synopsis naming them | Conformed | `_main()` / the `--check` and `--with-hooks` `add_argument` calls, `if args.check:` dispatching to `check()`, and `args.with_hooks` passed to `install()` | added by `chore-0033`. The synopsis writes `[--uninstall \| --check]` because `_main()` refuses the pair, per S-026 |
| Proposed Surface | Hooks module | Conformed | `HOOK_SUBPATHS` and `install()` / the hooks block recording `"name": "hooks"` | added by `chore-0033`. Placed through `_place()`, not `_place_adopted()`, so it is derived; `ADOPTED_ENTRY_NAMES` holds only `rules`, so `--check` compares it as derived too |
| Proposed Surface | Placed per tool | Conformed | `install()` / the per-skill `_place` and the rules placement | |
| Proposed Surface | Record | Conformed | `load_manifest()`, `save_manifest()`, `is_managed()`, and `install()` / `home = home.expanduser().resolve()` | the row says "a manifest of the targets this tool created" without constraining how a target is spelled, which is why `bug-0010`'s relative entries were a divergence from S-003 and S-007 rather than from this row. Every recorded target is now absolute, asserted directly by a test. **Re-audited 2026-11-23 by `chore-0033`**, which amended the row to describe the per-file digest map and the two ways a damaged record is read. The map is `digest_tree()`, keyed by `rel.as_posix()` over bytes, written into every entry by `install()` as `"digests": expected_digests(src, tool)` for a skill and `digest_tree(...)` for the rules and hooks modules; the shape rules are `_validate_manifest()`, per S-029 |
| Proposed Surface | Exit code | Conformed | `main()` / `return 2`, and `install()` / the `if problems` block returning 2 and `return 1 if conflicts else 0` | re-audited by `feat-0036`, which amended the row to add the draft collision. It exits 2, the same class as an unrecognised tool or profile, and returns before the placement loop, so nothing is placed. **Re-audited 2026-11-23 by `chore-0033`**, which amended the row with the damaged-record exit and `--check`'s three exits. Those are `report_unreadable_manifest()` returning 2 in all three commands, and `check()` returning 2 for nothing recorded, then 2 for any `unknown` or `error` before 1 for any `diverged`, with `_main()` returning 2 for `--check` combined with `--uninstall`; each was confirmed by execution, as recorded in the S-024 to S-029 rows |
| Proposed Surface | Output | Conformed | `install()` / the per-target print, the conflict summary, the drafts-held-back notice, and the closing count | re-audited by `feat-0036`, which amended the row to add the held-back drafts. The notice names each withheld skill, because a skill silently absent from an install is the failure the whole draft axis introduces the risk of. **Re-audited 2026-11-23 by `chore-0033`**, which amended the row with the hooks activation notes and `--check`'s report: `install()` / the `placed_hooks` loop prints one note per tool that received the module, and `check()` prints one line per scoped entry, the counts line, and a remedy line for `diverged`, `revised`, and `unknown` when each is present |

## Coverage proof

- **audited**: all 15 scenarios the spec defines, S-001 through S-015 with no gap in the ids, matched
  one for one by the 15 `Scenarios` rows above; and all 12 elements of its Proposed Surface table,
  covered by 6 `Proposed Surface` rows. The two element figures differ for one reason, and it is worth
  naming so a reader can check the matrix without reconstructing the grouping: the row
  `Invocation and its six flags` is compound, auditing the `Invocation` element together with the six
  flag elements (`--tools`, `--profile`, `--mode`, `--home`, `--dry-run`, `--uninstall`), which is 7 of
  the 12. The other 5 elements (`Placed per tool`, `Draft marker`, `Record`, `Exit code`, `Output`)
  have a row each, so 7 + 5 = 12 and nothing is unaudited. Counted 2026-08-05 against both files;
  `feat-0036` added the `Draft marker` element and re-audited `Exit code` and `Output`.
- **unreconciled**: none. No item diverged and none is unbuilt.
- **caveat on S-015's audit standing**: the scenario is new as of 2026-08-05 and the spec amendment
  carrying it is awaiting the author's re-read, so this row audits code against a contract clause that
  is written but not yet re-approved. Recorded rather than deferred, because leaving the matrix
  claiming "S-001 through S-014, every spec item was checked" beside a spec that carries fifteen would
  be the falser of the two states.
- **audited, recounted 2026-11-23 (`chore-0033`)**: the two bullets above are the 2026-08-05 count
  and are kept as the record of that date. `feat-0079`'s re-audit added five scenario rows and one
  compound surface row without recounting here, so this is the first recount since, made by counting
  the spec's `### Scenario` headings and Proposed Surface rows and this matrix's rows on that date.
  - **Scenarios: 26 of 29.** The spec defines S-001 to S-029 with no gap in the ids. Audited, one
    `Scenarios` row each: S-001 to S-015 (15), S-019 to S-023 (5, `feat-0079`), and S-024 to S-029
    (6, this pass), so 15 + 5 + 6 = 26. Unaudited: S-016, S-017, and S-018 (3, from `bug-0018`), so
    26 + 3 = 29. The one S-016 clause `bug-0056` audited is recorded in the header prose and not as a
    row, and it does not make S-016 audited.
  - **Proposed Surface: 19 of 21 elements, in 9 rows.** `Invocation and its six flags` covers 7;
    the `--skills`, `--include-drafts`, Invocation marker, Merged rules module row covers 4; the
    `--check` and `--with-hooks` row covers 2; `Draft marker`, `Hooks module`, `Placed per tool`,
    `Record`, `Exit code`, and `Output` cover 1 each, 6. So 7 + 4 + 2 + 6 = 19. Unaudited:
    `--replace-adopted` and `Adopted material` (2, both from `bug-0018`), so 19 + 2 = 21.
  - **Unreconciled: none.** No audited item diverged and none is unbuilt. The unaudited five (three
    scenarios, two elements) are unaudited, not unreconciled, and this is not a claim about them.
- **caveat on S-024 to S-029's audit standing**: the same as S-015's above. The amendment carrying
  them is pending the author's re-approval, so these rows audit code against wording that is written
  and not yet re-approved. Unlike S-015 the code preceded the wording by months here, so a clean row
  says mainly that the wording describes the code, which is the direction `chore-0033` was asked to
  close.

## Test coverage of spec invariants

Against [`tests/test_install.py`](../../tests/test_install.py), promoted from a characterization suite
to an acceptance suite by this task:

| Scenario | Covering test | Note |
|---|---|---|
| S-001 through S-008 | present | one each, plus a supporting test for how the skill set is identified |
| S-012 | present | added by `bug-0003`. Two tests: one installs to two homes and asserts reversing one leaves the other on disk and in the record, one asserts reversing an uninstalled home removes nothing. Both were run against the pre-fix `uninstall()` and failed |
| S-007 | strengthened | `bug-0009` added two. `test_uninstall_honours_a_home_the_caller_has_not_resolved` installs to a resolved home and reverses it under two spellings `main()` would never produce, a relative one and one carrying `..`; both subtests were run against the pre-fix `_beneath()` and failed. `test_uninstall_in_symlink_mode_removes_the_links_it_placed` covers the POSIX default mode, which had no test at all; it is a guard rather than a regression proof, since it passes on both sides of the fix and exists to fail against the plausible wrong one (resolving a recorded target through its own link). It is skipped where the platform or account cannot create a symlink, probed rather than inferred from `os.name`. `bug-0010` added `test_a_relative_home_is_reversible_and_never_orphans_its_targets`, which installs with a relative home and reverses from a different working directory under two spellings, because no single one can fail against the pre-fix code in both of its ways: naming the installed directory from elsewhere matched no relative entry at all, while repeating the install's own spelling from elsewhere claimed every entry, found none on disk, and dropped them from the record. Both subtests were run against the pre-fix `install()` and failed |
| S-003 | strengthened | `bug-0010` added `test_a_second_run_recognises_what_a_relative_home_placed`, which installs with a relative home and re-installs under the absolute spelling of the same directory, plus the supporting `test_every_recorded_target_is_absolute`, which asserts the property both consequences follow from rather than only the two symptoms. Every other re-run test passes one already-absolute home to both runs, so the spellings agree by construction and the exact-string comparison succeeds by accident. Both new tests were run against the pre-fix `install()` and failed |
| S-011 | present | added here; asserts the message names both ways out, not merely that it raises |
| S-005 | present | added here; the surprising-but-correct case, which is why it is worth pinning |
| S-009 | present | added by `chore-0017`. Pairs a supported tool with an unsupported one, so it also proves the valid entry does not rescue the invocation, and asserts nothing was placed |
| S-010 | present, one branch | added by `chore-0017`. See the note below |
| S-013 | present | added by `feat-0033`. Five tests: closure holds for every profile (the load-bearing one, since a subset shipping a skill without its composed sibling fails silently), the default places fewer than all, the three profiles are strictly nested, an expanded seed is reported, and a closed seed is not reported as expanded. Plus a rejection test asserting exit 2 and that nothing was placed |
| S-015 | present | added by `feat-0036`. Nine tests in `DraftMarkerTests`, run against a fixture skill tree rather than `.agents/skills/`, because no skill there carries a marker (`review-depth`, the draft this was filed on, was blessed by `feat-0035`) and marking one to make a test pass would regress that. Every placement oracle compares the placed set **by name** against a literal expected set, not by count, because the bug population is the inverse of the defect being fixed: a marker read too eagerly withholds a shipped skill and an adopter's next re-install simply stops refreshing it, with no error anywhere. Coverage: the draft is placed by no profile including `all`; an unmarked and an explicitly-shipped skill are both placed; a `status: draft` line in the body is not a marker; `status_of` reads each form, including the deliberate typo and case cases; closure still holds with a draft present, asserted against what landed on disk; a placed skill referencing a draft places nothing and exits 2; a seed naming a draft does the same; the run names what it withheld; a draft costs no profile any budget. Eight of the nine were run against the pre-`feat-0036` `install.py` and failed; the closure guard passes on both sides by design |
| S-014 | present | added by `feat-0033`. Three tests: the summary carries the installed profile's total and every profile's, a smaller profile costs strictly fewer characters, and a block-scalar description is measured without its indicator. **Extended 2026-11-24 (`feat-0094`)** for the amended clauses: `BudgetHeadlineTests` (four tests, hand-counted oracles: the headline and every profile figure exclude a user-invoked skill, which the aside names), and `SetupPointerTests` with `SetupPointerSelectionTests` (the pointer on an install and a dry run, never on `--check` or `--uninstall`, and the variant wording when `init-worktracking` is not placed), each written red first |
| S-024 | present | recorded by `chore-0033`; every test named in this row and the five below predates its scenario and none carries the `S-NNN` id yet, which is owed in `tests/test_install.py`. In `StalenessCheckTests`: `test_a_freshly_installed_tree_reports_current_and_exits_zero`, `test_a_symlinked_target_cannot_be_stale_and_is_not_reported` (skipped where symlinks cannot be made), `test_the_check_never_rewrites_the_install_or_the_record`, `test_the_check_is_scoped_to_the_home_it_is_given`, and `test_the_check_is_reachable_from_the_command_line` |
| S-025 | present | `test_a_skill_revised_in_the_kit_after_the_install_is_named_and_exits_non_zero`, `test_a_stale_supporting_file_is_reported_when_the_skill_md_still_matches`, `test_an_installed_target_removed_by_hand_is_reported_rather_than_passing`, and `test_the_derived_path_still_says_installed` for the two digests; the rendered clause by `test_check_is_clean_after_a_rendered_install_and_names_a_stale_copy`. No test diverges a hooks entry; it takes the same derived branch as a skill |
| S-026 | present, one clause by execution only | `test_a_manifest_written_before_this_change_reports_unknown_not_current`, `test_an_unrecorded_rules_entry_names_replace_adopted_rather_than_re_install`, `test_an_unrecorded_derived_entry_still_says_re_install`, `test_the_run_summary_names_both_remedies_when_the_unknown_entries_are_a_mix`, `test_an_empty_digest_map_is_no_baseline_at_all`, `test_an_unanswerable_entry_still_outranks_a_missing_lens`, `test_checking_a_home_with_nothing_recorded_does_not_report_it_as_current`, and `test_asking_to_check_and_uninstall_at_once_is_refused_and_removes_nothing`. `test_an_unreadable_file_is_an_error_verdict_not_a_traceback` covers an `error` verdict for an unreadable copy; no test covers a source that no longer exists in the kit, which was confirmed only by execution |
| S-027 | present | `test_an_adopter_edited_rules_file_is_not_reported_as_divergence`, `test_a_kit_revision_to_a_lens_the_adopter_never_touched_is_reported`, `test_a_kit_revision_to_a_lens_the_adopter_edited_stays_revised_and_exit_zero`, `test_the_revised_message_says_which_files_are_the_adopters_and_which_are_not`, `test_a_rules_file_deleted_from_the_install_is_named_and_exits_non_zero`, `test_only_the_missing_lens_is_named_and_an_edited_one_is_not`, `test_a_rules_file_the_adopter_added_is_ignored_by_the_check`, `test_a_missing_lens_and_a_moved_source_are_reported_in_one_entry`, and `test_the_adopted_path_names_the_record_not_the_install` |
| S-028 | present, the load-bearing clause by execution only | In `HookPlacementTests`: `test_the_module_lands_under_each_tools_own_hook_path`, `test_the_placement_is_recorded_with_a_digest_for_every_file_in_the_module`, `test_the_module_is_recorded_under_one_name_rather_than_per_file`, `test_without_the_flag_nothing_is_placed_and_nothing_is_recorded`, `test_a_dry_run_places_no_hooks_and_records_none`, `test_a_second_run_updates_the_hooks_rather_than_conflicting`, `test_uninstall_reverses_the_placement_and_drops_the_record`, `test_a_claude_placement_still_prints_the_registration_block`, `test_hooks_placed_for_opencode_alone_are_announced_and_named_inert`, `test_an_opencode_placement_a_plugin_would_read_is_reported_live`, and `test_every_tool_that_receives_the_module_is_told_about_it`. No test asserts that a settings file already in the home is left unchanged, which is the "activates nothing" half; it was confirmed only by execution. That class's docstring still says the spec says nothing about hooks, which stopped being true with this amendment |
| S-029 | present, two cases by execution only | In `MalformedManifestTests`: `test_every_malformed_shape_is_could_not_run_rather_than_diverged`, over `--check`, a previewed `--uninstall`, and a previewed install; `test_the_report_names_the_manifest_and_the_offending_entry`; `test_a_wrong_top_level_shape_says_what_the_file_is_instead`; `test_a_named_entry_is_reported_by_its_name_as_well_as_its_index`; `test_an_unknown_extra_key_is_still_a_valid_record`; and `test_corrupt_bytes_still_degrade_to_an_empty_record`. In `MalformedManifestInstallChoiceTests`, `test_a_real_install_places_nothing_and_leaves_the_record_alone`, the only test asserting the record byte-identical. No test runs a real `--uninstall` over a damaged record or uses a wrong-typed optional field; both were confirmed only by execution |

Every scenario now has a covering test. `chore-0017` gave `main()` the optional `argv` parameter that
`validate-skills.py` (`chore-0003`) and `build-adapters.py` (`feat-0026`) already had, which is what
made the CLI layer reachable at all. Both new tests were confirmed to fail against the pre-fix
`main()`.

**One pre-existing test was changed by `feat-0033`, and it is worth saying which and why.**
`test_install_places_every_skill_and_the_rules_module` asserted that a default run places all nineteen
skills. Once the default profile became `spine`, that assertion failed, correctly: the default no
longer places all of them. The test now requests `--profile all` explicitly, so it still asserts what
S-001 means (every skill in the requested set) rather than being weakened to match the new default.
The suite's other pre-existing scenarios were left asserting over the whole set for the same reason.

**One pre-existing test was changed by `feat-0036`, for the same class of reason.**
`test_install_places_every_skill_and_the_rules_module` asserted that a `--profile all` run places every
directory `discover_skills()` returns. S-015 narrows S-001's "every skill" to every *shipped* skill, so
the expected set is now derived from the frontmatter by `_marked_draft`, a second reader local to the
test file. That derivation is deliberately not `partition_drafts()`: building the expectation from the
code under test would let a misclassifying partition move the expectation and the placed set together,
leaving the test green through exactly the failure S-015 exists to catch. The two sets are identical
today, since no skill carries a marker, so the change asserts the same thing it always did while
staying correct the day one does.

**S-010 is covered on one branch only, and the reason is worth recording.** The rule reads `os.name`,
and faking that to exercise the other platform breaks `pathlib`, which selects `PosixPath` or
`WindowsPath` from the same attribute and raises on instantiation. The test therefore derives its
expectation from the running platform and asserts the wiring, so it fails if the default changes or
the flag stops feeding it, but the opposite platform's branch is exercised only by running the suite
there. A test that hardcoded `"copy"` would have passed everywhere and meant nothing off Windows,
which is the outcome this avoids. Closing the remaining half would mean extracting the default into
its own expression, a behaviour-preserving refactor deliberately left out of `chore-0017`'s scope.

## Observations

**S-001 presupposes a definition it does not state.** It says every skill is placed, without saying
what makes a directory a skill. The implementation answers "one holding a `SKILL.md`", which matches
`AGENTS.md` and is what `validate-skills.md` builds on, so nothing diverges. But a reader of this
contract alone cannot derive the rule, and the supporting test asserts it. Left as an observation
rather than a scenario, because the definition genuinely belongs to `AGENTS.md` and duplicating it
here would create a second place for it to drift.

**S-005 is the scenario most worth having written down.** That deleting the record turns the tool's
own past work into conflicts is surprising, looks like a bug, and is correct: a copied directory
carries nothing distinguishing it from a user's own, so the alternative is overwriting something the
tool cannot prove it created. The module docstring warned about it, the code implements it, and until
now no contract said it was intended. That is exactly the class of behavior a future editor would
"fix".

**Every audited item conforms, and the same caveat applies as to `build-adapters`.** This spec was
written by reading the implementation it audits, so a clean matrix largely confirms that two
documents agree. What makes this one stronger than a pure paper exercise is that the behavior was
pinned by tests **before** the contract was written, so the spec had to describe something already
fixed rather than something it could quietly reshape.
