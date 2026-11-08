# 18 Whole numbers fail with OVERFLOW when many decimal places are requested

- language: rust
- tier: L3   category: formatting   kind: fix
- expected outcome: {"outcome": "fix"}
- culprit: `crates/calc-eval/src/number.rs::Rational::to_decimal`

## Root cause

`to_decimal` multiplies by `10^places` to round, even for integers. For 30 places the scaled value exceeds `i128`. The early return for integers (`if self.is_integer() { return Ok(self.num.to_string()) }`) was removed.

## Reference fix

Restore the integer shortcut at the top of `to_decimal`.

## How to grade

Fix must keep fractional behaviour unchanged (the non-integer overflow is a documented limitation). Test: `12345678901` at 30 places prints unchanged, negative integer too.

## Hidden test

Files: `crates/calc-eval/tests/hidden_18.rs`

```sh
cargo test -p calc-eval --test hidden_18
```
