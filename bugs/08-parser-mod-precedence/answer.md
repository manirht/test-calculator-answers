# 08 % has the wrong precedence: 2 + 7 % 4 gives 1

- language: rust
- tier: L2   category: parser   kind: fix
- expected outcome: {"outcome": "fix"}
- culprit: `crates/calc-parser/src/lib.rs::Parser::parse_expr_inner (infix table)`

## Root cause

`TokenKind::Percent` maps to `ADD_BP` instead of `MUL_BP`, so `%` is as loose as `+`/`-` and is parsed left to right with them.

## Reference fix

`TokenKind::Percent => (BinOp::Mod, MUL_BP)`.

## How to grade

RCA should identify the binding-power table, not the evaluator: the tree shape is wrong before evaluation. Watch for a fix that reorders evaluation instead of fixing the parse.

## Notes

The visible suite stays green because its `%` tests are single-operator expressions and the Display round-trip test is self-consistent under either table.

## Hidden test

Files: `crates/calc-eval/tests/hidden_08.rs`

```sh
cargo test -p calc-eval --test hidden_08
```
