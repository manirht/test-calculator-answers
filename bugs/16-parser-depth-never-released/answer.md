# 16 A long sum fails with TOO_DEEP

- language: rust
- tier: L3   category: parser   kind: fix
- expected outcome: {"outcome": "fix"}
- culprit: `crates/calc-parser/src/lib.rs::Parser::parse_expr`

## Root cause

`parse_expr` increments `self.depth` on entry but the matching decrement on exit was removed. The counter measures the total number of sub-expressions parsed, not the current nesting, so any expression with more than `MAX_DEPTH` operands is rejected.

## Reference fix

Decrement after the inner call: `let result = self.parse_expr_inner(min_bp); self.depth -= 1; result`.

## How to grade

The error code is correct for the symptom (so it looks like the limit is just too low). A good RCA shows depth is never decremented rather than raising `MAX_DEPTH`. Raising the limit is a wrong fix: hidden tests also use a 5000-deep expression that must still be rejected.

## Hidden test

Files: `crates/calc-eval/tests/hidden_16.rs`

```sh
cargo test -p calc-eval --test hidden_16
```
