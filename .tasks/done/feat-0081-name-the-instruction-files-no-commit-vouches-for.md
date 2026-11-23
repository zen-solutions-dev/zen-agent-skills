---
id: feat-0081
title: Name, at session start, every auto-loaded instruction file that no commit vouches for
type: feat
status: done
priority: P1
parent: "ROADMAP Epic B #13: telemetry-guard (reframed as enforcement hooks)"
depends_on: []
touched_files:
  - .agents/hooks/instruction-provenance-reminder.py
  - tests/test_hooks_instruction_provenance.py
  - scripts/install.py
  - .codex/hooks.json
  - .opencode/plugins/zen-hooks.mjs
  - .agents/hooks/README.md
  - docs/CATALOG.md
  - SECURITY.md
  - docs/INSTALL.md
  - ROADMAP.md
  - CHANGELOG.md
  - .tasks/.scaffold.json
created: 2026-10-28
---

## Problem

Harnesses load instruction and configuration files by **location**, before the agent has read
anything: `CLAUDE.md` and `AGENTS.md` from the directory a session starts in and every directory
above it, and a project's `.claude/settings.json` and `.mcp.json` from its root. In October 2026
Forever Security reported that an `AGENTS.md` dropped into a Downloads folder steered Codex into
installing a malicious npm package in most test runs, and that a planted `CLAUDE.md` redirected
Claude Code's API endpoint about half the time. A web page can save such a file without a click,
and there is no patch, because loading those files is how the tools are meant to work. (Figures
from press coverage of Forever Security's write-up, "Markdown Is the New Executable"; the primary
page was not readable from the session that filed this.)

This kit makes `AGENTS.md` canonical in every repository it scaffolds, and its rule `A10` in
[`autonomy.md`](../../.agents/rules/autonomy.md) treats material an agent did not author as data.
But `A10` governs what an agent does **after** it reads something, and a planted instruction file
is loaded first. Nothing in the kit named such a file at the moment it mattered.

## Scope

**In scope:**
- A `SessionStart` reminder, [`instruction-provenance-reminder.py`](../../.agents/hooks/instruction-provenance-reminder.py),
  that names every auto-loaded file sitting outside any git repository or absent from git's index,
  with the reason for each, and points the agent at `A10`. Silent when every such file is
  committed.
- Memory files (`AGENTS.md`, `CLAUDE.md`, `CLAUDE.local.md`, `GEMINI.md`) checked in the launch
  directory and every directory above it; project files (`.claude/settings.json`,
  `.claude/settings.local.json`, `.mcp.json`, `.cursorrules`, `.windsurfrules`,
  `.github/copilot-instructions.md`) checked at the project root.
- The two personal-by-design files silent inside a repository, except a local settings file that
  sets a key that runs a program or redirects the agent (`hooks`, `env`, `apiKeyHelper`,
  `statusLine`, and similar).
- Wiring in all three adapters (`install.py`'s printed registration, `.codex/hooks.json`, the
  opencode plugin), its own test file, and the reader-facing docs that enumerate hooks.

**Out of scope:**
- The person's own user-scope configuration (`~/.claude/settings.json`, `~/.claude/CLAUDE.md`,
  `~/.codex/config.toml`). Uncommitted by design, so naming them would make the hook speak on
  every start. Auditing them is a different job.
- Registering the hook in this repository's committed `.claude/settings.json`. `AGENTS.md` records
  that a second hook there is a new decision, and it is the author's.
- Judging whether a committed file is safe.

## Decisions

- **A rejected alternative: asking git.** `git ls-files` is the obvious way to ask what is
  committed, and it was rejected for a reason specific to this hook's job: a downloaded folder can
  carry its own `.git/config`, and git runs programs named there (`core.fsmonitor` among them)
  when it reads the index. The hook parses the index file itself, versions 2 to 4 with SHA-1 or
  SHA-256, and stays the module's only-readers property intact: no hook here runs a program.
- **A seam left open deliberately: an unreadable index is "not confirmed", never "committed".** A
  split index, an unknown version, or a truncated file names the file with that reason. The
  direction is chosen: a reminder that speaks once too often costs a line, and one that passes a
  planted file as committed costs the point of the hook.
- **A seam left open deliberately: "in the index" includes staged.** A file someone staged and
  never committed is treated as vouched, because staging is an action taken inside the
  repository, which is the line this hook draws.

## Acceptance criteria (mechanically verifiable)

    python -m unittest tests.test_hooks_instruction_provenance tests.test_hooks tests.test_install -v
    python scripts/run-checks.py

- [x] A planted `AGENTS.md` in a folder no repository covers is named, with its reason, and the
      message points at `A10`.
- [x] An uncommitted `AGENTS.md` in a repository is named; committed ones are silent.
- [x] The index parser agrees with git on v2, v3 with an extended flag, v4 prefix compression, and
      a SHA-256 repository; a split index and a truncated index are reported as unconfirmed.
- [x] A linked worktree reads its own index.
- [x] Uncommitted personal files are silent; a local settings file that sets `hooks` and `env` is
      named with those keys.
- [x] User-scope settings at the home directory are not reported; only `startup` fires.
- [x] An AST guard proves the hook imports no process module and writes nothing.
- [x] Nothing inside this repository is reported when the hook runs against it.
- [x] Registered in all three adapters; the module-wide wiring tests cover it.

## Definition of done

- [x] Acceptance command(s) pass locally.
- [x] Conventions in AGENTS.md's conventions section followed.
- [x] `doc-sync` run over the reader-facing documents. The hook enumerations in
      `.agents/hooks/README.md` and `docs/CATALOG.md` gained a row, and `SECURITY.md` gained the
      instruction-file section the hook answers. `docs/INSTALL.md` was found already stale
      before this change: it said the module "ships three hooks, two reminders and one gate"
      when it shipped six. The count was replaced by a pointer to the README table, per the
      membership-not-enumeration rule in `AGENTS.md`, and the new hook was added to its list.
      `README.md` and `docs/ARCHITECTURE.md` name no individual hook and needed nothing.
- [x] File in `.tasks/done/`, `status: done`; one dated line added to `CHANGELOG.md`.
