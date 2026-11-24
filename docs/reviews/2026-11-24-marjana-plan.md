# 2026-11-24 Marjana overhaul: plan

Status: **approved** 2026-11-24. The maintainer set the direction in the session's opening brief and took the recommended option on four one-way-door questions (below). Orchestrated from one cloud session; research and implementation run in child sessions; everything lands on the integration branch `zen/marjana-2026-11-24` and reaches the maintainer as **one** pull request into `main`.

"Gundicha Marjana" is the maintainer's name for this pass: a thorough deep clean. Context, instruction files, ledgers and skills accrete; this round takes the dust out, brings every skill current with what the sources teach, and proves each one on real work.

## Inputs

- [Sources delta](2026-11-24-sources-delta.md) (`R1`): what Matt Pocock's skills, aihero.dev, and his repository at `d653911` teach that the [2026-11 overhaul](2026-11-overhaul-plan.md) did not adopt. About 45 rows, an install-time setup design, and an orchestrator design.
- [Marjana inventory](2026-11-24-marjana-inventory.md) (`R2`): measured context load, an `AGENTS.md` target outline, a ledger archive scheme, stale claims, open-task triage, retro proposals owed, per-skill health, stale branches. Proposals `P1` to `P13`.
- **Not reached:** the video `mU8WKII1gpk`. YouTube's bot check refused both the research session and the orchestrator (2026-11-24), and nobody tried to get around it. The video-derived conclusions in the 2026-11 overhaul plan, which read the full transcript on 2026-11-23, stand. The maintainer's own notes on the episode are welcome as a later input.

## Decisions (maintainer, 2026-11-24)

| # | Question | Decision |
|---|---|---|
| D1 | May an orchestrator merge other agents' work into an integration branch? (`A8` today: never merge your own work) | **Yes, with guards.** Only work it did not author, only after someone else verified it (`A7`), only into an integration branch. A person always merges into `developer` or `main`. Written into `autonomy.md` and `core.md`. |
| D2 | Where does the per-repository setup file live? | **`docs/agents/zen.md`**: prose plus one parseable `zen-config` block, written by a new `init-worktracking` step. The path and the block format are the one-way door, so they get a spec. |
| D3 | Stale remote branches | **Delete** `zen/overhaul-ws1-align` (already in `main`). **Tag, then delete** `zen/eval-slice-71f3d5` as `archive/eval-slice-71f3d5`. **Keep** the three oversight tasks: cherry-pick `feat-0073`, `feat-0074` and `feat-0075` from `claude/2026-10-22-oversight-tasks` into `.tasks/`, then delete that branch. Done by the orchestrator after the PR is opened, and reported in it. |
| D4 | Pull request target | **`main`**: one review, one merge. `developer` is fast-forwarded to match afterwards. |

Decisions the orchestrator took as two-way doors, each reversible by one revert: all of `P1` to `P8`, `P10` to `P13`; the retro proposals `R-001`, `R-005` and `R-007` (filed in the platform workstream); `R-003` and `R-004` stay owed and are recorded, not built; the three status drafts (`sitrep`, `quest-tracker`, `agent-observatory`) stay drafts in the kit this round, with health fixes only, and the personal-tier question is recorded on the roadmap.

## Principles this round adds

Each is written, in our own words, into the skill or lens named.

1. **Keep the always-loaded file nearly empty.** Only what is undiscoverable and globally relevant. The reasons live beside the rules, one link away. (`AGENTS.md`, the `init-worktracking` templates)
2. **A count or a status written as prose rots.** Derive it, or check it mechanically. (`ROADMAP.md`, a new roadmap draft-status check)
3. **One orchestrator holds the conversation; children do the work.** Research and build in fresh contexts, each on its own branch, landing on one integration branch, reaching the person as one pull request. (new `orchestrate`, draft)
4. **AFK or human-in-the-loop is a named choice per piece of work**, set by the door and the blast radius. (`mode` in task files, `orchestrate`, `zen`)
5. **Review once, fix once, then stop.** Re-check only the fixed findings. (`house-review`, `orchestrate`)
6. **Write history, not the present.** Date every claim; cite the commit a code claim was true at. (`writing-for-agents.md`, `orchestrate` memory)
7. **Skills speak in roles; one file per repository says what each role is there.** (`docs/agents/zen.md`)
8. **Composition must load, not merely mention.** A composing step says "read and follow" the sibling. (`writing-for-agents.md`, composing skills)
9. **Ratchet and prune.** A stricter check lands with an exception list; a check that fires on good code is removed. (`retro`)

## Workstreams

Five child sessions run in parallel. Each owns a disjoint set of paths. Task ids are reserved here so parallel sessions cannot collide.

| Workstream | Task | Owns | Delivers |
|---|---|---|---|
| **WS-A Context and ledgers** | [`chore-0100`](../../.tasks/done/chore-0100-marjana-context-and-ledgers.md) | `AGENTS.md`, `CLAUDE.md`, `docs/rationale/`, `CONTRIBUTING.md`, `docs/ARCHITECTURE.md`, `ROADMAP.md`, `CHANGELOG.md`, `docs/history/` (new), `docs/reviews/README.md` (new), `README.md`, `docs/CATALOG.md`, `docs/GETTING-STARTED.md`, `docs/INSTALL.md`, `docs/OBSERVATORY.md`, `docs/ISSUE-LINKING.md`, `.claude/settings.json`, task-file moves under `.tasks/` | `P1` rule-only `AGENTS.md` (target at most 10 KB), `P13` one-line `CLAUDE.md`; `P3` true "Current state" and the finished overhaul sections retired; `P4` and `P5` monthly archives under `docs/history/`; the missing `CHANGELOG.md` lines for PR #110 and PR #113; `P6` close `chore-0098` and `chore-0077`; `D3`'s cherry-pick of `feat-0073` to `feat-0075`; `P7` stale claims; `P12` the reviews index; the payload-measuring section in `docs/INSTALL.md` (`R1`, context hygiene) |
| **WS-B Setup and align** | [`feat-0091`](../../.tasks/feat-0091-marjana-setup-and-align.md) | `.agents/skills/` `init-worktracking`, `project-bootstrap`, `zen`, `grill`, `domain-language`, `spec-author`, `spec-quality`, `spec-plan-readiness`, `new-task`; `.tasks/README.md`, `.tasks/_TEMPLATE.md`, `.tasks/validate.py`; `GLOSSARY.md`; `docs/agents/` (new); `docs/spec/zen-config*.md` (new), `docs/spec/spec-author*.md` | `D2`: the `zen-config` spec, the "configure the skills" step in `init-worktracking`, and this repository's own `docs/agents/zen.md` as the first real run; `P2` both scaffolds user-invoked; a leaner seeded `AGENTS.md` template; the `mode: afk or hitl` task field; `grill` fog, out-of-scope and "prompt with the why"; `domain-language` tests a name against real sentences; `project-bootstrap` prints a pre-commit config; the quality-bar line; `P10` for the skills it owns; the `chore-0074` fix in `new-task` |
| **WS-C Orchestrate and build** | [`feat-0092`](../../.tasks/done/feat-0092-marjana-orchestrate-and-build.md) | `.agents/skills/` `orchestrate` (new), `research` (new), `fix-batch`, `reconcile-worktrees`, `verifier-agent`, `spec-conformance`, `agent-handoff`, `tdd`, `test-author`, `test-quality`, `systematic-debugging`; `.agents/rules/autonomy.md`, `.agents/rules/core.md`; `docs/spec/verifier-agent*.md`, `docs/spec/test-author*.md`, `docs/spec/systematic-debugging*.md` | `D1` in `autonomy.md` and `core.md`; draft `orchestrate` (`R1`'s seven steps, frontier waves, relay format, rework cap, dated memory, one review then stop, an optional Claude Code cloud section); draft `research` (both research reports today are its first real runs); `reconcile-worktrees` lands on an integration branch; `agent-handoff` compact cue and durability line; optional cross-family review line in `verifier-agent`; `P10` for the skills it owns |
| **WS-D Ship, learn and lenses** | [`feat-0093`](../../.tasks/done/feat-0093-marjana-ship-learn-and-lenses.md) | `.agents/skills/` `house-review`, `pr-describe`, `doc-author`, `doc-revise`, `doc-sync`, `human-handoff`, `retro`, `improve-architecture`; `.agents/rules/writing-for-agents.md`, `house-style.md`, `review-quality.md`; `docs/spec/house-review*.md`, `docs/spec/doc-sync*.md` | `house-review` stopping rule and comment-as-fig-leaf smell; `pr-describe` offers a stacked split for a large branch holding a one-way door; `retro` sampled sessions, ratchet, and checks audit; `human-handoff` questionnaire mode; a runbook may ship as a stdlib script (`doc-author`); `writing-for-agents.md` "write history, not the present" and "composition must load"; `P10` for the skills it owns, including `doc-sync` and `house-review` under 250 lines |
| **WS-E Platform and gates** | [`feat-0094`](../../.tasks/feat-0094-marjana-platform-and-gates.md) | `scripts/`, `tests/`, `.github/workflows/`, `.agents/hooks/`, `.agents/skills/` `sitrep`, `quest-tracker`, `agent-observatory`; `docs/spec/` files for `validate-skills`, `install`, `build-adapters`, `cloud-executable`, `tracker-links`, `agent-observatory`, `sitrep` | `R-005` the "Done when" validator warning; the `P3` roadmap draft-status check; `P11` the budget headline counts only what loads; `R-001` hermetic home for the test gate; `R-007` undecodable-name tests; `install.py` prints the one-line pointer to the setup step; `feat-0090` with `chore-0059` closed inside it; health fixes for the three status drafts; optionally an opt-in destructive-git gate hook and the Codex sidecar |

**Integration** ([`feat-0095`](../../.tasks/feat-0095-marjana-integrate-verify-and-ship.md), the orchestrator): land each workstream after one review; write the reader documents for the new skills; regenerate `.claude-plugin/`; an independent verification by a session that wrote none of it (`A7`); `retro` over this session; `pr-describe`; one draft pull request into `main`; then `D3`.

## Rules for every workstream session

1. **Branches.** Start from `zen/marjana-2026-11-24`. Work on `zen/marjana-<workstream>`. Push it; **do not open a pull request** (the maintainer reviews one, at the end). Before you report, merge the integration tip into your branch, so landing is a fast-forward. Never merge into `zen/marjana-2026-11-24`, `developer` or `main` (`A8`).
2. **Read first**: `AGENTS.md`, your task file, this plan, the sections of the two research reports your task cites, and [`writing-for-agents.md`](../../.agents/rules/writing-for-agents.md), the yardstick for every skill you write.
3. **Stay inside your owned paths.** Three exceptions: regenerate `.claude-plugin/` with `python3 scripts/build-adapters.py --marketplace` when you change a shipped skill or a lens; update a test that pins the text or metadata of a skill you own, and name it in your report; and move your own task file to `.tasks/done/` at close. Only WS-A edits `CHANGELOG.md`, `ROADMAP.md`, `README.md` and `docs/CATALOG.md`; everyone else lists what those should say under **Notes for integration**, including the one `CHANGELOG.md` line for their task.
4. **Study, do not copy.** Clone `https://github.com/mattpocock/skills` (MIT) into a scratch directory outside this repository when you need it. Write in this kit's own words; add a provenance block per `AGENTS.md` for adapted material, fetched with `urllib` and digested with `hashlib`.
5. **New skills are drafts**: `license: MIT`, and `status: draft` under `metadata`; a skill a person starts also carries `invocation: user`.
6. **Slim what you own**: incident history out of procedures into `references/`; one pointer line to `core.md`; descriptions lead with the trigger, third person, under about 400 characters; every workflow step ends with a "Done when"; no body over about 250 lines without a one-line reason.
7. **Amended contracts.** A behaviour change to a skill with a spec under `docs/spec/` amends the spec with a dated note naming your task, brings its conformance matrix up to date, and says in your report that the amendment needs the maintainer's approval.
8. **Dogfood every skill you own.** Run it on real work in this overhaul, or on a realistic scratch target outside the repository when real work cannot exercise it, and record each run in `docs/reviews/2026-11-24-dogfood/<workstream>.md`: skill, what it ran on, the evidence (command and output, or the file it produced), the verdict (works, fixed, or broken), and what changed in the skill because of it. A skill you could not exercise is recorded as not exercised, with the reason. Never write a run that did not happen.
9. **Acceptance.** `ZEN_CHECKS_SCOPE=full python3 scripts/run-checks.py` exits 0 before you push. Report the command and the verbatim tail of its output (`A4`).
10. **Commits** carry no `Co-Authored-By` trailer (`AGENTS.md`).
11. **Subagents**, if you use any, start with a fresh context, are told they are leaves, and run at medium effort unless they verify or debug.
12. **Report** with `send_message` to the orchestrator session `session_017QLseomNtJvsnYxQu8HkHp`: the branch, the head commit, at most 20 lines of summary, the run-checks tail, **Notes for integration**, and any question only the maintainer can answer. Then stop. A review comes back once; fix what it asks, re-run the checks, report again.

## Landing

The orchestrator lands each workstream after **one** review by a fresh-context reviewer that wrote none of it, following `house-review` (both axes: this plan and the task, then the written standards). One fix round, a focused re-check of the fixed findings, then it lands. Conflicts in `.claude-plugin/` are resolved by regenerating it, never by hand.
