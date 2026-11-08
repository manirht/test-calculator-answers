# sqrt(1/2) returns 1

```
$ calc eval "sqrt(1/2)"
1
$ calc eval "sqrt(4/3)"
2
```

I expected `0.7071067812` and `1.1547005384`. Whole numbers like `sqrt(2)` and `sqrt(16)` are fine, and so is `sqrt(9/4)` = `1.5`.
The wrong answers only seem to happen for fractions whose numerator is a perfect square, but whose denominator isn't (`1/2`,
`4/3`, `9/5`, ...).
