BUG = dict(
    id="14", slug="python-irr-negative-return", title="irr() says it did not converge for an investment that loses money",
    lang="python", tier="L3", category="finance", kind="fix",
    commit_message="refactor: narrow the irr search interval",
    issue=r'''
```
$ calc eval "irr(-100, 50)"
error[DOMAIN]: irr did not converge
```

I put in 100 and got 50 back, so the return is -50% and there is a perfectly good answer. `irr(-100, 110)` gives `0.1`
as expected, and so do a few others with positive returns. It is only when the money comes back as less than was put in
that it gives up.
''',
    answer=dict(
        culprit="python/calcstats/finance.py::irr",
        mechanism="The bisection interval starts at `Decimal(\"0\")` instead of `Decimal(\"-0.99\")`, so negative rates are outside the search range and the sign test reports non-convergence.",
        fix="Restore the lower bound to `Decimal(\"-0.99\")`.",
        grading="Python-only. The expected answer for the example is -0.5.",
    ),
    expected={"outcome": "stop", "reason": "unsupported_language_or_not_reproduced", "note": "Python-only bug"},
    edits=[("python/calcstats/finance.py", 'low, high = Decimal("-0.99"), Decimal(10)', 'low, high = Decimal("0"), Decimal(10)')],
    hidden={"python/tests/test_hidden_14.py": r'''import unittest
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
'''},
    run="cd python && python3 -m unittest discover -s tests -p test_hidden_14.py",
)
