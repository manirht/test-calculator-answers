# 20 pv(-1, 3, 100) kills the Python helper

- language: python (also rust)
- tier: L3   category: finance   kind: fix
- expected outcome: {"outcome": "stop", "reason": "unsupported_language_or_not_reproduced", "note": "root cause in Python"}
- culprit: `python/calcstats/finance.py::_check_rate`

## Root cause

The guard is `rate < -1` instead of `rate <= -1`. At exactly -1, `(1 + rate)` is 0 and `(1 + rate) ** -n` raises `ZeroDivisionError`, which `handle_request` does not catch (it only handles `CalcError`), so the helper process crashes. The Rust side reports it as EXTERNAL.

## Reference fix

`if rate <= -1:`. Optionally also catch `ZeroDivisionError` in `handle_request` and reply with a DOMAIN error.

## How to grade

The symptom is on the Rust side but the cause is in Python. A thorough fix also hardens `handle_request` so that no function can take the process down; accept either, prefer both.

## Notes

The visible rate-floor test uses -2, which is rejected under either comparison.

## Hidden test

Files: `python/tests/test_hidden_20.py`

```sh
cd python && python3 -m unittest discover -s tests -p test_hidden_20.py
```
