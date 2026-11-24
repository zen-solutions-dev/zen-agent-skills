---
id: feat-0083
title: Bind a spec's approval to the text a person approved, and block on text changed since
type: feat
status: done
priority: P1
parent: "ROADMAP Epic B: contract-driven delivery (the agent-workflow spine)"
depends_on: []
spec: docs/spec/verifier-agent.md
scenarios: [S-012, S-013]
touched_files:
  - .agents/skills/spec-author/scripts/spec_digest.py
  - .agents/skills/spec-author/SKILL.md
  - .agents/skills/verifier-agent/SKILL.md
  - .agents/skills/new-task/SKILL.md
  - .agents/skills/spec-plan-readiness/SKILL.md
  - .agents/skills/test-author/SKILL.md
  - tests/test_spec_digest.py
  - tests/test_validate_skills.py
  - docs/spec/verifier-agent.md
  - docs/spec/verifier-agent.conformance.md
  - docs/spec/spec-author.md
  - docs/spec/spec-author.conformance.md
  - docs/spec/test-author.md
  - docs/spec/README.md
  - .claude-plugin/plugin/
  - ROADMAP.md
  - CHANGELOG.md
  - .tasks/.scaffold.json
created: 2026-10-28
---

## Problem

`status: approved` says a person agreed to a contract. It does not say **which text** they agreed
to. An approved spec edited afterwards still reads `approved`, so `verifier-agent` verifies against
it, `new-task` decomposes it, and the evidence that results carries an approval nobody gave.
[`verifier-agent`](../../.agents/skills/verifier-agent/SKILL.md) already refuses to verify against a
draft because that "launders an unapproved contract into evidence"; text edited after approval is
the same contract in different clothes.

[`docs/spec/README.md`](../../docs/spec/README.md) knew this and recorded "a separate frontmatter key"
as "the preferred form if this is ever mechanised", deferred because the readers would stall on an
amended spec and because retrofitting every approved spec is "the author's pass and not an
agent's". The idea of binding an approval to a content hash comes from the 2026-10-28 read of
everything-claude-code's `operator-approval-loop`, which ties an approval to a draft's SHA-256 so
rewriting the draft voids it.

## Scope

**In scope:**
- A read-only, stdlib [`spec_digest.py`](../../.agents/skills/spec-author/scripts/spec_digest.py)
  shipped with `spec-author`: per spec, a verdict (`bound`, `unbound`, `changed`, `malformed`,
  `not-approved`, `unreadable`) and the digest of the text now; `--queue <directory>` for the
  re-approval queue.
- `spec-author` documents `approved_digest`, never writes it, and keeps it unchanged on an
  amendment.
- `verifier-agent`, `new-task`, `spec-plan-readiness`, and `test-author` run the script and block
  on `changed` or `malformed` (and, where a spec cannot be read, on `unreadable`); `unbound`
  proceeds and is reported. Each links `spec-author`, so an install that places one places the
  script. `test-author` was missed by the first version and found by the independent
  verification: tests are the most durable form a contract takes, and `A11` makes them the judge.
- Amendments, pending the maintainer's re-approval, to `docs/spec/verifier-agent.md` (S-012, S-013,
  the approval constraint) and `docs/spec/spec-author.md` (S-010, S-011, a constraint, two surface
  rows), with conformance rows in both matrices; the spec index's convention brought up to date.

**Out of scope:**
- Binding any existing spec. Every spec approved before this task is `unbound` until the maintainer
  re-reads it (decision 2 below).
- A CI gate on `changed`. A red check that only a person can turn green invites an agent to edit the
  digest, which `A11` forbids; the readers that consume a spec are where the block belongs.
- `spec-plan-readiness` gaining a check on `status` itself. It reads approval only for the digest.

## Decisions

Answered by Hamsa during the session that built this task:

1. **A spec whose text no longer matches its `approved_digest` blocks** verification,
   decomposition, and the readiness gate until re-approved, rather than proceeding with a warning.
2. **Existing approved specs are bound as the maintainer re-reads each**, not all at once, because
   binding them wholesale would declare every pending amendment approved without anyone reading it.

Recorded by the implementer:

- **A rejected alternative: recording the approving commit instead of a digest.** A commit needs the
  history present and reachable; a shallow clone or a cloud checkout may have neither. A digest of
  the text needs only the file.
- **A seam left open deliberately: the digest excludes the frontmatter.** Recording `status` and
  `approved_digest` must not change the digest they are checked against, so only the body counts.
  Line endings, a byte-order mark, and trailing newlines are normalised for the same reason: none
  of them changes what a person agreed to.
- **A seam left open deliberately: the script never writes approval.** It prints the line to copy.
  A script with an `approve` command would be one an agent can run.
- **A premise that turned out false: `check-citations.py` proves the matrix quotes.** It audits
  backtick spans only, so the double-quoted phrases in the conformance rows went unchecked, and
  two of them went stale in this change. Each quoted phrase in the rows this task touched was
  checked against the skill text by hand, whitespace-normalised.

## Risks and rollback

This task touches more than one module (four skills, two contracts, the spec index), so the rule
fires.
- **What could go wrong:** a bound spec amended in a pull request blocks that pull request's own
  verification until the maintainer re-approves. That is the decided behaviour, and the spec index
  says so.
- **What could go wrong:** the readers drift from the script. `tests/test_spec_digest.py` asserts
  every reader links `spec-author`, names the script, and names the `changed` verdict.
- **Rollback:** revert the commit. No existing spec carries `approved_digest`, so nothing persisted
  depends on it.

## Acceptance criteria (mechanically verifiable)

    python -m unittest tests.test_spec_digest -v
    python scripts/validate-skills.py
    python scripts/run-checks.py

- [x] The six verdicts and the three exit statuses are each asserted on a real file.
- [x] CRLF, a final newline, and a byte-order mark do not change a digest; a one-word edit does.
- [x] Recording `status` and `approved_digest` does not change the digest; the printed line binds.
- [x] `--queue` lists unbound and changed approved specs and skips drafts and sibling reports.
- [x] The script writes nothing (AST guard).
- [x] Every reader, `test-author` included, links `spec-author` and names the script and
      `changed`.
- [x] `verifier-agent`'s deterministic verdict rule names every blocking verdict, so it agrees with
      its step 1 and S-012. The first version left the rule saying only "not `approved`".
- [x] `--queue` names a file it could not read, a broken symlink included, and exits 2, rather
      than leaving it out of the count.
- [x] `install.py --skills verifier-agent` places `spec-author`; the `core`, `spine`, and `all`
      profiles place the same skills as before.
- [x] S-012 and S-013 in `verifier-agent.conformance.md`, S-010 and S-011 in
      `spec-author.conformance.md`, and `check-citations.py` resolves every quoted citation.

## Definition of done

- [x] Acceptance command(s) pass locally.
- [x] Conventions in AGENTS.md's conventions section followed.
- [x] `doc-sync` run over the reader-facing documents. `docs/spec/README.md` was the one whose
      claims this change falsified ("no marker key yet", re-approval "granted by editing the
      note") and is updated. `README.md`, `docs/CATALOG.md`, and `docs/GETTING-STARTED.md` describe
      approval as a person's act, which stays true, and needed nothing.
- [x] The declared spec's conformance matrix is up to date for S-012 and S-013.
- [x] File in `.tasks/done/`, `status: done`; one dated line added to `CHANGELOG.md`.
