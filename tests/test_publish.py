"""Tests for .agents/skills/new-quest/scripts/publish.py and the publishing keys (feat-0106).

Derived from the publishing scenarios of docs/spec/zen-config.md (S-047 to S-058); each test
names the scenario it covers. The script's seam is its command line, `main()`, with the `gh`
runner injected: the fake below holds an in-memory repository of issues, labels, sub-issues
and blocking links, answers the REST calls the script makes, and records every call. No test
touches the network or a real repository.

test-quality notes: the oracle is GitHub's resulting state (titles, bodies, states, labels,
links) and the list of calls, never "did not crash". Every fixture is a real git index in a
temporary directory with the repository's own validate.py, because the script decides what
it may publish from `git ls-files` and from that validator. What this cannot cover is the real
GitHub API: the fake answers the endpoints as their documentation describes them, and a live
apply is not exercised (recorded in docs/reviews/2026-11-25-dogfood/publish.md).

The validator's checks of the new keys are driven against both copies of validate.py, for
the reason test_zen_config.py gives.
"""
import contextlib
import importlib.util
import io
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / ".agents" / "skills" / "new-quest" / "scripts" / "publish.py"
COPIES = {
    "repository": REPO_ROOT / ".quests" / "validate.py",
    "template": (REPO_ROOT / ".agents" / "skills" / "init-worktracking" / "templates"
                 / "validate.py"),
}


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


publish = _load("zen_publish_under_test", SCRIPT)
VALIDATORS = {name: _load(f"publish_validate_{name}", path) for name, path in COPIES.items()}

REPO = "octo-org/octo-repo"
CONFIG = """# Agent skills setup

```zen-config
config_version: 1
tracker: quests
spec_dir: docs/spec
base_branch: main
{extra}
```
"""
ON = f"publish: github\npublish_repo: {REPO}"


def quest(qid, title="Do the thing", status="open", depends_on="[]", spec="", extra="",
          body="## Problem\n\nSee [the spec](../docs/spec/alpha.md#goals)."):
    return f"""---
id: {qid}
title: {title}
type: feat
status: {status}
priority: P1
parent: "a goal"
depends_on: {depends_on}
spec: "{spec}"
{extra}touched_files:
  - README.md
created: 2026-11-25
---

{body}
"""


SPEC = """---
title: alpha
status: approved
---

# alpha

## Goals

Text of the spec.
"""


class FakeGitHub:
    """An in-memory GitHub repository answering the REST calls publish.py makes."""

    def __init__(self):
        self.issues = {}
        self.labels = set()
        self.calls = []
        self.requests = []
        self.fail_on = None
        self._next = 1

    def add_issue(self, title, body, labels, state="open"):
        number = self._next
        self._next += 1
        self.issues[number] = {"number": number, "id": 1000 + number, "title": title,
                               "body": body, "state": state, "labels": set(labels),
                               "children": set(), "blocked_by": set()}
        return self.issues[number]

    def by_id(self, db_id):
        return next(i for i in self.issues.values() if i["id"] == db_id)

    def _view(self, issue):
        return {"number": issue["number"], "id": issue["id"], "title": issue["title"],
                "body": issue["body"], "state": issue["state"],
                "labels": [{"name": n} for n in sorted(issue["labels"])]}

    def __call__(self, args, stdin=None):
        self.calls.append((list(args), stdin))
        assert args[0] == "api", args
        method = args[args.index("-X") + 1] if "-X" in args else "GET"
        fields = {}
        rest = [a for a in args[1:] if a != "--paginate"]
        i, path = 0, None
        while i < len(rest):
            if rest[i] in ("-X", "--input"):
                i += 2
            elif rest[i] == "-f":
                k, _, v = rest[i + 1].partition("=")
                fields[k] = v
                i += 2
            else:
                path = rest[i]
                i += 1
        self.requests.append((method, path))
        if self.fail_on and self.fail_on(method, path):
            return 1, "", "HTTP 502: simulated failure"
        data = json.loads(stdin) if stdin else {}
        parts = path.split("/")[3:]  # after repos/owner/name
        if parts == ["issues"] and method == "GET":
            want = fields.get("labels")
            found = [self._view(i) for i in self.issues.values() if want in i["labels"]]
            return 0, json.dumps(found), ""
        if parts == ["labels"] and method == "GET":
            return 0, json.dumps([{"name": n} for n in sorted(self.labels)]), ""
        if parts == ["labels"] and method == "POST":
            self.labels.add(data["name"])
            return 0, json.dumps({"name": data["name"]}), ""
        if parts == ["issues"] and method == "POST":
            issue = self.add_issue(data["title"], data["body"], data["labels"])
            return 0, json.dumps(self._view(issue)), ""
        issue = self.issues[int(parts[1])]
        if len(parts) == 2 and method == "PATCH":
            for key in ("title", "body", "state"):
                if key in data:
                    issue[key] = data[key]
            return 0, json.dumps(self._view(issue)), ""
        if parts[2:] == ["labels"] and method == "POST":
            issue["labels"].update(data["labels"])
            return 0, "[]", ""
        if parts[2] == "labels" and method == "DELETE":
            issue["labels"].discard("/".join(parts[3:]))
            return 0, "", ""
        if parts[2:] == ["sub_issues"]:
            if method == "GET":
                return 0, json.dumps([self._view(self.issues[n])
                                      for n in sorted(issue["children"])]), ""
            child = self.by_id(data["sub_issue_id"])["number"]
            holders = [i for i in self.issues.values() if child in i["children"]]
            if holders and not data.get("replace_parent"):
                return 1, "", "HTTP 422: the issue already has a parent"
            for holder in holders:
                holder["children"].discard(child)
            issue["children"].add(child)
            return 0, "{}", ""
        if parts[2:] == ["sub_issue"] and method == "DELETE":
            issue["children"].discard(self.by_id(data["sub_issue_id"])["number"])
            return 0, "{}", ""
        if parts[2:4] == ["dependencies", "blocked_by"]:
            if method == "GET":
                return 0, json.dumps([self._view(self.issues[n])
                                      for n in sorted(issue["blocked_by"])]), ""
            if method == "POST":
                issue["blocked_by"].add(self.by_id(data["issue_id"])["number"])
                return 0, "{}", ""
            issue["blocked_by"].discard(self.by_id(int(parts[4]))["number"])
            return 0, "", ""
        raise AssertionError(f"unexpected call {method} {path}")

    def writes(self):
        return [c for c in self.calls if "-X" in c[0] and c[0][c[0].index("-X") + 1] != "GET"]

    def find(self, prefix):
        found = [i for i in self.issues.values() if i["title"].startswith(prefix)]
        assert len(found) == 1, (prefix, [i["title"] for i in self.issues.values()])
        return found[0]


class Repo:
    """A temporary git repository with the kit's validator and a setup file."""

    def __init__(self, extra=ON):
        self.dir = tempfile.TemporaryDirectory()
        self.root = Path(self.dir.name)
        (self.root / ".quests" / "done").mkdir(parents=True)
        (self.root / "docs" / "spec").mkdir(parents=True)
        (self.root / "docs" / "agents").mkdir(parents=True)
        shutil.copy(COPIES["repository"], self.root / ".quests" / "validate.py")
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        self.write("docs/agents/zen.md", CONFIG.format(extra=extra))
        self.write("docs/spec/alpha.md", SPEC)
        # Every quest fixture names README.md in touched_files, which validate.py checks.
        self.write("README.md", "# fixture\n")

    def write(self, rel, text, track=True):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        if track:
            subprocess.run(["git", "-C", str(self.root), "add", rel], check=True)

    def remove(self, rel):
        subprocess.run(["git", "-C", str(self.root), "rm", "-q", "-f", rel], check=True)

    def move(self, src, dst):
        subprocess.run(["git", "-C", str(self.root), "mv", src, dst], check=True)

    def close_quest(self, qid, src, **kwargs):
        """Move a quest to done/ with status done, as the lifecycle does."""
        dst = src.replace(".quests/", ".quests/done/")
        self.move(src, dst)
        kwargs.setdefault("body", "## Problem\n\nSee [the spec](../../docs/spec/alpha.md#goals).")
        self.write(dst, quest(qid, status="done", **kwargs))

    def run(self, *args, runner=None):
        out = io.StringIO()
        code = publish.main(["--repo-root", str(self.root), *args], runner=runner, out=out)
        return code, out.getvalue()

    def close(self):
        self.dir.cleanup()


class PublishTest(unittest.TestCase):
    def setUp(self):
        self.repo = Repo()
        self.addCleanup(self.repo.close)
        self.gh = FakeGitHub()

    def publish(self):
        code, out = self.repo.run("--apply", runner=self.gh)
        self.assertEqual(code, 0, out)
        return out

    def plan(self):
        code, out = self.repo.run(runner=self.gh)
        self.assertEqual(code, 0, out)
        return out


class OffByDefault(unittest.TestCase):
    """S-049: absent, `none` or malformed keys leave publishing off and call nothing."""

    def check_off(self, extra, expect):
        repo = Repo(extra=extra)
        self.addCleanup(repo.close)
        repo.write(".quests/feat-0001-a.md", quest("feat-0001"))
        gh = FakeGitHub()
        for args in ([], ["--apply"]):
            code, out = repo.run(*args, runner=gh)
            self.assertIn("Publishing is off", out)
            self.assertIn(expect, out)
            self.assertEqual(code, 1 if args else 0)
        self.assertEqual(gh.calls, [])

    def test_absent_key_is_off(self):
        self.check_off("", "does not set publish: github")

    def test_none_is_off(self):
        self.check_off(f"publish: none\npublish_repo: {REPO}", "does not set publish: github")

    def test_missing_repo_is_off(self):
        self.check_off("publish: github", "publish_repo")

    def test_malformed_repo_is_off(self):
        self.check_off("publish: github\npublish_repo: not a repo", "publish_repo")

    def test_unknown_value_is_off(self):
        self.check_off(f"publish: gitlab\npublish_repo: {REPO}", "publish 'gitlab'")

    def test_other_tracker_is_off(self):
        repo = Repo(extra=ON)
        self.addCleanup(repo.close)
        repo.write("docs/agents/zen.md", CONFIG.format(extra=ON).replace(
            "tracker: quests", "tracker: github"))
        code, out = repo.run(runner=FakeGitHub())
        self.assertIn("Publishing is off", out)
        self.assertIn("mirrors the local tracker", out)

    def test_validator_without_publishing_is_off(self):
        repo = Repo()
        self.addCleanup(repo.close)
        path = repo.root / ".quests" / "validate.py"
        path.write_text(path.read_text(encoding="utf-8").replace(
            "ZEN_PUBLISH_REPO_RE", "OLD_NAME"), encoding="utf-8")
        code, out = repo.run(runner=FakeGitHub())
        self.assertIn("predates publishing", out)


class DryRun(PublishTest):
    def test_dry_run_writes_nothing(self):
        """S-051: the default run lists the plan and makes only GET calls."""
        self.repo.write(".quests/feat-0001-a.md", quest("feat-0001", spec="docs/spec/alpha.md"))
        out = self.plan()
        self.assertIn("create quest feat-0001", out)
        self.assertIn("create spec alpha", out)
        self.assertIn("Nothing was changed", out)
        self.assertEqual(self.gh.writes(), [])
        self.assertEqual(self.gh.issues, {})

    def test_empty_tracker_plans_nothing(self):
        """S-051: a tracker with no quest plans no operation, not even a label."""
        self.assertIn("0 operation(s)", self.plan())
        self.publish()
        self.assertEqual(self.gh.labels, set())

    def test_offline_calls_nothing(self):
        """S-051: --offline plans without calling gh at all."""
        self.repo.write(".quests/feat-0001-a.md", quest("feat-0001"))
        code, out = self.repo.run("--offline", runner=self.gh)
        self.assertEqual(code, 0)
        self.assertIn("create quest feat-0001", out)
        self.assertEqual(self.gh.calls, [])


class Shape(PublishTest):
    def test_issue_shape(self):
        """S-052: titles, first line, table, rewritten links and the marker, last."""
        self.repo.write(".quests/feat-0001-a.md", quest("feat-0001", spec="docs/spec/alpha.md"))
        self.publish()
        issue = self.gh.find("feat-0001: ")
        self.assertEqual(issue["title"], "feat-0001: Do the thing")
        lines = issue["body"].split("\n")
        self.assertTrue(lines[0].startswith(
            f"_Published from [`.quests/feat-0001-a.md`](https://github.com/{REPO}/blob/main/"
            ".quests/feat-0001-a.md) by the Zen kit's `new-quest`. The file is the source of "
            "truth: edits made here are overwritten on the next publish._"))
        self.assertIn("| id | `feat-0001` |", issue["body"])
        self.assertIn(f"[the spec](https://github.com/{REPO}/blob/main/docs/spec/alpha.md#goals)",
                      issue["body"])
        self.assertRegex(lines[-1], r"^<!-- zen-publish v1 kind=quest id=feat-0001 "
                                    r"source=\.quests/feat-0001-a\.md digest=[0-9a-f]{12} -->$")
        self.assertEqual(issue["labels"], {"zen:published", "zen:quest"})
        spec = self.gh.find("Spec: alpha")
        self.assertEqual(spec["labels"], {"zen:published", "zen:spec"})
        self.assertIn("kind=spec id=alpha source=docs/spec/alpha.md", spec["body"])
        self.assertEqual(spec["children"], {issue["number"]})
        self.assertEqual(self.gh.labels, set(publish.ZEN_LABELS) - {"zen:in-progress"})

    def test_fenced_links_are_left_alone(self):
        """S-052: a link inside fenced code is text, not rewritten."""
        body = "```\n[x](../a.md)\n```\n[y](../a.md)"
        self.repo.write("a.md", "a\n")
        self.repo.write(".quests/feat-0001-a.md", quest("feat-0001", body=body))
        self.publish()
        text = self.gh.find("feat-0001")["body"]
        self.assertIn("```\n[x](../a.md)\n```", text)
        self.assertIn(f"[y](https://github.com/{REPO}/blob/main/a.md)", text)

    def test_long_body_is_truncated_under_the_limit(self):
        """S-052: a body over GitHub's limit is cut at a heading, and the marker kept."""
        body = "\n\n".join(f"## Part {n}\n\n" + "x" * 3000 for n in range(40))
        self.repo.write(".quests/feat-0001-a.md", quest("feat-0001", body=body))
        self.publish()
        text = self.gh.find("feat-0001")["body"]
        self.assertLessEqual(len(text), publish.BODY_LIMIT)
        self.assertIn("_Truncated: GitHub holds at most", text)
        self.assertTrue(text.split("\n")[-1].startswith("<!-- zen-publish v1"))


class Idempotence(PublishTest):
    def test_second_run_plans_nothing(self):
        """S-053: a re-run with nothing changed plans no operation."""
        self.repo.write(".quests/feat-0001-a.md", quest("feat-0001", spec="docs/spec/alpha.md"))
        self.repo.write(".quests/feat-0002-b.md", quest("feat-0002", depends_on="[feat-0001]"))
        self.publish()
        count = len(self.gh.issues)
        self.assertIn("0 operation(s)", self.plan())
        self.publish()
        self.assertEqual(len(self.gh.issues), count)

    def test_changed_file_edits_its_issue(self):
        """S-053: a changed quest edits the same issue, never a second one."""
        self.repo.write(".quests/feat-0001-a.md", quest("feat-0001"))
        self.publish()
        self.repo.write(".quests/feat-0001-a.md", quest("feat-0001", title="Renamed"))
        self.publish()
        self.assertEqual(len(self.gh.issues), 1)
        self.assertEqual(self.gh.find("feat-0001")["title"], "feat-0001: Renamed")

    def test_edit_on_github_is_overwritten(self):
        """S-053: the file is the source of truth; a hand edit to the body is replaced."""
        self.repo.write(".quests/feat-0001-a.md", quest("feat-0001"))
        self.publish()
        issue = self.gh.find("feat-0001")
        original = issue["body"]
        issue["body"] = "edited by hand\n\n" + original
        self.publish()
        self.assertEqual(issue["body"], original)

    def test_issue_is_found_by_marker_not_title(self):
        """S-053: an issue retitled by hand is still the quest's issue."""
        self.repo.write(".quests/feat-0001-a.md", quest("feat-0001"))
        self.publish()
        self.gh.find("feat-0001")["title"] = "something else"
        self.publish()
        self.assertEqual(len(self.gh.issues), 1)


class Status(PublishTest):
    def test_done_closes_and_open_reopens(self):
        """S-054: done closes the issue; an issue closed on GitHub while open is reopened."""
        self.repo.write(".quests/feat-0001-a.md", quest("feat-0001"))
        self.publish()
        issue = self.gh.find("feat-0001")
        issue["state"] = "closed"
        self.assertIn("reopen #", self.plan())
        self.publish()
        self.assertEqual(issue["state"], "open")
        self.repo.close_quest("feat-0001", ".quests/feat-0001-a.md")
        self.publish()
        self.assertEqual(issue["state"], "closed")
        self.assertIn("source=.quests/done/feat-0001-a.md", issue["body"])

    def test_done_never_published_gets_no_issue(self):
        """S-054: a quest already done when first seen is not published."""
        self.repo.write(".quests/done/feat-0001-a.md", quest("feat-0001", status="done"))
        self.publish()
        self.assertEqual(self.gh.issues, {})

    def test_in_progress_label(self):
        """S-054: status in_progress carries zen:in-progress, removed when it changes."""
        self.repo.write(".quests/feat-0001-a.md", quest("feat-0001", status="in_progress"))
        self.publish()
        issue = self.gh.find("feat-0001")
        self.assertIn("zen:in-progress", issue["labels"])
        self.repo.write(".quests/feat-0001-a.md", quest("feat-0001"))
        self.publish()
        self.assertNotIn("zen:in-progress", issue["labels"])

    def test_spec_closes_with_its_last_quest(self):
        """S-054: a spec issue is open while any of its quests is."""
        self.repo.write(".quests/feat-0001-a.md", quest("feat-0001", spec="docs/spec/alpha.md"))
        self.publish()
        self.repo.close_quest("feat-0001", ".quests/feat-0001-a.md", spec="docs/spec/alpha.md")
        self.publish()
        self.assertEqual(self.gh.find("Spec: alpha")["state"], "closed")


class Ownership(PublishTest):
    def test_role_labels_are_never_touched(self):
        """S-055: role.* labels a person or triage applied survive every publish."""
        self.repo.write(".quests/feat-0001-a.md", quest("feat-0001", status="in_progress"))
        self.publish()
        issue = self.gh.find("feat-0001")
        issue["labels"].add("ready for agent")
        self.repo.write(".quests/feat-0001-a.md", quest("feat-0001", title="New"))
        self.publish()
        self.assertIn("ready for agent", issue["labels"])
        removed = [r[1] for r in self.gh.requests if r[0] == "DELETE" and "/labels/" in r[1]]
        self.assertEqual(removed, [f"repos/{REPO}/issues/{issue['number']}/labels/zen:in-progress"])

    def test_unmarked_issue_is_left_alone(self):
        """S-055: an issue with the label and no marker is reported and not touched."""
        stray = self.gh.add_issue("feat-0001: by hand", "no marker", {"zen:published"})
        self.repo.write(".quests/feat-0001-a.md", quest("feat-0001"))
        out = self.publish()
        self.assertIn(f"#{stray['number']} carries zen:published but no valid marker", out)
        self.assertEqual(stray["body"], "no marker")
        self.assertEqual(len(self.gh.issues), 2)

    def test_repeated_marker_is_left_alone(self):
        """S-055: a second issue with the same marker is named and not touched."""
        self.repo.write(".quests/feat-0001-a.md", quest("feat-0001"))
        self.publish()
        first = self.gh.find("feat-0001")
        copy = self.gh.add_issue("a copy", first["body"], set(first["labels"]))
        self.repo.write(".quests/feat-0001-a.md", quest("feat-0001", title="Changed"))
        out = self.publish()
        self.assertIn(f"#{copy['number']} repeats the marker of #{first['number']}", out)
        self.assertEqual(copy["title"], "a copy")
        self.assertEqual(first["title"], "feat-0001: Changed")

    def test_nothing_is_ever_deleted(self):
        """S-056: a quest file removed leaves its issue as it was, reported."""
        self.repo.write(".quests/feat-0001-a.md", quest("feat-0001"))
        self.publish()
        issue = dict(self.gh.find("feat-0001"))
        self.repo.remove(".quests/feat-0001-a.md")
        out = self.publish()
        self.assertIn("has no quest file any more: left as it is", out)
        self.assertEqual(self.gh.find("feat-0001")["state"], issue["state"])
        self.assertFalse([r for r in self.gh.requests
                          if r[0] == "DELETE" and re.search(r"/issues/\d+$", r[1])])
        self.assertFalse([r for r in self.gh.requests if "transfer" in r[1]])


class Privacy(PublishTest):
    def test_private_quest_is_not_published(self):
        """S-057: private: true keeps a quest off GitHub."""
        self.repo.write(".quests/feat-0001-a.md", quest("feat-0001", extra="private: true\n"))
        self.publish()
        self.assertEqual(self.gh.issues, {})

    def test_private_after_publish_is_left_and_reported(self):
        """S-057: a quest made private after publishing is reported, never edited or closed."""
        self.repo.write(".quests/feat-0001-a.md", quest("feat-0001"))
        self.publish()
        before = dict(self.gh.find("feat-0001"))
        self.repo.write(".quests/feat-0001-a.md",
                        quest("feat-0001", title="Secret", extra="private: true\n"))
        out = self.publish()
        self.assertIn("feat-0001 is private now", out)
        self.assertEqual(self.gh.find("feat-0001")["title"], before["title"])

    def test_private_spec_is_not_published(self):
        """S-057: a private spec gets no issue; its quests are top-level."""
        self.repo.write("docs/spec/alpha.md", SPEC.replace("status: approved",
                                                           "status: approved\nprivate: true"))
        self.repo.write(".quests/feat-0001-a.md", quest("feat-0001", spec="docs/spec/alpha.md"))
        self.publish()
        self.assertEqual([i["title"] for i in self.gh.issues.values()], ["feat-0001: Do the thing"])

    def test_untracked_files_are_not_published(self):
        """S-057: only files git tracks in .quests/ and the spec directory are candidates."""
        self.repo.write(".quests/feat-0001-a.md", quest("feat-0001"), track=False)
        self.repo.write(".quests/feat-0002-b.md", quest("feat-0002", spec="docs/other/x.md"))
        self.repo.write("docs/other/x.md", SPEC)
        out = self.publish()
        self.assertEqual([i["title"] for i in self.gh.issues.values()], ["feat-0002: Do the thing"])
        self.assertIn("is not a spec file directly in docs/spec", out)


class Links(PublishTest):
    def test_dependencies_follow_the_files(self):
        """S-058: depends_on becomes blocked-by, and a removed dependency is unlinked."""
        self.repo.write(".quests/feat-0001-a.md", quest("feat-0001"))
        self.repo.write(".quests/feat-0002-b.md", quest("feat-0002", depends_on="[feat-0001]"))
        self.publish()
        one, two = self.gh.find("feat-0001"), self.gh.find("feat-0002")
        self.assertEqual(two["blocked_by"], {one["number"]})
        self.repo.write(".quests/feat-0002-b.md", quest("feat-0002"))
        self.publish()
        self.assertEqual(two["blocked_by"], set())

    def test_quest_moving_between_specs(self):
        """S-058: a quest whose spec changes moves to the new spec's issue."""
        self.repo.write("docs/spec/beta.md", SPEC.replace("alpha", "beta"))
        self.repo.write(".quests/feat-0001-a.md", quest("feat-0001", spec="docs/spec/alpha.md"))
        self.repo.write(".quests/feat-0002-b.md", quest("feat-0002", spec="docs/spec/beta.md"))
        self.publish()
        self.repo.write(".quests/feat-0001-a.md", quest("feat-0001", spec="docs/spec/beta.md"))
        self.publish()
        q = self.gh.find("feat-0001")["number"]
        self.assertEqual(self.gh.find("Spec: alpha")["children"], set())
        self.assertIn(q, self.gh.find("Spec: beta")["children"])

    def test_quest_without_spec_is_top_level(self):
        """S-058: no spec, no parent issue."""
        self.repo.write(".quests/feat-0001-a.md", quest("feat-0001"))
        self.publish()
        self.assertEqual(len(self.gh.issues), 1)


class Failure(PublishTest):
    def test_apply_stops_at_the_first_failure_and_resumes(self):
        """S-051: a failed call stops the run; the next run finishes without duplicates."""
        self.repo.write(".quests/feat-0001-a.md", quest("feat-0001"))
        self.repo.write(".quests/feat-0002-b.md", quest("feat-0002"))
        created = []
        self.gh.fail_on = lambda m, p: m == "POST" and p.endswith("/issues") and (
            created.append(1) or len(created) == 2)
        code, out = self.repo.run("--apply", runner=self.gh)
        self.assertEqual(code, 1)
        self.assertIn("Stopped:", out)
        self.assertEqual(len(self.gh.issues), 1)
        self.gh.fail_on = None
        self.publish()
        self.assertEqual(sorted(i["title"][:9] for i in self.gh.issues.values()),
                         ["feat-0001", "feat-0002"])

    def test_apply_without_gh_cannot_run(self):
        self.repo.write(".quests/feat-0001-a.md", quest("feat-0001"))

        def broken(args, stdin=None):
            return 4, "", "gh: not logged in"
        code, out = self.repo.run("--apply", runner=broken)
        self.assertEqual(code, 2)
        self.assertIn("Cannot apply", out)


def marker_of(qid, path, digest="0123456789ab"):
    return f"<!-- zen-publish v1 kind=quest id={qid} source={path} digest={digest} -->"


class ReviewFixes(PublishTest):
    """The feat-0106 verifier's reproductions (F1 to F7, F9), each re-run after the fix."""

    def apply_three_times(self):
        for _ in range(3):
            self.publish()

    def test_f1_a_body_carrying_another_quests_marker(self):
        """F1: marker text in a quest body, bare or fenced, never changes an identity."""
        other = marker_of("feat-0002", ".quests/feat-0002-b.md")
        body = f"## Problem\n\n{other}\n\n```\n{other}\n```\n\nText."
        self.repo.write(".quests/feat-0001-a.md", quest("feat-0001", body=body))
        self.repo.write(".quests/feat-0002-b.md", quest("feat-0002", title="Second"))
        self.apply_three_times()
        self.assertEqual(sorted(i["title"] for i in self.gh.issues.values()),
                         ["feat-0001: Do the thing", "feat-0002: Second"])
        first, second = self.gh.find("feat-0001"), self.gh.find("feat-0002")
        self.assertNotIn("\n<!-- zen-publish v1 kind=quest id=feat-0002", first["body"])
        self.assertIn("&lt;!-- zen-publish v1 kind=quest id=feat-0002", first["body"])
        self.assertEqual(publish.last_marker(first["body"]).group(2), "feat-0001")
        self.assertEqual(publish.last_marker(second["body"]).group(2), "feat-0002")

    def test_f1_a_forger_that_sorts_first(self):
        """F1: an earlier issue with another quest's marker mid-body is not that quest's."""
        forged = self.gh.add_issue("forged", "intro\n" + marker_of(
            "feat-0001", ".quests/feat-0001-a.md") + "\nnot a marker last", {"zen:published"})
        self.repo.write(".quests/feat-0001-a.md", quest("feat-0001"))
        self.apply_three_times()
        self.assertEqual(forged["title"], "forged")
        self.assertTrue(forged["body"].endswith("not a marker last"))
        self.assertEqual(len([i for i in self.gh.issues.values()
                              if i["title"].startswith("feat-0001")]), 1)

    def test_f2_orphaned_and_private_quests_keep_their_links(self):
        """F2: a quest gone or made private keeps its sub-issue and blocked-by links."""
        spec = "docs/spec/alpha.md"
        self.repo.write(".quests/feat-0001-a.md", quest("feat-0001", spec=spec))
        self.repo.write(".quests/feat-0002-b.md", quest("feat-0002", spec=spec,
                                                         depends_on="[feat-0001]"))
        self.repo.write(".quests/feat-0003-c.md", quest("feat-0003", spec=spec,
                                                         depends_on="[feat-0002]"))
        self.publish()
        one, two, three = (self.gh.find(f"feat-000{n}") for n in (1, 2, 3))
        alpha = self.gh.find("Spec: alpha")
        self.repo.remove(".quests/feat-0001-a.md")
        self.repo.write(".quests/feat-0002-b.md", quest("feat-0002", spec=spec,
                                                         extra="private: true\n"))
        before = {n: dict(i, labels=set(i["labels"])) for n, i in self.gh.issues.items()}
        out = self.publish()
        self.assertIn("has no quest file any more: left as it is", out)
        self.assertIn("feat-0002 is private now", out)
        self.assertEqual(alpha["children"], {one["number"], two["number"], three["number"]})
        self.assertEqual(two["blocked_by"], {one["number"]})
        self.assertEqual(three["blocked_by"], {two["number"]})
        for issue in (one, two):
            self.assertEqual(issue["body"], before[issue["number"]]["body"])
            self.assertEqual(issue["state"], before[issue["number"]]["state"])

    def test_f2_a_private_spec_keeps_its_children_and_is_noted_once(self):
        """F2: a spec made private keeps its sub-issues; the note appears once."""
        spec = "docs/spec/alpha.md"
        self.repo.write(".quests/feat-0001-a.md", quest("feat-0001", spec=spec))
        self.repo.write(".quests/feat-0002-b.md", quest("feat-0002", spec=spec))
        self.publish()
        alpha = self.gh.find("Spec: alpha")
        children = set(alpha["children"])
        self.repo.write("docs/spec/alpha.md", SPEC.replace("status: approved",
                                                           "status: approved\nprivate: true"))
        out = self.publish()
        self.assertEqual(alpha["children"], children)
        self.assertEqual(out.count("spec alpha is private now"), 1)

    def test_f3_truncation_never_cuts_inside_a_fence(self):
        """F3: a `#` line inside a fence is not a heading, and no cut lands in a fence."""
        fenced = "```bash\n" + "\n".join(f"# comment {n}\necho {'x' * 60}"
                                          for n in range(1200)) + "\n```"
        body = "## Intro\n\nShort.\n\n" + fenced + "\n\n## After\n\nEnd."
        self.repo.write(".quests/feat-0001-a.md", quest("feat-0001", body=body))
        self.publish()
        text = self.gh.find("feat-0001")["body"]
        self.assertLessEqual(len(text), publish.BODY_LIMIT)
        kept = text.split("_Truncated:")[0]
        self.assertEqual(kept.count("```") % 2, 0, "the cut left a fence open")
        self.assertGreater(len(kept), publish.BODY_LIMIT // 2)

    def test_f3_an_early_heading_does_not_lose_the_body(self):
        """F3: with the last heading early, the cut falls back to a paragraph break."""
        body = "## Only heading\n\n" + "\n\n".join("word " * 200 for _ in range(100))
        self.repo.write(".quests/feat-0001-a.md", quest("feat-0001", body=body))
        self.publish()
        text = self.gh.find("feat-0001")["body"]
        self.assertLessEqual(len(text), publish.BODY_LIMIT)
        self.assertGreater(len(text), publish.BODY_LIMIT // 2)

    def test_f4_a_path_the_marker_cannot_carry_is_refused(self):
        """F4: whitespace in a path is refused with a message, never published."""
        self.repo.write(".quests/feat-0001 a.md", quest("feat-0001"))
        out = self.publish()
        self.assertEqual(self.gh.issues, {})
        self.assertIn("holds a character the marker cannot carry", out)

    def test_f4_a_quest_validate_rejects_is_skipped(self):
        """F4: a quest file validate.py reports an error against is not published."""
        self.repo.write(".quests/feat-0001-a.md", quest("feat-0001", extra="private: maybe\n"))
        self.repo.write(".quests/feat-0002-b.md", quest("feat-0002"))
        out = self.publish()
        self.assertEqual([i["title"][:9] for i in self.gh.issues.values()], ["feat-0002"])
        self.assertIn(".quests/feat-0001-a.md is not published: validate.py rejects it", out)

    def test_f5_dry_run_names_the_current_title(self):
        """F5: an edit, close or reopen line shows the issue's title as it is now."""
        self.repo.write(".quests/feat-0001-a.md", quest("feat-0001"))
        self.publish()
        self.gh.find("feat-0001")["title"] = "renamed by hand"
        self.assertIn("now titled 'renamed by hand'", self.plan())

    def test_f5_a_marker_naming_another_file_is_left_alone(self):
        """F5: a marker whose source names another file is reported and not acted on."""
        forged = self.gh.add_issue("forged", "x\n\n" + marker_of(
            "feat-0001", ".quests/elsewhere.md"), {"zen:published"})
        self.repo.write(".quests/feat-0001-a.md", quest("feat-0001"))
        out = self.publish()
        self.assertIn(f"#{forged['number']} carries the marker of feat-0001 but names "
                      ".quests/elsewhere.md", out)
        self.assertEqual(forged["title"], "forged")
        self.assertEqual(len(self.gh.issues), 1)

    def test_f6_the_digest_is_of_the_body_without_the_marker(self):
        """F6: digest is sha256 of the rendered body without its marker line, 12 hex."""
        self.repo.write(".quests/feat-0001-a.md", quest("feat-0001"))
        self.publish()
        body = self.gh.find("feat-0001")["body"]
        text, _, marker_line = body.rpartition("\n\n")
        import hashlib
        self.assertEqual(publish.last_marker(marker_line).group(4),
                         hashlib.sha256(text.encode("utf-8")).hexdigest()[:12])

    def test_f7_a_long_path_still_fits_the_limit(self):
        """F7: the marker's real length is reserved, so body plus marker fit."""
        path = ".quests/feat-0001-" + "a" * 180 + ".md"
        body = "\n\n".join(f"## Part {n}\n\n" + "x" * 3000 for n in range(40))
        self.repo.write(path, quest("feat-0001", body=body))
        self.publish()
        text = self.gh.find("feat-0001")["body"]
        self.assertLessEqual(len(text), publish.BODY_LIMIT)
        self.assertIsNotNone(publish.last_marker(text))

    def test_f9_non_json_from_gh_is_a_publish_error(self):
        """F9: output that is not JSON is reported, not a traceback."""
        with self.assertRaises(publish.PublishError):
            publish._json_pages("HTTP 502 Bad Gateway")


class ValidatorKeys(unittest.TestCase):
    """S-047, S-048, S-050: the validator's checks of the publishing keys, both copies."""

    def findings(self, module, extra):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs" / "agents").mkdir(parents=True)
            (root / "docs" / "spec").mkdir()
            (root / "docs" / "agents" / "zen.md").write_text(CONFIG.format(extra=extra),
                                                              encoding="utf-8")
            return module.zen_config_findings(root)

    def test_valid_keys_pass(self):
        for name, module in VALIDATORS.items():
            with self.subTest(copy=name):
                self.assertEqual(self.findings(module, ON), [])
                self.assertEqual(self.findings(module, "publish: none"), [])
                self.assertEqual(self.findings(module, f"publish_repo: {REPO}"), [])

    def test_bad_keys_fail(self):
        cases = {
            "publish: yes": "publish 'yes' is not one of",
            "publish: github": "publish: github needs publish_repo",
            "publish: github\npublish_repo: none": "publish: github needs publish_repo",
            "publish_repo: a/b/c": "publish_repo 'a/b/c' must be owner/name",
            "publish_repo: o/..": "must be owner/name",
            "Publish: github": "unknown key 'Publish'",
        }
        for name, module in VALIDATORS.items():
            for extra, expect in cases.items():
                with self.subTest(copy=name, extra=extra):
                    found = self.findings(module, extra)
                    self.assertTrue(any(expect in f for f in found), found)

    def test_publish_needs_a_local_tracker(self):
        for name, module in VALIDATORS.items():
            with self.subTest(copy=name):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    (root / "docs" / "agents").mkdir(parents=True)
                    (root / "docs" / "spec").mkdir()
                    (root / "docs" / "agents" / "zen.md").write_text(
                        CONFIG.format(extra=ON).replace("tracker: quests", "tracker: gitlab"),
                        encoding="utf-8")
                    found = module.zen_config_findings(root)
                self.assertTrue(any("mirrors the local tracker" in f for f in found), found)

    def test_private_field_is_checked(self):
        """S-057: a quest's private field is true or false."""
        for name, path in COPIES.items():
            with self.subTest(copy=name), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                (root / ".quests").mkdir()
                shutil.copy(path, root / ".quests" / "validate.py")
                (root / ".quests" / "feat-0001-a.md").write_text(
                    quest("feat-0001", extra="private: maybe\n"), encoding="utf-8")
                (root / ".quests" / "feat-0002-b.md").write_text(
                    quest("feat-0002", extra="private: true\n"), encoding="utf-8")
                proc = subprocess.run([sys.executable,
                                       str(root / ".quests" / "validate.py")],
                                      capture_output=True, text=True, cwd=root)
                self.assertIn("private 'maybe' is not one of", proc.stdout + proc.stderr)
                self.assertNotIn("feat-0002-b.md: private", proc.stdout + proc.stderr)


if __name__ == "__main__":
    unittest.main()
