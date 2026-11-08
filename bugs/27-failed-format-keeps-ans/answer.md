# 27 A line that fails with OVERFLOW still replaces ans

- language: rust
- tier: L3   category: session-state   kind: fix
- expected outcome: {"outcome": "fix"}
- culprit: `crates/calc-eval/src/lib.rs::Calculator::eval_line_with`

## Root cause

`ans` is updated before the result is formatted. Formatting can fail (OVERFLOW at 30 places), and by then `ans` already holds the new value even though the caller received an error. The correct order is format first, then `set_ans`.

## Reference fix

Move `self.env.set_ans(value)` after `format::format_value(...)?`.

## How to grade

Ordering bug. The visible test only covers evaluation errors (`1/0`), where `ans` is never reached.

## Hidden test

Files: `crates/calc-eval/tests/hidden_27.rs`

```sh
cargo test -p calc-eval --test hidden_27
```
