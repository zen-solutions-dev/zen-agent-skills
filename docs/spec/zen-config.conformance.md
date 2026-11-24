---
title: zen-config conformance
spec: docs/spec/zen-config.md
audited: 2026-11-24
---

# zen-config conformance matrix

Spec-vs-implementation audit of the per-repository setup file `docs/agents/zen.md`, against
[`zen-config.md`](zen-config.md). **The spec is a draft (`status: draft`), pending the maintainer's
approval in the Marjana pull request, and this audit is against the draft text as it stood at
commit `5d3dc41`.** A row marked Conformed here says the implementation matches that draft; if the
approval changes the text, the rows it touches need re-auditing. Evidence is by function, constant,
test name, or quoted skill-body clause, never by line number; this audit is independent of test
pass/fail, and was run by a fresh-context agent that wrote none of the code.

The contract spans two kinds of surface, as
[`tracker-links.conformance.md`](tracker-links.conformance.md) does:

- **Code.** The check in [`.tasks/validate.py`](../../.tasks/validate.py) and its shipped copy
  [`.agents/skills/init-worktracking/templates/validate.py`](../../.agents/skills/init-worktracking/templates/validate.py):
  `parse_zen_config()`, `_exact_path()`, `zen_config_findings()`, the `ZEN_*` constants, and the
  task `mode` check in `main()`. The three functions are byte-identical between the two copies, and
  so are the constants apart from comments (compared on 2026-11-24), so every code row holds for
  both. Tests: [`tests/test_zen_config.py`](../../tests/test_zen_config.py), 43 passing on
  Linux with Python 3.13; `python3 .tasks/validate.py` and `--strict` both exit 0 over this
  repository, its own `docs/agents/zen.md` included.
- **Skill prose.** Step 6 of [`init-worktracking`](../../.agents/skills/init-worktracking/SKILL.md),
  its templates [`zen.md.tmpl`](../../.agents/skills/init-worktracking/templates/zen.md.tmpl),
  [`agent-skills.md.tmpl`](../../.agents/skills/init-worktracking/templates/agent-skills.md.tmpl)
  and [`_TEMPLATE.md.tmpl`](../../.agents/skills/init-worktracking/templates/_TEMPLATE.md.tmpl); the
  readers [`domain-language`](../../.agents/skills/domain-language/SKILL.md),
  [`grill`](../../.agents/skills/grill/SKILL.md),
  [`spec-author`](../../.agents/skills/spec-author/SKILL.md) and
  [`new-task`](../../.agents/skills/new-task/SKILL.md); this repository's
  [`.tasks/_TEMPLATE.md`](../../.tasks/_TEMPLATE.md); and, for the non-goals,
  [`zen`](../../.agents/skills/zen/SKILL.md). A prose clause can be audited for presence and
  correctness but not executed, so its evidence is the clause, plus a run where one exists.
- **The first real run**: [`docs/agents/zen.md`](../agents/zen.md) and this repository's
  [`AGENTS.md`](../../AGENTS.md).

Edge cases the tests do not cover were probed by a throwaway script driving both validator copies
against temporary repositories; where a row relies on a probe, its Note says so.

**Two runs of the configure step exist, and neither is verified here.** Both are reported by the
implementer and are recorded as reported, not proven: (a) on this repository, run with no person
present, values written as recommended and the contested ones routed to the maintainer; (b) on a
scratch repository outside this checkout, an agent standing in for the person ran
`project-bootstrap`, `init-worktracking` (lite) and the configure step with `tracker: github` and an
unreadable label list, and printed five label commands in a double-quoted form the spec has since
replaced with single quotes. Run (a) is partly checkable, from the file it left behind; run (b) is
not checkable from this checkout at all.

## Matrix

| Section | Item | Status | Evidence | Note |
|---|---|---|---|---|
| Scenarios | S-001 a well-formed configuration passes | Conformed | `zen_config_findings()` returns `[]`; `main()` turns each finding into `err(ZEN_CONFIG_PATH, msg)` and nothing else | `test_s001_a_well_formed_configuration_passes`, both copies. Also the real file: `docs/agents/zen.md` validates clean |
| Scenarios | S-002 no file is not an error | Conformed | `zen_config_findings()` / `if not path.is_file():` returning `[]` | `test_s002_no_file_is_not_an_error` asserts exit 0 and no "zen" in the output |
| Scenarios | S-003 an unknown key fails | Conformed | `zen_config_findings()` / "unknown key" over the set difference with `ZEN_KEYS`; `ZEN_ROLES` lists the five roles | `test_s003_an_unknown_key_fails`, `test_s003_an_unknown_role_fails`. The other-letter-case half (`Tracker: tasks`) has no test; a probe reported `unknown key 'Tracker'` |
| Scenarios | S-004 a path that does not exist fails | Conformed | `_exact_path()` compares each part against a directory listing; `zen_config_findings()` / "letter case included", "is not a directory", "is not a file" | Five tests, including `test_s004_a_path_differing_only_in_letter_case_fails_on_every_system`. Case-insensitive filesystems are covered by construction, not by a run: CI's Windows and macOS cells were not observed |
| Scenarios | S-005 `none` is a valid path value | Conformed | `zen_config_findings()` / `if value == "none":` before the path checks | `test_s005_none_is_a_valid_path_value` |
| Scenarios | S-006 a missing version fails | Conformed | `zen_config_findings()` / `config_version is required`; `test_s006_a_missing_version_fails`, `test_s006_a_block_of_only_malformed_lines_still_asks_for_a_version` | **Re-derived 2026-11-24 by the implementer, not the auditor**, after the D2 fix below: the early return now fires only on a block-count problem, so an all-malformed block also reports the missing version. The audit found this row Diverged at `5d3dc41`, citing the early return that fix removed |
| Scenarios | S-007 a newer version fails with one named message | Conformed | `zen_config_findings()` / "this validator reads versions up to" and "update .tasks/validate.py from the kit", returned alone before any other check | `test_s007_a_newer_version_fails_with_a_named_message`, `test_s007_a_newer_version_is_reported_alone`. A probe with a malformed line beside `config_version: 2` also got the one message |
| Scenarios | S-008 a value outside a closed set fails | Conformed | `ZEN_CHOICES`; `zen_config_findings()` names key, value and `sorted(allowed)` | `test_s008_a_tracker_outside_the_set_fails`, `test_s008_a_default_mode_outside_the_set_fails` |
| Scenarios | S-009 a repeated key fails | Conformed | `parse_zen_config()` / "is set more than once" | `test_s009_a_repeated_key_fails` |
| Scenarios | S-010 a line that is not `key: value` fails | Conformed | `parse_zen_config()` / "line is not 'key: value' with a value" quoting the line | `test_s010_a_line_that_is_not_key_value_fails`, `test_s010_an_empty_value_fails`. What counts as blank or a comment differs from the spec at the margin: see the line grammar row |
| Scenarios | S-011 the block must appear exactly once | Conformed | `parse_zen_config()` / "exactly one is required", with the count in the message | `test_s011_no_block_fails`, `test_s011_two_blocks_fail` |
| Scenarios | S-012 session logs outside the repository are not checked | Diverged | `zen_config_findings()` / `Path(session_logs).is_absolute()` decides whether the value is checked | Spec: an absolute or `~` value is not checked, and the Paths rule says what is outside "on every operating system alike". Code: `Path` is the running system's flavour, so `/home/me/logs` is not absolute on Windows and `C:/Users/me/logs` is not absolute on Linux or macOS. Either is then checked and fails "must be a forward-slash path inside the repository" on the system that does not call it absolute. Shown on Linux by probe and by `PureWindowsPath("/nowhere").is_absolute()` being false. `test_s012_session_logs_outside_the_repository_are_not_checked` uses `/nowhere/at/all`, so by this reasoning it fails on a Windows cell; not run on Windows here |
| Scenarios | S-013 a path that leaves the repository, or uses backslashes, fails | Conformed | `zen_config_findings()` / the backslash, leading `/` or `~`, first-segment colon and `target.resolve()` containment test, then "must be a forward-slash path inside the" repository | Five tests, including `test_s013_a_drive_letter_path_fails_on_every_system`. The symbolic-link half has no test; a probe of a link pointing outside the root failed as specified, and one pointing inside passed |
| Scenarios | S-014 a reader without the fact discovers it and says so | Diverged | `spec-author`: "say when you discovered the location instead"; `new-task`: "Say once whether each fact came from"; `domain-language`: "Otherwise discover them, and say that you did"; `grill`: "when the repository has that file" | Spec: discovery and the one line also apply when the file exists but does not set the key. `spec-author` ("and it sets" `spec_dir`) and `new-task` (per fact) cover that half. `domain-language` and `grill` key their branch on the file existing, not the key being set, so a file without `glossary` is not stated to fall through to discovery. Not exercised by any run |
| Scenarios | S-015 the walkthrough writes nothing until the person confirms | Conformed | `init-worktracking` step 6: "Explore, read-only.", "Write only on confirmation", and the done-when "on a decline, no file changed" | Clause present and correct. **Run (a) did not follow it**: `docs/agents/zen.md` says itself "No person was in the session that wrote this file", so it was written without a confirmation. No conforming run exists |
| Scenarios | S-016 a re-run keeps every value already present | Conformed | `init-worktracking` step 6: "keep every line of the existing file byte-identical, prose and comments included" and "change a key only when the person asks for it during the run" | Not exercised. Step 6's "Show the whole draft: the file from" the template can be misread on a re-run as regenerating from the template; the re-run sub-step is the one that governs |
| Scenarios | S-017 one pointer block in AGENTS.md | Conformed | `init-worktracking` step 6: "replaced in place when it exists" and "otherwise appended at the end"; `agent-skills.md.tmpl` | The template is byte-identical to the spec's pointer block (compared programmatically). Not exercised: run (a) had no confirmation, and this repository's `AGENTS.md` holds no `## Agent skills` section, so step 6's own done-when is not met here |
| Scenarios | S-018 missing labels are printed, never created | Conformed | `init-worktracking` step 6, Labels: "tracker lacks, print" with the two commands, and "run none" | Not exercised: run (b) found the label list unreadable, which is S-029, not this |
| Scenarios | S-019 prose, other fences and comments are free | Conformed | `parse_zen_config()` skips any other fence whole until a matching close; `ZEN_FENCE_RE` takes backticks or tildes | `test_s019_a_block_inside_a_tilde_fence_is_not_counted`, `test_s019_a_longer_info_string_is_not_a_block`, `test_s019_prose_other_fences_and_comments_are_not_reported` |
| Scenarios | S-020 a version that is not a whole number fails | Conformed | `zen_config_findings()` / ASCII-only `[1-9][0-9]*` match and "must be a positive whole number" | `test_s020_a_version_that_is_not_a_whole_number_fails`, `test_s020_unicode_digits_signs_and_leading_zeros_fail` |
| Scenarios | S-021 a configured fact is used instead of discovered | Conformed | `domain-language`: "use them and say so"; `grill`: "say which source you used"; `spec-author`: "that is the spec location; say so"; `new-task`: "Say once whether each fact came from" | Not exercised. `new-task` reads both `AGENTS.md`'s acceptance command and the configured `acceptance` without saying which wins; the spec's reading is that the configured one does |
| Scenarios | S-022 a reader does not rely on a block it cannot parse | Conformed | All four readers: "use none of it, discover instead" and "shows why", naming `python .tasks/validate.py` | The same sentence in each of the four. Not exercised |
| Scenarios | S-023 a settled section is not asked | Conformed | `init-worktracking` step 6: "when every key in it has exactly one candidate" and "skipping settled ones" | Not exercised. The skill does not restate the spec's per-key candidate sources, but its exploration list covers each of them |
| Scenarios | S-024 one section per question, each with a recommendation | Conformed | `init-worktracking` step 6: "Ask one section at a time", "in this order", and "Lead each with the recommended answer, so one word accepts it" | Clause present. Run (a) asked no question, having no person to ask; not exercised |
| Scenarios | S-025 the draft is shown whole before writing | Conformed | `init-worktracking` step 6: "Show the whole draft", with both templates named | Clause present. Run (a) showed no draft to a person; not exercised |
| Scenarios | S-026 a re-run changes a key the person asks to change | Conformed | `init-worktracking` step 6: "change a key only when the person asks for it during the run" | Not exercised |
| Scenarios | S-027 free-text values are not checked | Conformed | `ZEN_TEXT` keys and `role.` keys never reach a value check in `zen_config_findings()` | `test_s027_free_text_values_are_not_checked`; role values are free in `GOOD` |
| Scenarios | S-028 a malformed standards list fails | Conformed | `zen_config_findings()` / "has an empty entry" and "may be none only on its own" | `test_s028_an_empty_standards_entry_fails`, `test_s028_none_beside_other_standards_fails` |
| Scenarios | S-029 labels that could not be read are all printed | Conformed | `init-worktracking` step 6: "print one for every configured label other" than `none`, "and say why"; exploration: "an error message or a non-zero exit means it could not be read" | Run (b) is reported to have exercised this, printing five commands, in the superseded double-quoted form. Reported, not verified; the current single-quoted form is not exercised |
| Scenarios | S-030 a memory file is created with the draft | Conformed | `init-worktracking` step 6: "holding one heading line" | Not exercised: run (a) left `memory` out |
| Scenarios | S-031 a reader does not use a configured path that is missing | Conformed | All four readers: "a configured path that does not exist is discovered instead too, and said" | Not exercised |
| Scenarios | S-032 no AGENTS.md gets no new file | Conformed | `init-worktracking` step 6: "put the block in your reply instead, and create no file for it" | Not exercised |
| Scenarios | S-033 a tracker without labels gets no label command | Conformed | `init-worktracking` step 6: "Print none for" `tasks` or `other` | Run (a) used `tracker: tasks`; whether its reply printed a command cannot be checked from the file. Not exercised |
| Scenarios | S-034 a re-run proposes only what is missing | Conformed | `init-worktracking` step 6: "propose values only for keys it lacks, appended at the end of the block" | Not exercised |
| Scenarios | S-035 a task's empty mode takes the default | Conformed | `_TEMPLATE.md.tmpl` and `.tasks/_TEMPLATE.md`: "takes default_mode from docs/agents/zen.md, else hitl"; `new-task`: "Leave it empty to take" `default_mode` | `new-task` states the first half itself and inherits "else hitl" from the template it reads in its step 1. Not exercised |
| Scenarios | S-036 only a well-formed fence opens a block | Conformed | `ZEN_FENCE_RE` allows at most three spaces of indent; `parse_zen_config()` opens a block only on an info string equal to `zen-config` and closes on the same character at least as long | No test for the indented, tilde or longer-close cases; probes of all three counted exactly the well-formed blocks |
| Scenarios | S-037 the line grammar is literal | Conformed | `parse_zen_config()` / `stripped.partition(":")`; no quote stripping; `none` compared case-sensitively | `test_s037_the_value_is_split_at_the_first_colon_and_quotes_are_kept`, `test_s037_none_is_lower_case_only` |
| Scenarios | S-038 one decision on every system, every finding in one run | Diverged | `parse_zen_config()` / `text.splitlines()` and `line.strip()`; `zen_config_findings()` collects into one list; `main()` checks `--links` before any of it | Line endings and tabs: conformed (`test_s038_crlf_line_endings_and_tabs_decide_the_same`). `--strict` and `--links`: conformed (`test_s038_strict_reports_the_same_and_links_mode_does_not_check`; `check_links()` returns before the check, though a `--links` glob matching the file still link-checks its prose like any document). Every fault in one run: diverged for the all-malformed block recorded under S-006 (`test_s038_every_finding_is_reported_in_one_run` covers two value faults only) |
| Scenarios | S-039 a re-run over a broken file stops | Diverged | `init-worktracking` step 6: "when the block does not parse, write nothing and ask the person to repair it by hand" | Spec: it writes nothing, **reports what `python .tasks/validate.py` reports**, and asks for a hand repair. The clause runs the validator first but never says to report its findings; two of the three outcomes are present. Not exercised |
| Scenarios | S-040 an other tracker gets its prose | Conformed | `init-worktracking` step 6: "ask for a paragraph saying how to create, read, label and close an item, and put it below the block"; `zen.md.tmpl` carries `{{TRACKER_NOTES}}` after the block | Asked within the sub-step that asks the tracker section. Not exercised |
| Proposed Surface | File path `docs/agents/zen.md` | Conformed | `ZEN_CONFIG_PATH`; `init-worktracking` step 6 names the same path | Matches constraint `D2` |
| Proposed Surface | Block recognition | Conformed | `ZEN_FENCE_RE`; `parse_zen_config()` | See S-019 and S-036. An unclosed `zen-config` fence is counted as a block, as CommonMark runs it to the end of the document; the spec does not say either way |
| Proposed Surface | Line grammar | Diverged | `parse_zen_config()` / `text.splitlines()` and `line.strip()` | Spec: only `\r\n` and `\n` are line endings, and key and value are "trimmed of spaces and tabs; nothing else is stripped". Code: `splitlines()` also breaks at a lone `\r`, form feed, U+0085 and U+2028, and `strip()` removes every Unicode whitespace character. Probes: a value ending in a no-break space passed although the spec makes it a different, missing path; a line starting with a no-break space then `#` was read as a comment; a U+2028 inside an `acceptance` value split the line and failed S-010. The same rule decides blank and comment lines |
| Proposed Surface | `none`, lower case only; `./none` for a real path | Conformed | `zen_config_findings()` / `if value == "none":` | `test_s037_none_is_lower_case_only`; a probe of `./none` was checked as a path |
| Proposed Surface | Paths | Conformed | `zen_config_findings()` containment test; `_exact_path()` | Holds for every path key except `session_logs`, for which see S-012. A path inside the repository that passes through `..` (`docs/../GLOSSARY.md`) fails as "does not exist", since `..` is no name in a listing; the spec's per-segment letter-case rule arguably agrees, and does not say |
| Proposed Surface | `config_version` | Conformed | `ZEN_CONFIG_VERSION`; see S-006, S-007, S-020 | Required-ness diverges in one case, recorded under S-006 |
| Proposed Surface | `tracker` | Conformed | `ZEN_CHOICES`; `init-worktracking` step 6 asks it first | |
| Proposed Surface | `role.` keys | Conformed | `ZEN_ROLES`; no tracker test on them in `zen_config_findings()`; step 6 asks them for "external trackers only" | The spec says the walkthrough asks for `github`, `gitlab` and `other`; the skill's "external" includes `other` only if `other` is read as external, which it is in practice (Linear, Jira) but is not said |
| Proposed Surface | `glossary`, `memory` (files) | Conformed | `ZEN_FILES` | |
| Proposed Surface | `adr_dir`, `spec_dir` (directories) | Conformed | `ZEN_DIRS` | |
| Proposed Surface | `standards` | Conformed | `zen_config_findings()` splits on commas, trims, checks each entry as a file | See S-028 |
| Proposed Surface | `acceptance`, `base_branch`, `integration_prefix`, `merge_policy` | Conformed | `ZEN_TEXT` | See S-027 |
| Proposed Surface | `session_logs` | Diverged | `zen_config_findings()` / `Path(session_logs).is_absolute()` | Same root cause as S-012. The repository-path case is conformed (`test_s012_a_repository_relative_session_log_path_is_checked`) |
| Proposed Surface | `default_mode` | Conformed | `ZEN_CHOICES`; `MODES` and the task `mode` check in `main()`; templates: "else hitl" | `ModeFieldTests`: `test_an_absent_mode_is_valid`, `test_each_named_mode_is_valid`, `test_any_other_mode_fails` |
| Proposed Surface | Validator | Diverged | `main()` calls `zen_config_findings()` outside the `strict` branch and reports with `err(ZEN_CONFIG_PATH, msg)` | Default and `--strict` alike, errors against the file, the newer version alone, `--links` not checking: all conformed. "Reports every finding at once" fails in the S-006 case only. A file that is not UTF-8 is reported as an error too, which the spec does not mention |
| Proposed Surface | Readers: the binding table | Conformed | `domain-language` and `grill` read `glossary`, `adr_dir`; `spec-author` reads `spec_dir`; `new-task` reads `acceptance`, `glossary`, `default_mode` | Exactly the table. `zen` mentions the file only to point at the configure step, which the non-goals allow |
| Proposed Surface | Readers: read without the validator, ignore unknown keys | Conformed | No reader runs the validator; each names it only as the place to see why | Each reader looks up only its own keys, so an unknown key is ignored by construction |
| Proposed Surface | Readers: a closed-set value outside its set is treated as absent | Not-built | None found | The one closed-set key a reader reads is `default_mode`, in `new-task`, which says nothing about an invalid value. A task left empty there would take the invalid value or nothing, unspecified |
| Proposed Surface | Readers: a missing configured path is treated as absent | Conformed | All four readers: "a configured path that does not exist is discovered instead too, and said" | See S-031 |
| Proposed Surface | Readers: ask when discovery finds several candidates | Not-built | `spec-author` only: "When the convention is ambiguous, ask" | `domain-language` ("Use what you find"), `grill` and `new-task` state no ask for a fact with several candidates |
| Proposed Surface | Readers: name the source of each fact once | Conformed | See S-014 and S-021 | |
| Proposed Surface | Pointer block | Conformed | `agent-skills.md.tmpl`; step 6: "it ends at the next heading of level two or higher" | Byte-identical to the spec text |
| Proposed Surface | Walkthrough | Conformed | `init-worktracking` step 6: "Offer this step at the end of every fresh scaffold"; step 5: "go straight to step 6"; settled and section order as in S-023 and S-024 | Run on its own reaches step 6 through step 5, which needs a scaffolded repository; the `zen` router says the same ("run it alone on a repository already tracked") |
| Proposed Surface | Label commands | Conformed | `init-worktracking` step 6, Labels: both commands in single quotes, "writing each" quote as the escaped form | Current form not exercised; run (b) printed the superseded form |
| Constraints | Markdown file with one fenced `zen-config` block | Conformed | `zen.md.tmpl`; `parse_zen_config()` | |
| Constraints | The check runs in the validator installed at every tier | Conformed | `init-worktracking`: "ships at every tier"; the template copy carries the same three functions | |
| Constraints | Standard library only | Conformed | `.tasks/validate.py` imports only standard modules | |
| Constraints | Decides the same way on Windows, macOS and Linux | Diverged | `zen_config_findings()` / `Path(session_logs).is_absolute()` | Every other decision is written to be system-independent (`_exact_path()`, the explicit `/`, `~`, backslash and colon tests). `session_logs` is the exception: S-012 |
| Constraints | The walkthrough is a step of `init-worktracking` | Conformed | `init-worktracking` / "Step 6: configure the skills" | |
| Non-Goals | Facts only; no quality-bar key; no label creation; no `tracker: other` prose check; one version; `install.py` and `zen` only point | Conformed | `ZEN_KEYS` holds no preference or quality-bar key; step 6: "run none"; `zen_config_findings()` reads nothing outside the block; `ZEN_CONFIG_VERSION` is 1; `zen` only suggests the configure step | `scripts/install.py` does not mention the file |

## Coverage proof

- **audited**: S-001 through S-040 (40 rows); every Proposed Surface element (file, block
  recognition, line grammar, `none`, paths, all eighteen keys grouped into nine rows, validator,
  six reader clauses, pointer block, walkthrough, label commands: 24 rows); the five Constraints;
  the Non-Goals (one row). Goals 1 to 6 are carried by those scenarios (1 by S-001 and S-021,
  2 by S-003 to S-013 and S-022, 3 by S-002 and S-014, 4 by S-015 and S-023 to S-025, 5 by S-016
  and S-034, 6 by S-018 and S-029) and were not given rows of their own. 70 rows: 59 Conformed,
  9 Diverged, 2 Not-built.
- **unreconciled**: 11 rows from seven root causes. Dispositions are proposed; the maintainer
  decides them.
  - **D1, fix.** `session_logs` absoluteness depends on the operating system (S-012, `session_logs`,
    the same-decision constraint). Decide outside-ness with the Paths rule's own markers instead of
    `Path.is_absolute()`; `test_s012_session_logs_outside_the_repository_are_not_checked` is
    expected to fail on a Windows cell until then.
  - **D2, fix.** A block whose every line is malformed does not report the missing
    `config_version` (S-006, S-038, Validator).
  - **D3, fix or amend the spec.** The line grammar strips and splits on all Unicode whitespace and
    line separators, where the spec names spaces, tabs, `\r\n` and `\n` (Line grammar).
  - **D4, fix.** `domain-language` and `grill` do not state that a file which lacks their key falls
    through to discovery (S-014).
  - **D5, fix.** The re-run over a broken file does not say to report what the validator reports
    (S-039).
  - **N1, fix or amend the spec.** No reader says a closed-set value outside its set is treated as
    absent (`new-task` and `default_mode`).
  - **N2, fix or amend the spec.** Three of the four readers do not state the ask when discovery
    finds several candidates.

## Run evidence

**No configure-step scenario has a verified conforming run.** Of the twenty conversational
scenarios (S-014 to S-018, S-021 to S-026, S-029 to S-035, S-039, S-040), every one rests on its
clause alone. One, S-029, is reported exercised by run (b) in a superseded quoting form, and that
report is not verified. Run (a), the one run whose output is in this repository, departed from the
contract, and the file it wrote says so itself:

- It wrote `docs/agents/zen.md` with no person present (S-015) and so asked no section (S-024) and
  showed no draft (S-025). The file's own "Pending confirmation" note records this, and routes the
  contested values to the maintainer.
- It placed no `## Agent skills` section in this repository's `AGENTS.md` (S-017 and step 6's
  done-when), which the implementer's description of the run did not mention. With no
  confirmation, writing nothing at all would have been the conforming outcome, so the missing
  section is a symptom of the departure rather than a separate fault. It does mean this repository
  does not currently meet step 6's done-when.

Until the maintainer confirms or corrects the file in the Marjana pull request, `docs/agents/zen.md`
is a valid file (S-001 holds for it) written by a non-conforming run.

## Observations

**"Conformed" carries two strengths here, as in the tracker-links matrix.** For the twenty code
scenarios it means code was read, tests ran, and the gaps between tests were probed. For the twenty
conversational ones it means the clause exists and says the right thing, with no observed run
behind it. The code half is the stronger evidence, and D1 shows its own limit: every test here ran
on one operating system, and the one cross-system fault was found by reading, not by a run.

**Tests the spec's invariants lack**, flagged rather than written: the indented, tilde and
longer-close fences of S-036; the symbolic-link half of S-013; the other-letter-case half of S-003;
the all-malformed block of S-006; any non-space whitespace in the line grammar; and a Windows-style
`session_logs` value on a POSIX run and the reverse. The test module's docstring names "S-014 to
S-018" as the conversational scenarios, a narrower set than the twenty the spec now has.

**The clauses most likely to be misread are the re-run ones.** S-016, S-026, S-034 and S-039 are
four precise byte-level promises carried by two sentences of prose, next to a "Show the whole
draft" sub-step that names the template. If a later run regenerates the file from the template on a
re-run, the fix is the pattern the tracker-links matrix names: move the rule into something
mechanical, such as a validator check that a re-run's diff touches only added keys, rather than
firming the prose.

## Fixed after the audit, not re-audited

Dated 2026-11-24, `feat-0091`. The implementer, not the auditor, fixed every cause above that needed a code or wording change. **The rows above are left exactly as the audit wrote them; none was re-derived by an independent agent**, so each stays Diverged or Not-built until a fresh audit (`A7`) or the integration review re-checks it. Evidence is the change and the test that pins it, all passing on Linux with Python 3.13 only.

| Cause | Change | Evidence |
|---|---|---|
| D1, `session_logs` per operating system | Outside is decided by spelling alone: a leading `~`, `/` or backslash, or a colon in the first segment. `Path.is_absolute()` is no longer used | `test_s012_a_windows_style_outside_path_is_not_checked_anywhere`; the POSIX case `test_s012_session_logs_outside_the_repository_are_not_checked` unchanged |
| D2, an all-malformed block skips the version check | `zen_config_findings()` returns early only for a block-count problem | `test_s006_a_block_of_only_malformed_lines_still_asks_for_a_version` |
| D3, Unicode whitespace and line separators | `parse_zen_config()` folds `\r\n`, splits on `\n` alone, and strips spaces and tabs only | `test_s038_a_no_break_space_is_part_of_the_value` |
| D4, `domain-language` and `grill` keyed on the file, not the key | Both now discover any path no key gives; the shared reader clause names "a key the file does not set" | The reader clause, identical in all four readers: "A key the file does not set, or sets to a value outside its allowed set or a path that does not exist, is discovered instead" |
| D5, S-039 did not report the validator's findings | Step 6 now says "show the person what the validator reported" | `init-worktracking` step 6, sub-step 3 |
| N1, an invalid closed-set value | The shared reader clause treats "a value outside its allowed set" as absent | As D4 |
| N2, several candidates | The shared reader clause says "asking the person when discovery finds several candidates" | As D4 |

From the Observations: the other-letter-case half of S-003 (`test_s003_a_known_key_in_other_letter_case_is_unknown`) and the indented and tilde fences of S-036 (`test_s036_only_a_well_formed_fence_opens_a_block`) now have tests, and the test module's docstring no longer names a range. Still open: a test for the symbolic-link half of S-013; a run of the suite on Windows; an unclosed block and a `..` segment, on which the spec is silent; and the missing `## Agent skills` section in this repository's `AGENTS.md`, which `feat-0091` does not own (WS-A owns `AGENTS.md`) and hands to integration.

Also on 2026-11-24, after the audit: the maintainer confirmed in person all five contested values of this repository's `docs/agents/zen.md` (tracker, base branch, standards, default mode, decision-record directory), relayed by the orchestrator, and the file's prose now says so. The S-015 and S-025 rows stand as audited, because the confirmation came after the file was written, not before.

**Landing-review fix round, 2026-11-24, by the implementer, not re-audited.** The orchestrator's reviewer found six more gaps; each was fixed and, where it is code, pinned by a test: an unclosed block is now its own error and nothing after it is read (new `S-041`, `test_s041_an_unclosed_block_is_reported_as_unclosed`); a `.`, `..` or empty segment is refused with a request for a normalised path, bar one leading `./` (new `S-042`, `test_s042_dot_segments_are_refused_with_a_normalise_message`, `test_s042_a_leading_dot_slash_is_allowed`); the outside spellings are listed once in the Paths section and used by `S-012` and `S-013`; `none` is limited to path, free-text and `role.` keys; step 6 says "by name"; a configure-only run is reached whenever `.tasks/validate.py` exists; and the shared reader clause says the reply names a configured path that was missing (`S-031`). `S-041` and `S-042` have no row above: they were added after the audit.

