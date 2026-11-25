---
name: prototype
description: >-
  Prototypes to answer one design question that talk cannot settle: throwaway code on a logic branch
  (a self-contained page that drives a pure state model through hard cases) or a UI branch (several
  different variants on one existing route), captured on a throwaway branch with the verdict
  recorded on the quest. Use when "would this model hold?" or "what should this look like?" stalls.
license: MIT
metadata:
  status: draft
  drafted: "2026-11-25"
---

# prototype

A prototype is **throwaway code that answers one question**. It earns its cost when a decision has
stalled in talk: a state model that looks right on paper, a screen nobody can picture. The answer is
the deliverable; the code is evidence for it and is not merged.

Conventions: the prototype's code follows the target repository's conventions where it touches them,
and is marked throwaway everywhere; your report follows [`house-style.md`](../../rules/house-style.md).
Autonomy follows [`core.md`](../../rules/core.md), full text in
[`autonomy.md`](../../rules/autonomy.md): the throwaway branch is your own, and pushing it, like any
remote action, follows the repository's rules and the person's say.

## When not to use this

- The question can be settled by reading the code, a document or a source. Read it; a `grill`
  session looks facts up before it asks.
- The answer is already known and only needs building. Build it, test-first.

## Procedure

### Step 1: state the question

Write the question in one sentence, and what answer would change the plan: "Does the retry state
model reach a terminal state when the network drops twice mid-upload? If not, the quest needs a
cancel step." Name who will judge the answer (the person, a domain expert, a reviewer) and whether
they are present.

Done when the question and the decision it feeds are each one sentence, and the judge is named.

### Step 2: pick the branch

- **Logic**: the question is about behaviour, state, transitions or data shape. Read
  [`references/logic.md`](references/logic.md) now and follow it.
- **UI**: the question is about how something looks or is laid out. Read
  [`references/ui.md`](references/ui.md) now and follow it.

When the question is truly both, prototype the logic first: a layout built on a wrong model is
judged on the wrong thing. When the judge is absent and the question is ambiguous, choose by the
code nearest the question (a module: logic; a page or component: UI) and write that assumption at
the top of the prototype.

Done when one branch is chosen and its reference has been read.

### Step 3: build it, throwaway from the first line

Rules for both branches:

1. **Marked.** Put it beside the code it informs, named so nobody mistakes it for production
   (`prototype` in the file or route name), following the project's existing layout.
2. **One command to run.** The person starts it with one command from the project's task runner, or
   by opening one file.
3. **No persistence** unless persistence is the question; then a scratch store whose name says to
   wipe it.
4. **No polish.** No tests, no error handling beyond what keeps it running, no abstraction for later.
5. **State on screen.** After every action or variant switch, show the full state that matters, so
   the judge sees what changed.

Done when the prototype runs from one command, shows its state, and every file it adds is named as
a prototype.

### Step 4: get the verdict

Run it with the judge, or hand it over with the question at the top. Record what they did, what
surprised them, and the **verdict**: the answer to the Step 1 question, in a sentence, and which part
of the prototype showed it. "Not answered" is a verdict too, with what a second prototype would need.

Done when the verdict is one sentence tied to the Step 1 question, with the evidence that produced
it.

### Step 5: capture it and record the verdict

1. **Capture the prototype** as evidence: commit it on a throwaway branch, `prototype/<slug>`, cut
   from where the work started. It is never merged. Push it only where the repository's rules and
   the person allow; otherwise say that it is local.
2. **Record the verdict on the quest** the question came from, in its Decisions section (or on its
   linked issue): the question, the verdict, and a pointer to the branch and commit.
3. **Fold the decision in, not the code.** The validated decision goes into the quest, the spec or
   the grilling's decisions record; production code is written fresh, test-first, and may lift the
   prototype's pure module when the logic branch produced one.
4. **Remove it from the working branch**, so the main line keeps only the decision.

Done when the prototype is committed on `prototype/<slug>` (pushed or stated local), the verdict and
its pointer are on the quest or issue, and the working branch holds none of the prototype's files.

## Provenance

Adapted, in this kit's own words, from Matt Pocock's `prototype` skill and its two branch files: the
logic and UI branches, the pure liftable module, the guided scenarios, the variants switched on one
existing route, the five rules for both branches, and capturing the prototype on a throwaway branch
with its verdict are his. The decision-it-feeds sentence, the logic-first rule for a mixed question
and recording the verdict in the quest's Decisions section are this kit's (`feat-0108`, 2026-11-25).

```provenance
source: https://raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/prototype/SKILL.md
author: Matt Pocock
license: MIT
retrieved: 2026-11-25
sha256: 714de632d116bb73f65cdb5a882db15b9369a6713b9a47c0fad827848f0bfbe3
note: fetched with urllib and digested with hashlib on the retrieved date, at 2,931 bytes. Adapted, not copied.
```

```provenance
source: https://raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/prototype/LOGIC.md
author: Matt Pocock
license: MIT
retrieved: 2026-11-25
sha256: f61c7d249e786a79ef289018901c348271e1798dd0b0bc5607b5c6f4d4a01ab9
note: fetched with urllib and digested with hashlib on the retrieved date, at 6,036 bytes. Source of references/logic.md; adapted, not copied.
```

```provenance
source: https://raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/prototype/UI.md
author: Matt Pocock
license: MIT
retrieved: 2026-11-25
sha256: 723211e878acbc7b6ff09755263f3295cde724ba902ff0064da41eed51d45ad3
note: fetched with urllib and digested with hashlib on the retrieved date, at 6,913 bytes. Source of references/ui.md; adapted, not copied.
```
