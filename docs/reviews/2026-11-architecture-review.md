# Architecture review of the kit's own tooling

**Date:** 2026-11-23. **Skill:** [`improve-architecture`](../../.agents/skills/improve-architecture/SKILL.md), run as a draft, as its promotion use (`feat-0088`). **Run by:** the `kit-refresh-audit` session; step 2's walk was done by one fresh-context leaf subagent, and its two load-bearing claims were checked here (below).

**Status:** report only. Nothing is refactored. The skill wrote its offline HTML report to the operating system's temporary directory, as step 3 requires; this file is the durable record of the same run, kept in the repository because the promotion rule needs a report a person can act on later. That gap between the skill and its use is refinement 1 in `feat-0088`.

## Scope

Chosen by the skill's step 1 command over the last 200 commits:

```bash
git log -n 200 --name-only --format= | sort | uniq -c | sort -rn | head -40
```

The top of the list is ledgers (`CHANGELOG.md` 68 changes, `ROADMAP.md` 23), which are changed by design and were excluded. The code cluster below them was taken as the scope:

| Path | Changes in the window |
|---|---|
| `docs/spec/README.md` | 26 |
| `.tasks/.scaffold.json` | 21 |
| `tests/test_validate_skills.py`, `scripts/validate-skills.py` | 18, 12 |
| `tests/test_install.py`, `scripts/install.py` | 15, 12 |
| `tests/test_observatory_serve.py`, `scripts/observatory/serve.py` | 12, 12 |
| `scripts/build-adapters.py` and the generated `.claude-plugin/plugin/` tree | 6, 79 file changes |

## Candidates

Terms are those of [`vocabulary.md`](../../.agents/skills/improve-architecture/references/vocabulary.md). Dependency categories are its four: in-process, local stand-in, owned remote, third-party.

### 1. One owner for skill frontmatter (Strong, in-process)

- **Files:** `scripts/validate-skills.py` `parse_frontmatter`; `scripts/build-adapters.py` `split_frontmatter` and `discover_skills`; `scripts/install.py` `description_of` and `discover_skills`; `scripts/_skillmeta.py` `_frontmatter_lines`. `BLOCK_SCALAR_RE = re.compile(r"^[|>][+-]?\s*")` is defined three times (validator line 98, installer 168, adapters 186).
- **Problem:** four readers parse one format, and the code says so itself: `install.py` calls its copy "the third copy of this shape in scripts/" and says unifying them "is a standing recommendation, not a drive-by change", and `build-adapters.py` says that "is where the duplication is the real problem". The block-scalar fix (`bug-0006`) had to land in each copy.
- **Deletion test:** deleting `_skillmeta.py` would push metadata reading back onto three callers, so it earns its keep. Deleting one parser copy changes nothing for the others: they are duplicates, not modules.
- **Deepening:** `_skillmeta.py`, which all three scripts already import, gains `frontmatter(text) -> (fields, body)` and `discover_skills()`; the copies go.
- **Wins:** locality (a parser fix happens once); leverage (one interface for three scripts and the description budget).
- **Tests that survive:** the validator's tests through `main` and `_run`; the nine direct `parse_frontmatter` calls and three `split_frontmatter` calls move to the shared module.

### 2. One span-aware reader for links and profile edges (Strong, in-process, a latent defect)

- **Files:** validator `code_span_ranges`, `fenced_block_ranges`, `_link_targets`; adapters `code_span_ranges`, `fenced_block_ranges`, `SIBLING_LINK_RE`, `draft_refusals`; installer `SIBLING_REF_RE`, `sibling_refs`, `closure`, and the loop inside `resolve_profile`.
- **Problem:** the validator skips links inside code spans and fences; the installer and the adapter builder scan raw text. A sibling link shown as a fenced example therefore becomes an install edge and a draft refusal that the validator never checks. AGENTS.md calls that edge load-bearing.
- **Reproduced here, not taken from the walk:** a scratch skill whose only link is `[grill](../grill/SKILL.md)` inside a fenced block gives `install.sibling_refs: {'grill'}` and `validator _link_targets: []`. No shipped skill triggers it today.
- **Deletion test:** each copy is shallow; deleting `sibling_refs` moves one regex into its caller.
- **Deepening:** one shared module with span-aware `link_targets(text)` and `sibling_edges(text)`, called by all three; the installer keeps one `closure`. `.tasks/validate.py` and its template stay copied, because they ship to adopters and an AST test already holds them together.
- **Wins:** locality ("what is a link" decided once, after four separate fixes: `bug-0015`, `bug-0017`, `bug-0023`, `bug-0027` and `bug-0028`); leverage. It also makes `chore-0059`'s proposed identity test unnecessary for copies 3 and 4.
- **Tests that survive:** validator `main` tests and installer tests at `resolve_profile` and `select_skills`. New tests go at `sibling_edges`, the fenced example first.

### 3. Compute the spec index's figures (Worth exploring, local stand-in)

- **Files:** `docs/spec/README.md`; `scripts/check-citations.py` `audit`.
- **Problem:** the index restates scenario counts that only people recompute. No script or test reads the file. The figures moved from "160 scenarios" when `chore-0075` was filed to "Twelve specs, 186 scenarios, all approved." now, by hand each time.
- **Deepening:** `check-citations.py` counts distinct `S-NNN` per spec and fails when the index disagrees.
- **Wins:** locality (one checker instead of every task author). Already filed as [`chore-0075`](../../.tasks/chore-0075-the-spec-readme-carries-derived-arithmetic-that-nothing-recomputes.md); this adds the hot-spot evidence.

### 4. Dispatch observatory routes from the report registry (Speculative, local stand-in)

- **Files:** `scripts/observatory/serve.py`, the `REPORTS` tuple and `do_GET`.
- **Problem:** each report's endpoint is listed in `REPORTS` and again in an if-chain in `do_GET`, with nothing tying the two.
- **Deepening:** each `REPORTS` entry names its builder; `do_GET` dispatches from it.
- **Wins:** locality. Maintainer tooling only, so no adopter is affected either way. One test reaches past the interface (`serve._outcome_of`).

## Looked at and dismissed

- **`.tasks/.scaffold.json`:** its `id_high_water` is an id reservation every new task bumps on purpose; `stale_high_water` in `.tasks/validate.py` checks it.
- **`.claude-plugin/plugin/`:** a generated copy committed for the marketplace; the plugin-tree gate catches drift.
- **`.tasks/validate.py` and its template copy:** must stay copied (it ships), and are held together by an AST test.
- **`run-checks.py`:** thin, but passes the deletion test; without it the gate list is restated in CI.

## Not covered

The bodies of `install()`, `_check_entry`, `check()` and the uninstall and manifest logic; `check-citations.py` past `audit`; `observatory/ingest.py`, `db.py` and `index.html`. None of these is cleared, because none was read in depth.

## Top recommendation

**Candidate 2.** It is the only one with a reproduced latent defect, on the edge the installer resolves profiles from, and doing it first gives candidate 1 the shared module to land in.

## Next step

Steps 4 to 6 (explore the chosen candidate with `grill`, design it twice, hand off as a task) wait for the maintainer to pick a candidate. The promotion condition is "a report a person acted on": acting means picking one and turning it into a task, or rejecting it with a reason.
