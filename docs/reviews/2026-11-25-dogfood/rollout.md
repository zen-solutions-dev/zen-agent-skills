# Dogfood record: the rollout's first adopter (2026-11-25)

The skills run on real work during [the first adopter run](../2026-11-25-rollout-first-adopter.md). Every run below happened in the orchestrating session or in a child it dispatched, and each one says which. The adopter is a private repository, so its paths are not named here.

| Skill | What it ran on | Evidence | Verdict | What changed |
|---|---|---|---|---|
| `sitrep` | The orchestrating session, on this kit's `developer` and on the adopter's chore branch, for the maintainer's sitrep request | Kit: `waiting on you (0)`, `blocked (1)` (feat-0071), `notice: no integration branch`. Adopter: `in flight (1)`, `blocked (19)`, matching the cutover's own count of 19 quests blocked on the maintainer | Works on a second repository with no setup. The blocked list was the useful part. | The kit's notice is finding 8 in the run record. |
| `agent-handoff` | The orchestrating session, writing the brief for the next orchestrator | Step 1 chose "hand off" (the work travels to a new session). The brief was written outside the working tree | Worked as written | None |
| `new-quest` (its `validate.py`) | The adopter's 87 quest files, vendored byte for byte from `e694817` | `Checked 87 quest files: 0 error(s), 0 warning(s).` | Works outside this kit | Finding 2 (empty `touched_files`) |
| `tdd` | A child, on the adopter's first quest | Failing test first on every step: missing export, then each verifier finding shown failing open before its fix | Worked, and it caught a defect the fix itself introduced | Finding 6 |
| `verifier-agent` (as a brief) | A fresh child that neither wrote nor briefed the work | Mutation re-checks: 9 reverted fixes, 8 caught by tests | Found two real defects that the author's own review missed | None |
| `init-worktracking` | Not exercised: it was not installed in the adopter's cloud session, so its output was written by hand from its templates | (none) | Not run | Finding 1 |
| `grill`, `wayfinder` | Not exercised as skills. The migration questions went through pickers following the plan's question list | (none) | Not run | None |
