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
