import unittest

from tests.support.harness import parse_csv_rows, run_cli
from tests.support.models import bisection_attempts, bounded_stream, galloping_attempts


class SimulateTests(unittest.TestCase):
    def test_same_seed_is_byte_identical(self):
        arguments = ("simulate", "--seed", "7", "--max", "255", "--trials", "50")
        self.assertEqual(run_cli(*arguments).stdout, run_cli(*arguments).stdout)

    def test_different_seeds_differ(self):
        first = run_cli("simulate", "--seed", "1", "--trials", "50").stdout
        second = run_cli("simulate", "--seed", "2", "--trials", "50").stdout
        self.assertNotEqual(first, second)

    def test_rows_match_reference_models(self):
        models = {
            "linear": lambda target: target + 1,
            "bisection": lambda target: bisection_attempts(target, 0, 1023),
            "galloping": galloping_attempts,
        }
        targets = bounded_stream(42, 1024, 100)
        for strategy, model in models.items():
            with self.subTest(strategy=strategy):
                result = run_cli("simulate", "--strategy", strategy, "--seed", "42", "--max", "1023")
                self.assertEqual(result.returncode, 0)
                rows = parse_csv_rows(result.stdout)
                self.assertEqual([int(row["target"]) for row in rows], targets)
                self.assertEqual([int(row["attempts"]) for row in rows], [model(t) for t in targets])

    def test_summary_is_on_stderr_only(self):
        result = run_cli("simulate", "--trials", "5")
        self.assertIn("summary: trials=5", result.stderr)
        self.assertNotIn("summary", result.stdout)

    def test_maximum_bound_is_supported(self):
        result = run_cli("simulate", "--max", "2147483647", "--trials", "5")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(len(parse_csv_rows(result.stdout)), 5)
