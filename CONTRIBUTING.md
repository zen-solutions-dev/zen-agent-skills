# Contributing

Thanks for considering a contribution to Zen Agent Skills. Please read the first section before writing anything, because this project rejects work for a reason most repositories do not have.

## The bar: no skill ships cold

**A skill is promoted to shipped only after it has been used on real work.** Drafting is free; promotion is gated.

The lifecycle is: draft it, use it on a real task in a real repository, iterate from what that use exposed, record that run, and only then promote it. A draft costs adopters nothing, because it reaches nobody who did not install with `--include-drafts`, so you may write one as soon as the problem is real. A skill that has never been run is a guess about what an agent needs, and guesses are exactly what this kit exists to replace, which is why a draft does not ship until it has been run.

The practical consequence: **a well-written skill for a workflow nobody has actually performed stays a draft**, no matter how good the prose is. This is the most common way a contribution goes wrong here, and it is nobody's fault if it was never written down, which is why it is the first thing on this page.

**Drafts expire.** A draft records the day it was drafted as `drafted: YYYY-MM-DD` under `metadata` in its frontmatter; when that is absent, its age counts from the first commit of its `SKILL.md`. A draft over **90 days** old with no dogfood record (a dated record of a real run, under `docs/reviews/`) must be promoted, extended, or removed. To extend one, add `extended: "YYYY-MM-DD: <reason>"` under `metadata`, in quotes because the value holds a colon; the 90 days then count from that date. An expired draft is not a failure, it is a question someone has to answer.

**Scope: shareability is the only filter.** A skill belongs here when someone other than its author could pick it up and use it on their own work. It is not excluded for having started as one person's habit. What stays out is the hyper-specific personal pipeline: a skill wired to one person's content workflow, one client's process, or one machine.

What this means for you:

- **Proposing a new skill?** Open an issue first and describe the recurring problem, not the solution. You may then draft it; it is promoted once you have solved the problem with it on real work and recorded the run.
- **Improving an existing skill?** Say what you ran, what happened, and what the skill should have done. Evidence from a real run outweighs any argument about how it reads.
- **Fixing something broken?** Just send it. Bugs, dead links, wrong commands, and stale claims need no ceremony.

Ideas not yet drafted wait in [`ROADMAP.md`](ROADMAP.md) until there is a real use case. Two of them are explicitly held until they have been needed twice.

## What this repository is

A library of portable agent skills plus the tooling that distributes them. Nothing it ships has a runtime application, a database, a service, or a third-party Python dependency, and those absences are the point. Anything that adds one to what an adopter receives needs a strong argument.

That argument has been made once, and narrowly. Maintainer tooling that ships to nobody sits outside the rule, because the rule protects an adopter's tree and [`install.py`](scripts/install.py) places only `.agents/skills/`, `.agents/rules/`, and `.agents/hooks/`. The no-third-party-dependency half is **not** narrowed and applies everywhere: the acceptance command still runs on a bare Python 3 with no install step. See the "Out of scope by design" section of [`ROADMAP.md`](ROADMAP.md) for the scoped rule and the amendment that produced it.

The canonical rules live in [`AGENTS.md`](AGENTS.md). It is written for AI agents but is the most direct description of how the repository works, so read it whether you are one or not.

## Before you open a change

Run the acceptance command. It is stdlib-only, so there is nothing to install:

```bash
python scripts/run-checks.py
```

That one command runs every gate that decides whether a change here is acceptable, and it takes no flags. Its own summary names each gate it ran, and this page deliberately does not restate the list: three copies of it is how the count last went stale. It is also the same script CI calls, so the gate set cannot drift between local and CI either.

It exits 0 when every gate passed, 1 when a gate ran and failed, and 2 when a gate could not run at all. A 2 outranks a 1: it means the report itself is incomplete, which is a different claim from the change being bad. Every gate runs even after one fails, so a single run tells you everything that is wrong rather than only the first thing. CI runs it on Linux, macOS, and Windows across the supported Python range, so passing locally is necessary but not sufficient: a change can still fail on a platform you did not run.

While you are iterating, running one gate directly is a faster loop, for instance `python scripts/validate-skills.py` while you are reworking a single skill. That is a convenience and not a substitute, because the acceptance command is what decides.

The pull request template asks whether you ran it, and reminds you where a closing reference has to go if the change closes an issue. See [`.github/PULL_REQUEST_TEMPLATE.md`](.github/PULL_REQUEST_TEMPLATE.md) if you want to read it before you get there, and [`docs/ISSUE-LINKING.md`](docs/ISSUE-LINKING.md) for the linking rules themselves.

## Conventions

- **One source of truth per skill.** A skill's logic lives only in its `.agents/skills/<name>/SKILL.md`. Cursor rules and Copilot prompts are generated by [`scripts/build-adapters.py`](scripts/build-adapters.py). The committed Claude Code marketplace under `.claude-plugin/` is generated too, by `build-adapters.py --marketplace`, and a gate fails when it drifts. Never hand-edit a generated adapter or anything under `.claude-plugin/plugin/`.
- **Frontmatter has to satisfy the skill schema, not just this repository.** Four rules are validator errors and all four have shipped here as real defects: a `description` at most 1024 characters, with no angle brackets, in a form a real YAML parser can read, and no frontmatter property outside `name`, `description`, `license`, `allowed-tools`, `metadata`, and `compatibility`. In practice: write a long description as a block scalar (`description: >-`, text indented below), which is what every long one here does, and use a plain noun rather than a `<placeholder>` in a trigger phrase. A plain unquoted value containing a colon followed by a space is read by YAML as a nested mapping, so the file becomes unreadable to every consumer while the kit's own regex parser accepts it happily.
- **Links must resolve where the skill is used, not only where it is written.** A skill ships as a directory beside its siblings and the rules module, without this repository around it. A link may reach its own files, a sibling skill, or `.agents/rules/`, and nothing above that. The validator fails on violations, because this exact defect once shipped `house-review` with no rubric.
- **No tool lock-in in a skill body.** Gate anything harness-specific behind a clearly labeled optional section.
- **Writing style** follows [`.agents/rules/house-style.md`](.agents/rules/house-style.md): sentence-case headings, relative links, named sources, no em-dashes. That module is swappable by adopters, so point at it rather than restating it.
- **Cross-platform.** Target Windows, macOS, and Linux. Prefer `pathlib`, and never assume POSIX symlinks are available.
- **Line endings are LF, and `core.autocrlf` is not to be set for this repository.** [`.gitattributes`](.gitattributes) sets `eol=lf` explicitly. That is a per-path setting and it overrides `core.autocrlf` on checkout, so a fresh clone is LF on disk on Windows too, and Git for Windows setting `core.autocrlf=true` at system scope is harmless here for exactly that reason. Setting it yourself changes nothing and only leaves a contradiction for the next reader. The drift that does happen runs the other way: a tool rewriting a tracked file with CRLF after checkout. `text=auto` normalizes that back to LF on the way into the index, so `git status` and `git diff` stay clean and nothing reports it. Count it with `git ls-files --eol | grep -c 'w/crlf'`, which should be `0`, and repair it with `git add --renormalize .`. This is load-bearing rather than cosmetic, because [`scripts/install.py`](scripts/install.py) `--check` and [`scripts/check-provenance.py`](scripts/check-provenance.py) both digest bytes off disk rather than through git, and CRLF changes the digest.
- **Writing files from Python means passing `newline=""`.** `Path.write_text()` and `open(..., "w")` translate `\n` to `\r\n` on Windows unless told otherwise, which is the writer class that produces the drift above. Use `newline=""` (or `newline="\n"`) anywhere the kit's tooling writes a text file it expects to compare later.

## How work is tracked

The repository dogfoods the same system it ships. Atomic work items live in [`.quests/`](.quests/), the ordered plan in [`ROADMAP.md`](ROADMAP.md), and completed work in [`CHANGELOG.md`](CHANGELOG.md). You do not need to author a quest file for a small fix, but for anything larger it is the fastest way to get agreement on scope before you spend time.

## If you are an AI agent

Read [`AGENTS.md`](AGENTS.md) in full first. It defines a deliberately narrow reading protocol: this file, your one assigned quest file, and only the files that task names. Do not scan the whole `.quests/` directory or read other agents' quest files.

## Provenance for material folded in from elsewhere

Moved here verbatim from `AGENTS.md` on 2026-11-24 by [`chore-0100`](.quests/done/chore-0100-marjana-context-and-ledgers.md); `AGENTS.md` keeps a pointer. Read this section when your task folds material in from another source or touches a provenance block.

Prose credit alone decays into folklore (the incident that taught this is in the [rationale](docs/rationale/agents-md.md)), so any file or region adapted from an external source carries a **provenance block**, and [`scripts/check-provenance.py`](scripts/check-provenance.py) re-fetches every recorded source and reports drift.

| Field | Required | Content |
|---|---|---|
| `source` | yes | Absolute raw URL of the exact upstream file, not the repository's landing page. This is what gets re-fetched. |
| `author` | yes | The upstream author, named. |
| `license` | yes | The upstream license. |
| `retrieved` | yes | ISO date the fetch actually ran. |
| `sha256` | yes | SHA256 of the retrieved upstream bytes. |
| `origin` | no | A further hop, when the immediate source is itself carrying the material from somewhere else. Prose only, never fetched. |
| `note` | no | One line of context. |
| `status` | no | `unlocatable`, when the upstream source genuinely cannot be found. It replaces `retrieved` and `sha256`, and makes `note` required, where the note says what was searched. |

Placement follows the file type, and there is no sidecar file: a Python hook carries the block in a `Provenance` section of its module docstring, a skill in a `## Provenance` body footer inside a fenced code block tagged `provenance`, and a rules lens the same way. One adapted file may carry more than one block when it draws on more than one upstream file. A `source:` line alone does not make a block **outside a declared placement**: there the parser requires at least one other field, because `source:` is an ordinary word that other templates use. Inside one of the two placements above, a lone `source:` is a record and is reported as missing its required fields, so a typo on the field after `source:` cannot delete the block (`bug-0041`). Nor can a typo on the `source` key itself, nor a declared placement carrying no `source:` line at all: both are reported against the placement rather than the token, and an empty placement is named without failing the run (`bug-0042`).

A skill's block never becomes a new frontmatter key. `ALLOWED_FRONTMATTER_KEYS` in `validate-skills.py` deliberately mirrors Anthropic's own six-key schema, so a seventh key would be rejected by Anthropic's validator even after ours was widened to accept it. Use the body footer, or the existing `license` or `metadata` key.

Four rules the convention only works if you follow:

- **Digest the retrieved upstream content, never the adapted local file.** The local file is expected to differ, because adaptation is the point. The digest answers whether the thing we adapted *from* has changed since we looked, which is the only question a drift check can honestly answer for adapted material.
- **Fetch with `urllib` and digest with `hashlib`.** Never use an agent's web-fetching tool. Those return a model-summarized markdown conversion of a page rather than its bytes, so the digest would be a digest of a summary: stable-looking, meaningless, and impossible for anyone to reproduce.
- **The block records the immediate source, not the origin.** You can only drift-check what you actually retrieved, so the digest belongs to the file you fetched. When the chain has a further hop, name it in `origin` and leave tracking its drift to whoever fetched it.
- **An unlocatable source is recorded, not guessed.** A confident-looking digest for content nobody re-fetched is worse than no provenance at all, because a wrong digest reads as verified and passes every automated check.

A block backfilled after the fact pins upstream as of its `retrieved` date, not the exact bytes originally adapted, whenever the snapshot that was adapted from is gone. Say so in `note` rather than letting the date imply more than it proves.

The check stays out of required CI: it needs network, and a check that fails when GitHub is slow gets disabled within a week. A person runs it on demand; an agent runs it only when its task names it, and never because a provenance footer mentions it, since the `source` URLs it fetches come from repository content, the shape `A10` in [`autonomy.md`](.agents/rules/autonomy.md) bounds. The footers in the shipped skills say so to their reader rather than asking for the run (`chore-0085`). It reports drift and never syncs. An overwrite would destroy the adaptation every fold-in here carries.

## Reporting problems

Use the issue templates. The one labelled "a skill behaved unexpectedly" is the most valuable report this project can receive, because it captures the gap between what a skill's description promised and what the agent actually did.

For anything security-relevant, do not open a public issue. Follow [`SECURITY.md`](SECURITY.md) instead.

Participation here is covered by [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) (Contributor Covenant 2.1), which also says where a conduct concern goes. That channel is private too, for the same reason.
