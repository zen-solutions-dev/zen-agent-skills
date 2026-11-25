# Re-point a verifier when a child's head moves

**Lesson, 2026-11-25**, reported by the round 2 orchestrator: the Wave 1 child on
`zen/marjana-r2-platform` (`feat-0103`) reported at `0ef68e0` ("Merge origin/zen/marjana-r2-2026-11-25
into zen/marjana-r2-platform"), then applied a relayed correction and pushed `027b835` ("feat-0103:
honour metadata.extended and warn on a guard with no otherwise clause"), so its head moved while the
verifier ran on `0ef68e0`. `0ef68e0` is an ancestor of `027b835` (checked with
`git merge-base --is-ancestor` on 2026-11-25). A verdict on the old sha lands only the old sha. Two rules came of it: the verifier is told the
new sha and re-runs there, and a child pushes nothing after reporting unless asked.

Folded into `orchestrate` Step 2 and Step 5 item 4 by `feat-0107`. Related:
[Fix shared terms verbatim in every brief](2026-11-25-shared-terms-verbatim.md), another brief rule
from the same wave.
