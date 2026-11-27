---
id: feat-0115
title: Fold round 3's lessons into orchestrate before promotion
type: feat
status: done
priority: P2
parent: "ROADMAP Campaign G: rollout (docs/reviews/2026-11-27-promotions-plan.md)"
depends_on: []
spec: ""
scenarios: []
external: ""
mode: afk
touched_files:
  - .agents/skills/orchestrate/SKILL.md
  - .agents/skills/orchestrate/references/first-run.md
  - .agents/skills/orchestrate/references/claude-code.md
created: 2026-11-27
---

## Problem

The maintainer chose on 2026-11-27 to promote [`orchestrate`](../../.agents/skills/orchestrate/SKILL.md). Its owed run on a second project, by a session that did not write it, happened in rollout round 3 (`docs/reviews/2026-11-25-rollout-r3-plan.md`, `docs/reviews/2026-11-26-dogfood/rollout-r3.md`). That run left four lessons, three of them in `docs/agents/memory/` (the 2026-11-26 entries): run an adopter's own local-only pre-PR gate on the person's computer before briefing any child; in the Claude desktop app, a turn that a child's report started cannot start sessions, so the run used relays to idle children and background subagents; ask the verifier of a fix to a false claim to sweep for the same claim outside the quest's scope. The fourth: the person squash-merged a pull request whose job was to carry history (a merge of `main` into `developer`), and the next branch had to be re-merged; the run's final pull request body had not said which merge method it needs.

## Scope

**In scope:** Step 1's probe also runs the adopter's own pre-PR gate once on the person's computer when it is local-only. Step 5 item 4: the verifier of a fix to a false claim is asked to sweep for the same claim past the quest's scope. Step 6 item 4: the pull request body names the merge method it needs when a squash would drop history. The desktop transport limit goes in a labelled single-harness section (in `references/claude-code.md`, or a short section beside it, per AGENTS.md section 5). `references/first-run.md` gains a dated round 3 section, and its Owed list marks the second-project run as done and names what is still unexercised (the exploration child, the memory lint, the recurring-job offer). Keep `status: draft`: the flip is `feat-0116`.

**Out of scope:** Rewriting the procedure. Naming the private product app's repository, owner or users (the kit is public). Any file outside the skill's directory.

## Decisions

- **A premise that turned out false:** this quest's Problem said the run's final pull request body had not named the merge method it needs. Its verifier (2026-11-26, against `gh pr view`) found #121's body did say "Merge #120 first, with a merge commit"; it was #120's own body that named none, and #120 was squash-merged anyway. The skill's record and rule were corrected in a fix round (`839fe3f`), re-checked at `848b514`.

## Acceptance criteria (mechanically verifiable)

    ZEN_CHECKS_SCOPE=full python scripts/run-checks.py

- [ ] The four lessons are in the procedure or its references, each traced to round 3 in `first-run.md`.
- [ ] `python scripts/validate-skills.py` passes.

## Definition of done

- [ ] Acceptance command passes locally.
- [ ] Conventions in AGENTS.md's conventions section followed.
