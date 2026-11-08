use std::io::Write;
use std::process::{Command, Stdio};

fn ask(requests: &[&str]) -> Vec<serde_json::Value> {
    let mut child = Command::new(env!("CARGO_BIN_EXE_calc"))
        .arg("serve")
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .spawn()
        .unwrap();
    for request in requests {
        writeln!(child.stdin.as_mut().unwrap(), "{request}").unwrap();
    }
    let out = child.wait_with_output().unwrap();
    String::from_utf8_lossy(&out.stdout).lines().map(|l| serde_json::from_str(l).unwrap()).collect()
}

#[test]
fn fractions_reach_python_exactly() {
    let replies = ask(&[
        r#"{"id":1,"expr":"mean(1/3, 1/3, 1/3)"}"#,
        r#"{"id":2,"expr":"mean(1/3, 1/3, 1/3) * 3"}"#,
        r#"{"id":3,"expr":"median(1/7, 2/7, 3/7)"}"#,
    ]);
    assert_eq!(replies[0]["exact"], "1/3", "{}", replies[0]);
    assert_eq!(replies[1]["exact"], "1");
    assert_eq!(replies[2]["exact"], "2/7");
}
