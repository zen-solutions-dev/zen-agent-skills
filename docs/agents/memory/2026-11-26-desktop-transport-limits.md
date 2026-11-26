# In the desktop app, a turn started by a child cannot start sessions

**Lesson, 2026-11-26**, from rollout round 3, run from the Claude desktop app on the maintainer's computer. A turn the app started because a child session finished (or an answer to a question asked in that turn) was refused when it tried to start a new session, and starting a session in another folder was refused the same way. The run carried on two ways: by relaying the next task to an idle child already working in that folder (`SendMessage`), and by running builders and verifiers as background subagents, each in its own worktree. Both kept the brief, the leaf rule and the separate verifier. The cost: subagents do not show in the sidebar for the person to open.

So: start every session the run will need for a wave in a turn the person's own message started, or plan from the outset for subagents and relays.
