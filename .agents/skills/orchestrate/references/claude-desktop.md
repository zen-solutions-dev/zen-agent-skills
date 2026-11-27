# orchestrate in the Claude desktop app

Optional, and only when the orchestrating session runs in the Claude desktop app on the person's
computer.

- **A turn the app started because a child session finished cannot start a session**, and neither
  can a question answered inside such a turn; starting a session in another folder is refused the
  same way. Start every session a wave needs in a turn the person's own message started, or plan
  the wave for the two routes below from the outset.
- **Relay the next task to an idle child already working in that folder**, through the app's
  message tool. The relay carries a full brief (Step 2), and Step 4's acknowledgement rule applies.
- **Run builders and verifiers as background subagents**, each fresh, a leaf, and in its own
  worktree, with the same brief a session would get and a verifier that is neither the builder nor
  you (`A7`). A subagent does not show in the app's sidebar, so name each one and its branch in the
  relay to the person.

Seen in round 3 (2026-11-25 to 2026-11-26); the run is in [`first-run.md`](first-run.md).
