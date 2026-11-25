"""Acceptance tests for the zen-config check in .quests/validate.py (feat-0091).

Derived from docs/spec/zen-config.md; each test names the scenario it covers. The
scenarios about what a skill does in a conversation (the configure step and the
readers) are audited in that spec's conformance matrix rather than here.

Both copies of the validator are driven, for the reason test_quests_validate.py gives:
the copy `init-worktracking` installs is the one adopters run, and a rule that holds in
one copy only is the failure `bug-0026` found. The optional task `mode` field, added by
the same task, is tested here too.

Standard library only, per the conventions section of AGENTS.md.
"""
import contextlib
import importlib.util
import io
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
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


MODULES = {name: _load(f"zen_config_validate_{name}", path) for name, path in COPIES.items()}

TASK = """---
id: feat-0001
title: A task used only by this test
type: feat
status: open
priority: P1
parent: "a goal"
depends_on: []
{mode}touched_files:
  - README.md
created: 2026-11-24
---

## Problem

Body content is not what this test exercises.
"""

GOOD = """# Agent skills setup

Prose for people sits outside the block and is never parsed.

```text
tracker: not-a-tracker
```

```zen-config
# comments and blank lines are ignored

config_version: 1
tracker: github
role.ready-agent: ready for agent
role.blocked: blocked
glossary: GLOSSARY.md
adr_dir: none
spec_dir: docs/spec
standards: AGENTS.md, docs/style.md
acceptance: python -m pytest
base_branch: main
integration_prefix: integrate/
merge_policy: a person merges into main
session_logs: ~/.claude/projects
memory: none
default_mode: hitl
```
"""


class Fixture(unittest.TestCase):
    """A throwaway repository root, with both validator copies pointed at it."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        (self.root / ".quests").mkdir()
        (self.root / "docs" / "spec").mkdir(parents=True)
        (self.root / "docs" / "agents").mkdir()
        for name in ("README.md", "GLOSSARY.md", "AGENTS.md", "docs/style.md"):
            (self.root / name).write_text("fixture\n", encoding="utf-8")
        self._saved = {}
        for name, module in MODULES.items():
            self._saved[name] = (module.TASKS_DIR, module.REPO_ROOT)
            module.TASKS_DIR = self.root / ".quests"
            module.REPO_ROOT = self.root

    def tearDown(self):
        for name, module in MODULES.items():
            module.TASKS_DIR, module.REPO_ROOT = self._saved[name]
        self._tmp.cleanup()

    def write_config(self, text):
        (self.root / "docs" / "agents" / "zen.md").write_text(text, encoding="utf-8")

    def findings(self, module):
        return module.zen_config_findings(self.root)

    def run_main(self, module):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = module.main([])
        return code, buf.getvalue()

    def each(self):
        for name, module in MODULES.items():
            with self.subTest(copy=name):
                yield module


class ZenConfigTests(Fixture):

    def assert_one_finding(self, text, *fragments):
        self.write_config(text)
        for module in self.each():
            found = self.findings(module)
            self.assertEqual(len(found), 1, found)
            for fragment in fragments:
                self.assertIn(fragment, found[0])
            code, out = self.run_main(module)
            self.assertEqual(code, 1, out)
            self.assertIn("ERROR docs/agents/zen.md", out)

    def test_s001_a_well_formed_configuration_passes(self):
        self.write_config(GOOD)
        for module in self.each():
            self.assertEqual(self.findings(module), [])
            code, out = self.run_main(module)
            self.assertEqual(code, 0, out)

    def test_s002_no_file_is_not_an_error(self):
        for module in self.each():
            self.assertEqual(self.findings(module), [])
            code, out = self.run_main(module)
            self.assertEqual(code, 0, out)
            self.assertNotIn("zen", out)

    def test_s003_an_unknown_key_fails(self):
        self.assert_one_finding(GOOD.replace("memory: none", "memory: none\ncolour: blue"),
                                "unknown key", "colour")

    def test_s003_an_unknown_role_fails(self):
        self.assert_one_finding(GOOD.replace("role.blocked", "role.waiting"),
                                "unknown key", "role.waiting")

    def test_s004_a_missing_path_fails(self):
        self.assert_one_finding(GOOD.replace("glossary: GLOSSARY.md", "glossary: TERMS.md"),
                                "glossary", "TERMS.md", "does not exist")

    def test_s004_a_missing_standards_entry_fails(self):
        self.assert_one_finding(GOOD.replace("docs/style.md", "docs/gone.md"),
                                "standards", "docs/gone.md")

    def test_s004_a_directory_where_a_file_is_needed_fails(self):
        self.assert_one_finding(GOOD.replace("glossary: GLOSSARY.md", "glossary: docs"),
                                "glossary", "not a file")

    def test_s004_a_file_where_a_directory_is_needed_fails(self):
        self.assert_one_finding(GOOD.replace("spec_dir: docs/spec", "spec_dir: AGENTS.md"),
                                "spec_dir", "not a directory")

    def test_s004_a_path_differing_only_in_letter_case_fails_on_every_system(self):
        self.assert_one_finding(GOOD.replace("glossary: GLOSSARY.md", "glossary: glossary.md"),
                                "glossary", "letter case")

    def test_s005_none_is_a_valid_path_value(self):
        self.write_config(GOOD.replace("glossary: GLOSSARY.md", "glossary: none")
                          .replace("standards: AGENTS.md, docs/style.md", "standards: none"))
        for module in self.each():
            self.assertEqual(self.findings(module), [])

    def test_s006_a_missing_version_fails(self):
        self.assert_one_finding(GOOD.replace("config_version: 1\n", ""),
                                "config_version is required")

    def test_s007_a_newer_version_fails_with_a_named_message(self):
        self.assert_one_finding(GOOD.replace("config_version: 1", "config_version: 2"),
                                "config_version is 2", "versions up to 1", "update")

    def test_s007_a_newer_version_is_reported_alone(self):
        self.assert_one_finding(GOOD.replace("config_version: 1",
                                             "config_version: 3\nfuture_key: x"),
                                "config_version is 3")

    def test_s020_unicode_digits_signs_and_leading_zeros_fail(self):
        for value in ("\uff11", "+1", "01", "1.0"):
            self.assert_one_finding(GOOD.replace("config_version: 1", f"config_version: {value}"),
                                    "positive whole number")

    def test_s013_a_home_path_fails_for_a_key_other_than_session_logs(self):
        self.assert_one_finding(GOOD.replace("glossary: GLOSSARY.md", "glossary: ~/g.md"),
                                "glossary", "inside the repository")

    def test_s037_the_value_is_split_at_the_first_colon_and_quotes_are_kept(self):
        self.write_config(GOOD.replace("acceptance: python -m pytest",
                                       "acceptance: make check: all"))
        for module in self.each():
            values, problems = module.parse_zen_config(
                (self.root / "docs" / "agents" / "zen.md").read_text(encoding="utf-8"))
            self.assertEqual(values["acceptance"], "make check: all")
        self.assert_one_finding(GOOD.replace("glossary: GLOSSARY.md", 'glossary: "GLOSSARY.md"'),
                                "glossary", "does not exist")

    def test_s037_none_is_lower_case_only(self):
        self.assert_one_finding(GOOD.replace("adr_dir: none", "adr_dir: None"),
                                "adr_dir", "does not exist")

    def test_s038_crlf_line_endings_and_tabs_decide_the_same(self):
        self.write_config(GOOD.replace("\n", "\r\n").replace("glossary: ", "glossary:\t"))
        for module in self.each():
            self.assertEqual(self.findings(module), [])

    def test_s038_every_finding_is_reported_in_one_run(self):
        self.write_config(GOOD.replace("tracker: github", "tracker: jira")
                          .replace("default_mode: hitl", "default_mode: auto"))
        for module in self.each():
            self.assertEqual(len(self.findings(module)), 2)

    def test_s038_strict_reports_the_same_and_links_mode_does_not_check(self):
        self.write_config(GOOD.replace("tracker: github", "tracker: jira"))
        for module in self.each():
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                self.assertEqual(module.main(["--strict"]), 1)
            self.assertIn("tracker 'jira'", buf.getvalue())
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                module.main(["--links", "*.md"])
            self.assertNotIn("zen", buf.getvalue())

    def test_s003_a_known_key_in_other_letter_case_is_unknown(self):
        self.assert_one_finding(GOOD.replace("tracker: github", "Tracker: github"),
                                "unknown key", "Tracker")

    def test_s006_a_block_of_only_malformed_lines_still_asks_for_a_version(self):
        self.write_config("```zen-config\nnot a key value line\n```\n")
        for module in self.each():
            found = self.findings(module)
            self.assertEqual(len(found), 2, found)
            self.assertTrue(any("config_version is required" in f for f in found))

    def test_s012_a_windows_style_outside_path_is_not_checked_anywhere(self):
        for value in ("C:/Users/me/logs", "\\\\host\\share"):
            self.write_config(GOOD.replace("session_logs: ~/.claude/projects",
                                           f"session_logs: {value}"))
            for module in self.each():
                self.assertEqual(self.findings(module), [])

    def test_s036_only_a_well_formed_fence_opens_a_block(self):
        tilde = GOOD.replace("```zen-config", "~~~zen-config").replace("```\n", "~~~~\n")
        self.write_config(tilde.replace("```text", "~~~text"))
        for module in self.each():
            self.assertEqual(self.findings(module), [])
        self.write_config("    ```zen-config\n    bogus\n    ```\n\n" + GOOD)
        for module in self.each():
            self.assertEqual(self.findings(module), [])

    def test_s038_a_no_break_space_is_part_of_the_value(self):
        self.assert_one_finding(GOOD.replace("glossary: GLOSSARY.md", "glossary: GLOSSARY.md\u00a0"),
                                "glossary", "does not exist")

    def test_s041_an_unclosed_block_is_reported_as_unclosed(self):
        self.assert_one_finding(GOOD.rsplit("```", 1)[0] + "\n## Tracker\n\n- Tracker notes\n",
                                "never closed")

    def test_s042_dot_segments_are_refused_with_a_normalise_message(self):
        self.assert_one_finding(GOOD.replace("glossary: GLOSSARY.md", "glossary: docs/../GLOSSARY.md"),
                                "glossary", "normalised")
        self.assert_one_finding(GOOD.replace("spec_dir: docs/spec", "spec_dir: docs//spec"),
                                "spec_dir", "normalised")

    def test_s042_a_leading_dot_slash_is_allowed(self):
        (self.root / "none").write_text("a file named none\n", encoding="utf-8")
        self.write_config(GOOD.replace("glossary: GLOSSARY.md", "glossary: ./none"))
        for module in self.each():
            self.assertEqual(self.findings(module), [])

    def test_s008_a_tracker_outside_the_set_fails(self):
        self.assert_one_finding(GOOD.replace("tracker: github", "tracker: jira"),
                                "tracker", "jira", "gitlab")

    def test_s043_the_old_tracker_name_is_accepted(self):
        # `tasks` is the name before the rename to quests (feat-0101): a repository
        # configured before it must still validate, wherever its validator sits.
        for line in ("tracker: tasks", "tracker: quests"):
            self.write_config(GOOD.replace("tracker: github", line))
            for module in self.each():
                for folder in (".tasks", ".quests"):
                    with self.subTest(line=line, folder=folder):
                        module.TASKS_DIR = self.root / folder
                        self.assertEqual(self.findings(module), [])
                        code, out = self.run_main(module)
                        self.assertEqual(code, 0, out)

    def test_s007_the_update_message_names_the_directory_the_validator_sits_in(self):
        self.write_config(GOOD.replace("config_version: 1", "config_version: 2"))
        for module in self.each():
            for folder in (".tasks", ".quests"):
                with self.subTest(folder=folder):
                    module.TASKS_DIR = self.root / folder
                    found = self.findings(module)
                    self.assertEqual(len(found), 1, found)
                    self.assertIn(f"update {folder}/validate.py from the kit", found[0])

    def test_s008_a_default_mode_outside_the_set_fails(self):
        self.assert_one_finding(GOOD.replace("default_mode: hitl", "default_mode: auto"),
                                "default_mode", "auto", "afk")

    def test_s020_a_version_that_is_not_a_whole_number_fails(self):
        self.assert_one_finding(GOOD.replace("config_version: 1", "config_version: one"),
                                "'one'", "positive whole number")

    def test_s009_a_repeated_key_fails(self):
        self.assert_one_finding(GOOD.replace("base_branch: main",
                                             "base_branch: main\nbase_branch: dev"),
                                "base_branch", "more than once")

    def test_s010_a_line_that_is_not_key_value_fails(self):
        self.assert_one_finding(GOOD.replace("base_branch: main", "base_branch main"),
                                "base_branch main")

    def test_s010_an_empty_value_fails(self):
        self.assert_one_finding(GOOD.replace("base_branch: main", "base_branch:"),
                                "base_branch:")

    def test_s011_no_block_fails(self):
        self.assert_one_finding("# Agent skills setup\n\nNo block here.\n", "found 0")

    def test_s011_two_blocks_fail(self):
        self.assert_one_finding(GOOD + "\n```zen-config\nconfig_version: 1\n```\n", "found 2")

    def test_s012_session_logs_outside_the_repository_are_not_checked(self):
        for value in ("~/.claude/projects", "/nowhere/at/all"):
            self.write_config(GOOD.replace("session_logs: ~/.claude/projects",
                                           f"session_logs: {value}"))
            for module in self.each():
                self.assertEqual(self.findings(module), [])

    def test_s012_a_repository_relative_session_log_path_is_checked(self):
        self.assert_one_finding(GOOD.replace("session_logs: ~/.claude/projects",
                                             "session_logs: logs"),
                                "session_logs", "does not exist")

    def test_s013_a_path_that_leaves_the_repository_fails(self):
        self.assert_one_finding(GOOD.replace("spec_dir: docs/spec", "spec_dir: ../elsewhere"),
                                "spec_dir", "inside the repository")

    def test_s013_an_absolute_path_fails(self):
        absolute = str((self.root / "docs" / "spec").resolve())
        self.assert_one_finding(GOOD.replace("spec_dir: docs/spec", f"spec_dir: {absolute}"),
                                "spec_dir", "inside the repository")

    def test_s013_a_backslash_path_fails(self):
        self.assert_one_finding(GOOD.replace("spec_dir: docs/spec", "spec_dir: docs\\spec"),
                                "spec_dir", "forward-slash")

    def test_s013_a_drive_letter_path_fails_on_every_system(self):
        self.assert_one_finding(GOOD.replace("spec_dir: docs/spec", "spec_dir: C:/docs/spec"),
                                "spec_dir", "forward-slash")

    def test_s027_free_text_values_are_not_checked(self):
        self.write_config(GOOD.replace("base_branch: main", "base_branch: no such branch")
                          .replace("acceptance: python -m pytest", 'acceptance: "quoted" & odd'))
        for module in self.each():
            self.assertEqual(self.findings(module), [])

    def test_s028_an_empty_standards_entry_fails(self):
        self.assert_one_finding(GOOD.replace("AGENTS.md, docs/style.md",
                                             "AGENTS.md,, docs/style.md"),
                                "standards", "empty entry")

    def test_s028_none_beside_other_standards_fails(self):
        self.assert_one_finding(GOOD.replace("AGENTS.md, docs/style.md", "AGENTS.md, none"),
                                "standards", "on its own")

    def test_s019_a_block_inside_a_tilde_fence_is_not_counted(self):
        self.write_config("~~~\n```zen-config\nbogus\n```\n~~~\n\n" + GOOD)
        for module in self.each():
            self.assertEqual(self.findings(module), [])

    def test_s019_a_longer_info_string_is_not_a_block(self):
        self.write_config("```zen-config extra\nbogus\n```\n\n" + GOOD)
        for module in self.each():
            self.assertEqual(self.findings(module), [])

    def test_s019_prose_other_fences_and_comments_are_not_reported(self):
        # GOOD carries an invalid `tracker:` inside a `text` fence and a comment line in
        # the block; S-001 passing proves neither was read. This pins the fence half
        # directly, against a block-shaped example quoted in prose.
        self.write_config("````markdown\n```zen-config\nbogus\n```\n````\n\n" + GOOD)
        for module in self.each():
            self.assertEqual(self.findings(module), [])


class ModeFieldTests(Fixture):
    """The optional task `mode` field: `afk` or `hitl`, checked only when present."""

    def write_task(self, mode_line):
        (self.root / ".quests" / "feat-0001-test.md").write_text(
            TASK.format(mode=mode_line), encoding="utf-8")

    def test_an_absent_mode_is_valid(self):
        self.write_task("")
        for module in self.each():
            self.assertEqual(self.run_main(module)[0], 0)

    def test_each_named_mode_is_valid(self):
        for mode in ("afk", "hitl"):
            self.write_task(f"mode: {mode}\n")
            for module in self.each():
                self.assertEqual(self.run_main(module)[0], 0)

    def test_any_other_mode_fails(self):
        self.write_task("mode: auto\n")
        for module in self.each():
            code, out = self.run_main(module)
            self.assertEqual(code, 1)
            self.assertIn("mode 'auto'", out)


if __name__ == "__main__":
    unittest.main()
