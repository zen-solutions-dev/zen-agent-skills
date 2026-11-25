"""`install.py --with-hooks` prints an opt-in gate as a block of its own (feat-0103, F6).

A gate blocks work, so opting into it is its own step: the reminders' registration block
never carries a gate, and the gate's block is printed after it, labelled as a gate. In a
file of its own so it merges apart from additions to tests/test_install.py (R-203).
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import shutil
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("install_gate_block",
                                               REPO_ROOT / "scripts" / "install.py")
inst = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(inst)


def commands(block):
    return [h["command"] for entries in json.loads(block)["hooks"].values()
            for e in entries for h in e["hooks"]]


class GateBlockTests(unittest.TestCase):
    def test_the_reminders_block_carries_no_gate(self):
        reminders = " ".join(commands(inst.claude_registration(Path("/tmp/home"))))
        for gate in inst.OPT_IN_GATES:
            self.assertNotIn(gate, reminders)
        self.assertIn("skill-reachability-reminder.py", reminders)

    def test_the_gates_block_carries_only_the_gates_under_pre_tool_use(self):
        block = json.loads(inst.claude_registration(Path("/tmp/home"), gates=True))
        self.assertEqual(list(block["hooks"]), ["PreToolUse"])
        self.assertEqual(
            sorted(Path(c.split('"')[1]).name for c in
                   commands(inst.claude_registration(Path("/tmp/home"), gates=True))),
            sorted(inst.OPT_IN_GATES))

    def test_the_printed_output_labels_the_gate_and_prints_it_after_the_reminders(self):
        home = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, home, ignore_errors=True)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = inst.main(["--with-hooks", "--tools", "claude", "--home", str(home),
                              "--dry-run"])
        out = buf.getvalue()
        self.assertEqual(code, 0, out)
        reminders_at = out.index("INACTIVE for claude")
        gate_at = out.index("Separately, an opt-in GATE was placed")
        self.assertLess(reminders_at, gate_at)
        self.assertNotIn("destructive-git-gate.py", out[reminders_at:gate_at])
        self.assertIn("destructive-git-gate.py", out[gate_at:])


if __name__ == "__main__":
    unittest.main()
