# 2026-11 overhaul: what Matt Pocock's skills teach this kit

Status: **approved** 2026-11-23. The maintainer took the recommended option on every decision below and all four scope areas.

## Sources

- `mattpocock/skills` at `abeeaf9` (v1.3.2, MIT): every `SKILL.md`, its supporting files, `SCOPE.md`, `.out-of-scope/`, the ADRs, and the per-skill docs pages.
- "How to Actually Code with AI (ft. Matt Pocock)", NetworkChuck, YouTube `mU8WKII1gpk`: the full transcript.
- This repository at `main` = `b61dab8`: every skill, rule, hook and script, the open backlog, the unmerged branches, and a full `run-checks.py` run (exit 0, nine of nine gates).

The aim is to learn from Matt's work, not to copy it. Where a skill here adapts his text, it carries a provenance block per `AGENTS.md`.

## The short version

1. **The kit is rigorous at the back of the pipeline and thin at the front.** Verification, evidence, worktree recovery and review evidence are better here than anywhere comparable. But nothing gets the agent aligned with the person before the spec is written: [`spec-author`](../../.agents/skills/spec-author/SKILL.md) deliberately asks "at most one question". Matt's most-used skill is the opposite: a relentless, structured interview.
2. **Nothing closes the learning loop.** No retro, no shared glossary, no decision records. Matt's loop ends with "how can I improve my environment so I never have to write this comment again?", and the answer is almost always a deterministic check rather than more prose.
3. **The kit is heavy to carry.** 4,748 lines across 24 skills, a default install that puts 18 descriptions (10,209 characters) into every session, 15 skills linked in one cycle so no skill installs alone, and the same autonomy paragraph repeated 24 times.
4. **The everyday skills a developer reaches for are missing**: grilling, test-driven development, retro, architecture improvement, a glossary. Of the gaps the audit checked, only handoff is covered.
5. **Distribution does not update itself.** There is no committed plugin marketplace, the docs still point at `hams-ollo/zen-agent-skills`, and the installer has two hazards the audit reproduced.

## Side by side

| Concern | Matt Pocock's skills | This kit today | Verdict |
|---|---|---|---|
| Alignment before work | `grilling`: design tree, rounds over the frontier, a recommendation per question, facts found by a subagent, decisions put to the user | `spec-author` asks at most one question | **Adopt** |
| Shared language | Glossary and ADRs grown lazily during grilling; every skill reads the glossary | None (`doc-author` can write an ADR on request) | **Adopt** |
| Decomposition | `to-tickets`: vertical tracer-bullet slices, each sized to one fresh context window, blocking edges, expand-contract for wide refactors | `new-task`: honest `touched_files`, `depends_on`, an acceptance command | Keep ours, **add** slice sizing and expand-contract |
| Implementation | `implement-spec`: a fresh subagent per ticket in a worktree, one integration branch | `fix-batch`: parallel worktrees, a nine-field report, verifier before landing | Keep ours, **add** fresh-context and effort guidance, slim it |
| Tests | `tdd`: seams agreed first, test through narrow interfaces, no tautological tests | `test-author` runs after the implementation | **Adopt** a `tdd` skill |
| Debugging | `diagnosing-bugs`: no red-capable command, no hypothesis phase | `systematic-debugging` (draft): hypothesis budget, three verdicts | Keep ours, **add** feedback-loop-first, then promote |
| Review | `code-review`: two independent axes, spec and standards; the standards file is read at review time | `house-review`: evidence gate on every quote; `review-depth` picks the depth in 380 lines | Keep the evidence gate, **add** the two axes, fold `review-depth` in |
| PR | `pr`: evidence, one-way or two-way door, blast radius | `pr-describe`: closing keywords done right | Keep ours, **add** merge danger |
| Learning loop | `retro`: mechanical mistake becomes a check, judgement becomes a standard | None | **Adopt** |
| Architecture | `improve-codebase-architecture`: git hot spots, deep modules, a before-and-after report | None (`maintainability-review` on hold) | **Adopt** as a draft |
| Context management | Phase boundaries: continue, clear, handoff, subagent, compact; "context paranoia" near 150k tokens | `agent-handoff`, `human-handoff` | **Add** the boundary tree |
| Authoring doctrine | `writing-for-agents`: pointers, leading words, positive phrasing, the no-op test, pruning | `house-style.md` (prose conventions) and the validator | **Adopt** as a lens |
| Invocation | Orchestrators are user-invoked and cost no description budget | Every skill is model-invoked | **Adopt** |
| Routing | `ask-matt` maps every skill | The README diagram | **Adopt** as a `zen` router |
| Distribution | Self-updating plugin marketplace | `install.py` symlinks; plugin tree generated, not committed | **Adopt** if the rules module can travel in it |
| Testing the kit | One CI check: frontmatter parses | Nine gates, 1,254 tests, six CI cells | Ours is stronger; keep it |
| Evals | None ("my evals are people") | A pre-registered eval slice on an unmerged branch, never run | Keep ours on the roadmap |

## Principles this overhaul adopts

Each is written in our own words in the skill or lens named.

1. **Grill before you spec.** The agent interviews until the decision tree is empty. Finding facts is the agent's job; decisions are the person's. (`grill`, `spec-author`)
2. **Mint the language as you go.** A term is added to the glossary the first time a grilling session settles it. An ADR is written only when a decision is hard to reverse, surprising without context, and a real trade-off. (`domain-language`)
3. **Size work by context, not by calendar.** A task fits one fresh context window. When work will not fit, it goes through spec and tasks rather than one long session. (`new-task`, `fix-batch`, `agent-handoff`)
4. **Every subagent starts fresh.** A dispatched agent gets a fresh context, not a fork, and is told it is a leaf. Medium effort by default; high effort for verification and debugging. (`fix-batch`, `verifier-agent`)
5. **Always choose determinism.** A repeated correction becomes the cheapest deterministic check that catches it: type, lint rule, test, hook, CI. Only genuine judgement calls go to a standards file, which review reads and implementation does not. (`retro`, `house-review`)
6. **Review on two axes.** Did the change do what the contract asked, no more and no less? Does it meet the written standards? Two independent passes, each with our evidence gate. (`house-review`)
7. **State the merge danger.** Every PR says whether it is a one-way or two-way door and how wide its blast radius is, which tells the human how hard to look. (`pr-describe`)
8. **Write for agents.** A description is a pointer: lead with the word that triggers it. Say what to do rather than what not to do. Delete any sentence that does not change behaviour against the model's default. (`writing-for-agents` lens)
9. **Keep the description budget for what the model should reach for unprompted.** Orchestrators a person starts are user-invoked. (validator, frontmatter)

## What we deliberately do not adopt

- **Wrapper skills that only say "call the other skill".** Matt's most-reported problem is the agent not loading the composed skill. Our relative-link composition is sturdier, because the install profile pulls the dependency in. We compose by link where the composition must work, and name the skill in backticks where it is only a neighbour.
- **Hand-written per-skill docs pages with no check.** His have drifted from the skills. Our catalog stays small and link-checked.
- **Author-named skills** (`ask-matt`, `setup-matt-pocock-skills`). The router here is `zen`.
- **Leaving recursion to the harness.** His docs record a review fanning out to 50+ agents. Our dispatched agents are told they are leaves.
- **Blind repo-wide substitutions.** His em-dash sweep broke frontmatter in six skills. Our validator already parses YAML; every rewrite here runs it.
- **"No evals."** We keep the eval slice as the route to measuring whether a skill helps.

## What this kit keeps, because it is better

The `pass`, `fail` or `blocked` verifier; the command plus its verbatim output as evidence (`A4`); the review evidence gate; `doc-sync`'s dry-run-by-default classification; the worktree recovery lessons; the prompt-injection rule `A10`; hooks that block only when nobody could disagree; the idempotent, reversible installer; provenance with upstream digests; and the nine-gate acceptance command.

## Slimming rules for every workstream

Apply these to every skill a workstream owns:

- Move incident history out of procedures into `references/`. A procedure says what to do; the reference says why.
- Replace the repeated autonomy paragraph with one pointer line to `core.md`. The validator still sees the reference.
- Descriptions lead with the triggering word, in the third person, one trigger per branch, under about 400 characters.
- Link a sibling `SKILL.md` only where the skill genuinely composes it; otherwise name it in backticks. This breaks the 15-skill cycle.
- Target: no `SKILL.md` over about 250 lines, and a median under about 120.

## Workstreams

### Phase 0: groundwork (orchestrator, before dispatch)

- Integration branch `zen/overhaul-2026-11` from `developer`, and this plan committed on it.
- The `writing-for-agents` lens in `.agents/rules/`, with provenance, so every workstream rewrites against the same yardstick.
- The invocation convention: a user-invoked skill declares `invocation: user` under `metadata`. claude.ai and the Skills API reject a seventh frontmatter key, so the source stays six-key and the Claude Code install paths render `disable-model-invocation: true` (WS4).
- One task file per workstream, ids reserved up front so parallel sessions cannot collide.
- Repository URLs move from `hams-ollo` to `zen-solutions-dev`.

### Phase 1: four parallel child sessions

Each session owns a disjoint set of paths. None edits `README.md`, `docs/CATALOG.md`, `docs/GETTING-STARTED.md` or `ROADMAP.md`; each adds one line to `CHANGELOG.md` and lists its catalog and roadmap notes in its PR body for Phase 2.

| Workstream | Owns | Delivers |
|---|---|---|
| **WS1 Align** | `grill/`, `domain-language/`, `spec-author/`, `spec-quality/`, `spec-plan-readiness/`, `new-task/` | New `grill` and `domain-language` skills; `spec-author` composes `grill`; `new-task` sizes tasks to one fresh context, prefers vertical slices, sequences wide refactors as expand-contract; slimming |
| **WS2 Build** | `tdd/`, `test-author/`, `test-quality/`, `fix-batch/`, `reconcile-worktrees/`, `verifier-agent/`, `spec-conformance/`, `systematic-debugging/`, `agent-handoff/` | New `tdd` skill; deep-module and tautology checks in `test-quality`; fresh-context, leaf and effort guidance in `fix-batch`; feedback-loop-first in `systematic-debugging`; the phase-boundary tree in `agent-handoff`; slimming |
| **WS3 Ship and learn** | `retro/`, `improve-architecture/`, `house-review/`, `review-depth/`, `pr-describe/`, `doc-author/`, `doc-revise/`, `doc-sync/`, `human-handoff/`, `.agents/rules/review-quality.md` | New `retro` and draft `improve-architecture`; two-axis `house-review` reading a standards file, with `review-depth` folded in; merge danger in `pr-describe`; slimming |
| **WS4 Platform** | `scripts/`, `tests/`, `docs/INSTALL.md`, `.claude-plugin/` | Fix the two installer hazards; `--include-drafts`; install a single skill and its closure; adapters and the plugin tree exclude drafts (`chore-0077`); a committed, self-updating Claude Code marketplace if the rules module can travel inside it |

### Phase 2: integrate, document, verify, install

- The `zen` router skill, user-invoked, mapping every skill and when to reach for it.
- `README.md` with the quick start first, `docs/CATALOG.md`, `docs/GETTING-STARTED.md`, `ROADMAP.md` refreshed, and install profiles recomputed.
- `run-checks.py` green, then an independent verification by an agent that wrote none of it (`A7`).
- One PR from the integration branch into `developer` for the maintainer to review.
- Reinstall into the maintainer's Claude Code.

## Rules for every workstream session

1. **Branches.** Start from `zen/overhaul-2026-11`. Work on your own branch, `zen/overhaul-<workstream>`, and open a **draft** pull request into `zen/overhaul-2026-11`, never into `developer` or `main`. Never merge your own work (`A8`).
2. **Read first**: `AGENTS.md`, your task file, this plan, and [`writing-for-agents.md`](../../.agents/rules/writing-for-agents.md). The lens is the yardstick for every skill you write or rewrite.
3. **Study, do not copy.** Clone `https://github.com/mattpocock/skills` (MIT) into a scratch directory **outside** this repository. Write every adapted skill in this kit's own words and voice, then add a provenance block per `AGENTS.md`, fetched with `urllib` and digested with `hashlib`. Never commit his files.
4. **Stay inside your owned paths.** Outside them, the only edit allowed is one dated line in `CHANGELOG.md`. List anything `README.md`, `docs/CATALOG.md`, `docs/GETTING-STARTED.md`, `ROADMAP.md` or `AGENTS.md` should say under a **Notes for integration** heading in your pull request body.
5. **New skills are drafts**: `license: MIT` and `status: draft` under `metadata`. A skill a person starts by name also carries `invocation: user` under `metadata`.
6. **Slim what you own**, per the slimming rules above.
7. **Amended contracts.** When you change the behaviour of a skill that has a spec under `docs/spec/`, amend the spec with a dated amendment note naming your task, bring its conformance matrix citations up to date, and say in the pull request that the amendment needs the maintainer's approval.
8. **Acceptance.** `python scripts/run-checks.py` exits 0 before you push. Paste the command and the verbatim tail of its output in the pull request body (`A4`).
9. **Commits** carry no `Co-Authored-By` trailer (`AGENTS.md`).
10. **Subagents**, if you use any, start with a fresh context, are told they are leaves, and run at medium effort unless they verify or debug.
11. **Close out** per the lifecycle in `AGENTS.md`: the task file moves to `.tasks/done/` with its links re-anchored, and one `CHANGELOG.md` line.

## Decisions for the maintainer

1. **New skills and "no skill ships cold".** Recommended: land them as drafts, add `--include-drafts` to the installer, install them locally, and promote each after real use. This keeps the contribution bar.
2. **How hard to slim.** Recommended: moderate. Apply the slimming rules, fold `review-depth` into `house-review`, keep every other skill name. The aggressive option also merges `doc-author` into `doc-revise` and moves the three status drafts (`sitrep`, `agent-observatory`, `quest-tracker`) out of the shared kit.
3. **Which new skills.** Recommended: `grill`, `domain-language`, `retro`, `tdd`, `improve-architecture` (draft), and the `zen` router.
4. **Merge authority.** Recommended: child sessions open draft PRs into the integration branch, the orchestrator reviews and merges those, and the maintainer reviews the one PR into `developer`.
5. **Stale branches.** `claude/developer-branch-review-j26u9s` is superseded. `claude/2026-10-20-quest-tracker-skill` is superseded and still carries the client's name and private page links that `main` removed. Recommended: delete both. `zen/eval-slice-71f3d5` and `claude/2026-10-22-oversight-tasks` stay.
