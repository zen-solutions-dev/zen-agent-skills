# house-review in Claude Code

Claude Code mechanics for [`house-review`](../SKILL.md). The Markdown review the skill describes
works in any harness; this file only maps it onto one host.

- **Structured findings.** Under a workflow that expects structured findings, emit the same
  validated findings through the host's findings tool (for example `ReportFindings`). The rubric,
  severities, the validate-before-reporting rule, the evidence gate, and each finding's evidence and
  signature are identical either way; only the output channel changes. A channel with no field for
  the quote or signature carries them inside the fields it has.
- **The built-in `/code-review`.** It is a fast bug hunt at a level the user picks. When the user
  wants it instead, pass the depth through as quick `low`, standard `medium`, deep `max`.
