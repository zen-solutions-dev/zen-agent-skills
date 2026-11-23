# Red flags and rationalizations

Read on demand from [`systematic-debugging`](../SKILL.md) when you catch yourself guessing. Adapted
from the red flags and rationalizations in Jesse Vincent's `superpowers` `systematic-debugging`
(MIT); the provenance block is in the skill's own `## Provenance` section.

## Red flags

Every one of these is the same move, and the move is guessing. If you catch yourself here, you are
between steps 2 and 5 and you have skipped one, most often the red command.

- "It is probably X, let me just check whether changing X helps."
- "Quick fix now, work out why later."
- "Let me change these three things and rerun."
- "It passed that time, so it is fine."
- "I do not fully understand it, but this might work."
- "The reference is long, I will adapt the pattern from the parts I read."
- Reading code to build a theory before a red command exists.
- Naming a cause before running anything.
- Proposing a fix before the boundary is known.
- A hypothesis written after its trial.

## Common rationalizations

| Excuse | Reality |
|---|---|
| "This one is simple, the process is overkill." | Simple defects have causes too, and the process is short for them. It is long only when the defect is. |
| "It is urgent, there is no time to investigate." | Guess-and-check is slower than it feels, and it is the reason this is urgent twice. |
| "I will investigate properly after this one fix." | The first fix sets the premise every later one is written against. |
| "Reading the code told me what is wrong." | Reading tells you what the code says. Running tells you what it does. |
| "A red command is overhead; I can see the bug." | The red command is what every later trial runs. Without it each trial is a fresh guess. |
| "Two changes at once saves a round trip." | It costs the round trip anyway, because neither result attributes. |
| "It reproduced once, that is enough." | Once is a data point about one attempt. An intermittent defect needs a rate. |
| "The cause is obvious, the record is ceremony." | Then the record costs a minute. Write down when the answer arrived, and whether the procedure produced it. |

## Why the procedure says what it says

Several instructions in the skill were added after the skill was run on a real defect (`feat-0062`,
2026-08-29), and each closes a place where that run lost a trial:

- **The second source for a measurement** (step 1): the run formed a hypothesis from its own
  harness's timings, which turned out to be an artifact.
- **The knob before the rate** (step 2): the first two reproduction attempts failed because a writer
  was not held long enough, not because the defect was intermittent.
- **Probing the whole suspect region** (step 4): a probe covered three statements of a
  five-statement function and cleared it; the block was at the fifth.
- **A sufficient condition is not a cause** (step 5): the run's "confirming" trial raised a timeout,
  which ends any wait whatever is waiting, and a different single change fixed the same symptom.

The red-command phase itself (step 2) arrived later, with `feat-0077`, adapted from Matt Pocock's
`diagnosing-bugs`; the skill's provenance section records it.
