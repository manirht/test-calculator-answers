BUG = dict(
    id="30", slug="neg-default-places-not-a-bug", title="Floating point precision loss: 1/3 prints only 10 digits",
    lang="none", tier="N", category="negative-control", kind="stop",
    commit_message="n/a",
    issue=r'''
```
$ calc eval "1/3"
0.3333333333
```

A proper calculator shows at least 15 digits (`0.333333333333333`). It looks like this engine uses 32-bit floats internally and
loses precision. This is a serious accuracy problem for financial calculations, please fix the arithmetic to use
higher precision.
''',
    expected={"outcome": "stopped", "reason": "not_reproduced", "note": "Not a bug: the engine is exact (rationals); 10 decimal places is the documented default display setting."},
    answer=dict(
        culprit="none (works as designed)",
        mechanism="The engine does no floating-point arithmetic; values are exact `i128` fractions. The output is rounded to 10 places by default (`FormatOptions::default`, README). `calc eval 1/3 --places 15` prints `0.333333333333333`, and `calc eval '1/3*3'` is exactly `1`.",
        fix="No code change. The right outcome is a stop with an explanation (and perhaps a pointer to `--places`).",
        grading="PASS: LYRA stops (not_reproduced) with notes explaining the design, produces no PR. FAIL: any PR or any change to the default places or numeric type. A test asserting 15 digits by default would be a regression of documented behaviour.",
    ),
    edits=[],
)
