---
title: spec-author conformance
spec: docs/spec/spec-author.md
audited: 2026-11-23
revised: 2026-11-23 (feat-0076, re-audited in full against the rewritten skill body after the interview amendment; S-005 retired, S-008 and S-009 added); 2026-11-23 (feat-0083, the approval digest: S-010, S-011, a Constraint and two Proposed Surface rows added); 2026-11-24 (feat-0084, grill promoted and linked: S-008 and S-009 re-derived against the composed skill)
---

# spec-author conformance matrix

Spec-vs-implementation audit of [`spec-author`](../../.agents/skills/spec-author/SKILL.md) against
[`spec-author.md`](spec-author.md). First produced by `chore-0025`, revised by `chore-0027`, and
re-audited in full by `feat-0076` on 2026-11-23, because that task rewrote the skill body and
amended the contract in the same change. Every row below was re-derived against the rewritten body;
none was carried forward unread.

## What this audit can and cannot establish

`spec-author` is a prose skill, not a program, so both sides are natural language and the evidence
column cites a clause rather than a code path. This establishes that the skill **instructs** the
specified behavior, not that anything **enforces** it. A prose skill can conform perfectly here and
still be ignored by the agent running it. The same limit is recorded in
[`verifier-agent.conformance.md`](verifier-agent.conformance.md) and it applies unchanged.

One scenario, `S-003`, specifies behavior in a **different** skill. It is audited against
[`new-task`](../../.agents/skills/new-task/SKILL.md), which is where the contract places it.

**Audited by the agent that wrote the change.** `feat-0076` rewrote the skill, amended the spec, and
produced this matrix, so per `A7` this verdict is that agent's, not an independent one.

## Matrix

| Section | Item | Status | Evidence | Note |
|---|---|---|---|---|
| Scenarios | S-001 draft from a raw idea | Conformed | "The spec format" section (seven sections in fixed order, `status: draft` in the template) and Procedure step 4 / "Write the `ready` spec to the location above as `<slug>.md` with `status: draft`" | the location half is covered by S-006 and S-007 |
| Scenarios | S-002 self-check with spec-quality | Conformed | Procedure step 3 / "Done when its verdict is `ready`; the spec you write is that version, not the first draft" | the second clause is what satisfies "the file it writes is the `ready` version" |
| Scenarios | S-003 approval gate before decomposition | Conformed | [`new-task`](../../.agents/skills/new-task/SKILL.md) / "Refuse an unapproved spec, or one edited since its approval", with "`not-approved`, `changed`, `malformed`, or `unreadable`: stop and say which" | audited in `new-task` because the scenario places the behavior there; `feat-0076` slimmed `new-task` and kept this clause verbatim; `feat-0083` rewrote it to refuse text edited since approval too, which S-010 audits. Still a cross-skill dependency nothing enforces |
| Scenarios | S-004 read-only for implementation surfaces | Conformed | Procedure step 4 / "edits **only that spec file** (and the spec index, if the repository keeps one): never source code, tests, config, the glossary, or a decision record" | the index widening is unchanged and stays inside the spec location. `feat-0076` kept this scenario intact by design: settled terms are **offered** to `domain-language` as its own step (step 5) rather than written during this run, so composing the interview did not widen the write surface |
| Scenarios | S-005 retired | Retired | none: the scenario was retired by the `feat-0076` amendment | its behavior (exactly one clarifying question) is superseded by S-008. The skill no longer instructs it, which is the intended direction |
| Scenarios | S-006 the spec goes where the repository already keeps specs | Conformed | "Where the spec goes" / "Find the repository's spec location before writing" ... "Match it." | |
| Scenarios | S-007 a repository with no spec directory gets the documented fallback | Conformed | "Where the spec goes" / "Only when the repository has none does `docs/spec/<slug>.md` apply, as this kit's default" | |
| Scenarios | S-008 the interview settles decisions before any file is written | Conformed | Procedure step 1 / "interview the person over the decision tree until its frontier is empty and they confirm the shared understanding" and "Write no file until the interview has closed", composing [`grill`](../../.agents/skills/grill/SKILL.md) step 3 / "Number every question, continuing the numbering across rounds" and "your recommended answer worded so that "yes" accepts it" | re-derived by `feat-0084`, which promoted `grill` and deleted `spec-author`'s inline fallback: the numbered, recommended, yes-accepts form now lives only in `grill`, which `spec-author` links, so an install that places `spec-author` places `grill` with it |
| Scenarios | S-009 facts are looked up, not asked | Conformed | [`grill`](../../.agents/skills/grill/SKILL.md) step 2 / "Never ask the person a fact. Find it.", and its decisions record's "Facts found" section, "<fact> (source: <file, command, or lookup>)", composed by Procedure step 1 / "Then compose `grill`" | re-derived by `feat-0084`: the fallback that carried this rule inline is deleted, and the behavior is now carried by the composed skill alone |
| Scenarios | S-010 approved text edited after its approval is not decomposed | Conformed | `new-task` "Decomposing an approved spec" / "`not-approved`, `changed`, `malformed`, or `unreadable`: stop and say which" | added by `feat-0083`, pending the maintainer's re-approval. Like S-003, the behaviour lives in `new-task`, and this contract records it because `spec-author` owns the approval record |
| Scenarios | S-011 an amendment leaves the approval record alone | Conformed | "Amending an approved spec" / "leave `status: approved` and `approved_digest` exactly as they are", with step 5's "when the spec carried a digest, that it now reads `changed` until the person re-approves" | added by `feat-0083` |
| Proposed Surface | Output file: existing spec location, `docs/spec/<slug>.md` as fallback | Conformed | "Where the spec goes" | same clauses as S-006 and S-007 |
| Proposed Surface | Frontmatter `status`: `draft` author-set, `approved` human-set only | Conformed | "The spec format" / "**This skill only ever writes `status: draft`.**" | restated in step 5 |
| Proposed Surface | Body sections (seven, named) | Conformed | "The spec format" template / "these sections in this order, no others" | |
| Proposed Surface | Scenario ids stable `S-NNN`, never renumbered; a retired id stays in place | Conformed | "The spec format" / "never renumbered or reused" | the retired-id half is a property of the spec document, and `spec-author.md` itself is the instance: S-005 keeps its heading, marked retired |
| Proposed Surface | Interview round | Conformed | same clauses as S-008 | |
| Proposed Surface | Frontmatter `approved_digest`: human-set only, never written or changed by the skill | Conformed | "The spec format" / "writing either key is the person's act, never this skill's or any agent's" | added by `feat-0083` |
| Proposed Surface | `scripts/spec_digest.py`: read-only, six verdicts, `--queue` | Conformed | [`spec_digest.py`](../../.agents/skills/spec-author/scripts/spec_digest.py) docstring and `main`, with "The script only reads and prints" in "The spec format" | added by `feat-0083`; exercised by `tests/test_spec_digest.py` |
| Goals | 1. Draft a persistent spec with all seven parts | Conformed | Procedure steps 2 and 4 | covered by S-001 |
| Goals | 2. Compose `spec-quality` to reach a `ready` verdict | Conformed | Procedure step 3, and the preamble / "composes two others rather than restating them" | |
| Goals | 3. Represent an explicit human approval state | Conformed | "The spec format" `status` rule and step 5 | |
| Goals | 4. Align with the person before drafting | Conformed | Procedure step 1, "Align before drafting" | covered by S-008 and S-009 |
| Constraints | Composes `spec-quality` rather than restating it | Conformed | the preamble | |
| Constraints | The interview follows `grill`, with an inline fallback | Conformed | Procedure step 1 / "Fallback while `grill` is a draft" | |
| Constraints | Read-only for implementation surfaces | Conformed | Procedure step 4 | same evidence as S-004 |
| Constraints | `status` is one of `draft` or `approved`; never self-approves | Conformed | "The spec format" | |
| Constraints | An approval is tied to the text approved through `approved_digest`, which the skill never writes | Conformed | "The spec format" / "**Approval is bound to the text a person read.**" | added by `feat-0083` |
| Constraints | Specs go to the repository's existing spec location, `docs/spec/<slug>.md` as fallback | Conformed | "Where the spec goes" | recorded once per section it appears in |
| Non-Goals | Does not decompose into tasks | Conformed | step 5 / "Do not decompose it, and do not treat your draft as approved" | |
| Non-Goals | Does not write code, tests, or architecture | Conformed | step 4, and step 2's plan-material rule | |
| Open Questions | None | Conformed | spec states `None.` | |

## Coverage proof

**Audited** (31 items): scenarios S-001 to S-011, of which S-005 is retired; seven Proposed Surface
rows; Goals 1 to 4; six Constraints; two Non-Goals; the Open Questions section.

**Unreconciled** (0 items): none.

**Retired** (1 item): S-005, retired by the `feat-0076` amendment and superseded by S-008.

**Not-built**: none.

## Note on the risks this matrix leaves open

- `S-003` still lives in another skill's body, so `new-task` could lose its refusal clause with no
  test failing. Unchanged since `chore-0025`.
- `S-008` and `S-009` are carried by `grill` alone since `feat-0084` deleted the inline fallback,
  so a change to `grill`'s step 2 or step 3 can break `spec-author`'s contract with no edit to
  `spec-author`. The link is what keeps both in every install; nothing tests the composition.
- The amendment is pending the maintainer's re-approval; until then this matrix audits a contract
  nobody has re-approved.
