# AGENTS.md: rationale and history

The reasons and incidents behind rules in [`AGENTS.md`](../../AGENTS.md), moved here verbatim on
2026-10-20 by the kit refresh ([audit](../reviews/2026-10-kit-refresh-audit.md), finding 6.2).
`CLAUDE.md` now imports `AGENTS.md`, so every Claude Code session in this repository loads it at
launch, and about 30 percent of its words were history rather than rule. Each rule in `AGENTS.md`
still stands where it was; this file keeps the evidence for it. Nothing below was reworded; only
relative links were re-pointed so they resolve from here.

On 2026-11-24 `chore-0100` cut `AGENTS.md` to rules only and moved what it condensed to the end of this file, under "The rule text as it stood before 2026-11-24", with the former `_comment` of `.claude/settings.json` just before it.

## Why some scripts are not distribution scripts

Recorded 2026-08-28 by `chore-0076`, which needed a local store and a local server for [`docs/spec/agent-observatory.md`](../../docs/spec/agent-observatory.md); the sentence above had read as though every script were a distribution script, and five documents said so in five different scopes.

## Why the closeout list has its re-anchor, `doc-sync`, and conformance steps

The re-anchoring clause is in that list because the move silently invalidates every link in the file: a task authored in `.tasks/` correctly links to `../scripts/x.py`, and from `.tasks/done/` that same text means `.tasks/scripts/x.py`. `bug-0011` found 101 links across 36 completed tasks broken exactly this way, with `validate.py --strict` and the CI docs link step both passing, because neither looked here. `validate.py` now checks every link against the directory the file is actually in, so the move fails loudly.

The `doc-sync` step is in that list because its absence has cost real work. `feat-0031` shipped a user-facing feature that was dogfooded, given a conformance matrix and a verification record, and left every reader-facing document with zero mention of it. Updating `CHANGELOG.md` and the task file is bookkeeping, not documentation: a feature only a maintainer can find out about has not shipped for anyone else.

The conformance step is in that list because nothing else here asks whether the implementation matches the contract. A task that declares a `spec` closes by producing or updating that spec's `<spec>.conformance.md` with [`spec-conformance`](../../.agents/skills/spec-conformance/SKILL.md), over the scenarios its `scenarios` field claims. **Deferring is legal, and for a forward spec it is the only honest answer**: a contract written before its implementation has nothing to audit yet, so a scenario nothing has built is recorded as not-built with what is owed, and a spec with no implementation at all keeps its matrix owed, said plainly in the task rather than invented. A matrix written to satisfy this step is worse than no matrix. `cloud-executable` is the incident: approved 2026-08-07, with `feat-0045` and `feat-0046` both closed against it, it reached 2026-08-19 as the only approved spec of eleven with no matrix at all, having passed every stated obligation at both closeouts because no stated obligation mentioned the contract.

## How the lens-shape rule came to be enforced

The enforcement is new because the list was wrong, and how wrong is worth keeping. Until
`chore-0069` this rule named three lenses and was right about one: `spec-quality` carried the shape,
`test-quality` did not, and `review-quality.md` was never in this section's scope at all, since this
section opens by saying what a skill *directory* contains and that file is a rules module under
`.agents/rules/`, governed by the layout table above and the lens rules below. Two skills the rule
never named were shaped exactly as it prescribed, `spec-conformance` and `spec-plan-readiness`, and
the second of those calls itself a gate rather than a lens, so nothing classifies it either way.
Measured again on 2026-08-31: three skills declare themselves lenses (`spec-conformance`,
`spec-quality`, `test-quality`), and one of the three is reported.

That one report is `test-quality`, and it is left standing rather than cleared. Its headings are a
rubric (`Goal`, `Core rules`, `Review checklist`, `Commit gate`, `Reporting`), so the shape rule's
letter is broken there and its stated harm is not: it carries no procedure for an agent to run.
Which way that settles, reshaping the skill or rewording its declaration, is a change to the skill
rather than to this file, and renaming its headings to clear the warning would be satisfying the
validator instead of the rule.

**Settled 2026-11-23 by `feat-0077`.** The 2026-11 overhaul decided the question the paragraph above
left open: `test-quality` is a lens, so its body was reshaped into `Intent`, `Workflow` and `Output`
around the same rubric, and the warning cleared because the skill changed, not its headings' names.
No shipped skill trips the shape rule today.

The paragraph that rule replaced in `AGENTS.md`, as it stood:

**A skill's shape is declared in the skill and enforced by
[`validate-skills.py`](../../scripts/validate-skills.py), not listed here.** A lens says so in its own
body, in the form the bodies already use ("This skill is a lens", "This is a lens"), and the
validator reads that declaration and warns when the headings underneath it are a workflow's. The
declaration is what makes the check falsifiable: inferring the intended shape from the headings
would make every skill conform by construction, and a check that cannot fail is unchecked. A list
here would pass the day another lens is added and nobody edits it, which is the failure the
universal-lens rule below was filed for.

## How the universal-lens rule came to be enforced

The enforcement is new and the reason is worth keeping. This rule existed here in prose and nothing
checked it, so its two halves had drifted a long way apart without either being visible: on
2026-08-29 `house-style.md` was referenced by all twenty-two skills, which is discipline rather than
a guarantee, and `autonomy.md` by five, for the twenty-one days since `A10`, the kit's only rule
about material an agent did not author, was added to it. Every gate passed throughout, because the
only lens rule in the validator asked whether **at least one** skill pointed at a module and one
always did (`feat-0064`).

The paragraph that rule replaced in `AGENTS.md`, as it stood:

**Universality is declared in the lens and enforced by
[`validate-skills.py`](../../scripts/validate-skills.py), not listed here.** A list in this file, or in
that script, passes the day a fourth lens is added and nobody edits it, which is the failure
`feat-0048` was filed for. A lens that wants the stronger rule says so in its opening; one that says
nothing is topical and is still covered by the at-least-one rule.

## What the gates cannot see, by incident

**The other insufficiency is the one more runs do not close.** The paragraph above is about coverage
across the CI matrix, which a second platform closes. This one does not: every gate here decides a
mechanical property, and the defects below all sat outside what any of them sees. `bug-0045` emptied
`.agents/skills/`, `tests/`, and the `.tasks/` task files and reran this command; six of seven gates
reported `ok` over a repository holding nothing. `bug-0044` found seven links that resolve here and
dangle in every `cursor` and `vscode` tree the adapter builder ships, having "survived every gate".
`bug-0037` found three of sixty-five citations in a conformance matrix pointing at something other
than what they claimed, and why nothing could report it: the tests match on content and the link
check resolves paths, so neither sees a line anchor. The gates are healthy and catch what they were
built to catch; the claim is about what they cannot see, so read a green run as evidence about the
mechanical layer and nothing else. Buy the rest by hand, cheapest first: **construct the empty or
degenerate input and see what the tool actually says**, as `bug-0045` did by emptying the tree and
`bug-0046` did by renaming one `.md` to `.MD`, which carried two of eight provenance records out of
the run at exit 0. A check that cannot fail is unchecked, whatever it printed.

## Why the one hook registration is committed

The reason is mechanical rather than a preference. A user-level `~/.claude/settings.json` does not reach a cloud session, and a cloud session is the exact case this hook exists for: it clones the repository, gets none of the user-scope skills this kit installs, and would otherwise work without them and never say so. Verified against Anthropic's Claude Code documentation on 2026-08-07, which states the same thing from the other side by telling readers to commit settings files to change a cloud session's settings. A printed registration cannot be pasted by a machine that nobody is watching.

## Why the hook interpreter is a fallback (`bug-0050`)

The fallback replaced a one-sided `python3`, and the correction is worth recording because the reasoning was sound and the conclusion was wrong (`bug-0050`). `python3` was chosen as the portable default for the cloud sessions this exception exists for, with the Windows hazard known and stated: there `python3` is the Microsoft Store alias, a stub that advertises an install and exits without running anything. Both halves were true. What was wrong was the sentence joining them, that a static JSON file cannot probe and so cannot be right on both platforms at once. **It does not need to probe.** The cost of believing it was counted rather than estimated: the observatory's health report found this hook had exited non-zero on every session start in this checkout from 2026-08-07 to 2026-08-29, fourteen distinct failures, silent throughout, because a reminder must exit cleanly whatever happens. The one hook this repository commits, for the one argument that justified committing it, had never run.

## Why commits carry no co-author trailer

The reason is mechanical rather than stylistic. The `main protection` ruleset sets
`require_extra_approval_for_unattributed_changes`, so a commit trailer naming an identity with no
GitHub account marks the change unattributed and demands an extra approving review. The only human
here is also the author of every pull request, and **GitHub does not let a pull request author approve
their own pull request**, so the requirement cannot be satisfied as configured. On 2026-08-21 that
deadlocked the `developer` to `main` sync, 68 commits of which 44 carried the trailer, and it took an
admin bypass to land. The bypass stays available to the repository owner and the rule stays enforced
for everyone else; dropping the trailer is what keeps the rule from firing on work that is not
actually unattributed.

## Why the provenance convention exists

A meaningful share of this kit was adapted from somewhere else, and prose credit alone decays into folklore. `ROADMAP.md` once credited `doc-sync` to an upstream `document` workflow that was never vendored here, and the only surviving trace of the real contract was one line inside a gitignored folder that no longer exists. The attribution went wrong in under two weeks, and nothing could check it.

## Why the provenance check does not sync

Upstream's own `sync-maintainability-review.mjs` rewrites its vendored region in place, which is correct for verbatim vendoring and wrong here, because every fold-in in this kit was house-styled and retargeted and an overwrite would destroy the adaptation.

## Why .claude/settings.json says what it says

The `_comment` array of [`.claude/settings.json`](../../.claude/settings.json), moved here verbatim on 2026-11-24 by [`chore-0100`](../../.quests/done/chore-0100-marjana-context-and-ledgers.md), which left a five-line pointer in its place. It explains the one committed hook, its repository-relative path, the `python3 || python` fallback (`bug-0050`), and the two non-hook keys, `worktree.baseRef` and `attribution.commit`.

```text
Project-scope Claude Code settings for this repository, checked in deliberately.

This is the ONE place the kit activates a hook on someone's behalf rather than
printing a registration for them to paste. The conventions section of AGENTS.md
records why, beside the opt-in rule it bends. In short: a user-level registration
does not reach a cloud session, and a cloud session is the exact case this hook
exists for, so there is no other mechanism that works where it is needed.

Scoped as narrowly as the exception allows. One hook, in the reminder shape, which
never blocks and never writes: the worst case is one injected paragraph telling you
something you already knew. It fires only on a genuinely new session, not on resume,
clear, compact, or fork.

The path is repository-relative on purpose. install.py's printed registration uses an
absolute path into the user's home, because that copy is placed there; this one points
at the hook in the checkout, so a fresh clone runs it with nothing installed at all,
which is the state it reports on.

The interpreter is a fallback, `python3` then `python`, and that shape replaces a
deliberate one-sided choice this file used to defend at length (bug-0050).

The history is worth keeping because the reasoning was sound and the conclusion was
wrong. python3 was chosen as the portable default: this file exists to reach CLOUD
sessions, which run on Linux, where many distributions ship no `python` at all, and
macOS has not shipped one since 12.3. The hazard in the other direction was known and
observed rather than argued: feat-0038 hit the registered-and-inert failure on Windows,
where `python3` resolves to the Microsoft Store alias, the hook never launched, nothing
was emitted, and the session proceeded looking exactly as it would if skills were
reachable. Both halves are true. What was wrong was the sentence that followed them:
"A static JSON file cannot probe, so this cannot be right on both platforms at once."

It does not need to probe. A shell fallback is right on both, and the trade was never
necessary. Measured on Windows on 2026-08-31: `python3 <hook>` exits 9009 writing only
to stderr, so stdout stays clean, and `python3 <hook> || python <hook>` then runs the
real interpreter with stdin intact and emits the hook's single JSON object. On Linux and
macOS the first command succeeds and the second never runs.

The cost of the one-sided choice was counted rather than estimated, and it is why this
is a bug rather than a preference: the observatory's health report found this hook had
exited non-zero on EVERY session start in this checkout from 2026-08-07 to 2026-08-29,
14 distinct failures, silent throughout because a reminder must exit cleanly whatever
happens. The one hook this repository commits, for the one argument that justified
committing it, had never run.

The fallback is safe only because of the hooks module contract, and that is the bound.
A hook here ALWAYS exits 0, including on failure, so the only way the second command is
ever reached is the first interpreter never starting. A hook that exited non-zero after
writing to stdout would run twice and emit two objects, which corrupts the exchange. If
a future hook is registered here, that contract is what makes this shape legal.

`install.py`'s hook_interpreter() picks one name per platform, which it can because it
runs at registration time and knows the machine. This file cannot, and no longer has to.

Contract for the module: .agents/hooks/README.md

Two non-hook keys were added by the 2026-10 kit refresh, and neither is a hook, so the
one-hook exception above is unchanged (docs/reviews/2026-10-kit-refresh-audit.md):

worktree.baseRef = head. Subagent and --worktree worktrees otherwise branch from
origin's default branch, which is how fix-batch recorded three waves cut from main while
the dispatch branch was developer (finding 3.5). With head they start from the session's
own HEAD. fix-batch still pins an explicit sha, because other harnesses have no setting.

attribution.commit = empty. Claude Code adds a Co-Authored-By trailer by default, and
AGENTS.md forbids it here because it deadlocks the main protection ruleset (finding
4.3). Setting it removes the default at the source instead of relying on every agent to
remember the rule. Pull request attribution is left at its default.
```

## The rule text as it stood before 2026-11-24

[`chore-0100`](../../.quests/done/chore-0100-marjana-context-and-ledgers.md) cut `AGENTS.md` from 27,822 bytes to rules only, because every session in this repository loads it ([inventory, `P1`](../reviews/2026-11-24-marjana-inventory.md)). The paragraphs it condensed are kept below verbatim, links re-anchored for this directory, so no rule and no reason is lost. The provenance convention moved to [`CONTRIBUTING.md`](../../CONTRIBUTING.md#provenance-for-material-folded-in-from-elsewhere). Where a paragraph here and `AGENTS.md` differ, `AGENTS.md` is the rule.

### Header

Canonical rules for every AI agent working in this repository (Claude Code, Cursor, Codex, OpenCode, and any tool that reads `AGENTS.md`). This is the single source of truth. `CLAUDE.md` imports this file with `@AGENTS.md`, so Claude Code loads it at launch; any `.cursor/rules/*.mdc` or `.github/copilot-instructions.md` here is a thin pointer back to it. The reasons and incidents behind these rules are kept in [`docs/rationale/agents-md.md`](agents-md.md), so this file can stay short.

This repo is **Zen Agent Skills**: a portable, cross-harness library of agent skills, plus the tooling to install them into any project and any AI coding tool. It dogfoods its own system: this repository is tracked with the same `init-worktracking` skill it ships. Strategy lives in [`ROADMAP.md`](../../ROADMAP.md); atomic work lives in [`.tasks/`](../../.quests/); completed work is logged in [`CHANGELOG.md`](../../CHANGELOG.md).

### What this repository is, and the layout

A skills library, not an application. The deliverables are the skills under [`.agents/skills/`](../../.agents/skills/) and the tooling under [`scripts/`](../../scripts/) that distributes them. Success is measured by whether a skill is portable (works across harnesses), self-contained (needs no hidden context), and genuinely used and iterated on.

**Not every script distributes a skill.** Some tooling under `scripts/` serves the maintainer of this repository and is not a deliverable: [`install.py`](../../scripts/install.py) never places it, no adopter receives it, and the portability contract in the portability-contract section therefore does not reach it. It is still bound by the stdlib rule in the conventions section, so it runs on a bare Python 3 with no install step like everything else here.

## 2. Layout

| Path | Holds |
|---|---|
| [`.agents/skills/`](../../.agents/skills/) | The skills. One directory per skill, each with a `SKILL.md` harness-agnostic body. |
| [`.agents/rules/`](../../.agents/rules/) | The swappable lenses skills compose: [`house-style.md`](../../.agents/rules/house-style.md) for writing and formatting, [`review-quality.md`](../../.agents/rules/review-quality.md) for the review rubric and severities, [`autonomy.md`](../../.agents/rules/autonomy.md) for what an agent may do when nobody is watching, and, in `A10` and `A11`, for what it may do with material it did not author and with the check that judges its work, on any run at all, and [`writing-for-agents.md`](../../.agents/rules/writing-for-agents.md) for how a document behaves when an agent reads it, the yardstick for every `SKILL.md` and for this file. Each lens carries `paths` frontmatter so Claude Code loads it only when a skill reads it; [`core.md`](../../.agents/rules/core.md) is the one always-loaded file, one line per rule, held under a line budget by `validate-skills.py`. Adopters may replace any of them. Shipped alongside the skills by `install.py`, which places them in `~/.claude/rules/`, because a skill that references a lens is not self-contained without it. |
| [`.agents/hooks/`](../../.agents/hooks/) | Optional runtime guardrails (Python on stdin), each a *reminder* (injects context, never blocks) or a *gate* (blocks, only when the condition is decidable from the payload). The only thing the kit ships that runs inside an adopter's session, so installation is opt-in and activation is theirs: `install.py --with-hooks` places the files and prints the registration rather than editing anyone's settings. Contract in [`.agents/hooks/README.md`](../../.agents/hooks/README.md). |
| [`.claude-plugin/`](../../.claude-plugin/) | The committed Claude Code marketplace: the shipped skills and the lenses as one plugin, generated by `build-adapters.py --marketplace` and never edited by hand. A gate fails when it differs from what would be generated, so a change to a shipped skill or a lens regenerates it in the same commit. |
| [`scripts/`](../../scripts/) | Two kinds, and which kind a thing is matters more than the list. **Distribution tooling**, a deliverable, which ships the kit: `install.py`, `build-adapters.py`, `validate-skills.py`, `check-provenance.py`, `run-checks.py`, `check-citations.py`. **Maintainer tooling**, which reaches no adopter tree and which `install.py` never places: `observatory/`, a local reporting surface over this repository's own session corpus, contracted by [`agent-observatory.md`](../spec/agent-observatory.md). What decides the kind is whether an adopter receives it, not where it sits, and the stdlib rule in the conventions section governs both. **Membership is the term here, not the enumeration**: a script added or retired needs no amendment to this row, per the precedent [`chore-0049`](../../.quests/done/chore-0049-a-checker-for-conformance-matrix-citations.md) set when a gate count went stale the first time anyone added a gate. |
| [`.tasks/`](../../.quests/) | Atomic, agent-assignable work items for building this kit, plus `validate.py`. |
| [`docs/spec/`](../spec/) | Behavioral specifications (the contracts), plus the reports that sit beside them, one file kind per question asked: `<spec>.conformance.md` audits code against the contract, `<spec>.verification.md` records a verdict with evidence, `<spec>.readiness.md` records a go/no-go gate over a spec plus its task decomposition, `<spec>.characterization.md` records behavior pinned before a contract existed, `<spec>.runbook.md` tells a person how to perform a step no agent here can perform. |
| [`tests/`](../../tests/) | The kit's own tests, derived from the specifications under `docs/spec/`. |
| [`ROADMAP.md`](../../ROADMAP.md) | The strategic plan: which skills get built, in what order (builder-facing). |
| [`CHANGELOG.md`](../../CHANGELOG.md) | Append-only ledger of finished work. |
| [`docs/CATALOG.md`](../CATALOG.md) | The reader-facing narrative catalog (what the kit offers, for people browsing it). |

`ROADMAP.md` and `docs/CATALOG.md` overlap by design: `CATALOG.md` is the narrative for readers of the kit; `ROADMAP.md` is the execution order for whoever is building it. When they disagree, `ROADMAP.md` is authoritative for what happens next.

### Work altitude and lifecycle

| Altitude | Tier | Lives in |
|---|---|---|
| 30,000 ft | Epic (a tier of the catalog) | `ROADMAP.md` sections |
| 10,000 ft | Feature (one skill) | `ROADMAP.md` forward-plan items |
| 1,000 ft | Task | `.tasks/<id>.md` |
| 100 ft | acceptance | the task file's mechanical criteria |

A task file is the 1,000-foot decomposition of one roadmap Feature; its `parent:` links back up. **Only decompose a Feature into task files when it is actually about to be built.** Speculative task files for far-off skills rot and are dishonest about `touched_files`; keep those at the `ROADMAP.md` altitude until their turn.

Task lifecycle `open -> in_progress -> done`. On completion: confirm the acceptance command passes; confirm every `depends_on` is in `.tasks/done/`; **run `doc-sync` over the reader-facing documents and apply or dismiss each finding**; **when the task declares a `spec`, bring that contract's conformance matrix up to date, or record the deferral**; move the file to `.tasks/done/` with `status: done` and **re-anchor its relative links for the extra directory level**; add one dated line to `CHANGELOG.md`; strike the roadmap Feature through if it is complete.

**A spec is earned, not a default.** The spec chain (`spec-author` through `spec-conformance`) is for behaviour a person must agree before it is built. A task that changes no behavioural contract declares no `spec` and closes with the steps above minus the conformance one. The sizing rule adopters get is in the README under "Choosing a path".

Why the re-anchoring, `doc-sync`, and conformance steps are in that list, each with the incident that put it there, is in the [rationale](agents-md.md). On the conformance step: a task that declares a `spec` closes by producing or updating that spec's `<spec>.conformance.md` with [`spec-conformance`](../../.agents/skills/spec-conformance/SKILL.md), over the scenarios its `scenarios` field claims. **Deferring is legal, and for a forward spec it is the only honest answer**: a scenario nothing has built is recorded as not-built with what is owed, and a spec with no implementation at all keeps its matrix owed, said plainly in the task rather than invented. A matrix written to satisfy this step is worse than no matrix.

### How a skill is structured

Each skill is a directory under `.agents/skills/<name>/` containing:

- **`SKILL.md`** (required): YAML frontmatter (`name`, `description`) then a Markdown body, the single harness-agnostic source of truth. It must not depend on any one tool's features. The `description` says both what the skill does and when to use it, and leads with the key use case in the third person: Claude Code drops long descriptions first when its skill listing overflows, so `validate-skills.py` warns over 700 characters. Aim under ~500 lines; push detail into referenced files.
- **`templates/`**, **`references/`**, scripts (optional): supporting files, referenced one level deep.

Run `python scripts/validate-skills.py` to lint every skill against these rules.

### Who starts a skill

A skill is **model-invoked** by default: its description sits in the agent's context so the agent can reach it unprompted and other skills can compose it. A skill a person starts by name (an orchestrator such as `fix-batch`, a scaffold, the `zen` router) declares `invocation: user` under `metadata`. The Claude Code install paths render that as `disable-model-invocation: true` in the copy they place, which takes its description out of every session's context. It is never written as a top-level key in the source, because claude.ai and the Skills API reject any frontmatter key outside their six, and `metadata` is one of the six. The reasoning, and when to pick which, is in [`writing-for-agents.md`](../../.agents/rules/writing-for-agents.md).

A new skill lands as a draft, `status: draft` under `metadata`, and an install places it only when asked with `--include-drafts`. **A shipped skill names a draft sibling in backticks, never as a relative link**: the link is an install edge, and the installer refuses a profile in which a shipped skill depends on a draft. The link is made when the draft is promoted.

### Two body shapes, both valid

The body takes one of two shapes, decided by how the skill is consumed. Neither is preferred and
neither should be retrofitted onto the other.

- **Workflow skills** carry a procedure: ordered steps an agent executes, usually with sections for
  when to use it, when not to, inputs, the procedure itself, and notes. Most skills are workflows.
- **Lenses** carry `Intent`, `Workflow`, and an `Output` heading instead, because they are composed
  into another skill rather than run on their own. Giving a lens a step-by-step procedure invites an
  agent to run it standalone, which is the one thing it is not for.

**A skill's shape is declared in the skill and enforced by [`validate-skills.py`](../../scripts/validate-skills.py), not listed here.** A lens says so in its own body ("This skill is a lens" or "This is a lens"), and the validator warns when the headings under that declaration are a workflow's. Inferring the shape from the headings instead would make every skill conform by construction.

The history of this rule is in the [rationale](agents-md.md).

### Every skill points at every universal lens

Whatever its shape, a skill must reference each lens that declares itself universal, because a lens
is swappable: an adopter who replaces it is silently ignored by any skill that never points at it.
Two do so today, [`house-style.md`](../../.agents/rules/house-style.md) and
[`autonomy.md`](../../.agents/rules/autonomy.md), each saying `**Scope: universal.**` in its own opening.
[`review-quality.md`](../../.agents/rules/review-quality.md) is topical and is composed only by the skills
that review, which is correct: requiring the rest to name a rubric they never apply is the noise
that gets a rule ignored.

**Universality is declared in the lens and enforced by [`validate-skills.py`](../../scripts/validate-skills.py), not listed here.** A lens that wants the stronger rule says so in its opening; one that says nothing is topical and is still covered by the at-least-one rule.

The enforcement is new; how the two halves drifted apart before it is in the [rationale](agents-md.md).

Which conventions govern depends on what the skill writes:

- A skill that produces **its own output** (a report, a review, a spec) follows this repository's
  house-style module.
- A skill that writes **into a target repository** (`init-worktracking`, `new-task`, `pr-describe`,
  and the agent prompts `fix-batch` dispatches) follows **that repository's** conventions instead,
  and names this kit's module only as the fallback when the skill is run here. Importing this kit's
  voice into a repo that did not choose it is a defect, not a nicety.

A skill that does both says so, and says which applies where.

### Portability contract

- **`AGENTS.md` is canonical** in any repo this kit scaffolds. Cursor, Codex, and OpenCode read it natively. Claude Code reads only `CLAUDE.md` when one exists, so the `CLAUDE.md` this kit scaffolds imports `AGENTS.md` with `@AGENTS.md`; a sentence asking Claude to read the file is followed only when the model decides to open it.
- **Write once, adapt thin.** A skill's logic lives only in its `SKILL.md`. Any per-harness file is generated by [`scripts/build-adapters.py`](../../scripts/build-adapters.py), never hand-maintained in parallel.
- **No tool lock-in in skill bodies.** Gate any single-harness capability behind a clearly labeled optional section.
- **A skill's links must resolve where the skill is used, not only where it is written.** A skill ships as a directory alongside its sibling skills and the rules module, without this repository around it. So a link may reach its own files, a sibling skill, or `.agents/rules/`, and nothing above that. A link that escapes resolves here and dangles everywhere the skill actually runs, which is how `house-review` once shipped with no rubric: the failure is silent, because the body still reads correctly and only the missing target is absent. `validate-skills.py` fails on this, and `build-adapters.py` rewrites the three legal classes when it inlines a body, so the same rule holds on both distribution paths. When a skill needs to name a file outside that tree, such as the target repository's `AGENTS.md`, name it in prose rather than linking to it.
- **A relative link to a sibling `SKILL.md` is also a profile edge.** [`install.py`](../../scripts/install.py) resolves an install profile by expanding its seed over the sibling links it finds in skill bodies, so adding one link can pull that skill, and everything that skill links to, into a profile that did not carry it. The expansion is deliberate and correct: a profile that places a skill without what that skill composes ships a broken tree. What it means for an author is that the link syntax, not the mention, is the switch. Write `[doc-sync](../doc-sync/SKILL.md)` when the skill genuinely composes `doc-sync` and is broken without it; write the name in backticks, `doc-sync`, when you are only stating where it sits in the chain. `chore-0040` wrote the link form for a neighbour it merely named, and one edit pulled a fourteen-skill component into `core`.

### Conventions

Follow [`.agents/rules/house-style.md`](../../.agents/rules/house-style.md) for writing and formatting: no em-dashes, sentence-case headings, named sources, relative markdown links, Mermaid for diagrams. That file is swappable; this reference to it is not.

- **A relative link from one skill body to a sibling `SKILL.md` is load-bearing**, not merely formatting: it is a profile edge for `install.py`, and changing it changes which skills an install places. Read the portability contract above before adding or removing one.

- **Python** (tooling under `scripts/` and `.tasks/validate.py`): standard library only where possible, so it runs anywhere with a bare Python 3. PEP 8. No third-party dependency unless truly load-bearing and documented.

- **Cross-platform**: target Windows, macOS, and Linux. Prefer `pathlib`; never assume POSIX symlinks are available.

### The acceptance command

[`run-checks.py`](../../scripts/run-checks.py) runs every gate that decides whether a change here is acceptable, in one command with no flags: skill lint, the test suite, backlog validation, adapter and install dry runs, the real install cycle, the documentation link check, the conformance-matrix citation check, the roadmap bookkeeping check, and a secret scan. The set is open, and its membership rather than its size is the property: naming a count here goes stale the first time anyone adds a gate. It exits 0 when all pass, 1 when one ran and failed, and 2 when one could not run at all, with 2 outranking 1 for the same reason `install.py --check` and `check-provenance.py` do it: a gate that could not execute means the report is incomplete, which is a different claim from "the change is bad". Every gate runs even after one fails, because an agent working unattended gets one round trip and a report truncated at the first failure costs it another.

**A documentation-only change runs only the documentation gates and the secret scan**, and the report names every other gate as skipped. What counts as documentation, and the base it is measured against, is decided in one module, [`_change_scope.py`](../../scripts/_change_scope.py), that this command reads locally and in every CI cell. A moved file counts at both paths, and any change the module cannot work out runs every gate. Set `ZEN_CHECKS_SCOPE=full` to run every gate anyway.

[`.github/workflows/checks.yml`](../../.github/workflows/checks.yml) calls this same script rather than restating the gates. One rule, two callers, per `chore-0029`.

**Passing it is necessary but not sufficient.** CI runs three operating systems by two Python versions, so any single run of this command covers one of those six cells. A change that passes locally can still fail on a platform you did not run. The command says so in its own summary on every run, and it is repeated here because this is where an agent reads the rules before it starts working, rather than after a run has already happened.

**The other insufficiency is the one more runs do not close.** Every gate here decides a mechanical property, so read a green run as evidence about the mechanical layer and nothing else. Buy the rest by hand, cheapest first: **construct the empty or degenerate input and see what the tool actually says**. A check that cannot fail is unchecked, whatever it printed. The incidents behind this paragraph are in the [rationale](agents-md.md).

### The one committed hook registration

The layout table above states that hook installation is opt-in and activation is the adopter's: `install.py --with-hooks` places the files and prints a registration rather than editing anyone's settings. That rule holds everywhere except one place in this repository, and the exception is written here rather than left to be discovered.

[`.claude/settings.json`](../../.claude/settings.json) is committed, and it registers [`skill-reachability-reminder.py`](../../.agents/hooks/skill-reachability-reminder.py) on `SessionStart`. A project-scope settings file applies to every collaborator who opens this repository, so nobody opts in.

The reason is mechanical rather than a preference: a user-level `~/.claude/settings.json` does not reach a cloud session, and a cloud session is the exact case this hook exists for. The full argument is in the [rationale](agents-md.md).

The exception is kept as small as it can be: one hook, in the reminder shape, which never blocks and never writes, firing only on a genuinely new session. Its worst case is one injected paragraph. **Adding a second hook to that file, or any hook that blocks, is a new decision and not covered by this one.**

**The interpreter is a fallback, `python3 <hook> || python <hook>`, and the bound on that shape is the hooks module contract.** `a || b` reaches `b` only when `a` fails, and every hook here always exits 0, including on failure, so the only way the second interpreter runs is the first never starting. That is what makes the shape legal: a hook that exited non-zero *after* writing to stdout would run twice and emit two objects, which corrupts the exchange the harness parses. If a hook is ever registered here that does not honour exit 0, this command has to change with it. `tests/test_hooks.py` asserts both halves, running the committed command as the harness does and asserting every shipped hook exits 0 on every path.

The fallback replaced a one-sided `python3` that had never run on Windows (`bug-0050`); the [rationale](agents-md.md) records what that cost.

### Commit messages

**Do not add a `Co-Authored-By` trailer naming an AI model to any commit here.** This overrides the
default some harnesses apply, including Claude Code's, and it applies to every agent that commits in
this repository: an interactive session, a worktree agent dispatched by `fix-batch`, and a cloud
session alike. All three have added it. **It binds automated tooling as well as agents**: GitHub Copilot Autofix writes `Co-authored-by: Copilot Autofix powered by AI` into every commit it makes, so apply an Autofix suggestion by hand in a commit of your own rather than accepting its commit onto a branch here (`chore-0090`). Authorship of the work is already recorded where it belongs,
in the task file, the `CHANGELOG.md` line, and the pull request body.

The reason is mechanical: the `main protection` ruleset demands an extra approving review for a commit attributed to an identity with no GitHub account, and the only human here cannot approve their own pull request, so the trailer deadlocks the sync to `main`. The committed [`.claude/settings.json`](../../.claude/settings.json) sets `attribution.commit` to an empty string so Claude Code stops adding it by default; other harnesses still rely on this rule. The incident is in the [rationale](agents-md.md).

### Contribution bar

A skill earns a place in this kit only if it is something the author actually uses and has iterated on. Do not add speculative skills. A freshly drafted skill stays `in_progress` (or is marked as a draft in `ROADMAP.md`) until it has been used and refined; only then is it "shipped." Hyper-specific personal skills stay out of the shared kit (see `docs/CATALOG.md` tiers).

## Why the contribution bar gates promotion, and why drafts expire

Recorded 2026-11-25 by `feat-0102`, from the maintainer's decisions `D1` and `D2` in the [decision sheet](../reviews/2026-11-25-marjana-decisions.md). The [coverage map](../reviews/2026-11-25-skills-coverage-map.md) (section 4, rules 1 and 2) found the bar being read as a bar on writing a draft at all: it had kept `prototype`, `wait-what` and `wayfinder` unwritten, although a draft reaches no adopter without `--include-drafts`. The bar's value is that the catalog is honest about what has run, and that is a property of promotion, so the gate moved there. Free drafting has its own failure, a drafts folder that only grows, so a draft now expires after 90 days without a dogfood record and someone has to decide: promote, extend with a dated reason, or remove. `feat-0103` builds the warning; the key names (`metadata.drafted`, `metadata.extended`) and the number are fixed here so both sides agree.

The personal-tier exclusion had been applied to `teach`, a general skill, because its first use was personal. The maintainer made shareability the only filter: could someone else use it on their own work. The hyper-specific personal pipelines the tier was written for stay out under that test anyway.

## Why a shipped skill may load a draft by name

Recorded 2026-11-25 by `feat-0102`, from decision `R2-3` of the [round 2 plan](../reviews/2026-11-25-marjana-r2-plan.md) (coverage map, section 4, rule 9). Two rules collided: a relative link to a sibling is an install edge, so a shipped skill cannot link a draft; and "composition must load" says a backticked name is only a mention, which an agent reads as background. A shipped skill could therefore never use a draft it would benefit from (`tdd` with `systematic-debugging`, `zen` with `research`). The guarded form keeps both rules: the name stays in backticks, so nothing is installed, and the sentence is an explicit load with a fallback, so the step works with or without the draft. The exact wording is fixed so `validate-skills.py` can recognise it rather than guess at intent.
