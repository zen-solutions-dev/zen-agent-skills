# Plan F5: sandboxed runs for untrusted code and skills

Status: **plan only, nothing built.** Written 2026-11-25 for quest [`chore-0114`](../../.quests/chore-0114-plan-sandboxed-runs.md), Phase 3 of the [round 2 plan](2026-11-25-marjana-r2-plan.md). Decision F5 in [the decision record](2026-11-25-marjana-decisions.md): yes.

## Goal

A way to **run** code the maintainer did not write (a third-party skill's scripts, the reproduction steps in an issue, a contributor's tests) where it cannot read secrets, reach the network, or change the real checkout, and to get back only a report. Today the kit's answer is never to run it at all; that is safe and leaves questions unanswered ("does this skill's script do what it says?", "does this issue reproduce?").

The source is thin: Matt Pocock's Sandcastle, "his open-source TypeScript agent orchestrator: 'drop in any agent and run them in sandboxes,' Docker, Podman, Vercel" ([extraction](2026-11-25-podcast-extraction.md), section 2, "Tools and stack", ~1:27:30 to ~1:27:40). The extraction notes "Sandboxes appear only through Sandcastle" and nothing on vetting third-party skills (section 4, "Security"). The rest of this plan rests on the kit's own lessons.

## What exists to build on

- The [`vet-skill`](../../.agents/skills/vet-skill/SKILL.md) draft, whose isolation rules are the floor:
  - Fetch without executing: `GIT_LFS_SKIP_SMUDGE=1 git clone -c core.hooksPath=/dev/null`, no submodules; "Never `pip install`, `npm install`, a plugin installer or a setup script from it."
  - Any interpreter only **from outside the fetched tree, in isolated mode**: `python3 -I your-script.py <path>`, the tree passed as an argument, "a planted `hashlib.py` or `json.py` there runs on import."
  - Searches run from outside the tree, with the tree as a path argument.
  - Persistence is a finding: hooks, scheduled jobs, startup files, other skills.
- `fix-batch`'s sandbox rule: "Worktree isolation is a starting state, not a runtime sandbox." Rule `A1` in [`autonomy.md`](../../.agents/rules/autonomy.md) says the same for every agent.
- Cloud sessions are already disposable containers, and an environment's network can be limited to named hosts. The B5 environment of this round allows only GitHub hosts, package registries and MCP servers ([round 2 plan](2026-11-25-marjana-r2-plan.md), "The orchestrator's own Wave 1 items").
- The close-round nit (k) on `vet-skill`: the clone form and `sha256sum` are POSIX-only. A sandbox procedure needs the same Windows and macOS care (`AGENTS.md` section 6).

## What a sandboxed run must guarantee

1. **No secrets**: no credentials in the environment, no home directory, no git credentials, no connector access.
2. **No network**, or only hosts named in advance; package registries off.
3. **No write path back**: the checkout is a copy; nothing the run writes is merged, committed or installed. Only a text report leaves.
4. **Disposable**: destroyed after the run; nothing persists into the next.
5. **The report is data** (`A10`): what the code printed is quoted, never acted on.

## Candidate runners

| Runner | Fits | Gap |
|---|---|---|
| A claude.ai cloud session in an environment with no allowed hosts and package registries off | Disposable, no local machine at risk, no setup | The agent inside holds a GitHub token for its own repository; needs a session with no repository attached |
| A local container (Docker or Podman) with `--network none`, a read-only copy mounted, no home | Strong network isolation, offline, Sandcastle's model | Needs Docker or Podman installed; never mount the Docker socket |
| A GitHub Actions job with no secrets and read-only permissions | Free for public repositories | Has network by default; runs on GitHub's terms |

## Smallest first slice

1. A reference, `vet-skill/references/sandboxed-run.md`, that states the five guarantees above and one runner's exact steps. No new skill.
2. **One run**: a skill that already passed `vet-skill` has one of its scripts run in that runner, with the run's output as the only thing that comes back. Recorded as a dogfood record of `vet-skill`.
3. Then F4's use: one issue reproduction in the same runner.

## Risks and one-way doors

- **Running untrusted code at all is the one-way door.** Whatever it reads in the sandbox may already be gone; the guarantees must hold before the first run, not after.
- **A sandbox with network is not a sandbox for exfiltration.** Package installs inside it reach the internet; keep registries off unless the person allows one host for one run.
- **Escape routes**: a mounted Docker socket, a shared home, a credential helper, environment variables inherited from the host. Each is checked and named in the report.
- **False comfort.** A clean run shows what the code did this time, not what it does with other input or on another date (a time bomb, a server-side switch). The report says so.

## Rough size

Small to medium: one reference and one dogfood run (one quest); F4's reproduction is a second quest once F4 starts.

## Questions for the maintainer

1. **Which runner should sandboxed runs use first?** (a) A claude.ai cloud session in a saved environment with no allowed hosts, no package registries and no repository attached, recommended: nothing runs on your computer and nothing persists; (b) a Docker or Podman container on your computer with no network; (c) a GitHub Actions job with no secrets.
2. **What may a sandboxed run execute?** (a) Only code that already passed `vet-skill` or `triage`, recommended: a run answers a question the reading left open; (b) any code a person points at.
3. **What may come back out of a sandboxed run?** (a) Only a text report: the commands run and their output, recommended; (b) the report plus files the run produced, after a person reviews them.
4. **Should sandboxed runs be a step of `vet-skill` or a skill of their own?** (a) A reference inside `vet-skill`, recommended: its isolation rules are the floor and it is the first user; (b) a new draft skill both `vet-skill` and the issue-to-PR loop load.
