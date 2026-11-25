# Hold the orchestrator's own commits while children run

**Lesson, 2026-11-25**, reported by the round 2 orchestrator: its own commits to
`zen/marjana-r2-2026-11-25` while Wave 1 children were in flight forced extra merges twice, because
every running child then had to merge a moved tip before it could land by fast-forward. From then
on it held such commits on a side branch until the wave landed (for example `d15026a`, "held off
the integration branch while Wave 1 runs").

Folded into `orchestrate` Step 1 item 7 by `feat-0107`.
