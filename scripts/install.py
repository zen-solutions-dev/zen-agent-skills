#!/usr/bin/env python3
"""Install the Zen Agent Skills library into your AI tools' discovery directories.

Idempotent and safe to re-run. Previews with --dry-run, reverses with
--uninstall. Never clobbers a real file it did not create: such a target is
reported CONFLICT and skipped for you to resolve.

In copy mode, re-run recognition relies on scripts/.install-manifest.json to
know which targets this tool created. If that manifest is deleted, previously
copied targets are treated as unmanaged and reported CONFLICT (symlink mode
recognizes its own links directly and does not have this dependency). If it is
present but structurally damaged, every command stops at exit 2 naming the file
and the offending entry, rather than acting on a record it cannot read.

    python scripts/install.py --dry-run          # preview
    python scripts/install.py                     # install (copy on Windows, symlink on POSIX)
    python scripts/install.py --mode symlink      # force symlinks
    python scripts/install.py --tools claude      # only Claude Code
    python scripts/install.py --profile all       # every skill, not just the default set
    python scripts/install.py --check             # is an installed set still current?
    python scripts/install.py --replace-adopted   # take the kit's rules module, lose yours
    python scripts/install.py --uninstall         # remove what this installed
    python scripts/install.py --skills new-quest   # one skill plus its sibling-link closure
    python scripts/install.py --include-drafts    # also place draft skills, to try them

Named skills, drafts, and rendered copies (feat-0079)
----------------------------------------------------
`--skills a,b` places the named skills plus their closure over sibling links, and prints
that closure, so a person can ask for one skill without taking a whole profile. It replaces
`--profile` rather than combining with it.

`--include-drafts` lets a draft be placed. With a profile it adds every draft and their
closure to what the profile places; with `--skills` it lets the named set and its closure
contain drafts without adding the rest. Either way the run names each placed draft, because
a draft is placed only so a person can try it, and "no skill ships cold" is decided by use.

A skill declaring `metadata.invocation: user` is started by a person, by name. Claude Code
reads `disable-model-invocation: true` to keep such a skill's description out of every
session, and claude.ai rejects that key, so the source never carries it: the `claude` target
receives a rendered copy that does, and no other target is changed. A rendered skill is
therefore always copied, never linked, even in symlink mode, because a link would show the
unrendered source. Its recorded digests are the rendered bytes, so `--check` names a rendered
copy that has fallen behind its source as `diverged`, and re-installing refreshes it.

Two placement hazards are closed. A rules directory the kit did not place is merged into
file by file rather than refused whole, and a file already there that the kit did not place
is reported CONFLICT and left alone; `--uninstall` then removes only the files it placed.
And a same-named symlink pointing anywhere but this kit's source, that the record does not
name as this tool's, is a CONFLICT rather than being silently relinked.

Staleness, and why --check exists
---------------------------------
A copied skill is a snapshot taken at install time, so editing the skill here does
not change the installed copy and nothing said so: the stale copy is a valid skill
that passes every validator and reads correctly (chore-0031). So each entry in the
manifest now records a SHA256 per placed file, and --check re-reads the targets and
names any that no longer match their source. It reports and never rewrites, for the
same reason check-provenance.py does: an adopter may have edited an installed file
deliberately, and an overwrite destroys that without asking.

The baseline is per entry, not per manifest, so a manifest written before this change
degrades one entry at a time. Such an entry reports `unknown`, never `ok`: a clean
result for a state nobody recorded is the same silent failure --check exists to
remove, one level up. Re-install to establish a baseline, except for the adopted
rules module: re-installing that one preserves your files and records nothing, so
--replace-adopted is the only route to a baseline there (bug-0020).

A --profile selects which skills to place, and defaults to less than all of them
because every installed description is loaded so an agent can route to it. A profile
is expanded over sibling references before anything is placed, so it can never ship a
skill whose composed sibling is missing. --uninstall is unaffected by the profile: it
reverses every recorded target beneath --home, whichever run placed it.

A skill whose frontmatter carries `metadata.status: draft` is placed by no profile,
including `all`, so a skill the kit has not blessed is never distributed to an adopter
(S-015). No marker means shipped, so the exclusion is always a deliberate act.

Discovery targets (per tool), each skill linked/copied as <base>/<skill-name>:
    claude    -> ~/.claude/skills
    opencode  -> ~/.agents/skills

The swappable rules module (.agents/rules/) travels with the skills, placed as
the sibling <base>/../rules. That location is not arbitrary: a skill body
references its lens as ../../rules/<file>.md, which resolves from
<base>/<skill-name>/SKILL.md to exactly this directory. Without it, house-review
loses its whole rubric and twelve other skills lose their house-style module.

That module is adopted, not derived, and a re-install treats it accordingly
(bug-0018). A skill directory is regenerated wholesale, because it is the kit's;
a rules file you edited is kept, reported, and never merged into, because the
kit invites you to make it your own and an overwrite would destroy that work
with nothing anywhere to say so. The recorded digests draw the line: a file
matching its baseline is untouched and is refreshed, a file that does not is
yours. `--replace-adopted` takes the kit's copies when you want them.

Cursor and Copilot read repo-level pointer files, not a global skills dir, so
they are handled by build-adapters.py per project, not here.

Standard library only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
from pathlib import Path

# `_textio` is a sibling module in this directory, imported through the repository root so
# the one spelling works whether this file is run as a script or imported as a module of
# `scripts`, which `observatory/serve.py` already does for `install`. Same preamble as there,
# and the same reason: the two invocations put different directories on `sys.path`.
_TEXTIO_ROOT = Path(__file__).resolve().parent.parent
if str(_TEXTIO_ROOT) not in sys.path:
    sys.path.insert(0, str(_TEXTIO_ROOT))
from scripts._textio import NotUTF8, read_text_utf8   # noqa: E402
from scripts._skillmeta import (   # noqa: E402
    is_user_invoked_text, metadata_fields, render_for_claude, sibling_edges)

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / ".agents" / "skills"
RULES_DIR = REPO_ROOT / ".agents" / "rules"
HOOKS_DIR = REPO_ROOT / ".agents" / "hooks"
MANIFEST = REPO_ROOT / "scripts" / ".install-manifest.json"

# A skill's old name mapped to its current one. The old name is an alias: `--skills`
# accepts it, and a run retires a placement this tool recorded under it, which would
# otherwise point at a source that no longer exists. `new-task` became `new-quest` in the
# rename from tasks to quests (feat-0101).
RENAMED_SKILLS = {"new-task": "new-quest"}

TOOL_SUBPATHS = {
    "claude": Path(".claude") / "skills",
    "opencode": Path(".agents") / "skills",
}

# Which skills a profile asks for. Each is a seed, not the final set: it is expanded
# over sibling references before anything is placed (S-013), because a skill that
# composes a sibling by reference is broken without it.
#
# Until the 2026-11 overhaul these boundaries were dictated by the reference graph: one
# strongly connected component of fourteen skills meant any profile touching it was at
# least seventeen. The overhaul kept a sibling link only where a skill genuinely composes
# its sibling and named every neighbour in backticks, so the graph has no cycle and the
# seeds below are a choice again: `spine` names every shipped skill on the delivery path,
# including `doc-author`, which used to arrive only through a neighbour's link
# (feat-0080). `--skills` places any single skill with its closure. See docs/spec/install.md.
PROFILE_SEEDS = {
    "core": ["project-bootstrap", "init-worktracking", "pr-describe"],
    "spine": ["spec-author", "spec-plan-readiness", "new-quest", "fix-batch", "test-author",
              "spec-conformance", "verifier-agent", "reconcile-worktrees", "doc-sync",
              "pr-describe", "project-bootstrap", "init-worktracking", "house-review",
              "doc-author"],
    "all": None,  # everything discovered
}
DEFAULT_PROFILE = "spine"

# The one syntax that makes a skill a profile edge: a markdown link from one skill body
# to a sibling SKILL.md. The same skill named in backticks is prose and creates no edge,
# which is the form for stating chain position. Authors trip this by writing the readable
# link form for a neighbour they only meant to name (chore-0040), so the rule is stated
# for skill authors in AGENTS.md's portability contract, not only here where they will
# never read it. The syntax itself is read by `sibling_edges()` in `_skillmeta.py`, the
# reader the validator and the adapter builder share, so a link shown as an example in a
# code span or a fence is not an edge here either (feat-0090).
# Narrow readers for one frontmatter field, deliberately not a YAML parser. The block
# scalar case matters here for the same reason it does in validate-skills.py: without
# it the reported description budget is inflated by three characters per skill that
# uses one. This is the third copy of this shape in scripts/; unifying them is a
# standing recommendation, not a drive-by change.
DESC_FIELD_RE = re.compile(r"^description:\s*(.*)$")
BLOCK_SCALAR_RE = re.compile(r"^[|>][+-]?\s*")

# The draft marker (S-015). `metadata` is one of the six frontmatter properties the
# skill schema permits, so a nested `status` under it is the only spelling that is both
# legal for the external validator and mechanical here. A bare top-level `status:` key
# would be rejected outright by validate-skills.py's allow-list, and the flow form
# `metadata: {status: draft}` trips its plain-scalar-with-a-colon check, so only the
# block form below is read:
#
#     metadata:
#       status: draft
#
# Deliberately not a YAML parser. Read by `scripts/_skillmeta.py` since feat-0079.
DRAFT_STATUS = "draft"


def discover_skills():
    if not SKILLS_DIR.is_dir():
        return []
    return sorted(d for d in SKILLS_DIR.iterdir()
                  if d.is_dir() and (d / "SKILL.md").is_file())


def description_of(skill_dir: Path) -> str:
    """The skill's `description` value, or "" when absent.

    Only the frontmatter is scanned, and only for this one field. A block-scalar
    indicator is dropped so the length is the text's, matching what a harness measures.
    """
    text = read_text_utf8(skill_dir / "SKILL.md")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return ""
    parts, collecting = [], False
    for raw in lines[1:]:
        if raw.strip() == "---":
            break
        m = DESC_FIELD_RE.match(raw)
        if m:
            parts.append(BLOCK_SCALAR_RE.sub("", m.group(1).strip().strip('"').strip("'"), count=1))
            collecting = True
        elif collecting:
            if re.match(r"^\w[\w-]*:", raw):
                break
            if raw.strip():
                parts.append(raw.strip())
    return " ".join(p for p in parts if p).strip()


def status_of(skill_dir: Path) -> str:
    """The skill's `metadata.status` value, lowercased, or "" when it carries none.

    Only the frontmatter's `metadata:` block is read, so a `status:` line written
    anywhere in the body is prose and not a marker. That distinction is load-bearing:
    several skills in this kit discuss draft status in their bodies, and reading one of
    those as a marker would drop a shipped skill from every profile with no signal.

    An unrecognised value reads as shipped rather than as a draft, so a typo
    over-delivers (today's defect) instead of silently under-delivering (the worse one).

    The reader is `scripts/_skillmeta.py`, shared with build-adapters.py and
    validate-skills.py since feat-0079 so the three cannot disagree about a marker.
    """
    return metadata_fields(read_text_utf8(skill_dir / "SKILL.md")).get("status", "")


def is_user_invoked(skill_dir: Path) -> bool:
    """Whether the skill declares `metadata.invocation: user` (feat-0079)."""
    return is_user_invoked_text(read_text_utf8(skill_dir / "SKILL.md"))


def renders_for(tool: str, skill_dir: Path) -> bool:
    """Whether `tool` receives a rendered copy of this skill rather than the source.

    Only Claude Code reads `disable-model-invocation`, and claude.ai rejects it, so only
    the `claude` target renders, and only a user-invoked skill has anything to render.
    """
    return tool == "claude" and is_user_invoked(skill_dir)


def rendered_skill_md(skill_dir: Path) -> bytes:
    """The SKILL.md bytes a Claude Code copy of this skill carries."""
    return render_for_claude(read_text_utf8(skill_dir / "SKILL.md")).encode("utf-8")


def expected_digests(skill_dir: Path, tool: str) -> dict:
    """What a correct install of this skill for `tool` digests to.

    The source's own digests, except that a rendered copy's SKILL.md is the rendered
    bytes. Recorded at install and recomputed by `--check`, so a rendered copy is compared
    against what a re-install would place rather than against a source it never matched.
    """
    digests = digest_tree(skill_dir)
    if renders_for(tool, skill_dir):
        digests["SKILL.md"] = hashlib.sha256(rendered_skill_md(skill_dir)).hexdigest()
    return digests


def closure(names, by_name) -> set:
    """`names` expanded over sibling links until closed, within `by_name` (S-013)."""
    wanted = {n for n in names if n in by_name}
    stack = list(wanted)
    while stack:
        for ref in sibling_refs(by_name[stack.pop()]):
            if ref in by_name and ref not in wanted:
                wanted.add(ref)
                stack.append(ref)
    return wanted


def partition_drafts(skills):
    """Split discovered skills into (shipped, drafts).

    Absence of a marker means shipped, so this only ever holds back a skill that says
    so itself. Applied before a profile is resolved, so the closure in resolve_profile
    runs over the shipped set rather than around it.
    """
    draft_names = {d.name for d in skills if status_of(d) == DRAFT_STATUS}
    return ([d for d in skills if d.name not in draft_names],
            [d for d in skills if d.name in draft_names])


def draft_conflicts(selected, seed, draft_names) -> list:
    """Contradictions between what a profile would place and the draft markers.

    Two shapes, both of which would otherwise resolve silently and wrongly:

    - A selected skill references a draft sibling. Dropping the reference reintroduces
      the dangling-sibling defect S-013 exists to prevent; pulling the draft in defeats
      the marker. Neither is this tool's call to make, so it places nothing and says so.
    - A profile seed names a draft. The seed is filtered against the shipped set, so
      such a name would otherwise vanish from the request without a word.
    """
    problems = []
    for name in (seed or []):
        if name in draft_names:
            problems.append(f"the profile seed names {name!r}, which is marked a draft")
    for d in selected:
        for ref in sorted(sibling_refs(d) & set(draft_names)):
            problems.append(f"{d.name} references {ref!r} as a sibling, "
                            f"and {ref!r} is marked a draft")
    return problems


def sibling_refs(skill_dir: Path) -> set:
    """Skill names this skill links to as ../<name>/SKILL.md."""
    text = read_text_utf8(skill_dir / "SKILL.md")
    return sibling_edges(text) - {skill_dir.name}


def resolve_profile(profile: str, skills):
    """Return (selected_dirs, added_names) for a profile.

    The seed is expanded over sibling references until closed (S-013). Computed rather
    than listed, so a skill that gains a reference later cannot silently leave a
    profile shipping a dangling one.
    """
    by_name = {d.name: d for d in skills}
    seed = PROFILE_SEEDS[profile]
    if seed is None:
        return list(skills), []
    wanted = closure(seed, by_name)
    added = sorted(wanted - {n for n in seed if n in by_name})
    return [d for d in skills if d.name in wanted], added


def model_invoked_budget(skills):
    """Description characters an agent carries for these skills: the model-invoked ones.

    A user-invoked skill reaches Claude Code with `disable-model-invocation: true`, which
    keeps its description out of context, so counting it reports a cost no session pays
    (feat-0094, inventory P11). It is reported beside this figure, never inside it.
    """
    return sum(len(description_of(d)) for d in skills if not is_user_invoked(d))


def profile_budgets(skills):
    """Model-invoked description total per profile, so the figure is comparable."""
    return {name: model_invoked_budget(resolve_profile(name, skills)[0])
            for name in PROFILE_SEEDS}


class ManifestError(Exception):
    """The manifest parsed as JSON but is not a record this tool can read.

    Raised by `load_manifest()` and caught by each of its three callers, which is the
    shape the callers dictate: `install`, `uninstall`, and `check` all need to stop, but
    they stop with different words, and a sentinel return value would have every caller
    re-deriving the reason from a value that cannot carry one.
    """


# What a reader here actually dereferences, and nothing beyond it (bug-0024). Every key
# below is read by `install`, `uninstall`, `check`, or `_check_entry`; a key none of them
# reads is not validated, because a validator strict enough to reject a record written by
# a later version of this tool turns an upgrade into what looks like corruption. An
# unrecognised key is ignored in both directions, deliberately.
#
# `target` is the one required key: `install`, `uninstall`, and `check` each subscript it
# directly, so an entry without it is not a record of anything. The rest are optional and
# faulted on only when present and of the wrong type, since each has a reader that already
# tolerates its absence.
_OPTIONAL_ENTRY_TYPES = {
    "source": (str, "a string"),      # _check_entry: Path(entry.get("source", ""))
    "tool": (str, "a string"),        # check(): sort key and printed column
                                      # uninstall(): printed column
    "name": (str, "a string"),        # check(): sort key, and the ADOPTED_ENTRY_NAMES test
                                      # uninstall(): printed column
    "digests": (dict, "an object"),   # _compare(): iterated as a mapping
}
# Every reader named above reaches its key through `.get()`, and that is what makes the
# optionality real rather than asserted. `uninstall()` was missing from this list and
# subscripted both of its two, so a record this validator accepts killed it mid-loop, after
# it had already deleted a target (bug-0053). A reader added here without a `.get()` puts
# the same trap back, and the comment is the only place the two facts are stated together.


def _describe(value) -> str:
    """Name a JSON value's shape the way the file that holds it spells it."""
    return {type(None): "null", bool: "a boolean", int: "a number", float: "a number",
            str: "a string", list: "a list", dict: "an object"}.get(type(value),
                                                                    repr(value))


def _validate_manifest(data) -> None:
    """Raise `ManifestError` naming the first structural fault, or return.

    The message is half the fix. A manifest is per-machine and gitignored, so the reader
    of this message is the only person who can see the file: naming the entry and the key
    is the difference between a one-line repair and an investigation this report exists to
    save. The caller adds the path and the remedy.
    """
    if not isinstance(data, dict):
        raise ManifestError(f'its top-level value is {_describe(data)}, not an object '
                            f'with an "entries" list')
    entries = data.get("entries")
    if entries is None:
        raise ManifestError('it has no "entries" list')
    if not isinstance(entries, list):
        raise ManifestError(f'its "entries" is {_describe(entries)}, not a list')

    for i, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise ManifestError(f"entry {i} is {_describe(entry)}, not an object")
        where = f"entry {i}"
        if isinstance(entry.get("name"), str):
            where += f" ({entry['name']!r})"
        if "target" not in entry:
            raise ManifestError(f'{where} has no "target", so it records no installed '
                                f"path")
        target = entry["target"]
        if not isinstance(target, str) or not target:
            raise ManifestError(f'{where} has a "target" that is {_describe(target)}, '
                                f"not a path")
        for key, (want, described) in _OPTIONAL_ENTRY_TYPES.items():
            if key in entry and not isinstance(entry[key], want):
                raise ManifestError(f'{where} has a "{key}" that is '
                                    f"{_describe(entry[key])}, not {described}")


def load_manifest():
    """The recorded install, or `{"entries": []}` when there is nothing readable.

    Raises `ManifestError` when the file parses as JSON but is not shaped like a manifest.

    Corrupt bytes and a wrong shape are treated differently on purpose. Bytes that do not
    parse carry no recoverable information and never did name an install, so an empty
    record is a truthful reading of them. A file that parses does carry a record, possibly
    of targets under homes this run is not even looking at, and reading it as empty would
    quietly authorise placing over them or reporting them absent. So the wrong shape stops
    the run instead, at exit 2 (could not run) rather than exit 1 (diverged), because a
    caller scripting around `--check` treats 1 as an answer and 2 as the absence of one.
    """
    if MANIFEST.is_file():
        try:
            data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {"entries": []}
        _validate_manifest(data)
        return data
    return {"entries": []}


def report_unreadable_manifest(exc: ManifestError, consequence: str) -> int:
    """Print the stated exit-2 report for an unreadable manifest and return 2.

    One helper rather than three copies, so the path and the remedy cannot drift apart
    between the three commands that can hit this.
    """
    print(f"Cannot read the install record at {MANIFEST}: {exc}.")
    print(f"{consequence}")
    print("The record is written per machine and is not in version control, so an "
          "interrupted write, a full disk, or a partly synced home produces exactly "
          "this. Nothing here repairs it: re-install to establish a fresh record "
          "(python scripts/install.py), or delete the file and re-install, which is "
          "the same thing with the damaged copy gone.")
    return 2


def save_manifest(entries, dry):
    if dry:
        return
    # `newline=""` disables newline translation, so the manifest holds exactly the
    # newlines in the string rather than the platform default, which is CRLF on Windows.
    # The manifest is gitignored, so nothing is broken today; the point is that `--check`
    # compares digests of bytes read off disk, and a writer whose line endings vary by
    # platform is the shape that makes such a comparison answer differently per platform.
    MANIFEST.write_text(json.dumps({"entries": entries}, indent=2),
                        encoding="utf-8", newline="")


def is_managed(target: Path, manifest) -> bool:
    tp = str(target)
    return any(e.get("target") == tp for e in manifest["entries"])


# The one placed module an adopter is invited to rewrite. Matched by the entry name this
# tool records for it, so the classification travels in the record rather than being
# re-derived from a path. See `_check_entry` for what the invitation costs the check, and
# `_place_adopted` for what it costs placement.
ADOPTED_ENTRY_NAMES = {"rules"}


def _digestable(rel: Path, path: Path) -> bool:
    """Whether a file beneath a placed module is part of that module.

    Mirrors the ignore list `_copy` places with. Digesting a byte-cache would report a
    file missing from every install of the hooks module, since the source grows a
    `__pycache__` as soon as anything imports it and the copy deliberately has none.
    """
    return path.suffix != ".pyc" and "__pycache__" not in rel.parts


def digest_tree(root: Path) -> dict:
    """SHA256 per file beneath `root`, keyed by its POSIX-relative path.

    Per file and not per directory (chore-0031): a skill is a directory of templates and
    references, and a stale template is exactly as silent as a stale `SKILL.md`. Keys are
    POSIX-relative so a record written on Windows is readable on macOS and Linux.

    Bytes, never decoded text. This repository is LF by `.gitattributes`, but an installed
    copy lives outside git, and digesting decoded text would make the answer depend on how
    the reader normalises line endings rather than on what is actually on disk.
    """
    digests = {}
    if not root.is_dir():
        return digests
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        if not _digestable(rel, path):
            continue
        digests[rel.as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return digests


# Where each tool expects the hooks module, as a sibling of its skills directory. Absent
# from this map means the tool has no hook mechanism this installer knows how to place.
HOOK_SUBPATHS = {
    "claude": Path(".claude") / "hooks",
    "opencode": Path(".agents") / "hooks",
}

# Each hook in the module and the PostToolUse matcher that must wake it. A matcher may be
# broader than the hook's own condition, since every hook re-checks; it may never be
# narrower, or the hook is placed and silently never fires. `tests/test_hooks.py`
# asserts the delegation matcher against the hook's own tool set for exactly that reason.
# (script, event, matcher). The event was added by feat-0046 and is not cosmetic: this
# table carried only (script, matcher) while claude_registration() hardcoded PostToolUse,
# so a hook on any other event was placed by --with-hooks and never registered. That is
# the "installed, correct-looking, and doing nothing" failure feat-0038 hit twice, and it
# would have been silent here too.
HOOK_REGISTRATIONS = [
    ("delegation-reminder.py", "PostToolUse",
     "^Task$|^Agent$|^TaskOutput$|agent_run"),
    ("spec-conformance-gate.py", "PostToolUse",
     "^Edit$|^Write$|^MultiEdit$|^NotebookEdit$|apply_patch"),
    # `startup` only. The other sources continue a session already told.
    ("skill-reachability-reminder.py", "SessionStart", "startup"),
    # Same event and the same reasoning, and deliberately a second hook rather than a
    # branch inside the first: reachability is a directory-name match, currency reads and
    # digests files, and the reachability reminder's own message disclaims this question.
    ("install-currency-reminder.py", "SessionStart", "startup"),
    # `Stop` rather than `PostToolUse`: one line per finished turn is the granularity the
    # observatory needs, and a hook on every tool call would spool twenty lines for one
    # turn's worth of the same hint. No tool matcher, because this event carries no tool.
    ("observatory-event.py", "Stop", ""),
    # Shell tools only: Claude Code already refuses an edit tool aimed at the main
    # checkout, and what it does not watch is a shell command's write targets (2026-10
    # kit refresh, audit finding 4.2). The hook re-checks the tool name itself.
    ("worktree-boundary-reminder.py", "PostToolUse", "^Bash$|^PowerShell$"),
    # `startup` only, like the other two SessionStart reminders, and a hook of its own
    # rather than a branch in either: it asks whether the files a harness loaded at launch
    # are committed, which is neither reachability nor currency (feat-0081).
    ("instruction-provenance-reminder.py", "SessionStart", "startup"),
]


def hook_interpreter() -> str:
    """The interpreter name to write into a hook registration.

    Not hardcoded to `python3`. On Windows that name usually resolves to the Microsoft
    Store's app-execution alias, which prints an install advertisement and exits without
    running anything, so a registration naming it produces a hook that fails silently
    forever. Found by dogfooding feat-0038 on Windows, where the first draft did exactly
    that. Mirrors how `--mode` already defaults per platform.
    """
    return "python" if os.name == "nt" else "python3"


def claude_registration(home: Path) -> str:
    """The settings.json block a user pastes to activate the hooks.

    Printed rather than merged. Editing someone's settings file is the one step of this
    install the uninstall manifest cannot cleanly reverse, and a hook is the only thing
    the kit ships that runs inside their session, so the placement is automated and the
    activation is not: nothing fires until a person pastes this in.

    The path is absolute and resolved rather than `~/...`, because whether a tilde is
    expanded depends on how the harness spawns the command, and a registration that
    silently does not run is the worst outcome available here.

    Built from HOOK_REGISTRATIONS rather than written out, so a hook added to the module
    without a matcher here is a mistake that shows up as a missing entry instead of a hook
    that was placed and never fires.

    Grouped by event rather than emitted under a hardcoded one. The event lives in the
    table now, so adding a hook on a new lifecycle event needs no change here at all,
    which is what the previous shape got wrong.
    """
    hooks_home = home / HOOK_SUBPATHS["claude"]
    by_event = {}
    for script_name, event, matcher in HOOK_REGISTRATIONS:
        if not (HOOKS_DIR / script_name).is_file():
            continue
        command = f"{hook_interpreter()} \"{hooks_home / script_name}\""
        by_event.setdefault(event, []).append({
            "matcher": matcher,
            "hooks": [{"type": "command", "command": command}],
        })
    return json.dumps({"hooks": by_event}, indent=2)


def opencode_reader(home: Path) -> Path:
    """The file that decides whether an opencode hook placement is read by anything.

    `.opencode/plugins/zen-hooks.mjs` resolves its own `.agents/hooks` against
    `worktree || directory || process.cwd()`, which is the project root opencode opened
    and never the user's home. So the home-scoped copy this installer places is read
    exactly when the home it was given is itself that project root, and this path is the
    thing that would be doing the reading.
    """
    return home / ".opencode" / "plugins" / "zen-hooks.mjs"


def opencode_activation_note(home: Path, hooks_target: Path) -> str:
    """What an opencode `--with-hooks` run says about the copy it just placed.

    The counterpart of `claude_registration`, and deliberately a different message,
    because the two paths fail differently (bug-0048). A Claude Code placement is
    complete and merely unregistered: the files are where the harness already reads
    hooks from, and a person pastes a block to wake them. An opencode placement may
    instead be somewhere nothing reads at all, which no registration repairs, so this
    note states where the module landed, names the reader, and says whether that reader
    is actually there.

    The live-or-inert half is decided from the filesystem rather than from the shape of
    the path, so a placement that did nothing useful and a placement that worked are
    distinguishable in the output rather than only in a maintainer's head. Comparing the
    home against `Path.home()` was the cheaper rule and is the wrong one twice over: it
    answers whether this looks like the default run rather than whether anything reads
    the files, and string equality over a home resolved through a macOS `/var` symlink or
    a Windows 8.3 short name answers even that wrongly.

    The kit does not install the reader. `.opencode/plugins/zen-hooks.mjs` is committed in
    this repository as its own wiring, and nothing under `scripts/` distributes it, so the
    inert branch says that plainly instead of implying a re-run would fix it.
    """
    reader = opencode_reader(home)
    if reader.is_file():
        return (f"The hooks are placed and LIVE for opencode: {reader} reads "
                f"{hooks_target} from that project root.\n\n"
                f"`--uninstall` removes the files.")
    return (f"The hooks are placed but INERT for opencode. They landed at "
            f"{hooks_target}, and the opencode plugin resolves `.agents/hooks` against "
            f"the project root it opens rather than against a home, so nothing reads "
            f"this copy: there is no {reader}.\n\n"
            f"To make them run, the module has to sit at `<project>/.agents/hooks` in a "
            f"project whose `.opencode/plugins/zen-hooks.mjs` is present. This installer "
            f"ships neither that plugin nor a project scope: copy the plugin from this "
            f"kit into the project you want it in, then re-run with `--home` set to that "
            f"project root. `--uninstall` removes what was placed here.")


def discover_hooks():
    if not HOOKS_DIR.is_dir():
        return []
    return sorted(p for p in HOOKS_DIR.glob("*.py"))


def select_skills(all_skills, profile: str, only=None, include_drafts: bool = False):
    """Decide what a run places. Returns `(skills, added, problems)`.

    `skills` is the closed set to place, `added` the names the closure added to what was
    asked for, and `problems` a list of refusals; when it is non-empty nothing is placed.

    Three requests, one rule. A profile seeds from `PROFILE_SEEDS`; `only` (from
    `--skills`) seeds from the names given. Either way the seed is closed over sibling
    links (S-013) before anything is placed. Without `include_drafts` the closure runs over
    the shipped set and a draft anywhere in the request is a refusal (S-015); with it, a
    profile also seeds every draft, and a named set may reach drafts through its closure.
    """
    by_name = {d.name: d for d in all_skills}
    shipped, drafts = partition_drafts(all_skills)
    draft_names = {d.name for d in drafts}
    if only is not None:
        unknown = [n for n in only if n not in by_name]
        if unknown:
            return [], [], [f"no skill is named {n!r}" for n in unknown]
        named_drafts = [n for n in only if n in draft_names]
        if named_drafts and not include_drafts:
            return [], [], [f"{n!r} is marked a draft; pass --include-drafts to place it"
                             for n in named_drafts]
        pool = all_skills if include_drafts else shipped
        wanted = closure(only, {d.name: d for d in pool})
        skills = [d for d in pool if d.name in wanted]
        added = sorted(wanted - set(only))
        seed = None
    else:
        skills, added = resolve_profile(profile, shipped)
        seed = PROFILE_SEEDS[profile]
        if include_drafts:
            asked = {d.name for d in skills}
            wanted = closure(asked | draft_names, by_name)
            skills = [d for d in all_skills if d.name in wanted]
            added = sorted(set(added) | (wanted - asked - draft_names))
    if include_drafts:
        return skills, added, []
    return skills, added, draft_conflicts(skills, seed, draft_names)


def install(tools, mode, home: Path, dry: bool, profile: str = DEFAULT_PROFILE,
            with_hooks: bool = False, replace_adopted: bool = False,
            include_drafts: bool = False, only=None) -> int:
    # Resolved here and not only in `main()` (bug-0010), because every target below is
    # built from `home` and written verbatim into a persisted record. A relative spelling
    # records a string whose meaning depends on the reader's current directory, which
    # `bug-0009`'s normalisation cannot repair: there is no fixed path to normalise
    # toward. `install()` is a supported entry point (chore-0017), so the guarantee that a
    # recorded target is absolute belongs with the recording rather than with one caller.
    home = home.expanduser().resolve()
    all_skills = discover_skills()
    if not all_skills:
        print(f"No skills found under {SKILLS_DIR}.")
        return 0

    # Drafts are removed before the profile is resolved (S-015), so the closure that
    # keeps a profile sound (S-013) runs over the shipped set rather than around it,
    # unless `--include-drafts` asks for them (feat-0079).
    shipped, drafts = partition_drafts(all_skills)
    draft_names = {d.name for d in drafts}
    skills, added, problems = select_skills(all_skills, profile, only, include_drafts)
    request = (f"skills {', '.join(only)}" if only is not None else f"profile {profile!r}")

    if problems:
        print(f"Refusing to place anything for {request}: "
              + ("it collides with a draft marker, and every way through is wrong without "
                 "a person deciding." if only is None else "the request cannot be met."))
        for p in problems:
            print(f"  - {p}")
        if only is None:
            print("\nEither bless the draft by removing its marker, or mark the skill that "
                  "references it a draft too, or pass --include-drafts to place both. "
                  "Placing it would ship a reference to a skill this run did not place; "
                  "skipping the reference would ship the dangling sibling the closure "
                  "exists to prevent.")
        return 2

    placed_drafts = [d.name for d in skills if d.name in draft_names]
    if drafts and not include_drafts:
        print(f"{len(drafts)} skill(s) marked a draft are excluded from every profile, "
              f"including 'all': {', '.join(d.name for d in drafts)}. Pass "
              f"--include-drafts to try them.\n")
    if placed_drafts:
        print(f"Placing {len(placed_drafts)} draft skill(s) because --include-drafts was "
              f"given: {', '.join(placed_drafts)}. A draft is not shipped; it is placed so "
              f"a person can use it and decide whether to promote it.\n")
    if only is not None:
        print(f"Requested {len(only)} skill(s); with their closure over sibling links "
              f"this run places {len(skills)}: {', '.join(d.name for d in skills)}.\n")
    elif added:
        print(f"Profile {profile!r} was expanded to stay closed over sibling references: "
              f"{len(added)} skill(s) added ({', '.join(added)}). A skill that composes a "
              f"sibling is broken without it.\n")

    # Refusing to place anything is the stated choice for a damaged record (bug-0024).
    # The alternative, reading it as empty, is the documented behaviour for a *deleted*
    # manifest and would report CONFLICT for every target already there, which is a
    # defensible answer only when the tool genuinely knows nothing. Here it knows the
    # record exists and cannot be trusted, and proceeding would write a fresh manifest
    # over it, discarding whatever targets it recorded under other homes. That is the one
    # irreversible outcome available, so it is the one not taken.
    try:
        manifest = load_manifest()
    except ManifestError as exc:
        return report_unreadable_manifest(
            exc, "Nothing was placed: this run would have written a fresh record over "
                 "the damaged one, losing whatever it still records.")
    entries = {e["target"]: e for e in manifest["entries"]}
    conflicts = 0
    preserved_adopted = False
    tag = "[dry-run] " if dry else ""
    hooks = discover_hooks() if with_hooks else []
    if with_hooks and not hooks:
        print(f"--with-hooks was given but no hooks were found under {HOOKS_DIR}.\n")
    # Collected during placement rather than re-derived from `tools` afterwards, so the
    # activation note below is printed for exactly the tools that received a module
    # (bug-0048). The previous shape asked `"claude" in tools`, which is a different
    # question from "claude got the hooks" everywhere the two maps ever disagree.
    placed_hooks = []

    for tool in tools:
        base = home / TOOL_SUBPATHS[tool]
        if not dry:
            base.mkdir(parents=True, exist_ok=True)
        for src in skills:
            target = base / src.name
            render = renders_for(tool, src)
            # A rendered skill is always a copy: a link would show the unrendered source.
            placed_mode = "copy" if render else mode
            status = _place(src, target, placed_mode, dry, manifest)
            if status == "CONFLICT":
                conflicts += 1
            else:
                if render and not dry:
                    (target / "SKILL.md").write_bytes(rendered_skill_md(src))
                entries[str(target)] = {
                    "tool": tool, "name": src.name,
                    "target": str(target), "mode": placed_mode, "source": str(src),
                    "digests": expected_digests(src, tool),
                }
            marks = (["draft"] if src.name in draft_names else []) + \
                (["rendered: user-invoked"] if render else [])
            print(f"{tag}{status:9} {tool:8} {src.name}  -> {target}"
                  + (f"  ({'; '.join(marks)})" if marks else ""))

        for old, new in RENAMED_SKILLS.items():
            retired = base / old
            if str(retired) not in entries:
                continue  # never placed here by this tool: not ours to remove
            if not dry and (retired.is_symlink() or retired.exists()):
                _rm(retired)
            del entries[str(retired)]
            print(f"{tag}{'retired':9} {tool:8} {old}  ({retired}: renamed {new})")

        # The rules module, as the sibling <base>/../rules, so each skill's
        # ../../rules/<file>.md reference resolves in the installed layout too.
        #
        # Placed through `_place_adopted` and not `_place` (bug-0018): this is the one
        # module an adopter is invited to rewrite, so a re-run refreshes what they never
        # touched and leaves what they did. The previously recorded digests are the baseline
        # that separates the two, which is why they are read out of the existing entry
        # before it is overwritten.
        if RULES_DIR.is_dir():
            rules_target = base.parent / "rules"
            previous = entries.get(str(rules_target)) or {}
            recorded = previous.get("digests")
            # A real directory this tool did not place as a whole, or one it merged into
            # before, is merged into file by file (feat-0079). Refusing it whole left every
            # skill that composes a lens running without one, for the sake of protecting
            # files a per-file placement never touches.
            merging = rules_target.is_dir() and not rules_target.is_symlink() and (
                previous.get("mode") == "merged" or not is_managed(rules_target, manifest))
            if merging:
                status, digests, notes, clashes = _place_merged(
                    RULES_DIR, rules_target, dry, recorded or {}, replace_adopted)
                conflicts += clashes
                if digests:
                    entries[str(rules_target)] = {
                        "tool": tool, "name": "rules", "target": str(rules_target),
                        "mode": "merged", "source": str(RULES_DIR), "digests": digests,
                    }
                else:
                    # Nothing of the kit's is in there, so there is nothing to record.
                    entries.pop(str(rules_target), None)
            else:
                status, digests, notes = _place_adopted(
                    RULES_DIR, rules_target, mode, dry, manifest, recorded, replace_adopted)
                if status == "CONFLICT":
                    conflicts += 1
                else:
                    entries[str(rules_target)] = {
                        "tool": tool, "name": "rules",
                        "target": str(rules_target), "mode": mode,
                        "source": str(RULES_DIR), "digests": digests,
                    }
            if status == "preserved":
                preserved_adopted = True
            print(f"{tag}{status:9} {tool:8} rules  -> {rules_target}")
            for note in notes:
                # Named per file, not counted. A run that says it kept "1 file" leaves the
                # reader to go and find out which, which is the investigation the whole
                # report exists to save them.
                print(f"{tag}          {note}")

        # The hooks module, opt-in. Placed as the sibling <base>/../hooks, which for
        # Claude Code is the directory it already reads hooks from.
        if with_hooks and hooks and tool in HOOK_SUBPATHS:
            hooks_target = home / HOOK_SUBPATHS[tool]
            status = _place(HOOKS_DIR, hooks_target, mode, dry, manifest)
            if status == "CONFLICT":
                conflicts += 1
            else:
                entries[str(hooks_target)] = {
                    "tool": tool, "name": "hooks",
                    "target": str(hooks_target), "mode": mode, "source": str(HOOKS_DIR),
                    "digests": digest_tree(HOOKS_DIR),
                }
            print(f"{tag}{status:9} {tool:8} hooks  -> {hooks_target}")
            placed_hooks.append((tool, hooks_target))

    save_manifest(list(entries.values()), dry)
    if preserved_adopted:
        # Exit-neutral on purpose, matching how `--check` treats `revised`: an adopted file
        # this run left alone is news about the install, not a fault in it.
        print(f"\n{tag}The rules module is yours to edit, so files you changed were kept "
              f"rather than replaced. Nothing was merged: compare with `--check`, or pass "
              f"`--replace-adopted` to take the kit's copies and lose yours.")
    if conflicts:
        print(f"\n{conflicts} CONFLICT(s): a real file exists at those targets. "
              f"Move or remove them, then re-run.")
    if not RULES_DIR.is_dir():
        print(f"\nWARNING: no rules module at {RULES_DIR}. Skills that reference "
              f"../../rules/ (house-review's rubric, the house-style module) will "
              f"dangle in the installed layout.")
    # Over the shipped set, not everything discovered: a draft is placed by no profile,
    # so counting its description would report a budget no run can incur (S-015).
    budgets = profile_budgets(shipped)
    print(f"\n{tag}Done: {request}, {len(skills)} of {len(all_skills)} skill(s) "
          f"x {len(tools)} tool(s), plus the rules module"
          + (f", plus {len(hooks)} hook(s)." if hooks else "."))
    # One note per tool that received the module, rather than one note gated on Claude
    # Code (bug-0048). Both the "placed but INACTIVE" warning and the registration block
    # hung off the same `hooks and "claude" in tools` condition, so an opencode-only run
    # placed four hooks and said only how many, which is the "installed, correct-looking,
    # and doing nothing" failure feat-0038 hit twice arriving on the one path with no
    # warning attached. Every tool that gets files now gets a sentence about them, and
    # the sentences differ because the paths do: Claude Code's placement is complete and
    # unregistered, opencode's may be somewhere nothing reads.
    #
    # Every branch opens with "The hooks are placed", including the fallback, so the
    # invariant is countable: one note per tool that received the module. A two-case
    # enumeration with no fallback would re-open this very defect the day a third tool
    # joins HOOK_SUBPATHS without one, so the unknown case says it is unknown rather
    # than saying nothing. `test_every_tool_that_receives_the_module_is_told_about_it`
    # fails when that day arrives and the branch is not written.
    for placed_tool, placed_target in placed_hooks:
        if placed_tool == "claude":
            # Deliberately not done for the user.
            print(f"\n{tag}The hooks are placed but INACTIVE for claude. Nothing runs "
                  f"until you register them. Merge this into "
                  f"~/.claude/settings.json:\n")
            print(claude_registration(home))
            print(f"\nRemove that block to deactivate; `--uninstall` removes the files.")
        elif placed_tool == "opencode":
            print(f"\n{tag}{opencode_activation_note(home, placed_target)}")
        else:
            print(f"\n{tag}The hooks are placed at {placed_target} for {placed_tool}, "
                  f"and this installer does not know what reads them there or how to "
                  f"activate them. Check that tool's own hook wiring.")
    # A count, not a percentage: the harness budget scales with the context window and
    # is shared with skills this tool cannot see, so a proportion here would be invented.
    # The headline is what Claude Code loads, model-invoked descriptions only (feat-0094,
    # S-014 as amended); the user-invoked share is the aside below, because a reader takes
    # the first number away and the old headline overstated a session's cost.
    if only is None and not placed_drafts:
        print(f"{tag}Description budget: {budgets[profile]} characters for this profile, "
              f"what Claude Code loads: model-invoked only ("
              + ", ".join(f"{n}={budgets[n]}" for n in PROFILE_SEEDS) + ").")
    else:
        print(f"{tag}Description budget: {model_invoked_budget(skills)} characters for this "
              f"selection, what Claude Code loads: model-invoked only (profiles: "
              + ", ".join(f"{n}={budgets[n]}" for n in PROFILE_SEEDS) + ").")
    user_invoked = [d for d in skills if is_user_invoked(d)]
    if user_invoked:
        print(f"{tag}{sum(len(description_of(d)) for d in user_invoked)} character(s) more "
              f"belong to {len(user_invoked)} user-invoked skill(s) "
              f"({', '.join(d.name for d in user_invoked)}): Claude Code keeps them out of "
              f"context, so start one by name, as /<name>; OpenCode loads them.")
    # The second half of adopting the kit, which nothing used to mention: skills are
    # installed once per machine and configured once per repository (feat-0094; the
    # step itself is init-worktracking's, built by feat-0091).
    # Named only when this run places it: pointing an adopter at a skill they do not have
    # was the independent verifier's finding on the first version.
    if any(d.name == "init-worktracking" for d in skills):
        print(f"{tag}In each repository, run `init-worktracking` once to configure the skills "
              f"(docs/agents/zen.md).")
    else:
        print(f"{tag}Each repository is configured once by `init-worktracking`, and "
              f"`init-worktracking` is not in this selection: add it with "
              f"`--skills init-worktracking`.")
    # Printed on every run, because the whole point of the check is that nothing else
    # tells you the copy has gone stale: a reader who never learns the flag exists is in
    # the state chore-0031 was filed on.
    print(f"{tag}Run `python scripts/install.py --check` (with the same --home, if you "
          f"passed one) to see whether an installed set still matches this kit.")
    return 1 if conflicts else 0


def _place(src: Path, target: Path, mode: str, dry: bool, manifest) -> str:
    """Create one link/copy at target. Returns a status word."""
    if target.is_symlink():
        try:
            points_to = target.resolve()
        except OSError:
            points_to = None
        if mode == "symlink":
            if points_to == src.resolve():
                return "ok"
            # A link pointing anywhere else is relinked only when the record says this tool
            # made it, to a source it recorded (feat-0079). Relinking any same-named link
            # broke the "never clobbers" promise: a person's own link to their own skill
            # was silently repointed at the kit's.
            if not _recorded_link(target, points_to, manifest):
                return "CONFLICT"
            if not dry:
                target.unlink()
                _link(src, target)
            return "relinked"
        # copy mode but a symlink is there: ours only if it points exactly at our source
        if points_to == src.resolve():
            if not dry:
                target.unlink()
                _copy(src, target)
            return "updated"
        return "CONFLICT"

    if target.exists():
        if is_managed(target, manifest):
            if mode == "copy":
                if not dry:
                    _rm(target)
                    _copy(src, target)
                return "updated"
            if not dry:
                _rm(target)
                _link(src, target)
            return "relinked"
        return "CONFLICT"

    # nothing there
    if not dry:
        if mode == "symlink":
            _link(src, target)
        else:
            _copy(src, target)
    return "linked" if mode == "symlink" else "copied"


def _recorded_link(target: Path, points_to, manifest) -> bool:
    """Whether a link at `target` is one this tool recorded, pointing where it recorded.

    Both halves are needed. The record alone would let a person's link, made after this
    tool's was removed by hand, be repointed; the destination alone cannot be judged
    without the record, because a moved checkout leaves a link to a source that is gone.
    """
    if points_to is None:
        return False
    for entry in manifest["entries"]:
        if entry.get("target") == str(target) and entry.get("source"):
            try:
                if Path(entry.get("source")).resolve() == points_to:
                    return True
            except OSError:
                continue
    return False


def _place_adopted(src: Path, target: Path, mode: str, dry: bool, manifest,
                   recorded, replace: bool) -> tuple:
    """Place the adopted rules module without destroying what its adopter made theirs.

    Returns `(status, digests, notes)`: the status word to print, the digest map to record
    for this entry, and zero or more lines naming what the run declined to do.

    Why this exists at all (bug-0018). `_place` handles a managed target by removing it and
    copying the source back, which is right for a **derived** module and wrong for an
    **adopted** one. `.agents/rules/` is the module `AGENTS.md` calls swappable and
    `house-style.md` opens by inviting the reader to rewrite, so re-installing destroyed the
    one thing the kit specifically asks an adopter to own, silently and at exit 0. For a
    directory `_rm` took the whole tree, so a lens they *added* beside the kit's went too.
    `build-adapters.py` already got this right from a `dest.exists()` guard, and its
    contract states the reason as the contrast this function implements: supporting files
    are derived and are refreshed, a rules file is adopted and is preserved
    (`build-adapters.md` S-010 and S-014).

    Per file rather than per directory, for two reasons that pull the same way. A whole-tree
    verdict would refuse to deliver a lens the kit newly ships to anyone who edited any file
    in the module, and it cannot express the case the bug report singles out: a file the
    adopter added, which is neither the kit's to refresh nor the kit's to delete.

    The distinction is drawn against the **recorded baseline**, never against the source,
    and that is the whole design. A file differing from the recorded digest is the adopter's
    and is left alone; a file matching it differs only because the kit moved on, so it is
    ours to refresh. Deciding by "differs from the source" instead would preserve everything
    forever and pin every adopter to whatever shipped on the day they first installed, which
    is the inverse bug and just as silent. It is the same line `--check` already draws
    between `diverged` and `revised`.

    A preserved file keeps the digest previously recorded for it rather than taking the
    bytes now on disk. Recording what the adopter wrote would make the next run read their
    file as untouched and refresh over it, which is this same data loss delayed by one
    install. Keeping the baseline also lets `--check` keep answering the question it is for:
    the kit's copy has moved since you installed, and yours is yours.

    Only the copy path reaches here. In symlink mode the installed module *is* the kit's
    file, so there is no second copy to preserve and nothing to compare.
    """
    if (replace or mode != "copy" or target.is_symlink() or not target.exists()
            or not is_managed(target, manifest)):
        # Not a managed copy on disk, or the adopter has explicitly asked for the kit's.
        # `_place` keeps owning the CONFLICT rule (S-004), the fresh placement, and both
        # symlink branches: an unmanaged target is still refused rather than merged into.
        status = _place(src, target, mode, dry, manifest)
        return status, (None if status == "CONFLICT" else digest_tree(src)), []

    source = digest_tree(src)
    if not recorded:
        # The pre-digest case, exactly as in chore-0031: an install predating that change
        # recorded no baseline, so an edited file is indistinguishable from an untouched
        # one. The failure directions are not symmetric, so this preserves and says the
        # baseline is unknown. Falsiness rather than `is None`, matching `_check_entry`: a
        # `digests` map that is present but empty is no more of a baseline than a missing
        # one. Nothing is recorded either, because recording the source for files this run
        # did not place would claim a baseline that never existed.
        return "preserved", {}, [
            "no digest baseline was recorded for this install, so an edited file cannot be "
            "told from an untouched one: every file is left exactly as it is, and the "
            "baseline stays unknown.",
            "Run with --replace-adopted to take the kit's copy and record a baseline.",
        ]

    installed = digest_tree(target)
    digests = dict(recorded)
    placed, preserved, removed = [], [], []

    for rel in sorted(source):
        want, have, base = source[rel], installed.get(rel), recorded.get(rel)
        if have == want:
            digests[rel] = want                      # already exactly the kit's copy
        elif have is None and base is None:
            _copy_file(src / rel, target / rel, dry)  # new in the kit; nothing is at risk
            digests[rel] = want
            placed.append(rel)
        elif have == base:
            _copy_file(src / rel, target / rel, dry)  # untouched since we placed it
            digests[rel] = want
            placed.append(rel)
        elif have is None:
            # The digest goes with the file (bug-0022). Keeping it left the record asserting
            # a baseline for a file this very run has just said is gone, and nothing ever
            # reconciled the two, which is what let `--check` read that baseline forever. It
            # is not the "preserved file keeps its old baseline" property bug-0018 pinned:
            # that one is about a file the adopter *edited*, which is still on disk and
            # still has a baseline worth keeping.
            #
            # The seam this leaves open is stated rather than hidden: with no record of the
            # removal, a later run cannot tell this lens from one the adopter has never been
            # sent, so it places it. Remembering instead would need a tombstone in the
            # manifest, and the alternative is a deliberate deletion reported as divergence
            # on every check forever, which is noise aimed at exactly the people this
            # exemption was written for. Nothing of theirs is destroyed either way.
            preserved.append((rel, "you removed it, so this run does not restore it, and "
                                   "the record no longer claims it"))
            digests.pop(rel, None)
        elif base is None:
            preserved.append((rel, "yours, and the kit now ships a file of that name"))
        else:
            preserved.append((rel, "you edited it"))

    for rel in sorted(set(recorded) - set(source)):
        # The kit no longer ships this file. Removing it is only safe where the copy on
        # disk is provably the one this tool placed and nobody has touched it since.
        if installed.get(rel) == recorded[rel]:
            if not dry:
                (target / rel).unlink()
            removed.append(rel)
        elif rel in installed:
            preserved.append((rel, "you kept it after the kit dropped it"))
        digests.pop(rel, None)

    notes = [f"preserved {rel}: {why}" for rel, why in preserved]
    if placed:
        notes.append(f"refreshed {len(placed)} unmodified file(s): {', '.join(placed)}")
    if removed:
        notes.append(f"removed {len(removed)} unmodified file(s) the kit no longer ships: "
                     f"{', '.join(removed)}")
    if preserved:
        notes.append("Your copies are kept and the kit's are not merged in; that is a "
                     "person's call. Run with --replace-adopted to take the kit's instead.")
        return "preserved", digests, notes
    return ("updated" if placed or removed else "ok"), digests, notes


def _place_merged(src: Path, target: Path, dry: bool, recorded: dict,
                  replace: bool) -> tuple:
    """Merge the rules module into a directory this tool does not own whole (feat-0079).

    Returns `(status, digests, notes, conflicts)`. `digests` records only the files this
    tool placed, which is what `--uninstall` removes and `--check` compares; `conflicts`
    counts the files it refused.

    A file is the kit's only if the record says this tool placed it. Anything else at a
    lens's path is someone's, and is reported CONFLICT and left byte-for-byte alone (S-004
    per file), except a file already identical to the kit's, which is harmless and is left
    as theirs without a conflict and without being recorded. A file the adopter added
    under another name is never read. For a file this tool did place, the adopted rules of
    `_place_adopted` hold: untouched is refreshed, edited is kept, removed is not restored.
    """
    source = digest_tree(src)
    installed = digest_tree(target) if target.is_dir() else {}
    digests, placed, clashes, notes = {}, [], [], []
    for rel in sorted(source):
        want, have, base = source[rel], installed.get(rel), recorded.get(rel)
        if base is None:
            if have is None:
                _copy_file(src / rel, target / rel, dry)
                digests[rel] = want
                placed.append(rel)
            elif have == want:
                notes.append(f"kept {rel}: already there with the kit's exact content, "
                             f"so it stays yours and is not recorded")
            else:
                clashes.append(rel)
        elif have is None:
            notes.append(f"preserved {rel}: you removed it, so this run does not restore "
                         f"it, and the record no longer claims it")
        elif have == want:
            digests[rel] = want
        elif have == base or replace:
            _copy_file(src / rel, target / rel, dry)
            digests[rel] = want
            placed.append(rel)
        else:
            digests[rel] = base
            notes.append(f"preserved {rel}: you edited it")
    for rel in sorted(set(recorded) - set(source)):
        if installed.get(rel) == recorded[rel]:
            if not dry:
                (target / rel).unlink()
            notes.append(f"removed {rel}: the kit no longer ships it and it was untouched")
        elif rel in installed:
            notes.append(f"preserved {rel}: you kept it after the kit dropped it")
    for rel in clashes:
        notes.append(f"CONFLICT {rel}: a file this tool did not place is there; left "
                     f"unchanged, so skills that compose this lens read yours")
    if placed:
        notes.append(f"placed {len(placed)} file(s) into a directory this tool does not "
                     f"own whole: {', '.join(placed)}")
    return ("merged" if placed else "ok"), digests, notes, len(clashes)


def _link(src: Path, target: Path):
    try:
        os.symlink(src, target, target_is_directory=True)
    except (OSError, NotImplementedError) as e:
        raise SystemExit(
            f"symlink failed ({e}). On Windows, enable Developer Mode or run "
            f"with --mode copy.")


def _copy(src: Path, target: Path):
    # Byte-caches are not part of any module the kit distributes, and the hooks module
    # grows one as soon as the test suite imports it. Copying it would ship a stale .pyc
    # into an adopter's home for a source file that is about to be a symlink or a
    # different version.
    shutil.copytree(src, target, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))


def _copy_file(src: Path, target: Path, dry: bool):
    """Place one file, creating the directories above it. The per-file half of `_copy`.

    Needed because the adopted module is placed file by file (see `_place_adopted`), so
    `copytree` is the wrong granularity there: it would overwrite a whole directory to
    deliver one file.
    """
    if dry:
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, target)


def _rm(target: Path):
    if target.is_dir() and not target.is_symlink():
        shutil.rmtree(target)
    else:
        target.unlink()


def _beneath(target: str, home: Path) -> bool:
    """True when a recorded target lies under `home`.

    One manifest serves every home installed to from this checkout, because
    `install` merges into the existing record rather than replacing it. Reversal
    is therefore scoped here, per S-007 and S-012: without this, uninstalling a
    throwaway home also removes the user's real installation.

    Both sides are normalised first (bug-0009), because `is_relative_to` compares
    components as spelled. S-007 scopes reversal to a directory, not to one spelling
    of it, so a relative `home`, one carrying `..`, or one reached through a symlinked
    parent has to match the same recorded targets an absolute one does. Without that,
    such a caller matches nothing, every entry is classed as another home's, and the
    run reports success having removed nothing. `main()` resolves `--home`, so the CLI
    never hit this; `uninstall()` is a supported entry point (chore-0017) that callers
    and tests reach directly, and the guarantee belongs with the comparison rather
    than with one caller.

    The target's final component is deliberately left unresolved. In symlink mode
    every recorded target *is* a link this tool created, pointing back at its source
    in this checkout, so resolving it would place the target beneath no home at all.
    Its parent chain is safe to resolve and always contains `home`, which is what lets
    a symlinked home normalise identically on both sides.
    """
    try:
        t = Path(target)
        return (t.parent.resolve() / t.name).is_relative_to(home.resolve())
    except (OSError, ValueError):
        return False


def _home_of(target) -> Path:
    """The install home a recorded target sits under, derived from the path itself.

    A target is `<home>/.claude/skills/<name>` or `<home>/.claude/rules`, so the home is the
    parent of the first `.claude` or `.agents` component walking up. Derived rather than
    recorded because the manifest has never carried it, and a new key would be unreadable
    for every entry written before it.

    Falls back to the target's own parent when neither marker is present, which cannot match
    a home this tool placed into and so reads as "still there". That is the safe direction:
    the only thing this decides is whether `--check` calls an entry litter, and calling real
    litter live costs a line of output where the reverse invites deleting a live record.
    """
    target = Path(target)
    for parent in target.parents:
        if parent.name in (".claude", ".agents"):
            return parent.parent
    return target.parent


def uninstall(home: Path, dry: bool) -> int:
    try:
        manifest = load_manifest()
    except ManifestError as exc:
        return report_unreadable_manifest(
            exc, "Nothing was removed: the record names what this tool placed, and "
                 "removing files on the strength of a record it cannot read is exactly "
                 "the mistake to avoid.")
    if not manifest["entries"]:
        print("Nothing recorded as installed.")
        return 0

    mine = [e for e in manifest["entries"] if _beneath(e["target"], home)]
    others = [e for e in manifest["entries"] if not _beneath(e["target"], home)]

    tag = "[dry-run] " if dry else ""
    if not mine:
        print(f"Nothing recorded as installed beneath {home}.")
        if others:
            print(f"{len(others)} target(s) recorded under other homes are untouched.")
        return 0

    removed = 0
    # How many of `mine` have been dealt with, so the `finally` below can write a record
    # that matches the disk whatever happens in the loop (bug-0053). Writing the record once
    # after the loop is what let a failure part-way through lose every removal that had
    # already happened: the files were gone and the manifest still claimed them, which is
    # the over-claiming direction, and the next run reads that record to decide what it
    # placed. An entry is counted here whether it was removed or already gone, because
    # neither is installed any more and both leave the record.
    handled = 0
    try:
        for e in mine:
            target = Path(e["target"])
            # `.get()`, not subscription. `_validate_manifest()` requires only `target` and
            # treats `tool` and `name` as optional on purpose, so a record written by
            # another version of this tool is readable rather than corrupt-looking. This
            # function subscripted both and died on such a record *after* deleting its
            # target. `check()` already reads them this way; this is the third reader
            # agreeing with the other two. `(unnamed entry)` is the wording
            # `install-currency-reminder.py` uses for the same gap.
            label = f"{(e.get('tool') or '?'):8} {e.get('name') or '(unnamed entry)'}"
            if e.get("mode") == "merged" and target.is_dir() and not target.is_symlink():
                # Merged into a directory this tool does not own (feat-0079): remove only
                # the files it placed and nobody has edited since, never the directory.
                gone, kept = _unmerge(target, e.get("digests") or {}, dry)
                removed += 1
                print(f"{tag}removed   {label}  ({target}: {gone} file(s) this tool placed; "
                      f"the directory and everything else in it are kept)")
                for rel in kept:
                    print(f"{tag}          kept {rel}: edited since this tool placed it")
            elif target.is_symlink() or target.exists():
                if not dry:
                    _rm(target)
                removed += 1
                print(f"{tag}removed   {label}  ({target})")
            else:
                print(f"{tag}gone      {label}  ({target})")
            handled += 1
    finally:
        # `finally` rather than `except`: the record is made truthful and the failure still
        # surfaces. Swallowing an OSError from `_rm` would report a successful uninstall
        # over files that are still there, which is this defect inverted.
        save_manifest(others + mine[handled:], dry)
    print(f"\n{tag}Uninstalled {removed} target(s).")
    if others:
        print(f"{tag}Kept {len(others)} target(s) recorded under other homes.")
    return 0


def _unmerge(target: Path, digests: dict, dry: bool) -> tuple:
    """Remove the recorded, unedited files of a merged module. Returns (removed, kept)."""
    gone, kept = 0, []
    for rel, digest in sorted(digests.items()):
        path = target / rel
        if not path.is_file():
            continue
        if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            kept.append(rel)
            continue
        if not dry:
            path.unlink()
        gone += 1
    return gone, kept


def _compare(left: dict, right: dict, left_label: str = "installed",
             right_label: str = "source") -> list:
    """Every per-file disagreement between two digest maps.

    The labels are parameters because the two callers compare different things. The derived
    path really does hold a digest of the installed tree, but the adopted path passes the
    *recorded baseline*, and naming that "installed" printed a number matching nothing on
    disk: an adopter checksumming their own lens got a third value and no way to reconcile
    it. Reported by the automated reviewer on this pull request, which is the second time
    that reviewer has caught a class the local checks could not (see bug-0012).
    """
    problems = []
    for rel, digest in right.items():
        found = left.get(rel)
        if found is None:
            problems.append(f"{rel}: in the {right_label}, absent from the {left_label}")
        elif found != digest:
            problems.append(f"{rel}: {left_label} {found[:12]}, {right_label} {digest[:12]}")
    for rel in left:
        if rel not in right:
            problems.append(f"{rel}: in the {left_label}, absent from the {right_label}")
    return problems


def _check_entry(entry) -> tuple:
    """Classify one recorded target. Returns (status, message).

    status is one of `ok`, `linked`, `revised`, `diverged`, `unknown`, `error`, borrowing
    check-provenance.py's vocabulary rather than inventing a second one for the same idea.

    Three classifications are decisions rather than mechanics:

    - **`unknown`** for an entry carrying no recorded digests. The derived half of such an
      entry could be compared anyway, and deliberately is not: the adopted half cannot be
      answered without a baseline, and a per-entry verdict that reads `ok` while half of it
      is unanswerable is the clean-looking-but-partial result this check exists to remove.
      The status is one word, the remedy is not: an adopted entry is told to run
      `--replace-adopted`, because re-installing that one preserves it and records nothing.
    - **`linked`** for a target that is a symlink to its own source. It cannot be stale,
      because it *is* the source. Read from the filesystem rather than from the recorded
      `mode`, since a copy can replace a link between runs.
    - **`revised`** for the adopted rules module, where the question is not the derived
      one. A lens is the one file an adopter is invited to rewrite (`build-adapters.md`
      S-010 and S-014), so comparing their copy against the kit's is noise on every run for
      anyone who accepted the invitation. What is worth telling them is the other
      comparison: the kit's own copy has moved since they installed. That is
      check-provenance.py's question exactly, has the thing we copied *from* changed since
      we looked, and it is answerable only from the recorded baseline.
    """
    target = Path(entry.get("target", ""))
    source = Path(entry.get("source", ""))
    recorded = entry.get("digests")
    # Falsiness, not `is None`: a `digests` map that is present but empty is no more of a
    # baseline than a missing one, and treating it as valid let a hand-edited manifest
    # report `revised` at exit 0 for an entry nothing had been recorded for.
    if not recorded:
        # The remedy differs by kind, and only here (bug-0020). Re-installing a derived
        # entry does establish a baseline; re-installing an unrecorded adopted one
        # deliberately preserves every file and records nothing (bug-0018), so the adopter
        # follows the instruction, nothing changes, and the next run prints it again.
        # `--replace-adopted` is the one route to a baseline there. Asked of the entry name
        # for the reason the `revised` branch below asks it: the classification travels in
        # the record rather than being re-derived from a path.
        if entry.get("name") in ADOPTED_ENTRY_NAMES:
            return "unknown", ("installed before digests were recorded, so whether it is "
                               "current is unknown. A re-install preserves this module and "
                               "records nothing; run --replace-adopted to take the kit's "
                               "copy and establish a baseline.")
        return "unknown", ("installed before digests were recorded, so whether it is "
                           "current is unknown. Re-install to establish a baseline.")
    if not (target.exists() or target.is_symlink()):
        # Two ways to be gone, and they need different things from a reader (chore-0082).
        # A target missing from a home that is still there is a file somebody removed, and
        # re-installing restores it. A target whose whole home is gone is a record of an
        # install that no longer exists anywhere, usually a throwaway `--home` deleted
        # rather than uninstalled, and re-installing would recreate a tree nobody wants.
        # Reversal is scoped to `--home` by design (`S-007`, `S-012`), so `--uninstall` will
        # never reach it and it is counted `diverged` forever, inflating the one number a
        # person reads as a currency signal.
        if not _home_of(target).exists():
            return "diverged", (f"the installed target is gone, and so is the home it sat "
                                f"in, so this records an install that no longer exists "
                                f"anywhere: {target}")
        return "diverged", f"the installed target is gone: {target}"
    if not source.is_dir():
        return "error", (f"the kit no longer has a source at {source}, so the installed "
                         f"copy cannot be compared against anything.")
    tool = entry.get("tool", "")
    if target.is_symlink():
        try:
            same = target.resolve() == source.resolve()
        except OSError:
            same = False
        if same:
            if entry.get("name") not in ADOPTED_ENTRY_NAMES and \
                    (source / "SKILL.md").is_file() and renders_for(tool, source):
                # The source became user-invoked after this link was made. The link shows
                # the unrendered source, so Claude Code still loads its description.
                return "diverged", ("links to its source, but the skill is now user-invoked "
                                    "and Claude Code needs a rendered copy; re-install to "
                                    "replace the link with one")
            return "linked", "links to its source, so it cannot be stale"

    try:
        current = digest_tree(source)
    except OSError as exc:
        return "error", (f"the kit's source could not be read, so nothing can be compared "
                         f"against it: {exc}")
    if entry.get("name") in ADOPTED_ENTRY_NAMES:
        # Two independent questions, kept separable (bug-0022). The first is "has the kit's
        # copy moved since you installed", answerable only from the baseline. The second is
        # "is every file we placed still there", which needs the installed tree and which
        # nothing asked before: the comparison below ran the record against the source and
        # never opened the install, so whole-directory absence was caught a branch earlier
        # and per-file absence was caught by nothing at all. `_place_adopted` already names
        # a removed lens in plain words on the very next run, which is what makes the
        # silence here a defect rather than the exemption working as designed.
        #
        # The baseline, not the installed tree: naming it "installed" printed a digest
        # matching no file on disk (reported on this pull request).
        if entry.get("mode") == "merged":
            # A merged module records only the files this tool placed. A kit file sitting
            # on someone else's file was refused, not placed, so it is not news here.
            current = {rel: d for rel, d in current.items()
                       if rel in recorded or not (target / rel).exists()}
        moved = _compare(recorded, current, "recorded", "source now")
        try:
            installed = digest_tree(target)
        except OSError as exc:
            return "error", (f"the installed copy could not be read, so whether every "
                             f"file this install placed is still there is unanswerable: "
                             f"{exc}")
        # Absence only, never a digest mismatch. Reporting a changed file here would undo
        # the whole reason this branch exists: an adopter is invited to rewrite a lens, and
        # a file they edited is theirs. A missing file is a different claim, and it is the
        # only one being added. A file they *added* is absent from the baseline and so is
        # ignored in both directions, exactly as `_place_adopted` ignores it.
        missing = [rel for rel in sorted(recorded) if rel not in installed]
        if missing:
            # `diverged` rather than a new word, so the vocabulary stays one vocabulary:
            # this is the same claim the derived path already makes for a file it cannot
            # find, and it carries the exit code that claim already means. What is local to
            # the adopted module is the remedy, because re-installing does not bring the
            # file back, so the message says so rather than leaving the summary's generic
            # advice to mislead the one reader it is aimed at.
            lines = [f"      {rel}: this install placed it, and it is gone from the "
                     f"installed module" for rel in missing]
            if moved:
                lines.append("      and, separately, the kit's copy has moved since this "
                             "install:")
                lines.extend(f"      {p}" for p in moved)
            return "diverged", (
                "a file this install placed is missing from the adopted module:\n"
                + "\n".join(lines)
                + "\n      Deleting a lens is yours to do and nothing here restores it. "
                  "Re-install to have the removal recorded, after which this stops being "
                  "reported, or `--replace-adopted` to take the kit's copy back.")
        if not moved:
            return "ok", f"every file this install placed is still there, and the kit's "\
                         f"copy is unchanged since this install ({len(recorded)} file(s))"

        # The kit's copy has moved. Whether that is worth telling anyone depends on a
        # question this branch used to skip: did the adopter ever make this module theirs
        # (bug-0056)? Both states answered `revised` and said "yours is yours to keep", and
        # the currency hook excludes `revised` from what it reports on the stated ground
        # that firing on it would be crying wolf about a file the adopter was invited to
        # own. True of one state, false of the other, and the hook could not tell them apart
        # because this could not.
        #
        # The line is the one `_place_adopted()` already draws for placement: "A file
        # differing from the recorded digest is the adopter's and is left alone; a file
        # matching it differs only because the kit moved on, so it is ours to refresh."
        # `installed` is already in hand, digested a few lines up for the missing-file check.
        #
        # Only a file the kit actually *revised* can be stale, so the question is asked over
        # `changed` rather than over everything `moved` reports. `moved` also carries files
        # the kit newly ships and files it stopped shipping, and one of those is the
        # recorded-removal case `bug-0022` created: an adopter deletes a lens, the next
        # install drops its digest, and afterwards neither side claims it. That adopter
        # plainly made the module theirs, and nothing in a digest comparison can see it,
        # because both sides forgot the file. Asking only about `changed` leaves that case
        # where it belongs, at `revised` and exit 0.
        changed = sorted(rel for rel in recorded
                         if rel in current and current[rel] != recorded[rel])
        theirs = sorted(rel for rel in changed if installed.get(rel) != recorded[rel])
        if changed and not theirs:
            # Untouched, and out of date. Nothing here is the adopter's yet, so "yours is
            # yours to keep" describes a file they never made theirs, and `diverged` is both
            # true and already reported by the hook. Not a seventh verdict: `diverged`
            # already means the installed copy no longer matches this kit, which is exactly
            # the claim, and widening the vocabulary would cost a new concept for a
            # distinction the existing words carry.
            return "diverged", (
                "the kit's copy has changed since this install and yours is untouched, so "
                "nothing of yours is at stake and re-installing takes the change:\n"
                + "\n".join(f"      {p}" for p in moved))
        # Something in the module is theirs, so `revised` and its silence are right. The
        # counts are new: collapsing a module where one file was edited and two were not
        # into a single word tells the reader nothing about which files re-installing would
        # move, and that is the question they are about to have.
        if not changed:
            detail = (" Nothing the kit ships has been revised; what moved is a file added "
                      "or dropped, which re-installing reconciles.")
        elif len(theirs) < len(changed):
            detail = (f" Of the {len(changed)} file(s) the kit revised you have edited "
                      f"{len(theirs)} ({', '.join(theirs)}); the other "
                      f"{len(changed) - len(theirs)} are still as this install placed them, "
                      f"so re-installing would refresh those and leave yours alone.")
        else:
            detail = (f" You have edited every file the kit revised "
                      f"({', '.join(theirs)}), so re-installing changes nothing here.")
        return "revised", ("the kit's copy has changed since this install; yours is yours "
                           "to keep:\n" + "\n".join(f"      {p}" for p in moved) + "\n     "
                           + detail)

    if (source / "SKILL.md").is_file() and renders_for(tool, source):
        # A rendered copy is compared against what a re-install would place.
        current["SKILL.md"] = hashlib.sha256(rendered_skill_md(source)).hexdigest()
    try:
        problems = _compare(digest_tree(target), current)
    except OSError as exc:
        return "error", (f"the installed copy could not be read, so whether it is current "
                         f"is unanswerable: {exc}")
    if not problems:
        return "ok", f"{len(current)} file(s) match the source"
    return "diverged", ("DIVERGED from the source:\n"
                        + "\n".join(f"      {p}" for p in problems))


def check(home: Path) -> int:
    """Report every installed target beneath `home` that no longer matches its source.

    Detect and report, never rewrite. Re-installing is a person's decision, because an
    adopter may have edited an installed file on purpose and an overwrite destroys that
    without asking, which is the same call `feat-0043` made for adapted upstream material.

    Exit codes mirror check-provenance.py, including its precedence: an unanswerable run
    outranks a diverged one, since the first says the report itself cannot be trusted.

    0   every entry beneath this home matches its source, or cannot be stale
    1   at least one installed target has diverged from its source
    2   at least one entry has no baseline, or could not be compared at all, or the
        record itself could not be read
    """
    try:
        manifest = load_manifest()
    except ManifestError as exc:
        return report_unreadable_manifest(
            exc, "Nothing was checked, so this run makes no claim either way about "
                 "whether the installed skills are current.")
    scoped = [e for e in manifest["entries"] if _beneath(e["target"], home)]
    if not scoped:
        # Deliberately not zero. Nothing recorded is indistinguishable from a record that
        # was deleted (S-005), and reporting "current" for an install this tool cannot see
        # is exactly the silence chore-0031 removes.
        print(f"Nothing recorded as installed beneath {home}, so nothing can be checked.")
        print("If skills are installed there, the record is gone: re-install to "
              "establish a baseline.")
        return 2

    counts = {"ok": 0, "linked": 0, "revised": 0, "diverged": 0, "unknown": 0, "error": 0}
    # `counts` is keyed by status, and the unknown remedy is decided by kind (bug-0020).
    # Tracked in this loop rather than re-derived from the manifest afterwards, so the two
    # answers cannot drift apart.
    unknown_kinds = set()
    # Entries whose home is gone as well as their target. Counted apart from the rest of
    # `diverged` because the remedy is different and because they never leave the record on
    # their own: reversal is scoped to `--home`, so nothing prunes them.
    orphaned = []
    for entry in sorted(scoped, key=lambda e: (e.get("tool", ""), e.get("name", ""))):
        status, message = _check_entry(entry)
        counts[status] += 1
        if status == "diverged" and "so is the home it sat in" in message:
            orphaned.append(entry)
        if status == "unknown":
            unknown_kinds.add("adopted" if entry.get("name") in ADOPTED_ENTRY_NAMES
                              else "derived")
        print(f"{status:9} {entry.get('tool', ''):8} {entry.get('name', '')}  {message}")

    print(f"\n{counts['ok']} current, {counts['diverged']} diverged, "
          f"{counts['linked']} linked, {counts['revised']} revised upstream, "
          f"{counts['unknown']} unknown, {counts['error']} error(s).")
    if counts["diverged"] > len(orphaned):
        print("An installed copy no longer matches this kit. Re-install to refresh it, or "
              "keep your version: this check never rewrites anything.")
    if orphaned:
        print(f"{len(orphaned)} of those {counts['diverged']} record an install whose home "
              f"is gone too, so nothing is stale there and nothing will prune them: "
              f"--uninstall is scoped to --home and never reaches a home that no longer "
              f"exists. Remove them by hand, or re-run --uninstall with the same --home "
              f"before deleting one next time.")
    if counts["revised"]:
        print("An adopted file's source has moved since you installed. Your copy is left "
              "alone; merge the kit's change only if you want it.")
    if counts["unknown"]:
        print("An entry predates the digest baseline, so its state is unknown rather than "
              "current.")
        if "derived" in unknown_kinds:
            print("Re-install to establish one.")
        if "adopted" in unknown_kinds:
            print("The adopted rules module is among them, and re-installing it preserves "
                  "your files and records nothing: run --replace-adopted to establish a "
                  "baseline there.")
    if counts["error"] or counts["unknown"]:
        return 2
    return 1 if counts["diverged"] else 0


def main(argv=None) -> int:
    """Entry point. `argv` defaults to sys.argv[1:]; pass a list to drive it in a test.

    Wraps the real entry point so an undecodable file anywhere in the tree is reported
    as a diagnosis naming the file rather than as a traceback naming this tool
    (chore-0081).
    """
    try:
        return _main(argv)
    except NotUTF8 as exc:
        # Exit 2, could not run, rather than 1. Nothing was compared or placed: a file this
        # tool must read is not readable, which is a different claim from "the change is bad"
        # and is the distinction install.py --check and check-provenance.py already draw.
        print(f"Cannot read a file this run needs: {exc}", file=sys.stderr)
        return 2


def _main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Install the Zen Agent Skills library.")
    ap.add_argument("--dry-run", action="store_true", help="preview, write nothing")
    ap.add_argument("--uninstall", action="store_true", help="remove what was installed")
    ap.add_argument("--check", action="store_true",
                    help="report installed targets beneath --home that no longer match "
                         "their source; writes nothing")
    ap.add_argument("--mode", choices=["symlink", "copy"],
                    default="copy" if os.name == "nt" else "symlink",
                    help="link mode (default: copy on Windows, symlink elsewhere)")
    ap.add_argument("--tools", default="claude,opencode",
                    help="comma-separated subset of: " + ",".join(TOOL_SUBPATHS))
    ap.add_argument("--profile", default=None,
                    help="which skills to place: " + ", ".join(PROFILE_SEEDS)
                         + f" (default: {DEFAULT_PROFILE})")
    ap.add_argument("--skills", default=None,
                    help="comma-separated skill names to place, plus their closure over "
                         "sibling links; replaces --profile")
    ap.add_argument("--include-drafts", action="store_true",
                    help="also place skills marked metadata.status: draft, and say which "
                         "placed skills are drafts")
    ap.add_argument("--with-hooks", action="store_true",
                    help="also place .agents/hooks/ (opt-in: hooks run inside your "
                         "session, and stay inactive until you register them)")
    # Deliberately its own flag rather than a --mode value (bug-0018). --mode says how
    # files are placed; this says what happens to work an adopter did, which is a different
    # question and the destructive one.
    ap.add_argument("--replace-adopted", action="store_true",
                    help="overwrite the installed rules module with the kit's copy, "
                         "discarding your edits to it (by default an edited rules file is "
                         "preserved and reported)")
    ap.add_argument("--home", default=None,
                    help="override the base home dir (for testing/unusual setups)")
    args = ap.parse_args(argv)

    home = Path(args.home).expanduser().resolve() if args.home else Path.home()

    if args.check and args.uninstall:
        # Refused rather than ordered. Either precedence silently drops half of what was
        # asked for, and one of the two halves removes files.
        print("--check and --uninstall ask for different things; run them separately.")
        return 2
    if args.check:
        return check(home)
    if args.uninstall:
        return uninstall(home, args.dry_run)

    # De-duplicated, first mention wins, because a repeat is not a request to place twice.
    # `--tools claude,claude` used to run the whole placement loop once per mention and then
    # report "x 2 tool(s)", so the summary line disagreed with what a second run of the same
    # command would report. `dict.fromkeys` keeps the order the user typed, which the summary
    # and the per-target lines both read (chore-0038).
    tools = list(dict.fromkeys(t.strip() for t in args.tools.split(",") if t.strip()))
    bad = [t for t in tools if t not in TOOL_SUBPATHS]
    if bad:
        print(f"Unknown tool(s): {bad}. Choose from {list(TOOL_SUBPATHS)}.")
        return 2
    only = None
    if args.skills is not None:
        if args.profile is not None:
            print("--skills and --profile both say which skills to place; pass one.")
            return 2
        only = list(dict.fromkeys(n.strip() for n in args.skills.split(",") if n.strip()))
        if not only:
            print("--skills was given no skill names.")
            return 2
        for old in [n for n in only if n in RENAMED_SKILLS]:
            print(f"{old!r} was renamed {RENAMED_SKILLS[old]!r}; placing "
                  f"{RENAMED_SKILLS[old]!r}.")
        only = list(dict.fromkeys(RENAMED_SKILLS.get(n, n) for n in only))
    profile = args.profile or DEFAULT_PROFILE
    if profile not in PROFILE_SEEDS:
        print(f"Unknown profile: {profile!r}. Choose from {list(PROFILE_SEEDS)}.")
        return 2
    return install(tools, args.mode, home, args.dry_run, profile, args.with_hooks,
                   args.replace_adopted, args.include_drafts, only)


if __name__ == "__main__":
    raise SystemExit(main())
