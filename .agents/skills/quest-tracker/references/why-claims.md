# Why the tracker works the way it does

The reasons behind four of `quest-tracker`'s rules, moved out of the skill body
(`feat-0094`) because a run needs the rules, not their history.

- **Why claims rather than ticks.** The page is read by people as a record of checked work. A tick
  written by the agent that did the work is that agent verifying itself, and it carries no evidence a
  person could check. A claim keeps the evidence, and leaves the tick to someone else.
- **Why a claim records lines, not just the step.** A person verifying a claim sees which lines the
  agent says it did, and "Verify and tick" ticks exactly those, so a line no one did stays open.
- **Why every tick names what it rests on.** A tick by hand may rest on a person's own look, or on
  someone's word in a chat, and the page cannot tell which, so it says only what it has on record.
  The mark is how a reader of the page, or of the season log copied into the docs, tells a checked
  command from a remembered one.
- **Why the script refuses rather than warns.** A failed command is not a passed check, and a field
  that looks like a secret would reach the shared database before the page hid it. Both are cheaper
  to stop before the write than to clean up after it.
