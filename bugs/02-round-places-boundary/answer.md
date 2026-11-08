# 02 round(x, 20) is rejected even though the message says 0 to 20

- language: rust
- tier: L1   category: builtins   kind: fix
- expected outcome: {"outcome": "fix"}
- culprit: `crates/calc-eval/src/builtins.rs::call ("round" arm)`

## Root cause

The range check uses an exclusive upper bound, `(0..20).contains(&p)`, although the error message and intent are inclusive.

## Reference fix

Use `(0..=20)`.

## How to grade

Off-by-one on a range. RCA must point at the range expression in the `round` arm. A test at exactly 20 places and one at 21 (still an error) is expected.

## Hidden test

Files: `crates/calc-eval/tests/hidden_02.rs`

```sh
cargo test -p calc-eval --test hidden_02
```
