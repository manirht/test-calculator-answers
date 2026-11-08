# 24 mean(1/3, 1/3, 1/3) is not exactly 1/3

- language: rust (also python)
- tier: L5   category: python-bridge   kind: fix
- expected outcome: {"outcome": "fix"}
- culprit: `crates/calc-eval/src/bridge.rs::PythonBridge::call`

## Root cause

Arguments used to be sent as exact strings (`"1/3"`, via `Rational`'s Display). They are now converted to `f64` and printed (`0.3333333333333333`), which Python parses as the decimal 3333333333333333/10^16, not 1/3. Exactness is lost before Python sees the data.

## Reference fix

Send `a.to_string()` (the `n` or `n/d` form) as before.

## How to grade

Cross-language: symptom in a Python function's result, cause in the Rust bridge. A fix on the Python side (e.g. rounding to 15 places) would hide it: the hidden test checks the *exact* fraction.

## Notes

The visible end-to-end tests use whole numbers and 5/1200 with a 10-place result, which survive the float round trip.

## Hidden test

Files: `crates/calc-cli/tests/hidden_24.rs`

```sh
cargo test -p calc-cli --test hidden_24
```
