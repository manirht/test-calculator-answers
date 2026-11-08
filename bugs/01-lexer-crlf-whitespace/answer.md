# 01 Multi-line expressions fail with "unexpected character"

- language: rust
- tier: L1   category: lexer   kind: fix
- expected outcome: {"outcome": "fix"}
- culprit: `crates/calc-lexer/src/lib.rs::tokenize`

## Root cause

The whitespace arm of `tokenize` only skips space and tab. `\n` and `\r` fall through to the `UnexpectedChar` branch.

## Reference fix

Skip `\n` and `\r` as whitespace again: `b' ' | b'\t' | b'\n' | b'\r' => { i += 1; continue; }`.

## How to grade

RCA names `tokenize` / the whitespace match arm. Fix is one line. The regression test must tokenize an input containing `\n` and/or `\r\n`. A fix that special-cases the CLI (trimming input) instead of the lexer is incomplete: `1 +\n2` must lex.

## Hidden test

Files: `crates/calc-lexer/tests/hidden_01.rs`

```sh
cargo test -p calc-lexer --test hidden_01
```
