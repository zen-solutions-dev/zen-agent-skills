"""A file name that is not UTF-8 must not silence a directory walker (retro proposal R-007).

Twice a single undecodable byte took findings down with it: `chore-0081` ("an undecodable
byte crashes the toolchain") was about file *content*, and PR #108 ("a non-UTF-8 name
silenced every finding") was about a file *name* reaching a hook. `scripts/_textio.py` now
carries the content half for every distribution script. Nothing pinned the name half across
the toolchain, so this module runs every walker against one fixture shape: a tree in which
the tool has at least one real finding to report, plus a file whose name carries the byte
`0xff`, which no UTF-8 sequence can contain. Each test asserts three things: the tool does
not crash, it still reports the other finding, and it exits as its contract says for that
finding.

The undecodable file is deliberately benign. It sits where the walk reaches it and carries
nothing the tool would report, so the only way it can change the result is by breaking the
walk. Whether a tool can also *name* such a file in a finding is a different question, about
how it prints, and is not asked here.

Output is captured through a strict UTF-8 text stream over bytes, not an `io.StringIO`.
A `StringIO` accepts the lone surrogate Python decodes `0xff` into, so a tool that printed
the name would pass here and die on a real terminal or pipe, whose encoder is strict under
a UTF-8 locale. Hooks run as a subprocess with a JSON payload on stdin, exactly as the
harness runs them, against a fixture project and a fixture home.

Walkers included:
  scripts/validate-skills.py   skills tree, supporting files, `.agents/`-style portable root
  scripts/install.py           placement copy and `--check` digest walk (module globals
                               swapped as `tests/test_install.py`'s `_FixtureKit` does)
  scripts/build-adapters.py    adapter assets and rules rglob, and the marketplace `--check`
                               tree comparison and version digest (`build_marketplace` with
                               a fixture `repo_root`, so the real `.claude-plugin/` is not read)
  scripts/check-citations.py   matrix glob, basename index walk, tests rglob
  scripts/check-provenance.py  rglob over `.agents` and `scripts`, with an injected fetcher,
                               so no network is touched
  scripts/scan-secrets.py      both candidate sources: the `os.walk` fallback and `git ls-files`
  .tasks/validate.py           not under scripts/, but it globs and rglobs `.tasks/`
  scripts/run-checks.py        the roadmap gate's walk over `.agents/skills/*/SKILL.md`
                               (added by feat-0094, after the landing review found it)
  .agents/hooks/install-currency-reminder.py      rglob digest and skills iterdir
  .agents/hooks/instruction-provenance-reminder.py  os.listdir and git's index, which it parses
  .agents/hooks/skill-reachability-reminder.py    iterdir over the skill directories
  .agents/hooks/spec-conformance-gate.py          os.listdir for a sibling matrix

Excluded, and why:
  scripts/_change_scope.py                          walks no directory; it reads git's diff
                                                    for a list of paths
  scripts/_textio.py, scripts/_skillmeta.py         helpers that read files they are handed
  scripts/observatory/                              maintainer tooling over a session corpus,
                                                    out of scope by the task that asked for this
  .agents/hooks/delegation-reminder.py,
  .agents/hooks/worktree-boundary-reminder.py,
  .agents/hooks/observatory-event.py                read their payload, walk no directory

POSIX only. Windows names are UTF-16 and cannot hold the byte at all, so the module is
skipped there. A POSIX filesystem may still refuse the name (macOS APFS raises EILSEQ), so
the name is probed once and every test skips, rather than fails, where it cannot be made.

Standard library only, per the conventions section of AGENTS.md.
"""
import contextlib
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

REPO_ROOT = Path(__file__).resolve().parent.parent
HOOKS = REPO_ROOT / ".agents" / "hooks"
GIT = shutil.which("git")

# The byte under test. 0xff never appears in UTF-8, so a strict decode of it always fails.
BAD = b"bad-\xffname"


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


vs = _load("undecodable_validate_skills", REPO_ROOT / "scripts" / "validate-skills.py")
inst = _load("undecodable_install", REPO_ROOT / "scripts" / "install.py")
ba = _load("undecodable_build_adapters", REPO_ROOT / "scripts" / "build-adapters.py")
cc = _load("undecodable_check_citations", REPO_ROOT / "scripts" / "check-citations.py")
cp = _load("undecodable_check_provenance", REPO_ROOT / "scripts" / "check-provenance.py")
ss = _load("undecodable_scan_secrets", REPO_ROOT / "scripts" / "scan-secrets.py")
tv = _load("undecodable_tasks_validate", REPO_ROOT / ".tasks" / "validate.py")
rc = _load("undecodable_run_checks", REPO_ROOT / "scripts" / "run-checks.py")

NAME_SUPPORTED = False


def setUpModule():
    """Probe once whether this filesystem accepts a name that is not UTF-8."""
    global NAME_SUPPORTED
    if os.name == "nt":
        return
    with tempfile.TemporaryDirectory() as tmp:
        try:
            fd = os.open(os.path.join(os.fsencode(tmp), BAD), os.O_CREAT | os.O_WRONLY, 0o644)
        except OSError:
            return
        os.close(fd)
        NAME_SUPPORTED = True


def plant(directory, suffix=b".md", content=b"nothing to report here\n"):
    """Create `directory/bad-<0xff>name<suffix>` from a bytes path; return its str path."""
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    path = os.path.join(os.fsencode(str(directory)), BAD + suffix)
    with open(path, "wb") as handle:
        handle.write(content)
    return os.fsdecode(path)


class _StrictStream:
    """A text stream that encodes as a real UTF-8 stdout does: strictly, on every write."""

    def __init__(self):
        self.raw = io.BytesIO()
        self.stream = io.TextIOWrapper(self.raw, encoding="utf-8", errors="strict",
                                       newline="", write_through=True)

    def text(self):
        self.stream.flush()
        return self.raw.getvalue().decode("utf-8")


def call(fn, *args, **kwargs):
    """Run `fn` with stdout and stderr captured strictly; return (code, stdout, stderr)."""
    out, err = _StrictStream(), _StrictStream()
    with contextlib.redirect_stdout(out.stream), contextlib.redirect_stderr(err.stream):
        code = fn(*args, **kwargs)
    return code, out.text(), err.text()


@unittest.skipIf(os.name == "nt", "Windows names are UTF-16 and cannot carry the byte 0xff")
class _Case(unittest.TestCase):
    def setUp(self):
        if not NAME_SUPPORTED:
            self.skipTest("this filesystem refuses a file name that is not UTF-8")
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name).resolve()


# --------------------------------------------------------------------------- scripts


SKILL = "---\nname: {name}\ndescription: {desc}\n{meta}---\n\n# {name}\n\nBody text.\n"
DESC = ("Use this skill when you need a thorough action whose description states both what it "
        "does and when to use it.")


def write_skill(skills, name, meta=""):
    d = skills / name
    d.mkdir(parents=True, exist_ok=True)
    (d / "SKILL.md").write_text(SKILL.format(name=name, desc=DESC, meta=meta),
                                encoding="utf-8", newline="\n")
    return d


class ValidateSkillsTests(_Case):
    """The lint walks each skill's supporting files and the portable root beside `skills/`."""

    def test_a_missing_skill_md_is_still_reported(self):
        skills = self.root / "kit" / "skills"
        alpha = write_skill(skills, "alpha")
        plant(alpha / "references")                      # supporting-file rglob
        plant(self.root / "kit" / "hooks")               # portable-root rglob
        plant(self.root / "kit" / "rules", suffix=b".txt")
        (skills / "beta").mkdir()                        # the real finding

        code, out, _ = call(vs.main, skills)
        self.assertIn("beta: no SKILL.md", out)
        self.assertIn("Checked 2 skill(s)", out)
        self.assertEqual(1, code, out)


class InstallTests(_Case):
    """Placement copies the skill tree and `--check` digests both copies of it."""

    def setUp(self):
        super().setUp()
        self.skills = self.root / "skills"
        self.rules = self.root / "rules"
        self.home = self.root / "home"
        self.rules.mkdir()
        (self.rules / "house-style.md").write_text("# house style\n", encoding="utf-8")
        real = (inst.SKILLS_DIR, inst.RULES_DIR, inst.PROFILE_SEEDS, inst.MANIFEST)

        def restore():
            (inst.SKILLS_DIR, inst.RULES_DIR, inst.PROFILE_SEEDS, inst.MANIFEST) = real

        self.addCleanup(restore)
        inst.SKILLS_DIR = self.skills
        inst.RULES_DIR = self.rules
        inst.MANIFEST = self.root / "manifest.json"
        inst.PROFILE_SEEDS = {"core": ["alpha"], "spine": ["alpha"], "all": None}

    def test_a_diverged_copy_is_still_reported_by_check(self):
        alpha = write_skill(self.skills, "alpha")
        plant(alpha / "references")
        write_skill(self.skills, "beta")
        plant(self.rules, suffix=b".txt")

        args = ["--tools", "claude", "--mode", "copy", "--profile", "all",
                "--home", str(self.home)]
        code, out, err = call(inst.main, args)
        self.assertEqual(0, code, out + err)
        placed = self.home / ".claude" / "skills" / "alpha" / "references"
        self.assertIn(BAD + b".md", os.listdir(os.fsencode(str(placed))),
                      "the undecodable file was not placed with its skill")

        installed = self.home / ".claude" / "skills" / "beta" / "SKILL.md"
        installed.write_text("edited after install\n", encoding="utf-8")
        code, out, err = call(inst.main, ["--check", "--home", str(self.home)])
        self.assertRegex(out, r"diverged\s+claude\s+beta")
        self.assertIn("1 diverged", out)
        self.assertEqual(1, code, out + err)


class BuildAdaptersTests(_Case):
    """Assets and the rules module are rglobbed into the output, and the marketplace
    check rglobs and digests the staged plugin tree."""

    def setUp(self):
        super().setUp()
        self.skills = self.root / "skills"
        self.rules = self.root / "rules"
        self.rules.mkdir()
        (self.rules / "house-style.md").write_text("# house style\n", encoding="utf-8")
        real = (ba.SKILLS_DIR, ba.RULES_DIR)

        def restore():
            (ba.SKILLS_DIR, ba.RULES_DIR) = real

        self.addCleanup(restore)
        ba.SKILLS_DIR = self.skills
        ba.RULES_DIR = self.rules
        alpha = write_skill(self.skills, "alpha")
        plant(alpha / "references")
        plant(self.rules, suffix=b".txt")
        write_skill(self.skills, "gamma", meta="metadata:\n  status: draft\n")

    def test_a_withheld_draft_is_still_reported(self):
        out_dir = self.root / "out"
        code, out, err = call(ba.main, ["--target", "cursor,vscode", "--out", str(out_dir)])
        self.assertIn("1 draft skill(s) withheld: gamma", out)
        self.assertEqual(0, code, out + err)

    # Found a real defect when written: `plugin_version()` encoded each path as strict
    # UTF-8, so a 0xff name ended the run in a traceback. Fixed in feat-0094 with
    # `os.fsencode`; this test was the red command (expectedFailure until then).
    def test_an_out_of_date_marketplace_is_still_reported(self):
        shipped = [self.skills / "alpha"]
        parsed = {d: ba.split_frontmatter(ba.read_text_utf8(d / "SKILL.md"))
                  for d in shipped}
        # The fixture root has no committed marketplace at all, which is the finding.
        code, out, err = call(ba.build_marketplace, shipped, parsed, True,
                              repo_root=self.root)
        self.assertIn(".claude-plugin/marketplace.json: missing", out)
        self.assertIn("is out of date", out)
        self.assertEqual(1, code, out + err)


MATRIX = """---
title: thing conformance
spec: docs/spec/thing.md
---

# thing conformance matrix

Spec-vs-implementation audit of [`scripts/thing.py`](../../scripts/thing.py) against
[`thing.md`](thing.md).

## Matrix

| Section | Item | Status | Evidence | Note |
|---|---|---|---|---|
| Scenarios | S-001 a thing | Conformed | `scripts/thing.py` / `no_such_symbol()` | |
"""


class CheckCitationsTests(_Case):
    """Matrices are globbed, every file is indexed by basename, and tests are rglobbed."""

    def test_a_dead_citation_is_still_reported(self):
        spec = self.root / "docs" / "spec"
        spec.mkdir(parents=True)
        (self.root / "scripts").mkdir()
        (self.root / "tests").mkdir()
        (self.root / "scripts" / "thing.py").write_text("def assemble():\n    pass\n",
                                                       encoding="utf-8")
        (self.root / "tests" / "test_thing.py").write_text("def test_it():\n    pass\n",
                                                          encoding="utf-8")
        (spec / "thing.md").write_text("# thing\n", encoding="utf-8")
        (spec / "thing.conformance.md").write_text(MATRIX, encoding="utf-8")
        plant(spec)
        plant(self.root / "scripts", suffix=b".py", content=b"X = 1\n")
        plant(self.root / "tests", suffix=b".py", content=b"def test_other():\n    pass\n")

        stream = _StrictStream()
        code = cc.main([], out=stream.stream, root=self.root)
        out = stream.text()
        self.assertIn("no_such_symbol", out)
        self.assertIn("1 unresolved", out)
        self.assertEqual(1, code, out)


UPSTREAM = b"# upstream content\nthe bytes we adapted from\n"
PROVENANCE = """---
name: x
---

# X

Adapted, so it differs from upstream.

## Provenance

```provenance
source: https://raw.githubusercontent.com/example/example/main/SKILL.md
author: Someone
license: MIT
retrieved: 2026-08-06
sha256: {sha}
```
"""


class CheckProvenanceTests(_Case):
    """Every `.md` and `.py` under `.agents` and `scripts` is rglobbed. The fetcher is
    injected, so the run never touches the network."""

    def test_drift_is_still_reported(self):
        skill = self.root / ".agents" / "skills" / "x"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text(PROVENANCE.format(sha="0" * 64), encoding="utf-8")
        plant(skill)
        plant(self.root / "scripts", suffix=b".py", content=b"X = 1\n")

        def fetcher(url, timeout=30):
            return UPSTREAM

        stream = _StrictStream()
        code = cp.main(argv=[], root=self.root, fetcher=fetcher, out=stream.stream)
        out = stream.text()
        self.assertIn("1 drifted", out)
        self.assertIn(".agents/skills/x/SKILL.md", out)
        self.assertEqual(1, code, out)


# Assembled from parts so this file does not itself trip the secret scan.
FAKE_KEY = "AK" + "IA" + "ABCDEFGHIJKLMNOP"


def no_git(command, **_):
    raise FileNotFoundError("git")


class ScanSecretsTests(_Case):
    """Two sources of candidate paths: `git ls-files`, and an `os.walk` when git is absent."""

    def setUp(self):
        super().setUp()
        (self.root / "config.txt").write_text(f"key = {FAKE_KEY}\n", encoding="utf-8")
        plant(self.root)
        plant(self.root / "sub", suffix=b".txt")

    def _scan(self, runner):
        stream = _StrictStream()
        code = ss.main(root=self.root, runner=runner, out=stream.stream)
        return code, stream.text()

    def test_a_planted_key_is_still_reported_by_the_tree_walk(self):
        code, out = self._scan(no_git)
        self.assertIn("config.txt:1: looks like a AWS access key id", out)
        self.assertIn("1 finding(s)", out)
        self.assertIn("Scanned 3 file(s)", out)
        self.assertEqual(1, code, out)

    @unittest.skipIf(GIT is None, "git is not installed")
    def test_a_planted_key_is_still_reported_through_git(self):
        subprocess.run([GIT, "init", "-q"], cwd=self.root, check=True, capture_output=True)
        code, out = self._scan(None)
        self.assertIn("config.txt:1: looks like a AWS access key id", out)
        self.assertIn("1 finding(s)", out)
        self.assertIn("Scanned 3 file(s)", out)
        self.assertEqual(1, code, out)


TASK = """---
id: feat-0001
type: feat
status: {status}
priority: P2
created: 2026-11-24
parent: none
depends_on: []
touched_files: []
---

# A fixture task
"""


class TasksValidateTests(_Case):
    """Task files are globbed from `.tasks/` and `done/`, and every Markdown file under
    `.tasks/` is rglobbed for links."""

    def setUp(self):
        super().setUp()
        self.tasks = self.root / ".tasks"
        (self.tasks / "done").mkdir(parents=True)
        real = (tv.TASKS_DIR, tv.REPO_ROOT)

        def restore():
            (tv.TASKS_DIR, tv.REPO_ROOT) = real

        self.addCleanup(restore)
        tv.TASKS_DIR = self.tasks
        tv.REPO_ROOT = self.root

    def test_an_invalid_status_is_still_reported(self):
        (self.tasks / "feat-0001-fixture.md").write_text(TASK.format(status="bogus"),
                                                        encoding="utf-8")
        plant(self.tasks / "notes")
        plant(self.tasks / "done", suffix=b".txt")
        code, out, err = call(tv.main, [])
        self.assertIn("feat-0001-fixture.md: invalid status: 'bogus'", out)
        self.assertEqual(1, code, out + err)


# ----------------------------------------------------------------------------- hooks


def run_hook(name, payload, home):
    """Run a hook the way the harness does: a subprocess, one JSON payload on stdin."""
    env = dict(os.environ, HOME=str(home), USERPROFILE=str(home))
    done = subprocess.run([sys.executable, str(HOOKS / name)],
                          input=json.dumps(payload).encode("ascii"),
                          capture_output=True, env=env, cwd=str(home), timeout=60)
    return done.returncode, done.stdout.decode("utf-8"), done.stderr.decode("utf-8", "replace")


class _HookCase(_Case):
    def setUp(self):
        super().setUp()
        self.home = self.root / "home"
        self.home.mkdir()

    def emitted(self, name, payload):
        """The one object the hook wrote, asserted to be exactly one, at exit 0."""
        code, out, err = run_hook(name, payload, self.home)
        self.assertEqual(0, code, err)
        self.assertNotIn("Traceback", err)
        self.assertTrue(out.strip(), f"{name} stayed silent when it had a finding")
        return json.loads(out)


def startup(cwd):
    return {"hook_event_name": "SessionStart", "source": "startup", "cwd": str(cwd)}


class InstallCurrencyHookTests(_HookCase):
    """The hook digests each recorded skill with an rglob and iterdirs the skills tree."""

    def test_a_stale_install_is_still_reported(self):
        repo = self.root / "repo"
        (repo / "scripts").mkdir(parents=True)
        skills = repo / ".agents" / "skills"
        carrier = write_skill(skills, "carrier")
        plant(carrier / "references")
        write_skill(skills, "doc-sync")
        entries = []
        for name in ("carrier", "doc-sync"):
            target = self.home / ".claude" / "skills" / name
            target.mkdir(parents=True)
            (target / "SKILL.md").write_text("installed copy\n", encoding="utf-8")
            entries.append({"tool": "claude", "name": name, "target": str(target),
                            "mode": "copy", "source": str(skills / name),
                            "digests": inst.digest_tree(skills / name)})
        (repo / "scripts" / ".install-manifest.json").write_text(
            json.dumps({"entries": entries}), encoding="utf-8")
        # Move the kit's copy after the record was taken: that is staleness.
        (skills / "doc-sync" / "SKILL.md").write_text("moved on\n", encoding="utf-8")

        text = self.emitted("install-currency-reminder.py",
                            startup(repo))["hookSpecificOutput"]["additionalContext"]
        self.assertIn("stale", text)
        self.assertIn("doc-sync", text)
        self.assertNotIn("carrier", text)


@unittest.skipIf(GIT is None, "git is not installed")
class InstructionProvenanceHookTests(_HookCase):
    """The hook lists directories with `os.listdir` and parses git's index itself."""

    def test_an_uncommitted_instruction_file_is_still_reported(self):
        repo = self.root / "repo"
        repo.mkdir()
        subprocess.run([GIT, "init", "-q"], cwd=repo, check=True, capture_output=True)
        # A tracked file whose name is not UTF-8, so the index the hook parses holds it.
        plant(repo)
        subprocess.run([GIT, "add", "-A"], cwd=repo, check=True, capture_output=True)
        (repo / "AGENTS.md").write_text("planted\n", encoding="utf-8")

        text = self.emitted("instruction-provenance-reminder.py",
                            startup(repo))["hookSpecificOutput"]["additionalContext"]
        self.assertIn("`AGENTS.md` (in a repository, not committed)", text)

    def test_a_launch_directory_whose_name_is_not_utf8_still_reports(self):
        # The PR #108 shape: the undecodable component is in the path from the work tree
        # to the instruction file, so it reaches the index lookup.
        repo = self.root / "repo"
        repo.mkdir()
        subprocess.run([GIT, "init", "-q"], cwd=repo, check=True, capture_output=True)
        odd = os.path.join(os.fsencode(str(repo)), BAD)
        os.mkdir(odd)
        with open(os.path.join(odd, b"AGENTS.md"), "wb") as handle:
            handle.write(b"committed\n")
        subprocess.run([GIT, "add", "-A"], cwd=repo, check=True, capture_output=True)
        (repo / "CLAUDE.md").write_text("planted\n", encoding="utf-8")

        text = self.emitted("instruction-provenance-reminder.py",
                            startup(os.fsdecode(odd)))["hookSpecificOutput"]["additionalContext"]
        self.assertIn("CLAUDE.md", text)
        self.assertIn("in a repository, not committed", text)
        self.assertNotIn("AGENTS.md", text)


class SkillReachabilityHookTests(_HookCase):
    """The hook iterdirs each discovery directory looking for a kit skill."""

    def test_no_reachable_skill_is_still_reported(self):
        project = self.root / "project"
        foreign = project / ".claude" / "skills"
        write_skill(foreign, "someone-elses-skill")
        plant(foreign, suffix=b"")
        plant(self.home / ".claude" / "skills", suffix=b"")
        plant(self.home / ".agents" / "skills", suffix=b"")

        out = self.emitted("skill-reachability-reminder.py", startup(project))
        self.assertIn("skills found at either project scope or user scope",
                      out["hookSpecificOutput"]["additionalContext"])


class SpecConformanceGateTests(_HookCase):
    """The gate lists the spec's directory looking for a sibling conformance matrix."""

    def test_a_terminal_spec_without_a_matrix_still_blocks(self):
        spec = self.root / "docs" / "spec"
        spec.mkdir(parents=True)
        (spec / "thing.md").write_text("---\nstatus: shipped\n---\n# thing\n",
                                       encoding="utf-8")
        plant(spec)
        payload = {"hook_event_name": "PostToolUse", "tool_name": "Edit",
                   "cwd": str(self.root), "tool_input": {"file_path": str(spec / "thing.md")}}

        out = self.emitted("spec-conformance-gate.py", payload)
        self.assertEqual("block", out.get("decision"))
        self.assertIn("'thing.md' is marked status='shipped'", out["reason"])


if __name__ == "__main__":
    unittest.main()


class RunChecksRoadmapTests(_Case):
    """`check_roadmap()` walks the skills to read each one's status (feat-0094, P3).

    The fixture's draft list names a shipped skill, which is the finding, and leaves out a
    draft whose directory name carries the byte, which is a second finding that has to name
    it. Run through `run_all` on a strict stream, as the acceptance command prints it.
    """

    def test_a_wrong_draft_list_is_still_reported(self):
        skills = self.root / ".agents" / "skills"
        write_skill(skills, "alpha")
        bad = os.path.join(os.fsencode(str(skills)), BAD)
        os.makedirs(bad)
        with open(os.path.join(bad, b"SKILL.md"), "wb") as handle:
            handle.write(b"---\nname: x\ndescription: x\nmetadata:\n  status: draft\n---\n")
        (self.root / ".tasks" / "done").mkdir(parents=True)
        (self.root / "ROADMAP.md").write_text(
            "# Roadmap\n\n## Current state\n\n- **Drafts**: `alpha`.\n", encoding="utf-8")
        gate = rc.Gate("roadmap bookkeeping", [],
                       check=lambda: rc.check_roadmap(self.root, status_exceptions=()))
        code, out, _ = call(lambda: rc.run_all([gate], out=sys.stdout))
        self.assertEqual(code, 1, out)
        self.assertIn("`alpha` is named as a draft", out)
        self.assertIn("bad-\\xffname", out)
