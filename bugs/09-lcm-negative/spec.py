BUG = dict(
    id="09", slug="lcm-negative", title="lcm() returns a negative number when an argument is negative",
    lang="rust", tier="L2", category="builtins", kind="fix",
    commit_message="refactor: use a method reference in lcm",
    issue=r'''
```
$ calc eval "lcm(-4, 6)"
-12
$ calc eval "lcm(4, -6)"
-12
$ calc eval "lcm(-4, -6)"
12
```

A least common multiple is never negative. `lcm(4, 6)` is `12` as it should be, and `gcd(-12, 18)` correctly gives `6`.
I would expect `12` in all three cases above.
''',
    answer=dict(
        culprit="crates/calc-eval/src/builtins.rs::call (\"lcm\" arm)",
        mechanism="`lcm` computes `(a / g) * b` and the sign of the product follows the inputs. The `.abs()` on the result was dropped.",
        fix="Map the product through `v.abs()`: `.map(|v| Rational::from_int(v.abs()))`.",
        grading="Fix must make all three sign combinations positive. A fix that only takes `abs` of the arguments is equivalent and acceptable.",
    ),
    edits=[("crates/calc-eval/src/builtins.rs", ".map(|v| Rational::from_int(v.abs()))", ".map(Rational::from_int)")],
    hidden={"crates/calc-eval/tests/hidden_09.rs": r'''use calc_eval::{Calculator, NoBridge};

fn exact(input: &str) -> String {
    Calculator::new(Box::new(NoBridge)).eval_line(input).unwrap().exact
}

#[test]
fn lcm_is_never_negative() {
    assert_eq!(exact("lcm(-4, 6)"), "12");
    assert_eq!(exact("lcm(4, -6)"), "12");
    assert_eq!(exact("lcm(-4, -6)"), "12");
    assert_eq!(exact("lcm(0, -6)"), "0");
}
'''},
    run="cargo test -p calc-eval --test hidden_09",
)
