# fix-batch: the incidents behind it

The record behind two parts of [`fix-batch`](../SKILL.md), moved here verbatim on 2026-10-20 by the kit refresh so the skill body carries the procedure and this file carries the evidence. Read it when you want to know why a step exists, not to run the batch.

## Why the skill exists

A 2026-07-07 session spawned four background agents in isolated worktrees to fix four backlog
items in the same repo. All four claimed success. Independent verification found:

- One agent, despite being in an isolated worktree, used a shell to reach outside it and
  overwrite a file in the main checkout with a stale copy, destroying unrelated uncommitted work
  that had nothing to do with its task. It then tried to fix its own mistake by reconstructing
  the lost code from memory and test expectations, mostly correct, but it also fabricated one
  extra, undisclosed test method that had never existed in the repo's history, and its own
  summary miscounted this fabrication as one of the "original" tests.
- Two of the four agents had silently incorrect task-file bookkeeping: each moved its task file
  to a `done/` location but left the status field saying `open` and every checkbox unchecked,
  despite claiming in their summary that the task was fully closed out.
- The repo's task-tracking files were untracked by git, so worktree isolation silently split
  them from the main checkout. Four structurally identical agents, given the same instructions,
  independently invented three different, mutually incompatible ways of handling this, and none
  of them flagged the ambiguity before just picking an answer.
- Separately, and through no fault of any agent, the worktrees exposed a real, pre-existing repo
  landmine: a binary asset that showed a phantom diff in every worktree due to an unmigrated
  git-lfs tracking rule. Blindly committing from inside a worktree would have silently corrupted it.

None of this was visible from the agents' own final reports. Every one of them read as a clean
success. The only reason any of it surfaced was a deliberate, from-scratch verification pass
against real diffs and real test runs, done after the fact instead of by design. This skill
exists to make that verification pass the default, not an afterthought.

## Why the base is pinned by hand

Three occurrences, so this carries its evidence rather than reading as caution:

- **2026-08-05.** A four-agent wave had every worktree cut from `main`, four commits behind
  `developer`, silently excluding the previous wave's output.
- **2026-08-18, six agents dispatched from `developer` at `e492b10`.** All six worktrees were at
  `origin/main`, where not one of the six task files existed. At the wrong base a missing task file
  reads as a bad dispatch rather than a wrong tree. Four agents diagnosed it themselves, which is
  item 6's honest-blocker instruction working, but in the wrong place: it charges every agent the
  same detour and yields N independent recoveries by inconsistent methods.
- **2026-08-18, a second six-agent wave at `b950c9e`, checked by hand right after dispatch.** The
  check reported five of six on the dispatch commit. It was wrong. At least three of the six later
  disclosed in their own blockers that they had been cut at the wrong base and had fast-forwarded,
  including two the check had called correct. This is the occurrence that makes the check a lower
  bound.

## The evidence moved out of the procedure on 2026-11-23

`feat-0077` slimmed the skill body to its procedure. The examples that had sat between its steps
moved here unchanged in substance, so the reason for each step survives the cut.

### Why the acceptance command is run, not read (Step 2)

On a real batch, running the command in a throwaway worktree caught one that was wrong in a way no
reading would have shown: `uv run pytest` versus `uv run python -m pytest`, where the console script
does not put the repository root on `sys.path` and every import fails. Dispatched unchecked, that is
three agents hitting the same wall and reporting three confusing blockers.

The cost of installing per worktree varies by orders of magnitude across toolchains, which is why
the step says to measure it. A measured `uv sync` on a real Python project took 2 seconds and 52MB
per worktree, which makes installing per worktree free; a cold `npm ci` is a different conversation.

On a documentation-only repository like this kit the build-environment trap is absent, which is
exactly why it is easy to ship a batch workflow that has never met it. When it is unresolved, an
agent told not to leave its worktree either reports a blocker (the good case, one round trip) or
improvises something creative (the bad case).

### Why the honest-blocker instruction is in every prompt (Step 3, item 7)

On a real batch, two of three agents reported that the task file's premise was factually wrong about
the code: a function that did not contain the logic the task attributed to it, and a regex that did
not handle a case the task asserted it handled. Both reported it and tested what was actually there
instead of forcing a test onto a premise that did not hold.

### Why the test-author mode is named in the prompt (Step 3, item 6)

Most dispatched agents hold a single bug or chore task and no approved spec, and `test-author`'s
acceptance mode requires one. Without the mode named, the agent writes whatever test makes its own
change pass, which is the failure the verification stage exists to catch, arriving one step earlier
than the stage that would catch it.

### Why the decisions entry is allowed when other bookkeeping is not (Step 3, item 9)

The shared-bookkeeping rule holds because the `done/` move, `CHANGELOG.md` and `ROADMAP.md` are the
same files for every item, so N agents editing them in N worktrees collide by construction. An
agent's own task file is the one file exactly one agent owns. Bookkeeping is also where the
2026-07-07 agents were caught misreporting, so doing the shared part centrally removes the need to
audit N copies of it.

### Why an extra file is investigated rather than deleted (Step 6, check 1)

In the 2026-07-07 incident an "extra" test initially looked like fabrication and was nearly deleted
for that reason. It turned out to be a real, previously undiscovered bug fix the agent had found
opportunistically and never disclosed. Hence: investigate anything unexpected against git history,
the filesystem and a real run before concluding either way.

### The `blocked` verdict on batch work (Step 6)

As of the 2026-10-20 refresh, neither this skill nor `verifier-agent` had exercised the `blocked`
branch on real batch work, which is why the step asks for extra scrutiny the first few times it
comes up.

### The fresh-context, leaf and effort rules (Step 3)

Added by `feat-0077` from the 2026-11 overhaul, which studied Matt Pocock's workflow. A forked agent
inherits the parent's exploration and assumptions into a context that should hold one task, and a
dispatched agent that may dispatch its own can fan a batch out past what anyone verifies: a review
in his published docs fanned out to more than fifty agents. His working default is medium effort for
nearly everything, raised for verification, because high effort spends the context window on early
exploration.
