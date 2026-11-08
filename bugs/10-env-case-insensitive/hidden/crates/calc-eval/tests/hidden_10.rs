use calc_eval::{Calculator, ErrorCode, NoBridge};

#[test]
fn variable_names_are_case_sensitive() {
    let mut calc = Calculator::new(Box::new(NoBridge));
    calc.eval_line("Rate = 5").unwrap();
    assert_eq!(calc.eval_line("Rate * 2").unwrap().exact, "10");
    assert_eq!(calc.eval_line("rate").unwrap_err().code, ErrorCode::UnknownVar);
    calc.eval_line("rate = 1").unwrap();
    assert_eq!(calc.eval_line("Rate").unwrap().exact, "5");
    assert_eq!(calc.eval_line("rate").unwrap().exact, "1");
}
