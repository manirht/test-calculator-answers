BUG = dict(
    id="29", slug="registry-missing-function", title="pvariance() is reported as an unknown function",
    lang="rust", also=["python"], tier="L2", category="python-bridge", kind="fix",
    commit_message="refactor: tidy the list of external functions",
    issue=r'''
```
$ calc eval "pvariance(2,4,4,4,5,5,7,9)"
error[UNKNOWN_FUNC]: unknown function 'pvariance'
$ calc eval "variance(2,4,4,4,5,5,7,9)"
4.5714285714
$ calc eval "pstddev(2,4,4,4,5,5,7,9)"
2
```

The population variance function is in the Python package (I can call it directly) and the other statistics functions work
through `calc`. It's also missing from tab completion in `calc-ui`.
''',
    answer=dict(
        culprit="crates/calc-eval/src/bridge.rs::EXTERNAL_FUNCS",
        mechanism="`EXTERNAL_FUNCS` is the list of names the evaluator forwards to Python; `pvariance` was dropped from it. The evaluator then reports an unknown function without ever calling Python, and `calc serve`'s `functions` command (used for completion) omits it too.",
        fix="Add `\"pvariance\"` back to `EXTERNAL_FUNCS`.",
        grading="Registry drift between the Rust list and the Python `FUNCTIONS` table. A strong fix would also add a test that keeps the two lists in sync; accept either.",
    ),
    edits=[("crates/calc-eval/src/bridge.rs", '    "pvariance",\n', "")],
    hidden={"crates/calc-cli/tests/hidden_29.rs": r'''use std::io::Write;
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
'''},
    run="cargo test -p calc-cli --test hidden_29",
)
