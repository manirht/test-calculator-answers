BUG = dict(
    id="13", slug="python-output-truncates", title="pmt() is off by one in the 12th decimal place",
    lang="python", also=["rust"], tier="L3", category="finance", kind="fix",
    commit_message="refactor: use integer conversion when bounding result precision",
    issue=r'''
```
$ calc eval "pmt(5/1200, 360, 200000)" --places 12
1073.643246024277
```

My reference calculator (arbitrary precision) says `1073.643246024278`. The difference is always in the last kept
digit and always downwards, never upwards: I compared a dozen results and the engine's number is never larger than the
reference. With the default 10 places you can't see it, you have to ask for 12.
''',
    answer=dict(
        culprit="python/calcstats/protocol.py::format_number",
        mechanism="Results whose denominator is too large are rounded to 12 decimal places with `int(value * OUTPUT_SCALE)`, which truncates toward zero instead of rounding to nearest.",
        fix="`Fraction(round(value * OUTPUT_SCALE), OUTPUT_SCALE)`.",
        grading="Python-only root cause with a Rust-visible symptom. RCA must cross the language boundary: the number is formatted in Python before Rust sees it. Fix must round half away or to nearest (both unit tests accept either); negative values must round symmetrically.",
    ),
    expected={"outcome": "stop", "reason": "unsupported_language_or_not_reproduced", "note": "root cause in Python"},
    edits=[("python/calcstats/protocol.py", "value = Fraction(round(value * OUTPUT_SCALE), OUTPUT_SCALE)", "value = Fraction(int(value * OUTPUT_SCALE), OUTPUT_SCALE)")],
    hidden={"python/tests/test_hidden_13.py": r'''import unittest
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
'''},
    run="cd python && python3 -m unittest discover -s tests -p test_hidden_13.py",
)
