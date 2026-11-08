# 29 pvariance() is reported as an unknown function

- language: rust (also python)
- tier: L2   category: python-bridge   kind: fix
- expected outcome: {"outcome": "fix"}
- culprit: `crates/calc-eval/src/bridge.rs::EXTERNAL_FUNCS`

## Root cause

`EXTERNAL_FUNCS` is the list of names the evaluator forwards to Python; `pvariance` was dropped from it. The evaluator then reports an unknown function without ever calling Python, and `calc serve`'s `functions` command (used for completion) omits it too.

## Reference fix

Add `"pvariance"` back to `EXTERNAL_FUNCS`.

## How to grade

Registry drift between the Rust list and the Python `FUNCTIONS` table. A strong fix would also add a test that keeps the two lists in sync; accept either.

## Hidden test

Files: `crates/calc-cli/tests/hidden_29.rs`

```sh
cargo test -p calc-cli --test hidden_29
```
