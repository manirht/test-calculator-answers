# 23 mode() loses exactness: mode(1/3, 1/3, 1/2) * 3 is not 1

- language: python (also rust)
- tier: L4   category: stats   kind: fix
- expected outcome: {"outcome": "stop", "reason": "unsupported_language_or_not_reproduced", "note": "root cause in Python"}
- culprit: `python/calcstats/stats.py::mode`

## Root cause

`Counter(values)` was changed to `Counter(float(v) for v in values)`. The tallied keys are floats, so the returned mode is the binary float nearest to the value, converted back to an inexact Fraction. Values that are equal as fractions but not as floats could also be merged or split incorrectly.

## Reference fix

`Counter(values)`: keep the Fractions.

## How to grade

Python-only root cause, visible through the Rust CLI (`exact` field is 999999999999/1000000000000 style). RCA should notice that the arithmetic everywhere else stays in Fractions.

## Hidden test

Files: `python/tests/test_hidden_23.py`

```sh
cd python && python3 -m unittest discover -s tests -p test_hidden_23.py
```
