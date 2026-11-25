#!/usr/bin/env python3
"""Read a skill's `metadata` block, and render it for Claude Code. Shared, not shipped.

Three scripts need the same two answers about a skill, and before `feat-0079` each that
needed one carried its own reader: is this skill a draft, and does a person start it by
name. `install.py` read `metadata.status`; `build-adapters.py` read nothing and so shipped
drafts into every adapter (`chore-0077`); `validate-skills.py` could not tell a legal
`metadata.invocation` from a typo. One reader here, imported by all three, so the three
cannot disagree about what a skill declares.

The two fields
--------------
Both live under `metadata`, the one property of the six the skill schema permits that can
carry them. A seventh top-level key is rejected by claude.ai and the Skills API, so the
source stays six-key and only a Claude Code copy gains the key that harness reads:

    metadata:
      status: draft          # absent, or any other value, means shipped
      invocation: user       # absent means model-invoked; `model` says so explicitly

Only the block form is read. The flow form `metadata: {status: draft}` trips
`validate-skills.py`'s plain-scalar-with-a-colon check, so it is not a legal spelling here.
Deliberately not a YAML parser, for the reason every reader in `scripts/` gives: the
standard library has none, and the subset this kit writes is narrow and validated.

Rendering
---------
`render_for_claude()` gives a user-invoked skill `disable-model-invocation: true` as a
top-level frontmatter key, which is what Claude Code reads to keep the description out of
the agent's context. Every other path leaves the text byte-for-byte as it was: the key is
legal for Claude Code and illegal for claude.ai, so it may appear only in a copy placed
for Claude Code.

Links
-----
`link_targets()` and `sibling_edges()` are the one answer to "what is a link in this
body", shared since `feat-0090` by the validator, the installer and the adapter builder.
A link inside an inline code span or a fenced code block renders as literal text, so it is
a body *showing* an example, not making one: it is neither a link to check nor an install
edge. Before `feat-0090` the installer and the adapter builder scanned the raw text, so an
example in a fence became an install edge the validator never saw. The span helpers are
reproduced from `.quests/validate.py`, which ships to adopters and so may import nothing
from here; `tests/test_install.py` holds the two copies identical.

Standard library only. Like `_textio.py`, it reaches no adopter: `install.py` never places
it and nothing under `.agents/` imports it.
"""
from __future__ import annotations

import re

METADATA_KEY_RE = re.compile(r"^metadata:\s*$")
NESTED_FIELD_RE = re.compile(r"^\s+([\w-]+):\s*(.*?)\s*$")

DRAFT_STATUS = "draft"
INVOCATION_VALUES = ("user", "model")
USER_INVOKED = "user"
RENDERED_KEY = "disable-model-invocation"
RENDERED_LINE = f"{RENDERED_KEY}: true"


# A run of one or more backticks, and a fenced code block delimiter: a whole line whose
# content is a run of three or more backticks, optionally followed by an info string.
# Up to three spaces of indentation, per CommonMark. Kept character-identical to
# `.quests/validate.py`, the original, where bug-0015 and bug-0017 taught the backlog
# validator that a link rendered as literal text is not a link; a test compares the two.
BACKTICK_RUN_RE = re.compile(r"`+")
FENCE_RE = re.compile(r"^ {0,3}(`{3,})([^`]*)$")

# An inline link, read from its opening bracket, and a sibling skill link, read from the
# bracket that closes the link text. Both are checked against the span ranges below.
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
SIBLING_LINK_RE = re.compile(r"\]\(\.\./([^/)]+)/SKILL\.md")


def code_span_ranges(text):
    """Character ranges `(start, end)` of the inline code spans in `text`.

    A span opens with a run of backticks and closes with a run of the same length, so
    both the single and the double form are spans, and a check that knows only the first
    fixes half the occurrences it meets.

    Scanned one line at a time, deliberately, and an unmatched run opens nothing:
    pairing runs across the whole file means one stray backtick swallows everything up
    to the next stray one, and a caller that skips those ranges then reports success
    while checking nothing. See `code_span_ranges()` in .quests/validate.py, the original.
    """
    ranges = []
    offset = 0
    for line in text.splitlines(keepends=True):
        runs = [(m.start(), m.end()) for m in BACKTICK_RUN_RE.finditer(line)]
        i = 0
        while i < len(runs):
            opener = runs[i]
            width = opener[1] - opener[0]
            closer = next((j for j in range(i + 1, len(runs))
                           if runs[j][1] - runs[j][0] == width), None)
            if closer is None:
                i += 1
                continue
            ranges.append((offset + opener[0], offset + runs[closer][1]))
            i = closer + 1
        offset += len(line)
    return ranges


def fenced_block_ranges(text):
    """Character ranges `(start, end)` of the fenced code blocks in `text`.

    A fence is a line-level construct where an inline code span is a character-level
    one. Its delimiters sit alone on lines of their own, so code_span_ranges() pairs
    them with nothing: the two rules compose by union rather than by replacement.

    An unterminated opening fence yields no range at all, the same trade
    code_span_ranges() makes for an unmatched run and for the same reason: a detector
    that ran an unclosed fence to end of file would switch the caller's link check off
    for everything below it and report success while doing so. See
    `fenced_block_ranges()` in .quests/validate.py, the original.
    """
    ranges = []
    offset = 0
    start = None
    width = 0
    for line in text.splitlines(keepends=True):
        match = FENCE_RE.match(line.rstrip("\r\n"))
        if match:
            if start is None:
                start, width = offset, len(match.group(1))
            elif len(match.group(1)) >= width and not match.group(2).strip():
                ranges.append((start, offset + len(line)))
                start = None
        offset += len(line)
    return ranges


def literal_ranges(text):
    """Every range in `text` that renders as literal text: code spans and fenced blocks."""
    return code_span_ranges(text) + fenced_block_ranges(text)


def _outside(position, ranges):
    return not any(start <= position < end for start, end in ranges)


def link_targets(text):
    """Yield the raw target of every inline markdown link that renders as a link.

    A link whose opening bracket falls inside a code span or a fenced block is skipped
    (bug-0027). An optional `"title"` after the target is dropped.
    """
    ranges = literal_ranges(text)
    for m in LINK_RE.finditer(text):
        if not _outside(m.start(), ranges):
            continue
        target = m.group(1).strip().split(" ", 1)[0]
        if target:
            yield target


def sibling_edges(text):
    """The sibling skills a body links as `../<name>/SKILL.md`, outside every literal range.

    This is the install edge AGENTS.md calls load-bearing: `install.py` expands a profile
    over it and `build-adapters.py` refuses an emitted skill whose edge reaches a draft.
    """
    ranges = literal_ranges(text)
    return {m.group(1) for m in SIBLING_LINK_RE.finditer(text) if _outside(m.start(), ranges)}


def names_skill(text: str, name: str) -> bool:
    """Whether `text` names the skill `name`: as `` `name` ``, `[name]`, or `name/SKILL.md`.

    The one answer, shared since the round 2 close by `run-checks.py`'s listing gate and
    `validate-skills.py`'s dogfood-record match, so a bare word that happens to equal a
    skill's name (a draft called `plan`, and the word "plan" in prose) names nothing. Any
    backticked mention counts, whatever the sentence around it says: the match is lexical.
    """
    escaped = re.escape(name)
    return re.search(rf"`{escaped}`|\[{escaped}\]|(?<![\w-]){escaped}/SKILL\.md",
                     text) is not None


def _frontmatter_lines(text: str):
    """(lines, closing_index) for a frontmatter block, or (lines, None) when there is none."""
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return lines, None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return lines, i
    return lines, None


def metadata_fields(text: str) -> dict:
    """Every nested `key: value` under the frontmatter's `metadata:` block.

    Values are unquoted and lowercased, because both fields read here are enumerations and
    the case an author typed is not a fact about the skill. A `status:` or `invocation:`
    line in the body is prose and is never read: several skills discuss draft status in
    their bodies, and reading one of those as a marker would withhold a shipped skill.
    """
    lines, end = _frontmatter_lines(text)
    if end is None:
        return {}
    fields, inside = {}, False
    for raw in lines[1:end]:
        line = raw.rstrip("\r\n")
        if inside:
            if line.strip() and not line[:1].isspace():
                inside = False  # a new top-level key ended the metadata block
            else:
                m = NESTED_FIELD_RE.match(line)
                if m:
                    fields[m.group(1)] = m.group(2).strip().strip('"').strip("'").lower()
                continue
        if METADATA_KEY_RE.match(line):
            inside = True
    return fields


def status_of_text(text: str) -> str:
    """`metadata.status`, lowercased, or "" when the skill carries none."""
    return metadata_fields(text).get("status", "")


def is_draft_text(text: str) -> bool:
    return status_of_text(text) == DRAFT_STATUS


def invocation_of_text(text: str) -> str:
    """`user` or `model`. Absent, or a value nobody spelled right, reads as `model`.

    The unrecognised direction is the safe one: a model-invoked reading keeps the
    description visible, so a typo costs budget rather than hiding a skill the agent
    needed. `validate-skills.py` fails the typo, so it cannot ship.
    """
    value = metadata_fields(text).get("invocation", "")
    return USER_INVOKED if value == USER_INVOKED else "model"


def is_user_invoked_text(text: str) -> bool:
    return invocation_of_text(text) == USER_INVOKED


def render_for_claude(text: str) -> str:
    """The SKILL.md text a Claude Code copy should carry.

    A user-invoked skill gains `disable-model-invocation: true` as the last frontmatter
    line; anything else is returned unchanged. Idempotent: a text that already carries the
    key is returned as it is, so rendering a rendered copy changes nothing.
    """
    if not is_user_invoked_text(text):
        return text
    lines, end = _frontmatter_lines(text)
    if end is None:
        return text
    for raw in lines[1:end]:
        if raw.startswith(f"{RENDERED_KEY}:"):
            return text
    newline = "\r\n" if lines[end - 1].endswith("\r\n") else "\n"
    return "".join(lines[:end]) + RENDERED_LINE + newline + "".join(lines[end:])
