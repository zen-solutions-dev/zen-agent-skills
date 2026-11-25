# 2026-11-25 Marjana round 2: plan

Status: **approved in conversation** on 2026-11-25 by the maintainer (Hans Havlik), in the orchestrating session `session_017QLseoWFoRQDJMZM5nR9DQ`. Brief: [`2026-11-25-round-2-handoff.md`](2026-11-25-round-2-handoff.md). Decisions before this round: [`2026-11-25-marjana-decisions.md`](2026-11-25-marjana-decisions.md). Procedure: the `orchestrate` draft, its second real run.

Integration branch: **`zen/marjana-r2-2026-11-25`**, cut from `developer` at `ba0209f` (the merge of PR #117) with the handoff commit cherry-picked as `bfae134`. Everything lands there and reaches the maintainer as **one draft pull request into `developer`** (G8).

## Phase 0 facts, checked 2026-11-25

- PR #117 is merged: `origin/main` at `ba0209f`, "Merge pull request #117 from zen-solutions-dev/zen/marjana-2026-11-24".
- `origin/developer` is at `ba0209f` too, so G1 needed no fast-forward.
- Pushing a new branch to `origin` works from this session (B7, first probe).

## Decisions taken in this session (maintainer, 2026-11-25)

| # | Question | Decision |
|---|---|---|
| R2-1 | G7, the build order | **Two waves, as proposed**, now preceded by Wave 0 (R2-7). Wave 1: Rules and lenses, Platform and gates, and the orchestrator's own B5 and B13. Wave 2: Align and plan, Orchestrate and build, Ship and learn. Phase 3 plans last. |
| R2-2 | Tracker publishing to GitHub (coverage map rule 12), a one-way door | **Opt-in publishing, as a draft.** The local tracker stays the source of truth and mirrors one way out: specs as issues, quests as sub-issues, native blocking. A `triage` draft consumes the `role.*` labels. The shape of a published issue is the one-way part: its final shape is a check-in gate before landing. |
| R2-3 | Guarded load-by-name for drafts (coverage map rule 9) | **Adopt.** A shipped skill may say "if `<draft>` is installed, read and follow it now; otherwise continue without it". `validate-skills.py` accepts the line and draws no install edge. |
| R2-4 | How far the rename from tasks to quests goes | **Full rename**: `.tasks/` becomes `.quests/`, `new-task` becomes `new-quest`, the validator, the `zen-config` tracker value and every skill that names them. The old names stay accepted as aliases, so an adopter's repository keeps working. |
| R2-5 | The hierarchy's names | **Campaign** (was Epic), **Quest chain** (was Feature), **Quest** (was Task). A quest in no chain is a **Side quest**. |
| R2-6 | What the rarity colours mean | **Source reliability**, for research and citations: white unverified, green secondary, blue checked against the source, purple primary source cited, gold primary and independently confirmed. |
| R2-7 | When the rename happens | **First, alone**, as Wave 0 before any other child starts, so every later child writes quests. |

### Two-way decisions this session took, each with its revert

- The integration branch name `zen/marjana-r2-2026-11-25`. Revert: push the same commits under another name.
- Quest ids keep their kind prefixes and numbering (`feat-0101`, `chore-0102`): the rename moves the folder and the words, not the ids. Revert: a later sweep renames ids.
- Rarity is defined in `GLOSSARY.md` by Wave 0 and applied to `research` by Wave 2. Revert: one commit each.
- Children read and run the kit installed at project scope (`python3 scripts/install.py --include-drafts`) before work (`R-205`, until B5's environment lands).

### The maintainer's working preferences (for this orchestrator, not the kit)

- Contextual emojis in chat messages. Repository files keep the house style.
- Every question with choices or free-form input goes through the clickable picker, never a wall of text to scroll. This supersedes the handoff's section 7 suggestion of a plain-conversation round.

## Waves and workstreams

Each workstream is one child session with disjoint owned paths. Quest ids are reserved here. Every id below is written in the old `.tasks/` form until Wave 0 lands, and in the `.quests/` form after.

| Wave | Workstream | Id | Owns (summary) | Items |
|---|---|---|---|---|
| 0 | **Quest rename** | `feat-0101` | `.tasks/` (moved to `.quests/`), `new-task` (renamed `new-quest`), `init-worktracking`, `quest-tracker` and `sitrep` vocabulary, `.tasks/validate.py`, `docs/spec/zen-config*.md`, `GLOSSARY.md`, `AGENTS.md` sections 0 and 3, `docs/agents/zen.md`, every other file whose only change is the rename | R2-4, R2-5, R2-6's glossary entries. Amends the approved `zen-config` contract (A1): needs the maintainer's re-approval in the PR |
| 1 | **Rules and lenses** | `feat-0102` | `.agents/rules/`, `AGENTS.md` section 4 and 7, `CONTRIBUTING.md` | A8 with B1, D1, D2, D4, C3's rule, C5, E4's deep-module lens (`.agents/rules/deep-modules.md`), E8's smells in `review-quality.md`, C1 (`merge_policy` value), R2-3's rule text. **Check-in gate**: A8/B1 and C1 final text before landing |
| 1 | **Platform and gates** | `feat-0103` | `scripts/`, `tests/`, `.github/`, `.agents/hooks/` | B3, B4, B11 (`R-003`, `R-004`), D3, D5 (no tag cut), E7, E9's checks, install note and issue templates, R2-3's validator change |
| 1 | Orchestrator, directly | `chore-0104` | `docs/reviews/2026-11-24-dogfood/ws-d.md` triage notes only | B13 (`R-101` to `R-106`), B5 (cloud environment proposal) |
| 2 | **Align and plan** | `feat-0105` | `grill`, `spec-author`, `new-quest`, `zen`, `domain-language` | E4, `spec-author` synthesise-only mode, prefactor and E1, single-quest flow in `zen`, E9's declined-ideas register |
| 2 | **Tracker publishing** | `feat-0106` | new draft `triage`, a publishing reference under `new-quest/references/`, `docs/spec/zen-config*.md` publishing keys | R2-2. **Check-in gate**: the published issue shape before landing. Runs after `feat-0105` lands, since both touch `new-quest` |
| 2 | **Orchestrate and build** | `feat-0107` | `orchestrate`, `reconcile-worktrees`, `fix-batch`, `agent-handoff`, `systematic-debugging`, `research`, `tdd`, `verifier-agent` | E3, E2, B1 in skills, B2, B6, B7, B8, `tdd` in briefs, batch merges, `software-factory` brakes, E6 (re-approval), R2-6 in `research`, `claude --bg` line |
| 2 | **Ship and learn** | `feat-0108` | `pr-describe`, `house-review`, `retro`, new drafts `teach`, `vet-skill`, `prototype`, `wayfinder`, `wait-what` | E8, B9, C3 in `house-review`, C2, C4, E5, `wait-what`, E4's `retro` reads the writing lens |
| close | Integration | `feat-0109` | `CHANGELOG.md`, `ROADMAP.md`, `README.md`, `docs/CATALOG.md`, `.claude-plugin/` | Landing, doc-sync, verification, retro, PR |
| 3 | Plans only | `chore-0110` to `chore-0115` | `docs/reviews/` | F1 to F5, plus the **rollout campaign**: install and run the kit in each repository the maintainer keeps, the Zen product app first |

Only `feat-0109` (the orchestrator) edits `CHANGELOG.md`, `ROADMAP.md`, `README.md` and `docs/CATALOG.md`; every child passes its lines under "Notes for integration". `.claude-plugin/` is regenerated, never merged by hand.

## Rules for every child

Round 1's rules ([`2026-11-24-marjana-plan.md`](2026-11-24-marjana-plan.md), "Rules for every workstream session") hold, with these changes:

1. Branch from `zen/marjana-r2-2026-11-25`; work on `zen/marjana-r2-<workstream>`; report to session `session_017QLseoWFoRQDJMZM5nR9DQ`.
2. Before any work, install the kit at project scope with drafts (`python3 scripts/install.py --include-drafts`) and confirm the skills you need are reachable.
3. Leave your quest file where it is (B2): the orchestrator moves it at close.
4. A per-file list, never a shared count, wherever two children could both add (B3).
5. Effort: medium for building, high for verifying and debugging (C5).
6. Dogfood records go in `docs/reviews/2026-11-25-dogfood/<workstream>.md`.
