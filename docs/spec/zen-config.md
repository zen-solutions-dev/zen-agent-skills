---
title: zen-config
status: draft
---

# zen-config

Behavioral contract for the per-repository setup file the kit's skills read, `docs/agents/zen.md`,
for the check that validates it, and for the `init-worktracking` step that writes it.

Drafted 2026-11-24 by `spec-author` for `feat-0091`, from the maintainer's decision `D2` in the
[Marjana plan](../reviews/2026-11-24-marjana-plan.md) and the design in the
[sources delta](../reviews/2026-11-24-sources-delta.md) ("Install-time setup walkthrough"). The
`spec-quality` lens, each time run by a fresh-context agent, returned `needs_revision` twice: on the
first draft (findings in six fields) and on the first revision (23 narrower findings). This text
answers the second set and has not been re-checked since: by the plan's rule of one review and one
fix, the third run is the maintainer's reading at approval. Both runs are recorded in
[`ws-b.md`](../reviews/2026-11-24-dogfood/ws-b.md). **Pending the maintainer's approval in the
Marjana pull request.**

Six format decisions were put to the maintainer as `grill` round 1, relayed by the orchestrator,
and the maintainer accepted each recommended answer in person on 2026-11-24: one dotted key per role
label; `config_version` required whenever the file exists; `session_logs` may name an unchecked
place outside the repository while every other path key stays inside it; the quality bar is a line
of `AGENTS.md`, not a key; `standards` is one comma-separated list; a re-run changes a key only when
the person asks for it during the run. They are written into the contract below as decided.

**Amended 2026-11-25 by `feat-0101`** (the rename from tasks to quests, maintainer decisions R2-4
and R2-7 in the [round 2 plan](../reviews/2026-11-25-marjana-r2-plan.md)): the kit's own tracker
value is now `quests`, naming `.quests/`, and `tasks` stays accepted as an alias for it, so a
repository configured before the rename still validates (S-008 as amended, new S-043). The
validator now sits in `.quests/validate.py`, or in `.tasks/validate.py` in a repository still using
the old directory. **This amendment needs the maintainer's re-approval in the round 2 pull
request.**

**Amended 2026-11-25 by `feat-0102`** (maintainer decision C1 in the
[decision sheet](../reviews/2026-11-25-marjana-decisions.md): verified two-way-door pull requests
may merge themselves, per repository, opt-in, with sampling): `merge_policy` stays free text, and a
value whose first token is exactly `self-merge-sampled` now also turns that opt-in on, read by the
autonomy lens's rule `A8` (new S-044 to S-046, the `merge_policy` row and the Readers table below).
Off stays the default: every other value, and an absent key, means no self-merge. Sampling is random, by the merge commit's sha (the maintainer's change at the check-in gate,
2026-11-25). The validator does
not change. **This amendment needs the maintainer's re-approval in the round 2 pull request.**

**Amended 2026-11-25 by `feat-0106`** (maintainer decision R2-2 in the
[round 2 plan](../reviews/2026-11-25-marjana-r2-plan.md): opt-in publishing of the local tracker to
GitHub, as a draft): two new keys, `publish` and `publish_repo`, turn on a one-way mirror of
`.quests/` to GitHub issues, run by `scripts/publish.py` (in the `triage` draft since the round 2
close; see the note below); a quest or spec may set
`private: true` to stay off it; and the new `triage` draft becomes the first reader of the `role.*`
keys (new S-047 to S-059, the key and Readers tables, and the Publishing section below). Off stays
the default: an absent key, `none`, or anything malformed publishes nothing. The shape of a
published issue is a one-way door, and the maintainer approved it at the `feat-0106` check-in gate
on 2026-11-25, relayed by the round 2 orchestrator; it is recorded verbatim in
`references/publishing.md` (the `triage` draft's since the round 2 close) and summarised under
Publishing. The approved
[tracker-links](tracker-links.md) contract still lists mirroring and issue hierarchy among its
Non-Goals: that contract is `pr-describe`'s, which still touches no issue, and it is not changed.
**This amendment needs the maintainer's re-approval in the round 2 pull request.**

**Noted 2026-11-25, round 2 close** (maintainer decision on the whole-branch review's M1, in the
[round 2 plan](../reviews/2026-11-25-marjana-r2-plan.md)): publishing moved to a draft.
`scripts/publish.py` and `references/publishing.md` moved from `new-quest` into the `triage` draft,
and `new-quest`'s step 8 loads them by name, guarded, so publishing reaches an adopter only with
`--include-drafts` until the maintainer's live `--apply` passes. **No behaviour change**: the
script, its scenarios and the issue shape are the same; only where they live and which skill
holds them moved, in the key, Readers and Publishing text below. The same note adds `orchestrate`
(a draft) to the Readers table, for the `merge_policy` and `base_branch` it already read through
rule `A8` (review S11). **For re-approval with the amendments above.**

The path and the block format become a one-way door once an adopter
configures a repository against them, which is why this contract exists before anyone outside this
repository reads the file.

## Problem

Every skill in the kit rediscovers, on every run, where a repository keeps its tracker, glossary,
decision records, specs and acceptance command. `domain-language` searches for a glossary,
`spec-author` searches for a spec directory, and `init-worktracking` records the tracker only as a
prose boundary in `AGENTS.md`. The searches cost context, can land on a different answer each run,
and cannot learn a fact the repository does not show, such as which branch a person merges into or
which label marks work an agent may take.

An adopter also has no walkthrough that fits the kit to their repository. The skills speak of
**facts** ("the tracker", "the acceptance command", "the glossary"), and nothing records what each
fact is in a given repository.

## Goals

1. One committed file per repository records the facts the skills read, in a block a script parses
   with the Python standard library alone, and a skill uses a configured fact instead of
   discovering it.
2. A malformed configuration, an unknown key, a path that does not exist, or a file written for a
   newer format fails the shipped validator with a message naming the problem; a skill never relies
   on a block it cannot parse.
3. A repository without the file, or without a given key, keeps working: the reader discovers the
   fact itself and says so.
4. A walkthrough writes the file with the person, one section at a time, and writes nothing they did
   not confirm.
5. A re-run of the walkthrough keeps every value already present unless the person asks for it to
   change.
6. Labels the configuration names but the tracker lacks are surfaced for the person to create.

## Non-Goals

- **Behaviour preferences**: grilling cadence, tone, verbosity, review depth. The file records facts
  about the repository, not how a skill should behave.
- **The quality bar** (prototype, production or library). It is one line of the repository's
  `AGENTS.md`, which every agent reads every session.
- **A user-level or machine-level configuration.** The file belongs to the repository and is
  committed with it.
- **Harness settings.** Nothing in the file configures Claude Code, Cursor, Codex or any other tool.
- **Creating, editing or deleting tracker labels, issues or boards**, by the walkthrough, the
  validator or any reader, with two exceptions added by `feat-0106`: the publisher creates and edits
  the issues and `zen:` labels it owns (Publishing, below), and `triage` adds and removes `role.*`
  labels on the person's go. Nothing ever deletes an issue.
- **Migrating a file from one `config_version` to the next.** Version 1 is the only version.
- **What `install.py` and `zen` say about the walkthrough.** Both only point at it, and neither
  reads nor writes the file.
- **The task `mode` field itself**, which the task template defines; this contract only supplies its
  default.
- **Checking the prose of a `tracker: other` file**, which says in words how to create, read, label
  and close an item.

## Constraints

- The path is `docs/agents/zen.md` from the repository root (maintainer decision `D2`, 2026-11-24).
- The file is Markdown: prose for people, plus one fenced block whose info string is `zen-config`,
  the same placement idea the kit's provenance blocks use.
- The check runs in the validator `init-worktracking` installs at every tier, `.quests/validate.py`
  (`feat-0091` scope; `.tasks/validate.py` in a repository scaffolded before `feat-0101`), so every repository the walkthrough configures already carries it, whichever
  tracker it names.
- The parser uses the Python standard library only, and decides the same way on Windows, macOS and
  Linux.
- The walkthrough is a step of `init-worktracking`, which already explores the repository and
  writes into it in that repository's own conventions.

## Scenarios

### Scenario S-001: a well-formed configuration passes

- **Given** a repository whose `docs/agents/zen.md` holds one `zen-config` block with
  `config_version: 1` and known keys whose values are valid and whose paths exist
- **When** the shipped `validate.py` runs
- **Then** it reports no error against `docs/agents/zen.md`, and its exit status is decided by the
  other checks alone.

### Scenario S-002: no file is not an error

- **Given** a repository with no `docs/agents/zen.md`
- **When** the shipped `validate.py` runs
- **Then** it prints nothing about the configuration, and its exit status is decided by the other
  checks alone.

### Scenario S-003: an unknown key fails

- **Given** a `zen-config` block holding a key the Proposed Surface does not list, including a
  `role.` key naming a role it does not list, or a known key in other letter case
- **When** the shipped `validate.py` runs
- **Then** it reports an error naming the key, and exits non-zero.

### Scenario S-004: a path that does not exist fails

- **Given** a path key (`glossary`, `adr_dir`, `spec_dir`, `memory`, a repository-relative
  `session_logs`, or one entry of `standards`) naming a path that does not exist, that exists as a
  directory where the key needs a file or the reverse, or that differs from the path on disk only in
  letter case
- **When** the shipped `validate.py` runs
- **Then** it reports an error naming the key and the path, and exits non-zero, on every operating
  system alike.

### Scenario S-005: `none` is a valid path value

- **Given** a path key whose whole value is `none`
- **When** the shipped `validate.py` runs
- **Then** it reports no error for that key.

### Scenario S-006: a missing version fails

- **Given** a `zen-config` block with no `config_version` key
- **When** the shipped `validate.py` runs
- **Then** it reports an error saying `config_version` is required, and exits non-zero.

### Scenario S-007: a newer version than the validator knows fails with one named message

- **Given** a `zen-config` block whose `config_version` is higher than the highest version the
  validator reads, whatever other keys it holds
- **When** the shipped `validate.py` runs
- **Then** it reports exactly one error against the file, naming the file's version and the
  validator's highest version and saying the validator needs updating from the kit, and exits
  non-zero.

### Scenario S-008: a value outside a closed set fails

- **Given** a `tracker` outside `quests`, `tasks`, `github`, `gitlab`, `other`, or a `default_mode` outside
  `afk`, `hitl`
- **When** the shipped `validate.py` runs
- **Then** it reports an error naming the key, the value and the allowed values, and exits non-zero.

### Scenario S-009: a repeated key fails

- **Given** a `zen-config` block that sets the same key twice
- **When** the shipped `validate.py` runs
- **Then** it reports an error naming the key, and exits non-zero.

### Scenario S-010: a line that is not `key: value` fails

- **Given** a non-blank line in the block that is neither a `#` comment nor `key: value` with a
  non-empty key and a non-empty value
- **When** the shipped `validate.py` runs
- **Then** it reports an error quoting the line, and exits non-zero.

### Scenario S-011: the block must appear exactly once

- **Given** a `docs/agents/zen.md` holding no `zen-config` block, or more than one
- **When** the shipped `validate.py` runs
- **Then** it reports one error stating the number of blocks it found, and exits non-zero.

### Scenario S-012: session logs outside the repository are not checked

- **Given** a `session_logs` value with an outside spelling (see Paths in the Proposed Surface)
- **When** the shipped `validate.py` runs
- **Then** it reports no error for that key, whether or not the path exists on this machine.

### Scenario S-013: a path that leaves the repository, or uses backslashes, fails

- **Given** a path key, other than a `session_logs` with an outside spelling, whose value has an
  outside spelling, contains a backslash anywhere, or resolves outside the repository root
- **When** the shipped `validate.py` runs
- **Then** it reports an error naming the key and saying the path must be a forward-slash path
  inside the repository, and exits non-zero.

### Scenario S-014: a reader without the fact discovers it and says so

- **Given** a repository with no `docs/agents/zen.md`, or with one that does not set the key a skill
  needs, such as `domain-language` needing `glossary`
- **When** that skill runs
- **Then** it finds the fact by its own discovery, and its reply to the person contains one line
  naming the fact and saying it came from discovery rather than from `docs/agents/zen.md`.

### Scenario S-015: the walkthrough writes nothing until the person confirms

- **Given** the configure step of `init-worktracking` running in a repository, whether offered at
  the end of a fresh scaffold or started on its own
- **When** the person has not yet confirmed the draft, declines it, or declines the step itself
- **Then** no file in the repository has changed; the exploration only read.

### Scenario S-016: a re-run keeps every value already present

- **Given** a repository whose `docs/agents/zen.md` already sets a key, by an earlier run or by hand
- **When** the configure step runs again and the person does not ask, during that run, to change
  that key
- **Then** that key's line, and every prose line and comment line of the file, are byte-identical
  after the run.

### Scenario S-017: one pointer block in AGENTS.md

- **Given** the person confirms a draft, in a repository whose `AGENTS.md` has no `## Agent skills`
  section, or has exactly one
- **When** the configure step writes
- **Then** `AGENTS.md` holds exactly one `## Agent skills` section, its text exactly the pointer
  block below: an existing section is replaced in place, and a new one is appended at the end of
  the file.

### Scenario S-018: missing labels are printed, never created

- **Given** a confirmed configuration naming `role.` labels, with `tracker: github` or
  `tracker: gitlab`, whose label list the step read and found lacking some of them
- **When** the configure step finishes
- **Then** its reply prints, for each missing label, one label command from the Proposed Surface,
  and the step runs none of them.

### Scenario S-019: prose, other fences and comments are free

- **Given** a `docs/agents/zen.md` with prose and other fenced blocks outside the `zen-config` block,
  including an example `zen-config` block nested inside an outer fence, and `#` comment lines and
  blank lines inside the real block
- **When** the shipped `validate.py` runs
- **Then** none of them is reported, and the nested example is not counted as a block.

### Scenario S-020: a version that is not a whole number fails

- **Given** a `config_version` that is not a positive whole number
- **When** the shipped `validate.py` runs
- **Then** it reports an error naming the value and saying it must be a positive whole number, and
  exits non-zero.

### Scenario S-021: a configured fact is used instead of discovered

- **Given** a valid `docs/agents/zen.md` setting a key a skill needs, such as `acceptance: make check`
- **When** a skill that needs that fact runs
- **Then** it uses the configured value (`make check`) and its reply names `docs/agents/zen.md` as
  the source.

### Scenario S-022: a reader does not rely on a block it cannot parse

- **Given** a `docs/agents/zen.md` whose block count or line grammar fails (S-010, S-011), or whose
  `config_version` is newer than `1`
- **When** a skill that reads it runs
- **Then** it uses none of the file's values, discovers the facts it needs, and its reply says the
  file could not be parsed and names `python .quests/validate.py` as the check that shows why.

### Scenario S-023: a settled section is not asked

- **Given** a walkthrough section every key of which exploration found exactly one candidate for
- **When** the configure step runs
- **Then** it asks no question for that section, and the draft it shows carries the found values.

### Scenario S-024: one section per question, each with a recommendation

- **Given** a walkthrough with more than one unsettled section
- **When** the configure step asks
- **Then** each message to the person covers one section, in the order the Proposed Surface lists
  them, and offers a recommended answer the person accepts with one word.

### Scenario S-025: the draft is shown whole before writing

- **Given** every section answered or settled
- **When** the configure step reaches its draft
- **Then** it shows the whole `docs/agents/zen.md` and the `## Agent skills` block it will place in
  `AGENTS.md` before it asks the person to confirm.

### Scenario S-026: a re-run changes a key the person asks to change

- **Given** a repository whose `docs/agents/zen.md` sets a key
- **When** the person asks, during a configure run, to change that key, and confirms the draft
- **Then** that key's value becomes the confirmed value, and every other line of the file is
  byte-identical to its state before the run.

### Scenario S-027: free-text values are not checked

- **Given** any non-empty value for `acceptance`, `base_branch`, `integration_prefix`,
  `merge_policy` or a `role.` key
- **When** the shipped `validate.py` runs
- **Then** it reports no error for that key.

### Scenario S-028: a malformed standards list fails

- **Given** a `standards` value with an empty entry (`a.md,,b.md`), or `none` beside other entries
- **When** the shipped `validate.py` runs
- **Then** it reports an error naming `standards`, and exits non-zero.

### Scenario S-029: labels that could not be read are all printed

- **Given** a confirmed configuration naming `role.` labels, with a `github` or `gitlab` tracker
  whose label list could not be read (no command-line tool, not signed in, offline)
- **When** the configure step finishes
- **Then** its reply says the list could not be read and prints a label command for every
  configured label other than `none`.

### Scenario S-030: a memory file is created with the draft

- **Given** a confirmed draft whose `memory` names a file that does not exist yet
- **When** the configure step writes
- **Then** that file exists afterwards holding one heading line, so the validator's existence check
  passes.

### Scenario S-031: a reader does not use a configured path that is missing

- **Given** a parseable `docs/agents/zen.md` whose key a skill needs names a path that does not exist
- **When** that skill runs
- **Then** it discovers that fact instead, and its reply says the configured path was missing.

### Scenario S-032: no AGENTS.md gets no new file

- **Given** a repository with no `AGENTS.md`
- **When** the configure step writes a confirmed draft
- **Then** no file other than `docs/agents/zen.md` (and a new `memory` file) is created, and the
  step's reply carries the pointer block for the person to place.

### Scenario S-033: a tracker without labels gets no label command

- **Given** a confirmed configuration with `tracker: quests` (or its alias `tasks`) or `tracker: other`
- **When** the configure step finishes
- **Then** its reply prints no label command.

### Scenario S-034: a re-run proposes only what is missing

- **Given** a repository whose `docs/agents/zen.md` parses and lacks some keys
- **When** the configure step runs again and the person asks to change no key
- **Then** every value it proposes is for a key absent before the run, and the confirmed new keys
  are appended at the end of the block.

### Scenario S-035: a task's empty mode takes the default

- **Given** a task file whose `mode` is empty or absent
- **When** `new-quest` or another reader needs that task's mode
- **Then** the mode is the file's `default_mode` when it sets one, and `hitl` otherwise.

### Scenario S-036: only a well-formed fence opens a block

- **Given** a `zen-config` fence indented four or more spaces, or a fence whose info string is
  `zen-config` followed by more words, beside one well-formed block, or a well-formed block made of
  tildes, or closed by a longer fence than opened it
- **When** the shipped `validate.py` runs
- **Then** it counts exactly the well-formed blocks, as the Proposed Surface's block recognition
  says.

### Scenario S-037: the line grammar is literal

- **Given** a value holding a further colon (`acceptance: make check: all`), a value in quotes
  (`glossary: "GLOSSARY.md"`), or `None` in another letter case
- **When** the shipped `validate.py` runs
- **Then** the value is everything after the first colon, quotes are part of it, and `None` is a
  path like any other, so the quoted and the capitalised values fail S-004.

### Scenario S-038: one decision on every system, every finding in one run

- **Given** a block with Windows line endings or tabs beside the colon, or with several faults
- **When** the shipped `validate.py` runs, in its default run or with `--strict`
- **Then** line endings and tabs change no finding, every fault is reported in the one run (bar
  S-007), and `validate.py --links` reports nothing about the file.

### Scenario S-039: a re-run over a broken file stops

- **Given** a `docs/agents/zen.md` whose block does not parse (S-010, S-011)
- **When** the configure step runs again
- **Then** it writes nothing, reports what `python .quests/validate.py` reports, and asks the person
  to repair the file by hand first.

### Scenario S-040: an other tracker gets its prose

- **Given** a person who chooses `tracker: other`
- **When** the configure step drafts the file
- **Then** the draft carries a section below the block, in the person's words, saying how to
  create, read, label and close an item, and the step asks for it as part of the tracker section.

### Scenario S-041: an unclosed block is reported as unclosed

- **Given** a `zen-config` fence that no closing fence follows
- **When** the shipped `validate.py` runs
- **Then** it reports one error saying the block is never closed, reports nothing about the lines
  after the fence, and exits non-zero.

### Scenario S-042: a path is written normalised

- **Given** a path value holding a `.` or `..` segment or an empty segment, other than one leading
  `./`, such as `docs/../GLOSSARY.md`
- **When** the shipped `validate.py` runs
- **Then** it reports an error naming the key and asking for a normalised path, and exits non-zero,
  whether or not the path would resolve to a file that exists.

### Scenario S-043: the old tracker name is accepted

Added 2026-11-25 by `feat-0101`.

- **Given** a configuration written before the rename to quests, with `tracker: tasks`, and its
  validator in `.tasks/validate.py`
- **When** the shipped `validate.py` runs, from `.tasks/` or from `.quests/`
- **Then** it reports nothing about `tracker` and exits as it would for `tracker: quests`.

### Scenario S-044: a self-merge opt-in is read with its rate

Added 2026-11-25 by `feat-0102`.

- **Given** a configuration that sets `base_branch: developer` explicitly, in a repository whose
  merge method for `developer` creates a new commit (a merge commit or a squash), and whose
  `merge_policy` is `self-merge-sampled 1/4; a person merges developer into main`, or
  `self-merge-sampled`, or `self-merge-sampled; a person reviews samples`
- **When** an agent applying the autonomy lens's `A8` reads it to decide whether it may merge a
  verified two-way-door pull request into `developer`
- **Then** it treats sampled self-merge as on, with N = 4 for the first value and N = 5 for the other
  two, and still applies every guard `A8` lists; a pull request it merges is sampled for a person's
  review exactly when the merge commit's full sha, read as a hexadecimal integer, is divisible by N
  (`int(sha, 16) % N == 0`), so the sample cannot be predicted before the merge and can be checked
  after it.

### Scenario S-045: anything else leaves self-merge off

Added 2026-11-25 by `feat-0102`.

- **Given** a configuration with no `merge_policy`, or `merge_policy: none`, or a value that does
  not begin with the exact lower-case word `self-merge-sampled` (such as `Self-merge-sampled`,
  `allow self-merge-sampled`, `self-merge-sampled-ish`), or that begins with it followed by a token
  starting with a digit that is not `1/N` with N a whole number from 1 to 20 written without a
  leading zero (such as `1/0`, `1/21`, `2/5`, `1/05`), or a file the reader cannot parse; or a
  valid opt-in in a file that sets no `base_branch`, or `base_branch: none`, so the branch would
  have to be discovered (such as the remote's default, usually `main`); or a valid opt-in in a
  repository that merges into `base_branch` by fast-forward only
- **When** an agent applying `A8` reads it
- **Then** it treats sampled self-merge as off and merges nothing itself, and names
  the value it read, when there is one, in its report.

### Scenario S-046: the validator does not judge the opt-in

Added 2026-11-25 by `feat-0102`.

- **Given** any non-empty `merge_policy`, including `self-merge-sampled 1/0`
- **When** the shipped `validate.py` runs
- **Then** it reports no error for that key, as S-027 says; a malformed opt-in fails safe at the
  reader (S-045) rather than at the validator.

### Scenario S-047: valid publishing keys pass

Added 2026-11-25 by `feat-0106`, as are S-048 to S-059.

- **Given** a configuration with `tracker: quests` (or no `tracker`) and `publish: github` with
  `publish_repo: octo-org/octo-repo`, or `publish: none`, or a `publish_repo` alone
- **When** the shipped `validate.py` runs
- **Then** it reports no error for either key.

### Scenario S-048: malformed publishing keys fail

- **Given** a `publish` outside `github`, `none`; a `publish_repo` other than `none` that is not
  `owner/name` (such as `a/b/c`, `o/..`, `not a repo`); or `publish: github` with no `publish_repo`
  or `publish_repo: none`
- **When** the shipped `validate.py` runs
- **Then** it reports an error naming the key, and exits non-zero.

### Scenario S-049: publishing is off unless opted in

- **Given** a repository whose `docs/agents/zen.md` is absent, does not parse, has a newer
  `config_version`, sets no `publish` or `publish: none`, or holds any finding S-048 or S-050
  names, or whose `.quests/validate.py` predates the publishing keys
- **When** `scripts/publish.py` runs, as a dry run or with `--apply`
- **Then** it prints that publishing is off and why, calls nothing on GitHub, and exits 0 for a
  dry run and 1 with `--apply`.

### Scenario S-050: publishing mirrors only the local tracker

- **Given** `publish: github` with a `tracker` other than `quests` or `tasks`
- **When** the shipped `validate.py` runs
- **Then** it reports an error saying publishing mirrors the local tracker, and exits non-zero.

### Scenario S-051: a dry run by default, an apply only when asked

- **Given** a repository that opts in
- **When** `scripts/publish.py` runs without `--apply`
- **Then** it prints a numbered plan and its notes and makes no call that writes to GitHub (with
  `--offline`, no call at all); with `--apply` it carries the plan out in order through `gh`,
  stops at the first failed call saying so and exits 1, and a second run completes the rest
  without creating any issue twice.

### Scenario S-052: the published issue has the approved shape

- **Given** a quest `feat-0001` titled `Do the thing` in `.quests/feat-0001-a.md`, naming a spec
  titled `alpha`
- **When** it is published
- **Then** its issue is titled `feat-0001: Do the thing`, the spec's `Spec: alpha`; each body opens
  with the italic line naming the source file and saying edits made on GitHub are overwritten,
  carries the frontmatter table (a quest) or the status (a spec) and the file's body with every
  relative link outside fenced code made absolute at `base_branch` (or `HEAD`), is at most 65,536
  characters, cut with a note when longer at a boundary outside fenced code, and ends in the
  marker line `<!-- zen-publish v1 kind=<quest|spec> id=<id> source=<path> digest=<12 hex> -->`,
  whose digest is the sha256 of the body above it; and marker-shaped text in the file itself is
  rendered broken (`&lt;!--`), the one rewrite besides links (maintainer decision (a),
  2026-11-25), so the marker is the only marker-shaped line the body holds.

### Scenario S-053: publishing is idempotent by marker

- **Given** a repository published once
- **When** the publisher runs again with no file changed
- **Then** its plan holds no operation; a changed file, a title or body edited by hand on GitHub,
  text a person typed below the marker, or a quest moved to `done/` edits the same issue, found by
  the last marker-shaped line of its body and never by its title, and no second issue is created
  for any quest or spec.

### Scenario S-054: status maps from the file

- **Given** published quests
- **When** a quest moves to `.quests/done/` or sets `status: done`, or its issue is closed on
  GitHub while the quest is open, or a quest is done before it was ever published, or a quest's
  status is `in_progress`
- **Then** its issue is closed as completed; reopened, and the dry run shows the reopen; given no
  issue at all; labelled `zen:in-progress` until the status changes, respectively. A spec's issue
  is open exactly while one of its published quests is, and a spec gets an issue only when an open
  published quest names it.

### Scenario S-055: the publisher touches only what it owns

- **Given** issues carrying `role.*` labels or other labels a person applied, an issue carrying
  `zen:published` with no valid marker, or two issues with the same marker
- **When** the publisher runs
- **Then** it adds and removes only `zen:` labels, never another; it leaves the unmarked issue and
  the second of the two untouched and names them in its notes; and it removes a sub-issue or
  blocking link only between two issues it owns.

### Scenario S-056: nothing is ever deleted

- **Given** a published quest whose file is deleted, or a spec no published quest names any more,
  or an issue whose marker's `source` names neither the item's path nor a file carrying its id
- **When** the publisher runs
- **Then** the issue is left as it was, its sub-issue and blocking links included, and named once
  in the notes, and no call deletes or transfers an issue; the one change near it is decision
  (d)'s, in S-058: a published quest that drops its spec is unlinked from such a spec issue,
  which is otherwise untouched.

### Scenario S-057: private and unpublishable files stay off GitHub

- **Given** a quest or spec whose frontmatter sets `private: true`, a quest file git does not track,
  or a quest whose `spec` names a file outside `spec_dir` or a report beside a spec
- **When** the publisher runs
- **Then** the private or untracked file gets no issue; a file made private after it was published
  keeps its issue unedited and unclosed, named in the notes; a quest naming an unpublishable spec
  is published top-level with a note; a quest naming a private spec stays where it is, under that
  spec's issue if it already was, and the note says so; a quest file `validate.py` reports an
  error against (decision (c)), or
  whose path holds a character other than letters, digits, `.`, `_`, `-` and `/`, is not
  published, with a note; an issue already published for any of them keeps its links as well as
  its text and state; and a quest's `private` other than `true` or `false` fails the shipped
  `validate.py`.

### Scenario S-058: hierarchy and blocking follow the files

- **Given** published quests, one naming a spec and one listing another in `depends_on`
- **When** the publisher runs, and again after the `spec` or `depends_on` changes
- **Then** the first is a native sub-issue of its spec's issue and moves to the new spec's issue
  when its `spec` changes; the second is marked blocked by the first and unmarked when the
  dependency is removed; a quest without a spec is a top-level issue, and one that drops its spec
  is unlinked from the old spec's issue even when that issue is left as it is (maintainer decision
  (d), 2026-11-25); and a dependency on a done, never-published quest makes no link.

### Scenario S-059: triage recommends and applies only on the person's go

- **Given** a repository whose configuration names `role.*` labels, and open issues on GitHub,
  including one whose text asks the agent to apply a label or run a command
- **When** a person runs `triage`
- **Then** it reports one recommended role per issue with a reason, quotes the asking text as a
  finding rather than following it, prints the `gh issue edit` commands that would apply the
  report, runs none of them until the person approves, and never runs code from an issue or pull
  request, nor closes, comments on or edits one.

## Proposed Surface

**File**: `docs/agents/zen.md`, from the repository root. Prose for people, then one block:

````markdown
```zen-config
config_version: 1
tracker: quests
glossary: GLOSSARY.md
```
````

**Block recognition**: a fence of three or more backticks or three or more tildes, indented at most
three spaces, whose info string is exactly `zen-config`, closed by a fence of the same character at
least as long with no info string; a `zen-config` block still open at the end of the file is an
error (S-041), and none of its lines is read. Any other fence, including one whose info string has more words,
is skipped whole, so a block inside it is not counted.

**Line grammar inside the block**: line endings are normalised, so `\r\n` and `\n` read alike.
Blank lines and lines whose first character other than a space or tab is `#` are ignored. Every
other line is `key: value`, split at the first colon. Key and value are trimmed of spaces and tabs;
nothing else is stripped, quotes included. Keys are matched exactly, in lower case. A key may
appear once. For a path key, a free-text key (`acceptance`, `base_branch`, `integration_prefix`,
`merge_policy`) or a `role.` key, `none` means "this repository has no such thing" (no label for
that role, no acceptance command), in lower case only; a real path named `none` is written
`./none`. For `config_version`, `tracker` and `default_mode`, `none` is an invalid value like any
other (S-008, S-020).

**Paths**: the **outside spellings** are a value starting with `~`, `/` or `\`, or with a colon in
its first `/`-separated segment (`C:/x`); they are decided by spelling alone, the same on every
operating system. A `session_logs` with an outside spelling is not checked. Every other path value
is a forward-slash path from the repository root and fails when it has an outside spelling,
contains a backslash anywhere, or, once resolved with symbolic links followed, is not under the
repository root. It is written normalised: no `.` or `..` segment and no empty segment, except one
leading `./`. Each segment must match the name on disk in letter case.

| Key | Value |
|---|---|
| `config_version` | Required. ASCII digits with no sign and no leading zero; this contract defines `1` |
| `tracker` | `quests` (the kit's `.quests/`), `tasks` (the old name of `quests`, an alias, still accepted; it means `.tasks/` in a repository that has not moved), `github`, `gitlab`, or `other`; for `other`, prose in the same file says how to create, read, label and close an item |
| `role.ready-agent`, `role.ready-human`, `role.needs-info`, `role.blocked`, `role.out-of-scope` | The external tracker's label for that role; any non-empty text. The validator accepts them with any tracker; the walkthrough asks for them only for `github`, `gitlab` and `other` |
| `glossary` | The project glossary, a file |
| `memory` | The file where an orchestrating session keeps its dated log of decisions, a file |
| `adr_dir`, `spec_dir` | The decision-record directory and the spec directory |
| `standards` | The documents a review judges written standards against: comma-separated files, each trimmed of surrounding spaces, or `none` alone |
| `acceptance` | The one command that decides whether a change is acceptable |
| `base_branch`, `integration_prefix` | Where work lands, and the prefix integration branches carry |
| `merge_policy` | One line of prose: who merges what into where. Split on spaces, tabs and `;`, empty pieces dropped: when the first token is exactly `self-merge-sampled` (case-sensitive), the repository opts into sampled self-merge of verified two-way doors (S-044); if the next token starts with a digit it is the sampling rate and must be exactly `1/N`, N an integer from 1 to 20 with no leading zero, else the opt-in is off (S-045); with no such token N is 5. The opt-in also needs an explicit `base_branch` (not absent, not empty, not `none`) and a merge method that creates a new commit, else it is off (S-045). A merged pull request is sampled when its merge commit's full sha, as a hexadecimal integer, is divisible by N. Any other value leaves it off |
| `session_logs` | The directory where the harness keeps session transcripts for this repository: one of the outside spellings defined under Paths (not checked), a repository path (checked), or `none` |
| `default_mode` | `afk` (runs with nobody watching) or `hitl` (a person stays in the loop), for a task whose `mode` is empty; `hitl` when this key is absent |
| `publish` | `github` or `none`, from `feat-0106`. `github` opts into mirroring the local tracker to GitHub issues (Publishing, below); absent or `none` is off. Valid only with `tracker` absent, `quests` or `tasks` (S-050) |
| `publish_repo` | The repository the issues go to, `owner/name`, or `none`; required when `publish` is `github` (S-048). Named rather than left to `gh`, which may pick a fork's upstream |

**Validator**: `.quests/validate.py` checks the file whenever it exists, in its default run and with
`--strict` alike, and reports each finding as an error against `docs/agents/zen.md`. It reports every
finding at once, except that a newer `config_version` is reported alone. `--links` does not check
the file.

**Readers**: this contract binds the skills below, and one lens. Each reads its keys from a parseable file of a
known version without running the validator; a key it does not know is ignored, and a key whose
value falls outside its closed set or names a missing path is treated as absent. A fact whose key is
absent it discovers as it does without this file (asking the person when discovery finds several
candidates). Its reply names the source of each fact once. The self-merge opt-in is the exception to
discovery: an absent `merge_policy` means off, and so does an absent `base_branch` for it, since
self-merge never goes to a discovered branch; nothing is asked or inferred (S-045). Other skills may become readers later by
amendment.

| Skill | Keys it reads |
|---|---|
| `domain-language` | `glossary`, `adr_dir` |
| `grill` | `glossary`, `adr_dir` |
| `spec-author` | `spec_dir` |
| `new-quest` | `acceptance`, `glossary`, `default_mode`; and `publish`, to decide whether to load the `triage` draft's publishing (round 2 close) |
| `triage` (a draft), from `feat-0106` | every `role.*` key, `publish_repo`; and, through its `scripts/publish.py` (moved from `new-quest` at the round 2 close), `publish`, `publish_repo`, `spec_dir`, `base_branch` |
| `orchestrate` (a draft), noted at the round 2 close | `merge_policy` (the `self-merge-sampled` opt-in only), `base_branch`, as rule `A8` reads them: absent means off, never discovered |
| The autonomy lens (`.agents/rules/autonomy.md`, rule `A8`), from `feat-0102` | `merge_policy` (the `self-merge-sampled` opt-in only), `base_branch` |

**Publishing**, from `feat-0106`: `scripts/publish.py` mirrors the tracker one way. Since the
round 2 close it lives in the `triage` draft, which `new-quest` loads, guarded, when `publish` is
`github`.
It reads the configuration through the repository's own `validate.py` and publishes nothing unless
that validator finds the publishing keys valid (S-049). A dry run is the default; `--apply` acts
through `gh` only, with gh's own sign-in (S-051). Candidates are the quest files git tracks in the
tracker directory and its `done/`, and the spec files directly in `spec_dir` that a published
quest names, never one whose frontmatter sets `private: true` (S-057); nothing but their text and
the table drawn from a quest's frontmatter is sent. Specs are issues, quests their native
sub-issues or top-level issues, `depends_on` native blocking (S-058). Every published issue
carries the `zen:published` label and ends in its marker, and the publisher acts only on issues
carrying both (S-053, S-055); since anyone who can apply that label can therefore have an issue
edited, `references/publishing.md` names the label as the trust boundary to protect. The labels are `zen:published`, `zen:spec`, `zen:quest` and
`zen:in-progress`, fixed names; the publisher never applies or removes a `role.*` label. The full
approved shape, titles, body, labels and status, is in the `triage` draft's `references/publishing.md`;
S-052 to S-056 are its observable part. The quest frontmatter field `private` is `true` or
`false`, checked by `validate.py` (S-057).

**Pointer block** in `AGENTS.md`: exactly this text, a heading and one line; the section ends at
the next heading of level two or higher:

```markdown
## Agent skills

The kit's skills read this repository's setup from [`docs/agents/zen.md`](docs/agents/zen.md).
```

**Walkthrough**: the configure step of `init-worktracking`, offered at the end of every fresh
scaffold and run on its own when the person asks to configure the skills. A key's **candidate** is a
value the repository itself shows: an existing file or directory for a path key, a command in CI or
the manifest for `acceptance`, the remote's default branch for `base_branch`, a shared prefix of
existing branch names for `integration_prefix`. `merge_policy`, `default_mode` and role labels have
no candidate, so a section holding one is never settled. A section is **settled** when every key in
it has exactly one candidate. Sections, in this order, each skipped when settled: tracker and its role labels; documents (glossary, decision
records, specs, standards); how work lands (acceptance, base branch, integration prefix, merge
policy); agent work (default mode, session logs, memory). To change a key already set, the person
asks for it by name during the run.

**Label commands**, printed for a POSIX shell and never run: `gh label create '<label>'` for
`github`, `glab label create --name '<label>'` for `gitlab`, each label in single quotes with every
`'` inside it written `'\''`, so no character in a label is expanded.

## Open Questions

None.
