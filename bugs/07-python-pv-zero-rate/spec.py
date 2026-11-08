BUG = dict(
    id="07", slug="python-pv-zero-rate", title="pv() at a 0% rate returns a single payment",
    lang="python", tier="L1", category="finance", kind="fix",
    commit_message="refactor: simplify the zero-rate branch in pv",
    issue=r'''
```
$ calc eval "pv(0, 12, 100)"
100
```

Twelve payments of 100 with no interest are worth 1200 today, not 100. With any non-zero rate the result is right
(`pv(1/100, 12, 100)` is fine) and `pmt` and `fv` handle a zero rate correctly. It's only `pv`.
''',
    answer=dict(
        culprit="python/calcstats/finance.py::pv",
        mechanism="The `rate == 0` shortcut returns `payment` instead of `payment * n`.",
        fix="`return payment * n`.",
        grading="Python-only. Expected clean stop under current LYRA unless a Python profile exists. A good RCA compares with the sibling zero-rate branches in `pmt` and `fv`.",
    ),
    expected={"outcome": "stop", "reason": "unsupported_language_or_not_reproduced", "note": "Python-only bug (reachable from Rust via calc eval)"},
    edits=[("python/calcstats/finance.py", "    if rate == 0:\n        return payment * n\n    return payment * (1 -", "    if rate == 0:\n        return payment\n    return payment * (1 -")],
    hidden={"python/tests/test_hidden_07.py": r'''import unittest
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
'''},
    run="cd python && python3 -m unittest discover -s tests -p test_hidden_07.py",
)
