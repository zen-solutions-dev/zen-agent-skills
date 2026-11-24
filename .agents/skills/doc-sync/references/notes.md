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
