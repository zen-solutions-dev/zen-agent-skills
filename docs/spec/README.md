# Specifications

The behavioral contracts this kit builds and verifies against, plus the reports that sit beside
them. A spec says **what** should be true and **why**; it is not a plan, an architecture brief, or a
task list.

Specs are drafted by [`spec-author`](../../.agents/skills/spec-author/SKILL.md), reviewed by
[`spec-quality`](../../.agents/skills/spec-quality/SKILL.md), and approved by a human. Nothing is
decomposed into tasks until `status: approved` is set, and `spec-author` never sets it itself.

## Amending a spec that is already approved

The lifecycle is `draft` then `approved`, and it stops there. It carries no value for the state that
keeps recurring: **approved, then amended, with the amendment not yet re-approved.** A task that
implements a feature and extends its contract in the same pass is the normal shape of work here, so
this is a permanent, common state rather than a queue that will one day be empty.

The convention, in use since 2026-07-27 and written down here on 2026-08-06 (`chore-0030`):

1. **Leave `status: approved`, and any `approved_digest`.** The fields record the last contract a
   human agreed to and the exact text they read, which stays true of everything the amendment did
   not touch.
2. **Add a dated note to the spec's header**, under the existing approval line, naming the date, the
   amending task's id, and the scenarios or sections that changed. State the pending state in the
   words **pending the author's re-approval**, so the queue is at least findable with a search.
3. **Repeat it in any sibling report** whose rows audit the amended clauses, so a matrix is not read
   as auditing an approved contract in full.
   [`build-adapters.conformance.md`](build-adapters.conformance.md) and
   [`install.conformance.md`](install.conformance.md) both do this.
4. **Re-approval is the author's**, granted by re-reading the spec, recording the digest
   `spec-author`'s [`spec_digest.py`](../../.agents/skills/spec-author/scripts/spec_digest.py) prints
   for it as `approved_digest`, and editing the note. No agent grants it, and no agent changes
   `status` or `approved_digest`: changing the digest so a check passes is editing the judge
   (`A11`).

### Why an amended spec does not go back to `draft`

This is a mechanical constraint, not a preference.
[`verifier-agent`](../../.agents/skills/verifier-agent/SKILL.md) returns `blocked` on a spec whose
`status` is not `approved`, so a task that amends a contract and flips its status makes the
verification run for that very change unanswerable, and the amendment can never be verified into
place. [`new-task`](../../.agents/skills/new-task/SKILL.md) separately refuses to decompose an
unapproved spec, so one changed scenario would stall every other task waiting on the same contract.
Reopening to `draft` was tried once, on [`house-review`](house-review.md) (`chore-0012`), and the
note recording it is still in that spec's header.

**Since 2026-11-23 (`feat-0083`) a bound spec stalls anyway, and on purpose.** An approved spec that
carries an `approved_digest` reads `changed` once amended, and `verifier-agent`, `new-task`,
`spec-plan-readiness`, and `test-author` block on it until the author re-approves. That is the stall the paragraph
above avoided, chosen deliberately by the maintainer: verifying or decomposing against text nobody
approved launders it into evidence, which is the reason `verifier-agent` blocks on a draft at all.
Going back to `draft` still gains nothing, and loses the record of what was last approved.

### Why there is no third status value, and what the approval digest is

These read a spec's `status`: `verifier-agent` blocks on anything but `approved`; `new-task`
refuses to decompose it; `test-author` refuses to derive tests from it; `spec-plan-readiness` and
all three of those read it through `spec_digest.py`; [`doc-sync`](../../.agents/skills/doc-sync/SKILL.md) classifies a document
carrying one as a contract and therefore never edits it; the
[spec-closeout gate](../../.agents/hooks/spec-conformance-gate.py) tests it against a terminal-status
set that excludes `approved` on purpose, with a test pinning that; and the table below. A third value
would need a behavioural branch in every reader that compares against `approved`, plus a new concept
for every reader of every spec. So `status` keeps its two values.

What this page long called "the preferred form if this is ever mechanised", a separate frontmatter
key, exists since 2026-11-23 (`feat-0083`), with a stronger job than the one first imagined. It does
not name an amendment; it binds an approval to the text approved. `approved_digest` is the SHA-256 of
the spec's body as [`spec_digest.py`](../../.agents/skills/spec-author/scripts/spec_digest.py)
computes it, recorded by the author when approving. The script, which only reads, then answers for
any spec whether it is `bound` (the text matches), `unbound` (approved, tied to no text), `changed`
(edited since approval), or `malformed`, and lists the queue:

```bash
python .agents/skills/spec-author/scripts/spec_digest.py --queue docs/spec
```

**Every spec approved before 2026-11-23 is `unbound`**, by the maintainer's choice: each is bound when
the author re-reads it, rather than all at once, which would have declared every pending amendment
below approved without anyone reading it. So the protection reaches a spec only once it is re-read,
and until then the readers treat `unbound` as approved and say in their reports that it is tied to
no text. The table below stays as the record of **what** each pending amendment changed, which the
digest cannot say: it tells you that the text moved, not where.

### The author's re-approval queue

Every spec listed below is approved and carries an amendment the author has not re-read. Some carry
more than one: `install` carries two, `build-adapters` four, since `chore-0043`, again since
`chore-0062`, and again since `chore-0087`, `cloud-executable` three, since `chore-0061` and again
since `chore-0049`, and
`validate-skills` five, since `chore-0047`, again since `chore-0054`, again since `chore-0065`, and again since `feat-0064`.
The 2026-11 overhaul added a second to `house-review` (`feat-0078`), `spec-author` (`feat-0076`)
and `systematic-debugging` (`feat-0077`), and a first to `verifier-agent` (`feat-0077`); WS4 (`feat-0079`) added one more each to `install`,
`build-adapters` and `validate-skills`. `feat-0083`, the approval digest, added one more each to
`spec-author` and `verifier-agent`. `chore-0033` added a fourth to `install`, describing `--check`,
`--with-hooks`, and the damaged-record exit the implementation already had.

| Spec | Amendment | Amended |
|---|---|---|
| [`build-adapters`](build-adapters.md) | `S-015` to `S-017`, the `plugin` target (`feat-0034`); `S-018`, the code-span and fence exception (`chore-0043`); `S-019`, what a relative link inside an emitted lens must satisfy (`chore-0062`); `S-020` and the `Exit code` surface element, a destination outside the output root refused rather than written (`chore-0087`); `S-015`'s version clause, and `S-021` to `S-023`, drafts withheld, plugin-only rendering, and the committed marketplace with its drift check (`feat-0079`) | 2026-08-06, 2026-08-19, 2026-08-27, 2026-09-01, 2026-11-23 |
| [`cloud-executable`](cloud-executable.md) | `S-017` and `S-018` repointed from `bug-0018`, closed 2026-08-08, to the open `bug-0020` (`chore-0051`); `S-020` and the `Output` surface element, what a passing gate's entry carries (`chore-0061`); the `Gate set` surface element restated as a property rather than a count (`chore-0049`) | 2026-08-20, 2026-08-27, 2026-08-28 |
| [`doc-sync`](doc-sync.md) | `skipped` and `not_audited` split into two fields (`chore-0027`) | 2026-08-05 |
| [`house-review`](house-review.md) | `S-014` to `S-018`, the evidence gate and finding signature (`feat-0040`); `S-019` to `S-024`, the spec and standards axes and the depth selection absorbed from the retired `review-depth`, with `S-018` reworded and the spec-judgement non-goal narrowed (`feat-0078`) | 2026-08-05, 2026-11-23 |
| [`install`](install.md) | `S-015`, the draft-skill axis (`feat-0036`); `S-016` to `S-018`, Goal 10 and `--replace-adopted`, the adopted-versus-derived axis (`bug-0018`); `S-019` to `S-023`, the rules merge, a foreign symlink, `--include-drafts`, `--skills`, and invocation rendering, with the Non-Goal keeping drafts out of adapters withdrawn (`feat-0079`); `S-024` to `S-029`, `--check`, `--with-hooks`, and a record that parses but is the wrong shape, with the `--check`, `--with-hooks`, `Hooks module`, `Record`, `Exit code`, and `Output` surface elements (`chore-0033`) | 2026-08-05, 2026-08-07, 2026-11-23 |
| [`spec-author`](spec-author.md) | `S-006` and `S-007`, the spec location (`chore-0027`); Goal 4 and the interview: `S-005` retired, `S-008` and `S-009` added (`feat-0076`); the approval digest: a Constraint, two surface rows, `S-010` and `S-011` (`feat-0083`) | 2026-08-05, 2026-11-23 |
| [`systematic-debugging`](systematic-debugging.md) | `S-014` and `S-015`, where instrumentation may live and what happens where it cannot live anywhere, settling both Open Questions before anything was built against the contract (`chore-0078`); `S-016`, no red command means no hypothesis phase (`feat-0077`) | 2026-08-29, 2026-11-23 |
| [`validate-skills`](validate-skills.md) | `S-022`, the code-span and fence exception (`chore-0039`); `S-023` and the "what it reads" surface entry, the lens-composition rule (`chore-0047`); `S-024` and the `Output` and "what it reads" surface entries, the supporting-file link rule (`chore-0054`); `S-025` and the same two surface entries again, the non-skill `.agents/` markdown link rule (`chore-0065`); `S-026` and the "what it reads" entry again, the universal-lens rule (`feat-0064`); `S-027`, `metadata.invocation` (`feat-0079`) | 2026-08-19, 2026-08-20, 2026-08-21, 2026-08-27, 2026-08-29, 2026-11-23 |
| [`verifier-agent`](verifier-agent.md) | a dated note on dispatching the verifier with a fresh context, as a leaf, at high effort; no scenario changes, so whether it needs re-approval at all is the maintainer's call (`feat-0077`); the approval digest: the approval Constraint, `S-012` and `S-013` (`feat-0083`) | 2026-11-23 |

The `house-review` row was missed when this table was first written, and how it was missed is the
argument for eventually replacing this table with a marker key. That spec's note says its
frontmatter is "left at `approved` for the author to confirm at closeout" rather than using the
words *pending* or *re-approval*, so it is invisible to the search that finds the rest of this
table. A convention carried in prose can only be found by a reader who already knows every
phrasing it has ever taken. Since `feat-0083` the digest finds a changed spec whatever its note says,
but only once the spec is bound; for the specs still `unbound`, this table is the record.

## One file kind per question asked

A spec accumulates sibling reports. Each answers a different question, and none replaces another. A
spec may have one, several, or none. This is the same list carried in the layout table in
[`AGENTS.md`](../../AGENTS.md); if the two ever disagree, `AGENTS.md` is authoritative.

| File | Question it answers | Produced by |
|---|---|---|
| `<spec>.md` | What should be true? | [`spec-author`](../../.agents/skills/spec-author/SKILL.md) |
| `<spec>.conformance.md` | Does the implementation match the contract? | [`spec-conformance`](../../.agents/skills/spec-conformance/SKILL.md) |
| `<spec>.verification.md` | Was this run's work acceptable? | [`verifier-agent`](../../.agents/skills/verifier-agent/SKILL.md) |
| `<spec>.readiness.md` | May implementation begin at all? | [`spec-plan-readiness`](../../.agents/skills/spec-plan-readiness/SKILL.md) |
| `<spec>.characterization.md` | What did this behave like before a contract existed? | [`test-author`](../../.agents/skills/test-author/SKILL.md) |
| `<spec>.runbook.md` | How does a person perform a step no agent here can? | a human, or an agent writing for one |

The runbook is the newest kind, added 2026-08-07, and only one spec has one. It exists because
[`cloud-executable`](cloud-executable.md) is the first contract here whose verification depends on an
action nothing in this repository can take: `claude --cloud` refuses a non-interactive invocation, so
the proof session has to be started by a person from a terminal or a browser. Putting those
instructions in the verification record was the obvious alternative and is wrong, because that record
is a ledger of one attempt on one date while the instructions are current-state and will be edited.
A kind is worth adding when two documents would otherwise have to drift apart to stay correct.

The distinction between the first two reports is the one most easily lost. **Conformance** is a
matrix over the whole contract: every scenario and surface element classified `Conformed`,
`Diverged`, or `Not-built`, with a coverage proof. **Verification** is a verdict on one run, with
evidence, recorded at the moment that run happened. A conformance matrix is re-derivable at any
time; a verification record is history and is never rewritten.

That difference has a mechanical consequence. The spec-closeout gate looks for a
`<stem>.conformance.*` sibling, so a `.verification.md` alone does not satisfy it. `house-review`
carried only a verification record until `chore-0025`, and would have blocked on exactly that.

Every report except `<spec>.md` is a **ledger**: it records what was observed on a given date.
[`doc-sync`](../../.agents/skills/doc-sync/SKILL.md) skips them rather than reporting them as drift,
because a matrix quoting what a command printed in July is not stale when the command prints
something else today.

## The specs

| Spec | Status | Scenarios | Siblings |
|---|---|---|---|
| [`agent-observatory`](agent-observatory.md) | approved | 22 | [conformance](agent-observatory.conformance.md) (22 of 22 built), [readiness](agent-observatory.readiness.md) |
| [`build-adapters`](build-adapters.md) | approved | 23 | [conformance](build-adapters.conformance.md), [readiness](build-adapters.readiness.md) |
| [`cloud-executable`](cloud-executable.md) | approved | 20 | [conformance](cloud-executable.conformance.md), [readiness](cloud-executable.readiness.md), [verification: S-001 to S-016](cloud-executable.s001-s016.verification.md) (**fail**, fixed same day), [verification: the proof run](cloud-executable.verification.md) (**blocked**), [runbook](cloud-executable.runbook.md) |
| [`doc-sync`](doc-sync.md) | approved | 15 | [conformance](doc-sync.conformance.md) |
| [`house-review`](house-review.md) | approved | 24 | [conformance](house-review.conformance.md), [verification](house-review.verification.md) |
| [`install`](install.md) | approved | 29 | [conformance](install.conformance.md), [characterization](install.characterization.md) |
| [`sitrep`](sitrep.md) | approved | 40 | [conformance](sitrep.conformance.md) (28 of 40 built), [readiness](sitrep.readiness.md) (implementable) |
| [`spec-author`](spec-author.md) | approved | 11, one retired | [conformance](spec-author.conformance.md) |
| [`systematic-debugging`](systematic-debugging.md) | approved | 16 | [conformance](systematic-debugging.conformance.md) (16 of 16), [verification](systematic-debugging.verification.md) |
| [`test-author`](test-author.md) | approved | 5 | [conformance](test-author.conformance.md) |
| [`tracker-links`](tracker-links.md) | approved | 9 | [conformance](tracker-links.conformance.md), [verification](tracker-links.verification.md) |
| [`validate-skills`](validate-skills.md) | approved | 27 | [conformance](validate-skills.conformance.md), [verification](validate-skills.verification.md) |
| [`verifier-agent`](verifier-agent.md) | approved | 13 | [conformance](verifier-agent.conformance.md) |

[`sitrep`](sitrep.md) was added and approved on 2026-09-11, after the figures in the next paragraph were computed, so they do not include it. Nor do they include the 2026-11-23 overhaul amendments, which moved three of the counts in the table above: `house-review` from 18 to 24 (`feat-0078`), `spec-author` from 7 to 9 with `S-005` retired (`feat-0076`), and `systematic-debugging` from 15 to 16 (`feat-0077`), and WS4 moved three more: `install` from 18 to 23, `build-adapters` from 20 to 23, and `validate-skills` from 26 to 27 (`feat-0079`), `feat-0083` moved two more: `spec-author` from 9 to 11 and `verifier-agent` from 11 to 13; and `chore-0033` moved `install` again, from 23 to 29. Each was counted from the spec's own scenario headings on that date.

Twelve specs, 186 scenarios, all approved. **All twelve now carry a conformance matrix**, holding
all 186 of those scenarios, recomputed from the files on 2026-08-29 rather than incremented: the
twelve counts in the column above sum to 186, and no spec is now without a matrix. The figure moved
from 184 to 185 on 2026-08-29, when `feat-0064` amended `validate-skills` with `S-026`, and to 186
on 2026-09-01, when `chore-0087` amended `build-adapters` with `S-020`. The 2026-08-29 figure was
recomputed by counting `### Scenario S-NNN` headings across all twelve files rather than by adding
one; this one was incremented by hand from the row it changed, which is the discipline `chore-0075`
is open to mechanise and the reason it is worth mechanising.
[`systematic-debugging`](systematic-debugging.md) was the last one, audited at `feat-0061`'s
closeout on 2026-08-29.

**Carrying a matrix is not the same as being fully audited, and 184 is the first figure rather than
the second.** It counts scenarios in specs that have a matrix, not scenarios a matrix has classified.
`install` is the spec where the two differ: `bug-0018` added S-016 to S-018 on 2026-08-07 and the
matrix update is owed at that task's closeout, so part of that contract has never been audited.

**The second figure is deliberately not stated here.** Deriving it needs a per-matrix count of
classified rows, which nothing computes and which this file has already carried wrong: the standing
claim that `install`'s matrix "covers 15 of its 18 scenarios" does not survive a check, since that
matrix cites 17 of the 18 scenario ids. Whether the other two are classified rows or prose recording
what is owed is the question a reader has to answer by opening the file, and a number asserted here
would be a guess wearing arithmetic. `chore-0075` is the open task that would make every figure on
this page computed rather than hand-maintained, and this is the second one it would have caught.

[`systematic-debugging`](systematic-debugging.md) was the second **forward** spec here, written
before an implementation rather than pinning one that already existed, so from 2026-08-19 until
2026-08-29 it was the only spec with nothing to audit. It carries 15 rather than the 13 it was
approved with, since `chore-0078` settled both of its Open Questions on 2026-08-29, and 16 since
`feat-0077` added `S-016` on 2026-11-23.

[`cloud-executable`](cloud-executable.md) was the first forward spec and stopped being the exception
on 2026-08-19, when `chore-0034` audited it. That matrix is worth reading for what it declined to
claim: when it was written, S-017 to S-019 and the unattended pull request surface were all recorded
**Not-built**, because the Phase 4 proof run they describe was still recorded `blocked` and had never
run. A matrix that reported them any other way would have been worse than no matrix. The proof run of
2026-08-20 moved all but S-019, whose Given is a run whose gates fail, and that run's did not.

## A limit worth knowing before reading any matrix

Most of what this kit ships is prose, not code. When a spec describes a skill, both sides of its
conformance audit are natural language and the evidence column cites a clause rather than a code
path. That establishes the skill **instructs** the specified behavior, not that anything
**enforces** it: a prose skill can conform perfectly and still be ignored by the agent running it.

Closing that gap is what the [hooks module](../../.agents/hooks/README.md) is for, and it reaches
only the rules that are mechanically decidable. The rest is closed by exercising a skill on real
work and recording what happened, which is what the verification records are.
