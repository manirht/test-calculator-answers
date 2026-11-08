# 22 After the Python helper dies, every statistics call fails until calc is restarted

- language: rust (also python)
- tier: L4   category: python-bridge   kind: fix
- expected outcome: {"outcome": "fix"}
- culprit: `crates/calc-eval/src/bridge.rs::PythonBridge::call`

## Root cause

When a round trip fails, the dead `Session` must be dropped (`self.session = None`) so the next call spawns a new process. That reset was removed from the error arm; the broken session is reused and keeps failing.

## Reference fix

Restore `self.session = None;` before returning the error.

## How to grade

Hidden test uses a fake helper script that serves one request then exits: first call succeeds, second fails, third must succeed again. Also acceptable: retry once transparently on the second call, as long as the third works.

## Notes

The mismatched-id arm still resets the session, so only I/O failures are affected.

## Hidden test

Files: `crates/calc-eval/tests/hidden_22.rs`

```sh
cargo test -p calc-eval --test hidden_22
```
