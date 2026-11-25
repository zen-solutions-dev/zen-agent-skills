"""The `changelog lines` gate in `scripts/run-checks.py` (feat-0103, retro R-204).

A task-log line in CHANGELOG.md over the limit warns; the lines over it when the check
landed are excepted by digest, so only a new or edited long line warns, and an exception
matching nothing is named for deletion. The gate never fails. Kept in a file of its own so
it does not collide with additions to tests/test_run_checks.py (retro R-203).
"""
from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("run_checks_changelog",
                                               REPO_ROOT / "scripts" / "run-checks.py")
rc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rc)

HEAD = "# Changelog\n\n## Releases\n\n" + "- a release line " + "x" * 400 + "\n\n## Task log\n\n"
SHORT = "- [x] (2026-11-25) Closed `feat-0001`: short.\n"
LONG = "- [x] (2026-11-25) Closed `feat-0002`: " + "y" * 300 + "\n"


class ChangelogLinesTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def check(self, text, exceptions=()):
        if text is not None:
            (self.root / "CHANGELOG.md").write_text(text, encoding="utf-8")
        ok, report = rc.check_changelog_lines(self.root, exceptions)
        self.assertTrue(ok, "this gate warns and never fails")
        return report, rc.coverage_line(report)

    def test_a_new_long_line_warns_on_the_line_a_passing_gate_shows(self):
        report, shown = self.check(HEAD + SHORT + LONG)
        self.assertIn("WARN  CHANGELOG.md:10: task-log line is 339 characters, over 330", report)
        self.assertEqual(shown, "Measured 2 task-log line(s) in CHANGELOG.md: WARN 1 new "
                                "line(s) over 330 characters, at line(s) 10; 0 excepted, "
                                "0 stale exception(s).")

    def test_an_excepted_long_line_is_silent_and_counted(self):
        key = rc._line_key(LONG.rstrip("\n"))
        report, shown = self.check(HEAD + LONG, {key})
        self.assertNotIn("WARN", report)
        self.assertIn("1 excepted, 0 stale", shown)

    def test_editing_an_excepted_line_makes_it_new_again(self):
        key = rc._line_key(LONG.rstrip("\n"))
        report, _ = self.check(HEAD + LONG.replace("y", "z", 1), {key})
        self.assertIn("WARN 1 new line(s)", report)
        self.assertIn("1 stale exception(s)", report)

    def test_a_stale_exception_is_named_for_deletion(self):
        report, _ = self.check(HEAD + SHORT, {"0123456789abcdef"})
        self.assertIn("exception '0123456789abcdef' matches no line over the limit; delete "
                      "it from CHANGELOG_LONG_LINE_EXCEPTIONS", report)

    def test_a_line_at_the_limit_is_silent_and_releases_prose_is_not_read(self):
        at = "- " + "a" * 328 + "\n"
        report, shown = self.check(HEAD + at)
        self.assertNotIn("WARN", report)
        self.assertIn("Measured 1 task-log line(s)", shown)

    def test_the_degenerate_inputs_say_what_was_not_measured(self):
        _, shown = self.check(None)
        self.assertEqual(shown, "CHANGELOG.md: absent, so 0 task-log lines were measured.")
        _, shown = self.check("")
        self.assertEqual(shown, "CHANGELOG.md: no `## Task log` heading, so 0 task-log "
                                "lines were measured.")
        _, shown = self.check("# Changelog\n\n## Task log\n")
        self.assertIn("Measured 0 task-log line(s)", shown)

    def test_the_real_changelog_is_measured_and_never_fails(self):
        # Deliberately not asserting the absence of a warning: that would turn the gate's
        # warning into a test-suite failure, which the decision (B4) ruled out.
        ok, report = rc.check_changelog_lines()
        self.assertTrue(ok)
        self.assertRegex(rc.coverage_line(report), r"^Measured [1-9]\d* task-log line")

    def test_the_gate_is_registered_and_runs_on_a_documentation_change(self):
        gate = next(g for g in rc.gates() if g.name == "changelog lines")
        self.assertIs(gate.check, rc.check_changelog_lines)
        self.assertIn("changelog lines", rc.DOCS_GATES)


if __name__ == "__main__":
    unittest.main()
