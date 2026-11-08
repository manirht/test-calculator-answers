# 03 The constant e is wrong after the 13th decimal place

- language: rust
- tier: L1   category: constants   kind: fix
- expected outcome: {"outcome": "fix"}
- culprit: `crates/calc-eval/src/env.rs::euler`

## Root cause

Two digits of the constant were transposed: `271_828_182_845_950` instead of `271_828_182_845_905`.

## Reference fix

Restore `Rational::new(271_828_182_845_905, 100_000_000_000_000)`.

## How to grade

Pure data bug; no logic to find. Good RCA cites the literal and compares it against the true digits of e. Test must check more than the default 10 places.

## Hidden test

Files: `crates/calc-eval/tests/hidden_03.rs`

```sh
cargo test -p calc-eval --test hidden_03
```
