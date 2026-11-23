# fix-batch in Claude Code

Claude Code mechanics for [`fix-batch`](../SKILL.md). Other harnesses provide the same capability
(parallel, isolated, resumable agents with a fresh context) through their own mechanisms; the
procedure in the skill is what matters, and the tool names here are one local implementation.

- **Dispatch (Step 3), same-repository batch.** Create the worktrees yourself at the recorded
  dispatch sha (`git worktree add -b agent/<id> <path> <dispatch-sha>`), then dispatch ordinary
  background agents with the `Agent` tool, all in one message so they run in parallel, each
  `prompt` carrying the hardened prompt and the absolute worktree path. Start each as a fresh
  agent, not a fork of the current conversation, and say in the prompt that it is a leaf.
- **Effort.** Where the harness lets you set an agent's effort, use medium for implementing agents
  and high for the agent that runs `verifier-agent`.
- **Why `isolation: "worktree"` is not the primary path.** It has cut worktrees from `origin/main`
  while the dispatch branch was `developer`, three times on record, and it gives you no place to
  name a base. These worktrees branch from the remote default branch unless the `worktree.baseRef`
  setting is `"head"`, and that setting cannot name a branch or a sha. With it set to `"head"` they
  start from the session's own `HEAD`, which removes the commonest mis-cut but still pins nothing,
  so the explicit cut stays the primary path. If you use it anyway, the post-dispatch
  `git worktree list` check is the only signal you get, and it is a lower bound.
- **Batch against a different repository.** `isolation: "worktree"` worktrees the current project
  only. Use `git -C <target-repo> worktree add -b agent/<id> <path> <dispatch-sha>`. The sandbox rule
  in the prompt then carries the full weight, since there is no harness-level isolation at all; say
  so in the prompt rather than assuming the agent infers it.
- **Built-in `/batch`.** It decomposes an instruction into units itself, runs each in a worktree,
  and publishes each change. Use it for broad mechanical changes. Use `fix-batch` when the items are
  task files a person already approved and each needs independent verification before anything
  lands, which `/batch` does not describe.
- **Do not poll (Step 4).** Background agents re-invoke you on completion.
- **Resume a false-alarm blocker (Step 5).** Use `SendMessage` addressed to the agent's id or name,
  which continues that agent with its context intact rather than starting a fresh one.
- **Verification (Step 6).** Dispatch `verifier-agent` as a separate, fresh `Agent` call from the
  one that did the work, or run its procedure yourself, then run the batch checks with the `Bash`
  tool inside each worktree path.
