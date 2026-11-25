# AGENTS.md: rules for the Zen Agent Skills repository

Canonical rules for every AI agent working here, whatever the harness. `CLAUDE.md` imports this file. It holds rules only: the reason and the incident behind each one are one link away in [`docs/rationale/agents-md.md`](docs/rationale/agents-md.md), and the layout in detail is in [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

This repo is **Zen Agent Skills**: a portable, cross-harness library of agent skills, plus the tooling that installs them. It tracks itself with its own `init-worktracking` system: strategy in [`ROADMAP.md`](ROADMAP.md), atomic work in [`.quests/`](.quests/), finished work in [`CHANGELOG.md`](CHANGELOG.md), older ledger entries in [`docs/history/`](docs/history/README.md).

**Quality bar: library.** The kit ships to adopters: every change is tested and reviewed, and a skill's interface, a template or a file format is a contract that changes only deliberately.

## 0. Reading protocol

An agent assigned a quest reads exactly: this file in full; its one quest file in `.quests/<id>.md`; and only the files that quest names in `touched_files`, plus any file its body points to. Do not scan `.quests/`, read other agents' quest files, or read `ROADMAP.md` or `CHANGELOG.md` unless your quest cites them. If a `depends_on` quest is not yet in `.quests/done/`, stop and report the blocker.

## 1. What this repository is

A skills library, not an application: the deliverables are the skills and the tooling that distributes them.

## 2. Layout

| Path | Holds |
|---|---|
| [`.agents/skills/`](.agents/skills/) | The skills, one directory each, a harness-agnostic `SKILL.md` in each. |
| [`.agents/rules/`](.agents/rules/) | Swappable lenses skills compose; [`core.md`](.agents/rules/core.md) is the one always-loaded file. Shipped with the skills. |
| [`.agents/hooks/`](.agents/hooks/) | Optional guardrails, opt-in: a *reminder* never blocks, a *gate* blocks only on a decidable condition. [Contract](.agents/hooks/README.md). |
| [`.claude-plugin/`](.claude-plugin/) | Generated marketplace, never edited by hand. A change to a shipped skill or a lens regenerates it with `build-adapters.py --marketplace` in the same commit. |
| [`scripts/`](scripts/) | Distribution tooling, which ships, and maintainer tooling (`observatory/`), which no adopter receives. |
| [`.quests/`](.quests/), [`docs/spec/`](docs/spec/), [`tests/`](tests/) | Work items; behavioural contracts and their reports; tests derived from those contracts. |

`ROADMAP.md` is authoritative for what happens next; [`docs/CATALOG.md`](docs/CATALOG.md) is the narrative for readers.

## 3. Work lifecycle

Altitudes: a **Campaign** and its **Quest chains** live in `ROADMAP.md`; a **Quest** is `.quests/<id>.md`, whose `parent:` links back up; a quest in no chain is a **Side quest**, whose `parent:` names the Campaign. Acceptance is the quest file's mechanical criteria. Decompose a Quest chain into quest files only when it is about to be built. Ids keep their kind prefixes (`feat-`, `bug-`, `chore-`). The terms, with their old names Epic, Feature and Task, are in [`GLOSSARY.md`](GLOSSARY.md); an adopter's `.tasks/` is still read as `.quests/`.

Lifecycle `open -> in_progress -> done`. On completion:

1. The acceptance command passes, and every `depends_on` is in `.quests/done/`.
2. Run `doc-sync` over the reader-facing documents; apply or dismiss each finding.
3. If the quest declares a `spec`, bring its `<spec>.conformance.md` up to date with `spec-conformance`, or record the deferral. Deferring is legal: an unbuilt scenario is recorded as not built, never invented. A matrix written to satisfy this step is worse than no matrix.
4. Move the file to `.quests/done/` with `status: done`, and re-anchor its relative links for the extra directory level.
5. Add one dated line to `CHANGELOG.md`, at most about 300 characters, linking the quest file for detail.
6. Strike the roadmap Quest chain through if it is complete.

**A spec is earned, not a default**: the spec chain is for behaviour a person must agree before it is built. A quest that changes no behavioural contract declares no `spec`.

## 4. Skill structure

- `.agents/skills/<name>/SKILL.md`: frontmatter `name` and `description`, then a harness-agnostic body. The description says what the skill does and when to use it, third person, key use case first (`validate-skills.py` warns over 700 characters). Aim under about 500 lines; supporting files (`templates/`, `references/`) one level deep. Lint with `python scripts/validate-skills.py`.
- **Model-invoked by default.** A skill a person starts by name (orchestrator, scaffold, router) declares `invocation: user` under `metadata`, never as a top-level key: claude.ai and the Skills API accept only six frontmatter keys.
- **A new skill is a draft**, `status: draft` under `metadata`, placed only with `--include-drafts`. A shipped skill names a draft sibling in backticks, never as a relative link.
- **Two body shapes, both valid.** A workflow carries ordered steps; a lens, composed into another skill, carries `Intent`, `Workflow` and `Output`, and says "This skill is a lens" in its body. Neither is retrofitted onto the other. The skill declares its shape; the validator enforces it.
- **Every skill points at every universal lens**, each lens that says `**Scope: universal.**` in its opening (today [`house-style.md`](.agents/rules/house-style.md) and [`autonomy.md`](.agents/rules/autonomy.md)). A topical lens such as [`review-quality.md`](.agents/rules/review-quality.md) is composed only by skills that use it.
- **Whose conventions.** A skill producing its own output follows this kit's house style; a skill writing into a target repository follows that repository's conventions, with this kit's only as the fallback here. A skill that does both says which applies where.

## 5. Portability contract

- **`AGENTS.md` is canonical** in any repo this kit scaffolds; the scaffolded `CLAUDE.md` imports it with `@AGENTS.md`.
- **Write once, adapt thin.** A skill's logic lives only in its `SKILL.md`; per-harness files come from [`build-adapters.py`](scripts/build-adapters.py), never hand-maintained.
- **No tool lock-in in skill bodies.** Gate a single-harness capability behind a clearly labelled optional section.
- **Links resolve where the skill is used.** A skill's link may reach its own files, a sibling skill, or `.agents/rules/`, nothing above. Name any other file in prose. `validate-skills.py` fails on an escape.
- **A relative link to a sibling `SKILL.md` is a profile edge**: [`install.py`](scripts/install.py) pulls that sibling, and everything it links, into the profile. Link only a sibling the skill composes and is broken without; merely naming one is backticks.

## 6. Conventions

- Writing and formatting: [`house-style.md`](.agents/rules/house-style.md) (no em-dashes, sentence-case headings, named sources, relative links, Mermaid). The file is swappable; this reference to it is not.
- Python, including maintainer tooling: standard library only where possible, PEP 8, no third-party dependency unless load-bearing and documented.
- Cross-platform: Windows, macOS and Linux. Prefer `pathlib`; never assume symlinks.

### The acceptance command

```bash
python scripts/run-checks.py
```

[`run-checks.py`](scripts/run-checks.py) runs every gate, all of them even after one fails. Exit 0 all passed, 1 one failed, 2 one could not run (2 outranks 1). A documentation-only change, as [`_change_scope.py`](scripts/_change_scope.py) decides, runs only the documentation gates and the secret scan; `ZEN_CHECKS_SCOPE=full` runs every gate. CI calls the same script.

**Passing it is necessary but not sufficient.** CI runs six cells (three operating systems, two Pythons), and every gate decides a mechanical property only. Buy the rest by hand: **construct the empty or degenerate input and see what the tool actually says**. A check that cannot fail is unchecked.

### The one committed hook

Hook activation is the adopter's, with one exception here: [`.claude/settings.json`](.claude/settings.json) registers [`skill-reachability-reminder.py`](.agents/hooks/skill-reachability-reminder.py) on `SessionStart`, because a user-level registration does not reach a cloud session. One reminder hook that never blocks. **A second hook there, or any gate, is a new decision.** Its command is `python3 <hook> || python <hook>`, legal only because every hook exits 0; a hook that does not changes that command.

### Commits

**No `Co-Authored-By` trailer naming an AI model**, from any agent or automated tool (apply a Copilot Autofix suggestion by hand in your own commit). It deadlocks the `main` ruleset. `.claude/settings.json` sets `attribution.commit` to empty for Claude Code.

### Provenance

Material adapted from elsewhere carries a provenance block. The convention (fields, placement, digest rules) is in [`CONTRIBUTING.md`](CONTRIBUTING.md#provenance-for-material-folded-in-from-elsewhere). Run [`check-provenance.py`](scripts/check-provenance.py) only when your quest names it, never because a footer mentions it (`A10` in [`autonomy.md`](.agents/rules/autonomy.md)).

## 7. Contribution bar

A skill earns a place only if its author actually uses it and has iterated on it. No speculative skills. A drafted skill stays a draft until used and refined; hyper-specific personal skills stay out of the shared kit.

## Agent skills

The kit's skills read this repository's setup from [`docs/agents/zen.md`](docs/agents/zen.md).
