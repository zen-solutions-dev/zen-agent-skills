# Re-point a verifier when a child's head moves

**Lesson, 2026-11-25**, reported by the round 2 orchestrator: a Wave 1 child applied a relayed
correction after it had reported, so its branch head moved while the verifier ran on the reported
sha. A verdict on the old sha lands only the old sha. Two rules came of it: the verifier is told the
new sha and re-runs there, and a child pushes nothing after reporting unless asked.

Folded into `orchestrate` Step 2 and Step 5 item 4 by `feat-0107`. Related:
[Fix shared terms verbatim in every brief](2026-11-25-shared-terms-verbatim.md), another brief rule
from the same wave.
