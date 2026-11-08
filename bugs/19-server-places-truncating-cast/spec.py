BUG = dict(
    id="19", slug="server-places-truncating-cast", title="An enormous places value is accepted and treated as a small one",
    lang="rust", tier="L3", category="server-protocol", kind="fix",
    commit_message="refactor: simplify places conversion in the server",
    issue=r'''
The server is supposed to refuse more than 30 decimal places (`places must be at most 30`) and it does for 31, 100 and a
million. But some values slip through:

```
{"id": 1, "expr": "1/3", "places": 4294967298}
-> {"id": 1, "ok": true, "value": "0.33", ...}
```

`4294967298` is nowhere near 30 yet it is accepted and I get two decimal places. It looks like the number wraps around:
4294967298 is 2^32 + 2. I found this while fuzzing the protocol with large numbers, so it's an input validation problem
rather than something a real client would send.
''',
    answer=dict(
        culprit="crates/calc-cli/src/server.rs::options_for",
        mechanism="The request value is converted with `as u32`, which silently truncates a `u64` to its low 32 bits. `4294967298 as u32 == 2`. The original used `u32::try_from(p).ok()`, which rejects out-of-range values.",
        fix="`.and_then(|p| u32::try_from(p).ok())`.",
        grading="Validation bug in the protocol layer. The visible test with `places: -1` still passes because negative numbers are not `u64`. Expect an error reply with code BAD_REQUEST.",
    ),
    edits=[("crates/calc-cli/src/server.rs", ".and_then(|p| u32::try_from(p).ok())", ".map(|p| p as u32)")],
    hidden={"crates/calc-cli/tests/hidden_19.rs": r'''use std::io::Write;
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
'''},
    run="cargo test -p calc-cli --test hidden_19",
)
