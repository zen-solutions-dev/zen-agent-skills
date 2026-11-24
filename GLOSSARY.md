# Glossary

The shared language of Zen Agent Skills: one word per concept, written down when it is settled so the next session starts from it. Definitions only; decisions live in the task files and decision records, and how the code implements a term lives in the code. Kept with the [`domain-language`](.agents/skills/domain-language/SKILL.md) skill.

## Evaluation

The paired evaluation of skills against their absence (`feat-0051`).

**Case**:
One prompt plus its graders, run against a fixture.
_Avoid_: scenario (a behaviour in a spec), test (a unit test under `tests/`)

**Arm**:
One configuration every case runs under. There are two: the with-kit arm and the baseline.
_Avoid_: condition, variant

**Baseline**:
The arm with Claude Code as shipped, built-ins included, and none of the kit. A skill has earned its place only when it beats the baseline, not when it beats having nothing at all.
_Avoid_: control, no-skill, without-skill

**Grader**:
One check that scores a single run of a case.
_Avoid_: assertion

**Discriminating**:
Said of a grader whose result differs between the with-kit arm and the baseline. A case discriminates when at least one of its graders does; a grader that gives the same result in both arms has measured nothing.
_Avoid_: useful, effective

## Work and delegation

How work is split, who runs it, and how much a person is involved (the Marjana overhaul, 2026-11-24).

**Orchestrator**:
The one session that holds the conversation with the person, plans the work, dispatches child sessions, and lands their results on an integration branch. It decides and integrates; it does not build.
_Avoid_: coordinator, manager, lead agent

**Child session**:
A session an orchestrator starts with a fresh context and a written brief, which works on its own branch and reports back once.
_Avoid_: subagent (a leaf dispatched inside one session), worker, fork

**Integration branch**:
The branch every child session's work lands on before it reaches the person as one pull request. Only an orchestrator merges into it, and only work it did not author and someone else verified.
_Avoid_: staging branch, release branch

**Frontier**:
Every open decision, or every task, whose prerequisites are all settled: what can be asked or started now without guessing.
_Avoid_: next steps, backlog

**AFK**:
Said of work run with nobody watching, from the brief to a reviewable result. Suits work that is well specified, low risk and easy to verify. A task declares it as `mode: afk`.
_Avoid_: autonomous, unattended, background

**Human in the loop**:
Said of work a person stays present for while it runs, because it holds a one-way door, a wide blast radius, or a change hard to review. A task declares it as `mode: hitl`.
_Avoid_: supervised, interactive, HITL in prose

**One-way door**:
A decision that is expensive or impossible to reverse once others depend on it, such as a file format adopters configure against. It gets a spec and a person's approval before it is built.
_Avoid_: irreversible change, breaking change

**Two-way door**:
A decision one revert undoes. An agent may take it and report it.
_Avoid_: reversible change, low-risk change

## Setup

How the kit learns what a repository holds (`feat-0091`, [`zen-config`](docs/spec/zen-config.md)).

**Fact**:
Something a skill needs to know about the repository it runs in: the tracker, the glossary, the acceptance command, where work lands. Recorded as a key in `docs/agents/zen.md`, or discovered when the key is absent.
_Avoid_: setting, option, preference (the file records what is, not how a skill should behave)

**Role**:
A state a tracker item can be in that the skills act on (ready for an agent, ready for a person, needs information, blocked, out of scope), mapped to the tracker's own label.
_Avoid_: status (a task file's lifecycle field), label (the tracker's word for one role)
