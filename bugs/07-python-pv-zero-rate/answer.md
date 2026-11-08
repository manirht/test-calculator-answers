# 07 pv() at a 0% rate returns a single payment

- language: python
- tier: L1   category: finance   kind: fix
- expected outcome: {"outcome": "stop", "reason": "unsupported_language_or_not_reproduced", "note": "Python-only bug (reachable from Rust via calc eval)"}
- culprit: `python/calcstats/finance.py::pv`

## Root cause

The `rate == 0` shortcut returns `payment` instead of `payment * n`.

## Reference fix

`return payment * n`.

## How to grade

Python-only. Expected clean stop under current LYRA unless a Python profile exists. A good RCA compares with the sibling zero-rate branches in `pmt` and `fv`.

## Hidden test

Files: `python/tests/test_hidden_07.py`

```sh
cd python && python3 -m unittest discover -s tests -p test_hidden_07.py
```
