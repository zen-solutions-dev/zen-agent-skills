#!/usr/bin/env python3
"""Generate thin per-harness adapters from each skill's SKILL.md.

Each SKILL.md is the single harness-agnostic source of truth. Claude Code and
OpenCode read that format natively (install.py places it for them). Cursor and
VS Code do not, so this generates their native equivalents by inlining the skill
body, so the same instructions travel without being hand-maintained twice.

Targets:
    cursor  -> <out>/.cursor/rules/<name>.mdc          (Cursor rule)
    vscode  -> <out>/.github/prompts/<name>.prompt.md   (VS Code / Copilot prompt)
    plugin  -> <out>/skills/<name>/SKILL.md             (Claude Code plugin tree)
    codex   -> <out>/.agents/skills/<name>/SKILL.md     (Codex, verbatim, plus its
               <out>/.agents/skills/<name>/agents/openai.yaml sidecar, generated)

    python scripts/build-adapters.py                    # cursor and vscode, into ./ (cwd)
    python scripts/build-adapters.py --target cursor --out ../my-project
    python scripts/build-adapters.py --target plugin --out .tmp/plugin

Inlining a body verbatim would break every relative link in it, because the
adapter does not sit where the skill sits. A skill references three things
outside its own file, and all three are rewritten and their targets emitted:

    ../<sibling>/SKILL.md  ->  <sibling><adapter-ext>, the adapter beside it
    ../../rules/<file>     ->  ../../.agents/rules/<file>, emitted once
    templates/<file>       ->  ../../.agents/skills/<name>/templates/<file>

A link inside an inline code span or a fenced code block is left alone, because it
renders as literal text: the skill is showing an example link rather than making
one, and repointing it would change what the body says (bug-0028).

Both adapter directories are two levels below <out>, so `../../` reaches the
project root from either, and the shared material has one location rather than
one per target. An existing <out>/.agents/rules/ file is never overwritten: that
module is swappable by design, so a project's own copy outranks this one.

The plugin target does not inline. Installing a plugin copies its directory, so
a path leaving that directory resolves to nothing at the installed location and
the emitted tree has to be self-contained. It is laid out to be exactly that:
each skill keeps its own directory under skills/, and the rules module sits
beside it at rules/. That is the same geometry the source tree already has, with
the .agents/ parent dropped, because a skill at .agents/skills/<name>/ reaching
../../rules/<file> lands on .agents/rules/<file> exactly as a skill at
skills/<name>/ reaching the same path lands on rules/<file>. Every source link
therefore resolves unchanged, so a skill is copied verbatim instead of rewritten
and nothing in the tree points outside it. The shared prefix is stated per target
rather than globally for this reason: the depth is the same, the .agents/ segment
is not.

The plugin target is opt-in rather than a default, because a default run writes
into a project root and a committed .claude-plugin/ there is the hand-maintained
second copy this generator exists to prevent.

Every write lands inside <out>. A skill's frontmatter `name` becomes a path
component of the two inlining destinations, so a `..` segment in one would walk
out of the output root and write wherever it landed (bug-0060). Two things stop
that: a `name` that is not the source directory's name is refused, which is the
rule validate-skills.py already states, and `_write` compares the resolved
destination against the resolved root for every file it places. Either refusal
fails the whole run with exit 2, in a preview as well as in a real run, rather
than skipping the skill and emitting the rest.

The name rule runs as a pre-pass over every discovered skill, before the first
file of the run is written, and it reports every offending skill rather than the
first one it meets (bug-0062). It used to be applied inside the emit loop, which
left every skill sorted ahead of the offender on disk, and the shared material
with them, under an output root that defaults to the working directory. Goal 6
of the contract is to fail clearly on an unusable invocation rather than write a
partial result, and only the first half of that was true.

Drafts and invocation (feat-0079, chore-0077). A skill marked `metadata.status:
draft` is emitted by no target unless `--include-drafts` is given, matching
install.py, so an adapter never hands a project a skill the kit has not blessed. A
shipped skill that links a draft refuses the run, for the reason install.py refuses
it: the link would dangle, and which side is wrong is a person's call. A skill
declaring `metadata.invocation: user` gains `disable-model-invocation: true` in the
plugin tree only, because Claude Code is the one harness that reads the key and
claude.ai rejects it; the Cursor and VS Code adapters are not changed.

The committed marketplace (feat-0079). `--marketplace` regenerates the Claude Code
marketplace this repository commits, so `claude plugin marketplace add
zen-solutions-dev/zen-agent-skills` works from a clean machine:

    .claude-plugin/marketplace.json          the catalog, one plugin entry
    .claude-plugin/plugin/                   the plugin tree, shipped skills only

The tree is generated, committed, and owned whole by this tool: a run replaces it
rather than merging into it. `--marketplace --check` writes nothing and exits 1
naming every file that differs from what a run would generate, which is the
`plugin tree` gate in run-checks.py. The plugin's version is generated from a digest
of the tree, so it changes exactly when the content does, and Claude Code sees an
update on the next `claude plugin update` or, with auto-update on, at startup.

    python scripts/build-adapters.py --marketplace           # regenerate, then commit
    python scripts/build-adapters.py --marketplace --check   # is the committed tree current?

Standard library only. Generated adapters are overwritten each run (they are
derived artifacts); do not hand-edit them, edit the SKILL.md instead.
"""
from __future__ import annotations

import argparse
import filecmp
import hashlib
import json
import os
import re
import shutil
import tempfile
from collections import namedtuple
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
    code_span_ranges, fenced_block_ranges, is_draft_text, is_user_invoked_text,
    render_for_claude, sibling_edges)

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / ".agents" / "skills"
RULES_DIR = REPO_ROOT / ".agents" / "rules"

BANNER = "<!-- generated from .agents/skills/{name}/SKILL.md by build-adapters.py. Do not edit here. -->"

# Where an inlined adapter reaches for material shared between skills. Both
# adapter directories are two deep, so this is the same string for both of them.
# It is not the same for every target: the plugin target is two deep as well but
# reaches `../../rules/`, with no .agents/ segment, which is why the shared
# location is a property of the target below rather than this constant alone.
SHARED = "../../.agents"

# Where each target's shared material lands under <out>. The two inlining targets
# flatten every skill into one directory and share one .agents/ tree; the plugin
# target keeps each skill's own directory and must be self-contained, so its
# shared material sits at the plugin root (see the module docstring).
Layout = namedtuple("Layout", "rules_dir assets_dir")
LAYOUTS = {
    "cursor": Layout(".agents/rules", ".agents/skills"),
    "vscode": Layout(".agents/rules", ".agents/skills"),
    "plugin": Layout("rules", "skills"),
    # Codex reads a skill directory as it is, so its target keeps the source geometry
    # under `.agents/`, the layout the two inlining targets already place their shared
    # material in: the three share one copy of it in one project.
    "codex": Layout(".agents/rules", ".agents/skills"),
}

# The plugin's published identity, and the one place to edit it. Both manifests
# are generated from this single mapping, so the marketplace entry cannot drift
# from the plugin it points at.
#
# The version is generated, not typed (feat-0079). Claude Code detects an update by
# comparing the plugin's version string with the one it installed, so a hand-pinned
# string holds every adopter on the old copy until someone remembers to bump it, and
# leaving it out (which versions by commit) fails `claude plugin validate --strict`.
# `plugin_version()` appends a digest of the emitted tree to PLUGIN_BASE_VERSION as
# semver build metadata, so the string changes exactly when the plugin's content does.
# Bump the base only to say something to a human reader.
PLUGIN_BASE_VERSION = "0.1.0"
REPO_URL = "https://github.com/zen-solutions-dev/zen-agent-skills"
PLUGIN = {
    "name": "zen-agent-skills",
    "description": "Portable, cross-harness agent skills for spec-driven work: "
                   "authoring specs and tasks, dispatching parallel agents, and "
                   "reviewing, testing, and documenting what they produce.",
    "author": {"name": "Zen Solutions", "url": "https://github.com/zen-solutions-dev"},
    "homepage": REPO_URL,
    "repository": REPO_URL,
    "license": "MIT",
    "keywords": ["skills", "agents", "spec-driven", "code-review", "documentation"],
}

# The committed marketplace: its catalog sits at the repository root's .claude-plugin/,
# which is where `claude plugin marketplace add <owner>/<repo>` looks, and the plugin it
# lists sits beneath it, because a plugin's own .claude-plugin/plugin.json has to be at
# the plugin's root and the repository root is not the plugin.
MARKETPLACE_DIR = REPO_ROOT / ".claude-plugin"
MARKETPLACE_PLUGIN_DIR = MARKETPLACE_DIR / "plugin"
MARKETPLACE_PLUGIN_SOURCE = "./.claude-plugin/plugin"

LINK_RE = re.compile(r"\]\(([^)\s]+)((?:\s+\"[^\"]*\")?)\)")
SIBLING_RE = re.compile(r"^\.\./([^/]+)/SKILL\.md(#.*)?$")
RULES_RE = re.compile(r"^\.\./\.\./rules/(.+)$")
EXTERNAL_PREFIXES = ("http://", "https://", "mailto:")
# Kept identical to validate-skills.py's copy. Two parsers that agree are bad; two
# that have drifted apart are worse, and this defect had to be found twice already.
BLOCK_SCALAR_RE = re.compile(r"^[|>][+-]?\s*")

# What renders as literal text, and which sibling links are install edges, is decided
# once in `_skillmeta.py` for this script, install.py and validate-skills.py (feat-0090).


class OutsideOutputRoot(Exception):
    """A write whose destination resolved outside the run's output root.

    Raised rather than printed at the point of detection, because the two facts a
    reader needs are known in two different places: `_write` sees the destination and
    the root, and only the caller knows which skill and which target produced them.
    """

    def __init__(self, dest: Path, root: Path):
        self.dest = dest
        self.root = root
        super().__init__(f"{dest} is not under {root}")


def rewrite_links(body: str, skill_name: str, ext: str) -> str:
    """Repoint a skill body's relative links so they resolve from the adapter.

    A link inside an inline code span or a fenced code block is emitted unchanged,
    exactly as an anchor or an external URL already is. It renders as literal text
    rather than as a link, so it is a skill *showing* an example rather than making
    one, and repointing it rewrites what the body says instead of where it points:
    the kit reads one way and every generated adapter reads another (bug-0028).
    Nothing fails when that happens. The adapter renders, the run reports success,
    and the only reader who finds out is one following a documented example in
    another repository.

    The excluded ranges are computed once for the whole body rather than once per
    link, because `re.sub()` calls the replacement for every match and the natural
    placement inside `repl` would rescan the body each time. That is the note
    bug-0023 left when it made the same change in `broken_links()`.
    """
    spans = code_span_ranges(body) + fenced_block_ranges(body)

    def repl(m: re.Match) -> str:
        # LINK_RE here anchors on `](` rather than on the link text's opening bracket,
        # so `m.start()` is the bracket that closes the text. It falls inside the same
        # span or fence as the opening one for any link a span or fence contains, and
        # keying on it leaves a link whose *text* is a code span (which is how most
        # links in this kit are written) correctly rewritten.
        if any(start <= m.start() < end for start, end in spans):
            return m.group(0)  # rendered as literal text, so it is an example, not a link

        target, title = m.group(1), m.group(2)

        def out(new: str) -> str:
            return f"]({new}{title})"

        if target.startswith("#") or target.lower().startswith(EXTERNAL_PREFIXES):
            return m.group(0)  # anchors and external URLs travel unchanged

        sibling = SIBLING_RE.match(target)
        if sibling:
            # The sibling's adapter is generated into this same directory.
            return out(f"{sibling.group(1)}{ext}{sibling.group(2) or ''}")

        rules = RULES_RE.match(target)
        if rules:
            return out(f"{SHARED}/rules/{rules.group(1)}")

        if target.startswith("../"):
            # Nothing else should escape the skill directory; validate-skills.py
            # fails the build on those, so leaving it unrewritten is honest.
            return m.group(0)

        # Skill-local supporting file (templates/, references/, scripts/).
        return out(f"{SHARED}/skills/{skill_name}/{target}")

    return LINK_RE.sub(repl, body)


def emit_rules_module(out: Path, dry: bool,
                      layout: Layout = LAYOUTS["cursor"]) -> list[Path]:
    """Place the rules module every emitted body shares. Returns what was written.

    Once per layout, which is what the module is: one copy shared by every skill,
    so that swapping it is one edit rather than one per skill. `layout` says where
    it lands for the requesting target; the rule it is treated by does not vary
    with the layout, only its destination.

    Once per layout is also what a real run has always produced, but it used to
    get there by accident. This loop ran once per skill and the second and later
    passes short-circuited on `dest.exists()`. A preview writes nothing, so that
    guard never became true and the preview counted the module once per skill: 74
    shared assets reported against the 17 a real run writes (bug-0025). Emitting
    it where it belongs removes the divergence instead of compensating for it, and
    matches what this docstring already claimed.

    A copy already in the target project is never overwritten (S-010, S-014). The
    module is swappable by design, so the project's own copy outranks the kit's.

    The module is copied and never passed through `rewrite_links()`, and that is a
    decision rather than an omission (bug-0044). A lens may link its sibling lenses,
    which sit beside it in every layout and therefore resolve everywhere unchanged.
    It may not link a skill: cursor and vscode share one Layout and one emitted copy
    of this module, while their adapters land at `.cursor/rules/<name>.mdc` and
    `.github/prompts/<name>.prompt.md` respectively, so no single rewritten target
    resolves for both, and a default run emits exactly one file that would have to
    serve them both. The lenses name skills in prose instead, which is the rule
    `autonomy.md` states about itself, and the walk in
    `TestEmittedRulesModuleResolves` is what keeps a link from creeping back in.
    """
    written = []
    if not RULES_DIR.is_dir():
        return written
    for src in sorted(RULES_DIR.rglob("*")):
        if not src.is_file():
            continue
        dest = out / layout.rules_dir / src.relative_to(RULES_DIR)
        if dest.resolve() == src.resolve() or dest.exists():
            continue  # same file, or the project already has its own
        if not dry:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
        written.append(dest)
    return written


def emit_skill_assets(skill_dir: Path, out: Path, dry: bool,
                      layout: Layout = LAYOUTS["cursor"]) -> list[Path]:
    """Place one skill's own supporting files. Returns what was written.

    Everything but the SKILL.md itself: the templates, references, and scripts an
    emitted body points at. Per skill, unlike the rules module beside it, and
    unconditionally: these are derived from the kit rather than adopted, so a
    re-run refreshes them (S-014).

    Byte-caches are excluded, by the same rule `install.py` filters them with
    (`_digestable`, and the ignore list `_copy` places with). A skill directory
    grows a `templates/__pycache__/` as soon as anything imports what is in it,
    which the test suite does, and the payload this places is meant to be a
    portable human-readable skill rather than one checkout's compiled bytecode
    (bug-0036). The directory half of the rule stands on its own: a future
    artefact inside `__pycache__` with some other suffix is still not part of the
    skill. Real `.py` files under `templates/`, such as the validator
    `init-worktracking` scaffolds, are unaffected and still emit.
    """
    written = []
    for src in sorted(skill_dir.rglob("*")):
        if not src.is_file() or src.name == "SKILL.md":
            continue
        rel = src.relative_to(skill_dir)
        if src.suffix == ".pyc" or "__pycache__" in rel.parts:
            continue
        dest = out / layout.assets_dir / skill_dir.name / rel
        if dest.resolve() == src.resolve():
            continue  # building into the kit itself; the file is already there
        if not dry:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
        written.append(dest)
    return written


def split_frontmatter(text: str):
    """Return (frontmatter_dict, body_text).

    A block-scalar indicator is dropped so an emitted `description` is the scalar's
    text and not its YAML serialisation. Four skills write `description: >-`, and
    without this every adapter for them opened with `description: ">- Turns ..."`,
    which is well-formed and wrong: valid YAML holding three characters of syntax
    (bug-0006). The same fix is in validate-skills.py's copy of this parser, which
    is where the duplication is the real problem.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return {}, text
    data = {}
    key = None
    for raw in lines[1:end]:
        m = re.match(r"^(\w[\w-]*):\s*(.*)$", raw)
        if m:
            key = m.group(1)
            value = m.group(2).strip().strip('"').strip("'")
            data[key] = BLOCK_SCALAR_RE.sub("", value, count=1)
        elif key and raw.strip():
            data[key] = (data[key] + " " + raw.strip()).strip()
    body = "\n".join(lines[end + 1:]).strip()
    return data, body


def discover_skills():
    if not SKILLS_DIR.is_dir():
        return []
    return sorted(d for d in SKILLS_DIR.iterdir()
                  if d.is_dir() and (d / "SKILL.md").is_file())


# Where each inlining target places a skill, as a function of the frontmatter `name`.
# One source of truth, because two callers need the same answer: the emitter that writes
# the file, and `_main`'s name refusal, which names a destination the rejected name would
# have produced (bug-0060). A refusal that reconstructed the path itself would drift into
# naming something this tool no longer emits, which is a confident citation pointing at
# nothing. `plugin` is absent deliberately rather than by oversight: it builds its
# destination from the source directory, so a `name` is never a path component there and
# there is no escaping path to show.
NAME_DESTINATIONS = {
    "cursor": lambda name, out: out / ".cursor" / "rules" / f"{name}.mdc",
    "vscode": lambda name, out: out / ".github" / "prompts" / f"{name}.prompt.md",
}


def emit_cursor(src: Path, name, desc, body, out: Path, dry: bool) -> Path:
    dest = NAME_DESTINATIONS["cursor"](name, out)
    content = (
        f"---\ndescription: {json.dumps(desc)}\nalwaysApply: false\n---\n\n"
        f"{BANNER.format(name=name)}\n\n{rewrite_links(body, name, '.mdc')}\n"
    )
    _write(dest, content, dry, out)
    return dest


def emit_vscode(src: Path, name, desc, body, out: Path, dry: bool) -> Path:
    dest = NAME_DESTINATIONS["vscode"](name, out)
    content = (
        f"---\nmode: agent\ndescription: {json.dumps(desc)}\n---\n\n"
        f"{BANNER.format(name=name)}\n\n{rewrite_links(body, name, '.prompt.md')}\n"
    )
    _write(dest, content, dry, out)
    return dest


def emit_plugin(src: Path, name, desc, body, out: Path, dry: bool) -> Path:
    """Place a skill in the plugin tree, verbatim.

    Nothing is rewritten and nothing is re-serialised, except that a user-invoked
    skill gains `disable-model-invocation: true` (feat-0079). The plugin layout keeps
    the geometry every source link is written for, so a rewrite would have to
    reproduce the path it was given; and round-tripping the frontmatter through
    this module's reader would drop any key it does not model and flatten any it
    does. The destination uses the source *directory* name rather than the
    frontmatter `name`, because `../<dir>/SKILL.md` is what a sibling link names.
    """
    dest = out / "skills" / src.name / "SKILL.md"
    text = read_text_utf8(src / "SKILL.md")
    rendered = render_for_claude(text)
    if rendered != text:
        # A user-invoked skill: the one change a Claude Code copy carries (feat-0079).
        _write(dest, rendered, dry, out)
        return dest
    if dry:
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src / "SKILL.md", dest)
    return dest


def marketplace_manifest(source: str) -> dict:
    """The marketplace catalog, listing the one plugin at `source`."""
    return {
        "name": PLUGIN["name"],
        "owner": PLUGIN["author"],
        "description": PLUGIN["description"],
        "plugins": [{
            "name": PLUGIN["name"],
            "source": source,
            "description": PLUGIN["description"],
            "category": "development",
            "homepage": PLUGIN["homepage"],
        }],
    }


def emit_plugin_manifests(out: Path, dry: bool, with_marketplace: bool = True) -> list[Path]:
    """Write the manifests a Claude Code plugin, and optionally its marketplace, need.

    Both are generated from PLUGIN, so the marketplace entry cannot drift from
    the plugin it points at. The marketplace written here lists exactly one plugin,
    whose source is the emitted root itself, which is what lets `--target plugin
    --out <dir>` be added as a local marketplace. The committed marketplace writes
    its own catalog one level up instead (see `build_marketplace`).
    """
    pairs = [("plugin.json", dict(PLUGIN, version=plugin_version(out)))]
    if with_marketplace:
        pairs.append(("marketplace.json", marketplace_manifest("./")))
    written = []
    for fname, obj in pairs:
        dest = out / ".claude-plugin" / fname
        _write(dest, json.dumps(obj, indent=2) + "\n", dry, out)
        written.append(dest)
    return written


def plugin_version(out: Path) -> str:
    """PLUGIN_BASE_VERSION plus a 12-character digest of the emitted skills and rules.

    Over relative paths and bytes, sorted by their case-sensitive parts, so it is the
    same on every platform for the same content. Sorting the paths themselves was not:
    `WindowsPath` orders case-insensitively, so `SKILL.md` and `references/` swapped
    places and Windows computed a different version for the same tree (feat-0080). The
    manifests are excluded, since they carry the version and so cannot be part of what
    it digests. A preview writes no tree, so a preview's version is the base's.
    """
    digest = hashlib.sha256()
    for top in ("skills", "rules"):
        root = out / top
        if not root.is_dir():
            continue
        for path in sorted(root.rglob("*"), key=lambda p: p.relative_to(out).parts):
            rel = path.relative_to(out)
            if not path.is_file() or "__pycache__" in rel.parts or path.suffix == ".pyc":
                continue
            # The name's bytes on disk, not a strict UTF-8 encoding of it: a name holding a
            # byte that is not UTF-8 reaches here as a surrogate escape, which `.encode`
            # refuses, and the whole run ended in a traceback (feat-0094, found by R-007's
            # test). For every valid UTF-8 name the two give the same bytes, so no
            # existing version changes.
            digest.update(os.fsencode(rel.as_posix()) + b"\0")
            digest.update(path.read_bytes() + b"\0")
    return f"{PLUGIN_BASE_VERSION}+{digest.hexdigest()[:12]}"


def draft_refusals(parsed: dict, emitted: list) -> list[str]:
    """One message per emitted skill that links a skill this run withholds as a draft.

    The same refusal install.py makes (install.md S-015), for the same reason: the
    emitted link would dangle, and dropping either side is a person's decision.
    """
    emitted_names = {d.name for d in emitted}
    held = {d.name for d in parsed if d.name not in emitted_names}
    messages = []
    for d in emitted:
        refs = sibling_edges(parsed[d][1])
        for ref in sorted(refs & held):
            messages.append(f"{d.name} links {ref!r} as a sibling, and {ref!r} is marked a "
                            f"draft, so the emitted link would dangle")
    return messages


def build_plugin_tree(out: Path, skills, parsed: dict) -> None:
    """Emit a complete plugin tree into `out`, which is assumed empty."""
    emit_rules_module(out, False, LAYOUTS["plugin"])
    for d in skills:
        fm, body = parsed[d]
        emit_plugin(d, fm.get("name", d.name), fm.get("description", ""), body, out, False)
        emit_skill_assets(d, out, False, LAYOUTS["plugin"])
    emit_plugin_manifests(out, False, with_marketplace=False)


def tree_differences(expected: Path, actual: Path) -> list[str]:
    """Every file that differs between two trees, as POSIX-relative paths with a reason."""
    def files(root):
        if not root.is_dir():
            return set()
        return {p.relative_to(root).as_posix() for p in root.rglob("*")
                if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"}
    want, have = files(expected), files(actual)
    problems = [f"{rel}: missing from the committed tree" for rel in sorted(want - have)]
    problems += [f"{rel}: in the committed tree, and no longer generated"
                 for rel in sorted(have - want)]
    problems += [f"{rel}: differs from what would be generated"
                 for rel in sorted(want & have)
                 if not filecmp.cmp(expected / rel, actual / rel, shallow=False)]
    return problems


def build_marketplace(skills, parsed: dict, check: bool, repo_root: Path = REPO_ROOT) -> int:
    """Regenerate, or with `check` compare, the committed Claude Code marketplace.

    Built into a temporary directory first, then either compared or swapped in whole, so
    a failure part-way never leaves a half-written committed tree, and a skill removed
    from the kit leaves the plugin too. Drafts are never included: the marketplace is
    what an adopter receives by default, and a draft is tried with install.py instead.
    """
    market_dir = repo_root / ".claude-plugin"
    plugin_dir = market_dir / "plugin"
    catalog = json.dumps(marketplace_manifest(MARKETPLACE_PLUGIN_SOURCE), indent=2) + "\n"
    with tempfile.TemporaryDirectory() as tmp:
        staged = Path(tmp) / "plugin"
        staged.mkdir()
        build_plugin_tree(staged, skills, parsed)
        if check:
            problems = tree_differences(staged, plugin_dir)
            catalog_path = market_dir / "marketplace.json"
            have = catalog_path.read_bytes() if catalog_path.is_file() else None
            if have != catalog.encode("utf-8"):
                problems.insert(0, "../marketplace.json: differs from what would be "
                                   "generated" if have is not None
                                else "../marketplace.json: missing")
            if problems:
                print(f"The committed marketplace under {market_dir} is out of date "
                      f"({len(problems)} file(s)):")
                for p in map(_printable, problems):
                    print(f"  .claude-plugin/plugin/{p}" if not p.startswith("../")
                          else f"  .claude-plugin/{p[3:]}")
                print("Regenerate it with `python scripts/build-adapters.py --marketplace` "
                      "and commit the result.")
                return 1
            print(f"The committed marketplace is current: {len(skills)} skill(s) in "
                  f".claude-plugin/plugin/, and .claude-plugin/marketplace.json.")
            return 0
        market_dir.mkdir(parents=True, exist_ok=True)
        if plugin_dir.exists():
            shutil.rmtree(plugin_dir)
        shutil.copytree(staged, plugin_dir)
    (market_dir / "marketplace.json").write_text(catalog, encoding="utf-8", newline="")
    print(f"Regenerated the committed marketplace: {len(skills)} skill(s) in "
          f".claude-plugin/plugin/, and .claude-plugin/marketplace.json. Commit both.")
    return 0


def _printable(name: str) -> str:
    """A path for a report line, with any byte that is not UTF-8 shown as an escape.

    A name holding such a byte arrives as a surrogate escape, and printing it to a strict
    UTF-8 stream raises, which ended `--marketplace --check` in a traceback instead of the
    report it exists to give (feat-0094, found by `tests/test_undecodable_names.py`).
    """
    return name.encode("utf-8", "backslashreplace").decode("utf-8")


def _write(dest: Path, content: str, dry: bool, root: Path):
    """Write `content` to `dest`, which must resolve inside `root`.

    The containment check sits here rather than in each emitter because this is the
    one place every emitted file passes through, so a target added later inherits it
    instead of restating it (bug-0060). It is needed because a skill's frontmatter
    `name` becomes a path component in both inlining emitters, and a `..` segment in
    one walks straight out of the output root: `_main` refuses such a name before it
    dispatches an emitter, and this is the boundary that holds whatever gets past
    that. `emit_plugin_manifests` passes destinations this module builds itself, so
    the check is silent there by construction.

    Both sides are resolved, because the escape is a `..` segment that exists only
    before resolution and `is_relative_to` on unresolved paths compares the spelling
    rather than the location. `root` is resolved again here even though `_main`
    already resolved it, so the guarantee belongs to this function rather than to its
    callers remembering.

    The check runs *before* the `dry` early return, deliberately. A preview that
    reports a destination the real run would refuse is misleading, and the adapters
    gate in `run-checks.py` is a `--dry-run`, so a check behind that branch would
    never fire in the one place this repository actually exercises the tool.
    """
    resolved = dest.resolve()
    root = root.resolve()
    if not resolved.is_relative_to(root):
        raise OutsideOutputRoot(resolved, root)
    if dry:
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    # `newline=""` disables newline translation, so the bytes on disk are exactly the
    # newlines in `content` (LF) rather than the platform default, which is CRLF on
    # Windows. Emitted adapters are untracked, so nothing is broken today; the point is
    # that a writer whose line endings vary by platform is the shape that makes a
    # digest comparison answer differently on Windows than on Linux.
    dest.write_text(content, encoding="utf-8", newline="")


# The Codex sidecar (E7, feat-0103). Codex reads an optional `agents/openai.yaml` inside a
# skill directory for how its app shows the skill and whether the model may invoke it on
# its own. It is derived here from SKILL.md, never written by hand: `display_name` is the
# skill's name, `short_description` the first sentence of its description, and a skill
# declaring `metadata.invocation: user` gets `allow_implicit_invocation: false`, the
# Codex spelling of what `disable-model-invocation: true` says to Claude Code.
#
# Source, read 2026-11-25: OpenAI's "Build skills" page, https://learn.chatgpt.com/docs/
# build-skills (where developers.openai.com/codex/skills redirects), in part only as a
# summary of the page. It names `interface.display_name`, `interface.short_description`
# and `policy.allow_implicit_invocation` ("When false, Codex won't implicitly invoke the
# skill based on user prompt; explicit $skill invocation still works"; default true), and
# says Codex reads skills from `.agents/skills` up to the repository root and from
# `$HOME/.agents/skills`. It states no length limit: CODEX_SHORT_MAX is this kit's own
# choice, to keep a one-line label one line. Icons, colours, a default prompt and tool
# dependencies are not emitted, since SKILL.md carries none of them.
CODEX_SIDECAR = Path("agents") / "openai.yaml"
CODEX_SHORT_MAX = 120


def _yaml_string(value: str) -> str:
    """A double-quoted YAML scalar: every character that could end or escape it escaped."""
    escaped = (value.replace("\\", "\\\\").replace('"', '\\"')
               .replace("\n", "\\n").replace("\t", "\\t"))
    return f'"{escaped}"'


def short_description(description: str, limit: int = CODEX_SHORT_MAX) -> str:
    """The description's first sentence, cut at a word boundary to at most `limit`."""
    text = " ".join(description.split())
    first = re.split(r"(?<=[.!?])\s", text, maxsplit=1)[0]
    if len(first) <= limit:
        return first
    cut = first[:limit - 3].rsplit(" ", 1)[0].rstrip(",;:")
    return cut + "..."


def codex_sidecar(name: str, description: str, user_invoked: bool) -> str:
    """The text of a skill's `agents/openai.yaml`."""
    lines = [f"# generated from .agents/skills/{name}/SKILL.md by build-adapters.py. "
             f"Do not edit here.",
             "interface:",
             f"  display_name: {_yaml_string(name)}",
             f"  short_description: {_yaml_string(short_description(description))}"]
    if user_invoked:
        lines += ["policy:", "  allow_implicit_invocation: false"]
    return "\n".join(lines) + "\n"


def emit_codex(src: Path, name, desc, body, out: Path, dry: bool) -> Path:
    """Place a skill for Codex: SKILL.md verbatim, plus its generated sidecar.

    The supporting files are placed by `emit_skill_assets` under the same layout. When
    `out` is the kit itself, the SKILL.md is its own source and is left alone, and no
    sidecar is written into the source tree: Codex reads the source directly there, and
    a generated file among the sources is the hand-maintained copy this tool prevents.
    """
    skill_dir = out / LAYOUTS["codex"].assets_dir / src.name
    if skill_dir.resolve() == src.resolve():
        return skill_dir / "SKILL.md"
    text = read_text_utf8(src / "SKILL.md")
    _write(skill_dir / "SKILL.md", text, dry, out)
    sidecar = skill_dir / CODEX_SIDECAR
    _write(sidecar, codex_sidecar(name, desc, is_user_invoked_text(text)), dry, out)
    return sidecar


EMITTERS = {"cursor": emit_cursor, "vscode": emit_vscode, "plugin": emit_plugin,
            "codex": emit_codex}


def name_refusals(named_skills, targets, out: Path, tag: str = "") -> list[str]:
    """One refusal message per skill whose frontmatter `name` is not its directory.

    `named_skills` is `(skill_dir, name)` pairs, in discovery order. An empty list
    means the tree is usable, which is the only thing `_main` proceeds on.

    Two properties, and neither is the rule itself. The rule is validate-skills.py's,
    borrowed rather than moved (bug-0060), and it is applied here exactly as it was
    applied per skill before.

    The first is *when*. `_main` calls this over every discovered skill before it
    writes anything at all, so an unusable tree leaves nothing behind rather than
    everything sorted ahead of the first offender, plus the shared rules module that
    is placed before the loop even begins (bug-0062).

    The second is *how much*. Every offender is reported rather than the first, so one
    run tells an adopter the whole set to fix instead of one name per run. That is why
    this returns a list and prints nothing: the caller decides how a refusal is shown,
    and this is the only place that knows how many there are.

    `_write`'s containment check is unaffected and stays where it is. This is a second
    line of defence in front of that boundary rather than a replacement: it covers the
    names that become path components, and the boundary covers every destination,
    including whatever a rule about names does not reach.
    """
    # One destination is shown rather than one per requested target, and it is read
    # from NAME_DESTINATIONS rather than rebuilt here: a refusal that reconstructed the
    # path would drift into naming something this tool no longer emits, which is a
    # confident citation pointing at nothing. Computed once, because it depends on the
    # requested targets and not on the skill.
    shown = next((t for t in targets if t in NAME_DESTINATIONS), None)
    messages = []
    for skill_dir, name in named_skills:
        if name == skill_dir.name:
            continue
        if shown is None:
            # A plugin-only run. Nothing requested derives a path from `name`, so there
            # is no destination to show and inventing one would be false.
            where = ("No requested target derives a destination from it, so nothing "
                     f"would leave the output root {out}")
        else:
            # The message names a destination and not only the root, because the root
            # alone leaves a reader unable to see that the name escapes at all, which
            # is the fact that carries the severity. It is one target's destination out
            # of however many were requested, so it is labelled representative rather
            # than offered as the only one. No emitter is dispatched to obtain it.
            would_be = NAME_DESTINATIONS[shown](name, out).resolve()
            side = "inside" if would_be.is_relative_to(out) else "outside"
            where = (f"Representative, for target {shown!r}: {would_be}, {side} the "
                     f"output root {out}")
        messages.append(
            f"{tag}Refusing to emit skill {skill_dir.name!r}: frontmatter name "
            f"{name!r} != directory {skill_dir.name!r}, and that name becomes a path "
            f"component of every inlining target's destination. {where}. Fix the "
            f"SKILL.md frontmatter; validate-skills.py states the same rule.")
    return messages


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
    except OutsideOutputRoot as exc:
        # The backstop for any write `_main` does not wrap with the skill it belongs to.
        # Exit 2 for the same reason as above: nothing was placed, so the report is
        # incomplete rather than the input bad. A traceback here would name this tool
        # instead of the path that was refused.
        #
        # It is unreachable today, and kept anyway. `emit_plugin_manifests` is the only
        # `_write` caller outside `_main`'s try, and it builds its destination from `out`
        # itself, so that call cannot escape and nothing else can raise past `_main`. Do
        # not write a test for this arm: it would be a test for dead code. It earns its
        # place when the next `_write` caller lands outside that try, which is exactly
        # when a traceback would otherwise reach a user.
        print(f"Refusing to write outside the output root: {exc.dest} is not under "
              f"{exc.root}.", file=sys.stderr)
        return 2


def _main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Generate per-harness skill adapters.")
    ap.add_argument("--target", default="cursor,vscode",
                    help="comma-separated subset of: " + ",".join(EMITTERS)
                         + " (default: cursor,vscode; plugin is opt-in, because a "
                           "default run writes into a project root)")
    ap.add_argument("--out", default=".", help="output project root (default: cwd)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--include-drafts", action="store_true",
                    help="also emit skills marked metadata.status: draft (excluded by "
                         "default, matching install.py)")
    ap.add_argument("--marketplace", action="store_true",
                    help="regenerate the committed Claude Code marketplace under "
                         ".claude-plugin/ (shipped skills only); ignores --target and --out")
    ap.add_argument("--check", action="store_true",
                    help="with --marketplace: write nothing, exit 1 if the committed tree "
                         "differs from what would be generated")
    args = ap.parse_args(argv)

    if args.check and not args.marketplace:
        print("--check compares the committed marketplace; pass it with --marketplace.")
        return 2
    if args.marketplace:
        if args.include_drafts or args.dry_run:
            print("--marketplace ships shipped skills only and has its own --check; "
                  "--include-drafts and --dry-run do not apply.")
            return 2
        every = discover_skills()
        parsed = {d: split_frontmatter(read_text_utf8(d / "SKILL.md")) for d in every}
        refusals = name_refusals(((d, fm.get("name", d.name)) for d, (fm, _) in parsed.items()),
                                 ["plugin"], MARKETPLACE_PLUGIN_DIR)
        texts = {d: read_text_utf8(d / "SKILL.md") for d in every}
        shipped = [d for d in every if not is_draft_text(texts[d])]
        refusals += draft_refusals(parsed, shipped)
        if refusals:
            for message in refusals:
                print(message)
            print("Refusing to build the marketplace. Nothing was written.")
            return 2
        return build_marketplace(shipped, parsed, args.check)

    targets = [t.strip() for t in args.target.split(",") if t.strip()]
    bad = [t for t in targets if t not in EMITTERS]
    if bad:
        print(f"Unknown target(s): {bad}. Choose from {list(EMITTERS)}.")
        return 2

    out = Path(args.out).expanduser().resolve()
    discovered = discover_skills()
    if not discovered:
        print(f"No skills found under {SKILLS_DIR}.")
        return 0
    # Drafts are withheld unless asked for (chore-0077, feat-0079), matching install.py.
    texts = {d: read_text_utf8(d / "SKILL.md") for d in discovered}
    drafts = [d for d in discovered if is_draft_text(texts[d])]
    skills = discovered if args.include_drafts else [d for d in discovered if d not in drafts]

    # Targets sharing a layout share one copy of the shared material, so cursor
    # and vscode together still emit it once. A layout is per target, so asking
    # for cursor and plugin emits it into both trees.
    layouts = []
    for t in targets:
        if LAYOUTS[t] not in layouts:
            layouts.append(LAYOUTS[t])

    tag = "[dry-run] " if args.dry_run else ""

    # Every SKILL.md is read and parsed here, before anything is dispatched or placed,
    # and the result is carried into the loop below. Two reasons, both bug-0062. The
    # name rule has to be applied to the whole set before the first write, and the first
    # write of a run belongs to emit_rules_module() rather than to the loop, so a check
    # merely hoisted to the top of the loop would still leave the shared module behind.
    # And reading each file once means an undecodable SKILL.md is reported once, by the
    # one read, rather than giving two chances to describe the same failure differently.
    parsed = {d: split_frontmatter(texts[d]) for d in discovered}

    refusals = name_refusals(((d, parsed[d][0].get("name", d.name)) for d in skills),
                             targets, out, tag)
    refusals += [f"{tag}Refusing: {m}. Pass --include-drafts, or bless the draft."
                 for m in draft_refusals(parsed, skills)]
    if refusals:
        for message in refusals:
            print(message)
        # The whole set, and the assurance that goes with refusing before writing. An
        # adopter reading one refused run learns every name to fix and that the tree it
        # ran against is untouched, which for a default run is the working directory.
        print(f"{tag}Refusing the whole run: {len(refusals)} of {len(skills)} skill(s) "
              f"named above. No file was written under {out}.")
        return 2

    if drafts and not args.include_drafts:
        print(f"{tag}{len(drafts)} draft skill(s) withheld: "
              f"{', '.join(d.name for d in drafts)}. Pass --include-drafts to emit them.\n")
    elif drafts:
        print(f"{tag}Emitting {len(drafts)} draft skill(s) because --include-drafts was "
              f"given: {', '.join(d.name for d in drafts)}.\n")

    n = 0
    # The rules module is one copy shared by every skill, so it is emitted per
    # layout and outside the per-skill loop. Inside it, a preview counted it once
    # per skill (bug-0025); see emit_rules_module().
    assets = sum(len(emit_rules_module(out, args.dry_run, layout))
                 for layout in layouts)
    for d in skills:
        fm, body = parsed[d]
        name = fm.get("name", d.name)
        desc = fm.get("description", "")
        for t in targets:
            try:
                dest = EMITTERS[t](d, name, desc, body, out, args.dry_run)
            except OutsideOutputRoot as exc:
                # The boundary at `_write` fired, so the name check above did not cover
                # this destination. Reported with the skill and the target, which are
                # known here and not there.
                print(f"{tag}Refusing to emit skill {d.name!r} for target {t!r}: "
                      f"destination {exc.dest} is outside the output root {exc.root}.")
                return 2
            print(f"{tag}{t:7} {name}  -> {dest.relative_to(out) if dest.is_relative_to(out) else dest}")
            n += 1
        # The emitted bodies point at these; without them the links dangle.
        for layout in layouts:
            assets += len(emit_skill_assets(d, out, args.dry_run, layout))

    manifests = emit_plugin_manifests(out, args.dry_run) if "plugin" in targets else []
    for dest in manifests:
        print(f"{tag}{'plugin':7} manifest  -> {dest.relative_to(out)}")

    roots = ", ".join(sorted({Path(p).parts[0] + "/"
                              for layout in layouts for p in layout}))
    print(f"\n{tag}Generated {n} adapter file(s) for {len(skills)} skill(s), "
          f"plus {assets} shared asset file(s) under {roots}.")
    if manifests:
        print(f"{tag}Generated {len(manifests)} plugin manifest file(s) "
              f"under .claude-plugin/.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
