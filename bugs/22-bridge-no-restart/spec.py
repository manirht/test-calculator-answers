BUG = dict(
    id="22", slug="bridge-no-restart", title="After the Python helper dies, every statistics call fails until calc is restarted",
    lang="rust", also=["python"], tier="L4", category="python-bridge", kind="fix",
    commit_message="refactor: simplify error handling in PythonBridge::call",
    issue=r'''
In a long `calc serve` session the Python helper got killed (out-of-memory killer on my laptop). From then on:

```
> mean(1,2,3)
error[EXTERNAL]: write to python failed: Broken pipe (os error 32)
> mean(1,2,3)
error[EXTERNAL]: write to python failed: Broken pipe (os error 32)
```

and so on forever. Plain arithmetic keeps working. The first failure is understandable; the engine used to start a fresh
helper for the next call and everything carried on. Now only restarting the whole session helps.
''',
    answer=dict(
        culprit="crates/calc-eval/src/bridge.rs::PythonBridge::call",
        mechanism="When a round trip fails, the dead `Session` must be dropped (`self.session = None`) so the next call spawns a new process. That reset was removed from the error arm; the broken session is reused and keeps failing.",
        fix="Restore `self.session = None;` before returning the error.",
        grading="Hidden test uses a fake helper script that serves one request then exits: first call succeeds, second fails, third must succeed again. Also acceptable: retry once transparently on the second call, as long as the third works.",
        notes="The mismatched-id arm still resets the session, so only I/O failures are affected.",
    ),
    edits=[("crates/calc-eval/src/bridge.rs", "            Err(e) => {\n                self.session = None;\n                return Err(e);\n            }\n", "            Err(e) => return Err(e),\n")],
    hidden={"crates/calc-eval/tests/hidden_22.rs": r'''#![cfg(unix)]

use calc_eval::{Bridge, ErrorCode, PythonBridge, Rational};
use std::os::unix::fs::PermissionsExt;

const FAKE_HELPER: &str = r#"#!/bin/sh
reply() {
  id=$(printf '%s' "$1" | sed -e 's/.*"id":\([0-9]*\).*/\1/')
  printf '{"id":%s,"ok":true,"value":"7"}\n' "$id"
}
if [ ! -e "$HELPER_MARKER" ]; then
  touch "$HELPER_MARKER"
  read line
  reply "$line"
  exit 0
fi
while read line; do reply "$line"; done
"#;

#[test]
fn a_dead_helper_is_replaced_on_the_next_call() {
    let dir = std::env::temp_dir().join(format!("calc-hidden-22-{}", std::process::id()));
    std::fs::create_dir_all(&dir).unwrap();
    let script = dir.join("fake-python");
    std::fs::write(&script, FAKE_HELPER).unwrap();
    std::fs::set_permissions(&script, std::fs::Permissions::from_mode(0o755)).unwrap();
    std::env::set_var("CALC_PYTHON", &script);
    std::env::set_var("HELPER_MARKER", dir.join("started"));

    let mut bridge = PythonBridge::new();
    let one = [Rational::ONE];
    assert_eq!(bridge.call("mean", &one).unwrap().to_string(), "7");
    let err = bridge.call("mean", &one).expect_err("the helper exited after one request");
    assert_eq!(err.code, ErrorCode::External);
    assert_eq!(bridge.call("mean", &one).expect("a new helper is started").to_string(), "7");
    let _ = std::fs::remove_dir_all(&dir);
}
'''},
    run="cargo test -p calc-eval --test hidden_22",
)
