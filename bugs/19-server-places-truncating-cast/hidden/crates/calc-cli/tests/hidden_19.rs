use std::io::Write;
use std::process::{Command, Stdio};

#[test]
fn out_of_range_places_are_rejected_not_wrapped() {
    let mut child = Command::new(env!("CARGO_BIN_EXE_calc"))
        .arg("serve")
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .spawn()
        .unwrap();
    writeln!(child.stdin.as_mut().unwrap(), r#"{{"id":1,"expr":"1/3","places":4294967298}}"#).unwrap();
    let out = child.wait_with_output().unwrap();
    let reply: serde_json::Value = serde_json::from_slice(out.stdout.split(|b| *b == b'\n').next().unwrap()).unwrap();
    assert_eq!(reply["ok"], false, "{reply}");
    assert_eq!(reply["error"]["code"], "BAD_REQUEST");
}
