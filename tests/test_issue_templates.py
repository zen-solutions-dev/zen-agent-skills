"""The issue templates ask for what a report cannot be reproduced without (feat-0103, E9).

A skill's behaviour depends on the kit version installed, the model that ran it and the
effort it ran at, and a report missing any of them starts with a round trip to ask. Read as
text, standard library only: each form template must carry an `id:` for each of the three.
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

TEMPLATES = Path(__file__).resolve().parent.parent / ".github" / "ISSUE_TEMPLATE"
REQUIRED_IDS = ("kit_version", "model", "effort")


def form_templates():
    return sorted(p for p in TEMPLATES.glob("*.yml") if p.name != "config.yml")


class IssueTemplateTests(unittest.TestCase):
    def test_there_are_form_templates_to_check(self):
        self.assertTrue(form_templates(), f"no issue form templates under {TEMPLATES}")

    def test_every_form_asks_for_kit_version_model_and_effort(self):
        for path in form_templates():
            ids = set(re.findall(r"^\s+id:\s*(\S+)\s*$", path.read_text(encoding="utf-8"),
                                 re.MULTILINE))
            for wanted in REQUIRED_IDS:
                with self.subTest(template=path.name, field=wanted):
                    self.assertIn(wanted, ids)


if __name__ == "__main__":
    unittest.main()
