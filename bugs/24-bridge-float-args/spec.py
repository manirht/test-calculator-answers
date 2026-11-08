BUG = dict(
    id="24", slug="bridge-float-args", title="mean(1/3, 1/3, 1/3) is not exactly 1/3",
    lang="rust", also=["python"], tier="L5", category="python-bridge", kind="fix", suites=["rust", "python"],
    commit_message="refactor: send plain decimal numbers to the Python helper",
    issue=r'''
Arithmetic in this calculator is exact (`1/3 * 3` is exactly `1`) and the Python statistics are exact too, but once a
fraction goes through a statistics function it comes back slightly off:

```
$ calc eval "mean(1/3, 1/3, 1/3)" --places 15
0.333333333333
$ calc eval "mean(1/3, 1/3, 1/3) * 3" --places 15
0.999999999999
```

The mean of three identical values must be that value, and times 3 it must be exactly 1. With whole-number inputs
everything is fine, it's only when an argument is a fraction. The Python code itself looks exact when I call it directly
with `"1/3"` strings.
''',
    answer=dict(
        culprit="crates/calc-eval/src/bridge.rs::PythonBridge::call",
        mechanism="Arguments used to be sent as exact strings (`\"1/3\"`, via `Rational`'s Display). They are now converted to `f64` and printed (`0.3333333333333333`), which Python parses as the decimal 3333333333333333/10^16, not 1/3. Exactness is lost before Python sees the data.",
        fix="Send `a.to_string()` (the `n` or `n/d` form) as before.",
        grading="Cross-language: symptom in a Python function's result, cause in the Rust bridge. A fix on the Python side (e.g. rounding to 15 places) would hide it: the hidden test checks the *exact* fraction.",
        notes="The visible end-to-end tests use whole numbers and 5/1200 with a 10-place result, which survive the float round trip.",
    ),
    edits=[("crates/calc-eval/src/bridge.rs", "        let wire_args: Vec<String> = args.iter().map(|a| a.to_string()).collect();\n", "        let wire_args: Vec<String> = args\n            .iter()\n            .map(|a| (a.num() as f64 / a.den() as f64).to_string())\n            .collect();\n")],
    hidden={"crates/calc-cli/tests/hidden_24.rs": r'''use std::io::Write;
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
'''},
    run="cargo test -p calc-cli --test hidden_24",
)
