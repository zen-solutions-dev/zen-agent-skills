"""Tests for .agents/skills/spec-author/scripts/spec_digest.py (feat-0083).

test-quality notes: each test writes a real spec file and calls main() with injected output, the
lowest faithful layer for a command-line script whose contract is its printed verdict and its exit
status. Oracles are the exact verdict word and exit code, never "did not crash".

The defect each group protects against:
  verdicts      - an approved spec edited after approval still reads as approved, so work is
                  verified or decomposed against text nobody agreed to
  normalisation - a checkout on another platform, or an editor's final newline, reads as an edit
                  and blocks verification for no change of meaning
  frontmatter   - recording the approval (setting status and the digest) changes the very digest
                  it is checked against
  queue         - the re-approval queue misses a waiting spec, or lists a sibling report
  exit status   - a spec that could not be read is reported as a refusal rather than an
                  unanswered question
  read only     - the script starts writing approval itself
  consumers     - a skill that gates on approval stops naming the script, so the check quietly
                  stops happening there
"""
import ast
import importlib.util
import io
import shutil
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS = REPO_ROOT / ".agents" / "skills"
SCRIPT = SKILLS / "spec-author" / "scripts" / "spec_digest.py"

_spec = importlib.util.spec_from_file_location("spec_digest", SCRIPT)
sd = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sd)

BODY = "# a contract\n\n### Scenario S-001: it works\n\n- **Given** x\n- **Then** y\n"


def _spec_text(status="approved", digest=None, body=BODY, extra=""):
    lines = ["---", "title: a contract", f"status: {status}"]
    if digest is not None:
        lines.append(f"approved_digest: {digest}")
    return "\n".join(lines) + "\n" + extra + "---\n" + body


class _Tmp(unittest.TestCase):
    def setUp(self):
        self.dir = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.dir, ignore_errors=True)

    def write(self, name, text, newline="\n"):
        path = self.dir / name
        path.write_bytes(text.replace("\n", newline).encode("utf-8"))
        return path

    def run_main(self, *argv):
        out = io.StringIO()
        code = sd.main(list(argv), out=out)
        return code, out.getvalue()

    def verdict(self, path):
        return sd.assess(path)[0]


class VerdictTests(_Tmp):
    def test_an_approved_spec_matching_its_digest_is_bound(self):
        good = sd.digest(BODY)
        path = self.write("a.md", _spec_text(digest=good))
        self.assertEqual("bound", self.verdict(path))
        self.assertEqual(0, self.run_main(str(path))[0])

    def test_an_approved_spec_edited_after_approval_is_changed_and_refused(self):
        approved = sd.digest(BODY)
        path = self.write("a.md", _spec_text(digest=approved, body=BODY + "- **And** z\n"))
        code, text = self.run_main(str(path))
        self.assertEqual("changed", self.verdict(path))
        self.assertEqual(1, code)
        self.assertIn("re-reads it and records the new digest", text)

    def test_an_approved_spec_with_no_digest_is_unbound_and_may_be_relied_on(self):
        path = self.write("a.md", _spec_text())
        code, text = self.run_main(str(path))
        self.assertEqual("unbound", self.verdict(path))
        self.assertEqual(0, code)
        self.assertIn("not tied to any text", text)

    def test_a_draft_is_not_approved_and_refused(self):
        path = self.write("a.md", _spec_text(status="draft"))
        self.assertEqual("not-approved", self.verdict(path))
        self.assertEqual(1, self.run_main(str(path))[0])

    def test_a_spec_with_no_frontmatter_is_not_approved(self):
        path = self.write("a.md", BODY)
        self.assertEqual("not-approved", self.verdict(path))

    def test_a_digest_of_the_wrong_shape_is_malformed_and_refused(self):
        for bad in ("abc", "sha256:XYZ", "md5:" + "0" * 32, "sha256:" + "0" * 63):
            with self.subTest(bad=bad):
                path = self.write("a.md", _spec_text(digest=bad))
                self.assertEqual("malformed", self.verdict(path))
                self.assertEqual(1, self.run_main(str(path))[0])

    def test_the_printed_line_is_exactly_what_binds_the_spec(self):
        path = self.write("a.md", _spec_text())
        _, text = self.run_main(str(path))
        printed = text.split("approved_digest: ")[1].split()[0]
        bound = self.write("b.md", _spec_text(digest=printed))
        self.assertEqual("bound", self.verdict(bound))


class NormalisationTests(_Tmp):
    def test_crlf_and_lf_checkouts_have_the_same_digest(self):
        lf = self.write("lf.md", _spec_text())
        crlf = self.write("crlf.md", _spec_text(), newline="\r\n")
        self.assertEqual(sd.assess(lf)[1], sd.assess(crlf)[1])

    def test_a_final_newline_does_not_change_the_digest(self):
        one = self.write("one.md", _spec_text(body=BODY))
        none = self.write("none.md", _spec_text(body=BODY.rstrip("\n")))
        many = self.write("many.md", _spec_text(body=BODY + "\n\n"))
        self.assertEqual(sd.assess(one)[1], sd.assess(none)[1])
        self.assertEqual(sd.assess(one)[1], sd.assess(many)[1])

    def test_a_byte_order_mark_does_not_change_the_digest(self):
        plain = self.write("plain.md", _spec_text())
        marked = self.write("marked.md", "﻿" + _spec_text())
        self.assertEqual(sd.assess(plain)[1], sd.assess(marked)[1])

    def test_a_one_word_edit_does_change_it(self):
        a = self.write("a.md", _spec_text(body=BODY))
        b = self.write("b.md", _spec_text(body=BODY.replace("works", "breaks")))
        self.assertNotEqual(sd.assess(a)[1], sd.assess(b)[1])


class FrontmatterTests(_Tmp):
    def test_recording_the_approval_does_not_change_the_digest(self):
        draft = self.write("draft.md", _spec_text(status="draft"))
        approved = self.write("ok.md", _spec_text(digest=sd.assess(draft)[1],
                                                  extra="owner: someone\n"))
        self.assertEqual(sd.assess(draft)[1], sd.assess(approved)[1])
        self.assertEqual("bound", self.verdict(approved))

    def test_a_quoted_value_is_read_without_its_quotes(self):
        path = self.write("a.md", _spec_text(digest=f'"{sd.digest(BODY)}"'))
        self.assertEqual("bound", self.verdict(path))


class QueueTests(_Tmp):
    def test_the_queue_lists_waiting_approved_specs_and_nothing_else(self):
        self.write("bound.md", _spec_text(digest=sd.digest(BODY)))
        self.write("unbound.md", _spec_text())
        self.write("changed.md", _spec_text(digest=sd.digest(BODY), body=BODY + "more\n"))
        self.write("draft.md", _spec_text(status="draft"))
        self.write("thing.conformance.md", "---\ntitle: a matrix\nspec: x.md\n---\nrows\n")
        code, text = self.run_main("--queue", str(self.dir))
        self.assertEqual(0, code)
        self.assertIn("unbound.md: unbound", text)
        self.assertIn("changed.md: changed", text)
        self.assertNotIn("bound.md: bound", text)
        self.assertNotIn("draft.md", text)
        self.assertNotIn("conformance", text)
        self.assertIn("2 approved spec(s) waiting", text)

    def test_a_file_it_cannot_read_is_named_and_exits_two(self):
        self.write("unbound.md", _spec_text())
        (self.dir / "broken.md").write_bytes(b"---\nstatus: approved\n---\n\xff\xfe not utf-8\n")
        code, text = self.run_main("--queue", str(self.dir))
        self.assertEqual(2, code)
        self.assertIn("broken.md: unreadable", text)
        self.assertIn("1 file(s) could not be read", text)

    def test_a_broken_symlink_is_reported_as_unreadable(self):
        try:
            (self.dir / "gone.md").symlink_to(self.dir / "missing-target.md")
        except OSError:
            self.skipTest("this platform does not allow creating a symlink here")
        code, text = self.run_main("--queue", str(self.dir))
        self.assertEqual(2, code)
        self.assertIn("gone.md: unreadable", text)

    def test_an_unreadable_directory_exits_two(self):
        self.assertEqual(2, self.run_main("--queue", str(self.dir / "absent"))[0])


class ExitStatusTests(_Tmp):
    def test_a_missing_file_exits_two_and_outranks_a_refusal(self):
        draft = self.write("draft.md", _spec_text(status="draft"))
        code, text = self.run_main(str(draft), str(self.dir / "absent.md"))
        self.assertEqual(2, code)
        self.assertIn("absent.md: unreadable", text)

    def test_no_arguments_is_a_usage_error(self):
        self.assertEqual(2, self.run_main()[0])


class ReadOnlyTests(unittest.TestCase):
    def test_the_script_writes_nothing(self):
        # `replace` is left out on purpose: the script calls `str.replace` to normalise line
        # endings, and a guard that fires on that gets loosened until it guards nothing. The
        # imports check below covers the modules that could rename or delete.
        tree = ast.parse(SCRIPT.read_text(encoding="utf-8"))
        writers = {"write_text", "write_bytes", "unlink", "rename", "rmdir", "mkdir", "touch"}
        calls = {n.func.attr for n in ast.walk(tree)
                 if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)}
        self.assertFalse(calls & writers)
        imported = {a.name.split(".")[0] for n in ast.walk(tree) if isinstance(n, ast.Import)
                    for a in n.names}
        self.assertFalse(imported & {"os", "shutil", "subprocess", "tempfile"})
        opens = [n for n in ast.walk(tree)
                 if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "open"]
        self.assertEqual([], opens)


class ConsumerTests(unittest.TestCase):
    """Every skill that gates on approval must name the script and link spec-author.

    The link to spec-author's SKILL.md is the install edge: without it, `--skills verifier-agent`
    would place a skill whose check names a script that was never installed.
    """

    CONSUMERS = ("verifier-agent", "new-task", "spec-plan-readiness", "test-author")

    def test_each_consumer_links_spec_author_and_names_the_script(self):
        for name in self.CONSUMERS:
            with self.subTest(skill=name):
                body = (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")
                self.assertIn("](../spec-author/SKILL.md)", body)
                self.assertIn("scripts/spec_digest.py", body)
                self.assertIn("`changed`", body)
                # A link to a sibling's script is not one of the three link classes the
                # Cursor and VS Code adapters rewrite, so it would dangle there (bug-0044).
                self.assertNotIn("](../spec-author/scripts/", body)

    def test_spec_author_documents_the_binding(self):
        body = (SKILLS / "spec-author" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("approved_digest", body)
        self.assertIn("](scripts/spec_digest.py)", body)

    def test_the_prose_definition_matches_the_script(self):
        """spec-author states the digest for trees that carry no script; it must be this one."""
        body = " ".join((SKILLS / "spec-author" / "SKILL.md").read_text(encoding="utf-8").split())
        for clause in ("SHA-256 of the spec's body after its frontmatter",
                       "byte-order mark dropped", "normalised to `\\n`",
                       "trailing newlines removed"):
            self.assertIn(clause, body)
        text = "\ufeff---\nstatus: approved\n---\r\nline\r\n\n\n"
        fields, rest = sd.split(text)
        self.assertEqual(sd.digest(rest), sd.digest("line"))


if __name__ == "__main__":
    unittest.main()
