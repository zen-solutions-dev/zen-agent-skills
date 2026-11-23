# Why house-review works the way it does

The procedure in [`SKILL.md`](../SKILL.md) says what to do. This file says why, so the procedure
can stay short. Nothing here is a step.

## The name

It is named for the house rubric it applies rather than for the act of reviewing, which keeps it
clear of the review commands several harnesses ship built in. A skill cannot resolve a namespace
collision by asserting it is different, so the name avoids one instead (`chore-0012`).

## Two axes

A change can pass one axis and fail the other: code that follows every standard but builds the
wrong thing, or code that does exactly what the task asked while breaking the project's
conventions. Ranking the two together lets a pile of style findings bury the one missing
requirement, or the reverse. The axes are run as separate passes, in separate contexts where the
harness allows, because a reviewer who has just read the contract reads the code for the contract,
and the standards pass then inherits that framing.

The standards source is read at review time, not at implementation time. The implementing agent
carries the most context pressure: it explores, writes and debugs. The reviewer receives a diff and
has room to hold a standards file. So judgement-call standards belong to review, and mechanical ones
belong to a check that runs before review at all.

## The evidence gate

`verifier-agent`'s dogfood in this repository found a conformance matrix whose classifications
were right and whose every line citation had drifted eight lines after a refactor. A human caught
it, not the process. The gate turns "validate before reporting" into a check with one disposition
per outcome, and the re-anchor branch exists because dropping a finding whose pointer moved would
throw away a real defect for a bookkeeping reason.

The drop count is reported without the dropped content because the count is what makes a reviewer
whose citations routinely fail visible, and the content is exactly what the gate decided nobody
should rely on. Whether dropped findings should be recoverable on request is an open question in
the contract, left for a real case to decide.

## The absence form

Requiring a quote of code that does not exist would suppress the whole tests-and-coverage
category, which is made almost entirely of absences. The absence form quotes an anchor and records
the rerunnable search instead. The worked example in the procedure (`--with-hooks` untested) was a
live finding when written and was closed by `chore-0067` on 2026-08-27, so its search now returns
matches; it is kept because the shape is what it teaches.

## The depth rule

Depth was the one review parameter nothing set, so a one-line typo fix and a 900-line change across
installer, tests and a contract got the same treatment. That produced one of two failures depending
on mood rather than on the change. The rule used to live in a separate `review-depth` skill and was
folded in here by `feat-0078`.

- **R2 before R3.** A contract under a spec directory is markdown, and editing it changes what code
  is required to do. Checking risk first stops a contract edit being waved through as a docs change.
- **R2 before R5.** A small change to a trust boundary outranks a large change to inert code. Size is
  the weakest signal and is checked last.
- **R4.** A documentation change over 400 lines is a rewrite, and a rewrite can be wrong in ways a
  correction cannot.
- **Anchors, not blanket escalation.** The first draft escalated the whole changeset. Four of six
  real changesets tripped R2, usually on one CI workflow inside an ordinary change, and a `deep` that
  fires on two thirds of commits is the uniform setting the rule exists to replace.
- **Re-measure and cap the remainder.** The first anchored version reused the whole-set line count,
  so the remainder inherited the anchors' lines and R5 fired on it. Measured on `v0.1.0..5ba2311`:
  1047 reviewable lines across 7 directories, 30 of them in two anchors, and the remainder selected
  `deep`. Re-measured and capped, it is `deep` on the anchors and `standard` on the other 1017.
- **Prose and the reference count.** A widely linked document is not a widely depended-on surface:
  `docs/CATALOG.md` is linked from 19 files, and counting references over prose sent a four-line
  wording fix to `deep` on its first run. Prose reaches `blast_radius` only by being a named kind.
- **Rename detection and untracked files.** Without `-M` a moved file counts as a full delete plus a
  full add, so the measure depends on git config. Without counting untracked files, a working tree of
  new files measures zero, the same blind spot that once let `reconcile-worktrees` drop new files.
- **Exclusion matters.** In one external refactor exclusion took the count from 6512 lines to 655,
  because a `uv.lock` update was 90 percent of the diff. Generated material is not always obvious
  from the path: four `schemas/*.schema.json` files there were written by a sibling script.
- **An empty reviewable set is a failure, not a small change.** Every threshold is satisfied by zero,
  so an unmeasured change would otherwise get the cheapest review.

The thresholds (150, 400, 600, 5 directories, 5 referencing files) are starting numbers. Retune them
in the skill body; writing them as numbers makes retuning a visible edit rather than a mood.

**A known gap carried over:** for a path-scope review the signals are computed over the scoped paths,
which measures the files in full rather than a change, so `reviewable_lines` over-counts. It is
recorded in the roadmap rather than fixed here.
