#!/usr/bin/env python3
"""Run every gate that decides whether a change to this repository is acceptable.

One command, one exit code, no flags. This exists because until now the seven gates
lived only as seven separate steps in .github/workflows/checks.yml, so the only ways to
get the answer were to push and read CI, or to run seven commands by hand and remember
all seven. Measured 2026-08-07: the 97 acceptance chains across .quests/ and .quests/done/
run one, two, three, or five commands, and none of them runs the seven.

For a person that is friction. For an agent working unattended it is disqualifying: it
cannot push and wait for someone to read the result, and it has no way to know that the
three commands its task file named are not the seven that gate the merge.

    python scripts/run-checks.py

Exit codes, and why 2 outranks 1
--------------------------------
    0   every gate passed
    1   at least one gate ran and failed
    2   at least one gate could not run at all

The precedence is the same one install.py --check and check-provenance.py already use.
A gate that could not execute is not a gate that answered "no": it means the report
itself is incomplete, and that outranks a clean "no" because a reader who treats it as
one is reasoning from an answer nobody produced.

What this command is NOT
------------------------
Passing here is NECESSARY BUT NOT SUFFICIENT. CI runs three operating systems by two
Python versions; any single run of this covers one of those six cells. The summary says
so on every run rather than leaving the reader to remember it.

A documentation-only change runs the documentation gates
--------------------------------------------------------
`scripts/_change_scope.py` decides, from the paths the change touches, whether it is
documentation only (`chore-0098`, cloud-executable.md S-021 and S-022). When it is, the
gates in `DOCS_GATES` run and every other gate is reported as `skipped`, with the reason,
on its own line; when it is not, or when the change cannot be worked out, every gate runs.
The rule lives in that one module so this command and every CI cell answer alike. Set
`ZEN_CHECKS_SCOPE=full` to run every gate regardless.

Every gate runs, even after one fails
-------------------------------------
Deliberately not fail-fast. An unattended agent gets one round trip, and a report naming
only the first failure spends another one to find the second.

What the report carries per gate
--------------------------------
A status word, the gate's name, and then one indented line of the gate's own output
saying what it covered. The coverage line is there because without it a status word is
not falsifiable: measured 2026-08-22 over a copy of this repository with the skills,
the tests, and the task files removed, six of the seven gates exited 0 having examined
nothing, and the report was byte-for-byte the report of a full clean run (bug-0045).
Only `doc links` noticed, and only incidentally.

The counts themselves are not new. Every gate already prints one, each added by a task
that had just been burned by its absence; this command captured them and threw them away
on any gate that passed. See `coverage_line()` for which line is chosen and why.

Standard library only.
"""
from __future__ import annotations

import hashlib
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# `_change_scope` is a sibling module, imported through the repository root as
# install.py and build-adapters.py import theirs.
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
from scripts import _change_scope  # noqa: E402
from scripts import _skillmeta  # noqa: E402

# The throwaway home the install gates use. Chosen to match what checks.yml already
# used, and gitignored via `.tmp/`. Nothing outside it is ever touched: `--uninstall` is
# scoped to the home it is given (bug-0003), which is what makes running this on a
# development machine safe for a real installation.
THROWAWAY_HOME = "./.tmp/zen-home"

PY = sys.executable

# The gates a documentation-only change still runs: the ones whose subject is prose,
# task files and links, plus the secret scan, since a pasted credential in a README is
# the commonest way one reaches a public repository. Everything else exercises code.
DOCS_GATES = frozenset({
    "backlog",
    "changelog lines",
    "skill listings",
    "doc links",
    "matrix citations",
    "roadmap bookkeeping",
    "secret scan",
})


class Gate:
    """One named gate: a sequence of commands that must all succeed.

    `cleanup` runs after `commands` whether they passed or failed, and exists for one
    reason: the install gate places files, and a run that fails midway must not leave a
    populated throwaway home behind. Its failure is reported but does not by itself fail
    the gate, because a cleanup that could not run says nothing about the change under
    test.

    `check` is the second gate kind, added by `chore-0072`: an in-process callable
    returning `(ok, report)` instead of a list of commands. Every other gate here shells
    out to a script that a person can also run alone, and that remains the right default;
    this one exists because `chore-0072` owns exactly two files, this one and its test,
    so a gate with a script of its own would have been a third. The cost is named rather
    than hidden: an in-process gate cannot be run standalone, and it is the one gate whose
    crash could take the aggregator down with it, which `run_gate` handles explicitly.
    A gate carries commands or a check, never both.

    `hermetic_home` (feat-0094, retro R-001) runs the commands with `HOME`, `USERPROFILE`
    and `XDG_CONFIG_HOME` pointed at a scratch directory seeded with decoy instruction
    files, then removes it. See `hermetic_home_env`.
    """

    def __init__(self, name, commands, cleanup=None, check=None, hermetic_home=False):
        self.name = name
        self.hermetic_home = hermetic_home
        self.commands = commands
        self.cleanup = cleanup
        self.check = check


# The ROADMAP bookkeeping check (chore-0072). Its subject is ROADMAP.md, which AGENTS.md
# calls authoritative for what happens next and which no gate has ever read.
ROADMAP = "ROADMAP.md"

TASK_ID = re.compile(r"\b(?:feat|bug|chore|docs|spike)-\d{4}\b")

# A markdown block starts at a list item, a heading, or a table row, and otherwise runs to
# the next blank line. The unit matters, and it was measured: an earlier draft treated
# every unindented line as a new block, which split this file's wrapped paragraphs one
# line each and lost the chore-0042 defect entirely, because the claim and the id it was
# about sat on different lines.
BLOCK_START = re.compile(r"^\s*(?:[-*+]\s|\d+\.\s)|^#|^\|")

# Two tiers, and the split is the whole false-positive answer. A PRESENT-tense claim that
# work is outstanding contradicts a closed id on its own, so nothing in the block excuses
# it. A HEDGED phrase is one this file also uses historically, and its corrected idiom is
# always "Scoped as [id](...) and **shipped <date>**", so a completion marker anywhere in
# the same block means the sentence is a record rather than a claim.
#
# Measured before being written, over ROADMAP.md at b7cd720^ (the state chore-0066 found)
# and at 7a9558f (the state it left): 6 findings on the first, 0 on the second. The tense
# in "are filed rather than fixed" is load-bearing rather than stylistic. chore-0066
# corrected that exact sentence to "were filed rather than fixed and **both closed
# 2026-08-19**", so matching the bare phrase would fire on its own fix.
OPEN_STATE_PRESENT = (
    "are filed rather than fixed",
    "is filed rather than fixed",
    "not yet filed",
    "is still open",
    "are still open",
    "remains open",
    "remain open",
)
OPEN_STATE_HEDGED = (
    "scoped as",
    "pending",
    "ready to dispatch",
    "in flight",
    "awaiting",
)

# A completion word bolded at the head of its span, or sitting beside a date, or a
# struck-through item. Deliberately not the bare word: this file writes "the shipped task
# template" and "the shipped validator" as adjectives, and matching those suppressed two
# real defects when it was tried.
_COMPLETION_WORD = (r"(?:shipped|landed|closed|merged|superseded|completed|struck"
                    r"|discharged|corrected)")
COMPLETION_MARKER = re.compile(
    r"~~|\*\*\s*(?:and\s+)?" + _COMPLETION_WORD
    + r"|" + _COMPLETION_WORD + r"\b[^.\n]{0,25}\d{4}-\d{2}-\d{2}", re.IGNORECASE)

# chore-0066 removed the whole-file header on 2026-08-27, after it had read 2026-08-07 for
# twenty days with nothing checking it. This keeps that decision from being undone by
# someone who reads its absence as an oversight. The pattern needs the colon and a date on
# the same line, because the sentence recording the removal names the field in prose and
# must not match itself.
STALE_HEADER = re.compile(r"Last updated:.{0,20}?\d{4}-\d{2}-\d{2}")


def task_locations(repo_root=None):
    """Every task id under `.quests/`, mapped to the directories holding it.

    A set rather than a string, because an id sitting in both directories is a real state
    this must not silently resolve to one of them.
    """
    repo_root = REPO_ROOT if repo_root is None else Path(repo_root)
    found = {}
    for directory, where in ((repo_root / ".quests", "open"),
                             (repo_root / ".quests" / "done", "done")):
        if not directory.is_dir():
            continue
        for path in directory.glob("*.md"):
            match = TASK_ID.match(path.name)
            if match:
                found.setdefault(match.group(0), set()).add(where)
    return found


def markdown_blocks(text):
    """(first line number, block text) for every markdown block in `text`."""
    blocks = []
    current = None
    for number, raw in enumerate(text.splitlines(), 1):
        if not raw.strip():
            current = None
            continue
        if current is None or BLOCK_START.match(raw):
            current = [number, [raw]]
            blocks.append(current)
        else:
            current[1].append(raw)
    return [(number, "\n".join(lines)) for number, lines in blocks]


def roadmap_findings(text, locations):
    """Blocks whose prose claims a closed task id is still outstanding.

    Returns `[(line_number, [phrases], [ids])]`. The comparison runs over the block with
    its whitespace collapsed, because this file wraps prose at about a hundred columns and
    every multi-word phrase in the vocabulary straddles a line break somewhere in it.
    """
    findings = []
    for number, block in markdown_blocks(text):
        flat = " ".join(block.split())
        lowered = flat.lower()
        present = [p for p in OPEN_STATE_PRESENT if p in lowered]
        hedged = [p for p in OPEN_STATE_HEDGED if p in lowered]
        fired = present + ([] if COMPLETION_MARKER.search(flat) else hedged)
        if not fired:
            continue
        closed = sorted({i for i in TASK_ID.findall(block)
                         if locations.get(i) == {"done"}})
        if closed:
            findings.append((number, fired, closed))
    return findings


# The draft-status half of the same gate (feat-0094, inventory P3). The section it reads,
# and nothing else: "Current state" is the one part of ROADMAP.md that claims to say what
# is true now, while every section below it is a dated record, where "draft `grill`" in a
# shipped overhaul bullet is history rather than a claim about `grill` today.
CURRENT_STATE_RE = re.compile(r"^##[ \t]+Current state[ \t]*$", re.MULTILINE)
NEXT_SECTION_RE = re.compile(r"^##[ \t]+\S", re.MULTILINE)
BACKTICKED_RE = re.compile(r"`([^`\s]+)`")
DRAFT_WORD_RE = re.compile(r"\bdrafts?\b", re.IGNORECASE)
SHIP_WORD_RE = re.compile(r"\bship(?:s|ped|ping)?\b", re.IGNORECASE)
# A sentence ends at terminal punctuation followed by space, read with code spans masked so
# `core.md` or `install.py --dry-run` cannot end one. The unit is the sentence, not the
# block, because a true bullet names what PR #113 promoted right after the draft list
# (WS-A's rewrite, 2026-11-24), and a block-wide reading took those names for drafts.
SENTENCE_END_RE = re.compile(r"(?<=[.!?])\s+(?=\S)")
# A digit count beside the noun it counts, read only in a sentence that makes a draft or
# ship claim: "the default `spine` places 20 skills" is a profile's size, not the total.
# Digits only: a number written as a word is not read.
COUNT_RES = (
    ("skills", re.compile(r"\b(\d+)\s+skills\b", re.IGNORECASE)),
    ("ship", re.compile(r"\b(\d+)\s+(?:ship|ships|shipped)\b", re.IGNORECASE)),
    ("drafts", re.compile(r"\b(\d+)\s+(?:(?:are|is)\s+)?(?:a\s+)?drafts?\b",
                          re.IGNORECASE)),
)

# Findings known on the day the check landed, each excused by key and printed as
# excepted, never silenced (plan principle 9: a stricter check lands with an exception
# list). Every one is the 2026-11-23 "Current state" bullet the inventory's P3 found
# stale and `chore-0100` (WS-A) is rewriting in parallel; once that lands, each key here
# fires "no longer needed" and is deleted. An exception is a debt with a name, not a
# setting: adding one is a decision for whoever reviews the change.
#
# Emptied 2026-11-24 when chore-0100's true "Current state" landed: the eight keys the
# check shipped with (six promoted skills named as drafts, and `count:ship=19` and
# `count:drafts=10`) all stopped firing. A count key names its stale value, so a
# different wrong count is a new finding rather than this one.
ROADMAP_STATUS_EXCEPTIONS = frozenset()


# The changelog's task-log line limit (retro R-204, feat-0103). AGENTS.md says "at most
# about 300 characters"; the gate measures the raw Markdown line, links included, and
# warns past 330, the figure R-204 proposed, so "about" keeps its slack. A warning, not a
# failure: shortening a line is a person's edit, and the integrator is the one who writes
# these lines. The lines over it when the check landed are excepted by the SHA-256 of the
# line (first 16 hex digits), so editing one, or adding a new one, is what warns. The list
# only shrinks: a line shortened or archived to docs/history/ leaves a stale entry, which
# the gate names for deletion.
CHANGELOG = "CHANGELOG.md"
CHANGELOG_LINE_LIMIT = 330
CHANGELOG_LONG_LINE_EXCEPTIONS = frozenset({
    "3688bd439971ac56",  # 2026-11-23 chore-0033, 817 characters
    "a8fd524e8ea08cb5",  # 2026-11-23 chore-0092, 623 characters
    "b12444ee19cd7aaf",  # 2026-11-23 chore-0090, 552 characters
    "336650278762dbb0",  # 2026-11-23 chore-0085, 470 characters
    "4dcaa3a9fdcc72a9",  # 2026-11-23 release readiness for pull request 109, 1160 characters
    "d005b073b9cec670",  # 2026-11-23 chore-0096, 864 characters
    "dca9009bbeec6655",  # 2026-11-23 feat-0083, 1471 characters
    "4f5f4c13c479fd0b",  # 2026-11-23 feat-0082, 1040 characters
    "ef173590525ad0e8",  # 2026-11-23 feat-0081, 2063 characters
    "127986e6aa7d025b",  # 2026-11-23 feat-0080 closed, 831 characters
    "afb652b03a9e44b5",  # 2026-11-23 feat-0080 part A, 1025 characters
    "deb839d1e9e5dcdc",  # 2026-11-23 feat-0079, 1158 characters
    "6430932ec95570d8",  # 2026-11-23 feat-0078, 1055 characters
    "96b5b3100ed4f428",  # 2026-11-23 feat-0077, 981 characters
    "9493cf148573b3d3",  # 2026-11-23 feat-0076, 980 characters
    "ab7f3f111344ff17",  # 2026-11-23 chore-0095, 777 characters
    "af58a07ccd793bc6",  # 2026-10-21 feat-0072 amended, 707 characters
    "760f5011aa8053a4",  # 2026-10-20 feat-0072 closed, 2342 characters
    "98831ddae89253c4",  # 2026-10-20 chore-0094, 1942 characters
})


def skill_statuses(repo_root):
    """`{skill: is_draft}` for every skill under `.agents/skills/`, read as install.py does."""
    skills_dir = Path(repo_root) / ".agents" / "skills"
    found = {}
    if not skills_dir.is_dir():
        return found
    for skill_md in sorted(skills_dir.glob("*/SKILL.md")):
        try:
            text = skill_md.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue  # validate-skills.py reports an unreadable body; not this gate's subject
        # A directory name holding a byte that is not UTF-8 arrives as a surrogate escape,
        # which a strict stream cannot print; it is escaped for the report. No roadmap can
        # name such a skill, so nothing is compared against the raw name (landing review).
        name = os.fsencode(skill_md.parent.name).decode("utf-8", "backslashreplace")
        found[name] = _skillmeta.is_draft_text(text)
    return found


def current_state_section(text):
    """(first line number, section text) of `## Current state`, or None when absent."""
    match = CURRENT_STATE_RE.search(text)
    if match is None:
        return None
    following = NEXT_SECTION_RE.search(text, match.end())
    end = following.start() if following else len(text)
    return text[:match.start()].count("\n") + 1, text[match.start():end]


def _sentences(block):
    """`(offset, sentence)` for each sentence of a markdown block, split outside code spans."""
    masked = list(block)
    for start, end in _skillmeta.code_span_ranges(block):
        masked[start:end] = "x" * (end - start)
    masked = "".join(masked)
    pieces, last = [], 0
    for match in SENTENCE_END_RE.finditer(masked):
        pieces.append((last, block[last:match.start()]))
        last = match.end()
    pieces.append((last, block[last:]))
    return [(offset, p) for offset, p in pieces if p.strip()]


def roadmap_status_findings(text, statuses):
    """Claims in "Current state" that disagree with each skill's `metadata.status`.

    Returns `(findings, claims_read)`, where each finding is `(key, line, message)` and a
    key is what an exception names. Per sentence: a sentence using the word "draft"
    claims every skill it names in backticks is a draft; otherwise a sentence using
    "ship" claims every skill it names ships. When any sentence lists drafts, the lists
    together must name every draft, which is the reverse direction: a list missing a
    draft is the same rot as a list naming a promoted skill. A digit beside "skills",
    "ship" or "drafts" in one of those sentences is compared with the tree.
    """
    section = current_state_section(text)
    if section is None:
        return None, 0
    first, body = section
    findings, claims = [], 0
    listed_drafts = set()
    any_draft_list = False
    first_list_line = first
    counted = []
    for number, block in markdown_blocks(body):
        for offset, sentence in _sentences(block):
            # Cited at the sentence's own line, not the block's or the heading's.
            line = first + number - 1 + block.count("\n", 0, offset)
            names = [n for n in BACKTICKED_RE.findall(sentence) if n in statuses]
            # The words are read with every code span removed, because a span is a name
            # and not prose: `draft-two` would otherwise make its own sentence a claim.
            prose = BACKTICKED_RE.sub(" ", sentence)
            if DRAFT_WORD_RE.search(prose):
                kind = "draft"
            elif SHIP_WORD_RE.search(prose):
                kind = "shipped"
            else:
                continue
            counted.append((line, prose))
            if kind == "draft" and names and not any_draft_list:
                any_draft_list = True
                first_list_line = line
            for name in names:
                claims += 1
                at = line + sentence.count("\n", 0, max(sentence.find(f"`{name}`"), 0))
                if kind == "draft":
                    listed_drafts.add(name)
                    if not statuses[name]:
                        findings.append((f"draft:{name}", at,
                                         f"`{name}` is named as a draft, and its SKILL.md "
                                         f"carries no `status: draft`"))
                elif statuses[name]:
                    findings.append((f"shipped:{name}", at,
                                     f"`{name}` is named as shipped, and its SKILL.md "
                                     f"carries `status: draft`"))
    if any_draft_list:
        for name in sorted(n for n, draft in statuses.items()
                           if draft and n not in listed_drafts):
            findings.append((f"missing:{name}", first_list_line,
                             f"`{name}` carries `status: draft` and is missing from "
                             f"every draft list in this section"))
    actual = {"skills": len(statuses),
              "drafts": sum(1 for d in statuses.values() if d),
              "ship": sum(1 for d in statuses.values() if not d)}
    for line, prose in counted:
        flat = " ".join(prose.replace("*", "").split())
        for noun, pattern in COUNT_RES:
            for match in pattern.finditer(flat):
                claims += 1
                said = int(match.group(1))
                if said != actual[noun]:
                    findings.append((f"count:{noun}={said}", line,
                                     f"says {said} {noun}, and the tree holds "
                                     f"{actual[noun]}"))
    return findings, claims


def check_roadmap(repo_root=None, status_exceptions=None):
    """The `roadmap bookkeeping` gate: does ROADMAP.md still agree with .quests/?

    Returns (ok, report). Two of the three shapes chore-0066 mapped, and a bound naming
    what is left. The bound is not decoration. This catches the bookkeeping class and
    cannot catch the defect that mattered most in that pass, Epic E item 2 restating an
    acceptance bar that docs/spec/cloud-executable.md had already repointed eight days
    earlier. Catching that means reading the contract the roadmap restates, which is a
    different capability, so a green run here must not be read as "the roadmap is
    current".

    The third shape, a quoted shell command written into the file beside its own output,
    is deliberately not built. One instance is not a mechanism; telling a claim about a
    command's current output from a command quoted as an illustration needs the judgment
    this check has none of; and running shell text lifted out of a document is an action
    no gate here takes.
    """
    repo_root = REPO_ROOT if repo_root is None else Path(repo_root)
    text = (repo_root / ROADMAP).read_text(encoding="utf-8")
    locations = task_locations(repo_root)

    named = sorted(set(TASK_ID.findall(text)))
    closed = [i for i in named if locations.get(i) == {"done"}]
    outstanding = [i for i in named if locations.get(i) == {"open"}]
    unresolved = [i for i in named if len(locations.get(i, ())) != 1]
    blocks = markdown_blocks(text)
    findings = roadmap_findings(text, locations)
    header = STALE_HEADER.search(text)

    lines = []
    for number, phrases, ids in findings:
        lines.append(
            f"{ROADMAP}:{number}: {', '.join(ids)} "
            f"{'is' if len(ids) == 1 else 'are'} in .quests/done/, and this block "
            f"reads as outstanding: {'; '.join(repr(p) for p in phrases)}")
    if header:
        lines.append(
            f"{ROADMAP}: a `Last updated:` header is back ({header.group(0)!r}). "
            f"chore-0066 removed it on 2026-08-27 because a date nothing derives is a "
            f"claim nobody maintains, and `git log -1 ROADMAP.md` answers the same "
            f"question without being able to drift.")
    # Reported, never judged. An id naming no task file may be a typo or a file not yet
    # written, and this check cannot tell which; saying nothing would let the arithmetic
    # below imply a coverage it does not have.
    if unresolved:
        lines.append(f"{ROADMAP}: {len(unresolved)} id(s) named here resolve to no "
                     f"single task file and were not judged: "
                     f"{', '.join(unresolved)}")

    statuses = skill_statuses(repo_root)
    exceptions = (ROADMAP_STATUS_EXCEPTIONS if status_exceptions is None
                  else frozenset(status_exceptions))
    status_findings, status_claims = roadmap_status_findings(text, statuses)
    failing_status = []
    if status_findings is None:
        status_note = (f"no `## Current state` section, so no skill status claim was "
                       f"judged")
        lines.append(f"{ROADMAP}: {status_note}.")
    else:
        fired = {key for key, _, _ in status_findings}
        for key, number, message in status_findings:
            if key in exceptions:
                lines.append(f"{ROADMAP}:{number}: excepted ({key}): {message}")
            else:
                failing_status.append(key)
                lines.append(f"{ROADMAP}:{number}: {message}")
        # A stale key fails the gate (plan principle 9, the prune half). Reported only,
        # it was invisible on a passing run, and while it stood it excused any later
        # regression that happened to produce the same key (landing review, 2026-11-24).
        stale = sorted(exceptions - fired)
        for key in stale:
            lines.append(f"{ROADMAP}: exception {key!r} no longer needed; delete it from "
                         f"ROADMAP_STATUS_EXCEPTIONS in scripts/run-checks.py.")
        failing_status.extend(f"stale:{key}" for key in stale)
        status_note = (f"{status_claims} skill status claim(s) in Current state read "
                       f"against {len(statuses)} SKILL.md file(s), "
                       f"{len(failing_status) - len(stale)} wrong, "
                       f"{len(status_findings) - (len(failing_status) - len(stale))} "
                       f"excepted, {len(stale)} stale exception(s)")

    lines.append(
        f"Checked {ROADMAP}: {len(named)} task ids named, {len(closed)} in .quests/done/, "
        f"{len(outstanding)} in .quests/, {len(unresolved)} unresolved; {len(blocks)} "
        f"blocks read, {len(findings)} carrying an open-state claim over a closed id; "
        f"1 header rule, {0 if header is None else 1} tripped; {status_note}. "
        f"Not judged: the "
        f"restated-contract class (a roadmap claim restating a spec's own bar, which "
        f"needs reading that contract), quoted commands and their written-down output, "
        f"and a hedged phrase in a block that also carries a completion marker. "
        f"2 of the 3 shapes chore-0066 mapped are covered, so a pass here is evidence "
        f"about bookkeeping and about nothing else.")
    return (not findings and header is None and not failing_status,
            "\n".join(lines))


def _line_key(line):
    return hashlib.sha256(line.encode("utf-8")).hexdigest()[:16]


def check_changelog_lines(repo_root=None, exceptions=None, limit=None):
    """The `changelog lines` gate: a task-log line over the limit warns (R-204).

    Returns (ok, report), and ok is always True: this gate warns and never fails. The
    findings go on the report's last line, the one `coverage_line()` shows beside a
    passing gate, so a warning is visible without a failure to carry it. Reads the lines
    starting `- ` under `## Task log` only; the releases section above it is prose.
    """
    repo_root = REPO_ROOT if repo_root is None else Path(repo_root)
    exceptions = (CHANGELOG_LONG_LINE_EXCEPTIONS if exceptions is None
                  else frozenset(exceptions))
    limit = CHANGELOG_LINE_LIMIT if limit is None else limit
    path = repo_root / CHANGELOG
    if not path.is_file():
        return True, f"{CHANGELOG}: absent, so 0 task-log lines were measured."
    lines = path.read_text(encoding="utf-8").splitlines()
    # Found without regard to case or trailing space: a heading retyped as "## Task Log"
    # must not switch the gate off while it reports a clean pass.
    start = next((n + 1 for n, line in enumerate(lines)
                  if line.strip().lower() == "## task log"), None)
    if start is None:
        report = [f"WARN  {CHANGELOG}: exception {key!r} matches no line over the limit; "
                  f"delete it from CHANGELOG_LONG_LINE_EXCEPTIONS in scripts/run-checks.py"
                  for key in sorted(exceptions)]
        warn = "WARN " if exceptions else ""
        report.append(f"{warn}{CHANGELOG}: no `## Task log` heading, so 0 task-log lines "
                      f"were measured; {len(exceptions)} stale exception(s).")
        return True, "\n".join(report)
    entries = [(n, line) for n, line in enumerate(lines[start:], start + 1)
               if line.startswith("- ")]
    report, new, excepted, seen = [], [], 0, set()
    for number, line in entries:
        if len(line) <= limit:
            continue
        key = _line_key(line)
        if key in exceptions:
            excepted += 1
            seen.add(key)
            continue
        new.append(number)
        report.append(f"WARN  {CHANGELOG}:{number}: task-log line is {len(line)} characters, "
                      f"over {limit}; keep a closeout line to about 300 and put the detail "
                      f"in the quest file it links")
    stale = sorted(exceptions - seen)
    for key in stale:
        report.append(f"WARN  {CHANGELOG}: exception {key!r} matches no line over the "
                      f"limit; delete it from CHANGELOG_LONG_LINE_EXCEPTIONS in "
                      f"scripts/run-checks.py")
    warned = (f"WARN {len(new)} new line(s) over {limit} characters, at line(s) "
              f"{', '.join(map(str, new))}" if new else "0 new lines over the limit")
    report.append(f"Measured {len(entries)} task-log line(s) in {CHANGELOG}: {warned}; "
                  f"{excepted} excepted, {len(stale)} stale exception(s).")
    return True, "\n".join(report)


# The two documents that list the kit for a reader (E9, feat-0103): the `zen` router, which
# an agent reads to pick a skill, and the catalog a person reads. A skill neither names is
# reachable only by someone who already knows it exists. A draft is named too, or excepted
# here by name with the reason; an exception for a skill that is named, or gone, fails.
SKILL_LISTINGS = (".agents/skills/zen/SKILL.md", "docs/CATALOG.md")
UNLISTED_DRAFT_EXCEPTIONS = {}


def _names(text, name):
    """A listing names a skill as `` `name` ``, `[name]`, or by the path `name/SKILL.md`."""
    escaped = re.escape(name)
    return re.search(rf"`{escaped}`|\[{escaped}\]|(?<![\w-]){escaped}/SKILL\.md",
                     text) is not None


def check_skill_listings(repo_root=None, exceptions=None):
    """The `skill listings` gate: do the router and the catalog name every skill?

    Returns (ok, report). `zen` is not required to name itself.
    """
    repo_root = REPO_ROOT if repo_root is None else Path(repo_root)
    exceptions = UNLISTED_DRAFT_EXCEPTIONS if exceptions is None else dict(exceptions)
    statuses = skill_statuses(repo_root)
    lines, failing, checked = [], 0, 0
    for listing in SKILL_LISTINGS:
        path = repo_root / listing
        if not path.is_file():
            lines.append(f"{listing}: absent, so no skill could be found in it.")
            failing += 1
            continue
        checked += 1
        text = path.read_text(encoding="utf-8")
        owner = Path(listing).parent.name if listing.endswith("SKILL.md") else None
        for name in sorted(statuses):
            if name == owner:
                continue
            named = _names(text, name)
            if named and name in exceptions:
                lines.append(f"{listing}: names {name!r}, so its exception in "
                             f"UNLISTED_DRAFT_EXCEPTIONS is stale; delete it.")
                failing += 1
            elif not named and name in exceptions and statuses[name]:
                lines.append(f"{listing}: {name!r} excepted: {exceptions[name]}")
            elif not named:
                kind = "draft" if statuses[name] else "shipped skill"
                lines.append(f"{listing}: does not name the {kind} {name!r}; add it, as "
                             f"`{name}`" + (", or except the draft in "
                             f"UNLISTED_DRAFT_EXCEPTIONS with the reason"
                             if kind == "draft" else ""))
                failing += 1
    for name in sorted(set(exceptions) - set(statuses)):
        lines.append(f"exception {name!r} names no skill in the kit; delete it.")
        failing += 1
    lines.append(f"Checked {checked} of {len(SKILL_LISTINGS)} listing(s) against "
                 f"{len(statuses)} skill(s): {failing} finding(s) failing.")
    return failing == 0, "\n".join(lines)


def gates():
    """The gate set: every gate that decides whether a change here is acceptable.

    Ordered as checks.yml ran the ones it used to restate. The set is open by design and
    its membership is the property that matters, not its size: it began as the seven
    steps checks.yml carried, and `chore-0049` added the matrix-citation gate. Naming a
    count here, or in the contract, goes stale the first time anyone adds a gate, which is
    the class this repository keeps filing tasks about.

    A function rather than a module constant so a test can hold the canonical list
    without depending on import-time state, and so the interpreter is resolved at call
    time rather than at import.
    """
    install_home = ["--home", THROWAWAY_HOME]
    return [
        Gate("lint skills", [[PY, "scripts/validate-skills.py"]]),
        # Hermetic about the home directory since feat-0094 (retro R-001): a test that
        # reads the real home now fails in CI the way it fails on a maintainer's machine.
        Gate("test suite",
             [[PY, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"]],
             hermetic_home=True),
        Gate("backlog", [[PY, ".quests/validate.py", "--strict"]]),
        Gate("adapters dry run", [[PY, "scripts/build-adapters.py", "--dry-run"]]),
        # Added by feat-0079. The Claude Code marketplace is a generated tree committed
        # under .claude-plugin/, because that is what `claude plugin marketplace add`
        # fetches; a committed copy of generated output drifts the first time a skill
        # changes without it. This fails when it has, and names every file.
        Gate("plugin tree",
             [[PY, "scripts/build-adapters.py", "--marketplace", "--check"]]),
        Gate("install dry run", [[PY, "scripts/install.py", "--dry-run"] + install_home]),
        # Exercises the real placement path, including POSIX symlink mode, which the dry
        # run does not cover. Running it twice proves idempotence; the uninstall proves
        # the manifest can find what it created.
        #
        # `--with-hooks` is here by a decision recorded in chore-0067, not by habit. It
        # costs this gate the six files of .agents/hooks/ written into the gitignored
        # throwaway home per tool and removed again by the cleanup below, which needed no
        # change: `--uninstall` reverses every recorded target beneath the home it is
        # given, and the hooks placement is a recorded target. What it buys is the only
        # module the kit runs inside an adopter's session being placed at least once per
        # CI cell, in the real default mode for that platform, which is symlink on four of
        # the six. The rejected option was leaving the flag off and relying on the
        # component tests in tests/test_install.py alone: those run in-process and, off a
        # POSIX host or on an account that cannot symlink, never take the link branch at
        # all, so the saving would have been six temporary files against a placement path
        # that still ran on no cell.
        Gate("install cycle",
             [[PY, "scripts/install.py", "--with-hooks"] + install_home,
              [PY, "scripts/install.py", "--with-hooks"] + install_home],
             cleanup=[PY, "scripts/install.py", "--uninstall"] + install_home),
        # Calls the link rule in .quests/validate.py rather than restating it. An inline
        # copy of that rule drifted once already (chore-0029). Globbed rather than
        # listed, because a hardcoded list silently excludes every new document.
        #
        # Each of the three patterns must match at least one document or this gate
        # fails and names the one that did not (chore-0032). Until then the guard fired
        # only when every pattern matched nothing, so renaming `docs/` left this gate
        # green over 9 documents of 45. The three trees are all guaranteed present here,
        # which is why no pattern needs an escape and none is offered.
        Gate("doc links",
             [[PY, ".quests/validate.py", "--links",
               "*.md", ".github/**/*.md", "docs/**/*.md"]]),
        # Added by chore-0049. The doc-links gate above resolves a markdown link's path
        # and stops there; a conformance matrix's evidence is a symbol, a test name, or a
        # quoted phrase, and none of those is a path. So a matrix could go on asserting
        # that a renamed symbol exists with every gate green, which is what bug-0037
        # measured: seven of 65 pointers in one matrix aimed at something other than what
        # they claimed, from two independent causes in one month.
        Gate("matrix citations", [[PY, "scripts/check-citations.py"]]),
        # Added by chore-0072, and the first gate here that is a callable rather than a
        # script. Nothing above reads ROADMAP.md, which AGENTS.md calls authoritative for
        # what happens next: `backlog` walks the task files, and `doc links` resolves this
        # file's link paths and stops there. So a sentence saying a task is still to be
        # done, beside that task's own file sitting in `.quests/done/`, passed every gate,
        # which is what chore-0066 measured when it corrected nine of them at once.
        Gate("roadmap bookkeeping", [], check=check_roadmap),
        # Added by feat-0103 (retro R-204). Warns, never fails: a closeout line over the
        # limit is named on the line a passing gate shows. A documentation gate, since
        # CHANGELOG.md is prose.
        Gate("changelog lines", [], check=check_changelog_lines),
        # Added by feat-0103 (E9): the router and the catalog name every skill. A
        # documentation gate, since the catalog is prose.
        Gate("skill listings", [], check=check_skill_listings),
        # Added by chore-0098 (retro R-008). Runs on every change, documentation-only ones
        # included, which is why it is in DOCS_GATES.
        Gate("secret scan", [[PY, "scripts/scan-secrets.py"]]),
    ]


# What a person's home holds that a test must never read by accident (R-001). Each decoy
# says what it is, so a test that trips over one fails with a message naming the cause.
HOME_DECOYS = {
    ".claude/CLAUDE.md": "# Decoy from run-checks.py (R-001)\n\nA test read the real "
                         "home directory. Give it a fixture home instead.\n",
    ".claude/settings.json": '{"_decoy": "run-checks.py R-001: a test read the real home"}\n',
    "AGENTS.md": "# Decoy from run-checks.py (R-001)\n\nA test read the real home "
                 "directory. Give it a fixture home instead.\n",
}


def hermetic_home_env(home):
    """The environment for a hermetic gate: the current one with every home pointed at `home`.

    All three variables, because the readers differ: `Path.home()` reads `HOME` on POSIX
    and `USERPROFILE` on Windows, and XDG-aware tools (git among them) read
    `XDG_CONFIG_HOME` before either. The decoys are written into `home` first, so a test
    that reads the real home in CI meets instruction files the way it would on a
    maintainer's machine, rather than an empty runner home that lets it pass (R-001: CI
    passed all six cells while the same suite failed thirty tests locally).
    """
    home = Path(home)
    for relative, content in HOME_DECOYS.items():
        target = home / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    (home / ".config").mkdir(exist_ok=True)
    env = dict(os.environ)
    env.update(HOME=str(home), USERPROFILE=str(home),
               XDG_CONFIG_HOME=str(home / ".config"))
    return env


def _script_of(command):
    """The repository-relative script a command runs, when it names one.

    Returns None for a command that runs a module (`-m unittest`) rather than a file,
    since there is then no path to check.
    """
    if len(command) < 2 or command[1].startswith("-"):
        return None
    return command[1]


def _run(command, runner=None, env=None):
    """Execute one command. Returns (ok, unrunnable, output).

    The missing-script check happens before the call, and it is not belt-and-braces: a
    missing script is the most likely real cause of a gate that cannot run, and
    subprocess does NOT raise for it. `subprocess.run([sys.executable, "gone.py"])`
    starts the interpreter successfully and exits non-zero, so the whole
    could-not-run branch would be dead in exactly the case it exists for, and the gate
    would be reported as `failed` at exit 1 instead of `unrunnable` at exit 2.

    Found by exercising the branch against a real subprocess after a stubbed test of it
    passed. The stub raised OSError because that is what the code expected, which is the
    failure mode where a test confirms an assumption instead of checking it.
    """
    script = _script_of(command)
    if script is not None and not (REPO_ROOT / script).exists():
        return False, True, f"could not run: {script} does not exist"
    runner = subprocess.run if runner is None else runner
    try:
        # `env` is passed only when a gate asks for one, so a runner stand-in written
        # before `hermetic_home` existed keeps the signature it was written against.
        extra = {} if env is None else {"env": env}
        done = runner(command, cwd=str(REPO_ROOT), capture_output=True, text=True,
                      **extra)
    except OSError as exc:
        # The interpreter itself could not be started. Rarer than the case above, and
        # still distinct from a command that ran and returned non-zero.
        return False, True, f"could not run: {exc}"
    output = (done.stdout or "") + (done.stderr or "")
    return done.returncode == 0, False, output


def _run_check(gate):
    """Run an in-process gate. Same (status, output, cleanup_ok) shape as a command gate.

    The broad `except Exception` is the one place in this file that catches everything,
    and it is deliberate. Every other gate is a subprocess, so its crash is somebody
    else's traceback and a non-zero return code; an in-process gate raising would abort
    the aggregator itself and take the gates after it down with it, which is exactly the
    fail-fast behaviour this command was written not to have. A crash is reported as
    `unrunnable` rather than `failed`, for the same reason a missing script is: it means
    the question was never answered, not that the answer was no.
    """
    try:
        ok, output = gate.check()
    except Exception as exc:  # deliberately broad; see the docstring
        return "unrunnable", f"could not run: {type(exc).__name__}: {exc}", True
    return ("ok" if ok else "failed"), output, True


def run_gate(gate, runner=None):
    """Run one gate. Returns (status, output, cleanup_ok).

    `cleanup_ok` is reported separately from `status` rather than folded into it. A
    cleanup that fails leaves files behind, which a reader needs to know about, but it
    says nothing about whether the change under test is good, so it must not turn a
    passing gate into a failing one. Keeping them separate is what lets the report say
    both things at once.
    """
    if gate.check is not None:
        return _run_check(gate)
    if gate.hermetic_home:
        scratch = tempfile.mkdtemp(prefix="zen-hermetic-home-")
        try:
            return _run_commands(gate, runner, hermetic_home_env(scratch))
        finally:
            shutil.rmtree(scratch, ignore_errors=True)
    return _run_commands(gate, runner, None)


def _run_commands(gate, runner, env):
    """The command half of `run_gate`, with the environment it was given."""
    collected = []
    status = "ok"
    for command in gate.commands:
        ok, unrunnable, output = _run(command, runner, env)
        collected.append(output)
        if unrunnable:
            status = "unrunnable"
            break
        if not ok:
            status = "failed"
            break
    cleanup_ok = True
    if gate.cleanup is not None:
        ok, _unrunnable, output = _run(gate.cleanup, runner, env)
        if not ok:
            cleanup_ok = False
            collected.append("cleanup did not complete:\n" + output)
    return status, "\n".join(c for c in collected if c.strip()), cleanup_ok


def coverage_line(output):
    """The one line of a gate's own output to show beside its status. Display only.

    Every gate here already prints what it covered, and each of those counts was added
    by a task that had just been burned by its absence: `validate-skills.py`'s skill and
    supporting-file counts, `.quests/validate.py`'s `Checked N quest files`, `install.py`'s
    placed count and description budget, and `--links`'s document count. Until bug-0045
    this aggregator captured all of them and printed none, so seven gates passing over a
    full tree and seven gates passing over an empty one were byte-identical reports.

    The rule is the last non-blank line that contains a digit, falling back to the last
    non-blank line when no line has one, and to `(no output)` when a gate said nothing.

    Why a digit and not simply the last line, which is the cheaper rule bug-0045
    suggested trying first: it was measured against all seven real gates on 2026-08-22
    and it is uninformative for three of them. The test suite's last line is unittest's
    bare `OK`, which is identical over 482 tests and over zero, that being the exact
    failure this function exists to remove; both install gates end on `install.py`'s
    "Run ... --check" advice line, which says nothing about what was placed. The digit
    rule picks `Ran 482 tests in 8.395s` and `Description budget: ...` instead. It needs
    no per-gate knowledge and no name-to-regex table, which the task's implementation
    notes rule out as a second source of truth that drifts the first time a gate rewords
    its summary (the failure `chore-0029` recorded for a copied link rule).

    The fallback matters as much as the rule. A gate declining to look says so in words
    and no digits: `validate-skills.py`, `install.py`, and `build-adapters.py` all print
    "No skills found under <dir>." over an empty tree, so the fallback surfaces that
    sentence verbatim, which is the whole finding of bug-0045.

    This is display, never a verdict. The exit code stays the gates' own, and nothing
    here parses the text for anything but which line to echo.
    """
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    if not lines:
        return "(no output)"
    for line in reversed(lines):
        if any(character.isdigit() for character in line):
            return line
    return lines[-1]


def run_all(the_gates=None, runner=None, out=None, scope=None):
    """Run every gate in scope and report. Returns the exit code.

    `the_gates` and `runner` are injectable so the aggregation logic is reachable from a
    test without executing every real gate, which would make the failure and
    could-not-run branches untestable. `scope` is `(name, reason)` from
    `_change_scope.decide()`; None means the full set, with no scope line.
    """
    the_gates = gates() if the_gates is None else the_gates
    out = sys.stdout if out is None else out
    docs_only = scope is not None and scope[0] == _change_scope.DOCS
    if scope is not None:
        out.write(f"Scope: {scope[0]}. {scope[1]}.\n")

    counts = {"ok": 0, "failed": 0, "unrunnable": 0, "skipped": 0}
    notes = []
    for gate in the_gates:
        if docs_only and gate.name not in DOCS_GATES:
            counts["skipped"] += 1
            out.write(f"{'skipped':11} {gate.name}\n")
            out.write(f"{'':11} not run: the change is documentation only\n")
            continue
        status, output, cleanup_ok = run_gate(gate, runner)
        counts[status] += 1
        suffix = "" if cleanup_ok else "  (cleanup did not complete)"
        out.write(f"{status:11} {gate.name}{suffix}\n")
        # Every gate, passing or not, carries its own account of what it covered on an
        # indented second line. Unconditional on purpose: the passing case is the one
        # bug-0045 found silent, and a status word alone cannot distinguish a gate that
        # checked the whole tree from one that found nothing to check and said so.
        out.write(f"{'':11} {coverage_line(output)}\n")
        # A passing gate whose cleanup failed still needs its output shown, or the
        # leftover files are announced in one word and explained nowhere.
        if status != "ok" or not cleanup_ok:
            notes.append((gate.name, status, output))

    for name, status, output in notes:
        out.write(f"\n----- {name}: {status} -----\n{output.rstrip()}\n")

    skipped = (f", {counts['skipped']} skipped because the change is documentation only"
               if counts["skipped"] else "")
    out.write(f"\n{counts['ok']} passed, {counts['failed']} failed, "
              f"{counts['unrunnable']} could not run{skipped}.\n")
    out.write(f"Ran on {platform.system()}, Python {platform.python_version()}. "
              f"CI runs 3 operating systems x 2 Python versions, so this is one of six "
              f"cells: passing here is necessary but not sufficient.\n")

    if counts["unrunnable"]:
        return 2
    return 1 if counts["failed"] else 0


def main(argv=None, the_gates=None, runner=None, out=None) -> int:
    """Entry point. Takes no options; `argv` exists only to reject any that are passed."""
    argv = sys.argv[1:] if argv is None else argv
    if argv:
        out = sys.stdout if out is None else out
        out.write("run-checks.py takes no arguments; it runs every gate, always.\n")
        return 2
    # The scope is decided only for the real gate set. An injected set is a test of the
    # aggregation logic, which must not depend on the state of the checkout running it.
    scope = _change_scope.decide() if the_gates is None else None
    return run_all(the_gates, runner, out, scope)


if __name__ == "__main__":
    raise SystemExit(main())
