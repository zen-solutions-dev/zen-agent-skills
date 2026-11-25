# Recurring jobs wait on named repositories

**Problem, open as of 2026-11-25.** The maintainer approved a daily improvement loop (decision
`F1`, a scheduled `improve-architecture` pass opening one pull request) and a research refresh every
two weeks (`G4`), but did not name the repositories `F1` runs in; source:
`docs/reviews/2026-11-25-marjana-decisions.md`, sections F and G. `orchestrate` Step 7 offers a
recurring job and never schedules one or picks its repositories, so the loop waits on the
maintainer's list. Plans for `F1` are reserved for round 2's Phase 3 (`chore-0110` onwards).
