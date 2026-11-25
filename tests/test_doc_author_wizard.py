"""Tests for .agents/skills/doc-author/scripts/wizard.py (feat-0105).

test-quality notes: each test drives a real Wizard through `run` with scripted standard input and a
temporary directory, the lowest faithful layer for a library whose contract is what a person sees
and what lands on disk. Oracles are exact file contents, exit codes and summary lines.

The defect each group protects against:
  env file     - a re-run duplicates a key, loses a value with a quote in it, or leaves a secrets
                 file readable by others
  prompts      - a re-run makes the person type an answer the env file already holds
  secrets      - a secret is echoed into the transcript
  irreversible - a declined confirmation still performs the action, or the summary hides what did
                 not happen
  once         - a step already done on an earlier run is done twice
  dry walk     - a dry walk opens a browser, writes a file, runs a command or records a step
  input        - input that ends mid-run hangs or crashes instead of stopping with a summary
  command      - a failed command is reported as success
"""
import importlib.util
import io
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parent.parent
WIZARD = REPO_ROOT / ".agents" / "skills" / "doc-author" / "scripts" / "wizard.py"


def load():
    spec = importlib.util.spec_from_file_location("zen_wizard", WIZARD)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


wizard = load()


class Case(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.env = self.tmp / ".env"
        self.state = self.tmp / "state.json"

    def make(self, answers="", secrets=(), dry_run=False):
        self.out = io.StringIO()
        secret_iter = iter(secrets)

        def read_secret(prompt):
            self.out.write(prompt)
            try:
                return next(secret_iter)
            except StopIteration:
                raise EOFError from None

        return wizard.Wizard("Title", "Purpose.", env_file=self.env, state_file=self.state,
                             dry_run=dry_run, stdin=io.StringIO(answers), stdout=self.out,
                             read_secret=read_secret)


class EnvFile(Case):
    def test_upsert_is_idempotent_and_round_trips_a_quote(self):
        for _ in range(2):
            w = self.make()
            self.assertEqual(w.run([("save", lambda w: w.write_env("NAME", "it's"))]), 0)
        self.assertEqual(self.env.read_text(encoding="utf-8"), "NAME='it'\\''s'\n")
        self.assertEqual(self.make().existing("NAME"), "it's")

    def test_other_keys_are_kept(self):
        self.env.write_text("OTHER=1\nNAME=old\n", encoding="utf-8")
        self.make().write_env("NAME", "new")
        self.assertEqual(self.env.read_text(encoding="utf-8"), "OTHER=1\nNAME='new'\n")

    @unittest.skipUnless(os.name == "posix", "file modes are POSIX only")
    def test_a_new_env_file_is_private(self):
        self.make().write_env("NAME", "v")
        self.assertEqual(self.env.stat().st_mode & 0o777, 0o600)

    @unittest.skipUnless(os.name == "posix", "file modes are POSIX only")
    def test_the_file_is_private_before_the_secret_reaches_it(self):
        modes = []
        real_write = Path.write_text

        def spy(path, *args, **kwargs):
            modes.append(path.stat().st_mode & 0o777)
            return real_write(path, *args, **kwargs)

        with mock.patch.object(Path, "write_text", spy):
            self.make().write_env("TOKEN", "secret")
        self.assertEqual(modes, [0o600])

    def test_a_value_with_any_line_break_is_refused(self):
        # Every separator str.splitlines splits on, since existing() reads the file back that way.
        for sep in ["\n", "\r", "\r\n", "\v", "\f", "\x1c", "\x1d", "\x1e", "\x85",
                    "\u2028", "\u2029"]:
            with self.subTest(sep=repr(sep)):
                self.make().write_env("FIRST", "ok")  # the second write is the injection
                w = self.make()
                code = w.run([("save", lambda w: w.write_env("NAME", f"a{sep}EVIL=1"))])
                self.assertEqual(code, 1)
                self.assertIn("holds a line break, so it was not saved", self.out.getvalue())
                self.assertNotIn("EVIL", self.out.getvalue())
                self.assertIsNone(self.make().existing("EVIL"))
                self.assertEqual(self.env.read_text(encoding="utf-8"), "FIRST='ok'\n")

    def test_an_empty_value_is_saved(self):
        self.make().write_env("EMPTY", "")
        self.assertEqual(self.env.read_text(encoding="utf-8"), "EMPTY=''\n")
        self.assertEqual(self.make().existing("EMPTY"), "")


class Prompts(Case):
    def test_enter_keeps_the_saved_answer(self):
        self.env.write_text("REGION='eu-west'\n", encoding="utf-8")
        got = []
        w = self.make(answers="\n")
        self.assertEqual(w.run([("ask", lambda w: got.append(w.ask("REGION", "Region")))]), 0)
        self.assertEqual(got, ["eu-west"])

    def test_an_empty_answer_with_nothing_saved_is_asked_again(self):
        got = []
        w = self.make(answers="\nus-east\n")
        w.run([("ask", lambda w: got.append(w.ask("REGION", "Region")))])
        self.assertEqual(got, ["us-east"])
        self.assertIn("An answer is needed.", self.out.getvalue())


class Secrets(Case):
    def test_a_secret_is_written_but_never_printed(self):
        w = self.make(secrets=["s3cr3t-value"])
        code = w.run([("token", lambda w: w.write_env("TOKEN", w.ask_secret("TOKEN", "Token")))])
        self.assertEqual(code, 0)
        self.assertNotIn("s3cr3t-value", self.out.getvalue())
        self.assertEqual(self.make().existing("TOKEN"), "s3cr3t-value")


class Irreversible(Case):
    def test_no_stops_the_run_without_acting(self):
        acted = []
        w = self.make(answers="n\n")
        code = w.run([("publish", lambda w: w.irreversible("publish", lambda: acted.append(1))),
                      ("after", lambda w: acted.append(2))])
        self.assertEqual((code, acted), (1, []))
        summary = self.out.getvalue().split("== Summary ==")[1]
        self.assertIn("stopped at stage 1 of 2: declined: publish", summary)
        self.assertIn("not done: publish", summary)
        self.assertIn("not done: after", summary)

    def test_yes_acts_and_is_listed_done(self):
        acted = []
        w = self.make(answers="y\n")
        code = w.run([("publish", lambda w: w.irreversible("publish", lambda: acted.append(1)))])
        self.assertEqual((code, acted), (0, [1]))
        self.assertIn("done: publish", self.out.getvalue())


class Once(Case):
    def test_a_recorded_step_is_skipped_on_the_next_run(self):
        acted = []
        stage = [("create", lambda w: w.once("bucket", "create the bucket", lambda: acted.append(1)))]
        self.assertEqual(self.make().run(stage), 0)
        self.assertEqual(self.make().run(stage), 0)
        self.assertEqual(acted, [1])
        self.assertIn("already done: create the bucket", self.out.getvalue())


class OnceState(Case):
    def test_valid_json_that_is_not_an_object_counts_as_nothing_done(self):
        self.state.write_text("[]\n", encoding="utf-8")
        acted = []
        w = self.make()
        code = w.run([("create", lambda w: w.once("k", "make it", lambda: acted.append(1)))])
        self.assertEqual((code, acted), (0, [1]))
        self.assertIn("is not readable; treating every step as not done", self.out.getvalue())


class DryWalk(Case):
    def test_nothing_is_opened_written_run_or_recorded(self):
        acted = []

        def stage(w):
            w.open_url("https://example.invalid/")
            w.write_env("KEY", w.ask("KEY", "Key"))
            w.once("k", "make it", lambda: acted.append("once"))
            w.irreversible("send it", lambda: acted.append("irreversible"))
            w.command([sys.executable, "-c", "raise SystemExit(3)"])

        w = self.make(answers="value\ny\n", dry_run=True)
        with mock.patch.object(wizard.webbrowser, "open") as browser:
            code = w.run([("everything", stage)])
        self.assertEqual(code, 0)
        browser.assert_not_called()
        self.assertEqual(acted, [])
        self.assertFalse(self.env.exists())
        self.assertFalse(self.state.exists())
        self.assertIn("all 1 stages walked (dry walk)", self.out.getvalue())


class Input(Case):
    def test_input_that_ends_stops_with_a_summary(self):
        w = self.make(answers="")
        code = w.run([("ask", lambda w: w.ask("KEY", "Key"))])
        self.assertEqual(code, 1)
        self.assertIn("stopped at stage 1 of 1: input ended", self.out.getvalue())


class Command(Case):
    def test_a_failing_command_stops_the_run(self):
        w = self.make()
        code = w.run([("run", lambda w: w.command([sys.executable, "-c", "raise SystemExit(3)"]))])
        self.assertEqual(code, 1)
        self.assertIn("exited 3", self.out.getvalue())

    def test_a_missing_executable_stops_the_run_with_a_summary(self):
        w = self.make()
        code = w.run([("run", lambda w: w.command(["zen-no-such-program-0105"]))])
        self.assertEqual(code, 1)
        self.assertIn("stopped at stage 1 of 1: zen-no-such-program-0105 could not be run",
                      self.out.getvalue())

    def test_a_secret_reaches_the_command_on_standard_input(self):
        out = self.tmp / "got.txt"
        script = f"import sys; open({str(out)!r}, 'w').write(sys.stdin.read())"
        self.assertEqual(self.make().command([sys.executable, "-c", script], secret_input="abc"), 0)
        self.assertEqual(out.read_text(), "abc")


if __name__ == "__main__":
    unittest.main()
