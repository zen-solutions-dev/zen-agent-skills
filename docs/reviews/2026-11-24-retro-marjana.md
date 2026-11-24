# Retro: the 2026-11-24 Marjana orchestration

**Status:** report only. Nothing here is applied. Each proposal waits for the maintainer's approval by its id, then lands through `new-task`. Run by the orchestrating session with [`retro`](../../.agents/skills/retro/SKILL.md) at the close of `feat-0095`, after every workstream had landed.

**Sources (A6).**
- The orchestrating session itself, read directly.
- A sample of the seven child sessions, drawn failures first: WS-C (`feat-0092`). It pushed once before its checks were green, its own verifier first returned `fail`, and its landing review held the round's one landing blocker. Only its outputs were read (its reports, commits and dogfood record), not its transcript, so friction it never wrote down is missed.
- The round's review records: five landing reviews and five focused re-checks, by fresh-context subagents, and the independent verification.

Proposal ids start at `R-201`, so they cannot collide with the `R-001` to `R-008` series or with WS-D's report-only `R-101` to `R-106`.

## Guardrails

```text
guardrails:
  - run-checks.py, 11 gates: wired, passing at every landing on the integration branch (this one Linux cell)
  - .github/workflows/checks.yml, 3 operating systems x 2 Pythons: wired, but never ran on any commit of this round, because no pull request existed until the end. Finding, below
  - main protection ruleset: present (AGENTS.md); its required checks cannot be read from this session
  - pre-commit hooks: absent in this repository (project-bootstrap now prints one for adopters)
  - SessionStart skill-reachability-reminder: wired; it fired in child sessions, which ran every kit skill by reading its SKILL.md because none was installed. Finding, below
```

## Proposals

```text
proposals:
  - id: R-201
    rank: caught in review at real cost
    category: written standard (a decision for the maintainer)
    evidence: >-
      The orchestrator landed WS-C (c0579ad) and WS-B (6162d00) by its own merge commits, resolving
      mechanical conflicts only. Meanwhile, WS-C's D1 text, landed in c0579ad, says "A landing that
      needs a merge commit or a conflict resolution goes back to the child". WS-E was then sent back,
      and it cost one extra round trip and one extra re-check (52d3d19).
    recurrence: 2 merges against the rule, 1 send-back, in one round of 5 children
    proposal: >-
      Decide between two options. (a) Keep fast-forward only. The cost is one round trip per child
      after the first, in landing order. (b) Allow an orchestrator merge commit whose conflicts are
      confined to generated files, ledger lines and the orchestrator's own planning documents,
      re-checked by a verifier the orchestrator did not brief on the conflict, and listed in the pull
      request. Today's text is (a); this round practised (b) twice before the text existed.
    where: .agents/rules/autonomy.md A8, core.md, orchestrate Step 5

  - id: R-202
    rank: friction
    category: navigation
    evidence: >-
      Every child moved its task file to .tasks/done/ at close. That broke the task link in the
      plan's workstream table and in ROADMAP.md's Marjana section, and the doc-links gate failed in
      four children until each repointed its own row. All four later landings then conflicted on
      those same lines, and every resolution was a by-hand union. The doc-links and roadmap gates
      also forced extra grants outside each child's owned paths.
    recurrence: 5 children, 2 shared documents, 4 conflicted landings
    proposal: >-
      In orchestrate Step 2 (briefs) and in the plan template: a child does not move its own task
      file; the orchestrator closes it at landing, in the same push. Shared planning documents name
      a child's task by id in backticks, and link it only once it is closed.
    where: .agents/skills/orchestrate/SKILL.md, Step 2 and Step 5

  - id: R-203
    rank: friction
    category: automated check
    evidence: >-
      tests/test_validate_skills.py pins one total, {"markdown": N, ...}, for the kit's supporting
      files. WS-B, WS-C and WS-E each added references and each changed the same literal; every
      landing after the first conflicted there and was resolved by a recount.
    recurrence: 3 children, 2 conflicted landings
    proposal: >-
      Replace the total with a sorted list of (path, kind) pairs kept in a data file the test reads,
      one line per file. Parallel additions then merge as separate lines, and a forgotten file still
      fails the test.
    where: tests/test_validate_skills.py and a fixture beside it

  - id: R-204
    rank: friction
    category: automated check (ratchet)
    evidence: >-
      AGENTS.md now says a closeout line is "at most about 300 characters". The four task-log lines
      the workstreams supplied ran from about 330 to 560 characters, and the orchestrator shortened
      each by hand.
    recurrence: 4 of 4 supplied lines
    proposal: >-
      A run-checks warning for a CHANGELOG.md task-log line over 330 characters, with the lines over
      it today listed as an exception that only shrinks. New lines are held to the limit from the
      first commit.
    where: scripts/run-checks.py, the backlog or roadmap gate

  - id: R-205
    rank: friction
    category: missing information
    evidence: >-
      No child session had the kit installed. Every child ran each kit skill by reading its SKILL.md
      ("Kit skills were not reachable in this session", WS-A dogfood record), so no run exercised a
      skill's description triggering or the harness's own skill loading.
    recurrence: 7 of 7 child sessions
    proposal: >-
      A setup script on a personal cloud environment for this repository that runs
      `python3 scripts/install.py --tools claude --include-drafts`, so every cloud session starts
      with the kit loaded the way an adopter has it. This is an environment change, not a repository
      file: the maintainer approves it in the environment settings prompt.
    where: the cloud environment for zen-agent-skills (not this repository)

  - id: R-206
    rank: friction
    category: navigation
    evidence: >-
      The orchestrator's worker restarted three times. Each restart lost the integration branch's
      upstream tracking in the single-branch shallow clone, so a stop hook reported "no remote
      branch" for commits that were already pushed. A fetch refspec
      ('+refs/heads/zen/marjana-*:refs/remotes/origin/zen/marjana-*') fixed it for good.
    recurrence: 3 restarts, 2 false alarms
    proposal: >-
      One line in orchestrate's references/claude-code.md: after cloning, add a fetch refspec for
      the integration prefix, and after any restart confirm remote state with `git ls-remote`.
    where: .agents/skills/orchestrate/references/claude-code.md

  - id: R-207
    rank: friction
    category: missing information
    evidence: >-
      Deleting a branch was refused from the session two ways: `git push --delete` hung up, and the
      REST DELETE returned 403 "Write access to this GitHub API path is not permitted through this
      proxy". The maintainer's decision D3 (delete two stale branches) therefore cannot be carried
      out by the orchestrator.
    recurrence: 1 round
    proposal: >-
      orchestrate Step 1: when the plan holds a one-way-door action on the remote (deleting a branch
      or a tag), probe on a scratch ref that the session can perform it. When it cannot, put it in
      the pull request as a step for the person rather than discovering the refusal at the end.
    where: .agents/skills/orchestrate/SKILL.md Step 1

  - id: R-208
    rank: friction
    category: navigation
    evidence: >-
      WS-B's report (19:27) said grill round 2 was "still unanswered", although the orchestrator had
      relayed the maintainer's answers at about 19:12. The relay reached the child during its turn,
      and the child reported before it read the relay.
    recurrence: 1
    proposal: >-
      orchestrate Step 4: a relay of the person's answers asks the child to acknowledge it, and the
      orchestrator treats a later report that predates the acknowledgement as stale.
    where: .agents/skills/orchestrate/SKILL.md Step 4

  - id: R-209
    rank: caught in review at real cost
    category: written standard
    evidence: >-
      Three of the five landing reviews found a skill contradicting its own contract or its own
      guard. WS-D: house-review's new Step 8 reads signatures, while its spec said it "reads nothing
      from them". WS-C: reconcile-worktrees landed the branch head, not the verified commit, against
      D1's own "that exact commit". WS-E: the exception list hid a regression the gate exists to
      catch. In each case the author had updated the conformance matrix itself.
    recurrence: 3 of 5 reviews here, plus the three cases R-006 counted across 2 pull requests
    proposal: >-
      house-review spec axis: for a change that amends a contract, read the contract's Constraints,
      Non-Goals and every guard against each new step, and quote the line each one is checked
      against. A conformance matrix the author updated is not evidence on this axis.
    where: .agents/skills/house-review/SKILL.md (spec axis), review-quality.md

  - id: R-210
    rank: friction
    category: automated check
    evidence: >-
      CI (checks.yml, six cells) never ran on any commit of this round, because nothing opened a pull
      request until the end. Every gate result in the round comes from one Linux cell, Python 3.13.
    recurrence: the whole round
    proposal: >-
      Have checks.yml also run on push to branches matching the integration prefix (zen/**), so an
      orchestrated round gets all six cells before the person is asked to review. That costs CI
      minutes; the maintainer decides.
    where: .github/workflows/checks.yml
```

## Dismissed, with reasons

- **The video could not be fetched** (YouTube refused both the research child and the orchestrator). The `research` draft already tests every source's reachability before briefing and records what it cannot reach, so no further change is proposed.
- **`list_events` overflowed** at 111,342 characters. The lesson is already in `orchestrate/references/first-run.md`.
- **WS-C pushed once before its checks were green** (`d41fbeb`). Its own run caught this, and it disclosed it. The landing gate (re-check on the exact sha) makes an early push harmless, so the existing guardrail worked.
- **The orchestrator re-checked WS-A's fix commit itself** (`92d4697`). This was before D1's text named the orchestrator as an ineligible verifier. D1 now covers it, and the pull request lists the commit.
