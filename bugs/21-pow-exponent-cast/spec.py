BUG = dict(
    id="21", slug="pow-exponent-cast", title="2^4294967297 returns 2 instead of an overflow error",
    lang="rust", tier="L4", category="arithmetic", kind="fix",
    commit_message="perf: skip the checked conversion for exponents",
    issue=r'''
Huge exponents are supposed to be rejected: `2^99999999999` correctly says `error[OVERFLOW]`. But if I go a bit higher:

```
$ calc eval "2^4294967297"
2
$ calc eval "2^4294967296"
1
```

`2^4294967297` is certainly not 2 and `2^4294967296` is certainly not 1. These look like the exponent is wrapping around:
4294967296 is 2^32. I'd expect `error[OVERFLOW]: exponent is too large` for both, as for the smaller huge exponent.
''',
    answer=dict(
        culprit="crates/calc-eval/src/eval.rs::apply_binary (BinOp::Pow)",
        mechanism="The exponent is converted with `right.num() as i32`, which silently keeps only the low 32 bits. `4294967297 as i32 == 1`, `4294967296 as i32 == 0`. The original used `i32::try_from(...)` with an OVERFLOW error.",
        fix="`let exp = i32::try_from(right.num()).map_err(|_| EvalError::new(ErrorCode::Overflow, \"exponent is too large\"))?;`",
        grading="The visible `2^99999999999` test still passes (it truncates to a large positive i32 that overflows during multiplication), which is why only values near multiples of 2^32 misbehave. RCA should explain that.",
    ),
    edits=[("crates/calc-eval/src/eval.rs", "            let exp = i32::try_from(right.num())\n                .map_err(|_| EvalError::new(ErrorCode::Overflow, \"exponent is too large\"))?;\n", "            let exp = right.num() as i32;\n")],
    hidden={"crates/calc-eval/tests/hidden_21.rs": r'''use calc_eval::{Calculator, ErrorCode, NoBridge};

#[test]
fn exponents_beyond_i32_are_rejected() {
    let mut calc = Calculator::new(Box::new(NoBridge));
    for input in ["2^4294967296", "2^4294967297", "2^8589934593", "1^4294967297"] {
        let err = calc.eval_line(input).unwrap_err();
        assert_eq!(err.code, ErrorCode::Overflow, "{input}");
    }
    assert_eq!(calc.eval_line("2^10").unwrap().exact, "1024");
}
'''},
    run="cargo test -p calc-eval --test hidden_21",
)
