# Dogfood: `doc-sync` over the reader documents at round 2's close (`feat-0109`)

Run 2026-11-25 by the integration child of Marjana round 2 (branch `zen/marjana-r2-ledgers`, from
`zen/marjana-r2-2026-11-25` at `7dbad71`), following
[`doc-sync`](../../../.agents/skills/doc-sync/SKILL.md) as written. The brief named the scope and
approved applying or dismissing each finding, so the run applied findings within the documents
[`feat-0109`](../../../.quests/done/feat-0109-integrate-the-round-2-ledgers-and-listings.md) owns.

## Scope and classification

- **Documentation scope**, from the brief: `README.md`, `docs/CATALOG.md`, `docs/GETTING-STARTED.md`,
  `docs/INSTALL.md`, `docs/ARCHITECTURE.md`, and `ROADMAP.md`'s "Current state". Six documents, read
  in full except `ROADMAP.md`, of which only "Current state" and the new round 2 section were read.
- **Change scope**: round 2, `ba0209f..7dbad71`, plus this quest's own edits.
- **Classification**: all six current-state. `CHANGELOG.md` is a ledger and was skipped (this quest
  wrote its new lines from the quest files, not from an audit). `AGENTS.md`, the rules and the specs
  are contracts and were outside the scope.
- **Not audited**: the rest of `ROADMAP.md` (the Forward plan's Campaigns), which the brief did not
  name; every other Markdown document in the repository.

The run went after the round's renames and additions: grep for `task`, `.tasks`, `new-task`,
`Epic`, counts of skills, lenses and hooks, adapter targets, and the names of the new drafts, hooks
and lens; then each hit was read against the tree.

## Findings and dispositions

| Id | Document | Claim | Evidence | Confidence | Disposition |
|---|---|---|---|---|---|
| D-001 | `docs/ARCHITECTURE.md` | The rules directory holds four named lenses | `.agents/rules/deep-modules.md` exists (`feat-0102`) | grounded | **Applied**: `deep-modules.md` added to the list |
| D-002 | `docs/ARCHITECTURE.md` | `build-adapters.py` generates Cursor and VS Code adapters, plus a plugin target | `build-adapters.py --help` lists `cursor,vscode,plugin,codex` (`feat-0103`, E7) | grounded | **Applied**: a paragraph on the `codex` target, pointing at `INSTALL.md` |
| D-003 | `docs/ARCHITECTURE.md` | Work tracking stays local; the issue link is one-directional | `new-quest` step 8 and `references/publishing.md` publish quests to GitHub issues one way, opt-in (`feat-0106`) | suspected (still true read narrowly, but silent on publishing) | **Applied**: one sentence naming the opt-in publishing step and its direction |
| D-004 | `README.md` | "Cursor and VS Code or Copilot use project-level adapters" | `docs/INSTALL.md` has a Codex section and a `--target codex` row | suspected (true, incomplete) | **Applied**: Codex added |
| D-005 | `README.md` | "The four swappable lenses" in the layout table | five lens files beside `core.md` in `.agents/rules/` | grounded (counted) | **Applied**: five, with `deep-modules.md` described |
| D-006 | `README.md` | `build-adapters.py` makes "Cursor and VS Code adapters" | as D-002 | grounded | **Applied**: Codex added |
| D-007 | `docs/INSTALL.md` | The opening lists adapters "for Cursor and VS Code" | `docs/INSTALL.md` itself has a "Codex" section (self-contradiction) | grounded | **Applied**: Codex added |
| D-008 | `docs/CATALOG.md` | The hooks table lists every hook | `.agents/hooks/destructive-git-gate.py` exists and is in the hooks README's table, not the catalog's | grounded | **Applied**: a row for the gate |
| D-009 | `ROADMAP.md` (round 1 section) | Retro proposals `R-003` and `R-004` "stay owed" | `feat-0103` built both (B11) | suspected | **Dismissed** for the round 1 section, a dated record of what was true on 2026-11-24; **applied** instead as a note in the round 2 section's `feat-0103` line that they landed |
| D-010 | `README.md` | "Three report-only lenses are composed by the skills" (`spec-quality`, `test-quality`, `review-quality`) | `deep-modules.md` is composed too | suspected | **Dismissed**: `deep-modules.md` is a vocabulary that returns no verdict, so it is not a report-only lens in the sense the sentence means |
| D-011 | `docs/GETTING-STARTED.md` | "a small task", "turn the decisions into a task" (lines 223, 384, 453 and others) | the tracker's unit is now a quest (`feat-0101`) | suspected | **Dismissed**: the guide speaks to non-developers in plain English, where "task" is the ordinary word; it names no tracker path or skill by the old name |

Fixed by this quest's own edits before the audit, so not findings: the catalog's "(Epic B)" heading
(close-round item (d)), `README.md`'s "task file" wording, `ROADMAP.md`'s "Current state" counts,
and the six drafts missing from the catalog and `zen`.

**Verdict**: `drift_found`, eleven findings, nine applied in whole or part, three dismissed with
reasons. After the edits, `python3 .quests/validate.py --links README.md docs/ARCHITECTURE.md
docs/CATALOG.md docs/INSTALL.md ROADMAP.md` printed `checked 5 documents, 0 broken link(s)`.

## What the run showed about the skill

- Grepping for the round's new names (a new hook, a new lens, a new target) found more than
  grepping for the old ones did: seven of the eight fully applied findings were additions nobody had
  listed, not stale words.
- Step 1's rule that a dated record is a ledger decided D-009 cleanly: the round 1 section is a
  record, so the correction went where the present-tense claim lives.
- Not exercised: the contract branch (no contract was in scope) and a `not_audited` produced by a
  budget running out.
