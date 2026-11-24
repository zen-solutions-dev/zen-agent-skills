---
title: house-review
status: approved
---

# house-review

Behavioral contract for the [`house-review`](../../.agents/skills/house-review/SKILL.md) skill, written
2026-07-27 (`feat-0024`). This is a **characterization** spec: it records the contract the shipped
skill already holds, drafted from its actual behavior rather than from what it arguably should do.
Where the skill is genuinely ambiguous, that ambiguity is recorded in Open Questions rather than
resolved by inventing behavior.

Amended 2026-07-27 (`chore-0012`): the skill was renamed from `code-review` to `house-review` to
resolve a collision with harness built-in review commands, and both Open Questions were resolved into
the contract. Reopened to `draft` for that amendment; a human sets `status: approved`.

**Amended 2026-08-03 (`chore-0024`) on the author's explicit instruction, and re-approved.** S-013 adds
a bare explicit range, and the Modes and Range resolution rows now account for it. This repairs an
internal inconsistency rather than expanding scope: the Invocation row already permitted "a base, or a
commit range", and the two rows beneath it enumerated no mode and no resolution branch that such an
input could reach, so the table contradicted itself across three consecutive rows. The amendment also
states which side wins when an explicit range meets the resolved default, and that the difference
between the two is reported, because a range does not say on its own whether it was resolved or handed
over.

**Amended 2026-08-05 (`feat-0040`).** S-014 through S-018 add the evidence gate and the stable
finding signature: what a finding must prove before it is reported, what happens when its quote has
drifted, and how a finding whose evidence is an absence is cited. The Proposed Surface gains an
Evidence row and a Signature row, and the Output row now names both. This is an addition, not a
correction: no existing scenario changes, and S-007 (an unsubstantiated candidate is dropped) keeps
its wording, since the gate is the mechanism that makes it checkable rather than a new rule beside
it. The frontmatter is left at `approved` for the author to confirm at closeout, because in this
repository `approved` is not a terminal status and an amendment does not reopen a contract by
itself.

**Amended 2026-11-23 (`feat-0078`), pending the maintainer's approval.** The review now runs on
two independent axes, spec and standards (S-019 to S-022), and selects its own depth (S-023 and
S-024), absorbing the `review-depth` skill's selection rule so one skill decides how hard to look
and what a finding must prove. S-018 is reworded to name the depth step rather than the retired
skill, with its obligation unchanged. The Non-Goal on judging a spec is narrowed, because the spec
axis now judges one change against its contract; auditing a whole implementation scenario by
scenario remains `spec-conformance`'s. The Proposed Surface gains Axes and Depth rows, and the
Output row is amended. No existing scenario's obligation changes. The frontmatter stays at
`approved` per the `feat-0040` precedent; the new scenarios are not approved until the maintainer
says so.

**Amended 2026-11-24 (`feat-0093`), pending the maintainer's approval.** S-025 adds the re-check: a
review runs once, the author fixes once, and a second run reads only the first review's findings
(by signature) plus any blocker the fix introduced, then stops and hands what is still open to a
person. It answers the non-converging review loop the [sources delta](../reviews/2026-11-24-sources-delta.md)
records. The Modes row gains the re-check. No existing scenario's obligation changes; the skill's
wording behind several of them was compressed, and its conformance matrix was re-audited the same
day. The fig-leaf smell and the optional second reviewer from another model family are lens and
procedure guidance, not contract, and add no scenario. The frontmatter stays at `approved` per the
`feat-0040` precedent; S-025 is not approved until the maintainer says so.

Adding S-013 forced one further edit, recorded here rather than left to be noticed: S-002, S-003, and
S-004 each opened on "a request naming no scope", which a bare range satisfies, so on its own S-013
would have fired at the same time as S-002 with a different outcome. Their preconditions now read
"naming neither a path scope nor a range", which is what they meant when a bare range was not yet
contemplated. No behavior those three describe has changed.

## Problem

`house-review` is shipped, load-bearing, and composes a swappable lens, and it has no contract. Three
things about it are load-bearing and currently unstated anywhere a reader can check them.

It is **report-only**, which is the property an adopter most needs to be able to rely on: a review
skill that edits code is a different and much more dangerous tool. It **delegates its entire rubric**
to [`review-quality`](../../.agents/rules/review-quality.md), so the severities and categories an
adopter retunes live outside the skill and the skill's behavior changes when they do. And it
**resolves what to review** through a fallback chain that must not dead-end, because the most common
invocation ("review this") arrives with no scope at all.

None of that is asserted by a test or a contract today. A future edit could make the skill review
only the diff it was given, or hardcode a severity scheme, and nothing would object.

## Goals

1. Produce a severity-ranked review of real code, grounded in the changed lines rather than a summary.
2. Resolve what to review from an ambiguous request without dead-ending on the common cases.
3. Keep the review bar in a swappable lens, so an adopter retunes it in one file.
4. Leave the reviewed code unchanged.
5. Report coverage honestly when the change is too large to review completely.
6. Stay portable across harnesses, so the same findings are produced whatever channel carries them.
7. Make every citation in the review checkable against the file it names, so a reader can follow any
   finding to the code without trusting the reviewer.
8. Give every finding an identity that survives the code moving, so the same defect is countable
   across reviewers and runs.
9. Judge whether a change did what its contract asked, no more and no less, separately from whether
   it meets the repository's written standards, so neither judgement masks the other.
10. Spend review effort in proportion to a change's size and risk, from stated signals, so two runs
    over the same change reach the same depth for an inspectable reason.

## Non-Goals

- Applying, committing, or offering to apply the fixes it describes.
- Auditing a whole implementation against an approved spec, scenario by scenario, into a
  conformance matrix, which is `spec-conformance`; or judging whether tests are well designed, which
  is `test-quality`. The spec axis judges one change against its own contract and reports findings,
  not a matrix.
- Creating or editing a pull request, which is `pr-describe`.
- Running the test suite or any build command as part of forming the review.

## Constraints

- The rubric, the severity scheme, the validate-before-reporting protocol, the evidence shape, the
  evidence gate's branches, and the signature format live in the swappable `review-quality` lens,
  not in the skill. The skill composes them by reference.
- The spec-axis and standards-axis rules (categories, precedence of a repository standard over the
  rubric, citing the standard) live in the same lens. The depth signals and selection rule live in
  the skill.
- Counting how often a signature repeats across runs, and judging a repeated finding futile, are out
  of this contract. The skill emits signatures and reads nothing from them.
- Changeset resolution is shared with `pr-describe`, so "review this" and "describe this" resolve to
  the same range in the same repository state.
- The default output is Markdown, so the skill works in any harness. A harness may carry the same
  findings through its own structured findings channel instead.

## Scenarios

### Scenario S-001: an explicit path scope reviews the named files in full

- **Given** a request naming specific files, a directory, or a path glob
- **When** the skill runs
- **Then** it reviews those files as they currently stand, in full, computes no commit range, and does
  not widen the scope beyond what was named.

### Scenario S-012: a range supplied alongside a path scope narrows a change review

- **Given** a request naming both a path scope and an explicit base or commit range
- **When** the skill runs
- **Then** it reviews that range restricted to the named paths, as a change review rather than a
  full-file review, because a request naming a range is asking about a change.

### Scenario S-013: a bare explicit range is reviewed as given, not resolved

- **Given** a request naming an explicit base or commit range and no path scope, such as a single
  historical commit
- **When** the skill runs
- **Then** it reviews that range as a change review, without computing a merge-base range of its own,
  and reports the changeset as supplied rather than resolved, because a range does not carry any record
  of which of the two produced it.

### Scenario S-002: with neither a scope nor a range named, the branch's own range is reviewed

- **Given** a git repository with at least one commit, on a branch ahead of its merge-base with the
  default branch, and a request naming neither a path scope nor a range
- **When** the skill runs
- **Then** it reviews the committed range from that merge-base to `HEAD`, and notes any uncommitted
  changes as available to fold in rather than silently including or ignoring them.

### Scenario S-003: an empty committed range falls back to the working tree

- **Given** a request naming neither a path scope nor a range, where the committed range is empty,
  because the work sits on the default branch or is not yet committed
- **When** the skill runs
- **Then** it reviews the working-tree changes, tracked edits together with untracked files, rather
  than reporting that there is nothing to review.

### Scenario S-004: nothing to review is stated, not worked around

- **Given** a request naming neither a path scope nor a range, where both the committed range and the
  working tree are empty
- **When** the skill runs
- **Then** it states that there is nothing to review and stops, without selecting a substitute scope.

### Scenario S-005: the reviewed code is never modified

- **Given** any review, in any mode, including one whose findings each carry a concrete suggested fix
- **When** the skill finishes
- **Then** every reviewed file is byte-for-byte unchanged, no commit exists that the run created, and
  the suggested fixes appear only as text in the review.

### Scenario S-006: findings are ordered by severity and are individually actionable

- **Given** a review that produced findings at more than one severity
- **When** the review is written
- **Then** findings appear ordered from `blocker` to `nit`, grouped by file within a severity, and
  each carries a `file:line` anchor, the issue, why it matters, and a concrete suggested fix.

### Scenario S-007: a candidate finding that cannot be substantiated is dropped

- **Given** a candidate finding that the real code does not bear out, such as an unchecked input that
  is in fact validated elsewhere
- **When** the review is written
- **Then** that candidate does not appear in the review at any severity, rather than appearing with a
  hedge or a lowered severity.

### Scenario S-008: a clean change is reported as clean

- **Given** a review in which no candidate finding survives validation
- **When** the review is written
- **Then** it states plainly that the change looks clean and why, and reports no findings.

### Scenario S-009: the severity scheme comes from the lens, not the skill

- **Given** a `review-quality` lens whose severity names or rubric categories have been changed by an
  adopter
- **When** the skill runs
- **Then** the review uses the lens's current scheme, because the skill carries no independent copy of
  it.

### Scenario S-010: a change too large to review completely reports its coverage

- **Given** a change whose reviewable content exceeds what the run can read
- **When** the review is written
- **Then** the verdict line states how much was reviewed and the review names what was not read, so a
  partial review is never presented as a complete one.

### Scenario S-011: a structured findings channel changes the channel, not the findings

- **Given** a harness that provides its own structured findings output
- **When** the skill emits through that channel instead of Markdown
- **Then** the findings, their severities, and the validate-before-reporting rule are identical to the
  Markdown form; only the output channel differs.

### Scenario S-014: a finding whose quoted evidence resolves nowhere is dropped

- **Given** a candidate finding whose quoted code is not present anywhere in the file it cites, at
  the revision under review, or whose cited path does not resolve at all
- **When** the review is written
- **Then** that candidate is absent from the review entirely, rather than reported at a lower
  severity, hedged, or marked possible, and the review reports how many candidates the gate dropped
  without restating them.

### Scenario S-015: a quote found at a shifted line is re-anchored, not dropped

- **Given** a candidate finding whose quoted code is present in the cited file but at a different
  line than the citation states, because a later edit moved it
- **When** the review is written
- **Then** the finding is reported with its line corrected to where the text actually is, is marked
  as re-anchored, and keeps the same signature it would have had before the code moved, because the
  pointer drifted and the defect did not.

### Scenario S-016: a finding about something absent is citable

- **Given** a finding whose subject does not exist in the code, such as a missing test or an
  unhandled branch, so there is no offending line to quote
- **When** the review is written
- **Then** the finding is reported with a quote of the nearest anchor, a one-line statement of what
  is absent, and the rerunnable search that established the absence, and the gate admits it on that
  evidence rather than dropping it for having nothing to quote.

### Scenario S-017: every reported finding carries a stable signature

- **Given** any review that reports at least one finding
- **When** the review is written
- **Then** each finding carries a signature composed of its severity, its evidence path, its rubric
  category, and a slug of its summary, containing no line number, so the same defect reported by a
  second reviewer or in a later run produces the same signature.

### Scenario S-018: depth does not change what a finding must prove

- **Given** a review running at any depth, including the cheapest one
- **When** the review is written
- **Then** the evidence shape, the gate, and the drop-rather-than-hedge rule are applied unchanged,
  because depth sets how much is read and how exhaustively the rubric is swept, never the standard
  of proof a finding must meet.

### Scenario S-019: the spec axis reports missing, unasked-for, and wrong work against the contract

- **Given** a change with a contract (a spec, the task file the change completes, or the issue it
  closes)
- **When** the skill runs
- **Then** the spec axis reports requirements the change omits or only partly meets, behaviour the
  contract did not ask for, and requirements implemented incorrectly, each quoting the contract line
  it rests on, and each through the same evidence gate as any other finding.

### Scenario S-020: with no contract, the spec axis says so and stops

- **Given** a change for which no contract can be found and the user supplied none
- **When** the skill runs
- **Then** the spec axis reports that no contract is available and produces no findings, rather than
  inferring the intent from the diff and grading the change against itself.

### Scenario S-021: the standards axis reads the repository's written standards

- **Given** a target repository with a written standards file, such as `CODING_STANDARDS.md` or
  `CONTRIBUTING.md`
- **When** the skill runs
- **Then** the standards axis reviews the change against that file and the lens rubric, cites the
  standard (file and rule) in each finding resting on it, suppresses a rubric finding the
  repository's standard explicitly endorses, and labels a rubric finding with no written standard
  behind it as a judgement call.

### Scenario S-022: the two axes are independent and are not reranked

- **Given** any review that runs both axes, in a harness with or without subagents
- **When** the review is written
- **Then** each axis has its own section, verdict, severity ordering and worst finding, no single
  worst finding is named across both, and where no subagents exist the spec axis is finished and
  written down before the standards axis is read for.

### Scenario S-023: depth is chosen from stated signals, and an explicit depth wins

- **Given** a change and a request that either names `quick`, `standard` or `deep`, or names none
- **When** the skill runs
- **Then** a named depth is used as given, and otherwise the depth comes from the first matching
  rule over the stated signals (reviewable lines, directory spread, risk flags, blast radius,
  documentation-only scope), with the depth, the rule that fired, the excluded paths and any
  escalated files reported in the output; when a user's depth disagrees with detection, the
  detected depth is reported alongside without overriding it.

### Scenario S-024: an unmeasurable change is reviewed at standard depth

- **Given** a change for which a depth signal cannot be computed, or whose reviewable set is empty
  after exclusions
- **When** the skill selects a depth
- **Then** it selects `standard`, names the signal that failed, and does not fall through to
  `quick`.

### Scenario S-025: a re-check reads only the first review's findings, then stops

- **Given** a change that was reviewed, and one fix round the author made in answer to that review
- **When** the skill is asked whether the findings were fixed
- **Then** it re-reads only the first review's findings, by signature, against the fix's revision,
  marks each one fixed, open or disputed, reads the fix range only for a blocker the fix itself
  introduced, and stops: it does not run a new full review, and it hands every finding still open to
  a person rather than starting another round.

## Proposed Surface

| Element | Detail |
|---|---|
| Invocation | A request to review, optionally naming a path scope, a base, or a commit range |
| Modes | A re-check of an earlier review's findings after one fix round (S-025); explicit path scope (full-file review); explicit range with no path scope (change review over the range as given); a path scope plus a range (change review narrowed to those paths); or change review of the resolved default (when neither is named) |
| Range resolution | An explicit range if the request named one, else merge-base with the default branch, then working tree, then nothing to review. Which of the two produced the changeset is reported, as supplied or resolved |
| Severities | `blocker`, `major`, `minor`, `nit`, defined by the `review-quality` lens |
| Evidence | Per finding: path, line range, symbol where the file has one, and an exact quote, resolved against the revision under review. A finding about something absent carries an anchor quote, what is absent, and the search that established it |
| Signature | Per finding: `severity`, evidence path, rubric category slug, and a summary slug, joined by `\|`, carrying no line number. Format defined by the `review-quality` lens |
| Axes | Spec (against the contract: `spec-missing`, `spec-extra`, `spec-wrong`) and standards (against the repository's written standards plus the lens rubric), run as independent passes, never reranked against each other |
| Depth | `quick`, `standard` or `deep`, from an explicit request or rules R1 to R7 over five signals; risk-flagged files are anchors at `deep` with a re-measured remainder capped at `standard`; unmeasurable selects `standard` |
| Output | A header block (depth and rule, changeset and whether supplied or resolved, coverage, exclusions, sources per axis, gate drop count when anything was dropped), then a Spec section and a Standards section, each with its own verdict and inspected files and findings ordered by severity, each finding with `file:line`, its evidence, its signature, the issue, why, and fix |
| Side effects | None. No file is written, no commit is made |

## Open Questions

One, opened by the `feat-0040` amendment and stated at the end of this section. The `feat-0078`
and `feat-0093` amendments open none.

Both questions this spec originally opened were resolved by `chore-0012` on 2026-07-27: a range supplied
alongside a path scope narrows a change review to those paths (now `S-012`), and the name collision
was resolved by renaming the skill rather than by asserting a distinction. Re-approved by the author on 2026-07-27.

The `chore-0024` amendment on 2026-08-03 opens none. It closes a contradiction the table already
carried rather than deciding anything new, and it was re-approved on the same day.

The `feat-0040` amendment on 2026-08-05 opens one, deliberately left rather than decided here:
whether a finding dropped by the gate should be recoverable on request (a reviewer asked "what did
you drop?" has a reasonable question, and answering it hands over exactly the unverifiable claims
the gate removed). The contract states the count only. Whoever needs the other half should decide it
against a real case, not in advance.
