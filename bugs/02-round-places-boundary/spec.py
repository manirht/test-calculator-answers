BUG = dict(
    id="02", slug="round-places-boundary", title="round(x, 20) is rejected even though the message says 0 to 20",
    lang="rust", tier="L1", category="builtins", kind="fix",
    commit_message="fix: tighten the places check in round()",
    issue=r'''
```
$ calc eval "round(1/3, 20)"
error[DOMAIN]: round places must be between 0 and 20
```

20 is between 0 and 20, so I would expect this to work. `round(1/3, 19)` is fine and `round(1/3, 21)` fails with the same
message, which makes sense. Only the boundary value is wrong.
''',
    answer=dict(
        culprit="crates/calc-eval/src/builtins.rs::call (\"round\" arm)",
        mechanism="The range check uses an exclusive upper bound, `(0..20).contains(&p)`, although the error message and intent are inclusive.",
        fix="Use `(0..=20)`.",
        grading="Off-by-one on a range. RCA must point at the range expression in the `round` arm. A test at exactly 20 places and one at 21 (still an error) is expected.",
    ),
    edits=[("crates/calc-eval/src/builtins.rs", "if !(0..=20).contains(&p) {", "if !(0..20).contains(&p) {")],
    hidden={"crates/calc-eval/tests/hidden_02.rs": r'''use calc_eval::{Calculator, NoBridge};

#[test]
fn round_accepts_twenty_places() {
    let mut calc = Calculator::new(Box::new(NoBridge));
    let result = calc.eval_line("round(1/3, 20)").expect("20 places is allowed");
    assert_eq!(result.exact, "33333333333333333333/100000000000000000000");
    assert!(calc.eval_line("round(1/3, 21)").is_err());
}
'''},
    run="cargo test -p calc-eval --test hidden_02",
)
