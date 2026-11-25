---
title: house-review conformance
spec: docs/spec/house-review.md
audited: 2026-11-25
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

**Re-audited 2026-11-24 (`feat-0093`)** after the skill gained Step 8 (the re-check after one fix
round) and was compressed under the kit's 250-line guide. `S-025` and the re-check half of the
Modes row are new and await the maintainer's approval. Every row whose quoted evidence the
compression reworded was re-read against the skill at that date and its quote replaced; no row's
status changed. Step 6 now points at the lens's evidence gate and states its branches in short
rather than in full, so `S-007`, `S-014` and `S-015` rest on the skill and the lens together.

**Re-audited 2026-11-25 (`feat-0108`)** after the skill gained the guard check (Step 4 collects the
guards, Step 5 marks them) and the security axis (Step 4 names the door, Step 5 runs the axis, Step 7
reports it). `S-026`, `S-027` and the Guards surface row are new and await the maintainer's
re-approval; the Axes and Output rows were re-audited against their amended text; `S-022` was
re-read because the closing line now says "across the axes", and its status holds. The audit was run
by the agent that wrote the change, so it is the author's own reading (`A7`), not an independent
verdict.

## What this audit can and cannot establish

`house-review` is a prose skill, so evidence is a clause rather than a code path, and this
establishes that the skill **instructs** the specified behavior rather than that anything enforces
it. Same limit as [`verifier-agent.conformance.md`](verifier-agent.conformance.md).

This spec also has a sibling [`house-review.verification.md`](house-review.verification.md), which
is a different artifact answering a different question. See the note at the end.

## Matrix

| Section | Item | Status | Evidence | Note |
|---|---|---|---|---|
| Scenarios | S-001 explicit path scope reviews named files in full | Conformed | Step 1 / "**A path scope with no range**: review the named files, directory or glob in full, as they stand; no range is computed", and Step 3 / "An explicit path scope pre-bounds the review; do not widen it" | all three obligations present: full-file, no range computed, no widening. Re-audited 2026-11-24 (`feat-0093`) after the step was compressed to bullets |
| Scenarios | S-012 a range alongside a path scope narrows a change review | Conformed | Step 1 / "**Both**: review the range restricted to the named paths, not the files in full" | re-audited 2026-11-24 (`feat-0093`) |
| Scenarios | S-013 a bare explicit range is reviewed as given, not resolved | Conformed | Step 1 / "**An explicit range**: that range *is* the changeset, reported as **supplied**; compute no merge-base of your own" | the header block's `changeset` line carries the label, so the reporting requirement is in the output shape as well as the step. Re-audited 2026-11-24 (`feat-0093`): the reason a range is labelled (it carries no record of its origin) moved out with the compression and is not an obligation of the scenario |
| Scenarios | S-002 neither scope nor range: the branch's own range | Conformed | Step 1 / "Branch ahead of base: review the committed range `<base>..HEAD` (note and offer to include any uncommitted changes)" | |
| Scenarios | S-003 an empty committed range falls back to the working tree | Conformed | Step 1 / "Range empty (on the default branch, or work uncommitted): review the working-tree changes (`git diff HEAD` plus untracked files). Do not dead-end" | |
| Scenarios | S-004 nothing to review is stated, not worked around | Conformed | Step 1 / "Both empty: nothing to review, say so and stop" | |
| Scenarios | S-005 the reviewed code is never modified | Conformed | Step 7 / "Edit and commit nothing", the preamble / "**report-only**: it never edits or commits", and Step 7's done-when / "nothing in the repository was edited or committed" | stated three times. Re-audited 2026-11-24 (`feat-0093`): the Notes restatement was removed as a duplicate of the preamble, and Step 8 (the re-check) reads the code and its cited evidence but writes nothing |
| Scenarios | S-006 findings ordered by severity and individually actionable | Conformed | Step 7 / "ordered `blocker` first, grouped by file within a severity", with the two finding templates carrying a `file:line` location, the issue, why it matters, the evidence, the signature, and a suggested fix | ordering is now within each axis, which the amended contract (S-022) requires |
| Scenarios | S-007 an unsubstantiated candidate is dropped | Conformed | Step 5 / "Validate every candidate against the real code, and drop what you cannot substantiate", backed by Step 6 / "found nowhere, or the path does not resolve, **drop**, with no lower severity and no hedge" | see the note below on how strong this row is. Re-audited 2026-11-24 (`feat-0093`): Step 6 now points at the lens's gate and states its branches in short, rather than restating them in full |
| Scenarios | S-008 a clean change is reported as clean | Conformed | Step 7 / "When nothing survives the gate, say the change looks clean and why, with the drop count; a clean axis still lists what it inspected", with the lens's review protocol rule 7 / "Say when it is clean" | re-audited 2026-11-24 (`feat-0093`) |
| Scenarios | S-009 the severity scheme comes from the lens, not the skill | Conformed | Design choices / "the rubric, severities, evidence shape, gate and signature live in the lens" | verified negatively: the skill body defines no severity names of its own. The depth table names which severities each depth writes down, using the lens's names, which an adopter renaming them would also have to update; recorded as the one place the body leans on the lens's vocabulary. Re-audited 2026-11-24 (`feat-0093`): the Notes bullet this row cited was removed as a duplicate of Design choices |
| Scenarios | S-010 a change too large to review reports its coverage | Conformed | Step 3 / "**When the change still does not fit, say so in the `coverage` line and name what you did not read**", and Step 7's header `coverage:` line | re-audited 2026-11-24 (`feat-0093`) |
| Scenarios | S-011 a structured findings channel changes the channel, not the findings | Conformed | `references/claude-code.md`, reached from the Notes bullet "How the review maps onto Claude Code (a host findings tool, the built-in `/code-review`)" | moved out of the body by `chore-0096`, unchanged in substance; the section heading that reached it became a Notes bullet on 2026-11-24 (`feat-0093`) |
| Scenarios | S-014 a finding whose quoted evidence resolves nowhere is dropped | Conformed | Step 6 / "found nowhere, or the path does not resolve, **drop**, with no lower severity and no hedge", the lens's gate section, and "Report **how many candidates the gate dropped** in the header (no line when none)" | re-audited 2026-11-24 (`feat-0093`) |
| Scenarios | S-015 a quote found at a shifted line is re-anchored, not dropped | Conformed | Step 6 / "found at another line, **re-anchor and report**, saying so", the lens's gate section, plus the lens's "The line number is deliberately not in it" | the signature's stability under re-anchoring holds because the signature has no line field. Re-audited 2026-11-24 (`feat-0093`) |
| Scenarios | S-016 a finding about something absent is citable | Conformed | Step 5 / "a defect in absent code (a missing test, an unhandled branch) takes the absence form, never a quote of code that does not exist", Step 6's absence branch, the lens's `absent` and `searched` fields, and Step 7's `Evidence (absence)` line | re-audited 2026-11-24 (`feat-0093`): the worked absence example became a one-line field description |
| Scenarios | S-017 every reported finding carries a stable signature | Conformed | Step 6 / "give each survivor the lens's line-free **signature**", the lens's signature section, worked in both Step 7 templates | the lens's category list now includes the three spec-axis slugs |
| Scenarios | S-018 depth does not change what a finding must prove | Conformed | Step 6 / "**Depth does not touch this step.** A `quick` review is a smaller read, never a lower standard of proof", and Design choices / "depth changes how much is read, never what a finding must prove" | re-audited 2026-11-24 (`feat-0093`) |
| Scenarios | S-019 the spec axis reports missing, unasked-for, and wrong work | Conformed | Step 5 / "what it asked for that is missing or partial (`spec-missing`), what the change does that nobody asked for (`spec-extra`), and what looks built but wrong (`spec-wrong`)", and the lens's "Every spec finding quotes the contract line it rests on" | the gate obligation is met by the lens rule that the contract quote is resolved "against the contract file just as the code quote does against the code" |
| Scenarios | S-020 with no contract, the spec axis says so and stops | Conformed | Step 4 / "the spec axis reports \"no contract available\" and is skipped. It never invents one from the diff", and the lens's "it never reconstructs intent from the diff" | |
| Scenarios | S-021 the standards axis reads the repository's written standards | Conformed | Step 4 / "`CODING_STANDARDS.md` and `CONTRIBUTING.md` whenever they exist", Step 5 / "each finding cites the standard (file and rule)", and the lens's "**The repository overrides the rubric.**" and "**Cite the standard.**" | the judgement-call label is in both the skill ("is labelled as one") and the lens |
| Scenarios | S-022 the two axes are independent and are not reranked | Conformed | Step 5 / "run the axes in sequence: finish the spec axis, through Step 6, and write its findings down before reading for the standards axis", and Step 7 / "Never name a single worst finding across the axes" | the subagent branch states a fresh context and the leaf rule, per the overhaul plan's subagent rule. Re-audited 2026-11-25 (`feat-0108`): the quote read "across both axes" until a third axis was added |
| Scenarios | S-023 depth is chosen from stated signals, and an explicit depth wins | Conformed | Step 2 / "If the user named `quick`, `standard` or `deep`, that is the depth", the signal table, the R1 to R7 table with "First match wins", and Step 7's header `depth:` and `excluded:` lines | the disagreement report is Step 2 / "report `detected_depth` and the files that would have escalated" |
| Scenarios | S-024 an unmeasurable change is reviewed at standard depth | Conformed | Step 2 / "When a signal cannot be computed, or the reviewable set is empty, select `standard` and say which signal failed" | re-audited 2026-11-24 (`feat-0093`) |
| Scenarios | S-025 a re-check reads only the first review's findings, then stops | Conformed | Step 1 / "asks whether its findings were fixed is a **re-check**: skip to Step 8", and Step 8 / "re-check only what the first review asked for", each finding marked **fixed**, **open** or **disputed**, the fix range read "at `quick` depth for a blocker the fix introduced", then "Then stop. A finding still open after this goes to the person to decide, not into another round" | added 2026-11-24 (`feat-0093`); audits the skill against a scenario the maintainer has not yet approved. The lens's review protocol rule 8 states the same stopping rule for every reviewing skill |
| Scenarios | S-026 the spec axis quotes and checks every guard of the contract | Conformed | Step 4 / "**The contract's guards**, from every spec source found: each line that forbids, limits or refuses something", "the guards of the contract as it stood before the amendment as well as after", "Quote each guard verbatim, with its file and section", and "A conformance matrix or verification record the change's own author updated is not a guard source and not evidence on this axis"; Step 5 / "mark it **held** ... **broken** (a `spec-wrong` finding ...), or **not reached**"; Step 7 / "The Spec section lists the guards after its verdict" | added 2026-11-25 (`feat-0108`), pending re-approval. Broken guards pass the gate because they are ordinary `spec-wrong` findings and Step 6 applies to every candidate |
| Scenarios | S-027 a one-way door gets a security axis of its own | Conformed | Step 4 / "**The door**: one-way or two-way, by the one-way list of the sampled self-merge's two-way-door guard" and "read it now"; Step 5 / "**Security axis.** Required when Step 4 named the door one-way", "It is a pass of its own, with its own verdict and inspected list"; Step 7 / "A one-way door whose security axis was skipped opens the review with that line" and "Never name a single worst finding across the axes" | added 2026-11-25 (`feat-0108`), pending re-approval. The inspection list is the lens's security-axis paragraph in [`review-quality.md`](../../.agents/rules/review-quality.md); the door list is `A8` guard 2 in [`autonomy.md`](../../.agents/rules/autonomy.md), per the amended Constraint. Re-audited in the fix round of 2026-11-25 after the door was repointed |
| Proposed Surface | Invocation | Conformed | Step 1 | |
| Proposed Surface | Modes (four, enumerated, plus the re-check) | Conformed | Step 1's four branches, and its re-check branch into Step 8 | the re-check row added 2026-11-24 (`feat-0093`), pending approval |
| Proposed Surface | Range resolution, and reporting supplied vs. resolved | Conformed | Step 1's numbered resolution and both the "supplied" and "resolved" statements | |
| Proposed Surface | Severities `blocker`, `major`, `minor`, `nit` defined by the lens | Conformed | [`review-quality.md`](../../.agents/rules/review-quality.md) severity scheme, referenced from the preamble and Step 5 | |
| Proposed Surface | Evidence: path, lines, symbol, quote, with an absence form | Conformed | The lens's two evidence tables, applied in Steps 5 and 6 | |
| Proposed Surface | Signature: four fields, no line number | Conformed | The lens's signature section, emitted in Step 6 and shown in both Step 7 templates | |
| Proposed Surface | Axes: spec (with guards), standards (with the smell baseline) and security where required, independent, not reranked | Conformed | Step 5's three axis paragraphs, "Apply the lens's **smell baseline**", and the lens's "Two axes" section | re-audited 2026-11-25 (`feat-0108`) against the amended row |
| Proposed Surface | Guards: numbered, quoted with file and section, each marked held, broken or not reached | Conformed | Step 4 / "into a numbered list", Step 5's three marks, Step 7's guard list | added 2026-11-25 (`feat-0108`), pending re-approval |
| Proposed Surface | Depth: explicit or R1 to R7, anchors and capped remainder, unmeasurable selects standard | Conformed | Step 2's rule table, the R2 row's "capped at `standard`", and the fallback sentence | |
| Proposed Surface | Output: header block with the door and the security axis's status, then a Spec section with its guards, a Standards section and a Security section when it ran, with verdicts, inspected files and ordered findings | Conformed | Step 7's header block (`door:` and `security axis:` lines) and "a `## Spec` section, a `## Standards` section and, when the axis ran, a `## Security` section, each opening with its own one-line verdict" | re-audited 2026-11-25 (`feat-0108`) against the amended row |
| Proposed Surface | Re-check output: one line per signature with its mark, the counts, any new blocker, closed or what a person must decide | Conformed | Step 8 / "Report one line per signature with its mark, the count of each mark, and any new blocker", and its done-when / "the report says the review is closed or names what the person must decide" | added 2026-11-24 (`feat-0093`), pending approval |
| Proposed Surface | Side effects: none | Conformed | the preamble / "**report-only**: it never edits or commits", Step 7 / "Edit and commit nothing", and Step 7's done-when / "nothing in the repository was edited or committed" | the gate, the depth signals and the re-check read files and run searches or a cited read-only command, and write nothing. Re-audited 2026-11-24 (`feat-0093`): this row cited Notes, which no longer restates it |
| Open Questions | One, on whether gate-dropped findings should be recoverable on request | Conformed | spec's Open Questions section | the skill reports the count and not the content, and [`references/rationale.md`](../../.agents/skills/house-review/references/rationale.md) names the question as open |

## Coverage proof

**Audited** (40 items): scenarios S-001 through S-027 (all twenty-seven); the twelve Proposed
Surface rows, with Re-check output added on 2026-11-24 (`feat-0093`) and Guards on 2026-11-25
(`feat-0108`); and the Open Questions section.

**Unreconciled**: none.

**Not-built**: none. Every scenario and every surface element has evidence.

## The weakest row, named rather than buried

`S-007` was this matrix's weakest row and is the reason
[`feat-0040`](../../.quests/done/feat-0040-evidence-gate-and-finding-signature.md) was filed. The original
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
[`feat-0039`](../../.quests/done/feat-0039-spec-conformance-gate-hook.md) will look for: the gate accepts
a `<stem>.conformance.*` sibling, so a `.verification.md` alone does not satisfy it, and before this
task `house-review` would have blocked on exactly that.
