import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from tests.support.harness import PROJECT_ROOT


class MakefileTests(unittest.TestCase):
    def test_set_file_writes_build_output_and_preserves_readme(self):
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            shutil.copy(PROJECT_ROOT / "makefile", workspace / "makefile")
            shutil.copy(PROJECT_ROOT / "guessinggame.sh", workspace / "guessinggame.sh")
            readme = workspace / "README.md"
            readme.write_text("sentinel\n", encoding="utf-8")
            subprocess.run(["make", "set_file"], cwd=workspace, check=True, capture_output=True)
            self.assertEqual(readme.read_text(encoding="utf-8"), "sentinel\n")
            output = (workspace / "build" / "project-info.md").read_text(encoding="utf-8")
            line_count = len((workspace / "guessinggame.sh").read_text(encoding="utf-8").splitlines())
            self.assertIn(f"Lines in guessinggame.sh: {line_count}", output)
