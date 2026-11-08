BUG = dict(
    id="03", slug="constant-e-digits", title="The constant e is wrong after the 13th decimal place",
    lang="rust", tier="L1", category="constants", kind="fix",
    commit_message="chore: update built-in constants",
    issue=r'''
```
$ calc eval e --places 14
2.7182818284595
```

Euler's number is 2.718281828459045..., so to 14 places I expect `2.71828182845905`. The first twelve digits are right and then
it drifts, which I only noticed because I compared against a reference.

(`pi` looks fine.)
''',
    answer=dict(
        culprit="crates/calc-eval/src/env.rs::euler",
        mechanism="Two digits of the constant were transposed: `271_828_182_845_950` instead of `271_828_182_845_905`.",
        fix="Restore `Rational::new(271_828_182_845_905, 100_000_000_000_000)`.",
        grading="Pure data bug; no logic to find. Good RCA cites the literal and compares it against the true digits of e. Test must check more than the default 10 places.",
    ),
    edits=[("crates/calc-eval/src/env.rs", "271_828_182_845_905", "271_828_182_845_950")],
    hidden={"crates/calc-eval/tests/hidden_03.rs": r'''use calc_eval::{Calculator, FormatOptions, NoBridge, RoundMode};

#[test]
fn e_is_correct_to_fourteen_places() {
    let mut calc = Calculator::new(Box::new(NoBridge));
    calc.options = FormatOptions::new(14, RoundMode::HalfUp).unwrap();
    assert_eq!(calc.eval_line("e").unwrap().text, "2.71828182845905");
}
'''},
    run="cargo test -p calc-eval --test hidden_03",
)
