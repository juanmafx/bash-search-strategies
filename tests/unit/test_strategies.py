import unittest

from tests.support.harness import shell_integers


class StrategyExampleTests(unittest.TestCase):
    def test_linear_counts_every_probe(self):
        self.assertEqual(shell_integers("solve_linear 9; echo $SOLVER_ATTEMPTS"), [10])

    def test_bisection_finds_midpoint_in_one_probe(self):
        self.assertEqual(shell_integers("solve_bisection 3 0 6; echo $SOLVER_ATTEMPTS"), [1])

    def test_bisection_single_value_range(self):
        self.assertEqual(shell_integers("solve_bisection 0 0 0; echo $SOLVER_ATTEMPTS"), [1])

    def test_galloping_zero_takes_one_probe(self):
        self.assertEqual(shell_integers("solve_galloping 0; echo $SOLVER_ATTEMPTS"), [1])

    def test_galloping_hits_power_boundary(self):
        self.assertEqual(shell_integers("solve_galloping 7; echo $SOLVER_ATTEMPTS"), [4])

    def test_bit_length(self):
        script = "for v in 0 1 2 3 4 1023 1024 2147483648; do bit_length $v; done"
        self.assertEqual(shell_integers(script), [0, 1, 2, 2, 3, 10, 11, 32])
