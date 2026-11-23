---
title: house-review conformance
spec: docs/spec/house-review.md
audited: 2026-11-23
---

# house-review conformance matrix

Spec-vs-implementation audit of [`house-review`](../../.agents/skills/house-review/SKILL.md) against
[`house-review.md`](house-review.md). Produced by `chore-0025`.

This spec has a history worth knowing before reading the matrix. It was written by `feat-0024` to
exercise `verifier-agent`'s `blocked` branch against a real unapproved contract, amended by
`chore-0012` (which resolved a name collision by renaming the skill), and amended again by
`chore-0024` on 2026-08-03, which added `S-013` after finding the skill body contradicted itself
inside one step: Step 1 said there were two modes and then relied on a third. So three of the
thirteen scenarios this matrix first covered (`S-012`, `S-013`, and the `Modes` surface row) exist because someone audited
this skill by hand and found a real defect. This matrix is the first mechanical pass over the whole
contract.

**Re-audited 2026-08-05 (`feat-0040`)** after the evidence gate and the finding signature landed.
Five scenarios (`S-014` through `S-018`) and two surface rows (Evidence, Signature) are new and
audited below, the `Output` row was re-audited against its amended text, and the Step numbers in the
existing rows were corrected where the new Step 4 shifted them. The section below on the weakest row
is rewritten, because `S-007` was the row `feat-0040` was filed to strengthen.

**Re-audited 2026-11-23 (`feat-0078`)** after the two review axes and the depth rule landed in the
skill. Six scenarios (`S-019` through `S-024`) and two surface rows (Axes, Depth) are new, `S-018`
and the `Output` row were re-audited against their amended text, and every row's step numbers were
corrected: the skill gained a depth step (Step 2) and a sources step (Step 4), so the survey is now
Step 3, the axes Step 5, the gate Step 6 and the write-up Step 7. The amendment awaits the
maintainer's approval, so the new rows audit the skill against a contract that is not yet approved.

## What this audit can and cannot establish

`house-review` is a prose skill, so evidence is a clause rather than a code path, and this
establishes that the skill **instructs** the specified behavior rather than that anything enforces
it. Same limit as [`verifier-agent.conformance.md`](verifier-agent.conformance.md).

This spec also has a sibling [`house-review.verification.md`](house-review.verification.md), which
is a different artifact answering a different question. See the note at the end.

## Matrix

| Section | Item | Status | Evidence | Note |
|---|---|---|---|---|
| Scenarios | S-001 explicit path scope reviews named files in full | Conformed | Step 1 / "**A path scope with no range (review the named files in full).**", and Step 3's closing line "An explicit path scope is the user pre-bounding the review for you; honor it and do not widen" | all three obligations present: full-file, no range computed ("No range is computed"), no widening |
| Scenarios | S-012 a range alongside a path scope narrows a change review | Conformed | Step 1 / "**A path scope alongside an explicit range narrows this mode; it does not turn it into a full-file review.**" | |
| Scenarios | S-013 a bare explicit range is reviewed as given, not resolved | Conformed | Step 1 / "**An explicit range (review that range as given).**" with "**supplied rather than resolved**, since a range carries no record of which of the two produced it" | the header block's `changeset` line carries the label, so the reporting requirement is in the output shape as well as the step |
| Scenarios | S-002 neither scope nor range: the branch's own range | Conformed | Step 1 / "Branch ahead of base: review the committed range `<base>..HEAD` (note and offer to include any uncommitted changes)" | |
| Scenarios | S-003 an empty committed range falls back to the working tree | Conformed | Step 1 / "Range empty (on the default branch, or work uncommitted): review the working-tree changes (`git diff HEAD` plus untracked files). Do not dead-end" | |
| Scenarios | S-004 nothing to review is stated, not worked around | Conformed | Step 1 / "Both empty: nothing to review, say so and stop" | |
| Scenarios | S-005 the reviewed code is never modified | Conformed | Step 7 / "Do not edit or commit anything", the preamble / "**report-only**: it never edits or commits", and Notes / "it reviews, it does not change code, and it never commits" | stated three times; Step 7 places the prohibition after the fix-bearing finding templates |
| Scenarios | S-006 findings ordered by severity and individually actionable | Conformed | Step 7 / "ordered `blocker` first, grouped by file within a severity", with the two finding templates carrying a `file:line` location, the issue, why it matters, the evidence, the signature, and a suggested fix | ordering is now within each axis, which the amended contract (S-022) requires |
| Scenarios | S-007 an unsubstantiated candidate is dropped | Conformed | Step 5 / "**validate every candidate finding against the real code before it becomes a reported finding**, and drop anything you cannot substantiate", backed by Step 6 / "**drop the finding.** Not at a lower severity, not with a hedge" | see the note below on how strong this row is |
| Scenarios | S-008 a clean change is reported as clean | Conformed | Step 7 / "If nothing substantive survives validation, say the change looks clean and why, rather than manufacturing findings" and "A review whose findings were all dropped by the gate is a clean review with a drop count" | |
| Scenarios | S-009 the severity scheme comes from the lens, not the skill | Conformed | Notes / "the rubric and severities live in the swappable" lens, "not hardcoded here" | verified negatively: the skill body defines no severity names of its own. The depth table names which severities each depth writes down, using the lens's names, which an adopter renaming them would also have to update; recorded as the one place the body leans on the lens's vocabulary |
| Scenarios | S-010 a change too large to review reports its coverage | Conformed | Step 3 / "**When the change still does not fit, say so in the verdict line and name what you did not read.**", and Step 7's header `coverage:` line | |
| Scenarios | S-011 a structured findings channel changes the channel, not the findings | Conformed | "Running this in Claude Code" / "the evidence gate, and each finding's evidence and signature are identical either way; only the output channel changes" | |
| Scenarios | S-014 a finding whose quoted evidence resolves nowhere is dropped | Conformed | Step 6 / "**Quote found nowhere in the file, or the path does not resolve**: **drop the finding.** Not at a lower severity, not with a hedge", and "Report **how many candidates the gate dropped**, as one line in the output, without restating them" | |
| Scenarios | S-015 a quote found at a shifted line is re-anchored, not dropped | Conformed | Step 6 / "Correct the line number to where the text actually is and say the finding was re-anchored. Do not drop it. The code moved; the defect did not", plus the lens's "The line number is deliberately not in it" | the signature's stability under re-anchoring holds because the signature has no line field |
| Scenarios | S-016 a finding about something absent is citable | Conformed | Step 5 / "Reaching for a quote of code that does not exist is the mistake here", Step 6's absence branch, the lens's `absent` and `searched` fields, and Step 7's `Evidence (absence)` template | |
| Scenarios | S-017 every reported finding carries a stable signature | Conformed | Step 6 / "give every surviving finding the lens's **signature**", the lens's signature section, worked in both Step 7 templates | the lens's category list now includes the three spec-axis slugs |
| Scenarios | S-018 depth does not change what a finding must prove | Conformed | Step 6 / "**Depth does not touch this step.** A `quick` review is a smaller read, never a lower standard of proof", and the Design choices bullet "Depth changes how much is read, never what a finding must prove" | re-audited against the amended wording; the composition across two skills it used to span is now one skill, so the two statements can no longer drift apart across a skill boundary |
| Scenarios | S-019 the spec axis reports missing, unasked-for, and wrong work | Conformed | Step 5 / "what it asked for that is missing or partial (`spec-missing`), what the change does that nobody asked for (`spec-extra`), and what looks built but wrong (`spec-wrong`)", and the lens's "Every spec finding quotes the contract line it rests on" | the gate obligation is met by the lens rule that the contract quote is resolved "against the contract file just as the code quote does against the code" |
| Scenarios | S-020 with no contract, the spec axis says so and stops | Conformed | Step 4 / "the spec axis reports \"no contract available\" and is skipped. It never invents one from the diff", and the lens's "it never reconstructs intent from the diff" | |
| Scenarios | S-021 the standards axis reads the repository's written standards | Conformed | Step 4 / "`CODING_STANDARDS.md` and `CONTRIBUTING.md` whenever they exist", Step 5 / "each finding cites the standard (file and rule)", and the lens's "**The repository overrides the rubric.**" and "**Cite the standard.**" | the judgement-call label is in both the skill ("is labelled as one") and the lens |
| Scenarios | S-022 the two axes are independent and are not reranked | Conformed | Step 5 / "run the axes in sequence: finish the spec axis, through Step 6, and write its findings down before reading for the standards axis", and Step 7 / "Never name a single worst finding across both axes" | the subagent branch states a fresh context and the leaf rule, per the overhaul plan's subagent rule |
| Scenarios | S-023 depth is chosen from stated signals, and an explicit depth wins | Conformed | Step 2 / "If the user named `quick`, `standard` or `deep`, that is the depth", the signal table, the R1 to R7 table with "First match wins", and Step 7's header `depth:` and `excluded:` lines | the disagreement report is Step 2 / "report `detected_depth` and the files that would have escalated" |
| Scenarios | S-024 an unmeasurable change is reviewed at standard depth | Conformed | Step 2 / "When a signal cannot be computed, or the reviewable set comes out empty, select `standard` and say which signal failed" | |
| Proposed Surface | Invocation | Conformed | Step 1 | |
| Proposed Surface | Modes (four, enumerated) | Conformed | Step 1's four branches | |
| Proposed Surface | Range resolution, and reporting supplied vs. resolved | Conformed | Step 1's numbered resolution and both the "supplied" and "resolved" statements | |
| Proposed Surface | Severities `blocker`, `major`, `minor`, `nit` defined by the lens | Conformed | [`review-quality.md`](../../.agents/rules/review-quality.md) severity scheme, referenced from the preamble and Step 5 | |
| Proposed Surface | Evidence: path, lines, symbol, quote, with an absence form | Conformed | The lens's two evidence tables, applied in Steps 5 and 6 | |
| Proposed Surface | Signature: four fields, no line number | Conformed | The lens's signature section, emitted in Step 6 and shown in both Step 7 templates | |
| Proposed Surface | Axes: spec and standards, independent, not reranked | Conformed | Step 5 and the lens's "Two axes" section | |
| Proposed Surface | Depth: explicit or R1 to R7, anchors and capped remainder, unmeasurable selects standard | Conformed | Step 2's rule table, the R2 row's "capped at `standard`", and the fallback sentence | |
| Proposed Surface | Output: header block, then a Spec and a Standards section with verdicts, inspected files and ordered findings | Conformed | Step 7's header block and "a `## Spec` section and a `## Standards` section, each opening with its own one-line verdict" | |
| Proposed Surface | Side effects: none | Conformed | Step 7 and Notes | the gate and the depth signals read files and run searches, and write nothing |
| Open Questions | One, on whether gate-dropped findings should be recoverable on request | Conformed | spec's Open Questions section | the skill reports the count and not the content, and [`references/rationale.md`](../../.agents/skills/house-review/references/rationale.md) names the question as open |

## Coverage proof

**Audited** (35 items): scenarios S-001 through S-024 (all twenty-four); the ten Proposed Surface
rows; and the Open Questions section.

**Unreconciled**: none.

**Not-built**: none. Every scenario and every surface element has evidence.

## The weakest row, named rather than buried

`S-007` was this matrix's weakest row and is the reason
[`feat-0040`](../../.tasks/done/feat-0040-evidence-gate-and-finding-signature.md) was filed. The original
audit put it this way: the skill instructed dropping any finding it could not substantiate, but
nothing checked that a reported finding *was* substantiated, and the failure mode is invisible by
construction, since a review full of confident, well-formatted, unverifiable findings looks exactly
like a good review. That was not hypothetical here: `verifier-agent`'s dogfood found a conformance
matrix whose classifications were correct but whose line citations had drifted eight lines after a
refactor, caught because a human looked.

The evidence gate is that instruction turned into a check with a defined outcome per branch, so the
row is now stronger than it was. It is worth being precise about how much stronger, because
overstating it would recreate the same problem one level up.

**What changed**: a finding now has to carry a quote, the quote has to be resolved against the file
at the revision under review, and each outcome has one stated disposition. A drifted citation is
re-anchored rather than dropped, and an unresolvable one is dropped rather than hedged. Those are
answers the skill did not have before, and the drop count makes a reviewer whose citations routinely
fail to resolve visible in the output.

**What did not change**: `house-review` is prose, so the gate is an instruction like everything else
in this matrix, and the limit stated at the top of this file still applies. Nothing executes the
gate, and a review that skipped it produces output that looks the same minus the evidence lines. The
gate is meaningfully more checkable than what it replaced, because a reader can now rerun any
citation themselves, which is the property `S-007` was missing. It is not enforcement.

## Why this file exists alongside `house-review.verification.md`

They answer different questions and neither replaces the other:

- **This file (`.conformance.md`)** asks *does the implementation match the contract?* It is
  produced by [`spec-conformance`](../../.agents/skills/spec-conformance/SKILL.md), covers every
  scenario and surface element, and classifies each `Conformed`, `Diverged`, or `Not-built`.
- **[`house-review.verification.md`](house-review.verification.md)** asks *was this run's work
  acceptable?* It is an evaluation record produced by `feat-0024` while exercising
  `verifier-agent`'s `blocked` branch, and it records a verdict with evidence for one run.

A spec can have one, both, or neither. The distinction is now stated in the layout table in
`AGENTS.md` and is what the spec-closeout gate in
[`feat-0039`](../../.tasks/done/feat-0039-spec-conformance-gate-hook.md) will look for: the gate accepts
a `<stem>.conformance.*` sibling, so a `.verification.md` alone does not satisfy it, and before this
task `house-review` would have blocked on exactly that.
