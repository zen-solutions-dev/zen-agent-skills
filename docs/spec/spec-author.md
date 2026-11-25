---
title: spec-author
status: approved
---

# spec-author

Behavioral contract for the `spec-author` skill (ROADMAP Campaign B item 2). Drafted 2026-07-24
and reviewed with the `spec-quality` lens as the first in-kit dogfood of that skill.

## Problem

The kit can turn a rough idea into atomic task files with [`new-quest`](../../.agents/skills/new-quest/SKILL.md),
and it now has a [`spec-quality`](../../.agents/skills/spec-quality/SKILL.md) lens for reviewing
scenario-based specs. But nothing drafts the spec in the first place. Ideas jump straight to tasks
with no durable behavioral contract, so intent is not captured before decomposition and there is
nothing for `spec-quality` or a later conformance audit to check against. The contract-driven spine
has a lens but no author.

## Goals

1. Draft a persistent spec document from a raw idea, capturing problem, goals, non-goals,
   constraints, scenarios, proposed surface, and open questions.
2. Compose the `spec-quality` lens so the returned draft has a `spec-quality` verdict of `ready`.
3. Represent an explicit human approval state that downstream decomposition can gate on.
4. Align with the person before drafting: settle every decision the contract depends on through a
   structured interview, or take it from a decisions record the person already confirmed in this
   conversation, so the draft records decisions the person made rather than assumptions.

## Non-Goals

- Decomposing the spec into task files. That is `new-quest`.
- Writing implementation code, tests, or architecture.
- Choosing implementation strategy or file layout.

## Constraints

- Specs are Markdown with YAML frontmatter, named `<slug>.md`, and are written to the repository's
  existing spec location when it has one, so a run adopts the convention already in place rather
  than imposing a second one. `docs/spec/<slug>.md` is the documented fallback, used only when the
  repository has no spec location of its own.
- The skill composes `spec-quality` rather than restating its rules inline.
- The interview follows the `grill` skill's mechanism and is composed from it rather than designed
  anew.
- Specification work is read-only for implementation surfaces: a run creates or edits only the spec
  file, never implementation source.
- Frontmatter carries a `status` field whose value is one of `draft` or `approved`. `approved` is
  set only by a human; `spec-author` never sets `approved` itself.
- An approval is tied to the text approved: the human approving records `approved_digest`, the
  digest the skill's `scripts/spec_digest.py` prints, and `spec-author` never writes or changes it.

## Scenarios

### Scenario S-001: draft from a raw idea

- **Given** a one-line feature idea and no existing spec
- **When** spec-author runs
- **Then** it writes a Markdown file named `<slug>.md` to the repository's spec location, containing
  frontmatter with `status: draft` and all seven body sections (Problem, Goals, Non-Goals,
  Constraints, Scenarios, Proposed Surface, Open Questions), with at least one scenario carrying a
  stable `S-NNN` id.

### Scenario S-002: self-check with spec-quality

- **Given** a drafted spec that a first pass of the `spec-quality` lens would return as
  `needs_revision`
- **When** spec-author finishes drafting
- **Then** it revises the draft and re-checks until the `spec-quality` verdict is `ready`, and the
  file it writes is the `ready` version.

### Scenario S-003: approval gate before decomposition

- **Given** a spec whose frontmatter `status` is `draft`
- **When** `new-quest` is asked to decompose it
- **Then** `new-quest` refuses and reports that the spec is not `approved`.

### Scenario S-004: read-only for implementation surfaces

- **Given** any drafting run
- **When** spec-author completes
- **Then** the only file created or modified is the spec in the repository's spec location, and no
  implementation source file is written.

### Scenario S-005: retired

Retired on 2026-11-23 by `feat-0076` and superseded by `S-008`. It specified exactly one clarifying
question, only for an idea too vague to yield a contract. The id is kept so it is never reused.

### Scenario S-006: the spec goes where the repository already keeps specs

- **Given** a repository that already keeps its specs in a directory of its own
- **When** spec-author writes the spec
- **Then** it writes the spec into that directory.

### Scenario S-007: a repository with no spec directory gets the documented fallback

- **Given** a repository with no spec directory of its own
- **When** spec-author writes the spec
- **Then** it writes the spec to `docs/spec/<slug>.md`.

### Scenario S-008: the interview settles decisions before any file is written

- **Given** a source request that leaves at least one decision open which the contract depends on
- **When** spec-author runs
- **Then** before writing any file it asks the person numbered questions in rounds, each question
  carrying a recommended answer worded so that "yes" accepts it, and it writes the spec only after
  no open decision remains and the person has confirmed the shared understanding.

### Scenario S-009: facts are looked up, not asked

- **Given** an open point the repository can answer (what the code does, which files exist, what a
  command prints)
- **When** spec-author interviews the person
- **Then** no question put to the person asks for that fact, and the fact is recorded with where it
  was found.

### Scenario S-010: approved text edited after its approval is not decomposed

- **Given** a spec with `status: approved` whose `approved_digest` no longer matches its text
- **When** `new-quest` is asked to decompose it
- **Then** `new-quest` refuses and reports that the approved text changed and waits on re-approval.

### Scenario S-011: an amendment leaves the approval record alone

- **Given** an approved spec carrying an `approved_digest`
- **When** spec-author amends it
- **Then** it leaves `status` and `approved_digest` exactly as they were, adds a dated note naming
  the amendment as pending re-approval, and reports that the spec now reads `changed` until the
  person re-approves it.

### Scenario S-012: a confirmed decisions record skips the interview

- **Given** a conversation that already holds a `grill` decisions record for the request, which the
  person confirmed and which settles every decision the contract depends on
- **When** spec-author runs
- **Then** it asks the person no question that record settled, names the record it drafted from, and
  writes each of the record's deferred decisions as an Open Question.

## Proposed Surface

| Element | Detail |
|---|---|
| Output file | `<slug>.md`, Markdown with YAML frontmatter, written to the repository's existing spec location, which is the `spec_dir` of `docs/agents/zen.md` when that file sets it; `docs/spec/<slug>.md` when the repository has none |
| Frontmatter `status` | `draft` (author-set) or `approved` (human-set only) |
| Frontmatter `approved_digest` | `sha256:` plus 64 hex digits, the digest of the approved text as `scripts/spec_digest.py` prints it; human-set only, never written or changed by the skill |
| `scripts/spec_digest.py` | read-only: prints a spec's verdict (`bound`, `unbound`, `changed`, `malformed`, `not-approved`, `unreadable`) and digest; `--queue <directory>` lists approved specs waiting on re-approval |
| Body sections | Problem, Goals, Non-Goals, Constraints, Scenarios, Proposed Surface, Open Questions |
| Scenario ids | stable `S-NNN`, never renumbered; a retired id stays in place, marked retired |
| Interview round | numbered questions, each with a recommended answer worded so "yes" accepts it; ends when no open decision remains and the person confirms |
| Synthesise-only mode | taken when this conversation holds a confirmed `grill` decisions record for the request; no interview round for what the record settled, and a round only for a decision it left unsettled |

## Open Questions

None.

Amended on 2026-08-05 by `chore-0027` and re-checked to `ready` with the `spec-quality` lens: the
Constraints, the Proposed Surface output-file row, and scenarios `S-001` and `S-004` now say the
spec is written to the repository's spec location rather than to a fixed path, and two new
scenarios state which location that is, `S-006` for a repository that already keeps specs somewhere
and `S-007` for the `docs/spec/<slug>.md` fallback. No existing id was renumbered or reused. This
closes the single divergence recorded in
[`spec-author.conformance.md`](spec-author.conformance.md). The contract had lagged the skill rather
than the skill having erred: this spec was written for this repository before `spec-author` was
generalised to run in repositories that already keep specs somewhere of their own. The amendment
decided nothing new, and it needs a maintainer's re-approval.

Amended on 2026-11-23 by `feat-0076` and re-checked to `ready` with the `spec-quality` lens: Goal 4
and a Constraint make the skill interview the person before drafting, by composing `grill`;
`S-005` (exactly one clarifying question) is retired and superseded by `S-008` (rounds of numbered
questions with recommendations until no decision is open and the person confirms) and `S-009`
(facts are looked up, never asked); the Proposed Surface gains an interview-round row and states
how a retired id is kept. No id was renumbered or reused. `status` is deliberately left `approved`:
**this amendment changes behavior and is pending the maintainer's re-approval.**

Amended on 2026-11-23 by `feat-0083`: an approval is now tied to the text a person approved. A
Constraint, two Proposed Surface rows (`approved_digest` and the read-only `scripts/spec_digest.py`),
and two scenarios are added: `S-010` (approved text edited since approval is not decomposed) and
`S-011` (an amendment leaves the approval record alone). No id was renumbered or reused. `status` is
deliberately left `approved`: **this amendment changes behavior and is pending the maintainer's
re-approval.** Nothing here binds this spec's own text; by the maintainer's decision, every spec
approved before this amendment stays unbound until the maintainer re-reads it.

Amended on 2026-11-24 by `feat-0091`: the repository's spec location is read from the `spec_dir`
key of `docs/agents/zen.md` when that file sets it, before any discovery, and the run says which
source it used (the per-repository setup file is specified in [`zen-config.md`](zen-config.md)).
Only the Proposed Surface output-file row changes; `S-006` is unchanged in wording and now covers a
configured location as well as a discovered one. No id was renumbered or reused. `status` is
deliberately left `approved`: **this amendment changes behavior and is pending the maintainer's
re-approval.**

Amended on 2026-11-25 by `feat-0105`: a synthesise-only mode. Goal 4 also accepts a decisions record
the person already confirmed in this conversation; `S-012` (a confirmed decisions record skips the
interview) and a Proposed Surface row are added. `S-008` is unchanged: a decision the record leaves
open is still put to the person before any file is written. No id was renumbered or reused. `status`
is deliberately left `approved`: **this amendment changes behavior and is pending the maintainer's
re-approval.**

Amended again on 2026-11-25 by `feat-0105`, by the maintainer's decision that day: the Constraint on
the interview no longer says that the skill runs `grill`'s mechanism inline when `grill` is not
installed. The skill has carried no inline fallback since `feat-0084`, and `install.py` always places
`grill` with `spec-author` because the skill links it. No scenario or id changes. Pending the
maintainer's re-approval with the amendment above.
