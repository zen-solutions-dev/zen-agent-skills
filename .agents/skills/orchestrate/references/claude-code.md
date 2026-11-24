# orchestrate in Claude Code cloud sessions

Optional, and only for Claude Code on the web. A child can be a separate cloud session, and the
remote-session tools carry the transport:

- `create_session` starts a child with its brief as the prompt; `send_message` is how a child
  reports back and how you reply to it.
- `list_events` overflows without a tight filter: pass `kinds` (for example `["result"]`) and a
  small `limit`, and use it only to check that a child is alive. The report is the evidence.
- `send_later` schedules the fallback check-in.
- A worker restart can drop a branch's upstream tracking and leave a landing unpushed: Step 5's
  push-and-check rule is the guard.
- A cloud environment's network policy can refuse a host. Probe from the environment the child will
  run in; a refusal can clear after a worker restart, and some sites stop automated clients at a bot
  check, which is recorded as unreachable and never worked around.
