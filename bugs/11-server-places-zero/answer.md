# 11 :places 0 has no effect in the REPL

- language: rust (also ts)
- tier: L3   category: server-protocol   kind: fix
- expected outcome: {"outcome": "fix"}
- culprit: `crates/calc-cli/src/server.rs::options_for`

## Root cause

`calc serve` ignores a `places` value of 0 in a request (it is filtered out as if it were absent) and falls back to the session default of 10 places. The TS REPL is correct: it sends `places: 0`, and the symptom looks like a front-end bug.

## Reference fix

Treat `"places": 0` like any other non-negative integer: remove the zero filter in `options_for`.

## How to grade

Root cause is in the Rust server, not TypeScript. A good RCA traces the request from the REPL (`places: 0` is sent) to the server and shows the reply. The repro belongs in `calc-cli` (send `{"expr":"10/4","places":0}` and expect `3`). Fixing the TS side to avoid sending 0 is a wrong fix.

## Hidden test

Files: `crates/calc-cli/tests/hidden_11.rs`

```sh
cargo test -p calc-cli --test hidden_11
```
