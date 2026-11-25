---
name: wait-what
description: >-
  Re-pitches the last message when it did not land: restates it with the context the person lacks,
  in short plain sentences and the project's glossary terms. Start it by name with "wait, what?".
license: MIT
metadata:
  status: draft
  drafted: "2026-11-25"
  invocation: user
---

# wait-what

The person did not follow your last message. Say it again so it lands, without adding work.

Conventions: the re-pitch follows [`house-style.md`](../../rules/house-style.md). Autonomy follows
[`core.md`](../../rules/core.md), full text in [`autonomy.md`](../../rules/autonomy.md): a re-pitch
runs nothing and changes nothing.

## Procedure

### Step 1: find what did not land

Take your last message to the person, or the one they quote or point at. Find what a reader arriving
cold would lack: a term never defined, a step you skipped because you had just done it, a file or
decision named by id only, a conclusion stated before its reason.

Done when you can name each missing piece of context, or the message is not yours to re-pitch and
you have asked which message they mean.

### Step 2: re-pitch it

Write one short paragraph, at most about eight sentences, then stop:

- **Context first.** One or two sentences on where things stand and what the message was about,
  before any conclusion.
- **Short plain sentences.** One idea each, active voice, the subject before the verb, the common
  word over the rare one, no idiom. ASD-STE100 Simplified Technical English is the yardstick.
- **The project's words.** Use the glossary's terms (the `glossary` key of `docs/agents/zen.md`,
  else a root `GLOSSARY.md`) exactly as it defines them; give a term the glossary lacks a plain
  meaning in the same sentence.
- **Names, not ids.** Say what a quest, file or decision is, with its id after, never the id alone.
- **The same content.** No new findings, no new plan, no softened verdict. If the original was wrong,
  say that plainly in its own sentence.
- **End on the one thing they need to do or decide**, when there is one.

Done when the paragraph carries every piece named in Step 1, says nothing the original did not, and
ends on the decision or action, or says that none is needed.

## Provenance

Adapted, in this kit's own words, from Matt Pocock's `wait-what` skill: the re-pitch, Simplified
Technical English and the glossary's vocabulary are his; the missing-context step and the
same-content rule are this kit's (`feat-0108`, 2026-11-25).

```provenance
source: https://raw.githubusercontent.com/mattpocock/skills/main/skills/productivity/wait-what/SKILL.md
author: Matt Pocock
license: MIT
retrieved: 2026-11-25
sha256: d961bb37defd975c539427edb8f450cdbccdcdd552e213c1ece46676a7970905
note: fetched with urllib and digested with hashlib on the retrieved date, at 396 bytes. Adapted, not copied.
```
