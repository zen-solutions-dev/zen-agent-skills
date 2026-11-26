---
id: chore-0121
title: Teach tdd and test-quality that a fix claiming "every X" is tested through behaviour over every module reached
type: chore
status: open
priority: P2
parent: "ROADMAP Campaign G: rollout (docs/reviews/2026-11-25-rollout-first-adopter.md, finding 6)"
depends_on: []
spec: ""
scenarios: []
external: ""
mode: afk
touched_files:
  - .agents/skills/test-quality/SKILL.md
  - .agents/skills/tdd/SKILL.md
  - .claude-plugin/
created: 2026-11-25
---

## Problem

The rollout's first adopter quest (2026-11-25, [the first adopter run](../docs/reviews/2026-11-25-rollout-first-adopter.md), finding 6) claimed that every `git` call in a gate was bounded by a time limit. Its guard test grepped one source file for the bounded helper, so a `git` call in a module the gate imports was missed and passed; an independent verifier found it. A source-regex guard proves what one file says, not what the program does.

Neither [`test-quality`](../.agents/skills/test-quality/SKILL.md) (the lens that judges tests) nor [`tdd`](../.agents/skills/tdd/SKILL.md) (the procedure that writes them) names this shape.

## Scope

**In scope:**

- One check in `test-quality`'s Workflow: when a change claims a property over a set ("every call", "all callers", "each module"), the test exercises that property through behaviour, over every module the code path reaches, and a grep of source is at most a supplement. A short example in the kit's own words.
- One line in `tdd` (its Notes, or the step where a test is chosen) pointing at that check.
- Regenerate the committed marketplace with `python scripts/build-adapters.py --marketplace` if either skill ships in it, in the same commit.

**Out of scope:** Any other change to either skill. Naming the adopter repository, its files or its users: the kit is public.

## Acceptance criteria (mechanically verifiable)

    ZEN_CHECKS_SCOPE=full python scripts/run-checks.py

- [ ] `test-quality` carries the check and `tdd` points at it.
- [ ] `python scripts/validate-skills.py` passes, and the marketplace gate is green.

## Definition of done

- [ ] Acceptance command passes locally.
- [ ] Conventions in AGENTS.md's conventions section followed.
