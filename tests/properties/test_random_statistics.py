import unittest

from tests.support.harness import shell_integers
from tests.support.models import chi_square

CHI_SQUARE_CRITICAL_DF9_ALPHA_001 = 27.877
CHI_SQUARE_CRITICAL_DF15_ALPHA_001 = 37.697
SAMPLE_SIZE = 20000
DRAW_SCRIPT = 'rng_seed "$1"; for ((i = 0; i < $3; i++)); do rng_bounded "$2"; echo $RNG_VALUE; done'


def draw(seed, value_range, count=SAMPLE_SIZE):
    return shell_integers(DRAW_SCRIPT, str(seed), str(value_range), str(count))


class GeneratorStatistics(unittest.TestCase):
    def test_uniformity_chi_square(self):
        for seed in (1, 42, 12345):
            with self.subTest(seed=seed):
                values = draw(seed, 10)
                observed = [values.count(bucket) for bucket in range(10)]
                statistic = chi_square(observed, SAMPLE_SIZE / 10)
                self.assertLess(statistic, CHI_SQUARE_CRITICAL_DF9_ALPHA_001)

    def test_serial_pairs_chi_square(self):
        values = draw(42, 4)
        pairs = [0] * 16
        for index in range(0, len(values) - 1, 2):
            pairs[values[index] * 4 + values[index + 1]] += 1
        statistic = chi_square(pairs, (SAMPLE_SIZE // 2) / 16)
        self.assertLess(statistic, CHI_SQUARE_CRITICAL_DF15_ALPHA_001)

    def test_values_stay_in_range(self):
        values = draw(7, 13, 5000)
        self.assertGreaterEqual(min(values), 0)
        self.assertLessEqual(max(values), 12)

    def test_first_draw_across_adjacent_seeds_is_uniform(self):
        script = 'for ((s = 0; s < $1; s++)); do rng_seed "$s"; rng_bounded 10; echo $RNG_VALUE; done'
        values = shell_integers(script, "5000")
        observed = [values.count(bucket) for bucket in range(10)]
        self.assertLess(chi_square(observed, 500), CHI_SQUARE_CRITICAL_DF9_ALPHA_001)
