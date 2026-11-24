---
id: chore-0033
title: The install contract's Proposed Surface is two flags behind the CLI it describes
type: chore
status: done
priority: P2
parent: "ROADMAP Epic A: broadly shareable (the public kit)"
depends_on: []
touched_files:
  - docs/spec/install.md
  - docs/spec/install.conformance.md
  - docs/spec/README.md
created: 2026-08-06
---

## Problem

[`install.md`](../../docs/spec/install.md) is an approved contract, and its Proposed Surface table now
lists neither of two flags the tool actually has:

| Flag | Shipped by | Recorded in the spec |
|---|---|---|
| `--with-hooks` | `feat-0038` | no |
| `--check` | `chore-0031` | no |

The `Record` row is also stale in the same direction: it describes the manifest as "a manifest of the
targets this tool created", which stopped being the whole truth when `chore-0031` added a per-file
digest map to every entry.

**A contract that under-describes its implementation is the failure `chore-0027` closed for two other
specs**, and its reasoning applies unchanged: a wrong contract is worse than a missing one, because
the next audit re-derives the same divergence and a reader trusting the spec is misled. Both
divergences here are the implementation being deliberately ahead of its contract, so the spec moves
and no code does.

**Neither omission was an oversight by the task that caused it, and that is the point.** `feat-0038`
shipped `--with-hooks` without amending. `chore-0031` declined to amend deliberately and recorded
why: every amendment in `install.md` carries "on the author's explicit instruction" (lines 13, 19,
27), and that task carried none. `feat-0034` amended `build-adapters.md` in the previous wave only
because its task file stated the author had authorised it. So the convention is working as designed,
and the backlog it produces is the thing that needs draining, one flag at a time or one task like
this one.

Found by `chore-0031`'s verification on 2026-08-06, which flagged the surface as diverged and
dispositioned it accepted-with-reason rather than to-fix.

## Scope

**In scope:** amend `docs/spec/install.md` with scenarios for `--check` and `--with-hooks`, extend the
Proposed Surface table with both flags and the manifest's digest map, add a dated amendment note in
the form the existing three use, and update
[`install.conformance.md`](../../docs/spec/install.conformance.md) with a row per new scenario and a
recomputed coverage proof.

**This task carries the author's instruction to amend**, which is what the other three amendments in
that file each record and what `chore-0031` correctly declined to assume.

**Leave `status: approved` exactly as it is**, and mark the new note as pending the author's
re-approval in its own text, per the convention `chore-0030` recorded in
[`docs/spec/README.md`](../../docs/spec/README.md). Flipping the field to `draft` makes `verifier-agent`
return `blocked` on the run verifying this very task. Add the row to that file's re-approval queue.

**Out of scope:**

- Any change to `scripts/install.py`. The implementation is correct; the contract is behind it.
- Re-approving this or any other spec, which is the author's.
- The behaviour of `--check` itself, including the adopted-lens carve-out, which `chore-0031`
  verified and `bug-0020` refines.
- The other amended specs in the queue.

## Decisions

- **2026-11-23: worked by the release-readiness session, which delegated the drafting to a subagent
  and verified it; the scenario ids differ from what this file predicted.** The next free id was
  `S-024`, not `S-016`, because `bug-0018` and `feat-0079` took `S-016` to `S-023` first. Six scenarios
  landed: `S-024` current, `S-025` diverged at exit 1 with both digests, `S-026` cannot-answer at exit
  2 (including nothing recorded, which exits 2 rather than 0), `S-027` the adopted rules module,
  `S-028` `--with-hooks` placed and not activated, and `S-029` a record that parses but is the wrong
  shape (the `bug-0024` behaviour from the Decision above). Every exit code was confirmed by running
  the tool against throwaway homes; `S-029` was re-run independently by the session (install,
  `--check` and `--uninstall` each exit 2, the record's SHA-256 unchanged, nothing placed).
- **The implementation note that the kit's copy moving under an adopted file is "reported
  exit-neutrally" is out of date**, because `bug-0056` narrowed it: an untouched lens that has fallen
  behind is `diverged` at exit 1, and only a lens with the adopter's edits at stake is `revised` at
  exit 0. `S-027` follows the code and `S-016`'s wording, and the matrix row says so.
- **Owed, and not done here:** tagging the tests in `tests/test_install.py` with `S-024` to `S-029`
  (the `HookPlacementTests` docstring still says the spec "says nothing about hooks"), and tests for
  three paths confirmed only by running the tool: a source missing from the kit giving `error`, a
  pre-existing settings file left byte-identical by `--with-hooks`, and a real `--uninstall` over a
  damaged record. No Goal in `install.md` names the staleness check or the hooks, which
  `spec-quality` may flag; adding one was outside this task.

- **2026-08-20: one more surface to add, found by `bug-0024`.** That task made a structurally invalid
  manifest exit 2 naming the offending entry, across `--check`, `--uninstall` and install, and the
  contract does not describe that behaviour at all. Its agent recommended a scenario for it and could
  not write one, since `docs/spec/install.md` is outside its `touched_files` and this task already owns
  the file. Add it in the same pass as the two flags: an unreadable-but-parsing manifest exits 2,
  places nothing, and leaves the record byte-identical. Its tests are ready to tag with the id.


- **2026-08-20: `touched_files` corrected before dispatch, and the task deferred one wave because of
  it.** Acceptance criterion "`docs/spec/README.md`'s re-approval queue gains the row" required
  editing a file the surface did not declare. That is the same authoring defect that let `chore-0034`
  and `chore-0043` collide in that paragraph undetected on 2026-08-19, and it is invisible to the
  pre-dispatch overlap check, which reads `touched_files`. Declared now. The consequence is that this
  task collides with any sibling amending a spec in the same wave, which is why it was held out of the
  2026-08-20 wave in favour of `chore-0047`, which needs that file for two reasons rather than one.

## Implementation notes

**Write the scenarios from what was verified, not from the code.** `chore-0031`'s verification
established the behaviour that matters at contract level: a fresh install reports current and exits
zero; a diverged file is named with both digests and exits 1; a manifest with no digests reports
`unknown` rather than `current` and exits 2; a symlinked target cannot be stale; an adopter-edited
rules file is not faulted, while the kit's copy moving underneath it is reported exit-neutrally. That
last pair is the contract-level statement of the adopted-versus-derived distinction
[`build-adapters.md`](../../docs/spec/build-adapters.md) already draws in `S-010` and `S-014`, and the
two specs should read consistently.

**`--with-hooks` needs less.** It places the hooks module and prints the registration rather than
editing anyone's settings, which `AGENTS.md` already states as the opt-in contract. One scenario
covering "placed, not activated" is the load-bearing half.

**Next free scenario id is `S-016`**, since `feat-0036` took `S-015`. Check rather than assume.

**Do not extend the conformance matrix's coverage proof by hand-waving.** `feat-0036`'s closeout
records a matrix asserting it had audited "S-001 through S-014, every spec item" beside a spec
carrying fifteen. State both counts and the arithmetic.

## Risks and rollback

Required: this amends an approved contract.

The risk is amending in a way that pins behaviour the implementation does not actually have, which
turns a lagging contract into a wrong one. Every scenario must be checkable against the current code,
and the conformance row must cite a real code location. Rollback is one revert; no code depends on
the spec text.

## Acceptance criteria (mechanically verifiable)

    python scripts/validate-skills.py && python .tasks/validate.py --strict && python -m unittest discover -s tests -p "test_*.py"

- [x] `docs/spec/install.md` carries a scenario for `--check` covering, at minimum, current,
      diverged, and no-baseline, each with its exit code.
- [x] It carries a scenario for `--with-hooks` stating that hooks are placed and not activated.
- [x] The adopted-versus-derived treatment of the rules module is stated at contract level and does
      not contradict `build-adapters.md` `S-010` and `S-014`.
- [x] The Proposed Surface table lists both flags and describes the manifest's digest map.
- [x] Scenario ids continue from the highest already in the file, with no reuse.
- [x] A dated amendment note is added in the form the existing three use, marked pending the
      author's re-approval, and `status:` still reads `approved`.
- [x] `docs/spec/README.md`'s re-approval queue gains the row.
- [x] `install.conformance.md` has a row per new scenario with evidence by code location, and its
      coverage proof states both counts and the arithmetic.
- [x] No change to `scripts/install.py`.
- [x] Existing tests still pass, unchanged in intent.

## Definition of done

- [x] Acceptance command(s) pass locally.
- [x] Conventions in AGENTS.md's conventions section followed.
- [x] `doc-sync` run over the reader-facing documents and its findings applied or dismissed with a
      reason.
- [x] File moved to `.tasks/done/`, `status: done`, **with its relative links re-anchored for the
      extra directory level**; one dated line added to `CHANGELOG.md` referencing this task id.

## Closeout (2026-11-23)

`install.md` carries `S-024` to `S-029`, the `--check`, `--with-hooks` and `Hooks module` surface
rows, a `Record` row describing the per-file digest map, and a dated amendment note pending the
author's re-approval; `status: approved` is unchanged and no `approved_digest` was added.
`install.conformance.md` has a row per new scenario and surface element, evidence by code location,
and a coverage proof of 26 of 29 scenarios (S-001 to S-015, S-019 to S-029; S-016 to S-018 still
unaudited) and 19 of 21 surface elements. `docs/spec/README.md`'s queue row and its scenario-count
table gained the amendment. `python scripts/validate-skills.py`, `python .tasks/validate.py --strict`,
`python scripts/check-citations.py` and `python -m unittest tests.test_install` pass; the full
unittest run fails only in `tests/test_hooks_instruction_provenance.py`, which a sibling session owns
and this task did not touch. No change to `scripts/install.py`.
