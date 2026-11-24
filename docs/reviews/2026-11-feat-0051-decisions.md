# Decisions record: the paired evaluation harness (`feat-0051`), 2026-11-23

**How it was made:** routed by [`zen`](../../.agents/skills/zen/SKILL.md), interviewed with [`grill`](../../.agents/skills/grill/SKILL.md) over three rounds plus a close, terms kept with [`domain-language`](../../.agents/skills/domain-language/SKILL.md) in [`GLOSSARY.md`](../../GLOSSARY.md). All three skills were drafts; this is the real use recorded in `feat-0089`, `feat-0084` and `feat-0085`. Every decision below is the maintainer's, given in this session; the facts were looked up by two fresh-context leaf subagents and spot-checked in the main session.

**Confirmed restatement:** `feat-0051` becomes three tasks that evaluate `house-review`, `verifier-agent` and `fix-batch`, on demand, with `claude plugin eval` run from a scratch copy that pairs each case against Claude Code as shipped, on Sonnet only, capped at $25, with local reports, committed summaries, no gate yet, and the lens ablation filed separately.

## Decisions

1. The suite runs on demand only, started by the maintainer with a cost ceiling; a path-scoped pull request trigger is revisited once three cases have run twice with stable results. (Q1)
2. A drop in pass rate gates nothing yet. What would earn a gate: three or more skills whose every case discriminates on two separate runs. (Q2)
3. Evals live in a root-level `evals/` directory, one subdirectory per skill; never inside a skill directory (the installer copies whole skill directories into an adopter's home) and never under `tests/` (the offline gate). (Q3)
4. The runner is `claude plugin eval`, behind a staging script that copies the generated plugin tree and the root `evals/<skill>/` into a scratch directory outside the repository and runs `--ablation with-without` there, so the agent under test only touches a copy and cannot write the graders. (Q4)
5. The October branch `zen/eval-slice-71f3d5` is mined, then closed: keep its grader-isolation rule, its keep / merge / retire / trim decision rules, and its fixtures for skills that still exist; drop the `review-depth` cases and its `claude -p` runner. (Q5)
6. The first three skills are `house-review`, `verifier-agent` and `fix-batch`; each case is re-anchored to cite the closed task its failure came from. (Q6)
7. The baseline is Claude Code as shipped, built-ins included, as the single baseline arm. (Q7) Recorded as a Decisions entry in the rewritten `feat-0051`, not as a new `docs/adr/`. (Q18)
8. The maintainer signs in themself; the staging script never reads, copies or passes a credential. The CLI on `PATH` is updated so it has `--eval-dir` and `--trust-plugin`. (Q8)
9. First pass: Sonnet 5.5 only, three runs per case per arm, `--max-cost-usd 25`. Haiku and Opus follow in a second pass once cases are shown to discriminate; Anthropic's three-model checklist item is deferred on purpose, not dropped. (Q9)
10. Reports are never published: the staging script always passes `--no-publish`. (Q11)
11. After a run, only a summary is committed under `evals/results/` (scores per case and arm, which graders discriminated, total cost, model, CLI version); transcripts and the HTML report stay out of git. (Q12)
12. The staging script's plumbing is tested offline by `run-checks.py`, with no model call. (Q13)
13. The lens ablation is out of the first pass and filed as its own follow-up, reusing this runner and the October A1, A3, A4 and A10 fixtures. (Q14)
14. The staging script passes `--threshold 0`, so a low score never reads as a broken command. (Q15)
15. `new-task` rewrites `feat-0051` as three tasks, each sized to one fresh context: (a) the staging script and its offline tests; (b) cases for the three skills; (c) the first run and the closeout, blocked on the maintainer's sign-in. (Q16)

## Terms

Written to [`GLOSSARY.md`](../../GLOSSARY.md) as each settled (Q10, Q17): **Case**, **Arm**, **Baseline**, **Grader**, **Discriminating**.

## Facts found

- No `claude` CLI on this machine is signed in: `claude auth status` gives `"loggedIn": false, "authMethod": "none"` (source: the command, run on v2.1.232 on `PATH` and on the desktop app's v2.1.330).
- `claude plugin eval` exists in both versions; `--eval-dir`, `--trust-plugin` and a path-target with-without default arrived by v2.1.330 (source: `claude plugin eval --help` on each).
- It reads cases from, and writes results to, a directory below the plugin, and publishes its report to claude.ai unless `--no-publish` is passed (source: the same help text).
- The repository's plugin tree holds 19 skills, none a draft, and no `evals/` (source: listing `.claude-plugin/plugin/`).
- `zen/eval-slice-71f3d5` (2026-10-21) holds a pre-registered 413-run harness that was never run; it runs `claude -p` children with `--permission-mode bypassPermissions` (`run.py` line 110), pins October revisions of every skill, and spends 72 of its runs on the retired `review-depth` (source: the branch's `evals/rank9/PLAN.md` and `harness/run.py`).

## Still open

- The incident-to-eval ratchet (`feat-0051` amendment C): deferred by the task itself to the closeout of the first run; owner, sub-task (c).
- Rewriting `feat-0051` as the three tasks of decision 15: owner, the maintainer's next `new-task` session.
