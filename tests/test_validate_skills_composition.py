"""Tests for three cross-skill checks in `scripts/validate-skills.py` (feat-0103).

- **Composed-by claims** (retro `R-003`): a description saying "Composed by A, B and C"
  fails when a named composer does not exist or does not link the claimant's SKILL.md.
- **Guarded load-by-name** (maintainer decision R2-3): a shipped skill may name a draft in
  backticks inside "If `x` is installed, read and follow it; otherwise ...", which draws
  no install edge; a relative link to a draft fails; an unguarded "read and follow `x`"
  of a draft warns.
- **Draft expiry** (maintainer decision D1): a draft older than 90 days, by
  `metadata.drafted` or else its first git commit, that no file under
  `docs/reviews/*dogfood*` names, warns.

Kept in a file of their own rather than appended to `tests/test_validate_skills.py`, so a
parallel branch adding to either file does not collide in the other (retro R-203).
"""
from __future__ import annotations

import contextlib
import datetime
import importlib.util
import io
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location(
    "validate_skills_composition", REPO_ROOT / "scripts" / "validate-skills.py")
vs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(vs)

DESC = ("Use this skill when you need a thorough action whose description states both what "
        "it does and when to use it.")
DRAFT_META = "metadata:\n  status: draft\n"
TODAY = datetime.date(2026, 11, 25)


def skill(name, desc=DESC, body="body text\n", meta=""):
    return f"---\nname: {name}\ndescription: {desc}\n{meta}---\n{body}"


class Fixture(unittest.TestCase):
    """A throwaway repository with `.agents/skills/` and no git history."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._tmp.name)
        self.skills = self.repo / ".agents" / "skills"
        self.skills.mkdir(parents=True)

    def tearDown(self):
        self._tmp.cleanup()

    def write(self, name, text):
        d = self.skills / name
        d.mkdir(parents=True, exist_ok=True)
        (d / "SKILL.md").write_text(text, encoding="utf-8")

    def run_main(self, today=TODAY):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = vs.main(self.skills, today=today)
        return code, buf.getvalue()


class ComposedByTests(Fixture):
    def test_the_claims_are_parsed_from_a_folded_description(self):
        self.assertEqual(
            vs.composed_by_claims("A lens. Composed by test-author, tdd and fix-batch; "
                                  "distinct from review-quality."),
            ["test-author", "tdd", "fix-batch"])
        self.assertEqual(vs.composed_by_claims("Composed by `a`, `b`, and `c`."),
                         ["a", "b", "c"])
        self.assertEqual(vs.composed_by_claims("Composed by alpha."), ["alpha"])

    def test_a_description_without_the_claim_or_empty_claims_nothing(self):
        self.assertEqual(vs.composed_by_claims(""), [])
        self.assertEqual(vs.composed_by_claims(DESC), [])

    def test_a_claimed_composer_that_links_the_skill_passes(self):
        self.write("lens", skill("lens", DESC + " Composed by user."))
        self.write("user", skill("user", body="Read [lens](../lens/SKILL.md).\n"))
        code, out = self.run_main()
        self.assertEqual(code, 0, out)

    def test_a_claimed_composer_without_the_link_fails_and_names_both(self):
        self.write("lens", skill("lens", DESC + " Composed by user and other."))
        self.write("user", skill("user", body="Read [lens](../lens/SKILL.md).\n"))
        self.write("other", skill("other", body="Mentions `lens` in backticks only.\n"))
        code, out = self.run_main()
        self.assertEqual(code, 1, out)
        self.assertIn("ERROR lens: description says it is composed by 'other', but "
                      "other/SKILL.md has no relative link to ../lens/SKILL.md", out)
        self.assertNotIn("composed by 'user'", out)

    def test_a_link_inside_a_code_span_does_not_count(self):
        self.write("lens", skill("lens", DESC + " Composed by user."))
        self.write("user", skill("user", body="Example: `[lens](../lens/SKILL.md)`.\n"))
        code, out = self.run_main()
        self.assertEqual(code, 1, out)
        self.assertIn("composed by 'user'", out)

    def test_a_composer_that_is_not_a_skill_fails(self):
        self.write("lens", skill("lens", DESC + " Composed by ghost."))
        code, out = self.run_main()
        self.assertEqual(code, 1, out)
        self.assertIn("composed by 'ghost', and no skill has that name", out)

    def test_the_real_kit_passes(self):
        texts = {d.name: (d / "SKILL.md").read_text(encoding="utf-8")
                 for d in (REPO_ROOT / ".agents" / "skills").iterdir() if d.is_dir()}
        descs = {n: vs.parse_frontmatter(t)[0]["description"] for n, t in texts.items()}
        errors = []
        vs.check_composed_by(descs, texts, errors)
        self.assertEqual(errors, [])
        self.assertTrue(any(vs.composed_by_claims(d) for d in descs.values()),
                        "no real description makes the claim, so this test checks nothing")


GUARDED = ("If `drafty` is installed, read and follow it; otherwise continue without it.\n")


class GuardedLoadTests(Fixture):
    def setUp(self):
        super().setUp()
        self.write("drafty", skill("drafty", meta=DRAFT_META))
        (self.repo / "docs" / "reviews").mkdir(parents=True)
        # Named by a dogfood record, so the expiry check stays silent in these cases.
        (self.repo / "docs" / "reviews" / "x-dogfood.md").write_text("`drafty`\n",
                                                                       encoding="utf-8")

    def test_the_guarded_sentence_is_accepted_and_draws_no_install_edge(self):
        self.write("shipped", skill("shipped", body=GUARDED))
        code, out = self.run_main()
        self.assertEqual(code, 0, out)
        self.assertIn("0 error(s), 0 warning(s)", out)
        self.assertEqual(vs.sibling_edges(GUARDED), set())

    def test_a_relative_link_to_a_draft_fails(self):
        self.write("shipped", skill("shipped", body="Use [drafty](../drafty/SKILL.md).\n"))
        code, out = self.run_main()
        self.assertEqual(code, 1, out)
        self.assertIn("ERROR shipped/SKILL.md: links the draft 'drafty' as "
                      "../drafty/SKILL.md", out)

    def test_a_relative_link_beside_the_guard_still_fails(self):
        self.write("shipped", skill("shipped", body=GUARDED
                                    + "See [drafty](../drafty/SKILL.md).\n"))
        code, out = self.run_main()
        self.assertEqual(code, 1, out)

    def test_a_draft_linking_a_draft_is_not_this_rule(self):
        self.write("other", skill("other", meta=DRAFT_META,
                                  body="Use [drafty](../drafty/SKILL.md).\n"))
        (self.repo / "docs" / "reviews" / "x-dogfood.md").write_text(
            "`drafty` `other`\n", encoding="utf-8")
        code, out = self.run_main()
        self.assertEqual(code, 0, out)

    def test_an_unguarded_load_of_a_draft_warns(self):
        self.write("shipped", skill("shipped", body="Now read and follow `drafty`.\n"))
        code, out = self.run_main()
        self.assertEqual(code, 0, out)
        self.assertIn("WARN  shipped/SKILL.md: tells the agent to read and follow the draft "
                      "'drafty' with no guard", out)

    def test_an_unguarded_load_of_a_shipped_skill_is_silent(self):
        self.write("helper", skill("helper"))
        self.write("shipped", skill("shipped", body="Now read and follow `helper`.\n"))
        code, out = self.run_main()
        self.assertIn("0 error(s), 0 warning(s)", out)

    def test_words_between_it_and_otherwise_are_accepted(self):
        self.write("shipped", skill("shipped", body=(
            "If `drafty` is installed, read and follow it now; otherwise skip it.\n")))
        code, out = self.run_main()
        self.assertIn("0 error(s), 0 warning(s)", out)

    def test_a_guard_with_no_otherwise_clause_warns(self):
        self.write("shipped", skill("shipped", body=(
            "If `drafty` is installed, read and follow it. Then carry on.\n")))
        code, out = self.run_main()
        self.assertEqual(code, 0, out)
        self.assertIn("guards the draft 'drafty' with no '; otherwise' clause", out)

    def test_the_guard_line_alone_without_otherwise_warns(self):
        # Review F1/F2: the guard on its own, with no second load anywhere in the body.
        self.write("shipped", skill("shipped", body=(
            "If `drafty` is installed, read and follow it.\n")))
        code, out = self.run_main()
        self.assertEqual(code, 0, out)
        self.assertIn("guards the draft 'drafty' with no '; otherwise' clause", out)
        self.assertNotIn("with no guard;", out)

    def test_every_unguarded_phrasing_warns(self):
        # Review F3: case, and the kit's other idiom, "read `x` (now) and follow it".
        for body in ("Read and follow `drafty` first.\n",
                     "Read `drafty` now and follow it.\n",
                     "Then read `drafty` and follow it.\n",
                     "READ AND FOLLOW `drafty`.\n"):
            with self.subTest(body=body):
                self.write("shipped", skill("shipped", body=body))
                code, out = self.run_main()
                self.assertEqual(code, 0, out)
                self.assertIn("tells the agent to read and follow the draft 'drafty' with "
                              "no guard", out)

    def test_the_guarded_form_stays_exempt_in_every_case(self):
        for body in ("If `drafty` is installed, read and follow it; otherwise go on.\n",
                     "If `drafty` is installed, read and follow it now; otherwise skip.\n"):
            with self.subTest(body=body):
                self.write("shipped", skill("shipped", body=body))
                code, out = self.run_main()
                self.assertIn("0 error(s), 0 warning(s)", out)

    def test_a_guarded_load_satisfies_a_drafts_composed_by_claim(self):
        # Review F4: the link the claim used to demand is the one S-030 forbids.
        self.write("drafty", skill("drafty", DESC + " Composed by shipped.", meta=DRAFT_META))
        self.write("shipped", skill("shipped", body=GUARDED))
        code, out = self.run_main()
        self.assertEqual(code, 0, out)
        self.assertIn("0 error(s), 0 warning(s)", out)

    def test_a_guard_without_otherwise_does_not_satisfy_the_claim(self):
        self.write("drafty", skill("drafty", DESC + " Composed by shipped.", meta=DRAFT_META))
        self.write("shipped", skill("shipped",
                                    body="If `drafty` is installed, read and follow it.\n"))
        code, out = self.run_main()
        self.assertEqual(code, 1, out)
        self.assertIn("composed by 'shipped', but shipped/SKILL.md has no relative link", out)
        self.assertIn("also satisfies it", out)

    def test_a_guarded_load_does_not_satisfy_a_shipped_skills_claim(self):
        self.write("lens", skill("lens", DESC + " Composed by shipped."))
        self.write("shipped", skill("shipped", body=(
            "If `lens` is installed, read and follow it; otherwise go on.\n")))
        code, out = self.run_main()
        self.assertEqual(code, 1, out)
        self.assertNotIn("also satisfies it", out)

    def test_a_guard_missing_its_otherwise_clause_is_unguarded(self):
        self.write("shipped", skill("shipped", body=(
            "If `drafty` is installed, read and follow it.\nThen read and follow `drafty`.\n")))
        code, out = self.run_main()
        self.assertIn("with no guard", out)


class DraftExpiryTests(Fixture):
    def setUp(self):
        super().setUp()
        (self.repo / "docs" / "reviews").mkdir(parents=True)

    def test_an_old_draft_no_record_names_warns_with_its_age_and_source(self):
        self.write("drafty", skill("drafty", meta=DRAFT_META + "  drafted: 2026-08-01\n"))
        code, out = self.run_main()
        self.assertEqual(code, 0, out)
        self.assertIn("WARN  drafty/SKILL.md: a draft for 116 days (since 2026-08-01, from "
                      "metadata.drafted), over 90, and no file under docs/reviews/ with 'dogfood' in its "
                      "path names it", out)

    def test_exactly_ninety_days_is_not_over(self):
        self.write("drafty", skill("drafty", meta=DRAFT_META + "  drafted: 2026-08-27\n"))
        code, out = self.run_main()
        self.assertIn("0 warning(s)", out)

    def test_a_dogfood_record_naming_it_silences_the_warning(self):
        self.write("drafty", skill("drafty", meta=DRAFT_META + "  drafted: 2026-01-01\n"))
        d = self.repo / "docs" / "reviews" / "2026-11-24-dogfood"
        d.mkdir()
        (d / "ws.md").write_text("Ran `drafty` on its own work.\n", encoding="utf-8")
        code, out = self.run_main()
        self.assertIn("0 warning(s)", out)

    def test_the_name_as_a_whole_word_counts_as_naming_it(self):
        # AGENTS.md section 7: "names the skill, by its name or as <name>/SKILL.md".
        self.write("drafty", skill("drafty", meta=DRAFT_META + "  drafted: 2026-01-01\n"))
        for text in ("Ran drafty on real work.\n", "See drafty/SKILL.md.\n"):
            with self.subTest(text=text):
                (self.repo / "docs" / "reviews" / "dogfood.md").write_text(
                    text, encoding="utf-8")
                code, out = self.run_main()
                self.assertIn("0 warning(s)", out)

    def test_a_longer_hyphenated_name_does_not_count(self):
        self.write("drafty", skill("drafty", meta=DRAFT_META + "  drafted: 2026-01-01\n"))
        (self.repo / "docs" / "reviews" / "dogfood.md").write_text(
            "Ran drafty-two and undrafty.\n", encoding="utf-8")
        code, out = self.run_main()
        self.assertIn("a draft for", out)

    def test_a_record_outside_the_dogfood_glob_does_not_count(self):
        self.write("drafty", skill("drafty", meta=DRAFT_META + "  drafted: 2026-01-01\n"))
        (self.repo / "docs" / "reviews" / "retro.md").write_text("`drafty`\n",
                                                                   encoding="utf-8")
        code, out = self.run_main()
        self.assertIn("a draft for", out)

    def test_a_shipped_skill_never_expires(self):
        self.write("old", skill("old", meta="metadata:\n  drafted: 2020-01-01\n"))
        code, out = self.run_main()
        self.assertIn("0 warning(s)", out)

    def test_an_extension_restarts_the_ninety_days(self):
        self.write("drafty", skill("drafty", meta=DRAFT_META + "  drafted: 2026-01-01\n"
                                   + '  extended: "2026-10-01: waiting on a real run"\n'))
        code, out = self.run_main()
        self.assertIn("0 warning(s)", out)
        self.write("drafty", skill("drafty", meta=DRAFT_META + "  drafted: 2026-01-01\n"
                                   + '  extended: "2026-08-01: old extension"\n'))
        code, out = self.run_main()
        self.assertIn("(since 2026-08-01, from metadata.extended)", out)

    def test_a_recent_extension_silences_an_old_draft(self):
        # Review F1, the exact case.
        self.write("drafty", skill("drafty", meta=DRAFT_META + "  drafted: 2026-01-01\n"
                                   + '  extended: "2026-11-01: still in use"\n'))
        code, out = self.run_main()
        self.assertEqual(code, 0, out)
        self.assertIn("0 warning(s)", out)

    def test_quoted_and_unquoted_dates_read_the_same(self):
        for line in ("  drafted: 2026-08-01\n", '  drafted: "2026-08-01"\n',
                     "  drafted: '2026-08-01'\n"):
            with self.subTest(line=line):
                self.write("drafty", skill("drafty", meta=DRAFT_META + line))
                code, out = self.run_main()
                self.assertIn("(since 2026-08-01, from metadata.drafted)", out)

    def test_a_drafted_date_in_the_future_is_invalid(self):
        # Review F7: a future date would otherwise keep the warning quiet for years.
        self.write("drafty", skill("drafty", meta=DRAFT_META + "  drafted: 2027-06-01\n"))
        code, out = self.run_main()
        self.assertIn("metadata.drafted '2027-06-01' is not a YYYY-MM-DD date that is not "
                      "in the future", out)

    def test_a_shallow_clone_says_unknown_rather_than_dating_its_boundary(self):
        self.write("drafty", skill("drafty", meta=DRAFT_META))
        calls = []

        def fake(argv, **_kw):
            calls.append(argv)
            if "--is-shallow-repository" in argv:
                return subprocess.CompletedProcess(argv, 0, stdout="true\n", stderr="")
            return subprocess.CompletedProcess(argv, 0, stdout="2026-01-01\n", stderr="")
        with mock.patch.object(vs.subprocess, "run", side_effect=fake):
            code, out = self.run_main()
        self.assertIn("unknown (no metadata.drafted, and this is a shallow clone)", out)
        self.assertNotIn("2026-01-01", out)

    def test_a_record_nested_deeper_under_reviews_counts(self):
        # The path rule as AGENTS.md defines it: `dogfood` anywhere in the path below
        # docs/reviews/, no date required.
        self.write("drafty", skill("drafty", meta=DRAFT_META + "  drafted: 2026-01-01\n"))
        d = self.repo / "docs" / "reviews" / "round-2-dogfood" / "ws-a"
        d.mkdir(parents=True)
        (d / "notes.md").write_text("`drafty` ran here.\n", encoding="utf-8")
        code, out = self.run_main()
        self.assertIn("0 warning(s)", out)

    def test_an_extension_without_a_date_is_reported(self):
        self.write("drafty", skill("drafty", meta=DRAFT_META + '  extended: "soon"\n'))
        code, out = self.run_main()
        self.assertIn("metadata.extended 'soon' does not start with a YYYY-MM-DD date", out)

    def test_a_malformed_drafted_value_is_reported_as_unknown(self):
        self.write("drafty", skill("drafty", meta=DRAFT_META + "  drafted: last spring\n"))
        code, out = self.run_main()
        self.assertIn("drafted metadata.drafted 'last spring' is not a YYYY-MM-DD date that "
                      "is not in the future; the 90-day expiry cannot be checked", out)

    def test_without_drafted_and_without_git_the_date_is_unknown(self):
        self.write("drafty", skill("drafty", meta=DRAFT_META))
        with mock.patch.object(vs.subprocess, "run", side_effect=FileNotFoundError("git")):
            code, out = self.run_main()
        self.assertEqual(code, 0, out)
        self.assertIn("drafted unknown (no metadata.drafted, and git is unavailable)", out)

    def test_without_drafted_the_first_git_commit_dates_it(self):
        self.write("drafty", skill("drafty", meta=DRAFT_META))
        fake = subprocess.CompletedProcess([], 0, stdout="2026-11-01\n2026-03-02\n", stderr="")
        with mock.patch.object(vs.subprocess, "run", return_value=fake) as run:
            code, out = self.run_main()
        self.assertIn("a draft for 268 days (since 2026-03-02, from the first git commit "
                      "adding it)", out)
        self.assertIn("--diff-filter=A", run.call_args[0][0])

    def test_a_skills_directory_outside_the_agents_layout_skips_the_check(self):
        flat = self.repo / "flat"
        (flat / "drafty").mkdir(parents=True)
        (flat / "drafty" / "SKILL.md").write_text(
            skill("drafty", meta=DRAFT_META + "  drafted: 2020-01-01\n"), encoding="utf-8")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            vs.main(flat, today=TODAY)
        self.assertIn("0 warning(s)", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
