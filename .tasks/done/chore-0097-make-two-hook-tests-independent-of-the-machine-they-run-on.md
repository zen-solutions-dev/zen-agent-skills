---
id: chore-0097
title: Make two hook tests independent of the machine they run on
type: chore
status: done
priority: P1
parent: "ROADMAP 2026-11 overhaul follow-up"
depends_on: []
touched_files:
  - tests/test_hooks_instruction_provenance.py
  - tests/test_hooks.py
  - .agents/hooks/instruction-provenance-reminder.py
  - .tasks/.scaffold.json
created: 2026-11-23
---

## Problem

`python scripts/run-checks.py` failed on a maintainer's Windows machine (Python 3.11.10) at
`developer` `0305d5c`, while CI passed all six cells. Two independent causes, both in the tests:

- **Test isolation, 30 tests.** Every test in
  [`test_hooks_instruction_provenance.py`](../../tests/test_hooks_instruction_provenance.py) builds its
  fixtures with `tempfile`. On Windows the temporary directory sits under the person's home, and the
  hook ([`instruction-provenance-reminder.py`](../../.agents/hooks/instruction-provenance-reminder.py))
  walks from the launch directory up to the filesystem root by design. On a machine with a real
  `~/.claude/CLAUDE.md`, every test found that file above the fake home it passed: 4 failures on an
  unexpected finding and 26 errors from the tests' own `relative_to` calls. On Linux CI `/tmp` is not
  under home, so nothing above the temp root was ever there to find.
- **Codex wiring test.** `test_every_codex_command_launches_and_exits_zero` in
  [`test_hooks.py`](../../tests/test_hooks.py) ran the commands under whatever `shutil.which("bash")`
  returned. From PowerShell that is `C:\Windows\System32\bash.exe`, the WSL launcher, which with no
  working distribution fails before it reads a command (`execvpe /bin/bash failed 2`). From Git Bash
  the same test passed, because `bash` resolves to Git's.

The hook is correct: `findings(Path.home(), Path.home())` returns `[]` on the same machine, and it
skips `~/.claude/CLAUDE.md` at the home it is given, which in real use is the real one. It was not
changed.

## Scope

**In scope:** a sandbox per test whose parent directories are invisible to the hook, a regression
test that plants instruction files and a git repository above the sandbox and asserts exact results,
and a probe that skips the Codex test with the reason when no `bash` or `sh` on PATH can run `true`.

The `chore` high-water mark in `.tasks/.scaffold.json` moves to 97, which `validate.py --strict`
requires once this file exists.

**Out of scope:** the hook itself, `CHANGELOG.md` (owned by another session during the release; the
dated line for this task is owed there), and the status of the two draft skills used below.

## Decisions

- **Rejected: filtering findings to paths under the temp root.** It fixes `found()` but not the
  `evaluate()` tests, and it cannot undo a git repository above the root turning "outside any git
  repository" into "not committed". The fence wraps the hook's two filesystem lookups, `_entry` and
  `find_work_tree`, and leaves the walk inside the sandbox as the hook does it.
- **Rejected: patching `os.listdir` and the `Path` predicates.** Broader, and every new lookup the
  hook grows would leak around it.
- **A premise that turned out false:** the brief's red command for the Codex test is not machine
  wide. It reproduces from PowerShell and passes from Git Bash, so a fix verified only from the
  agent's own Bash tool would have looked green while changing nothing.

## Acceptance criteria (mechanically verifiable)

    python scripts/run-checks.py

- [x] `NothingAboveTheSandboxLeaksInTests` fails without the fence (both tests, with the planted
      paths and the reason flipped to "in a repository, not committed") and passes with it.
- [x] All 48 tests in `test_hooks_instruction_provenance.py` pass on the machine that failed.
- [x] With the hook's home exemption disabled in memory, `test_user_memory_at_home_is_not_reported`
      fails again, so the fence did not make the suite vacuous.
- [x] The Codex test skips from PowerShell with the WSL stderr in the reason, and runs (not skipped)
      and passes from Git Bash.
- [x] Every gate in `run-checks.py` passes locally.

## Definition of done

- [x] Acceptance command passes locally (one of six CI cells).
- [x] Conventions in AGENTS.md's conventions section followed.
- [x] `doc-sync`: no reader-facing document describes these tests' fixtures; nothing to apply.
- [ ] One dated line in `CHANGELOG.md`: owed to the release-readiness session that owns that file.

## Real-use record: `systematic-debugging` and `tdd`

Both skills are drafts. This is evidence for their promotion, recorded by the agent that used them;
their `status` was not changed here.

### `systematic-debugging`

Run before any edit, bound declared as 5 disproved hypotheses per defect, record kept outside the
tracked tree. Verdict for both: `root_cause_found`, one hypothesis each, none disproved.

**What it did well**

- **Red command before a hypothesis caught a false premise.** The Codex test passed when first run
  from the agent's Git Bash. The skill's line "check whether you are the one varying it" pointed at
  the condition nobody was holding still, which `bash` PATH resolves to; rerunning from PowerShell
  pinned it and reproduced the failure. Without that step the fix would have been verified in an
  environment where the test already passed.
- **"An observation that could have disconfirmed it."** The confirming trial for the Codex defect was
  `bash -c true` under the same resolution: it fails with the same WSL stderr, and would have
  succeeded had the command been at fault. That is sharper than "the skip makes it go away", which
  is the sufficient-condition trap the skill names.
- **Restating the symptom as an observable** (the exact `ValueError` path and the extra
  `(C:/Users/.../.claude/CLAUDE.md, outside any git repository)` finding) localized the isolation
  defect without any instrumentation.

**What it got wrong, or where it was friction**

- **No verdict for "the defect is in the test".** The code under test was correct; the tests were
  wrong. Step 7 covers the report being in error, not the oracle. `root_cause_found` with
  `implicated_files` naming a test file works, but the skill never says a test can be the implicated
  code, and step 7's wording nudges toward "nothing to fix".
- **Diagnose-and-fix in one assignment has no path.** Step 8 answers a diagnose-then-fix request
  with the diagnosis alone and sends the fix to `fix-batch`. That is overkill for a two-file test
  fix assigned to the same agent; the skill should name the hand-over to `tdd` in the same session
  as legal, which is what `tdd`'s own "When to use" already says.
- **Step 4 (localize with boundary instrumentation) had nothing to do.** The error text localized
  both defects. The step is conditional ("where a failure crosses components"), but its "Done when"
  still demands a `hypotheses` entry naming a boundary, which here would be ceremony.

### `tdd`

Seam recorded rather than asked (unattended): the `_Tmp` fixture's sandbox boundary, observed
through the hook's public `findings()` and `evaluate()`. Behaviours: (1) nothing above the sandbox
changes a result; (2) the existing 46 tests pass with a real file above their temp root; (3) the Codex
test skips on an unusable shell and runs unchanged on a usable one.

**What it did well**

- **"Watch it fail for the right reason."** The regression test's first run showed both leaks at
  once: the planted files and the reason flipped by the repository above. That proved the test pins
  the whole bug population, not just the one file this machine happens to have, and it is red on
  every platform, which the original failures were not.
- **The `test-quality` checklist at step 6 found a gap.** Item 9 (does the oracle cover the bug
  population) showed the planted set lacked a project settings file read at a work-tree root above;
  it was added.

**What it got wrong, or where it was friction**

- **"Never mock your own modules" is too absolute.** The narrowest correct fence wraps the hook's own
  `_entry` and `find_work_tree`, because that is where its filesystem boundary lives. The rule
  should allow wrapping a module's own I/O seam when the boundary is inside the module, which its
  "inject it as a parameter" advice would otherwise force as a production change for a test-only
  need.
- **It assumes the green code is production code.** Here every line written was test fixture. The
  skill has no guidance for fixing test infrastructure, where the risk is not a missing behaviour
  but existing tests becoming vacuous. The check that caught that risk (disable the hook's home
  exemption in memory and watch a test go red) came from `AGENTS.md`'s "construct the degenerate
  input", not from the skill.
- **Environment-conditional behaviour does not fit red-green.** The Codex skip can only be observed
  by changing PATH, so a test of it would mock `subprocess` and prove little. It was verified by
  running under both shells instead; the skill offers no pattern for that.
