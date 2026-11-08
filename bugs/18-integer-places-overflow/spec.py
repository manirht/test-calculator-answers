BUG = dict(
    id="18", slug="integer-places-overflow", title="Whole numbers fail with OVERFLOW when many decimal places are requested",
    lang="rust", tier="L3", category="formatting", kind="fix",
    commit_message="refactor: remove special case for integers in to_decimal",
    issue=r'''
```
$ calc eval 12345678901 --places 10
12345678901
$ calc eval 12345678901 --places 30
error[OVERFLOW]: arithmetic overflow
```

It's an integer, so there is nothing to round and it should print as is however many places I ask for. I only noticed
because a script passes `--places 30` for everything. Fractions with more than a few integer digits and 30 places
overflow too, but that I can understand, a whole number is a different matter.
''',
    answer=dict(
        culprit="crates/calc-eval/src/number.rs::Rational::to_decimal",
        mechanism="`to_decimal` multiplies by `10^places` to round, even for integers. For 30 places the scaled value exceeds `i128`. The early return for integers (`if self.is_integer() { return Ok(self.num.to_string()) }`) was removed.",
        fix="Restore the integer shortcut at the top of `to_decimal`.",
        grading="Fix must keep fractional behaviour unchanged (the non-integer overflow is a documented limitation). Test: `12345678901` at 30 places prints unchanged, negative integer too.",
    ),
    edits=[("crates/calc-eval/src/number.rs", "        if self.is_integer() {\n            return Ok(self.num.to_string());\n        }\n", "")],
    hidden={"crates/calc-eval/tests/hidden_18.rs": r'''use calc_eval::{Calculator, FormatOptions, NoBridge, RoundMode};

#[test]
fn integers_are_printed_as_is_at_any_precision() {
    let mut calc = Calculator::new(Box::new(NoBridge));
    calc.options = FormatOptions::new(30, RoundMode::HalfUp).unwrap();
    assert_eq!(calc.eval_line("12345678901").unwrap().text, "12345678901");
    assert_eq!(calc.eval_line("-98765432109").unwrap().text, "-98765432109");
    assert_eq!(calc.eval_line("1/4").unwrap().text, "0.25");
}
'''},
    run="cargo test -p calc-eval --test hidden_18",
)
