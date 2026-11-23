# Deep-module vocabulary

Use these words exactly in every candidate, card and design. Consistent words are the point: a
report that says "component" in one card and "module" in the next makes the reader wonder whether
they are different things. Ousterhout's *A Philosophy of Software Design* is the source of the
deep-module idea; Michael Feathers' *Working Effectively with Legacy Code* is the source of "seam".

## Terms

| Term | Meaning | Say this instead of |
|---|---|---|
| **Module** | Anything with an interface and an implementation, at any scale: a function, a class, a package, a slice across tiers. | unit, component, service |
| **Interface** | Everything a caller must know to use the module correctly: the signature, and also its invariants, ordering rules, error modes, required configuration and performance. | API, signature |
| **Implementation** | The code inside a module. | |
| **Depth** | Leverage at the interface: how much behaviour a caller or a test reaches per unit of interface it has to learn. **Deep**: much behaviour, small interface. **Shallow**: an interface nearly as complex as what it hides. | |
| **Seam** | The place a module's interface lives, where behaviour can change without editing that place. Where to put a seam is its own decision. | boundary |
| **Adapter** | A concrete thing that fills an interface at a seam. It names a role, not a size. | |
| **Leverage** | What callers gain from depth: one implementation paying back across many call sites and tests. | |
| **Locality** | What maintainers gain from depth: change, bugs and verification concentrate in one place. | |

## Principles

- **Depth belongs to the interface.** A deep module may be built from small internal parts; they
  are just not part of its interface. Internal seams, used by its own tests, are fine.
- **The deletion test.** Ask what the callers would have to write if the module were gone. If they
  would write almost nothing, it was passing calls through; if its complexity would land on every
  caller, the module was earning its place.
- **Tests stand where callers stand.** A test uses the module through the same entry points its
  callers do. When a test has to reach behind them, the module's shape is wrong, not the test.
- **One adapter is a hypothetical seam; two make it real.** Introduce a seam only when something
  actually varies across it, usually production and test.
- **Measure depth by leverage, not by line ratio.** Counting implementation lines against interface
  lines rewards padding.

## Dependency categories

Classify a candidate's dependencies before proposing the deepened shape; the category decides how
the deepened module is tested.

| Category | What it is | How the deepened module is tested |
|---|---|---|
| **In-process** | Pure computation or in-memory state, no I/O. | Fold the shallow modules together and test the result at its own entry points; nothing needs swapping out. |
| **Local stand-in** | A dependency with a local substitute (an embedded database, an in-memory filesystem). | Run the stand-in in the test suite; the seam stays internal. |
| **Owned remote** | Your own service across a network. | A port at the seam: an HTTP or queue adapter in production, an in-memory one in tests. |
| **Third-party** | A service you do not control. | The dependency is injected as a port; tests use a fake adapter. |

## Testing after a deepening: replace, do not layer

Write the new tests at the deepened module's interface, asserting observable outcomes. The old tests
on the shallow modules it absorbed become redundant once the new ones exist; delete them. A test that
has to change when only the implementation changes was testing past the interface.

## Phrasing that fits

- "The order-intake module is shallow: its interface nearly matches its implementation."
- "Discount rules are spread over three callers; none of them owns pricing."
- "One entry point for pricing would give the tests one place to stand."
- "Two adapters justify the seam: HTTP in production, in-memory in tests."

Wins are named in these terms ("locality: bugs concentrate in one module", "leverage: one interface,
eight call sites"), never as "cleaner" or "easier to maintain", which say nothing checkable.

## Provenance

The deletion test, the dependency categories and the reporting vocabulary are adapted, in this kit's
own words, from Matt Pocock's `codebase-design` and `improve-codebase-architecture` skills. The same
upstream files are recorded in [`../SKILL.md`](../SKILL.md); these blocks pin what this file adapts.

```provenance
source: https://raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/codebase-design/SKILL.md
author: Matt Pocock
license: MIT
retrieved: 2026-11-23
sha256: 2c20617f87ec8af6a434859f381b2f061a69b530444e74eb39e78bb016a6d1e2
note: the deletion test and the interface-as-test-surface principle, reworded after the 2026-11 verification (F4) found two sentences too close.
```

```provenance
source: https://raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/codebase-design/DEEPENING.md
author: Matt Pocock
license: MIT
retrieved: 2026-11-23
sha256: f3dd099ce99289bd213914d8ee3e2429b78309c3957ca4583f7659551b1d53c1
note: the dependency categories and how a deepened module is tested.
```

```provenance
source: https://raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/improve-codebase-architecture/HTML-REPORT.md
author: Matt Pocock
license: MIT
retrieved: 2026-11-23
sha256: 581e8bb5a521e46bbda8ca7e19b15948bed882187108092ebb90c62513b77528
note: the idea of naming wins in checkable terms; the example phrasings are this kit's own.
```
