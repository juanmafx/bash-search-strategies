import unittest

from tests.support.harness import run_shell

CHECK = 'if parse_bounded_integer "$1" "$2" "$3"; then echo "$PARSED_INTEGER"; else echo rejected; fi'


def parse(raw, minimum="0", maximum="9999999999"):
    return run_shell(CHECK, raw, minimum, maximum).stdout.strip()


class ParseBoundedIntegerTests(unittest.TestCase):
    def test_accepts_plain_decimal(self):
        self.assertEqual(parse("42"), "42")

    def test_leading_zeros_are_decimal_not_octal(self):
        self.assertEqual(parse("010"), "10")
        self.assertEqual(parse("09"), "9")

    def test_accepts_inclusive_bounds(self):
        self.assertEqual(parse("5", "5", "7"), "5")
        self.assertEqual(parse("7", "5", "7"), "7")

    def test_rejects_out_of_range(self):
        self.assertEqual(parse("4", "5", "7"), "rejected")
        self.assertEqual(parse("8", "5", "7"), "rejected")

    def test_rejects_non_decimal_forms(self):
        for raw in ("", " ", "-1", "+1", "1.5", "0x10", "1e3", "abc", "1 2", "1\n", "\n1", "٣"):
            with self.subTest(raw=raw):
                self.assertEqual(parse(raw), "rejected")

    def test_rejects_more_than_ten_digits(self):
        self.assertEqual(parse("12345678901"), "rejected")
