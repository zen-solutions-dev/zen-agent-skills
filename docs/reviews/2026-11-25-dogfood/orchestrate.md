# Dogfood record: Orchestrate and build (`feat-0107`), 2026-11-25

Every skill this workstream changed, what it ran on, the evidence, the verdict, and what changed.
Written by the `feat-0107` child of the round 2 orchestration on branch `zen/marjana-r2-orchestrate`,
cut from `d906b20`. A skill not exercised is recorded as not exercised, with the reason. The skills
were read from their `SKILL.md` files in the checkout: `orchestrate`, `fix-batch` and
`reconcile-worktrees` are user-invoked, so the session's skill tool did not list them, and the
others were read the same way for one consistent source.

| Skill | Ran on | Evidence | Verdict | What changed from the run |
|---|---|---|---|---|
| `tdd` | `systematic-debugging/scripts/hitl_loop.py`, written test-first in this quest | Six script tests and the structural tests written first and run: 5 failed for the right reason (the script and its phrases absent), 1 passed vacuously because Python itself exits 2 on a missing script; that test was tightened to assert the script's own message, then the script was written and all 59 passed | Worked: the vacuous pass was caught only because the red run was read test by test | The missing-file test asserts `cannot read the steps file` |
| `systematic-debugging` | Not exercised on a real defect | No defect arose in this quest that needed diagnosing | Not exercised. Its second independent run, `feat-0063`, stays owed | Twelve mutations of the new obligations (eight in the body, four in the script), each run one at a time against the suite: all twelve killed. That tests the suite, not the skill |
| `research` | The four upstream files this quest adapted from, fetched 2026-11-25 with `urllib` and digested with `hashlib` | Rarity applied: `software-factory` (6,110 bytes, `567326e9...`) and `claude-handoff` (1,424 bytes, `79357a18...`) are Purple, primary sources cited; `chief-of-staff` (4,470 bytes, `1f508d8e...`) is Blue: its digest on `main` equals the digest pinned at `d653911` on 2026-11-24, which shows the file is unchanged, not that a second independent source agrees (Gold at first, corrected in the fix round); the `claude --bg` and `--name` flags are Gold, `claude-handoff` confirmed by running `claude --help` (Claude Code 2.1.332) | Worked for citations; the ladder sorted four sources without a judgement call | None to the skill; the run is small and was not a full research file |
| `sitrep` | This repository at `e64a671` | `sitrep.py` printed `waiting on you: 0 [Green]`, `blocked: 2 [Green]`, `in flight: 1 [Purple]` | Matches the reconciled table: quest-entry counts are Green (secondary), a count read from git's state is Purple (primary). No script change needed | Text only, as the brief asked |
| `fix-batch` | The new `spec_digest` step, on `docs/spec/systematic-debugging.md` after this quest's amendment | `spec_digest.py` printed `unbound`, exit 0: approved with no `approved_digest`, so not a blocker | The step's command works as written. The batch itself, and the landing order, not exercised: this quest dispatched no batch | None |
| `reconcile-worktrees` | The `merge-tree` form in Step 5, against the real integration tip | `git merge-tree --write-tree origin/zen/marjana-r2-2026-11-25 HEAD` printed one tree id and exited 0, so no conflicted path: the documented "lists conflicted paths, if any" holds | Command form checked. Nothing was landed: a child lands nothing | None |
| `orchestrate` | Its memory: six entries under `docs/agents/memory/` ingested from this round's sources, then the lint | Lint over the 7 files: no orphan, no dead index link, no undated entry, no bare "currently"; the six entries read by hand for contradictions, none found | Ingest and lint worked on a small memory. Steps 1 to 6 (probe, exploration child, start slow, five questions, relays, landing) not exercised: this session is a leaf and orchestrates nothing | The `memory` key names the index file, because the approved `zen-config` contract types `memory` as a file; found while writing the key |
| `agent-handoff` | The optional `claude --bg` section | Flags checked with `claude --help` on Claude Code 2.1.332: `--bg, --background` and `-n, --name` exist | Line checked; no session launched, since nothing in this quest needed one | None |
| `verifier-agent` | Not changed and not exercised | Owned by this workstream; no item required a change | Not exercised | None |

## Fix round, 2026-11-25

An independent verifier returned `fail` on `93f7ef3`. What the fixes ran on, with evidence:

- **`tdd`, again on `hitl_loop.py`**: the unwritable-log test was written first and watched fail
  for the right reason (exit 1, a traceback, after both a `y` and an `n` answer), then the fix made
  it pass. Two mutations of the fix (the `except` narrowed so `OSError` escapes, and the failure
  path returning 1) were both killed. Three more mutations of the new skill sentences (`S-019`'s
  unattended branch, `S-020`'s threshold, the redaction note for the script's log) were also killed.
- **`research` and `sitrep`**: the ladder is one canonical block, found exactly once by a
  byte-for-byte search in each of `GLOSSARY.md`, `research/SKILL.md` and `sitrep/SKILL.md`.
  `sitrep.py` printed the same tiers as before (`[Green]` for quest-entry counts, `[Purple]` for
  the git count), and its script is unchanged.
- **`orchestrate` memory**: the three lesson entries now cite verified shas (`d15026a`, `0ef68e0`
  and `027b835` on `zen/marjana-r2-platform`, `d64f08c` and `7845524`). Each was checked with
  `git log` and `git merge-base --is-ancestor` before it was cited.

