# orchestrate: the memory, its layout and its lint

Reference for Step 7 and "Memory: write history, not the present" in [`../SKILL.md`](../SKILL.md).
The rules there decide what an entry says; this file decides where it goes and how it is kept
honest.

## Where it lives

The `memory` key of the repository's setup file names the index, a file; the entries sit in the
same directory. Without the key, use wherever the repository already keeps dated notes, else a
location agreed with the person before the first write. In the Zen Agent Skills repository the key
is `docs/agents/memory/README.md` (set on 2026-11-25, `feat-0107`).

- **`README.md` is the index**: every entry, newest first, one line each, as
  `- YYYY-MM-DD [kind] [title](file.md): one-line summary`. Kinds: `decision`, `problem`,
  `preference`, `lesson`. A superseded entry keeps its line, marked `superseded by [title](file.md)`.
- **One file per entry**, named `YYYY-MM-DD-<slug>.md`, holding one decision, problem, preference or
  lesson: the dated claim, who made or saw it, the commit or source it rests on, and the entries it
  relates to, linked.
- **Sources are cited, never copied in**: a report, a transcript, a pull request is linked by path,
  commit or URL.

## Ingest, query

- **Ingest**: when the run learns something durable, write the entry and update every entry it
  touches (a new link, a `superseded by` line), and the index, in the same commit.
- **Query**: before a decision or a brief, read the index and the entries it points at for the area.
  An answer worth keeping becomes an entry.

## The lint

Run at the close of a run, or when the index has grown since the last lint, by a fresh leaf child or
by the orchestrator. It reads the index and every file under the memory path, and reports each
finding with the files it names:

| Finding | What it is | Fixed by |
|---|---|---|
| **Contradiction** | Two entries that cannot both hold, neither marked superseded by the other | a new entry that says which holds, as of when, superseding the other |
| **Orphan** | A file under the memory path the index does not link, or an index line whose file is missing | an index line for the file, or a note on the line that the file was removed and when |
| **Overtaken** | A claim a newer entry, a commit or a source has overtaken, still unmarked | a `superseded by` line on the old entry and its index line |
| **Undated** | A claim with no date, or a code claim with no commit; a bare "currently" | a dated superseding entry; the undated one stays as written |

Findings are fixed by adding, never by rewriting what an entry said. A lint that finds nothing says
which files it read, so an empty result is a result.
