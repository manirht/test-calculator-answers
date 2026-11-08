import unittest
from fractions import Fraction as F

from calcstats.protocol import format_number


class OutputRounding(unittest.TestCase):
    def test_rounds_to_nearest_not_down(self):
        value = F(2, 3) + F(1, 10**30)
        self.assertEqual(F(format_number(value)), F(666666666667, 10**12))

    def test_negative_values_round_symmetrically(self):
        value = -(F(2, 3) + F(1, 10**30))
        self.assertEqual(F(format_number(value)), F(-666666666667, 10**12))


if __name__ == "__main__":
    unittest.main()
