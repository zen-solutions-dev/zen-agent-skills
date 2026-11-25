"""Decide whether a change is documentation only, from the paths it changes.

One rule, two callers: `run-checks.py` reads it on a person's machine and in every CI cell,
so a docs-only change runs the same reduced gate set in both places and nobody restates the
rule in a workflow file (the shape `chore-0029` set for the link rule).

The answer is one of two scopes:

    docs   every changed path is documentation this repository's tests never read
    full   anything else, and every case where the answer could not be worked out

**"Run the tests when the answer is missing."** No git, an unknown base, a failed diff, or
an empty change all answer `full`. A wrong `docs` skips the test suite on a code change; a
wrong `full` costs a few minutes. Only the second is safe to fall into.

**A moved file counts at both its old and new path.** `git diff --name-status -M` reports a
rename as `R<score> old new`, and both paths are classified, so moving `scripts/x.py` to
`docs/x.md` is not docs-only.

What counts as documentation
----------------------------
A Markdown file, outside every tree whose Markdown is a deliverable or a contract, and not
one of the documents the test suite reads from the real repository:

- `.agents/` holds the skills and lenses themselves, which are what this kit ships;
  `.claude-plugin/` is their generated copy; `docs/spec/` holds contracts and their
  conformance matrices, which tests and gates read; `.quests/` is checked by the backlog
  gate and its template is read by tests; `tests/`, `scripts/` and `evals/` are code.
- `TESTED_DOCUMENTS` names each document a test opens from the real repository. A test that
  starts reading another one is caught by `tests/test_change_scope.py`, which scans the
  suite for `REPO_ROOT / ... "<name>.md"` reads and fails until the document is listed here.

Which base the change is measured against
-----------------------------------------
In a pull request's CI run, GitHub sets `GITHUB_BASE_REF` to the target branch, and the
change is `origin/<base>...HEAD`. On a person's machine the base is `ZEN_CHANGE_BASE` when
set, otherwise the first of `origin/developer` and `origin/main` that exists, and the
working tree's uncommitted and untracked files are added to the change. A push to a branch
(no pull request) has no base, so it is `full`.

`ZEN_CHECKS_SCOPE=full` forces the full gate set, for a person who wants every gate anyway.

Standard library only.
"""
from __future__ import annotations

import os
import subprocess
from pathlib import Path, PurePosixPath

REPO_ROOT = Path(__file__).resolve().parent.parent

DOCS = "docs"
FULL = "full"

# Trees whose Markdown is a deliverable, a contract, or read by a gate other than the
# documentation gates. A change under any of them is never docs-only.
NOT_DOCUMENTATION = (
    ".agents/",
    ".claude-plugin/",
    ".quests/",
    "docs/spec/",
    "evals/",
    "scripts/",
    "tests/",
)

# Documents the test suite opens from the real repository rather than a fixture. Kept
# honest by tests/test_change_scope.py, which finds every such read in tests/.
TESTED_DOCUMENTS = frozenset({
    "AGENTS.md",
    "CLAUDE.md",
    "docs/CATALOG.md",
    "docs/OBSERVATORY.md",
})

LOCAL_BASES = ("origin/developer", "origin/main")


def is_documentation(path: str) -> bool:
    """True when a repository-relative path is documentation no test or code gate reads."""
    posix = str(PurePosixPath(path.replace("\\", "/")))
    if not posix.lower().endswith(".md"):
        return False
    if posix in TESTED_DOCUMENTS:
        return False
    return not any(posix.startswith(prefix) for prefix in NOT_DOCUMENTATION)


def classify(paths) -> tuple[str, str]:
    """`(scope, reason)` for a collection of changed paths. Empty means `full`."""
    paths = sorted(set(paths))
    if not paths:
        return FULL, "no changed paths found, so every gate runs"
    code = [p for p in paths if not is_documentation(p)]
    if code:
        shown = ", ".join(code[:3]) + (f" and {len(code) - 3} more" if len(code) > 3 else "")
        return FULL, f"{len(paths)} changed path(s), {len(code)} not documentation ({shown})"
    return DOCS, f"{len(paths)} changed path(s), all documentation"


def parse_name_status(text: str) -> list[str]:
    """Every path in `git diff --name-status` output; a rename or copy yields both paths."""
    paths = []
    for line in text.splitlines():
        fields = line.split("\t")
        if len(fields) < 2:
            continue
        paths.extend(f for f in fields[1:] if f)
    return paths


def _git(args, runner=None):
    runner = subprocess.run if runner is None else runner
    try:
        done = runner(["git", *args], cwd=str(REPO_ROOT), capture_output=True, text=True)
    except OSError:
        return None
    return done.stdout if done.returncode == 0 else None


def changed_paths(env=None, runner=None):
    """`(paths, base_description)`, or `(None, reason)` when the change cannot be worked out."""
    env = os.environ if env is None else env
    base_branch = env.get("GITHUB_BASE_REF", "").strip()
    in_ci = bool(env.get("GITHUB_ACTIONS"))
    if base_branch:
        base = f"origin/{base_branch}"
    elif in_ci:
        return None, "a CI run with no pull request base"
    else:
        base = env.get("ZEN_CHANGE_BASE", "").strip() or next(
            (b for b in LOCAL_BASES if _git(["rev-parse", "--verify", "--quiet", b], runner)),
            "")
        if not base:
            return None, "no base branch found (looked for " + ", ".join(LOCAL_BASES) + ")"
    committed = _git(["diff", "--name-status", "-M", f"{base}...HEAD"], runner)
    if committed is None:
        return None, f"could not diff against {base}"
    paths = parse_name_status(committed)
    if not in_ci:
        uncommitted = _git(["diff", "--name-status", "-M", "HEAD"], runner)
        untracked = _git(["ls-files", "--others", "--exclude-standard"], runner)
        if uncommitted is None or untracked is None:
            return None, "could not read the working tree"
        paths += parse_name_status(uncommitted) + [p for p in untracked.splitlines() if p]
    return paths, base


def decide(env=None, runner=None) -> tuple[str, str]:
    """The scope for this run, and a one-line reason a reader can check."""
    env = os.environ if env is None else env
    if env.get("ZEN_CHECKS_SCOPE", "").strip().lower() == FULL:
        return FULL, "ZEN_CHECKS_SCOPE=full"
    paths, where = changed_paths(env, runner)
    if paths is None:
        return FULL, f"the change could not be worked out ({where}), so every gate runs"
    scope, reason = classify(paths)
    return scope, f"{reason}, against {where}"


if __name__ == "__main__":
    scope, reason = decide()
    print(f"{scope}: {reason}")
