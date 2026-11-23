# Glossary format

The default shape for a glossary this skill creates. When the repository already has a glossary in
another shape, keep that shape and use these rules only for the content.

## Shape

```markdown
# <Context name>

<One or two sentences: what this part of the system is and why it exists.>

## Language

**Order**:
A customer's request for one or more products, accepted at checkout.
_Avoid_: purchase, transaction

**Cancellation**:
The withdrawal of a whole Order before it ships. A partial withdrawal is a Refund.
_Avoid_: void, abort
```

## Rules

- **Pick one word.** When several words name a concept, choose the best and list the rest under
  `_Avoid_`.
- **Define what it is**, not what it does, in one or two sentences.
- **Domain terms only.** A concept specific to this project belongs; a general programming concept
  (timeout, cache, retry, error type) does not, however often the code uses it.
- **State the boundary** when two terms sit next to each other, as `Cancellation` does above.
- **Group under subheadings** once natural clusters appear. A flat list is fine until then.
- **No implementation detail.** File names, class names, and decisions belong in the code and the
  decision records.

## More than one context

When the repository has separate bounded contexts that use words differently, keep one glossary per
context beside its code, and a map file at the root that lists each context, where its glossary
lives, and how the contexts relate (who emits what, which identifiers are shared). Decide which
context a term belongs to before writing it; when that is unclear, ask.

## Provenance

```provenance
source: https://raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/domain-modeling/GLOSSARY-FORMAT.md
author: Matt Pocock
license: MIT
retrieved: 2026-11-23
sha256: 21dcc40cdec8e151a829b98ab1517c1867bc444e3665134a98c6983411996801
note: fetched with urllib and digested with hashlib on the retrieved date, at 2,300 bytes. Adapted in this kit's words; the boundary rule is this kit's.
```
