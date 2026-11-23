# Why these rules

The reasons behind the rules in [`SKILL.md`](../SKILL.md), kept here so the procedure stays a
procedure.

## Why the skill blocks a little

Mature agent frameworks and hard experience agree: jumping to code on an underspecified task costs
far more than a few minutes of elicitation. So the skill asks its questions and shows its split
before writing files. The friction is the feature for anything non-trivial. The other side is real
too: a change finished in one sitting needs no task file.

## Why one fresh context window

A task that needs more context than one session holds is finished by an agent that has forgotten its
own early reading, or by a handoff that drops detail. Sizing to one fresh window keeps the agent's
whole understanding of the task in front of it from the first read to the acceptance run.

## Why vertical slices

A horizontal slice can only be verified once every sibling lands, so a defect in the first surfaces
at the end, when every slice is in flight. A tracer bullet is verifiable alone, so it fails alone.

## Why `touched_files` holds only existing paths

`validate.py --strict` reports a path that is not in the tree, and `--strict` is what a backlog gate
runs. A file to be created is therefore named in **Scope**, the only place the implementing agent can
read where it goes.

## Why every claim about the code is checked

Two real premise errors were caught by agents mid-batch after being written from a quick read: "the
regex already handles the anchor form", and "the Devanagari filtering lives in `clean()`". Both were
confident, and both were wrong. A vague task prompts a question; a confident error prompts
compliance.

## Why the id is the higher of the manifest and the scan

The shipped validator compares `.tasks/.scaffold.json` against the tree and reports every type it
has fallen below, so in a repository with a green backlog gate the manifest is current. But the
manifest is written by hand at closeout. Trusting a stale one hands out an id already taken, and the
duplicate-id error arrives only after the file exists and has been cross-referenced.

## Why the risk rule is deterministic

It is the rule `spec-plan-readiness` applies, quoted so the two cannot drift. "Touches more than one
module" is answerable from the `touched_files` list, not from how risky the work feels.
