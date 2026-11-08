use calc_eval::{Calculator, ErrorCode, NoBridge};

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
