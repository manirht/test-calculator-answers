# 21 2^4294967297 returns 2 instead of an overflow error

- language: rust
- tier: L4   category: arithmetic   kind: fix
- expected outcome: {"outcome": "fix"}
- culprit: `crates/calc-eval/src/eval.rs::apply_binary (BinOp::Pow)`

## Root cause

The exponent is converted with `right.num() as i32`, which silently keeps only the low 32 bits. `4294967297 as i32 == 1`, `4294967296 as i32 == 0`. The original used `i32::try_from(...)` with an OVERFLOW error.

## Reference fix

`let exp = i32::try_from(right.num()).map_err(|_| EvalError::new(ErrorCode::Overflow, "exponent is too large"))?;`

## How to grade

The visible `2^99999999999` test still passes (it truncates to a large positive i32 that overflows during multiplication), which is why only values near multiples of 2^32 misbehave. RCA should explain that.

## Hidden test

Files: `crates/calc-eval/tests/hidden_21.rs`

```sh
cargo test -p calc-eval --test hidden_21
```
