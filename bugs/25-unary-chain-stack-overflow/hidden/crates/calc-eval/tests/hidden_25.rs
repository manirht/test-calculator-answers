use calc_eval::{Calculator, ErrorCode, NoBridge};

#[test]
fn a_long_run_of_unary_minus_is_rejected_not_a_crash() {
    let mut calc = Calculator::new(Box::new(NoBridge));
    let input = format!("{}1", "-".repeat(200_000));
    assert_eq!(calc.eval_line(&input).unwrap_err().code, ErrorCode::TooDeep);
    assert_eq!(calc.eval_line("---1").unwrap().exact, "-1");
}
