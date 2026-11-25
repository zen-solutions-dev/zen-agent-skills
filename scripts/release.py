#!/usr/bin/env python3
"""Cut a release of the kit: bump the version, date the changelog, print the tag commands.

    python scripts/release.py --bump {major,minor,patch} [--date YYYY-MM-DD] [--dry-run]
    python scripts/release.py --version X.Y.Z [--date YYYY-MM-DD] [--dry-run]
    python scripts/release.py --check

Decision D5, "add tagged releases". Until this script, the kit had one tag (`v0.1.0`,
2026-07-29) and a release after it recorded in `CHANGELOG.md` as "Not tagged."

The one source of truth for the version
---------------------------------------
Before this script the kit carried no version a release could bump. The only version
strings were `PLUGIN_BASE_VERSION = "0.1.0"` in `build-adapters.py`, which exists to give
the generated Claude Code plugin a version string and is suffixed with a content digest,
and the `### v0.1.0 (2026-07-29)` heading in the changelog. Neither is a place a person
edits to say "this is release X".

So the version lives in a top-level `VERSION` file holding one semantic version,
`MAJOR.MINOR.PATCH`, and a trailing newline. Nothing else. Pre-release and build suffixes
are refused: the kit has never needed one, and a parser that accepts what nobody uses is a
parser whose edge cases nobody tests.

When `VERSION` is absent the current version is taken as `0.0.0`, and the run says so. The
changelog's released sections are a second floor: the new version must exceed the highest
`### vX.Y.Z` heading under `## Releases` as well, because without that, a first
`--bump minor` from an absent `VERSION` would produce `v0.1.0` a second time. A bump counts
from whichever of the two is higher, and says which.

What it writes
--------------
Two files, and only after every check has passed:

- `VERSION`, the new version.
- `CHANGELOG.md`, only its `## Releases` section. The first `### Unreleased...` heading in
  that section becomes `### vX.Y.Z (YYYY-MM-DD)`, keeping any subtitle after a colon and
  every line of its body, and a fresh empty `### Unreleased` heading goes above it. With no
  Unreleased section, an empty `### vX.Y.Z (date)` section is inserted with a placeholder
  line asking the maintainer to summarise it, and the run says so; an Unreleased section
  with an empty body gets the same placeholder. Every line outside the Releases section,
  the task log included, is left byte for byte as it was. Line endings are preserved.

What it never does
------------------
It never tags, pushes, commits, or runs any git command that writes. Tagging is the
person's step: the script prints the `git tag -a` and `git push` commands and says it ran
neither. It reads git at most twice (`git status --porcelain` to warn about uncommitted
changes, `git tag --list vX.Y.Z` to refuse a tag that already exists), and when git is
missing or the root is not a repository it says so and carries on. `--no-git` skips both.

`--dry-run` computes and prints everything, the changelog change as a unified diff, and
writes nothing. `--check` writes nothing either: it validates that `VERSION`, if present,
is a semantic version and that the changelog has a `### vX.Y.Z` section for it.

Exit codes
----------
    0   done (or, with --check, valid)
    1   refused: a malformed version or date, a version not greater than the current one,
        a version the changelog or git already records, a changelog with no
        `## Releases` heading
    2   could not run: a file missing, unreadable, not UTF-8, or not writable

The same precedence as `run-checks.py` and `install.py --check`: a run that could not read
its input produced no answer, which is a different fact from an answer of "no".

Standard library only, per the conventions section of `AGENTS.md`. Maintainer tooling: it
reaches no adopter tree.
"""
from __future__ import annotations

import argparse
import datetime
import difflib
import re
import subprocess
import sys
from pathlib import Path

# The same preamble as install.py: `_textio` is imported through the repository root so the
# one spelling works whether this file is run as a script or imported as a module.
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
from scripts._textio import decode_error_message   # noqa: E402

REPO_ROOT = _ROOT
SEMVER = re.compile(r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)")
RELEASES_HEADING = re.compile(r"##\s+Releases\s*")
H2 = re.compile(r"##\s")
H3 = re.compile(r"###\s")
UNRELEASED = re.compile(r"###\s+Unreleased\b[\s:]*(?P<subtitle>.*?)\s*", re.IGNORECASE)
RELEASED = re.compile(r"###\s+v(?P<version>\d+\.\d+\.\d+)\b")
PLACEHOLDER = "Summarise this release here before tagging it."

OK, REFUSED, CANNOT_RUN = 0, 1, 2


class Refused(Exception):
    """An input the script understood and declines to act on (exit 1)."""


class CannotRun(Exception):
    """An input the script could not read or write at all (exit 2)."""


def parse_version(text: str, where: str) -> tuple[int, int, int]:
    """`text` as a (major, minor, patch) triple, or `Refused` naming where it came from."""
    match = SEMVER.fullmatch(text.strip())
    if not match:
        shown = text.strip() or "(empty)"
        raise Refused(f"{where}: {shown!r} is not a semantic version MAJOR.MINOR.PATCH, "
                      f"for example 1.4.0 (no leading 'v', no suffix).")
    return tuple(int(part) for part in match.groups())


def fmt(version: tuple[int, int, int]) -> str:
    return ".".join(str(part) for part in version)


def bump(version: tuple[int, int, int], part: str) -> tuple[int, int, int]:
    major, minor, patch = version
    if part == "major":
        return (major + 1, 0, 0)
    if part == "minor":
        return (major, minor + 1, 0)
    return (major, minor, patch + 1)


def read_text(path: Path) -> str:
    """The file's text with its line endings untouched, or `CannotRun`."""
    try:
        with open(path, encoding="utf-8", newline="") as handle:
            return handle.read()
    except UnicodeDecodeError as exc:
        raise CannotRun(decode_error_message(path, exc)) from None
    except OSError as exc:
        raise CannotRun(f"{path}: could not be read ({exc.strerror or exc}).") from None


def write_text(path: Path, text: str) -> None:
    try:
        with open(path, "w", encoding="utf-8", newline="") as handle:
            handle.write(text)
    except OSError as exc:
        raise CannotRun(f"{path}: could not be written ({exc.strerror or exc}).") from None


def read_current(root: Path) -> tuple[tuple[int, int, int], str, str | None]:
    """(version, how it was found, the file's raw text or None when absent)."""
    path = root / "VERSION"
    if not path.exists():
        return (0, 0, 0), "VERSION is absent, so the current version is taken as 0.0.0", None
    raw = read_text(path)
    return parse_version(raw, str(path)), f"VERSION says {raw.strip()}", raw


def releases_span(lines: list[str], path: Path) -> tuple[int, int]:
    """Indexes of the `## Releases` heading line and of the line that ends its section."""
    start = next((i for i, line in enumerate(lines)
                  if RELEASES_HEADING.fullmatch(line.rstrip("\r\n"))), None)
    if start is None:
        raise Refused(f"{path}: no '## Releases' heading, so there is no section to date. "
                      f"Add one above the task log and run again.")
    end = next((i for i in range(start + 1, len(lines)) if H2.match(lines[i])), len(lines))
    return start, end


def released_versions(lines: list[str], start: int, end: int) -> list[tuple[int, int, int]]:
    found = []
    for line in lines[start + 1:end]:
        match = RELEASED.match(line)
        if match:
            found.append(tuple(int(p) for p in match.group("version").split(".")))
    return found


def line_ending(text: str) -> str:
    return "\r\n" if "\r\n" in text else "\n"


def date_changelog(text: str, path: Path, version: str, date: str) -> tuple[str, list[str]]:
    """The changelog with its Unreleased section dated as `version`, and notes on what changed."""
    lines = text.splitlines(keepends=True)
    start, end = releases_span(lines, path)
    eol = line_ending(text)
    notes = []
    heading = f"### v{version} ({date})"
    fresh = [f"### Unreleased{eol}", eol]

    unreleased = next((i for i in range(start + 1, end)
                       if UNRELEASED.fullmatch(lines[i].rstrip("\r\n"))), None)
    if unreleased is not None:
        subtitle = UNRELEASED.fullmatch(lines[unreleased].rstrip("\r\n")).group("subtitle")
        body_end = next((i for i in range(unreleased + 1, end) if H3.match(lines[i])), end)
        body = lines[unreleased + 1:body_end]
        new_heading = heading + (f": {subtitle}" if subtitle else "")
        replacement = fresh + [new_heading + eol]
        if any(line.strip() for line in body):
            replacement += body
            notes.append(f"Renamed the Unreleased section to '{new_heading}', keeping its text.")
        else:
            replacement += [eol, PLACEHOLDER + eol, eol]
            notes.append(f"The Unreleased section was empty: '{new_heading}' carries a "
                         f"placeholder line. Summarise the release there before tagging.")
        lines[unreleased:body_end] = replacement
    else:
        first_h3 = next((i for i in range(start + 1, end) if H3.match(lines[i])), None)
        at = first_h3 if first_h3 is not None else end
        block = fresh + [heading + eol, eol, PLACEHOLDER + eol, eol]
        if at > 0 and lines[at - 1].strip():
            block = [eol] + block
        if at == len(lines) and lines and not lines[-1].endswith(("\n", "\r")):
            lines[-1] += eol
        lines[at:at] = block
        notes.append(f"No Unreleased section was found: inserted an empty '{heading}' "
                     f"section with a placeholder line. Summarise the release there "
                     f"before tagging.")
    return "".join(lines), notes


def git_read(root: Path, *args: str) -> str | None:
    """Stdout of a read-only git command, or None when git is missing or it failed."""
    try:
        done = subprocess.run(["git", "-C", str(root), *args], capture_output=True,
                              text=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return None
    return done.stdout if done.returncode == 0 else None


def git_notes(root: Path, tag: str) -> list[str]:
    """Warnings from reading git. Raises `Refused` when the tag already exists."""
    existing = git_read(root, "tag", "--list", tag)
    if existing is None:
        return ["git could not be read here (not installed, or not a repository), so the "
                "working tree and existing tags were not checked."]
    if existing.strip():
        raise Refused(f"git already has a tag {tag}. Choose a higher version.")
    status = git_read(root, "status", "--porcelain")
    if status and status.strip():
        return ["The working tree has uncommitted changes. Commit the release on its own, "
                "so the tag names exactly the release."]
    return []


def next_steps(tag: str) -> str:
    return "\n".join([
        "Tagging is your step. This script did not tag, push, or commit, and ran no git "
        "command that writes. Once VERSION and CHANGELOG.md are committed and merged:",
        f'  git tag -a {tag} -m "Zen Agent Skills {tag}"',
        f"  git push origin {tag}",
    ])


def run_check(root: Path) -> int:
    version, how, raw = read_current(root)
    changelog = root / "CHANGELOG.md"
    text = read_text(changelog)
    if raw is None:
        print(f"{how}. Nothing to check against the changelog.")
        return OK
    lines = text.splitlines(keepends=True)
    start, end = releases_span(lines, changelog)
    if version not in released_versions(lines, start, end):
        raise Refused(f"{how}, but {changelog} has no '### v{fmt(version)}' section under "
                      f"'## Releases'.")
    print(f"{how}, and {changelog.name} has a section for v{fmt(version)}.")
    return OK


def run_release(args: argparse.Namespace, root: Path) -> int:
    if args.date:
        try:
            datetime.date.fromisoformat(args.date)
        except ValueError:
            raise Refused(f"--date: {args.date!r} is not a date YYYY-MM-DD.") from None
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", args.date):
            raise Refused(f"--date: {args.date!r} is not a date YYYY-MM-DD.")
        date = args.date
    else:
        date = datetime.date.today().isoformat()

    current, how, _raw = read_current(root)
    changelog = root / "CHANGELOG.md"
    text = read_text(changelog)
    lines = text.splitlines(keepends=True)
    start, end = releases_span(lines, changelog)
    released = released_versions(lines, start, end)
    floor = max(released, default=(0, 0, 0))
    print(f"{how}.")
    if released:
        print(f"The changelog's highest released section is v{fmt(floor)}.")

    base = max(current, floor)
    if args.version:
        new = parse_version(args.version, "--version")
    else:
        new = bump(base, args.bump)
        if base != current:
            print(f"Bumping from v{fmt(base)}, the changelog's, since it is higher.")
    if new <= base:
        raise Refused(f"v{fmt(new)} is not greater than v{fmt(base)}, the current version. "
                      f"A release must increase the version.")

    version, tag = fmt(new), f"v{fmt(new)}"
    warnings = [] if args.no_git else git_notes(root, tag)
    new_text, notes = date_changelog(text, changelog, version, date)

    print(f"Release {tag}, dated {date}.")
    for note in notes + warnings:
        print(f"Note: {note}")
    if args.dry_run:
        print("Dry run: nothing written. The changes would be:")
        print(f"  VERSION: {fmt(current) if _raw is not None else '(absent)'} -> {version}")
        diff = difflib.unified_diff(text.splitlines(), new_text.splitlines(),
                                    "CHANGELOG.md", "CHANGELOG.md (after)", n=1, lineterm="")
        for line in diff:
            print(f"  {line}")
    else:
        write_text(changelog, new_text)
        write_text(root / "VERSION", version + "\n")
        print(f"Wrote VERSION ({version}) and dated the changelog section.")
    print(next_steps(tag))
    return OK


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Bump the kit version, date the changelog, and print (never run) the "
                    "git tag and push commands.")
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--bump", choices=("major", "minor", "patch"),
                        help="which part of the current version to increase")
    action.add_argument("--version", metavar="X.Y.Z", help="release this exact version")
    action.add_argument("--check", action="store_true",
                        help="validate VERSION and its changelog section; write nothing")
    parser.add_argument("--date", metavar="YYYY-MM-DD", help="release date (default today)")
    parser.add_argument("--dry-run", action="store_true",
                        help="print what would change and write nothing")
    parser.add_argument("--no-git", action="store_true",
                        help="skip the read-only git checks (dirty tree, existing tag)")
    parser.add_argument("--root", type=Path, default=REPO_ROOT,
                        help="repository root holding VERSION and CHANGELOG.md")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        return run_check(root) if args.check else run_release(args, root)
    except Refused as exc:
        print(f"Refused: {exc}", file=sys.stderr)
        return REFUSED
    except CannotRun as exc:
        print(f"Could not run: {exc}", file=sys.stderr)
        return CANNOT_RUN


if __name__ == "__main__":
    sys.exit(main())
