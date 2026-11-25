# Dogfood: round 2 align and plan (`feat-0105`)

Recorded 2026-11-25 by the Wave 2 "Align and plan" child of Marjana round 2, on branch `zen/marjana-r2-align`, cut from `zen/marjana-r2-2026-11-25` at `d906b20`. One section per changed skill: what it ran on, the evidence, the verdict, and what the run changed. Every run below happened in this session. No person was present (an AFK child session), so any step that puts a decision to a person is recorded as not exercised.

Before any work, `ZEN_CHECKS_SCOPE=full python3 scripts/run-checks.py` passed on the base (`13 passed, 0 failed, 0 could not run`). The kit's skills were installed at project scope with drafts, and the edited skills reloaded from the working tree as they changed (the harness listed `grill`, `spec-author` and `domain-language` with their new descriptions mid-session).

## `doc-author`: the wizard library

**Ran on.** A runbook a person would really walk: creating the five `role.*` labels `zen-config` names, for the `triage` draft `feat-0106` builds, on a GitHub repository. Written in the scratch directory outside this checkout as `setup_role_labels.py`, built on an unedited copy of `scripts/wizard.py`, four stages (repository, token, labels, an announcing comment behind `irreversible`).

**Evidence.**

- `python3 -m py_compile setup_role_labels.py` printed nothing and exited 0.
- A dry walk, `printf 'me/demo\nfake-token\ny\n' | BROWSER=true python3 setup_role_labels.py --dry-run`, printed all four stages in order ("Stage 1 of 4 ... (3 left after this)" to "Stage 4 of 4"), `would write GH_REPO to .env`, `would write GH_TOKEN to .env`, `would create role.ready-agent` and the other four, and the confirmation, then `all 4 stages walked (dry walk)`, exit 0. No `.env` and no state file appeared in the directory; the token was never printed.
- The declined path, the same with `n` for the last answer, ended `stopped at stage 4 of 4: declined: post a comment ...` and `not done: Announce`, exit 1.
- `python3 -m unittest tests.test_doc_author_wizard`: 13 tests, OK. Each mutation below made it fail: `confirm` accepting `n` (failures=1), `once` ignoring its record (failures=1), `write_env` writing in a dry walk (failures=1).

**Verdict.** Works for its case. **Changed by the run:** piped answers left the next line glued to the prompt (`Repository:   (would write ...`); `_readline` now ends the prompt's line when standard input is not a terminal. Also seen: `getpass` warns "Password input may be echoed" when input is piped, which is correct and is left alone. Not exercised: a real (non-dry) walk against GitHub, and Windows.

## `zen`: the one-quest flow, the bug chain, the declined-ideas read

**Ran on.** Three questions this round raises, answered by following the skill's four steps, reading each named skill's `SKILL.md` frontmatter first (`tdd`, `verifier-agent`, `house-review`, `systematic-debugging`, the last a draft).

1. "`feat-0106` is one quest; what do I run?" Placed at build. The hint: the one-quest flow (read the quest, `tdd` at the seams its plan agreed, the acceptance command, `verifier-agent` by someone else, `house-review`), mode human in the loop, because `feat-0106` holds a check-in gate on a one-way door.
2. "Should the kit get a `triage` skill?", then "a `loop-me` skill?" The step 3 rule sent both to `docs/declined-ideas.md`. `triage`: declined 2026-11-24, **reopened** 2026-11-25 by R2-2 and owned by `feat-0106`, so the hint is to wait for that draft. `loop-me`: declined, holds, so no new skill is suggested.
3. "`validate-skills.py` warns on a line it should accept": a bug with an unknown cause, so `systematic-debugging` *(draft)* then `tdd`, the red command becoming the first failing test.

**Verdict.** Each question reached one skill and one mode. **Changed by the run:** nothing. (Light path 3 was pointed at the one-quest flow while editing, before the run; the run confirmed the two no longer describe the same path twice.) The register held no entry for `wait-what` (a "Missing" verdict, never declined), which is correct: an idea never declined is not in the register.

## `new-quest`: prefactor and the test-seams record

**Ran on.** This quest's own file, [`feat-0105`](../../../.quests/done/feat-0105-align-and-plan-for-round-2.md), id reserved by the round 2 plan.

**Evidence.** Step 4's prefactor bullet was answered in one line ("none", with the reason); the test-seams bullet produced two seams at the highest points (`run-checks.py`, and the wizard library at `Wizard.run`), each with what it catches and misses, recorded once in the quest's Implementation notes, as the step says for a plan with no Quest chain entry. `python3 .quests/validate.py --strict` then reported two errors: `id_high_water['feat'] is 103 but feat-0105 already exists`, and an unresolved link to this record before it existed. Step 6's manifest raise (to 105) and this file cleared both.

**Verdict.** Works. Not exercised: step 4's confirmation of the split with a person; the orchestrator's brief fixed the split. **Changed by the run:** nothing in the skill. Noted for integration: raising `id_high_water` is a shared count, so sibling children raising it to 106, 107 and 108 will conflict on one line.

## `spec-author`: synthesise only

**Ran on.** The amendment of [`spec-author.md`](../../spec/spec-author.md) itself. The decisions it records were confirmed by the maintainer (the coverage map's `to-spec` row as adopted under the round 2 plan) and handed to this session in its brief, so the run drafted from that record and asked no question.

**Evidence.** The amendment adds `S-012`, a Proposed Surface row, and widens Goal 4; a dated note names `feat-0105` and the pending re-approval; `status` stays `approved`. The [`spec-quality`](../../../.agents/skills/spec-quality/SKILL.md) workflow, steps 2 to 8, applied to the amended text, found no finding: `S-012`'s Then is observable (no question asked, the record named, deferred decisions as Open Questions), Goal 4 is covered by `S-008`, `S-009` and `S-012`, and the new surface row appears in `S-012` and, for its unsettled-decision half, in `S-008`. `python3 .agents/skills/spec-author/scripts/spec_digest.py docs/spec/spec-author.md` read `unbound` before and after: the spec carries no `approved_digest`.

**Verdict.** Partly exercised. A brief is not "a `grill` decisions record in this conversation" in the strict sense the new step sets, so this run is the nearest real case, not the case itself. Not exercised: a whole `grill` interview followed by `spec-author` in one conversation, which needs a person. **Changed by the run:** the conformance matrix's Constraint row quoted a phrase `feat-0084` deleted; re-derived and flagged.

## `grill`: E4

**Ran on.** This round's own brief, as the opening input: read in full before anything else, with every source it names (plan, decisions, coverage map rows, podcast notes, the lens, the glossary, the six skills).

**Evidence.**

- **Explore before the first question.** All reading finished before any question was formed. Two questions that looked like decisions became facts on reading: whether `spec-author`'s spec was approved (it is, `unbound`), and whether `domain-language` was shipped (it is, so `grill` may link it).
- **A term collision.** The new term "declined idea" collides with "out of scope" (`grill`'s close, and the `role.out-of-scope` label in `GLOSSARY.md` line 120). The rename question would be: keep "declined idea" for kit-level decisions and avoid "out of scope" for it. Resolved here as the recommended answer, since no person was present.
- **`domain-language` per term.** Run in its one-term mode for "Declined idea" and "Prefactor": step 1 found the glossary from `docs/agents/zen.md` (`glossary: GLOSSARY.md`), step 2 grepped `GLOSSARY.md` and `.agents/` (no prior definition of either; "seam" lives in `deep-modules.md`), step 3 wrote both entries into a scratch copy, `GLOSSARY.scratch.md` in the session's scratch directory, under "Quests". `GLOSSARY.md` itself is unchanged (`git status` shows nothing), as the brief requires.
- **Module shape.** Asked of the wizard library: one module with one entry point (`Wizard.run`) and helpers a stage calls, deep, rather than a script template with the helpers pasted into each runbook (shallow copies). The deep shape was built.

**Verdict.** Partly exercised. Not exercised: the brain-dump playback and any round with a person, both of which need a person. **Changed by the run:** nothing further in the skill.

## `domain-language`: the one-term mode and the rename offer

Exercised inside the `grill` run above, on a scratch glossary. The rename offer was not exercised: neither term disagreed with a name in the code (`grep -rn -i "declined idea\|prefactor"` over `.agents/` found only the new skill text).

## Terms that would be written to `GLOSSARY.md`

For the integrator, who owns whether they land (`feat-0107` owns the Rarity section):

- **Declined idea**: a skill, technique or rule this kit studied and chose not to adopt, recorded with its date, its reason and where it was decided. _Avoid_: rejected idea, won't-do, out of scope.
- **Prefactor**: a behaviour-preserving change made first so the work it eases becomes a small change; a quest of its own, accepted by the existing tests. _Avoid_: preparatory refactor, cleanup.
