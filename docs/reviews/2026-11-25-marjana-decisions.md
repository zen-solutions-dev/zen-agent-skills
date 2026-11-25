# Marjana decisions, 2026-11-25

The maintainer's answers to the "Marjana Decision Sheet" (a private decision sheet), read from the sheet's own store on 2026-11-25 at about 02:50 UTC and transcribed here verbatim, choice and note, so a session that cannot open the artifact still has them. The sheet covered the open items of [the Marjana round](2026-11-24-marjana-plan.md), [its retro](2026-11-24-retro-marjana.md), and [the coverage map](2026-11-25-skills-coverage-map.md). Where an answer approves a change to a contract or a rule, the change itself is still to be made; this file records the decision, not the work.

## A. Contracts

| Id | Item | Answer |
|---|---|---|
| A1 | The setup file and its format (`docs/spec/zen-config.md`) | Approve |
| A2 | Review once, fix once, then stop (`house-review` `S-025`) | Approve |
| A3 | Verifiers record the exact commit (`verifier-agent`) | Approve |
| A4 | The context budget counts only what loads (`install` `S-014`) | Approve |
| A5 | A warning for steps with no completion criterion (`validate-skills` `S-028`) | Approve |
| A6 | `spec-author` reads the spec folder from the setup file | Approve |
| A7 | Documentation-only changes run the documentation gates (`cloud-executable` `S-021`, `S-022`) | Approve |
| A8 | The final wording of rule D1 | Loosen it (see B1) |
| A9 | Stricter checks land with an exception list (the ratchet) | Approve |

## B. Retro proposals

| Id | Item | Answer |
|---|---|---|
| B1 | `R-201`: how an orchestrator lands a child that is behind | Allow mechanical-only orchestrator merges, re-checked and listed in the PR |
| B2 | `R-202`: children leave their task files alone | Approve |
| B3 | `R-203`: a per-file list instead of one count | Approve |
| B4 | `R-204`: a warning for long changelog lines | Approve |
| B5 | `R-205`: the kit installed in every cloud session | Approve |
| B6 | `R-206`: notes for restarts | Approve |
| B7 | `R-207`: check early which remote actions are allowed | Approve |
| B8 | `R-208`: relays are acknowledged | Approve |
| B9 | `R-209`: review reads the contract's guards | Approve |
| B10 | `R-210`: CI on integration branches | Later. Note: "lets save CI minutes where we can, this should be something we can allow, but jusr run the CI on the Final PR's for now." |
| B11 | `R-003` and `R-004`, owed from the earlier retro | Approve |
| B12 | `R-002`: does the `main` ruleset also protect `developer`? | Not checked yet |
| B13 | WS-D's own retro proposals, `R-101` to `R-106` | Let the next session triage them |

## C. The big questions

| Id | Item | Answer |
|---|---|---|
| C1 | Should verified two-way-door PRs merge themselves? | Allow it per repository, opt-in, with sampling |
| C2 | Should the kit include `teach`? | Adopt teach as a draft |
| C3 | A security axis in `house-review` | Required on one-way doors, optional otherwise |
| C4 | A skill for vetting other people's skills | Build it as a draft |
| C5 | Effort level for child sessions | Medium for children, high for verifiers and debugging |

## D. Rules worth revisiting

| Id | Item | Answer |
|---|---|---|
| D1 | When the contribution bar applies | Gate promotion, add a draft expiry |
| D2 | The kit's scope | Shareability is the only filter. Note: "Id like to expand, Matt Pococks repo and skill set and his webpage is really a very noice target id like to use for aiming towards with our Zen Solutions Dev platform I am envisioning and crafting towards with you," |
| D3 | The destructive-git gate | Ship it opt-in now |
| D4 | Sketches in PR summaries | Allow code-shaped sketches in PRs |
| D5 | How releases reach adopters | Add tagged releases |

## E. Gaps from the coverage map

| Id | Item | Answer |
|---|---|---|
| E1 | Agree test seams once per plan | Do it |
| E2 | A rule for resolving merge conflicts | Do it |
| E3 | Turn on `orchestrate`'s memory (plus page updates, lint, the recurring-job offer, the exploration child) | Do it |
| E4 | Three lost compositions (`grill` writes the glossary live; `retro` reads the writing lens; the deep-module vocabulary as a shared lens) | Do it |
| E5 | A decision map for big efforts (`wayfinder`), a `prototype` draft, and the lost `wayfinder` roadmap entry | Do it |
| E6 | Finish the debugging skill (missing rungs, ranked hypotheses, its second independent run); promote `research` after one run outside this repository | Do it |
| E7 | Codex and Copilot parity (Codex `agents/openai.yaml`, verified installs) | Do it |
| E8 | Sharper PR and review text (visual summary, glossary terms, named code smells) | Do it |
| E9 | Small items: a declined-ideas register `zen` and `retro` read; a check that `zen` and the catalog name every skill; an install note on name clashes with Matt's skills; issue templates asking for version, model and effort; a re-pitch rule when a relay is unclear; a standard-library wizard script library | Do all of them |

## F. Wider goals, from the podcast

| Id | Item | Answer |
|---|---|---|
| F1 | A daily improvement loop (scheduled `improve-architecture`, one PR) | Yes. Which repositories was not answered. |
| F2 | A knowledge wiki fed by your channels | Yes |
| F3 | One shared vocabulary across kit, website and courses | Yes |
| F4 | An issue-to-PR loop for public repositories | Yes |
| F5 | Sandboxed runs for untrusted code and skills | Yes |
| F6 | Your own notes on the podcast | Not answered |
| F7 | Who else to learn from | Note: "I meant Dan Koe." Then: Matt Pocock, Aaron Knightly, Tom Scryleus, Wanderloots, Robert Greene, Gabor Mate, Nick Saraev, Bruce Lee, Clark Kegley, Jayme Edwards (host of the Developer Reborn YouTube channel), Dan Martell, Cal Newport, Carl Jung, the Tech with Tim YouTube channel, Doms Gaming Channel, Joe Hudson, NetworkChuck, David Shapiro, Mo Gawdat, Boris Cherny, Tristan Harris, Gary V, Alex Hormozi. Spellings as given. |

## G. Housekeeping and the next session

| Id | Item | Answer |
|---|---|---|
| G1 | `developer` brought up to `main` | Do it for me |
| G2 | Branch clean-up | Not yet |
| G3 | The brain-dump PR in the ops repository | Not yet |
| G4 | A scheduled research refresh | Yes, every two weeks |
| G5 | Archive the finished child sessions | Archive them |
| G6 | Keep the meta-analysis | Commit it to docs/reviews |
| G7 | Next session: what comes first | Not answered |
| G8 | Next session: where the work lands | developer, as zen.md says |
| G9 | The website overhaul | After the skills round |

The sheet's free-text brain dump was empty when read.

## Still open after this sheet

- **G7, the build order.** Not answered; the handoff proposes one for the maintainer to confirm.
- **Tracker publishing.** The coverage map's rule 12 (tracking is deliberately local, while `zen-config` accepts GitHub trackers and role labels that nothing reads) was not on the sheet. C1's per-repository auto-merge leans toward GitHub, but the question itself is undecided and is a one-way door.
- **A guarded load-by-name for drafts** (coverage map rule 9) was not on the sheet.
- **F1's repositories**, **F6**, and **B12** (a GitHub setting only the maintainer can read).

## Round 2, Phase 0 answers (2026-11-25)

Given by the maintainer in the round 2 orchestrating session, in conversation, after the three questions of the [round 2 handoff](2026-11-25-round-2-handoff.md) section 6.

| Id | Item | Answer |
|---|---|---|
| G7 | The build order | Yes, as proposed: wave 1 is Rules and lenses plus Platform and gates, with the orchestrator's own B13 and B5; wave 2 is Align and plan, Orchestrate and build, Ship and learn; the F1 to F5 plans last. The final text of A8/B1 and C1 comes back before it lands. |
| T1 | Tracker publishing (coverage map rule 12) | (a) Opt-in publishing as a draft: `.tasks/` stays the source of truth and is mirrored one way, specs as issues and tasks as sub-issues, with a `triage` draft as the consumer of the `role.*` labels. |
| T2 | A guarded load-by-name for drafts (coverage map rule 9) | Yes: a shipped skill may say "if `<draft>` is installed, read and follow it now", and `validate-skills.py` accepts it without an install edge. |
| T3 | How questions are asked (coverage map rule 16) | The maintainer prefers the clickable multiple-choice picker over questions in prose, which feel overwhelming to scroll. This settles rule 16's comparison for this maintainer: keep the structured question tool. |
| T4 | Direction | Adopt the skills Matt Pocock uses in his daily work with agents and fleets of agents. |
