# Migrating a pre-existing tracker

Used when the survey found a tracker already in the repository. Never create a parallel system silently. Present the migration as a **dry run** and get confirmation before writing.

1. **Show the mapping**: which existing items become `.tasks/` files, which completed items become `CHANGELOG.md` lines, and how groupings map to `ROADMAP.md` Features. Preserve wording, and note provenance ("Seeded YYYY-MM-DD from the former `TODO.md`").
2. **Archive the source before writing**: copy the original to `<name>.archived.md`, or leave a one-line pointer to the new location. Delete the source only once its content is confirmed migrated, and only on the person's explicit say-so.
3. **Offer the three outcomes**; one tracker per repository is the goal:
   - **Migrate** (usually best): port the contents in, then retire the old file.
   - **Adopt**: keep the existing file as canonical and point `AGENTS.md` at it by its real name instead of forcing `ROADMAP.md` or `CHANGELOG.md`.
   - **Coexist**: scaffold anyway and keep the old one, only when the person explicitly wants both. Warn that two trackers drift.

An **out-of-repository tracker** (GitHub Issues, GitLab, Linear, Jira, Notion) cannot be migrated. Ask whether the file-based system replaces or complements it; the configure step then records it as `tracker` in `docs/agents/zen.md`, which is where the skills read which tracker is authoritative.

Done when the person has chosen an outcome for every tracker found, and nothing was deleted without their say-so.
