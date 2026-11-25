# Hold the orchestrator's own commits while children run

**Lesson, 2026-11-25**, reported by the round 2 orchestrator: its own commits to
`zen/marjana-r2-2026-11-25` while Wave 1 children were in flight forced extra merges twice, because
every running child then had to merge a moved tip before it could land by fast-forward. From then
on it held such commits on a side branch until the wave landed: `d15026a` ("Record the maintainer's
check-in gate answers on feat-0102 (held off the integration branch while Wave 1 runs)") is one,
reachable from `origin/zen/marjana-r2-2026-11-25` at `d906b20` (checked with `git log` on
2026-11-25). The two commits that forced the extra merges were not named in the report this entry
is written from.

Folded into `orchestrate` Step 1 item 7 by `feat-0107`.
