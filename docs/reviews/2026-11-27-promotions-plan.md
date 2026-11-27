# Draft promotions, 2026-11-27: plan

Written 2026-11-27 by the orchestrating session of rollout round 3, after a promotion review of the twelve drafts against the contribution bar in `AGENTS.md` section 7. Integration branch `zen/promote-r4-2026-11-27`, cut from `zen/rollout-r3-2026-11-25` at `bad1f56` (pull request #121, not yet merged into `developer`), because both change the generated marketplace. The final pull request goes into `developer`.

## The review

| Draft | Real use on record | Verdict |
|---|---|---|
| `sitrep` | This kit and the Zen product app (a private repository), with no setup; its findings fixed (`chore-0122`) or filed (`feat-0111`, `feat-0073`) | Promote |
| `vet-skill` | One real vetting of an outside skill, iterated at `cad9c99` | Promote |
| `research` | Round 1's research questions and round 2's citations | Promote, with `orchestrate`, which links it |
| `orchestrate` | Rounds 1 to 3, including the owed second project | Promote, with round 3's lessons folded in |
| `systematic-debugging` | Two real defects | Not this round: `feat-0063` still owes its diagnosis record |
| `agent-observatory` | Ingest and query; session actions never ran | Extended 60 days |
| `quest-tracker` | Script steps; never published a tracker page | Extended 60 days |
| `wait-what`, `prototype`, `wayfinder`, `teach`, `triage` | One run, partial, simulated, or none | Kept as drafts |

## The maintainer's answers, 2026-11-27

| Id | Question | Answer |
|---|---|---|
| P-1 | Which drafts are promoted | `sitrep`, `vet-skill`, `orchestrate` with `research` |
| P-2 | The two partially used drafts | Extend both by 60 days |

## Children

| Quest | Wave | Owned paths | Door |
|---|---|---|---|
| [`feat-0112`](../../.quests/done/feat-0112-refine-sitrep-from-its-real-use-before-promotion.md) | 1 (first, alone) | `sitrep/SKILL.md` | Two-way |
| [`feat-0113`](../../.quests/done/feat-0113-confirm-vet-skill-s-first-use-fixes-landed-before-promotion.md) | 1 | `vet-skill/SKILL.md` | Two-way |
| [`feat-0114`](../../.quests/done/feat-0114-refine-research-from-its-real-use-before-promotion.md) | 1 | `research/SKILL.md` | Two-way |
| [`feat-0115`](../../.quests/done/feat-0115-fold-round-3-s-lessons-into-orchestrate-before-promotion.md) | 1 | `orchestrate/` | Two-way |
| [`feat-0116`](../../.quests/done/feat-0116-promote-sitrep-vet-skill-research-and-orchestrate-and-extend-two-draft.md) | 2 | the six skills' frontmatter and draft notices, `zen`, `docs/CATALOG.md`, profile tables, `scripts/install.py`, `.claude-plugin/` | Two-way: a promotion reverts with one commit |

Wave 1 children keep `status: draft`, so none of them touches the marketplace or the listings; `feat-0116` alone does. The orchestrator owns `CHANGELOG.md`, `ROADMAP.md` and this plan.
