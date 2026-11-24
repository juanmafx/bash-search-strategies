import tempfile
import unittest
from pathlib import Path

from tests.support.harness import PROJECT_ROOT, run_cli


class InputSafetyTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.sentinel = self.directory / "sentinel"

    def payloads(self):
        path = self.sentinel
        return (
            f"a[$(touch {path})]",
            f"$(touch {path})",
            f"`touch {path}`",
            f"0; touch {path}",
            f"x[`touch {path}`]",
        )

    def test_guess_is_never_evaluated(self):
        for payload in self.payloads():
            with self.subTest(payload=payload):
                result = run_cli("--dir", str(self.directory), stdin=f"{payload}\n0\n", timeout=5)
                self.assertEqual(result.returncode, 0)
                self.assertFalse(self.sentinel.exists())

    def test_option_values_are_never_evaluated(self):
        for option in ("--seed", "--max", "--max-attempts"):
            for payload in self.payloads():
                with self.subTest(option=option, payload=payload):
                    self.assertEqual(run_cli(option, payload).returncode, 2)
                    self.assertFalse(self.sentinel.exists())

    def test_simulate_options_are_never_evaluated(self):
        for option in ("--seed", "--max", "--trials", "--strategy"):
            for payload in self.payloads():
                with self.subTest(option=option, payload=payload):
                    self.assertEqual(run_cli("simulate", option, payload).returncode, 2)
                    self.assertFalse(self.sentinel.exists())

    def test_invalid_input_is_not_echoed(self):
        result = run_cli("--dir", str(self.directory), stdin="\x1b[2Jmarker\n0\n", timeout=5)
        self.assertNotIn("marker", result.stdout + result.stderr)

    def test_hostile_directory_name_is_treated_as_data(self):
        hostile = self.directory / "$(touch sentinel)"
        hostile.mkdir()
        (hostile / "entry").touch()
        result = run_cli("--dir", str(hostile), stdin="1\n", cwd=self.directory, timeout=5)
        self.assertEqual(result.returncode, 0)
        self.assertFalse(self.sentinel.exists())

    def test_inherited_glob_settings_cannot_change_the_target(self):
        (self.directory / ".hidden").touch()
        (self.directory / "visible").touch()
        hostile = {"BASHOPTS": "dotglob:failglob", "GLOBIGNORE": "visible"}
        result = run_cli("--dir", str(self.directory), stdin="1\n", timeout=5, extra_environment=hostile)
        self.assertEqual(result.returncode, 0)
        self.assertIn("Solved in 1 attempt(s).", result.stdout)

    def test_source_has_no_dynamic_evaluation(self):
        forbidden = ("eval ", "source <(", "bash -c", "sh -c")
        files = [PROJECT_ROOT / "guessinggame.sh", *sorted((PROJECT_ROOT / "src").rglob("*.sh"))]
        for path in files:
            text = path.read_text(encoding="utf-8")
            for token in forbidden:
                with self.subTest(path=path.name, token=token):
                    self.assertNotIn(token, text)
