# Architecture review of `scripts/`

**Date:** 2026-11-24. **Read at:** commit `4b41861`. **Skill:** [`improve-architecture`](../../.agents/skills/improve-architecture/SKILL.md), steps 1 to 3. **Run by:** one leaf agent with no subagents, so step 2's walk was done in this session and every claim below was checked against the file it cites.

**Status:** report only. Nothing is refactored. The offline HTML report went to the session's scratch directory; this file is the durable record of the same run, written because the person was not present to pick a candidate. Another workstream may be editing `scripts/` on another branch, so every `path:line` below is as of `4b41861`.

This run follows the [2026-11 architecture review](2026-11-architecture-review.md) of the whole kit. Its candidates 1, 2 and 4 are rechecked here at the new commit; candidate 3 lives in `docs/spec/` and is outside this scope.

## Scope

The direction was `scripts/`, given by the person. Step 1's hot-spot command, restricted to it:

```bash
git log -n 200 --name-only --format= -- scripts/ | sort | uniq -c | sort -rn | head -30
```

| Changes | Path |
|---|---|
| 34 | `scripts/install.py` |
| 23 | `scripts/validate-skills.py` |
| 15 | `scripts/build-adapters.py` |
| 12 | `scripts/observatory/serve.py` |
| 10 | `scripts/check-provenance.py` |
| 9 | `scripts/observatory/ui/index.html` |
| 7 | `scripts/run-checks.py` |
| 5 | `scripts/observatory/ingest.py` |
| 4 | `scripts/check-citations.py` |
| 1 or 2 each | `observatory/pricing.json`, `observatory/db.py`, `scan-secrets.py`, `_textio.py`, `_skillmeta.py`, `_change_scope.py` |

Only 81 commits touch `scripts/`, so the 200-commit window is its whole history. **Corrected
2026-11-24** in the landing review's fix round: the first run counted from a shallow clone (48
commits, `install.py` 17); the table above is recounted on a full clone (`git fetch --unshallow`).
The same five files lead either way, so the scope and the candidates are unchanged. Left out of the ranking: `observatory/pricing.json`, a rate table that changes by design. Nothing else in `scripts/` is a ledger or generated tree. The top cluster taken as the scope is `install.py`, `validate-skills.py`, `build-adapters.py`, `observatory/serve.py` and `check-provenance.py`, with `_skillmeta.py` and `observatory/db.py` read because the candidates land in them.

No glossary or decision record (ADR) exists for `scripts/`. [`AGENTS.md`](../../AGENTS.md) acts as one: the stdlib rule, the profile-edge rule, and the shipped `.tasks/validate.py` copy are constraints, not candidates.

## Candidates

Terms are those of [`vocabulary.md`](../../.agents/rules/deep-modules.md). Dependency categories are its four: in-process, local stand-in, owned remote, third-party.

### 1. Give the install manifest entry a module of its own (Strong, local stand-in)

- **Files:** `scripts/install.py`: `install` (706), `uninstall` (1292), `_check_entry` (1402), `check` (1607), `_validate_manifest` (388), `ADOPTED_ENTRY_NAMES` (484).
- **Problem:** a manifest entry is a bare dict built by hand in four places and classified again by each of its four readers, so what kind of entry a record is (derived skill, hooks, adopted rules, merged rules) has no owner.
- **Evidence, each checked in the file:**
  - Four hand-built literals: `install.py:801`, `:834`, `:847`, `:869`.
  - Kind re-derived by name at `install.py:1441`, `:1472`, `:1486`, `:1653` (`entry.get("name") in ADOPTED_ENTRY_NAMES`), and by mode at `:828`, `:1334`, `:1498` (`.get("mode") == "merged"`).
  - A leak across the `_check_entry` seam: `check` finds an orphaned entry by searching the prose of the returned message, `if status == "diverged" and "so is the home it sat in" in message:` (`install.py:1650`). Rewording the message at `:1458-1460`, where the phrase already straddles two string literals, silently breaks the orphan count.
  - The code says the invariant has no home: the comment at `install.py:374-379` records that `uninstall` broke it (`bug-0053`) and that "the comment is the only place the two facts are stated together".
  - The stated invariant already does not hold: the comment at `install.py:357` says every key a reader dereferences is listed in `_OPTIONAL_ENTRY_TYPES`, and `mode` is read at `:828`, `:1334` and `:1498` but is not listed (`:366-373`). Harmless today, because each read is a comparison, but it shows the list and its readers drifting.
  - Nine issue ids are cited in the manifest code alone (`install.py:346-520` and `:1292-1686`): `bug-0012`, `bug-0018`, `bug-0020`, `bug-0022`, `bug-0024`, `bug-0053`, `bug-0056`, `chore-0031`, `chore-0082`.
- **Deletion test:** there is no module to delete; the complexity already sits on every caller. Deleting `_validate_manifest` would put the type checks back on four readers, so it earns its keep, but it covers only the shape and not the kind.
- **Proposed deepening:** one `ManifestEntry` module (inside `install.py` or beside it) with constructors for each kind, a `kind` property, and `.get()`-safe accessors, and `_check_entry` returning a verdict that carries `orphaned` as a field rather than as words in a sentence.
- **Wins:** locality (the adopted and merged rules are decided once, where `bug-0018`, `bug-0020` and `bug-0022` each had to fix a reader); leverage (one interface for `install`, `uninstall`, `check` and `_check_entry`); tests stand where callers stand (a test asserts `verdict.orphaned`, not a substring).
- **Dependency category:** local stand-in. The entries describe files under a home directory; the existing tests already run against a temporary home, which stays the stand-in.

### 2. One span-aware Markdown reader for links, fences and profile edges (Strong, in-process)

- **Files:** `scripts/validate-skills.py` `code_span_ranges` (246), `fenced_block_ranges` (277), `_link_targets` (306); `scripts/build-adapters.py` `code_span_ranges` (219), `fenced_block_ranges` (250), `SIBLING_LINK_RE` (181); `scripts/install.py` `SIBLING_REF_RE` (161), `sibling_refs` (312); `scripts/check-provenance.py` `_FENCE_RE` (128), `declared_lines` (219), `parse_records` (334).
- **Problem:** four scripts decide what counts as code in a Markdown file, under three different rules.
- **Evidence, each checked in the file:**
  - The previous review's finding still holds at `4b41861`: the validator and the adapter builder carry byte-identical span helpers (a diff of the two `code_span_ranges` bodies differs only in line numbers), and the installer scans raw text (`install.py:315`).
  - New here: `check-provenance.py` has its own fence rule, `_FENCE_RE` at `:128`, accepting backtick and tilde fences at any indent and closing on the next fence line with no width check (`:247-248`). The validator's rule, `FENCE_RE` at `validate-skills.py:123`, accepts only backticks, up to three spaces of indent, and closes on a fence at least as wide.
  - Reproduced in this session: a 4-backtick example fence holding a `provenance` block is one fence to `validate-skills.fenced_block_ranges` and a live record to `check-provenance.parse_records`, which reports it as "missing required field(s): license, retrieved, sha256". A `~~~` fence holding `[grill](../grill/SKILL.md)` is no fence to the validator, which returns the link as live.
- **Deletion test:** each copy is shallow. Deleting `sibling_refs` moves one regex into its caller; deleting one `fenced_block_ranges` changes nothing for the other.
- **Proposed deepening:** one shared module, beside `_skillmeta.py`, exposing `code_ranges(text)`, `link_targets(text)` and `sibling_edges(text)`, called by the validator, the installer, the adapter builder and `check-provenance.py`. The shipped `.tasks/validate.py` copy stays copied, as `AGENTS.md` and the AST test require.
- **Wins:** locality (what counts as code is decided once); leverage (four callers, one interface); the profile edge `AGENTS.md` calls load-bearing is read by the same rule the validator checks.
- **Already filed:** [`feat-0090`](../../.quests/done/feat-0090-one-span-aware-reader-for-links-and-profile-edges.md) covers the validator, installer and adapter builder. It does not name `check-provenance.py`; the fence divergence above is new evidence for widening it or for a follow-up.
- **Dependency category:** in-process.

### 3. One owner for skill frontmatter and discovery (Strong, in-process)

- **Files:** `scripts/validate-skills.py` `parse_frontmatter` (209), `BLOCK_SCALAR_RE` (98); `scripts/build-adapters.py` `split_frontmatter` (418), `discover_skills` (452), `BLOCK_SCALAR_RE` (186); `scripts/install.py` `description_of` (191), `discover_skills` (184), `BLOCK_SCALAR_RE` (168); `scripts/_skillmeta.py` `_frontmatter_lines` (51); `scripts/observatory/serve.py` (77, 573).
- **Problem:** four readers parse the same frontmatter and two discover the same skills, and the shared module all three main scripts already import (`build-adapters.py:119`, `install.py:120`, `validate-skills.py:61`) owns only the `metadata` block.
- **Evidence, each checked in the file:**
  - `BLOCK_SCALAR_RE` is defined three times with the same pattern; `split_frontmatter`'s own docstring calls the validator copy "where the duplication is the real problem" (`build-adapters.py:425-426`).
  - `discover_skills` is the same five lines at `install.py:184` and `build-adapters.py:452`.
  - New here: the observatory imports all of `install.py` (`serve.py:77`) to call one function, `install.discover_skills()` (`serve.py:573`).
  - `feat-0090` defers this candidate explicitly ("Unifying frontmatter parsing (the review's candidate 1) ... as its own task", `feat-0090:37`), and no task carries it yet.
- **Deletion test:** deleting `_skillmeta.py` would push metadata reading back onto three callers, so it earns its keep. Deleting one parser copy changes nothing for the others: they are duplicates, not modules.
- **Proposed deepening:** `_skillmeta.py` gains `frontmatter(text) -> (fields, body)` and `discover_skills()`; the copies and the observatory's import of the installer go.
- **Wins:** locality (a parser fix like `bug-0006` lands once); leverage (one interface for four scripts); the observatory stops depending on the installer's whole interface.
- **Dependency category:** in-process.

### 4. Dispatch observatory routes from the report registry (Speculative, local stand-in)

- **Files:** `scripts/observatory/serve.py`, `REPORTS` (116-133) and `ObservatoryHandler.do_GET` (2343).
- **Problem:** each report's endpoint is named in `REPORTS` and again in an if-chain at `serve.py:2370-2385`, with nothing tying the two.
- **Deletion test:** not applicable; this is a missing link between two existing pieces rather than a shallow module.
- **Proposed deepening:** each `REPORTS` entry names its builder, and `do_GET` dispatches from it.
- **Wins:** locality (adding a report is one edit). Maintainer tooling only, so no adopter is affected.
- **Dependency category:** local stand-in (the SQLite store the tests already build).
- **Unchanged from the previous review.** Five reports, all built, so the payoff waits on a sixth.

### 5. Give the session store a read interface (Speculative, local stand-in)

- **Files:** `scripts/observatory/db.py` (`SCHEMA` at 43, `connect` at 211); `scripts/observatory/serve.py`.
- **Problem:** `db.py` owns the schema and the connection, but every read is raw SQL in `serve.py`: 22 `SELECT` statements against seven of its tables (`message` nine times, `session` five), so the schema itself is the interface between the two.
- **Deletion test:** deleting `db.py` would push schema creation and version checks onto `ingest.py` and `serve.py`, so it earns its keep; its read side is absent rather than shallow.
- **Proposed deepening:** named read functions in `db.py` (sessions in scope, messages for a session, agent runs) that the five report builders call.
- **Wins:** locality (a schema change, now at version 4 per `db.py:27`, touches one module); tests stand where callers stand.
- **Dependency category:** local stand-in (SQLite on a temporary file).
- **Why speculative:** `db.py` changed twice in the window; the friction is structural rather than observed in the history.

## Looked at and dismissed

- **`run-checks.py`:** carries the roadmap gate inline (`check_roadmap`, 241) where other gates are separate scripts. It passes the deletion test, and its `markdown_blocks` (202) reads paragraphs, not code, so it is not a fifth Markdown reader in the sense of candidate 2.
- **The `_textio` import preamble** repeated at the head of four scripts (for example `build-adapters.py:111-119`): five lines each, and the comment explains why the two invocation paths need it. Not worth a module.
- **`check-citations.py`:** four changes in the window, one entry point (`audit`, 560), self-contained.

## Not covered

`build-adapters.py` past its parsing helpers; `install.py`'s `_place_adopted` and `_place_merged` bodies; `observatory/ingest.py`, `observatory/ui/index.html`, `scan-secrets.py` and `_change_scope.py`. None of these is cleared, because none was read in depth.

## Top recommendation

**Candidate 1, the manifest entry.** `install.py` is the top hot spot in `scripts/`, the manifest code alone cites nine issues, the one place the kind of an entry is decided is a comment, and nothing is filed for it. Candidate 2 is equally strong but already has `feat-0090` in flight; the cheapest action there is to add `check-provenance.py`'s fence rule to that task's scope.

## Next step

Steps 4 to 6 (explore the chosen candidate with `grill`, design it twice, hand off as a spec or task) wait for the person to pick a candidate.
