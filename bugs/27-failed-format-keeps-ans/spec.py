BUG = dict(
    id="27", slug="failed-format-keeps-ans", title="A line that fails with OVERFLOW still replaces ans",
    lang="rust", tier="L3", category="session-state", kind="fix",
    commit_message="refactor: update ans as soon as a value is computed",
    issue=r'''
```
> :places 30
> 5
5
> 123456789012/7
error[OVERFLOW]: arithmetic overflow
> ans
17636684144.857142857142857142857142857
```

When a line fails, the previous result should stay in `ans` (that's what happens for `1/0`: `ans` is still `5` afterwards).
Here the line reports an error but `ans` has silently changed to the value of the failed line, which I never saw.
The error comes from printing with 30 places; the computation itself was fine.
''',
    answer=dict(
        culprit="crates/calc-eval/src/lib.rs::Calculator::eval_line_with",
        mechanism="`ans` is updated before the result is formatted. Formatting can fail (OVERFLOW at 30 places), and by then `ans` already holds the new value even though the caller received an error. The correct order is format first, then `set_ans`.",
        fix="Move `self.env.set_ans(value)` after `format::format_value(...)?`.",
        grading="Ordering bug. The visible test only covers evaluation errors (`1/0`), where `ans` is never reached.",
    ),
    edits=[("crates/calc-eval/src/lib.rs", "        let text = format::format_value(&value, &options)?;\n        self.env.set_ans(value);\n", "        self.env.set_ans(value);\n        let text = format::format_value(&value, &options)?;\n")],
    hidden={"crates/calc-eval/tests/hidden_27.rs": r'''use calc_eval::{Calculator, ErrorCode, FormatOptions, NoBridge, RoundMode};

#[test]
fn a_failed_line_leaves_ans_alone() {
    let mut calc = Calculator::new(Box::new(NoBridge));
    calc.options = FormatOptions::new(30, RoundMode::HalfUp).unwrap();
    assert_eq!(calc.eval_line("5").unwrap().exact, "5");
    let err = calc.eval_line("123456789012/7").unwrap_err();
    assert_eq!(err.code, ErrorCode::Overflow);
    assert_eq!(calc.eval_line("ans").unwrap().exact, "5");
}
'''},
    run="cargo test -p calc-eval --test hidden_27",
)
