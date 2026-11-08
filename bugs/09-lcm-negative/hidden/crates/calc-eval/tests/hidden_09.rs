use calc_eval::{Calculator, NoBridge};

fn exact(input: &str) -> String {
    Calculator::new(Box::new(NoBridge)).eval_line(input).unwrap().exact
}

#[test]
fn lcm_is_never_negative() {
    assert_eq!(exact("lcm(-4, 6)"), "12");
    assert_eq!(exact("lcm(4, -6)"), "12");
    assert_eq!(exact("lcm(-4, -6)"), "12");
    assert_eq!(exact("lcm(0, -6)"), "0");
}
