# orchestrate: the first real run, and what it taught

Dated history, kept out of the procedure so the steps stay short. Each lesson names the step it
shaped.

## 2026-11-24: the "Marjana" overhaul of the Zen Agent Skills kit

One orchestrating Claude Code cloud session ran the overhaul before this skill existed, and the
skill was written during that run by one of its children (WS-C), so this records the run as of the
moment WS-C was briefed, not its end. By then the orchestrator had cut the integration branch
`zen/marjana-2026-11-24`, landed two research children's reports (`2940be0`), taken a decision round
with the maintainer, and planned five workstream children, each on `zen/marjana-<workstream>`, with
reserved quest ids and disjoint owned paths. The plan it committed is in the Zen Agent Skills
repository at `docs/reviews/2026-11-24-marjana-plan.md` (commit `9598355`).

What the orchestrator reported learning, as of 2026-11-24:

1. **Probe every source before briefing a research child** (Step 2). A proxy refused two hosts until a
   worker restart, and YouTube's bot check refused both the research child and the orchestrator.
   The research child reported what it could not reach and reconstructed none of it.
2. **Children push a named branch and report by message; nobody opens an intermediate pull request**
   (Step 2). The person reviews exactly one. The two research children reported in about 8 and 10
   minutes.
3. **Verify each report before merging it** (Step 5): spot-check two or three of its claims against
   the tree.
4. **The orchestrator's worker restarted twice**, losing a branch's upstream tracking and leaving a
   merge commit unpushed (Step 5, and the cloud section). Push after every landing; check remote
   state after any restart.
5. **`list_events` without a tight `kinds` filter and `limit` overflowed**, at about 111,000
   characters (cloud section). Rely on the child's report; use events only to check progress.
6. **A fallback check-in** at about forty minutes guards against a child that finishes silently
   (Step 3).
7. **The decision round asked only one-way-door questions**, four of them, each standing on its own
   with the recommended option first (Step 1). Everything reversible proceeded and was recorded with
   its revert.
8. **Reserve quest ids up front, give each child disjoint paths, and give each shared ledger exactly
   one owner** (Step 2). The plan gave `CHANGELOG.md` and `ROADMAP.md` to one workstream and told the
   others to pass their lines under "Notes for integration"; whether that held is for the run's own
   record, not this note.

The rule this run needed before the skill could exist was `A8`'s integration-branch exception, taken
by the maintainer as decision `D1` and written into the autonomy lens by the same workstream that
wrote this skill.

## 2026-11-25: round 2

The second real run, again on the Zen Agent Skills kit, by an orchestrating Claude Code cloud
session that did not write this skill. It cut `zen/marjana-r2-2026-11-25` from `developer` at
`ba0209f`, ran a rename alone as Wave 0, two children in Wave 1 and four planned for Wave 2, and its
plan is in the Zen Agent Skills repository at `docs/reviews/2026-11-25-marjana-r2-plan.md`. This
section records what the orchestrator reported learning as of the Wave 2 briefs (integration tip
`d906b20`), passed to the child (`feat-0107`) that folded it into the procedure.

1. **The orchestrator's own commits to the integration branch while children were in flight forced
   extra merges twice.** It then held them on a side branch until the wave landed (Step 1, item 7).
2. **A child applied a relay after reporting**, moving its head while its verifier ran on the old
   sha. Verifiers are re-pointed at the new head, and children push nothing after reporting unless
   asked (Step 2, Step 5 item 4).
3. **Two siblings defined one term two ways** (a "dogfood record"). A key name or definition shared
   across children is fixed by the orchestrator in both briefs, verbatim (Step 2).
4. **Most fix rounds introduced one more small blocker of their own**: a stale conformance quote, a
   `VERSION` value that broke the release path. A focused re-check of each fix round is worth its
   cost (Step 5 item 7).
5. **Verifiers found real defects in every first report**: an untested alias table, invalid YAML,
   self-merge reaching `main`, a fail-open hook. Verification by another agent is not ceremony
   (Step 5 item 4).
6. **The maintainer prefers the clickable question picker** for every question with choices, and
   contextual emojis in chat (Step 1 item 6 keeps the first as "the harness's structured question
   tool"; both are recorded as preferences in the repository's memory, `docs/agents/memory/`).

Round 1's retro proposals `R-202` (children leave their quest files), `R-206` (restart notes),
`R-207` (probe remote actions early) and `R-208` (relays acknowledged), approved as `B2`, `B6`, `B7`
and `B8` on 2026-11-25, are folded into Steps 1, 2, 4, 5 and 6 and the cloud reference by the same
quest, with `A8`'s mechanical-merge landing (`B1`) and the conflict rule (`E2`).

Recorded at the round 2 close (2026-11-25): **this run closed quest files in batches, not at each
landing** as Step 5 item 6 asks. `feat-0101`, `feat-0102`, `feat-0103` and `feat-0107` were moved
to `done/` together in one commit (`03e4862`), and `feat-0105` and `feat-0108` together in another
(`f579655`); only `feat-0106` was closed at its own landing (`854b91a`). Each batch was listed as
the orchestrator's own unverified work. The rule stands; the run did not keep it.

## 2026-11-25 to 2026-11-26: round 3, the second project

The third real run, by an orchestrating session that did not write this skill, run from the Claude
desktop app on the maintainer's computer in `hitl` mode, across two repositories: this kit and the
Zen product app (a private repository). Its kit integration branch was `zen/rollout-r3-2026-11-25`,
cut at `8708b83`. Its plan is in the Zen Agent Skills repository at
`docs/reviews/2026-11-25-rollout-r3-plan.md`, its dogfood record at
`docs/reviews/2026-11-26-dogfood/rollout-r3.md`, and three of its lessons are entries dated
2026-11-26 in `docs/agents/memory/`. Start slow held twice (one child per repository first); five
kit quests landed by fast-forward or a listed mechanical merge (`57f2782`, `c5decce`); one review,
one fix child (`5e43036`) and one per-finding re-check closed it. Folded in by `feat-0115` on
2026-11-27:

1. **The adopter's pre-PR gate needed a git-ignored list held only on the maintainer's computer**,
   so two branches verified by cloud sessions could not be opened as pull requests. When first run
   there, the gate's own tests failed for reasons unrelated to the work (a CRLF-sensitive regex and
   a global git hook), which cost one extra quest and a restack (Step 1 item 3).
2. **A turn the desktop app started because a child session finished, and a question answered
   inside such a turn, could not start a new session, nor any session in another folder.** The run
   relayed work to an idle child already in that folder and ran builders and verifiers as
   background subagents, each in its own worktree (the desktop app section of
   [`claude-code.md`](claude-code.md)).
3. **A verifier told to sweep for the same claim past its quest's scope found the claim still live
   in about twelve places the quest had scoped out**; that finding became its own quest (Step 5
   item 4).
4. **The maintainer squash-merged the kit's pull request #120, a merge of `main` into
   `developer`**, so `main`'s release commit stayed out of `developer`'s history and the next
   branch (#121) had to merge `developer` again; #121's body had not said it needed a merge commit
   (Step 6 item 4).

## Owed

- A run on a project other than this kit, by a session that did not write this skill, before
  promotion. Round 2 (2026-11-25) was a second run by a session that did not write it, but on the
  same project. Done 2026-11-26: round 3 ran on the Zen product app as well as this kit, by a
  session that did not write it.
- Recorded 2026-11-24, settled 2026-11-25: the `zen-config` keys in Inputs were re-checked against
  the approved `docs/spec/zen-config.md` when `memory` was set (`feat-0107`).
- The start-slow brake, the five questions, the exploration child, the memory lint and the
  recurring-job offer were written in round 2 and are not yet exercised by a run that started with
  them. As of round 3 (2026-11-26): the start-slow brake was exercised and held twice. The
  exploration child, the memory lint and the recurring-job offer are still unexercised, and round
  3's plan does not record the five questions per child.
