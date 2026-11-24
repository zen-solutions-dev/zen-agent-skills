"""Tests for scripts/scan-secrets.py, the `secret scan` gate (chore-0098).

Every credential below is assembled at runtime from parts, so this file never contains a
match for the patterns it tests and the gate stays clean over its own test.
"""
import importlib.util
import io
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location(
    "scan_secrets", REPO_ROOT / "scripts" / "scan-secrets.py")
ss = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ss)

SAMPLES = {
    "private key": "-----BEGIN RSA " + "PRIVATE KEY-----",
    "AWS access key id": "AK" + "IA" + "Q" * 16,
    "GitHub token": "gh" + "p_" + "a1" * 18,
    "GitHub fine-grained token": "github" + "_pat_" + "A" * 60,
    "Anthropic API key": "sk-" + "ant-" + "x" * 30,
    "OpenAI API key": "sk-" + "proj-" + "A" * 40,
    "Slack token": "xo" + "xb-" + "1234567890-abc",
    "Google API key": "AI" + "za" + "B" * 35,
    "Stripe live key": "sk" + "_live_" + "C" * 24,
}


def no_git(command, **_):
    raise FileNotFoundError("git")


class PatternTests(unittest.TestCase):
    def test_every_pattern_has_a_sample_that_it_finds(self):
        self.assertEqual({kind for kind, _ in ss.PATTERNS}, set(SAMPLES))
        for kind, sample in SAMPLES.items():
            with self.subTest(kind=kind):
                self.assertEqual([(1, kind)], ss.scan_text(f"token = {sample}\n"))

    def test_ordinary_prose_and_code_are_clean(self):
        text = ("The key is to ask: what does sk-ant mean here?\n"
                "AKIA is a prefix, and ghp_ alone is not a token.\n"
                "def ask_for_key(api_key): return api_key\n")
        self.assertEqual([], ss.scan_text(text))

    def test_an_allowed_line_is_skipped(self):
        line = f"example = {SAMPLES['GitHub token']}  # {ss.ALLOW_MARKER}\n"
        self.assertEqual([], ss.scan_text(line))


class ScanTests(unittest.TestCase):
    def test_a_planted_token_fails_the_gate_and_is_not_echoed(self):
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "README.md").write_text(
                f"# x\n\nexport TOKEN={SAMPLES['Anthropic API key']}\n", encoding="utf-8")
            buf = io.StringIO()
            code = ss.main(root=Path(tmp), runner=no_git, out=buf)
            self.assertEqual(1, code)
            self.assertIn("README.md:3: looks like a Anthropic API key", buf.getvalue())
            self.assertNotIn(SAMPLES["Anthropic API key"], buf.getvalue())

    def test_a_clean_tree_passes_and_says_what_it_scanned(self):
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "a.md").write_text("nothing here\n", encoding="utf-8")
            Path(tmp, "b.bin").write_bytes(b"\0\1\2")
            buf = io.StringIO()
            self.assertEqual(0, ss.main(root=Path(tmp), runner=no_git, out=buf))
            self.assertIn("Scanned 1 file(s)", buf.getvalue())
            self.assertIn("skipped 1 binary or oversized; 0 finding(s)", buf.getvalue())

    def test_the_tree_walk_skips_the_git_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, ".git").mkdir()
            Path(tmp, ".git", "config").write_text(SAMPLES["GitHub token"], encoding="utf-8")
            self.assertEqual([], ss.scan(Path(tmp), no_git)[0])

    def test_this_repository_is_clean(self):
        findings, scanned, _ = ss.scan()
        self.assertGreater(scanned, 0)
        self.assertEqual([], findings)


if __name__ == "__main__":
    unittest.main()
