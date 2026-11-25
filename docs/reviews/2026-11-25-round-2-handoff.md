# Handoff: Marjana round 2

Written on 2026-11-25 by the orchestrating session of the first Marjana round (session `session_017QLseomNtJvsnYxQu8HkHp`), following `agent-handoff` Step 3. It is the whole brief: the next session runs from this file and the files it points to, with no memory of the session that wrote it.

## 1. Job and kind of work

You are the **orchestrating session for round 2** of the Zen Agent Skills overhaul. The work: turn the maintainer's decisions of 2026-11-25 into changes to the kit, run by child sessions, landed on one integration branch, and handed to the maintainer as **one draft pull request into `developer`** (decision G8). Kind of work: orchestration. You plan, brief, relay, land and verify by delegation; children write the changes. Default mode `hitl` (this repository's `docs/agents/zen.md`): every item marked as a check-in gate below waits for the maintainer.

## 2. Context and reach

You start with a fresh context and no memory of the session that wrote this. The procedure you follow is the kit's own `orchestrate` draft: read `.agents/skills/orchestrate/SKILL.md` and its `references/` now and follow them, and record each place the skill fell short, since this round is its second real run.

## 3. Do-not-touch constraints

- **Never merge into `developer` or `main`.** The maintainer merges. Rule `A8` and its exception in `.agents/rules/autonomy.md` bind you; decision B1 loosens that exception (mechanical-only orchestrator merges, re-checked and listed in the PR), but the loosened text is a round 2 deliverable, so until it lands, land children by fast-forward only.
- **No `Co-Authored-By` trailer** on any commit (`AGENTS.md` section 6).
- **Do not copy Matt Pocock's files.** Write in this kit's words, with a provenance block per `CONTRIBUTING.md`, fetched with `urllib` and digested with `hashlib`.
- **Do not touch `zen-solutions-ops` or `zen-solutions-site`.** F2 (the knowledge wiki) and G9 (the website) are separate efforts; plan them, do not build them here.
- **Do not cut a release tag** (D5) without the maintainer's go: the first tag is outward-facing.
- **Do not schedule recurring jobs on any repository** (F1) without the maintainer naming the repository.
- **Do not delete branches or push tags**: the session proxy refuses both (retro `R-207`). Hand those to the maintainer as commands.

## 4. Read these first, in order

1. `AGENTS.md` and `docs/agents/zen.md`.
2. This file.
3. [`2026-11-25-marjana-decisions.md`](2026-11-25-marjana-decisions.md): every decision, verbatim, and what is still open.
4. [`2026-11-25-skills-coverage-map.md`](2026-11-25-skills-coverage-map.md): all 39 of Matt's skills against ours, the rules that block adoption, and what each adoption takes.
5. [`2026-11-25-podcast-extraction.md`](2026-11-25-podcast-extraction.md): the podcast's loop, practices and the 34 items new to the kit.
6. [`2026-11-24-retro-marjana.md`](2026-11-24-retro-marjana.md): proposals `R-201` to `R-210`.
7. [`2026-11-24-marjana-plan.md`](2026-11-24-marjana-plan.md): how round 1 was run (rules for child sessions, landing), which worked.
8. `.agents/skills/orchestrate/references/first-run.md`: the lessons from round 1.

## 5. Background: what is proven, as of 2026-11-25

- **Round 1 is pull request #117** (`zen/marjana-2026-11-24` into `main`, head `d72b064`): CI green on all six cells, independently verified (`pass`), not merged when this was written. It shipped the deep clean, the setup step (`docs/agents/zen.md`), the drafts `orchestrate` and `research`, rule D1, the review stop rule, and new gates. Its dogfood records are under `docs/reviews/2026-11-24-dogfood/`.
- **The maintainer approved** every pending contract (A1 to A7, A9), the retro proposals B2 to B9 and B11, and every gap item E1 to E9. See the decision record for C, D and F.
- **What worked in round 1**: two research children, then five build children with disjoint paths; reports by `send_message`, no intermediate PRs; one fresh-context landing review each, one fix round, a focused re-check pinned to the exact commit; landing by fast-forward; one PR.
- **What failed or cost time**: task-file moves broke shared links (`R-202`); a shared test count collided (`R-203`); children ran without the kit installed (`R-205`); worker restarts lost branch tracking (`R-206`); branch deletion and tag pushes are refused by the proxy (`R-207`); a relay crossed a report (`R-208`).
- **Environment facts**: YouTube refuses cloud addresses for transcripts, and the Eden connector's `eden_read_social_post` fetches them. GitHub's GraphQL is refused; open PRs with `gh api repos/<owner>/<repo>/pulls`. CI runs only on the final PR this round (B10: Later).
- **Effort** (C5): medium for children, high for verifiers and debugging.

## 6. Scope, in phases, with check-in gates

**Phase 0: preconditions.**

1. Check whether #117 has merged into `main` and whether `developer` has been fast-forwarded to it (G1 asked for that). If #117 is merged and `developer` is behind, fast-forward it. If #117 is not merged, **stop and check in**: round 2 needs it as its base.
2. Cut the integration branch from `developer`, and cherry-pick the commit that added this file and its three companions (branch `zen/marjana-r2-handoff`).
3. **Stop and check in** with three questions:
   - **G7**: confirm or change the build order below.
   - **Tracker publishing**: keep `.tasks/` only, or add opt-in GitHub publishing (specs as issues, tasks as sub-issues)? The coverage map's rule 12 explains why it is open. This is a one-way door.
   - **Guarded load-by-name** for drafts (coverage map rule 9): adopt or not.

**Phase 1: the plan.** Write `docs/reviews/2026-11-2x-marjana-r2-plan.md` with the workstreams below, owned paths kept disjoint, and task ids reserved up front. Proposed grouping, to adjust:

| Workstream | Items | Notes |
|---|---|---|
| Rules and lenses | A8 with B1 (loosen D1), D1 (contribution bar gates promotion, drafts expire), D2 (shareability is the only filter), D4 (code-shaped sketches allowed in PRs), C3 (security axis rule), C5 (effort guidance), E4's deep-module lens, E8's smells in `review-quality.md`, C1 (opt-in self-merge of verified two-way doors, a `merge_policy` value) | **Stop and check in** with the final text for A8/B1 and C1 before landing: both change what an unattended agent may do |
| Align and plan | E4 (`grill` writes the glossary live, and the podcast's explore-before-asking, rename offer, dictated-dump opening and module-shape question), `spec-author` synthesise-only mode, `new-task` prefactor and E1 (one test-seams list per plan), a single-task flow line in `zen`, E9's declined-ideas register | |
| Orchestrate and build | E3 (memory on with a chosen path, lint, recurring-job offer, exploration child), E2 (merge-conflict rule), B1 in `orchestrate` and `reconcile-worktrees`, B2, B6, B7, B8, `tdd` in build briefs, agent-ordered batch merges, the `software-factory` brakes, E6 (`systematic-debugging` rungs and ranked hypotheses; `research` promotion after one run outside this repository), the optional `claude --bg` line in `agent-handoff` | E6 amends an approved contract: the maintainer re-approves it in the PR |
| Ship and learn | E8 (`pr-describe` smallest visual and glossary terms), B9 (review quotes the contract's guards), C3 in `house-review`, new drafts `teach` (C2), a skill-vetting skill (C4), `prototype` and a `wayfinder`-style decision map with its roadmap entry (E5), `wait-what` | Drafts follow D1 once it lands |
| Platform and gates | B3 (per-file supporting list), B4 (changelog line warning, as a ratchet), B11 (`R-003` composed-by check, `R-004` quoted-phrase audit), D3 (the opt-in destructive-git gate, reading the whole command), D5 (a stdlib release script; no tag cut), E7 (Codex `agents/openai.yaml`, verified Codex and Copilot installs), E9 (zen and catalog completeness check, install note on name clashes, issue templates) | |
| Orchestrator, directly | B13 (triage `R-101` to `R-106` from `2026-11-24-dogfood/ws-d.md`), B5 (propose the cloud environment with an install setup script; the maintainer approves it in a settings prompt) | |

**Phase 2: build, land, verify** as round 1 did: one review per workstream, one fix round, a pinned re-check, then landing. Then one independent verification, a `retro` over a sample of children, and one draft PR into `developer`.

**Phase 3: the wider goals, as plans only.** For F1 (daily improvement loop), F2 (knowledge wiki fed by channels), F3 (one shared vocabulary, the seed of the website's knowledge graph), F4 (issue-to-PR loop) and F5 (sandboxed runs): one short plan each in `docs/reviews/`, ending in the questions only the maintainer can answer. **Stop and check in** before building any of them.

**Out of scope**: the website overhaul (G9: its own session, after this round); Discord and the newsletter; anything in `zen-solutions-ops`.

## 7. Suggested skills

- `orchestrate`: the procedure for the whole run.
- `grill`: the Phase 0 questions. Try one round in plain conversation rather than a picker, since round 1 accepted every recommended option and Matt argues pickers narrow answers (coverage map rule 16).
- `new-task`: the task files.
- `agent-handoff`: every child brief.
- `house-review`, then `verifier-agent`: each landing.
- `reconcile-worktrees`: landing at the verified commit.
- `research`: any new source.
- `doc-sync`: before the PR.
- `pr-describe`, including the new visual summary: the PR body.
- `retro`: the close.

## 8. Done when

- One draft PR from the round 2 integration branch into `developer` is open.
- The full gate passes on its head: `ZEN_CHECKS_SCOPE=full python3 scripts/run-checks.py` exits 0, and CI is green on that PR.
- An independent verification report under `docs/reviews/` says `pass`.
- Every item in the decision record is either landed with its task closed, or listed in the PR body as deferred with the reason.
- Each new or changed skill has a dogfood row with real evidence.
