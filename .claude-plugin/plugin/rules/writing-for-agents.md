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
- Every step ends on a clear, demanding completion criterion, on a line of its own beginning
  "Done when".

## Provenance

Adapted, in this kit's own words, from Matt Pocock's `writing-for-agents` skill. The two-loads
framing, the information ladder, completion criteria, leading words, the no-op test and the
invocation split are his; the checklist and the kit-specific rules are this repository's.

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
