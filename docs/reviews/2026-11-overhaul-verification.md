# 2026-11 overhaul: independent verification

Verified 2026-11-23, on `zen/overhaul-2026-11` at `99619f0` (the head of PR #98), against `origin/developer` at `66b16e1`. The work under verification is `chore-0095`, `feat-0076`, `feat-0077`, `feat-0078` and `feat-0079` (closed), and `feat-0080` (open).

Rule `A7`: the verifier is a cloud session that wrote none of this work. It ran the commands itself. It dispatched two leaf readers, each with a fresh context and at high effort, to read the rewritten and new skills against the checklist. Their claims that this report relies on were spot-checked by hand, and each one is cited to a file and line below. Nothing in the skills or tooling was changed. This file is the only change.

## Verdict

```text
verdict: fail
blocking_reasons:
  - reason: an acceptance criterion of feat-0080 is unmet
    detail: "The default profile's description characters are reported before and after" is reported
      nowhere: not in PR #98, not in PR #104, not in ROADMAP.md or CHANGELOG.md. The measurement is
      below (10,209 before, 6,827 after); it only has to be published.
  - reason: a shipped skill states a composition that no longer exists
    detail: test-quality's description says it is "Composed by test-author, tdd and fix-batch", but
      fix-batch no longer names test-quality anywhere (finding F1).
```

The failure is narrow. Every declared command passed. The install cycle, the marketplace and the invocation rendering behave as the tasks claim. Nothing the plan says must be kept has been lost. The verdict is `fail` rather than `pass` because the `verifier-agent` rule allows a pass only when every criterion is met, and one is not. Two small edits flip it: publish the numbers, and fix F1. The other findings are for the maintainer's review and do not block landing.

## Check 1: the acceptance command

```text
$ python3 scripts/run-checks.py ; echo EXIT=$?
ok          lint skills
ok          test suite            OK (skipped=2)
ok          backlog               Checked 237 task files: 0 error(s), 0 warning(s).
ok          adapters dry run      Generated 38 adapter file(s) for 19 skill(s)
ok          plugin tree           The committed marketplace is current: 19 skill(s)
ok          install dry run
ok          install cycle
ok          doc links             checked 62 documents, 0 broken link(s)
ok          matrix citations      779 audited + 409 unaudited = 1188 extracted, over 13 matrix file(s)
ok          roadmap bookkeeping
10 passed, 0 failed, 0 could not run.
Ran on Linux, Python 3.13.18. CI runs 3 operating systems x 2 Python versions, so this is one of six cells: passing here is necessary but not sufficient.
EXIT=0
```

The two skipped tests are Windows-only by design (`process identity is established from procStart, which is verified only on Windows`). `validate-skills.py` reports `Checked 29 skill(s): 0 error(s), 0 warning(s).`

**CI has not passed on any commit after the groundwork.** The workflow runs for `acbaae0` (`chore-0095`) concluded `success`. Every run since then, from `144991f` to `a724c81`, concluded `cancelled`, because a newer push superseded it. Run 209 for the head `99619f0` was `queued` when this was written. As a result, `49f77ac` ("two Windows-only failures in feat-0079's code and tests") has not been run on Windows by anyone.

## Check 2: the install cycle into a scratch home

All runs below used `--home <scratchpad>/home1`, never the real home.

```text
$ python3 scripts/install.py --home $H --tools claude --include-drafts      # exit 0
Placing 10 draft skill(s) because --include-drafts was given: agent-observatory, domain-language, grill, improve-architecture, quest-tracker, retro, sitrep, systematic-debugging, tdd, zen. ...
Profile 'spine' was expanded to stay closed over sibling references: 3 skill(s) added (doc-revise, spec-quality, test-quality).
copied    claude   zen  -> .../zen  (draft; rendered: user-invoked)
Done: profile 'spine', 27 of 29 skill(s) x 1 tool(s), plus the rules module.
Description budget: 10919 characters for this selection (profiles: core=1610, spine=6827, all=7568).
Of that, 1586 character(s) belong to 5 user-invoked skill(s) (fix-batch, improve-architecture, reconcile-worktrees, retro, zen) ...
$ ... --check        # exit 0
5 current, 0 diverged, 23 linked, 0 revised upstream, 0 unknown, 0 error(s).
$ ... --uninstall    # exit 0
Uninstalled 28 target(s).
```

- **Drafts.** All 10 drafts were placed, and each placement line is marked `(draft)`. The two skills left out of the 29 are `agent-handoff` and `human-handoff`, which `spine` does not include. After the uninstall, only the empty `.claude/skills` directory was left.
- **Invocation rendering.** Each of the five `invocation: user` skills (`fix-batch`, `improve-architecture`, `reconcile-worktrees`, `retro`, `zen`) is copied rather than linked. In each one, the placed `SKILL.md` has exactly one `disable-model-invocation: true` line, and its source has none. For example, the placed `zen/SKILL.md` frontmatter keeps `metadata: {status: draft, invocation: user}` and adds `disable-model-invocation: true`.
- **Single skills.**
  - `--skills grill --include-drafts` exits 0 and places only `grill` and the rules module (`Description budget: 368`).
  - `--skills new-task` exits 0 and places only `new-task` (`362`).
  - As a negative check, `--skills grill` without the flag refuses with exit 2: `'grill' is marked a draft; pass --include-drafts to place it`.
  - Each placement was then uninstalled, with exit 0.

## Check 3: the marketplace and the plugin tree

```text
$ python3 scripts/build-adapters.py --marketplace --check     # exit 0
The committed marketplace is current: 19 skill(s) in .claude-plugin/plugin/, and .claude-plugin/marketplace.json.
$ CLAUDE_CONFIG_DIR=<scratch> claude plugin validate . --strict                     # exit 0, Claude Code 2.1.330
√ Validation passed
$ CLAUDE_CONFIG_DIR=<scratch> claude plugin validate .claude-plugin/plugin --strict  # exit 0
√ Validation passed
```

`.claude-plugin/plugin/skills/` holds exactly the 19 shipped skills, with no draft among them. The plugin copies of `fix-batch` and `reconcile-worktrees` carry `disable-model-invocation`, and no other plugin copy does.

## Check 4: provenance (network)

`python3 scripts/check-provenance.py` exited 1 with the summary `33 up to date, 3 drifted, 0 unlocatable, 0 error(s).`

- **New blocks.** All 27 blocks this overhaul added are `up to date`, and every one of them points at `mattpocock/skills`. They sit in:
  - the `writing-for-agents.md` lens (2 blocks) and `review-quality.md` (1 block);
  - `agent-handoff`, `domain-language` and its two references, `grill`, `house-review`, `improve-architecture` (5 blocks), `new-task`, `pr-describe`, `retro`, `systematic-debugging` (the second block), `tdd` (3), `test-quality` (the second and third blocks) and `zen` (2).
- **Pre-existing drift.** The three drifts were already in the `origin/developer` blocks, with the same recorded digests, and the overhaul did not cause them. All three are `moonray/repoprompt-workflows`:
  - `.agents/hooks/delegation-reminder.py:41`;
  - `.agents/rules/review-quality.md:243` (`skills/review-quality/SKILL.md`);
  - `.agents/rules/review-quality.md:252` (`workflows/Deep-Review.md`).

## Check 5: each skill against the writing-for-agents checklist

The six checklist items are:

- **(a)** the description, which should lead with the trigger word and stay under about 400 characters;
- **(b)** the body, which should stay under about 250 lines, with history kept in `references/`;
- **(c)** sibling links, which should appear only where a skill composes the sibling, and never to a draft from a shipped skill;
- **(d)** one pointer line to `core.md`;
- **(e)** fresh leaf subagents;
- **(f)** a completion criterion on every step.

Every skill in both tables uses no em-dash, and its headings are in sentence case. No shipped skill relative-links a draft.

**Slimming targets.** Across all 29 skills, the median `SKILL.md` is 156 lines, against the plan's target of about 120. The base median was 191. Five skills are over 250 lines: `fix-batch` 251, `house-review` 256, `doc-sync` 257, `quest-tracker` 283 (not owned by any workstream) and `systematic-debugging` 300.

### New skills

| Skill | Lines | Description | Checklist concerns | Plan principle |
|---|---|---|---|---|
| `grill` | 147 | 368 | (a) the description restates the procedure; (f) step 4 ends "Then go back to step 3." with no stop condition, step 1's criterion is weak | Kept: the interview stops on an empty frontier (:81), facts are the agent's to find and decisions the person's (:45), and there is a recommendation per question (:61) |
| `domain-language` | 116 | 355 | (a) it leads with "Keeps", two phrasings of one trigger, and ends on a prohibition; (f) step 5 has no "Done when" | Kept: the glossary is lazy (:66-67), and the three ADR tests are all required (:76-85) |
| `tdd` | 173 | 397 | (d) :137 links `autonomy.md`, and `core.md` appears only in backticks; (f) step 7 has none; it restates test-quality's tautology and mock rules (:74-79) | Kept: seams first (:46-58), narrow interfaces (:50, :71), no tautologies (:74-76) |
| `retro` | 130 | 306 | (a) second person; (f) steps 3 and 5 have none; :22 says "It changes nothing until the person approves", but step 1 (:46) runs the repository's check command | Kept: a mechanical mistake becomes a check, and judgement becomes a standard (:72-80) |
| `improve-architecture` | 166 | 304 | (f) steps 4 and 5 have none; the `git log ... \| sort \| uniq -c` pipeline at :46 is POSIX-only | Kept: draft and user-invoked |
| `zen` | 157 | 229 | (f) step 3 has none; it says "A person starts it" for fix-batch and reconcile-worktrees, but not for retro and improve-architecture | Kept: it names all 28 other skills, with no stray name, and its draft marks match the frontmatter exactly; it hints and never fires (:6) |

### Rewritten skills, compared with `origin/developer`

| Skill | Lines (base, now) | Description | Behaviour the plan says to keep |
|---|---|---|---|
| `fix-batch` | 452, 251 | 379 | **Kept.** The nine-field report is identical: base :338-348, now :204-214. It still runs `verifier-agent` before landing, with `pass`/`fail`/`blocked` (:160-172). The A4 command plus its verbatim tail is "the load-bearing pair" (:221). The recovery preconditions (`--ff-only`, never `git reset --hard`, the staleness disclosure) stay inline at :97-107, and the incidents are in `references/incidents.md`. Fresh context, leaf and effort-by-role are new (:82-91). **Lost:** the pointer to the `test-quality` lens (base :200), which is F1. **Concern:** the verifier dispatched at :165 is not told it is a leaf. |
| `house-review` | 244, 256 | 394 | **Kept.** The evidence gate keeps all of its branches and the drop count (:164-180). There are two independent axes with no reranking (:143-154). Standards are read at review time (:134-137). The `review-depth` rule survives (five signals, R1-R7, anchors, the unmeasurable-to-`standard` fallback; :78-115). **Weakened:** the output block (:186-191) no longer emits the measured signal values that `review-depth` printed (base `review-depth/SKILL.md:287-305`). Amended S-023 does not require them, but spec Goal 10, "an inspectable reason", is served less well. |
| `pr-describe` | 193, 212 | 376 | **Kept** verbatim (:136-151): every closing-keyword rule, which covers body not title, the keyword repeated per issue, the default branch only (otherwise a bare reference and a warning), `.tasks/done/` counting, and nothing emitted when the task is uncertain. Merge danger was added: the door, the blast radius and how hard to look (:98-123). The skill grew. |
| `doc-sync` | 322, 257 | 374 | **Kept.** Dry run by default (:162, :244). The current-state, contract and ledger classes (:81-85). Unclassifiable is treated as contract (:89). Notes moved to `references/notes.md`. |
| `systematic-debugging` | 363, 300 | 362 | **Kept.** The hypothesis budget (:51-54). Three verdicts, "no fourth" (:58-64). The red command comes before any hypothesis, with "No red command, no hypothesis phase" (:124). It names `house-style.md` and `autonomy.md` only in backticks (:265-267), where the base linked `autonomy.md`. |
| `agent-handoff` | 91, 156 | 378 | **Added.** The phase-boundary tree: continue, clear, hand off, subagent, compact, where the first yes wins (:29-49). Nothing was lost. The skill grew. |
| `spec-author` | 194, 156 | 374 | **Composes `grill`**, named in backticks while `grill` is a draft (:98-110). The one-question rule was retired deliberately: S-005 retired, S-008 and S-009 added, with the amendment pending approval. The inline fallback (:102-105) never produces a "decisions record", but :110 requires one. |
| `new-task` | 150, 170 | 362 | **Kept**: honest `touched_files`, `depends_on`, and a literal acceptance command. **Added**: one fresh context window (:26), tracer bullets (:28), and expand, migrate, contract (:47-59). |
| `test-quality` | 189, 169 | 368 | **Kept**: every old check. **Added**: tautology (:36-40) and deep modules (:42-44). Its description claims fix-batch composes it (F1). |

The most common failure is checklist item (f). Steps without a "Done when" were found in `grill`, `domain-language`, `tdd`, `retro`, `improve-architecture`, `zen`, `fix-batch` (steps 4, 5 and 7), `house-review` (3, 5 and 7), `pr-describe` (1, 3 and 4), `doc-sync` (every step), `systematic-debugging` (3 and 5-8), `agent-handoff` (4), `spec-author` (4 and 5) and `new-task` (5 and 7). The lens says every step ends on a completion criterion, and the overhaul did not apply that rule.

Specs: dated 2026-11-23 amendments exist for `spec-author`, `systematic-debugging`, `verifier-agent`, `house-review`, `install`, `build-adapters` and `validate-skills`. PR #98 lists all seven as needing the maintainer's approval.

## Check 6: study, do not copy

`mattpocock/skills` was cloned at `abeeaf9`, the commit the plan names, into the scratchpad, outside the repository. A script (`python3 -I`) normalised each changed `.md` under `.agents/` and each of the 127 upstream `.md` files, then reported two things: identical sentences of six or more words, and shared runs of ten or more words.

- **No reproduced span is longer than 20 words.** That means no single sentence over about 25 words is copied verbatim.
- **Short verbatim pairs, two consecutive sentences each.** All of them are in `improve-architecture/references/vocabulary.md`:
  - :25, "The deletion test. Imagine deleting the module.";
  - :27, "The interface is the test surface. Callers and tests cross the same seam.";
  - :41, "Merge the modules and test through the new interface directly. No adapter.";
  - :55-56, which reproduces two of `HTML-REPORT.md`'s example phrasings, "Pricing leaks across the seam." and "Deepen: one interface, one place to test." (upstream :117-118).
  - These come from `codebase-design/SKILL.md:63-64`, `DEEPENING.md:11` and `HTML-REPORT.md`. `vocabulary.md` carries no provenance block of its own; the blocks are in `improve-architecture/SKILL.md`.
- **Close paraphrase.**
  - `retro/SKILL.md:72-75` follows upstream `retro/SKILL.md:19` clause by clause, for about 45 words: "gets a deterministic check, full stop: a custom rule in the repository's own linter, a hook, or a CI job, whichever its language and existing guardrails make cheapest". The next sentence, "Default to building the check over writing the rule.", is verbatim.
  - `agent-handoff/SKILL.md:21-22` ("Mid-phase there is nothing to decide: continue, or split what is left into subagents.") lightly rewords `PHASE-BOUNDARIES.md:5`.
- **Shorter matches.** These are one term or one clause each, and acceptable: `grill`, `new-task` (expand-contract wording), `house-review/references/rationale.md:14` ("A change can pass one axis and fail the other"), `tdd`, `test-quality` and the lens.

Everything is MIT and has provenance, so this is not a licence problem. It does depart from the plan's "in this kit's own words".

## Check 7: cross-skill coherence

- **Drafts.** No shipped skill relative-links a draft. `install.py` would refuse one, and the profile dry runs passed.
- **`review-depth`.** No file names `review-depth` as a current skill. Every remaining mention outside `.tasks/done/`, `CHANGELOG.md` and `docs/reviews/` is historical or says it was retired:
  - `README.md:49`, `ROADMAP.md:34-36,65,98,481,495`, `docs/ARCHITECTURE.md:43,61` and `docs/OBSERVATORY.md:352-357`;
  - `docs/spec/house-review.md:39` and `docs/spec/README.md:89`;
  - `house-review/SKILL.md:247` and its rationale, plus their plugin copies;
  - comments in `scripts/check-provenance.py`, `scripts/validate-skills.py` and three tests (one of which, `test_hooks_currency.py:199`, builds a fixture skill with that name);
  - the open `chore-0070` and `feat-0080`.
  - The only nit is `tests/test_install.py:815`, whose docstring still calls it "the draft this behaviour was filed on" without saying it is gone.
- **Catalog.** `docs/CATALOG.md` has 29 rows. Status (`shipped`/`draft`) and invocation (`model`/`user`) match every skill's frontmatter exactly, checked by script.
- **`zen`.** It names every skill, and its draft marks match.
- **Install commands.** The commands in `README.md`, `CATALOG.md`, `INSTALL.md`, `GETTING-STARTED.md` and `zen` use only flags that `install.py --help` lists.
- **Profiles.** `INSTALL.md`'s profile table (core 3, spine 17, all 19) matches the installer: 14 seeds expand by 3 to 17.
- **Description budget.** The default profile is `spine`. With `--dry-run` into a scratch home:
  - at `origin/developer`, `Description budget: 10209 characters for this profile` over 18 skills;
  - at the head, `6827` over 17 skills, of which 747 characters belong to the two user-invoked skills, which leaves **6,080 in a Claude Code session's context**.
  - These are the "before and after" that `feat-0080` asks for and that no document reports yet.
- **Closed tasks.** The closed task files are inconsistent with their status. `feat-0079` is `status: done` with all 8 acceptance and done checkboxes unticked (`.tasks/done/feat-0079-*.md:141-154`), even though this verification confirms the criteria behind them hold. `feat-0076` records one criterion as "Half met" (:141). That deviation is justified, because linking draft `grill` from shipped `spec-author` is forbidden.

## Check 8: commit trailers

`git log origin/developer..HEAD --format=%B | grep -ci co-authored` returns `0` across all 26 commits. Every commit is authored `Claude <noreply@anthropic.com>`. GitHub resolves that identity to the `claude` account with a verified signature, so it is not the account-less identity the `AGENTS.md` rule guards against. It does differ from `origin/developer`'s history, which is entirely `hams-ollo`. Before PR #98 meets the `main protection` ruleset, confirm that the ruleset accepts it.

## Findings, ranked

| # | Severity | Where | What | Suggested fix |
|---|---|---|---|---|
| F1 | medium | `.agents/skills/test-quality/SKILL.md:6-7`; `.agents/skills/fix-batch/SKILL.md` (prompt item 6, :124-127) | test-quality says it is "Composed by test-author, tdd and fix-batch", but fix-batch dropped the base :200 instruction to "pick the layer and oracle through the [`test-quality`] lens" and no longer names it. One of the two is wrong, and it is a shipped description that ships in the plugin. | Restore the one-clause pointer in fix-batch's prompt item 6, or remove fix-batch from test-quality's description. |
| F2 | medium | `feat-0080` acceptance; PR #98 body | The before and after figures for the default profile's description characters are unreported. | Publish 10,209 (18 skills) to 6,827 (17 skills; 6,080 model-facing in Claude Code) in PR #98 and the feat-0080 close-out. |
| F3 | medium | GitHub Actions on `zen/overhaul-2026-11` | No CI cell has passed since `acbaae0`. Every later run was cancelled, and the head run is queued. The Windows fixes in `49f77ac` have never run on Windows. | Let run 209 finish on all six cells before the maintainer reviews PR #98. |
| F4 | medium | `.agents/skills/improve-architecture/references/vocabulary.md:25,27,41,55-56`; `.agents/skills/retro/SKILL.md:72-75` | Copied too closely from upstream (Check 6). | Reword in the kit's own voice, and add a provenance block to `vocabulary.md`, as `domain-language/references/` does. |
| F5 | low | the 14 skills listed under Check 5 | Steps without a completion criterion, against the lens's own checklist. | Add a "Done when" to each step. The cheapest place to start is the drafts, before promotion. |
| F6 | low | `fix-batch` 251, `house-review` 256, `doc-sync` 257, `systematic-debugging` 300; median 156 | Over the plan's limits of about 250 lines and a median of about 120. `pr-describe`, `agent-handoff` and `new-task` grew. | Move the next tier of reference material behind links, or record that the limit was relaxed. |
| F7 | low | `.agents/skills/spec-author/SKILL.md:102-110` | The `grill` fallback never produces the "decisions record" that the Done-when at :110 requires. | Say that the fallback ends by writing the decisions record, or loosen :110. |
| F8 | low | `.agents/skills/house-review/SKILL.md:186-191` | The depth output no longer carries the measured signal values `review-depth` printed. The rule is reported but its inputs are not. | Add a `signals:` line to the output block. |
| F9 | low | `.agents/skills/tdd/SKILL.md:137`; `fix-batch:247-249`; `agent-handoff:130`; `test-quality:135`; `systematic-debugging:265-267` | The autonomy pointer is not the plan's one line to `core.md`: these link `autonomy.md` (or only name it) and in places restate rules. | Normalise to the one-line `core.md` pointer the other overhaul skills use. |
| F10 | low | `.agents/skills/fix-batch/SKILL.md:165` | A verifier dispatched to a "separate fresh agent at high effort" is not told it is a leaf, which plan principle 4 requires. | Add "a leaf". |
| F11 | low | `.agents/skills/retro/SKILL.md:22` and :46 | "It changes nothing until the person approves", but step 1 runs the repository's check command, which here includes a real install cycle into a temporary home. | Qualify :22 ("changes no tracked file"), or have step 1 read the last CI result first. |
| F12 | low | `.agents/skills/improve-architecture/SKILL.md:46` | The hot-spot pipeline is POSIX-only (`sort \| uniq -c \| head`), while the same skill allows for Windows at :76. | Give a portable form, or say it needs a POSIX shell. |
| F13 | low | `.agents/skills/zen/SKILL.md` (full flow, :41; :79, :97 compared with :103-106) | The full flow lists "`grill`, then `spec-author`", which invites running the interview twice, since `spec-author` composes `grill`. Only two of the four user-invoked skills are said to be started by a person. | Write "`spec-author` (which runs `grill`)", and mark all four user-invoked skills the same way. |
| F14 | nit | `.tasks/done/feat-0079-*.md:141-154`; `tests/test_install.py:815`; `fix-batch/references/incidents.md:107` | The closed task has its checkboxes unticked. A docstring calls `review-depth` a current draft. The incidents note credits Matt Pocock's ideas in prose without a provenance block. | Tick the boxes that hold, update the docstring, and decide whether idea-level credit needs a block. |

## Re-verification, 2026-11-23

Re-run on `zen/overhaul-2026-11` at `4723d95` ("feat-0080: answer the independent verification and close the integration") by the same verifier. The verifier wrote none of the fixes and changed nothing apart from this section.

### Verdict

```text
verdict: pass
blocking_reasons: []
```

- **Commands.** Every declared command succeeded.
- **Criteria.** Every criterion of `feat-0080` is now met.
- **Findings.** F1 through F4 and F7 through F14 are resolved. F5 and F6 are deferred honestly to `chore-0096`.
- **Open caveat (F3).** The one remaining gap is outside the code. One of the six CI cells, macOS on Python 3.11, never ran, because GitHub could not acquire a runner for it. The other five passed, both Windows cells included.

### Commands, rerun

```text
$ python3 scripts/run-checks.py ; echo EXIT=$?
10 passed, 0 failed, 0 could not run.
Ran on Linux, Python 3.13.18. CI runs 3 operating systems x 2 Python versions, so this is one of six cells: passing here is necessary but not sufficient.
EXIT=0
$ install.py --home <scratch> --tools claude --include-drafts        # exit 0; 27 of 29, 10 drafts
$ ... --check                                                        # 5 current, 0 diverged, 23 linked, 0 revised upstream, 0 unknown, 0 error(s).
$ ... --uninstall                                                    # Uninstalled 28 target(s).
$ build-adapters.py --marketplace --check                            # The committed marketplace is current: 19 skill(s)
$ CLAUDE_CONFIG_DIR=<scratch> claude plugin validate . --strict      # √ Validation passed
$ check-provenance.py                                                # 36 up to date, 3 drifted, 0 unlocatable, 0 error(s).
```

- **Install.** All five user-invoked skills still render `disable-model-invocation: true` in the copy that is placed, and still have none in the source.
- **Provenance.** The three drifts are the same pre-existing `moonray/repoprompt-workflows` blocks as before. The three new blocks in `improve-architecture/references/vocabulary.md` (:70, :79, :88) are up to date.
- **Commit trailers.** `git log 99619f0..4723d95 --format=%B | grep -ci co-authored` gives `0`.

**CI, run 45269597448 on `4723d95`:** the run concluded `failure` because one job was cancelled.

| Cell | Python 3.11 | Python 3.14 |
|---|---|---|
| ubuntu-latest | success | success |
| windows-latest | success | success |
| macos-latest | **cancelled** | success |

The macOS 3.11 job's annotations read: "The job was not acquired by Runner of type hosted even after multiple attempts" and "Due to capacity constraints, jobs targeting macOS arm64 runners may experience longer queue times". The job has no steps and no log. It was never run, so it neither passed nor failed. The verifier did not re-run it, because the run belongs to PR #98.

### Each finding

| # | Status | Evidence at `4723d95` |
|---|---|---|
| F1 | resolved | `fix-batch/SKILL.md` prompt item 6 now reads "pick the layer and oracle through the `[test-quality](../test-quality/SKILL.md)` lens". `test-quality`'s description claim holds again. |
| F2 | resolved | `.tasks/done/feat-0080-*.md:86-87`: "10,209 characters over 18 skills before, 6,827 over 17 after, of which 6,080 is model-facing in Claude Code". `CHANGELOG.md:25` closes `feat-0080`. |
| F3 | partly open | 5 of 6 cells passed, including both Windows cells, so `49f77ac` is now proven on Windows. macOS 3.11 never ran, as described above. Re-run that one job before PR #98 merges. |
| F4 | resolved | The Check 6 script was rerun on `vocabulary.md`, `retro/SKILL.md`, `agent-handoff/SKILL.md` and `fix-batch/references/incidents.md`. `retro` has no match at all. The only matches left are single terms or clauses (the `Interface` table row, "locality: bugs concentrate in one module", the 10-word "the phase boundary. A phase is a chunk of work" against the upstream docs page), with no pair of consecutive sentences. `vocabulary.md` now carries its own three provenance blocks. |
| F5 | deferred, honestly | `.tasks/chore-0096-*.md` names every step from F5. Its acceptance is checkable ("Every step heading ... is followed, before the next heading, by a line starting 'Done when'"). The reason it gives holds: a criterion written only to clear a finding is worse than none. |
| F6 | deferred, honestly | `chore-0096` requires either moving reference material out of the long skills or recording the limit in the lens. A nit: its counts are one line stale, because `fix-batch` is now 252 and `house-review` 257 after F1, F8 and F10. |
| F7 | resolved | `spec-author`'s fallback now ends "then write the decisions record (decisions, terms, facts found, still open) that `grill` would have written." |
| F8 | resolved | `house-review/SKILL.md:187`: `signals: reviewable_lines=412 directories=3 risk_flags=[] blast_radius=[] documentation_only=false`. |
| F9 | resolved | `tdd`, `fix-batch`, `agent-handoff`, `test-quality` and `systematic-debugging` now each read "follows `[core.md](../../rules/core.md) (full text: [autonomy.md](...))`". `fix-batch` still restates which A-rules map to its own steps, which is acceptable because it adds information rather than duplicating the rules. |
| F10 | resolved | `fix-batch`: "a separate fresh agent at high effort that is told it is a leaf". |
| F11 | resolved | `retro`: "It edits no file in the repository until the person approves ... the only command it runs before then is the repository's own check command, once, in step 1." |
| F12 | resolved | `improve-architecture` says the pipeline needs a POSIX shell and gives a `python -c` equivalent. |
| F13 | resolved | `zen`'s full flow is now "`spec-author` (which runs the `grill` interview first)". `retro` and `improve-architecture` now say "A person starts it", like `fix-batch` and `reconcile-worktrees`. |
| F14 | resolved | `feat-0079` has 0 unticked boxes. The `tests/test_install.py` docstring records that `review-depth` was retired. `incidents.md` names its source (`docs/engineering/code-review.md`). The maintainer chose idea-level credit with no provenance block, which is consistent with `AGENTS.md`, because no text was adapted. |

### What a pass means here

The pass is a statement about the evidence that was gathered: the mechanical gates pass, the criteria are met, and the findings are dispositioned. It does not certify quality. That is the job of the maintainer's review of PR #98 and of the seven spec amendments still awaiting approval. It also does not cover the macOS 3.11 cell, which has not run.
