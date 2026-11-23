#!/usr/bin/env python3
"""Tell whether an approved spec still says what was approved.

A spec's `status: approved` records that a person agreed to a contract. On its own it does not say
WHICH text they agreed to, so an approved spec edited afterwards still reads as approved, and
anything verified or decomposed against it inherits an approval nobody gave. This script ties the
approval to the text: a person approving a spec records the digest this script prints in the
spec's frontmatter as `approved_digest`, and every later reader runs the script to learn whether
the text still matches.

It only reads. It never writes `approved_digest` or `status`, because approving is a person's act:
the person copies the printed line into the frontmatter themselves.

Usage
-----
    python spec_digest.py SPEC [SPEC ...]
    python spec_digest.py --queue DIRECTORY

For each SPEC it prints the verdict and the digest of the text as it stands now:

    bound         approved, and the text matches the recorded digest
    unbound       approved, with no recorded digest: the approval is not tied to any text
    changed       approved, and the text no longer matches the recorded digest
    malformed     approved, and the recorded digest is not `sha256:` plus 64 hex digits
    not-approved  the status is anything but `approved`
    unreadable    the file could not be read

`--queue` lists every approved spec directly inside DIRECTORY that is unbound, changed, or
malformed, the person's re-approval queue, and every `.md` file there it could not read.

Exit status: 0 when every SPEC named may be relied on (bound or unbound), 1 when any may not
(changed, malformed, not-approved), 2 when any could not be read or the arguments are wrong. Two
outranks one, because a spec that could not be read is an unanswered question, not a refusal.
`--queue` reports and exits 0, or 2 when the directory, or a file in it, could not be read: a file
it cannot read might be an approved spec, so leaving it out would understate the queue.

The digest
----------
SHA-256 over the spec's body: everything after the closing `---` of its frontmatter, decoded as
UTF-8, with a leading byte-order mark dropped, every line ending normalised to `\\n`, and trailing
newlines at the end of the file removed. The frontmatter is excluded, so setting `status` or
`approved_digest` never changes the digest it is checked against. Line endings and a final newline
are normalised because an editor or a checkout on another platform changes them without anyone
changing a word.
"""
import hashlib
import re
import sys
from pathlib import Path

VERDICTS_RELIED_ON = {"bound", "unbound"}
DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
KEY_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*?)\s*$")


def split(text: str):
    """Return (frontmatter dict, body) for a spec's text. No frontmatter means an empty dict."""
    if text.startswith("﻿"):
        text = text[1:]
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return {}, text
    for end in range(1, len(lines)):
        if lines[end].strip() == "---":
            fields = {}
            for line in lines[1:end]:
                match = KEY_RE.match(line)
                if match:
                    fields[match.group(1)] = match.group(2).strip().strip("'\"")
            return fields, "\n".join(lines[end + 1:])
    return {}, text


def digest(body: str) -> str:
    return "sha256:" + hashlib.sha256(body.rstrip("\n").encode("utf-8")).hexdigest()


def assess(path: Path):
    """Return (verdict, current digest or None, recorded digest or None)."""
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return "unreadable", None, None
    fields, body = split(text)
    current = digest(body)
    recorded = fields.get("approved_digest") or None
    if fields.get("status") != "approved":
        return "not-approved", current, recorded
    if recorded is None:
        return "unbound", current, None
    if not DIGEST_RE.match(recorded):
        return "malformed", current, recorded
    return ("bound" if recorded == current else "changed"), current, recorded


def describe(path: Path, verdict: str, current, recorded) -> str:
    lines = [f"{path}: {verdict}"]
    if current:
        lines.append(f"  digest now:      {current}")
    if recorded:
        lines.append(f"  digest approved: {recorded}")
    if verdict == "changed":
        lines.append("  The text changed after it was approved. Nothing may be verified or "
                     "decomposed against it until a person re-reads it and records the new digest.")
    elif verdict == "unbound":
        lines.append("  Approved, but the approval is not tied to any text.")
    if verdict in ("unbound", "changed", "malformed", "not-approved") and current:
        lines.append(f"  To approve this text, a person sets in its frontmatter: "
                     f"status: approved, and approved_digest: {current}")
    return "\n".join(lines)


def main(argv=None, out=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    out = sys.stdout if out is None else out
    if not argv or argv[0] in ("-h", "--help"):
        out.write(__doc__)
        return 0 if argv else 2
    if argv[0] == "--queue":
        if len(argv) != 2:
            out.write("usage: spec_digest.py --queue DIRECTORY\n")
            return 2
        directory = Path(argv[1])
        try:
            candidates = sorted(p for p in directory.iterdir() if p.suffix == ".md" and p.is_file())
        except OSError as error:
            out.write(f"{directory}: cannot read the directory ({error})\n")
            return 2
        queued, unread = [], []
        for path in candidates:
            verdict, current, recorded = assess(path)
            if verdict in ("unbound", "changed", "malformed"):
                queued.append(describe(path, verdict, current, recorded))
            elif verdict == "unreadable":
                unread.append(describe(path, verdict, current, recorded))
        out.write("\n".join(queued + unread) + ("\n" if queued or unread else ""))
        out.write(f"{len(queued)} approved spec(s) waiting on a person's re-approval in {directory}\n")
        if unread:
            out.write(f"{len(unread)} file(s) could not be read, so the queue may be longer\n")
            return 2
        return 0
    worst = 0
    for name in argv:
        verdict, current, recorded = assess(Path(name))
        out.write(describe(Path(name), verdict, current, recorded) + "\n")
        if verdict == "unreadable":
            worst = 2
        elif verdict not in VERDICTS_RELIED_ON and worst == 0:
            worst = 1
    return worst


if __name__ == "__main__":
    sys.exit(main())
