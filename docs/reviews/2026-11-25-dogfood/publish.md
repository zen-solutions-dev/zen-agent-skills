# Dogfood: tracker publishing (`feat-0106`)

Run on 2026-11-25 by the agent that built [`publish.py`](../../../.agents/skills/new-quest/scripts/publish.py) and the `triage` draft, on branch `zen/marjana-r2-publish`. **Not an independent run (`A7`)**: the author ran it. The brief allowed the dry run only, on this repository's own `.quests/`; no real repository was written to, and no `gh` call reached GitHub.

## What was run

| Run | Where | Command | Result |
|---|---|---|---|
| A | This checkout, as configured (no `publish` key) | `python3 .agents/skills/new-quest/scripts/publish.py`, then with `--apply` | "Publishing is off: docs/agents/zen.md does not set publish: github. Nothing was read from or sent to GitHub." Exit 0, then exit 1 |
| B | A local clone in the session scratchpad, with `publish: github` and `publish_repo: zen-solutions-dev/zen-agent-skills` added to its `docs/agents/zen.md` | `publish.py --offline` | 38 operations planned, exit 0, nothing changed |
| C | An empty git repository that opts in, no quest file | `publish.py --offline` | First run: "1 operation(s)", creating `zen:published` for no issue. **A defect, fixed**: labels are now planned only when an issue will carry one, pinned by `test_empty_tracker_plans_nothing`. After the fix: 0 operations |
| D | A directory that is not a git repository | `publish.py --repo-root <dir> --offline` | "Could not list tracked files with git (...); nothing planned." Exit 2 |

Run B's plan, in summary: 4 labels to create; 3 spec issues (`sitrep`, `systematic-debugging`, `zen-config`); 23 quest issues, one per quest in `.quests/` that is not done; 6 sub-issue links; 2 blocked-by links (`feat-0071` by `feat-0070`, `feat-0102` by `feat-0101`). None of the 242 quests in `done/` was planned, as Q2 says. The one note was the offline one. Its first line, verbatim:

```text
Dry run: 38 operation(s) on zen-solutions-dev/zen-agent-skills, from 265 quest file(s).
```

The rendered bodies were inspected for two items. `Spec: zen-config` is 32,090 characters, under the limit, with every relative link absolute at `developer` and the marker last. `feat-0106`'s issue opens with the approved first line and the frontmatter table.

## What it showed

- **The plan is honest about in-flight state.** `feat-0101` to `feat-0106` would be published as `zen:in-progress`, because round 2 leaves landed quest files in place until close (B2). Publishing mirrors the files exactly, including when the files lag.
- **A first publish is large.** 38 operations for a tracker this size. The procedure says to state the count to the person before the apply.
- **The degenerate inputs were where the defect was.** Run C found the one wrong behaviour of the session; the tests built from the scenarios had all passed before it.

## What was not exercised

- **A live `--apply`.** Nothing was written to any GitHub repository. The REST endpoints (`issues`, `labels`, `sub_issues`, `sub_issue`, `dependencies/blocked_by`) and their payloads follow GitHub's documentation as read by the author. The tests' fake encodes the same reading, so a misreading would pass the tests and fail the first live apply. The first adopter to opt in should run the dry run, then `--apply` on a scratch repository first.
- **A dry run that reads GitHub** (without `--offline`). That would have listed issues in the real repository; it was not run.
- **`triage`**: no run against real issues. Its rows in the conformance matrix are prose only.
