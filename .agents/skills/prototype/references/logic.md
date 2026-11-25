# The logic branch

A logic prototype answers a question about **behaviour**: whether a state model, a set of
transitions or a data shape holds up once it is pushed through the cases that are hard to reason
about on paper. It is one self-contained page that anyone, a developer or not, opens and drives.

## 1. Put the question at the top

The page opens with the question from Step 1 of the skill, in a visible paragraph, not a code
comment, so a judge who opens it later knows what they are checking.

## 2. Write the logic as a pure module

The part that answers the question is a small module with no page in it: no DOM, no event handlers
reaching in, no I/O. The page calls it; it never calls the page. Pick the shape the question needs,
not the one easiest to wire:

| The question is about | Shape |
|---|---|
| Discrete events changing one value | A reducer: `(state, action) -> state` |
| Which actions are legal in which state | A state machine with named states and transitions |
| Transformations with no current state | A few pure functions over a plain data type |
| Something that truly owns ongoing state | A small object with a narrow method surface |

Keeping it pure is what lets the validated logic move into the real code later; the page around it
is thrown away.

## 3. Build the page around it

One file: plain HTML, CSS and script, everything inline, no framework, no build, no server, so it
opens by double-click and survives being sent around. Write every label in the **domain's words**
(the glossary's terms), not the code's. From top to bottom:

1. **The question** and one line on what the page lets you explore.
2. **The state**, as labelled fields rather than a raw dump, redrawn after every action, with what
   just changed marked.
3. **Free play**: one button per action, always available, in any order.
4. **Scenarios**, one per tab: a few plain sentences on the situation and what to watch, then the
   ordered buttons for its steps. Starting a scenario resets to a known state so it runs the same
   every time. Include the happy path, the awkward edge case, and an attempt at something that must
   be refused.

Keep it plain: readable type, spacing, one accent colour, nothing that competes with the state.

## 4. Hand it over and listen for the surprise

The useful moments are "that should not be possible" and "I expected something else": those are
defects in the idea, which is what the prototype exists to find. Add an action or a scenario when
the judge asks for one.

## What does not belong

- Tests, a real database, a framework, a bundler or a server.
- Generality for a case the question does not ask about.
- Logic tangled into the page: if the module touches the page, it can no longer be lifted out.
- The page in production. The module may be lifted; the page stays on the prototype branch.
