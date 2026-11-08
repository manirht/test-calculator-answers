use calc_eval::{Calculator, ErrorCode, NoBridge};

#[test]
fn exponents_beyond_i32_are_rejected() {
    let mut calc = Calculator::new(Box::new(NoBridge));
    for input in ["2^4294967296", "2^4294967297", "2^8589934593", "1^4294967297"] {
        let err = calc.eval_line(input).unwrap_err();
        assert_eq!(err.code, ErrorCode::Overflow, "{input}");
    }
    assert_eq!(calc.eval_line("2^10").unwrap().exact, "1024");
}
