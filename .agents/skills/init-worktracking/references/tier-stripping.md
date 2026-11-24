# Tier stripping at lite

At **lite** there is no `ROADMAP.md` and no `CHANGELOG.md`, so strike every reference to them out of what you write. A scaffold whose own files link to things that do not exist teaches an agent that broken references are normal here. Three files carry those references:

- **`AGENTS.md`**: the `ROADMAP.md` and `CHANGELOG.md` links in the work-tracking section, the clause in the reading protocol that names them, and lifecycle step 3. The lifecycle still describes the model; it stops pointing at absent files.
- **`.tasks/README.md`**: the strategy and ledger sentence in the opening paragraph, and the `CHANGELOG.md` and `ROADMAP.md` clauses in its lifecycle section.
- **`.tasks/_TEMPLATE.md`**, which every task the repository ever writes is copied from, so two edits:
  1. The definition-of-done checkbox that requires a dated `CHANGELOG.md` line. Drop that clause, or the template propagates an unsatisfiable step into every task file.
  2. The `parent` comment and its seed value. Strike the `ROADMAP#N feature-slug` form from the comment, keep the free-text form, and seed a plain example of it (`parent: "one line naming the goal this serves"`). `parent` stays required at lite: what it names changes, not whether it is answered.

`validate.py` still ships at lite, unchanged: it is one stdlib file, and `new-task`, `reconcile-worktrees` and `doc-sync` tell agents to run it unconditionally.
