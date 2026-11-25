"""Tests for scripts/release.py, decision D5 ("add tagged releases").

Every test runs against a temporary directory through `--root`, with `--no-git` except the
one test that checks git's absence degrades gracefully, so no test reads or writes the real
repository and none runs a git command that writes. Standard library only, per the
conventions section of AGENTS.md.
"""
import contextlib
import importlib.util
import io
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("zen_release", REPO / "scripts" / "release.py")
release = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(release)

HEAD = "# Changelog\n\nIntro line.\n\n---\n\n## Releases\n\n"
TASK_LOG = ("## Task log\n\n"
            "- [x] (2026-11-24) Closed `feat-0095`: one line.\n\n"
            "- [x] (2026-11-23) Closed `chore-0097`: another line.\n")
WITH_UNRELEASED = (HEAD + "### Unreleased: the big overhaul\n\nWhat changed.\n\n"
                   "### v0.1.0 (2026-07-29)\n\nFirst release.\n\n" + TASK_LOG)
WITHOUT_UNRELEASED = HEAD + "### v0.1.0 (2026-07-29)\n\nFirst release.\n\n" + TASK_LOG
NO_RELEASED = HEAD + "### Unreleased\n\nSomething.\n\n" + TASK_LOG


class ReleaseCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def write(self, name, text):
        (self.root / name).write_bytes(text.encode("utf-8"))

    def run_release(self, *argv, git=False):
        args = ["--root", str(self.root), "--date", "2026-11-25", *argv]
        if not git:
            args.append("--no-git")
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = release.main(args)
        return code, out.getvalue(), err.getvalue()

    def version(self):
        return (self.root / "VERSION").read_text(encoding="utf-8")

    def changelog(self):
        return (self.root / "CHANGELOG.md").read_bytes().decode("utf-8")


class Bumping(ReleaseCase):
    def test_each_part_bumps_from_version(self):
        for part, expected in (("major", "2.0.0"), ("minor", "1.5.0"), ("patch", "1.4.4")):
            with self.subTest(part=part):
                self.write("VERSION", "1.4.3\n")
                self.write("CHANGELOG.md", WITH_UNRELEASED)
                code, out, _ = self.run_release("--bump", part)
                self.assertEqual(code, 0)
                self.assertEqual(self.version(), expected + "\n")
                self.assertIn(f"### v{expected} (2026-11-25): the big overhaul\n",
                              self.changelog())

    def test_explicit_version(self):
        self.write("VERSION", "0.1.0\n")
        self.write("CHANGELOG.md", WITH_UNRELEASED)
        code, out, _ = self.run_release("--version", "3.0.7")
        self.assertEqual(code, 0)
        self.assertEqual(self.version(), "3.0.7\n")
        self.assertIn("Release v3.0.7, dated 2026-11-25.", out)

    def test_lower_or_equal_version_is_refused_and_nothing_written(self):
        for given in ("0.9.9", "1.0.0"):
            with self.subTest(given=given):
                self.write("VERSION", "1.0.0\n")
                self.write("CHANGELOG.md", WITH_UNRELEASED)
                code, _, err = self.run_release("--version", given)
                self.assertEqual(code, 1)
                self.assertIn("is not greater than v1.0.0", err)
                self.assertEqual(self.version(), "1.0.0\n")
                self.assertEqual(self.changelog(), WITH_UNRELEASED)

    def test_a_version_the_changelog_already_records_is_refused(self):
        self.write("CHANGELOG.md", WITH_UNRELEASED)
        code, _, err = self.run_release("--version", "0.1.0")
        self.assertEqual(code, 1)
        self.assertIn("not greater than v0.1.0", err)
        self.assertFalse((self.root / "VERSION").exists())

    def test_absent_version_is_zero_and_said_so(self):
        self.write("CHANGELOG.md", NO_RELEASED)
        code, out, _ = self.run_release("--bump", "patch")
        self.assertEqual(code, 0)
        self.assertIn("VERSION is absent, so the current version is taken as 0.0.0", out)
        self.assertEqual(self.version(), "0.0.1\n")

    def test_absent_version_bumps_from_the_changelog_floor(self):
        self.write("CHANGELOG.md", WITH_UNRELEASED)
        code, out, _ = self.run_release("--bump", "minor")
        self.assertEqual(code, 0)
        self.assertIn("Bumping from v0.1.0, the changelog's", out)
        self.assertEqual(self.version(), "0.2.0\n")


class DryRun(ReleaseCase):
    def test_dry_run_writes_nothing(self):
        self.write("VERSION", "1.0.0\n")
        self.write("CHANGELOG.md", WITH_UNRELEASED)
        before = {p.name: p.read_bytes() for p in self.root.iterdir()}
        code, out, _ = self.run_release("--bump", "minor", "--dry-run")
        self.assertEqual(code, 0)
        after = {p.name: p.read_bytes() for p in self.root.iterdir()}
        self.assertEqual(before, after)
        self.assertIn("Dry run: nothing written", out)
        self.assertIn("VERSION: 1.0.0 -> 1.1.0", out)
        self.assertIn("+### v1.1.0 (2026-11-25): the big overhaul", out)

    def test_dry_run_with_absent_version_creates_no_file(self):
        self.write("CHANGELOG.md", WITH_UNRELEASED)
        self.run_release("--bump", "patch", "--dry-run")
        self.assertFalse((self.root / "VERSION").exists())


class Changelog(ReleaseCase):
    def test_unreleased_section_is_renamed_and_fresh_one_added(self):
        self.write("CHANGELOG.md", WITH_UNRELEASED)
        self.run_release("--version", "0.2.0")
        expected = (HEAD + "### Unreleased\n\n### v0.2.0 (2026-11-25): the big overhaul\n\n"
                    "What changed.\n\n### v0.1.0 (2026-07-29)\n\nFirst release.\n\n"
                    + TASK_LOG)
        self.assertEqual(self.changelog(), expected)

    def test_without_unreleased_an_empty_section_is_inserted_and_said(self):
        self.write("CHANGELOG.md", WITHOUT_UNRELEASED)
        code, out, _ = self.run_release("--version", "0.2.0")
        self.assertEqual(code, 0)
        self.assertIn("No Unreleased section was found", out)
        expected = (HEAD + "### Unreleased\n\n### v0.2.0 (2026-11-25)\n\n"
                    + release.PLACEHOLDER + "\n\n### v0.1.0 (2026-07-29)\n\nFirst release.\n\n"
                    + TASK_LOG)
        self.assertEqual(self.changelog(), expected)

    def test_an_empty_unreleased_body_gets_the_placeholder(self):
        self.write("CHANGELOG.md", HEAD + "### Unreleased\n\n" + TASK_LOG)
        code, out, _ = self.run_release("--version", "0.1.0")
        self.assertEqual(code, 0)
        self.assertIn("was empty", out)
        self.assertIn("### v0.1.0 (2026-11-25)\n\n" + release.PLACEHOLDER, self.changelog())

    def test_task_log_bytes_are_untouched(self):
        for text in (WITH_UNRELEASED, WITHOUT_UNRELEASED):
            with self.subTest(unreleased=text is WITH_UNRELEASED):
                self.write("CHANGELOG.md", text)
                self.run_release("--version", "5.0.0")
                after = (self.root / "CHANGELOG.md").read_bytes()
                tail = TASK_LOG.encode("utf-8")
                self.assertTrue(after.endswith(tail))
                self.assertEqual(after.index(b"## Task log"), len(after) - len(tail))
                self.assertTrue(after.startswith(HEAD.encode("utf-8")))

    def test_crlf_line_endings_are_preserved(self):
        crlf = WITH_UNRELEASED.replace("\n", "\r\n")
        self.write("CHANGELOG.md", crlf)
        self.run_release("--version", "0.2.0")
        after = (self.root / "CHANGELOG.md").read_bytes()
        self.assertNotIn(b"\n", after.replace(b"\r\n", b""))
        self.assertTrue(after.endswith(TASK_LOG.replace("\n", "\r\n").encode("utf-8")))

    def test_empty_changelog_is_refused(self):
        self.write("CHANGELOG.md", "")
        code, _, err = self.run_release("--bump", "patch")
        self.assertEqual(code, 1)
        self.assertIn("no '## Releases' heading", err)
        self.assertEqual(self.changelog(), "")
        self.assertFalse((self.root / "VERSION").exists())

    def test_missing_changelog_cannot_run(self):
        self.write("VERSION", "1.0.0\n")
        code, _, err = self.run_release("--bump", "patch")
        self.assertEqual(code, 2)
        self.assertIn("CHANGELOG.md: could not be read", err)
        self.assertEqual(self.version(), "1.0.0\n")

    def test_non_utf8_changelog_cannot_run(self):
        (self.root / "CHANGELOG.md").write_bytes(b"## Releases\n\xff\n")
        code, _, err = self.run_release("--bump", "patch")
        self.assertEqual(code, 2)
        self.assertIn("not valid UTF-8", err)


class VersionFile(ReleaseCase):
    def test_malformed_version_is_refused(self):
        for bad in ("1.2\n", "v1.2.3\n", "1.2.3-rc1\n", "01.2.3\n"):
            with self.subTest(bad=bad):
                self.write("VERSION", bad)
                self.write("CHANGELOG.md", WITH_UNRELEASED)
                code, _, err = self.run_release("--bump", "patch")
                self.assertEqual(code, 1)
                self.assertIn("is not a semantic version", err)
                self.assertEqual(self.changelog(), WITH_UNRELEASED)

    def test_empty_version_file_is_refused_by_name(self):
        self.write("VERSION", "")
        self.write("CHANGELOG.md", WITH_UNRELEASED)
        code, _, err = self.run_release("--bump", "patch")
        self.assertEqual(code, 1)
        self.assertIn("'(empty)' is not a semantic version", err)

    def test_malformed_explicit_version_and_date_are_refused(self):
        self.write("CHANGELOG.md", WITH_UNRELEASED)
        code, _, err = self.run_release("--version", "2.0")
        self.assertEqual(code, 1)
        args = ["--root", str(self.root), "--no-git", "--bump", "patch", "--date", "25/11/2026"]
        with contextlib.redirect_stdout(io.StringIO()), \
                contextlib.redirect_stderr(io.StringIO()) as err:
            self.assertEqual(release.main(args), 1)
        self.assertIn("is not a date", err.getvalue())


class Output(ReleaseCase):
    def test_prints_tag_and_push_and_says_they_were_not_run(self):
        self.write("CHANGELOG.md", WITH_UNRELEASED)
        code, out, _ = self.run_release("--version", "0.2.0")
        self.assertEqual(code, 0)
        self.assertIn('git tag -a v0.2.0 -m "Zen Agent Skills v0.2.0"', out)
        self.assertIn("git push origin v0.2.0", out)
        self.assertIn("Tagging is your step", out)
        self.assertIn("did not tag, push, or commit", out)

    def test_git_unavailable_degrades_to_a_note(self):
        # The temp directory is not a repository: git either is absent or fails there.
        self.write("CHANGELOG.md", WITH_UNRELEASED)
        code, out, _ = self.run_release("--version", "0.2.0", "--dry-run", git=True)
        self.assertEqual(code, 0)
        self.assertIn("git could not be read here", out)

    def test_an_existing_tag_is_refused_and_a_dirty_tree_warned(self):
        # git is a system boundary, so its two reads are replaced, never written to.
        self.write("CHANGELOG.md", WITH_UNRELEASED)
        answers = {"tag": "v0.2.0\n", "status": ""}
        with mock.patch.object(release, "git_read", lambda root, cmd, *a: answers[cmd]):
            code, _, err = self.run_release("--version", "0.2.0", git=True)
            self.assertEqual(code, 1)
            self.assertIn("already has a tag v0.2.0", err)
            answers.update(tag="", status=" M CHANGELOG.md\n")
            code, out, _ = self.run_release("--version", "0.2.0", "--dry-run", git=True)
            self.assertEqual(code, 0)
            self.assertIn("uncommitted changes", out)


class Check(ReleaseCase):
    def test_check_passes_when_the_section_exists(self):
        self.write("VERSION", "0.1.0\n")
        self.write("CHANGELOG.md", WITH_UNRELEASED)
        code, out, _ = self.run_release("--check")
        self.assertEqual(code, 0)
        self.assertIn("has a section for v0.1.0", out)

    def test_check_refuses_a_version_without_a_section(self):
        self.write("VERSION", "0.3.0\n")
        self.write("CHANGELOG.md", WITH_UNRELEASED)
        code, _, err = self.run_release("--check")
        self.assertEqual(code, 1)
        self.assertIn("no '### v0.3.0' section", err)

    def test_check_with_absent_version_says_so(self):
        self.write("CHANGELOG.md", WITH_UNRELEASED)
        code, out, _ = self.run_release("--check")
        self.assertEqual(code, 0)
        self.assertIn("VERSION is absent", out)

    def test_after_a_release_check_passes(self):
        self.write("CHANGELOG.md", WITHOUT_UNRELEASED)
        self.run_release("--bump", "minor")
        code, out, _ = self.run_release("--check")
        self.assertEqual(code, 0, out)


if __name__ == "__main__":
    unittest.main()
