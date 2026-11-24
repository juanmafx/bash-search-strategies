import tempfile
import unittest
from pathlib import Path

from tests.support.harness import run_cli
from tests.support.models import bounded_stream


class PlayDirectoryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        for name in ("a", "b", "c"):
            (self.directory / name).touch()

    def test_correct_guess_wins(self):
        result = run_cli(stdin="3\n", cwd=self.directory)
        self.assertEqual(result.returncode, 0)
        self.assertIn("Congratulations", result.stdout)
        self.assertIn("Solved in 1 attempt(s).", result.stdout)

    def test_hints_then_win(self):
        result = run_cli("play", "--dir", str(self.directory), stdin="1\n9\n3\n")
        self.assertEqual(result.returncode, 0)
        self.assertLess(result.stdout.index("too low"), result.stdout.index("too high"))
        self.assertIn("Solved in 3 attempt(s).", result.stdout)

    def test_empty_input_does_not_win(self):
        result = run_cli(stdin="", cwd=self.directory)
        self.assertEqual(result.returncode, 4)
        self.assertNotIn("Congratulations", result.stdout)

    def test_end_of_input_terminates(self):
        result = run_cli(stdin="1\n", cwd=self.directory, timeout=5)
        self.assertEqual(result.returncode, 4)

    def test_final_line_without_newline_is_read(self):
        result = run_cli(stdin="3", cwd=self.directory)
        self.assertEqual(result.returncode, 0)

    def test_crlf_input_is_accepted(self):
        result = run_cli(stdin="3\r\n", cwd=self.directory)
        self.assertEqual(result.returncode, 0)

    def test_invalid_guess_is_not_counted(self):
        result = run_cli(stdin="abc\n3\n", cwd=self.directory)
        self.assertEqual(result.returncode, 0)
        self.assertIn("Invalid guess", result.stderr)
        self.assertIn("Solved in 1 attempt(s).", result.stdout)

    def test_max_attempts_stops_game(self):
        result = run_cli("--max-attempts", "2", stdin="1\n1\n3\n", cwd=self.directory)
        self.assertEqual(result.returncode, 3)
        self.assertNotIn("Congratulations", result.stdout)


class PlayRandomTests(unittest.TestCase):
    def test_seeded_target_is_reproducible(self):
        target = bounded_stream(42, 101, 1)[0]
        result = run_cli("--seed", "42", "--max", "100", stdin=f"{target}\n")
        self.assertEqual(result.returncode, 0)
        self.assertIn("Solved in 1 attempt(s).", result.stdout)

    def test_unseeded_random_target_is_in_range(self):
        result = run_cli("--random", "--max", "0", stdin="0\n")
        self.assertEqual(result.returncode, 0)


class UsageTests(unittest.TestCase):
    def test_help(self):
        result = run_cli("--help")
        self.assertEqual(result.returncode, 0)
        self.assertIn("Usage:", result.stdout)

    def test_version_matches_file(self):
        result = run_cli("--version")
        version = (Path(__file__).resolve().parents[2] / "VERSION").read_text().strip()
        self.assertEqual(result.stdout.strip(), f"guessinggame {version}")

    def test_rejected_arguments_exit_with_usage_code(self):
        cases = (
            ("--unknown",),
            ("--seed",),
            ("--seed", "abc"),
            ("--seed", "4294967296"),
            ("--max", "2147483648"),
            ("--max-attempts", "0"),
            ("--dir", "/nonexistent-path"),
            ("--dir", ""),
            ("--dir", "", "--random"),
            ("--dir", ".", "--random"),
            ("simulate", "--strategy", "unknown"),
            ("simulate", "--trials", "0"),
            ("simulate", "--unknown"),
        )
        for arguments in cases:
            with self.subTest(arguments=arguments):
                self.assertEqual(run_cli(*arguments).returncode, 2)
