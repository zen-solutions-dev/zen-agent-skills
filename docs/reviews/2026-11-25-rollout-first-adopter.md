# Rollout, first adopter: the kit's first run in the Zen product app (2026-11-25)

In short: the kit's first run outside this repository went into the maintainer's Zen product app, a private repository, as Campaign G's first slice. Its build plan moved onto quest tracking, and one real quest ran end to end. Both branches passed independent verification, and the maintainer opens and merges their pull requests. The kit's v0.2.0 was released for this first. This record names no private repository and carries no detail of the product's users.

## What happened

| Step | Result | Evidence |
|---|---|---|
| The kit released to `main` | Pull request #119 was merged as `e694817`, VERSION 0.2.0, and `developer` was merged back to it after. The maintainer pushes the `v0.2.0` tag: the cloud session's push of it was refused with HTTP 403. | All six CI cells were green on #119. |
| The migration map | A planning child mapped the adopter's build plan to Campaigns, Quest chains and Quests. It asked thirteen questions, and the maintainer answered all thirteen in pickers. | A plan file in the adopter repository. |
| The quests cutover | 87 open quests: 41 in 14 chains and 46 Inbox side quests, 19 of them blocked on the maintainer. The finished work was frozen in a dated archive. `docs/agents/zen.md` was written with `tracker: quests`, base `main`, `hitl`, and the person merging every pull request. The vendored `validate.py` runs in the adopter's CI. | `validate.py --strict`: 87 files, 0 errors. Board, landing and gate suites green. Independent verifier: PASS. |
| The first quest, end to end | A time limit on the adopter's pre-PR gate's `git` calls, built test first. The verifier failed the first version on two real defects (a missed call in an imported module, and a timeout read as "not a checkout", which failed open), and both were fixed test first. | Gate tests 62 of 62. Verifier re-check: PASS. Nine reverted fixes: every one but one caught by a test (a nit). |
| Pull requests | Not opened from the cloud. The adopter's gate needs a list of names that never leaves the maintainer's computer, and the child correctly refused to go around it. | The maintainer opens both from their own checkout. |

Rarity of the evidence above: Gold for the test runs and the verifier's mutation checks (independently confirmed), Purple for the commit and pull request ids.

## Findings for the kit

Each is a candidate quest for the next orchestrator, not yet filed.

1. **`init-worktracking` did not run in the adopter's cloud session.** The kit was not installed there, so its output was written by hand from the templates. Proposed: the rollout procedure installs the kit in the adopter's cloud environment first (setup script), and the plan says so.
2. **`validate.py` rejects an empty `touched_files`.** A quest that is a person's own step (a deploy, a dashboard setting) has no files, so the adopter named the record it is noted in. Proposed: allow an empty list when `mode: hitl` and the body names the person, or document the workaround in `new-quest`.
3. **Tags cannot be pushed from a cloud session (403).** [`RELEASING.md`](../RELEASING.md) leaves tagging to the person already. Proposed: say that a cloud session cannot do it, and tag the merge commit by id when `main` takes squash merges.
4. **A squash merge to `main` leaves `developer` behind.** After a squash release, `main` must be merged back into `developer` (done here). Proposed: add it to the release steps.
5. **An adopter's own gate can make cloud pull requests impossible.** Proposed: the rollout procedure asks early whether the adopter's pre-PR checks need local-only files, and plans for the person to open the pull requests.
6. **A source-regex guard is not a behavioural test.** The first quest's guard grep'd one file, so a missed call in an imported module passed. Proposed: a line in `tdd` or `test-quality`: when a fix claims "every X", test X through behaviour, over every module reached.
7. **Branch heads moved after a verifier was briefed** (the round 2 lesson again). It was caught by re-pointing the verifier. Proposed: the verifier brief names the exact heads, and the child pushes nothing after reporting unless asked (now said in every brief).
8. **`sitrep` on this kit says `no integration branch`.** Its rule is `origin`'s default branch, else `main`, but this kit integrates on `developer`. Proposed: commit a `.sitrep.json` with `"integration_branch": "developer"`.

## Skills used on real work

Recorded in [the dogfood record](2026-11-25-dogfood/rollout.md).
