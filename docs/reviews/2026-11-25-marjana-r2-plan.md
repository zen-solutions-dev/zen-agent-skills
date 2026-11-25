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
| R2-8 | `quest-tracker` already says "quest" and "quest chain" for a run of steps on its page | **Fix in a later round** (show real quests on the page, or rename its term). Round 2 keeps the one clarifying sentence Wave 0 added. |
| R2-9 | `sitrep`'s white-to-gold evidence tiers against the new rarity ladder | **One ladder** for sources and figures alike. Built in Wave 2 with R2-6 in `research` (`feat-0107`), reconciling `sitrep`'s tiers. |
| R2-10 | Do the old names (`.tasks/`, `tracker: tasks`, `new-task`) ever expire? | **Warn, then remove.** The validator, `sitrep` and `install.py` warn on an old name from this round (`feat-0103`, which also owns `.quests/validate.py` for this change); the aliases are removed at the **second tagged release**, so the first release carries the warning. |

### Two-way decisions this session took, each with its revert

- The integration branch name `zen/marjana-r2-2026-11-25`. Revert: push the same commits under another name.
- Quest ids keep their kind prefixes and numbering (`feat-0101`, `chore-0102`): the rename moves the folder and the words, not the ids. Revert: a later sweep renames ids.
- Rarity is defined in `GLOSSARY.md` by Wave 0 and applied to `research` by Wave 2. Revert: one commit each.
- Children read and run the kit installed at project scope (`python3 scripts/install.py --include-drafts`) before work (`R-205`, until B5's environment lands).

### The maintainer's working preferences (for this orchestrator, not the kit)

- Contextual emojis in chat messages. Repository files keep the house style.
- Every question with choices or free-form input goes through the clickable picker, never a wall of text to scroll. This supersedes the handoff's section 7 suggestion of a plain-conversation round.

### Check-in gate on `feat-0102`, 2026-11-25

The maintainer approved the A8/B1 and C1 wording with these answers: a **mechanical** merge stays strict (no conflict, or conflicts only in regenerated generated files; ledger and plan conflicts go back to the child); self-merge targets `base_branch` only; and sampling is **random**, not by pull request number. The orchestrator implemented "random" as: a self-merged pull request is sampled when its merge commit's sha, read as a hexadecimal integer, is divisible by N (unpredictable before the merge, checkable after; default N 5, cap 20). Revert: one commit to guard 4.

### Maintainer answers on `feat-0103`'s questions, 2026-11-25

- Commit a `VERSION` file at **0.2.0**, and `build-adapters.py`'s plugin version reads it. No tag is cut (D5). **Superseded the same day**: 0.2.0 broke the release path (no `v0.2.0` section, and 0.2.0 could never be released), so the maintainer set `VERSION` to **0.1.0**, the last real tag; the next release, on his go, cuts 0.2.0.
- The old-name warnings are **never** promoted by `--strict`.
- The 24 unresolved quoted phrases `R-004` found go to a quest next round, reserved as `chore-0118`; the audit then switches to failing.
- The destructive-git gate keeps its four extra rows (`switch --discard-changes`, `push --prune`, `prune`, `worktree remove --force`).

## The orchestrator's own Wave 1 items (`chore-0104`)

**B5, done 2026-11-25.** A personal cloud environment `zen-agent-skills`, approved by the maintainer in its prompt, saved for this repository. Its setup script installs the kit with drafts (`python3 scripts/install.py --include-drafts`), run first by hand from the checkout's parent and seen to place every skill. Network: limited to `github.com`, `raw.githubusercontent.com`, `codeload.github.com`, `api.github.com`, package registries and MCP servers. The Default environment is unchanged. Wave 2 children start on it.

**B13, triaged 2026-11-25.** WS-D's `retro` run of 2026-11-24 was report-only, and its proposals survive only as the summary in [`2026-11-24-dogfood/ws-d.md`](2026-11-24-dogfood/ws-d.md); no branch holds their full text (`git grep` over every remote ref, 2026-11-25).

| Id | What survives | Triage |
|---|---|---|
| `R-101` | CI on the integration prefix | **Dismissed.** Its premise was wrong (`ws-d.md` says so), and B10 put CI on integration branches at Later. |
| `R-102` | The plan's skill limits as `validate-skills.py` errors, a ratchet | **Accepted**, not built this round: reserved as `chore-0116`. |
| `R-103` | A closed quest with no changelog line, a ratchet | **Accepted**, not built this round: reserved as `chore-0117`, with `R-105`. |
| `R-104` | Nothing beyond its id | **Lost.** Not reconstructed. |
| `R-105` | A `parent` that resolves nowhere, a ratchet | **Accepted**, with `R-103` in `chore-0117`. |
| `R-106` | Nothing beyond its id | **Lost.** Not reconstructed. |

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

## Wave 2 record and the close-round list

Decisions, landings and the findings held for the close round's single fix child, written during Wave 2 and committed after it landed (lesson (a): no orchestrator commits while children run).

- 2026-11-25, on feat-0107: the maintainer kept `memory` as a file (the index `docs/agents/memory/README.md`), so the zen-config format is unchanged. The systematic-debugging amendment (S-017 to S-020, the S-016 exception) is for re-approval in the final PR.
- 2026-11-25, on feat-0105: the maintainer retired spec-author's "inline fallback when grill is not installed" constraint (install.py always places grill with spec-author); the register `docs/declined-ideas.md` keeps upstream positions the kit declined, such as "questions in plain prose". The spec-author amendment is for re-approval in the final PR.
- TODO feat-0105 fix round: retire spec-author Constraint 'inline fallback when grill is not installed' (spec + conformance row), per maintainer.
- Close-round fix list (feat-0109's one fix child): (a) A8 in autonomy.md lacks zen-config S-045's "names the value it read ... in its report"; (b) review-quality.md security-axis list says "the same list as" A8 guard 2 but omits approved spec, acceptance checks, mode: hitl; (c) validate-skills GUARD_OPEN_RE forbids a newline before "; otherwise", so a wrapped guard warns (retro R-301) — allow wrapping; (d) docs/CATALOG.md:36 "(Epic B)"; (e) remove ROADMAP_STATUS_EXCEPTIONS/UNLISTED_DRAFT_EXCEPTIONS bridges once ROADMAP/zen/CATALOG list the drafts.
- Rarity Gold, orchestrator decision 2026-11-25: "a blue or purple claim that an independent check agrees with: a second primary source, a run, a measurement, or a test that pins it" (keeps sitrep's script unchanged).
- 2026-11-25, on feat-0108: the prototype dogfood branch `prototype/self-merge-sampling` stays local (the record names its commit); the rollout campaign keeps the Zen product app first and the rest waits on the maintainer (wayfinder W-01). The house-review amendment (S-026, S-027) is for re-approval in the final PR. ROADMAP_STATUS_EXCEPTIONS from feat-0108 are a bridge the integration owner removes at close.
- 2026-11-25, check-in gate on feat-0106 (R2-2, one-way door): the maintainer approved the published-issue shape as proposed (titles `Spec: <title>` and `<id>: <title>`; body with source line, metadata table, verbatim text, absolute links, hidden `<!-- zen-publish v1 kind= id= source= digest= -->` marker; sub-issues under the spec issue; native blocked-by; done closes, spec closes when all its quests close; `publish: github|none` and `publish_repo: owner/name`; `private: true` never published), with every recommended answer: never touch role.* labels; no issues for done quests never published; specless quest is a top-level issue; an issue closed on GitHub while its quest is open is reopened; fixed label names zen:published, zen:spec, zen:quest, zen:in-progress.
- Close-round nits from feat-0107's re-check: (f) systematic-debugging conformance row S-020 claims the baseline is asserted, it is not (narrow the row or add an assertion); (g) memory entry 2026-11-25-shared-terms-verbatim.md quotes a paraphrase of AGENTS.md §7 (quote it verbatim); (h) GLOSSARY ladder entries lost the per-term `_Avoid_:` format (decide); (i) hitl_loop.py docstring stray wrap.
- Quest closes: feat-0101, 0102, 0103, 0107 moved to .quests/done/ at 03e4862 (own unverified work; list in PR).
- Landings: feat-0108 by fast-forward to c51a64a; feat-0105's follow-up 8b784e7 by MECHANICAL MERGE dc8089c onto c51a64a (first real use of A8's B1 rule): `git merge-tree` conflicted only in `.claude-plugin/plugin/.claude-plugin/plugin.json`, rebuilt with `build-adapters.py --marketplace`; merge commit differs from the merge-tree tree only in that path; `ZEN_CHECKS_SCOPE=full python3 scripts/run-checks.py` on dc8089c: "13 passed, 0 failed, 0 could not run." List in the PR body. Quests feat-0105, feat-0108 closed at f579655 (own unverified work).
- Close-round nits from feat-0108's re-check: (j) review-quality.md security-axis list claims "the same list as" A8 guard 2 but omits approved spec, acceptance command, mode: hitl, tag/release (same as (b)); (k) vet-skill POSIX-only `GIT_LFS_SKIP_SMUDGE=1 git clone` (give the PowerShell form) and `sha256sum` absent on macOS/Windows (point at the -I alternative); (l) vet-skill: read history only from the fresh clone; (m) the guarded-load rule covers only shipped skills, so a draft's unguarded load is never flagged (decide); (n) wizard.py docstring should be a raw string; spec-author/SKILL.md line 117 wrap.
- 2026-11-25, feat-0106 amendments to the approved issue shape, decided by the maintainer after the first re-check: (a) marker-shaped lines in file text are neutralised, the one exception to "nothing else is rewritten"; (b) truncation falls back from a heading (if it keeps half the limit) to a paragraph break to a hard cut, never inside a fence; (c) a quest the repo's validate.py rejects is not published and its issue frozen, shown in the dry run; (d) a quest that drops its spec moves to top-level even when the old spec issue is frozen. Second re-dispatch of feat-0106 (the cap).
- 2026-11-25, feat-0106: one live `--apply` on a throwaway repository is OWED, run by the maintainer, before any adopter turns publishing on; publishing and `triage` stay drafts until then. `publish_repo` stays required.

## Close round: the whole-branch review and the maintainer's answers (2026-11-25)

One fresh reviewer read `ba0209f..d5df285` with `house-review` (both axes plus the security axis): 2 must-fix, 11 should-fix, 5 nits, no blocking security issue. The maintainer answered the four that were theirs:

- **Publishing moves into a draft**: `publish.py` and `publishing.md` move from `new-quest` into the `triage` draft, and `new-quest` loads it in the guarded form. It reaches adopters only with `--include-drafts` until the maintainer's live `--apply` passes.
- **Gold is relabelled** "Independently confirmed", keeping the wider meaning (a blue or purple claim an independent check agrees with); `sitrep`'s script is unchanged. This ratifies the orchestrator's earlier widening.
- **Alias expiry is named**: `v0.2.0` warns, `v0.3.0` removes the old names (`.tasks/`, `tracker: tasks`, `new-task`).
- **Scrub the remaining account details**: this round's private artifact link and environment id, and the older `C:\Users\<name>` paths and "Answered by <name>" lines. The PR body recommends a **squash merge**, so the branch's commits, which still hold scrubbed names, never reach `developer`'s history; the merge is the maintainer's.
- 2026-11-25, close: the close round's fix child landed at `e6dda0f` after its focused re-check passed (one blocker introduced by fix (c), the guard regex crossing paragraphs, fixed and re-checked). Item (h) dismissed by the orchestrator: one "To avoid" line keeps the three ladder copies identical. Owed, not built: the guard regex still lets an ATX heading directly under a guard line (no blank line) borrow a later "; otherwise"; the kit's own Markdown separates headings with blank lines, so this is a nit for a later quest. Published issues keep "by the Zen kit's `new-quest`" in their first line: it is part of the approved shape. Dated records keep the maintainer's name as approver and session ids as provenance (A7), by design.
