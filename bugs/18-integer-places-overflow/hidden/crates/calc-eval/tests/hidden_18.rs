use calc_eval::{Calculator, FormatOptions, NoBridge, RoundMode};

#[test]
fn integers_are_printed_as_is_at_any_precision() {
    let mut calc = Calculator::new(Box::new(NoBridge));
    calc.options = FormatOptions::new(30, RoundMode::HalfUp).unwrap();
    assert_eq!(calc.eval_line("12345678901").unwrap().text, "12345678901");
    assert_eq!(calc.eval_line("-98765432109").unwrap().text, "-98765432109");
    assert_eq!(calc.eval_line("1/4").unwrap().text, "0.25");
}
