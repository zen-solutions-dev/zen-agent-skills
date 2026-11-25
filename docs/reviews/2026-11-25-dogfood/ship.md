# Dogfood record: Ship and learn (`feat-0108`), 2026-11-25

One run per skill this workstream changed or created, on branch `zen/marjana-r2-ship`, cut from
`zen/marjana-r2-2026-11-25` at `d906b20`. Every run below happened in the feat-0108 child session
on 2026-11-25. Where a run was done by a fresh subagent, that is said; every verdict is this
session's or its subagents' own reading, not an independent verification (`A7`).

## `house-review` (changed: guards, security axis, smells)

- **Ran on**: feat-0102's landed work, range `7496499..3b1bd22` restricted to `.agents/rules/`,
  `AGENTS.md` and `CONTRIBUTING.md`, contract `.quests/feat-0102-rules-and-lenses-for-round-2.md`.
  Run by a fresh subagent at high effort, following the skill at `ba290b9`.
- **Evidence**: header `door: one-way (a permission change: A8's two new exceptions ...) security
  axis: run`; 25 guards quoted, 18 held, 2 broken, 5 not reached; Spec 3 findings (worst
  `major|.agents/rules/autonomy.md|spec-missing|self-merge-off-path-omits-naming-the-value`),
  Standards 6, Security 3. The guard check found what `R-209` predicted: zen-config S-045's "names
  the value it read ... in its report" has no line in A8.
- **Verdict**: works; the guard list and the door are followable and found real defects. Costliest
  step: quoting every guard of a 46-scenario spec.
- **What changed** (the commit after `cad9c99`): guards of a large spec scoped to Constraints, Non-Goals and
  the named scenarios, with the left-out count said; a disagreement between sources is a finding and
  the more specific source wins; an amendment that retires a guard makes it held, quoting the
  amendment; a change that edits a standard is judged by the standard at the base; the door list
  gains `autonomy.md`'s self-merge additions (approved spec, acceptance checks, `mode: hitl`).
  Left as found: rename counting under a path scope, the blast-radius kind of `AGENTS.md`, and a slot
  for side facts in the header.

## `pr-describe` (changed: smallest-visual Summary, glossary terms)

- **Ran on**: this branch, against `origin/zen/marjana-r2-2026-11-25`, by this session. Body drafted
  to the session's scratchpad, no pull request opened.
- **Evidence**: the Summary picked a table (one row per skill, parallel changes) and a diff-shaped
  call tree for `house-review`'s new steps, both from `references/visuals.md`; "one-way door" and
  "draft" used as `GLOSSARY.md` defines them.
- **Verdict**: works; the table was the right shape and took under a minute to choose.
- **Found**: the skill's Door definition (does a revert undo it) is narrower than `autonomy.md`'s
  self-merge guard 2, which also makes an approved-spec change or a checks change one-way. By the
  skill this branch is two-way; by A8 it is not self-mergeable. Not changed here (`pr-describe`'s
  Door is a contract the merge-danger section shares with `review-quality.md`); passed to
  integration.

## `retro` (changed: reads the writing lens at classification, and the declined-ideas register)

- **Ran on**: this session, report-only, by this session. `docs/declined-ideas.md` does not exist on
  this branch (`feat-0105` creates it), so that read was "where it exists" and found nothing.
- **Evidence** (proposals, none applied):
  - `R-301`, automated check: `GUARD_OPEN_RE` in `scripts/validate-skills.py` forbids a newline
    between "read and follow it" and "; otherwise", so a guarded sentence wrapped at 100 columns
    warns as unguarded. This session rewrapped four sentences to dodge it. Proposal: allow `\n` in
    that span.
  - `R-302`, navigation: adding one skill needed six companion edits (`UNLISTED_DRAFT_EXCEPTIONS`,
    `ROADMAP_STATUS_EXCEPTIONS`, `KIT_SKILL_NAMES` in the reachability hook, the supporting-files
    fixture, the marketplace, `id_high_water`), each found only by a failing gate. Proposal: one
    "Adding a skill" checklist in `CONTRIBUTING.md`, pointed at from `AGENTS.md` section 4.
  - `R-303`, written standard: an orchestrator brief that bars `ROADMAP.md` should name
    `ROADMAP_STATUS_EXCEPTIONS` as an allowed edit, as it named `UNLISTED_DRAFT_EXCEPTIONS`.
  - Dismissed: a quest `touched_files` entry for a file not yet created; `new-quest` already says
    such a file belongs in Scope.
- **Verdict**: works; the writing lens's no-op and pointer rules shaped `R-302` as a pointer, not a
  rule.

## `teach` (new draft)

- **Ran on**: a **simulated learner**, a fresh subagent given a persona (a non-engineer who reads
  agents' pull requests and believes risk is mostly size). No person was in this session, so this is
  a simulation, not real use. Concept: the Door line of a pull request's Merge danger.
- **Evidence**: Step 2's questions surfaced the misconception ("I'd assume it's mostly the large
  ones"); one piece taught with a source; the learner answered an application question ("only 3
  lines, but once it's merged the emails go out ... reverting the code can't pull them back") and a
  multiple-choice question correctly, then asked a follow-up that led to blast radius.
- **Verdict**: the procedure runs end to end. The teacher broke the skill's own quiz rule: the four
  options were of unequal length. Kept as is: the rule is right and was not followed.
- **Not shown**: a real person's learning, and the learning record (the simulation declined none and
  wrote none).

## `vet-skill` (new draft)

- **Ran on**: Matt Pocock's `wayfinder` at `mattpocock/skills` `d653911`, by a fresh subagent at
  high effort, fetched into the scratchpad with hooks off, nothing run.
- **Evidence**: verdict "install with changes": one blocker (an unattended task ticket that signs up
  for services and records "credentials location" on the tracker, `wayfinder/SKILL.md:80`), five
  majors (the map's editable Notes choose which skills load, `A10`; a name clash with this kit's
  draft; a self-updating install route).
- **Verdict**: useful on first use. The subagent listed thirteen gaps in the skill.
- **What changed** (`cad9c99`): scope covers files outside the skill's directory it loads, clone with
  `core.hooksPath=/dev/null` and enough history, clashes looked for in every install location and in
  names called at run time, shared input others edit, no remote images, a severity for known harness
  keys, a dependency-to-vet-first verdict, pinned copy-and-digest install steps, and whose verdict it
  is.

## `prototype` (new draft)

- **Ran on**: a real open question of this round: does `autonomy.md` A8 guard 4 (sample a self-merge
  when `int(sha, 16) % N == 0`) sample about one merge in N, and how long can a run go unsampled?
  Logic branch, by this session.
- **Evidence**: a one-file page with a pure module, free play and three scenarios; the module driven
  from Node over 20,000 random shas per N: N=5 sampled 0.1961 (target 0.2000), N=20 0.0495 (target
  0.0500), longest unsampled run 136 at N=20; P(no sample in 60 merges at N=20) = 0.046.
- **Verdict**: the rule's rate is right for every N tried; at the cap a person can go a long stretch
  with no sample, which is the rate's trade-off, not a defect. Judge: this session, the maintainer
  absent.
- **Captured** on local branch `prototype/self-merge-sampling` at `1d164d7`, **not pushed** (the brief
  names one branch to push). The verdict could not go on the source quest, `feat-0102`, which this
  workstream does not own; it is here instead.

## `wayfinder` (new draft)

- **Ran on**: the round's rollout campaign (install the kit in each repository the maintainer keeps,
  the Zen product app first), charting mode, by this session. The map was written to the scratchpad,
  not the repository, since Phase 3 owns those plans.
- **Evidence**: a map with a destination, four typed tickets (`W-01` which repositories, grill; `W-02`
  profile and tier, grill; `W-03` name clashes, research; `W-04` layout facts, task), three fog
  entries and two out-of-scope lines.
- **Verdict**: partly exercised. Step 1 needs `grill` with a person, and none was present, so the
  destination is a recommended answer marked unconfirmed. Working mode was not exercised: every
  ticket waits on `W-01`, which only the maintainer can answer.

## `wait-what` (new draft)

- **Ran on**: the round 2 plan's "Check-in gate on `feat-0102`" paragraph, a dense message to the
  maintainer, by this session.
- **Evidence**: Step 1 found five missing pieces (what A8, B1 and C1 are; what "mechanical" means;
  what guard 4 is). The re-pitch, eight short sentences, opened "This is about when an agent may
  merge work, rule A8 in the kit's autonomy rules" and ended "You need to do nothing unless you want
  a different way to pick; undoing it is one commit."
- **Verdict**: works; the same-content rule kept the re-pitch from adding the prototype's finding.
