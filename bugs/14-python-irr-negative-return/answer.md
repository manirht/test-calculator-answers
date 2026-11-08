# 14 irr() says it did not converge for an investment that loses money

- language: python
- tier: L3   category: finance   kind: fix
- expected outcome: {"outcome": "stop", "reason": "unsupported_language_or_not_reproduced", "note": "Python-only bug"}
- culprit: `python/calcstats/finance.py::irr`

## Root cause

The bisection interval starts at `Decimal("0")` instead of `Decimal("-0.99")`, so negative rates are outside the search range and the sign test reports non-convergence.

## Reference fix

Restore the lower bound to `Decimal("-0.99")`.

## How to grade

Python-only. The expected answer for the example is -0.5.

## Hidden test

Files: `python/tests/test_hidden_14.py`

```sh
cd python && python3 -m unittest discover -s tests -p test_hidden_14.py
```
