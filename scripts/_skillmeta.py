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
