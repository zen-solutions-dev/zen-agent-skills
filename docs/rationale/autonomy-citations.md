# Autonomy module: citations and history

This document holds the record behind each rule in the autonomy module,
[`.agents/rules/autonomy.md`](../../.agents/rules/autonomy.md). It was moved here verbatim on
2026-10-20 by the kit refresh ([audit](../reviews/2026-10-kit-refresh-audit.md), findings 1.2 and
1.3), because Claude Code loads `~/.claude/rules/` into every session and the citations were most of
what that cost bought. Nothing below was reworded; only relative links were re-pointed so they still
resolve from here. The module keeps each rule's text, its scope, and a one-line pointer to its
source; this file keeps the evidence that admitted it.

The rule the module states about itself still holds: a rule that cannot be cited does not belong in
it. The citation moved; it did not go away.

## The module's original opening

This file is a **swappable module**, the third beside [`house-style.md`](../../.agents/rules/house-style.md) and
[`review-quality.md`](../../.agents/rules/review-quality.md). Those two govern how an agent writes and how it reviews.
This one governs what an agent may do **when nobody is watching**: in a worktree, in a batch, in a
cloud session, in any run where the answer to "should I?" cannot be a question put to a person.

**One rule here is not scoped that way, and the exception is stated at the top because it was
inherited rather than chosen.** `A10` governs what an agent may do with material it did not author,
and that is a property of the material rather than of the run. An agent reading a hostile diff in an
attended session acts on an embedded instruction exactly as one in a batch does, and the person
watching sees a tool call rather than a provenance violation. `A10` was added under this module's
unattended framing because its citation was an automated workflow, and the framing does not fit the
rule as written. **`A10` applies to every run, attended or not.** `A1` to `A9` keep the scope above.
Recorded 2026-08-29 by `feat-0064`, which found the rule reaching two of the eleven skills that read
outside-authored material, and all five of its referrers introducing it with "when this runs
unattended".

**Scope: universal.** Every skill in this kit references this module, and `validate-skills.py` fails
when one does not. A lens reaches an agent only through a skill that points at it, so a universal
lens that some skills never name is silently inert for exactly those skills. This module sat at five
of twenty-two referrers for the twenty-one days after `A10` landed, and every gate passed throughout,
because the only rule about lens composition asked whether **at least one** skill pointed at a lens.

It is separated from the skills so an adopter can retune the ceiling, or replace it with their own,
without touching skill logic. If you are adopting this kit: keep it, empty it, or rewrite it.

**v1 is a consolidation, not an invention.** Every rule below was already being applied somewhere in
this kit, in prose, one skill at a time, without the thing they have in common ever being named.

## The principle

> **Detect and report, never rewrite. The failure mode must be inaction.**

An unattended agent that does too little leaves work on the table, and a person picks it up. An
unattended agent that does too much destroys work nobody knew it touched, reports success, and the
loss surfaces later with no trace of what caused it. Those two failures are not symmetric, so the
rules below all lean the same way: **when uncertain, stop and say so.**

The principle is not new here. It is already applied in four independent places, and named in none
of them:

| Where | How it shows up |
|---|---|
| `doc-sync` | States it outright: dry run is the default, detection never changes a file, and a contract document is never edited because a disagreement there means the code is wrong. |
| [`review-quality.md`](../../.agents/rules/review-quality.md), protocol rule 6 | "Report only. State the findings and the suggested fixes. Do not edit or commit anything." |
| `scripts/install.py`, the `check()` docstring | Carries the sentence verbatim: "Detect and report, never rewrite. Re-installing is a person's decision." |
| `scripts/check-provenance.py` | Reports drift and never syncs, deliberately declining upstream's in-place rewrite, because every fold-in here was adapted and an overwrite would destroy the adaptation. |

Four independent authors of four unrelated components reached the same rule. That is the argument
for writing it down once.

## Why every rule here carries a citation

Each rule names where it was already exercised: a file and line, a task id, or a recorded incident.
**A rule that cannot be cited does not belong in v1.**

This is the evidence gate from [`review-quality.md`](../../.agents/rules/review-quality.md) applied to a rules module,
and it exists for one reason: an invented rule reads exactly like a consolidated one. Both are one
confident sentence in the imperative. Nothing about the prose distinguishes a constraint this kit
learned by losing work from a plausible-sounding rule someone thought of while writing this file, and
a module that mixes the two silently spends the authority of the first on the second.

**Decided 2026-08-27: an external incident satisfies this gate, if it is marked as one.** Every
citation in `A1` to `A9` is internal to this repository, so the first rule resting on someone else's
incident widens the gate, and the widening is recorded here rather than made quietly. The conditions
are that the incident is named, dated, and attributed to whoever reported it, so a reader can go and
check it, and that the rule says in its own *Cited* line that it rests on one. What does not change:
an external incident is evidence that the class is real, not that this kit has run into it, so a rule
admitted this way is marked the way `A8` is marked rather than dressed up as a consolidation. `A10`
is the first and so far the only rule admitted on one. (Updated 2026-11-23: `A11` is the second rule whose *Cited* line names outside research, alongside two internal exercises; see its entry below.)

References to files outside the installed skill tree are named in prose rather than linked, per the
portability contract in `AGENTS.md`: this module ships to adopters without this repository around it,
so a link that escapes the tree would resolve here and dangle everywhere it actually runs.

A skill is named in prose too, for the same reason one layer further in. A lens ships beside the
skills, and where the skills sit relative to it is not one answer: the plugin tree and an
`install.py` tree keep a `SKILL.md` per skill directory, while the cursor and vscode trees inline
every body into `.cursor/rules/` or `.github/prompts/` and leave no `SKILL.md` to point at. No one
link text resolves in all four, and `build-adapters.py` copies this module rather than rewriting it,
because the module is swappable and its text is the adopter's. `bug-0044` is what that cost: seven
links to a sibling skill's `SKILL.md`, correct here and dangling in every cursor and vscode tree the
kit had ever emitted.

## The citation for each rule

### A1

*Cited:* `fix-batch`, the dispatch-prompt section, states this verbatim and says why: worktree
isolation is a starting-state guarantee, not a runtime sandbox, and nothing stops a shell call from
going wherever it wants unless you say so directly. *The incident:* an agent in an isolated worktree
used a shell to reach outside it and overwrite a file in the main checkout with a stale copy,
destroying unrelated uncommitted work that had nothing to do with its task.

### A2

*Cited:* `fix-batch`, the verification step: "Confirm the changes touch only the files the task scoped
it to. Anything extra is a finding, not a bonus, investigate it, do not assume it is helpful just
because tests pass."

### A3

*Cited:* `scripts/install.py`, module docstring: "Never clobbers a real file it did not create: such
a target is reported CONFLICT and skipped for you to resolve." Pinned at contract level as `S-004` in
the `install` spec, and again as `S-010` in the `build-adapters` spec, where a rules file already
present in the target project is never overwritten. *The counter-example worth citing:* task
`bug-0018` is this rule failing in shipped code. `install.py` removes and replaces the rules
directory on re-install, so an adopter's edited lens is destroyed silently at exit 0, in the one file
the kit specifically asks them to make their own. The rule was written down in one half of the
distribution path and not implemented in the other.

### A10

*Cited by an external incident, and marked as such.* **Clinejection:** Cline's AI issue-triage
workflow, added 21 December 2025 and configured `allowed_non_write_users: "*"`, interpolated the
GitHub issue title straight into the agent's prompt, so an attacker-chosen title made the agent
`npm install` from a repository whose `preinstall` script poisoned the Actions cache and stole the npm
release token; an unauthorised `cline@2.3.0` was published on 17 February 2026. Adnan Khan, who found
it, names why the constraint belongs on the action rather than on inspection: "Since Claude runs `npm
install` via the Bash tool, there is no opportunity for the LLM to inspect what executes." **The form
is deliberate.** The rule follows the design-pattern formulation of Beurer-Kellner et al.
(arXiv:2506.08837): once an agent has ingested untrusted input, it must be constrained so that the
input cannot trigger any consequential action. A detector was rejected rather than overlooked, because
detection is published as broken by name: Zhan et al. (NAACL 2025 Findings, arXiv:2503.00061) broke
all eight defences they evaluated, and "The Attacker Moves Second" (arXiv:2510.09023) bypassed
twelve defences. The cost is the one those authors state plainly, and it is real here too: a
constrained agent cannot solve arbitrary tasks, and this rule will sometimes stop a run that was
never under attack.
**Unlike every rule above it, this one is not a consolidation of something this kit already did.**
Neither trigger the held section named has fired.

### A11

*Cited internally, with outside research for the class, and marked as such.* Added 2026-11-23 by
[`feat-0082`](../../.quests/done/feat-0082-an-agent-may-not-edit-its-own-judge.md), on the author's
decision. The rule rests on two kinds of evidence, and they answer different questions.

**That this kit already works this way.** Two closed tasks show the shape exercised rather than
invented. [`bug-0013`](../../.quests/done/bug-0013-validator-rejects-file-scheme-links.md) found half
of its own acceptance criterion wrong (a grep it expected to return three hits returned five) and
recorded that "rather than quietly satisfied", leaving the two extra hits alone because changing them
"would weaken a real check rather than fix this one".
[`bug-0010`](../../.quests/done/bug-0010-install-records-an-unresolved-home.md) met an assertion that
would fail on macOS for a correct reason and fixed it "by comparing resolved forms rather than by
loosening it until it passes". Neither names a rule; both obey this one.

**That the failure is real, and grows with capability.** ImpossibleBench (Ziqian Zhong, Aditi
Raghunathan and Nicholas Carlini, arXiv:2510.20270, submitted 23 October 2025, ICLR 2026) builds task
variants whose specification contradicts their unit tests, so any pass implies a shortcut, and
reports that frontier models frequently take one, editing or deleting the failing tests, with
stronger models cheating more. METR's "Recent Frontier Models Are Reward Hacking" (Sydney Von Arx,
Lawrence Chan and Elizabeth Barnes, 5 June 2025) documents models altering tests and scoring code and
reaching for the answer the scorer had already computed, while showing they knew this departed from
what the user wanted. This is the same gate widening `A10` used: published research is evidence that
the class is real, not that this kit has run into it, and the *Cited* line says so.

**The form is borrowed, and named.** The boundary half, that every done condition carries an unstated
"must not" beside it and that the builder "may not edit the acceptance conditions", follows
`skills/loop-design-check/SKILL.md` in Affaan Mustafa's everything-claude-code (MIT), read at commit
`25278e7` on 2026-10-28. Only the idea was taken; no text was adapted, so the module carries no
provenance block for it.

**Why every run, like `A10`.** Editing the check is as available to an attended agent as to an
unattended one, and the person watching sees a passing run rather than a changed judge. The rule
names a property of the judge, not of the run, so it takes `A10`'s scope rather than the module's
default.

### A4

*Cited:* `fix-batch`'s delegate evidence contract, the `validation command` and `validation result`
rows, established by task `feat-0041`. The reason recorded there is the whole point: "the validation
command and its result" cannot be answered in prose without either running it or lying.

### A5

*Cited:* `fix-batch`'s findings field states it directly: "`none` is a valid answer and is not the
same as silence." *Two recorded incidents, both from the same batch:* an agent fabricated an extra,
undisclosed test method that had never existed in the repository's history and then miscounted it as
one of the originals; and a different extra change initially looked like fabrication and was nearly
deleted, when it turned out to be a real, previously undiscovered bug fix the agent had found
opportunistically and never disclosed. Both directions cost the reviewer the same investigation, and
disclosure would have cost the agent one sentence.

### A6

*Cited:* `spec-conformance` requires a coverage proof and says an empty result is valid only
alongside the audited set, because "no divergence" requires positive evidence that the whole spec
was checked. *The incident:* a conformance matrix asserted it had audited "S-001 through S-014,
every spec item" beside a spec carrying fifteen scenarios, recorded in task `feat-0036`'s closeout
and named again in `chore-0033` as the reason to state both counts and the arithmetic rather than
the claim.

### A7

*Cited:* `verifier-agent`: "Independence is the point. Where the harness allows the separation, the
agent that verifies should not be the agent that wrote the implementation. Self-verification is the
failure mode this skill exists to remove."

### A9

**A9. Verify the commit you are working from before trusting anything you read, and disclose the
result.** (Ids are assigned in order of addition and rules are grouped by topic, so `A9` sits here,
beside the other evidence rules, rather than after `A8`. The ids are stable references: `fix-batch`
cites `A1`, `A2`, `A4`, and `A5`, `verifier-agent` cites `A7`, and the cloud runbook cites `A8`, so
renumbering to restore file order would break all of them.)

*Cited, twice on one day, from opposite ends.* On 2026-08-20 a cloud proof session was staged on a
branch cut from `main`, 99 files and 11,296 insertions behind `developer`, and implemented and
validated against `main`'s copies while its pull request targeted `developer`. GitHub reported the
pull request mergeable and clean throughout, because the one function it edited was byte-identical on
both branches. The cost was a false finding in a shipped report: it rediscovered `bug-0021`, already
fixed and already merged, and offered it as new. **The same day, from the other direction**, a branch
correctly cut from `developer` went red on all six CI cells because its target moved underneath it,
green on the branch and failing on the merge result. *The gap this closes:* `bug-0034` fixed both
neighbouring cases by putting the check in the **dispatcher's** hands, and deliberately declined to
put one in a per-agent prompt because that duplicates one diagnosis across N agents. Correct for a
batch, and it does not transfer: a lone unattended session has no dispatcher, so there is no other
end to put the check on. Recorded as `bug-0043`.

### A8

*Cited, with one honest qualification.* The shape is exercised: `pr-describe` is "draft text only,
never touches GitHub", printing both artifacts and surfacing the command rather than running it, so
the agent prepares and a person dispatches. **The specific ceiling, a `claude/` branch and a draft
pull request that is never merged, is a decision recorded in `ROADMAP.md` Campaign E rather than a rule
this kit has already run under.** It is the only rule in v1 in that position, it is named as such
rather than dressed up as consolidated, and confirming or amending it against a real unattended run
is the first job of v2.

**The one exception, added 2026-11-24 (`D1`).** An orchestrator may fast-forward an integration
branch to work it did not author, once an agent that is neither the author nor the orchestrator,
nor dispatched or briefed by the author, has passed that exact commit; only a person merges into
the base branch. Cited to the maintainer's decision `D1` in
[the Marjana plan](../reviews/2026-11-24-marjana-plan.md), approved in person on 2026-11-24, and to
the run it was written from: that round's orchestrator landed five workstreams this way, each at
the commit a fresh-context verifier passed. The guards were tightened while that run was under way,
after two of its landings had used orchestrator merge commits that the final text sends back to the
child; [the orchestrator's dogfood record](../reviews/2026-11-24-dogfood/orchestrator.md) says so.

**Two amendments, added 2026-11-25 (`feat-0102`).**

- **The mechanical merge (`B1`).** Retro proposal `R-201` of the
  [Marjana retro](../reviews/2026-11-24-retro-marjana.md) found that the 2026-11-24 orchestrator had
  landed WS-C and WS-B by its own merge commits while the text said such a landing goes back to the
  child, and that the send-back it then imposed on WS-E cost a round trip. It offered fast-forward
  only, or merges confined to generated files, ledger lines and planning documents. The maintainer
  chose "mechanical-only orchestrator merges, re-checked and listed in the PR"
  ([decisions](../reviews/2026-11-25-marjana-decisions.md), `A8` and `B1`). The rule takes the
  narrow reading: a ledger or planning conflict needs a choice of order or wording, which is
  judgement, so only a conflict a command resolves is mechanical. Re-deriving the two 2026-11-24
  merges with `git merge-tree` on 2026-11-25 showed both conflicted in `ROADMAP.md` and the plan
  document, and the second in a test file too, so this definition would have sent both back; the
  record is in [the round 2 rules dogfood](../reviews/2026-11-25-dogfood/rules.md).
- **Sampled self-merge (`C1`).** "Allow it per repository, opt-in, with sampling." It sits in `A8`
  because it is the one place an agent merges work it authored, and in `merge_policy` because that
  is the per-repository fact the skills already read. Default off, and off on any value a reader
  cannot parse, so a typo fails toward a person. The two-way-door list follows `pr-describe`'s merge
  danger, widened by the kit's own one-way surfaces (approved specs, the acceptance command, CI and
  hook configuration). Sampling was first written as "pull request number divisible by N"; at the
  check-in gate on 2026-11-25 the maintainer approved the wording and changed that one point:
  sampling must be random. It is now the merge commit's full sha, read as a hexadecimal integer,
  divisible by N: unpredictable before the merge, because the platform creates the commit, and
  checkable by anyone after it. A pull request number is known in advance, so an agent could have
  steered which of its merges a person sees. Not yet run anywhere: a decision, not a consolidation.

## Considered for v1 and held, for want of a citation

The gate is only real if it excludes things. These were wanted and left out, because this kit has not
run into them yet and a plausible number is not evidence. One of the four has since been discharged,
and it stays listed with the reason, because a gate that can be emptied quietly is not a gate:

- **Retry limits and futility classification.** Scoped as task `feat-0042`, which states honestly
  that it is preventive rather than observed, and carries its own kill criterion.
- **Token, wall-clock, or compute budgets.** Held as Campaign E item 7, behind the batch mode, because a
  bound with no observed run to calibrate against is a guess with a number on it.
- **Escalation paths, meaning when an unattended agent should stop and wait for a person rather than
  reporting and finishing.** Real, and currently unanswerable: nothing here has run unattended long
  enough to know where the line falls.
- **Instructions embedded in material a skill was pointed at. Discharged on 2026-08-27 as `A10`, and
  not by the route this entry named.** Neither stated trigger fired: no skill here has yet been
  pointed at material from outside the maintainer's control, and nothing has come through the private
  channel `SECURITY.md` opens. What changed is the gate rather than the evidence. Per the decision
  recorded above, an external incident (Clinejection) was accepted as the citation, and the rule is
  marked as resting on one. The entry is kept here rather than deleted so that the discharge, and the
  route it took, are both on record.
