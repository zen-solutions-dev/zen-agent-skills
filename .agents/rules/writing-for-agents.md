---
paths:
  - "**/rules/writing-for-agents.md"
---

# Zen writing-for-agents lens (edit freely)

This file is a **swappable module**, the companion to [`house-style.md`](house-style.md). The house
style governs how prose reads to a person. This lens governs how a document behaves when an agent
reads it: a `SKILL.md`, an `AGENTS.md` or `CLAUDE.md`, a reference file reached through a link. The
goal is predictability: the agent takes the same *process* on every run, even when the output
differs. It is topical, so the `paths` frontmatter keeps it out of every session; the skills that
write or revise documents for agents read it when they do.

## Pointers decide when material is reached

A **pointer** is anything always in the agent's context that names material outside it and the
condition for reaching it. A skill's `description` is a pointer. So is a line in `AGENTS.md` that
names a document. The wording of the pointer, not the quality of the target, decides how reliably
the agent gets there. When must-have material is being missed, sharpen the pointer first, and
inline the material only when sharpening fails.

- **Lead with the triggering word.** The first words of a description do the triggering.
- **One trigger per case.** Synonyms for one case are one case written twice; keep one.
- **Cut what the body already says.** A pointer names the case, the body does the work.

## Two budgets

- **Context budget**: what is loaded on every turn whether it fires or not. Every description and
  every always-loaded rule spends it. Spend it only on what the agent must reach unprompted.
- **Attention budget**: what the person has to remember exists. A skill only a person starts costs
  them a name to remember. Spend it where a person's judgement belongs in the loop.

## Where material sits

A document holds **steps** (what the agent does, in order) and **reference** (rules, definitions,
facts consulted on demand). Rank each piece by how soon the agent needs it:

1. A step in the file.
2. Reference in the file.
3. Reference in a separate file under `references/`, reached by a link.

Inline what every path through the skill needs; move what only some paths need behind a link. A
procedure says what to do. The incident that taught a rule, and the history of how it changed,
belong in a reference file or the repository's rationale, never between two steps. Keep a concept's
definition, rules and caveats under one heading rather than scattered.

**Sprawl** is the failure: a document too long even when every line is true. Attention thins over
the excess. The cure is the ladder above, not smaller type.

## Completion criteria

Every step ends on a condition that tells the agent it is done.

- **Clear**: the agent can tell done from not done. "Understanding reached" invites stopping early;
  "every open question has an answer or a named owner" does not. Sharpen the condition before
  restructuring anything.
- **Demanding**: the condition sets how much digging happens. "Every changed file accounted for"
  drives more work than "list the changes".

When a clear condition still gets rushed, hide the later steps across a real context boundary: a
subagent or a handoff. An inline step still sees what comes after it.

## Leading words and positive phrasing

A **leading word** is a compact concept the model already knows (tracer bullet, red, frontier,
blast radius, one-way door) used as a single repeated token. It anchors the same behaviour every
time it appears, and in a description it improves triggering. Prefer an existing word to a coined
one: a coined word has to be defined, an existing one arrives with its meaning. Collapse a phrase
restated at several sites ("fast, deterministic, cheap to run") into one word (*tight*).

State the behaviour you want. A prohibition puts the unwanted behaviour into context and can make
it more likely. Keep a prohibition only as a hard guardrail with no positive phrasing, and pair it
with the positive target.

## Pruning

- **One source of truth per meaning.** A rule restated in two skills drifts in one of them. Point
  at the owner instead.
- **The environment is a source of truth.** A document that restates a script's flags, a config
  file or a directory listing is a cache that goes stale. Record what the agent cannot find by
  looking: the unwritten convention, the reason, the trap.
- **The no-op test.** Does this sentence change behaviour compared with what the model does by
  default? If not, delete the whole sentence. Two readers who disagree about a no-op disagree about
  the default, and settle it by running the document. A word too weak to beat the default (*be
  thorough*) is a no-op; a stronger word (*relentless*) is the fix.
- **Sediment** is what accumulates when adding feels safe and removing feels risky. Prune on every
  edit, not in a separate pass nobody schedules.

## Write history, not the present

A document an agent reads later is a record of what was true when it was written, and it reads as
the present unless it says otherwise. A claim about a moving thing (a file's contents, a count, a
status, which branch holds what) stays honest only if it carries its own moment:

- **Date the claim.** "On 2026-11-24 `scripts/` held one checker per gate" can be re-checked; "the
  scripts directory holds one checker per gate" cannot be told apart from a stale one.
- **Cite the commit a code claim was true at.** A short hash or a tag pins what was read, so the next
  reader can diff from there instead of trusting the sentence.
- **Never write a bare "currently", "now" or "at the moment".** Each one is an undated claim wearing
  the present tense. Replace it with the date, or delete it when the sentence reads the same without.
- **Supersede, never rewrite.** When a dated claim stops being true, add the newer one with its own
  date and leave the old line, or move it to a history file. A silently rewritten record loses the
  evidence that anything changed.

This applies to anything kept across sessions: memory, a handoff, a report, a decision record. A
rule or a procedure is not a claim about the present and needs no date; the rule above about the
environment as a source of truth still decides what belongs in a document at all.

## Composition must load

A skill composes another when one of its steps depends on the other's discipline. Naming the
sibling is not enough: an agent that sees a skill's name in prose reads it as background and often
carries on from memory, so the sibling's rules never reach the run. Write each composing step as an
instruction to load:

- **Say read and follow, at the step that needs it.** "Read `../doc-revise/SKILL.md` now and follow it
  for this edit" loads; "this composes `doc-revise`" only mentions. The same holds
  for a lens: "apply the rubric in `review-quality.md`" before the step that uses it.
- **Keep it harness-neutral.** Reading the file works in every harness. Where a harness has its own
  loader (a skill tool, a slash command), name it in a labelled optional section, never in the step.
- **Load where the step is, not at the top.** A load instruction in the opening paragraph has decayed
  by the step that needs it; put it at that step, and keep the opening to a pointer.
- **A mention stays a mention.** A neighbour named only to say where a skill sits in a chain is not
  composed; leave it in backticks, with no load instruction and no link, so it creates no install
  edge.
- **A draft is loaded by name, guarded.** A shipped skill cannot link a draft sibling, because the
  link would install it, and a backticked name alone is only a mention. Compose a draft with exactly
  this form, at the step that needs it: a sentence that starts ``If `<name>` is installed, read and
  follow it``, then, in the same sentence, a fallback clause starting `; otherwise`. For example:
  ``If `research` is installed, read and follow it now; otherwise answer from the sources already in
  hand.`` The name stays in backticks, so it draws no install edge, and the fallback keeps the step
  whole when the draft is absent. `validate-skills.py` in the Zen Agent Skills repository recognises
  this form.

## Invocation

- A **model-invoked** skill keeps a model-facing description so the agent can reach it unprompted
  and other skills can compose it. It costs context budget on every turn. Use it for disciplines
  and lenses the agent should reach on its own: debugging, test design, review rubrics.
- A **user-invoked** skill is one a person starts by name: an orchestrator such as a batch run, a
  scaffold, or a router. In Claude Code, `disable-model-invocation: true` removes its description
  from the agent's context, so it costs no context budget; its description becomes a one-line
  summary written for the person. A harness without the feature treats it as model-invoked.

In this kit a skill declares the choice as `invocation: user` under `metadata`, never as a top-level
key: claude.ai and the Skills API reject any frontmatter key outside their six, and `metadata` is one
of the six. The Claude Code install paths render it as `disable-model-invocation: true` in the copy
they place. A skill that declares nothing is model-invoked.

Pick model-invoked only when the agent must reach the skill on its own, or another skill must.

## Checklist for a skill in this kit

- The description leads with the triggering word, is written in the third person, names one
  trigger per case, and stays under about 400 characters.
- The body stays under about 250 lines; detail, history and harness-specific mechanics live in
  `references/`. A body may run past that only when the excess is procedure every run needs (a
  step, a gate, the output contract) or the provenance footer, and the skill says so in one line.
  Moving a step or a gate behind a link to meet the number hides it from the run that needs it.
- A relative link to a sibling `SKILL.md` appears only where this skill genuinely composes that
  skill, because the link is also an install dependency. A neighbour is named in backticks.
- The autonomy rules are reached with one pointer line to `core.md`, not restated.
- Every dispatched subagent starts with a fresh context, not a fork of the parent, and is told it
  is a leaf that dispatches nothing further.
- A dispatch names its effort level where the harness has one: **medium** for an agent that builds,
  **high** for one that verifies or debugs. Verifying and debugging are where a shallow pass returns
  a confident wrong verdict, and building is where extra effort mostly buys extra scope.
- Every step ends on a clear, demanding completion criterion, on a line of its own beginning
  "Done when".
- A summary, verdict rule or opening promise that restates a step is re-read against that step
  whenever either is edited; prefer pointing at the step to restating it.
- Every composing step tells the agent to read and follow the sibling or lens at that step, not
  merely names it.
- A claim the skill writes into a record that outlives the session (memory, a report, a handoff)
  carries a date, and a code claim its commit; no bare "currently".

## Provenance

Adapted, in this kit's own words, from Matt Pocock's `writing-for-agents` skill. The two-loads
framing, the information ladder, completion criteria, leading words, the no-op test and the
invocation split are his; the checklist and the kit-specific rules are this repository's. "Write
history, not the present" is adapted from the memory rules of his `chief-of-staff` skill, and
"composition must load" from the reason his changelog gives for making cross-skill invocation an
explicit instruction (`feat-0093`, 2026-11-24).

```provenance
source: https://raw.githubusercontent.com/mattpocock/skills/main/skills/productivity/writing-for-agents/SKILL.md
author: Matt Pocock
license: MIT
retrieved: 2026-11-23
sha256: 551adca942227b44192edba88acd4e8db911f0121ce58ad16944ccf6a896a74a
note: fetched with urllib and digested with hashlib on the retrieved date, at 10,886 bytes. Adapted, not copied; this file is expected to differ.
```

```provenance
source: https://raw.githubusercontent.com/mattpocock/skills/main/skills/productivity/writing-for-agents/SKILL-MECHANICS.md
author: Matt Pocock
license: MIT
retrieved: 2026-11-23
sha256: c768e6307c7c10728c401c213f2c4ba71c542127eeb7ad2956aabd15a0fa0059
note: fetched with urllib and digested with hashlib on the retrieved date, at 2,629 bytes. Source of the invocation split.
```

```provenance
source: https://raw.githubusercontent.com/mattpocock/skills/main/skills/in-progress/chief-of-staff/SKILL.md
author: Matt Pocock
license: MIT
retrieved: 2026-11-24
sha256: 1f508d8ebbdbad8704bb24c5016094897a4ebbfe5804e370434b5e5fbeb59c4a
note: fetched with urllib and digested with hashlib on the retrieved date, at 4,470 bytes, identical to d653911. Source of "write history, not the present".
```

```provenance
source: https://raw.githubusercontent.com/mattpocock/skills/main/CHANGELOG.md
author: Matt Pocock
license: MIT
retrieved: 2026-11-24
sha256: 4428dd2711eb5e51ae8bca7a55a1144e3afd5805afb96c9480faa1081b77622e
note: fetched with urllib and digested with hashlib on the retrieved date, at 66,893 bytes. The entries for pull requests 878 and 880 are the source of "composition must load"; a changelog moves often, so expect drift here.
```
