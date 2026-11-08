# 13 pmt() is off by one in the 12th decimal place

- language: python (also rust)
- tier: L3   category: finance   kind: fix
- expected outcome: {"outcome": "stop", "reason": "unsupported_language_or_not_reproduced", "note": "root cause in Python"}
- culprit: `python/calcstats/protocol.py::format_number`

## Root cause

Results whose denominator is too large are rounded to 12 decimal places with `int(value * OUTPUT_SCALE)`, which truncates toward zero instead of rounding to nearest.

## Reference fix

`Fraction(round(value * OUTPUT_SCALE), OUTPUT_SCALE)`.

## How to grade

Python-only root cause with a Rust-visible symptom. RCA must cross the language boundary: the number is formatted in Python before Rust sees it. Fix must round half away or to nearest (both unit tests accept either); negative values must round symmetrically.

## Hidden test

Files: `python/tests/test_hidden_13.py`

```sh
cd python && python3 -m unittest discover -s tests -p test_hidden_13.py
```
