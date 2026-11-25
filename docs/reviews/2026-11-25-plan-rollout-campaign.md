# Rollout campaign: map

Charted 2026-11-25 by a Phase 3 child session of the Marjana round 2 orchestration, for quest [`chore-0115`](../../.quests/chore-0115-plan-the-rollout-campaign.md). Status: charting. **Plan only: nothing is installed in any repository.** The format is the `wayfinder` draft's map ([`map-format.md`](../../.agents/skills/wayfinder/references/map-format.md)); its first charting run, on 2026-11-25, wrote a scratch map of this same effort ([dogfood record](2026-11-25-dogfood/ship.md), the `wayfinder` section), and this file is that map made durable.

## Destination

The kit installed, configured and proven by one real quest end to end in each repository the maintainer keeps, the Zen product app first (his "main quest", launching soon), so he can show others "here's how we do it" and teach it.

## Notes

- Domain: the maintainer's own repositories. The Zen product app is first; the rest he names after his GitHub spring cleaning.
- Every session loads `wayfinder`, `grill`, `init-worktracking` and `new-quest`.
- This map does not carry execution: each repository's rollout becomes its own quests once its tickets resolve.
- **The per-repository procedure** each rollout follows, once the tickets below settle its choices:
  1. **Install.** From a checkout of this kit, `python3 scripts/install.py --dry-run` first, then the real run, with `--include-drafts` or not (W-02). It places skills at user scope by default; a cloud session sees only what is committed or what its environment's setup script installs, so a repository worked in the cloud gets a saved environment whose setup script runs the install, as this repository's B5 environment does ([round 2 plan](2026-11-25-marjana-r2-plan.md)).
  2. **Configure.** `init-worktracking`: scaffold the tier, then its Step 6, "configure the skills", which writes `docs/agents/zen.md` (tracker, acceptance command, base branch, default mode, glossary, role labels). Check it with `python .quests/validate.py`.
  3. **First real quest, end to end.** One small change the repository actually needs: `new-quest` writes it, a session builds it (`tdd` where there is code), `house-review` reviews it, `pr-describe` writes the body, a draft pull request opens, the maintainer merges, the quest moves to `done/` with its changelog line.
  4. **Proven** (W-05 confirms): that quest is in `.quests/done/` with its pull request merged; the acceptance command ran and its output tail is recorded; a dogfood record names each skill used and what fell short; every friction point is a quest or a dismissed finding.

## Tickets

### W-01: Which repositories, in what order?

- type: grill
- blocked by: none
- claimed: no
- status: open
- answer: none yet

The product app is first. Which repository is it, and which others follow once the spring cleaning is done? Every other ticket waits on the first answer.

### W-02: Which profile, and drafts or not?

- type: grill
- blocked by: [W-01]
- claimed: no
- status: open
- answer: none yet

`install.py` places `spine` by default (`core`, `spine` or `all`, with `--include-drafts` to add drafts). A product app about to launch may want fewer, stable skills; a repository used to teach may want the full set.

### W-03: Name clashes with Matt Pocock's skills

- type: research
- blocked by: [W-01]
- claimed: no
- status: open
- answer: none yet

`docs/INSTALL.md` says the two kits share `tdd`, `research` and `retro`, and now `teach`, `prototype` and `wayfinder`, and that `install.py` refuses to overwrite a directory it did not place. For each repository: are Matt's skills installed at the same scope, and which copy should win?

### W-04: Each repository's layout facts

- type: task
- blocked by: [W-01]
- claimed: no
- status: open
- answer: none yet

The facts `docs/agents/zen.md` records: its test command, its base branch, whether it has a glossary, its issue labels. Discovered by reading the repository, confirmed by the maintainer in the configure step.

### W-05: What counts as proven?

- type: grill
- blocked by: none
- claimed: no
- status: open
- answer: none yet

The Notes propose four conditions. Is one quest enough for a product app, or does proof need a second quest someone other than the maintainer runs?

### W-06: Cloud sessions or local?

- type: grill
- blocked by: [W-01]
- claimed: no
- status: open
- answer: none yet

Where does the maintainer work on each repository? Cloud sessions need a saved environment per repository with an install setup script; local work needs only the user-scope install.

## Decisions so far

- none yet

## Not yet specified

- The "here's how we do it" material: a written walkthrough, a `teach` lesson, a recorded session, or the website (G9's session). Graduates to a ticket once the first repository is proven.
- Whether each repository turns on tracker publishing (`publish: github`), sampled self-merge (`merge_policy`), or the improvement loop of [plan F1](2026-11-25-plan-f1-improvement-loop.md).
- CI per repository (B10: CI runs on final pull requests only, for now).

## Out of scope

- The website overhaul (G9: its own session, after the skills round).
- `zen-solutions-ops` (round 2 handoff, section 3).
- Changing any repository's code beyond its first real quest.

## Questions for the maintainer

1. **Which repository is the Zen product app?** Name it, so the rollout starts there (W-01). The other repositories wait until you name them after the spring cleaning.
2. **Should the product app get the kit's draft skills?** (a) No: the default `spine` profile without drafts while it launches, drafts added later, recommended; (b) yes, everything with `--include-drafts`, so the rollout also dogfoods the drafts.
3. **Where will you work on the product app?** (a) Both cloud and local: a saved cloud environment whose setup script installs the kit, plus the user-scope install on your computer, recommended; (b) cloud only; (c) local only.
4. **What counts as the kit being proven in a repository?** (a) The four conditions in this map's Notes: one real quest merged, the acceptance output recorded, a dogfood record, every friction point filed, recommended; (b) those four plus a second quest run by someone other than you, before you teach it.
5. **What should the first real quest in the product app be?** (a) A small fix or chore you already want done, chosen by you, recommended; (b) a quest the agent proposes after reading the repository.
