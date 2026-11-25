# orchestrate in Claude Code cloud sessions

Optional, and only for Claude Code on the web. A child can be a separate cloud session, and the
remote-session tools carry the transport:

- `create_session` starts a child with its brief as the prompt; `send_message` is how a child
  reports back and how you reply to it.
- `list_events` overflows without a tight filter: pass `kinds` (for example `["result"]`) and a
  small `limit`, and use it only to check that a child is alive. The report is the evidence.
- `send_later` schedules the fallback check-in.
- A worker restart can drop a branch's upstream tracking and leave a landing unpushed: Step 5's
  push-and-check rule is the guard. A session clone is often single-branch and shallow, so after
  cloning add a fetch refspec for the integration prefix (for example
  `git config --add remote.origin.fetch '+refs/heads/zen/*:refs/remotes/origin/zen/*'`), and after
  any restart confirm what the remote holds with `git ls-remote origin` before trusting a stop
  hook's "no remote branch".
- Some remote actions are refused through the session's proxy while pushing works: on 2026-11-24 a
  branch delete was refused both by `git push --delete` and by the REST API (HTTP 403). Step 1's
  probe finds this at the start of a run.
- `send_message` reaches a child during its turn, and a child can report before it reads the
  message. Step 4's acknowledgement rule is the guard.
- A cloud environment's network policy can refuse a host. Probe from the environment the child will
  run in; a refusal can clear after a worker restart, and some sites stop automated clients at a bot
  check, which is recorded as unreachable and never worked around.
