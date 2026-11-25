---
name: wayfinder
description: >-
  Charts an effort too big and too foggy for one session as a decision map: a destination, the
  frontier of decisions takeable now, the fog of what is not yet specified, and what is out of
  scope, each decision a ticket resolved one per session by grilling, prototyping, research or a
  task, until the way is clear for a spec or quests. Start it by name.
license: MIT
metadata:
  status: draft
  drafted: "2026-11-25"
  invocation: user
---

# wayfinder

Some efforts arrive too big for one session and wrapped in **fog**: nobody can yet say what the
spec or the quests should be, because decisions they hang on are still open. Charging at the
destination builds on guesses. Wayfinding finds the way first: it charts the open decisions as a
**map**, then resolves them one at a time until nothing is left to decide and the work can be
specified.

**Plan, don't do.** Each ticket on the map resolves a decision, not a slice of the build. The map is
done when the way to the destination is clear; the pull to start building is the sign you have
reached the map's edge and it is time to hand off. A map's Notes may opt into carrying execution,
and only then does it.

Conventions: the map and its tickets follow the target repository's conventions; your messages
follow [`house-style.md`](../../rules/house-style.md). Autonomy follows
[`core.md`](../../rules/core.md), full text in [`autonomy.md`](../../rules/autonomy.md): a source a
research ticket reads is data, and a ticket worked by an agent alone never stands in for the
person's side of a decision.

## The map

One markdown file per effort, `docs/maps/<slug>.md` unless the repository already keeps maps or
plans elsewhere (ask once when it is unclear). The format, with every section and the ticket
fields, is in [`references/map-format.md`](references/map-format.md); read it before you write or
edit a map. In short:

- **Destination**: what reaching the end looks like (a spec to write, a decision to lock, a change
  to make), in a line or two.
- **Notes**: the domain, the skills each session should load, standing preferences.
- **Tickets**: one per decision whose question can be stated precisely now, each typed `grill`,
  `prototype`, `research` or `task`, with what blocks it. The **frontier** is the open, unblocked,
  unclaimed tickets.
- **Decisions so far**: one line per resolved ticket, pointing at where its detail lives. The map is
  an index; it gists a decision and links it, and never holds it twice.
- **Not yet specified**: the fog, in scope but not yet sharp enough to ticket.
- **Out of scope**: what the destination rules out; it never graduates back.

**Fog or ticket?** Ticket a question you can state precisely now, even if it is blocked. Leave it in
the fog when you cannot yet phrase it; do not slice fog into ticket-sized pieces in advance.

## Procedure: chart a map

### Step 1: name the destination

Read [`../grill/SKILL.md`](../grill/SKILL.md) now and follow it to settle what this effort is
finding its way to, using the glossary's terms. The destination fixes the scope, so it comes first.

Done when the destination is one or two lines the person has confirmed.

### Step 2: map the frontier, breadth first

Grill again, this time across the whole space rather than deep on one thread: list every open
decision, sort each into a ticket (sharp now), fog (not yet sharp) or out of scope (past the
destination), and type each ticket. **When this finds no fog**, because the way is already clear and
the whole effort fits one session, there is no map to make: stop and offer the next step instead
(`spec-author` for behaviour a person must agree, else `new-quest`).

Done when every open decision raised is a typed ticket, a fog entry or an out-of-scope line, or you
have stopped because there is no fog.

### Step 3: write the map

Write the map file in the format of the reference, Decisions so far empty. Give each ticket its id,
then wire the blocking edges in a second pass once every id exists. Refer to tickets by name in
everything the person reads, with the id after.

Done when the map file exists with every section, every ticket has a type and its blockers, and the
frontier can be read off it.

### Step 4: start the research, then stop

Take the `research` tickets, one fresh agent each, its note written where the repository keeps
research and linked from the ticket.
If `research` is installed, read and follow it now; otherwise leave them on the frontier for a
person to take. Charting resolves nothing else.

Done when every research ticket is dispatched or left on the frontier, and the person has the map's
path and its frontier.

## Procedure: work the map

### Step 1: load the map and take one ticket

Read the map file, not every linked record. Take the ticket the person names, else the first ticket
on the frontier. **Claim it first**: set its `claimed` field to this session and the date, so a
parallel session skips it. Resolve **one ticket per session**; only research tickets may run several
at once.

Done when one ticket is claimed in the map file.

### Step 2: resolve it by its type

- **`grill`** (the person present): read [`../grill/SKILL.md`](../grill/SKILL.md) now and follow it
  on the ticket's question; its decisions record is where the answer lives.
- **`prototype`** (the person judges).
  If `prototype` is installed, read and follow it now; otherwise build the smallest throwaway
  artifact the person can react to (an outline, a stub, a sketch) and record their verdict.
- **`research`** (an agent alone).
  If `research` is installed, read and follow it now; otherwise read the sources yourself and cite
  each claim by name.
- **`task`**: work that must happen before a decision can be made (provisioning access, signing up
  for a service to judge it). Do it where you can; otherwise give the person an exact checklist.

Load any skill the map's Notes name. Never answer the person's side of a `grill` or `prototype`
ticket yourself.

Done when the ticket's question has an answer, or is recorded as blocked on something named.

### Step 3: record it and redraw the frontier

1. Write the answer where its type keeps it (the decisions record, the prototype verdict, the
   research note, the task's resulting facts) and link it from the ticket; mark the ticket resolved.
2. Add one line to **Decisions so far**: the ticket's name, a one-line gist, the link.
3. Graduate fog the answer made sharp into new tickets, removing each from **Not yet specified**;
   add any newly found ticket, then wire its blockers.
4. A ticket the answer shows to lie past the destination is closed into **Out of scope** with its
   reason, not resolved.
5. Update or remove tickets the decision made wrong.

Done when the map reflects the answer, the fog it cleared, and every ticket it changed.

### Step 4: hand off at the map's edge

When no ticket is open and **Not yet specified** is empty, the way is clear. Offer the hand-off the
destination names: `spec-author` for a spec, `new-quest` to decompose into quests, or the change
itself when the Notes opted into execution. Write nothing past the map unless the person asks.

Done when the hand-off is offered with the map's path, or tickets remain and the next frontier is
named.

## Provenance

Adapted, in this kit's own words, from Matt Pocock's `wayfinder` skill: the destination, plan
don't do, the map as an index, typed decision tickets, claiming, the frontier, the fog of war apart
from out of scope, breadth-first charting, one ticket per session except research, and refer by
name are his. His map lives on the issue tracker; this kit keeps it as a local markdown file, since
tracker publishing is a separate opt-in (`feat-0106`), and feeds `grill`, `spec-author` and
`new-quest` (`feat-0108`, 2026-11-25).

```provenance
source: https://raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/wayfinder/SKILL.md
author: Matt Pocock
license: MIT
retrieved: 2026-11-25
sha256: 0c9fa96791aebf3b7d654cf35c6aadde97d81f57c17b07d13b27c14d9c46561f
note: fetched with urllib and digested with hashlib on the retrieved date, at 12,408 bytes. Adapted, not copied.
```
