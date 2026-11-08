use calc_eval::{Calculator, FormatOptions, NoBridge, RoundMode};

#[test]
fn e_is_correct_to_fourteen_places() {
    let mut calc = Calculator::new(Box::new(NoBridge));
    calc.options = FormatOptions::new(14, RoundMode::HalfUp).unwrap();
    assert_eq!(calc.eval_line("e").unwrap().text, "2.71828182845905");
}
