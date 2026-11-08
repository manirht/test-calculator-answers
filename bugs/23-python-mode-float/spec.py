BUG = dict(
    id="23", slug="python-mode-float", title="mode() loses exactness: mode(1/3, 1/3, 1/2) * 3 is not 1",
    lang="python", also=["rust"], tier="L4", category="stats", kind="fix",
    commit_message="perf: count values as floats in mode",
    issue=r'''
Everything else in the statistics functions is exact (`mean(1/3, 1/3, 1/3) * 3` is exactly `1`), but `mode` isn't:

```
$ calc eval "mode(1/3, 1/3, 1/2)" --places 12
0.333333333333
$ calc eval "mode(1/3, 1/3, 1/2) * 3" --places 12
0.999999999999
```

I expected `0.333333333333` times 3 to be exactly 1 because the mode is the value `1/3`, not an approximation of it. For
whole numbers `mode` is fine, which is why it took me a while to notice.
''',
    answer=dict(
        culprit="python/calcstats/stats.py::mode",
        mechanism="`Counter(values)` was changed to `Counter(float(v) for v in values)`. The tallied keys are floats, so the returned mode is the binary float nearest to the value, converted back to an inexact Fraction. Values that are equal as fractions but not as floats could also be merged or split incorrectly.",
        fix="`Counter(values)`: keep the Fractions.",
        grading="Python-only root cause, visible through the Rust CLI (`exact` field is 999999999999/1000000000000 style). RCA should notice that the arithmetic everywhere else stays in Fractions.",
    ),
    expected={"outcome": "stop", "reason": "unsupported_language_or_not_reproduced", "note": "root cause in Python"},
    edits=[("python/calcstats/stats.py", "    counts = Counter(values)", "    counts = Counter(float(v) for v in values)")],
    hidden={"python/tests/test_hidden_23.py": r'''import unittest
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
'''},
    run="cd python && python3 -m unittest discover -s tests -p test_hidden_23.py",
)
