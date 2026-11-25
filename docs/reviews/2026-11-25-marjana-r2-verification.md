# 2026-11-25 Marjana round 2: independent verification

Verification of the integration branch `zen/marjana-r2-2026-11-25` against its base `ba0209f`
(`developer`), as the [round 2 handoff](2026-11-25-round-2-handoff.md) section 8 asks ("an
independent verification report under `docs/reviews/` says `pass`", and "every item in the decision
record is either landed with its task closed, or listed as deferred with the reason"). Written by
following [`verifier-agent`](../../.agents/skills/verifier-agent/SKILL.md) at high effort. The
contract is [the decisions record](2026-11-25-marjana-decisions.md) (every A to G item, and T1 to
T4) and every decision in [the round 2 plan](2026-11-25-marjana-r2-plan.md) (`R2-1` to `R2-10` and
every later dated decision, the close round's included). Report only: this file is the one change
on its branch.

Two passes. The first verified `fcb5419b12029c554f187c1445fd99963b5dadc9` and returned `fail` on one
decision with no disposition. The orchestrator answered the findings in one commit,
`12af0368fc807ac7d0a977511f5a424c3a0ae466` (three files: `ROADMAP.md`, `docs/spec/README.md`,
`docs/spec/zen-config.md`), and the second pass re-checked that commit. The verdict below is for
`12af036`; the `fcb5419` verdict and its findings are kept further down as history, and every line
number outside the decision table refers to `fcb5419`.

## Verdict

```text
verdict: pass
blocking_reasons: []
conformance:
  audited: not assessed as a matrix. No single spec is the contract; the contract is the
    decisions record and the plan. Eight approved specs and the draft zen-config carry
    round 2 amendments, each flagged for re-approval (listed below). All 13 approved specs
    read "unbound" from spec_digest.py --queue, and zen-config reads "not-approved"
    (status draft; the maintainer's A1 approval is owed as a digest, ROADMAP.md:42).
  unreconciled: []
criteria: 10 of 10 met (below)
findings: at 12af036, 3 open (all nit or information: findings 7 and 8 below, and R1 in
  the re-check); findings 1 to 6 of the fcb5419 pass are resolved
verified_by: a fresh Claude Code cloud session, session_017QLsenP2h73FgguebCoXZL, high
  effort, a leaf that dispatched nothing. It authored none of the round's work and was
  briefed by the orchestrator (session_017QLseoWFoRQDJMZM5nR9DQ), not by any child that
  wrote the work, so it is independent of every child's commits and NOT independent of
  the orchestrator's brief, nor of the orchestrator's fix commit 12af036, which it
  re-checked but did not write. The model identifier is withheld from repository files
  by this harness's rule. Commit verified:
  12af0368fc807ac7d0a977511f5a424c3a0ae466.
```

## Re-check at `12af036`

`git rev-parse origin/zen/marjana-r2-2026-11-25` printed `12af0368fc807ac7d0a977511f5a424c3a0ae466`;
`git log --oneline fcb5419..12af036` shows that one commit, and `git diff --stat fcb5419 12af036`
prints `3 files changed, 9 insertions(+), 2 deletions(-)`. Each finding of the first pass, against
the new text:

| Finding at `fcb5419` | Status at `12af036` | Evidence |
|---|---|---|
| 1, F7 has no disposition | resolved | `ROADMAP.md:43` "F7, the people the maintainer named to learn from: recorded in the decision record as the source list for later research rounds; nothing was built from it this round." |
| 2, A3 and A7 missing from the owed list | resolved | `ROADMAP.md:42` "recording, as an approval digest, the round 1 approvals the decision sheet gave on 2026-11-25 (A1 `zen-config`, A3 `verifier-agent`, A7 `cloud-executable`)" |
| 3, A1's approval recorded nowhere near the contract | resolved | `docs/spec/zen-config.md:21` "**Note 2026-11-25:** the maintainer approved this contract's round 1 text on the 2026-11-25 decision sheet (decision `A1`); the approval digest is not yet recorded"; `status` left `draft`, as rule 4 of `docs/spec/README.md` requires |
| 4, the re-approval queue table is stale | resolved by pointer | `docs/spec/README.md:86` "the table below predates the two Marjana rounds. The current queue ... is in `ROADMAP.md`, "Owed after this round"" |
| 5, `ROADMAP.md:36` says `feat-0109` is in progress | resolved | `ROADMAP.md:36` "**closed 2026-11-25**" with a link to `.quests/done/feat-0109-...md` |
| 6, G2, G3, B10 and L20 not in the owed list | resolved | `ROADMAP.md:44` (G2, G3, B10) and `:45` (the guard-sentence heading nit, "No quest reserved yet.") |
| 7, the old username in pre-existing lines | open, information | unchanged; outside the scrub's scope |
| 8, unticked acceptance boxes on closed quests | open, information | unchanged |

One new nit, **R1**: `ROADMAP.md:43` says F7 is "recorded in the decision record as the source list
for later research rounds", but the decision record itself lists the names with no stated use; the
purpose is the orchestrator's reading, not the maintainer's words. The disposition ("nothing was
built from it this round") stands either way. Also, `ROADMAP.md:42` lists specs, not each
amendment, so `docs/spec/README.md:86`'s "including every amendment of 2026-11-24 and 2026-11-25"
overstates what the ROADMAP line holds; the per-spec headers carry the amendments.

Commands re-run on a detached worktree at `12af036`:

- `ZEN_CHECKS_SCOPE=full python3 scripts/run-checks.py`, exit 0. Tail:

  ```text
  13 passed, 0 failed, 0 could not run.
  Ran on Linux, Python 3.13.18. CI runs 3 operating systems x 2 Python versions, so this is one of six cells: passing here is necessary but not sufficient.
  ```

- `python3 scripts/validate-skills.py`, exit 0: `Checked 37 skill(s): 0 error(s), 0 warning(s).`
- `python3 .quests/validate.py --strict`, exit 0: `Checked 274 quest files: 0 error(s), 0 warning(s).`
- `git log fcb5419..12af036 --format=%B | grep -ci co-authored-by`: `0`.

The fix commit touches no script, skill, test or generated file, so the install, merge and
private-data results of the first pass carry over unchanged; I did not re-run them.

## The first pass, at `fcb5419` (history)

```text
verdict: fail   (at fcb5419; superseded by the pass above)
blocking_reasons:
  - reason: a decision in the record has no disposition
    detail: F7 ("Who else to learn from", a list of names) is neither landed nor listed as
      deferred: no file outside the decisions record names it or any of its names
      (git grep for "Dan Koe", "Cal Newport", "Saraev", "who else to learn", and "F7" in
      ROADMAP.md, the plan and .quests/, at fcb5419). The handoff's done-when needs every
      item landed or listed as deferred with the reason.
conformance:
  audited: not assessed as a matrix. No single spec is the contract; the contract is the
    decisions record and the plan. Eight approved specs and the draft zen-config carry
    round 2 amendments, each flagged for re-approval (listed below). All 13 approved specs
    read "unbound" from spec_digest.py --queue, and zen-config is status draft.
  unreconciled: []
criteria: 9 of 10 met (below); the unmet one is the decision table's completeness
findings: 8 (1 blocking, 3 should-fix, 4 nit or information)
verified_by: a fresh Claude Code cloud session, session_017QLsenP2h73FgguebCoXZL, high
  effort, a leaf that dispatched nothing. It authored none of the round's work and was
  briefed by the orchestrator (session_017QLseoWFoRQDJMZM5nR9DQ), not by any child that
  wrote the work, so it is independent of every child's commits and NOT independent of
  the orchestrator's brief for this check. The model identifier is withheld from
  repository files by this harness's rule. Commit verified:
  fcb5419b12029c554f187c1445fd99963b5dadc9.
```

**What turns this into `pass`.** One line that records F7's disposition (for example in
`ROADMAP.md`'s "Owed after this round", or the plan: what the list is for, or that it is an input
with no action this round), then a re-check of that one commit. Every mechanical check below passed;
the should-fix findings do not block on their own. (Done at `12af036`; see the re-check above.)

## Base and branch (`A9`)

- `git rev-parse origin/zen/marjana-r2-2026-11-25` printed `fcb5419b12029c554f187c1445fd99963b5dadc9`:
  the branch had not moved.
- `git rev-parse origin/developer` printed `ba0209f802f0678ea6c72bdc9bdf7ec8a096d81f`, and
  `git merge-base fcb5419 origin/developer` printed the same sha: the base is current, nothing to
  rebase.
- `git log --oneline ba0209f..fcb5419 | wc -l` printed `60`; `git diff --stat` printed
  `530 files changed, 16322 insertions(+), 2003 deletions(-)`.

At `12af036`, `origin/developer` is still `ba0209f` and `12af036` is one commit on `fcb5419`.

Every first-pass check ran on a detached checkout of `fcb5419`, on Linux, Python 3.13.18, git 2.43.0: one of
CI's six cells.

## Criteria

| # | Criterion (from the brief) | Status | Evidence |
|---|---|---|---|
| 1 | Every decision landed, or deferred with a recorded reason (table below) | met at `12af036` (unmet at `fcb5419`) | 73 landed, 18 deferred, 0 missing; at `fcb5419` 1 was missing (F7) |
| 2 | `feat-0101` to `feat-0109` in `.quests/done/` with `status: done` | met | `grep -m1 "^status:"` on each of the eight files printed `status: done` (there is no `feat-0104`; `chore-0104` has no quest file and is recorded in the plan, as `feat-0109`'s Decisions say) |
| 3 | `chore-0110` to `chore-0115` open | met | each is in `.quests/` and prints `status: open` |
| 4 | The full gate passes | met | command 1 below, exit 0 |
| 5 | `validate-skills.py` passes with drafts | met | command 2 below, exit 0 |
| 6 | A fresh install places no draft and no publisher without `--include-drafts`, and places them with it | met | commands 4 to 6 below |
| 7 | No private repository name, account detail or secret in tracked files | met, with one note | command 8; finding 7 |
| 8 | No `Co-Authored-By` in `ba0209f..fcb5419` | met | command 9 prints `0` |
| 9 | Every amended approved spec carries a dated amendment flagged for re-approval | met | the list below |
| 10 | The mechanical merge `dc8089c` re-derived | met | command 10 below |

## The decision table

"Landed" names the closed quest and one piece of evidence in the tree at `fcb5419`. "Deferred" names
where the reason is recorded. Line numbers are at `fcb5419`. A1 to A7 approved contract text that
round 1 wrote; by [`docs/spec/README.md`](../spec/README.md) rule 4, recording an approval (the
`approved_digest`) is the maintainer's act and no agent's, so "landed" there means the approved text
is in the tree and the recording is owed.

### A. Contracts

| Id | Status | Quest | Evidence or where the reason is recorded |
|---|---|---|---|
| A1 | landed; recording owed | `feat-0091` | `docs/spec/zen-config.md:21` "**Note 2026-11-25:** the maintainer approved this contract's round 1 text" (`status: draft` left for the maintainer); owed in `ROADMAP.md:42` "A1 `zen-config`" (finding 3, fixed at `12af036`) |
| A2 | landed; recording owed | `feat-0093` | `docs/spec/house-review.md:48` "S-025 adds the re-check"; `house-review` in `ROADMAP.md:42` |
| A3 | landed; recording owed | `feat-0092` | `.agents/skills/verifier-agent/SKILL.md:202` "the full sha of the exact commit the verdict covers"; recording owed in `ROADMAP.md:42` "A3 `verifier-agent`" (finding 2, fixed at `12af036`) |
| A4 | landed; recording owed | `feat-0094` | `docs/spec/install.md:14` "S-014 add a profile axis"; `install` in `ROADMAP.md:42` |
| A5 | landed; recording owed | `feat-0094` | `docs/spec/validate-skills.md:574` `Scenario S-028: a workflow step with no "Done when" line warns`; in `ROADMAP.md:42` |
| A6 | landed; recording owed | `feat-0091` | `.agents/skills/spec-author/SKILL.md:35` "When the repository has `docs/agents/zen.md` and it sets `spec_dir`"; in `ROADMAP.md:42` |
| A7 | landed; recording owed | `chore-0098` | `docs/spec/cloud-executable.md:53` "`S-021` (a documentation-only change runs the documentation gates"; recording owed in `ROADMAP.md:42` "A7 `cloud-executable`" (finding 2, fixed at `12af036`) |
| A8 | landed | `feat-0102` | `.agents/rules/autonomy.md:171` "**A mechanical merge.**" |
| A9 | landed | `feat-0103` | `scripts/run-checks.py:305` `CHANGELOG_LONG_LINE_EXCEPTIONS = frozenset({` (a ratchet keyed by line digest) |

### B. Retro proposals

| Id | Status | Quest | Evidence or where the reason is recorded |
|---|---|---|---|
| B1 | landed | `feat-0102`, `feat-0107` | `.agents/skills/orchestrate/SKILL.md:201` "a **mechanical merge** exactly as `A8`'s"; first used at `dc8089c` |
| B2 | landed | `feat-0107` | `.agents/skills/orchestrate/SKILL.md:124` "leave your quest file where it is" |
| B3 | landed | `feat-0103` | `tests/fixtures/supporting-files.txt:4` "instead of colliding on one total (retro R-203" |
| B4 | landed | `feat-0103` | `scripts/run-checks.py:543` `def check_changelog_lines(`; gate "changelog lines" ran |
| B5 | landed | `chore-0104` (no file; plan section "The orchestrator's own Wave 1 items") | read-only `get_environment` of this session: environment `zen-agent-skills`, personal, limited network with exactly the four GitHub hosts the plan names, setup script `python3 scripts/install.py --include-drafts` |
| B6 | landed | `feat-0107` | `.agents/skills/orchestrate/SKILL.md:127` "after a restart of your worker, fetch" |
| B7 | landed | `feat-0107` | `.agents/skills/orchestrate/SKILL.md:72` "**Probe the remote actions the run will need**" |
| B8 | landed | `feat-0107` | `.agents/skills/orchestrate/SKILL.md:126` "acknowledge every relay in one line" |
| B9 | landed | `feat-0108` | `.agents/skills/house-review/SKILL.md:119` "**The contract's guards**" |
| B10 | deferred | none | `ROADMAP.md:44` "B10 (CI on integration branches)", "Each waits on the maintainer."; `.github/workflows` still triggers on `push` to `main` and on `pull_request` only |
| B11 | landed | `feat-0103` | `scripts/validate-skills.py:977` "Composed by A, B and C"; `scripts/check-citations.py:57` "Quoted phrase" |
| B12 | deferred | none | `ROADMAP.md:49` "B12 (`R-002`) ... not yet checked" |
| B13 | landed | `chore-0104` | the plan's B13 triage table; `chore-0116` and `chore-0117` reserved in `ROADMAP.md:46` |

### C, D. The big questions and the rules

| Id | Status | Quest | Evidence |
|---|---|---|---|
| C1 | landed | `feat-0102` | `.agents/rules/autonomy.md:207` "The first token is exactly `self-merge-sampled`" |
| C2 | landed as a draft | `feat-0108` | `.agents/skills/teach/SKILL.md`, `status: draft`, `drafted: "2026-11-25"` |
| C3 | landed | `feat-0102`, `feat-0108` | `.agents/rules/review-quality.md:229` "**Security axis** ... **Required when the change is a one-way door**" |
| C4 | landed as a draft | `feat-0108` | `.agents/skills/vet-skill/SKILL.md`, `status: draft` |
| C5 | landed | `feat-0102` | `.agents/rules/writing-for-agents.md:166` "A dispatch names its effort level ... **medium** for an agent that builds" |
| D1 | landed | `feat-0102`, `feat-0103` | `AGENTS.md` section 7 "**A draft expires.**"; `scripts/validate-skills.py:1089` `DRAFT_EXPIRY_DAYS = 90` |
| D2 | landed | `feat-0102` | `AGENTS.md` section 7 "**Shareability is the only scope filter.**" |
| D3 | landed | `feat-0103` | `.agents/hooks/destructive-git-gate.py`, in no committed wiring (`feat-0103` Decisions) |
| D4 | landed | `feat-0102`, `feat-0108` | `.agents/rules/house-style.md:25` "**A pull request summary may carry a code-shaped sketch.**" |
| D5 | landed, no tag cut | `feat-0103` | `VERSION` reads `0.1.0`; `scripts/release.py:2` "Cut a release of the kit" |

### E. Gaps from the coverage map

| Id | Status | Quest | Evidence or where the reason is recorded |
|---|---|---|---|
| E1 | landed | `feat-0105` | `.agents/skills/new-quest/SKILL.md:150` "**Agree the test seams once, for the whole plan.**" |
| E2 | landed | `feat-0107` | `.agents/skills/reconcile-worktrees/SKILL.md:128` "Confirm they are separate, non-conflicting regions" |
| E3 | landed | `feat-0107` | `docs/agents/zen.md:19` `memory: docs/agents/memory/README.md`; `.agents/skills/orchestrate/SKILL.md:78` "**exploration child**", `:258` "**Offer a recurring job**" |
| E4 | landed | `feat-0105`, `feat-0108`, `feat-0102` | `grill/SKILL.md:6` "writes each settled term to the glossary as it lands"; `retro/SKILL.md:26` reads `writing-for-agents.md`; `.agents/rules/deep-modules.md` |
| E5 | landed as drafts | `feat-0108` | `wayfinder` and `prototype`, `status: draft`; `ROADMAP.md:55` the `wayfinder` entry |
| E6 | landed; two parts deferred | `feat-0107` | `docs/spec/systematic-debugging.md:42` "`S-017` to `S-020` are new"; deferred: the second independent run (`ROADMAP.md:40`) and `research`'s promotion (`ROADMAP.md:41`) |
| E7 | landed; one part deferred | `feat-0103` | `scripts/build-adapters.py:670` "The Codex sidecar (E7, feat-0103)"; deferred: verified Codex and Copilot installs (`ROADMAP.md:48`) |
| E8 | landed | `feat-0102`, `feat-0108` | `.agents/rules/review-quality.md:203` "**Smell baseline.**"; `pr-describe/SKILL.md:76` reads the glossary |
| E9 | landed | `feat-0103`, `feat-0105`, `feat-0107` | `docs/declined-ideas.md`; gate "skill listings" ran; `docs/INSTALL.md:273` "Skill names shared with Matt Pocock's skills"; `.github/ISSUE_TEMPLATE/bug_report.yml:55` "Effort or reasoning level"; `orchestrate/SKILL.md:178` "**Re-pitch once.**"; `doc-author/scripts/wizard.py` |

### F, G. Wider goals and housekeeping

| Id | Status | Where |
|---|---|---|
| F1 to F5 | deferred (plans only, by the handoff's Phase 3) | `docs/reviews/2026-11-25-plan-f1-improvement-loop.md` to `...-plan-f5-sandboxed-runs.md`; `chore-0110` to `chore-0114` open; F1's repositories owed in `ROADMAP.md:49` |
| F6 | deferred | `ROADMAP.md:49` "F6, the maintainer's own notes on the podcast, not answered" |
| F7 | deferred | `ROADMAP.md:43` "F7, the people the maintainer named to learn from ... nothing was built from it this round" (missing at `fcb5419`, recorded at `12af036`; see the re-check) |
| G1 | landed | the plan's "Phase 0 facts": `origin/developer` already at `ba0209f`; confirmed above |
| G2 | deferred | `ROADMAP.md:44` "G2 (branch clean-up)", "Each waits on the maintainer." |
| G3 | deferred | `ROADMAP.md:44` "G3 (the brain-dump PR in the ops repository)" |
| G4 | deferred | `ROADMAP.md:49` "G4, a research refresh every two weeks, approved but not scheduled" |
| G5 | landed | `ROADMAP.md:50` "G5, archiving round 1's finished child sessions, was done" (not independently checked) |
| G6 | landed | `docs/reviews/2026-11-25-skills-coverage-map.md`, committed in `bfae134` |
| G7 | landed | `R2-1` |
| G8 | landed in the plan | the plan names one draft PR into `developer`; the PR is not open yet and was not checked |
| G9 | deferred | the handoff section 6 "Out of scope: the website overhaul (G9 ...)", and the maintainer's answer |

### T and R2. Phase 0 answers and the plan's decisions

| Id | Status | Quest | Evidence or where the reason is recorded |
|---|---|---|---|
| T1, R2-2 | landed as a draft; live apply deferred | `feat-0106` | `.agents/skills/triage/scripts/publish.py:61` the `zen-publish v1` marker; `triage` `status: draft`; live `--apply` owed in `ROADMAP.md:39` |
| T2, R2-3 | landed | `feat-0102`, `feat-0103` | `AGENTS.md` section 5 "**A draft is loaded by name, guarded.**"; `scripts/validate-skills.py:1021` `UNGUARDED_LOAD_RE`; `new-quest/SKILL.md:207` uses the guard |
| T3 | landed | `feat-0105` | `docs/declined-ideas.md:138` "Questions in plain prose instead of a structured question tool" |
| T4 | landed (direction) | `feat-0105`, `feat-0107`, `feat-0108` | the E items above; `docs/INSTALL.md:273` |
| R2-1, G7 | landed | all | commit order: `a2fab2b` (the rename) is the first build commit after the plan commits `7992df3` and `3967ee7` |
| R2-4 | landed | `feat-0101` | `.quests/validate.py:2` "Validate the .quests/ backlog, or a .tasks/ one" |
| R2-5 | landed | `feat-0101` | `GLOSSARY.md:69` "**Campaign**", `:73` "**Quest chain**" |
| R2-6 | landed | `feat-0101`, `feat-0107` | `.agents/skills/research/SKILL.md:50` the ladder, identical to `GLOSSARY.md:102` and `sitrep/SKILL.md:98` |
| R2-7 | landed | `feat-0101` | as R2-1 |
| R2-8 | deferred | none | `ROADMAP.md:47` "(decision `R2-8`), in a later round" |
| R2-9 | landed | `feat-0107` | `.agents/skills/sitrep/SKILL.md:81` "the one rarity ladder this kit uses for sources and figures alike" |
| R2-10 | landed; removal deferred | `feat-0103` | `.quests/validate.py:769` `ALIAS_REMOVAL = "the old names are aliases: v0.2.0 warns; v0.3.0 removes the old names"`; `ROADMAP.md:51` |

### Later dated decisions in the plan

| # | Decision | Status | Evidence or where the reason is recorded |
|---|---|---|---|
| L1 | The four two-way decisions (branch name, id prefixes kept, rarity in two steps, kit installed in children) | landed | branch name and ids as stated; `GLOSSARY.md:102`; the plan's child rule 2 |
| L2 | `feat-0102` check-in gate: strict mechanical merge, `base_branch` only, random sampling | landed | `autonomy.md:210` "`base_branch` to a branch name, explicitly"; `:233` "read as a hexadecimal integer, is divisible by N" |
| L3 | `VERSION` at 0.1.0 (superseding 0.2.0) | landed | `VERSION` reads `0.1.0` |
| L4 | Old-name warnings never promoted by `--strict` | landed | `feat-0103` Decisions; `python3 .quests/validate.py --strict` exits 0 on the tree |
| L5 | The 24 quoted phrases to `chore-0118` | deferred | `ROADMAP.md:46` |
| L6 | The destructive-git gate keeps its four extra rows | landed | `destructive-git-gate.py:119` "git push --prune", `:147` "git switch --discard-changes", `:172` "git prune", `:184` "git worktree remove --force" |
| L7 | `memory` kept as a file | landed | `docs/agents/zen.md:19` |
| L8 | `spec-author`'s inline fallback retired; the declined-ideas register | landed | `docs/spec/spec-author.md` second `feat-0105` amendment; `docs/declined-ideas.md` |
| L9 | Close-round fix list (a) to (n) | landed, (h) dismissed | (a) `autonomy.md:217` "names the value it read"; (b)/(j) `review-quality.md:229` now points at guard 2 instead of claiming "the same list as" (no match for that phrase); (c) `GUARD_OPEN_RE` at `validate-skills.py:1031`; (d) `CATALOG.md:119` "(Campaign B was Epic B)"; (e) `run-checks.py:292` `ROADMAP_STATUS_EXCEPTIONS = frozenset()`, `:605` `UNLISTED_DRAFT_EXCEPTIONS = {}`; (k) `vet-skill/SKILL.md:36` PowerShell form, `:45` `shasum` and `Get-FileHash`; (l) `:60` "only from the fresh clone"; (m) `AGENTS.md` section 5 "A draft loading a draft is not checked"; (n) `wizard.py:153` `r"""`. (f), (g), (i) spot-checked only |
| L10 | Rarity Gold wording | landed | `GLOSSARY.md:102` |
| L11 | Prototype branch stays local; the rollout campaign keeps the Zen product app first | landed (records) | the plan; `ROADMAP.md:55` ticket `W-01` |
| L12 | `feat-0106` check-in gate: the published issue shape | landed | `publish.py:61` marker, `:69` `zen:in-progress`, `:175` `is_private` |
| L13 | `feat-0106` amendments (a) to (d) | landed | `publish.py:59` "neutralised", `:459` "**frozen**"; `python3 -m unittest tests.test_publish` "Ran 54 tests ... OK" |
| L14 | One live `--apply` owed before adopters publish | deferred | `ROADMAP.md:39` |
| L15 | Publishing moves into the `triage` draft | landed | installs below: `publish.py` and `publishing.md` appear only under `triage/` and only with `--include-drafts` |
| L16 | Gold relabelled "Independently confirmed" | landed | `GLOSSARY.md:102`, `research/SKILL.md:50`, `sitrep/SKILL.md:98` |
| L17 | Alias expiry named: v0.2.0 warns, v0.3.0 removes | landed | `.quests/validate.py:769`; `sitrep/scripts/sitrep.py:112` |
| L18 | Scrub the account details; recommend a squash merge | landed in the tree; the squash is the maintainer's | command 8 below |
| L19 | The close round's fix child at `e6dda0f` | landed | `git merge-base --is-ancestor e6dda0f fcb5419` exits 0 |
| L20 | Guard regex heading nit owed to a later quest | deferred | `ROADMAP.md:45` "No quest reserved yet." |

Count at `12af036`: **73 landed, 18 deferred, 0 missing**, over 91 rows (at `fcb5419`: 73, 17, 1) (T1, T2 and G7 share rows with
`R2-2`, `R2-3` and `R2-1`).

## Amended approved specs flagged for re-approval

Every approved spec this range amended in behaviour carries a dated 2026-11-25 amendment and a
pending flag, and all eight are in `ROADMAP.md:42`:

| Spec | Amendment and flag |
|---|---|
| `build-adapters` | "Amended 2026-11-25 (`feat-0103`) ... **This amendment is pending the maintainer's re-approval**" |
| `house-review` | "**Amended 2026-11-25 (`feat-0108`), pending the maintainer's re-approval.**" |
| `install` | two, `feat-0101` and `feat-0103`, each "Pending the ... re-approval" |
| `sitrep` | two, `feat-0101` and `feat-0103`, "needs the maintainer's re-approval in the round 2 pull request" |
| `spec-author` | two, `feat-0105`, "pending the maintainer's re-approval" |
| `systematic-debugging` | `feat-0107`, "**pending the maintainer's re-approval**" |
| `validate-skills` | `feat-0103`, "Pending the maintainer's re-approval of this amendment." |
| `zen-config` (draft) | three, `feat-0101`, `feat-0102`, `feat-0106`, each "needs the maintainer's re-approval in the round 2 pull request" |

Six more specs changed only words and paths in the rename, each with "**Noted 2026-11-25:
rename-only edit, `feat-0101`, no behaviour change.**": `agent-observatory`, `cloud-executable`,
`doc-sync`, `test-author`, `tracker-links`, `verifier-agent`. I read each diff: only "Epic" to
"Campaign", `new-task` to `new-quest`, and `.tasks/` to `.quests/` changed.
`python3 .agents/skills/spec-author/scripts/spec_digest.py --queue docs/spec` ends "13 approved
spec(s) waiting on a person's re-approval in docs/spec", every one `unbound`.

## Commands and their tails

1. Command: `ZEN_CHECKS_SCOPE=full python3 scripts/run-checks.py`. Exit status: 0. Tail:

   ```text
   ok          changelog lines
               Measured 47 task-log line(s) in CHANGELOG.md: 0 new lines over the limit; 19 excepted, 0 stale exception(s).
   ok          skill listings
               Checked 2 of 2 listing(s) against 37 skill(s): 0 finding(s) failing.
   ok          secret scan
               Scanned 632 file(s) for 9 credential shape(s), skipped 0 binary or oversized; 0 finding(s). Fixed-prefix shapes only: a credential with no published prefix is not detected.

   13 passed, 0 failed, 0 could not run.
   Ran on Linux, Python 3.13.18. CI runs 3 operating systems x 2 Python versions, so this is one of six cells: passing here is necessary but not sufficient.
   ```

2. Command: `python3 scripts/validate-skills.py --include-drafts`. Exit status: 0. Tail:

   ```text
   Checked 37 skill(s): 0 error(s), 0 warning(s).
   Link-checked 25 supporting file(s) beside the 37 skill(s) checked; skipped 10 template(s) whose links are written for another repository and 12 non-markdown file(s). Also link-checked 7 file(s) under .agents outside the skills tree; skipped 0 template(s) and 9 non-markdown file(s).
   ```

   The script takes no arguments: `--help` prints the same two lines, so `--include-drafts` is
   ignored and every one of the 37 skills, drafts included, is checked either way.

3. Command: `python3 .quests/validate.py --strict`. Exit status: 0. Tail:
   `Checked 274 quest files: 0 error(s), 0 warning(s).`

4. Command: `python3 scripts/install.py --home <scratch>/h1 --mode copy --profile all`. Exit
   status: 0. Placed 25 skills in `.claude/skills/`. None of the 12 drafts' directories exists (a
   `find` for each name); no file named `publish*` exists anywhere under the home. Tail:
   `Run \`python scripts/install.py --check\` (with the same --home, if you passed one) to see whether an installed set still matches this kit.`

5. Command: `python3 scripts/install.py --home <scratch>/h2 --mode copy --profile all --include-drafts`.
   Exit status: 0. Placed 37 skills, every draft among them, and
   `triage/references/publishing.md` and `triage/scripts/publish.py`.

6. Command: `python3 scripts/install.py --home <scratch>/h3 --mode copy` (default `spine`). Exit
   status: 0. Placed 20 skills, no draft. `python3 scripts/install.py --dry-run` names the 12 drafts
   "excluded from every profile, including 'all'".

7. Command: `python3 -m unittest tests.test_publish`. Exit status: 0. Tail: `Ran 54 tests in
   2.578s` / `OK`.

8. Private-data greps over `git grep` at `fcb5419`: tracked paths containing the maintainer's GitHub
   username (from the commit author field): none. Contents: 12 lines in 9 files, every one present
   at `ba0209f` (one by way of the rename of `tests/test_tasks_validate.py`) (finding 7). `env_` followed by six or more id characters: none. The claude.ai
   artifact URL path: two lines, both a test or a quest asserting its absence. `C:\Users\<name>`:
   only the placeholder `C:\Users\you` in `docs/INSTALL.md:137`. A personal email address: none.
   "Answered by <name>": none ("Answered by the maintainer" only). The secret scan is command 1's
   last gate: 0 findings.

9. Command: `git log ba0209f..fcb5419 --format=%B | grep -ci "co-authored-by"`. Output: `0`.

10. The mechanical merge `dc8089c`. Parents `c51a64a` (feat-0108's fix round) and `8b784e7`
    (feat-0105's follow-up). `git merge-tree --write-tree --name-only c51a64a 8b784e7` exited 1
    with tree `2a6690ae0381dca1d3dd696886c8ac7140ab52de`, conflicted path
    `.claude-plugin/plugin/.claude-plugin/plugin.json` only, and
    `CONFLICT (content): Merge conflict in .claude-plugin/plugin/.claude-plugin/plugin.json`.
    `git diff --name-only 2a6690a dc8089c` prints that one path; the diff replaces the two conflicting
    `"version"` lines with `"version": "0.1.0+c37903ced78f"`. In a scratch worktree at `dc8089c`,
    `python3 scripts/build-adapters.py --marketplace` exited 0 and `git status --porcelain` printed
    nothing: the resolved file is exactly what the generator writes. `dc8089c` is an ancestor of
    `fcb5419`.

## Findings at `fcb5419`, ranked

1. **Blocking. F7 has no disposition.** Where: the decisions record, section F, row F7; absent
   from `ROADMAP.md`, the plan and `.quests/`. Evidence: the greps in the blocking reason. The
   answer is a list of people to learn from; nothing records what it feeds (the knowledge wiki
   plan, the research refresh G4, or nothing this round).

2. **Should-fix. Two approved contracts are missing from the re-approval owed list.**
   `ROADMAP.md:42` lists `zen-config`, `sitrep`, `install`, `validate-skills`, `build-adapters`,
   `systematic-debugging`, `spec-author` and `house-review`. A3 (`verifier-agent`,
   `docs/spec/verifier-agent.md:33` "Amended 2026-11-24 by feat-0092, **pending the maintainer's
   approval**") and A7 (`cloud-executable`, `docs/spec/cloud-executable.md:51` "**pending the
   author's re-approval**") were approved on the sheet and still wait on the recording, but no
   owed line names them, so the maintainer's re-read could skip both.

3. **Should-fix. A1's approval is recorded nowhere near the contract it approved.** The decisions
   record says A1 "Approve", but `docs/spec/zen-config.md:18` still reads "**Pending the
   maintainer's approval in the Marjana pull request.**", and `ROADMAP.md` "Current state" calls it
   "the draft `zen-config` contract" without saying the maintainer approved it. Setting `status` is
   the maintainer's (`docs/spec/README.md` rule 4), so this is a pointer to add, not a status to
   flip. Consequence: `feat-0102` and `feat-0106` declare `spec: "docs/spec/zen-config.md"`, a
   draft, so a per-quest `verifier-agent` run against either is `blocked` until it is recorded.

4. **Should-fix. The re-approval queue table in `docs/spec/README.md` is stale.** The page says
   "for the specs still `unbound`, this table is the record", and all 13 are `unbound`. Its last
   dated row is 2026-11-24 (`chore-0098`). It has no row for any round 2 amendment, nor for round
   1's `feat-0091` to `feat-0094` amendments; round 2 changed only three words in the file
   (`new-task` to `new-quest`). Partly pre-existing at `ba0209f`, widened by this round.

5. **Nit. `ROADMAP.md:36` says "Integration (`feat-0109`, in progress)"** while
   `.quests/done/feat-0109-...md` reads `status: done` and `CHANGELOG.md:71` says "Closed
   `feat-0109`". The roadmap gate did not catch it: the line names the id in backticks, not as a
   link to an open file.

6. **Nit. G2 and G3 ("Not yet") and B10 ("Later") are carried only in the decisions record and the
   plan**, not in `ROADMAP.md`'s "Owed after this round", which is where the next round will look.
   L20 (the guard-regex heading case) is owed with no reserved id.

7. **Information. The maintainer's GitHub username remains in 12 tracked lines in 9 files**, all
   present at `ba0209f`: `CHANGELOG.md`'s v0.1.0 tag link, `chore-0021`, `chore-0031`, `chore-0095`
   and `feat-0079`, two review documents, and two test fixtures (`tests/test_observatory_serve.py`,
   and `tests/test_quests_validate.py`, renamed from `tests/test_tasks_validate.py`). They name the repository's former owner, which is public
   history, and the close round's scrub scope (the plan's close entry) did not name them. No path
   contains it.

8. **Information. The closed round 2 quests leave their acceptance boxes unticked.** Each of
   `feat-0101` to `feat-0109` has 4 to 8 `- [ ]` lines, where round 1's `feat-0091` to `feat-0094`
   ticked theirs. `feat-0108`'s criterion "`Checked 36 skill(s)` ... among its 11 draft skills"
   no longer holds as written (37 and 12 since `feat-0106`'s `triage`); the plan records the
   quests as closed by the orchestrator as "own unverified work", which this report now checks as
   a whole.

## What this verification did not check (`A6`)

- **Per-quest conformance.** No `spec-conformance` matrix was re-derived; the existing
  `*.conformance.md` files were not spot-checked row by row beyond the `systematic-debugging`
  `S-020` row (close-round item (f)).
- **Behaviour of the new skills in use.** No skill was run on real work; the dogfood records under
  `docs/reviews/2026-11-25-dogfood/` were not audited, so the handoff's "each new or changed skill
  has a dogfood row with real evidence" is unverified here.
- **CI.** Only one of the six cells ran (Linux, Python 3.13). The pull request does not exist yet,
  so its CI and its body (where the handoff also allows deferrals to be listed) were not checked.
- **The landing chain.** Whether each child commit was verified by an independent agent before
  landing (`A8`'s condition, including `8b784e7` before `dc8089c`) was not traced; only the merge's
  mechanics were re-derived.
- **Close-round items (g) and (i)** were read at one line each, not reviewed; item (h) was taken as
  dismissed per the plan.
- **G5** (child sessions archived) and **G1's fast-forward** of `main` were taken from the records;
  `origin/main` was not fetched.
- **The secret scan's limits.** It detects fixed-prefix credential shapes only, as its own output
  says; the hand greps above cover the named account details, not every possible secret.
- **Code quality.** Out of scope for a verification; that is `house-review`, which the plan records
  as run once over `ba0209f..d5df285`. That review's report is not committed, so its 2 must-fix and
  11 should-fix findings' dispositions were not checked one by one.
