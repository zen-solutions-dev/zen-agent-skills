---
name: zen
description: >-
  Router over the Zen Agent Skills kit: says which skill or flow fits where you are now, from a
  rough idea to a shipped and reviewed change, and which light path a small change can take
  instead. Hints only; it never starts a skill.
license: MIT
metadata:
  invocation: user
disable-model-invocation: true
---

# zen

Point the person at the right skill. Nobody remembers every skill in this kit, so they ask here.
The answer is a **hint**: a skill name, a one-line reason, and the next step after it. The person
starts that skill themselves.

Conventions: your answer follows [`house-style.md`](../../rules/house-style.md). Autonomy follows
[`core.md`](../../rules/core.md), full text in [`autonomy.md`](../../rules/autonomy.md).

## How to answer

1. **Place the person.** From what they said and what the repository shows (a `.quests/` directory, or `.tasks/`, its old name,
   a spec under `docs/spec/`, an open branch, a failing command), name the stage they are in: no
   project yet, an idea, a plan, a build, a change to verify, a change to ship, or a look back.
   Look beyond the current checkout too: another worktree or an unmerged branch may already hold
   work on the same thing (`git worktree list`, `git branch -a`), and that changes the route.
   When the repository has `.quests/` but no `docs/agents/zen.md`, add one line to the reply: the
   configure step of `init-worktracking` records what the skills read here, so they stop
   rediscovering it.
   Done when you can name one stage, or you have asked the one question that decides it.
2. **Pick the lightest path that fits**, using [the light paths](#the-light-paths) first and the
   flows only when the change has earned them. Done when you have one path and its reason.
3. **Read before you recommend.** Before you say what a skill does or that a step can be skipped,
   read that skill's `SKILL.md` if it is installed; the summaries below are for orientation. Name
   any draft you recommend as a draft, and say it needs `install.py --include-drafts`.
   Done when every skill the reply will name has had its `SKILL.md` read or is said to be not
   installed, and every draft among them is marked as one.
4. **Reply with the hint.** The skill to start now, one line on why, the skill that usually
   follows it, and whether the work suits **AFK** (nobody watching: well specified, low risk, easy
   to verify) or **human in the loop** (a one-way door, a wide blast radius, or hard to review).
   Done when the reply names exactly one next skill and one mode, or says plainly that no skill
   fits and the person should just do the work.

## The light paths

The full chain is something a change earns. Ask in this order; the first yes wins.

1. **Does a person have to agree the behaviour before it is built?** Full flow: `spec-author`
   (which runs the `grill` interview first), approval, and the rest of the chain below.
2. **Are there decisions only the person can make, but no behaviour anyone else must agree?**
   `grill` on its own, then `new-quest` writes the quest files from its decisions record. No spec.
3. **Does it span more than one sitting, or go to another agent?** Quest file: `new-quest` writes one
   file with an acceptance command, and `verifier-agent` checks it before it lands. No spec.
4. **Otherwise, direct.** Make the change, run the project's acceptance command, and ask for
   `house-review` if the change warrants one.

## The flows

The kit runs one spine, align, plan, build, verify, ship, learn, with setup in front of it. Every
step is also useful on its own. *(draft)* marks a skill not yet promoted.

**Setup**, once per repository:

- `project-bootstrap`: a new or bare repository gets a stack-matched baseline, then hands to
  `init-worktracking`.
- `init-worktracking`: an existing repository gets `AGENTS.md`, `.quests/`, and by tier a roadmap and
  changelog. Every task-based skill below needs it. Its configure step writes `docs/agents/zen.md`,
  the facts the skills read; run it alone on a repository already tracked.

**Align**, before anything is written down:

- `grill`: "grill me". An interview in rounds until no decision is silently assumed.
  Facts are looked up; only decisions go to the person. Start here for any real change.
- `domain-language`: a term is settled or contested, or a decision is hard to reverse.
  Keeps the glossary and writes an ADR only when one is earned.

**Plan**:

- `research` *(draft)*: a question the repository cannot answer. A fresh agent reads primary
  sources and writes one cited file.
- `spec-author`: behaviour a person must agree. Writes Given/When/Then scenarios and stops for
  approval. It composes `spec-quality`, the lens that judges a spec's well-formedness.
- `new-quest`: an approved spec, or a change that needs a quest file, becomes tasks each sized to one
  fresh context window.
- `spec-plan-readiness`: the go/no-go gate over a spec plus its tasks, before any code.

**Build**:

- `tdd`: new code, test-first, one red-green slice at a time.
- `orchestrate` *(draft)*: a piece of work too big for one context. One session holds the
  conversation; child sessions research and build on their own branches, landing on one
  integration branch and reaching the person as one pull request.
- `fix-batch`: two or more independent quest files to parallel agents, each in its own worktree,
  each starting fresh. A person starts it.
- `systematic-debugging` *(draft)*: something is broken and the cause is unknown. Builds a red
  command first and diagnoses; it never fixes.
- `test-author`: tests from an approved spec, or tests that pin legacy behaviour, after the fact.
- `test-quality`: the lens `tdd`, `test-author` and `fix-batch` use to judge a test.

**Verify**:

- `verifier-agent`: before work lands. Runs the declared commands and returns pass, fail, or
  blocked with evidence.
- `spec-conformance`: does the code match its spec, scenario by scenario. `verifier-agent` composes
  it.
- `house-review`: a review on two axes, the spec and the written standards, at a depth chosen from
  the change's size and risk. Report only.

**Ship**:

- `reconcile-worktrees`: verified worktrees land in the main checkout one at a time. A person
  starts it.
- `doc-sync`: which documents the change made wrong. Dry run by default.
- `pr-describe`: the pull request body and changelog entry, ending with the merge danger.

**Learn**:

- `retro`: after a build, especially one that went sideways. A repeated correction
  becomes a check; a judgement call becomes a written standard. A person starts it.
- `improve-architecture`: a spare moment, or a bug with no good seam to test it at. Finds
  deepening refactors in the hot spots; a chosen one goes back to `grill` or `new-quest`. A person
  starts it.

**Handoffs and context**:

- `agent-handoff`: at a phase boundary, whether to continue, clear, hand off, dispatch a subagent,
  or compact, and the brief when it is a handoff. Keep align and plan in one unbroken session where
  they fit; each build task can start fresh from its quest file.
- `human-handoff`: an update for a partner, client, or teammate.

**Documents**:

- `doc-author`: a document that does not exist yet.
- `doc-revise`: an existing document, edited in place in its own voice.

**Status**:

- `sitrep` *(draft)*: "where are we" for one repository, from its quest files and git.
- `agent-observatory` *(draft)*: questions across many agent sessions: what is running, what it
  cost.
- `quest-tracker` *(draft)*: a season of work run from a shared tracker page.

## Notes

- **Every hint is a suggestion.** When the person already knows what they want, say which skill
  does it and stop.
- **A draft has not been used on real work yet.** Recommend it when it fits, and say so, so the
  person knows its rough edges are expected.

## Provenance

Adapted, in this kit's own words, from Matt Pocock's `ask-matt` router: a user-invoked map of every
skill, the main flow with on-ramps, reading a skill before recommending it, and context hygiene at
phase boundaries are his. The light paths, the stage-placement step and the kit's own flows are this
repository's. The phase-boundary tree itself lives in `agent-handoff`.

```provenance
source: https://raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/ask-matt/SKILL.md
author: Matt Pocock
license: MIT
retrieved: 2026-11-23
sha256: 1371f5ce005de0992a44b137748bfb960a56948aa9871b405fe9d90b24332e3c
note: fetched with urllib and digested with hashlib on the retrieved date, at 12,594 bytes. Adapted, not copied; this file is expected to differ.
```

```provenance
source: https://raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/ask-matt/PHASE-BOUNDARIES.md
author: Matt Pocock
license: MIT
retrieved: 2026-11-23
sha256: a8aa20158609ef39e2b308b6ba0660c91066838d07a867202e63a7744a88a3ed
note: fetched with urllib and digested with hashlib on the retrieved date, at 4,249 bytes. Read for the context-hygiene line; the tree itself is adapted in agent-handoff.
```
