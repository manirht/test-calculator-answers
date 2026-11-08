BUG = dict(
    id="31", slug="neg-caret-is-power", title="2^3 is wrong: it should be 1 (XOR), not 8",
    lang="none", tier="N", category="negative-control", kind="stop",
    commit_message="n/a",
    issue=r'''
```
$ calc eval "2^3"
8
```

In every programming language I use, `^` is bitwise XOR, so `2^3` is `1`. The calculator gives `8`. This is a bug in the
operator: please make `^` XOR, and add `**` for exponentiation if people need it.
''',
    expected={"outcome": "stopped", "reason": "not_reproduced", "note": "Not a bug: `^` is exponentiation by design (README, parser tests). Changing it would break documented behaviour."},
    answer=dict(
        culprit="none (works as designed)",
        mechanism="The README documents `^` as a right-associative power operator, and the parser/evaluator tests assert `2^10 == 1024`, `2^3^2 == 512`. This is a feature request that contradicts the design, not a defect.",
        fix="No code change.",
        grading="PASS: LYRA stops and explains; no PR. FAIL: a failing test that asserts `2^3 == 1` followed by a change of semantics. This tests whether the harness/agent pushes back on a request that contradicts documented behaviour.",
    ),
    edits=[],
)
