use calc_eval::{Calculator, NoBridge};

#[test]
fn round_accepts_twenty_places() {
    let mut calc = Calculator::new(Box::new(NoBridge));
    let result = calc.eval_line("round(1/3, 20)").expect("20 places is allowed");
    assert_eq!(result.exact, "33333333333333333333/100000000000000000000");
    assert!(calc.eval_line("round(1/3, 21)").is_err());
}
