import unittest
from fractions import Fraction as F

from calcstats import finance
from calcstats.protocol import handle_request


class PvZeroRate(unittest.TestCase):
    def test_pv_sums_the_payments(self):
        self.assertEqual(finance.pv(F(0), F(12), F(100)), 1200)

    def test_through_the_protocol(self):
        reply = handle_request({"id": 1, "fn": "pv", "args": ["0", "12", "100"]})
        self.assertEqual(reply, {"id": 1, "ok": True, "value": "1200"})


if __name__ == "__main__":
    unittest.main()
