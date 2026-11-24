import unittest

from tests.support.harness import shell_integers
from tests.support.models import bounded_stream, seeded_state, xorshift32


class XorshiftTests(unittest.TestCase):
    def test_matches_published_xorshift32_vector(self):
        values = shell_integers("RNG_STATE=2463534242; rng_next; echo $RNG_STATE")
        self.assertEqual(values, [723471715])

    def test_step_matches_reference_model(self):
        for state in (1, 2, 0x80000000, 0xFFFFFFFF, 0xDEADBEEF):
            with self.subTest(state=state):
                values = shell_integers('RNG_STATE=$1; rng_next; echo $RNG_STATE', str(state))
                self.assertEqual(values, [xorshift32(state)])

    def test_seed_matches_reference_model(self):
        for seed in (0, 1, 42, 2463534242, 4294967295):
            with self.subTest(seed=seed):
                values = shell_integers('rng_seed "$1"; echo $RNG_STATE', str(seed))
                self.assertEqual(values, [seeded_state(seed)])

    def test_state_is_never_zero_after_seeding(self):
        values = shell_integers('rng_seed 2463534242; echo $RNG_STATE')
        self.assertNotEqual(values[0], 0)

    def test_bounded_stream_matches_reference_model(self):
        script = 'rng_seed "$1"; for i in {1..200}; do rng_bounded "$2"; echo $RNG_VALUE; done'
        for seed, value_range in ((42, 10), (7, 1), (9, 1024), (1, 2147483648)):
            with self.subTest(seed=seed, value_range=value_range):
                values = shell_integers(script, str(seed), str(value_range))
                self.assertEqual(values, bounded_stream(seed, value_range, 200))
