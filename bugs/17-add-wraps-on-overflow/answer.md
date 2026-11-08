# 17 Adding to the largest integer gives a negative number

- language: rust
- tier: L3   category: arithmetic   kind: fix
- expected outcome: {"outcome": "fix"}
- culprit: `crates/calc-eval/src/number.rs::Rational::add`

## Root cause

The numerator sum uses `wrapping_add` instead of `checked_add`. Overflow wraps around into the negative range. `+ 1` still reports OVERFLOW only by accident: it wraps to `i128::MIN`, which `Rational::new` rejects.

## Reference fix

`a.checked_add(b).ok_or_else(overflow)?`.

## How to grade

The accidental OVERFLOW for `+ 1` hides the bug from casual testing. RCA should explain it. Subtraction goes through `add`, so one fix covers both.

## Notes

The visible overflow test uses values that sum to exactly `i128::MAX + 1`, which wraps to MIN and is rejected by the constructor, so it still passes.

## Hidden test

Files: `crates/calc-eval/tests/hidden_17.rs`

```sh
cargo test -p calc-eval --test hidden_17
```
