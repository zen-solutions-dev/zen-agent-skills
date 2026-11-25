"""The wizard library: the shared behaviour of every runbook script doc-author writes.

A runbook script walks a person through steps only they can take (a dashboard to click through, a
credential to create, a one-off cutover). Every such script behaves alike because every one imports
this file: numbered stages, prompts that remember earlier answers, secrets read without echo, a
confirmation before anything irreversible, steps that are skipped when already done, and a dry walk
that performs nothing.

Copy this file unchanged beside the runbook script and import it; never hand-edit the copy, so a
fix here reaches every wizard by copying the file again. Standard library only, on Windows, macOS
and Linux alike.

    import sys
    from wizard import Wizard

    def get_token(w):
        w.open_url("https://example.com/settings/tokens")
        w.step("Create a token with read access, then copy it.")
        token = w.ask_secret("EXAMPLE_TOKEN", "Paste the token")
        w.write_env("EXAMPLE_TOKEN", token)

    def publish(w):
        w.irreversible("publish the release", lambda: w.command(["gh", "release", "create", "v1"]))

    if __name__ == "__main__":
        w = Wizard("Example setup", "Connects this repository to Example.", dry_run="--dry-run" in sys.argv)
        sys.exit(w.run([("Create a token", get_token), ("Publish", publish)]))

A dry walk: run the script with `--dry-run`, answers piped to standard input, and the `BROWSER`
environment variable set to a command that does nothing. Every stage prints in order, every
confirmation is asked, and nothing is opened, written, run or recorded.

Adapted from the bash `template.sh` of Matt Pocock's `wizard` skill; the provenance block is in
doc-author's SKILL.md.
"""
import getpass
import json
import os
import subprocess
import sys
import webbrowser
from pathlib import Path


class WizardStopped(Exception):
    """Raised to stop the run: a declined confirmation, or input that ended."""


class Wizard:
    def __init__(self, title, purpose, env_file=".env", state_file=".wizard-state.json",
                 dry_run=False, stdin=None, stdout=None, read_secret=None):
        self.title, self.purpose = title, purpose
        self.env_file, self.state_file = Path(env_file), Path(state_file)
        self.dry_run = bool(dry_run) or os.environ.get("WIZARD_DRY_RUN") == "1"
        self.stdin = stdin or sys.stdin
        self.stdout = stdout or sys.stdout
        self._read_secret = read_secret or (lambda prompt: getpass.getpass(prompt))
        self.done, self.skipped = [], []
        self._stage, self._total = 0, 0

    # Output -------------------------------------------------------------------------------

    def _print(self, text=""):
        print(text, file=self.stdout, flush=True)

    def banner(self):
        self._print(f"== {self.title} ==")
        self._print(self.purpose)
        if self.dry_run:
            self._print("Dry walk: nothing will be opened, written, run or recorded.")

    def stage(self, name):
        self._stage += 1
        left = self._total - self._stage
        self._print()
        self._print(f"-- Stage {self._stage} of {self._total}: {name} ({left} left after this) --")

    def say(self, text):
        self._print(f"  {text}")

    def step(self, text):
        self._print(f"  * {text}")

    def note(self, text):
        self._print(f"  ({text})")

    def warn(self, text):
        self._print(f"  ! {text}")

    # Input --------------------------------------------------------------------------------

    def _readline(self, prompt):
        self.stdout.write(prompt)
        self.stdout.flush()
        line = self.stdin.readline()
        if not line:
            raise WizardStopped("input ended before an answer was given")
        if not getattr(self.stdin, "isatty", lambda: False)():
            self.stdout.write("\n")  # a piped answer is not echoed, so end the prompt's line
        return line.rstrip("\r\n")

    def pause(self, message="Press Enter when that is done."):
        self._readline(f"  {message} ")

    def confirm(self, question):
        """A yes-or-no gate whose default is no."""
        return self._readline(f"  {question} [y/N] ").strip().lower() in ("y", "yes")

    def ask(self, key, prompt):
        """A visible answer. On a re-run the value already in the env file is the default."""
        existing = self.existing(key)
        hint = f" [{existing}]" if existing else ""
        while True:
            answer = self._readline(f"  {prompt}{hint}: ").strip()
            if answer or existing:
                return answer or existing
            self.warn("An answer is needed.")

    def ask_secret(self, key, prompt):
        """A hidden answer, never printed. Enter keeps a value already in the env file."""
        existing = self.existing(key)
        hint = " (Enter keeps the saved value)" if existing else ""
        while True:
            try:
                answer = self._read_secret(f"  {prompt}{hint}: ")
            except EOFError:
                raise WizardStopped("input ended before an answer was given") from None
            if answer or existing:
                return answer or existing
            self.warn("An answer is needed.")

    # Effects ------------------------------------------------------------------------------

    def open_url(self, url):
        self.say(f"Open: {url}")
        if not self.dry_run:
            webbrowser.open(url)

    def existing(self, key):
        """The value of `key` in the env file, unquoted, or None."""
        if not self.env_file.is_file():
            return None
        for line in self.env_file.read_text(encoding="utf-8").splitlines():
            name, sep, value = line.partition("=")
            if sep and name.strip() == key:
                value = value.strip()
                if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
                    value = value[1:-1].replace("'\\''", "'")
                return value
        return None

    def write_env(self, key, value):
        """Upsert KEY='VALUE' in the env file. Idempotent; never prints the value.

        A value holding a line break is refused: it would end its line and inject another key.
        A line break is anything `str.splitlines` splits on, since `existing` reads the file
        back that way: \r, \n, \v, \f, \x1c, \x1d, \x1e, \x85, \u2028 and \u2029.
        A new env file is created private (0600 on POSIX) before any value is written to it.
        """
        if value and value.splitlines() != [value]:
            raise WizardStopped(f"the value for {key} holds a line break, so it was not saved")
        if self.dry_run:
            self.note(f"would write {key} to {self.env_file}")
            return
        quoted = "'" + value.replace("'", "'\\''") + "'"
        lines = []
        if self.env_file.is_file():
            lines = self.env_file.read_text(encoding="utf-8").splitlines()
        new_line, replaced = f"{key}={quoted}", False
        for i, line in enumerate(lines):
            if line.partition("=")[0].strip() == key:
                lines[i], replaced = new_line, True
        if not replaced:
            lines.append(new_line)
        if not self.env_file.exists():
            flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
            os.close(os.open(self.env_file, flags, 0o600))  # private before it holds anything
        self.env_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
        self.note(f"{key} saved to {self.env_file}")

    def command(self, args, secret_input=None):
        """Run a command as an argument list (never through a shell), a secret on standard input."""
        if self.dry_run:
            self.note("would run: " + " ".join(args))
            return 0
        try:
            result = subprocess.run(args, input=secret_input, text=True)
        except OSError as error:  # a missing or unrunnable executable
            raise WizardStopped(f"{args[0]} could not be run: {error.strerror or error}") from None
        if result.returncode != 0:
            raise WizardStopped(f"{args[0]} exited {result.returncode}")
        return result.returncode

    def irreversible(self, description, action):
        """Ask first; a no stops the run. Deletes, migrations, publishing and sending go here."""
        if not self.confirm(f"About to {description}. This cannot be undone. Go ahead?"):
            raise WizardStopped(f"declined: {description}")
        if self.dry_run:
            self.note(f"would {description}")
            return
        action()
        self.done.append(description)

    def once(self, key, description, action):
        """Run `action` unless an earlier run recorded `key` as done; then record it."""
        state = self._state()
        if state.get(key):
            self.note(f"already done on an earlier run: {description}")
            self.skipped.append(description)
            return
        if self.dry_run:
            self.note(f"would {description}")
            return
        action()
        state[key] = True
        self.state_file.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n",
                                   encoding="utf-8")
        self.done.append(description)

    def _state(self):
        if not self.state_file.is_file():
            return {}
        try:
            state = json.loads(self.state_file.read_text(encoding="utf-8"))
        except ValueError:
            state = None
        if not isinstance(state, dict):
            self.warn(f"{self.state_file} is not readable; treating every step as not done")
            return {}
        return state

    # The run ------------------------------------------------------------------------------

    def run(self, stages):
        """Run (name, function) stages in order. Returns 0 when all ran, 1 when stopped."""
        self._total, self._stage = len(stages), 0
        self.banner()
        stopped = None
        try:
            for name, function in stages:
                self.stage(name)
                function(self)
        except (WizardStopped, KeyboardInterrupt) as stop:
            stopped = str(stop) or "interrupted"
        self._print()
        self._print("== Summary ==")
        for item in self.done:
            self._print(f"  done: {item}")
        for item in self.skipped:
            self._print(f"  already done: {item}")
        if stopped:
            remaining = [name for name, _ in stages[max(self._stage - 1, 0):]]
            self._print(f"  stopped at stage {self._stage} of {self._total}: {stopped}")
            for name in remaining:
                self._print(f"  not done: {name}")
            return 1
        self._print(f"  all {self._total} stages walked" + (" (dry walk)" if self.dry_run else ""))
        return 0
