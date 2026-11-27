"""The Codex target of `scripts/build-adapters.py` and its generated sidecar (E7, feat-0103).

`--target codex` places each skill under `<out>/.agents/skills/<name>/`, where Codex reads
skills, with its SKILL.md verbatim and an `agents/openai.yaml` derived from the SKILL.md,
never written by hand. In a file of its own so it merges apart from additions to
tests/test_build_adapters.py (retro R-203).
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("build_adapters_codex",
                                               REPO_ROOT / "scripts" / "build-adapters.py")
ba = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ba)


def run(*argv):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = ba.main(list(argv))
    return code, buf.getvalue()


class SidecarTextTests(unittest.TestCase):
    def test_a_model_invoked_skill_carries_no_policy(self):
        self.assertEqual(
            ba.codex_sidecar("alpha", "Does a thing. Use it when asked.", False),
            "# generated from .agents/skills/alpha/SKILL.md by build-adapters.py. Do not "
            "edit here.\ninterface:\n  display_name: \"alpha\"\n"
            "  short_description: \"Does a thing.\"\n")

    def test_a_user_invoked_skill_turns_implicit_invocation_off(self):
        text = ba.codex_sidecar("alpha", "Does a thing.", True)
        self.assertTrue(text.endswith("policy:\n  allow_implicit_invocation: false\n"))

    def test_hostile_characters_are_escaped_into_one_double_quoted_scalar(self):
        desc = 'Reads "quoted": a #hash, a back\\slash, and café über all.'
        line = ba.codex_sidecar("alpha", desc, False).splitlines()[3]
        self.assertEqual(line, '  short_description: "Reads \\"quoted\\": a #hash, a '
                               'back\\\\slash, and café über all."')

    def test_a_long_first_sentence_is_cut_at_a_word_and_marked(self):
        short = ba.short_description("word " * 60 + "end.")
        self.assertLessEqual(len(short), ba.CODEX_SHORT_MAX)
        self.assertTrue(short.endswith("word..."))

    def test_an_empty_description_gives_an_empty_short_description(self):
        # The degenerate input. validate-skills.py fails a skill with no description,
        # so this cannot ship; the sidecar still parses rather than crashing the run.
        self.assertIn('  short_description: ""\n', ba.codex_sidecar("alpha", "", False))


class CodexTargetTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.out = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_every_shipped_skill_is_placed_with_a_sidecar_derived_from_its_skill_md(self):
        code, out = run("--target", "codex", "--out", str(self.out))
        self.assertEqual(code, 0, out)
        shipped = [d for d in ba.discover_skills()
                   if not ba.is_draft_text((d / "SKILL.md").read_text(encoding="utf-8"))]
        self.assertTrue(shipped)
        for d in shipped:
            with self.subTest(skill=d.name):
                placed = self.out / ".agents" / "skills" / d.name
                source = (d / "SKILL.md").read_text(encoding="utf-8")
                self.assertEqual((placed / "SKILL.md").read_text(encoding="utf-8"), source)
                fm, _ = ba.split_frontmatter(source)
                self.assertEqual(
                    (placed / "agents" / "openai.yaml").read_text(encoding="utf-8"),
                    ba.codex_sidecar(d.name, fm.get("description", ""),
                                     ba.is_user_invoked_text(source)))
        # The rules module lands where a placed skill's ../../rules/ links reach.
        self.assertTrue((self.out / ".agents" / "rules" / "core.md").is_file())

    def test_a_second_run_is_byte_identical(self):
        run("--target", "codex", "--out", str(self.out))
        first = {p: p.read_bytes() for p in self.out.rglob("*") if p.is_file()}
        run("--target", "codex", "--out", str(self.out))
        second = {p: p.read_bytes() for p in self.out.rglob("*") if p.is_file()}
        self.assertEqual(first, second)

    def test_drafts_are_withheld_unless_asked_for(self):
        run("--target", "codex", "--out", str(self.out))
        self.assertFalse((self.out / ".agents" / "skills" / "teach").exists())
        run("--target", "codex", "--out", str(self.out), "--include-drafts")
        sidecar = self.out / ".agents" / "skills" / "teach" / "agents" / "openai.yaml"
        self.assertIn("allow_implicit_invocation: false", sidecar.read_text(encoding="utf-8"))

    def test_a_dry_run_writes_nothing(self):
        code, out = run("--target", "codex", "--out", str(self.out), "--dry-run")
        self.assertEqual(code, 0, out)
        self.assertEqual(list(self.out.iterdir()), [])

    def test_the_kit_itself_as_the_output_gets_no_sidecar_in_its_sources(self):
        code, out = run("--target", "codex", "--out", str(REPO_ROOT), "--dry-run")
        self.assertEqual(code, 0, out)
        self.assertFalse(list((REPO_ROOT / ".agents" / "skills").glob("*/agents/openai.yaml")))
        self.assertIn("plus 0 shared asset file(s)", out)

    def test_emitting_a_skill_onto_its_own_source_writes_nothing(self):
        # Codex reads the kit's own `.agents/skills/` directly; a sidecar written there
        # would be a generated file among the sources.
        src = self.out / ".agents" / "skills" / "alpha"
        src.mkdir(parents=True)
        (src / "SKILL.md").write_text("---\nname: alpha\ndescription: d.\n---\nb\n",
                                      encoding="utf-8")
        dest = ba.emit_codex(src, "alpha", "d.", "b\n", self.out, False)
        self.assertEqual(dest, src / "SKILL.md")
        self.assertEqual(sorted(p.name for p in src.iterdir()), ["SKILL.md"])

if __name__ == "__main__":
    unittest.main()
