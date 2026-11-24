# Dogfood record: WS-E, platform and gates (`feat-0094`)

Plan rule 8 of the [Marjana plan](../2026-11-24-marjana-plan.md): every skill this workstream owns or
used, what it ran on, the evidence, the verdict, and what changed because of it. Run on 2026-11-24
from `zen/marjana-ws-e`, branched at `9598355`. Every command below was run in this session; output
is quoted verbatim, trimmed only where marked.

This kit's skills were not installed in the session (the reachability hook said so at start), so
each skill was followed by reading its `SKILL.md`. That is why the observatory row below finds no
`Skill` tool call.

## `tdd`: one red and one green run per change

Each change was written test-first. Where the first red was an interface error (a missing keyword
argument) rather than the missing behaviour, the interface was added as a no-op and the tests
re-run, so that each red below fails on the behaviour, as step 3 requires.

| Change | Red (before the code) | Green (after) |
|---|---|---|
| `R-005` "Done when" warning | `python3 -m unittest tests.test_validate_skills.TestStepsEndOnDoneWhen`: `FAILED (failures=4, errors=3)`; e.g. `'with no "Done when" line' not found in '...0 warning(s)...'`, `module 'validate_skills' has no attribute 'steps_missing_done_when'` | same command `OK` (9 tests), once the three drafts below were fixed |
| `P3` roadmap draft-status check | `python3 -m unittest tests.test_run_checks.RoadmapDraftStatusTests`: `FAILED (failures=9)`; e.g. `True is not false : a promoted skill listed as a draft passed` | `OK` (11 tests). The first green run also found a real defect in the new code: a name such as `draft-two` matched the word "draft", so a code span made its own block a draft list. Fixed by reading words with spans masked |
| `P3`, second cycle | WS-A's true rewrite of "Current state" (`zen/marjana-ws-a`), added verbatim as a fixture: `FAILED (failures=1)`, `False is not true` | `OK` (13 tests) after claims are read per sentence, not per block. A first attempt split on colons as well and turned ten tests red, because it cut each draft list off from its own "drafts" heading; it now splits on `.`, `!` and `?` only |
| `P11` budget headline, setup pointer | `python3 -m unittest tests.test_install.BudgetHeadlineTests tests.test_install.SetupPointerTests`: `FAILED (failures=6)`; e.g. `'Description budget: 100 characters' not found` | `OK`; `tests.test_install` 160 tests `OK` |
| `R-001` hermetic home | `python3 -m unittest tests.test_run_checks.HermeticHomeTests`: `FAILED (failures=7)`; e.g. `AssertionError: 'ok' != 'failed'` for the check that reads the real home (this container's home, like a CI runner's, holds no `CLAUDE.md`, so it passed) | `OK`; the real test-suite gate under the hermetic home: `Ran 1471 tests`, with only the two then-expected draft failures |
| `feat-0090` shared link reader | `python3 -m unittest tests.test_install.SharedLinkReaderTests tests.test_install.SpanHelpersAgreeWithTheBacklogValidatorTests`: `FAILED (failures=13)`; e.g. `test_a_fenced_example_link_to_a_draft_is_not_a_draft_refusal: Lists differ: ["alpha links 'grill' as a sibling, ..."] != []` | `OK`; the three tools' modules 370 tests `OK`; placements byte-identical (below) |
| `chore-0059` reduced guard | mutation: `FENCE_RE`'s `{0,3}` changed to `{0,4}` in `_skillmeta.py`: `FAIL: ... (name='FENCE_RE')`, `FAILED (failures=1)` | reverted: `OK` |

**Each new check fails on a constructed bad input and passes on the tree.**

- `R-005`: on the tree it warns, exit 0, for exactly the seven skills the inventory predicted:
  `agent-observatory`, `init-worktracking`, `project-bootstrap`, `quest-tracker`,
  `reconcile-worktrees`, `test-author` and `verifier-agent`. After this workstream's fixes, five
  remain, all owned by other workstreams: `init-worktracking` (8 steps), `project-bootstrap` (5),
  `reconcile-worktrees` (6), `test-author` (5), `verifier-agent` (1).
- `P3`: with the exception list emptied, the base `ROADMAP.md` fails with `32 skill status claim(s)
  in Current state read against 29 SKILL.md file(s), 8 wrong, 0 excepted`. With the list, it passes
  with the same 8 excepted. WS-A's rewrite passes with an empty list, and the report names all eight
  exceptions as `no longer needed`.
- `P11`: `python3 scripts/install.py --dry-run` prints `Description budget: 7200 characters for this
  profile, model-invoked only (core=1610, spine=7200, all=7941).` It printed `7947 ... (core=1610,
  spine=7947, all=9527)` before the change. The difference is the 747 and 1,586 characters P11
  measured.
- `R-001`: the constructed check `sys.exit(1 if (Path.home() / '.claude' / 'CLAUDE.md').exists()
  else 0)` passes outside the gate and fails inside it.
- `feat-0090`: `install.py --dry-run --profile <p>` for `core`, `spine` and `all`, each with and
  without `--include-drafts`, is byte-identical before and after the change: 8, 40 and 47
  placements, and 16, 48 and 55 with drafts. `build-adapters.py --dry-run` is byte-identical too.

## `test-author`: not exercised as a procedure

Its procedure derives tests from an approved spec. Here the behaviour came first and the scenarios
(`S-028` in `validate-skills.md`, the `S-014` amendment in `install.md`) were written alongside it,
so its step 1 would have refused: neither amendment is approved. Not run, for that reason. The
contract work it would have done is in the conformance rows instead, each naming its covering tests.

## `test-quality`: applied to every test written

Its review checklist ran over each new class before commit, and over the delegated
`tests/test_undecodable_names.py` before it was taken. What changed because of it:

- The `P11` oracles are hand-counted (`"a" * 100`, `"b" * 40`) rather than a call back into
  `description_of`, which would have been a tautology.
- Each fixture-only test class gained one test against the real tree, so that a rule which only
  passes on small fixtures shows up. One example is
  `test_this_repositorys_roadmap_has_the_section_this_reads`.
- The delegated module captures output through a strict UTF-8 stream, not `StringIO`. `StringIO`
  accepts a lone surrogate and would have hidden the second defect below.

Verdict: works.

## `systematic-debugging`: one real defect, two sites

The `R-007` module, written by a delegated leaf agent, found that `build-adapters.py` cannot survive
a file name holding the byte `0xff`. The red command was the module's own `expectedFailure` test,
plus a standalone reproduction:

```text
$ python3 repro.py          # plugin_version() over a copy of .agents/ with references/bad-\xffname.md
UnicodeEncodeError: 'utf-8' codec can't encode character '\udcff' in position 26: surrogates not allowed
```

**Cause, confirmed before any fix.** `rglob` hands back the byte as a surrogate escape, and
`plugin_version()` encoded the path as strict UTF-8.

**Fix.** `os.fsencode(rel.as_posix())`, which gives the name's bytes on disk. For every valid UTF-8
name these are the same bytes as before, and `build-adapters.py --marketplace --check` still reports
the committed tree current. The standalone reproduction then printed `0.1.0+a507f4e46cc4`.

**Second site.** Removing the `expectedFailure` marker turned the test red again, at a different
line: `--marketplace --check` printed the differing path to a strict stream. The first defect had
been hiding the second. Fixed with a `_printable()` helper that backslash-escapes the byte. The
module then ran `OK`.

Verdict: works. Step 1's red command is what turned up the second site.

## `verifier-agent`

Run by a fresh-context agent that wrote none of this work (`A7`), over this task's acceptance
criteria. Its verdict is recorded in the "Independent verification" section of
[`feat-0094`](../../../.tasks/done/feat-0094-marjana-platform-and-gates.md).

## `sitrep` (draft, owned): works, with one observation

`python3 .agents/skills/sitrep/scripts/sitrep.py`, run on this repository, exit 0:

```text
waiting on you (0)
in flight (1)
  worktree /home/user/zen-agent-skills [zen/marjana-ws-e]  1 changed paths
blocked (2)
  P1 feat-0095  Integrate the Marjana workstreams, verify independently, and open one pull request  (chore-0100, feat-0091, feat-0092, feat-0093, feat-0094)
  P2 feat-0071  Place the sitrep into Claude Code sessions with a session-start hook, the reporting rules, and its registration  (feat-0070)
...
notice: no integration branch
```

Both blocked entries are true. The observation: this clone has `origin/main` but no `origin/HEAD`
and no local `main`, so the board found no integration branch, and so listed no unmerged branches.
Not fixed here, because it is a behaviour change to `sitrep.py` under a spec. It is offered as a
finding for `feat-0070`. What changed in the skill: the description (569 to 377 characters), a
`core.md` pointer, and a "Done when" on each of its three procedure steps.

## `quest-tracker` (draft, owned): script steps work; publishing not exercised

On a scratch target. `python3 scripts/tracker.py check templates/quest-tracker.html` exits 1 with:

```text
issue:  `storageKey` is still the template's (`quest-template`): give this project its own, so viewers' remembered filters do not mix.
issue:  The page's <title> is missing or still the template's: name the tracker.
```

These are the two refusals step 1 names. `claim --step ws-e-gates --agent ws-e --lines 0 --command
"python3 -c 'print(1)'"` exits 0 and prints a claim whose `command` and `result` (`"1\nexit status
0"`) are separate fields, as rule 4 requires. Step 0 confirmed the host has the capability, but no
tracker was published: a shared page is outward-facing and nobody asked for one.

What changed in the skill:

- The description, from 606 to 382 characters.
- A `core.md` pointer.
- A "Done when" on each of its five steps.
- The rationale notes, moved to `references/why-claims.md`.
- A one-line reason for the 274-line body: steps 1 to 3 and the host section are procedure every
  run needs.

## `agent-observatory` (draft, owned): works

**Step 1.** `.observatory/store.db` was absent, so the answer was to run the ingester, not to parse
transcripts by hand. `python3 scripts/observatory/ingest.py --store <scratch>/obs.db` printed:

```text
2 transcript(s) found, 2 with new content.
788 record(s) ingested, 3629388 byte(s) read.
1 subagent sidecar(s) read.
0 record(s) unreadable.
```

**Step 2.** The question "what did the sessions on this machine use?" was answered from the store,
with its scope: 1 session (this one), 1 subagent run, and tool calls `Bash` 149, `Edit` 2, `Write`
1, `Agent` 1. There were no `Skill` calls, which is the reachability finding above, measured.

**Steps 3 and 4.** Not exercised: no session action was asked for.

What changed in the skill: the description (599 to 386 characters), a `core.md` pointer, and a
"Done when" on each of its four steps.
