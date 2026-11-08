# 19 An enormous places value is accepted and treated as a small one

- language: rust
- tier: L3   category: server-protocol   kind: fix
- expected outcome: {"outcome": "fix"}
- culprit: `crates/calc-cli/src/server.rs::options_for`

## Root cause

The request value is converted with `as u32`, which silently truncates a `u64` to its low 32 bits. `4294967298 as u32 == 2`. The original used `u32::try_from(p).ok()`, which rejects out-of-range values.

## Reference fix

`.and_then(|p| u32::try_from(p).ok())`.

## How to grade

Validation bug in the protocol layer. The visible test with `places: -1` still passes because negative numbers are not `u64`. Expect an error reply with code BAD_REQUEST.

## Hidden test

Files: `crates/calc-cli/tests/hidden_19.rs`

```sh
cargo test -p calc-cli --test hidden_19
```
