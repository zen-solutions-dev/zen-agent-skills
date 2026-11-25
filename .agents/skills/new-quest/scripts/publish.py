#!/usr/bin/env python3
"""publish: mirror a repository's local quest tracker to GitHub issues, one way.

    python publish.py                 # dry run: print the plan, change nothing
    python publish.py --offline       # dry run without calling gh at all
    python publish.py --apply         # carry the plan out through gh

The procedure is `references/publishing.md` beside this skill, and the contract is the
publishing section of `docs/spec/zen-config.md` in the Zen Agent Skills repository
(`feat-0106`, scenarios S-047 to S-058). The issue shape it writes was approved by the
maintainer on 2026-11-25 as a one-way door: once adopters' repositories hold issues in
it, changing it costs them. Change it only by amending that contract.

Standard library only. Six properties shape everything below.

**The local tracker is the source of truth.** Issues are a mirror. Nothing read from
GitHub changes a file here, and the script writes no file at all.

**Off unless opted in.** Publishing runs only when `docs/agents/zen.md` parses and sets
`publish: github` with a well-formed `publish_repo`, as the repository's own
`.quests/validate.py` decides. Anything else is off, and the script says why.

**A dry run by default.** Without `--apply` it reads, and at most lists issues through
`gh api`; it never writes to GitHub.

**Idempotent by marker, never by title.** Every published issue ends in a hidden marker
naming its kind and id, and carries the `zen:published` label. A re-run finds its issues
by marker, edits only what changed, and never creates a second issue for one quest.

**It touches only what it owns.** It edits, closes, reopens, labels and links only issues
that carry both `zen:published` and a valid marker. It adds and removes only `zen:`
labels, never `role.*` ones, and it removes only links between two issues it owns.

**It never deletes.** No issue is deleted or transferred. A quest file that is gone, or
turned private after it was published, leaves its issue as it was, and the plan says so.

The `gh` runner is injected (`run_gh`), so the tests drive every path with a fake and
never touch the network.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import posixpath
import re
import shutil
import subprocess
import sys
from pathlib import Path

MARKER_VERSION = "v1"
MARKER_RE = re.compile(
    r"^<!-- zen-publish v1 kind=(quest|spec) id=([A-Za-z0-9._-]+) "
    r"source=(\S+) digest=([0-9a-f]{12}) -->$", re.MULTILINE)
LABEL_PUBLISHED = "zen:published"
LABEL_KIND = {"quest": "zen:quest", "spec": "zen:spec"}
LABEL_IN_PROGRESS = "zen:in-progress"
ZEN_LABELS = {
    LABEL_PUBLISHED: ("5319e7", "Mirrored from the repository's local tracker; edit the file, not the issue"),
    "zen:quest": ("1d76db", "A quest mirrored from .quests/"),
    "zen:spec": ("0e8a16", "A spec mirrored from the spec directory"),
    LABEL_IN_PROGRESS: ("fbca04", "The quest's status is in_progress"),
}
BODY_LIMIT = 65536
SKIP_NAMES = {"README.md", "_TEMPLATE.md"}
LINK_RE = re.compile(r"(!?\[[^\]\n]*\]\()([^)\s]+)(\))")
FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
SCHEME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")


class PublishError(Exception):
    """A step that could not be carried out; the message says which and why."""


# --- reading the repository -------------------------------------------------------------

def load_validator(root):
    """The repository's own validate.py, imported, or None when it has none."""
    for name in (".quests", ".tasks"):
        path = root / name / "validate.py"
        if path.is_file():
            spec = importlib.util.spec_from_file_location("zen_publish_validate", path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
    return None


def read_config(root, validator):
    """`(config, None)` when publishing is on, or `(None, reason)` when it is off.

    The decision is the repository's own validator's, so the publisher never accepts a
    file that `python .quests/validate.py` rejects. Any finding about the publishing keys,
    or a file that does not parse, turns publishing off (S-049, S-050).
    """
    if validator is None:
        return None, "no .quests/validate.py to check docs/agents/zen.md with"
    if not hasattr(validator, "ZEN_PUBLISH_REPO_RE"):
        return None, ("this repository's validate.py predates publishing; update it from "
                      "the kit's init-worktracking template")
    path = root / validator.ZEN_CONFIG_PATH
    if not path.is_file():
        return None, f"{validator.ZEN_CONFIG_PATH} does not exist"
    values, problems = validator.parse_zen_config(path.read_text(encoding="utf-8"))
    if problems:
        return None, (f"{validator.ZEN_CONFIG_PATH} does not parse ({problems[0]}); run "
                      f"python .quests/validate.py")
    findings = validator.zen_config_findings(root)
    if any(f.startswith("config_version") for f in findings):
        return None, f"{findings[0]}"
    publish = values.get("publish")
    if publish in (None, "none"):
        return None, "docs/agents/zen.md does not set publish: github"
    bad = [f for f in findings if f.startswith(("publish", "unknown key 'publish"))]
    if bad:
        return None, f"docs/agents/zen.md: {bad[0]}"
    if publish != "github":
        return None, f"publish {publish!r} is not github"
    spec_dir = values.get("spec_dir")
    if spec_dir in (None, "none") or not (root / spec_dir).is_dir():
        spec_dir = None
    branch = values.get("base_branch")
    return {"repo": values["publish_repo"], "spec_dir": spec_dir,
            "branch": branch if branch not in (None, "none") else "HEAD"}, None


def tracked_files(root):
    """Every path git tracks under `root`, as forward-slash strings."""
    out = subprocess.run(["git", "-C", str(root), "ls-files", "-z"],
                         capture_output=True, check=True).stdout
    return {p.decode("utf-8", "replace") for p in out.split(b"\0") if p}


def split_frontmatter(text):
    """`(frontmatter_text, body)`; frontmatter is "" when the file has none."""
    lines = text.replace("\r\n", "\n").split("\n")
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return "\n".join(lines[:i + 1]), "\n".join(lines[i + 1:]).strip("\n")
    return "", text.strip("\n")


def is_private(fm):
    return str(fm.get("private", "")).strip().lower() == "true"


def read_quests(root, tracked, validator):
    """Every tracked quest file in the tracker directory and its done/, as dicts."""
    tracker = ".quests" if (root / ".quests").is_dir() else ".tasks"
    quests = []
    for rel in sorted(tracked):
        parts = rel.split("/")
        if parts[0] != tracker or not rel.endswith(".md") or parts[-1] in SKIP_NAMES:
            continue
        if not (len(parts) == 2 or (len(parts) == 3 and parts[1] == "done")):
            continue
        text = (root / rel).read_text(encoding="utf-8")
        fm = validator.parse_frontmatter(text) or {}
        qid = fm.get("id")
        if not isinstance(qid, str) or not re.fullmatch(r"[A-Za-z0-9._-]+", qid or ""):
            continue
        status = fm.get("status") if isinstance(fm.get("status"), str) else ""
        quests.append({
            "kind": "quest", "id": qid, "path": rel, "fm": fm,
            "title": fm.get("title") if isinstance(fm.get("title"), str) else qid,
            "status": status, "done": len(parts) == 3 or status == "done",
            "private": is_private(fm), "body": split_frontmatter(text)[1],
            "depends_on": [d for d in fm.get("depends_on") or [] if isinstance(d, str)]
            if isinstance(fm.get("depends_on"), list) else [],
            "spec": fm.get("spec") if isinstance(fm.get("spec"), str) else "",
        })
    return quests


def read_spec(root, tracked, validator, spec_dir, rel):
    """The spec at `rel` when it is a publishable spec file, else None with a reason."""
    if not spec_dir:
        return None, "no spec_dir is configured"
    rel = rel[2:] if rel.startswith("./") else rel
    name = posixpath.basename(rel)
    if (posixpath.dirname(rel) != spec_dir.rstrip("/") or name in SKIP_NAMES
            or not name.endswith(".md") or "." in name[:-3]):
        return None, f"{rel} is not a spec file directly in {spec_dir}"
    if rel not in tracked:
        return None, f"{rel} is not tracked by git"
    text = (root / rel).read_text(encoding="utf-8")
    fm = validator.parse_frontmatter(text) or {}
    title = fm.get("title") if isinstance(fm.get("title"), str) and fm.get("title") else name[:-3]
    return {"kind": "spec", "id": name[:-3], "path": rel, "fm": fm, "title": title,
            "status": fm.get("status") if isinstance(fm.get("status"), str) else "",
            "private": is_private(fm), "body": split_frontmatter(text)[1]}, None


# --- rendering an issue -----------------------------------------------------------------

def rewrite_links(body, source, repo, branch):
    """Relative Markdown links made absolute on GitHub, outside fenced code only."""
    base = posixpath.dirname(source)
    out, fence = [], None
    for line in body.split("\n"):
        match = FENCE_RE.match(line)
        if fence is None and match:
            fence = match.group(1)[0]
        elif fence is not None and match and match.group(1)[0] == fence:
            fence = None
        elif fence is None:
            def fix(m):
                target = m.group(2)
                if SCHEME_RE.match(target) or target.startswith(("#", "/", "<")):
                    return m.group(0)
                path, _, frag = target.partition("#")
                resolved = posixpath.normpath(posixpath.join(base, path)) if path else source
                if resolved.startswith("../") or resolved == "..":
                    return m.group(0)
                url = f"https://github.com/{repo}/blob/{branch}/{resolved}"
                return m.group(1) + url + ("#" + frag if frag else "") + m.group(3)
            line = LINK_RE.sub(fix, line)
        out.append(line)
    return "\n".join(out)


def _cell(value):
    if isinstance(value, list):
        value = ", ".join(value)
    value = str(value or "").replace("|", "\\|").replace("\n", " ")
    return f"`{value}`" if value else ""


def title_of(item):
    return f"Spec: {item['title']}" if item["kind"] == "spec" else f"{item['id']}: {item['title']}"


def render(item, repo, branch):
    """`(title, body)` of the issue for `item`, the marker last (the approved shape)."""
    url = f"https://github.com/{repo}/blob/{branch}/{item['path']}"
    lines = [f"_Published from [`{item['path']}`]({url}) by the Zen kit's `new-quest`. "
             "The file is the source of truth: edits made here are overwritten on the "
             "next publish._", ""]
    fm = item["fm"]
    if item["kind"] == "quest":
        rows = [("id", item["id"]), ("type", fm.get("type")), ("priority", fm.get("priority")),
                ("status", item["status"]), ("mode", fm.get("mode")), ("parent", fm.get("parent")),
                ("spec", item["spec"]), ("scenarios", fm.get("scenarios")),
                ("external", fm.get("external"))]
        lines += ["| Field | Value |", "|---|---|"]
        lines += [f"| {k} | {_cell(v)} |" for k, v in rows if v]
    else:
        lines.append(f"Status: {_cell(item['status']) or 'not stated'}")
    lines += ["", rewrite_links(item["body"], item["path"], repo, branch)]
    text = "\n".join(lines).rstrip("\n")
    title = title_of(item)
    marker_room = 200
    if len(text) + marker_room > BODY_LIMIT:
        note = (f"\n\n_Truncated: GitHub holds at most {BODY_LIMIT} characters. "
                f"Read the rest in [`{item['path']}`]({url})._")
        cut = BODY_LIMIT - marker_room - len(note)
        head = text[:cut]
        heading = head.rfind("\n#")
        text = (head[:heading] if heading > 0 else head).rstrip("\n") + note
    digest = hashlib.sha256((title + "\n" + text).encode("utf-8")).hexdigest()[:12]
    marker = (f"<!-- zen-publish {MARKER_VERSION} kind={item['kind']} id={item['id']} "
              f"source={item['path']} digest={digest} -->")
    return title, f"{text}\n\n{marker}"


# --- reading GitHub ---------------------------------------------------------------------

def run_gh(args, stdin=None):
    """The real runner: `gh` with `args`, no shell. Returns (code, stdout, stderr)."""
    proc = subprocess.run(["gh", *args], input=stdin, capture_output=True, text=True,
                          encoding="utf-8")
    return proc.returncode, proc.stdout, proc.stderr


def _json_pages(text):
    """`gh api --paginate` prints one JSON array per page; join them into one list."""
    decoder, items, i = json.JSONDecoder(), [], 0
    text = text.strip()
    while i < len(text):
        value, i = decoder.raw_decode(text, i)
        items.extend(value if isinstance(value, list) else [value])
        while i < len(text) and text[i].isspace():
            i += 1
    return items


def gh_json(runner, args, stdin=None):
    code, out, err = runner(args, stdin)
    if code != 0:
        raise PublishError(f"gh {' '.join(args[:3])} failed: {(err or out).strip()[:300]}")
    return _json_pages(out) if out.strip() else []


def read_remote(runner, repo):
    """Owned issues by (kind, id), plus what the plan has to report about the rest."""
    issues = gh_json(runner, ["api", "--paginate", "-X", "GET", f"repos/{repo}/issues",
                              "-f", f"labels={LABEL_PUBLISHED}", "-f", "state=all",
                              "-f", "per_page=100"])
    labels = {l["name"] for l in gh_json(runner, ["api", "--paginate", f"repos/{repo}/labels",
                                                  "-X", "GET", "-f", "per_page=100"])}
    owned, notes = {}, []
    for issue in sorted(issues, key=lambda i: i["number"]):
        if "pull_request" in issue:
            continue
        match = MARKER_RE.search(issue.get("body") or "")
        if not match:
            notes.append(f"#{issue['number']} carries {LABEL_PUBLISHED} but no valid marker: "
                         "left alone")
            continue
        key = (match.group(1), match.group(2))
        if key in owned:
            notes.append(f"#{issue['number']} repeats the marker of #{owned[key]['number']} "
                         f"({key[0]} {key[1]}): left alone")
            continue
        owned[key] = {"number": issue["number"], "id": issue["id"],
                      "title": issue.get("title", ""), "state": issue.get("state", "open"),
                      "digest": match.group(4),
                      "body": (issue.get("body") or "").replace("\r\n", "\n"),
                      "labels": {l["name"] for l in issue.get("labels", [])}}
    for (kind, _), issue in owned.items():
        if kind == "spec":
            children = gh_json(runner, ["api", "--paginate", "-X", "GET",
                                        f"repos/{repo}/issues/{issue['number']}/sub_issues"])
            issue["children"] = {c["number"] for c in children}
        else:
            blockers = gh_json(runner, ["api", "--paginate", "-X", "GET",
                                        f"repos/{repo}/issues/{issue['number']}"
                                        "/dependencies/blocked_by"])
            issue["blocked_by"] = {b["number"] for b in blockers}
    return owned, labels, notes


# --- planning ---------------------------------------------------------------------------

def plan(quests, specs, owned, labels, repo, branch):
    """The ordered operations that make GitHub match the tracker, and the notes."""
    ops, notes = [], []
    by_id = {q["id"]: q for q in quests}

    def has_issue(item):
        return (item["kind"], item["id"]) in owned

    published = [q for q in quests if not q["private"] and (not q["done"] or has_issue(q))]
    for q in quests:
        if q["private"] and has_issue(q):
            notes.append(f"{q['id']} is private now and was published as "
                         f"#{owned[('quest', q['id'])]['number']}: left as it is")
    spec_of, spec_items = {}, {}
    for q in published:
        if not q["spec"]:
            continue
        spec, why = specs(q["spec"])
        if spec is None:
            notes.append(f"{q['id']} names spec {q['spec']}, which is not published ({why}): "
                         "its issue is top-level")
        elif spec["private"]:
            notes.append(f"{q['id']} names spec {q['spec']}, which is private: its issue is "
                         "top-level")
            if has_issue(spec):
                notes.append(f"spec {spec['id']} is private now and was published as "
                             f"#{owned[('spec', spec['id'])]['number']}: left as it is")
        else:
            spec_items[spec["id"]] = spec
            spec_of[q["id"]] = spec["id"]
    spec_open = {sid: any(not q["done"] for q in published if spec_of.get(q["id"]) == sid)
                 for sid in spec_items}
    specs_published = [s for sid, s in sorted(spec_items.items())
                       if spec_open[sid] or has_issue(s)]
    items = specs_published + published
    wanted = {(i["kind"], i["id"]) for i in items}
    for key, issue in sorted(owned.items(), key=lambda kv: kv[1]["number"]):
        if key in wanted:
            continue
        if key[0] == "quest" and key[1] not in by_id:
            notes.append(f"#{issue['number']} (quest {key[1]}) has no quest file any more: "
                         "left as it is")
        elif key[0] == "spec" and key[1] not in spec_items:
            notes.append(f"#{issue['number']} (spec {key[1]}) is named by no published quest "
                         "any more, or its file is gone: left as it is")

    # Labels are created only for issues that will carry them: an empty tracker plans nothing.
    needed = ({LABEL_PUBLISHED} | {LABEL_KIND[i["kind"]] for i in items}) if items else set()
    if any(i["kind"] == "quest" and i["status"] == "in_progress" and not i["done"]
           for i in items):
        needed.add(LABEL_IN_PROGRESS)
    for name in sorted(needed - labels):
        color, description = ZEN_LABELS[name]
        ops.append({"op": "create-label", "name": name, "color": color,
                    "description": description})

    for item in items:
        key = (item["kind"], item["id"])
        is_open = (not item["done"]) if item["kind"] == "quest" else spec_open[item["id"]]
        title, body = render(item, repo, branch)
        want = {LABEL_PUBLISHED, LABEL_KIND[item["kind"]]}
        if item["kind"] == "quest" and item["status"] == "in_progress" and is_open:
            want.add(LABEL_IN_PROGRESS)
        if key not in owned:
            ops.append({"op": "create", "key": key, "title": title, "body": body,
                        "labels": sorted(want)})
            continue
        issue = owned[key]
        # The whole body is compared, not only the digest, so an edit made on GitHub is
        # overwritten on the next publish, as the issue's first line promises.
        if body != issue.get("body") or title != issue["title"]:
            ops.append({"op": "edit", "key": key, "title": title, "body": body})
        if is_open and issue["state"] == "closed":
            ops.append({"op": "reopen", "key": key})
        elif not is_open and issue["state"] == "open":
            ops.append({"op": "close", "key": key})
        zen_have = {l for l in issue["labels"] if l in ZEN_LABELS}
        for name in sorted(want - zen_have):
            ops.append({"op": "label-add", "key": key, "name": name})
        for name in sorted(zen_have - want):
            ops.append({"op": "label-remove", "key": key, "name": name})

    # Links, removals first so a quest moving between specs never holds two parents.
    keys_by_number = {issue["number"]: key for key, issue in owned.items()}
    adds = []
    for sid, spec in spec_items.items():
        skey = ("spec", sid)
        want_children = {("quest", q["id"]) for q in published if spec_of.get(q["id"]) == sid}
        have = {keys_by_number[n] for n in owned.get(skey, {}).get("children", set())
                if n in keys_by_number}
        for child in sorted(have - want_children):
            ops.append({"op": "unlink-sub", "parent": skey, "child": child})
        adds += [{"op": "link-sub", "parent": skey, "child": c}
                 for c in sorted(want_children - have)]
    for skey, issue in sorted(owned.items()):
        if skey[0] == "spec" and skey[1] not in spec_items:
            for n in sorted(issue.get("children", set())):
                if n in keys_by_number:
                    ops.append({"op": "unlink-sub", "parent": skey, "child": keys_by_number[n]})
    published_keys = {("quest", q["id"]) for q in published}
    for q in published:
        qkey = ("quest", q["id"])
        want_blockers = {("quest", d) for d in q["depends_on"] if ("quest", d) in published_keys}
        for d in q["depends_on"]:
            if ("quest", d) not in published_keys and d in by_id and not by_id[d]["done"]:
                notes.append(f"{q['id']} depends on {d}, which is not published: no link")
        have = {keys_by_number[n] for n in owned.get(qkey, {}).get("blocked_by", set())
                if n in keys_by_number}
        for b in sorted(have - want_blockers):
            ops.append({"op": "unblock", "key": qkey, "blocker": b})
        adds += [{"op": "block", "key": qkey, "blocker": b}
                 for b in sorted(want_blockers - have)]
    return ops + adds, notes


def describe(op, owned):
    def ref(key):
        return f"#{owned[key]['number']}" if key in owned else "a new issue"
    kind = op["op"]
    if kind == "create-label":
        return f"create label {op['name']}"
    if kind == "create":
        return f"create {op['key'][0]} {op['key'][1]}: {op['title']!r} [{', '.join(op['labels'])}]"
    if kind == "edit":
        return f"edit {ref(op['key'])} ({op['key'][1]}): title and body"
    if kind in ("close", "reopen"):
        return f"{kind} {ref(op['key'])} ({op['key'][1]})"
    if kind in ("label-add", "label-remove"):
        verb = "add" if kind == "label-add" else "remove"
        return f"{verb} label {op['name']} on {ref(op['key'])} ({op['key'][1]})"
    if kind in ("link-sub", "unlink-sub"):
        verb = "make" if kind == "link-sub" else "stop making"
        return (f"{verb} {ref(op['child'])} ({op['child'][1]}) a sub-issue of "
                f"{ref(op['parent'])} (spec {op['parent'][1]})")
    verb = "mark" if kind == "block" else "unmark"
    return (f"{verb} {ref(op['key'])} ({op['key'][1]}) as blocked by "
            f"{ref(op['blocker'])} ({op['blocker'][1]})")


# --- applying ---------------------------------------------------------------------------

def apply(ops, owned, runner, repo):
    """Carry `ops` out in order; stop at the first failure. Returns the count done."""
    done = 0
    for op in ops:
        kind = op["op"]
        if kind == "create-label":
            gh_json(runner, ["api", "-X", "POST", f"repos/{repo}/labels", "--input", "-"],
                    json.dumps({"name": op["name"], "color": op["color"],
                                "description": op["description"]}))
        elif kind == "create":
            made = gh_json(runner, ["api", "-X", "POST", f"repos/{repo}/issues", "--input", "-"],
                           json.dumps({"title": op["title"], "body": op["body"],
                                       "labels": op["labels"]}))[0]
            owned[op["key"]] = {"number": made["number"], "id": made["id"]}
        else:
            key = op.get("key") or op.get("child")
            number = owned[key]["number"]
            path = f"repos/{repo}/issues/{number}"
            if kind == "edit":
                gh_json(runner, ["api", "-X", "PATCH", path, "--input", "-"],
                        json.dumps({"title": op["title"], "body": op["body"]}))
            elif kind == "close":
                gh_json(runner, ["api", "-X", "PATCH", path, "--input", "-"],
                        json.dumps({"state": "closed", "state_reason": "completed"}))
            elif kind == "reopen":
                gh_json(runner, ["api", "-X", "PATCH", path, "--input", "-"],
                        json.dumps({"state": "open"}))
            elif kind == "label-add":
                gh_json(runner, ["api", "-X", "POST", f"{path}/labels", "--input", "-"],
                        json.dumps({"labels": [op["name"]]}))
            elif kind == "label-remove":
                gh_json(runner, ["api", "-X", "DELETE", f"{path}/labels/{op['name']}"])
            elif kind in ("link-sub", "unlink-sub"):
                parent = owned[op["parent"]]["number"]
                body = json.dumps({"sub_issue_id": owned[key]["id"]})
                if kind == "link-sub":
                    gh_json(runner, ["api", "-X", "POST",
                                     f"repos/{repo}/issues/{parent}/sub_issues", "--input", "-"],
                            body)
                else:
                    gh_json(runner, ["api", "-X", "DELETE",
                                     f"repos/{repo}/issues/{parent}/sub_issue", "--input", "-"],
                            body)
            elif kind == "block":
                gh_json(runner, ["api", "-X", "POST", f"{path}/dependencies/blocked_by",
                                 "--input", "-"],
                        json.dumps({"issue_id": owned[op["blocker"]]["id"]}))
            elif kind == "unblock":
                gh_json(runner, ["api", "-X", "DELETE",
                                 f"{path}/dependencies/blocked_by/{owned[op['blocker']]['id']}"])
        done += 1
    return done


# --- the command ------------------------------------------------------------------------

def main(argv=None, runner=None, out=None):
    out = out or sys.stdout
    parser = argparse.ArgumentParser(description="Mirror .quests/ to GitHub issues, one way.")
    parser.add_argument("--repo-root", default=".", help="the repository (default: .)")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--apply", action="store_true", help="carry the plan out through gh")
    mode.add_argument("--offline", action="store_true",
                      help="dry run that calls nothing, planning as if nothing were published")
    args = parser.parse_args(argv)
    root = Path(args.repo_root).resolve()

    def say(text=""):
        print(text, file=out)

    validator = load_validator(root)
    config, reason = read_config(root, validator)
    if config is None:
        say(f"Publishing is off: {reason}. Nothing was read from or sent to GitHub.")
        return 1 if args.apply else 0
    repo = config["repo"]
    try:
        tracked = tracked_files(root)
    except (OSError, subprocess.CalledProcessError) as exc:
        say(f"Could not list tracked files with git ({exc}); nothing planned.")
        return 2
    quests = read_quests(root, tracked, validator)
    cache = {}

    def specs(rel):
        if rel not in cache:
            cache[rel] = read_spec(root, tracked, validator, config["spec_dir"], rel)
        return cache[rel]

    runner = runner or (run_gh if shutil.which("gh") else None)
    owned, labels, notes = {}, set(), []
    if args.offline:
        notes.append("offline: GitHub was not read, so the plan assumes nothing is "
                     "published yet")
    elif runner is None:
        if args.apply:
            say("Cannot apply: gh is not installed. Install the GitHub CLI and run gh auth login.")
            return 2
        notes.append("gh is not installed: the plan assumes nothing is published yet")
    else:
        try:
            owned, labels, notes = read_remote(runner, repo)
        except PublishError as exc:
            if args.apply:
                say(f"Cannot apply: {exc}")
                return 2
            notes.append(f"GitHub could not be read ({exc}): the plan assumes nothing is "
                         "published yet")
    ops, plan_notes = plan(quests, specs, owned, labels, repo, config["branch"])
    notes += plan_notes

    say(f"{'Applying' if args.apply else 'Dry run'}: {len(ops)} operation(s) on {repo}, "
        f"from {sum(1 for q in quests)} quest file(s).")
    for n, op in enumerate(ops, 1):
        say(f"{n:4}. {describe(op, owned)}")
    for note in notes:
        say(f"note: {note}")
    if not args.apply:
        say("Nothing was changed. Run again with --apply to carry this plan out.")
        return 0
    try:
        done = apply(ops, owned, runner, repo)
    except PublishError as exc:
        say(f"Stopped: {exc}. Run again to continue: the plan picks up where this stopped.")
        return 1
    say(f"Applied {done} operation(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
