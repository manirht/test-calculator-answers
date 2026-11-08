BUG = dict(
    id="10", slug="env-case-insensitive", title="Variable names are not case-sensitive",
    lang="rust", tier="L2", category="variables", kind="fix",
    commit_message="refactor: normalize variable names in Env",
    issue=r'''
The README says variable names are case-sensitive. They are not:

```
> Rate = 5
5
> rate * 2
10
> RATE = 7
7
> Rate
7
```

`rate`, `Rate` and `RATE` are all the same variable. I use `T` for time and `t` for temperature in the same session
and they overwrite each other. Expected: `rate` should be an unknown variable after only `Rate` was assigned.
''',
    answer=dict(
        culprit="crates/calc-eval/src/env.rs::Env::{get,set}",
        mechanism="Variable names are lower-cased on the way in (`set`) and on lookup (`get`), collapsing names that differ only by case.",
        fix="Store and look up the name as given: `self.vars.insert(name.to_string(), value)` and `self.vars.get(name)`.",
        grading="Both `get` and `set` must change; fixing only one leaves asymmetric behaviour. The reserved names (`pi`, `e`, `ans`) stay lower-case only.",
    ),
    edits=[
        ("crates/calc-eval/src/env.rs", "self.vars.get(name).copied()", "self.vars.get(&name.to_lowercase()).copied()"),
        ("crates/calc-eval/src/env.rs", "self.vars.insert(name.to_string(), value);", "self.vars.insert(name.to_lowercase(), value);"),
    ],
    hidden={"crates/calc-eval/tests/hidden_10.rs": r'''use calc_eval::{Calculator, ErrorCode, NoBridge};

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
'''},
    run="cargo test -p calc-eval --test hidden_10",
)
