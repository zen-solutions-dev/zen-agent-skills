# Skill catalog

Every skill Zen Agent Skills ships, plus what is drafted, what is planned, and what is deliberately not built yet.

The kit is organized by how broadly a skill is worth sharing. The axis is deliberate: broadly-useful skills go in the public kit; hyper-specific personal skills stay out and serve as portfolio demos instead.

A skill is listed as **shipped** once it lives under [`.agents/skills/`](../.agents/skills/) and has been used and iterated on for real. A skill that is written and lives there but has not yet earned that is a **draft**, listed under [drafts](#drafts-built-but-not-yet-used-on-real-work) rather than in a tier, because a default install does not place it. A skill that is not written at all is **planned**, and stays planned until it has earned its place. This is the same "seed by inspection, not speculation" principle the skills themselves follow.

Every skill also says who starts it. **Model** means its description sits in the agent's context so
the agent reaches for it unprompted. **User** means a person starts it by name (`invocation: user`
under `metadata`); on Claude Code the installer hides its description from the agent, so it costs no
context in sessions that never use it. Not sure which skill fits? Start `zen`, the router, which maps
every skill below to the moment you reach for it.

## Tier A: broadly shareable (the public kit)

| Skill | Status | Invocation | What it does |
|---|---|---|---|
| `project-bootstrap` | shipped | model | The front door: a stack-matched baseline (gitignore, editorconfig, linter and formatter, license, README stub) for a new or bare repository, then `init-worktracking`. |
| `init-worktracking` | shipped | model | Scaffolds `AGENTS.md`, `.tasks/`, and by tier a roadmap and changelog into any repository, seeded by inspecting it. |
| `new-task` | shipped | model | Turns an idea, bug, or approved spec into task files, each sized to one fresh context window, sliced vertically, with an acceptance command. Wide refactors are sequenced as expand, migrate, contract. |
| `fix-batch` | shipped | user | Dispatches independent task files to parallel agents, each in its own worktree with a fresh context and told it is a leaf, then verifies every result. A missing field in a delegate's report blocks acceptance. |
| `reconcile-worktrees` | shipped | user | Lands verified worktrees in the main checkout one at a time: real base, untracked files, phantom binary diffs, overlaps. Leaves a reviewable diff uncommitted. |
| `house-review` | shipped | model | Reviews a change on two independent axes, spec (did it do what was asked, no more, no less) and standards (the repository's `CODING_STANDARDS.md` or `CONTRIBUTING.md` plus the swappable `review-quality` lens), at a depth chosen from the change's size and risk. Every finding's quote must resolve against the file. Report only. |
| `pr-describe` | shipped | model | Drafts a pull request body and changelog entry in the target repository's own format, ending with the merge danger: one-way or two-way door and blast radius. Closes a linked GitHub issue correctly. Never touches GitHub itself. |
| `agent-handoff` | shipped | model | At a phase boundary, decides whether to continue, clear, hand off, dispatch a subagent, or compact, and writes the brief when it is a handoff. |
| `human-handoff` | shipped | model | Packages project state for a partner, client, or teammate, with client-facing redaction. |
| `doc-author` | shipped | model | Writes new, code-grounded Markdown documents: READMEs, architecture with Mermaid, guides, decision records. |
| `doc-revise` | shipped | model | Revises an existing document in place, in its own voice, touching only what was asked. |
| `ci-scaffold` | planned (hold) | | Generate CI matched to the detected stack. Hold until used twice. |
| `release-cut` | planned (hold) | | Version bump, changelog roll-up, tag, notes. Hold until used twice. |

## The contract-driven delivery spine (Epic B)

These skills turn an agreed contract into verified work. Each was dogfooded on real in-kit work before it was blessed. Four (`spec-quality`, `spec-plan-readiness`, `test-quality`, `spec-conformance`) were folded in from `repoprompt-workflows` (Balarama Bosch, MIT), with provenance in [`NOTICE`](../NOTICE) and in a checkable block inside each adapted file. The kit dogfoods this spine on itself: specifications under [`docs/spec/`](spec/), tests under [`tests/`](../tests/).

| Skill | Status | Invocation | What it does |
|---|---|---|---|
| `spec-author` | shipped | model | Interviews the person in rounds until no decision is open, then drafts a behavioural spec with Given/When/Then scenarios, self-checks it with `spec-quality`, saves it as `draft`, and stops for human approval. |
| `spec-quality` | shipped | model | Lens: is a spec contract-level, observable, non-redundant, and free of open questions. Returns `ready` or `needs_revision`. |
| `spec-plan-readiness` | shipped | model | Go/no-go gate over an approved spec plus its tasks. A blocked verdict authorizes no tests, code, or delegation. |
| `test-quality` | shipped | model | Lens for test design: the lowest faithful layer, an independent oracle, mocks only at system boundaries. Rejects tautological and implementation-coupled tests. Used by `tdd`, `test-author` and `fix-batch`. |
| `test-author` | shipped | model | Tests after the fact: one per scenario of an approved spec, tagged `S-NNN`, plus characterization and regression tests. Never production code. |
| `spec-conformance` | shipped | model | Audits an implementation against its spec into a conformed, diverged, or not-built matrix. |
| `verifier-agent` | shipped | model | Runs the declared commands, composes `spec-conformance`, and returns `pass`, `fail`, or `blocked` with evidence before anything lands. Never edits what it verifies. |
| `doc-sync` | shipped | model | Detects documentation drift by checking prose against repository facts. Classifies each document as current-state, contract (report-only), or ledger (skipped). Dry run by default. |

## Drafts: built but not yet used on real work

A **draft** is written and lives under [`.agents/skills/`](../.agents/skills/), but has not yet been used on real work and refined from it. The Claude Code plugin never carries it, and the installer places it only when you ask with `--include-drafts`, and the installer names what it held back on every run rather than dropping it silently. Try them, and expect rough edges: real use is what promotes a draft. What each still owes is tracked in [`ROADMAP.md`](../ROADMAP.md).

| Skill | Status | Invocation | What it does |
|---|---|---|---|
| `zen` | draft | user | The router: says which skill or flow fits where you are, and which light path a small change can take instead. Hints only. |
| `grill` | draft | model | "Grill me": an interview in rounds over the decision tree, one recommended answer per question, facts looked up rather than asked, closing with a decisions record. The first step of any real change. |
| `domain-language` | draft | model | Keeps the project's glossary, and writes an ADR only when a decision is hard to reverse, surprising, and a real trade-off. Reports glossary-versus-code mismatches; never renames code. |
| `tdd` | draft | model | Red-green development: agrees the seam first, then one behaviour at a time, watching each test fail for the right reason. |
| `systematic-debugging` | draft | model | Diagnoses a defect to its cause: a red command first, then one hypothesis at a time, ending in one of three verdicts. Never fixes. Kept a draft at its first dogfood (`feat-0062`), where an independent check refuted the cause the run reached. |
| `retro` | draft | user | Looks back over a session or pull requests and proposes environment changes so a correction is never needed twice: a check where the mistake has a fixed shape, a written standard only for a judgement call. Applies only what you approve. |
| `improve-architecture` | draft | user | Finds the hot spots that make a codebase hard for an agent and proposes deepening refactors as an offline HTML report. Candidates feed `grill`, `spec-author` or `new-task`. |
| `sitrep` | draft | model | "Where are we" for one repository, from its tracked task files and git, with an evidence tier on every figure. Changes nothing. |
| `agent-observatory` | draft | model | Questions across many agent sessions: what is running, what a wave cost, which skills were used, what failed. Never starts, resumes, interrupts, or ends a session. |
| `quest-tracker` | draft | model | Runs a season of project work from one shared tracker page, with agent sessions reporting finished work as claims a person verifies. Needs a host that publishes a page with a shared database, which today is Claude artifacts. |

## Lenses: the swappable rules skills compose

Four rules modules under [`.agents/rules/`](../.agents/rules/) install alongside the skills, because a skill that composes a lens is not self-contained without it. Replace any of them with your own.

| Lens | What it governs |
|---|---|
| [`house-style.md`](../.agents/rules/house-style.md) | How prose reads to a person: no em-dashes, sentence-case headings, named sources, Mermaid for diagrams. Universal. |
| [`autonomy.md`](../.agents/rules/autonomy.md) | What an agent may do when nobody is watching, and what it may do with material it did not write. Universal; [`core.md`](../.agents/rules/core.md) is its one-line-per-rule summary every session loads. |
| [`review-quality.md`](../.agents/rules/review-quality.md) | The review rubric and severities, including the spec and standards axes `house-review` runs. |
| [`writing-for-agents.md`](../.agents/rules/writing-for-agents.md) | How a document behaves when an agent reads it: descriptions as pointers, completion criteria, the no-op test, model- versus user-invoked. New in the 2026-11 overhaul. |

## Tier B: semi-scalable (great for teams and clients)

| Skill | Status | What it does |
|---|---|---|
| `repo-explainer` | planned | A "start here" guided tour of an unfamiliar codebase. Strong for client onboarding. |
| `sop-drafter` | planned | Turn a described workflow into a documented standard operating procedure. |
| `security-audit` | planned | Repeatable dependency and secret scan with a written summary. |
| `adr` | planned | Architecture decision records / decision log entries. |

## Tier C: hyper-specific (personal, stays out of the shared kit)

The author's Content OS pipeline: `produce`, `clip-machine`, `repurpose`, `video-editing`, `video-cutting`, `episode-brief`, `youtube-transcript`, `idea-discovery`. These are showcase and portfolio demos ("look what is possible"), not plug-and-play for others. They live in their own repo, not here.

## Hooks: the rules that do not depend on remembering

Every skill above is prose. An agent follows it for as long as it holds it in context, which is fine for a rule you consult on purpose and useless for a rule that has to fire when nobody is thinking about it.

The [hooks module](../.agents/hooks/README.md) is the answer to the second kind. A hook is a small program your harness runs at a lifecycle event, and it comes in exactly two shapes: a **reminder** injects context and never blocks, and a **gate** refuses, but only when the condition can be decided mechanically rather than interpreted.

| Hook | Shape | Fires when |
|---|---|---|
| `delegation-reminder` | reminder | a delegated agent reports back in the foreground, to note that its summary is a claim and not evidence. A background launch is skipped, because nothing has come back yet |
| `spec-conformance-gate` | gate | work a contract governs is closed with no audit of whether the implementation matches it |
| `skill-reachability-reminder` | reminder | a session starts with none of this kit's skills reachable at either scope, so work that assumes one would proceed without it and nothing else would say so. A library of somebody else's skills does not count, which is what `bug-0021` fixed after a cloud container's own 24 skills silenced it |
| `install-currency-reminder` | reminder | a session starts in the kit's own repository and its install record no longer agrees with the working tree, so the copies you are working with are stale, have no digest baseline to be checked against, or were never installed. `install.py --check` has always been able to answer this; nothing ever asked it, and eighteen stale skills went unreported for ten days as a result |
| `worktree-boundary-reminder` | reminder | a shell command run inside a linked git worktree looks like it writes and names a path outside that worktree. Claude Code refuses an edit tool aimed at the main checkout but does not track where a `cp`, a `mv`, or a redirect writes, and its sandbox does not run on native Windows |
| `instruction-provenance-reminder` | reminder | a session starts with an `AGENTS.md`, `CLAUDE.md`, settings file, or MCP config that no commit vouches for: outside any repository, as in a Downloads folder, or present in one without being committed. Harnesses load these before anything else runs, so a planted one is an instruction from a stranger, and this is what names it |

These are the only things the kit ships that run inside your session, so they are opt-in (`install.py --with-hooks`) and you activate them yourself.

## What the kit borrows, and how you can check it

Some of what is above came from somewhere else, chiefly Balarama Bosch's [repoprompt-workflows](https://github.com/moonray/repoprompt-workflows) (MIT): four of the Epic B lenses, the review lens, and both hooks. Attribution for all of it is in [`NOTICE`](../NOTICE).

Prose credit on its own decays, though. This kit's own roadmap once credited a skill to an upstream workflow that had never been vendored here, and by the time anyone noticed, the folder that would have settled it was gone. So since `feat-0043` every adapted file also carries a **provenance block**: the exact upstream file it came from, the author, the license, the date it was retrieved, and the SHA256 of the bytes that were retrieved. Running `scripts/check-provenance.py` re-fetches each recorded source and tells you whether upstream has moved since.

Two properties are worth knowing if you adopt this. The digest is of the *upstream* file, never of the adapted local one, which differs on purpose, so what the check answers is "has the thing we adapted from changed", not "has anyone edited our copy". And the check only ever reports: it never rewrites an adapted file, because overwriting a house-styled adaptation with upstream's current text would silently undo the adaptation. A source that genuinely cannot be located is recorded as unlocatable rather than given a plausible-looking guess, since a wrong digest reads as verified.

## The two building blocks the whole kit reuses

- **`AGENTS.md`** as the canonical, cross-tool instruction file.
- **A harness-agnostic `SKILL.md` body** plus thin generated per-harness adapters. This is what makes any skill above portable.
