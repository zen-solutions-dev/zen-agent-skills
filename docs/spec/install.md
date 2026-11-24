---
title: install
status: approved
---

# install

Behavioral contract for [`scripts/install.py`](../../scripts/install.py), written 2026-07-27
(`feat-0029`). A **retrospective** spec: the implementation exists and its behavior was pinned first by
[`install.characterization.md`](install.characterization.md), so this describes a contract that
already holds rather than proposing one. Approved by the author on 2026-07-27.

**Amended 2026-07-28 (`feat-0033`) on the author's explicit instruction, and re-approved.** S-013 and
S-014 add a profile axis, so a run can place a subset of the skills and report what that subset costs in
description characters. The amendment also records the constraint that decides how small a profile can
be, which is not a matter of preference: the skills reference each other, so a profile is only sound if
it is closed over those references.

**Amended 2026-08-05 (`feat-0036`) on the author's explicit instruction, following the `feat-0033`
precedent above. Pending the author's re-read: the amendment is written, the approval is not this
task's to grant.** S-015 adds a draft axis. The kit's own contribution bar (`AGENTS.md` section 7)
says a freshly drafted skill is not shipped until it has been used and refined, and until now that
distinction lived only in prose (`ROADMAP.md`, `docs/CATALOG.md`), so no tool could act on it and
this one placed every skill it found. The amendment also states what happens where the draft axis
and the closure of S-013 disagree, because both silent resolutions are defects.

**Amended 2026-08-07 (`bug-0018`) on the author's explicit instruction, given 2026-08-07 and
recorded in that task. Pending the author's re-approval: the amendment is written, the approval is
not this task's to grant.** `S-016` to `S-018` and Goal 10 add the adopted-versus-derived axis to
placement, and the Proposed Surface gains `--replace-adopted`. The contract said what happens to a
target the tool did not place (`S-004`) and nothing about a target it *did* place and the adopter
then edited, so the implementation removed and replaced the rules module on every re-run, destroying
an adopter's own lens silently at exit 0. `build-adapters.md` `S-010` and `S-014` already draw this
line for the other half of the distribution story; these scenarios draw the same line here rather
than a second one.

**Amended 2026-11-23 (`feat-0079`), under the 2026-11 overhaul plan the maintainer approved that
day. Pending the maintainer's approval of this amendment itself: the plan approved the work, and
the wording below is not this task's to approve.** `S-019` to `S-023` close the two hazards the
2026-11 audit reproduced and add three requests. An existing rules directory the tool did not place
is merged into file by file rather than refused whole (`S-019`), which narrows how `S-004` applies
to that one module without changing what it protects. A same-named symlink pointing elsewhere is a
conflict (`S-020`), which `S-004` always said and `_place()` did not do. `--include-drafts`
(`S-021`) lets a person try a draft, which amends `S-015`'s "placed by no profile" to "placed by no
profile unless asked"; `--skills` (`S-022`) places a named set and its closure; and a skill declaring
`metadata.invocation: user` reaches Claude Code rendered (`S-023`). The Non-Goal that kept the draft
axis out of adapter generation is withdrawn: `build-adapters.md` is amended by the same task.

**Amended 2026-11-23 (`chore-0033`) on the author's explicit instruction, which that task file
carries. Pending the author's re-approval: the amendment is written, the approval is not this
task's to grant.** The implementation was ahead of its contract and this moves the contract, not the
code. `S-024` to `S-027` state `--check`, which `chore-0031` shipped and `bug-0020`, `bug-0022` and
`bug-0056` refined, including how it treats the adopted rules module, in the terms `S-016` and
`build-adapters.md` `S-010` and `S-014` already use. `S-028` states `--with-hooks` (`feat-0038`):
placed, recorded, and not activated. `S-029` states what every command does with a record that parses
but is the wrong shape (`bug-0024`). The Proposed Surface gains both flags and a `Hooks module`
element, and its `Record` row now describes the per-file digest map every entry carries. Each exit
code in these scenarios was confirmed by running the tool against throwaway homes on 2026-11-23.

**Amended 2026-11-24 (`feat-0094`), under the Marjana plan the maintainer approved that day.
Pending the maintainer's approval of this amendment itself: the plan approved the work, and the
wording below is not this task's to approve.** `S-014`'s budget is what an agent carries: the
headline and every per-profile figure count model-invoked descriptions only, and the user-invoked
share is reported beside them rather than inside them. Since `S-023` a user-invoked skill reaches
Claude Code rendered so that its description is never loaded, so the old headline overstated a
session's cost by every user-invoked description in the profile (747 characters on `spine` and 1,586
on `all`, measured 2026-11-24). The same amendment adds one closing line to an install run: a pointer
to the per-repository setup step, because placing the skills is half of adopting them.

**Amended 2026-07-28 (`bug-0003`) and re-approved by the author on 2026-07-28.** S-007 was scoped to
the home it was given and S-012 was added. The original wording, "remove the recorded targets and empty the record",
was satisfied by an implementation that removed every recorded target from every home ever installed
to from this checkout, which destroyed a working installation while reporting success. The contract
never said what `--uninstall` should do when the record spans more than one home, so the code was not
diverging from it. This amendment states it.

## Problem

The kit's skills are useless until a harness can find them. Claude Code and OpenCode both discover
skills from a directory, so placing the canonical directories is the whole job, and this is the tool
that does it.

Two things about that job are easy to get wrong and were both got wrong at some point. A skill is not
self-contained: twelve of them compose a swappable rules module through a relative reference, and
until 2026-07-27 the tool shipped the skills without it, so the most rubric-dependent skill in the kit
arrived with an empty reference where its severities should have been. And placing files into a
directory a user owns means every write is a chance to destroy something the user put there, so what
the tool refuses to touch matters more than what it places.

Neither property is asserted anywhere a reader can check. The rules module's location looks arbitrary
rather than derived from what the skills reference, and the rule that an unmanaged target is never
overwritten exists only as a branch.

## Goals

1. Place every skill where each requested harness discovers it, from the single canonical source.
2. Place the rules module where the skills' own references resolve to, so a composed lens is never
   dangling once installed.
3. Be safe to run repeatedly, recognising the tool's own previous targets rather than refusing them.
4. Never modify or remove anything the tool did not place.
5. Support previewing a run and reversing a completed one.
6. Fail clearly on an unusable invocation rather than placing part of it.
7. Work out of the box on Windows, macOS, and Linux, since a portability promise that starts with a
   failed install is not one.
8. Let a run place a coherent subset of the skills rather than all of them, and say what the subset
   costs, because every installed description is loaded so an agent can route to it and that budget is
   shared with skills this tool cannot see.
9. Distribute only the skills the kit considers shipped, so a draft in the tree is never handed to an
   adopter as though it were blessed.
10. Keep what an adopter made their own, while still refreshing what they did not touch. Goal 4
    covers a target the tool never placed; this covers one it placed and the adopter then edited,
    which is a different question and the one the swappable rules module makes unavoidable.

## Non-Goals

- Generating project-level adapters for harnesses that read repository configuration. That is
  `build-adapters.py`. **The draft axis of S-015 deliberately stops at this tool's boundary and is not
  carried into adapter generation**, decided 2026-08-05 (`feat-0036`) and recorded here rather than
  left in a report, since a decision nobody can find later is one that gets re-made. Three reasons, in
  order: `build-adapters.py` has its own approved contract, and extending the axis to it is that
  contract's amendment to make, not this one's; this tool distributes to an adopter's global discovery
  directory, where an unblessed skill arrives looking blessed, while adapter generation writes into one
  named project at the request of whoever runs it; and the two failure modes differ, since an adapter
  is a derived artifact regenerated on demand rather than something an adopter's harness silently keeps
  loading. The inconsistency is real and is worth its own task: a maintainer who wants a draft withheld
  everywhere should amend `build-adapters.md` too. **Withdrawn 2026-11-23 (`feat-0079`, `chore-0077`):**
  `build-adapters.md` now withholds drafts by the same rule, because the plugin target it generates is
  distributed exactly as this tool's output is.
- Judging whether a skill is well-formed. That is `validate-skills.py`.
- Installing dependencies, or changing any harness setting beyond placing directories where it looks.
- Managing, updating, or removing skills the tool did not place, including a user's own.

## Constraints

- Standard library only.
- A skill references the rules module relatively, from inside its own directory. The module's install
  location is therefore not a choice: it is wherever those existing references resolve to.
- Symlink creation requires privilege on Windows that a normal account may lack, so the two placement
  modes are not interchangeable and the default depends on the platform.
- Re-run recognition needs a record of what the tool created, because a copied directory is
  indistinguishable from a user's own. That record is the manifest, and its presence is therefore part
  of the observable contract rather than an internal detail. Symlink mode can recognise its own links
  directly and does not depend on it.
- Skills reference each other as `../<name>/SKILL.md`, and some of those references are load-bearing:
  a skill may compose a sibling's discipline by reference and deliberately not restate it. A subset that
  omits a referenced sibling therefore ships the same dangling-reference defect the kit's own validator
  raises as an error. Any subset this tool places must be closed over those references.
- Whether a skill is a draft is a property of the skill, so it has to be carried by the skill itself
  rather than by a list inside this tool or by prose in a planning document. A list here is a second
  source of truth that drifts from `ROADMAP.md`; parsing prose makes placement depend on wording. The
  marker's spelling is constrained from outside: the skill frontmatter schema is an allow-list of six
  properties, of which `metadata` is the only one that can carry a status at all.
- The reference graph, and not editorial judgment, bounds the available subsets. Measured 2026-07-28 it
  has one strongly connected component of fourteen skills, every member of which reaches seventeen. The
  only separable skills are `agent-handoff` and `human-handoff` (a closed pair) and
  `init-worktracking`, `pr-describe`, and `project-bootstrap` (which reference no sibling). There is no
  useful middle size, and a profile set that pretends otherwise would be lying about what it installs.

## Scenarios

### Scenario S-001: each requested tool receives every skill

- **Given** a set of skills and one or more requested tools
- **When** the tool runs against a home directory
- **Then** every skill is placed under that tool's discovery directory, one per skill, and no
  directory is placed for a tool that was not requested.

### Scenario S-002: the rules module lands where the skills' references resolve

- **Given** skills that reference the rules module relatively from their own directories
- **When** the tool runs
- **Then** the module is placed such that those existing references resolve on disk, without the
  skills being rewritten.

### Scenario S-003: a re-run recognises the tool's own targets

- **Given** a home directory holding targets this tool placed on a previous run
- **When** the tool runs again with the same arguments
- **Then** it replaces or relinks those targets and reports doing so, rather than reporting a conflict
  against its own work, and exits zero.

### Scenario S-004: an unmanaged target is refused, not overwritten

- **Given** a file or directory at a target path that this tool did not place
- **When** the tool runs
- **Then** that path is left byte-for-byte unchanged, the conflict is reported naming it, and the run
  exits non-zero while continuing to place the targets that are free.

### Scenario S-005: a lost record makes previous copies unmanaged

- **Given** targets previously placed by copying, and a record of them that has since been deleted
- **When** the tool runs again
- **Then** those targets are treated as unmanaged and refused per S-004, because a copied directory
  carries nothing distinguishing it from a user's own.

### Scenario S-006: a preview run writes nothing

- **Given** any invocation requested as a preview
- **When** it completes
- **Then** no target and no record exists that the run would have created, and the reported outcome
  describes what would have been placed.

### Scenario S-007: reversing a run removes what it placed beneath the given home

- **Given** a completed run whose targets are recorded
- **When** the tool is asked to reverse it against the same home
- **Then** each recorded target beneath that home is removed, those entries leave the record, and
  nothing the tool did not place is touched.

### Scenario S-008: reversing with nothing recorded is not an error

- **Given** no record of any previous run
- **When** the tool is asked to reverse one
- **Then** it reports that nothing is recorded and exits zero.

### Scenario S-012: reversing one home leaves another home's installation intact

- **Given** completed runs against two different homes, both recorded
- **When** the tool is asked to reverse one of them
- **Then** only that home's targets are removed, the other home's targets remain on disk and remain
  recorded, and a later reversal of the other home still finds them.

### Scenario S-009: an unrecognised tool is rejected before anything is placed

- **Given** a requested tool that is not supported, alone or alongside a supported one
- **When** the tool runs
- **Then** it names the unrecognised tool and the supported ones, places nothing, and exits non-zero.

### Scenario S-010: the placement mode defaults to what the platform can do

- **Given** no explicitly requested placement mode
- **When** the tool runs
- **Then** it copies on Windows and links elsewhere, because symlink creation there requires privilege
  a normal account may lack.

### Scenario S-011: a failed link reports what to do instead

- **Given** a requested link mode on a system that refuses to create symlinks
- **When** placement is attempted
- **Then** the run stops with a message naming the alternatives available to the user, rather than an
  unhandled error.

### Scenario S-013: a profile places a closed subset, and says when it grew the request

- **Given** a requested profile naming a set of skills
- **When** the tool runs
- **Then** it places that set expanded to its closure over sibling references, so no placed skill
  references a skill the same run did not place, and it reports the expansion when the closure added
  anything to what was asked for. An unrecognised profile is named, nothing is placed, and the run exits
  non-zero, as for an unrecognised tool.

### Scenario S-014: the run reports what the profile costs in description characters

- **Given** any run that places skills
- **When** it reports its outcome
- **Then** the summary states the total description characters for the profile being placed, and the
  same total for each available profile so the figure is comparable rather than absolute. It is reported
  as a character count and not as a proportion of any harness's budget, which depends on the context
  window and on skills this tool cannot see.
- **And** every one of those totals counts model-invoked skills only, because a user-invoked skill's
  description is not loaded (`S-023`). When the placed set holds a user-invoked skill, a separate line
  states their combined characters and names them, as an aside to the total rather than part of it.
- **And** an install run, real or dry, ends with one line pointing at the per-repository setup step:
  in each repository, run `init-worktracking` once to configure the skills. `--check` and
  `--uninstall` do not print it. (Added 2026-11-24, `feat-0094`.)

### Scenario S-015: a skill marked a draft is placed by no profile

- **Given** a skill whose own frontmatter marks it a draft
- **When** the tool runs with any profile, including the one that asks for everything
- **Then** that skill is placed for no requested tool, the run names what it held back rather than
  omitting it silently, the reported totals count it as discovered but not placed, and its description
  is excluded from every profile's budget, since no run can incur it.
- **And** a skill carrying no marker is placed exactly as before, because absence means shipped and a
  skill can therefore only ever be withheld deliberately. That direction is the one worth stating: the
  over-delivery this scenario prevents ships something extra and visible, while reading a marker too
  eagerly stops refreshing a skill an adopter already relies on, with nothing anywhere to say so.
- **And** when a skill the profile would place references a draft, or when the profile's own requested
  set names one, nothing is placed and the run exits non-zero naming both skills. Both silent
  resolutions are defects: following the reference ships the draft the marker exists to withhold, and
  dropping it ships the dangling sibling S-013 exists to prevent. Which side is wrong, the marker or
  the reference, is a person's call and not this tool's.

### Scenario S-016: an adopted file the user edited is preserved, a derived one is refreshed

- **Given** a previously installed home in which the adopter has edited a file of the rules module,
  and a skill whose installed copy also differs from the kit's
- **When** the tool runs again
- **Then** the edited rules file is left byte-for-byte unchanged and the run reports having kept it,
  naming the file, while the skill's copy is replaced as before and the run exits zero.
- **And** a rules file the adopter **added** beside the kit's is neither removed nor recorded as the
  tool's, because it is not the tool's to manage in either direction.
- **And** a rules file the adopter has **not** touched is still refreshed when the kit's copy has
  changed, so accepting the invitation to edit one file does not pin the whole module to whatever
  shipped first. The two cases are told apart by whether the installed file still matches the digest
  recorded when it was placed, which is the same line `--check` draws between `diverged` and
  `revised`; comparing against the current source instead would preserve everything forever.
- **And** the distinction is a property of the material, not of the file's location: the rules module
  is **adopted**, which the kit invites and therefore may not overwrite, and a skill's contents are
  **derived**, which the kit owns and must keep current. `build-adapters.md` `S-010` and `S-014`
  state the same contrast for the other distribution path, and this scenario does not restate it
  differently.

### Scenario S-017: an install with no recorded baseline preserves rather than guesses

- **Given** an installed home whose record predates the per-file digests, so nothing says what the
  adopted module looked like when it was placed
- **When** the tool runs again
- **Then** every file of that module is left as it is, the run states that the baseline is unknown
  rather than reporting the module as current or as edited, and no baseline is invented for it.
- **And** the reason is that the two errors do not cost the same: preserving a file that was never
  edited costs a stale lens the adopter can see, while overwriting one that was costs work that
  cannot be recovered.

### Scenario S-018: an adopter can ask for the kit's copy explicitly

- **Given** an installed rules module the adopter has edited and now wants replaced by the kit's
- **When** the tool runs with the option that requests exactly that
- **Then** the kit's copies are placed over theirs, the record carries the newly placed digests as
  the baseline, and the option is its own named flag rather than a value of the placement mode,
  since it decides what happens to the adopter's work rather than how files are placed.

### Scenario S-019: an existing rules directory the tool did not place is merged into, file by file

- **Given** a real directory at the rules module's target that this tool did not place, holding files
  of the adopter's own, one of which has the same name as a lens the kit ships
- **When** the tool runs
- **Then** every lens whose path is free is placed into that directory, the file at the clashing path
  is left byte-for-byte unchanged and reported as a conflict naming it, the adopter's other files are
  never read or touched, and the run exits non-zero per `S-004` while placing the rest.
- **And** a file already there with exactly the kit's content is not a conflict and is not recorded as
  the tool's, since nothing was placed.
- **And** reversing the run removes only the files the tool placed and nobody has edited since, and
  never the directory, because the directory is not the tool's.
- **And** a re-run treats the files it placed by `S-016`'s rules: untouched is refreshed, edited is
  kept. The reason for the change: refusing the directory whole left every skill that composes a lens
  running without one, to protect files a per-file placement never touches.

### Scenario S-020: a same-named symlink pointing elsewhere is a conflict

- **Given** a symbolic link at a skill's target that points somewhere other than the kit's source
- **When** the tool runs in symlink mode
- **Then** the link is left pointing where it did, the target is reported as a conflict, and the run
  exits non-zero per `S-004`,
- **unless** the record names that target as this tool's, linked to the source it now points at,
  which is the tool's own link left behind by a moved checkout, and is relinked per `S-003`.

### Scenario S-021: drafts are placed when asked for, and named

- **Given** skills marked a draft, and a run requesting drafts
- **When** the tool runs with a profile
- **Then** every draft is placed together with the profile's set, all of it closed over sibling
  references per `S-013`, and the run names each placed draft on its own line and in a summary.
- **And** with a named set (`S-022`), drafts may appear in the named set and its closure, and the
  drafts outside it are not added.
- **And** without the request, `S-015` holds unchanged.

### Scenario S-022: a named set of skills is placed with its closure

- **Given** one or more skill names in place of a profile
- **When** the tool runs
- **Then** it places those skills expanded to their closure over sibling references and prints the
  closure before placing anything.
- **And** an unknown name, a named draft without the drafts request, or a profile requested alongside
  the names places nothing and exits non-zero, naming what is wrong.

### Scenario S-023: a user-invoked skill reaches Claude Code rendered, and only Claude Code

- **Given** a skill declaring `invocation: user` under `metadata`
- **When** the tool places it for Claude Code
- **Then** the placed `SKILL.md` carries `disable-model-invocation: true` as a top-level frontmatter
  key and is otherwise byte-identical to the source, and the placement is a copy in either mode,
  since a link would show the unrendered source.
- **And** every other tool receives the source unchanged, because the key is legal only for Claude
  Code and claude.ai rejects it.
- **And** the record carries the rendered digests, so the staleness check reports a rendered copy
  that has fallen behind its source as diverged, and reports a linked skill whose source has since
  become user-invoked as needing a rendered copy.

### Scenario S-024: `--check` reports a current install as current, and writes nothing

- **Given** a home holding targets this tool placed and recorded, none of which has changed since,
  and a kit whose copies have not changed since either
- **When** the tool is run with `--check` against that home
- **Then** it reports one line per recorded target beneath that home, each `ok`, followed by a count
  per status, and exits zero.
- **And** a target that is a symbolic link to its own source is reported `linked` rather than
  compared, because it is the source and cannot be stale, and it does not change the exit code.
- **And** the check writes nothing, whatever it finds: no installed file and no byte of the record.
  An adopter may have edited an installed file on purpose, so whether to re-install is a person's
  call and never this mode's.
- **And** it reads only the entries beneath the home it was given, per `S-012`, so the state of
  another recorded home never changes this one's answer.

### Scenario S-025: a derived target that no longer matches the kit is named, with both digests, at exit 1

- **Given** an installed skill, or an installed hooks module, whose files differ from the kit's
  current copy, because an installed file was edited, the kit's file was revised, or a file exists on
  one side only
- **When** the tool is run with `--check`
- **Then** that target is reported `diverged`, naming each differing file with an abbreviated digest
  of the installed copy and of the kit's, the targets that still match are reported `ok`, and the run
  exits 1.
- **And** a target removed from disk altogether is reported `diverged` and named, at exit 1, because
  absence is a divergence a check that only opens the files it can find would miss.
- **And** a user-invoked skill's copy is compared against the rendered bytes a re-install would
  place, per `S-023`.

### Scenario S-026: a check that cannot answer says so at exit 2, which outranks a divergence

- **Given** a recorded entry beneath the home that carries no per-file digests, because it predates
  them or its map is empty
- **When** the tool is run with `--check`
- **Then** that entry is reported `unknown`, never `ok`, and the run exits 2, because a clean result
  for a state nobody recorded is the silence the check exists to remove.
- **And** the remedy is stated per entry: a derived entry is told to re-install, and the adopted rules
  module is told to run `--replace-adopted`, because re-installing that module preserves it and
  records nothing, per `S-017`.
- **And** an entry whose source no longer exists in the kit is reported `error`, at exit 2, for the
  same reason: nothing could be compared.
- **And** when nothing is recorded beneath the home at all, the run says nothing can be checked and
  exits 2, not zero. An empty record cannot be told from a deleted one (`S-005`), so it says nothing
  about what is on disk.
- **And** within one run exit 2 outranks exit 1, since a report holding an unanswerable entry cannot
  be trusted as a whole. `--check` given together with `--uninstall` is refused at exit 2 with
  nothing removed, because either precedence drops half the request and one half deletes files.

### Scenario S-027: `--check` faults an adopted file only when the kit's copy moved and the file is untouched

- **Given** an installed home whose rules module carries a recorded baseline
- **When** the tool is run with `--check`
- **Then** a rules file the adopter edited is not a fault while the kit's copy of it has not moved
  since the install: the module is reported `ok` and the run exits zero.
- **And** when the kit's copy has moved since the install, the installed file is compared against the
  baseline recorded when it was placed, never against the kit's current copy. Where every file the
  kit revised still matches its baseline, nothing of the adopter's is at stake and the installed copy
  is simply stale, so the module is reported `diverged` at exit 1. Otherwise the module is reported
  `revised` at exit zero, naming which revised files are the adopter's and which a re-install would
  refresh; that includes the case where what moved is only a file the kit added or stopped shipping.
- **And** a file this install placed that is now missing from the installed module is reported
  `diverged` at exit 1, naming it, while a file the adopter added beside the kit's is ignored in both
  directions.
- **And** this is the same line `S-016` draws for placement and `build-adapters.md` `S-010` and
  `S-014` draw for the other distribution path. The rules module is **adopted**, so an adopter's edit
  is theirs and is never reported as a fault, and only the kit's own untouched copy falling behind is.
  A skill's contents are **derived**, so any difference is reported, per `S-025`.

### Scenario S-028: `--with-hooks` places the hooks module and activates nothing

- **Given** a run requesting `--with-hooks` for one or more tools
- **When** the tool runs
- **Then** the kit's hooks module is placed for each requested tool at that tool's own hook path,
  recorded as one entry carrying a digest per file like any derived target, and the summary counts
  the hooks placed.
- **And** nothing is activated: no harness settings file is created or edited. For Claude Code the
  run says the hooks are inactive and prints the registration block a person would merge into their
  settings; for OpenCode it says where the module landed and whether the plugin that would read it is
  present there, reporting the placement `LIVE` or `INERT`. Every tool that received the module is
  told about it.
- **And** without the flag no hooks module is placed or recorded, a preview places and records none
  per `S-006`, a re-run replaces the module rather than reporting a conflict per `S-003`, and
  `--uninstall` removes it per `S-007` with no flag of its own.
- **And** the reason activation stays with a person: a hook is the only thing the kit ships that runs
  inside an adopter's session, and editing their settings is a harness setting change the Non-Goals
  rule out and the record could not cleanly reverse.

### Scenario S-029: a record that parses but is the wrong shape stops every command at exit 2

- **Given** an install record that parses as JSON but is not shaped like one: it has no `entries`
  list, an entry that is not an object, an entry with no `target` or a `target` that is not a
  non-empty string, or an optional field of the wrong type
- **When** the tool is run in any mode: placing, `--uninstall`, or `--check`, previewed or not
- **Then** it names the record's path and what is wrong with it, down to the offending entry by index
  and by name where it has one, places nothing, removes nothing, checks nothing, leaves the record
  byte-for-byte unchanged, and exits 2.
- **And** 2 rather than 1, because 1 means `--check` found a divergence and here nothing was compared.
- **And** a placing run refuses rather than reading the record as empty, because proceeding would
  write a fresh record over the damaged one and lose every target it records under other homes, the
  one irreversible outcome available.
- **And** a record whose bytes do not parse at all is read as no record, as a deleted one is per
  `S-005`, since it never named an install; and a key the tool does not recognise leaves a record
  valid, so a record written by a later version is not mistaken for damage.

## Proposed Surface

| Element | Detail |
|---|---|
| Invocation | `python scripts/install.py [--tools <list>] [--profile <name> \| --skills <list>] [--include-drafts] [--mode <symlink\|copy>] [--home <dir>] [--dry-run] [--with-hooks] [--replace-adopted] [--uninstall \| --check]` |
| `--tools` | Comma-separated subset of the supported tools; defaults to all of them |
| `--profile` | Which skills to place: `core` (the separable front door), `spine` (the delivery loop), or `all`. Defaults to `spine`, which is smaller than `all`. Each is expanded to its closure over sibling references before anything is placed |
| `--skills` | Comma-separated skill names placed with their closure over sibling references, per S-022. Replaces `--profile` |
| `--include-drafts` | Also place draft skills, per S-021 |
| `--mode` | `symlink` or `copy`; defaults to copy on Windows and symlink elsewhere. A user-invoked skill is copied for Claude Code in either mode, per S-023 |
| `--home` | Base directory to install beneath; defaults to the user's home |
| `--dry-run` | Preview: report what would be placed, write nothing |
| `--replace-adopted` | Overwrite the installed rules module with the kit's copy, discarding the adopter's edits to it. Its own flag and not a `--mode` value, per S-018. Without it, an edited file is preserved and reported |
| `--uninstall` | Remove the recorded targets beneath `--home` and drop those entries from the record, leaving entries for other homes |
| `--check` | Report, per recorded target beneath `--home`, whether it still matches the kit, as `ok`, `linked`, `revised`, `diverged`, `unknown`, or `error`, per S-024 to S-027. Writes nothing. Refused alongside `--uninstall` |
| `--with-hooks` | Also place the hooks module, per S-028. Opt-in: it is placed and recorded, and the run prints how to activate it rather than activating it |
| Placed per tool | Each skill's directory under that tool's discovery path, plus the rules module as their sibling |
| Hooks module | With `--with-hooks` only: the kit's `.agents/hooks/` placed at `<home>/.claude/hooks` for Claude Code and `<home>/.agents/hooks` for OpenCode, recorded as one entry named `hooks`. Derived, like a skill directory, so a re-run replaces it and `--check` compares it per S-025. No settings file is written |
| Adopted material | The rules module only. Placed file by file so an untouched file can be refreshed while an edited one beside it is kept, and so a file the adopter added is left alone. Skill directories are derived and are replaced wholesale |
| Draft marker | Carried by the skill itself, in the `metadata` frontmatter property the skill schema permits: `metadata.status: draft`. No marker, or any other value, means shipped |
| Invocation marker | Carried by the skill: `metadata.invocation: user`. Rendered as `disable-model-invocation: true` into the Claude Code copy only, per S-023 |
| Merged rules module | A rules directory the tool did not place is recorded with mode `merged` and only the files the tool placed, per S-019 |
| Record | A manifest of the targets this tool created, enabling re-run recognition in copy mode. Each entry names its target, tool, name, placement mode, and source, and carries a per-file digest map: the SHA-256 of every file placed, keyed by its path relative to the target (for a rendered copy, the rendered bytes, per S-023). The map is the baseline `--check` compares against and the line S-016 draws between an untouched and an edited adopted file. An entry without one has no baseline (S-026). A record that parses but is the wrong shape stops every command (S-029); one that does not parse is read as no record (S-005) |
| Exit code | non-zero on an unrecognised tool or profile, a profile colliding with a draft marker, or any unmanaged-target conflict, zero otherwise. For every command, 2 when the record parses but is the wrong shape, before anything is placed, removed, or checked (S-029). For `--check`: 0 when every entry beneath the home is `ok`, `linked`, or `revised`; 1 when one is `diverged`; 2 when one is `unknown` or `error`, when nothing is recorded beneath the home, or when it is combined with `--uninstall`, 2 outranking 1 (S-024 to S-027) |
| Output | one line per target with its outcome, then a summary carrying the placed count and the description-character total per profile; conflicts, any closure expansion, any skills held back as drafts, and any adopted file preserved rather than replaced additionally summarised, the last named per file. With `--with-hooks`, one activation note per tool that received the module (S-028). For `--check`, one line per recorded target beneath the home carrying its status and what differs, then a count per status and a remedy line for each of `diverged`, `revised`, and `unknown` that is present |

A note on what the default change does **not** do, because the quiet version of it would be a defect.
Defaulting to `spine` means `agent-handoff` and `human-handoff` stop being refreshed by a default run.
It does not remove them: this tool only places and updates, reversal is `--uninstall`, and both the
directories and their manifest entries survive. An adopter who installed them before this change keeps
them, unchanged, until they pass `--profile all`.

## Open Questions

1. **Should the record live inside the kit repository?** It currently does, which means installing
   from a read-only or shared checkout cannot record what it placed, and a user who reclones loses
   re-run recognition for targets that still exist. Recommendation: leave it as is for now, since the
   failure is visible (targets become conflicts per S-005) rather than silent, and moving it into the
   home directory would make one manifest serve installs from several checkouts, which is a different
   and probably worse problem. Revisit if anyone installs from a shared checkout.
