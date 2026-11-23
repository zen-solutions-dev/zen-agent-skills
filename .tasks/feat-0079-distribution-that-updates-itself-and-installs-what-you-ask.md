---
id: feat-0079
title: Distribution that installs what you ask for, renders invocation, and updates itself
type: feat
status: open
priority: P1
parent: "ROADMAP 2026-11 overhaul WS4 Platform"
depends_on: [chore-0095]
spec: docs/spec/install.md
scenarios: []
touched_files:
  - scripts/install.py
  - scripts/build-adapters.py
  - scripts/validate-skills.py
  - scripts/run-checks.py
  - tests/test_install.py
  - tests/test_build_adapters.py
  - tests/test_validate_skills.py
  - tests/test_run_checks.py
  - docs/INSTALL.md
  - docs/spec/install.md
  - docs/spec/install.conformance.md
  - docs/spec/build-adapters.md
  - docs/spec/build-adapters.conformance.md
  - docs/spec/validate-skills.md
  - docs/spec/validate-skills.conformance.md
  - CHANGELOG.md
created: 2026-11-23
---

## Problem

Installing the kit into Claude Code is all or nothing, does not update itself, and has two hazards
the 2026-11 audit reproduced with dry runs:

- An existing `~/.claude/rules/` directory is reported as a conflict, so **no** lens is installed,
  and every skill that composes one runs without it ([`install.py`](../scripts/install.py), the
  rules placement).
- A same-named symlink that points somewhere else is silently relinked, which contradicts the
  installer's "never clobbers" promise.

Beyond the hazards:

- **No single skill installs alone.** Fifteen skills link to each other in one cycle, so asking for
  `new-task` places fifteen. The other workstreams break the cycle in skill bodies; this one makes
  the installer able to take a named set.
- **Drafts cannot be tried.** No profile places a draft, so the new skills from this overhaul could
  never be used, which is the only way under "no skill ships cold" to promote them. `chore-0077`
  also found that the adapters and the plugin tree ship drafts when they should not.
- **Every skill costs description budget.** A skill a person starts by name should cost none. In
  Claude Code `disable-model-invocation: true` does that, but claude.ai and the Skills API reject any
  frontmatter key outside their six. The kit therefore declares it as `invocation: user` under
  `metadata` (see [`writing-for-agents.md`](../.agents/rules/writing-for-agents.md), the invocation
  section), and the distribution paths have to render it.
- **No self-updating channel.** There is no committed `.claude-plugin/marketplace.json`, so
  `claude plugin marketplace add zen-solutions-dev/zen-agent-skills` does not work, and the generated
  plugin manifest still names `hams-ollo` as the repository.

Read [`docs/reviews/2026-11-overhaul-plan.md`](../docs/reviews/2026-11-overhaul-plan.md) in full,
including its rules for every workstream session, before starting.

**New paths this task creates**, so `touched_files` cannot list them yet: `.claude-plugin/` at the repository root.

## Scope

**In scope:**

1. **Fix both hazards.** An existing rules directory the kit does not manage gets the kit's lens
   files placed into it one by one, never overwriting a file the kit did not place (reported as a
   conflict instead). A same-named symlink pointing elsewhere is a reported conflict.
2. **`--include-drafts`**: also place draft skills and their closure, and say which placed skills
   are drafts.
3. **`--skills a,b`**: place the named skills plus their sibling-link closure, and print the closure.
4. **Render invocation.** `validate-skills.py` accepts `invocation` under `metadata` only with the
   value `user` or `model`, alongside `status`. Every path that places a skill for Claude Code (the
   installer's `claude` target and the plugin tree) gives a user-invoked skill
   `disable-model-invocation: true` in the copy it places, and no other path does. The installer
   links skill directories by default on POSIX; choose and document how a rendered `SKILL.md` stays
   current (for example a generated copy that `--check` reports as stale), and test it.
5. **Drafts out of adapters** (`chore-0077`): the Cursor, Copilot and plugin outputs exclude drafts
   unless asked for, matching the installer.
6. **A committed marketplace.** Add `.claude-plugin/` so these work from a clean machine:

       claude plugin marketplace add zen-solutions-dev/zen-agent-skills
       claude plugin install zen-agent-skills@zen-agent-skills

   The plugin must ship only shipped skills by default, carry the rendered invocation, and keep every
   lens reachable from every skill that composes one. Decide between a committed generated tree and a
   manifest that points at `.agents/`, record the decision and the rejected alternative in the task,
   and make `run-checks.py` fail when the committed plugin output drifts from what
   `build-adapters.py` would generate (if you commit a generated tree). Validate with
   `claude plugin validate . --strict` if the `claude` CLI is available, and install into a scratch
   configuration directory, never the real one.
7. **`docs/INSTALL.md`** covers the plugin path first, then the installer, then the adapters; and
   the repository URLs in `build-adapters.py` move to `zen-solutions-dev`.

**Out of scope:** changing what any profile seeds (the integration task recomputes profiles once the
other workstreams land), editing any `SKILL.md`, and every file outside `touched_files` except one
`CHANGELOG.md` line.

## Implementation notes

Facts checked against the Claude Code documentation on 2026-11-23 (re-check anything you rely on):

- `disable-model-invocation: true` removes a skill's description from context; it loads only when a
  person invokes it. Claude Code silently ignores unknown frontmatter keys. Uploads to claude.ai, the
  Skills API, or `package_skill.py` accept only `name`, `description`, `license`, `compatibility`,
  `metadata`, `allowed-tools`, and reject any other key. Source:
  `https://code.claude.com/docs/en/skills.md`.
- A plugin ships skills, agents, hooks, MCP and LSP servers, output styles and more; **rules files and
  `CLAUDE.md` are not plugin components**. A plugin's install directory is a normal directory exposed
  as `${CLAUDE_PLUGIN_ROOT}`, substituted inside `SKILL.md` bodies; `${CLAUDE_SKILL_DIR}` is the
  skill's own directory. Whether a relative `../../rules/x.md` link resolves is undocumented. Paths in
  `plugin.json` start with `./` and stay inside the plugin root. Sources:
  `https://code.claude.com/docs/en/plugins/components.md`,
  `https://code.claude.com/docs/en/plugins/manifest-reference.md`.
- Plugin skills are namespaced (`/zen-agent-skills:new-task`). Auto-update is on by default only for
  official marketplaces; for this one the person turns it on in `/plugin` or runs
  `claude plugin update`. A marketplace entry may list specific skill subdirectories; check
  `https://code.claude.com/docs/en/plugins/marketplace-reference.md` for the exact syntax.
- The skill listing budget is 1% of the context window, each description capped at 1,536 characters;
  on overflow descriptions are dropped, least-invoked first.

Mirror the style of the existing tests. The installer is stdlib-only and cross-platform: no symlink
assumption on Windows.

## Risks and rollback

This changes the installer's placement behaviour and adds a distribution channel, so it touches more
than one module. A regression shows up in `install.py --check` on an existing install; the rollback is
reverting the merge, after which `install.py` reinstalls the previous layout. The marketplace is
additive: removing `.claude-plugin/` withdraws it.

## Acceptance criteria (mechanically verifiable)

    python scripts/run-checks.py

- [ ] Exit 0, with the command and the verbatim tail in the pull request body.
- [ ] New tests cover: both hazards, `--include-drafts`, `--skills` closure, invocation rendering on
      the Claude Code paths only, and drafts excluded from adapters.
- [ ] A dry run into a scratch home with `--include-drafts --tools claude` lists every draft.
- [ ] The marketplace commands above succeed against a scratch configuration, or the pull request
      says exactly why they could not be run here.

## Definition of done

- [ ] Acceptance command passes.
- [ ] Spec amendments and conformance updates flagged for the maintainer's approval.
- [ ] Task file moved to `.tasks/done/` with `status: done` and links re-anchored; one dated line in
      `CHANGELOG.md`.
- [ ] Draft pull request into `zen/overhaul-2026-11`, with "Notes for integration".
