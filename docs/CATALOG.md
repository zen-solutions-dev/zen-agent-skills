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
| `project-bootstrap` | shipped | user | The front door: a stack-matched baseline (gitignore, editorconfig, linter and formatter, license, README stub) for a new or bare repository, plus a printed, never installed, pre-commit config, then `init-worktracking`. |
| `init-worktracking` | shipped | user | Scaffolds a lean `AGENTS.md`, `.quests/`, and by tier a roadmap and changelog into any repository, seeded by inspecting it. Then **configures the skills** for that repository: it explores, recommends, confirms one section at a time, and writes `docs/agents/zen.md`, which every skill reads for the tracker, glossary, specs, acceptance command, branches and default mode. Run it once per repository after installing. |
| `new-quest` | shipped | model | Turns an idea, bug, or approved spec into quest files (it was `new-task`, and still reads a `.tasks/` tracker), each sized to one fresh context window, sliced vertically, riskiest first, with an acceptance command and a `mode`: `afk` for work an agent can finish unattended, `hitl` for work that needs a person in the loop. Plans a prefactor first and one list of test seams per plan. Wide refactors are sequenced as expand, migrate, contract. Where `docs/agents/zen.md` opts in and the `triage` draft is installed, its publishing step loads that draft's publishing, which mirrors the tracker one way to GitHub issues (specs as issues, quests as sub-issues). |
| `fix-batch` | shipped | user | Dispatches independent quest files to parallel agents, each in its own worktree with a fresh context and told it is a leaf, then verifies every result. A missing field in a delegate's report blocks acceptance. Work whose items depend on each other goes to `orchestrate` instead. |
| `reconcile-worktrees` | shipped | user | Lands verified work one item at a time, either into the main checkout (real base, untracked files, phantom binary diffs, overlaps, leaving a reviewable diff uncommitted) or onto an integration branch as a fast-forward to the exact commit that was verified. |
| `house-review` | shipped | model | Reviews a change on two independent axes, spec (did it do what was asked, no more, no less, and every guard its contract states kept) and standards (the repository's `CODING_STANDARDS.md` or `CONTRIBUTING.md` plus the swappable `review-quality` lens and its smell baseline), plus a security axis, required on a one-way door, at a depth chosen from the change's size and risk. Every finding's quote must resolve against the file. After one fix round it re-checks only the fixed findings, then stops. Report only. |
| `pr-describe` | shipped | model | Drafts a pull request body and changelog entry in the target repository's own format, opening on the smallest visual that explains the change and in the glossary's terms, ending with the merge danger: one-way or two-way door and blast radius. Closes a linked GitHub issue correctly. Never touches GitHub itself. |
| `agent-handoff` | shipped | model | At a phase boundary, decides whether to continue, clear, hand off, dispatch a subagent, or compact, and writes the brief when it is a handoff. |
| `human-handoff` | shipped | model | Packages project state for a partner, client, or teammate, with client-facing redaction. A questionnaire mode asks someone else the questions the person cannot answer. |
| `doc-author` | shipped | model | Writes new, code-grounded Markdown documents: READMEs, architecture with Mermaid, guides, decision records. A guide whose steps a person must run can come with a standard-library setup wizard built on its `wizard.py`. |
| `doc-revise` | shipped | model | Revises an existing document in place, in its own voice, touching only what was asked. |
| `zen` | shipped | user | The router: says which skill or flow fits where you are, and which light path a small change can take instead, including the one-quest flow and the bug chain (`systematic-debugging`, then `tdd`). Reads the repository's declined-ideas register before it suggests a new skill. Hints only. |
| `retro` | shipped | user | Looks back over a session or pull requests and proposes environment changes so a correction is never needed twice: a check where the mistake has a fixed shape, a written standard only for a judgement call. Reads one session, a pull request, or a sample of about one session in five; ratchets a stricter check in with an exception list, and prunes a check that fires on good code. Reads the writing-for-agents lens while it classifies and the declined-ideas register before it proposes. Applies only what you approve. |
| `improve-architecture` | shipped | user | Finds the hot spots that make a codebase hard for an agent and proposes deepening refactors as an offline HTML report. Candidates feed `grill`, `spec-author` or `new-quest`. |
| `sitrep` | shipped | model | "Where are we" for one repository, from its tracked quest files and git, with an evidence tier on every figure, on the same rarity ladder `research` uses. Changes nothing. |
| `research` | shipped | model | One question against primary sources, by a fresh agent, written up as one cited markdown file that names every source it could not reach, each claim marked on the rarity ladder of source reliability (white unverified to gold independently confirmed). |
| `orchestrate` | shipped | user | Runs a day of work from one orchestrating session: plans with the person, dispatches research and build children on their own branches in frontier waves, lands each verified commit on one integration branch, then one review and one draft pull request for the person. Holds the conversation; children do the work. Lands by fast-forward or by a mechanical merge, keeps a dated, linted memory of decisions, problems, preferences and lessons, and offers a recurring job where a task plainly recurs. |
| `vet-skill` | shipped | user | Vets another author's skill before you install it: pins and digests the revision, checks provenance and license, inventories what it reads, runs and fetches, and hunts for prompt injection and exfiltration against the autonomy rules. Report only: install, install with changes, or do not install. |
| `ci-scaffold` | planned (hold) | | Generate CI matched to the detected stack. Hold until used twice. |
| `release-cut` | planned (hold) | | Version bump, changelog roll-up, tag, notes. Hold until used twice. |

## The contract-driven delivery spine (Campaign B)

These skills turn an agreed contract into verified work. Each was dogfooded on real in-kit work before it was blessed. Four (`spec-quality`, `spec-plan-readiness`, `test-quality`, `spec-conformance`) were folded in from `repoprompt-workflows` (Balarama Bosch, MIT), with provenance in [`NOTICE`](../NOTICE) and in a checkable block inside each adapted file. The kit dogfoods this spine on itself: specifications under [`docs/spec/`](spec/), tests under [`tests/`](../tests/).

| Skill | Status | Invocation | What it does |
|---|---|---|---|
| `grill` | shipped | model | "Grill me": an interview in rounds over the decision tree, one recommended answer per question, facts looked up rather than asked, closing with a decisions record. Explores before the first question, takes a dictated brain dump whole, writes each settled term to the glossary as it lands, and asks one question on module shape. The first step of any real change. |
| `domain-language` | shipped | model | Keeps the project's glossary, taking one term at a time from `grill` as it settles, and writes an ADR only when a decision is hard to reverse, surprising, and a real trade-off. Reports glossary-versus-code mismatches and offers the rename as its own quest; never renames code. |
| `spec-author` | shipped | model | Interviews the person with `grill` until no decision is open, or drafts straight from a decisions record they already confirmed in the conversation, then writes a behavioural spec with Given/When/Then scenarios, self-checks it with `spec-quality`, saves it as `draft`, and stops for human approval. |
| `spec-quality` | shipped | model | Lens: is a spec contract-level, observable, non-redundant, and free of open questions. Returns `ready` or `needs_revision`. |
| `spec-plan-readiness` | shipped | model | Go/no-go gate over an approved spec plus its quests. A blocked verdict authorizes no tests, code, or delegation. |
| `test-quality` | shipped | model | Lens for test design: the lowest faithful layer, an independent oracle, mocks only at system boundaries. Rejects tautological and implementation-coupled tests. Used by `tdd`, `test-author` and `fix-batch`. |
| `tdd` | shipped | model | Red-green development: agrees the seam first, then one behaviour at a time, watching each test fail for the right reason. |
| `test-author` | shipped | model | Tests after the fact: one per scenario of an approved spec, tagged `S-NNN`, plus characterization and regression tests. Never production code. |
| `spec-conformance` | shipped | model | Audits an implementation against its spec into a conformed, diverged, or not-built matrix. |
| `verifier-agent` | shipped | model | Runs the declared commands, composes `spec-conformance`, and returns `pass`, `fail`, or `blocked` with evidence, naming the exact commit it verified, before anything lands. Never edits what it verifies. |
| `doc-sync` | shipped | model | Detects documentation drift by checking prose against repository facts. Classifies each document as current-state, contract (report-only), or ledger (skipped). Dry run by default. |

## Drafts: built but not yet used on real work

A **draft** is written and lives under [`.agents/skills/`](../.agents/skills/), but has not yet been used on real work and refined from it. The Claude Code plugin never carries it, and the installer places it only when you ask with `--include-drafts`, and the installer names what it held back on every run rather than dropping it silently. Try them, and expect rough edges: real use is what promotes a draft. What each still owes is tracked in [`ROADMAP.md`](../ROADMAP.md).

| Skill | Status | Invocation | What it does |
|---|---|---|---|
| `systematic-debugging` | draft | model | Diagnoses a defect to its cause: a red command first (a person-in-the-loop loop when only a person can see the symptom), ranked hypotheses tested one at a time, secrets redacted from what it records, ending in one of three verdicts. Never fixes. Kept a draft at its first dogfood (`feat-0062`), where an independent check refuted the cause the run reached; a second independent run (`feat-0063`) is owed. |
| `agent-observatory` | draft | model | Questions across many agent sessions: what is running, what a wave cost, which skills were used, what failed. Never starts, resumes, interrupts, or ends a session. |
| `quest-tracker` | draft | model | Runs a season of project work from one shared tracker page, with agent sessions reporting finished work as claims a person verifies. Needs a host that publishes a page with a shared database, which today is Claude artifacts. |
| `triage` | draft | user | Triages a GitHub repository's open issues into the role labels `docs/agents/zen.md` names: reads each issue as data, recommends one role with a reason, and applies labels only on the person's go. Never runs code from an issue. Also holds the kit's opt-in tracker publishing, which `new-quest` loads. Stays a draft, with tracker publishing, until a live publish on a throwaway repository. |
| `teach` | draft | user | Teaches the person one concept at their level and checks it stuck: finds what they know, grounds the lesson in primary sources, teaches one small piece with an example from their own work, then asks them to retrieve or apply it. |
| `prototype` | draft | model | Answers one design question talk cannot settle with throwaway code: a logic prototype that drives a pure state model through hard cases, or several UI variants on one route, on a throwaway branch with the verdict recorded on the quest. `grill` and `wayfinder` reach for it. |
| `wayfinder` | draft | user | Charts an effort too big and too foggy for one session as a decision map: a destination, the frontier of decisions takeable now, the fog, and what is out of scope, resolving one decision per session by grilling, prototyping, research or a quest until a spec or quests can be written. |
| `wait-what` | draft | user | Re-pitches the last message when it did not land: restates it with the context the person lacks, in short plain sentences and the project's glossary terms. |

## Lenses: the swappable rules skills compose

Five rules modules under [`.agents/rules/`](../.agents/rules/) install alongside the skills, because a skill that composes a lens is not self-contained without it. Replace any of them with your own.

| Lens | What it governs |
|---|---|
| [`house-style.md`](../.agents/rules/house-style.md) | How prose reads to a person: no em-dashes, sentence-case headings, named sources, Mermaid for diagrams. Universal. |
| [`autonomy.md`](../.agents/rules/autonomy.md) | What an agent may do when nobody is watching, including how an orchestrator may land verified work it did not author on an integration branch (a fast-forward or a mechanical merge, `A8`) and the opt-in, sampled self-merge of a two-way door, what it may do with material it did not write (`A10`), and that it may not edit the check that judges its work (`A11`). Universal; [`core.md`](../.agents/rules/core.md) is its one-line-per-rule summary every session loads. |
| [`review-quality.md`](../.agents/rules/review-quality.md) | The review rubric and severities, including the spec and standards axes `house-review` runs, the security axis for a one-way door, and a baseline of code smells. |
| [`deep-modules.md`](../.agents/rules/deep-modules.md) | The vocabulary for module shape: deep modules with small interfaces, seams, and depth. Composed by `improve-architecture`, `grill`, `new-quest` and `house-review`; it was `improve-architecture`'s `references/vocabulary.md`. |
| [`writing-for-agents.md`](../.agents/rules/writing-for-agents.md) | How a document behaves when an agent reads it: descriptions as pointers, completion criteria, the no-op test, model- versus user-invoked, write history rather than the present, and composition that loads the sibling rather than naming it. |

## Tier B: semi-scalable (great for teams and clients)

| Skill | Status | What it does |
|---|---|---|
| `repo-explainer` | planned | A "start here" guided tour of an unfamiliar codebase. Strong for client onboarding. |
| `sop-drafter` | planned | Turn a described workflow into a documented standard operating procedure. |
| `security-audit` | planned | Repeatable dependency and secret scan with a written summary. |
| `adr` | covered | No separate skill: the shipped `domain-language` writes an architecture decision record when a decision is hard to reverse. |

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
| `destructive-git-gate` | gate | a shell command is about to run a git operation that loses work or history the reflog cannot restore: a force push without a lease, `reset --hard`, a forced `clean`, `branch -D`, and the like. Read from the parsed command, never a pattern over its text. The one hook no committed wiring registers, in any harness |
| `observatory-event` | reminder | a turn finishes and a local observatory may be watching. It injects nothing and blocks nothing: it appends one line to a spool file that nothing reads unless the [observatory](OBSERVATORY.md) is running |

These are the only things the kit ships that run inside your session, so they are opt-in (`install.py --with-hooks`) and you activate them yourself.

## What the kit borrows, and how you can check it

Some of what is above came from somewhere else, chiefly Balarama Bosch's [repoprompt-workflows](https://github.com/moonray/repoprompt-workflows) (MIT): four of the Campaign B lenses (Campaign B was Epic B), the review lens, and two of the hooks, `delegation-reminder` and `spec-conformance-gate`. Attribution for all of it is in [`NOTICE`](../NOTICE).

Prose credit on its own decays, though. This kit's own roadmap once credited a skill to an upstream workflow that had never been vendored here, and by the time anyone noticed, the folder that would have settled it was gone. So since `feat-0043` every adapted file also carries a **provenance block**: the exact upstream file it came from, the author, the license, the date it was retrieved, and the SHA256 of the bytes that were retrieved. Running `scripts/check-provenance.py` re-fetches each recorded source and tells you whether upstream has moved since.

Two properties are worth knowing if you adopt this. The digest is of the *upstream* file, never of the adapted local one, which differs on purpose, so what the check answers is "has the thing we adapted from changed", not "has anyone edited our copy". And the check only ever reports: it never rewrites an adapted file, because overwriting a house-styled adaptation with upstream's current text would silently undo the adaptation. A source that genuinely cannot be located is recorded as unlocatable rather than given a plausible-looking guess, since a wrong digest reads as verified.

## The two building blocks the whole kit reuses

- **`AGENTS.md`** as the canonical, cross-tool instruction file.
- **A harness-agnostic `SKILL.md` body** plus thin generated per-harness adapters. This is what makes any skill above portable.
