# The map format

A map is one markdown file. The sections below appear in this order; a section with nothing in it
keeps its heading and says "none yet".

```markdown
# <Effort name>: map

Charted <YYYY-MM-DD> by <who>. Status: charting | working | way clear | abandoned.

## Destination

<One or two lines: the spec, decision or change this map finds its way to.>

## Notes

<The domain; the skills every session loads; standing preferences; whether this map carries
execution (default: it does not).>

## Tickets

### W-01: <the ticket's name, a short question>

- type: grill | prototype | research | task
- blocked by: [W-03] | none
- claimed: <session, YYYY-MM-DD> | no
- status: open | resolved | out of scope
- answer: <link to the record that holds it> | none yet

<The question, in a few sentences: what must be decided or found, and why it matters to the
destination.>

## Decisions so far

- [W-02: <name>](<link>): <one-line gist of the answer>

## Not yet specified

- <A suspected question or an area to revisit, as loosely as the view allows.>

## Out of scope

- <What is ruled out, and why>, closed from [W-05](<link>) when it came from a ticket.
```

## Rules

- **Ids** are `W-NN`, unique within the map, never reused. Everything a person reads names the ticket
  first and gives the id after it.
- **The frontier** is every ticket with `status: open`, `claimed: no`, and every ticket in its
  `blocked by` resolved. A reader finds it by reading the Tickets section, so keep each ticket's fields
  current.
- **A ticket holds the question, never the answer.** The answer lives in its own record (a grilling's
  decisions record, a prototype verdict on its quest, a research note) and the ticket links it.
- **Dates** on the chart line, every claim and every Decisions so far entry that names when it was
  settled, so a later session can tell a stale map from a live one.
- **A resolved ticket stays** in Tickets with its status, so the route walked stays readable;
  Decisions so far is its index.
