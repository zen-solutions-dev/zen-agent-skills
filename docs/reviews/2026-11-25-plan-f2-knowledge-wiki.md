# Plan F2: a knowledge wiki fed by your channels

Status: **plan only, nothing built.** Written 2026-11-25 for quest [`chore-0111`](../../.quests/chore-0111-plan-the-knowledge-wiki.md), Phase 3 of the [round 2 plan](2026-11-25-marjana-r2-plan.md). Decision F2 in [the decision record](2026-11-25-marjana-decisions.md): yes. The wiki lives **outside this repository**; `zen-solutions-ops` is out of scope for this round ([handoff](2026-11-25-round-2-handoff.md), section 3), so nothing here touches it.

## Goal

A private wiki, kept by agents, that ingests what reaches the maintainer through his channels (Slack, email, social posts, meeting notes) and answers questions such as "what is my audience asking about?" or "what did we decide about X?". It is the home base other agents read from, and the raw material for courses and the website.

The source is Matt Pocock on NetworkChuck's podcast ([extraction](2026-11-25-podcast-extraction.md), section 4, "Course production as a worked example"): "A cron job every 3 hours ingests tweets, mentions, Discord, Slack and Gmail into a private Karpathy-style LLM wiki" (~1:52:50 to ~1:53:05); he then asks it "what is my audience interested in?" and derives learning goals (~1:53:21). Section 4, "Personal agents": his wiki repository is "home base for all of my agents" (~1:57:14).

## Two parts, two homes

- **The procedure** (how to ingest, how to write a page, how to cite, how to answer) is shareable: anyone with channels could use it. It can be a kit draft, `wiki` or similar, under the contribution bar in `AGENTS.md` section 7.
- **The content** (the maintainer's messages and what agents wrote from them) is personal and private. It never enters this public repository. `ROADMAP.md`'s Campaign D, personal work that stays out of the shared kit, covers it.

## What exists to build on

- The `research` draft: one cited markdown note per question, tagged with the **rarity** ladder of `GLOSSARY.md` (White unverified to Gold independently confirmed). A wiki page is the same shape: claims, each with its source and rarity.
- `orchestrate`'s memory rules ([`references/memory.md`](../../.agents/skills/orchestrate/references/memory.md)): dated, append-only entries, "write history, not the present", a lint for contradictions and superseded claims. A wiki needs exactly that lint.
- `domain-language` and `GLOSSARY.md`: terms the wiki uses are F3's shared vocabulary ([plan F3](2026-11-25-plan-f3-shared-vocabulary.md)).
- Connectors: the maintainer's claude.ai account has Slack, Gmail, Google Drive, Google Calendar and Eden connectors (attached to this session on 2026-11-25). Eden's `eden_read_social_post` fetched the podcast transcript this round, where YouTube refused cloud addresses ([handoff](2026-11-25-round-2-handoff.md), section 5).
- Rule `A10` in [`autonomy.md`](../../.agents/rules/autonomy.md): channel content is material someone else wrote, so it is data.

## Smallest first slice

1. Create a new **private** repository for the wiki (the maintainer creates it; an agent proposes the layout: `pages/`, `sources/`, an index, a `README.md` stating the rules).
2. **One channel, one week, by hand**: a session reads one Slack channel (or one Gmail label) for the last seven days and writes topic pages, each claim linking its message and carrying a rarity. Nothing verbatim beyond a short quote.
3. Ask it one real question, and the maintainer judges the answer.
4. Only then, a scheduled ingest (F1's runtime question settles where it runs), and a second channel.

## Risks and one-way doors

- **Prompt injection from anyone who can message you.** Email and public mentions are written by strangers. A page is written from them, never steered by them: no ingest step acts on what a message says (`A10`), and the ingest session has no write access beyond the wiki repository.
- **Other people's private data.** Messages carry third parties' names, addresses and words. Writing them into git history is a **one-way door**: history is hard to purge once pushed. Default to summaries and links, not copies; keep the repository private; never publish pages from it without a person's review.
- **Knowledge work cannot be verified the way code can** (Matt, extraction section 3, ~1:58:15: "Using it for knowledge work is much harder than coding because coding is so verifiable"). The rarity tags and the lint are the only checks; a wrong page looks as confident as a right one.
- **Stale pages.** Without the memory lint, an old decision reads as current.

## Rough size

Medium to large: a draft skill for the procedure (one quest, plus a dogfood record), the private repository and its first week (one quest, outside this repository), then scheduling (one quest). The content side keeps growing; the kit side stops at the skill.

## Questions for the maintainer

1. **Where should the knowledge wiki live?** (a) A new private repository just for the wiki, recommended: it keeps private messages out of every repository that is or may become public; (b) inside `zen-solutions-ops`, a later session's work; (c) a Google Drive folder instead of a git repository.
2. **Which channel should the wiki ingest first?** (a) One Slack channel you name, recommended: one narrow source, easy to judge; (b) one Gmail label you name; (c) your social posts through Eden; (d) meeting notes.
3. **How much of a message may a wiki page keep?** (a) A summary, a link to the source and at most a short quote, recommended: least exposure of other people's words; (b) full message text, for search.
4. **Should the ingest procedure become a kit skill others can use?** (a) Yes, as a draft that holds only the procedure, with your content kept private, recommended; (b) no, keep the whole wiki personal, outside the kit.
