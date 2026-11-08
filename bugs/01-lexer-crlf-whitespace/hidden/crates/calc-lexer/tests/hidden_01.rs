use calc_lexer::{tokenize, TokenKind};

#[test]
fn line_breaks_are_whitespace() {
    let tokens = tokenize("1 +\r\n 2\n").expect("line breaks are whitespace");
    let kinds: Vec<TokenKind> = tokens.into_iter().map(|t| t.kind).collect();
    assert_eq!(
        kinds,
        vec![TokenKind::Number("1".into()), TokenKind::Plus, TokenKind::Number("2".into()), TokenKind::Eof]
    );
}
