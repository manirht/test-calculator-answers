use std::io::Write;
use std::process::{Command, Stdio};

#[test]
fn pvariance_is_available_and_listed() {
    let mut child = Command::new(env!("CARGO_BIN_EXE_calc"))
        .arg("serve")
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .spawn()
        .unwrap();
    {
        let stdin = child.stdin.as_mut().unwrap();
        writeln!(stdin, r#"{{"id":1,"expr":"pvariance(2,4,4,4,5,5,7,9)"}}"#).unwrap();
        writeln!(stdin, r#"{{"id":2,"cmd":"functions"}}"#).unwrap();
    }
    let out = child.wait_with_output().unwrap();
    let replies: Vec<serde_json::Value> =
        String::from_utf8_lossy(&out.stdout).lines().map(|l| serde_json::from_str(l).unwrap()).collect();
    assert_eq!(replies[0]["exact"], "4", "{}", replies[0]);
    assert!(replies[1]["functions"].as_array().unwrap().iter().any(|f| f == "pvariance"));
}
