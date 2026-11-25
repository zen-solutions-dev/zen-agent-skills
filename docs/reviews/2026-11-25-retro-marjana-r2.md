# Retro: the 2026-11-25 Marjana round 2 orchestration

**Status:** report only. Nothing here is applied. Each proposal waits for the maintainer's approval by its id, then lands through `new-quest`. Run with [`retro`](../../.agents/skills/retro/SKILL.md) by a leaf session dispatched by the round 2 orchestrator (`session_017QLseoWFoRQDJMZM5nR9DQ`), after the close round landed at `fcb5419` on `zen/marjana-r2-2026-11-25`. Classification read [`writing-for-agents.md`](../../.agents/rules/writing-for-agents.md) and [`declined-ideas.md`](../declined-ideas.md) first.

**Ids.** The round 2 `retro` dogfood run in [`2026-11-25-dogfood/ship.md`](2026-11-25-dogfood/ship.md) already used `R-301` to `R-303`. This report continues at `R-304`, and says where it builds on those three.

**Sources (A6).**

- The round's plan, [`2026-11-25-marjana-r2-plan.md`](2026-11-25-marjana-r2-plan.md), in full; the round 2 section of `orchestrate`'s `references/first-run.md`; every entry under [`docs/agents/memory/`](../agents/memory/README.md); round 1's [retro](2026-11-24-retro-marjana.md) (`R-201` to `R-210`); the eight dogfood records under [`2026-11-25-dogfood/`](2026-11-25-dogfood/); `git log ba0209f..fcb5419` (60 commits) and the stat of each orchestrator and close-round commit.
- **A sample of 4 of the round's 10 child sessions**, drawn failures first, all four that failed a first verification and then had a fix round with something notable in it: tracker publishing (`session_017QLseoyH14TPLErJA34AGx`, `feat-0106`, two re-dispatches, the cap), rules and lenses (`session_017QLsenmurm5cefHqCoNeqy`, `feat-0102`, a fix round that left a stale quote), platform and gates (`session_017QLseoudEC1adiuhqiqabq`, `feat-0103`, head moved mid-verification), Phase 3 plans (`session_017QLseo873YPiRD3ck4BHRH`, private names). **All four were readable.** Only their `result` events were read, the newest page of each (`list_events`, `kinds: ["result"]`; each reported `has_more`), so their first reports and any friction inside a turn are missed; the plan and the dogfood records stand in for the first reports.
- **Not covered:** the orchestrating session's own transcript (so whether the picker and emoji preferences were kept in practice is not audited here), the six unsampled children, every verifier and reviewer session, and CI, which never ran on a commit of this round.

## Guardrails

```text
guardrails:
  - run-checks.py, 13 gates: wired, passing. ZEN_CHECKS_SCOPE=full on a clean tree at fcb5419: "13 passed, 0 failed, 0 could not run." (Linux, Python 3.13.18, one of six cells)
  - .github/workflows/checks.yml, 3 OS x 2 Pythons: wired on push to main and on pull_request only, so it ran on no commit of this round (R-210 recurs; dismissed below as decided)
  - main ruleset: present per AGENTS.md; its required checks cannot be read from this session
  - pre-commit hooks: absent in this repository
  - SessionStart skill-reachability-reminder: wired (.claude/settings.json)
  - the B5 cloud environment: wired; setup script installs the kit with drafts; children reported skills reachable (align.md, platform.md)
  - scripts/release.py --check: exists, passes today ("VERSION says 0.1.0, and CHANGELOG.md has a section for v0.1.0."), but is run by no gate. Finding: R-305
  - a check for private names or account details: absent. The secret scan says of itself "Fixed-prefix shapes only". Finding: R-304
```

### Checks audit

Each gate's firings this round, from the sampled sessions, the dogfood records and the commits, judged.

| Gate | Fired on | Judged | Disposition |
|---|---|---|---|
| lint skills, guard sentence | Four good guarded sentences wrapped at 100 columns (`ship.md`, `R-301`) | Good code misread | Fixed at close (`b957215`, item (c)); the fix itself crossed paragraphs and was fixed again (`e6dda0f`). Keep. The ATX-heading nit is already owed in the plan |
| lint skills, dogfood record match | Nothing it should have: the platform fix round widened a match to "names the skill as a whole word" (`0d8e4f9`), under which a record naming any common word satisfies a draft named `research` | **Could not fail** for common-word names | Narrowed at close to backticked, bracketed or path forms (`AGENTS.md` section 7). Keep |
| lint skills, draft expiry by date | Nothing. This checkout is shallow (`git rev-parse --is-shallow-repository`: `true`), and six drafts carry no `metadata.drafted`, so their dates read "unknown (shallow clone)" (platform session's report) | **Cannot fail on age** in a cloud session for those six | `R-306`, a ratchet |
| matrix citations | Today "0 unresolved, 23 double-quoted phrase(s) reported" | **Cannot fail** on a stale double-quoted phrase, the class of the S-044 quote left by `feat-0102`'s fix round (`3b1bd22`) | Already reserved as `chore-0118` (the audit switches to failing). `R-307` asks only that it go first in round 3 |
| roadmap bookkeeping, skill listings | Correct in-flight work: children barred from `ROADMAP.md` had to except their own new drafts by name (`41b8e92`, `ade3ca2`) | Firing as designed: a bridge, emptied at close (`08d0e1b`), and it then caught real missing listings | Keep. The navigation cost is `R-302`, taken up in `R-311` |
| changelog lines | 19 excepted lines, 0 new over the limit | Real | Keep |
| secret scan | 0 findings | Real for its shapes; blind to private names | `R-304` adds the missing check beside it |

No gate is proposed for pruning: none fired mostly on good code once its fix landed.

## Proposals

```text
proposals:
  - id: R-304
    rank: shipped
    category: automated check
    evidence: >-
      Phase 3 plans failed verification on private repository names. Its first fix round
      (988f145, session_017QLseo873YPiRD3ck4BHRH) "found 27 mentions in 16 files, including older
      dated records outside my original scope"; the second (d5df285) found two more names the first
      search had not been given, one of them inside shipped code comments (sitrep.py,
      observatory/serve.py) and the approved sitrep spec. The close round then scrubbed an artifact
      link, an environment id, local user paths and "Answered by <name>" lines (plan, close-round
      answers). All of it was pushed to a public repository's branch first; history keeps it, which
      is why the PR body recommends a squash merge.
    recurrence: 3 scrub passes in one round (988f145, d5df285, b957215), each finding what the
      previous search was not told to look for
    proposal: >-
      A run-checks gate, "private terms": read a term list from a file that is never committed
      (the path in ZEN_PRIVATE_TERMS, else ~/.config/zen/private-terms), one literal per line, and
      fail on any tracked file containing one, printing the file and line but never the term
      (print its line number in the list). With no list present it reports "not checked: no term
      list" and passes, so adopters and CI are unaffected. The maintainer keeps the list; briefs say
      "run-checks covers private names" instead of naming them.
    where: scripts/scan-secrets.py (a second mode) or a new check in scripts/run-checks.py; one
      line in CONTRIBUTING.md
    why this and not a written rule: the mistake has a fixed shape (a literal string), and the
      written instruction "write no private repository name" was in force and failed three times
    door: two-way (a gate; revert removes it)
    cost: about 60 lines and three tests (absent list, clean tree, one hit); shown failing on a
      planted term before it is reported applied

  - id: R-305
    rank: caught in review at real cost
    category: automated check
    evidence: >-
      feat-0103's fix round committed VERSION at 0.2.0, the maintainer's first answer (9bb5867). The child itself wrote
      "release.py --check will say the changelog has no v0.2.0 section ... No gate runs that check."
      The re-check caught it, the maintainer reversed the decision, and a further commit followed
      (952dd6f, "VERSION at 0.1.0, the last tagged release (maintainer correction)"), plus the
      plan's "Superseded the same day" note.
    recurrence: 1, but the plan's lesson (4) names it as one of the fix-round blockers
    proposal: >-
      Add Gate("release metadata", [[PY, "scripts/release.py", "--check"]]) to run-checks.py.
    where: scripts/run-checks.py
    why this and not a written rule: the script already decides it; it is simply unwired
    door: two-way
    cost: one line plus a test that a VERSION with no changelog section fails the gate

  - id: R-306
    rank: friction
    category: ratchet
    evidence: >-
      Draft expiry counts from metadata.drafted, else from the first commit of SKILL.md. Cloud
      checkouts are shallow, so the fallback reads "unknown (shallow clone)" (platform session,
      fix-round report: "every draft here now dates as unknown. None warns, because all six are
      named in a dogfood record"). The date half of the check therefore cannot fire in the
      environment where this kit's rounds run.
    recurrence: every cloud session; 6 of 12 drafts today
    proposal: >-
      validate-skills.py: a draft with no metadata.drafted is an error, with an exception list
      beside the check that only shrinks. New drafts already carry it (the six of 2026-11-25).
    where: scripts/validate-skills.py, with its test
    exceptions: 6 at fcb5419 (agent-observatory, orchestrate, quest-tracker, research, sitrep,
      systematic-debugging); each comes off by adding the date its first commit gives in a full clone
    door: two-way
    cost: about 20 lines; one quest to add six dates from a full clone

  - id: R-307
    rank: caught in review at real cost
    category: ratchet (already reserved)
    evidence: >-
      feat-0102's fix round left the S-044 conformance row quoting self-merge wording autonomy.md no
      longer held; its re-check called it a blocker (3b1bd22). The citations gate reports
      double-quoted phrases rather than failing on them (today 23), so it could not catch this.
    recurrence: the same class as the 24 phrases R-004 found; plan lesson (4) "a stale conformance
      quote"
    proposal: >-
      No new change: chore-0118 is already the ratchet. Take it first in round 3, before any child
      edits a contract, so a fix round's stale quote fails at the child's own run-checks.
    where: ROADMAP.md ordering of chore-0118
    exceptions: 23 double-quoted phrases at fcb5419
    door: two-way
    cost: chore-0118's own

  - id: R-308
    rank: caught in review at real cost
    category: written standard
    evidence: >-
      feat-0106 (one-way door) had its issue shape approved at the check-in gate, then failed review
      with F1 to F9 (identity marker, truncation inside fences, frozen issues, trust boundary), then
      its re-check with N1 to N3, and needed four maintainer amendments (a) to (d) to the approved
      shape: two re-dispatches, the cap (plan, Wave 2 record; sampled session, about 11 USD). Each
      finding was an edge of the shape, not of the code.
    recurrence: 1 one-way door this round, every one of its rounds
    proposal: >-
      orchestrate, at a check-in gate on a one-way door: before the child builds, a fresh leaf reads
      the proposed shape with house-review's security axis and lists its adversarial cases (forged
      input, limits, deleted or private sources, edits made outside the tool). The person approves
      the shape with those cases answered.
    where: .agents/skills/orchestrate/SKILL.md, Step 2 (check-in gate)
    why this and not a check: which edge cases matter is a judgement on a design not yet built
    door: two-way
    cost: one short subagent per one-way door; this round, one

  - id: R-309
    rank: caught in review at real cost
    category: written standard
    evidence: >-
      The Phase 3 plans child owned docs/reviews/ only. A relayed decision ("scrub them everywhere")
      had it edit shipped code comments in sitrep.py and observatory/serve.py, the approved
      docs/spec/sitrep.md, and closed quest files and history ledgers (d5df285, 988f145). The
      orchestrator also reports a link sweep of its own that edited a shipped file; this retro could
      not locate that commit by message or path, so it rests on the orchestrator's word.
    recurrence: 2 (one verified, one reported)
    proposal: >-
      orchestrate Step 4: a relay that reaches beyond the child's owned paths names every path it
      adds, and when one is shipped (.agents/) or an approved spec, the relay goes to the close
      round's fix child or a child that owns it, not to a plans child; the verifier's brief lists
      the added paths.
    where: .agents/skills/orchestrate/SKILL.md, Step 4
    why this and not a check: owned paths live in the brief, which no gate reads
    door: two-way
    cost: two sentences

  - id: R-310
    rank: caught in review at real cost
    category: written standard
    evidence: >-
      3 of the 4 sampled fix rounds disclosed work beyond their findings, as A5 asks: feat-0102 added
      a sentence on never re-merging to change sampling; feat-0103 widened dogfood-record matching to
      a whole word ("Change beyond the review's list"); feat-0106 added dated conformance tables
      "marked as written by me and not re-audited". The whole-word widening made the check unable to
      fail for common-word names and had to be narrowed again at the close.
    recurrence: 3 of 4 sampled fix rounds
    proposal: >-
      orchestrate Step 5 item 7: the focused re-check covers the fixed findings and every change the
      fix round disclosed as beyond them; an undisclosed change found by diff is itself a finding.
    where: .agents/skills/orchestrate/SKILL.md Step 5 item 7; one line in house-review Step 8
    why this and not a check: whether an extra change is sound is a review judgement
    door: two-way
    cost: one sentence each; slightly larger re-checks

  - id: R-311
    rank: friction
    category: navigation
    evidence: >-
      Builds on R-302 and R-303 (ship.md), not yet built: CONTRIBUTING.md has no "Adding a skill"
      section. New evidence: feat-0108 needed a separate commit to make five drafts known to the
      hook, the roadmap gate and the marketplace (41b8e92); feat-0106 excepted its draft's roadmap
      findings by name because ROADMAP.md was not its own (ade3ca2).
    recurrence: 2 of 2 children that added a skill this round
    proposal: >-
      R-302 as written: one "Adding a skill" checklist in CONTRIBUTING.md (KIT_SKILL_NAMES in the
      reachability hook, tests/fixtures/supporting-files.txt, the two exception lists, the
      marketplace rebuild, id_high_water), pointed at from AGENTS.md section 4; and R-303's line in
      the brief template naming the exception lists as allowed edits for a child barred from
      ROADMAP.md.
    where: CONTRIBUTING.md; AGENTS.md section 4 (one pointer line); orchestrate brief template
    door: two-way
    cost: about 12 lines

  - id: R-312
    rank: friction
    category: navigation
    evidence: >-
      The plan's rule 2 and its two-way decisions tell every child to install "at project scope",
      but install.py has no scope option (--help lists none), and the quest-rename child recorded
      "It placed at user scope ... the installer has no project-scope option" (quests.md). The
      feat-0107 child found orchestrate, fix-batch and reconcile-worktrees absent from its skill
      tool because they are user-invoked, and read them from SKILL.md (orchestrate.md).
    recurrence: 2 children wrote it down; every brief carried the wording
    proposal: >-
      In orchestrate's references/claude-code.md, the cloud section: "The B5 environment already
      installs the kit with drafts at user scope; a child confirms with install.py --check. A
      user-invoked skill is not listed by the skill tool; read its SKILL.md." Drop "project scope"
      from the brief template.
    where: .agents/skills/orchestrate/references/claude-code.md
    door: two-way
    cost: two lines

  - id: R-313
    rank: friction
    category: written standard
    evidence: >-
      The plans child replaced "his" and "he" for the maintainer in its plans (sampled session,
      first fix round); the round's own plan still says "on his go" in the VERSION note.
    recurrence: 2 files this round
    proposal: >-
      house-style.md: refer to a person by role ("the maintainer") or name; use a pronoun only when
      the person has stated theirs.
    where: .agents/rules/house-style.md
    why this and not a check: a pronoun check fires on quoted sources and on stated pronouns
    door: two-way
    cost: one line
```

### What would make round 3 cheaper

The sampled sessions alone cost about 50 USD in list price at their last report (platform about 25, publishing about 11, rules about 8, plans about 6); every one had at least one fix round. Of the defects that forced a fix round or a re-check, three had a fixed shape a gate could have caught at the child's own run: the release path (`R-305`), a stale quoted phrase (`R-307`) and private names (`R-304`). The rest were judgement on contracts, which verification is for (plan lesson 5). So, in order: land `R-304`, `R-305` and `chore-0118` before Wave 1; read one-way door shapes adversarially before building (`R-308`); keep relays inside owned paths (`R-309`).

## Dismissed, with reasons

- **CI on the integration branch.** This round again ran every gate on one Linux cell (`R-210` recurs). Dismissed as decided: B10 put CI on integration branches at Later; the recurrence is recorded here for when Later comes.
- **Children self-review before reporting, to pass the first verification.** Every first report failed, but the defects that were mechanical are taken by `R-304`, `R-305` and `R-307`; the rest were judgement a second agent is there to catch (`A7`), and the children already ran the acceptance command.
- **The orchestrator's commits mid-wave, a relay applied after a report, shared terms defined two ways.** Already in [`docs/agents/memory/`](../agents/memory/README.md) and folded into `orchestrate` by `feat-0107`. The plan shows the Wave 2 record held until Wave 2 landed (`7dbad71`), so no recurrence after the fold was seen.
- **Quest files closed in batches.** Recorded in `first-run.md` at the close; the rule stands and nothing new is proposed.
- **The guard regex wrapping (`R-301`).** Built at the close (`b957215`, `e6dda0f`); its remaining ATX-heading gap is owed in the plan.
- **Questions in prose instead of the picker.** Matches the declined entry "Questions in plain prose instead of a structured question tool" (declined 2026-11-25, the maintainer's answer T3). No new evidence: the orchestrator's transcript was not read.
- **Rewriting history to remove private names.** Not possible from a session and not needed: the maintainer chose a squash merge, so the branch's commits never reach `developer`.
- **An invalid YAML example in `AGENTS.md` (`feat-0102` F1).** A one-off, fixed by quoting, and the validator now reads the quoted form.
- **Automating this retro.** Matches the declined entry "Automating `retro` after every session"; sampling was used.
