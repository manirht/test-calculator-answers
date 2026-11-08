BUG = dict(
    id="16", slug="parser-depth-never-released", title="A long sum fails with TOO_DEEP",
    lang="rust", tier="L3", category="parser", kind="fix",
    commit_message="refactor: return the inner parse result directly",
    issue=r'''
I generate formulas from a spreadsheet export. A sum with a couple of hundred terms fails:

```
$ calc eval "$(yes 1 | head -300 | paste -sd+ -)"
error[TOO_DEEP]: expression is nested too deeply
```

There is no nesting here at all, it's `1+1+1+...+1`. A 100 term sum works and so does any other long flat
expression up to a point, then it suddenly stops working. Deeply nested parentheses are *supposed* to be rejected, but this
isn't nested.
''',
    answer=dict(
        culprit="crates/calc-parser/src/lib.rs::Parser::parse_expr",
        mechanism="`parse_expr` increments `self.depth` on entry but the matching decrement on exit was removed. The counter measures the total number of sub-expressions parsed, not the current nesting, so any expression with more than `MAX_DEPTH` operands is rejected.",
        fix="Decrement after the inner call: `let result = self.parse_expr_inner(min_bp); self.depth -= 1; result`.",
        grading="The error code is correct for the symptom (so it looks like the limit is just too low). A good RCA shows depth is never decremented rather than raising `MAX_DEPTH`. Raising the limit is a wrong fix: hidden tests also use a 5000-deep expression that must still be rejected.",
    ),
    edits=[("crates/calc-parser/src/lib.rs", "        let result = self.parse_expr_inner(min_bp);\n        self.depth -= 1;\n        result\n", "        self.parse_expr_inner(min_bp)\n")],
    hidden={"crates/calc-eval/tests/hidden_16.rs": r'''use calc_eval::{Calculator, ErrorCode, NoBridge};

#[test]
fn flat_expressions_of_any_length_parse() {
    let mut calc = Calculator::new(Box::new(NoBridge));
    let sum = vec!["1"; 300].join("+");
    assert_eq!(calc.eval_line(&sum).unwrap().exact, "300");
    let product = vec!["1"; 500].join("*");
    assert_eq!(calc.eval_line(&product).unwrap().exact, "1");
}

#[test]
fn real_nesting_is_still_rejected() {
    let mut calc = Calculator::new(Box::new(NoBridge));
    let deep = format!("{}1{}", "(".repeat(5000), ")".repeat(5000));
    assert_eq!(calc.eval_line(&deep).unwrap_err().code, ErrorCode::TooDeep);
}
'''},
    run="cargo test -p calc-eval --test hidden_16",
)
