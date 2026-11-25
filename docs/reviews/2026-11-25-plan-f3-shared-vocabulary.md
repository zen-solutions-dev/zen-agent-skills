# Plan F3: one shared vocabulary across kit, website and courses

Status: **plan only, nothing built.** Written 2026-11-25 for quest [`chore-0112`](../../.quests/chore-0112-plan-the-shared-vocabulary.md), Phase 3 of the [round 2 plan](2026-11-25-marjana-r2-plan.md). Decision F3 in [the decision record](2026-11-25-marjana-decisions.md): yes. The website (`zen-solutions-site`) is out of scope this round ([handoff](2026-11-25-round-2-handoff.md), section 3, and G9: "After the skills round"); this plan touches only what this repository would export.

## Goal

One vocabulary, defined once, that the kit's skills, the Zen Solutions website and the courses all use: the same word for the same idea everywhere, each term with a stable address a page or an agent can link. It seeds the website's knowledge graph: terms are the nodes, "see also" and "avoid" are the edges.

The source is Matt Pocock on NetworkChuck's podcast ([extraction](2026-11-25-podcast-extraction.md), section 2, "Resources and ecosystem"): his AI coding dictionary is "a graph of every term he uses with definitions", "like the glossary ... but applied to AI coding", and all his resources share one language (~48:39 to ~49:14). Section 5 item 26: "The kit has no glossary of its own terms (door, blast radius, leaf, smart zone). A kit-level dictionary would serve both people and agents." Section 3, "Ubiquitous language": "If you use a shared language, it just feels like the agent is in your brain" (~22:47).

## What exists to build on

- [`GLOSSARY.md`](../../GLOSSARY.md), checked 2026-11-25. Sections: Evaluation (case, arm, baseline, grader, discriminating), Work and delegation (orchestrator, child session, integration branch, frontier, AFK, human in the loop, one-way door, two-way door), Quests (campaign, quest chain, quest, side quest), Rarity (white, green, blue, purple, gold), Setup (fact, role). Each entry is a bold term, a definition, and usually an `_Avoid_:` line naming the words not to use.
- The `domain-language` skill keeps that file: it adds a term when it is settled and reports a mismatch between glossary and code.
- The rarity ladder is already copied word for word into `research` and `sitrep`, and `GLOSSARY.md` says "a change is made in all three". That is a shared vocabulary kept by hand, and the first place an export would pay for itself.
- The `teach` draft, which builds lessons a course could reuse. Matt chose skill vocabulary that points "out to books and ... well-known methodologies" so it can be taught (extraction, Stage 13, ~1:09:40).
- The deep-module lens ([`deep-modules.md`](../../.agents/rules/deep-modules.md)): terms borrowed from John Ousterhout's *A Philosophy of Software Design*, not yet in the glossary.

## Gaps found while writing this

- Terms the kit uses that the glossary lacks: blast radius, leaf, smart zone and dumb zone (credited to Dex Horthy, extraction item 35), deep module, ratchet, dogfood record, draft.
- The close-round nit (h) in the [round 2 plan](2026-11-25-marjana-r2-plan.md): the rarity entries lost the per-term `_Avoid_:` format. An export needs one format.
- R2-8: `quest-tracker` uses "quest" and "quest chain" for steps on its page, a second meaning of the same words.

## Smallest first slice

1. **Fix the format**: every entry a bold term, a definition, an optional `_Avoid_:`, and an optional `_See also_:` naming other terms (the graph's edges). One quest, inside this repository, with `domain-language`.
2. **A standard-library export script**, `scripts/export-glossary.py` or similar, that reads `GLOSSARY.md` and writes JSON: one object per term (a slug id, the term, section, definition, avoid list, see-also list). Pinned by a test; run by `run-checks.py` so a malformed entry fails. No website change.
3. Add the missing kit terms above, one decision each.
4. Later, outside this repository: the website reads the export. That is G9's session.

## Risks and one-way doors

- **Term addresses are a one-way door once published.** When the website links `/glossary/two-way-door`, renaming the slug breaks every link outside the kit. Decide the slug rule before the first export leaves this repository.
- **Two sources of truth.** If the website or a course edits a definition locally, the vocabulary forks. The export must flow one way, from this repository out.
- **Borrowed terms.** Defining another author's term (Ousterhout's deep module, Evans's ubiquitous language, Matt's software factory) in the kit's words needs a named source per entry, per the house style.
- **Scope creep into a dictionary of everything.** The glossary holds terms the kit decided; it is not an encyclopedia.

## Rough size

Small to medium for this repository: the format fix and the export script with its test (two quests), then term additions (one quest per batch). The website and course side is G9's.

## Questions for the maintainer

1. **Where should the one shared vocabulary be written?** (a) In this kit's `GLOSSARY.md`, exported to the website and courses, recommended: it already exists and `domain-language` keeps it; (b) in a separate vocabulary repository that the kit, the website and the courses all read; (c) on the website, with the kit copying from it.
2. **Which terms belong in the shared vocabulary?** (a) The terms the kit has decided, plus borrowed terms the kit uses, each credited to its author, recommended; (b) only the kit's own terms; (c) a full AI coding dictionary like Matt Pocock's.
3. **How should a term's web address be formed?** (a) A slug of the term, never changed once published, with an old slug kept as an alias after a rename, recommended; (b) a numeric id; (c) decide when the website is built.
4. **Are the courses an existing place the vocabulary must reach?** (a) Not yet: plan for the website first and add courses when one exists, recommended; (b) yes, at a place you name.
