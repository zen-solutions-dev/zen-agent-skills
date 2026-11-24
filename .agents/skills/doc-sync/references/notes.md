# doc-sync: notes and reasons

The procedure in [`SKILL.md`](../SKILL.md) says what to do. This file holds the reasons, so the
procedure stays short. Nothing here is a step.

## Why bound the scope first

The default scope is every tracked Markdown document, and on a real repository that is routinely
more than fits. An audit that runs out of budget partway through does not fail: it reports on the
documents it reached and says nothing about the rest. Since the value of this skill is that a clean
verdict means something, an unbounded run can produce the one output worse than not running at all.

## Why the staleness vocabulary is derived, not fixed

A list of staleness words carried over from a previous run or another repository misses whichever
word this one actually uses. Widening the vocabulary widens what counts as a stale word, not what
counts as evidence: a document using "draft" still needs a contradicting fact.

## Why ungroundable suspicion produces nothing

A report padded with ungrounded suspicion is one the reader stops trusting, and once they stop
reading it the skill has no value. Silence on an ungroundable passage is correct behaviour.

## There is no exact oracle

Natural language does not compile, and whether a sentence still describes the code is often a
judgement. This skill is a systematic sweep, not a proof. Expect false positives, design for cheap
dismissal, and do not present the output as more precise than it is. The `grounded` split exists to
keep the mechanical hits from being diluted by the judgement calls.

## The most valuable findings are the dullest

A reference to something renamed or deleted, a status label that outlived its state, a count that
stopped matching. These are cheap to check mechanically and nearly invisible to a person re-reading
familiar prose.

## The ledger skip suppresses things that look actionable, on purpose

Archived task files and changelogs accumulate references that no longer resolve, because the file
moved or the code did. Those are not drift: the entry still describes its moment correctly. If link
integrity across the whole repository is what you want, that is a separate mechanical check, and
running it through this skill would bury the real findings under archive noise.

## A contract finding is a bug report

It is not a documentation task. It likely belongs in the repository's task tracker, and possibly to
`spec-conformance` for a full audit of that contract against the implementation.

## Run it after each landed change

Running it after each change costs less than running it before a release, because the drift is
fresh and the cause is still obvious.

## Why the link re-check is unconditional

The composed editing discipline in `doc-revise` verifies links after a structural change, and
correcting a stale claim is usually not one. So the re-check belongs in this skill's apply step, and
it runs on every applied edit rather than only on the ones that look structural.

## Why the link checker's mode matters here

In this kit `python .tasks/validate.py --links <path>` resolves every relative link against the
directory the file actually lives in, the same rule the CI docs link step applies to the root,
`.github/` and `docs/` trees. The checker's other modes walk the tracker directory only, so they
would report clean without having read the edited document at all (`bug-0014`).

## Why the habits in Step 2

Moved here from the procedure on 2026-11-24 (`feat-0093`), which kept the habits and shed the
argument. **Formatting does not define a claim**: prose wraps, so a qualifier and the subject it
qualifies routinely land on different lines, and a scan that compares text within one line, or that
looks only at marked-up tokens, misses the references that matter. **Counts drift silently** because
nobody recounts them, and "all six" or "three lenses" is the cheapest claim in a document to check.
**A quoted or capitalized word is no evidence** it names a skill, a file or a command; looking for
the wrong kind of thing fills the report with dismissals.

The fourth habit, the undated present tense, is the detecting half of the "write history, not the
present" rule in `writing-for-agents.md`: a bare "currently" is a claim with no date to check it
against, so in a current-state document it is grounded like any other claim. It reaches no further:
a ledger is still skipped entirely, so the habit narrows nothing in this skill's contract.

