"""The kit's version has one source, the top-level VERSION file (feat-0103).

The maintainer decided on 2026-11-25 to commit VERSION at 0.2.0 and to have the plugin's
version read it, so `scripts/release.py` bumps one file and the marketplace follows.
"""
from __future__ import annotations

import importlib.util
import re
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("build_adapters_version",
                                               REPO_ROOT / "scripts" / "build-adapters.py")
ba = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ba)


class KitVersionTests(unittest.TestCase):
    def test_the_plugin_base_version_is_the_version_file(self):
        on_disk = (REPO_ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertRegex(on_disk, r"^\d+\.\d+\.\d+$")
        self.assertEqual(ba.PLUGIN_BASE_VERSION, on_disk)

    def test_the_generated_plugin_version_starts_with_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertTrue(ba.plugin_version(Path(tmp)).startswith(
                ba.PLUGIN_BASE_VERSION + "+"))

    def test_a_malformed_or_missing_version_file_stops_the_tool(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "VERSION"
            for text in ("", "v1.2.3\n", "1.2\n", "01.2.3\n"):
                with self.subTest(text=text):
                    bad.write_text(text, encoding="utf-8")
                    with self.assertRaises(SystemExit) as caught:
                        ba.kit_version(bad)
                    self.assertIn("not a MAJOR.MINOR.PATCH version", str(caught.exception))
            with self.assertRaises(SystemExit) as caught:
                ba.kit_version(Path(tmp) / "absent")
            self.assertIn("Cannot read the kit version", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
