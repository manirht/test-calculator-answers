use calc_eval::{Calculator, FormatOptions, NoBridge, RoundMode};

#[test]
fn sqrt_of_a_fraction_with_a_square_numerator_only() {
    let mut calc = Calculator::new(Box::new(NoBridge));
    calc.options = FormatOptions::new(12, RoundMode::HalfUp).unwrap();
    assert_eq!(calc.eval_line("sqrt(1/2)").unwrap().text, "0.707106781186");
    assert_eq!(calc.eval_line("sqrt(4/3)").unwrap().text, "1.154700538379");
    assert_eq!(calc.eval_line("sqrt(9/4)").unwrap().exact, "3/2");
}
