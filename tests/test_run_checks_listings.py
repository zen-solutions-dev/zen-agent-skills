"""The `skill listings` gate in `scripts/run-checks.py` (feat-0103, decision E9).

The `zen` router and docs/CATALOG.md each name every skill in the kit; a draft is named too
or excepted by name with a reason, and an exception that is no longer needed fails. In a
file of its own so additions here and to tests/test_run_checks.py merge apart (R-203).
"""
from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("run_checks_listings",
                                               REPO_ROOT / "scripts" / "run-checks.py")
rc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rc)

SHIPPED = "---\nname: {0}\ndescription: d\n---\nbody\n"
DRAFT = "---\nname: {0}\ndescription: d\nmetadata:\n  status: draft\n---\nbody\n"


class SkillListingsTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.skill("zen", SHIPPED, "Pick `alpha` or [beta](../beta/SKILL.md).\n")
        self.skill("alpha", SHIPPED)
        self.skill("beta", SHIPPED)
        (self.root / "docs").mkdir()
        self.catalog("`zen`, `alpha` and [beta](../.agents/skills/beta/SKILL.md).\n")

    def tearDown(self):
        self._tmp.cleanup()

    def skill(self, name, shape, body=""):
        d = self.root / ".agents" / "skills" / name
        d.mkdir(parents=True, exist_ok=True)
        (d / "SKILL.md").write_text(shape.format(name) + body, encoding="utf-8")

    def catalog(self, text):
        (self.root / "docs" / "CATALOG.md").write_text(text, encoding="utf-8")

    def check(self, exceptions=None):
        return rc.check_skill_listings(self.root, exceptions or {})

    def test_every_skill_named_in_both_passes_and_zen_need_not_name_itself(self):
        ok, report = self.check()
        self.assertTrue(ok, report)
        self.assertEqual(rc.coverage_line(report), "Checked 2 of 2 listing(s) against 3 "
                                                   "skill(s): 0 finding(s) failing.")

    def test_a_shipped_skill_missing_from_one_listing_fails_and_is_named(self):
        self.skill("gamma", SHIPPED)
        self.catalog("`zen`, `alpha`, `beta`, `gamma`\n")
        ok, report = self.check()
        self.assertFalse(ok)
        self.assertIn(".agents/skills/zen/SKILL.md: does not name the shipped skill 'gamma'",
                      report)
        self.assertNotIn("docs/CATALOG.md: does not name", report)

    def test_a_bare_word_does_not_count_as_naming(self):
        self.catalog("`zen`, `beta`, and an alpha release.\n")
        ok, report = self.check()
        self.assertFalse(ok)
        self.assertIn("docs/CATALOG.md: does not name the shipped skill 'alpha'", report)

    def test_an_unnamed_draft_fails_unless_excepted_with_a_reason(self):
        self.skill("drafty", DRAFT)
        ok, report = self.check()
        self.assertFalse(ok)
        self.assertIn("does not name the draft 'drafty'; add it, as `drafty`, or except",
                      report)
        ok, report = self.check({"drafty": "experimental, not yet routed"})
        self.assertTrue(ok, report)
        self.assertIn("'drafty' excepted: experimental, not yet routed", report)

    def test_an_exception_for_a_shipped_skill_does_not_excuse_it(self):
        self.skill("gamma", SHIPPED)
        ok, report = self.check({"gamma": "no"})
        self.assertFalse(ok)
        self.assertIn("does not name the shipped skill 'gamma'", report)

    def test_a_stale_exception_fails(self):
        ok, report = self.check({"alpha": "old reason"})
        self.assertFalse(ok)
        self.assertIn("names 'alpha', so its exception in UNLISTED_DRAFT_EXCEPTIONS is stale",
                      report)
        ok, report = self.check({"ghost": "gone"})
        self.assertFalse(ok)
        self.assertIn("exception 'ghost' names no skill in the kit", report)

    def test_the_degenerate_inputs(self):
        (self.root / "docs" / "CATALOG.md").unlink()
        ok, report = self.check()
        self.assertFalse(ok)
        self.assertIn("docs/CATALOG.md: absent, so no skill could be found in it.", report)
        self.assertIn("Checked 1 of 2 listing(s)", report)
        empty = Path(self._tmp.name) / "empty"
        empty.mkdir()
        ok, report = rc.check_skill_listings(empty, {})
        self.assertFalse(ok)
        self.assertIn("against 0 skill(s)", report)

    def test_the_real_kit_passes_and_the_gate_runs_on_documentation_changes(self):
        ok, report = rc.check_skill_listings()
        self.assertTrue(ok, report)
        gate = next(g for g in rc.gates() if g.name == "skill listings")
        self.assertIs(gate.check, rc.check_skill_listings)
        self.assertIn("skill listings", rc.DOCS_GATES)


if __name__ == "__main__":
    unittest.main()
