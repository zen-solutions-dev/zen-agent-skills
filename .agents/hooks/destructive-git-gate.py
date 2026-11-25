#!/usr/bin/env python3
"""Gate hook: a shell command may not run a destructive git operation unasked.

Shape: **gate**. Fires on `PreToolUse` for a shell tool (`Bash`, `PowerShell`, and the
opencode and Codex shell tools) and blocks, before it runs, a git command that throws away
work or history in a way `git reflog` cannot bring back: a force push without a lease, a
remote branch deletion or a mirror push, `reset --hard`, a forced `clean`, a forced branch
deletion, a `checkout` or `restore` that overwrites working-tree files, dropping or clearing
the stash, expiring the reflog or pruning unreachable objects now, deleting a ref, and
`filter-branch`. Every operation, with its reason and its way out, is one row of `RULES`.

Opt-in, and registered by no committed wiring
---------------------------------------------
It is installed only when asked for: `install.py --with-hooks` places this file and prints
a Claude Code `PreToolUse` registration, which the person adds to their settings by hand.
No wiring this repository commits registers it. Not `.claude/settings.json`: that file
carries one committed reminder by a recorded exception in `AGENTS.md`, and a second
committed hook, or any gate there, is a new decision this file does not make. Not the
Codex `.codex/hooks.json` or the opencode adapter either, since a session in this
repository runs those without anyone choosing them; a person who wants it there adds the
entry themselves (see `.agents/hooks/README.md`).

The rule, and why it is decidable
---------------------------------
"Do not destroy work the person has not agreed to lose" is written in the autonomy lens
(`.agents/rules/autonomy.md`). Whether a command does that is decidable from the command's
argv alone, so this is a gate rather than a reminder. The command is **tokenised, never
matched with a regular expression**: quoting is resolved as a POSIX shell would resolve it,
the text is split at `;`, `&&`, `||`, `|`, `&`, newlines and parentheses, and these inner
commands are examined recursively: the bodies of `$( ... )` and backticks; `bash -c '...'`
(and `sh`, `zsh`, `dash`, `ksh`, with or without `--`) and `eval`; `pwsh` / `powershell`
`-c` / `-Command`; `cmd /c`; `env -S` / `--split-string`; `git submodule foreach` and
`git rebase --exec` / `-x`; and the argv after `find -exec` / `-execdir` up to `;` or `+`.
Within one simple command, leading `NAME=value` assignments and the wrappers `sudo`, `env`,
`command`, `time`, `nohup`, `nice`, `timeout`, `xargs` (with its options that take an
argument) and `exec` are skipped; `git` is recognised by its basename (`/usr/bin/git`,
`git.exe`); git's global options (`-C <path>`, `-c k=v`, `--git-dir`, `--work-tree`,
`--no-pager`, ...) are skipped; and the subcommand's own options are parsed, short clusters
(`-fdx`) and unambiguous long abbreviations (`--forc`) included. So `echo "git reset
--hard"` is an `echo`, and a commit message reading `reset --hard` is a commit. A push lease
is read per ref: `--force-with-lease=<ref>` covers that ref alone, so forcing another ref in
the same push still blocks, while a bare `--force-with-lease` covers everything pushed.

The escape
----------
Every block names the safe form where one exists (`--force-with-lease`, `--dry-run`, commit
or stash first), says the person can run the command themselves in a terminal, and says how
to remove this gate if they disagree with it.

Limits, stated rather than hidden
---------------------------------
* It reads argv. A git alias (`git nuke` defined in git config, or `-c alias.x=...`), a
  script or Makefile target that calls git internally, and a variable holding the
  subcommand (`git $OP`) are not seen, nor is a word made by substitution (`git
  $(echo reset) --hard`): the body of `$( ... )` is examined, its output is not known.
* Only the runners named above are opened. `watch`, `parallel`, `ssh`, `su -c`, `script
  -c`, `make`, `npx` and every other program that runs a command it is given are not
  modelled, nor are `pwsh -EncodedCommand`, `-File`, or `powershell.exe`'s bare positional
  command.
* Nesting is followed to a depth of 8 (`_MAX_DEPTH`). A `$( ... )` nested deeper makes the
  line untokenisable, and a runner nested deeper is not opened.
* The tokeniser is a POSIX shell's. For the `PowerShell` tool it swaps in PowerShell's
  escape character (a backtick, with backslash literal) and otherwise reads POSIX rules.
  `cmd /c` text is split by the same lexer in that mode; cmd.exe quoting (`^` escapes,
  `%VAR%`), fish syntax and PowerShell's own operators are not modelled, which is right
  for plain commands and may miss an unusually quoted one.
* `$( ... )` content that cannot be parsed (an unclosed `$(`, an unbalanced quote inside)
  makes its line untokenisable.
* Text that cannot be tokenised whole is read line by line, because a shell runs the lines
  before a syntax error. A single line that still cannot be tokenised (an unbalanced quote,
  an unclosed `$(`) is allowed: the gate fails open, as every hook here must, rather than
  block on a guess. The same holds for an inner `-c` body.
* A forced push with a lease naming one ref and no refspec blocks, since what is pushed
  then is not in argv.
* It knows the operations in `RULES` and nothing else. `rebase`, `commit --amend` and the
  like are recoverable from the reflog and deliberately not blocked.

Contract
--------
stdin   a JSON object with `hook_event_name`, `tool_name`, and `tool_input.command`
stdout  one JSON object, `{"decision": "block", "reason": ...}`, or nothing
exit    always 0
"""
import json
import shlex
import sys
from pathlib import PureWindowsPath

SHELL_TOOLS = {
    "Bash",          # Claude Code
    "PowerShell",    # Claude Code on Windows
    "bash",          # opencode
    "shell",         # Codex
    "local_shell",   # Codex
    "exec_command",  # Codex
}

_OPT_OUT = ("If you disagree with this gate, remove the destructive-git-gate.py entry from "
            "your hook settings; it is opt-in.")

# The one data table. key -> (the operation as a person would type it, why it is blocked,
# the way out). Detectors below return a key; nothing else carries a message.
RULES = {
    "push-force": (
        "git push --force",
        "overwrites the remote branch and can discard commits someone else pushed",
        "Use --force-with-lease (it refuses if the remote moved since you fetched), or run "
        "it yourself in a terminal"),
    "push-delete": (
        "git push --delete",
        "deletes a branch or tag on the remote, where no local reflog can recover it",
        "Run it yourself in a terminal if the remote ref really should go"),
    "push-mirror": (
        "git push --mirror",
        "makes the remote match this repository exactly, deleting every remote ref this "
        "clone does not have",
        "Push the branches you mean by name, or run it yourself in a terminal"),
    "push-prune": (
        "git push --prune",
        "deletes every remote branch that has no local counterpart",
        "Delete the remote branches you mean by name, or run it yourself in a terminal"),
    "reset-hard": (
        "git reset --hard",
        "discards every uncommitted change in the index and working tree, which no reflog "
        "records",
        "Commit or stash first (git stash), use git reset --keep, or run it yourself in a "
        "terminal"),
    "clean-force": (
        "git clean --force",
        "deletes untracked files, which git never stored and cannot bring back",
        "Run git clean --dry-run first to see what would go, or run it yourself in a "
        "terminal"),
    "branch-force-delete": (
        "git branch -D",
        "deletes a branch even when its commits are merged nowhere else",
        "Use git branch -d, which refuses an unmerged branch, or run it yourself in a "
        "terminal"),
    "checkout-force": (
        "git checkout --force",
        "switches branches by throwing away local changes",
        "Commit or stash first (git stash), or run it yourself in a terminal"),
    "checkout-paths": (
        "git checkout -- <path>",
        "overwrites working-tree files with another version, discarding uncommitted edits",
        "Commit or stash first (git stash), or run it yourself in a terminal"),
    "switch-discard": (
        "git switch --discard-changes",
        "switches branches by throwing away local changes",
        "Commit or stash first (git stash), or run it yourself in a terminal"),
    "restore-worktree": (
        "git restore <path>",
        "overwrites working-tree files, discarding uncommitted edits",
        "Commit or stash first (git stash); git restore --staged alone only unstages. Or "
        "run it yourself in a terminal"),
    "stash-drop": (
        "git stash drop",
        "deletes a stash entry",
        "Apply it first (git stash apply), or run it yourself in a terminal"),
    "stash-clear": (
        "git stash clear",
        "deletes every stash entry",
        "Apply the ones you need first (git stash apply), or run it yourself in a terminal"),
    "reflog-expire-now": (
        "git reflog expire --expire=now",
        "erases the reflog, which is how lost commits are found again",
        "Leave the default expiry, or run it yourself in a terminal"),
    "gc-prune-now": (
        "git gc --prune=now",
        "deletes unreachable objects immediately instead of after the grace period",
        "Run git gc without --prune=now, or run it yourself in a terminal"),
    "prune": (
        "git prune",
        "deletes unreachable objects that a reflog entry may still need",
        "Run git prune --dry-run first, or run it yourself in a terminal"),
    "update-ref-delete": (
        "git update-ref -d",
        "deletes a ref directly, bypassing the safety checks of branch and tag",
        "Use git branch -d or git tag -d, or run it yourself in a terminal"),
    "filter-branch": (
        "git filter-branch",
        "rewrites history across every named ref",
        "Run it yourself in a terminal, on a fresh clone"),
    "worktree-remove-force": (
        "git worktree remove --force",
        "removes a worktree along with its uncommitted and untracked files",
        "Commit or stash in that worktree first, or run it yourself in a terminal"),
}


def reason_for(key):
    operation, why, way_out = RULES[key]
    return (f"Destructive-git gate: blocked `{operation}`: it {why}. {way_out}. {_OPT_OUT}")


# --------------------------------------------------------------------------------------
# Tokenising: shell text -> every simple command's argv, nested ones included.
# --------------------------------------------------------------------------------------

class _Untokenisable(ValueError):
    """The text is not a complete shell command (unbalanced quote or substitution)."""


_SEPARATORS = ";&|"
_MAX_DEPTH = 8


def _grow(word, chars):
    """Append to the word being built, in place, starting one if none is open."""
    if word is None:
        word = []
    word.extend(chars)
    return word


class _Lexer:
    """A small POSIX-shell lexer that keeps quoting and operators apart.

    `shlex` with `punctuation_chars` cannot tell a quoted `";"` from a real separator, and
    does not descend into `$( ... )` or backticks, so this does both by hand. It produces
    argv lists only; it never evaluates anything.
    """

    def __init__(self, text, depth=0, powershell=False):
        self.s = text
        self.i = 0
        self.depth = depth
        self.commands = []
        # PowerShell escapes with a backtick and treats a backslash as an ordinary
        # character, so `C:\Git\bin\git.exe` survives. Everything else is read as POSIX.
        self.escape = "`" if powershell else "\\"
        self.powershell = powershell

    def run(self):
        self._sequence(None)
        return self.commands

    def _peek(self, offset=0):
        j = self.i + offset
        return self.s[j] if j < len(self.s) else ""

    def _nested(self, closer):
        """Lex a `$( ... )` or backtick body in place, adding its commands to ours."""
        if self.depth >= _MAX_DEPTH:
            raise _Untokenisable("nesting too deep")
        inner = _Lexer(self.s, self.depth + 1, self.powershell)
        inner.i = self.i
        inner._sequence(closer)
        self.commands.extend(inner.commands)
        self.i = inner.i

    def _sequence(self, closer):
        s = self.s
        argv = []
        word = None          # list of characters, or None between words
        skip_word = False    # the next word is a redirection target, not an argument
        heredoc_next = None  # None, or the strip-tabs flag of a pending `<<` delimiter
        heredocs = []        # (delimiter, strip_tabs) waiting for the next newline
        paren_depth = 0

        def finish_word():
            nonlocal word, skip_word, heredoc_next
            if word is None:
                return
            text = "".join(word)
            word = None
            if heredoc_next is not None:
                heredocs.append((text, heredoc_next))
                heredoc_next = None
            elif skip_word:
                skip_word = False
            else:
                argv.append(text)

        def end_command():
            nonlocal argv, skip_word
            finish_word()
            skip_word = False
            if argv:
                self.commands.append(argv)
            argv = []

        while self.i < len(s):
            c = s[self.i]
            if closer == "`" and c == "`":
                end_command()
                self.i += 1
                return
            if c == ")":
                self.i += 1
                if paren_depth == 0 and closer == ")":
                    end_command()
                    return
                paren_depth = max(0, paren_depth - 1)
                end_command()
                continue
            if c in " \t\r":
                finish_word()
                self.i += 1
                continue
            if c == "\n":
                end_command()
                self.i += 1
                if heredocs:
                    self._skip_heredocs(heredocs)
                    heredocs = []
                continue
            if c == "#" and word is None:
                while self.i < len(s) and s[self.i] != "\n":
                    self.i += 1
                continue
            if c == self.escape:
                nxt = self._peek(1)
                if nxt == "\n":
                    self.i += 2
                    continue
                if nxt == "":
                    self.i += 1
                    continue
                word = _grow(word, nxt)
                self.i += 2
                continue
            if c == "'":
                end = s.find("'", self.i + 1)
                if end < 0:
                    raise _Untokenisable("unbalanced single quote")
                word = _grow(word, s[self.i + 1:end])
                self.i = end + 1
                continue
            if c == '"':
                word = _grow(word, self._double_quoted())
                continue
            if c == "$" and self._peek(1) == "(":
                self.i += 2
                self._nested(")")
                word = _grow(word, "$(...)")
                continue
            if c == "$" and self._peek(1) == "'" and not self.powershell:
                word = _grow(word, self._ansi_c_quoted())
                continue
            if c == "`" and not self.powershell:
                self.i += 1
                self._nested("`")
                word = _grow(word, "`...`")
                continue
            if c == "(":
                end_command()
                paren_depth += 1
                self.i += 1
                continue
            if c in "<>" or (c == "&" and self._peek(1) == ">"):
                if word is not None and "".join(word).isdigit():
                    word = None  # a file-descriptor number such as the 2 in 2>
                else:
                    finish_word()
                if c == "<" and self._peek(1) == "<" and self._peek(2) != "<":
                    self.i += 2
                    strip = self._peek() == "-"
                    if strip:
                        self.i += 1
                    heredoc_next = strip
                    continue
                self.i += 1
                while self._peek() in ("<", ">", "&", "|"):
                    self.i += 1
                if self._peek() != "(":
                    skip_word = True
                continue
            if c in _SEPARATORS:
                end_command()
                self.i += 1
                while self._peek() in ("&", "|", ";"):
                    self.i += 1
                continue
            word = _grow(word, c)
            self.i += 1

        if closer is not None:
            raise _Untokenisable(f"unclosed {closer!r}")
        end_command()

    def _double_quoted(self):
        s = self.s
        out = []
        self.i += 1
        while self.i < len(s):
            c = s[self.i]
            if c == '"':
                self.i += 1
                return out
            if c == self.escape and (self.powershell
                                     or self._peek(1) in ('"', "\\", "$", "`", "\n")):
                if self._peek(1) != "\n":
                    out.append(self._peek(1))
                self.i += 2
                continue
            if c == "$" and self._peek(1) == "(":
                self.i += 2
                self._nested(")")
                out.extend("$(...)")
                continue
            if c == "`" and not self.powershell:
                self.i += 1
                self._nested("`")
                out.extend("`...`")
                continue
            out.append(c)
            self.i += 1
        raise _Untokenisable("unbalanced double quote")

    def _ansi_c_quoted(self):
        s = self.s
        out = []
        self.i += 2
        while self.i < len(s):
            c = s[self.i]
            if c == "'":
                self.i += 1
                return out
            if c == "\\" and self.i + 1 < len(s):
                out.append(s[self.i + 1])
                self.i += 2
                continue
            out.append(c)
            self.i += 1
        raise _Untokenisable("unbalanced $' quote")

    def _skip_heredocs(self, heredocs):
        """Step over here-document bodies: they are data, not commands."""
        s = self.s
        for delimiter, strip_tabs in heredocs:
            while self.i < len(s):
                end = s.find("\n", self.i)
                line = s[self.i:] if end < 0 else s[self.i:end]
                self.i = len(s) if end < 0 else end + 1
                if (line.lstrip("\t") if strip_tabs else line) == delimiter:
                    break


def split_commands(text, depth=0, powershell=False):
    """Every simple command's argv in `text`, including nested and `-c` bodies.

    Raises `_Untokenisable` when `text` itself cannot be tokenised. An inner body that
    cannot be tokenised is read leniently instead (see `_split_lenient`), so it never
    hides the commands around it.
    """
    found = []
    for argv in _Lexer(text, depth, powershell).run():
        _expand(argv, depth, found)
    return found


def _split_lenient(text, depth=0, powershell=False):
    """`split_commands`, but text that cannot be tokenised whole is read line by line.

    A shell runs a script one line at a time, so `git reset --hard` on the first line runs
    before an unbalanced quote on the second is ever seen. Each line is classified on its
    own; a single line that still cannot be tokenised contributes nothing (fail open).
    """
    try:
        return split_commands(text, depth, powershell)
    except _Untokenisable:
        pass
    found = []
    lines = text.splitlines()
    if len(lines) < 2:
        return found
    for line in lines:
        try:
            found.extend(split_commands(line, depth, powershell))
        except _Untokenisable:
            continue
    return found


def _expand(argv, depth, found):
    """Add argv, then every command it runs inside itself, to `found`."""
    found.append(argv)
    if depth >= _MAX_DEPTH:
        return
    for inner in _inner_commands(argv):
        if isinstance(inner, list):
            _expand(inner, depth + 1, found)
        else:
            text, powershell = inner
            found.extend(_split_lenient(text, depth + 1, powershell))


# --------------------------------------------------------------------------------------
# One simple command: strip wrappers, find git, find the subcommand.
# --------------------------------------------------------------------------------------

_KEYWORDS = {"{", "}", "!", "if", "then", "else", "elif", "fi", "do", "done", "while",
             "until", "case", "esac", "in"}
# Wrapper -> the options of it that take a separate argument.
_WRAPPERS = {
    "sudo": {"-u", "-g", "-C", "-D", "-h", "-p", "-r", "-t", "-U", "-T"},
    "doas": {"-u", "-C"},
    "env": {"-u", "-C", "-S", "--unset", "--chdir", "--split-string"},
    "command": set(),
    "builtin": set(),
    "exec": {"-a"},
    "time": {"-f", "-o", "--format", "--output"},
    "nohup": set(),
    "nice": {"-n", "--adjustment"},
    "ionice": {"-c", "-n", "-p"},
    "stdbuf": {"-i", "-o", "-e"},
    "xargs": {"-n", "-L", "-P", "-I", "-d", "-E", "-s", "-a", "--max-args", "--max-procs",
              "--delimiter", "--max-chars", "--arg-file", "--process-slot-var"},
    "timeout": {"-s", "-k", "--signal", "--kill-after"},
}
# Wrappers that take one positional before the command they run.
_WRAPPER_POSITIONAL = {"timeout": 1}
_SHELLS = {"bash", "sh", "zsh", "dash", "ksh", "mksh", "ash", "busybox"}


def _basename(token):
    name = PureWindowsPath(token).name.lower()  # splits on both / and \
    return name[:-4] if name.endswith(".exe") else name


def _is_assignment(token):
    name, eq, _ = token.partition("=")
    return bool(eq) and name.replace("_", "a").isalnum() and not name[0].isdigit()


def _command_words(argv, env_split=None):
    """argv with leading assignments, keywords and wrappers removed.

    When `env_split` is a list, the text of each `env -S` / `--split-string` is appended
    to it: that text is itself a command line, which `_inner_commands` reads.
    """
    i = 0
    while i < len(argv):
        token = argv[i]
        if token in _KEYWORDS or _is_assignment(token):
            i += 1
            continue
        name = _basename(token)
        if name in _WRAPPERS:
            takes_arg = _WRAPPERS[name]
            i += 1
            while i < len(argv) and (argv[i].startswith("-") or
                                     (name == "env" and _is_assignment(argv[i]))):
                if argv[i] == "--":
                    i += 1
                    break
                if name == "env" and env_split is not None:
                    token = argv[i]
                    if token in ("-S", "--split-string") and i + 1 < len(argv):
                        env_split.append(argv[i + 1])
                    elif token.startswith("--split-string="):
                        env_split.append(token.partition("=")[2])
                    elif token.startswith("-S") and len(token) > 2:
                        env_split.append(token[2:])
                if argv[i] in takes_arg:
                    i += 1
                i += 1
            i += _WRAPPER_POSITIONAL.get(name, 0)
            continue
        return argv[i:]
    return []


def _shell_script(name, rest):
    """The script text of `bash -c '...'` (and the other POSIX shells), or None."""
    if name == "busybox" and rest and _basename(rest[0]) in _SHELLS:
        rest = rest[1:]
    saw_c = False
    k = 0
    while k < len(rest):
        token = rest[k]
        if token == "--":
            k += 1
            break
        if not token.startswith(("-", "+")):
            break
        if token.startswith("-") and not token.startswith("--") and "c" in token[1:]:
            saw_c = True
        k += 2 if token in ("-o", "+o", "-O", "+O") else 1
    if saw_c and k < len(rest):
        return rest[k]
    return None


def _powershell_script(rest):
    """The text after `-c` / `-Command` (any unambiguous abbreviation), or None."""
    for k, token in enumerate(rest):
        flag = token.lower().lstrip("-/")
        if token[:1] in "-/" and (flag in ("c", "cwa", "commandwithargs")
                                  or (len(flag) >= 3 and "command".startswith(flag))):
            return " ".join(rest[k + 1:]) or None
    return None


def _cmd_script(rest):
    """The text after cmd.exe's `/c` or `/k`, or None. Its quoting is not modelled."""
    for k, token in enumerate(rest):
        if not token.startswith("/"):
            return None
        if token[:2].lower() in ("/c", "/k"):
            return " ".join([token[2:]] + rest[k + 1:]).strip() or None
    return None


def _find_exec(rest):
    """Each argv `find` runs through `-exec`, `-execdir`, `-ok` or `-okdir`."""
    found = []
    k = 0
    while k < len(rest):
        if rest[k] in ("-exec", "-execdir", "-ok", "-okdir"):
            end = k + 1
            while end < len(rest) and rest[end] not in (";", "+"):
                end += 1
            if end > k + 1:
                found.append(rest[k + 1:end])
            k = end
        k += 1
    return found


def _git_scripts(subcommand, args):
    """The shell text git itself runs: `submodule foreach` and `rebase --exec`."""
    found = []
    if subcommand == "submodule":
        k = 0
        while k < len(args) and args[k].startswith("-"):
            k += 1
        if k < len(args) and args[k] == "foreach":
            rest = args[k + 1:]
            while rest and rest[0] in ("--recursive", "-q", "--quiet", "--"):
                rest = rest[1:]
            if len(rest) == 1:
                found.append(rest[0])
            elif rest:
                found.append(" ".join(shlex.quote(t) for t in rest))
    elif subcommand == "rebase":
        k = 0
        while k < len(args):
            token = args[k]
            if token in ("-x", "--exec") and k + 1 < len(args):
                found.append(args[k + 1])
                k += 1
            elif token.startswith("--exec="):
                found.append(token.partition("=")[2])
            elif token.startswith("-x") and len(token) > 2:
                found.append(token[2:])
            elif token == "--":
                break
            k += 1
    return found


def _inner_commands(argv):
    """What argv runs inside itself: shell text as (text, powershell), or an argv list."""
    env_split = []
    words = _command_words(argv, env_split)
    if env_split:
        # `env -S 'git push' --force` runs the split text with the remaining words.
        tail = " ".join(shlex.quote(w) for w in words)
        return [((text + " " + tail).strip(), False) for text in env_split]
    if not words:
        return []
    name = _basename(words[0])
    rest = words[1:]
    if name == "eval":
        return [(" ".join(rest), False)] if rest else []
    if name in _SHELLS:
        script = _shell_script(name, rest)
        return [(script, False)] if script is not None else []
    if name in ("pwsh", "powershell"):
        script = _powershell_script(rest)
        return [(script, True)] if script is not None else []
    if name == "cmd":
        # The same lexer, in its PowerShell mode so `C:\Git\git.exe` keeps its
        # backslashes; cmd.exe's own `^` escapes and `%VAR%` are not modelled.
        script = _cmd_script(rest)
        return [(script, True)] if script is not None else []
    if name == "find":
        return _find_exec(rest)
    invocation = _git_invocation(argv)
    if invocation is not None:
        return [(text, False) for text in _git_scripts(*invocation)]
    return []


# Global options that consume the next word when not written with `=`.
_GIT_GLOBAL_WITH_ARG = {"-C", "-c", "--git-dir", "--work-tree", "--namespace",
                        "--super-prefix", "--config-env", "--exec-path", "--list-cmds"}
_GIT_GLOBAL_EQ_ONLY = {"--exec-path", "--list-cmds"}


def _git_invocation(argv):
    """(subcommand, its args) if argv runs git, else None."""
    words = _command_words(argv)
    if not words or _basename(words[0]) != "git":
        return None
    i = 1
    while i < len(words):
        token = words[i]
        if token in ("-h", "--help", "--version", "-v"):
            return None
        if token.startswith("-"):
            if token in _GIT_GLOBAL_WITH_ARG and token not in _GIT_GLOBAL_EQ_ONLY:
                i += 2
            else:
                i += 1
            continue
        return token, words[i + 1:]
    return None


# --------------------------------------------------------------------------------------
# Option parsing for one subcommand.
# --------------------------------------------------------------------------------------

class _Options:
    """Parsed options: `short` letters, `long` names in order, positionals, `--` paths."""

    def __init__(self):
        self.short = []
        self.long = []          # (name, value or None), in command-line order
        self.positionals = []
        self.after_dashdash = []
        self.saw_dashdash = False

    def has_short(self, *letters):
        return any(letter in self.short for letter in letters)

    def has_long(self, *names):
        return any(name in names for name, _ in self.long)

    def values(self, name):
        return [value for n, value in self.long if n == name]


def _resolve_long(name, known):
    """git accepts any unambiguous prefix of a long option, so `--forc` is `--force`."""
    if name in known or not known:
        return name
    matches = [k for k in known if k.startswith(name)]
    return matches[0] if len(matches) == 1 else name


def _parse(args, short_with_arg="", long_known=(), long_with_arg=()):
    opts = _Options()
    known = set(long_known) | set(long_with_arg)
    i = 0
    while i < len(args):
        token = args[i]
        i += 1
        if opts.saw_dashdash:
            opts.after_dashdash.append(token)
        elif token == "--":
            opts.saw_dashdash = True
        elif token.startswith("--"):
            name, eq, value = token[2:].partition("=")
            name = _resolve_long(name, known)
            if not eq and name in long_with_arg and i < len(args):
                value, i = args[i], i + 1
            opts.long.append((name, value if (eq or name in long_with_arg) else None))
        elif token.startswith("-") and len(token) > 1:
            letters = token[1:]
            for k, letter in enumerate(letters):
                opts.short.append(letter)
                if letter in short_with_arg:
                    if k == len(letters) - 1:
                        i += 1  # the argument is the next word
                    break       # otherwise the rest of the cluster is the argument
        else:
            opts.positionals.append(token)
    return opts


# --------------------------------------------------------------------------------------
# Detectors: one per subcommand, each returning a RULES key or None.
# --------------------------------------------------------------------------------------

_WHOLE_TREE = {".", "./", ":/", ":/.", ":", "*"}


def _push(args):
    o = _parse(args, short_with_arg="o",
               long_known=("force", "force-with-lease", "no-force-with-lease",
                           "force-if-includes", "no-force-if-includes", "mirror", "delete",
                           "prune", "dry-run", "all", "branches", "tags", "follow-tags",
                           "set-upstream", "porcelain", "verbose", "quiet", "progress",
                           "no-verify", "verify", "atomic", "signed", "thin", "no-thin",
                           "ipv4", "ipv6", "no-force"),
               long_with_arg=("repo", "push-option", "receive-pack", "exec",
                              "recurse-submodules"))
    if o.has_short("n") or o.has_long("dry-run"):
        return None
    if o.has_long("mirror"):
        return "push-mirror"
    refspecs = (o.positionals + o.after_dashdash)[1:]  # the first is the remote
    if o.has_short("d") or o.has_long("delete") or any(r.startswith(":") and len(r) > 1
                                                      for r in refspecs):
        return "push-delete"
    if o.has_long("prune"):
        return "push-prune"
    # A bare --force-with-lease protects every ref pushed; --force-with-lease=<ref> (or
    # <ref>:<expect>) protects that ref alone; --no-force-with-lease cancels all of them.
    lease_all = False
    leased = set()
    for name, value in o.long:
        if name == "force-with-lease":
            ref = (value or "").partition(":")[0]
            if ref:
                leased.add(_short_ref(ref))
            else:
                lease_all = True
        elif name == "no-force-with-lease":
            lease_all = False
            leased = set()
    force_all = o.has_short("f") or o.has_long("force", "force-if-includes")
    forced = refspecs if force_all else [r for r in refspecs if r.startswith("+")]
    if lease_all or not (forced or force_all):
        return None
    if force_all and not refspecs:
        # What gets pushed is not in argv, so a named lease cannot be shown to cover it.
        return "push-force"
    for refspec in forced:
        if _short_ref(_destination(refspec)) not in leased:
            return "push-force"
    return None


def _destination(refspec):
    """The remote ref a refspec updates: `+src:dst` -> dst, `+name` -> name."""
    refspec = refspec[1:] if refspec.startswith("+") else refspec
    src, colon, dst = refspec.partition(":")
    return dst if colon else src


def _short_ref(ref):
    for prefix in ("refs/heads/", "heads/"):
        if ref.startswith(prefix):
            return ref[len(prefix):]
    return ref


def _reset(args):
    o = _parse(args, long_known=("hard", "soft", "mixed", "merge", "keep", "quiet", "patch",
                                 "help", "recurse-submodules", "no-refresh", "refresh",
                                 "intent-to-add", "pathspec-from-file",
                                 "pathspec-file-nul"))
    return "reset-hard" if o.has_long("hard") else None


def _clean(args):
    o = _parse(args, short_with_arg="e",
               long_known=("force", "dry-run", "quiet", "interactive", "exclude"),
               long_with_arg=("exclude",))
    if o.has_short("n", "i") or o.has_long("dry-run", "interactive"):
        return None
    if o.has_short("f") or o.has_long("force"):
        return "clean-force"
    return None


def _branch(args):
    o = _parse(args, short_with_arg="u",
               long_known=("delete", "force", "move", "copy", "list", "remotes", "all",
                           "verbose", "quiet", "track", "no-track", "show-current",
                           "edit-description", "create-reflog", "ignore-case",
                           "omit-empty", "abbrev", "no-abbrev", "column", "no-column",
                           "color", "no-color", "merged", "no-merged", "contains",
                           "no-contains", "points-at", "sort", "format",
                           "set-upstream-to", "unset-upstream", "recurse-submodules"),
               long_with_arg=("set-upstream-to", "contains", "no-contains", "merged",
                              "no-merged", "points-at", "sort", "format"))
    if o.has_short("D"):
        return "branch-force-delete"
    deleting = o.has_short("d") or o.has_long("delete")
    if deleting and (o.has_short("f") or o.has_long("force")):
        return "branch-force-delete"
    return None


def _checkout(args):
    o = _parse(args, short_with_arg="bB",
               long_known=("force", "quiet", "progress", "no-progress", "ours", "theirs",
                           "track", "no-track", "guess", "no-guess", "detach", "orphan",
                           "ignore-skip-worktree-bits", "merge", "conflict", "patch",
                           "ignore-other-worktrees", "overwrite-ignore",
                           "no-overwrite-ignore", "recurse-submodules",
                           "no-recurse-submodules", "overlay", "no-overlay",
                           "pathspec-from-file", "pathspec-file-nul"),
               long_with_arg=("orphan",))
    if o.has_short("f") or o.has_long("force"):
        return "checkout-force"
    if o.after_dashdash or o.has_long("pathspec-from-file"):
        return "checkout-paths"
    if any(p in _WHOLE_TREE for p in o.positionals):
        return "checkout-paths"
    return None


def _switch(args):
    o = _parse(args, short_with_arg="cC",
               long_known=("discard-changes", "force", "create", "force-create", "detach",
                           "guess", "no-guess", "quiet", "progress", "no-progress", "merge",
                           "conflict", "track", "no-track", "orphan",
                           "ignore-other-worktrees", "recurse-submodules",
                           "no-recurse-submodules"),
               long_with_arg=("create", "force-create", "orphan"))
    if o.has_short("f") or o.has_long("discard-changes", "force"):
        return "switch-discard"
    return None


def _restore(args):
    o = _parse(args, short_with_arg="s",
               long_known=("source", "staged", "worktree", "patch", "quiet", "progress",
                           "no-progress", "ours", "theirs", "merge", "conflict",
                           "ignore-unmerged", "ignore-skip-worktree-bits",
                           "recurse-submodules", "no-recurse-submodules", "overlay",
                           "no-overlay", "pathspec-from-file", "pathspec-file-nul"),
               long_with_arg=("source",))
    staged = o.has_short("S") or o.has_long("staged")
    worktree = o.has_short("W") or o.has_long("worktree")
    if staged and not worktree:
        return None
    if o.positionals or o.after_dashdash or o.has_long("pathspec-from-file"):
        return "restore-worktree"
    return None


def _stash(args):
    o = _parse(args)
    action = o.positionals[0] if o.positionals else ""
    return {"drop": "stash-drop", "clear": "stash-clear"}.get(action)


def _is_now(value):
    value = (value or "").strip().lower()
    return value in ("now", "all") or value.startswith("0")


def _reflog(args):
    if not args or args[0] != "expire":
        return None
    o = _parse(args[1:], long_known=("expire", "expire-unreachable", "all", "rewrite",
                                     "updateref", "stale-fix", "dry-run", "verbose",
                                     "single-worktree"),
               long_with_arg=("expire", "expire-unreachable"))
    if o.has_short("n") or o.has_long("dry-run"):
        return None
    values = o.values("expire") + o.values("expire-unreachable")
    return "reflog-expire-now" if any(_is_now(v) for v in values) else None


def _gc(args):
    o = _parse(args, long_known=("prune", "no-prune", "aggressive", "auto", "quiet",
                                 "force", "keep-largest-pack", "cruft", "no-cruft",
                                 "max-cruft-size", "detach", "no-detach"))
    prune = None
    for name, value in o.long:
        if name == "prune":
            prune = value
        elif name == "no-prune":
            prune = None
    return "gc-prune-now" if _is_now(prune) else None


def _prune(args):
    o = _parse(args, long_known=("dry-run", "verbose", "progress", "expire"),
               long_with_arg=("expire",))
    if o.has_short("n") or o.has_long("dry-run"):
        return None
    return "prune"


def _update_ref(args):
    o = _parse(args, short_with_arg="m")
    return "update-ref-delete" if o.has_short("d") else None


def _worktree(args):
    if not args or args[0] != "remove":
        return None
    o = _parse(args[1:], long_known=("force",))
    return "worktree-remove-force" if o.has_short("f") or o.has_long("force") else None


_DETECTORS = {
    "push": _push,
    "reset": _reset,
    "clean": _clean,
    "branch": _branch,
    "checkout": _checkout,
    "switch": _switch,
    "restore": _restore,
    "stash": _stash,
    "reflog": _reflog,
    "gc": _gc,
    "prune": _prune,
    "update-ref": _update_ref,
    "filter-branch": lambda args: "filter-branch",
    "worktree": _worktree,
}


def classify(command, powershell=False):
    """The RULES key of the first destructive git operation in `command`, or None.

    `command` is shell text, or an argv list as some harnesses send it. Text that cannot be
    tokenised whole is read line by line; a single line that cannot be tokenised is
    allowed: the gate fails open rather than block on a guess.
    """
    if isinstance(command, list):
        if not all(isinstance(t, str) for t in command):
            return None
        argvs = []
        _expand(command, 0, argvs)
    else:
        argvs = _split_lenient(command, powershell=powershell)
    for argv in argvs:
        invocation = _git_invocation(argv)
        if invocation is None:
            continue
        subcommand, args = invocation
        detector = _DETECTORS.get(subcommand)
        key = detector(args) if detector else None
        if key:
            return key
    return None


def evaluate(payload):
    """Return a block object for this payload, or None to stay silent."""
    if not isinstance(payload, dict):
        return None
    if payload.get("hook_event_name") != "PreToolUse":
        return None
    if payload.get("tool_name") not in SHELL_TOOLS:
        return None
    tool_input = payload.get("tool_input")
    command = tool_input.get("command") if isinstance(tool_input, dict) else None
    if not isinstance(command, (str, list)):
        return None
    key = classify(command, powershell=payload.get("tool_name") == "PowerShell")
    if key is None:
        return None
    return {"decision": "block", "reason": reason_for(key)}


def main(stdin=None, stdout=None) -> int:
    """Read one payload, emit at most one object. Streams are injectable for testing."""
    stdin = sys.stdin if stdin is None else stdin
    stdout = sys.stdout if stdout is None else stdout
    try:
        payload = json.load(stdin)
    except Exception:
        return 0
    try:
        out = evaluate(payload)
        if out is not None:
            stdout.write(json.dumps(out))
    except Exception:
        # A guardrail that breaks a session because it could not parse a command is worse
        # than no guardrail. Fail open, always.
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
