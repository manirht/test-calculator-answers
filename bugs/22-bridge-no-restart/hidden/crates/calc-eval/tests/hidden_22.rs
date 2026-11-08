#![cfg(unix)]

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
