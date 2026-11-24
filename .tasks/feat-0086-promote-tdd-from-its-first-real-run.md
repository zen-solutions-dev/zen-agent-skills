---
id: feat-0086
title: Promote tdd from its first real run, on the hook test isolation fix
type: feat
status: in_progress
priority: P1
parent: "ROADMAP 2026-11 overhaul: drafts the overhaul added"
depends_on: []
spec: ""
scenarios: []
touched_files:
  - .agents/skills/tdd/SKILL.md
  - .agents/skills/test-author/SKILL.md
  - .agents/skills/fix-batch/SKILL.md
  - .claude-plugin/plugin/
created: 2026-11-23
---

## Problem

`tdd` is a draft because nobody had built a real change with it. Its promotion condition: "it has built a real change red to green".

## The real use

Not redone here. The sibling session `kit-test-fixes` used `tdd` on 2026-11-23 to make the instruction-provenance hook tests independent of the machine they run on, and recorded the use in its own task, `chore-0097` (`.tasks/done/chore-0097-make-two-hook-tests-independent-of-the-machine-they-run-on.md`, section "Real-use record: `systematic-debugging` and `tdd`"), on branch `zen/chore-test-isolation-9a7f1c`, commit `cbb70e5`. Named in backticks rather than linked, because the file is not on this branch until that work merges into `developer`; it becomes a link at the rebase in Phase 3.

The fix it built is the one this session's `retro` found from the other side: 30 tests in `tests/test_hooks_instruction_provenance.py` failing on the maintainer's machine because they read the real home directory ([`2026-11-retro-pr-108.md`](../docs/reviews/2026-11-retro-pr-108.md), `R-001`).

**Met, pending merge.** The red test was seen failing for the right reason on every platform, then green. The condition holds once `chore-0097` is in `developer`; this task does not promote before that, and Phase 3 checks it after the rebase.

## What the use exposed (from `chore-0097`'s record)

1. **"Never mock your own modules" is too absolute.** The narrowest correct fence wrapped the hook's own filesystem entry points, because that is where its boundary lives; "inject it as a parameter" would have forced a production change for a test-only need.
2. **It assumes the green code is production code.** Every line written was test fixture. The skill has no guidance for fixing test infrastructure, where the risk is existing tests becoming vacuous. The check that caught it (disable the hook's home exemption in memory and watch a test go red) came from `AGENTS.md`'s "construct the degenerate input", not the skill.
3. **Environment-conditional behaviour does not fit red-green.** A skip that depends on which shell is on `PATH` could only be verified by running under both shells; the skill offers no pattern for that.
4. **What worked:** "watch it fail for the right reason" proved the test pins the whole bug population; the `test-quality` checklist at step 6 found a missing case (a project settings file above the sandbox), which was added. Recording the seam rather than asking, when unattended, worked as written.

## Refinements (apply on promotion)

- Step 3's mocking rule: allow wrapping a module's own I/O seam when the system boundary sits inside that module, and say that is the exception, not a licence to mock collaborators.
- New short section, "Fixing test infrastructure": the green code is a fixture; the red step is a test that goes red when the fixture is removed or the guarded behaviour is disabled, so existing tests cannot silently become vacuous.
- Notes: an environment-conditional behaviour is verified by running under each environment and recording the command and result for each, not by mocking the environment.

## Link conversion (on promotion)

- `test-author` to `tdd`: the three backtick mentions in "How it differs from `tdd`" and "When not to use" become one relative link at the first mention. `test-author` does not compose `tdd`, it hands off to it, so the edge pulls `tdd` into every profile with `test-author`. That is wanted: the hand-off is the skill's own advice. Confirm with the maintainer.
- `fix-batch` to `tdd`: prompt item "New behaviour built test-first goes through `tdd` where the target has it." becomes a link. This one composes: the dispatched agent is told to use it.
- After both, recompute the install profiles (`python scripts/install.py --dry-run` per profile) and report the change in counts; `docs/INSTALL.md`'s profile table belongs to `kit-release-ready`.

## Acceptance criteria (mechanically verifiable)

    python scripts/run-checks.py
    python .tasks/validate.py

- [ ] `chore-0097` is in `.tasks/done/` on `developer` after the Phase 3 rebase.
- [ ] Refinements above applied to `tdd/SKILL.md`.
- [ ] `metadata.status: draft` removed; links converted; `zen` and `docs/CATALOG.md` updated (with `kit-release-ready`).
- [ ] `python scripts/build-adapters.py --marketplace` rerun.

## Definition of done

- [ ] Acceptance commands pass.
- [ ] `doc-sync` over the reader-facing documents, findings applied or dismissed.
- [ ] Moved to `.tasks/done/`, links re-anchored; a dated `CHANGELOG.md` line proposed in the pull request body.
