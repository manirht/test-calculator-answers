BUG = dict(
    id="01", slug="lexer-crlf-whitespace", title="Multi-line expressions fail with \"unexpected character\"",
    lang="rust", tier="L1", category="lexer", kind="fix",
    commit_message="refactor: simplify whitespace handling in the lexer",
    issue=r'''
I keep long formulas in shell scripts and wrap them over several lines so they stay readable:

```sh
calc eval "1000 *
  (1 + 0.05)"
```

This used to work. Now it fails:

```
error[SYNTAX]: unexpected character '
' at 6
```

The same thing happens with expressions copied out of a Windows text file (the line ends with a carriage return).
A line break should be treated like a space.
''',
    answer=dict(
        culprit="crates/calc-lexer/src/lib.rs::tokenize",
        mechanism="The whitespace arm of `tokenize` only skips space and tab. `\\n` and `\\r` fall through to the `UnexpectedChar` branch.",
        fix="Skip `\\n` and `\\r` as whitespace again: `b' ' | b'\\t' | b'\\n' | b'\\r' => { i += 1; continue; }`.",
        grading="RCA names `tokenize` / the whitespace match arm. Fix is one line. The regression test must tokenize an input containing `\\n` and/or `\\r\\n`. A fix that special-cases the CLI (trimming input) instead of the lexer is incomplete: `1 +\\n2` must lex.",
    ),
    edits=[("crates/calc-lexer/src/lib.rs", "b' ' | b'\\t' | b'\\n' | b'\\r' => {", "b' ' | b'\\t' => {")],
    hidden={"crates/calc-lexer/tests/hidden_01.rs": r'''use calc_lexer::{tokenize, TokenKind};

#[test]
fn line_breaks_are_whitespace() {
    let tokens = tokenize("1 +\r\n 2\n").expect("line breaks are whitespace");
    let kinds: Vec<TokenKind> = tokens.into_iter().map(|t| t.kind).collect();
    assert_eq!(
        kinds,
        vec![TokenKind::Number("1".into()), TokenKind::Plus, TokenKind::Number("2".into()), TokenKind::Eof]
    );
}
'''},
    run="cargo test -p calc-lexer --test hidden_01",
)
