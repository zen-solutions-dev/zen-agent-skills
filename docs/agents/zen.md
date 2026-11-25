# Agent skills setup

What each fact the Zen Agent Skills read is in this repository. The skills read the `zen-config` block below; the prose is for people. Written by the configure step of `init-worktracking` on 2026-11-24, its first real run (`feat-0091`). Edit it by hand freely: a re-run keeps every value already set unless you ask, during the run, for a key to change. `python .quests/validate.py` checks the block, and the format is [`docs/spec/zen-config.md`](../spec/zen-config.md).

A key left out means the skills discover that fact themselves. `none` means the repository has no such thing.

```zen-config
config_version: 1
tracker: quests
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

- **Tracker.** Work is tracked in [`.quests/`](../../.quests/), which was `.tasks/` until the rename to quests on 2026-11-25 (`feat-0101`); a quest links its GitHub issue with `external`. No role labels are mapped, because the `quests` tracker has none.
- **Decision records.** `none`: this repository records a decision in the Decisions section of the quest that carries the work, and the reasons behind its rules in [`docs/rationale/`](../rationale/).
- **Base branch.** Work lands on `developer`; a person promotes `developer` to `main`. The 2026-11-24 Marjana round's pull request into `main` (decision `D4`) is a one-off, and `developer` is fast-forwarded afterwards.
- **Memory** is left out until `orchestrate` (a draft in this round) settles where its dated log lives.
- **Confirmed.** The tracker, base branch, standards, default mode and decision-record directory were each a choice between candidates. No person was in the session that wrote this file, so the recommended answers were written first and routed to the maintainer, who confirmed all five in person on 2026-11-24.
