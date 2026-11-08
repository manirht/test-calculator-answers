BUG = dict(
    id="15", slug="sqrt-fraction-exact-check", title="sqrt(1/2) returns 1",
    lang="rust", tier="L3", category="builtins", kind="fix",
    commit_message="refactor: simplify the perfect-square check in sqrt",
    issue=r'''
```
$ calc eval "sqrt(1/2)"
1
$ calc eval "sqrt(4/3)"
2
```

I expected `0.7071067812` and `1.1547005384`. Whole numbers like `sqrt(2)` and `sqrt(16)` are fine, and so is `sqrt(9/4)` = `1.5`.
The wrong answers only seem to happen for fractions whose numerator is a perfect square, but whose denominator isn't (`1/2`,
`4/3`, `9/5`, ...).
''',
    answer=dict(
        culprit="crates/calc-eval/src/builtins.rs::sqrt",
        mechanism="The exact-root shortcut only checks that the numerator is a perfect square (`rn * rn == n`). The denominator check was dropped, so `1/2` is treated as exactly `isqrt(1)/isqrt(2)` = `1/1`.",
        fix="Require both: `rn * rn == n && rd * rd == d`.",
        grading="The approximate path is correct; the bug is the shortcut guard. A fix that removes the shortcut entirely would still pass hidden tests but would make `sqrt(9/4)` approximate; prefer keeping exact roots exact (the visible suite asserts `sqrt(9/4) == 3/2`).",
    ),
    edits=[("crates/calc-eval/src/builtins.rs", "if rn * rn == n && rd * rd == d {", "if rn * rn == n {")],
    hidden={"crates/calc-eval/tests/hidden_15.rs": r'''use calc_eval::{Calculator, FormatOptions, NoBridge, RoundMode};

#[test]
fn sqrt_of_a_fraction_with_a_square_numerator_only() {
    let mut calc = Calculator::new(Box::new(NoBridge));
    calc.options = FormatOptions::new(12, RoundMode::HalfUp).unwrap();
    assert_eq!(calc.eval_line("sqrt(1/2)").unwrap().text, "0.707106781186");
    assert_eq!(calc.eval_line("sqrt(4/3)").unwrap().text, "1.154700538379");
    assert_eq!(calc.eval_line("sqrt(9/4)").unwrap().exact, "3/2");
}
'''},
    run="cargo test -p calc-eval --test hidden_15",
)
