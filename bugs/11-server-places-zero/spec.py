BUG = dict(
    id="11", slug="server-places-zero", title=":places 0 has no effect in the REPL",
    lang="rust", also=["ts"], tier="L3", category="server-protocol", kind="fix", suites=["rust", "ts"],
    commit_message="refactor: only apply places overrides that are set",
    issue=r'''
In the interactive session:

```
> :places 0
places = 0
> 10/4
2.5
```

I would expect `3` (half-up, zero decimal places). `:places 2` and `:places 5` work as expected, and the echoed
setting says `places = 0`, so the REPL believes it is set. Starting with `calc-ui --places 0` doesn't help either.
`calc eval "10/4" --places 0` on its own prints `3`, so the engine can do it.
''',
    answer=dict(
        culprit="crates/calc-cli/src/server.rs::options_for",
        mechanism="`calc serve` ignores a `places` value of 0 in a request (it is filtered out as if it were absent) and falls back to the session default of 10 places. The TS REPL is correct: it sends `places: 0`, and the symptom looks like a front-end bug.",
        fix="Treat `\"places\": 0` like any other non-negative integer: remove the zero filter in `options_for`.",
        grading="Root cause is in the Rust server, not TypeScript. A good RCA traces the request from the REPL (`places: 0` is sent) to the server and shows the reply. The repro belongs in `calc-cli` (send `{\"expr\":\"10/4\",\"places\":0}` and expect `3`). Fixing the TS side to avoid sending 0 is a wrong fix.",
    ),
    edits=[("crates/calc-cli/src/server.rs", '    if let Some(value) = request.get("places") {', '    if let Some(value) = request.get("places").filter(|v| v.as_u64() != Some(0)) {')],
    hidden={"crates/calc-cli/tests/hidden_11.rs": r'''use std::io::Write;
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
'''},
    run="cargo test -p calc-cli --test hidden_11",
)
