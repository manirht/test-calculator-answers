# 10 Variable names are not case-sensitive

- language: rust
- tier: L2   category: variables   kind: fix
- expected outcome: {"outcome": "fix"}
- culprit: `crates/calc-eval/src/env.rs::Env::{get,set}`

## Root cause

Variable names are lower-cased on the way in (`set`) and on lookup (`get`), collapsing names that differ only by case.

## Reference fix

Store and look up the name as given: `self.vars.insert(name.to_string(), value)` and `self.vars.get(name)`.

## How to grade

Both `get` and `set` must change; fixing only one leaves asymmetric behaviour. The reserved names (`pi`, `e`, `ans`) stay lower-case only.

## Hidden test

Files: `crates/calc-eval/tests/hidden_10.rs`

```sh
cargo test -p calc-eval --test hidden_10
```
