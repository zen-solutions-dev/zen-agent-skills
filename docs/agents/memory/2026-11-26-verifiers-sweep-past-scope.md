# Ask verifiers to sweep for the same claim past the quest's scope

**Lesson, 2026-11-26**, from rollout round 3. A docs quest in the Zen product app removed a past date from its public road-ahead page and passed. Its verifier had been told to grep the whole public page for the same claim and to classify each hit; it found the live landing page still promising that date in about twelve places, which the quest had scoped out. That finding became its own quest, with words the maintainer approved line by line before the freeze. A verifier briefed only on the quest's own files would have passed it and left the larger defect live.

So: in a verifier brief for a fix of a false claim, name the claim and ask for every place it still appears, in or out of scope, as findings.
