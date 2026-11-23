# Decision record format

The default shape for a decision record (ADR) this skill creates, used only when the repository has
no format of its own.

## Location and numbering

`docs/adr/NNNN-<slug>.md`, numbered one past the highest existing record, four digits. Create the
directory with the first record, never before.

## Shape

```markdown
# <Short title of the decision>

<One to three sentences: the context, what was decided, and why.>
```

That is a complete record. Its value is that the decision and its reason are written down, not that
sections are filled. Add any of these only when it carries something a reader needs:

- **Status** frontmatter: `proposed`, `accepted`, `deprecated`, or `superseded by NNNN`, once a
  decision has been revisited.
- **Considered options**: when a rejected alternative will otherwise be proposed again.
- **Consequences**: when a downstream effect is not obvious.

## What tends to earn a record

All three tests in the skill still apply; these are the kinds of decision that usually pass them.

- The architecture's shape: a monorepo, an event-sourced write model.
- How contexts talk to each other: events rather than synchronous calls.
- A technology with lock-in: the database, the message bus, the auth provider.
- A boundary or a scope "no": which context owns customer data, what the product will not do.
- A deliberate departure from the obvious path, which stops the next person "fixing" it.
- A constraint the code cannot show: a compliance rule, a partner's latency contract.

## Provenance

```provenance
source: https://raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/domain-modeling/ADR-FORMAT.md
author: Matt Pocock
license: MIT
retrieved: 2026-11-23
sha256: 944c92aa790e8fbdc9199640b170979abb8a34ba8d0fe18c2a01a63bce140ca0
note: fetched with urllib and digested with hashlib on the retrieved date, at 2,733 bytes. Adapted in this kit's words.
```
