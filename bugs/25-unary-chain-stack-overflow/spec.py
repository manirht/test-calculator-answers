BUG = dict(
    id="25", slug="unary-chain-stack-overflow", title="calc crashes (SIGSEGV) on a very long run of minus signs",
    lang="rust", tier="L6", category="parser", kind="fix",
    commit_message="perf: parse prefix operators without the depth bookkeeping",
    issue=r'''
Found while fuzzing the CLI with long inputs:

```
$ calc eval "$(printf -- '-%.0s' $(seq 1 200000))1"
Segmentation fault (core dumped)
```

Deeply nested parentheses are rejected cleanly (`error[TOO_DEEP]: expression is nested too deeply`), but the same amount of
nesting written as repeated unary minus takes the whole process down. In `calc serve` that kills the session, and anything
that feeds untrusted formulas to the server (a web form, a shared sheet) can crash it with one line.
''',
    answer=dict(
        culprit="crates/calc-parser/src/lib.rs::Parser::parse_expr_inner (prefix `-` branch)",
        mechanism="The prefix `-` branch recurses through `parse_expr_inner` directly, bypassing `parse_expr`, which is where the nesting depth is counted and limited. A long chain of unary minuses therefore recurses without bound and overflows the stack. The original called `self.parse_expr(PREFIX_BP)`.",
        fix="Call `self.parse_expr(PREFIX_BP)?` in the prefix branches (also `+`, which was left alone) so `MAX_DEPTH` applies.",
        grading="Memory-safety-flavoured robustness bug. The repro is a test that crashes the test process rather than failing an assertion: a good agent should explain how it reproduced it (or write the test to assert on the parse result with an expectation of `TooDeep`, run in a thread with a large stack to observe the difference). A fix that only raises the thread stack size is wrong.",
        notes="The base suite deliberately has no unary-chain depth test.",
    ),
    edits=[("crates/calc-parser/src/lib.rs", "            TokenKind::Minus => {\n                let inner = self.parse_expr(PREFIX_BP)?;\n", "            TokenKind::Minus => {\n                let inner = self.parse_expr_inner(PREFIX_BP)?;\n")],
    hidden={"crates/calc-eval/tests/hidden_25.rs": r'''use calc_eval::{Calculator, ErrorCode, NoBridge};

#[test]
fn a_long_run_of_unary_minus_is_rejected_not_a_crash() {
    let mut calc = Calculator::new(Box::new(NoBridge));
    let input = format!("{}1", "-".repeat(200_000));
    assert_eq!(calc.eval_line(&input).unwrap_err().code, ErrorCode::TooDeep);
    assert_eq!(calc.eval_line("---1").unwrap().exact, "-1");
}
'''},
    run="cargo test -p calc-eval --test hidden_25",
)
