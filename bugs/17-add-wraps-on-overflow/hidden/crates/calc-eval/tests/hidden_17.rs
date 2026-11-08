use calc_eval::{Calculator, ErrorCode, NoBridge};

#[test]
fn addition_past_the_limit_is_an_overflow_error() {
    let mut calc = Calculator::new(Box::new(NoBridge));
    let max = "170141183460469231731687303715884105727";
    for tail in ["+ 1", "+ 2", "+ 1000"] {
        let err = calc.eval_line(&format!("{max} {tail}")).unwrap_err();
        assert_eq!(err.code, ErrorCode::Overflow, "{tail}");
    }
    let err = calc.eval_line(&format!("-{max} - 2")).unwrap_err();
    assert_eq!(err.code, ErrorCode::Overflow);
}
