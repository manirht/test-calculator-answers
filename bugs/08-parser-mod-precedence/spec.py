BUG = dict(
    id="08", slug="parser-mod-precedence", title="% has the wrong precedence: 2 + 7 % 4 gives 1",
    lang="rust", tier="L2", category="parser", kind="fix",
    commit_message="refactor: share binding powers between operators in the parser",
    issue=r'''
```
$ calc eval "2 + 7 % 4"
1
```

I expected `5`: modulo should bind like `*` and `/`, so this is `2 + (7 % 4)` = `2 + 3`. It looks like the addition happens first,
`(2 + 7) % 4` = `1`. `2 + 7 * 4` and `2 + 7 / 4` are both fine.

Parenthesised versions work, which is why I only noticed it in a longer formula.
''',
    answer=dict(
        culprit="crates/calc-parser/src/lib.rs::Parser::parse_expr_inner (infix table)",
        mechanism="`TokenKind::Percent` maps to `ADD_BP` instead of `MUL_BP`, so `%` is as loose as `+`/`-` and is parsed left to right with them.",
        fix="`TokenKind::Percent => (BinOp::Mod, MUL_BP)`.",
        grading="RCA should identify the binding-power table, not the evaluator: the tree shape is wrong before evaluation. Watch for a fix that reorders evaluation instead of fixing the parse.",
        notes="The visible suite stays green because its `%` tests are single-operator expressions and the Display round-trip test is self-consistent under either table.",
    ),
    edits=[("crates/calc-parser/src/lib.rs", "TokenKind::Percent => (BinOp::Mod, MUL_BP),", "TokenKind::Percent => (BinOp::Mod, ADD_BP),")],
    hidden={"crates/calc-eval/tests/hidden_08.rs": r'''use calc_eval::{Calculator, NoBridge};

fn exact(input: &str) -> String {
    Calculator::new(Box::new(NoBridge)).eval_line(input).unwrap().exact
}

#[test]
fn modulo_binds_like_multiplication() {
    assert_eq!(exact("2 + 7 % 4"), "5");
    assert_eq!(exact("10 - 7 % 4"), "7");
    assert_eq!(exact("2 * 7 % 4"), "2");
    assert_eq!(exact("7 % 4 * 2"), "6");
}
'''},
    run="cargo test -p calc-eval --test hidden_08",
)
