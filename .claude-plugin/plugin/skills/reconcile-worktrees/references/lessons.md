# reconcile-worktrees: the lessons behind it

The incidents behind the rules in [`reconcile-worktrees`](../SKILL.md), moved out of the procedure
on 2026-11-23 by `feat-0077` so the skill body carries what to do and this file carries why. Every
rule they taught is still stated in the skill; nothing here is procedure.

## Why the skill exists (2026-07-07)

Reconciling several worktrees by hand after a batch of parallel agent fixes turned out to be its own
source of risk, separate from whatever the agents did wrong. In the incident that motivated
`fix-batch`: task-file bookkeeping split three incompatible ways across worktrees because some agents
wrote directly to the main checkout and others did not; a binary asset showed an identical phantom
diff in every worktree because of an unmigrated git-lfs rule, which would have silently corrupted the
file if any worktree's changes had been committed with a blanket `git add -A`; and two worktrees
touched the same file in different, non-overlapping regions, which is safe to combine only once you
have checked it.

## Why the landing branch is merged with its target first (Step 1)

A branch that lags its target cannot see any file authored after the cut, so the acceptance command
passes on the branch while the merge result fails. This happened twice in the repository the skill
was written in. Wave 2's branch could not see a task file added to the target after the cut, one
that linked to a task the wave had moved into `done/`: the branch ran green and the `pull_request`
job ran red on all six CI cells. Wave 4 repeated the shape and is the sharper case, because its
`pull_request` job never fired at all, leaving the branch-alone run, green by construction, as the
only signal. The defect was found only by reproducing the merge locally, and it came with a real
conflict in a shared bookkeeping file both branches had bumped. A check that exists only in CI is
not a check when the trigger can skip.

## Why untracked files are enumerated separately (Steps 2 and 5)

Measured on a real three-agent batch whose items were each "add a test file": all three `git diff`
patches were **0 bytes**, so the whole batch would have landed nothing and reported success.
Whenever the work is new files, which is a large fraction of real tasks, the tracked-diff half
returns nothing and the untracked half is the entire result. It produces no error, just an empty
patch and a worktree about to be deleted.

## Why the patch goes through a file, not a pipe (Step 5)

A pipe is where encoding corruption happens: Windows PowerShell 5.1 pipes UTF-16 by default, which
mangles a patch. A file also lets you read what you are about to apply and re-apply it after a
failure.

## Where harnesses put worktrees

Under Claude Code, `fix-batch` worktrees are the ones `git worktree list` reports for the background
agents, commonly under `.claude/worktrees/` or a similarly named directory. Claude Code also runs a
periodic sweep that removes the worktrees it created for subagents and background sessions once they
are older than its `cleanupPeriodDays` setting, keeping any that still hold changed or untracked
files or unpushed commits. So a worktree with work in it waits for this skill, and an agent worktree
you expected but cannot find may simply have held nothing. Neither the sweep nor the exit prompt
lands anything.
