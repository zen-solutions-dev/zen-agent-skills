"""Tests for scripts/_change_scope.py: which changes are documentation only (chore-0098).

Derived from docs/spec/cloud-executable.md S-021 and S-022. Git is reached through an
injected runner, so each case states the exact `git diff --name-status` output it answers,
and one case runs real git in a scratch repository to prove a rename is reported as both
paths by git itself, not only by the stub.
"""
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts import _change_scope as cs

REPO_ROOT = Path(__file__).resolve().parent.parent


class _Done:
    def __init__(self, returncode, stdout=""):
        self.returncode = returncode
        self.stdout = stdout


def git_stub(diff="", uncommitted="", untracked="", bases=("origin/developer",)):
    """A runner answering the four git calls the module makes."""
    def runner(command, **_):
        args = command[1:]
        if args[:1] == ["rev-parse"]:
            return _Done(0 if args[-1] in bases else 1, "")
        if args[:1] == ["diff"]:
            return _Done(0, uncommitted if args[-1] == "HEAD" else diff)
        if args[:1] == ["ls-files"]:
            return _Done(0, untracked)
        raise AssertionError(f"unexpected git call {command}")
    return runner


CI = {"GITHUB_ACTIONS": "true", "GITHUB_BASE_REF": "developer"}


class ClassificationTests(unittest.TestCase):
    def test_markdown_outside_the_code_trees_is_documentation(self):
        for path in ("README.md", "docs/INSTALL.md", "docs/reviews/x.md", "GLOSSARY.md",
                     ".github/pull_request_template.md", "CHANGELOG.md", "ROADMAP.md"):
            with self.subTest(path=path):
                self.assertTrue(cs.is_documentation(path))

    def test_a_skill_a_spec_a_task_or_code_is_not(self):
        for path in (".agents/skills/grill/SKILL.md", ".agents/rules/core.md",
                     ".claude-plugin/plugin/skills/zen/SKILL.md", "docs/spec/install.md",
                     ".quests/feat-0001-x.md", "tests/README.md", "scripts/x.py",
                     ".github/workflows/checks.yml", "evals/x/case.md", "notes.txt"):
            with self.subTest(path=path):
                self.assertFalse(cs.is_documentation(path))

    def test_a_document_the_tests_read_is_not(self):
        for path in sorted(cs.TESTED_DOCUMENTS):
            with self.subTest(path=path):
                self.assertFalse(cs.is_documentation(path))

    def test_one_code_path_makes_the_whole_change_full(self):
        scope, reason = cs.classify(["README.md", "docs/INSTALL.md", "scripts/install.py"])
        self.assertEqual(cs.FULL, scope)
        self.assertIn("scripts/install.py", reason)

    def test_an_empty_change_is_full(self):
        self.assertEqual(cs.FULL, cs.classify([])[0])


class DecisionTests(unittest.TestCase):
    """S-021: the scope a run takes, and S-022's answer when the change is unknowable."""

    def test_a_pull_request_touching_only_documentation_is_docs(self):
        scope, reason = cs.decide(CI, git_stub(diff="M\tREADME.md\nA\tdocs/reviews/x.md\n"))
        self.assertEqual(cs.DOCS, scope)
        self.assertIn("against origin/developer", reason)

    def test_a_moved_file_counts_at_both_paths(self):
        # S-022: a script moved into docs/ is not a documentation change.
        diff = "R087\tscripts/old.py\tdocs/old.md\n"
        self.assertEqual(["scripts/old.py", "docs/old.md"], cs.parse_name_status(diff))
        self.assertEqual(cs.FULL, cs.decide(CI, git_stub(diff=diff))[0])

    def test_a_ci_run_with_no_pull_request_base_is_full(self):
        scope, reason = cs.decide({"GITHUB_ACTIONS": "true"}, git_stub())
        self.assertEqual(cs.FULL, scope)
        self.assertIn("no pull request base", reason)

    def test_a_failed_diff_is_full(self):
        def runner(command, **_):
            return _Done(128, "")
        self.assertEqual(cs.FULL, cs.decide(CI, runner)[0])

    def test_no_git_at_all_is_full(self):
        def runner(command, **_):
            raise FileNotFoundError("git")
        self.assertEqual(cs.FULL, cs.decide(CI, runner)[0])

    def test_locally_an_uncommitted_code_edit_makes_it_full(self):
        stub = git_stub(diff="M\tREADME.md\n", uncommitted="M\tscripts/install.py\n")
        self.assertEqual(cs.FULL, cs.decide({}, stub)[0])

    def test_locally_an_untracked_file_counts(self):
        stub = git_stub(diff="M\tREADME.md\n", untracked="tests/test_new.py\n")
        self.assertEqual(cs.FULL, cs.decide({}, stub)[0])

    def test_locally_with_no_base_branch_it_is_full(self):
        stub = git_stub(diff="M\tREADME.md\n", bases=())
        scope, reason = cs.decide({}, stub)
        self.assertEqual(cs.FULL, scope)
        self.assertIn("no base branch", reason)

    def test_the_override_forces_full(self):
        stub = git_stub(diff="M\tREADME.md\n")
        self.assertEqual(cs.FULL, cs.decide({**CI, "ZEN_CHECKS_SCOPE": "full"}, stub)[0])


@unittest.skipUnless(shutil.which("git"), "git is not installed")
class RealGitTests(unittest.TestCase):
    """The rename half of S-022 against git itself, not a stub of it."""

    def test_git_reports_a_rename_as_both_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            def git(*args):
                return subprocess.run(["git", "-C", tmp, *args], capture_output=True,
                                      text=True, check=True).stdout
            git("init", "-q")
            git("config", "user.email", "t@example.invalid")
            git("config", "user.name", "t")
            Path(tmp, "scripts").mkdir()
            Path(tmp, "scripts", "tool.py").write_text("print('a long enough body')\n" * 5)
            git("add", "-A")
            git("commit", "-qm", "base")
            Path(tmp, "docs").mkdir()
            git("mv", "scripts/tool.py", "docs/tool.md")
            git("commit", "-qm", "move")
            paths = cs.parse_name_status(git("diff", "--name-status", "-M", "HEAD~1...HEAD"))
            self.assertEqual({"scripts/tool.py", "docs/tool.md"}, set(paths))
            self.assertEqual(cs.FULL, cs.classify(paths)[0])


class TestedDocumentsGuardTests(unittest.TestCase):
    """Keeps TESTED_DOCUMENTS honest: every real document a test opens is never docs-only.

    A test that reads a document from the real repository can be broken by a change to
    that document alone. If that change were classed docs-only, the test suite would not
    run on it, and the break would surface on somebody else's pull request.
    """

    READ = re.compile(r"REPO_ROOT((?:\s*/\s*\"[^\"]+\")+)")

    def test_every_document_a_test_reads_from_the_repository_is_full(self):
        found = set()
        for test_file in sorted((REPO_ROOT / "tests").glob("test_*.py")):
            text = test_file.read_text(encoding="utf-8")
            for match in self.READ.finditer(text):
                parts = re.findall(r"\"([^\"]+)\"", match.group(1))
                path = "/".join(parts)
                if path.lower().endswith(".md"):
                    found.add((path, test_file.name))
        self.assertTrue(found, "the scan found no document reads at all; the pattern broke")
        for path, test_file in sorted(found):
            with self.subTest(path=path, read_by=test_file):
                self.assertFalse(cs.is_documentation(path),
                                 f"{test_file} reads {path} from the repository; add it to "
                                 f"TESTED_DOCUMENTS so a change to it runs the tests")


if __name__ == "__main__":
    unittest.main()
