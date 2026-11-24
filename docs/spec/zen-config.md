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
`spec-quality` lens, run by a fresh-context agent, returned `needs_revision` on the first draft with
findings in six fields; this revision answers each, and the re-run is recorded in
[`ws-b.md`](../reviews/2026-11-24-dogfood/ws-b.md). **Pending the maintainer's approval in the
Marjana pull request.** The path and the block format become a one-way door once an adopter
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
- **Creating, editing or deleting tracker labels, issues or boards.**
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
- The check runs in the validator `init-worktracking` installs at every tier, `.tasks/validate.py`
  (`feat-0091` scope), so every repository the walkthrough configures already carries it, whichever
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

- **Given** a `tracker` outside `tasks`, `github`, `gitlab`, `other`, or a `default_mode` outside
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

- **Given** a `session_logs` value that is an absolute path or starts with `~`
- **When** the shipped `validate.py` runs
- **Then** it reports no error for that key, whether or not the path exists on this machine.

### Scenario S-013: a path that leaves the repository, or uses backslashes, fails

- **Given** a path key other than an absolute or `~` `session_logs`, whose value is absolute,
  resolves outside the repository root, or contains a backslash
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

- **Given** the configure step of `init-worktracking` running in a repository
- **When** the person has not yet confirmed the draft, or declines it
- **Then** no file in the repository has changed; the exploration only read.

### Scenario S-016: a re-run keeps every value already present

- **Given** a repository whose `docs/agents/zen.md` already sets a key, by an earlier run or by hand
- **When** the configure step runs again and the person does not ask, during that run, to change
  that key
- **Then** that key's line, and every prose line and comment line of the file, are byte-identical
  after the run; the run proposes values only for keys absent before it.

### Scenario S-017: one pointer block in AGENTS.md

- **Given** the person confirms a draft, in a repository whose `AGENTS.md` has no `## Agent skills`
  section, or has one
- **When** the configure step writes
- **Then** `AGENTS.md` holds exactly one `## Agent skills` section of at most three lines, linking to
  `docs/agents/zen.md`; an existing section is replaced in place, never duplicated. When the
  repository has no `AGENTS.md`, no file is created to hold the block, and the step's reply carries
  the block for the person to place.

### Scenario S-018: missing labels are printed, never created

- **Given** a confirmed configuration naming `role.` labels, with `tracker: github` or
  `tracker: gitlab`, whose label list the step read and found lacking some of them
- **When** the configure step finishes
- **Then** its reply prints, for each missing label, `gh label create "<label>"` or
  `glab label create --name "<label>"`, with any double quote in the label escaped as `\"`, and the
  step runs none of them.

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

- **Given** a `docs/agents/zen.md` whose block count or line grammar fails (S-010, S-011)
- **When** a skill that reads it runs
- **Then** it uses none of the file's values, discovers the facts it needs, and its reply says the
  file could not be parsed and names `python .tasks/validate.py` as the check that shows why.

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
  `AGENTS.md`, and writes both only after the person confirms.

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
- **Then** it reports an error naming `standards`, and exits non-zero; entries are otherwise
  trimmed of surrounding spaces before they are checked.

### Scenario S-029: labels that could not be read are all printed, and not every tracker has any

- **Given** a confirmed configuration naming `role.` labels
- **When** the configure step finishes and the tracker is `github` or `gitlab` but its label list
  could not be read (no command-line tool, not signed in, offline), or the tracker is `tasks` or
  `other`
- **Then** for an unreadable list its reply prints a create command for every configured label and
  says the list could not be read; for `tasks` or `other` it prints no command.

### Scenario S-030: a memory file is created with the draft

- **Given** a confirmed draft whose `memory` names a file that does not exist yet
- **When** the configure step writes
- **Then** that file exists afterwards holding one heading line, so the validator's existence check
  passes.

## Proposed Surface

**File**: `docs/agents/zen.md`, from the repository root. Prose for people, then one block:

````markdown
```zen-config
config_version: 1
tracker: tasks
glossary: GLOSSARY.md
```
````

**Block recognition**: a fence of three or more backticks or three or more tildes, indented at most
three spaces, whose info string is exactly `zen-config`, closed by a fence of the same character at
least as long with no info string. Any other fence, including one whose info string has more words,
is skipped whole, so a block inside it is not counted.

**Line grammar inside the block**: blank lines and lines whose first non-space character is `#` are
ignored. Every other line is `key: value`, split at the first colon. Key and value are trimmed of
spaces; nothing else is stripped, quotes included. Keys are matched exactly, in lower case. A key
may appear once. `none` means "this repository has no such thing", in lower case only; a real path
named `none` is written `./none`.

| Key | Value |
|---|---|
| `config_version` | Required. A positive whole number; this contract defines `1` |
| `tracker` | `tasks` (the kit's `.tasks/`), `github`, `gitlab`, or `other`; for `other`, prose in the same file says how to create, read, label and close an item |
| `role.ready-agent`, `role.ready-human`, `role.needs-info`, `role.blocked`, `role.out-of-scope` | The tracker's label for that role; any non-empty text |
| `glossary`, `memory` | A file, as a forward-slash path from the repository root, or `none` |
| `adr_dir`, `spec_dir` | A directory, as a forward-slash path from the repository root, or `none` |
| `standards` | Comma-separated files, each a forward-slash path from the repository root, or `none` alone |
| `acceptance` | The one command that decides whether a change is acceptable |
| `base_branch`, `integration_prefix` | Where work lands, and the prefix integration branches carry |
| `merge_policy` | One line of prose: who merges what into where |
| `session_logs` | A directory where session logs are kept: absolute or `~` (not checked), a repository path (checked), or `none` |
| `default_mode` | `afk` (runs with nobody watching) or `hitl` (a person stays in the loop), for a task whose `mode` is empty |

**Validator**: `.tasks/validate.py` checks the file whenever it exists, in its default run and with
`--strict` alike, and reports each finding as an error against `docs/agents/zen.md`. It reports every
finding at once, except that a newer `config_version` is reported alone. `--links` does not check
the file.

**Readers**: a skill reading a fact the table defines reads the key when the file is valid and sets
it, and otherwise discovers the fact; either way its reply names the source once.

**Pointer block** in `AGENTS.md`: a `## Agent skills` section of at most three lines linking to
`docs/agents/zen.md`.

**Walkthrough**: the configure step of `init-worktracking`, offered at the end of every fresh
scaffold and run on its own when the person asks to configure the skills. Sections, in this order,
each skipped when exploration settled it: tracker and its role labels; documents (glossary, decision
records, specs, standards); how work lands (acceptance, base branch, integration prefix, merge
policy); agent work (default mode, session logs, memory). To change a key already set, the person
asks for it by name during the run.

**Label commands**: `gh label create "<label>"` for `github`, `glab label create --name "<label>"`
for `gitlab`; printed, never run.

## Open Questions

Routed to the maintainer through the orchestrator on 2026-11-24 as grill round 1. The contract above
is written with each recommended answer; each names what changes under the other answer.

1. **Role labels as one dotted key per role** (`role.ready-agent: ready-for-agent`) rather than one
   `roles:` line holding a list. Recommended: yes, because a label may hold spaces or commas and an
   unknown role is caught on its own line. Under the other answer, the Proposed Surface table and
   S-003, S-018, S-027 and S-029 change. Hardest to reverse of these.
2. **`config_version` required whenever the file exists.** Recommended: yes, because a file without
   it cannot say what it predates. Under the other answer, S-006 is retired and a missing version
   reads as `1`.
3. **`session_logs` may name a place outside the repository, unchecked; every other path key must
   be inside it.** Recommended: yes, because session logs live in the harness's home directory.
   Under the other answer, S-012 is retired and S-013 covers `session_logs` too.
4. **`standards` as one comma-separated list.** Recommended: yes, because the standards are few and
   read together, and a one-line list keeps the block short. The cost is that a path holding a comma
   cannot be named; under the other answer each standard is its own `standards.<n>` key, and S-028
   is retired.
5. **A re-run changes a key only when the person asks for it during the run**, with no attempt to
   detect a hand edit. Recommended: yes, because it is deterministic and needs no stored history.
   Under the other answer, S-016 and S-026 change to compare against a recorded copy of the last
   written file.
