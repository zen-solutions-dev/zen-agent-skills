# Agent skills setup

What each fact the Zen Agent Skills read is in this repository. The skills read the `zen-config` block below; the prose is for people. Written by the configure step of `init-worktracking` on 2026-11-24, its first real run (`feat-0091`). Edit it by hand freely: a re-run keeps every value already set unless you ask, during the run, for a key to change. `python .tasks/validate.py` checks the block, and the format is [`docs/spec/zen-config.md`](../spec/zen-config.md).

A key left out means the skills discover that fact themselves. `none` means the repository has no such thing.

```zen-config
config_version: 1
tracker: tasks
glossary: GLOSSARY.md
adr_dir: none
spec_dir: docs/spec
standards: AGENTS.md, .agents/rules/house-style.md, .agents/rules/writing-for-agents.md, .agents/rules/review-quality.md
acceptance: python scripts/run-checks.py
base_branch: developer
integration_prefix: zen/
merge_policy: an orchestrator merges verified work it did not author into a zen/ integration branch; a person merges into developer and main
session_logs: ~/.claude/projects
default_mode: hitl
```

## Notes

- **Tracker.** Work is tracked in [`.tasks/`](../../.tasks/); a task links its GitHub issue with `external`. No role labels are mapped, because the `tasks` tracker has none.
- **Decision records.** `none`: this repository records a decision in the Decisions section of the task that carries the work, and the reasons behind its rules in [`docs/rationale/`](../rationale/).
- **Base branch.** Work lands on `developer`; a person promotes `developer` to `main`. The 2026-11-24 Marjana round targets `main` directly by the maintainer's decision `D4`, and `developer` is fast-forwarded afterwards.
- **Memory** is left out until `orchestrate` (a draft in this round) settles where its dated log lives.
- **Pending confirmation.** The tracker, standards, base branch and default mode were each a choice between candidates. No person was in the session that wrote this file, so the recommended answers were written and routed to the maintainer, who confirms or corrects them in the Marjana pull request.
