use std::io::Write;
use std::process::{Command, Stdio};

#[test]
fn zero_places_in_a_request_is_honoured() {
    let mut child = Command::new(env!("CARGO_BIN_EXE_calc"))
        .arg("serve")
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .spawn()
        .unwrap();
    writeln!(child.stdin.as_mut().unwrap(), r#"{{"id":1,"expr":"10/4","places":0}}"#).unwrap();
    let out = child.wait_with_output().unwrap();
    let reply: serde_json::Value = serde_json::from_slice(out.stdout.split(|b| *b == b'\n').next().unwrap()).unwrap();
    assert_eq!(reply["value"], "3");
}
