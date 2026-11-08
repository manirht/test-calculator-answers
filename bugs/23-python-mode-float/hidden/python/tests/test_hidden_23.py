import unittest
from fractions import Fraction as F

from calcstats import stats
from calcstats.protocol import handle_request


class ModeIsExact(unittest.TestCase):
    def test_returns_the_fraction_itself(self):
        self.assertEqual(stats.mode(F(1, 3), F(1, 3), F(1, 2)), F(1, 3))

    def test_through_the_protocol(self):
        reply = handle_request({"id": 1, "fn": "mode", "args": ["1/3", "1/3", "1/2"]})
        self.assertEqual(reply["value"], "1/3")

    def test_ints_still_work(self):
        self.assertEqual(stats.mode(F(3), F(3), F(1), F(1), F(2)), 1)


if __name__ == "__main__":
    unittest.main()
