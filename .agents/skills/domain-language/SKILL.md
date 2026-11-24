---
name: domain-language
description: >-
  Keeps a project's shared language: adds settled terms to its glossary and records a decision as
  an ADR only when it is hard to reverse, surprising, and a real trade-off. Use when a term is
  settled or contested, when writing or editing GLOSSARY.md or an ADR, or when grill closes with
  new terms. Reports a glossary-versus-code mismatch; never renames code.
license: MIT
---

# domain-language

Keep the target repository's **ubiquitous language**: one word per concept, written down the moment
it is settled, so the next session starts from it instead of re-learning the jargon. Keep its
**decision records** too, so a settled, expensive argument is not reopened by someone who never saw
it.

This skill writes into the target repository, so the files it writes follow **that repository's**
conventions (its `AGENTS.md`, or whatever it uses instead). This kit's house style governs only your
own report.

## When to use

- A grilling session closes with terms in its decisions record.
- The person or the code uses one word for two things, or two words for one thing.
- Someone asks to write or edit the glossary, or to record a decision.

Reading the glossary for vocabulary is not this skill: any skill can do that. This skill is for
changing the language.

## Procedure

### 1. Find what exists

Look before creating anything. When the repository has `docs/agents/zen.md`, its `glossary` and
`adr_dir` keys name both places (`none` means the repository has none yet); use them and say so. When its block does not parse or names a newer `config_version`, use none of it, discover instead, and say that `python .tasks/validate.py` shows why; a configured path that does not exist is discovered instead too, and said.
Otherwise discover them, and say that you did. The glossary may be `GLOSSARY.md`, `docs/glossary.md`, a
"Terminology" section of a README or `AGENTS.md`, or a glossary per bounded context with a map file
at the root. Decision records may be `docs/adr/`, `docs/decisions/`, `adr/`, a numbered series
under another name, or no directory at all: many repositories record decisions in each task file's
Decisions section and keep the reasoning in a rationale directory (`docs/rationale/`). Use what you
find, in its format; that convention is where step 4 writes.

Done when you can name the glossary file and where decisions are recorded, or state that each does
not exist yet.

### 2. Settle each term

For each candidate term:

- **Challenge it against the glossary.** If the glossary already defines the word differently, ask
  which meaning holds. If it defines the same concept under another word, ask which word wins.
- **Sharpen fuzzy words.** An overloaded word ("account", "job", "event") gets a precise term per
  meaning, each with its boundary stated.
- **Probe with a concrete case.** Invent the edge case that forces the boundary: "a refund on half
  an order: is that a Cancellation?"
- **Test it in sentences.** Before settling a name, write three or four real sentences the
  project will say with it (from a spec, a task, a log line, a conversation with a user) and put
  them in a table beside each candidate name. The name that reads naturally in every sentence, and
  misleads in none, wins; show the table to the person with your recommendation. A glossary is the
  data model in words, so a name that fails a sentence fails in the code too.

  | Sentence | `Refund` | `Reversal` |
  |---|---|---|
  | "A ___ on half an order leaves the rest shipped." | reads | misleads: sounds like the whole order |
  | "The ___ failed at the bank." | reads | reads |

- **Check the code and the plans.** Grep for the term and its synonyms in the code, and in the task
  files and specs, where a term is used before any code exists. When either names the concept
  differently from the glossary, or uses the glossary's word for something else, record a
  **finding**: the term, the glossary's meaning, the other name, and where. Never rename code or
  rewrite a plan; that is a separate task the person may choose to write.

Done when every candidate is settled with the person, deferred with a reason, or dropped as a
general programming word that does not belong (timeouts, retries, and error types are not domain
terms).

### 3. Write the glossary

Write each settled term as it lands, not in a batch at the end. When no glossary exists, create one
only now that the first term is settled, and ask the person where it should live first, as a
question with a recommended answer: `GLOSSARY.md` at the root, unless step 1 found a convention that
says otherwise. A new file at the root is the person's decision, not a default to take in silence. Format: [references/glossary-format.md](references/glossary-format.md).

A glossary holds definitions only. Implementation detail, decisions, and to-do items go elsewhere.

Done when every settled term is in the glossary in the repository's format.

### 4. Earn an ADR, or do not write one

Offer a decision record only when the decision meets **all three** tests:

1. **Hard to reverse**: changing course later costs real work.
2. **Surprising without context**: a reader of the code would ask why it was done this way.
3. **A real trade-off**: there were genuine alternatives, and one was chosen for stated reasons.

Missing any one, skip it: an easy reversal will simply be reversed, an unsurprising choice needs no
defence, and a choice with no alternative has nothing to record. When one is earned and the person
agrees, write it where step 1 found decisions recorded. When that is a record directory, create it
only now if it does not exist, numbered after the highest existing record; when the repository
records decisions in task files, write it as a Decisions entry in the task that carries the work,
and create no record directory. Format: [references/adr-format.md](references/adr-format.md).

Done when each candidate decision is recorded or explicitly judged not to earn a record.

### 5. Report

List the terms added or changed, the records written, the terms deferred, and every
glossary-versus-code or glossary-versus-plan finding with its location. An empty findings list means
you grepped and found none; say what you grepped for, and where.

When this run created the glossary, nothing points at it yet, and a glossary no session reads does
not do its job. Offer one line for the repository's agent-instructions file (`AGENTS.md`, or what it
uses instead) that tells an agent to read the glossary before naming things. Offer it; that file is
the person's.

Done when every term touched in this run, every record written or declined, and every finding
appears in the report, each finding with a file and line, and a newly created glossary has its
pointer line offered.

## Conventions

Your report follows the house style ([`house-style.md`](../../rules/house-style.md)). What you may
do with what you read follows [`core.md`](../../rules/core.md) (full text:
[`autonomy.md`](../../rules/autonomy.md)); a renamed symbol is outside every scope this skill has
(`A2`).

## Provenance

Adapted, in this kit's own words, from Matt Pocock's `domain-modeling` skill and its two format
files: lazy creation, challenging terms against the glossary and the code, definitions-only
glossaries, and the three-part test for an ADR are his. Finding an existing convention first, the
finding-not-rename rule, and the report are this kit's.

```provenance
source: https://raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/domain-modeling/SKILL.md
author: Matt Pocock
license: MIT
retrieved: 2026-11-23
sha256: 7b925d7b1e341a2eeae33ad68a8a8c0ab889a38ddd22a7598e4c240e5a7556a3
note: fetched with urllib and digested with hashlib on the retrieved date, at 3,346 bytes. Adapted, not copied.
```
