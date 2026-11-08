use calc_eval::{Calculator, ErrorCode, FormatOptions, NoBridge, RoundMode};

#[test]
fn a_failed_line_leaves_ans_alone() {
    let mut calc = Calculator::new(Box::new(NoBridge));
    calc.options = FormatOptions::new(30, RoundMode::HalfUp).unwrap();
    assert_eq!(calc.eval_line("5").unwrap().exact, "5");
    let err = calc.eval_line("123456789012/7").unwrap_err();
    assert_eq!(err.code, ErrorCode::Overflow);
    assert_eq!(calc.eval_line("ans").unwrap().exact, "5");
}
