BUG = dict(
    id="17", slug="add-wraps-on-overflow", title="Adding to the largest integer gives a negative number",
    lang="rust", tier="L3", category="arithmetic", kind="fix",
    commit_message="perf: avoid a branch in Rational::add",
    issue=r'''
```
$ calc eval "170141183460469231731687303715884105727 + 2"
-170141183460469231731687303715884105726
```

I know there is a limit on how big numbers can get (multiplying two huge numbers reports `OVERFLOW`, which is fine), but this one
returns a *wrong number* instead of an error, which is much worse than failing. `... + 1` correctly reports `OVERFLOW`; adding
2 or more doesn't. Same for subtracting from the most negative number.
''',
    answer=dict(
        culprit="crates/calc-eval/src/number.rs::Rational::add",
        mechanism="The numerator sum uses `wrapping_add` instead of `checked_add`. Overflow wraps around into the negative range. `+ 1` still reports OVERFLOW only by accident: it wraps to `i128::MIN`, which `Rational::new` rejects.",
        fix="`a.checked_add(b).ok_or_else(overflow)?`.",
        grading="The accidental OVERFLOW for `+ 1` hides the bug from casual testing. RCA should explain it. Subtraction goes through `add`, so one fix covers both.",
        notes="The visible overflow test uses values that sum to exactly `i128::MAX + 1`, which wraps to MIN and is rejected by the constructor, so it still passes.",
    ),
    edits=[("crates/calc-eval/src/number.rs", "let n = a.checked_add(b).ok_or_else(overflow)?;", "let n = a.wrapping_add(b);")],
    hidden={"crates/calc-eval/tests/hidden_17.rs": r'''use calc_eval::{Calculator, ErrorCode, NoBridge};

#[test]
fn addition_past_the_limit_is_an_overflow_error() {
    let mut calc = Calculator::new(Box::new(NoBridge));
    let max = "170141183460469231731687303715884105727";
    for tail in ["+ 1", "+ 2", "+ 1000"] {
        let err = calc.eval_line(&format!("{max} {tail}")).unwrap_err();
        assert_eq!(err.code, ErrorCode::Overflow, "{tail}");
    }
    let err = calc.eval_line(&format!("-{max} - 2")).unwrap_err();
    assert_eq!(err.code, ErrorCode::Overflow);
}
'''},
    run="cargo test -p calc-eval --test hidden_17",
)
