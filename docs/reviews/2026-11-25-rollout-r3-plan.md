# Rollout round 3: plan

Written 2026-11-25 by the orchestrating session that took over from [the first adopter run](2026-11-25-rollout-first-adopter.md), run with the [`orchestrate`](../../.agents/skills/orchestrate/SKILL.md) draft in `hitl` mode. Integration branch `zen/rollout-r3-2026-11-25`, cut from `zen/rollout-handoff-2026-11-25` at `8708b83` (the head of pull request #120, not yet merged into `developer`), so the findings record it builds on is in its base. The final pull request goes into `developer` and shows #120's changes until #120 merges.

## State at the start (Phase 0)

- `v0.2.0` is pushed, at `e694817`.
- Pull request #120 is open as a draft, six of six CI cells green at `8708b83`.
- In the Zen product app (a private repository), the quests cutover and its first quest are pushed and verified, not yet opened as pull requests.

## The maintainer's answers, 2026-11-25

| Id | Question | Answer |
|---|---|---|
| R3-1 | What first? | The product app first, with the kit's findings filed alongside. |
| R3-2 | The first quest's two review nits | A follow-up quest in the product app, built after its branch merges. |
| R3-3 | The product app's stale public date | A docs quest there now; the maintainer deploys. |
| R3-4 | Which kit findings become quests | Findings 1 and 5, 2, 3 and 4, and 6. |
| R3-5 | Finding 8, sitrep's integration branch | Both: a committed `.sitrep.json` now, and sitrep reading `zen-config` filed as a spec quest. |
| R3-6 | Who opens the product app's two pull requests | A child session on the maintainer's computer, through the product app's own pre-PR gate, as drafts. |
| R3-7 | A cloud environment for the product app | Yes: the orchestrator writes the setup script, the maintainer creates it. |

Finding 7 (point verifiers at exact heads) is dismissed: [`orchestrate`](../../.agents/skills/orchestrate/SKILL.md) Step 2 ("after you report, push nothing more unless asked") and Step 5 item 4 (re-point the verifier at a moved head) already say it.

## Two-way decisions taken without asking

- The integration branch is cut from #120's head rather than `developer`. Revert: rebase it onto `developer` once #120 merges.
- In the product app, whose policy is that no agent merges, "landed" means verified and pushed, for the start-slow brake. Its quest files close on their own branches, as its first quest did.
- Children run as local sessions on the maintainer's computer, each in its own worktree; build children at medium effort, verifiers at high, documentation children on a cheaper model.
- Remote-action probe: pushing a branch works from this computer. A tag push was not probed: tagging is the maintainer's step.

## Kit children

| Quest | What | Owned paths | Door |
|---|---|---|---|
| `chore-0119` | The rollout installs the kit in the adopter's cloud environment, and asks early about local-only gates | `docs/INSTALL.md`, the rollout map | Two-way |
| `chore-0120` | Release steps: a cloud session cannot push tags; tag by id; merge `main` back after a squash | `docs/RELEASING.md` | Two-way |
| `chore-0121` | `test-quality` and `tdd`: a claim over "every X" is tested through behaviour | the two skills, the marketplace | Two-way |
| `chore-0122` | `.sitrep.json` says this kit integrates on `developer` | `.sitrep.json` | Two-way |
| `feat-0110` | The validator accepts an empty `touched_files` on a `hitl` quest | both `validate.py` copies, the templates, its tests, the marketplace | Two-way |
| `feat-0111` | sitrep falls back to `zen-config`'s `base_branch` | filed only; waits for the maintainer's approval of a spec amendment | One-way (a spec) |

`chore-0121` and `feat-0110` both regenerate `.claude-plugin/`, so they run one after the other, never together. The orchestrator owns `CHANGELOG.md`, `ROADMAP.md` and this plan; every child passes its lines under "Notes for integration".
