import math
import random
import unittest

from tests.support.harness import shell_integers
from tests.support.models import bisection_attempts, galloping_attempts

PROPERTY_SEED = 20260101
EXHAUSTIVE_LIMIT = 256


def bisection_for_all(upper_bound):
    script = (
        'for ((t = 0; t <= $1; t++)); do solve_bisection "$t" 0 "$1"; echo $SOLVER_ATTEMPTS; done'
    )
    return shell_integers(script, str(upper_bound))


class BisectionProperties(unittest.TestCase):
    def test_worst_case_is_exactly_bit_length(self):
        for size in (1, 2, 3, 4, 7, 8, 9, 63, 64, 65, EXHAUSTIVE_LIMIT):
            with self.subTest(size=size):
                attempts = bisection_for_all(size - 1)
                self.assertEqual(max(attempts), size.bit_length())

    def test_no_comparison_strategy_beats_information_bound(self):
        for size in (2, 5, 16, 100, EXHAUSTIVE_LIMIT):
            with self.subTest(size=size):
                self.assertGreaterEqual(max(bisection_for_all(size - 1)), math.ceil(math.log2(size + 1)))

    def test_mean_matches_balanced_tree_for_complete_sizes(self):
        for height in range(1, 9):
            size = 2**height - 1
            with self.subTest(size=size):
                attempts = bisection_for_all(size - 1)
                expected_total = sum(level * 2 ** (level - 1) for level in range(1, height + 1))
                self.assertEqual(sum(attempts), expected_total)

    def test_shell_matches_model_on_random_ranges(self):
        generator = random.Random(PROPERTY_SEED)
        for _ in range(200):
            high = generator.randrange(0, 2**31)
            target = generator.randint(0, high)
            values = shell_integers(
                'solve_bisection "$1" 0 "$2"; echo $SOLVER_ATTEMPTS', str(target), str(high)
            )
            self.assertEqual(values, [bisection_attempts(target, 0, high)])
            self.assertLessEqual(values[0], (high + 1).bit_length())


class GallopingProperties(unittest.TestCase):
    def test_exhaustive_bound_and_model_agreement(self):
        script = 'for ((t = 0; t < $1; t++)); do solve_galloping "$t"; echo $SOLVER_ATTEMPTS; done'
        attempts = shell_integers(script, str(EXHAUSTIVE_LIMIT))
        for target, observed in enumerate(attempts):
            with self.subTest(target=target):
                self.assertEqual(observed, galloping_attempts(target))
                self.assertLessEqual(observed, max(1, 2 * (target).bit_length()))

    def test_bound_holds_for_large_random_targets(self):
        generator = random.Random(PROPERTY_SEED)
        for _ in range(200):
            target = generator.randrange(0, 2**31)
            values = shell_integers('solve_galloping "$1"; echo $SOLVER_ATTEMPTS', str(target))
            self.assertEqual(values, [galloping_attempts(target)])
            self.assertLessEqual(values[0], max(1, 2 * target.bit_length()))


class ParserProperties(unittest.TestCase):
    def test_round_trip_for_random_integers(self):
        generator = random.Random(PROPERTY_SEED)
        script = 'parse_bounded_integer "$1" 0 9999999999; echo "$PARSED_INTEGER"'
        for _ in range(200):
            value = generator.randrange(0, 10**10)
            padded = str(value).zfill(generator.randint(len(str(value)), 10))
            self.assertEqual(shell_integers(script, padded), [value])
