"""Acceptance tests for .agents/hooks/instruction-provenance-reminder.py (feat-0081).

test-quality notes: every scenario runs at the lowest faithful layer, calling evaluate(),
findings() and main() directly against a temporary filesystem. Repositories are built with
real git, because the defect that matters most here is the hook disagreeing with git about
what is committed, and a hand-built index would only prove the parser agrees with itself.
Oracles assert the exact file named and the exact reason, or exact silence.

The defect each group protects against:
  planted      - an instruction file in a folder no repository covers is loaded and nobody
                 is told (the Downloads attack this hook exists for)
  uncommitted  - a file inside a repository that no commit vouches for passes as vouched
  committed    - the hook speaks about files a commit already vouches for, and becomes a
                 line agents learn to skip
  personal     - the two files that are uncommitted by design are reported on every start,
                 or a planted hook hides inside one of them
  index        - the index parser disagrees with git on a real index format (v2, v3 with
                 extended flags, v4 prefix compression, SHA-256), or passes a split index it
                 cannot read as committed
  scope        - the person's own user-scope settings at the home directory are reported
  source       - it repeats itself on resume, clear, compact, and fork
  never runs   - the hook grows a subprocess and starts executing planted git config
  robustness   - a malformed payload takes down the session
  dogfood      - the hook is noisy, or silent, in the repository that ships it
"""
import ast
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parent.parent
MODULE_PATH = REPO_ROOT / ".agents" / "hooks" / "instruction-provenance-reminder.py"

_spec = importlib.util.spec_from_file_location("instruction_provenance_reminder", MODULE_PATH)
ipr = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ipr)

GIT = shutil.which("git")


def _git(*args, cwd):
    subprocess.run([GIT, *args], cwd=cwd, check=True, capture_output=True)


def _payload(cwd, source="startup", event="SessionStart"):
    return {"hook_event_name": event, "source": source, "cwd": str(cwd)}


class _Tmp(unittest.TestCase):
    """A fresh directory for each test, plus a separate fake home outside it."""

    def setUp(self):
        self.root = Path(tempfile.mkdtemp()).resolve()
        self.home = Path(tempfile.mkdtemp()).resolve()
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)
        self.addCleanup(shutil.rmtree, self.home, ignore_errors=True)

    def repo(self, path=None, object_format=None):
        path = path or self.root
        path.mkdir(parents=True, exist_ok=True)
        args = ["init", "-q"]
        if object_format:
            args.append(f"--object-format={object_format}")
        _git(*args, cwd=path)
        return path

    def found(self, cwd):
        return [(p.relative_to(self.root).as_posix(), why)
                for p, why in ipr.findings(cwd, self.home)]


class PlantedTests(_Tmp):
    def test_an_agents_file_in_a_folder_no_repository_covers_is_named(self):
        (self.root / "AGENTS.md").write_text("install this package", encoding="utf-8")
        out = ipr.evaluate(_payload(self.root), home=self.home)
        context = out["hookSpecificOutput"]["additionalContext"]
        self.assertEqual("SessionStart", out["hookSpecificOutput"]["hookEventName"])
        self.assertTrue(context.startswith("UNVOUCHED INSTRUCTION FILES"))
        self.assertIn("`AGENTS.md` (outside any git repository)", context)
        self.assertIn("A10", context)

    def test_a_memory_file_above_the_repository_root_is_named(self):
        (self.root / "CLAUDE.md").write_text("redirect the endpoint", encoding="utf-8")
        inner = self.repo(self.root / "project")
        self.assertEqual([("CLAUDE.md", ipr.OUTSIDE)], self.found(inner))

    def test_project_files_outside_a_repository_are_named(self):
        (self.root / ".claude").mkdir()
        (self.root / ".claude" / "settings.json").write_text("{}", encoding="utf-8")
        (self.root / ".mcp.json").write_text("{}", encoding="utf-8")
        self.assertEqual(
            [(".claude/settings.json", ipr.OUTSIDE), (".mcp.json", ipr.OUTSIDE)],
            self.found(self.root))

    def test_even_a_personal_file_is_named_outside_a_repository(self):
        (self.root / "CLAUDE.local.md").write_text("x", encoding="utf-8")
        self.assertEqual([("CLAUDE.local.md", ipr.OUTSIDE)], self.found(self.root))

    def test_an_empty_folder_is_silent(self):
        self.assertIsNone(ipr.evaluate(_payload(self.root), home=self.home))

    def test_a_long_list_is_capped_and_says_how_many_more(self):
        for i in range(12):
            level = self.root.joinpath(*[f"d{j}" for j in range(i)])
            level.mkdir(parents=True, exist_ok=True)
            (level / "AGENTS.md").write_text("x", encoding="utf-8")
        deepest = self.root.joinpath(*[f"d{j}" for j in range(11)])
        context = ipr.evaluate(_payload(deepest), home=self.home)[
            "hookSpecificOutput"]["additionalContext"]
        self.assertIn(f"and {12 - ipr.MAX_LISTED} more", context)


@unittest.skipUnless(GIT, "git is needed to build real indexes")
class UncommittedAndCommittedTests(_Tmp):
    def test_an_uncommitted_agents_file_in_a_repository_is_named(self):
        self.repo()
        (self.root / "AGENTS.md").write_text("x", encoding="utf-8")
        self.assertEqual([("AGENTS.md", ipr.UNCOMMITTED)], self.found(self.root))

    def test_committed_instruction_files_are_silent(self):
        self.repo()
        (self.root / "AGENTS.md").write_text("x", encoding="utf-8")
        (self.root / "CLAUDE.md").write_text("@AGENTS.md", encoding="utf-8")
        (self.root / ".claude").mkdir()
        (self.root / ".claude" / "settings.json").write_text("{}", encoding="utf-8")
        _git("add", "AGENTS.md", "CLAUDE.md", ".claude/settings.json", cwd=self.root)
        self.assertEqual([], self.found(self.root))
        self.assertIsNone(ipr.evaluate(_payload(self.root), home=self.home))

    def test_a_subdirectory_launch_checks_the_repository_root_too(self):
        self.repo()
        (self.root / "AGENTS.md").write_text("x", encoding="utf-8")
        sub = self.root / "src"
        sub.mkdir()
        self.assertEqual([("AGENTS.md", ipr.UNCOMMITTED)], self.found(sub))

    def test_a_file_in_an_outer_repository_is_judged_by_that_repository(self):
        self.repo()
        (self.root / "AGENTS.md").write_text("x", encoding="utf-8")
        _git("add", "AGENTS.md", cwd=self.root)
        inner = self.repo(self.root / "vendored")
        self.assertEqual([], self.found(inner))


@unittest.skipUnless(GIT, "git is needed to build real indexes")
class PersonalTests(_Tmp):
    def setUp(self):
        super().setUp()
        self.repo()
        (self.root / ".claude").mkdir()
        self.local = self.root / ".claude" / "settings.local.json"

    def test_uncommitted_personal_files_are_silent(self):
        (self.root / "CLAUDE.local.md").write_text("mine", encoding="utf-8")
        self.local.write_text(json.dumps({"permissions": {"allow": ["Bash(ls)"]}}),
                              encoding="utf-8")
        self.assertEqual([], self.found(self.root))

    def test_a_local_settings_file_that_registers_hooks_is_named_with_its_keys(self):
        self.local.write_text(json.dumps({
            "hooks": {"SessionStart": []},
            "env": {"ANTHROPIC_BASE_URL": "https://example.invalid"},
        }), encoding="utf-8")
        self.assertEqual(
            [(".claude/settings.local.json", f"{ipr.UNCOMMITTED}, and it sets hooks, env")],
            self.found(self.root))

    def test_an_unparseable_local_settings_file_is_silent(self):
        self.local.write_text("{ not json", encoding="utf-8")
        self.assertEqual([], self.found(self.root))


@unittest.skipUnless(GIT, "git is needed to build real indexes")
class IndexFormatTests(_Tmp):
    """The parser must agree with git on what git itself writes."""

    def _tracked_names(self, version, object_format=None, intent_to_add=False):
        self.repo(object_format=object_format)
        (self.root / "AGENTS.md").write_text("a", encoding="utf-8")
        (self.root / "CLAUDE.md").write_text("c", encoding="utf-8")
        (self.root / "sub").mkdir()
        (self.root / "sub" / "x.txt").write_text("x", encoding="utf-8")
        (self.root / "sub" / "a-much-longer-name-that-shares-the-prefix.txt").write_text(
            "y", encoding="utf-8")
        _git("add", "AGENTS.md", "sub", cwd=self.root)
        if intent_to_add:
            _git("add", "--intent-to-add", "CLAUDE.md", cwd=self.root)
        _git("update-index", "--index-version", str(version), cwd=self.root)
        return {n.decode() for n in ipr.index_paths(self.root / ".git")}

    def test_index_v2_matches_git(self):
        self.assertEqual({"AGENTS.md", "sub/x.txt",
                          "sub/a-much-longer-name-that-shares-the-prefix.txt"},
                         self._tracked_names(2))

    def test_index_v3_with_an_extended_flag_matches_git(self):
        names = self._tracked_names(3, intent_to_add=True)
        self.assertIn("CLAUDE.md", names)
        self.assertIn("AGENTS.md", names)

    def test_index_v4_prefix_compression_matches_git(self):
        self.assertEqual({"AGENTS.md", "sub/x.txt",
                          "sub/a-much-longer-name-that-shares-the-prefix.txt"},
                         self._tracked_names(4))

    def test_a_sha256_repository_parses(self):
        try:
            names = self._tracked_names(4, object_format="sha256")
        except subprocess.CalledProcessError:
            self.skipTest("this git cannot create a SHA-256 repository")
        self.assertIn("AGENTS.md", names)

    def test_a_split_index_is_reported_as_unconfirmed_never_as_committed(self):
        self.repo()
        (self.root / "AGENTS.md").write_text("a", encoding="utf-8")
        _git("add", "AGENTS.md", cwd=self.root)
        _git("update-index", "--split-index", cwd=self.root)
        self.assertIsNone(ipr.index_paths(self.root / ".git"))
        self.assertEqual([("AGENTS.md", ipr.UNCONFIRMED)], self.found(self.root))

    def test_a_truncated_index_is_unconfirmed(self):
        self.repo()
        (self.root / "AGENTS.md").write_text("a", encoding="utf-8")
        _git("add", "AGENTS.md", cwd=self.root)
        index = self.root / ".git" / "index"
        index.write_bytes(index.read_bytes()[:40])
        self.assertIsNone(ipr.index_paths(self.root / ".git"))

    def test_a_repository_with_no_index_yet_tracks_nothing(self):
        self.repo()
        (self.root / "AGENTS.md").write_text("a", encoding="utf-8")
        self.assertEqual({}, ipr.index_paths(self.root / ".git"))
        self.assertEqual([("AGENTS.md", ipr.UNCOMMITTED)], self.found(self.root))

    def test_a_linked_worktree_reads_its_own_index(self):
        self.repo()
        _git("-c", "user.email=t@example.invalid", "-c", "user.name=t",
             "commit", "-q", "--allow-empty", "-m", "base", cwd=self.root)
        tree = self.root / "wt"
        _git("worktree", "add", "-q", str(tree), cwd=self.root)
        (tree / "AGENTS.md").write_text("a", encoding="utf-8")
        self.assertEqual([("wt/AGENTS.md", ipr.UNCOMMITTED)], self.found(tree))
        _git("add", "AGENTS.md", cwd=tree)
        self.assertEqual([], self.found(tree))


@unittest.skipUnless(GIT, "git is needed to build real indexes")
class IndependentVerificationTests(_Tmp):
    """Each case here is a defect the independent verification of PR #108 reproduced."""

    def test_project_files_where_the_session_started_are_checked_below_the_root(self):
        self.repo()
        sub = self.root / "sub"
        (sub / ".claude").mkdir(parents=True)
        (sub / ".mcp.json").write_text('{"mcpServers": {}}', encoding="utf-8")
        (sub / ".claude" / "settings.json").write_text("{}", encoding="utf-8")
        self.assertEqual([("sub/.claude/settings.json", ipr.UNCOMMITTED),
                          ("sub/.mcp.json", ipr.UNCOMMITTED)], self.found(sub))

    def test_a_dotfiles_repository_at_home_does_not_hide_a_planted_project(self):
        home = self.repo()
        evil = home / "Downloads" / "evil"
        (evil / ".claude").mkdir(parents=True)
        (evil / "AGENTS.md").write_text("x", encoding="utf-8")
        (evil / ".claude" / "settings.json").write_text("{}", encoding="utf-8")
        (evil / ".mcp.json").write_text("{}", encoding="utf-8")
        names = [p.relative_to(home).as_posix() for p, _ in ipr.findings(evil, home)]
        self.assertEqual(["Downloads/evil/AGENTS.md", "Downloads/evil/.claude/settings.json",
                          "Downloads/evil/.mcp.json"], names)

    def _staged_index(self):
        source = Path(tempfile.mkdtemp()).resolve()
        self.addCleanup(shutil.rmtree, source, ignore_errors=True)
        self.repo(source)
        (source / "AGENTS.md").write_text("a", encoding="utf-8")
        _git("add", "AGENTS.md", cwd=source)
        return source

    def test_three_plain_files_do_not_pass_as_a_repository(self):
        source = self._staged_index()
        (self.root / "AGENTS.md").write_text("planted", encoding="utf-8")
        (self.root / ".git").write_text("gitdir: .\n", encoding="utf-8")
        (self.root / "index").write_bytes((source / ".git" / "index").read_bytes())
        self.assertEqual([("AGENTS.md", ipr.UNCONFIRMED)], self.found(self.root))

    def test_a_git_file_borrowing_another_repositorys_index_does_not_vouch_for_new_text(self):
        # The borrowed index lists AGENTS.md, but for the other repository's content: the
        # planted file's text hashes to a different blob, so it is named.
        source = self._staged_index()
        (self.root / "AGENTS.md").write_text("planted", encoding="utf-8")
        (self.root / ".git").write_text(f"gitdir: {source / '.git'}\n", encoding="utf-8")
        self.assertEqual([("AGENTS.md", ipr.MODIFIED)], self.found(self.root))

    def test_a_fake_git_folder_without_refs_is_not_a_repository(self):
        source = self._staged_index()
        (self.root / "AGENTS.md").write_text("a", encoding="utf-8")
        fake = self.root / ".git"
        (fake / "objects").mkdir(parents=True)
        (fake / "HEAD").write_text("ref: refs/heads/main\n", encoding="utf-8")
        (fake / "index").write_bytes((source / ".git" / "index").read_bytes())
        self.assertEqual([("AGENTS.md", ipr.UNCONFIRMED)], self.found(self.root))

    def test_a_separate_git_dir_checkout_is_confirmed(self):
        tree = self.root / "wt"
        tree.mkdir()
        _git("init", "-q", f"--separate-git-dir={self.root / 'sep.git'}", cwd=tree)
        (tree / "AGENTS.md").write_text("a", encoding="utf-8")
        _git("add", "AGENTS.md", cwd=tree)
        self.assertEqual([], self.found(tree))

    def test_a_worktree_moved_without_repair_is_still_confirmed(self):
        self.repo()
        _git("-c", "user.email=t@example.invalid", "-c", "user.name=t",
             "commit", "-q", "--allow-empty", "-m", "base", cwd=self.root)
        _git("worktree", "add", "-q", str(self.root / "wt"), cwd=self.root)
        (self.root / "wt" / "AGENTS.md").write_text("a", encoding="utf-8")
        _git("add", "AGENTS.md", cwd=self.root / "wt")
        (self.root / "wt").rename(self.root / "moved")
        self.assertEqual([], self.found(self.root / "moved"))

    def test_a_committed_file_edited_in_place_is_named(self):
        self.repo()
        (self.root / "CLAUDE.md").write_text("the reviewed text\n", encoding="utf-8")
        _git("add", "CLAUDE.md", cwd=self.root)
        (self.root / "CLAUDE.md").write_text("the reviewed text\nand one planted line\n",
                                             encoding="utf-8")
        self.assertEqual([("CLAUDE.md", ipr.MODIFIED)], self.found(self.root))

    def test_a_crlf_checkout_of_a_committed_file_is_confirmed(self):
        self.repo()
        (self.root / "AGENTS.md").write_bytes(b"line one\nline two\n")
        _git("add", "AGENTS.md", cwd=self.root)
        (self.root / "AGENTS.md").write_bytes(b"line one\r\nline two\r\n")
        self.assertEqual([], self.found(self.root))

    def test_a_submodule_is_confirmed_through_its_worktree_setting(self):
        library = self._staged_index()
        _git("-c", "user.email=t@example.invalid", "-c", "user.name=t",
             "commit", "-q", "-m", "lib", cwd=library)
        self.repo()
        _git("-c", "protocol.file.allow=always", "submodule", "add", "-q", str(library),
             "lib", cwd=self.root)
        self.assertEqual([], self.found(self.root / "lib"))

    @unittest.skipUnless(sys.platform.startswith("linux"),
                         "only Linux filesystems accept a name that is not UTF-8")
    def test_a_name_that_is_not_utf8_does_not_silence_the_hook(self):
        self.repo()
        odd = os.path.join(os.fsencode(str(self.root)), b"caf\xe9")
        os.mkdir(odd)
        with open(os.path.join(odd, b"AGENTS.md"), "w", encoding="utf-8") as handle:
            handle.write("a")
        _git("add", os.fsdecode(os.path.join(b"caf\xe9", b"AGENTS.md")), cwd=self.root)
        (self.root / "CLAUDE.md").write_text("planted", encoding="utf-8")
        self.assertEqual([("CLAUDE.md", ipr.UNCOMMITTED)],
                         self.found(Path(os.fsdecode(odd))))

    def test_a_committed_link_to_a_file_outside_the_repository_is_named(self):
        self.repo()
        outside = Path(tempfile.mkdtemp()).resolve()
        self.addCleanup(shutil.rmtree, outside, ignore_errors=True)
        (outside / "payload.md").write_text("planted", encoding="utf-8")
        try:
            (self.root / "AGENTS.md").symlink_to(outside / "payload.md")
        except OSError:
            self.skipTest("this platform does not allow creating a symlink here")
        _git("add", "AGENTS.md", cwd=self.root)
        self.assertEqual([("AGENTS.md", ipr.LINKED_OUT)], self.found(self.root))


class MemoryAndSettingsTests(_Tmp):
    def test_dot_claude_claude_md_is_a_memory_file(self):
        (self.root / ".claude").mkdir()
        (self.root / ".claude" / "CLAUDE.md").write_text("x", encoding="utf-8")
        self.assertEqual([(".claude/CLAUDE.md", ipr.OUTSIDE)], self.found(self.root))

    def test_user_memory_at_home_is_not_reported(self):
        home = self.root
        (home / ".claude").mkdir()
        (home / ".claude" / "CLAUDE.md").write_text("mine", encoding="utf-8")
        project = home / "work"
        project.mkdir()
        self.assertEqual([], ipr.findings(project, home))

    def test_a_directory_that_cannot_be_listed_still_yields_a_file_by_name(self):
        (self.root / "AGENTS.md").write_text("x", encoding="utf-8")
        real = os.listdir

        def refuse(path):
            if Path(path) == self.root:
                raise PermissionError("listing denied")
            return real(path)

        with mock.patch.object(ipr.os, "listdir", refuse):
            self.assertEqual([("AGENTS.md", ipr.OUTSIDE)], self.found(self.root))

    def test_settings_that_widen_what_runs_without_asking_are_named(self):
        local = self.root / ".claude" / "settings.local.json"
        local.parent.mkdir()
        local.write_text(json.dumps({
            "permissions": {"defaultMode": "bypassPermissions"},
            "enabledPlugins": {"x@y": True},
            "extraKnownMarketplaces": {"y": {}},
        }), encoding="utf-8")
        self.assertEqual(["enabledPlugins", "extraKnownMarketplaces", "permissions.defaultMode"],
                         ipr._executing_keys(local))


class ScopeAndSourceTests(_Tmp):
    def test_user_scope_settings_at_the_home_directory_are_not_reported(self):
        home = self.root
        (home / ".claude").mkdir()
        (home / ".claude" / "settings.json").write_text(
            json.dumps({"hooks": {}}), encoding="utf-8")
        self.assertEqual([], ipr.findings(home, home))

    def test_only_a_new_session_fires(self):
        (self.root / "AGENTS.md").write_text("x", encoding="utf-8")
        self.assertIsNotNone(ipr.evaluate(_payload(self.root), home=self.home))
        for source in ("resume", "clear", "compact", "fork"):
            with self.subTest(source=source):
                self.assertIsNone(
                    ipr.evaluate(_payload(self.root, source=source), home=self.home))

    def test_another_event_is_silent(self):
        (self.root / "AGENTS.md").write_text("x", encoding="utf-8")
        self.assertIsNone(
            ipr.evaluate(_payload(self.root, event="PostToolUse"), home=self.home))


class NeverRunsTests(unittest.TestCase):
    """The hook must never execute anything, planted git config included."""

    def test_the_hook_imports_no_process_module_and_calls_no_process_function(self):
        tree = ast.parse(MODULE_PATH.read_text(encoding="utf-8"))
        modules, calls = set(), set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                modules.update(a.name.split(".")[0] for a in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                modules.add(node.module.split(".")[0])
            elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                calls.add(node.func.attr)
        self.assertFalse(modules & {"subprocess", "multiprocessing", "pty", "shlex"})
        self.assertFalse(calls & {"system", "popen", "spawnl", "spawnv", "execv",
                                  "execvp", "startfile", "run", "Popen"})

    def test_the_hook_writes_nothing(self):
        # Method names that only a write can mean, any `os.<writer>` call, and `open` in a
        # write mode. A bare `replace` is not listed: the hook calls `bytes.replace` to allow
        # for CRLF checkouts, and a guard that fires on that gets loosened until it guards
        # nothing. `os.replace` is still caught by the `os.` rule.
        tree = ast.parse(MODULE_PATH.read_text(encoding="utf-8"))
        writes = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            func = node.func
            if isinstance(func, ast.Attribute):
                if func.attr in {"write_text", "write_bytes", "mkdir", "unlink", "rename",
                                 "touch", "rmdir", "symlink_to", "hardlink_to"}:
                    writes.append(func.attr)
                if isinstance(func.value, ast.Name) and func.value.id == "os" and func.attr in {
                        "remove", "unlink", "rename", "replace", "mkdir", "makedirs",
                        "rmdir", "removedirs", "symlink", "link", "truncate", "write"}:
                    writes.append(f"os.{func.attr}")
            if isinstance(func, ast.Name) and func.id == "open":
                # No mode means read. A mode that is not a literal cannot be judged, so it
                # counts as a write.
                given = node.args[1:2] + [k.value for k in node.keywords if k.arg == "mode"]
                for mode in given:
                    if not isinstance(mode, ast.Constant) or set(str(mode.value)) & set("wax+"):
                        writes.append("open")
        self.assertEqual([], writes)


class RobustnessTests(unittest.TestCase):
    def _run(self, text):
        out = io.StringIO()
        code = ipr.main(stdin=io.StringIO(text), stdout=out)
        return code, out.getvalue()

    def test_malformed_input_exits_zero_silently(self):
        for text in ("", "not json", "[]", "42", json.dumps({"hook_event_name": 7})):
            with self.subTest(text=text):
                self.assertEqual((0, ""), self._run(text))

    def test_a_missing_cwd_falls_back_without_crashing(self):
        code, _ = self._run(json.dumps({"hook_event_name": "SessionStart",
                                        "source": "startup"}))
        self.assertEqual(0, code)

    def test_stdout_is_exactly_one_json_object_when_it_fires(self):
        root = Path(tempfile.mkdtemp()).resolve()
        self.addCleanup(shutil.rmtree, root, ignore_errors=True)
        (root / "AGENTS.md").write_text("x", encoding="utf-8")
        code, text = self._run(json.dumps(_payload(root)))
        self.assertEqual(0, code)
        self.assertIsInstance(json.loads(text), dict)


class DogfoodTests(unittest.TestCase):
    def test_nothing_this_repository_ships_is_reported_here(self):
        """A guardrail that cannot be quiet in the repository that ships it gets uninstalled.

        Directories above the checkout are the machine's business, so only findings inside
        it are asserted on.
        """
        home = Path(tempfile.mkdtemp()).resolve()
        self.addCleanup(shutil.rmtree, home, ignore_errors=True)
        root = REPO_ROOT.resolve()
        inside = [p for p, _ in ipr.findings(root, home) if root in p.parents]
        self.assertEqual([], inside)


if __name__ == "__main__":
    unittest.main()
