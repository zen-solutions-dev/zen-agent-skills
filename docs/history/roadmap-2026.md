# Roadmap archive: 2026

The finished parts of [`ROADMAP.md`](../../ROADMAP.md), moved here unchanged on 2026-11-24 by [`chore-0100`](../../.tasks/done/chore-0100-marjana-context-and-ledgers.md) except that every relative link is re-anchored for this directory and every in-page link points back at `ROADMAP.md`. Task `parent:` fields cite these headings by name, so each heading is kept exactly as it was. The [index](README.md) lists every archive.

## The 2026-11 overhaul

Planned and approved on 2026-11-23 in [the overhaul plan](../reviews/2026-11-overhaul-plan.md), which compares the kit with Matt Pocock's skills: rigorous at the back of the pipeline, thin at the front, no learning loop, and heavy to carry. Integration branch `zen/overhaul-2026-11`.

- **Groundwork** ([`chore-0095`](../../.tasks/done/chore-0095-groundwork-for-the-2026-11-overhaul.md)), **shipped 2026-11-23**: the plan, the [`writing-for-agents.md`](../../.agents/rules/writing-for-agents.md) lens, the `metadata.invocation: user` convention, and repository URLs moved to `zen-solutions-dev`.
- **WS1 Align** ([`feat-0076`](../../.tasks/done/feat-0076-align-before-planning-with-grill-and-domain-language.md)), **shipped 2026-11-23**: draft `grill` and `domain-language`; `spec-author` interviews before it drafts; `new-task` sizes tasks to one fresh context, slices vertically, and sequences wide refactors as expand, migrate, contract.
- **WS2 Build** ([`feat-0077`](../../.tasks/done/feat-0077-build-discipline-with-tdd-and-fresh-context-dispatch.md)), **shipped 2026-11-23**: draft `tdd`; `test-quality` reshaped as a proper lens; fresh-context, leaf and effort guidance in `fix-batch`; a red command before any hypothesis in `systematic-debugging`; the phase-boundary decision in `agent-handoff`.
- **WS3 Ship and learn** ([`feat-0078`](../../.tasks/done/feat-0078-close-the-loop-with-retro-two-axis-review-and-merge-danger.md)), **shipped 2026-11-23**: draft `retro` and `improve-architecture`; `house-review` on two axes with `review-depth`'s depth rule folded in; merge danger in `pr-describe`.
- **WS4 Platform** ([`feat-0079`](../../.tasks/done/feat-0079-distribution-that-updates-itself-and-installs-what-you-ask.md)), **shipped 2026-11-23**: the two installer hazards, `--include-drafts`, a single skill with its closure (`--skills`), `invocation: user` rendered as `disable-model-invocation` on the Claude Code paths, and a committed, self-updating Claude Code marketplace under `.claude-plugin/`. The default profile's description budget fell from 10,209 characters to 6,438.
- **Integration** ([`feat-0080`](../../.tasks/done/feat-0080-integrate-the-overhaul-with-a-router-docs-and-verification.md)), **shipped 2026-11-23**: the draft `zen` router, the reader documents, deleting `review-depth`, recomputing the install profiles, and independent verification. After the recomputation the default profile's budget is 6,827 characters (measured 2026-11-23 by `install.py --dry-run`), not WS4's 6,438.

### Drafts the overhaul added, and what promotes each

Every one of these is a draft because nobody has used it on real work yet. Promotion needs exactly that: one real use, refined from what it exposed, recorded in the task that promotes it. Writing more prose about a draft does not move it.

| Draft | Promoted when |
|---|---|
| `grill` | it has interviewed a person ahead of a real spec or task |
| `domain-language` | it has kept a real glossary through a grilling session |
| `tdd` | it has built a real change red to green |
| `retro` | it has run on a real session or pull request and an approved proposal has landed |
| `improve-architecture` | it has produced a report a person acted on |
| `zen` | it has routed a person to the right skill on real work |

`systematic-debugging` was already a draft and now also carries the red-command gate; its promotion is [`feat-0063`](../../.tasks/feat-0063-a-second-independent-run-of-systematic-debugging-before-it-ships.md).

### Links to convert on promotion

A shipped skill names a draft in backticks, because a relative link is an install edge and the installer refuses a shipped skill that depends on a draft. Each of these becomes a link when its target is promoted:

- `spec-author` to `grill`: delete the marked fallback paragraph in `spec-author`, link `grill`, and re-derive rows `S-008` and `S-009` of [`spec-author.conformance.md`](../spec/spec-author.conformance.md).
- `test-author` and `fix-batch` to `tdd`.
- `house-review` to `retro`, and `retro` to `house-review`, if the composition should become an install edge.
- `spec-author` and `grill` to `domain-language`, where the glossary step should become an install edge.

### Carried forward from the overhaul

- `review-quality.md` folds in only the in-scope parts of the upstream `moonray/repoprompt-workflows` drift: the revalidation gate for `fixed`, futility classification, and frozen-baseline re-anchoring are not reconciled.
- `review-depth`'s known path-scope measurement mismatch, recorded below under the 2026-08-18 pass, now lives in `house-review`'s rationale reference, since `house-review` owns the depth rule.

### Release readiness (2026-11-23)

Before pull request 109 carries the overhaul to `main`, the release-quality chores under Epic A were drained where the fix was documentary: [`chore-0033`](../../.tasks/done/chore-0033-amend-install-spec-for-check-and-with-hooks.md) (the install contract catches up with `--check` and `--with-hooks`), [`chore-0085`](../../.tasks/done/chore-0085-six-provenance-footers-instruct-an-agent-to-run-the-fetcher.md) (provenance footers address a person), [`chore-0090`](../../.tasks/done/chore-0090-copilot-autofix-commits-carry-the-trailer-agents-md-forbids.md) (the trailer rule binds automated tooling), [`chore-0091`](../../.tasks/done/chore-0091-the-tasks-readme-frontmatter-table-omits-the-title-row.md), and [`chore-0092`](../../.tasks/done/chore-0092-the-description-budget-figures-are-stale-and-name-the-wrong-collision-cluster.md). Left open with a note on what remains: [`chore-0073`](../../.tasks/chore-0073-four-bookkeeping-corrections-the-wave-16-agents-reported-and-left.md) (a test retag and two matrix rows) and [`chore-0075`](../../.tasks/chore-0075-the-spec-readme-carries-derived-arithmetic-that-nothing-recomputes.md) (a new checker). Still to record here once they merge: the sibling test-isolation fix and the draft-promotion reports.

---

## Epic A: broadly shareable (the public kit): shipped items

Each item verbatim, in its original number, as it stood in `ROADMAP.md` on 2026-11-24.

1. ~~**`project-bootstrap`.** The umbrella front door: language-aware scaffold (gitignore, editorconfig, linter/formatter, license, README stub) that then calls `init-worktracking`.~~ **Shipped** (`feat-0001` draft, `feat-0002` house code-style layer; blessed 2026-07-24).

2. ~~**`pr-describe`.** Draft a PR body and changelog entry from a branch's diff, in the target repo's own changelog format (draft-only, never touches GitHub).~~ **Shipped** (`feat-0003` draft, `feat-0004` working-tree fallback from field iteration; blessed 2026-07-24).

3. ~~**`house-review`.** House-style review with an explicit rubric and severities, composing the swappable [`review-quality`](../../.agents/rules/review-quality.md) lens (moonray's quality-lens pattern).~~ **Shipped** (`feat-0007`; blessed 2026-07-24 after dogfooding).

6. ~~**Fold in `doc-author` / `doc-revise`** from `zen-solutions-studio`.~~ **Shipped** (`feat-0011`, `feat-0012`; dogfooded on the in-kit architecture guide and documentation consistency pass, then blessed 2026-07-24 after user sign-off).

7. ~~**Fold in `agent-handoff` / `human-handoff`** (already portable by design).~~ **Shipped** (`feat-0009`, `feat-0010`; dogfooded with the fold-in brief and in-kit partner status update, then blessed 2026-07-24 after user sign-off).

9. ~~**`tracker-links`: GitHub issue linking.**~~ **Shipped** (`feat-0030`, `feat-0031`; blessed 2026-07-28 after a real dogfood: issue #1 opened, task linked, PR #2 merged, issue closed itself. Coverage honestly recorded at two of seven scenarios in [`docs/spec/tracker-links.verification.md`](../spec/tracker-links.verification.md).) Let a task file name the upstream GitHub issue it serves, and have `pr-describe` carry that into the pull request description so merging closes it. Specified in [`docs/spec/tracker-links.md`](../spec/tracker-links.md) (`status: approved`, 9 scenarios). The value is not the plumbing but the silent-failure surface around it: GitHub ignores a closing keyword in a pull request title and in comments, ignores it entirely unless the pull request targets the default branch, and closes only the first issue when one keyword is followed by a list. Each failure produces a pull request that looks right, merges cleanly, and leaves the tracker wrong. Dogfooded on this repository's own issues.

## Epic B: contract-driven delivery (the agent-workflow spine): shipped items

Each item verbatim, in its original number, as it stood in `ROADMAP.md` on 2026-11-24.

1. ~~**`spec-quality`.** A reusable quality gate for scenario-based specifications: keep contracts observable, non-redundant, grounded in repository context, traceable through stable scenario IDs, and free of implementation planning. Report explicit blockers for ambiguity, uncovered goals or surfaces, and unresolved questions.~~ **Shipped** (`feat-0013`; folded in from `repoprompt-workflows` (Balarama Bosch, MIT), house-styled; blessed 2026-07-24 after dogfooding it on the new `docs/spec/spec-author.md` draft, where it caught five findings; user sign-off recorded).

2. ~~**`spec-author`.** Draft a persistent, executable `SPEC.md` from a raw idea before task decomposition: outcomes, anti-goals, architectural constraints, prior decisions, and mechanically testable verification criteria. It composes `spec-quality`; planning and specification work are read-only for implementation surfaces, and an explicit human approval state is required before `new-task` consumes a specification.~~ **Shipped** (`feat-0017`; authored 2026-07-24 by extracting the drafting discipline from the upstream RPCE Spec workflow into a portable skill that composes `spec-quality`; blessed 2026-07-24 after dogfooding it to draft `docs/spec/test-author.md`, where its `spec-quality` self-check caught six findings before returning a `ready` spec; user sign-off recorded).

3. ~~**`spec-plan-readiness`.** Gate implementation on an approved specification plus an ordered, repository-grounded plan. Block tests, code, and delegation until scenarios, tasks, validation, risks, rollback notes, task-to-scenario traceability, and a first safe task are all explicit.~~ **Shipped** (`feat-0014`; folded in from `repoprompt-workflows` (Balarama Bosch, MIT), house-styled and retargeted from RPCE "Deep Plan" to the kit's `.tasks/` model; blessed 2026-07-24 after gating the `spec-author` build (spec plus a two-task decomposition) to `implementable` with a scenario-to-test map; user sign-off recorded).

4. ~~**`test-quality`.** A reusable test-quality lens for choosing the lowest faithful test layer, naming the plausible defect each test protects, testing the real bug population, asserting meaningful observable outcomes, and handling fixtures, mocks, diagnostics, and trust boundaries deliberately.~~ **Shipped** (`feat-0015`; folded in from `repoprompt-workflows` (Balarama Bosch, MIT), house-styled; blessed 2026-07-24 after applying it to the untested `scripts/validate-skills.py`, producing a layer/oracle recommendation and surfacing a testability issue; user sign-off recorded).

5. ~~**`test-author`** (promoted from the former Epic B). Derive focused acceptance tests from approved specifications and task criteria, while retaining characterization-test support for legacy code with no coverage. Compose `test-quality` and run between implementation and reconciliation so test evidence is part of the core workflow.~~ **Shipped** (`feat-0018`; authored 2026-07-24 by extracting the discipline from the upstream RPCE Test workflow into a portable skill composing `test-quality` and `spec-quality`; blessed 2026-07-24 after dogfooding it to derive the `validate-skills.py` acceptance suite from `docs/spec/validate-skills.md` (11 passing tests, closing `chore-0003`), correctly omitting the accepted S-008 divergence rather than faking a pass; user sign-off recorded).

6. ~~**`spec-conformance`.** Audit every approved scenario and public-surface element against code and test evidence, producing a positive conformance matrix of `Conformed`, `Diverged`, or `Not-built` items and an explicit unreconciled set. It reports, never repairs, implementation divergence.~~ **Shipped** (`feat-0016`; folded in from `repoprompt-workflows` (Balarama Bosch, MIT), house-styled, composing into `fix-batch` verification rather than duplicating it; blessed 2026-07-24 after auditing `scripts/validate-skills.py` against `docs/spec/validate-skills.md` into a conformance matrix with one accepted divergence; user sign-off recorded).

7. ~~**`verifier-agent`.** Independently test an implementation against its approved specification and task acceptance criteria before reconciliation. It composes `spec-conformance`, produces structured pass, fail, or blocked evidence, runs the declared commands, and never edits the implementation it verifies.~~ **Shipped** (`feat-0019`; authored 2026-07-24 against `docs/spec/verifier-agent.md`, the first spec drafted by `spec-author` and explicitly approved before decomposition; blessed 2026-07-24 after dogfooding it on `scripts/validate-skills.py`, where it returned `pass` and caught a live defect neither the tests nor a fresh audit would surface: the conformance matrix's evidence citations had drifted +8 lines after the `chore-0003` refactor, with classifications still correct on stale pointers. It reported the drift rather than repairing it, and the skill was iterated from that evidence; `chore-0005` re-anchored the citations. User sign-off recorded. Completes the core spec-to-reconcile loop; the `blocked` verdict path is specified but not yet exercised on real work).

9. ~~**`doc-sync`.** Detect documentation drift caused by code changes or audit a documentation set, distinguishing current-state docs from human-owned contracts. Default to a code-grounded dry run; require explicit approval before updating current-state documentation and never silently rewrite contract documents. Keep it distinct from `doc-author` and `doc-revise`.~~ **Shipped** (`feat-0020`; authored in-kit 2026-07-25 against `docs/spec/doc-sync.md`, the second spec drafted by `spec-author` and explicitly approved before decomposition, after two open questions on approval auditability and vendored material were resolved into the contract. Dogfooded in dry-run mode across this repository's own documentation set: 38 documents audited, 29 skipped as ledger, 12 findings, nothing modified. It surfaced all three dangling references to a `document` skill that never existed here, plus five drift instances the known-answer set did not anticipate, and correctly declined to edit a contract document. The run's weakness was mechanical precision (13 heuristic hits for 1 true positive) and the skill was iterated from that evidence. Blessed 2026-07-25 after `chore-0006` exercised the apply path; user sign-off recorded. Earlier revisions of this line credited an upstream `document` workflow; no such skill was ever vendored here, and the only surviving trace of its contract is the dry-run-first instruction at `repoprompt-workflows-main/.agents/workflows/Loop.md:194`, so this skill was authored rather than folded in).

10. ~~**`review-depth`.** Select quick, standard, or deep review from deterministic signals: change size, directory spread, severe risk flags, blast radius, and documentation-only scope. Compose it with `house-review` so review effort matches risk and an explicit user choice always overrides detection.~~ **Folded into `house-review` 2026-11-23** (`feat-0078`), which now selects its own depth with the same rule. **Shipped** (`feat-0035`; authored 2026-07-31, blessed 2026-08-05 on author sign-off. Dogfooded against six in-repository changesets and one external Python repository with a real lockfile, and iterated from what those runs found: the blanket-escalation rule was replaced after four of six changesets tripped it, a prose carve-out was added to `blast_radius` after nineteen referencing files sent a four-line fix to `deep`, and the exclusion classes were proven on a 6512-line `uv.lock` and 938 lines of generated schema. Two dogfood criteria remain unticked and are accepted rather than claimed: the per-changeset depth records were not kept and cannot be reconstructed, so the evidence is recorded as conclusions in the skill body rather than as a per-run table. Using it is also what exposed the mode contradiction inside `house-review`, closed by `chore-0024`).

12. ~~**Decision log (v1, task-file only).** Have each worktree agent record its non-recoverable decisions (rejected alternatives, deliberately open seams, falsified task premises) in its own task file, and have `pr-describe` surface them. Deliberately excludes the spec-sibling rollup (`docs/spec/<name>.decisions.md`, consumed by `new-task`) until v1 proves the entries are worth reading, and carries an explicit kill criterion so the convention cannot survive by default.~~ **Shipped** ([`feat-0037`](../../.tasks/done/feat-0037-task-file-decision-log-v1.md); 2026-08-05, in a four-item parallel batch). An optional `## Decisions` section in the task template, defined once there with a four-item exclusion list, referenced in prose by `fix-batch` and `pr-describe` rather than restated, since a link from a skill body into `.tasks/` escapes the installed skill tree. The `fix-batch` item names itself the exception that proves the closeout-bookkeeping rule: `done/`, `CHANGELOG.md`, and `ROADMAP.md` are the same files for every item in a batch, while an agent's own task file is the one file exactly one agent owns. Composes with item 16's mechanical contract in the same file rather than adding a tenth field to it. Kept distinct from item 13's phase 2 (telemetry: retries, budgets, stop signals), which covers mechanical run-state rather than semantic continuity; building them together would conflate the two. Triggered by observed loss rather than by plan: two of three agents in the `feat-0025` batch found their task file's premise factually wrong about the code, and nothing in the system captured it. **Kill criterion, first data point:** the implementing agent wrote three entries into its own task file and all three are unrecoverable from the diff, the verification record, or the spec. Review again after the next batch of three or more agents before deciding whether the rollup is worth building.

15. ~~**Evidence gate and stable finding signature.** Require every review finding to carry a resolvable citation (path, line range, symbol, and an exact quote of the cited code), and drop any finding whose quote does not resolve against the file on disk. Give each finding a stable signature (severity, normalized path, summary, area id) so findings can be deduplicated across lenses and counted across runs.~~ **Shipped** ([`feat-0040`](../../.tasks/done/feat-0040-evidence-gate-and-finding-signature.md); 2026-08-05, in a four-item parallel batch). The evidence shape, the gate's five-branch disposition table, and the signature live in the `review-quality` lens; `house-review` applies them as a named step and `verifier-agent` cites code the same way. Two design points were forced by the work rather than planned: a quote found at a shifted line is **re-anchored and reported, not dropped**, since the finding is real and only the pointer moved, and a finding whose evidence is an **absence** (a missing test, an unhandled branch) has its own citable form, or the gate would have silently suppressed the whole test-coverage category. Dogfooded against `b50cc76`, a commit the implementing agent did not write: 3 candidates, 1 dropped for a quote resolving nowhere, 1 re-anchored 49 to 74, 1 absence finding kept. Building it also exposed that the `review-depth` composition was one-directional, since `house-review` had never named it back. Not speculative: `verifier-agent`'s own dogfood found a conformance matrix whose classifications were correct and whose line citations had drifted eight lines after a refactor, caught only because a human looked. `review-quality` rule 2 already asks for validation before reporting; this makes it mechanical. Taken from `repoprompt-workflows`' Deep Review governance without taking the workflow.

16. ~~**Delegate evidence contract for `fix-batch`.** Require a fixed field set from every worktree agent's report (task id, covered scenarios, files changed, tests, the validation command **and** its verbatim result, findings in the evidence shape above, recommended next step), and block acceptance when a field is missing. Reject transcript-style reports.~~ **Shipped** ([`feat-0041`](../../.tasks/done/feat-0041-delegate-evidence-contract-for-fix-batch.md); 2026-08-05, in a four-item parallel batch). Nine fields, each checkable by the orchestrator in one pass and answerable from inside a single worktree, enforced at both ends: `fix-batch` quotes the list into every dispatched prompt and gates Step 6 on it, and `reconcile-worktrees` refuses to land a worktree whose report does not meet it. The dogfood was unusually direct, since the batch that implemented this task was dispatched by the pre-contract `fix-batch` with a hand-rolled report shape: seven of that draft's nine fields survived verbatim, it had **missed** "tests added, changed, or run" and "blockers and assumptions" (both places where an agent's silence is indistinguishable from a clean result), and its `decisions` field was correctly refused as belonging to item 12's decision log rather than to the mechanical contract. The value is not the ceremony: "the validation command and its result" cannot be answered in prose without either running it or lying. Kept distinct from the decision log in item 12, which carries semantic continuity while this carries mechanical evidence. Taken from `repoprompt-workflows`' Loop workflow, without its ledger and budget machinery, which assumes a persistent orchestrator this kit does not have.

18. ~~**Provenance convention for folded-in material.** Record source URL, license, author, retrieval date, and a SHA256 digest of the retrieved content for anything adapted from an external source, and add an on-demand check that re-fetches and reports drift.~~ **Shipped** ([`feat-0043`](../../.tasks/done/feat-0043-vendored-sync-provenance-convention.md); 2026-08-06, in a four-item parallel batch). Attribution here decayed into folklore in under two weeks: the `doc-sync` line in this file once credited an upstream `document` workflow that was never vendored, and the gitignored fold-in source it cited is now gone from the tree entirely. The convention lives in the conventions section of `AGENTS.md` and [`check-provenance.py`](../../scripts/check-provenance.py) reports drift on demand, exiting 0, 1, or 2 for match, drift, and unreachable. Upstream's automatic in-place sync was deliberately **not** copied, since every fold-in here was house-styled and retargeted and an overwrite would destroy the adaptation. **The task expected some sources to be unlocatable and none were**: all seven backfill targets carry a real digest from a live 2026-08-06 fetch, 8 records across 7 files, each recording in its own note that the digest pins upstream as of the retrieval date rather than the exact bytes adapted, since the snapshot they were adapted from is gone. Verification re-fetched all eight independently and confirmed three attributions by content rather than by matching path names.

21. ~~**Approval bound to the text approved.** A spec's `status: approved` said a person agreed to a contract and never said which text, so an approved spec edited afterwards still read as approved and anything verified or decomposed against it inherited an approval nobody gave.~~ **Shipped 2026-11-23** ([`feat-0083`](../../.tasks/done/feat-0083-bind-a-spec-approval-to-the-text-approved.md)), on the maintainer's two decisions: a spec whose text no longer matches its `approved_digest` **blocks** `verifier-agent`, `new-task`, `spec-plan-readiness`, and `test-author` until re-approved, and the specs approved before this stay `unbound` until the maintainer re-reads each, rather than being bound wholesale to text with unread amendments. `spec-author` ships the read-only `scripts/spec_digest.py`, whose `--queue` makes the re-approval queue machine-readable for the first time. Suggested by the 2026-10-28 read of everything-claude-code's `operator-approval-loop`, which binds an approval to a draft's hash.

## Kit hardening (from the 2026-07-25 review pass)

A read of all 19 shipped skills on 2026-07-25, the first deliberate pass rather than a per-skill dogfood. It found four systemic issues and two gaps that need a decision before they can be decomposed. Filed rather than fixed, so each item can be dispatched to an isolated agent.

**All eight landed 2026-07-25**, the same day the pass that found them ran. Wave 1 was parallel-safe (disjoint `touched_files`); wave 2 waited on `bug-0002`, which touches the same files. The table stays as the record of what the pass found and how it was sequenced. (Corrected 2026-08-27, `chore-0066`; it read "Ready to dispatch" for the thirty-three days after the last of them closed.)

| Task | Wave | What |
|---|---|---|
| [`bug-0002`](../../.tasks/done/bug-0002-agents-section-references-by-name.md) | 1 | **Portability defect.** Skills reference `AGENTS.md` by section *number*, but the numbering differs between this repo and the repos `init-worktracking` scaffolds. `new-task` is correct for scaffolded repos and wrong here; `spec-plan-readiness` is correct here and wrong there. `.tasks/_TEMPLATE.md` propagates the wrong pointer into every task file. Reference sections by name. |
| [`chore-0007`](../../.tasks/done/chore-0007-clear-stale-skill-status-claims.md) | 1 | Seven stale status claims, including three skills (`house-review`, `pr-describe`, `project-bootstrap`) that call themselves a draft and shipped in the same file. |
| [`feat-0021`](../../.tasks/done/feat-0021-iterate-doc-sync-detection.md) | 1 | Iterate `doc-sync` from the four drift instances this review found that its own dogfood missed. Line-scoped matching and an incomplete staleness vocabulary were the causes. |
| [`chore-0008`](../../.tasks/done/chore-0008-cross-link-doc-trio.md) | 1 | `doc-author` and `doc-revise` have no reference to `doc-sync`; the documentation trio only links one way. |
| [`chore-0009`](../../.tasks/done/chore-0009-agent-handoff-harness-neutral.md) | 1 | `agent-handoff`'s description hardcodes "Claude Code", putting harness lock-in in the kit's most visible field. |
| [`feat-0023`](../../.tasks/done/feat-0023-extend-validate-skills-lint.md) | 1 | `validate-skills.py` catches none of the above. Extend it so this class of defect fails a command instead of waiting for a human read. |
| [`feat-0022`](../../.tasks/done/feat-0022-wire-verifier-agent-into-fix-batch.md) | 2 | Wire `verifier-agent` into `fix-batch` Step 6 and `reconcile-worktrees`. Deferred by `feat-0019` until the skill had been used; it has been. |
| [`chore-0010`](../../.tasks/done/chore-0010-spec-plan-readiness-compose-test-quality.md) | 2 | `spec-plan-readiness` restates `test-quality`'s layer taxonomy inline instead of composing it. Two copies free to drift. |

Decided on 2026-07-25 and now filed:

| Task | Decision |
|---|---|
| ~~[`chore-0011`](../../.tasks/done/chore-0011-document-skill-shapes-and-house-style-pointers.md)~~ | **Done.** All 19 skills now reference the house-style module and `AGENTS.md` documents both body shapes. The task's own premise was wrong: four skills needed target-repo-aware wording, not two, and `pr-describe` would have been given a paragraph contradicting a rule in its own body. |
| ~~[`feat-0024`](../../.tasks/done/feat-0024-exercise-verifier-blocked-branch.md)~~ | **Done.** The `blocked` branch fired on a real unapproved contract and matched S-005 on every clause. Produced `docs/spec/house-review.md` (11 scenarios) and the reusable evaluation-record format at `docs/spec/house-review.verification.md`. Two findings filed as `chore-0014`. |

## Kit mechanics hardening (from the 2026-07-27 review pass)

The second kit-wide pass, and the first to go at what each skill's procedure actually *does* when
run on a real repository rather than at its structure. It found two blockers, five majors, and
eight smaller issues, none visible to either validator. All thirteen were fixed the same day; see
the 2026-07-27 `CHANGELOG.md` entry for the full account. The headline two:

- **The installer shipped the skills without the lenses they compose.** 14 of 19 skills referenced
  `.agents/rules/`, which `install.py` never carried, so `house-review` arrived with no rubric at
  all. Fixed by installing the rules module as the sibling the existing links already assumed.
- **`reconcile-worktrees` silently dropped every new file an agent created.** Its `git diff | git
  apply` mechanism could not see untracked files, and `fix-batch` requires agents to leave work
  uncommitted, so the deliverable landed nowhere and the worktree holding the only copy was then
  deleted.

The pattern behind most of them: the kit is documentation and stdlib Python with no dependency
tree, no large diffs, and no binary assets, so procedures that assume a normal software repository
had never met one. That is the standing risk in dogfooding a tool on the repository that builds it,
and it is what `feat-0025` exists to close.

| Task | What |
|---|---|
| ~~[`feat-0025`](../../.tasks/done/feat-0025-exercise-batch-loop-on-dependency-bearing-repo.md)~~ | **Done.** Ran a real three-agent batch against `gaudiya-vaishnava-knowledge-wiki` (9 tests to 47). The reconciliation fix was load-bearing: all three deliverables were new files, so all three `git diff` patches were 0 bytes and the pre-fix mechanism would have lost the entire batch while reporting success. Six findings folded back into `fix-batch`, `reconcile-worktrees`, and `new-task`. The batch-loop hardening is no longer cold. |
| ~~[`chore-0012`](../../.tasks/done/chore-0012-decide-code-review-skill-name.md)~~ | **Done.** Renamed `code-review` to `house-review`, named for the rubric it applies rather than the act of reviewing. Both Open Questions in its contract resolved and re-approved. The rename exposed and fixed a defect in `.tasks/validate.py --strict`, which was checking completed tasks' `touched_files` and so broke permanently on any rename. |
| ~~[`chore-0013`](../../.tasks/done/chore-0013-amend-validate-skills-contract.md)~~ | **Done.** Amended the `validate-skills` contract to cover the four checks the implementation had outgrown it by, and the regenerated matrix caught a live divergence in `S-014` while doing it: the check had shipped on 2026-07-25, was believed correct for two days, and only surfaced once a scenario stated the condition semantically instead of restating the implementation. Fixed the same day. |
| ~~[`feat-0026`](../../.tasks/done/feat-0026-write-build-adapters-spec.md)~~ | **Done.** Wrote and approved `docs/spec/build-adapters.md` (13 scenarios), closed the five that had no test (30 to 35 tests), and restored the softened documentation claims. The audit surfaced one unstated contract decision: an existing rules file is preserved but an edited skill template is overwritten, an asymmetry invisible to both the spec and the tests. Recommendation recorded; the call is human. |

**All three branches are now exercised on real work**, each on a genuine trigger rather than a staged
one, and each recorded in the format `feat-0024` established:

- ~~**`verifier-agent`'s `blocked` verdict**~~ (`feat-0024`), at [`house-review.verification.md`](../spec/house-review.verification.md).
- ~~**`test-author`'s characterization mode**~~ (`feat-0027`), at [`install.characterization.md`](../spec/install.characterization.md).
- ~~**`spec-plan-readiness`'s blocking paths**~~ (`feat-0028`), at [`build-adapters.readiness.md`](../spec/build-adapters.readiness.md).

Each run found something the branch itself was not being tested for: an unresolved precondition
ambiguity (`chore-0014`), two testability defects in `install.py`, and a second seam between the
spine's front and back halves (`chore-0016`, now closed). Exercising a branch on real work has so far
been more productive than the branch coverage was the point of.

Both seams between the spine's halves are now closed. `spec-plan-readiness` was folded in from
upstream against a different planning artifact, and its Step 3 requirements had never been reconciled
against the task format this kit authors: `feat-0025` added task-to-scenario traceability and
`chore-0016` added risk and rollback notes. A full re-read of that list during `chore-0016` found no
third gap, so the two were the whole of it.
- **The wider spec and test coverage question.** Even after `feat-0024`, 5 of 19 skills will have a contract and none will have behavioral tests. Whether that gap is worth closing skill by skill, or whether the targeted-branch approach is sufficient, is a judgment to make once there is evidence from the first three exercises.

## Kit coherence hardening (from the 2026-08-18 review pass)

**Landed 2026-08-18, in one worktree-isolated batch of six**: `bug-0026`, `bug-0028`, `bug-0031`,
`bug-0032`, `chore-0041` and `feat-0049`. Two findings the batch itself surfaced were filed rather
than fixed and **both closed 2026-08-19**:
[`chore-0042`](../../.tasks/done/chore-0042-renormalise-the-authors-working-tree.md), the renormalise
remainder plus the two `Path.write_text` sites that can reintroduce the drift, and
[`chore-0043`](../../.tasks/done/chore-0043-amend-build-adapters-spec-for-the-code-span-exception.md), the
contract half of `bug-0028`, since six scenarios govern `rewrite_links()` and none of them excepts a
link that is not a link. `chore-0042`'s working-tree half turned out to rest on a wrong model of the
problem: the index was already LF throughout, so `git add --renormalize .` staged nothing, and there
is no renormalise commit, which is the correct outcome rather than a missed one. (Both had read as
open until 2026-08-27, corrected by `chore-0066`.)

The batch also hit the `fix-batch` dispatch trap for the second recorded
time: all six worktrees were cut from `origin/main` rather than from the dispatch commit, and four
of the six agents diagnosed and recovered from it unprompted.

The third kit-wide pass, and the first to ask whether the twenty skill bodies still agree with each
other and with the templates they ship. Every gate was green before and after: `run-checks.py`
reported 7 passed, `validate.py --strict` reported 114 task files with no errors, and the suite was
292 tests. That is the finding as much as any single item below. **None of the ten was reachable from
the acceptance command**, because every one of them is a claim in prose that stopped being true, and
no validator read a skill body for whether it agrees with another skill body. **Two of the ten are
reachable now**, and by the fix's own choice rather than by anything that existed on the day:
`feat-0048` taught `validate-skills.py` that a self-declared lens under `.agents/rules/` must have an
inbound reference, and `bug-0029` added a drift test over the two task templates' frontmatter keys
and section headings as sets. Noted 2026-08-27 by `chore-0066`, and it sharpens the finding rather
than softening it: the gates catch a class only once somebody builds the check for it, so a green run
says nothing about the eight that are still only prose.

Two are the kit's own named failure signature, something that reports success while doing nothing:

- **The shipped task template lost the two things two skills point at it for.** `fix-batch` tells
  every dispatched agent that the admissible decision-entry kinds are "defined once, in the target
  repository's task template", and `pr-describe` says "the task template owns which entries are
  admissible" and reads an `external` field to build GitHub closing references. Neither the
  `## Decisions` section nor the `external` field exists in `_TEMPLATE.md.tmpl`, so in every
  repository this kit scaffolds, one instruction is a dangling pointer and one feature can never
  fire. Scoped as [`bug-0029`](../../.tasks/done/bug-0029-shipped-task-template-lost-decisions-and-external.md)
  and **shipped 2026-08-19**: both are now in the shipped template, and the durable half is a drift
  test over the two templates' frontmatter keys and section headings as sets, verified failing
  against the pre-change template. The acceptance criterion as authored asked for that test over the
  *required* keys and `external` is optional, so the test as specified could never have caught the
  defect it was written for; the agent widened it to the full declared key set and recorded the
  rejection rather than satisfying the wording.
  This settles the question [`bug-0026`](../../.tasks/done/bug-0026-scaffolded-validator-lost-the-external-check.md)
  deliberately deferred as "a separate and arguable question": it is not a question of whether to
  teach an adopter the field, because two shipped skills already treat the template as the authority.
- **`doc-sync`'s prescribed link check cannot see the documents `doc-sync` edits.** It names
  `python .tasks/validate.py --strict`, whose default mode walks `.tasks/` only, while the documents
  `doc-sync` classifies as current-state and edits are `README.md` and `docs/*.md`. The check passes
  instantly having checked nothing. Scoped as
  [`bug-0031`](../../.tasks/done/bug-0031-doc-sync-link-check-does-not-reach-the-edited-document.md) **Shipped 2026-08-18** (`bug-0031`), and reproduced live during the same session's closeout, when a task-file rename left a `ROADMAP.md` link dead and `--strict` passed anyway..

The rest:

- **`autonomy.md` is a declared lens with zero inbound references.** It opens by naming itself the
  third module beside `house-style.md` and `review-quality.md`, and links outward into five skills;
  none of the twenty links back. Compare 20 of 20 composing `house-style.md`. The consolidation runs
  in one direction only, so an agent following a skill body never reaches the ceiling, and a lens no
  skill composes cannot be exercised, which means it cannot clear the contribution bar. This is the
  gating item under Epic E #3. Scoped as
  [`feat-0048`](../../.tasks/done/feat-0048-wire-the-autonomy-lens-into-the-skills.md) and **shipped
  2026-08-19**: the lens was then referenced from exactly the five skills whose rules it holds
  (`doc-sync`, `fix-batch`, `pr-describe`, `spec-conformance`, `verifier-agent`), each naming the
  specific rule it takes, and that set matched the lens's own outbound link list. **Superseded
  2026-08-29 by [`feat-0064`](../../.tasks/done/feat-0064-make-a10-reach-the-skills-that-read-outside-content.md),
  which took it to all twenty-two.** Five was a tight rule for a lens whose rules were about how an
  agent behaves unattended, and the wrong rule once `A10` was added on 2026-08-27, since that one is
  about material an agent reads and every skill reads something. The lens now declares
  `**Scope: universal.**` and a second validator rule enforces it, so the wiring list is derived from
  the lens rather than pinned to a set a later rule outgrew. The durable half is
  a new `validate-skills.py` rule, that a file under `.agents/rules/` declaring itself a lens must
  have an inbound reference; writing it found that `main()` had never opened `.agents/rules/` at all,
  which is why an unwired lens was invisible to every gate. **This closes the gate it names under
  Epic E #3, and the one Epic B #20 names in the same words.** Recorded as met, on 2026-08-27 by
  `chore-0066`, and neither hold is discharged here: that is a judgment and it is the author's.
- **The lite tier scaffolds a required field that cannot be satisfied.** Lite ships no `ROADMAP.md`,
  `_TEMPLATE.md.tmpl` seeds `parent: "ROADMAP#N feature-slug"`, `parent` is required by the shipped
  validator, and `new-task` demands a real ROADMAP parent and offers to add a Feature to a file that
  is not there. `new-task` never mentions the tier. The "Tier stripping at lite" list omits the
  template. Scoped as [`bug-0030`](../../.tasks/done/bug-0030-lite-tier-parent-field-has-no-roadmap-to-name.md)
  and **shipped 2026-08-19**: the template's `parent` comment names both forms, the tier-stripping
  list covers it, and `new-task` now detects the absence of `ROADMAP.md` and branches rather than
  offering to add a Feature to a file that is not there. The fix was cheap because the shipped
  validator checks `parent` for presence with no format rule, so free text at lite needs no validator
  change; that is written into the task's decisions as the thing to revisit if a consumer ever parses
  the field.
- **`test-author` is the one spine skill that will derive tests from an unapproved contract.** It
  names an approved spec as its input three times and gates only on well-formedness, while
  `verifier-agent` blocks on a non-`approved` status and `new-task` refuses one outright. Tests are
  the most durable form an unapproved contract can take, because they outlive the draft. Scoped as
  [`bug-0032`](../../.tasks/done/bug-0032-test-author-never-checks-the-spec-is-approved.md) **Shipped 2026-08-18** (`bug-0032`), with characterization mode explicitly exempt so the mode for code with no contract stays reachable..
- **Four prose claims that stopped being true**, bundled because each is a line or two with no design
  question behind it: `init-worktracking`'s tier justification names `fix-batch` as one of three
  skills that run `validate.py` unconditionally, and `fix-batch` has never mentioned the file; four
  skills state four different versions of the kit spine and none matches the README diagram, which is
  the only correct one, and neither `spec-author` nor `verifier-agent` appears in any of them;
  `fix-batch` points worktree agents at `test-author` without naming the characterization mode those
  agents actually need; and `spec-conformance` writes a report to disk by default while
  `verifier-agent`, which composes it, promises no file unless a destination was supplied. Scoped as
  [`chore-0040`](../../.tasks/done/chore-0040-four-coherence-corrections-across-skill-bodies.md) and
  **shipped 2026-08-20**: all four premises were re-derived rather than inherited and all four still
  held, despite `bug-0030`, `bug-0032` and `feat-0048` having landed on the same files in between.
  Two things the task file itself got wrong are the useful part: `pr-describe` carries two spine
  statements rather than one, and the README diagram the task named as the correct reference is
  itself wrong, filed and since closed as `bug-0039`.
- **Thirty tracked files are CRLF on disk against an `eol=lf` policy**, with `core.autocrlf=true` set
  at repository scope pulling the other way and a `.gitattributes` comment describing behaviour the
  next line overrides. Invisible to `git status`, because `text=auto` normalises on the way back in,
  and material because two comparators here read bytes off disk rather than through git. Scoped as
  [`chore-0041`](../../.tasks/done/chore-0041-working-tree-crlf-against-the-eol-lf-policy.md) **Shipped 2026-08-18** on its policy half (`chore-0041`). The run falsified two of the finding's own claims: `core.autocrlf=true` sits at system scope, the Git for Windows installer default, not at repository scope, so there is nothing to unset; and a fresh worktree reports `0` at `w/crlf` against this checkout's `30`, so the drift is one machine's. The renormalise remainder, re-scoped accordingly, is [`chore-0042`](../../.tasks/done/chore-0042-renormalise-the-authors-working-tree.md)..

Two findings were **not** filed, and are recorded here so a later reader does not take the silence
for an oversight:

- **`review-depth` measures a path-scope review against the wrong quantity.** For `house-review`'s
  path-scope-with-no-range mode it computes `reviewable_lines` from a diff over the scoped paths,
  which measures the change to those files rather than their length, while `house-review` then reads
  them in full. Downgraded on reproduction rather than dropped: the skill does carry an explicit
  fallback for an unmeasurable signal and does handle a path scope in its Inputs, so this is a
  measurement mismatch, not the unhandled gap it first appeared to be. Not worth a task until
  someone hits it.
- **`doc-author` (55 lines) and `doc-revise` (46) are structural outliers**: no numbered procedure, no
  Inputs section, roughly a third the size of every other skill, while `doc-sync` (301 lines)
  composes `doc-revise` "by reference for the editing half". Left to the author's judgment, because
  the useful frame for it is Anthropic's degrees-of-freedom rubric (high freedom where many
  approaches work, low freedom where the path is a narrow bridge) and applying that rubric across the
  kit is a larger decision than repairing two files.

One candidate was **dropped** on reproduction: that `review-depth` has no handling at all for
`house-review`'s first review mode. Both the fallback and the path-scope input exist.

The external benchmark that ran alongside this pass produced Epic C #5, Epic B #19 and #20, and the
design amendment to Epic E #6. Its finding about the kit's own architecture is worth recording here
rather than only in the epics: read against Prithvi Rajasekaran's harness-design write-up for
Anthropic, all four of the levers he names are already implemented here, and his closing rule, only
increase complexity when needed, is the one to hold against a kit then at twenty skills. The two
measurable divergences from Anthropic's skill authoring guidance are that progressive disclosure is
enforced (`MAX_BODY_LINES = 500`) and exercised nowhere (zero `references/` directories, 18 of 20
skills a single file, `fix-batch` at 396 lines then and 479 when re-measured on 2026-08-27), and that
descriptions then averaged 759 against
the 1024-character ceiling, so roughly 15,000 characters of metadata loaded before any skill triggered
(re-measured 2026-11-23, after the overhaul shortened them: a mean of 398 and 7,568 characters in all
over the 19 shipped skills). Both are
trades worth making knowingly rather than by accretion; neither is filed.
