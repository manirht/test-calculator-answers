# 25 calc crashes (SIGSEGV) on a very long run of minus signs

- language: rust
- tier: L6   category: parser   kind: fix
- expected outcome: {"outcome": "fix"}
- culprit: `crates/calc-parser/src/lib.rs::Parser::parse_expr_inner (prefix `-` branch)`

## Root cause

The prefix `-` branch recurses through `parse_expr_inner` directly, bypassing `parse_expr`, which is where the nesting depth is counted and limited. A long chain of unary minuses therefore recurses without bound and overflows the stack. The original called `self.parse_expr(PREFIX_BP)`.

## Reference fix

Call `self.parse_expr(PREFIX_BP)?` in the prefix branches (also `+`, which was left alone) so `MAX_DEPTH` applies.

## How to grade

Memory-safety-flavoured robustness bug. The repro is a test that crashes the test process rather than failing an assertion: a good agent should explain how it reproduced it (or write the test to assert on the parse result with an expectation of `TooDeep`, run in a thread with a large stack to observe the difference). A fix that only raises the thread stack size is wrong.

## Notes

The base suite deliberately has no unary-chain depth test.

## Hidden test

Files: `crates/calc-eval/tests/hidden_25.rs`

```sh
cargo test -p calc-eval --test hidden_25
```
