use calc_eval::{Calculator, NoBridge};

fn exact(input: &str) -> String {
    Calculator::new(Box::new(NoBridge)).eval_line(input).unwrap().exact
}

#[test]
fn modulo_binds_like_multiplication() {
    assert_eq!(exact("2 + 7 % 4"), "5");
    assert_eq!(exact("10 - 7 % 4"), "7");
    assert_eq!(exact("2 * 7 % 4"), "2");
    assert_eq!(exact("7 % 4 * 2"), "6");
}
