"""Tests for .agents/hooks/destructive-git-gate.py (decision D3: ship it opt-in).

test-quality notes: every case calls main() with injected streams, matching the convention
in test_hooks.py, and asserts the exact output: either one block object whose reason names
the operation as written in the literal oracle below, or nothing at all. The operation
labels are spelled out here rather than read back from the module's table, so a renamed or
mis-keyed rule fails a test instead of agreeing with itself.

The defect each group protects against:
  blocks       - a destructive git command runs with nothing said (the gate's whole job)
  evasions     - quoting, global options, wrappers or chaining walk a command past the gate
  stays quiet  - the gate blocks a safe or read-only command and gets uninstalled
  robustness   - a malformed payload takes down the session
"""
import importlib.util
import io
import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MODULE_PATH = REPO_ROOT / ".agents" / "hooks" / "destructive-git-gate.py"

# Hyphenated filename, so it is not importable by a normal import statement.
_spec = importlib.util.spec_from_file_location("destructive_git_gate", MODULE_PATH)
gate = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gate)

OPT_OUT = ("If you disagree with this gate, remove the destructive-git-gate.py entry from "
           "your hook settings; it is opt-in.")


def run_raw(text):
    out = io.StringIO()
    code = gate.main(stdin=io.StringIO(text), stdout=out)
    return code, out.getvalue()


def payload(command, tool="Bash", event="PreToolUse"):
    return {"hook_event_name": event, "tool_name": tool,
            "tool_input": {"command": command}}


def run(command, **kwargs):
    return run_raw(json.dumps(payload(command, **kwargs)))


class _GateCase(unittest.TestCase):

    def assertBlocks(self, command, operation, **kwargs):
        code, out = run(command, **kwargs)
        self.assertEqual(code, 0)
        self.assertTrue(out, f"expected a block for {command!r}, got silence")
        obj = json.loads(out)  # exactly one JSON object, or this raises
        self.assertEqual(set(obj), {"decision", "reason"})
        self.assertEqual(obj["decision"], "block")
        self.assertTrue(
            obj["reason"].startswith(f"Destructive-git gate: blocked `{operation}`: it "),
            f"{command!r} was blocked as the wrong operation: {obj['reason']!r}")
        self.assertTrue(obj["reason"].endswith(OPT_OUT), "the opt-out escape is missing")

    def assertSilent(self, command, **kwargs):
        code, out = run(command, **kwargs)
        self.assertEqual(code, 0)
        self.assertEqual(out, "", f"expected silence for {command!r}, got {out!r}")


class BlockedFormsTests(_GateCase):
    """Every operation in the table, in each spelling the brief names."""

    CASES = [
        ("git push --force", "git push --force"),
        ("git push -f origin main", "git push --force"),
        ("git push -fu origin main", "git push --force"),
        ("git push origin +main", "git push --force"),
        ("git push --force-if-includes origin main", "git push --force"),
        ("git push --force --no-force-with-lease", "git push --force"),
        ("git push --mirror", "git push --mirror"),
        ("git push --delete origin old", "git push --delete"),
        ("git push -d origin old", "git push --delete"),
        ("git push origin :old", "git push --delete"),
        ("git push --del origin old", "git push --delete"),
        ("git push --prune origin", "git push --prune"),
        ("git reset --hard", "git reset --hard"),
        ("git reset --hard HEAD~3", "git reset --hard"),
        ("git reset -q --hard origin/main", "git reset --hard"),
        ("git reset --ha", "git reset --hard"),
        ("git clean -f", "git clean --force"),
        ("git clean --force", "git clean --force"),
        ("git clean -fd", "git clean --force"),
        ("git clean -xdf", "git clean --force"),
        ("git branch -D topic", "git branch -D"),
        ("git branch --delete --force topic", "git branch -D"),
        ("git branch -d -f topic", "git branch -D"),
        ("git branch -df topic", "git branch -D"),
        ("git checkout -- .", "git checkout -- <path>"),
        ("git checkout .", "git checkout -- <path>"),
        ("git checkout -- src/app.py", "git checkout -- <path>"),
        ("git checkout main -- src/app.py", "git checkout -- <path>"),
        ("git checkout -f main", "git checkout --force"),
        ("git checkout --force main", "git checkout --force"),
        ("git switch --discard-changes main", "git switch --discard-changes"),
        ("git restore .", "git restore <path>"),
        ("git restore src/app.py", "git restore <path>"),
        ("git restore --source HEAD~1 src/app.py", "git restore <path>"),
        ("git restore --staged --worktree src/app.py", "git restore <path>"),
        ("git restore -SW src/app.py", "git restore <path>"),
        ("git stash drop", "git stash drop"),
        ("git stash drop stash@{1}", "git stash drop"),
        ("git stash clear", "git stash clear"),
        ("git reflog expire --expire=now --all", "git reflog expire --expire=now"),
        ("git reflog expire --expire-unreachable=now --all",
         "git reflog expire --expire=now"),
        ("git gc --prune=now", "git gc --prune=now"),
        ("git prune", "git prune"),
        ("git update-ref -d refs/heads/topic", "git update-ref -d"),
        ("git filter-branch --tree-filter 'rm -f x' HEAD", "git filter-branch"),
        ("git worktree remove --force ../wt", "git worktree remove --force"),
    ]

    def test_every_destructive_form_blocks_with_its_operation_named(self):
        for command, operation in self.CASES:
            with self.subTest(command=command):
                self.assertBlocks(command, operation)

    def test_the_reason_names_the_way_out_in_full(self):
        # One reason pinned verbatim, so the escape cannot quietly drop out of the text.
        code, out = run("git push --force")
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out), {
            "decision": "block",
            "reason": ("Destructive-git gate: blocked `git push --force`: it overwrites the "
                       "remote branch and can discard commits someone else pushed. Use "
                       "--force-with-lease (it refuses if the remote moved since you "
                       "fetched), or run it yourself in a terminal. " + OPT_OUT),
        })

    def test_every_rule_in_the_table_names_a_way_out(self):
        for key, (operation, why, way_out) in gate.RULES.items():
            with self.subTest(rule=key):
                self.assertTrue(operation.startswith("git "))
                self.assertTrue(why and way_out)
                self.assertIn("yourself in a terminal", way_out)


class EvasionTests(_GateCase):
    """Spellings that a regular expression over the text would miss or misread."""

    CASES = [
        ("git 'push' \"--force\"", "git push --force"),
        ('git push --"force"', "git push --force"),
        ("git pu\\sh --force", "git push --force"),
        ("git -C /tmp/x push -f", "git push --force"),
        ("git -c core.x=y reset --hard", "git reset --hard"),
        ("git --git-dir .git --work-tree . reset --hard", "git reset --hard"),
        ("git --no-pager -P reset --hard", "git reset --hard"),
        ("cd x && git reset --hard", "git reset --hard"),
        ("true; git clean -fdx", "git clean --force"),
        ("false || git clean -fdx", "git clean --force"),
        ("ls | git branch -D x", "git branch -D"),
        ("sleep 1 & git stash clear", "git stash clear"),
        ("echo hi\ngit reset --hard", "git reset --hard"),
        ("( git reset --hard )", "git reset --hard"),
        ("{ git reset --hard; }", "git reset --hard"),
        ('bash -c "git push --force"', "git push --force"),
        ("sh -c 'cd x && git reset --hard'", "git reset --hard"),
        ("bash -o pipefail -lc 'git reset --hard'", "git reset --hard"),
        ("eval git reset --hard", "git reset --hard"),
        ("$(git reset --hard)", "git reset --hard"),
        ('echo "$(git stash drop)"', "git stash drop"),
        ("echo `git stash clear`", "git stash clear"),
        ("GIT_DIR=. git reset --hard", "git reset --hard"),
        ("env FOO=1 git reset --hard", "git reset --hard"),
        ("sudo git reset --hard", "git reset --hard"),
        ("sudo -u root git reset --hard", "git reset --hard"),
        ("nohup git push -f &", "git push --force"),
        ("timeout 30 git push -f", "git push --force"),
        ("/usr/bin/git reset --hard", "git reset --hard"),
        ("git.exe push -f", "git push --force"),
        ("git status 2>/dev/null && git reset --hard", "git reset --hard"),
        ("for b in a c; do git branch -D $b; done", "git branch -D"),
    ]

    def test_every_evasion_is_still_blocked(self):
        for command, operation in self.CASES:
            with self.subTest(command=command):
                self.assertBlocks(command, operation)

    def test_powershell_paths_keep_their_backslashes(self):
        # Under POSIX rules the backslashes would be escapes and `git.exe` would vanish.
        self.assertBlocks("C:\\Git\\bin\\git.exe reset --hard", "git reset --hard",
                          tool="PowerShell")
        self.assertBlocks("git push `\n --force", "git push --force", tool="PowerShell")

    def test_an_argv_list_command_is_read_as_argv(self):
        # Some harnesses send the command as an argv array rather than shell text.
        self.assertBlocks(["git", "push", "-f"], "git push --force", tool="exec_command")
        self.assertBlocks(["bash", "-lc", "git reset --hard"], "git reset --hard",
                          tool="exec_command")

    def test_every_shell_tool_name_is_covered(self):
        for tool in ("Bash", "PowerShell", "bash", "shell", "local_shell", "exec_command"):
            with self.subTest(tool=tool):
                self.assertBlocks("git reset --hard", "git reset --hard", tool=tool)


class SafeFormsTests(_GateCase):
    """Read-only and safe forms, including ones that merely contain the scary words."""

    CASES = [
        "git status",
        "git log --oneline -5",
        "git push",
        "git push origin main",
        "git push -u origin topic",
        "git push --force-with-lease",
        "git push --force-with-lease=main:abc123 origin main",
        "git push --force --force-with-lease origin main",
        "git push -f --dry-run origin main",
        "git push --forc origin main",  # ambiguous abbreviation: git itself refuses it
        "git reset",
        "git reset --soft HEAD~1",
        "git reset --keep HEAD~1",
        "git reset HEAD file.txt",
        "git clean -n",
        "git clean -fn",
        "git clean --dry-run -fdx",
        "git branch -d topic",
        "git checkout main",
        "git checkout -b topic",
        "git checkout -b topic origin/main",
        "git checkout -",
        "git switch main",
        "git switch -c topic",
        "git restore --staged src/app.py",
        "git restore -S src/app.py",
        "git restore",
        "git stash",
        "git stash push -m 'drop this later'",
        "git stash list",
        "git stash pop",
        "git reflog",
        "git reflog expire --expire=90.days.ago --all",
        "git reflog expire --expire=now --dry-run --all",
        "git gc",
        "git gc --prune=2.weeks.ago",
        "git prune --dry-run",
        "git update-ref refs/heads/x HEAD",
        "git worktree remove ../wt",
        "git help reset",
        "git --help",
        'echo "git reset --hard"',
        "echo 'git push --force' > notes.txt",
        "grep 'push --force' file",
        "grep -r 'git clean -fdx' docs/",
        'git commit -m "reset --hard"',
        'git commit -m "$(printf "x")"',
        "git log --grep='push --force'",
        "cat <<EOF\ngit reset --hard\nEOF\necho ok",
        "git status # then git reset --hard",
        "gitk --all",
        "legit reset --hard",
        "printf '%s\\n' git reset --hard",
        "",
    ]

    def test_every_safe_form_is_silent(self):
        for command in self.CASES:
            with self.subTest(command=command):
                self.assertSilent(command)

    def test_a_bare_branch_force_delete_still_blocks(self):
        # `git branch -D` with no name fails in git, but the gate reads intent from argv
        # and does not try to predict git's own argument errors.
        self.assertBlocks("git branch -D", "git branch -D")


class UntokenisableLineTests(_GateCase):
    """(a) A shell runs earlier lines before it reaches a syntax error on a later one."""

    def test_a_destructive_line_before_an_unbalanced_quote_blocks(self):
        self.assertBlocks('git reset --hard\necho "unterminated', "git reset --hard")

    def test_a_destructive_line_after_an_unbalanced_quote_blocks(self):
        self.assertBlocks("echo 'unterminated\ngit push --force", "git push --force")

    def test_only_safe_lines_around_an_unbalanced_quote_stay_silent(self):
        self.assertSilent('git status\necho "unterminated')

    def test_an_unbalanced_quote_inside_a_c_body_does_not_hide_its_neighbours(self):
        self.assertBlocks("git reset --hard; bash -c \"echo 'x\"", "git reset --hard")


class InnerCommandTests(_GateCase):
    """(b) and (d): programs that run a command they are given."""

    CASES = [
        # (b) `--` ends the shell's options; the next word is still the -c script.
        ("bash -c -- 'git push --force'", "git push --force"),
        ("sh -c -- 'git reset --hard'", "git reset --hard"),
        # PowerShell and cmd.exe.
        ("pwsh -c 'git push --force'", "git push --force"),
        ("pwsh -NoProfile -Command 'git reset --hard'", "git reset --hard"),
        ('powershell -Command "git clean -fdx"', "git clean --force"),
        ("powershell.exe -c 'git stash clear'", "git stash clear"),
        ("cmd /c 'git reset --hard'", "git reset --hard"),
        ('cmd.exe /c "git branch -D topic"', "git branch -D"),
        ("cmd /c 'C:\\Git\\bin\\git.exe reset --hard'", "git reset --hard"),
        # env's split string.
        ("env -S 'git push --force'", "git push --force"),
        ("env --split-string='git reset --hard'", "git reset --hard"),
        # Commands git itself runs.
        ("git submodule foreach 'git reset --hard'", "git reset --hard"),
        ("git submodule foreach --recursive 'git clean -fdx'", "git clean --force"),
        ("git rebase --exec 'git reset --hard' main", "git reset --hard"),
        ("git rebase -x 'git clean -fdx' main", "git clean --force"),
        ("git rebase --exec='git stash clear' main", "git stash clear"),
        # find's -exec argv, up to `;` or `+`.
        ("find . -name x -exec git branch -D {} \\;", "git branch -D"),
        ("find . -execdir git clean -fdx {} +", "git clean --force"),
        # xargs options that take an argument are stepped over.
        ("xargs -n 1 git branch -D", "git branch -D"),
        ("xargs -r -L 1 -P 4 git branch -D", "git branch -D"),
        ("xargs --max-args 1 git branch -D", "git branch -D"),
    ]

    def test_every_inner_destructive_command_blocks(self):
        for command, operation in self.CASES:
            with self.subTest(command=command):
                self.assertBlocks(command, operation)

    def test_an_argv_list_find_exec_is_read(self):
        self.assertBlocks(["find", ".", "-exec", "git", "reset", "--hard", ";"],
                          "git reset --hard", tool="exec_command")

    SAFE = [
        "bash -c -- 'git status'",
        "bash -- script.sh",
        "pwsh -c 'git status'",
        "cmd /c 'git log'",
        "env -S 'git fetch'",
        "git submodule foreach 'git status'",
        "git submodule foreach git pull",
        "git rebase -x 'make test' main",
        "git rebase --exec='git log -1' main",
        "find . -name '*.orig' -exec rm {} \\;",
        "find . -exec echo git reset --hard {} +",
        "xargs -n 1 git branch -d",
    ]

    def test_safe_inner_commands_stay_silent(self):
        for command in self.SAFE:
            with self.subTest(command=command):
                self.assertSilent(command)


class LeaseScopeTests(_GateCase):
    """(c) `--force-with-lease=<ref>` protects that ref alone."""

    def test_forcing_a_ref_the_lease_does_not_name_blocks(self):
        for command in ("git push --force-with-lease=main origin +other",
                        "git push -f --force-with-lease=main origin other",
                        "git push --force-with-lease=main:abc123 origin +other",
                        "git push -f --force-with-lease=main origin main other",
                        "git push -f --force-with-lease=main origin"):
            with self.subTest(command=command):
                self.assertBlocks(command, "git push --force")

    def test_a_lease_on_the_forced_ref_is_silent(self):
        for command in ("git push --force-with-lease=main origin +main",
                        "git push -f --force-with-lease=main origin main",
                        "git push -f --force-with-lease=main:abc123 origin main",
                        "git push --force-with-lease=refs/heads/main origin +HEAD:main",
                        "git push --force-with-lease=main origin +main other"):
            with self.subTest(command=command):
                self.assertSilent(command)

    def test_a_bare_lease_covers_every_ref_pushed(self):
        for command in ("git push --force-with-lease origin +other",
                        "git push -f --force-with-lease origin main other"):
            with self.subTest(command=command):
                self.assertSilent(command)


class FilteringTests(_GateCase):
    """Two-stage filtering: the hook re-checks the event and the tool itself."""

    def test_a_non_shell_tool_is_silent(self):
        for tool in ("Edit", "Write", "Read", "Task", "TaskCreate", "Grep"):
            with self.subTest(tool=tool):
                self.assertSilent("git reset --hard", tool=tool)

    def test_another_event_is_silent(self):
        # PostToolUse is too late to block: the command has already run.
        for event in ("PostToolUse", "SessionStart", "Stop", None):
            with self.subTest(event=event):
                self.assertSilent("git reset --hard", event=event)


class RobustnessTests(unittest.TestCase):
    """Every malformed input exits 0 and prints nothing."""

    def assertSilentRaw(self, text):
        code, out = run_raw(text)
        self.assertEqual(code, 0)
        self.assertEqual(out, "")

    def test_malformed_json_is_silent(self):
        self.assertSilentRaw("{not json")

    def test_empty_stdin_is_silent(self):
        self.assertSilentRaw("")

    def test_a_non_object_payload_is_silent(self):
        for text in ("[]", "42", '"git reset --hard"', "null"):
            with self.subTest(text=text):
                self.assertSilentRaw(text)

    def test_missing_fields_are_silent(self):
        for obj in ({}, {"hook_event_name": "PreToolUse"},
                    {"hook_event_name": "PreToolUse", "tool_name": "Bash"},
                    {"hook_event_name": "PreToolUse", "tool_name": "Bash", "tool_input": {}},
                    {"hook_event_name": "PreToolUse", "tool_name": "Bash",
                     "tool_input": "git reset --hard"}):
            with self.subTest(obj=obj):
                self.assertSilentRaw(json.dumps(obj))

    def test_a_non_string_command_is_silent(self):
        for command in (None, 42, {"cmd": "git reset --hard"}, ["git", 3, "--hard"], True):
            with self.subTest(command=command):
                self.assertSilentRaw(json.dumps(payload(command)))

    def test_a_single_untokenisable_line_fails_open(self):
        # The documented limit: one line that cannot be tokenised is allowed, because a gate
        # that blocks on a guess is worse than none (see the module docstring). The shell
        # would refuse each of these one-line commands itself, so nothing destructive runs.
        # A multi-line command is read line by line instead; see UntokenisableLineTests.
        for command in ("git reset --hard 'unterminated",
                        'git push --force "unterminated',
                        "echo $(git reset --hard"):
            with self.subTest(command=command):
                self.assertSilentRaw(json.dumps(payload(command)))

    def test_deep_nesting_fails_open_rather_than_recursing_without_bound(self):
        command = "$(" * 50 + "git reset --hard" + ")" * 50
        code, out = run(command)
        self.assertEqual(code, 0)
        self.assertEqual(out, "")


if __name__ == "__main__":
    unittest.main()
