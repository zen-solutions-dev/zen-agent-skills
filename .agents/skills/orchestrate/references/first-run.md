# orchestrate: the first real run, and what it taught

Dated history, kept out of the procedure so the steps stay short. Each lesson names the step it
shaped.

## 2026-11-24: the "Marjana" overhaul of the Zen Agent Skills kit

One orchestrating Claude Code cloud session ran the whole overhaul before this skill existed, and the
skill was written from that run by one of its children. The orchestrator cut the integration branch
`zen/marjana-2026-11-24`, dispatched two research children, took a decision round with the
maintainer, then dispatched five workstream children, each on `zen/marjana-<workstream>`, with
reserved task ids and disjoint owned paths. The plan it committed is in the Zen Agent Skills
repository at `docs/reviews/2026-11-24-marjana-plan.md` (commit `9598355`).

What the orchestrator reported learning, as of 2026-11-24:

1. **Probe every source before briefing a research child** (Step 2). A proxy refused two hosts until a
   worker restart, and YouTube refused cloud addresses outright. The research child reported what it
   could not reach and reconstructed none of it.
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
8. **Reserve task ids up front, give each child disjoint paths, and give each shared ledger exactly
   one owner** (Step 2). The other children passed their changelog and roadmap lines to the
   orchestrator under "Notes for integration".

The rule this run needed before the skill could exist was `A8`'s integration-branch exception, taken
by the maintainer as decision `D1` and written into the autonomy lens by the same workstream that
wrote this skill.

## Owed

- A second run on a different project, by a session that did not write this skill, before promotion.
- The `zen-config` keys this skill reads are being specified in parallel (2026-11-24); re-check the
  key names in Inputs once that spec is approved.
