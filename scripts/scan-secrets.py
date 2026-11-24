#!/usr/bin/env python3
"""Scan the repository's files for credentials that must never be committed.

    python scripts/scan-secrets.py

Runs as the `secret scan` gate in `run-checks.py`, on every change, documentation-only
ones included: a pasted token in a README is the commonest way a secret reaches a public
repository, so this is the one gate the docs-only scope keeps beside the documentation
checks (`chore-0098`, from `retro` proposal `R-008`).

What it reads: every file git tracks or would add (`git ls-files --cached --others
--exclude-standard`), skipping binaries and files over 1 MB. Outside a git checkout it walks
the tree instead, skipping `.git/` and the usual generated directories.

What it looks for: credential shapes with a fixed, published prefix, so a match is very
unlikely to be anything else (private-key headers, cloud and platform tokens). It does not
guess at high-entropy strings: that finds real secrets and a great many false ones, and a
gate that cries wolf gets switched off. The bound is stated in every report.

A finding names the file, the line and the kind of credential, never the matched text, so
the report cannot itself leak what it found. A line that must carry a credential-shaped
example says `secret-scan: allow` on the same line.

Exit codes: 0 nothing found, 1 at least one finding, 2 the scan could not run.

Standard library only.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MAX_BYTES = 1_000_000
ALLOW_MARKER = "secret-scan: allow"
SKIP_DIRS = {".git", "__pycache__", ".tmp", "node_modules", ".venv", "venv"}

# Each pattern is a credential with a fixed, documented prefix. Built from parts so this
# file does not contain a match for its own patterns.
PATTERNS = [
    ("private key", re.compile("-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP |ENCRYPTED )?"
                               "PRIVATE" + " KEY-----")),
    ("AWS access key id", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}\b")),
    ("GitHub fine-grained token", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{60,}\b")),
    ("Anthropic API key", re.compile(r"\bsk-ant-[A-Za-z0-9_-]{20,}")),
    ("OpenAI API key", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9]{40,}\b")),
    ("Slack token", re.compile(r"\bxox[abposr]-[A-Za-z0-9-]{10,}")),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
    ("Stripe live key", re.compile(r"\b[rs]k_live_[0-9A-Za-z]{24,}\b")),
]


def candidate_files(root=REPO_ROOT, runner=None):
    """Repository-relative paths to scan: git's view when available, else a tree walk."""
    runner = subprocess.run if runner is None else runner
    try:
        done = runner(["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
                      cwd=str(root), capture_output=True)
    except OSError:
        done = None
    if done is not None and done.returncode == 0:
        return sorted({p for p in done.stdout.decode("utf-8", "surrogateescape").split("\0")
                       if p})
    found = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            found.append(str(Path(dirpath, name).relative_to(root)).replace("\\", "/"))
    return sorted(found)


def scan_text(text):
    """`[(line_number, kind)]` for every credential-shaped match outside an allowed line."""
    findings = []
    for number, line in enumerate(text.splitlines(), start=1):
        if ALLOW_MARKER in line:
            continue
        for kind, pattern in PATTERNS:
            if pattern.search(line):
                findings.append((number, kind))
    return findings


def scan(root=REPO_ROOT, runner=None):
    """`(findings, scanned, skipped)` where findings is `[(path, line, kind)]`."""
    findings, scanned, skipped = [], 0, 0
    for rel in candidate_files(root, runner):
        path = Path(root, rel)
        try:
            if not path.is_file() or path.stat().st_size > MAX_BYTES:
                skipped += 1
                continue
            data = path.read_bytes()
        except OSError:
            skipped += 1
            continue
        if b"\0" in data:
            skipped += 1
            continue
        scanned += 1
        text = data.decode("utf-8", "replace")
        findings.extend((rel, line, kind) for line, kind in scan_text(text))
    return findings, scanned, skipped


def main(argv=None, root=REPO_ROOT, runner=None, out=None) -> int:
    out = sys.stdout if out is None else out
    try:
        findings, scanned, skipped = scan(root, runner)
    except Exception as exc:  # report, never crash silently
        out.write(f"could not run: {type(exc).__name__}: {exc}\n")
        return 2
    for rel, line, kind in findings:
        out.write(f"{rel}:{line}: looks like a {kind}. Remove it and rotate the credential; "
                  f"mark a deliberate example with '{ALLOW_MARKER}' on the same line.\n")
    out.write(f"Scanned {scanned} file(s) for {len(PATTERNS)} credential shape(s), skipped "
              f"{skipped} binary or oversized; {len(findings)} finding(s). Fixed-prefix "
              f"shapes only: a credential with no published prefix is not detected.\n")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
