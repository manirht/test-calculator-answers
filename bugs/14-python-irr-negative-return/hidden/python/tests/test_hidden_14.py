import unittest
from fractions import Fraction as F

from calcstats import finance


class IrrNegative(unittest.TestCase):
    def test_losing_investment(self):
        rate = finance.irr(F(-100), F(50))
        self.assertAlmostEqual(float(rate), -0.5, places=9)

    def test_positive_still_works(self):
        self.assertAlmostEqual(float(finance.irr(F(-100), F(110))), 0.1, places=9)


if __name__ == "__main__":
    unittest.main()
