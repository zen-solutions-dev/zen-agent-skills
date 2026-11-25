# Fix shared terms verbatim in every brief

**Lesson, 2026-11-25**, reported by the round 2 orchestrator: two Wave 1 siblings each defined a
"dogfood record", differently, because each brief described the term in its own words. A key name
or a definition two children share is written once by the orchestrator and pasted into both briefs
word for word. In `AGENTS.md`, `d64f08c` (`feat-0102`) defined it as "a dated record of a real run
under `docs/reviews/`"; the fix round `7845524` changed it to "a file under `docs/reviews/` whose
path contains `dogfood` and that names the skill, by its name or as `<name>/SKILL.md`", the
definition in section 7 as of `d906b20` (quoted verbatim; the round 2 close then narrowed "by its
name" to the backticked, bracketed or path forms). The sibling's other
definition is not cited here, because the report this entry is written from did not name its
commit.

Folded into `orchestrate` Step 2 by `feat-0107`. Related:
[Re-point a verifier when a child's head moves](2026-11-25-verifier-on-moved-head.md).
