# 15 sqrt(1/2) returns 1

- language: rust
- tier: L3   category: builtins   kind: fix
- expected outcome: {"outcome": "fix"}
- culprit: `crates/calc-eval/src/builtins.rs::sqrt`

## Root cause

The exact-root shortcut only checks that the numerator is a perfect square (`rn * rn == n`). The denominator check was dropped, so `1/2` is treated as exactly `isqrt(1)/isqrt(2)` = `1/1`.

## Reference fix

Require both: `rn * rn == n && rd * rd == d`.

## How to grade

The approximate path is correct; the bug is the shortcut guard. A fix that removes the shortcut entirely would still pass hidden tests but would make `sqrt(9/4)` approximate; prefer keeping exact roots exact (the visible suite asserts `sqrt(9/4) == 3/2`).

## Hidden test

Files: `crates/calc-eval/tests/hidden_15.rs`

```sh
cargo test -p calc-eval --test hidden_15
```
